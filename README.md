---
disabled: true
---

# opencode-agents

Reusable, opinionated agent definitions for OpenCode 2.

Primary agents describe **how work should be performed**. Model choice is separate because OpenCode lets you switch the active model for a primary session. Model-specific names are used mainly for subagents whose model must be fixed when delegated.

Copy the agents you want into `~/.config/opencode/agents/` or a project's `.opencode/agents/` directory, then review their models and permissions.

## Quick start

For most engineering work:

```text
direct + Sol Medium
```

For a request where you want OpenCode to decide what should be delegated:

```text
autopilot + Sol Medium
```

For a large, multi-phase, or long-running objective:

```text
orchestrator + Sol Medium
```

Choose the workflow first, then change the primary model when the task justifies it.

## Primary workflows

| Agent | Use it when |
| --- | --- |
| `direct` | You want one model to own the engineering task and preserve implementation, debugging, and validation context |
| `autopilot` | You want the primary to inspect the repository, make small direct changes, and route substantive work to workers |
| `orchestrator` | The objective is large, multi-phase, long-running, or benefits from durable state and context isolation |
| `contained` | You need separation between local execution and internet research |
| `gated-direct` | You want direct engineering with approval-gated shell and external-directory access |
| `tutor` | You want Socratic programming and engineering tutoring |
| `yolo` | You intentionally want high-authority direct execution |

The default model in a primary file is only a starting point. A primary workflow can be loaded and then switched to another model without needing another agent definition.

## Primary model selection

Use **Sol Medium as the default**. It provides the best general balance for implementation quality, debugging, architecture, and orchestration.

| Model | Recommended use |
| --- | --- |
| Luna xHigh | Cheaper, straightforward, bounded work where some quality tradeoff is acceptable |
| Sol Medium | Default for normal software engineering and orchestration |
| Astra Low | Hard work where more intelligence is useful without going to the normal Astra Medium tier |
| Astra Medium | Difficult, subtle, security-sensitive, architectural, or high-consequence work |

Practical defaults:

```text
Normal coding                 direct + Sol Medium
Cheap/simple coding           direct + Luna xHigh
Hard coding                   direct + Astra Low
Very hard/consequential code  direct + Astra Medium

Normal routed work            autopilot + Sol Medium
Cheap/light routing           autopilot + Luna xHigh
Difficult planning/routing    autopilot + Astra Low

Long-running work             orchestrator + Sol Medium
```

For mature codebases, optimize for **quality per accepted change**, not inference cost alone. A cheaper model is not a win if it creates unnecessary abstractions, tests, wrappers, cleanup, or follow-up work.

## Delegated workers

Subagents keep fixed models so routing remains deterministic.

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

## How the main workflows differ

### `direct`

Use this when you know what you want changed and want the selected model to keep the important implementation and debugging context itself. It may offload mechanical or noisy work, but substantive implementation stays in the primary session.

This is the normal choice when context preservation matters.

### `autopilot`

Use this when you want the primary to decide how the work should be performed. It can inspect the repository, understand files directly, update plans or documentation, make small obvious edits, and delegate substantive implementation to fixed-model workers.

Typical routing:

```text
mechanical work       -> luna-runner
normal engineering    -> sol-code
difficult engineering -> astra-code
independent review    -> sol-review
short operational work -> ops-fast
large/noisy context    -> context-glm
```

### `orchestrator`

Use this for a substantial workstream rather than an ordinary request. It maintains durable work state, owns dependent phases, and can survive context compaction or eventual supervision by a higher-level agent more cleanly.

It may read and edit files directly. The boundary is behavioral, not tool-based: small changes, planning, documentation, configuration, and integration are appropriate; sustained application implementation and debugging loops should usually be delegated.

## Design

- Optimize for accepted code quality, not raw inference cost alone.
- Use `luna-runner` for clearly mechanical cheap work; use `sol-code` as the normal floor for delegated software engineering.
- Prefer one cohesive worker over chains of planners, coders, reviewers, and validators.
- Primary orchestrators may read files, run useful commands, update plans and docs, change configuration, and make small obvious edits.
- Delegate sustained application implementation and debugging loops when separation improves context or quality.
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
