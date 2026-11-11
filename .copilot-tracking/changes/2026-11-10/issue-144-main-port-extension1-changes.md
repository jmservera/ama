---
title: Issue 144 main-based slice A port changes
description: Actual changes, evidence and limits for the main-based worker permit port (E1)
ms.date: 2026-11-10
task_id: issue-144-main-port-extension1
---

## Status

Implemented and locally validated at the DEMO targeted tier. Base: origin/main 6d4cd62475ba89a214055f761b8e3276ef063d44. Refs #144 only. The record was registered prospectively before implement-start and updated after implementation.

## Changes

* `src/core/src/zava_forward/core/ai.py`: `Ai.is_live` (extracted from the inline loopback test in `_request`, same behavior) and `Ai.request_plan` on the current `provider_body`.
* `src/core/src/zava_forward/core/ai_consumption.py`: `DISPATCH_START_CAP_SECONDS`, `DISPATCH_DRIFT_MARGIN_SECONDS`, `_scope`, `reserve_in` (hold reason `authority-expiring`), `dispatch_window_ms`, `complete_in`. `reserve` and `complete` are unchanged wrappers; the first completion wins.
* `src/core/src/zava_forward/core/assistants.py`: `issue_permit` reads database time after the blocking task-row UPDATE and uses it for the margin, `issued_at` and `lease_remaining`. Denials: `consent-not-granted`, `captured-readings` (fail closed to manual), request mismatch, and send fence refusal (allowance refunded, no reservation). `fence_send` body extracted to `_fence_in` with identical checks. `claim` honors the permit marker (`blocked-reclaim`). Added `complete_result`, `_settle_meter`, `_markers`, `_permit_block`, `_refuse_attempt`.
* `src/core/tests/test_ai_consumption.py`: joined reservation window and first completion in one transaction.
* `src/api/tests/test_ai_consumption_api.py`: permit regressions with a clock that jumps only after the task-row UPDATE returns (positive control, margin crossing, authority expiry crossing), denials, consent and captured-readings fail closed with positive control, fence unavailable, marker, settlement and refund cases.

## Not changed

* B scope (queue_azure, dispatch, server, queue tests, publisher, routes, Date and backoff), the lineage digest hook, reconcile and settlement-conflict: deferred.

## Evidence

Logs are under the external `144-main-port-extension1-1110/logs/`; exits were read directly.

| Log | Content | Exit |
| --- | --- | --- |
| 00, 02 | baseline missing-dependency and import failures (kept) | 1 |
| 01 | pip install, own venv | 0 |
| 03 | frozen main baseline 153 tests, 58 skipped | 0 |
| 04, 05, 11, 12, 14, 15 | first-failure ruff syntax, E501 and format results (kept) | 1 |
| 07 | RED: stale pre-update clock mutation, 3 of 3 clock tests fail; restored | 1 |
| 20 | first core mypy, 4 test arg-type errors (kept) | 1 |
| 16 to 19, 21 to 24 | ruff check, ruff format check, mypy core strict and api test file after fixes | 0 |
| 25 | api affected selectors 385 tests, 93 skipped | 0 |
| 26 | core affected selectors 59 tests | 0 |
| 27 | agents test_dispatch 15 tests | 0 |

## Skips and unobserved

* Real MSSQL lock-crossing tests were not run (SQL not authorized); SQLite deterministic clock tests cover the logic only. The 93 skipped api tests are existing SQL or environment skips.
* Consent and captured-readings tests patch `_sensors_granted` and `_captured_sensors`; real sensor fixtures were not run.
* Log 15 (ruff format check across all five files) is not meaningful for format-excluded files; per-project checks (16 to 19) are the configured ones.
* No full gate, Docker, cloud, provider or model call.
* `ai_consumption.py` was edited once with a Python replace script rather than the edit tool; the diff was verified.
