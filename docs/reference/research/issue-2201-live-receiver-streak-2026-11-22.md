---
title: Issue 2201 receiver streak, callback failure check and map freshness (demo, 2026-11-22 15:30 UTC)
description: Receiver and simulator executions since 15:00 UTC, three consecutive scheduled receiver successes, no recurrence of IOT_CALLBACK_FAILED, the code path that hides its exception, and a fresh map probe
ms.date: 2026-11-22
ms.topic: reference
---

Scope: synthetic demo, desktop only, resource group `ama`. Azure was read only (job execution lists, one Log Analytics query set, one staff-app probe); no resource was created or changed, so none needs deleting. Sign-in values were read at runtime and never printed. It follows the [log causes note](./issue-2201-live-receiver-logs-2026-11-22.md), which left two items open: the 15:00 run and map freshness. Refs #2201, #184.

## Evidence

Recorded under `.copilot-tracking/evidence/2026-11-22/issue-2201-live6/`: `receiver-executions.json`, `simulator-executions.json`, `receiver-log-lines.json`, `failure-lines-since-10.json`, `probe_readings.py`, `probe-readings.json` and `probe-stdout.txt`. Reads ran between 15:27 and 15:29 UTC.

## Executions since 15:00 UTC

| Job | Execution | Start (UTC) | End (UTC) | Status |
| --- | --- | --- | --- | --- |
| `job-live-receiver` | `29922660` | 15:00:00 | 15:25:38 | Succeeded |
| `job-live-simulator` | `29922660` | 15:00:00 | 15:02:15 | Succeeded |
| `job-live-simulator` | `29922667` | 15:07:00 | 15:09:03 | Succeeded |
| `job-live-simulator` | `29922675` | 15:15:00 | 15:17:03 | Succeeded |
| `job-live-simulator` | `29922682` | 15:22:00 | 15:24:15 | Succeeded |

No execution of either job started since 15:00 with a status other than Succeeded. The simulator has been Succeeded on every run listed from 14:00 (12 of 12).

## Consecutive receiver successes

Scheduled receiver runs at 14:00 (`29922600`), 14:30 (`29922630`) and 15:00 (`29922660`) are all Succeeded, in cron order with no failed or manual run between them. That is three consecutive scheduled successes after the S3 database scale and on the #2231 image. The 15:30 run was due at the time of the probe and is not counted.

## IOT_CALLBACK_FAILED

The Log Analytics query for `Cannot run`, `IOT_CALLBACK`, `Traceback` and `Exception` in `job-live-receiver` since 10:00 UTC returns the same six lines as the earlier note and nothing after 13:53:41. The single `IOT_CALLBACK_FAILED` (run `29922570`, 13:30) did not recur in the 14:00, 14:30 or 15:00 runs, so no exception could be captured.

It cannot be captured from logs as written. In `iot_stream.py` the last handler of the event callback is `except Exception:` followed by `failure = StreamError("IOT_CALLBACK_FAILED")`; the exception class and message are dropped before the job prints `Cannot run: <code>`. Console lines for the 14:00 and 14:30 runs show only `receipts=1037` and `receipts=1055` on stdout; the 15:00 run had written no console line by 15:29 UTC (ingestion lag, as seen for earlier runs). Capturing the cause needs a code change that logs the exception type, which this task does not make.

## Map freshness

Staff app probe at 15:28:56 UTC:

* `/api/map?zoom=14` returned 200 with 443 items.
* `/api/cases/ZF-2025-0030/sensors` and `/api/cases/ZF-2025-0331/sensors` returned `state` `ok`, `freshness` `fresh`, 12 readings each, latest `observed_at` `2026-11-22T15:20:00Z`, which is 8 minutes before the probe.
* Three other probed cases (`ZF-2025-0031`, `ZF-2025-0029`, `ZF-2025-0148`) returned `consent-withheld`, which hides values by design (#2192).

The previous probe saw readings to 13:35:00Z; the newest reading has advanced by 1 hour 45 minutes.

## Per-criterion table

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Root cause recorded with evidence (logs, exit code) | Partly proven | SQL failures (`SENSOR_SQL_UNAVAILABLE` at 100 DTU) and the 11:32 argument error are in the log note; the 13:30 `IOT_CALLBACK_FAILED` exception stays unproven because it did not recur and the code drops its type; exit codes are not logged |
| Fix merged and deployed | Proven | #2231 and #2234 per earlier notes; image unchanged, runs Succeeded on it |
| Three consecutive scheduled runs Succeeded | Proven | 14:00, 14:30, 15:00 above |
| Readings from IoT Hub appear in the store and the employee map, with timestamps | Proven for the demo | Map 200 with 443 items; case sensors `fresh` with latest `2026-11-22T15:20:00Z`; hub-to-store hop inferred from the live path, not traced per message |

Routed follow-up: log the exception class in the `IOT_CALLBACK_FAILED` handler so a recurrence is diagnosable; this needs a source change and the full tier.
