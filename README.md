---
disabled: true
---

# opencode-agents

Reusable, opinionated agent definitions for [OpenCode](https://opencode.ai/).

This repository is a small agent toolbox for software engineering. It separates implementation, orchestration, review, repository operations, high-volume work, and contained research so each task can use an appropriate model and permission boundary.

Copy the agents you want into `~/.config/opencode/agents/` or a project's `.opencode/agents/` directory, then review their models, providers, and permissions.

## Features

- **Model-aware routing:** Luna for short and bounded work, Sol for general engineering, and Astra for unusually difficult or consequential work.
- **Dedicated orchestration:** primary agents can delegate implementation, operations, GitHub work, and independent review instead of doing everything in one context.
- **Low-cost volume lanes:** Ollama/GLM and Luna workers handle tests, logs, searches, repository synthesis, and mechanical tasks.
- **Independent review:** `sol-review` provides a separate read-only review context for correctness, architecture, security, compatibility, and difficult diagnosis.
- **Permission boundaries:** destructive Git and system commands are denied broadly, while external directory access is usually approval-gated or denied.
- **Contained workflows:** dedicated agents separate local code execution from internet research and lower-trust reasoning.
- **Specialized agents:** repository lifecycle, OpenCode configuration, Cloudflare, exploration, and tutoring each have focused roles.

## Core engineering agents

| Agent | Model | Purpose |
| --- | --- | --- |
| `luna-code` | GPT-5.6 Luna xHigh | Short, clear, low-risk implementation |
| `sol-code` | GPT-5.6 Sol Medium | Default implementation, debugging, refactoring, and integration |
| `astra-code` | GPT-6 Astra Medium | Difficult, subtle, security-sensitive, or consequential engineering |
| `sol-review` | GPT-5.6 Sol High | Read-only independent review and difficult diagnosis |
| `autopilot-sol` | GPT-5.6 Sol Medium | Evidence-driven engineering orchestration and acceptance decisions |
| `orchestrator-sol` | GPT-5.6 Sol Medium | Long-running workstreams with durable state across dependent phases |

`sol-code` is the default general-purpose coding agent. Use `luna-code` when the task is clearly bounded and straightforward, and select `astra-code` when the work genuinely benefits from additional capability. Routing is deliberate rather than a sequential escalation ladder.

## Supporting agents

| Area | Agents | Purpose |
| --- | --- | --- |
| Operations and context | `ops-autopilot-ollama`, `ops-fast`, `context-glm`, `openai-mini-runner` | Tests, builds, CI, logs, inventory, long-context analysis, and mechanical execution |
| Ollama toolbox | `autopilot-ollama`, `coder-ollama`, `general-lite-ollama`, `explore-ollama`, `planner-ollama`, `search-ollama`, `review-ollama`, `review-ollama-strict`, `manual-ollama-high` | Cost-efficient planning, implementation, exploration, search, and review |
| Exploration | `explore` | Fast read-only codebase exploration |
| Repository and configuration | `github`, `config` | Git/GitHub lifecycle and OpenCode configuration management |
| Containment | `contained`, `contained-code-local`, `contained-net-research`, `contained-net-remote`, `contained-text-only` | Separate local execution, internet access, remote research, and lower-trust reasoning |
| Human-gated work | `gated-direct` | Normal engineering with approval required before shell or external-directory access |
| Specialists | `cloudflare-expert`, `tutor-luna` | Cloudflare/infrastructure work and Socratic programming tutoring |
| Manual autonomy | `yolo` | High-authority autonomous execution when intentionally selected |

## Design

The agent set is built around a few simple ideas:

1. Use the cheapest capable model for the work instead of sending every task to the most expensive model.
2. Keep implementation, review, orchestration, operations, and repository lifecycle as separate responsibilities when that separation improves context quality or safety.
3. Offload noisy work such as tests, logs, searches, and large output analysis so premium coding context stays focused.
4. Use fresh, read-only review when independent reasoning is more valuable than preserving implementation context.
5. Make trust boundaries explicit. General coding agents usually ask before leaving the project directory, while contained agents use stricter isolation.

## Permissions

Each agent carries its own tool and command policy. Common safeguards include denying destructive Git operations, destructive system commands, and unrestricted privilege escalation. Sensitive files such as `.env` may require approval, and external directory access is intentionally limited.

Project-specific trusted paths and workflow requirements should be configured locally rather than weakening the global agent definitions.

Review an agent's model and permissions before installing it, especially the manual or high-authority profiles.
