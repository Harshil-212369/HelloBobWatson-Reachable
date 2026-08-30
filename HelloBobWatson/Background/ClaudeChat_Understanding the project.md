---
title: Understanding the project — naming the error class and specifying Tier 1 git checks
This chat's date: 2026-08-29
Today's date: 2026-08-29
source: [FILL — paste chat url]
tags: [ibm-bob, techxchange-hackathon, liveness-checker, artifact-runtime-divergence, git, problem-statement, tier-1]
Subject:
  Opened with a Bob access blocker — the IDE showed an expired trial while an
  enterprise seat existed. Diagnosed it as a tenant-resolution problem, then
  confirmed it was exactly that (Settings → General → Team dropdown, switched
  bob-001 → ibm-coding-challenge-uat). Then asked three things: (1) name the
  class of error I keep hitting, (2) explain how the Bob access incident maps
  onto the failure class my hackathon project detects, (3) give me the concrete
  git checks for Tier 1 plus an execution order.
---

## What I was trying to do overall

Get a precise, defensible name for the failure class my IBM TechXchange Dev Day
hackathon project detects, so the problem statement rests on a definition rather
than a vibe — and get the Tier 1 git check list specified concretely enough to
start implementing.

## What I learned

**The error class, stated precisely:**

> A signal attesting to an artifact was read as a signal attesting to its consumption.

**Three components must all be present.** Remove any one and it is a normal bug,
not this bug:

| Component | Definition |
|---|---|
| **Artifact/runtime divergence** | What exists on disk (or in a registry, or a provisioning system) is not what the running process resolved. |
| **Resolution ambiguity** | Multiple candidate artifacts exist and *something else* chose one — a default, PATH order, a cached layer, a tenant selector. The choice is invisible at the point of use. |
| **Signal misattribution** | A true signal was observed. It attested to proposition A ("the artifact is correct"). It was read as proposition B ("the runtime is using it"). |

**The Bob access incident mapped onto the class:**

| Component | The incident |
|---|---|
| Artifact | Enterprise entitlement on `ibm-coding-challenge-uat`. Correct, provisioned, real. |
| Runtime | Bob IDE panel, bound to `bob-001`. |
| Ambiguity | Two teams in the Settings → General → Team dropdown. One selected by default. Invisible unless Settings is opened. |
| Misattributed signal | The email *"You have been added as a team member."* True. Attests to provisioning. Says nothing about which tenant the IDE resolved. |

- My **first diagnostic move was wrong in an instructive way**: I checked the
  artifact (MyIBM → "IBM Bob Trial: Expired") instead of the resolution. MyIBM
  shows the *personal* trial and has no visibility into the team seat at all. I
  was reading a true fact about the wrong object. The fix required inspecting
  what the runtime had resolved — which is the exact epistemic move the tool
  automates.
- **Where the analogy strains, and I must say so before a judge does:** the
  mechanism differs. This was SaaS tenant selection; my six documented incidents
  are code artifacts and load paths. Correct framing is *"same failure class,
  different substrate."* Claiming the tool would have caught the Bob incident is
  overreach and must not be claimed.

**The verdict design and why it holds up:**

- **Git can prove a change is not live. It cannot prove a change is live.** Git
  sees the repo; it never sees the process.
- Therefore three verdicts, not two:

| Verdict | Basis |
|---|---|
| **NOT LIVE** | Proven from git. The change is not where a consumer would look. |
| **UNCONFIRMED** | Git is clean. No positive evidence of consumption exists. |
| **LIVE** | Requires a runtime probe. Tier 2 only. **Never emitted by Tier 1.** |

- A checker that only proves the negative is honest, and honest survives
  interrogation. A confident `LIVE` derived from git alone collapses under one
  question.

**On the checks themselves:**

- **Check 5 (`git check-ignore`) is the demo lead.** It catches precisely what
  check 1 structurally cannot: `git status` is *defined* to hide ignored files.
  A gitignored file the runtime loads works on my machine forever and has never
  existed for anyone else. Most validators miss this entirely.
- **Check 2 needs a guard.** `@{upstream}` exits non-zero when no upstream is
  configured — probe first and emit a distinct "no upstream configured" finding
  rather than crashing.
- **`git worktree list` is the highest-value second-wave check.** It is the
  git-native version of the Bob Shell vs. IDE panel two-surface drift problem I
  already decided to avoid. Editing in one worktree, running from another, same
  bug different substrate.
- **Fixtures are written at implementation time, not after.** A check with no
  deliberately-broken fixture repo proving it fires is a check I cannot demo.

## Project Decisions I made

1. **Three-verdict system confirmed**, with `LIVE` explicitly reserved for Tier 2
   runtime probing. Tier 1 emits only `NOT LIVE` and `UNCONFIRMED`.
2. **Core five git checks locked** for Tier 1 (see snippets).
3. **`git check-ignore` leads the demo**, not `git status` — it is the check that
   demonstrates something a naive implementation structurally cannot see.
4. **Any check without a named incident gets cut.** Credibility of the problem
   statement rests on "check N catches incident N" being literally true.
5. **Problem statement goes two incidents deep, not six shallow.**
6. **The Bob tenant incident is illustrative, not evidentiary.** It appears in
   the writeup as a same-class/different-substrate example, never as a claim the
   tool would have caught it.
7. **Session export located before any code is written.**

## Open questions / next actions

- [ ] **Locate the Bob session export mechanism (~20 min).** Run one throwaway
      task, export it, inspect the format. Required deliverable, unknown shape —
      do not discover this at hour 44. Candidates: the `···` overflow menu and
      the checklist icon in the Bob panel header; Bobalytics (external link, may
      only give consumption metrics rather than the task transcript the rules
      require). Fallback: `File logging` is on, and Settings → General → Log
      directory → Open gives an independent on-disk record of what Bob did.
- [ ] **Write the problem statement (~40 min).** Structure: failure class in one
      sentence → the three components → two of the six incidents in full detail
      with repo names.
- [ ] **Build Tier 1 scaffold (~2 hrs)**, in this order:
      1. Repo discovery and validation (`rev-parse --show-toplevel`, bail cleanly
         outside a repo)
      2. Check runner returning structured findings —
         `{check_id, verdict, evidence, remediation}`
      3. Core five, one at a time, each with a broken fixture repo proving it fires
      4. Verdict aggregation (worst verdict wins)
      5. CLI entrypoint and text report
      6. Exit codes: `0` unconfirmed-clean, `1` not-live, `2` tool error
- [ ] **Produce the check-to-incident mapping** and pressure-test each line.
- [ ] **Draft the solution statement** — only after Tier 1 runs end to end.
- [ ] Tier 2 (load-path inference, subagents) is not touched until the above is done.

## Tasks I decided that I will do later or I may think of doing them later

- Second-wave git checks if time allows: `git submodule status --recursive`,
  `git worktree list`, `git rev-parse -q --verify MERGE_HEAD`,
  `git log -1 --format='%H %cI' -- <path>`.
- Tier 2: load-path inference via document understanding and parallel subagents.
- Watch for Bob silently defaulting back to `bob-001` mid-session — it would
  reproduce the expired-trial behaviour and look like a Bob bug rather than a
  tenant selection. Glance at the Plan line if anything gets weird.

## Snippets worth keeping

**Core five Tier 1 checks.** Each line is the probe; the fail condition is what
promotes the finding to `NOT LIVE`.

```bash
# 1. Dirty tree — fails if output is non-empty
git status --porcelain=v1

# 2. Unpushed / stale — output is "behind<TAB>ahead"; fails if either is non-zero
git rev-list --left-right --count @{upstream}...HEAD

# 3. Detached HEAD — fails on exit code 1
git symbolic-ref -q HEAD

# 4. Untracked load-bearing file — fails if a path matches a load-bearing pattern
git ls-files --others --exclude-standard

# 5. Ignored load-bearing file — fails on exit 0 (prints the matching rule)
git check-ignore -v -- <path>
```

**Upstream guard for check 2.** `@{upstream}` exits non-zero when no upstream is
configured, which would crash check 2. Probe first and emit a distinct
"no upstream configured" finding instead.

```bash
git rev-parse --abbrev-ref --symbolic-full-name @{upstream} 2>/dev/null
```

**Repo root / bail-out for scaffold step 1.** Confirms the tool is operating on
the repo it thinks it is, and exits cleanly when run outside a repo.

```bash
git rev-parse --show-toplevel
```

**Tenant fix for the Bob access incident**, for the record: Bob Settings →
General → Team dropdown → switch `bob-001` to `ibm-coding-challenge-uat`.
Confirmation signal is the Plan line reading `enterprise plan` rather than
`trial plan`.
