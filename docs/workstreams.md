---
disabled: true
---

# Bounded workstreams with native tasks

Use `orchestrator` on GPT-6 Sol Medium to carry an approved plan through implementation, validation, review when warranted, authorized Git actions, and CI. This extends PR #1's model/context-locality decisions; it does not revert coding workers to the earlier Sol Medium default.

## Roles, not an agent tree

```text
orchestrator (Sol Medium)
  +-- sol-code (Sol High), or a bounded Astra escalation
  |     +-- ops-context: long tests, logs, evidence synthesis
  |     +-- ops-fast: short checks
  |     +-- luna-runner: an already-decided mechanical change
  +-- sol-review (Sol High): independent sibling
  +-- github: authorized Git/CI lifecycle
```

The three coding profiles allow only those three utility children. Utility and review workers cannot delegate. Review, model escalation, and Git authorization remain with the manager. `github` keeps its existing Ollama GLM configuration; no provider/model ladder is added. Other existing specialist and Ollama workflows remain available without becoming the default workstream path.

`direct` remains a model-switchable primary for human-led exploration and cohesive implementation. It is not made into a child manager. Use `sol-code`, `astra-code`, or `astra-code-medium` when delegation is the goal.

## OpenCode configuration

Merge [the small V2 settings fragment](../examples/workstreams.json) into the actual global/project config after inspecting precedence. It enables depth two with automatic compaction, a 15,000-token retained tail, a 20,000-token reserve, and bounded tool output. The example is a merge fragment, not a complete config file, and deliberately omits `$schema`.

OpenCode V2's current migration guide directs V2 users to `experimental.subagent_depth` and says the older top-level `subagent_depth` is unsupported V1 syntax. The current public `https://opencode.ai/config.json` schema is still compatibility-facing: it advertises the top-level key and does not presently admit the V2 experimental key. Treat that as an upstream transition mismatch, not permission to guess. On the installed `opencode2` version, verify the resolved configuration and an actual depth-two task before unattended adoption. If the installed release changes this surface, follow that release's V2 runtime/docs. Agent permissions must also allow the child: increasing depth alone does not grant delegation.

The other fragment fields are native V2 settings: `compaction.auto`, `compaction.keep.tokens`, `compaction.buffer`, and `tool_output.{max_lines,max_bytes}`.

Install the selected root agent Markdown files in `~/.config/opencode/agents/` or the project's `.opencode/agents/`. Do not install this guide or the example as an agent. Select `orchestrator` and **Sol Medium** explicitly for the manager session; selecting a primary agent does not necessarily replace a session's already-selected model. Check the resolved model before starting. Fixed child models remain in their agent files.

### Existing rcfiles integration

For a setup managed through rcfiles, reuse the existing `/program` command rather than adding a second launcher. In `.config/opencode/commands/program.md`, verify `agent: orchestrator`, `model: openai/gpt-6-sol#medium`, and `$ARGUMENTS` forwarding. Update stale command-level model overrides when installing these agent definitions.

Do not assume checked-in dotfiles are the host's resolved configuration. Inspect global, project, command, and session model selections before deployment. Preserve unrelated providers, MCP, security settings, and context limits. Use explicit `/program` selection rather than changing every project's default. This agent collection does not migrate rcfiles or install anything on a running host.

The fragment deliberately adds no provider overrides, warming, model-limit inflation, native-provider compaction policy, custom compaction tool, plugin, or service. Automatic compaction remains a fallback, not the main context-management strategy.

## Start with an authority contract

A useful `/program` request is:

```text
Complete the next accepted tranche of Issue <id> in <repository>.
Scope: <bounded objective and exclusions>.
Acceptance: <observable behavior plus required local/package/platform gates>.
Authority: edit and validate; stop before commit, push, merge, or release.
Budget: <optional cost/time/escalation limit>.
```

For unattended progress, explicitly grant the Git actions you want and identify the branch/PR boundary. A worker completing a task is not a reason for the manager to stop and ask you to transport the result. A new external contract, destructive operation, exhausted budget, or missing authorization is a reason to stop.

This is native tool-loop orchestration, not a background daemon. It still needs a running session, available providers, and resolved permissions. A stopped/cancelled/session-limited run resumes from its checkpoint; the agent must not promise execution after the runtime has stopped.

## Tasks as context boundaries

A task owns one cohesive outcome, not one command. The parent receives a compact final handoff and records the actual child session ID returned by the tool. Resume that child for tightly related corrections when useful. Start fresh for a new tranche or a deliberately independent review. Re-review can resume the original reviewer for focused finding closure.

Handoffs preserve status, changed scope, decisions, validation, uncertainty, and next action. They omit work diaries and raw output. A normal coding handoff is roughly 200-400 words; a clean review is usually shorter. These are targets, not limits that justify hiding findings. Large logs/manifests belong in task-specific local artifacts.

A final handoff **does not compact or erase the child history**. Repeatedly resuming a child can still grow its context. Retire completed children rather than carrying them across unrelated tranches. Do not churn useful context merely to reduce a token number, and do not preserve obsolete context merely because the model has room or cached input may be cheaper.

Native task sessions isolate conversation, not files or credentials. Use one active writer per shared checkout, pause edits during validation/review, and wait for utility children before reporting completion. Read-only profiles can still run repository tests with filesystem effects; shell rules are guardrails, not sandboxing.

## Recovery and acceptance evidence

The manager alone maintains `.opencode/work/current.md` in a locally ignored work directory. A sufficient checkpoint is:

```text
Objective / authorized actions / non-goals
Current tranche and next action
Checkout / branch / HEAD / relevant dirty-tree identity
Active child IDs, roles, status, and owned paths
Accepted decisions and open findings, with repository pointers
Validation: command, tested revision/tree, platform, result, log location
Git/CI: committed/pushed SHA, required checks and pending gates
```

Do not copy ROADMAP or OpenSpec into a second planning system. Native todos are a convenience for current steps, not authoritative recovery state. After compaction or resumption, verify the actual checkout and any running jobs before acting on the checkpoint. Store short task artifacts under the work directory or a task-specific temporary directory without committing sensitive logs.

A worker's `READY FOR REVIEW` is not independent approval. Review applies to the inspected tree, and tests apply to their tested tree/environment. Reuse unchanged evidence rather than rerunning a full suite for every comment edit; rerun affected checks when relevant bytes, dependencies, toolchain, or acceptance conditions change. Missing package or native-platform validation remains a missing gate.

## Bounded validation before adoption

After installing, use a disposable checkout and no commit/push authority to verify:

1. `orchestrator` launches `sol-code`; it can launch `ops-fast` or `ops-context` at depth two.
2. The coding worker cannot delegate a reviewer, another coder, a manager, or `github`; a utility cannot delegate further.
3. The manager commissions `sol-review` as a fresh sibling and can resume the same implementation child for a correction.
4. The parent receives compact handoffs with complete-log pointers, and waits for child completion rather than treating launch as success.
5. A fresh or compacted manager reconciles `.opencode/work/current.md` against a dirty checkout without losing work or repeating already-authorized mutations.

Agent files and instructions alone cannot prove runtime permission/continuation behavior. Check the resolved configuration on the actual installed version before relying on unattended operation.

## References

- [Agents and model/permission inheritance](https://opencode.ai/v2/docs/agents)
- [Native subagent tasks and continuation](https://opencode.ai/v2/docs/tools)
- [V2 depth and configuration migration](https://opencode.ai/v2/docs/migrate-v1)
- [Compaction semantics and limits](https://opencode.ai/v2/docs/compaction)
