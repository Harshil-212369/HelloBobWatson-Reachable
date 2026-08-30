# IBM Bob Usage Statement
**Project:** Reachable | **Team:** HelloBobWatson

---

IBM Bob 2.0 was used to design, plan, and build every layer of Reachable.

**Plan Mode** was used to architect the three-verdict system (NOT LIVE / UNCONFIRMED / LIVE), determine which check families belong to deterministic scripts versus AI inference, and sequence the Tier 1 build order before any code was written. The session export from this planning session is included in the repository under `HelloBobWatson/docs/bob-sessions/`.

**Agent Mode** was used to scaffold the full Tier 1 CLI (`reachable/reachable.py`), implement Check Families A and B (git liveness and registration liveness), create the demo fixture repositories demonstrating each incident class, and validate the ASCII-only output constraint required by the Windows PowerShell 5.1 environment.

**Document Understanding** (Tier 2) — Bob reads the target project's README, schema, and documentation to infer the intended load path, then compares what is documented against what exists on disk. This is the only check that cannot be performed with a schema validator, because the knowledge lives in prose, not in a machine-readable spec. This directly addresses Incident 1: a file edited in a path that nothing in the runtime ever reads.

**Parallel Subagents** (Tier 2) — multiple subagents scan different framework documentation files simultaneously, allowing load-path inference across multiple conventions in a single run without sequential blocking.

**Custom Skill** — a `bob-session-export` skill was created at `HelloBobWatson/.bob/skills/bob-session-export.md` to encode the per-session export workflow as reusable procedural memory. This skill fires at the end of each work session and guides the export, naming convention, commit, and push steps — ensuring the required deliverable (exported Bob report of all relevant sessions) is never missed.

All Bob task session exports (Markdown format) are committed to `HelloBobWatson/docs/bob-sessions/` in the public repository, with one export file per meaningful work session.

---
*Note: IBM watsonx.ai and watsonx Orchestrate were not used in this submission.*
