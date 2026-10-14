---
disabled: true
---

# opencode-agents

Permission-scoped OpenCode 2 profiles. Keep cohesive engineering in one context;
use a child only when independence, substantial context isolation, or a distinct
capability earns the handoff cost.

## Default workflow

`direct` investigates, implements, validates, and performs authorized routine Git
and `gh` work itself. A commit, normal push, or simple PR is not a reason to launch
another model. The engineer who changed the code reads its own failures.

`direct.md` and `coder.md` intentionally have **empty Markdown bodies**. They retain
model selection, descriptions, and ordered permissions while OpenCode supplies
its native model-specific system prompt. Do not add explanatory text below their
frontmatter: even one sentence replaces that default. Put shared project policy
in the applicable `AGENTS.md`, and task-specific procedures in selectively loaded
skills or the task itself. Do not paste Codex or upstream OpenCode prompts here.

This behavior is verified in the source of **OpenCode v2.0.26**. It is not proof
that a particular host, override, or future version resolves identically.

## Profiles

| Profile | Default | Reason to use |
| --- | --- | --- |
| direct | openai/gpt-6.1-sol#xhigh | One primary engineering context; native system prompt |
| coder | openai/gpt-6.1-sol#high | Substantial separable implementation; native prompt; no commit/push or children |
| review | openai/gpt-6.1-sol#high | Independent read-only assessment |
| adversarial | xai/grok-4.7 | Independent failure hunting |
| operations | openai/gpt-6-luna#high | Long/noisy execution and evidence isolation; no implementation |
| utility | openai/gpt-6-luna#medium | Settled mechanical edits where delegation actually pays |
| github | openai/gpt-6.1-sol#medium | Substantial remote lifecycle, release, or CI work; optional MCP access |
| cloudflare | openai/gpt-6.1-sol#high | Cloudflare-specific API/documentation capabilities |
| config | openai/gpt-6.1-sol#medium | OpenCode configuration and routing changes |

The existing model/effort defaults are deliberately retained, not claimed to be
optimal. Benchmark effort separately from this prompting change. Session model
selection is independent of primary-agent selection; verify the resolved pair.
A user-requested subagent model override selects that child's model. Do not
silently weaken a selection after provider failure.

The optional `gated-direct`, `tutor`, and `contained*` profiles remain distinct
human-approval, teaching, or trust workflows. Install only profiles you use.
Specialists keep short purpose-specific system prompts where an execution or
review contract is more useful than generic coding behavior. Empty bodies are
not a universal requirement.

## Long work without a manager hierarchy

Use one owner with terminal workers. The owner can implement directly, send a
bounded outcome to `coder`, inspect the diff and evidence, and resume that same
child for corrections. It finishes the accepted outcome rather than making the
user relay prompts. Independent review starts fresh. Dependent writers stay
sequential; independent concurrent writers need separate worktrees and an
integration owner. See [workstreams](docs/workstreams.md).

Keep `experimental.subagent_depth: 1`. `direct` remains `mode: all`, but no
self-delegation route is enabled. A narrower `coder` preserves the useful
permission boundary without another coding prompt. No recursive manager chain,
mandatory planning/review chain, scheduler, or prompt-merging plugin is needed.

## Tool visibility and permissions

Profiles start deny-by-default and allow named capabilities. OpenCode v2.0.26
filters wholly denied tools before building the direct tool list and Code Mode
catalog. Skills and MCP server instructions have their own permission-aware
filters. A connected server is not necessarily visible to every agent.

Default MCP tools run through Code Mode. `github` and `cloudflare` therefore allow
`execute` **and** only their intended nested MCP tool names. `execute` does not
bypass nested checks. Other roles do not gain these MCP tools or Switchboard
access. Connecting a disabled server remains a separate configuration change.

Global rules precede agent rules; the last matching rule wins. Project overrides,
saved approvals, plugins, and managed policy must also be considered. Permission
patterns are guardrails, not OS containment: shell commands and tests can write
files or access the network. Preserve hard privacy policies, destructive-command
denials, and each profile's authority. Do not interpret a static pass as a sandbox
or live-runtime qualification.

## External harnesses

`claude` and `antigravity` remain optional terminal adapters through independently
installed [Switchboard](https://github.com/christian-taillon/opencode-switchboard).
Their bodies and external model/effort, continuation, and failure contracts are
unchanged. Install and authenticate vendor CLIs separately.

Keep `/claude` and `/antigravity` as explicit commands with their respective
`agent` and `subagent: true`. `direct` may delegate to `claude` only on an explicit
user request; preserve that selection rule in ambient `AGENTS.md`. Antigravity
remains explicit-command-only. Neither is an automatic fallback. The direct
Switchboard tools remain denied to ordinary engineering profiles.

The OpenCode wrapper's model is not the external CLI's model. Vendor tools do not
inherit OpenCode shell hooks or permission enforcement. Keep vendor configuration
and credentials outside this public repository. The ordinary workflow requires
neither adapter.

## Installation and migration

Install selected root-level agent Markdown files into
`~/.config/opencode/agents/` or a project's `.opencode/agents/`. Review permissions
first. Documentation is `disabled: true` to avoid accidental agent discovery.
Keep provider credentials, private host settings, and active recovery state out
of this repository.

This revision removes `autopilot`. Its durable owner loop belongs in an explicit
`/work` command/skill using `direct`, `subagent: false`, and an explicitly selected
model. Update all installed `/program` overrides and references at the same time;
remove the old agent and command rather than keeping aliases. The companion
configuration supplies the workstream skill. Stage outside live configuration
because files can auto-reload. Keep active sessions intact until controlled
activation; an agent removal does not safely migrate their stored selections.

An empty `direct` body also means shared authority rules must remain available:
follow repository policy; preserve unrelated changes; protect environment files;
authorize publication explicitly; delegate only when it earns its overhead;
forward bounds and validation to children; select external adapters only on
explicit request. Skills are procedures, not enforcement. V2.0.26 accepts a config
`instructions` array without resolving it; use actual `AGENTS.md` files.

## Validation and evaluation

```sh
uv run tests/test_config.py
uv run tests/test_config.py --config /path/to/sanitized-candidate.json
```

The default uses a portable fixture, not personal configuration or credentials.
The suite checks native shapes, empty engineering bodies, ordered permissions,
terminal routes, adapter isolation, MCP Code Mode access, and privacy contracts.
CI runs it on PRs. It does not emulate a provider, validate live authentication,
or prove engineering-quality improvement.

Before activation verify the installed schema and actual provider-bound request:
native GPT/Astra prompt present once; private policy still present; irrelevant
MCP tools/instructions absent; allowed specialist tools reachable; children and
external adapters retain their boundaries. Redact credentials and private code.

Then compare baseline and candidate on identical clean worktrees, same model and
effort, and representative bug-fix, refactor, Git-only, and long-work tasks.
Measure acceptance, regressions, human corrections, unnecessary delegations,
time, and available token/cache usage. Repeat representative cases; one successful
run is not a general result. Keep a dated local record, not another service.

## Design evidence

- [OpenCode prompt selection](https://github.com/anomalyco/opencode/blob/v2.0.26/packages/core/src/plugin/optimize.ts) and [base transcript](https://github.com/anomalyco/opencode/blob/v2.0.26/packages/core/src/session/model-request.ts): a non-empty custom system bypasses the native model prompt.
- [Tool snapshot](https://github.com/anomalyco/opencode/blob/v2.0.26/packages/core/src/tool.ts) and [MCP instructions](https://github.com/anomalyco/opencode/blob/v2.0.26/packages/core/src/mcp/instructions.ts): visibility and Code Mode reachability are distinct from prompt text.
- [OpenAI harness engineering, February 2026](https://openai.com/index/harness-engineering/): make repository knowledge navigable and validate outcomes mechanically. Its throughput/merge choices are not blanket policy for other projects.
- [Anthropic context engineering, September 2025](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents): use high-signal context and just-in-time retrieval, not exhaustive instructions.
- [Anthropic multi-agent research, June 2025](https://www.anthropic.com/engineering/multi-agent-research-system): delegation helps independent breadth but adds cost. Its research results and token multipliers are not coding benchmarks.
