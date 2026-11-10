---
title: Issue 144 main-based slice A port plan
description: Plan for E1, a minimal main-based selective port of the worker permit slice A with fail-closed current main safeguards
ms.date: 2026-11-10
task_id: issue-144-main-port-extension1
---

## Scope

Base origin/main `6d4cd62475ba89a214055f761b8e3276ef063d44`. Files changed: `core/ai.py`, `core/ai_consumption.py`, `core/assistants.py`, `core/tests/test_ai_consumption.py`, `api/tests/test_ai_consumption_api.py`, and this task's RPI records. Not touched: B queue, dispatch, server, queue tests, infra, README. No merge or cherry-pick of the old lineage. Research: [research](../../research/2026-11-10-issue-144-main-port-extension1-research.md).

## Design

* `Ai.is_live(capability)` and `Ai.request_plan(system, user, deployment, temperature, max_tokens)` on `provider_body`; `_request` uses `is_live`. No `_body`, no dispatch hook.
* `Consumption`: `_scope`, `reserve_in(..., min_window)`, `dispatch_window_ms`, `complete_in`; `reserve` and `complete` wrap them with unchanged behavior (first completion wins).
* `Assistants`: `PERMIT_*` constants; claim-time permitted marker; `_markers`; `_fence_in(db, attempt, capability)` extracted from `fence_send` (same checks, same `send-refused` event, same restamp) and reused by `fence_send` and `issue_permit`; `_permit_block` extended with consent and captured-readings gates; `_refuse_attempt`; `issue_permit` (fresh time after the blocking UPDATE used for margin, `issued_at` and `lease_remaining`); `complete_result` with `_settle_meter`.
* Fail closed: no consent denies; captured readings deny (manual); fence refusal denies and refunds with no reservation. Order in `issue_permit`: state and lease, duplicate, `_permit_block` (suspension, admission, epoch, binding, release, source, consent, captured readings), request match, fence, reserve. The fence runs after the request match and before the reservation so a refusal reserves nothing.

## Test plan (commands later fixed in details)

* Core ledger: reserve_in expiring-window hold, joined-transaction behavior, complete_in first-completion-wins, `reserve` and `complete` unchanged.
* Service permit (SQLite): grant once and mark; denials reserve nothing; clock regression with database time advanced at the blocking UPDATE (expired and inside-margin refusal, positive valid window grants); window clipping; suspension refund; marker blocks reclaim; settlement binds to the marker; result without permit closes task.
* New fail-closed: consent withdrawn denies (no reservation, task manual); captured readings deny (consent granted); fence refusal (attempt not live) denies with no reservation and a `send-refused` event; allowed path restamps attempt to `sending`; existing `execute()` and `fence_send` tests unchanged.
* Impacted selectors: `test_ai_call_site_inventory.py`, `test_ai_dispatch_marker.py`, `test_ai_consumption.py`, `test_ai_consumption_api.py`, `test_assistants.py` (SQLite), plus quality sensor and simulation selectors if they exercise `fence_send`. Ruff, mypy on changed packages as the repository configures them.
* No SQL, Docker, cloud, provider, full gate. MSSQL lock-crossing coverage stays unobserved.

## Pause points

Implement-start only after plan-done and the prospective changes record exist. E1 is one batch: if a failure needs logic outside this scope, stop and report.
