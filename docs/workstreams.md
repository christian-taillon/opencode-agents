---
disabled: true
---

# Flat workstreams

Use Direct for a cohesive engineering conversation. Use Autopilot for an accepted
outcome that benefits from bounded phases, independent leaves, or durable recovery.
Neither requires a management layer or external adapter.

```text
autopilot (primary)
  +-- coder (implement and validate)
  +-- review / adversarial (independent evidence)
  `-- operations / utility / specialists
```

Each leaf returns terminal evidence or a blocker. It never launches children.
The primary sequences corrections and any next expertise, retaining ownership
of scope, architecture, acceptance, and lifecycle decisions.

## Bounded contract

```text
Objective: <accepted outcome and exclusions>
Acceptance: <observable behavior and required boundary checks>
Ownership: <checkout, dirty files, assigned writable paths>
Authority: edit and validate; stop before commit/push/publication
Budget: <optional time/cost limit>
```

The implementer reads its own raw failures. Required gates finish before a phase
is accepted. Independent non-overlapping work may run concurrently, but never
concurrent writers in one checkout. Resume a returned child for cohesive correction
only after its previous call has finished; create a fresh context for independent
review or a new outcome. Evidence, not a verdict, drives acceptance.

## Configuration and command

Set `experimental.subagent_depth: 1` in the global OpenCode configuration.
V2.0.26 uses this nested setting, not a top-level field. Primary depth
`0` may call a leaf; leaf depth `1` is blocked. Its own `subagent: * -> deny` rules
also forbid grandchildren, including when a leaf is selected directly.

`/program` selects `autopilot` with explicit `subagent: false`, forcing the current
session instead of a background child manager. Its explicit command model selects
Sol High; primary selection by ID alone would retain the session's stored model.
Migrate any installed Markdown command still selecting a retired role;
file-based overrides can outrank the global JSON configuration.
Keep model selection separate from role selection and honor explicit overrides.

## Recovery

Reuse native child `sessionID` continuation, permission-scoped skills, compaction,
and Git worktree support rather than adding a scheduler, session store, shared
instruction framework, or plugin. Skills load only when relevant; `AGENTS.md`
supplies active policy, not the currently unresolved config `instructions` array.

Native compaction already preserves continuity but is lossy. The small optional
checkpoint below records execution position for substantial work; it does not
replace native session history or compaction. No provider-native compaction,
warming, or new worktree settings are installed by this design.

Only substantial work needs `.opencode/work/current.md`, a short locally ignored
checkpoint written only by Autopilot:

```text
Objective / authority / non-goals
Current phase / next action
Checkout / branch / HEAD / dirty boundary
Child sessionIDs / roles / terminal or active status
Accepted decisions / open findings
Validation commands / exits / tested environment / log pointers
Lifecycle state
```

On recovery, reconcile actual Git/worktree state and repository-authoritative
guidance first. These outrank the checkpoint, which outranks recollection. Native
todos are current-step tracking, not another roadmap. Never imply unfinished
jobs, static checks, or local tests prove runtime/remote qualification.

## Adoption gates

1. Inspect global and project configuration/agent/command overrides.
2. Remove retired IDs and migrate `/program` without aliases.
3. Validate portable static contracts and pinned V2 candidate normalization.
4. Obtain separate activation authority; preserve sessions and unrelated settings.
5. After controlled activation, verify primary-to-leaf permission/depth behavior
   and continuation against the actual server version. This last gate is runtime,
   not satisfied by source inspection.
