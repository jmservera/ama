---
title: "Plan: conversational assistant panel (#159)"
ms.date: 2026-10-15
---

## Phases

* [x] Phase 1: core `chat_panel` (permitted sources, cited parse, abstain, fallback, withheld) and core tests.
* [x] Phase 2: agents `chat.ChatModel` adapter over `AgentWorker.provider_call`, with tests.
* [x] Phase 3: api routes `POST /api/chat/threads/{id}/ask` and `/proposals`, composed in `App`; api tests.
* [x] Phase 4: web `chat.js` collapsed panel on the case card, style, script tag.
* [x] Phase 5: ruff, mypy, all src suites, local run with synthetic data and keyboard-only browser check.
* [x] Phase 6: docs (src/api README, reference index, log), artifacts, commit, PR with `Refs #159`.

## Decisions

* Additive endpoints; the existing `/messages` contract is untouched.
* Proposals go through `Assistants.invoke`; chat has no other write path.
* Panel is a `details` disclosure so it is never required.

## Critique (single pass, executed)

* Verdict: proceed. Compatible findings applied: keep the old endpoint contract; cap citations (12); drop uncited replies; do not call the model without case facts; add a narrow mypy override instead of widening exemptions.
* No conflict with confirmed owner decisions; no user decision required.

## Out of scope (unticked)

* Screen-reader test, live model run, real chat data, streaming and resumable panel.
