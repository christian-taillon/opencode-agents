---
disabled: true
---

# opencode-agents

Reusable, opinionated agent definitions for OpenCode 2.

Primary agents describe **how work should be performed**. Model choice is intentionally separate because OpenCode lets you switch the active model for a primary session. Model-specific names are reserved mainly for subagents whose model must be fixed when they are delegated.

Copy the agents you want into `~/.config/opencode/agents/` or a project's `.opencode/agents/` directory, then review their models and permissions.

## Primary workflows

| Agent | Purpose |
| --- | --- |
| `direct` | Own one engineering task in the primary context, preserving implementation and debugging state |
| `autopilot` | Normal engineering control plane for inspection, light direct edits, routing, and acceptance |
| `orchestrator` | Durable long-running workstream manager for multi-phase or intentionally nested work |
| `contained` | Security-oriented workflow that separates local execution from internet research |
| `gated-direct` | Direct engineering with approval-gated shell and external-directory access |
| `tutor` | Socratic programming and engineering tutoring |
| `yolo` | High-authority direct execution when intentionally selected |

The default model in a primary file is a starting point, not part of the workflow identity. For example, `direct` can be run with Luna, Sol, or Astra depending on the task while preserving the same direct-work behavior.

## Delegated workers

| Agent | Fixed role |
| --- | --- |
| `luna-runner` | Luna High utility worker for commands, tests, docs, simple configuration, and mechanical edits |
| `sol-code` | Sol Medium default delegated software-engineering worker |
| `astra-code` | Astra Medium worker for difficult or consequential engineering |
| `sol-review` | Sol High independent read-only review |
| `coder-ollama` | Cost-first Ollama implementation worker |
| `general-lite-ollama` | Cheap Ollama mechanical/configuration worker |
| `review-ollama` | Cost-first Ollama reviewer |
| `ops-fast` | Short operational checks and focused commands |
| `context-glm` | Long tests, logs, repository synthesis, and other noisy context-heavy work |
| `ops-autopilot-ollama` | Intentionally large operational sub-workstream manager |
| `github` | Git and GitHub lifecycle specialist |
| `config` | OpenCode 2 configuration specialist |
| `cloudflare-expert` | Cloudflare infrastructure specialist |

Containment also uses `contained-code-local`, `contained-net-research`, and `contained-text-only` as trust-boundary helpers.

## Choosing a primary

Use `direct` when you know the task and want one model to retain the important implementation, debugging, and validation context.

Use `autopilot` when you want the primary to inspect the repository, make small direct changes when appropriate, and route substantive work to fixed-model workers.

Use `orchestrator` when the objective is large enough to benefit from durable state, several dependent phases, context isolation, or eventual supervision by another agent.

## Design

- Optimize for accepted code quality, not raw inference cost alone.
- Use `luna-runner` for clearly mechanical cheap work; use `sol-code` as the normal floor for delegated software engineering.
- Prefer one cohesive worker over chains of planners, coders, reviewers, and validators.
- Primary orchestrators may read files, run useful commands, update plans and docs, change configuration, and make small obvious edits. They should delegate sustained application implementation and debugging loops.
- Offload long tests, logs, and broad synthesis so premium engineering context stays focused.
- Use independent review only when risk or uncertainty justifies a separate reasoning path.
- Keep trust boundaries explicit. Contained agents separate local code authority from internet research.
- Keep project-specific workflow policy in project-local configuration, `AGENTS.md`, or skills.

## Nested orchestration

Normal workflows should remain shallow. For long-running autonomous work, `orchestrator` can itself be delegated when OpenCode 2's `experimental.subagent_depth` is configured to permit the hierarchy. `ops-autopilot-ollama` provides the same pattern for a large bounded operational sub-workstream.

Extra orchestration layers should buy real context isolation, durable phase ownership, or useful fan-out rather than becoming the default path.

## Permissions

Agent files use OpenCode 2 permission rules with `action`, `resource`, and `effect`. Common destructive operations are denied, external-directory access is limited or approval-gated, and contained profiles use stricter separation.

Command blacklists are guardrails, not strong sandboxing. Use contained or external isolation when a real security boundary is required.
