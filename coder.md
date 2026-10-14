---
description: Terminal implementation worker for substantial separable outcomes; validate own changes and return evidence. No Git publication or child agents.
mode: subagent
model: openai/gpt-6.1-sol#high
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
  resource: '*'
  effect: deny
- action: shell
  resource: git commit*
  effect: deny
- action: shell
  resource: git push*
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
