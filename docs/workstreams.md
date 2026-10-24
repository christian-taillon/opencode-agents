---
disabled: true
---

# One owner, bounded workers

The default is direct execution. Long work changes how an accepted outcome is
tracked, not who owns it. Use a `/work` command or an explicitly invoked skill in
the current `direct` session; do not insert a second manager between user and
engineer. Keep the command and full workflow at one authoritative installation
location rather than duplicating them in every agent.

The owner decides the approach, implements cohesive work, validates it, and does
authorized routine Git/gh operations. Delegate substantial independent work,
noisy evidence collection, or a genuine specialist capability. A short command,
commit, or summary usually costs less to execute than to explain to a child.

## Branches, commits, and pull requests

Use one primary branch and PR for one coherent engineering outcome. Include its
implementation, related diagnosis and fixes, regression tests, documentation,
and necessary cleanup. Keep the outcome bounded; a long workstream may deliver
several independently useful outcomes rather than one accumulating mega-PR.

Before opening another PR, inspect the existing workstream and accepted scope.
A completed worker, session, task, or commit is not a new PR boundary. Use
meaningful commits to make related changes reviewable; there is no minimum or
maximum commit count. Split when work can ship or roll back independently, has
a materially different risk or approval boundary, or no longer forms one
understandable review. Do not add unrelated fixes merely to make a PR broader.

The integration owner combines accepted worker changes into that branch and
validates the resulting revision. Worker worktrees provide isolation, not a PR
per worker. Keep dependent work together where practical; a temporary integration
branch is evidence, not another routine PR or a substitute for final-head checks.

Run focused checks during development and required broader checks on the
integrated result. Batch authorized publication at meaningful checkpoints rather
than pushing every local commit. This does not skip required CI, platform checks,
review, signing, or human merge approval. Existing commit/push/PR/merge authority
still applies; this policy grants none.

## Delegation contract

Give a child the objective, relevant paths and settled decisions, allowed write
scope/checkout, acceptance and validation, lifecycle authority, and the evidence
to return. Include essential constraints, not the full conversation. A worker
starts fresh and does not inherit the parent's task history or permissions.

The owner inspects the result and actual diff/check evidence. Resume the same
child session for cohesive corrections after it finishes; fresh context is for
independent review or a different outcome. Do not repeatedly re-prompt the worker
with the entire original task. Reuse valid unchanged test evidence, while running
integration checks for newly combined changes.

Run dependent writers sequentially. Independent concurrent writers need separate
worktrees, explicit ownership, and a single integration owner. Do not have the
parent edit the same checkout as a running writer. Terminal workers return unmet
expertise or authority rather than launching more managers.

## Recovery and completion

Only substantial work needs a small private checkpoint. Record objective and
authority, current phase/next action, checkout/HEAD/dirty boundary, child IDs and
status, decisions, validation pointers, and unresolved blockers. Keep one owner
per worktree and exclude runtime state from Git. Do not create a second roadmap.

After compaction or resumption, reconcile repository state and authoritative
project decisions before trusting the checkpoint. Completed work, a blocked
provider, an unanswered decision, an approval boundary, and a pending check are
different states. Continue corrections while they make progress; diagnose repeated
no-progress loops instead of paying for identical retries indefinitely.

Finish when the accepted outcome and required checks are satisfied. Do not stop
merely because a child returned, but do not broaden the project to remain busy.
Report a concrete blocker when authority, environment, budget, or missing evidence
prevents completion. A prompt is not a durable scheduler across a dead process.

## Project knowledge and improvement

Use a small project `AGENTS.md` as a map to accepted architecture, current scope,
and executable checks. Skills disclose specialized procedures when needed.
Critical privacy and authority rules remain available without skill selection.

When repeated failures show missing context or validation, prefer a focused
project documentation or test correction. Propose global harness changes with
evidence and a comparison. Do not weaken tests, permissions, or acceptance to
improve apparent success, and do not rewrite the running harness mid-task.
