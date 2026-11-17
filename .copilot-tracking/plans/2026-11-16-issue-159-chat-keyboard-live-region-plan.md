---
title: Issue 159 plan
ms.date: 2026-11-16
---

## Plan

* [x] Phase 1: add a visible, programmatically linked keyboard instruction to the shared chat widget and link it from the employee chat input (details: `.copilot-tracking/details/2026-11-16-issue-159-chat-keyboard-live-region-details.md`).
* [x] Phase 2: extend the jsdom-style unit test and employee browser check (hint visible, Tab order textarea, skill, Send; axe).
* [x] Phase 3: README note; ruff and mypy; focused tests.

## Critique (single pass)

Verdict: proceed. Compatible findings applied directly: keep hint in the widget so every state is scanned by existing axe runs; do not alter live-region politeness (existing tests lock it and the observed announcements are already correct); do not touch resident strings.
