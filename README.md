---
disabled: true
---

# opencode-agents

Opinionated agent definitions for OpenCode 2, tuned for code quality over token economy.

Copy the agents you want into `~/.config/opencode/agents/` or a project's `.opencode/agents/`, then review their models and permissions.

The flat layout is deliberate: OpenCode 2 derives agent IDs from paths, so moving `review.md` to `specialists/review.md` renames `review` to `specialists/review`. Markdown documentation under the agent tree uses `disabled: true` so it is not selectable.

## Companion: Switchboard

[OpenCode Switchboard](https://github.com/christian-taillon/opencode-switchboard) provides the plugin execution/session contract and standalone wrapper templates for external harness subagents. This repository provides opinionated parent routing and customized agent definitions, including `claude` and `antigravity`.

Install the backend using [Switchboard's installation instructions](https://github.com/christian-taillon/opencode-switchboard#install); its [optional native profiles](https://github.com/christian-taillon/opencode-switchboard#optional-native-subagent-profiles) are standalone alternatives to these customized wrappers. See its [delegation contract](https://github.com/christian-taillon/opencode-switchboard/blob/main/skills/switchboard/SKILL.md) for task and session handling.

The repositories are installed and updated separately; neither automatically synchronizes the other. Generic Switchboard use does not require this agent collection or its routing policy.

## Design

Three ideas drive the routing:

1. **The engineer who changes code runs its tests.** Raw failures are the most valuable signal in a coding loop; summaries lose it. Owners run their own checks and hand only very long or noisy runs to `ops-context`, keeping the diagnosis.
2. **Claude Code is the primary coder and planner.** Substantive work goes to `claude` (Opus 5.5): plan in `plan` mode, check the plan, then resume the same session in `full` mode to implement. Routine, well-specified work stays on GPT-6.1 Sol High (`direct` or `code`).
3. **Review crosses model families.** A different family catches different defects. Claude-authored changes are reviewed by `review` (Sol High); OpenAI- or Gemini-authored changes by `claude` in `plan` mode with Opus 5.5. `adversarial` (Grok 4.7) adds failure hunting for high-consequence changes.

Keep topology shallow. Every handoff loses context, so a child must buy isolation, independence, a specialist boundary, or real parallelism.

## Primary workflows

| Agent | Model | Use it when |
| --- | --- | --- |
| `autopilot` | Sol High | Default. One outcome: plan, route to `claude` or `code`, review, accept |
| `direct` | Sol High | Routine engineering, or when this conversation's context matters most; does the work itself |
| `orchestrator` | Sol High | A multi-tranche workstream (`/program`): sequences tranches to `claude`/`code`, reviews, keeps a checkpoint |
| `gated-direct` | Sol High | Human approval before host commands or access outside the project |
| `contained` | Sol Medium | Separate trust boundaries for local code, network research, and text-only reasoning |
| `tutor` | Luna High | Socratic teaching without implementing |
| `yolo` | Sol High | Manual-only high-authority direct implementation |

```text
autopilot / orchestrator
  +-- claude  (Claude Code via Switchboard; Opus 5.5)  substantive plan + implement
  +-- code    (Sol High)                               routine implementation
  +-- review  (Sol High) | claude plan-mode (Opus)     cross-family review
  +-- adversarial (Grok 4.7)                           failure hunting
  +-- ops-context / ops-fast / qwen-task / utility     long runs, quick checks, mechanical edits
  `-- github / config / cloudflare-expert              specialist boundaries
```

`orchestrator` dispatches tranches straight to the implementing worker, with no intermediate control plane. `subagent_depth: 3` covers `orchestrator -> code -> ops-*`.

## Workers

| Agent | Default model | Role |
| --- | --- | --- |
| `claude` | Luna High wrapper -> Claude Code Opus 5.5 | Substantive implementation, planning, and cross-family review through Switchboard |
| `antigravity` | Luna High wrapper -> Gemini 3.8 Flash | Independent Gemini attempt or broad cross-file synthesis through Switchboard |
| `code` | Sol High | Routine, well-specified implementation and debugging |
| `review` | Sol High | Independent read-only review |
| `adversarial` | Grok 4.7 | Read-only failure hunting: breaking inputs, states, interleavings |
| `ops-context` | Sol Medium | Long tests and builds, large logs, evidence synthesis |
| `ops-fast` | Luna High | Short focused commands and lookups |
| `qwen-task` | Ollama Qwen | Cheap resumable reruns and repetitive commands |
| `utility` | Luna Medium | Explicit mechanical edits, docs, simple configuration |
| `github` | Sol Medium | Git and GitHub lifecycle |
| `config` | Sol Medium | OpenCode configuration and agent-definition repairs |
| `cloudflare-expert` | Sol High | Cloudflare infrastructure |

The wrappers (`claude`, `antigravity`) are thin: they translate a task into one Switchboard delegation and return the result. The OpenCode `subagent` `model` parameter changes only the wrapper; pass `externalModel` and `externalEffort` in the task prompt to select the external model. External harnesses do not inherit OpenCode permissions or hooks, so parents state applicable policy in the task.

Autonomous child-model overrides are limited to Luna Medium/High, Sol Medium/High, and Astra Medium. A model the user names explicitly is always honored; use `/models` for exact IDs.

## Permissions

Agent files use OpenCode 2 ordered permission rules (`action`, `resource`, `effect`). Global rules apply before agent rules and the last match wins, so the broad-deny-then-allow pattern here is intentional. A child uses its own permissions; the parent's `subagent` rules only decide which children it may launch. Command deny lists are guardrails, not a sandbox.

The global configuration also hard-denies read access to `*.env` and `*.env.*` and shell commands naming `.env`. These policies override agent allows and saved approvals, but they are not OS isolation. Only `config` may load `customize-opencode`.

## Contract checks

After changing agents or global routing and permissions, run:

```sh
uv run tests/test_config.py
```

It checks agent shapes, ordered permission and hard-policy behavior, default and specialist routing, the review boundary, skill isolation, and the routing topology. It reads configuration without resolving credentials and never opens environment files. It does not prove runtime behavior; use `--config` and `--agents` for another installation.
