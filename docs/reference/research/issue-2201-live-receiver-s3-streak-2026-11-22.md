---
title: Issue 2201 receiver streak and SQL S3 health (demo, 2026-11-22)
description: Nine consecutive scheduled job-live-receiver successes from 14:00 to 18:00 UTC on image 541068, SQL retrofit on Standard S3 with no saturation, and a fresh map probe
ms.date: 2026-11-22
ms.topic: reference
---

Scope: synthetic demo, desktop only, resource group `ama`. Azure was read only; nothing was created or changed, so nothing needs deleting. Sign-in values were read at runtime by the probe helper and never printed. It follows the [receiver streak note](./issue-2201-live-receiver-streak-2026-11-22.md) and the [log causes](./issue-2201-live-receiver-logs-2026-11-22.md). Refs #2201, #184.

## Evidence

Recorded under `.copilot-tracking/evidence/2026-11-22/issue-2201-live7/`: `receiver-executions.json`, `job-settings.json`, `api-revisions.json`, `sql-dbs.json`, `dtu-30m.json`, `dtu-limit-5m.txt`, `sql-health.json`, `failure-lines.json`, `probe_readings.py`, `probe-readings.json` and `employee-map.png`. Read at 18:30 to 18:33 UTC.

## Receiver streak

The job runs image `crcutovertestrzsrg.azurecr.io/zava-forward-api@sha256:541068a6...2c38` (arguments `--seconds 1500 --events 100000`, replica timeout 1620 s, retry limit 0), and every listed execution since 12:01 UTC shows that digest. Scheduler-started executions (names of the form `job-live-receiver-<period>`) after the last failure:

| Start (UTC) | End (UTC) | Status |
| --- | --- | --- |
| 14:00:00 | 14:25:48 | Succeeded |
| 14:30:00 | 14:55:24 | Succeeded |
| 15:00:00 | 15:25:38 | Succeeded |
| 15:30:00 | 15:55:30 | Succeeded |
| 16:00:00 | 16:25:26 | Succeeded |
| 16:30:00 | 16:55:37 | Succeeded |
| 17:00:00 | 17:25:33 | Succeeded |
| 17:30:00 | 17:55:43 | Succeeded |
| 18:00:00 | 18:25:28 | Succeeded |

That is nine in a row, each about 25 minutes. The 18:30 run was still Running when read and is not counted. The previous scheduled run, 13:30, Failed.

The API app is now on revision `0000051` with a newer digest (`866cc28e...`); the receiver job has not been rolled to it. "Current image" here means the image the job runs, which is the one the streak was measured on.

## SQL health on S3

* `retrofit` on `sql-cutover-test-rzsrg` reports `Standard`, capacity 100 DTU (S3).
* The activity log records two "Update SQL database" operations at 13:53:53 and 13:54:00 UTC; `dtu_limit` moves from 10 to 100 in the 13:55 five-minute bucket.
* `dtu_consumption_percent` per 30 minutes from 14:00 to 18:30: average 14 to 19 percent, maximum 77 to 89 percent. Before the scale (12:00 to 13:30, S0) the maximum was 100 in every bucket and the average 78 to 95 percent.
* Over 14:00 to 18:30, `connection_failed` is 0 and `deadlock` is 0.

Reading: the database has headroom and is not saturated; short peaks reach about 89 percent, which is not a sustained limit.

## Failure lines

`ContainerAppConsoleLogs` for `job-live-receiver` since 13:20 UTC (workspace `log-cutover-test`, query as already approved) holds one line matching `FAILED`, `UNAVAILABLE`, `Traceback` or `ERROR`: `Cannot run: IOT_CALLBACK_FAILED` from the 13:30 execution. Nothing matches after the S3 scale. Ingestion lag could hide a very recent line; the execution statuses are the primary evidence.

## Map and readings

Staff app probe at 18:32 UTC (Playwright, signed in at runtime): `/api/map?zoom=14` returned 200. Cases `ZF-2025-0030` and `ZF-2025-0331` return `state` `ok`, `freshness` `fresh`, health `ok`, latest `observed_at` `2026-11-22T18:30:00Z`. Other probed cases return `consent-withheld` by design. Screenshot: `employee-map.png`. The hub-to-store hop is inferred from the live path; no direct hub capture was taken.

## Per-criterion table

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Root cause recorded with evidence (logs, exit code) | Proven for the SQL failures; the 13:30 trigger stays unproven | Earlier notes tie `SENSOR_SQL_UNAVAILABLE` to S0 saturation; the 13:30 failure is `IOT_CALLBACK_FAILED` with no exception class logged; execution records carry no exit code |
| Fix merged and deployed | Proven | #2231 and #2234 on main, job on digest 541068; the DB scale to S3 at 13:53 UTC is a live change by another worker |
| Three consecutive scheduled runs Succeeded | Proven | Nine, 14:00 to 18:00 UTC, one digest |
| Readings from IoT Hub appear in the store and the employee map, with timestamps | Proven for the demo | Map 200; readings to 18:30:00Z, fresh; hub hop inferred |
| SQL DTU healthy on S3 (goal) | Proven | Standard 100 DTU; maximum 89 percent, average under 20 percent, no connection failures |

Open work: log the exception class in the `IOT_CALLBACK_FAILED` handler (full tier, not done here).
