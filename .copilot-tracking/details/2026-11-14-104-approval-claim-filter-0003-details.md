---
title: Issue 104 approval claim filter details
ms.date: 2026-11-14
---

## Phase 1

Regex `FORBIDDEN` in `src/core/src/zava_forward/core/ai.py` matches `(I|we) have/'ve/had [just|now|already] <action>` and `has/have [now|just|already] been <action>`, plus `email sent` and `message sent`. Actions cover approved, updated, changed, ranked, sent, recorded, submitted and similar.

## Phase 2

* `src/agents/tests/test_ai_claim_filter.py`
* `src/api/tests/test_assistant_reserve_guard.py`

## Phase 3

Commands run from a venv at `/tmp/venv-104-0003`.
