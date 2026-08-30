# Hackathon Submission Plan — "Reachable" Liveness Checker
**Deadline:** 10:00 AM ET, August 30, 2026
**Team:** HelloBobWatson | Solo: Harshil Suthar
**Track:** Debugging / Local Developer Preflight
**Repo:** (to be created in Sub-Task 0)
**Python:** 3.12.10 confirmed on PATH (Windows, no WSL)
**Bob tenant:** `ibm-coding-challenge-uat` confirmed (enterprise plan)
**Bob export:** Found — JSON and Markdown both available

---

## Reference Documents (Bob reads these — NOT the original PDFs/TXTs)

| Guide | Path |
|---|---|
| Max Jesch Enablement Session | `HelloBobWatson/docs/GUIDE_MaxJesch_Enablement.md` |
| IBM YouTube — Agent Memory | `HelloBobWatson/docs/GUIDE_IBM_Youtube_AgentMemory.md` |
| IBM YouTube — Agent Skills | `HelloBobWatson/docs/GUIDE_IBM_Youtube_AgentSkills.md` |
| Hackathon Rules Summary | `HelloBobWatson/docs/GUIDE_HackathonRules_Summary.md` |
| Context injection (session start) | `HelloBobWatson/CONTEXT.md` |
| Bob session export skill | `HelloBobWatson/.bob/skills/bob-session-export.md` |
| Full project spec | `HelloBobWatson/Background/PROBLEM_HANDOFF.md` |

**PDFs and IBM_Youtube TXTs are in `.bobignore` — Bob reads the docs/ summaries above instead.**

---

## Top-Level Overview

**Goal:** Maximise judging score (out of 20) by 10:00 AM ET Aug 30 with 3 hours of active work
(12 hours wall-clock, 9 of which are sleep/inactive).

**Project:** *Reachable* — a CLI liveness checker that answers one question:
> "Does the running system actually contain the change I just made?"

Three verdicts only: `NOT LIVE` | `UNCONFIRMED` | `LIVE`

**Strategy:**
- Tier 1 = guaranteed demo (git + registration checks, no model, no cloud)
- Tier 2 = scoring differentiator (Bob Doc Understanding + parallel Subagents = required IBM features)
- Tier 3 = skip unless both Tier 1+2 are done and genuine time remains

**Scoring criteria (from Official Rules):**

| Criterion | Points | How we score it |
|---|---|---|
| Completeness & feasibility | 5 | Tier 1 working end-to-end, catches real incidents |
| Effectiveness & efficiency | 5 | Time-to-signal demo: existing toolchain returns green, tool returns NOT LIVE in <5s |
| Design & usability | 5 | Clean text output modelled on gitleaks/trufflehog, one line per finding |
| Creativity & innovation | 5 | Composition of three check families as ONE verdict; load-path inference from prose |

**Minimum score to make prizes:** 12.5 / 20

---

## CONFIRMED ANSWERS — baked into this plan

### Demo fixtures (Q1)
**Do NOT break your real repos.** Use these two IBM sample repos as fixture targets:
- `https://github.com/IBM/galaxium-travels`
- `https://github.com/Austinkkk3/Bob-Dev-Day-Halifax`

Strategy: clone both locally; create controlled git states to demonstrate specific incidents.
Specifically demonstrate these three incident types against cloned fixtures:
1. **Incident 5** — make local commits, do NOT push → `git log origin/main..HEAD` non-empty → `[NOT LIVE]`
2. **Incident 3** — add a skill file with no/malformed YAML frontmatter → registration check fires → `[NOT LIVE]`
3. **Incident 1 or 2** — add a file in the wrong directory (e.g., `.claude/skills/` vs `skills/`) → `[NOT LIVE]`

These three cover Families A and B and give the demo its three-scenario structure.

### Measurable impact metric (Q5/Q7 — confirmed correct framing)
**Do NOT use calendar time.** Use time-to-signal:
> "The existing toolchain (git status, build, lint) returns green on these three broken states.
> `reachable` returns NOT LIVE with reason and fix command in under N seconds."

Film this on camera. That is the 90-second demo the rules require.

### Auto-fix defence (Q6 — rehearse this answer)
If a judge asks "why not just move the file automatically?":
> "Every one of the six incidents was caused by a system silently doing something other than
> what the developer intended. A tool that silently moves files is the same failure with better
> intentions. `reachable` prints the exact command. The developer runs it."

This is a five-point answer. Costs nothing to build. Put it in the problem statement.

### UNCONFIRMED defence (Q5 — if judges attack stale-docs weakness)
If a judge asks "what if the docs are wrong?":
> "The tool has an explicit UNCONFIRMED verdict for exactly this case. If two docs disagree,
> if the stated load path references files that don't exist, or if no authoritative document
> names the load path — the tool says UNCONFIRMED with the reason, and tells you what to
> check manually. It never fabricates confidence it doesn't have."

This is what turns the LLM's fuzziness from a liability into the design.

---

## Bob Session Export Schedule

The Official Rules require: *"exported IBM Bob report of all relevant tasks/sessions."*
Export after **every session** where meaningful work is done. Use Markdown format.
Save to `HelloBobWatson/docs/bob-sessions/` with naming: `session-YYYY-MM-DD-HH-MM-<topic>.md`

**Minimum four exports:**
1. **This planning session** — export NOW before switching to Agent mode
2. **After Tier 1 build** — after Family A+B working end-to-end
3. **After writing problem + Bob usage statements**
4. **After Tier 2** (if completed)

---

## Sub-Tasks

---

### Sub-Task 0 — Git Repository Initialisation + .bobignore + .gitignore
**Status:** `[ ] pending`

**Intent:** Create a public GitHub repo. Rename the draft ignore files. All subsequent work commits here.

**Expected Outcomes:**
- Public GitHub repository `reachable` exists (or similar name)
- `.gitignore` and `.bobignore` committed at repo root (renamed from `_draft_*.txt` files)
- `README.md` committed
- No credentials in any committed file
- Initial commit pushed; repo is publicly accessible

**Todo List:**
1. In Agent mode: rename `_draft_gitignore.txt` → `.gitignore` and `_draft_bobignore.txt` → `.bobignore`
2. `git init` in workspace root
3. Create public GitHub repo (browser or `gh repo create reachable --public`)
4. `git remote add origin <url>`
5. `git add .` — review staged files, confirm no credentials present
6. `git commit -m "init: Reachable liveness checker scaffold"`
7. `git push -u origin main`
8. Verify repo is publicly accessible in browser

**CRITICAL:** Review every staged file before committing. IBM Cloud API keys in repo = immediate account suspension.

**Relevant Context:**
- `.bobignore` excludes: all PDFs, `IBM_Youtube/` TXTs, credentials, `__pycache__`, `.venv`, `.git/`
- `HANDOFF_bobignore_parity_and_context_staleness.md`: verify `.bobignore` uses gitignore glob syntax (assumed but not confirmed)

---

### Sub-Task 1 — Written Problem & Solution Statement
**Status:** `[ ] pending`

**Intent:** Write the 500-word judge-facing statement. No code required. High points-per-minute.

**Expected Outcomes:**
- ≤500 words, ready to paste into submission form
- Covers: specific problem, target users, interaction model, creativity, measurable impact

**Confirmed draft structure:**

**Para 1 — Hook (≈60 words):**
> Six times in eight weeks across three real repositories, the same failure: a success signal —
> file saved, installer exited 0, commit created, agent responded coherently — was taken as proof
> the change was running. In every case it was not. The artifact was correct. The runtime consumed
> a different one. No existing tool catches all six.

**Para 2 — What the gap is (≈80 words):**
> `git status` is clean. The build passes. The agent answers fluently. None of these observe
> the runtime. `git status` hides ignored files by definition. A skill installer can exit 0 and
> never index. CI can check out a different branch than the one you fixed. An agentic IDE can
> track a stale copy of your project. Success signals are not liveness signals. The distinction
> is structural, not a bug in any one tool.

**Para 3 — Solution (≈120 words):**
> `reachable` is a CLI that answers one question per change: *Does the running system actually
> contain this?* Three verdicts: NOT LIVE (proven divergence), UNCONFIRMED (cannot establish
> liveness with available evidence), LIVE (runtime probe, Tier 2 only). Tier 1 is fully
> deterministic — git and registration checks with no model dependency. Check Family A catches
> unpushed commits, CI branch mismatches, dirty trees, detached HEAD, and — the demo lead —
> files that are gitignored and therefore structurally invisible to `git status`. Check Family B
> catches missing YAML frontmatter, files in wrong directories, and absent index entries.
> Tier 2 adds IBM Bob Document Understanding to infer load paths from a project's own prose
> documentation, using parallel subagents to scan multiple frameworks simultaneously.

**Para 4 — Users + interaction (≈80 words):**
> Any developer who has ever said "but I saved the file" or "the commit is there." One command:
> `reachable` — zero config on any git repo. Output is one finding per line: what is wrong,
> where, why, and the exact command to fix it. The tool never fixes automatically. Every one of
> the six incidents was caused by a system silently doing something other than what was intended.
> A tool that silently mutates state is the same failure with better intentions.

**Para 5 — Measurable impact (≈60 words):**
> On three reconstructed incidents the existing toolchain reports success — `git status` clean,
> build passing, installer exit 0. `reachable` reports NOT LIVE with the reason and fix command
> in under five seconds. This is demonstrated live in the video. The metric is time-to-signal,
> not calendar time between commits.

**Relevant Context:**
- `PROBLEM_HANDOFF.md` sections 2, 9, 10 — incidents table, impact metric, novelty claim
- `ClaudeChat_Understanding the project.md` — verdict design rationale
- `Gemini speculations.pdf` distilled answer — UNCONFIRMED as the defence, not better prompting

---

### Sub-Task 2 — Written Bob Usage Statement
**Status:** `[ ] pending`

**Intent:** Satisfy deliverable 3 with named, specific Bob features. Vague answers lose points.

**Draft (fill in task session numbers after building):**

> IBM Bob 2.0 was central to designing and building every layer of Reachable.
>
> **Plan Mode** was used to design the three-verdict architecture (NOT LIVE / UNCONFIRMED / LIVE),
> determine which check families belong to deterministic scripts vs. AI inference, and sequence
> the Tier 1 build order before any code was written.
>
> **Agent Mode** was used to scaffold the full Tier 1 CLI (`reachable.py`), implement Check
> Families A and B (git liveness + registration liveness), create the test fixture repos
> demonstrating each incident, and validate the ASCII-only output constraint.
>
> **Document Understanding** (Tier 2) — Bob reads the target project's README, schema, and
> documentation to infer the intended load path, then compares it to what exists on disk.
> This is the only check that cannot be done with a schema validator, because the knowledge
> is in prose, not in a machine-readable spec.
>
> **Parallel Subagents** (Tier 2) — multiple subagents scan different framework documentation
> files simultaneously, allowing load-path inference across multiple conventions in a single run.
>
> **Custom Skill** — a `bob-session-export` skill was created to guide the per-session export
> workflow (required deliverable), encoding the export steps as reusable procedural memory.
>
> Bob session exports (Markdown) are in `HelloBobWatson/docs/bob-sessions/` in the repository.

**Fill in before submitting:**
- Task session IDs or export file names
- Actual Tier 2 status (remove paragraph if not completed)

---

### Sub-Task 3 — Tier 1 CLI Scaffold (Families A + B)
**Status:** `[ ] pending`

**Intent:** Build the demoable core. Deterministic. No model. No network. Must run on Windows Python 3.12 + PowerShell 5.1.

**Expected Outcomes:**
- `reachable/reachable.py` — CLI entry point, accepts `--path`
- `reachable/checks/family_a.py` — git liveness checks
- `reachable/checks/family_b.py` — registration liveness checks
- `reachable/checks/runner.py` — structured finding objects `{check_id, verdict, evidence, remediation}`
- Text report to stdout, ASCII-only
- Exit codes: `0` = no findings, `1` = NOT LIVE found, `2` = tool error
- Silence ≠ safety: clean run explicitly prints "No liveness issues detected (Tier 1 checks passed)"
- Never auto-fixes — prints exact command, developer runs it

**Check Family A — git liveness (all five, in order):**

| Check | Probe | Fires on | Incident |
|---|---|---|---|
| A1 | `git status --porcelain=v1` | Non-empty output | General dirty tree |
| A2 | `git rev-list --left-right --count @{u}...HEAD` | Either count non-zero (guard with upstream probe first) | Incidents 4, 5 |
| A3 | `git symbolic-ref -q HEAD` | Exit code 1 (detached HEAD) | General |
| A4 | `git ls-files --others --exclude-standard` | Path matches load-bearing pattern | General untracked |
| A5 | `git check-ignore -v -- <path>` | Exit 0 (prints matching rule) | Incident 1 — **DEMO LEAD** |

**Upstream guard for A2:**
```
git rev-parse --abbrev-ref --symbolic-full-name @{upstream} 2>$null
```
If this returns nothing/errors → emit "no upstream configured" finding instead of crashing.

**Check Family B — registration liveness:**

| Check | What it looks for | Incident |
|---|---|---|
| B1 | YAML frontmatter absent or malformed in skill files (`*.md`, `*.yaml`) | Incident 3 |
| B2 | File in wrong directory vs. what schema/config expects | Incident 2 |
| B3 | `git check-ignore` on load-bearing files | Incident 1 (shared with A5) |

**Demo fixture setup (cloned repos — do NOT touch real repos):**
```
# Clone demo targets
git clone https://github.com/IBM/galaxium-travels demo-fixtures/galaxium-travels
git clone https://github.com/Austinkkk3/Bob-Dev-Day-Halifax demo-fixtures/bob-dev-day-halifax
```

Then create controlled broken states in the clones:
- Fixture 1 (Incident 5): `cd demo-fixtures/galaxium-travels && git commit --allow-empty -m "fix: unpushed change"` → do NOT push
- Fixture 2 (Incident 3): Add a `skills/my-skill.md` with no YAML frontmatter block
- Fixture 3 (Incident 2): Add a skill to `.claude/skills/` when scanner expects `skills/`

Each fixture must produce `[NOT LIVE]` output when `reachable` runs against it.

**Build order (follow exactly, do not skip steps):**
1. Repo discovery (`git rev-parse --show-toplevel` — bail cleanly outside a repo)
2. Finding data structure `{check_id, verdict, evidence, remediation}`
3. Check runner (iterates checks, collects findings)
4. A1 — dirty tree
5. A2 — unpushed/stale (with upstream guard)
6. A3 — detached HEAD
7. A4 — untracked load-bearing files
8. A5 — gitignored load-bearing file ← validate against Fixture 1
9. B1 — missing YAML frontmatter ← validate against Fixture 2
10. B2 — wrong directory ← validate against Fixture 3
11. B3 — `git check-ignore` on load-bearing files
12. Verdict aggregation (worst verdict wins)
13. Text report + exit codes
14. Full end-to-end run on all three fixtures

**Relevant Context:**
- `PROBLEM_HANDOFF.md` sections 3, 6, 7, 11
- `ClaudeChat_Understanding the project.md` — five checks, upstream guard, fixtures-first rule
- Python 3.12.10, Windows, no WSL, ASCII-only output, subprocess to git

---

### Sub-Task 4 — Demo Fixtures Verification
**Status:** `[ ] pending` (part of Sub-Task 3, but tracked separately)

**Intent:** Before recording video, confirm each fixture produces the expected `[NOT LIVE]` output.

**Expected Outcomes:**
- `reachable --path demo-fixtures/galaxium-travels` → `[NOT LIVE] unpushed commits`
- `reachable --path demo-fixtures/bob-dev-day-halifax` → `[NOT LIVE] missing YAML frontmatter`
- A third fixture state → `[NOT LIVE]` for wrong directory or gitignored file
- Existing toolchain (`git status`, build passing) returns green on the same states

**This is the core of the video demo.** Film: existing toolchain → green → then `reachable` → NOT LIVE.

---

### Sub-Task 5 — Demo Video
**Status:** `[ ] pending`

**Intent:** Record the 90s–3min video. This is the first thing judges engage with.

**Expected Outcomes:**
- Publicly accessible URL (YouTube, Vimeo, or Google Drive)
- ≥90 seconds of working solution on screen
- Narrated throughout
- Shows Bob being used (show Bob panel briefly)

**Video structure (~2.5 minutes):**

| Timestamp | Content |
|---|---|
| 0:00–0:20 | Spoken: "Six times in 8 weeks, a success signal lied. The file was saved. The commit was there. The agent answered. But the running system never saw the change." |
| 0:20–0:45 | Show Fixture 1: `git status` → clean. Build → passes. But `git log origin/main..HEAD` shows unpushed commits. |
| 0:45–1:15 | `reachable` on Fixture 1 → `[NOT LIVE] 1 unpushed commit on main. Fix: git push origin main` |
| 1:15–1:45 | `reachable` on Fixture 2 → `[NOT LIVE] skills/my-skill.md: no YAML frontmatter, will not be indexed`. Then Fixture 3 → wrong directory catch. |
| 1:45–2:10 | (If Tier 2) Show Bob reading README, inferring load path, subagents in parallel |
| 2:10–2:30 | Show Bob panel — task session, Agent Mode, one-sentence "this was built with Bob" |
| 2:30–2:50 | Closing: "`reachable`. One command before you ship." |

**Screen recorder:** Win+G (Xbox Game Bar) or OBS Studio. Upload to YouTube (unlisted is fine — must be publicly accessible).

---

### Sub-Task 6 — Bob Session Exports
**Status:** `[ ] pending`

**Intent:** Required deliverable. Export after every session. Already confirmed: both JSON and Markdown available in the export dialog.

**Export cadence:**
1. **NOW** — export this planning session (Markdown) before switching to Agent mode
2. After Tier 1 build complete
3. After problem statement + Bob usage statement written
4. After Tier 2 (if done)

**Where to save:** `HelloBobWatson/docs/bob-sessions/session-YYYY-MM-DD-HH-MM-<topic>.md`
**Commit and push after each export.**

---

### Sub-Task 7 — Tier 2: Load-Path Inference via Bob Document Understanding
**Status:** `[ ] pending — only start after Tier 1 end-to-end + exports done`

**Intent:** The payoff feature. Uses Bob Agent Mode + Document Understanding + parallel Subagents.
Directly demonstrates all three required IBM Bob 2.0 features from the hackathon brief.

**Gate:** Ask explicitly whether Tier 1 is complete. Do not infer from repo state. Do not start in parallel.

**Expected Outcomes:**
- `reachable/checks/family_c.py` — load-path liveness
- Bob reads target repo's README/schema/docs
- Parallel subagents: one reads README, one maps directory tree
- Returns `LIVE` only if positive evidence found in runtime-observable docs
- Defaults to `UNCONFIRMED` with reason (one of the five UNCONFIRMED triggers from `PROBLEM_HANDOFF.md` section 5)
- Subagent reasoning behind `--verbose`; clean report by default

**UNCONFIRMED triggers (any one fires it):**
1. No authoritative document names the load path
2. Two+ docs disagree
3. Docs reference files that don't exist on disk (stale docs)
4. Runtime cannot be observed directly
5. Single unversioned source, no corroborating structure

**Relevant Context:**
- `PROBLEM_HANDOFF.md` sections 3C, 4, 5
- `Gemini speculations.pdf` — UNCONFIRMED as design, not weakness; stream reasoning in video/verbose

---

### Sub-Task 8 — Final Submission
**Status:** `[ ] pending`

**Intent:** Submit all four deliverables before 10:00 AM ET.

**Checklist:**
- [ ] Repo is public and accessible
- [ ] `HelloBobWatson/docs/bob-sessions/` contains at least 2 export files, committed and pushed
- [ ] Problem & solution statement ≤500 words — pasted into submission form
- [ ] Bob usage statement — pasted into submission form
- [ ] Video URL entered (publicly accessible)
- [ ] Repo URL entered
- [ ] Click Submit
- [ ] Read AI Submission Advisor feedback email
- [ ] If "Needs a second look" flags: revise and resubmit before deadline

**Target: submit no later than 9:00 AM ET** — leaves 1 hour for AI Advisor feedback + revision.

---

## Execution Order & Active Time Budget

| Sub-Task | Active time | Hard gate |
|---|---|---|
| Export this session NOW | 5 min | Do before anything else |
| 0 — Git repo init | 10 min | None |
| 1 — Problem statement draft | 30 min | None |
| 2 — Bob usage statement draft | 15 min | Sub-Task 1 done |
| 3 — Tier 1 CLI scaffold | 90 min | Repo exists |
| 4 — Demo fixture verification | 20 min | Tier 1 working |
| 6 — Export session (Tier 1) | 5 min | After Tier 1 |
| 5 — Demo video | 40 min | Fixtures verified |
| 7 — Tier 2 (stretch) | 60 min | Tier 1 done, exports in repo |
| 8 — Final submission | 15 min | All above |

**Conservative path (skip Tier 2):** ~3.5 hours active
**With Tier 2:** ~4.5 hours active
