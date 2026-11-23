---
title: Issue 2201 live10 changes
ms.date: 2026-11-23
---

Status: implemented. Full tier (src change); `rpi-checks.py --all` not run (coordinator). Azure read-only; no throwaway resource, nothing to delete.

## Files

* `src/api/src/zava_forward/api/live_receiver.py`: the unexpected-failure branch of `main` prints `Cannot run: RECEIVER_FAILED error_type=<Class>` (class name only), exit code 4 unchanged.
* `src/api/tests/test_live_control.py`: `test_unexpected_failure_prints_only_the_exception_class` (exit 4, exact stderr, no message text).
* Evidence: `.copilot-tracking/evidence/2026-11-23/issue-2201-live10/` (probe script, `probe-readings.json`, `executions.json`, `employee-map.png`). Research: `.copilot-tracking/research/2026-11-23/issue-2201-live10-research.md`.

## Per-criterion table

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Root cause recorded with evidence (logs, exit code) | Partly proven | Log Analytics shows 09:30 to 11:30 UTC runs logged only `IOT_RECEIVE_FAILED`: cause unproven; SQL causes proven in the 22 Nov note; exit codes are not logged by the platform; this change adds the class for the one branch still blind |
| Fix merged and deployed | Proven for earlier fixes; not for this change | job image digest `541068a6...2c38` runs; this commit is local and undeployed |
| Three consecutive scheduled runs Succeeded | Proven | executions 12:00 to 18:30 UTC 23 Nov all Succeeded (14); 19:00 still Running at read time |
| Readings from IoT Hub in store and employee map, with timestamps | Proven for the demo | 19:10 UTC probe: map 200 with 443 items; two cases `ok`, 12 readings, latest `2026-11-23T19:05:00Z`, `fresh` |
| New code evidence (goal) | Proven | new regression test passes |

## Validation

* From `src/api`: `unittest` for `test_live_control` and `test_iot_stream` OK; `mypy` clean (373 files); `ruff check` and `ruff format --check` clean.
* Hosted CI not observed (not pushed).
