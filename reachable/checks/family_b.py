"""
family_b.py - Check Family B: Registration Liveness (DETERMINISTIC given schema).

Checks:
  B1 - Missing or malformed YAML frontmatter in skill/agent files
  B2 - File placed in a directory the runtime does not scan
  B3 - Load-bearing file is gitignored (shared with A5; surfaces in Family B
       report context as a registration failure, not just a git failure)

All output ASCII-only (Windows PowerShell 5.1 constraint).
"""

import os
import subprocess

from reachable.checks.runner import Finding, NOT_LIVE, UNCONFIRMED

# ---------------------------------------------------------------------------
# Known scanner conventions: maps framework name -> (expected_dir, alt_dirs)
# A file in alt_dirs but NOT in expected_dir triggers B2.
# ---------------------------------------------------------------------------
SCANNER_CONVENTIONS = [
    # Claude Code / Bob: scans skills/ at repo root
    {
        "framework": "Claude/Bob skill",
        "expected_dirs": ["skills"],
        "shadow_dirs": [".claude/skills", ".bob/skills", "skill"],
        "file_patterns": [".md", ".yaml", ".yml"],
    },
    # Generic agent manifest: looks for agents/ or agent/
    {
        "framework": "generic agent",
        "expected_dirs": ["agents", "agent"],
        "shadow_dirs": [".agents", "src/agents"],
        "file_patterns": [".yaml", ".yml", ".json"],
    },
]


def _has_yaml_frontmatter(filepath):
    """
    Return True if the file starts with a valid YAML frontmatter block (---).
    Returns False if absent or malformed.
    """
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            first_line = f.readline().rstrip()
            if first_line != "---":
                return False
            # Scan for closing ---
            for line in f:
                if line.rstrip() == "---":
                    return True
            return False  # Opening --- found but no closing ---
    except (IOError, OSError):
        return False


# Directories that are considered skill/agent registries
SKILL_DIRS = {"skills", ".bob/skills", ".claude/skills", "agents", "agent"}

def _is_skill_file(path):
    """
    Return True only if the file is inside a known skill/agent directory.
    Avoids false-positives on docs files that happen to mention 'skills'.
    """
    lower = path.replace("\\", "/").lower()
    return (
        any(lower.startswith(d + "/") or ("/" + d + "/") in lower
            for d in SKILL_DIRS)
        and any(lower.endswith(ext) for ext in [".md", ".yaml", ".yml"])
    )


def _git_check_ignore(repo_root, rel_path):
    """Return True if the file is gitignored."""
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", rel_path],
        cwd=repo_root,
        capture_output=True,
    )
    return result.returncode == 0


# ---------------------------------------------------------------------------
# B1 - Missing or malformed YAML frontmatter
# Incident 3: skills committed to correct directory but never indexed because
# the YAML frontmatter block was absent. The installer exited 0.
# ---------------------------------------------------------------------------
def check_b1_missing_frontmatter(repo_root):
    findings = []
    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for fname in filenames:
            if not fname.endswith((".md", ".yaml", ".yml")):
                continue
            full = os.path.join(dirpath, fname)
            rel  = os.path.relpath(full, repo_root)
            if not _is_skill_file(rel):
                continue
            if not _has_yaml_frontmatter(full):
                findings.append(Finding(
                    check_id="B1",
                    verdict=NOT_LIVE,
                    subject=rel,
                    evidence=(
                        "Skill/agent file has no valid YAML frontmatter block. "
                        "Runtime will not index it; installer may still exit 0."
                    ),
                    remediation=(
                        "Add a frontmatter block at the top of the file:\n"
                        "  ---\n"
                        "  name: <skill-name>\n"
                        "  description: <when to use this skill>\n"
                        "  ---"
                    ),
                ))
    return findings


# ---------------------------------------------------------------------------
# B2 - File in wrong directory (shadow directory)
# Incident 2: skill placed in .claude/skills/ but runtime scans skills/ only.
# ---------------------------------------------------------------------------
def check_b2_wrong_directory(repo_root):
    findings = []
    for convention in SCANNER_CONVENTIONS:
        expected = convention["expected_dirs"]
        shadow   = convention["shadow_dirs"]
        patterns = convention["file_patterns"]
        framework = convention["framework"]

        # Collect files in shadow dirs
        for dirpath, dirnames, filenames in os.walk(repo_root):
            dirnames[:] = [
                d for d in dirnames
                if d not in _B_SKIP_DIRS
                and not _dir_is_gitignored(repo_root, dirpath, d)
            ]
            rel_dir = os.path.relpath(dirpath, repo_root).replace("\\", "/")

            # Is this path inside a shadow dir?
            in_shadow = any(
                rel_dir == s or rel_dir.startswith(s + "/")
                for s in shadow
            )
            if not in_shadow:
                continue

            for fname in filenames:
                if not any(fname.endswith(p) for p in patterns):
                    continue
                rel_file = os.path.relpath(
                    os.path.join(dirpath, fname), repo_root
                ).replace("\\", "/")
                findings.append(Finding(
                    check_id="B2",
                    verdict=NOT_LIVE,
                    subject=rel_file,
                    evidence=(
                        "File is in '{shadow}' but {fw} scans '{expected}'. "
                        "The runtime will never see this file.".format(
                            shadow=rel_dir,
                            fw=framework,
                            expected="' or '".join(expected),
                        )
                    ),
                    remediation=(
                        "Move the file to one of: {dirs}".format(
                            dirs=", ".join(expected))
                    ),
                ))
    return findings


# ---------------------------------------------------------------------------
# Public: list of all Family B checks in run order
# ---------------------------------------------------------------------------
FAMILY_B_CHECKS = [
    check_b1_missing_frontmatter,
    check_b2_wrong_directory,
]
