# Demo Video Script — Reachable
**Target length:** 2.5 minutes | **Minimum:** 90 seconds of working solution
**Record with:** Win+G (Xbox Game Bar) or OBS Studio
**Upload to:** YouTube (unlisted is fine — must be publicly accessible)

---

## Pre-recording checklist (do before hitting record)

- [ ] Open two PowerShell windows side by side:
      Left:  `cd` to the workspace root (Aug27 Hackathon folder)
      Right: keep idle for contrast shots
- [ ] Bob IDE panel visible in background (so it appears on screen)
- [ ] Run once to warm up (no recording): `python reachable/reachable.py --path demo-fixtures/galaxium-travels`
- [ ] Font size bumped up in terminal (Ctrl+Scroll) so output is readable on video
- [ ] Close notifications / do not disturb on

---

## Script (speak these words, show these screens)

---

### SEGMENT 1 — Hook (0:00–0:20) | SPEAK, no typing yet

> "Six times in eight weeks, the same thing happened.
> I saved the file. The commit was there. The build passed.
> The agent answered confidently.
> But the running system had never seen the change.
> The success signal lied.
> This is Reachable."

**Screen:** Show the Bob IDE panel with the project open. Nothing running yet.

---

### SEGMENT 2 — Show the lie (0:20–0:45) | DEMO: existing toolchain

**Speak:**
> "Here is Fixture 1. A real IBM sample repo — galaxium-travels.
> Let me show you what the existing toolchain says."

**Type and run (show output on screen):**
```
git -C demo-fixtures/galaxium-travels status
```

**Speak while output shows:**
> "Git status: clean. Nothing to commit, working tree clean.
> The toolchain says everything is fine."

**Speak:**
> "But there is a commit sitting locally that has never been pushed to origin.
> Git status is defined to hide this. It says clean. It always says clean."

---

### SEGMENT 3 — Reachable on Fixture 1 (0:45–1:10) | DEMO: unpushed commit

**Speak:**
> "Now I run Reachable."

**Type and run:**
```
python reachable/reachable.py --path demo-fixtures/galaxium-travels
```

**Speak as output appears:**
> "NOT LIVE. Unpushed commits — 2 local commits not yet pushed to origin/main.
> Fix: git push.
> One command. The reason. The exact fix."

---

### SEGMENT 4 — Reachable on Fixture 2 (1:10–1:40) | DEMO: missing YAML frontmatter

**Speak:**
> "Fixture 2. A different failure class. A skill file was added to the skills directory —
> the correct directory — but with no YAML frontmatter.
> The installer exited zero. No error. The skill was never indexed."

**Type and run:**
```
python reachable/reachable.py --path demo-fixtures/bob-dev-day-halifax
```

**Speak as output appears:**
> "NOT LIVE. skills/demo-skill.md — no valid YAML frontmatter block.
> Runtime will not index it. Installer may still exit zero.
> And the fix: add the frontmatter block. Exact template provided."

---

### SEGMENT 5 — Reachable on Fixture 3 / wrong directory (1:40–2:05) | DEMO: B2

**Speak:**
> "And the third class. A file placed in the wrong directory.
> The skill has valid frontmatter. It looks correct.
> But the runtime scans skills/ — not .claude/skills/.
> The file will never be read."

**Type and run (reachable on galaxium-travels again — it already has the nav-skill finding):**
```
python reachable/reachable.py --path demo-fixtures/galaxium-travels
```

**Speak as the B2 finding appears:**
> "NOT LIVE. .claude/skills/nav-skill.md — file is in the wrong directory.
> Claude and Bob scan skills/. This file is invisible to the runtime.
> Fix: move it."

**Speak:**
> "Three different failure classes. One command. All caught in under two seconds."

---

### SEGMENT 6 — Show Bob (2:05–2:25) | Show the IDE

**Switch to Bob IDE panel on screen.**

**Speak:**
> "Reachable was designed and built entirely with IBM Bob 2.0.
> Plan Mode — to design the three-verdict architecture before writing any code.
> Agent Mode — to scaffold the CLI, implement the checks, and validate against fixtures.
> The session exports from every build session are in the repository."

**Point at / scroll to the bob-sessions folder in the file tree briefly.**

---

### SEGMENT 7 — Close (2:25–2:45)

**Back to terminal. Run one final clean check on main repo:**
```
python reachable/reachable.py --path .
```

*(This will show A2 unpushed if any — or clean if all pushed. Either is fine — it shows the tool working on real state.)*

**Speak:**
> "Reachable. One question: does the running system actually contain the change I just made?
> Three verdicts: NOT LIVE, UNCONFIRMED, LIVE.
> No auto-fix. No guessing. The exact command. You run it.
> Because every one of these failures was caused by a system silently doing
> something other than what you intended.
> This tool is not that."

---

## After recording

1. Trim to under 3 minutes in any video editor (or just re-record if it ran long)
2. Upload to YouTube → set to **Unlisted** (still publicly accessible via link)
3. Copy the YouTube URL
4. Paste into the hackathon submission form under "Video demonstration URL"

---

## Submission form — copy-paste sources

| Field | Source file |
|---|---|
| Video URL | YouTube link (after upload) |
| Problem & solution statement | `HelloBobWatson/docs/problem-statement.md` — paste the 5 paragraphs (skip the heading) |
| Bob usage statement | `HelloBobWatson/docs/bob-usage-statement.md` — paste everything after the `---` line |
| Code repository URL | `https://github.com/Harshil-212369/HelloBobWatson-Reachable` |
