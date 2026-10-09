---
disabled: true
---

# Bounded workstreams with Claude/Code execution

`orchestrator` is the durable development manager. It owns architecture and planning context, sequencing, recovery, acceptance, and the user conversation. `autopilot` is a standalone engineering control plane, never an orchestrator child.

## Topology

```text
orchestrator (primary)
  +-- claude / code (foreground bounded tranche)
  |     +-- ops-context / ops-fast / qwen-task / utility
  +-- review (independent acceptance review when warranted)
  +-- github / config / other specialists
```

`orchestrator` defines the next tranche and its acceptance contract, then routes implementation directly to `claude` or `code`. Implementing agents run their own tests, linters, and builds and read the raw failures; only long or noisy runs go to `ops-context`.

## OpenCode V2 configuration

The longest normal path is two child levels, so merge this fragment into the resolved V2 configuration:

```json
{
  "subagent_depth": 2,
  "compaction": {
    "auto": true,
    "keep": { "tokens": 15000 },
    "buffer": 20000
  },
  "tool_output": {
    "max_lines": 1000,
    "max_bytes": 32768
  }
}
```

OpenCode 2 uses top-level `subagent_depth`. The default is `1`; this topology needs `2` for `orchestrator -> claude | code -> ops-context | ops-fast | qwen-task | utility`. Parent `subagent` permissions still control which child IDs each layer may launch, while each child runs with its own configured permissions. Global permission rules apply before agent-specific rules and the last matching rule wins.

`autopilot` uses `mode: all`, which V2 documents as usable either as the primary agent or as a subagent; that capability does not make it an orchestrator child.

## Foreground contract

OpenCode V2 foreground subagent calls wait for the child result; `background: true` returns immediately and later injects a completion result. The durable workstream does not place a required dependency on that callback path.

For `/program` work:

1. Orchestrator selects one bounded tranche.
2. Orchestrator launches Claude or Code in the foreground.
3. The implementing agent completes every required child, command, test, build, and validation before returning.
4. Orchestrator inspects the returned diff and evidence, then continues to correction, review, lifecycle work, or the next tranche.

Required work must not return as `still running`, `waiting for notification`, or equivalent. Long commands should normally use a sufficient foreground timeout rather than background execution merely because they are slow.

Direct primary Autopilot use may still use background execution for genuinely independent, non-overlapping work. This restriction is about the critical dependency chain, not a global ban on useful concurrency.

## New child versus continuation

A child session owns one cohesive outcome. Keep the returned `sessionID`.

- Resume that `sessionID` after the prior call has returned when correcting or extending the same bounded outcome and its context is still useful.
- Start a fresh child for a new tranche, stale context, or deliberately independent review.
- Do not send another prompt into a child while its prior call is still running.

This preserves useful context without depending on concurrent prompts into one child session. Cheap mechanical workers are resumable too: a focused Qwen validation child can run a test, return a failure summary, and be resumed after a correction for the related rerun rather than paying a fresh-context cost for each command.

## Start with an authority contract

A useful `/program` request remains explicit about scope and lifecycle authority:

```text
Complete the next accepted tranche of Issue <id> in <repository>.
Scope: <bounded objective and exclusions>.
Acceptance: <observable behavior plus required local/package/platform gates>.
Authority: edit and validate; stop before commit, push, merge, or release.
Budget: <optional cost/time/escalation limit>.
```

For unattended progress, explicitly authorize the Git actions you want. A worker completing a tranche is not a reason for the manager to stop and ask the user to transport the result.

## Recovery

`orchestrator` alone maintains `.opencode/work/current.md` in a locally ignored work directory. Keep it short:

```text
Objective / authority / non-goals
Current tranche and next action
Checkout / branch / HEAD / dirty-tree identity
Active child sessionIDs, roles, and status
Accepted decisions and open findings
Validation: command, tested tree/environment, result, log pointer
Git/CI lifecycle state
```

After compaction or resumption, reconcile this checkpoint against the actual checkout and any active jobs before acting. Actual Git/worktree state and repository-local authoritative guidance, accepted OpenSpec, and accepted issue decisions outrank the checkpoint; the reconciled checkpoint outranks live model recollection for runtime position. Native todos are convenient current-step tracking, not a second roadmap.

## Adoption checks

Before relying on this unattended:

1. Verify the resolved config applies top-level `subagent_depth` of at least `2`.
2. Verify `autopilot` is available as a standalone control plane, not an orchestrator child.
3. Verify `orchestrator -> claude | code -> ops-context | ops-fast | qwen-task | utility` works with the configured permissions.
4. Verify required tranche work remains foreground and returns terminal evidence.
5. Verify a completed Claude/Code child can be resumed by `sessionID` for a focused correction.
6. Verify a fresh tranche creates a fresh Claude/Code child.

For external harness tranches, [Switchboard's delegation contract](https://github.com/christian-taillon/opencode-switchboard/blob/main/skills/switchboard/SKILL.md) covers the execution/session boundary; [opencode-agents](https://github.com/christian-taillon/opencode-agents) supplies the opinionated parent routing described here.

## References

- https://opencode.ai/v2/docs/agents
- https://opencode.ai/v2/docs/config
- https://opencode.ai/v2/docs/permissions
- https://opencode.ai/v2/docs/migrate-v1
- https://github.com/anomalyco/opencode/issues/45480
