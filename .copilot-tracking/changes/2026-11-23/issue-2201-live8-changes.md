---
title: Issue 2201 live8 changes
ms.date: 2026-11-23
---

Full tier (src change). Azure read only; no throwaway resource created. Status: implemented.

## Files

* `src/api/src/zava_forward/api/iot_stream.py` (record `callback_error_type`)
* `src/api/src/zava_forward/api/live_receiver.py` (print it on failure)
* `src/api/tests/test_iot_stream.py` (one test)
* `.copilot-tracking/evidence/2026-11-23/issue-2201-live8/receiver-executions.json`

## Per-criterion table

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Root cause recorded with evidence (logs, exit code) | Unproven for 09:30 to 11:30 UTC 23 Nov | five Failed runs, exception class not logged until this change; no exit code in execution records |
| Fix merged and deployed | Not newly provable | #2231, #2234 earlier; this change is local and undeployed |
| Three consecutive scheduled runs Succeeded | Not holding now | 12:00 Succeeded after five Failed; earlier streak 22:00 to 09:00 UTC |
| Readings from IoT Hub in store and map, with timestamps | Not re-proven | no map probe this run; demo-proven in live7 |
| New code evidence (goal) | Proven | `test_unexpected_callback_failure_records_only_the_exception_class` passes |

## Validation

* From `src/api`: `unittest` for `test_iot_stream`, `test_live_receiver_sql`, `test_live_control` OK (2 skipped); `mypy` clean; `ruff check` and `ruff format --check` clean.
* `rpi-checks.py --all` not run (coordinator). Hosted CI not observed (not pushed). Redeploying the image is a later owner-authorised step.
