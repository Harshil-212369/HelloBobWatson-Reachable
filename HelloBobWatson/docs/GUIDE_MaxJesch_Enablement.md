# Max Jesch Enablement Session — Distilled Guide
**Speaker:** Max Jesch, PM of IBM Bob  
**Session date:** August 29, 2026  
**Source:** Pre-event hackathon enablement session PDF (do not re-read the PDF — read this file)

---

## 1. Bob's Four-Phase Workflow

```
Explore → Plan → Implement → Verify
```

- **Each phase is a context boundary.** Start a new conversation per phase; do not let them bleed.
- **Aim to complete only half the circle per session.** e.g. Explore+Plan in one session, Implement+Verify in another.
- **Verification must be designed during Planning**, not figured out afterward.
- **Bob forgets mistakes.** Write them down separately (in a handoff doc, a PROBLEM_HANDOFF.md, etc.) rather than relying on in-context memory across sessions.

---

## 2. Compaction

- `/compact` is **lossy.** Use it only when context is genuinely full, not as a shortcut.
- When compacted, critical constraints (encoding rules, incident table, UNCONFIRMED policy) must be re-injected from external docs.

---

## 3. Skills

- Skills = reusable prompt templates.
- They **save tokens** — load the skill once, the knowledge is available without re-explaining.
- **Description is the trigger.** Bob decides whether to use a skill based on the `description` field. Write it to match the moment the skill should fire, not what the skill does abstractly.
- Create with `/create-skill` for anything done more than once.
- Fragile, multi-step jobs = **script them, do not skill them.** Scripts are deterministic; skills are probabilistic.

---

## 4. Modes

- Built-in modes: `agent`, `ask`, `plan`.
- You can create **custom modes** with restricted permissions (e.g., a read-only review mode with no write access — useful for safe code review without accidental edits).
- Bob operates within the personality/permissions of the active mode.

---

## 5. Hooks (DETERMINISTIC — not a suggestion, an enforcement)

Unlike modes and skills (which are instructional), hooks are code that runs unconditionally.

| Hook trigger | Example use |
|---|---|
| Pre-conversation start | Bash script: check branch cleanliness, Java version, env vars |
| Pre-push (GitHub Action) | Scan for API secrets in staged files |
| Post-PR creation | Bob PR review — Implementation plan + GitHub Issues + Bob's review |

**Do not ask Bob to build the hooks themselves.** Keep them deterministic Python/bash. Bob is for the ambiguous parts.

---

## 6. Verification Pattern

- Implement and Verify are separated by a blurry line — treat them as distinct sessions.
- Use GitHub Actions + Pull Request review as the verification harness.
- Pattern: `Implementation plan → GitHub Issues → Commit → PR → Bob PR review`

---

## 7. Sensors vs. Guides

Max explicitly flagged: **"Focus on Sensors too, not just guides."**  
Interpretation for this project: Build checks that *observe* the runtime (sensors), not just instructions that tell you what to do (guides). This maps directly to the Reachable project's thesis.
