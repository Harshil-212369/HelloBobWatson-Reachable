# IBM YouTube — 4 Types of Memory AI Agents Need
**Source:** IBM YouTube, presenter: Martin Keen | Framework: Koala (Princeton research)  
**Do not re-read the original txt file — read this file**

---

## The Four Memory Types

| Type | Analogy | Function | How to implement |
|---|---|---|---|
| **Working Memory** | RAM | The context window — active for this session only | Automatic; managed by the model |
| **Semantic Memory** | Reference book | Persistent facts, rules, documentation the agent must know | Markdown files injected at session start (e.g., `claude.md`, `PROBLEM_HANDOFF.md`) |
| **Procedural Memory** | Muscle memory / skills | How the agent performs specific tasks | Bob Skills (`skill.md` with YAML frontmatter) — use progressive disclosure: index first, load specific skill on demand |
| **Episodic Memory** | Personal diary | Past interactions and lessons learned | Distilled notes (NOT raw transcripts) stored between sessions, e.g., session summary exports |

---

## Key Design Rules

- **Not every agent needs all four.** Simple agents = working memory only. A full coding agent like this project = all four.
- **Progressive disclosure for procedural memory:** don't inject all skills at once; index them and pull specific ones when needed to preserve context budget.
- **Episodic memory = distilled summaries, not full transcripts.** Full transcripts bloat context and bury the signal.

---

## Application to This Project

| What we have | Which memory type |
|---|---|
| `PROBLEM_HANDOFF.md` | Semantic memory — injected at session start |
| `ClaudeChat_Understanding the project.md` | Episodic memory — distilled session notes |
| Skills created (e.g., `bob-session-export`) | Procedural memory |
| Bob's active context window | Working memory |
