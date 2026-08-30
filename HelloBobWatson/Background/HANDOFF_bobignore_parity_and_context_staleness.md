# HANDOFF — `.bobignore` Parity Check + Context-Staleness Detection

**Status:** SCOPED-OUT FUTURE WORK (IBM TechXchange Dev Day Hackathon, Aug 2026)
**Parent project:** Liveness checker / artifact-runtime divergence detector
**Author:** Harshil Suthar
**Created:** 2026-08-29

---

## ⛔ INSTRUCTIONS FOR BOB — READ BEFORE ACTING ON ANYTHING BELOW

### PRIMARY GATE (blocking)

**Do not begin any work described in this document until you have explicitly asked me whether Tier 1, Tier 2, and Tier 3 of the liveness checker are complete — and I have confirmed all of them are.**

Ask the question directly. Do not infer completion from the repository state, from a passing test run, from a commit existing, or from this document being open. Those are artifact signals, not completion signals — which is the exact failure class this whole project exists to detect. Wait for my answer in the conversation.

If any tier is incomplete, stop and say so. Do not start this work "in parallel." Do not offer a partial version. The tiered build order is non-negotiable: guaranteed-demoable work finishes before stretch work begins.

### SECONDARY INSTRUCTION (verification, blocking on the code path)

**Verify this caveat before any code in this document is trusted or run:**

> The Python example below assumes `.bobignore` uses gitignore glob syntax, and therefore parses it with `pathspec`'s `gitwildmatch` matcher. **This assumption was never verified.** It was inferred from the fact that the IBM hackathon repository template ships `.gitignore` and `.bobignore` together for the same stated purpose (preventing credential exposure).

To verify:

1. Locate the official IBM Bob documentation on ignore files (`Configuration → Ignoring files`).
2. Confirm the pattern syntax `.bobignore` actually uses — glob/gitwildmatch, regex, literal paths, or something else.
3. Confirm whether `.bobignore` supports negation (`!pattern`), directory-only patterns (`trailing/`), and comments (`#`), since `gitwildmatch` supports all three and a mismatch produces silent wrong answers rather than errors.
4. Report what you find. **If the syntax differs, the parser must be replaced — do not adapt the patterns to fit the parser.**

A silent parser mismatch here would produce false-negative `secret_exposure_risk` results, which is worse than not running the check at all. Treat an unverified parser as a blocking defect, not a TODO.

### STANDING RULES FOR THIS WORK

- Every check must map to a **specific named incident** from the documented case set. If no incident backs a check, say so explicitly rather than presenting it as equally evidenced.
- No unfalsifiable metrics. If a number can't have its derivation explained, it does not go in.
- "I didn't measure that, here's what I'd measure" is the correct answer to an unknown. Guessing is not.

---

## ORIGINAL ANALYSIS (verbatim, unedited)

Correcting my own framing from last turn first: these aren't two separate ideas. They're two halves of one mechanism. Not re-reading unchanged files (the `.bobignore` point) is only safe *if* you also know when the cache goes stale (the context-consistency point). Skip the staleness check and you've recreated the exact bug your whole project is about — success signal ("I already read this file") mistaken for liveness signal ("this is still what the file says") — just inside Bob's own memory instead of the target system's runtime. That's a stronger novelty argument than "third failure surface," so use that framing in the write-up, not what I said last turn.

One gating question before I build anything: **is this going into Tier 1 as working code, or into the write-up as scoped-out future work?** Deadline is 10:00 AM ET tomorrow. Worth knowing before you spend hours on it.

Here's what's actually verified about Bob's mechanisms (searched just now, not from memory):

| Mechanism | Verified in Bob docs? | Fits which half |
|---|---|---|
| **Skill** | Yes — knowledge injection, not a runnable check | Neither. Wrong tool. |
| **Custom mode** | Yes — YAML, tool-permission restricted, per-workspace or global | The *prospective* mitigation: a read-only mode whose role definition says "check a file's mtime against your last read before acting on it." Soft guarantee — it's an instruction, not an introspection API. |
| **Hooks** (pre/post-tool-use, like Claude Code has) | **Not found.** I searched specifically and didn't turn up a Bob equivalent. Don't put this in a deliverable as fact. | N/A |
| **Git hook** (pre-commit) | Standard, not Bob-specific | The `.bobignore` parity check — free, reuses your existing Tier 1 pattern-matching logic |
| **CI** | Yes, explicitly — Bob's own site: *"With Bob Shell, I can... embed into your CI/CD pipeline across every stage of development."* | Same parity check, wrapped as a pipeline gate — and it directly name-checks "release and deployment workflows" from the challenge brief |

**Ship now, Tier 1, no new dependency** — extend your existing `git check-ignore` logic to also load `.bobignore` and diff the two:

```python
import pathspec
from pathlib import Path

def check_bobignore_parity(repo_root: str) -> dict:
    """Feeds findings into your existing verdict engine — doesn't emit
    NOT LIVE / UNCONFIRMED / LIVE on its own."""
    root = Path(repo_root)
    gitignore = _load(root / ".gitignore")
    bobignore = _load(root / ".bobignore")
    findings = {"secret_exposure_risk": [], "context_bloat_risk": []}

    for f in (str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()):
        git_ignored, bob_ignored = gitignore.match_file(f), bobignore.match_file(f)
        if git_ignored and not bob_ignored:
            findings["secret_exposure_risk"].append(f)  # Bob can read what git hides
        junk = ("node_modules/", "__pycache__/", "dist/", "build/", ".venv/")
        if any(m in f for m in junk) and not bob_ignored:
            findings["context_bloat_risk"].append(f)  # heuristic, not hard fail
    return findings

def _load(path: Path) -> pathspec.PathSpec:
    lines = path.read_text().splitlines() if path.exists() else []
    return pathspec.PathSpec.from_lines("gitwildmatch", lines)
```

Wire it as a **hook**: `.git/hooks/pre-commit` calling `python3 [FILL: your entrypoint] --check bobignore-parity --fail-on secret_exposure_risk`

Wire it as **CI**: one GitHub Actions step, same command, non-blocking on `context_bloat_risk`, blocking on `secret_exposure_risk`.

Caveat I haven't verified: I assumed `.bobignore` uses gitignore glob syntax because the hackathon template pairs the two files for the same purpose. Confirm that against the actual template before you trust `pathspec`'s `gitwildmatch` parser on it.

**Don't build yet — write-up only:** the actual context-staleness *detection* (cross-referencing Bob's last-read timestamp for a file against its mtime) depends entirely on whether the Bob session export logs per-file read times. Your own notes list finding that export format as still-open. If you haven't confirmed it has that field, this is exactly the kind of claim your own rules would tell you to cut. Draft language for the limitations section instead:

> *"We did not verify whether Bob's session export exposes per-file read timestamps. If it does, the same staleness check we apply to git working-tree state could extend to Bob's own context cache — flagging when Bob acts on a file it read before a subsequent edit. We scoped this out rather than assume the export format."*

That's the "here's what I'd measure" move, not a guess.

Last thing: your rule is every check maps to a named incident. Does one of your six actually involve Bob/ignore-file context bloat, or would this be a seventh, unpressure-tested one? If it's the latter, that's worth flagging in the write-up too rather than presenting it as equally evidenced.

---

## OPEN ITEMS CARRIED FORWARD

| # | Item | Blocking? | Owner |
|---|---|---|---|
| 1 | Confirm Tier 1 / Tier 2 / Tier 3 all complete — **by asking, not inferring** | Yes — gates everything | Harshil (answer) / Bob (ask) |
| 2 | Verify `.bobignore` pattern syntax vs. `gitwildmatch` | Yes — gates the code path | Bob |
| 3 | Confirm whether Bob session export contains per-file read timestamps | Yes — gates staleness detection entirely | Harshil |
| 4 | Determine whether an existing documented incident backs the ignore-file/context-bloat check, or whether it would be a new unpressure-tested case | No — but must be disclosed in write-up either way | Harshil |
| 5 | `[FILL]` — entrypoint path for the pre-commit hook invocation | No | Harshil |

## FRAMING TO REUSE

The one-sentence version, for the write-up and for any future pitch:

> A cached read is a success signal, not a liveness signal. The same divergence we detect between edited artifact and running system also occurs between what an agent read and what the file currently says.
