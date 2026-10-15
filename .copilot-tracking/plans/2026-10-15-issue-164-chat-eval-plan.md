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

## PR 307 review-fix scope

Owner-directed continuation on `feat/src-chat-eval-164`, not a new lifecycle.
The earlier completion and critique remain historical evidence.

* [x] P05-T01: Normalize lexical refusal inputs, cover requested action/contact
  phrasings, drop assistant history and withhold lexical action claims.
* [x] P05-T02: Count critical known gaps as blockers, never passes; cover report,
  category totals, CLI and enablement with synthetic regression tests.
* [x] P05-T03: Run all five src suites, ruff and mypy; reconcile changes, review,
  documentation and state; commit and push to the existing branch without force.

Approval thresholds, reviewer, real-model behaviour and human review remain
unapproved or unmeasured. Nothing is enabled.

P05-T03 complete: validated source fix `2f6f73a` was pushed normally to the same
branch; this delivery-record update follows on that branch.
The golden CLI intentionally exits 1 for the open critical unsupported-claim gap,
not an unexpected regression.
