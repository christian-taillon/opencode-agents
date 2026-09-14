---
disabled: true
---

# opencode-agents

Reusable, opinionated agent definitions for OpenCode 2.

The repository separates implementation, orchestration, review, repository operations, low-cost volume work, and contained research so each task can use an appropriate model and permission boundary without unnecessary agent chains.

Copy the agents you want into `~/.config/opencode/agents/` or a project's `.opencode/agents/` directory, then review their models and permissions.

## Core engineering

| Agent | Purpose |
| --- | --- |
| `luna-runner` | Cheap OpenAI utility work using Luna High |
| `luna-code` | Bounded implementation using Luna xHigh |
| `sol-code` | Default implementation, debugging, refactoring, and integration |
| `astra-code` | Difficult, subtle, security-sensitive, or consequential engineering |
| `sol-review` | Independent read-only review and difficult diagnosis |
| `autopilot-sol` | Normal evidence-driven engineering orchestration |
| `orchestrator-sol` | Durable long-running workstream manager and optional nested orchestrator |

Use `luna-runner` for commands, tests, documentation, simple configuration, repository inspection, summarization, and mechanical low-risk edits. Use `luna-code` when the task remains bounded but needs more software-engineering judgment.

Routing is evidence-driven, not a Luna -> Sol -> Astra -> review ladder. One cohesive worker should own ordinary implementation whenever possible.

## Supporting agents

| Area | Agents | Purpose |
| --- | --- | --- |
| Ollama engineering | `autopilot-ollama`, `coder-ollama`, `general-lite-ollama`, `review-ollama` | Cost-first implementation and selective review |
| Operations | `ops-fast`, `context-glm`, `ops-autopilot-ollama` | Short checks, long/noisy context, and intentionally large operational workstreams |
| Repository/config | `github`, `config` | Git/GitHub lifecycle and OpenCode 2 configuration |
| Containment | `contained`, `contained-code-local`, `contained-net-research`, `contained-text-only` | Separate local execution from internet and lower-trust reasoning |
| Human-gated work | `gated-direct` | Engineering with approval-gated shell and external-directory access |
| Specialists | `cloudflare-expert`, `tutor-luna` | Cloudflare infrastructure and Socratic programming tutoring |
| Manual autonomy | `yolo` | Direct high-authority execution when intentionally selected |

OpenCode's built-in `explore` agent is used for generic read-only codebase scouting instead of maintaining a duplicate local explore agent.

## Design

- Use the cheapest capable model for the task.
- Prefer Luna High for cheap OpenAI utility work and Luna xHigh when bounded work needs more intelligence.
- Prefer one cohesive worker over chains of planners, coders, reviewers, and validators.
- Keep implementation workers as leaves unless nesting has a specific purpose.
- Offload long tests, logs, and broad synthesis so premium coding context stays focused.
- Use independent review only when risk or uncertainty justifies a separate reasoning path.
- Keep trust boundaries explicit. Contained agents separate local code authority from internet research.
- Keep project-specific workflow policy in project-local configuration, `AGENTS.md`, or skills rather than global prompts.

## Nested orchestration

Normal workflows are designed to work with one delegation hop.

For long-running autonomous work, `orchestrator-sol` and `ops-autopilot-ollama` provide deliberate nested-manager roles. Configure OpenCode 2's `experimental.subagent_depth` only when the hierarchy requires it. Extra orchestration layers should buy real context isolation, durable phase ownership, or useful fan-out rather than becoming the default path.

## Permissions

Agent files use native OpenCode 2 permission syntax with `permissions`, `shell`, and `subagent` actions. Common destructive operations are denied, external directory access is limited or approval-gated, and contained profiles use stricter separation.

Command blacklists are guardrails, not strong sandboxing. Use contained or external isolation when a real security boundary is required.
