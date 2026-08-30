# opencode-agents

Reusable agent definitions for [OpenCode](https://opencode.ai/).

## Install

Copy the agents you want into your global or project agent directory:

```text
~/.config/opencode/agents/
.opencode/agents/
```

Review each agent's model and permissions before use. Model availability depends on your configured providers, and project configuration can override global definitions.

## Agent groups

- `autopilot-codex.md` and its workers provide the established OpenAI-oriented lane.
- `autopilot-codex2.md` and its workers use native OpenCode V2 agent syntax for interactive cycle management.
- `orchestrator-codex.md` owns a bulk workstream via `/program` until complete, blocked, or out of scope. It reuses the Codex2 workers and does not replace `autopilot-codex2`.
- `autopilot-ollama.md` and the `*-ollama.md` workers provide the Ollama Cloud lane.
- `contained*.md` separates local code authority from internet research.
- `config.md`, `github*.md`, and `cloudflare-expert.md` provide specialized configuration and platform workflows.

OpenCode V2 accepts V1-compatible agent definitions. This repository intentionally contains both styles because the two autopilot lanes target different tested runtimes; it does not normalize working definitions merely for stylistic consistency.

## Model policy

The current Ollama Cloud definitions use `ollama-cloud/glm-5.3-flash`, with low reasoning for lightweight retrieval and operations and maximum reasoning for substantive work. OpenAI model IDs and variants reflect the configured routing ladder and may need to be adapted to your provider catalog.

## Safety

Permission rules are part of each agent definition. Read them before installation, keep credentials in environment variables, and avoid publishing resolved diagnostic output that may contain environment-provided secrets.
