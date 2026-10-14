---
description: Default engineer; own cohesive work and routine Git directly. Delegate only for independence, substantial isolation, or a specialist capability.
mode: all
model: openai/gpt-6.1-sol#xhigh
permissions:
- action: '*'
  resource: '*'
  effect: deny
- action: external_directory
  resource: '*'
  effect: ask
- action: question
  resource: '*'
  effect: allow
- action: read
  resource: '*'
  effect: allow
- action: read
  resource: '*.env'
  effect: deny
- action: read
  resource: '*.env.*'
  effect: deny
- action: glob
  resource: '*'
  effect: allow
- action: grep
  resource: '*'
  effect: allow
- action: edit
  resource: '*'
  effect: allow
- action: shell
  resource: '*'
  effect: allow
- action: execute
  resource: '*'
  effect: allow
- action: webfetch
  resource: '*'
  effect: allow
- action: websearch
  resource: '*'
  effect: allow
- action: skill
  resource: '*'
  effect: allow
- action: skill
  resource: customize-opencode
  effect: deny
- action: subagent
  resource: utility
  effect: allow
- action: subagent
  resource: coder
  effect: allow
- action: subagent
  resource: operations
  effect: allow
- action: subagent
  resource: review
  effect: allow
- action: subagent
  resource: config
  effect: allow
- action: subagent
  resource: github
  effect: allow
- action: subagent
  resource: cloudflare
  effect: allow
- action: subagent
  resource: adversarial
  effect: allow
- action: subagent
  resource: claude
  effect: allow
- action: shell
  resource: git push --force*
  effect: deny
- action: shell
  resource: git push -f *
  effect: deny
- action: shell
  resource: git reset --hard*
  effect: deny
- action: shell
  resource: git clean *
  effect: deny
- action: shell
  resource: git checkout -- *
  effect: deny
- action: shell
  resource: git restore *
  effect: deny
- action: shell
  resource: rm -rf *
  effect: ask
- action: shell
  resource: rm -fr *
  effect: ask
- action: shell
  resource: sudo *
  effect: deny
- action: shell
  resource: su *
  effect: deny
---
