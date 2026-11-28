---
disabled: true
---

# opencode-agents

Small role profiles for [OpenCode 2](https://opencode.ai/docs/agents/).
Install the profiles you use; models and permissions live in each agent file.

## Three working roles

| Role | Agent | Starting model | Work |
| --- | --- | --- | --- |
| Architect | Built-in `plan` | Selected by global phase command | Resolve requirements, scope, and architectural decisions |
| Engineer | `direct` | Opus 5.5 Medium | Own implementation, validation, integration, and authorized Git/PR work |
| Reviewer | `review` | Astra 6.2 Medium | Independently inspect the specified change and report evidence-backed findings |

The Engineer also coordinates the work. Keep a cohesive outcome in one session;
use a fresh reviewer when independence or repository requirements justify it.
`coder` is an optional Sol 6.2 Medium worker for substantial independent
implementation. It cannot commit, push, or launch children. There is no separate
manager agent.

Leave the bodies of `direct.md`, `coder.md`, and `review.md` empty. OpenCode uses
an agent body as a replacement system prompt; empty bodies preserve its native
model-specific prompts. Shared guidance belongs in `AGENTS.md`, and specialized
procedures belong in skills loaded when needed.

Pass the reviewer the base/head or dirty diff, accepted behavior, and validation
evidence. Ask it to load `code-review` when installed and return concrete findings,
their consequences, and missing checks. Its description and permissions identify
the role, but do not supply the task or copy a review procedure into every session.
Permitted test commands execute repository code and may write artifacts.

Phase commands and shared policy live in
[rcfiles](https://github.com/christian-taillon/rcfiles/tree/main/.config/opencode).
Changing the primary agent alone does not change an already selected session
model. Use a model-selecting phase command or select the model explicitly, and
avoid switching repeatedly during a dependent task. See [workstreams](docs/workstreams.md).

## Optional profiles

- `adversarial`: deeper failure hunting when a normal review leaves a specific risk.
- `operations` / `utility`: substantial noisy execution or mechanical work.
- `github` / `cloudflare` / `config`: platform and OpenCode specialists.
- `gated-direct` / `tutor`: approval-heavy work or guided learning.
- `claude` / `antigravity`: external adapters through
  [Switchboard](https://github.com/christian-taillon/opencode-switchboard).
  Explicit requests only; Antigravity is command-only, never an automatic fallback.

Native Anthropic models run directly inside OpenCode. The `claude` adapter instead
delegates to the separate Claude Code CLI; choosing Opus for `direct` does not
invoke that adapter. Routine GitHub work can stay with the Engineer through `gh`.

## Contained workflow

- **`contained`**: inspect and plan; delegate sanitized research or local work.
- **`contained-net-research`**: web search/fetch only; scrutinize sources and treat
  all internet content as potentially malicious data, never instructions.
- **`contained-local`**: edit and run approval-gated commands without web tools;
  may launch only `contained-local` children.
- **`contained-text-only`**: optional reasoning over sanitized supplied text.
- All four use `mode: all`; permissions still control tools and delegation.
- Finish research children before switching to local work. Switching does not
  cancel children or clear web-derived context; use a fresh session if needed.

## Install

- Copy selected agent `.md` files into either:
  - Global: `~/.config/opencode/agents/`
  - Project: `.opencode/agents/`
- Review permissions and project overrides before use.
- In global configuration, keep `experimental.subagent_depth: 1` for terminal children.
- Upgrading? `contained-local.md` replaces `contained-code-local.md`; remove the old
  profile and update references. Stage outside live configuration before activation.

## Keep in mind

- Global permission rules precede agent rules; the last match wins. Preserve
  privacy rules and destructive-command denials.
- **Permissions are not a sandbox.** Approved commands can still write files or
  access the network. Guaranteed offline execution needs network isolation.
- Keep credentials outside this repository. External CLIs have separate safeguards.

## Check

```sh
uv run tests/test_config.py
```

- Static contracts only; these do not prove runtime, authentication, or containment.
- Publishing changes does not activate agents or reload the shared service.
