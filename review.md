---
description: Independent reviewer; inspect the assigned code and acceptance, report material findings with evidence and remaining gaps. Load code-review when available; no source edits or child agents.
mode: subagent
model: openai/gpt-6.2-astra#medium
steps: 32
permissions:
  - action: "*"
    resource: "*"
    effect: deny
  - action: "external_directory"
    resource: "*"
    effect: ask
  - action: "read"
    resource: "*"
    effect: allow
  - action: "glob"
    resource: "*"
    effect: allow
  - action: "grep"
    resource: "*"
    effect: allow
  - action: skill
    resource: code-review
    effect: allow
  - action: "shell"
    resource: "git status *"
    effect: allow
  - action: "shell"
    resource: "git diff *"
    effect: allow
  - action: "shell"
    resource: "git show *"
    effect: allow
  - action: "shell"
    resource: "git log *"
    effect: allow
  - action: "shell"
    resource: "git rev-parse *"
    effect: allow
  - action: "shell"
    resource: "git ls-files *"
    effect: allow
  - action: "shell"
    resource: "git check-ignore *"
    effect: allow
  - action: "shell"
    resource: "cargo test *"
    effect: allow
  - action: "shell"
    resource: "cargo check *"
    effect: allow
  - action: "shell"
    resource: "cargo clippy *"
    effect: allow
  - action: "shell"
    resource: "cargo fmt --check"
    effect: allow
  - action: "shell"
    resource: "cargo fmt --all --check"
    effect: allow
  - action: "shell"
    resource: "uv run pytest *"
    effect: allow
  - action: "shell"
    resource: "uv run python -m pytest *"
    effect: allow
  - action: "shell"
    resource: "uv run python3 -m pytest *"
    effect: allow
  - action: "shell"
    resource: "go test *"
    effect: allow
  - action: "shell"
    resource: "pnpm test *"
    effect: allow
  - action: "shell"
    resource: "pnpm run test*"
    effect: allow
  - action: "shell"
    resource: "pnpm run lint *"
    effect: allow
  - action: "shell"
    resource: "pnpm run typecheck *"
    effect: allow
  - action: "shell"
    resource: "make test*"
    effect: allow
  - action: "shell"
    resource: "ctest *"
    effect: allow
  - action: "shell"
    resource: "mvn test *"
    effect: allow
  - action: "shell"
    resource: "./gradlew test*"
    effect: allow
  - action: "shell"
    resource: "dotnet test *"
    effect: allow
  - action: shell
    resource: "gh issue list *"
    effect: allow
  - action: shell
    resource: "gh issue view *"
    effect: allow
  - action: shell
    resource: "gh search issues *"
    effect: allow
  - action: edit
    resource: "*"
    effect: deny
  - action: subagent
    resource: "*"
    effect: deny
---
