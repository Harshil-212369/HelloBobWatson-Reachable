"""
family_a.py - Check Family A: Git Liveness (DETERMINISTIC, no model).

Checks:
  A1 - Dirty working tree (git status --porcelain=v1)
  A2 - Unpushed commits / stale from upstream (with upstream guard)
  A3 - Detached HEAD
  A4 - Untracked load-bearing files
  A5 - Gitignored load-bearing files (DEMO LEAD)

All subprocess output decoded as ascii, errors='replace' to survive any
unexpected bytes on Windows PowerShell 5.1.
"""

import subprocess
import os

from reachable.checks.runner import Finding, NOT_LIVE, UNCONFIRMED

# Patterns that indicate a file is load-bearing (extend as needed)
LOAD_BEARING_PATTERNS = [
    ".md", ".yaml", ".yml", ".py", ".js", ".ts",
    ".json", ".toml", ".cfg", ".ini", ".env",
    "skill", "agent", "config", "schema", "manifest",
]

# Directories that are never load-bearing (generated / cached artifacts)
SKIP_DIRS = {
    "__pycache__", ".tox", ".eggs", "node_modules",
    ".venv", "venv", "env", "build", "dist", ".git",
}


def _git(args, cwd, check=False):
    """Run a git command; return (stdout, stderr, returncode)."""
    result = subprocess.run(
        ["git"] + args,
        cwd=cwd,
        capture_output=True,
    )
    stdout = result.stdout.decode("ascii", errors="replace").strip()
    stderr = result.stderr.decode("ascii", errors="replace").strip()
    return stdout, stderr, result.returncode


def _is_load_bearing(path):
    """Heuristic: does this path look like something a runtime would load?"""
    lower = path.lower()
    return any(pat in lower for pat in LOAD_BEARING_PATTERNS)


# ---------------------------------------------------------------------------
# A1 - Dirty working tree
# ---------------------------------------------------------------------------
def check_a1_dirty_tree(repo_root):
    stdout, _, rc = _git(["status", "--porcelain=v1"], cwd=repo_root)
    if rc != 0 or not stdout:
        return []
    lines = [l for l in stdout.splitlines() if l.strip()]
    if not lines:
        return []
    sample = lines[0].strip()
    return [Finding(
        check_id="A1",
        verdict=NOT_LIVE,
        subject="working tree",
        evidence="{n} uncommitted change(s). First: {s}".format(
            n=len(lines), s=sample),
        remediation="git add <files> && git commit -m '<message>'",
    )]


# ---------------------------------------------------------------------------
# A2 - Unpushed / stale from upstream (with upstream guard)
# ---------------------------------------------------------------------------
def check_a2_unpushed(repo_root):
    # Guard: probe for upstream first
    upstream_out, _, upstream_rc = _git(
        ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"],
        cwd=repo_root,
    )
    if upstream_rc != 0 or not upstream_out:
        return [Finding(
            check_id="A2",
            verdict=UNCONFIRMED,
            subject="upstream tracking",
            evidence="No upstream branch configured for current branch.",
            remediation=(
                "git branch --set-upstream-to=origin/<branch> <branch>  "
                "or  git push -u origin <branch>"
            ),
        )]

    stdout, _, rc = _git(
        ["rev-list", "--left-right", "--count",
         "@{upstream}...HEAD"],
        cwd=repo_root,
    )
    if rc != 0 or not stdout:
        return []

    parts = stdout.split()
    if len(parts) != 2:
        return []

    behind, ahead = parts[0], parts[1]

    findings = []
    if ahead != "0":
        findings.append(Finding(
            check_id="A2",
            verdict=NOT_LIVE,
            subject="unpushed commits",
            evidence="{n} local commit(s) not yet pushed to {u}".format(
                n=ahead, u=upstream_out),
            remediation="git push",
        ))
    if behind != "0":
        findings.append(Finding(
            check_id="A2",
            verdict=NOT_LIVE,
            subject="stale branch",
            evidence="Local branch is {n} commit(s) behind {u}".format(
                n=behind, u=upstream_out),
            remediation="git pull --rebase",
        ))
    return findings


# ---------------------------------------------------------------------------
# A3 - Detached HEAD
# ---------------------------------------------------------------------------
def check_a3_detached_head(repo_root):
    _, _, rc = _git(["symbolic-ref", "-q", "HEAD"], cwd=repo_root)
    if rc == 0:
        return []
    # Exit 1 means detached HEAD
    head_out, _, _ = _git(["rev-parse", "--short", "HEAD"], cwd=repo_root)
    return [Finding(
        check_id="A3",
        verdict=NOT_LIVE,
        subject="HEAD",
        evidence="Detached HEAD at {h}. Commits here will not update any branch.".format(
            h=head_out or "unknown"),
        remediation="git checkout <branch>  to reattach to a branch",
    )]


# ---------------------------------------------------------------------------
# A4 - Untracked load-bearing files
# ---------------------------------------------------------------------------
def check_a4_untracked(repo_root):
    stdout, _, rc = _git(
        ["ls-files", "--others", "--exclude-standard"],
        cwd=repo_root,
    )
    if rc != 0 or not stdout:
        return []
    findings = []
    for path in stdout.splitlines():
        path = path.strip()
        # Skip generated/cached artifact directories
        parts = path.replace("\\", "/").split("/")
        if any(p in SKIP_DIRS for p in parts):
            continue
        if path and _is_load_bearing(path):
            findings.append(Finding(
                check_id="A4",
                verdict=NOT_LIVE,
                subject=path,
                evidence="File is untracked -- not committed, will not travel with the repo.",
                remediation="git add {p} && git commit -m 'add {p}'".format(p=path),
            ))
    return findings


# ---------------------------------------------------------------------------
# A5 - Gitignored load-bearing file (DEMO LEAD)
#
# git status --porcelain is DEFINED to hide ignored files, so git status
# returning clean does not mean the file travels. This check is the one that
# catches what a naive implementation structurally cannot see.
# ---------------------------------------------------------------------------
def check_a5_gitignored(repo_root):
    """
    Walk the repo and call git check-ignore on every file that looks
    load-bearing. If git check-ignore exits 0 the file is ignored.
    Skips generated/cached artifact directories (e.g. __pycache__).
    """
    findings = []
    for dirpath, dirnames, filenames in os.walk(repo_root):
        # Skip .git and known artifact dirs
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            if not _is_load_bearing(fname):
                continue
            rel = os.path.relpath(os.path.join(dirpath, fname), repo_root)
            stdout, _, rc = _git(
                ["check-ignore", "-v", "--", rel],
                cwd=repo_root,
            )
            if rc == 0 and stdout:
                # File is ignored; stdout contains the matching rule
                findings.append(Finding(
                    check_id="A5",
                    verdict=NOT_LIVE,
                    subject=rel,
                    evidence=(
                        "File is gitignored and will never travel to origin. "
                        "Rule: {rule}".format(rule=stdout.split(":")[0])
                    ),
                    remediation=(
                        "Either remove the ignore rule for this file, "
                        "or use 'git add -f {p}' if intentional".format(p=rel)
                    ),
                ))
    return findings


# ---------------------------------------------------------------------------
# Public: list of all Family A checks in run order
# ---------------------------------------------------------------------------
FAMILY_A_CHECKS = [
    check_a1_dirty_tree,
    check_a2_unpushed,
    check_a3_detached_head,
    check_a4_untracked,
    check_a5_gitignored,
]
