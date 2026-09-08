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

## Codex2 routing

`autopilot-codex2` is the Sol Medium strategic control plane. It routes normal implementation to `coder-luna` (Luna High); `coder-astra` (Astra Low) is reserved for unusually difficult, subtle, or consequential implementation and is not a routine second pass. `coder-luna-max` remains available to other or manual workflows but is not exposed to Codex2.

Specialized workers are used by role: `review-terra` for independent review or difficult diagnosis, `advisor-sol` for architecture, security, and consequential tradeoffs, `ops-fast` for short mechanical checks, `github-ollama` for GitHub and CI operations, and `ops-autopilot-ollama` for large bounded operational workstreams. The latter may use `context-glm` for large or noisy work. There is no automatic escalation ladder; routing is evidence-driven.

## Model policy

The current Ollama Cloud definitions use `ollama-cloud/glm-5.3` (non-Flash) for judgment agents — orchestration, planning, implementation, review, GitHub, config, and contained agents — and `ollama-cloud/glm-5.3-flash` for lightweight retrieval and operations workers. OpenAI model IDs and variants reflect the configured routing ladder and may need to be adapted to your provider catalog.

## Safety

Permission rules are part of each agent definition. Read them before installation, keep credentials in environment variables, and avoid publishing resolved diagnostic output that may contain environment-provided secrets.
