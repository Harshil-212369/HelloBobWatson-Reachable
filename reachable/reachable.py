"""
reachable.py - CLI entry point for the Reachable liveness checker.

Usage:
    python reachable/reachable.py [--path <path>]

Exit codes:
    0  No liveness issues found (Tier 1 checks passed)
    1  NOT LIVE finding(s) detected
    2  Tool error (check raised an exception)

All output is ASCII-only (Windows PowerShell 5.1 constraint).
"""

import argparse
import subprocess
import sys
import os


def find_repo_root(start_path):
    """
    Walk up from start_path to find the git repo root.
    Returns the root path string, or None if not inside a git repo.
    """
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=start_path,
        capture_output=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.decode("ascii", errors="replace").strip()


def main():
    parser = argparse.ArgumentParser(
        description=(
            "reachable -- Liveness checker for developer changes.\n"
            "Answers: Does the running system actually contain the change I just made?"
        )
    )
    parser.add_argument(
        "--path", "-p",
        default=".",
        help="Path inside the repo to check (default: current directory)",
    )
    parser.add_argument(
        "--tier1-only",
        action="store_true",
        default=True,
        help="Run Tier 1 checks only (default; no model dependency)",
    )
    args = parser.parse_args()

    # Resolve path
    target = os.path.abspath(args.path)
    if not os.path.exists(target):
        sys.stderr.write("ERROR: path does not exist: {p}\n".format(p=target))
        sys.exit(2)

    # Find repo root
    repo_root = find_repo_root(target)
    if repo_root is None:
        sys.stderr.write(
            "ERROR: '{p}' is not inside a git repository.\n"
            "reachable requires a git repo to run Tier 1 checks.\n".format(p=target)
        )
        sys.exit(2)

    print("Reachable -- Tier 1 Liveness Check")
    print("Repo root : {r}".format(r=repo_root))
    print("Checking  : {t}".format(t=target))
    print("-" * 40)

    # Import checks (done here so import errors surface cleanly)
    try:
        # Support both: python reachable/reachable.py  AND  python -m reachable
        _here = os.path.dirname(os.path.abspath(__file__))
        _root = os.path.dirname(_here)
        if _root not in sys.path:
            sys.path.insert(0, _root)
        from reachable.checks.runner   import CheckRunner
        from reachable.checks.family_a import FAMILY_A_CHECKS
        from reachable.checks.family_b import FAMILY_B_CHECKS
        from reachable.checks.family_c import annotate_with_cost
    except ImportError as e:
        sys.stderr.write("ERROR: failed to import checks: {e}\n".format(e=e))
        sys.exit(2)

    runner = CheckRunner(repo_root)

    print("Running Family A (git liveness)...")
    for check in FAMILY_A_CHECKS:
        runner.run(check)

    print("Running Family B (registration liveness)...")
    for check in FAMILY_B_CHECKS:
        runner.run(check)

    # Family C: annotate NOT LIVE findings with economic cost data.
    # If annotation fails for any reason, A+B output is unchanged.
    try:
        print("Running Family C (economic liveness annotation)...")
        runner.findings = annotate_with_cost(runner.findings, repo_root)
    except Exception as exc:
        sys.stderr.write(
            "WARNING: Family C annotation failed: {e}\n".format(e=exc))

    print("")
    print(runner.report())

    # Exit code
    verdict = runner.worst_verdict()
    if verdict is None:
        sys.exit(0)

    from reachable.checks.runner import NOT_LIVE
    if verdict == NOT_LIVE:
        sys.exit(1)

    sys.exit(0)  # UNCONFIRMED is not a hard failure


if __name__ == "__main__":
    main()
