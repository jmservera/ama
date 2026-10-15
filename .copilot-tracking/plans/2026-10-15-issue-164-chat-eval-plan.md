---
title: Issue 164 chat evaluation plan
description: Plan for the offline multi-turn chat evaluation and refusal boundary
ms.date: 2026-10-15
---

## Phases

* [x] Phase 1: out-of-scope refusal and history carry filter in core `chat_panel` (tests in core and api).
* [x] Phase 2: `chat_eval.py` harness and `evals/chat_golden.json`, registered; golden, injection, poisoning, comparison, failure recording, version bindings.
* [x] Phase 3: UI handling of `refused`, READMEs, reference index and log.
* [x] Phase 4: local validation, review, PR with `Refs #164`.

Details: [phase details](../details/2026-10-15-issue-164-chat-eval-details.md). Critique: [critique](../research/2026-10-15-issue-164-chat-eval-critique.md).
