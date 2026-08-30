# CONTEXT INJECTION — Read this at the start of every Bob session

Project: **Reachable** | Team: HelloBobWatson (solo: Harshil Suthar)
Event: IBM TechXchange 2026 Dev Day Hackathon | Deadline: 10:00 AM ET Aug 30 2026

---

## What this project is

A CLI liveness checker that answers: **"Does the running system actually contain the change I just made?"**

Three verdicts only: `NOT LIVE` | `UNCONFIRMED` | `LIVE`
- `NOT LIVE` = proven divergence (git/registration)
- `UNCONFIRMED` = cannot establish liveness with available evidence — NOT an error state
- `LIVE` = only emitted by Tier 2 after runtime probe — NEVER by Tier 1

---

## The six real incidents (ground truth)

| # | Edited | Runtime consumed | Lying signal |
|---|---|---|---|
| 1 | `IDENTITY.md` | `AGENTS.md/SOUL.md/USER.md` — wrong load path | File saved |
| 2 | Skill in `.claude/skills/` | Host scans `skills/` — different dir | File saved in plausible dir |
| 3 | Two skills, correct dir | No YAML frontmatter, not indexed — installer said OK | Installer exit 0 |
| 4 | Pipeline fix on `feat/v3-long-audio-transcription` | GHA checks out `main`; branch never merged | Commit created, tests passed locally |
| 5 | Four commits locally | GitHub counts only pushed work | Commit created |
| 6 | Files in project folder | Agent tracked a separate copy; stale version used | Agent responded coherently |

**Single failure pattern:** success signal (file saved / installer OK / commit created / agent responded) mistaken for liveness signal.

---

## Build tiers

| Tier | What | Status |
|---|---|---|
| Tier 1 | Families A+B — git + registration checks, CLI, text report. No model. | `[ ] pending` |
| Tier 2 | Family C — load-path inference via Doc Understanding + parallel subagents | `[ ] pending` |
| Tier 3 | `--json` flag, second framework | `[ ] pending — only if Tiers 1+2 done` |

**Do NOT touch Tier 2 until Tier 1 runs end-to-end against fixtures.**

---

## Hard constraints (never violate)

- ASCII only in all script output (Windows PowerShell 5.1 / no WSL)
- Tool NEVER auto-fixes anything — prints exact command, developer runs it
- LIVE verdict NEVER emitted by Tier 1
- UNCONFIRMED is a valid first-class result, not a failure
- Every check must map to a named incident — cut any check without one
- No IBM Cloud credentials in any committed file

---

## Key files to know about

| File | Purpose |
|---|---|
| `HelloBobWatson/Background/PROBLEM_HANDOFF.md` | Full spec — read before implementing anything |
| `HelloBobWatson/Background/ClaudeChat_Understanding the project.md` | Five git checks locked, verdict design rationale |
| `HelloBobWatson/docs/GUIDE_HackathonRules_Summary.md` | Scoring criteria, deliverables, export rules |
| `HelloBobWatson/docs/GUIDE_MaxJesch_Enablement.md` | Bob workflow phases, hooks, skills guidance |
| `hackathon-submission-plan.md` | Full ordered plan with sub-tasks |

---

## Current open actions (update as completed)

- [ ] Locate Bob session export mechanism — find it BEFORE writing code
- [ ] `git init` + create public GitHub repo
- [ ] Write problem & solution statement (500 words max)
- [ ] Build Tier 1 scaffold (Families A+B)
- [ ] Capture Bob session exports after each session
- [ ] Record demo video
- [ ] Submit by 10:00 AM ET Aug 30
