# PROBLEM_HANDOFF.md

Project: **Reachable**
Team: HelloBobWatson (solo)
Event: IBM TechXchange 2026 Pre-conference Dev Day Hackathon, Aug 28-30 2026
Track: Debugging (local developer preflight)

Read this whole file before proposing an implementation. The origin story is what
makes the tool defensible; the spec alone is not.

---

## 1. The question the tool answers

One question, per change:

> **Does the running system actually contain the change I just made?**

Three verdicts, and only three:

| Verdict | Meaning |
|---|---|
| `NOT LIVE` | Proven divergence. The runtime is consuming something other than what was edited. |
| `UNCONFIRMED` | The tool cannot establish liveness with the evidence available. It refuses to assert. |
| `LIVE` | Positively verified by observing the runtime, not the filesystem. |

`UNCONFIRMED` is a first-class result, not an error state. See section 5.

---

## 2. The six incidents this comes from

All six occurred in the operator's own repositories over eight weeks:
`pay-per-session-tutoring-agent`, `cpol507-pipeline`, and an OpenClaw/aitch
workspace. Fixing commits exist and serve as ground truth.

| # | What was edited | What the runtime actually consumed | Signal that lied |
|---|---|---|---|
| 1 | `IDENTITY.md` | `AGENTS.md` / `SOUL.md` / `USER.md`. The edited file was never in the load path. | File saved |
| 2 | A skill in `.claude/skills/` | The host scans `skills/`. `.claude/skills/` is a different tool's convention. | File saved in a plausible directory |
| 3 | Two skills, correct directory | No YAML frontmatter, so never indexed. **The installer printed "success".** | Installer exit 0 |
| 4 | A pipeline fix on branch `feat/v3-long-audio-transcription` | GitHub Actions checks out `main`. The branch was never merged. | Commit created, tests passed locally |
| 5 | Four commits made locally | GitHub counts only pushed work. Contribution graph empty. | Commit created |
| 6 | Files edited in the project folder while an agentic IDE tracked a separate copy | The agent answered from a stale version. Fluent, confident, deprecated, and no error was raised. | Agent responded coherently |

### The single shape

**The artifact existed and was correct. The runtime consumed a different one.**

In every case a **success signal** (file saved, installer OK, commit created,
agent responded) was mistaken for a **liveness signal**. None of those four
things proves the running system can see the change.

The fix was identical every time: **run the check that observes the runtime, not
the filesystem.** Ask the host whether the skill is loaded. Start a fresh session
and ask the agent what it read. Confirm `git log origin/main..HEAD` is empty.
Read the deployed branch, not the local one.

### Why incident 6 matters most for this hackathon

Incident 6 is the same bug class, created by agentic development itself. Bob,
and every tool like it, maintains its own view of a project: a load path, a
context set, an index. When that view diverges from disk, the result is a
confident wrong answer with no error. This tool is a preflight for that failure.

---

## 3. What to build

Point it at a repository. It returns a verdict per change, with the reason and
the exact fix command.

### Check family A - git liveness (DETERMINISTIC)

Local refs vs `origin` vs the ref CI actually builds.

- `git log origin/<branch>..HEAD` non-empty means unpushed. (Incident 5)
- Current branch not merged into the branch CI checks out. (Incident 4)
- Dirty working tree; detached HEAD; untracked but load-bearing files.
- Parse the CI workflow file to learn which ref is actually built. Do not assume `main`.

No model in this path. `git` output is exact; a model here can only introduce error.

### Check family B - registration liveness (DETERMINISTIC, given a schema)

Files present on disk but not registered with the runtime.

- Missing or malformed YAML frontmatter. (Incident 3)
- Manifest or index entry absent.
- File sits in a directory the host does not scan. (Incident 2)
- `git check-ignore` says the file is ignored and therefore never travels.

The model's only role here is *locating* the schema or manifest. Once found,
validation is code.

**Prior art to respect, not duplicate:** `claude plugin validate`,
`agent-ecosystem/skill-validator`, and SkillCheck already validate skill
frontmatter against a spec. This tool must not claim that as novel. Its
contribution is asking registration as one part of a single liveness verdict.

### Check family C - load-path liveness (PROBABILISTIC)

Which config and context files does the runtime *actually* read?

Read the project's own README, schema, and documentation to infer the intended
load path, then compare that to what exists on disk. This catches incident 1:
an edited file that nothing reads.

This is the only genuinely ambiguous step, and the only place a model belongs.
It is also the part that generalises beyond any one framework, because it does
not require hardcoded per-tool rules.

**Known weakness, must be handled explicitly:** if the docs are stale, this check
can produce a false verdict in either direction. Mitigation is section 5, not
better prompting.

---

## 4. Which parts are AI and which are scripts

| Check | Implementation | Reason |
|---|---|---|
| A - git | Script. No model. | `git` is exact. A guess can only be wrong. |
| B - registration | Script, model locates the schema | Deterministic once the rules are known. |
| C - load path | Model, with mandatory `UNCONFIRMED` | Reading prose to infer intent is genuinely ambiguous. |

A tool whose thesis is *false success signals cost me a week* cannot itself
generate false greens. Match prescriptiveness to fragility: loose step, write
instructions; fragile step, write code.

---

## 5. The UNCONFIRMED policy

The tool returns `UNCONFIRMED` and refuses to assert liveness when any of these hold:

1. No authoritative document naming the load path could be located.
2. Two or more documents disagree about the load path.
3. The documentation's stated load path references files that do not exist on
   disk, implying the docs are stale.
4. The runtime cannot be observed directly and only filesystem evidence is available.
5. The inferred load path is derived from a single unversioned source with no
   corroborating structure in the repo.

Output must always state *why* it could not conclude. Example:

    [UNCONFIRMED] agent context load path
      Documented (README.md:41): AGENTS.md, SOUL.md, USER.md
      On disk:                   AGENTS.md, IDENTITY.md
      USER.md and SOUL.md are absent. Documentation may be stale.
      Cannot confirm whether IDENTITY.md is read.
      Next: start a fresh session and ask the agent which files it loaded.

---

## 6. Output format

One line per finding: what, where, why, fix. Model the report on the secret
scanners (gitleaks, trufflehog) and on expected-vs-actual diffs (terraform plan).
Show both sides of every mismatch.

    [NOT LIVE] IDENTITY.md
      Edited:    4 days ago (a3f9c2e)
      Expected:  AGENTS.md, SOUL.md, USER.md  (per README.md:41)
      Consumed:  IDENTITY.md is not in the documented load path
      Fix:       move content into AGENTS.md, or add IDENTITY.md to the load path

Default output is the clean report. Subagent reasoning goes behind `--verbose`.

**Encoding constraint:** keep all generated scripts and output ASCII. Windows
PowerShell 5.1 reads BOM-less scripts as ANSI and mangles non-ASCII characters,
producing parser errors far from the real line.

---

## 7. What the tool must never do

**It does not fix anything automatically.** It prints the exact command and the
developer runs it.

Every one of the six incidents was caused by a system silently doing something
other than what was intended. A tool that silently moves files is the same
failure with better intentions.

---

## 8. Scope

**Build:** three check families, a CLI, a clean text report, a `--json` flag.

**Do not build:** a web UI, a VS Code extension, multi-language plugin support,
a hosted service, auth, or a database. If time remains, add one more framework's
load-path rules instead of any of the above.

**Tier 1 (must ship first, guaranteed demo):** families A and B, CLI, text report.
No external services, no model dependency. Complete and running before Tier 2 starts.

**Tier 2 (the payoff):** family C via document understanding and parallel subagents.

**Tier 3 (only if genuinely free):** `--json`, a second framework's rules.

---

## 9. Measuring impact

Do **not** claim elapsed calendar time between a stale commit and its fix. That
interval includes sleeping, classes, and unrelated work. It is not lost
engineering time and a judge will say so.

Measure **time to signal** instead, and demonstrate it on camera:

1. Reset a repository to the broken state for three of the six incidents.
2. Run the normal loop: build, lint, save, ask the agent. Record what it reports.
3. Run `reachable`. Record what it reports and how long it takes.

The claim then becomes falsifiable and reproducible:

> On three of six reconstructed incidents the existing toolchain reports success.
> `reachable` reports NOT LIVE, with the reason, in under N seconds.

No percentage appears anywhere that cannot be reconstructed from a log.

---

## 10. Novelty claim, stated honestly

Individually, most of these checks exist. `git status` reports being ahead of
origin. Frontmatter validators exist. Infrastructure drift tools (driftctl,
Spacelift, Terraform) compare cloud state to IaC, which is a different layer.

The contribution is:

1. **Composition** - git, registration, and load path asked as one question with
   one verdict, rather than three unrelated tools a developer must remember to run.
2. **Load-path inference from a project's own prose documentation**, which no
   schema-based validator can do, because there is no schema to validate against.

Do not claim more than these two.

---

## 11. Working notes for the implementing agent

- Verify before declaring done. Run the check that observes the runtime and show
  its output. This project is about that discipline; it must not be built in a way
  that violates its own thesis.
- Show actual file contents and diffs rather than summarising them.
- Prefer commands that state their assumptions and throw, over commands that
  default. A fallback default inside a verification script is a false-green generator.
- Environment: Windows, no WSL for this event. PowerShell 5.1 encoding caveat above.
- One authoritative editing surface for the whole build. Do not alternate between
  the IDE panel and a shell. That alternation is incident 6.
