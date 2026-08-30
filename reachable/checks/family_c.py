"""
family_c.py - Check Family C: Economic Liveness (annotation layer).

This is NOT an independent scan. It annotates existing NOT LIVE findings
from Families A and B with the cost of agentic work that produced no
runtime effect.

Verify-First results (against actual Bob session exports):
  V1: YES  - Bob exports session records as .md files
  V2: NO   - Exports contain no per-action Bobcoin cost field
  V3: NO   - Exports contain no structured file-path-per-action data
  V4: NO   - No stable action identifier in exports
  V5: NO   - No usable proxy (token counts, duration) in exports

Decision rule (from handoff brief, section 3):
  V3 fails -> Family C emits UNCONFIRMED and stops.
  Never fabricate a cost figure the evidence does not support.

Family C therefore annotates every NOT LIVE finding with:
  cost: UNCONFIRMED (no per-action cost data in Bob session export)
        Check Bobalytics for aggregate session spend.

If Families A and B produce zero NOT LIVE findings, Family C adds nothing.
If Family C itself errors, Families A and B output is unchanged.

ASCII-only output. No network calls. No new verdicts. No auto-fix.
"""

import os

from reachable.checks.runner import Finding, NOT_LIVE, UNCONFIRMED

# Path where Bob session exports are expected (relative to repo root)
BOB_SESSIONS_DIR = os.path.join("HelloBobWatson", "docs", "bob-sessions")

# The annotation appended to every NOT LIVE finding's remediation block
COST_UNCONFIRMED_LINE = (
    "cost: UNCONFIRMED -- Bob session export contains no per-action cost data.\n"
    "      Bobcoin spend on this change cannot be attributed from available records.\n"
    "      Check Bobalytics for aggregate session spend."
)


def _find_session_exports(repo_root):
    """
    Return list of .md session export files found in the bob-sessions dir.
    Returns empty list (not an error) if the directory does not exist.
    """
    sessions_path = os.path.join(repo_root, BOB_SESSIONS_DIR)
    if not os.path.isdir(sessions_path):
        return []
    return [
        os.path.join(sessions_path, f)
        for f in os.listdir(sessions_path)
        if f.endswith(".md") and f != "README.md"
    ]


def annotate_with_cost(findings, repo_root):
    """
    Given a list of Finding objects (from Families A+B), annotate every
    NOT LIVE finding with a cost line.

    Returns the same list with remediation fields extended -- does not add
    new Finding objects, does not change verdicts.

    If this function raises, the caller must catch and leave findings unchanged.
    """
    not_live_findings = [f for f in findings if f.verdict == NOT_LIVE]
    if not not_live_findings:
        return findings  # Nothing to annotate

    session_files = _find_session_exports(repo_root)

    if not session_files:
        # No session exports found at all -- still annotate, but say so
        cost_line = (
            "cost: UNCONFIRMED -- No Bob session exports found in "
            "{d}".format(d=BOB_SESSIONS_DIR)
        )
    else:
        # Session files exist but V2/V3 failed -- standard UNCONFIRMED
        cost_line = COST_UNCONFIRMED_LINE

    # Annotate each NOT LIVE finding in-place
    for f in not_live_findings:
        f.remediation = f.remediation + "\n  " + cost_line

    return findings
