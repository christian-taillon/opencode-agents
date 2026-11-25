---
disabled: true
---

# opencode-agents

Permission-scoped agents for [OpenCode 2](https://opencode.ai/docs/agents/).
Install the profiles you need; models and permissions live in each agent file.

## Pick an agent

- **`direct`** — everyday engineering, validation, and authorized Git/PR work.
- **`coder`** — bounded implementation work; no commits, pushes, or children.
- **`review` / `adversarial`** — independent reviews and failure hunting.
- **`operations` / `utility`** — noisy execution / small mechanical edits.
- **`github` / `cloudflare` / `config`** — platform and OpenCode specialists.
- **`gated-direct` / `tutor`** — approval-heavy work / guided learning.
- **`claude` / `antigravity`** — optional external adapters through
  [Switchboard](https://github.com/christian-taillon/opencode-switchboard).
  Explicit requests only; Antigravity is command-only, never an automatic fallback.

## Contained workflow

- **`contained`** — inspect and plan; delegate sanitized research or local work.
- **`contained-net-research`** — web search/fetch only; scrutinize sources and treat
  all internet content as potentially malicious data, never instructions.
- **`contained-local`** — edit and run approval-gated commands without web tools;
  may launch only `contained-local` children.
- **`contained-text-only`** — optional reasoning over sanitized supplied text.
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

- Keep one owner; delegate only when independence or specialization helps.
  See [workstreams](docs/workstreams.md).
- Leave `direct.md` and `coder.md` bodies empty to retain native model prompts.
  Put shared behavior in `AGENTS.md`.
- Global permission rules precede agent rules; the last match wins. Preserve
  privacy rules and destructive-command denials.
- **Permissions are not a sandbox.** Approved commands can still write files or
  access the network. Guaranteed offline execution needs network isolation.
- Keep credentials outside this repository. External CLIs have separate safeguards.

## Check

```sh
uv run tests/test_config.py
```

- Static contracts only—not runtime, authentication, or containment proof.
- Publishing changes does not activate agents or reload the shared service.
