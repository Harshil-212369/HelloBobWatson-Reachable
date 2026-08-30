# Problem and Solution Statement
**Project:** Reachable | **Team:** HelloBobWatson | **Track:** Debugging

---

Six times in eight weeks across three real repositories, the same failure occurred: a success signal — file saved, installer exited 0, commit created, agent responded coherently — was taken as proof the change was running. In every case it was not. The artifact was correct. The runtime consumed a different one. No existing tool catches all six.

`git status` was clean. The build passed. The agent answered fluently. But none of these observe the runtime. `git status` hides ignored files by definition — a gitignored skill file works on one machine and has never existed for anyone else. A skill installer can exit 0 and never index the file because the YAML frontmatter is missing. CI can check out a different branch than the one that was fixed. An agentic IDE can track a stale copy of the project and answer confidently from a version that was deprecated two commits ago. Success signals are not liveness signals. The distinction is structural, not a bug in any one tool.

`reachable` is a CLI that answers one question per change: does the running system actually contain this? Three verdicts: NOT LIVE (proven divergence), UNCONFIRMED (cannot establish liveness with available evidence — a first-class result, not an error), and LIVE (runtime probe, AI tier only). Tier 1 is fully deterministic with no model dependency. Check Family A covers git liveness: unpushed commits, CI branch mismatches, dirty working tree, detached HEAD, and — the demo lead — files that are gitignored and therefore structurally invisible to `git status`. Check Family B covers registration liveness: missing YAML frontmatter, files placed in the wrong directory, and absent index entries. Tier 2 adds IBM Bob Document Understanding to infer intended load paths from a project's own prose documentation, using parallel subagents to scan multiple frameworks simultaneously. The tool never auto-fixes. It prints the exact command. The developer runs it. Every one of the six incidents was caused by a system silently doing something other than what was intended — a tool that silently mutates state is the same failure with better intentions.

Target users: any developer who has said "but I saved the file" or "the commit is there." Zero configuration on any git repository. One command: `reachable`. Output is one finding per line — what is wrong, where, why, and the exact fix command.

On three reconstructed incidents, the existing toolchain reports success: `git status` clean, build passing, installer exit 0. `reachable` reports NOT LIVE with the reason and fix command in under five seconds. That result is demonstrated live in the video. The novelty is composition: git liveness, registration liveness, and AI load-path inference asked as one question with one verdict, rather than three unrelated tools a developer must remember to run separately.

---
*Word count: ~370 words*
