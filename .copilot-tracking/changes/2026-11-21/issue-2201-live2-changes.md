---
title: Issue 2201 changes (second pass)
ms.date: 2026-11-21
---

## Changes

* `src/api/src/zava_forward/api/iot_stream.py`: bounded-window `HubReceiver` retries `SENSOR_SQL_UNAVAILABLE` (2, 5, 15, 30 s), counts `sql_retries`; uncertain commit and other failures stay fatal.
* `src/api/src/zava_forward/api/live_receiver.py`: prints `sql_retries=N`.
* `src/api/tests/test_iot_stream.py`: retry, exhausted-retry and uncertain-commit tests.
* `src/api/README.md`, `docs/reference/research/issue-2201-live-receiver-proof-2026-11-21.md`, `docs/reference/README.md`, `docs/reference/log.md`.
* Evidence: `.copilot-tracking/evidence/2026-11-21/issue-2201-live2/` (executions, probe JSON, map screenshot, log captures, watcher script).

## Validation

Tier FULL (src change), classified by actual impact; the complete gate is coordinator-owned and was not run. Targeted: 104 tests in `test_iot_stream`, `test_live_control`, `test_live_receiver_sql` pass (2 skipped); `ruff check`, `ruff format --check`, `mypy` (src/api) clean. Azure: read only, nothing created, nothing to delete. No credential printed.

## Per-criterion status

| Criterion | Status | Basis |
| --- | --- | --- |
| Root cause recorded with evidence (logs, exit code) | Partly proven | Captured stderr `Cannot run: SENSOR_SQL_UNAVAILABLE` for executions 29921700 (1 min in) and 29921730 (17 min in); deadline defect proven earlier by source, test and a Succeeded run. Unproven: database fault cause, numeric exit code, older failures (workspace denies this client, finished replicas not retained) |
| Fix merged and deployed | Partly proven | Bounded-window fix merged (#2210) and job updated 21:33 UTC. The SQL retry is a local commit; no push, image build or job update authorised, registry denies this client |
| Three consecutive scheduled runs Succeeded | Unproven | After 21:33: 22:00 Failed, 22:30 Succeeded, 23:00 Failed, 23:30 Failed; retry not deployed |
| Readings from IoT Hub in store and employee map with timestamps | Proven for the demo | `/api/map` item and `/api/cases/*/sensors` carry `observed_at` 2026-11-21T22:45:00Z, age 24 s, fresh, five minute steps; screenshot of the map section |
