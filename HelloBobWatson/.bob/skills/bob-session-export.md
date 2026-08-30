---
name: bob-session-export
description: |
  Use this skill at the END of every Bob task session during the IBM hackathon.
  It guides you through exporting the IBM Bob task session summary — which is a
  required submission deliverable ("exported IBM Bob report of all relevant
  tasks/sessions"). Run this after completing any meaningful unit of work:
  planning, implementing a check family, writing the problem statement, or
  finishing Tier 2. Do NOT wait until the end of the hackathon to export; the
  rules require all relevant sessions, not just the final one.
---

# Skill: Bob Session Export

## When to run this

Export at the end of **every session** where meaningful work was done. Minimum sessions:
1. After this planning session
2. After Tier 1 implementation (Families A+B complete)
3. After the problem statement + Bob usage statement are written
4. After Tier 2 (Family C) if completed

The rules say: *"exported IBM Bob report of all relevant tasks/sessions used for the contest."*
That means every session, not one at the end.

---

## How to export a Bob session summary

### Method 1 — Task panel (preferred)
1. Look at the Bob panel header. Find the **checklist icon** or **`···` overflow menu**.
2. Click it and look for "Export task summary", "Export session", or "Download report".
3. Save the file (likely `.md` or `.json`) to `HelloBobWatson/docs/bob-sessions/`.
4. Name it: `session-YYYY-MM-DD-HH-MM-<short-topic>.md`
   - Example: `session-2026-08-29-21-00-planning.md`

### Method 2 — Bobalytics (if Method 1 unavailable)
1. Open Bobalytics from the Bob panel or browser.
2. Look for task/session history with a download or export option.
3. Note: Bobalytics may show consumption metrics only — if so, use Method 3.

### Method 3 — File logging fallback
1. In Bob: `Settings → General → Log directory → Open`
2. Find the log file for the current session.
3. Copy the relevant session log to `HelloBobWatson/docs/bob-sessions/`.
4. Note in the README that this is a log file, not a task summary export.

---

## After exporting

1. Move/copy the export file to `HelloBobWatson/docs/bob-sessions/`
2. `git add HelloBobWatson/docs/bob-sessions/`
3. `git commit -m "chore: add Bob session export — <topic>"`
4. `git push`

The repo must be publicly accessible and the screenshots/exports must be visible in it.

---

## What a good session export contains

- The task or question you started with
- The key decisions made or output produced
- Any commands run and their results
- Files created or modified

If the export is thin (just a title), supplement it with a screenshot of the Bob panel showing the task and its output, saved as a `.png` in the same folder.

---

## Verification check

Before moving to the next session, confirm:
- [ ] Export file exists in `HelloBobWatson/docs/bob-sessions/`
- [ ] File is committed and pushed to the public repo
- [ ] File name includes the date and topic
