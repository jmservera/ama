---
title: Issue 123 live re-check and handoff timezone regression tests (2026-11-23)
description: Live re-observation of the two open #123 criteria and of the 2026-11-21 handoff queue failure, plus regression tests that guard it
ms.date: 2026-11-23
ms.topic: reference
---

Scope: synthetic demo, desktop only, head `111d83c961`. Refs #123. No GitHub issue was ticked or closed and no Azure resource was created or changed. It follows the [2026-11-21 verdict](./issue-123-live-criteria-verdict-2026-11-21.md), which stays unchanged.

## Observations

| Item | Observation on 2026-11-23 | Class |
| --- | --- | --- |
| Handoff queue failure from 2026-11-21 | Signed-in probe on `ca-cutover-test-demo-api`: `/api/handoffs/unaccepted`, `.csv` and `/api/handoffs/unowned` return 200; `#/handoff-waiting` renders "Recorded as of 23 Nov 2026, 19:11 UTC. Longest wait first." Probe and output: `.copilot-tracking/evidence/2026-11-23/issue-123-live-20261123T190834Z/`. Cause of recovery: the demo data seed recorded in the [#2256 note](./issue-2256-live-2026-11-23d.md) plus the code that reports an unreadable offered time as unknown age. | Azure observed |
| Code at HEAD | `handoff_ageing` returns `age_hours: None` for a time with no timezone; `app.js` shows "Unknown. The offered time has no recorded timezone." | Local observed |
| Test gap | The core test covered a missing `offered_at` key only. The live failure shape (minute precision, no timezone) and the HTTP JSON and CSV routes had no test. | Local observed |

## Change

Two regression tests, no production code change (focused tier):

* `src/core/tests/test_handoff_escalation_83.py`: `test_timezone_less_minute_precision_offered_at_reports_unknown_age`.
* `src/api/tests/test_handoff_api.py`: `test_timezone_less_offered_time_keeps_waiting_queue_and_download_readable` (unaccepted JSON, unowned JSON, unaccepted CSV all 200).

Both files pass (core 14 tests, API 8 tests), `ruff check` and `ruff format` are clean, and the `src/api` mypy run is clean. The `src/core` mypy run reports 3 errors (two missing OpenTelemetry stubs and one unused ignore) that are identical without this change.

## Criterion verdicts

| #123 criterion | Verdict | Reason |
| --- | --- | --- |
| Complete the scoped #440 stabilization checkpoint before closure | Unproven | #440 criterion 8 (published PR, non-worker reviewer, current coordinator behavior tests) is open; the issue text says merged children do not satisfy it. Owner and publication act. |
| All child features closed or deferred | Unproven | #126 and #440 remain open; closing or deferring is an owner decision, and #126 needs DPO, Legal and independent assessment, which the demo does not require. |

## Limits

* Focused tier; no full gate and no `rpi-checks.py` run.
* The probe read status codes and screen text only; no case content was recorded.
