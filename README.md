# Reachable — Liveness Checker

**IBM TechXchange 2026 Pre-conference Dev Day Hackathon**  
Team: HelloBobWatson | Solo: Harshil Suthar

---

## What it does

`reachable` answers one question per change:

> **Does the running system actually contain the change I just made?**

Three verdicts, and only three:

| Verdict | Meaning |
|---|---|
| `NOT LIVE` | Proven divergence. The runtime is consuming something other than what was edited. |
| `UNCONFIRMED` | Cannot establish liveness with available evidence. Refuses to assert. |
| `LIVE` | Positively verified by observing the runtime (Tier 2 only). |

---

## Why it exists

Six real incidents from the developer's own repos over eight weeks — each time a **success signal** (file saved, installer OK, commit created, agent responded coherently) was mistaken for a **liveness signal**. See [`HelloBobWatson/Background/PROBLEM_HANDOFF.md`](HelloBobWatson/Background/PROBLEM_HANDOFF.md) for the full incident table.

---

## Build tiers

| Tier | Contents | Status |
|---|---|---|
| **Tier 1** | Check Families A (git) + B (registration), CLI, text report — no model dependency | `[ ] building` |
| **Tier 2** | Check Family C (load-path inference via IBM Bob Document Understanding + parallel subagents) | `[ ] pending` |
| **Tier 3** | `--json` flag, second framework support | `[ ] stretch only` |

---

## Usage

```bash
# Tier 1 — runs git + registration checks on current repo
python reachable/reachable.py [--path <file_or_dir>]

# Tier 2 — adds AI load-path inference (requires Bob)
python reachable/reachable.py --tier2 [--path <file_or_dir>]
```

Output is a clean text report, one finding per line:

```
[NOT LIVE] IDENTITY.md
  Edited:    4 days ago (a3f9c2e)
  Expected:  AGENTS.md, SOUL.md, USER.md  (per README.md:41)
  Consumed:  IDENTITY.md is not in the documented load path
  Fix:       move content into AGENTS.md, or add IDENTITY.md to the load path
```

---

## IBM Bob Usage

This project was built using IBM Bob 2.0:
- **Plan Mode** — architecture design, verdict system, five git checks
- **Agent Mode** — Tier 1+2 scaffold, test fixtures, CLI
- **Document Understanding** — load-path inference from project README/schema (Tier 2)
- **Parallel Subagents** — concurrent multi-framework doc scanning (Tier 2)

Bob session exports are in [`HelloBobWatson/docs/bob-sessions/`](HelloBobWatson/docs/bob-sessions/).

---

## Project structure

```
.
├── reachable/                    # CLI source code
│   ├── reachable.py              # Entry point
│   ├── checks/                   # Check families A, B, C
│   └── tests/
│       └── fixtures/             # Deliberately broken repos for each incident
├── HelloBobWatson/
│   ├── CONTEXT.md                # Inject at every Bob session start
│   ├── Background/               # Original handoff docs and Claude chat exports
│   ├── docs/                     # Distilled guides (Bob reads these, not the PDFs)
│   │   ├── GUIDE_MaxJesch_Enablement.md
│   │   ├── GUIDE_IBM_Youtube_AgentMemory.md
│   │   ├── GUIDE_IBM_Youtube_AgentSkills.md
│   │   ├── GUIDE_HackathonRules_Summary.md
│   │   └── bob-sessions/         # Exported IBM Bob task session summaries
│   └── .bob/
│       └── skills/
│           └── bob-session-export.md
├── hackathon-submission-plan.md  # Master plan
├── .gitignore
└── .bobignore
```

---

## Submission checklist

- [ ] Video demo URL (90s–3min, publicly accessible)
- [ ] Problem & solution statement (≤500 words)
- [ ] Bob usage statement
- [ ] This repo URL (public) with Bob session exports in `docs/bob-sessions/`
