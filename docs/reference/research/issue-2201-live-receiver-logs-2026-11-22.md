---
title: Issue 2201 receiver failure causes from Log Analytics (demo, 2026-11-22)
description: Console log text for every job-live-receiver failure since 10:35 UTC, the cause of each, and the scheduled run streak after the database moved to S3
ms.date: 2026-11-22
ms.topic: reference
---

Scope: synthetic demo, desktop only, resource group `ama`. Azure was read only; no resource was created or changed, so none needs deleting. It follows the [recheck](./issue-2201-live-receiver-recheck-2026-11-22.md), which could not read logs. Refs #2201, #184.

## Evidence

Recorded under `.copilot-tracking/evidence/2026-11-22/issue-2201-live5/`: `executions.json` (read 14:57 UTC), `log-groups.json`, `log-lines.json` and `log-lines-recent.json`.

* Workspace `log-cutover-test` now answers `az monitor log-analytics query`. The table is `ContainerAppConsoleLogs` (not the `_CL` variant); the filter column is `JobName`, the execution is `ContainerGroupName`, and the text is `Log` with `Stream`.
* The receiver writes one or two lines per run: `Cannot run: <code>` on stderr for a failure, `sql_retries=N` on stderr and `receipts=N` on stdout for a finished run. No exit code is logged, but a `Cannot run` line is the failure path of `zava_forward.api.live_receiver`.

## Causes by failed run

| Execution | Start (UTC) | Status | Log line | Cause |
| --- | --- | --- | --- | --- |
| `llf5nfh` | 10:35 | Failed | `Cannot run: SENSOR_SQL_UNAVAILABLE` | SQL write refused or rolled back (`sensor_consumer.py`); first run on image `...62c38` |
| `29922420` | 11:00 | Failed | `Cannot run: SENSOR_SQL_UNAVAILABLE` | same |
| `m5hxnwa` | 11:32 | Failed | `unrecognized arguments: --control-file,/certs/control.json,--seconds,90,--events,100000` | operator started the job with an argument list the receiver does not accept; not a scheduled-run fault |
| `g4cnuoc`, `29922450`, `0bz2ny1` | 11:36, 11:30, 11:50 | Failed | `Cannot run: SENSOR_SQL_UNAVAILABLE` | same SQL cause |
| `29922570` | 13:30 | Failed | `Cannot run: IOT_CALLBACK_FAILED` at 13:53:41 | an exception other than a consumer or stream error reached the IoT callback (`iot_stream.py`, last `except Exception`); the exception type is not logged, so the exact trigger is unproven |

Succeeded runs log the retries that the 2231 fix absorbs: `sql_retries=32` to `37` with `receipts` 654 to 720 at 12:27, 12:55 and 13:26. The 14:00 run logged `receipts=1037`, a higher count than any earlier run.

## Database

`retrofit` now reports SKU Standard with capacity 100 DTU (S3). Thirty minute metric buckets: `dtu_consumption_percent` maximum 100 from 12:30 to 14:00, then 81 (14:00) and 89 (14:30) with averages near 14 percent. The 100 percent ceiling coincides with every `SENSOR_SQL_UNAVAILABLE` failure and with 32 to 37 retries in succeeded runs; the S3 scale removed it.

## Executions since 14:00 UTC

| Execution | Start (UTC) | End (UTC) | Status | Started by |
| --- | --- | --- | --- | --- |
| `29922600` | 14:00:00 | 14:25:48 | Succeeded | scheduler |
| `29922630` | 14:30:00 | 14:55:24 | Succeeded | scheduler |

Consecutive scheduled successes: two (14:00, 14:30). The 15:00 run had not started at 14:57 UTC. The 14:30 run wrote no console line within the query window; the 14:00 run's line arrived after the run ended, so ingestion lag is the likelier reason, not a fault.

## Per-criterion table

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Root cause recorded with evidence (logs, exit code) | Proven for the SQL failures and the 11:32 argument error; unproven for 13:30 | Log text above; exit codes are not logged; 13:30 shows only `IOT_CALLBACK_FAILED` with no exception detail |
| Fix merged and deployed | Proven for #2231 and #2234 (earlier notes); unchanged here | Job image `...62c38` in the log image column; no change made |
| Three consecutive scheduled runs Succeeded | Unproven now: two since 14:00 | 14:00 and 14:30 Succeeded; the 15:00 run decides. The 04:00 to 05:00 streak and 12:30, 13:00 pair stand as earlier history |
| Readings from IoT Hub appear in the store and the employee map, with timestamps | Not re-probed | Store writes are shown by `receipts=1037` at the 14:00 run; the map probe in the recheck (443 items, readings to 13:35:00Z) was not repeated, so freshness now is not proven |
