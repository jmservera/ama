---
title: Issue 2201 receiver recheck after the 2234 merge (demo, 2026-11-22)
description: Every job-live-receiver execution since 10:34 UTC with who started it, why the earlier three-run proof no longer holds as a current streak, and a fresh map probe
ms.date: 2026-11-22
ms.topic: reference
---

Scope: synthetic demo, desktop only, resource group `ama`. Azure was read only; no resource was created or changed, so none needs deleting. Sign-in values were read at runtime and never printed. It follows the [three-run proof](./issue-2201-live-three-runs-2026-11-22.md), which covered 04:00 to 05:00 UTC. Refs #2201, #184.

## Evidence

Recorded under `.copilot-tracking/evidence/2026-11-22/issue-2201-live4/`: execution lists read at 13:40 and 13:55 UTC, job settings, SQL metrics, probe script, probe JSON and the employee map screenshot.

* PR #2234 merged 2026-11-22 09:51:57 UTC; API revision `--0000047` was created 10:34:13 UTC. The job and revision 47 run image digest `sha256:541068a6...2c38`. Other workers created revisions 48 and 49 and a throwaway sampler job during this window (13:41 UTC onward); the API was unreachable for about 13 minutes while they activated.
* "Who started" is read from the execution name: a name made of the cron period number (for example `29922480`) is the Container Apps scheduler (`*/30 * * * *`); a random seven character suffix is a manual `start` by a signed-in operator principal (activity log, principal not recorded here). Operator job edits are logged at 12:00:43, 12:01:08 and 12:10:18 UTC.

## Executions since 10:34 UTC

| Execution | Start (UTC) | End (UTC) | Status | Started by | Note |
| --- | --- | --- | --- | --- | --- |
| `llf5nfh` | 10:35:03 | none | Failed | operator | first run on 541068 |
| `29922420` | 11:00:00 | none | Failed | scheduler | 1500 s |
| `29922450` | 11:30:00 | none | Failed | scheduler | 1500 s |
| `m5hxnwa` | 11:32:51 | none | Failed | operator | |
| `fhatma0` | 11:34:02 | 11:36:21 | Succeeded | operator | `--seconds 90` |
| `g4cnuoc` | 11:36:52 | none | Failed | operator | 1500 s |
| `0bz2ny1` | 11:50:21 | none | Failed | operator | `--seconds 240` |
| `2muim64` | 11:55:18 | 12:00:17 | Succeeded | operator | `--seconds 240` |
| `29922480` | 12:00:00 | 12:05:50 | Succeeded | scheduler | `--seconds 240` (temporary edit) |
| `z6cwh3y` | 12:01:03 | none | Stopped | operator | stopped at 12:01:31 |
| `n76pukf` | 12:01:51 | 12:27:42 | Succeeded | operator | 1500 s, `ZF_RECEIVER_BATCH_SIZE=10` |
| `29922510` | 12:30:00 | 12:56:07 | Succeeded | scheduler | 1500 s |
| `29922540` | 13:00:00 | 13:26:23 | Succeeded | scheduler | 1500 s |
| `29922570` | 13:30:00 | none | Failed | scheduler | read Running at 13:40, Failed at 13:55 |

Scheduled runs only, from the merge on: 10:00 Succeeded, 10:30 Stopped (image `6b829b84...`, an earlier build), 11:00 Failed, 11:30 Failed, 12:00 Succeeded, 12:30 Succeeded, 13:00 Succeeded, 13:30 Failed. The only unbroken scheduled streak is 12:00, 12:30, 13:00, and the 12:00 run used a shortened `--seconds 240` window from an operator edit. At the standing settings the streak is two (12:30, 13:00), and the latest scheduled run failed.

## Map

Staff app probe at 13:55 UTC (Playwright, signed in at runtime): `/api/map?zoom=14` returned 200 with 443 items. `/api/cases/ZF-2025-0030/sensors` and `ZF-2025-0331` returned `state` `ok`, 12 readings, latest `observed_at` `2026-11-22T13:35:00Z` (reading ids `LIVE-STQEOYP62W2-20261122T1335Z`, `LIVE-SIBP5GIQWTN-20261122T1335Z`), `freshness` `stale` because the 13:30 run failed and no newer reading arrived. Three other probed cases return `consent-withheld` by design. Screenshot: `employee-map.png`.

## Failed runs: logs and cause

* Logs could not be captured. `az monitor log-analytics query` on `log-cutover-test` is refused (`NspValidationFailedError`, network security perimeter blocks this caller) and `az containerapp job logs show` reports no replica for a finished execution. Opening the workspace would be a production network change, which the demo authorisation excludes.
* Execution records carry no exit code or status message, only `Failed`.
* Differential: the 11:30 (Failed) and 12:30 (Succeeded) runs share image, arguments and resources; the only template difference is `ZF_RECEIVER_BATCH_SIZE=10` added at 12:00. A sibling worker's unmerged branch (`f5b4a8f2c7`) reads that variable and records that a batch size of 50 failed live with `SENSOR_SQL_UNAVAILABLE`. It is not proven that image 541068 contains that code. The 13:30 run then failed with settings identical to the 13:00 success, so the setting does not explain every failure.
* SQL context: database `retrofit` (Standard S0) reported `dtu_consumption_percent` maximum 100 in every five minute bucket from 12:55 to 13:50 UTC, including the succeeded window, with `connection_failed` 0. Sustained saturation, shared with other workers' jobs, is consistent with the earlier `SENSOR_SQL_UNAVAILABLE` capture but does not separate a failed run from a succeeded one.
* Conclusion: the cause of the 10:35 to 11:50 and 13:30 failures is not proven. Inference only: write contention on the saturated S0 database.

## Per-criterion table

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Root cause recorded with evidence (logs, exit code) | Unproven for runs since 10:34 | Earlier causes stand (deadline as failure, fixed in #2231; `SENSOR_SQL_UNAVAILABLE` on 2026-11-21); logs and exit codes are unreachable for 11:00, 11:30 and 13:30 |
| Fix merged and deployed | Proven for #2231 and #2234 | Both on main; job and API revision 47 share digest 541068; the batch change is unmerged and not claimed |
| Three consecutive scheduled runs Succeeded | Partly proven | 12:00, 12:30, 13:00 (12:00 on a shortened window); 04:00, 04:30, 05:00 earlier; not a current streak, because 13:30 Failed |
| Readings from IoT Hub appear in the store and the employee map, with timestamps | Proven for the demo, with a stale tail | Map 200 with 443 items; case readings to 13:35:00Z; hub-to-store hop inferred from the live path, and freshness went stale after the 13:30 failure |
