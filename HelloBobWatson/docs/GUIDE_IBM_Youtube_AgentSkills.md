# IBM YouTube — 5 Ways to Give AI Agents Skills + 5 Best Practices
**Source:** IBM YouTube (two videos)  
**Do not re-read the original txt files — read this file**

---

## Part 1 — 5 Patterns for Connecting Agents to Tools (ascending security)

| Pattern # | Name | How it works | Trade-off |
|---|---|---|---|
| 5 | Direct Connection | User → Agent → Tool | Simple; agent uses own credentials; no user visibility |
| 4 | Direct + OAuth | Adds identity provider | User identity visible to tool; agent invisible (impersonation risk) |
| 3 | MCP | Agent → MCP → Tool; agent only knows MCP protocol | Good abstraction; agent doesn't need per-tool knowledge |
| 2 | Token Exchange | Agent authenticates itself; user delegates via token propagation | Full observability; risk = long-lived token storage |
| 1 | Vault (best) | Vault holds long-term token; issues short-lived creds to MCP | Minimal replay window if intercepted; gold standard |

**For this hackathon:** Pattern 3 (MCP) is sufficient and what IBM Bob uses natively.

---

## Part 2 — 5 Best Practices for Building Agent Skills

### 1. Description is the trigger
- The `description` field in YAML frontmatter determines if the skill ever runs.
- Format: `name` (max 64 chars) + `description` (max 1,024 chars)
- **Oversell rather than undersell.** If the description undersells, the agent skips the skill even when it should run.

### 2. Fragile multi-step jobs = script, not skill
- Skills are probabilistic. Scripts are deterministic.
- Any step where failure is silent or partially correct → write a script.

### 3. Standard folder structure
```
skills/      ← skill YAML + Markdown files
refs/        ← reference documents the skills link to
```

### 4. Skill security
- Skills can contain/run code.
- Installing a skill from the internet = running arbitrary code on your machine.
- Only install skills from sources you control or trust explicitly.

### 5. Reference standard
- `agentskills.io` — canonical reference for skill authoring patterns.

---

## YAML Frontmatter Template

```yaml
---
name: my-skill-name          # max 64 chars, kebab-case
description: |               # max 1024 chars — write this to fire at the RIGHT moment
  Use this skill when [specific trigger condition].
  It [what it does]. It does NOT [what it avoids].
---
```
