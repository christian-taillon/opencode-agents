---
disabled: true
---

# opencode-agents

Generic OpenCode 2 roles, optimized for correct, maintainable work before cost.

## Flat design

```text
direct (default) / autopilot
  +-- coder / review / adversarial
  +-- utility / operations
  `-- config / github / cloudflare
```

Maximum one OpenCode delegation hop. Every worker is terminal, enforced by
ordered permissions as well as instructions. Missing expertise returns to the
primary, which may commission another independent leaf. No manager-to-manager,
coder-to-operations, or reviewer-to-reviewer chain.

**Direct** keeps design, implementation, debugging, validation, and judgment in
one context. Delegate only for real independence, specialty, isolation, or useful
parallelism. Its intentional `mode: all` and Sol XHigh default are preserved;
if explicitly invoked as a child it must not delegate. Depth `1` blocks that
second hop even though its primary permissions permit named leaves.

**Autopilot** owns an accepted outcome. It can implement directly or commission
bounded leaves, inspect evidence, correct, and continue accepted phases. Only
substantial work needs its single private recovery checkpoint. `/program` selects
Autopilot, not an intermediary. See [workstreams](docs/workstreams.md).

## Inventory and defaults

| Role | Default | Responsibility |
| --- | --- | --- |
| direct | openai/gpt-6.1-sol#xhigh | Default single-context engineer; mode all |
| autopilot | openai/gpt-6.1-sol#high | Outcome-owning primary |
| coder | openai/gpt-6.1-sol#high | One cohesive engineering outcome |
| review | openai/gpt-6.1-sol#high | Independent read-only assessment |
| adversarial | xai/grok-4.7 | Read-only failure hunting |
| utility | openai/gpt-6-luna#medium | Settled mechanical edits/checks |
| operations | openai/gpt-6-luna#high | No-edit execution, retrieval, noisy evidence |
| config | openai/gpt-6.1-sol#medium | OpenCode definitions/configuration |
| github | openai/gpt-6.1-sol#medium | Authorized Git/GitHub lifecycle |
| cloudflare | openai/gpt-6.1-sol#high | Cloudflare infrastructure; stronger existing default retained |

Identity denotes responsibility, not a model. Use native agent `model:
provider/model#variant`, normal model selection, or the V2 subagent `model`
override. Honor explicit user selection. Reasoning, continuity, and validation
come before cost; never silently weaken a selection after failure. Other
configured non-Anthropic models, including Astra and local models, are selectable
when justified. No rigid cheap-first routing or inference of availability from spend.
For repetitive operations the previous local selection remains available as
`operations` with `model: ollama/qwen3.8:27b`; for deeper evidence synthesis use
a justified override such as `openai/gpt-6.1-sol#medium`. Check configured model
availability before selecting, rather than creating model-named roles.

Selecting a primary agent by ID does not change the session's stored model.
Select the intended model/variant explicitly for an existing session; the root
default model does not retain variants. Agent/command references and native
subagent model overrides avoid model-named worker identities.

The engineer who changes code runs checks and reads failures. A primary may
commission operations separately when isolation helps. Commission fresh
independent review when risk or policy warrants it, optionally across model
families; add adversarial review for consequential failure modes. Reviews are not
automatic planning/implementation/escalation chains.

### Optional human-selected profiles

- `gated-direct`: normal project edits, approval-gated shell/external access;
  terminal even when invoked as a child.
- `tutor`: Socratic teaching, no implementation or delegation.
- `contained`: primary separating trust boundaries. Its terminal
  `contained-code-local`, `contained-net-research`, and `contained-text-only`
  leaves retain local/no-network, public-internet/no-repository, and sanitized
  text-only boundaries respectively. Tool permissions are not an OS sandbox.

### Optional external adapters

`claude` and `antigravity` are explicit user selections, not ordinary workflow
routes or fallbacks. They are terminal OpenCode adapters through independently
installed [Switchboard](https://github.com/christian-taillon/opencode-switchboard).
The ordinary workflow works without either adapter or plugin. These files alone
own external harness/model/effort selection, mode, continuation, permission
boundaries, and failure handling. Their OpenCode model changes only the wrapper;
`externalModel`/`externalEffort` select the external process. External processes
are integration calls, not additional OpenCode delegation hops, and do not inherit
OpenCode permission enforcement. Never copy external vendor configuration here.

After installing the plugin and both wrapper files, separately merge the tiny
[optional command fragment](examples/switchboard.json) to enable `/claude` and
`/antigravity`. These explicit user commands create native background children,
using each wrapper's configured Luna High model. They are separate from `/program`
and do not grant ordinary primaries adapter-launch permissions. `@claude` text
alone is not a supported entry point under this routing policy. External task
model/mode/authority remains the dedicated adapter's responsibility. Review any
installed command overrides before activation; neither commands nor plugin are
installed automatically by this repository.

## Installation and configuration

Review models and permissions before copying selected files into global
`~/.config/opencode/agents/` or project `.opencode/agents/`. Keep the flat layout:
paths define IDs. Documentation in the tree is `disabled: true`.

Global configuration is applied first. Discovered project direct configs are
merged farthest-to-closest, then `.opencode` configs farthest-to-closest; local
agent/command overrides can change the result. Inspect them before activation.
Markdown agents own behavior; do not duplicate their prompts in JSON.
Use `AGENTS.md` for active global/project guidance: the config `instructions`
array currently accepts entries but does not resolve them.

V2.0.26's installed schema and runner support:

```json
{"default_agent":"direct","experimental":{"subagent_depth":1}}
```

Top-level `subagent_depth` is unsupported in that version. The runner counts the
calling session's ancestors: primary depth `0` may launch a leaf; leaf depth `1`
cannot launch again. Verify against the installed version on upgrades, rather
than assuming the public schema is V2. [Example](examples/workstreams.json)
contains the flat `/program` command and optional output/compaction settings.
The command explicitly sets `subagent: false` to stay in the current session,
with its existing Sol High model selection. Native child sessionIDs, relevant
skills, compaction, and Git worktrees supply continuity and isolation; no custom
scheduler, shared instruction framework, or new plugin is required.

Global permission rules precede agent rules; last matching rule wins. Children
use their own permissions; parent rules select callable IDs. Keep destructive
denials and hard privacy policies, including environment-file read/shell denials.
Only `config` may load `customize-opencode`. Broad shell access is not a sandbox;
tests can write artifacts and command deny lists are guardrails.

Direct retains native Code Mode `execute` access. That permission enables the
runtime, not every nested tool: each nested tool remains subject to its own
rules. The primary's broad-deny-first policy still denies unallowed integration
tools. No Code Mode access is added to profiles that deliberately lacked it.

V2.0.26 hard permission policies use `experimental.policies` with action
`tool.use` and resources such as `read:*.env` or `shell:*.env*`. Its policy hook
hard-denies matching permission checks. Current public policy docs describe
`action: permission`, while pinned V2.0.26 source and the inspected installed
executable's embedded schema and enforcement hook use `tool.use`. This is a
version-dependent migration: guard the old rules and rename the action only
after verifying the target implementation, preserving resources and deny
effects. Static executable inspection does not qualify the running server or
active policy enforcement.

## Migration (no aliases)

| Previous ID | Replacement | Decision |
| --- | --- | --- |
| code | coder | One generic coding responsibility |
| cloudflare-expert | cloudflare | Same specialist/model/permissions, shorter responsibility ID |
| orchestrator | autopilot | Bounded phases and durable recovery absorbed |
| ops-fast, ops-context | operations | Same no-edit authority; scope/model override selects effort |
| qwen-task | operations with explicit local model override | No-edit/destructive restrictions retained or strengthened; broader operational tools |
| yolo | direct | No unique trust boundary beyond direct execution; direct remains authoritative |

Operations deliberately has broader operational tools than the previous local
task profile: external-directory access asks and web tools are allowed. Its
no-edit/destructive restrictions are retained or strengthened; this is not a
claim that every former permission was equally restrictive.

Other original roles are retained or optional as listed above. No compatibility
aliases remain. Remove old files, routes, command IDs, and project/global instruction
references deliberately. Change `/program`'s agent to `autopilot`; live Markdown
command overrides must also be migrated, not just a JSON example.

The staged safety migration removes unconditional temporary-delete allows (a
wildcard also matches traversal or extra arguments), preserves approval for those
deletes, and keeps important force-push/reset/sudo denies after Plan's broad shell
ask. Broad-shell specialists also deny short `git push -f`. These are narrow
ordering corrections, not a shell sandbox or a comprehensive command parser.

Apply guarded JSON Patch operations only to an in-memory copy. Complete every
precondition and operation, including the full expected safe `experimental`
object, before atomically persisting a separately authorized result. A changed or
existing nested depth must fail closed, not be overwritten by `add`. Never persist
partial results after a failed test or copy credential-bearing configs into a
candidate or diagnostic. Verify the target implementation separately.

Prepare changes outside a live installation: native config and command files can
auto-reload, so isolation is necessary even without an explicit restart. Never
overwrite dirty input or copy
a credential-bearing config. Apply only reviewed routing/depth patches, preserving
providers, personal models, policy, and unrelated settings. Activation is separate
authority: drain work and close clients before an operator changes/restarts the
native shared service. Keep old active sessions intact until then; native clients
can respawn the server. Do not start a private server as a workaround.

## Validation

```sh
uv run tests/test_config.py
uv run tests/test_config.py --config /path/to/sanitized-installation-candidate.json
```

The default uses the tracked sanitized fixture, never a personal global config.
The explicit option checks supplied configuration without interpolation or printing
its values. Do not supply environment files or symlinks. Tests check static fields,
named routes, depth, last-match permission outcomes, role boundaries, and adapter isolation;
they do not simulate a sandbox or qualify a running server. Validate candidate
normalization against the pinned installed V2 schema before activation, then perform
separately authorized runtime checks. Source/static passes are not runtime proof.
The supplied candidate is treated as a global document followed by its Markdown
agent directory, matching the pinned loader. Later project overrides, saved
approvals, managed policies, arbitrary scripts, and grep resource semantics remain
outside this bounded static proof; validate those separately where acceptance needs them.

References: [V2 agents](https://opencode.ai/v2/docs/agents),
[config](https://opencode.ai/v2/docs/config),
[permissions](https://opencode.ai/v2/docs/permissions),
[policies](https://opencode.ai/v2/docs/policies),
[models](https://opencode.ai/v2/docs/models),
[commands](https://opencode.ai/v2/docs/commands),
[instructions](https://opencode.ai/v2/docs/instructions),
[skills](https://opencode.ai/v2/docs/skills),
[compaction](https://opencode.ai/v2/docs/compaction).
