---
disabled: true
---

# opencode-agents

Reusable agent definitions for [OpenCode](https://opencode.ai/). Copy the
agents you need into `~/.config/opencode/agents/` or a project's
`.opencode/agents/` directory, then review their models and permissions.

## OpenAI engineering architecture

| Agent | Model | Purpose |
| --- | --- | --- |
| `luna-code` | Luna xHigh | Short, clear, bounded coding |
| `sol-code` | Sol Medium | Default software engineering |
| `astra-code` | Astra Medium | Difficult, subtle, consequential engineering |
| `sol-review` | Sol High | Independent review, architecture, difficult diagnosis |
| `autopilot-sol` | Sol Medium | Strategic task orchestration |
| `orchestrator-sol` | Sol Medium | Long-running autonomous workstreams |

`sol-code` is the default coding agent. Choose `luna-code` deliberately for
clearly easy work and `astra-code` deliberately when concrete evidence shows
that additional capability matters. This is evidence-driven routing, not a
sequential escalation ladder. Do not automatically run Luna, then Sol, then
Astra, then review.

The coding agents use `mode: all` so a human can select them directly or an
orchestrator can invoke them as subagents. `sol-review` is read-only and uses a
fresh child context when independent reasoning is the point of the review.
Continue the same worker task/session for cohesive follow-up when its prior
investigation remains useful; start fresh for independent work, a different
model, or intentional independent review.

Astra High is a manual, exceptional override only. It has no automatic route
or dedicated agent here. Astra xHigh and Astra Max are prohibited, and Terra is
not part of the normal coding/orchestration graph.

## Supporting lanes

- `autopilot-ollama.md` and the `*-ollama.md` agents handle volume work.
  Prefer `ops-autopilot-ollama`, `context-glm`, and `ops-fast` for long tests,
  builds, logs, inventory, and other noisy operations.
- `github` is the repository and GitHub lifecycle specialist, using Luna High
  for Git state, commits, branches, pull requests, releases, and CI operations.
  Repository-specific workflow policy belongs in project-local skills rather
  than the global agent definition.
- `gated-direct.md` preserves a human approval boundary for shell and external
  directory operations.
- `contained*.md` separates local code authority from internet research.
- `config.md`, `github.md`, and `cloudflare-expert.md` provide specialized
  configuration, GitHub, and platform workflows.
- `tutor-luna.md` is a separate Socratic programming tutor and does not write
  solutions or delegate implementation.

## Migration from the previous OpenAI graph

| Old name | New name or disposition |
| --- | --- |
| `codex-direct` | `sol-code` |
| `coder-luna` | `luna-code` |
| `coder-astra` | `astra-code` |
| `review-terra`, `advisor-sol` | `sol-review` |
| `autopilot-codex`, `autopilot-codex2` | `autopilot-sol` |
| `orchestrator-codex` | `orchestrator-sol` |
| `coder-codex`, `coder-luna-max`, `sol-escalation`, `escalation`, `coder-quality` | Removed as duplicates or automatic escalation paths |

No compatibility aliases are retained. External commands, project overrides,
or scripts that select an old name must be updated to the new name.

## Safety

General coding and orchestration agents use `external_directory: ask`. Trusted
external development paths should be allowed through project-local OpenCode
configuration rather than globally weakening agent permissions.

The `mode: all` coding agents keep this approval boundary when invoked as
subagents, so legitimate external access may prompt there too. A stricter
parent/session or project policy can still constrain a child and must not be
bypassed. Contained and isolation-focused agents intentionally retain
`external_directory: deny`.

To avoid repeated prompts for a trusted path, append a narrow per-agent rule in
the project's `opencode.json(c)`:

```jsonc
{
  "agents": {
    "sol-code": {
      "permissions": [
        {
          "action": "external_directory",
          "resource": "~/projects/shared/*",
          "effect": "allow"
        }
      ]
    }
  }
}
```

Permission rules are part of each agent definition. Read them before
installation, keep credentials in environment variables, and do not publish
resolved OpenCode diagnostics because they can contain environment-provided
secrets.
