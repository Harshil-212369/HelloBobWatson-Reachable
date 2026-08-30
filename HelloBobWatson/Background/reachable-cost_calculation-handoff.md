# Handoff Brief — Reachable, Check Family C: Economic Liveness

**Project:** Reachable | **Team:** HelloBobWatson | **Track:** Debugging
**Purpose of this document:** hand to IBM Bob in **Plan Mode** before any implementation. Do not open Agent Mode until the Verify-First block below is resolved.

---

## 1. Existing context Bob must hold

Reachable is a CLI that answers one question per change: **does the running system actually contain this?**

Three verdicts:

| Verdict | Meaning |
|---|---|
| `NOT LIVE` | Proven divergence between artifact and runtime |
| `UNCONFIRMED` | Liveness cannot be established from available evidence — a first-class result, not an error |
| `LIVE` | Positive runtime probe (AI tier only) |

Existing check families:

- **Family A — git liveness.** Unpushed commits, CI branch mismatch, dirty tree, detached HEAD, gitignored files invisible to `git status`.
- **Family B — registration liveness.** Missing YAML frontmatter, wrong directory, absent index entry.
- **Tier 2** — Bob Document Understanding infers intended load paths from project prose; parallel subagents scan multiple framework conventions.

Standing constraints that Family C inherits:
- **The tool never auto-fixes.** It prints the exact command; the developer runs it.
- **ASCII-only output** (Windows PowerShell 5.1 target).
- **Zero configuration** on any git repository.
- One finding per line: what is wrong, where, why, exact fix.

---

## 2. The extension thesis

> Reachable already detects changes that never reached the runtime. Every one of those changes **cost Bobcoins to produce**. Family C attaches the price tag to the finding.

A `NOT LIVE` verdict is not only a correctness result. It is **spend that bought nothing** — agentic work billed at 1 Bobcoin = $0.50 that produced zero runtime effect.

**This is not a second product bolted on.** It is the same epistemic failure Reachable was built for, applied to a second signal:

| Domain | Signal that is trusted | What it does not observe |
|---|---|---|
| Correctness (Families A/B) | `git status` clean, exit 0, build passed | Whether the runtime loaded the change |
| Economics (Family C) | Bobcoin balance decremented | Whether the spend produced a live change |

Both are the same structural error: **a reported signal is treated as evidence about a thing it never measured.** Family C is the existing thesis carried one layer out.

---

## 3. Verify-First — resolve before writing code

Bob must confirm these against actual local artifacts. **Do not assume any of them.** If a source does not exist, Family C degrades to `UNCONFIRMED` and that is an acceptable, in-spec outcome.

| # | Question | How to check |
|---|---|---|
| V1 | Does BobShell emit a machine-readable session/audit record on disk? | Inspect the local Bob install; locate the audit or session artifact path |
| V2 | Does that record carry a **per-action Bobcoin cost**, or only an aggregate? | Read one real export end to end |
| V3 | Does each record carry file paths touched, so an action can be joined to a Reachable finding? | Same export |
| V4 | Is there a stable action identifier to key on? | Same export |
| V5 | If V2 is false, is there a usable proxy (action type, token counts, duration)? | Same export |

**Decision rule:** if V2 and V3 both hold, Family C reports attributed cost. If V3 holds but V2 does not, report **action counts, not dollars**. If V3 fails, Family C emits a single `UNCONFIRMED` line and stops. Never estimate a coin figure the evidence does not support — fabricating a number contradicts the entire premise of the project.

---

## 4. Specification — Check Family C

**New check: C1 — unattributed spend on non-live changes.**

```
Input:  set of NOT LIVE findings from Families A and B (file paths)
        + Bob session/audit records for the current working period
Join:   file path touched by a Bob action  ->  path in a NOT LIVE finding
Output: one line per matched finding
```

**Output line contract** (ASCII only, same shape as existing findings):

```
NOT LIVE  <path>  gitignored, invisible to git status
          cost: 3 Bob actions, 4.5 Bobcoins spent on a change the runtime never loaded
          fix: git add -f <path> && git commit -m "..." && git push
```

When cost data is unavailable:

```
NOT LIVE  <path>  gitignored, invisible to git status
          cost: UNCONFIRMED (no per-action cost in session record)
          fix: git add -f <path> && git commit -m "..." && git push
```

**Placement:** Family C is an **annotation layer on existing findings**, not an independent scan. It must not introduce a new verdict, a new command, or a new config file. If Family C fails entirely, Families A and B must still run and pass unchanged.

---

## 5. Out of scope — do not build

- No spend forecasting, no budget dashboard, no burn-rate model. Reachable reports observed facts about the current change, not projections.
- No new subcommands. Family C rides on `reachable`.
- No network calls, no telemetry upload.
- No auto-fix, in keeping with the existing constraint.

---

## 6. Framing rules for all written output

Judges are IBM. Every artifact — README, submission text, video narration, commit messages — follows these:

| Use | Do not use |
|---|---|
| "Attributes agentic spend to runtime outcomes" | "IBM's pricing is opaque" |
| "Surfaces spend that produced no live change" | "Bobcoins are unpredictable" |
| "Extends Bob's audit trail into cost attribution" | Any criticism of IBM metering |

The frame is **building on BobShell's self-documenting audit records**, which are an IBM capability. Family C makes that existing capability actionable. That is a compliment to the product, and it is also accurate.

---

## 7. Acceptance criteria

1. Families A and B produce byte-identical output when Family C is disabled or unavailable.
2. On a demo fixture with a gitignored skill file, output shows the correctness finding **and** the attributed cost line.
3. With the session record removed, the same fixture emits `cost: UNCONFIRMED` and exits with the same code.
4. Runtime for the full scan stays under five seconds.
5. Output remains ASCII-only under PowerShell 5.1.
6. The Plan Mode session for Family C is exported to `HelloBobWatson/docs/bob-sessions/` via the existing `bob-session-export` skill.

---

## 8. First instruction to Bob

> Enter Plan Mode. Read this brief. Before proposing an implementation, execute the Verify-First block in section 3 against the actual Bob installation and report findings V1 through V5 with the evidence you used. Propose no code until V1-V5 are answered.
