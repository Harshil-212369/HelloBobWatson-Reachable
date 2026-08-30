"""
runner.py - Finding data structure and check runner.
All output is ASCII-only (Windows PowerShell 5.1 constraint).
"""

# Verdict constants
NOT_LIVE    = "NOT LIVE"
UNCONFIRMED = "UNCONFIRMED"
LIVE        = "LIVE"

# Verdict rank: highest rank wins when aggregating
VERDICT_RANK = {NOT_LIVE: 2, UNCONFIRMED: 1, LIVE: 0}


class Finding:
    """One liveness problem found by a check."""

    def __init__(self, check_id, verdict, subject, evidence, remediation):
        """
        check_id    - string, e.g. "A2"
        verdict     - NOT_LIVE or UNCONFIRMED (LIVE never emitted by Tier 1)
        subject     - the file or path this finding is about
        evidence    - one-line description of what was observed
        remediation - exact command or action for the developer to run
        """
        self.check_id    = check_id
        self.verdict     = verdict
        self.subject     = subject
        self.evidence    = evidence
        self.remediation = remediation

    def render(self):
        """Return ASCII text block for this finding."""
        lines = [
            "[{v}] {s}  (check {c})".format(
                v=self.verdict, s=self.subject, c=self.check_id),
            "  Evidence:    {e}".format(e=self.evidence),
            "  Fix:         {r}".format(r=self.remediation),
        ]
        return "\n".join(lines)


class CheckRunner:
    """Runs a list of check functions and aggregates findings."""

    def __init__(self, repo_root):
        self.repo_root = repo_root
        self.findings  = []

    def run(self, check_fn):
        """
        Call check_fn(repo_root) -> list[Finding] | None.
        Appends any findings returned.
        """
        try:
            result = check_fn(self.repo_root)
            if result:
                self.findings.extend(result)
        except Exception as exc:
            # Surface tool errors as UNCONFIRMED rather than crashing
            self.findings.append(Finding(
                check_id="TOOL",
                verdict=UNCONFIRMED,
                subject="(internal)",
                evidence="Check raised an exception: {e}".format(e=str(exc)),
                remediation="Run reachable again; if this persists, file a bug",
            ))

    def worst_verdict(self):
        if not self.findings:
            return None
        return max(self.findings, key=lambda f: VERDICT_RANK[f.verdict]).verdict

    def report(self):
        """Return the full ASCII text report."""
        if not self.findings:
            return "No liveness issues detected (Tier 1 checks passed)."

        lines = ["Reachable -- Tier 1 Liveness Report",
                 "=" * 40]
        for f in self.findings:
            lines.append("")
            lines.append(f.render())
        lines.append("")
        lines.append("=" * 40)
        lines.append(
            "Summary: {n} finding(s). Worst verdict: {v}".format(
                n=len(self.findings), v=self.worst_verdict())
        )
        return "\n".join(lines)
