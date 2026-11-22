---
title: Issue 2191 fresh coverage re-proof after the S3 change, 2026-11-22
description: A second 30 minute live series, 18:35 to 19:03 UTC, showing 51.5 to 58.5 percent of 443 homes with a fresh stored reading on SQL S3, and why the earlier 24.9 percent figure came from DTU saturation and the consent mix
ms.date: 2026-11-22
---

Refs #2191. Synthetic demo, desktop only. Live Azure in resource group `ama` under the owner decisions of 2026-11-18. No change was made to the estate, code or consent data in this pass; no push.

## Why stored readings lagged the cohort

The 110 of 441 (24.9 percent) figure was a result of two limits, both already diagnosed in earlier notes:

* Consent mix: the 222 home cohort was half granted, so the receiver could store at most about 111 homes ([readings note](./issue-2191-live-readings-2026-11-22.md)). The cohort was rebuilt to 261 granted and 27 declined.
* SQL throughput: batching and the receiver window were not binding; the 10 DTU Standard S0 database sat at 100 percent DTU, so stored rows trailed the simulator ([capacity note](./issue-2191-live-sql-capacity-2026-11-22.md)). The `retrofit` database was moved to S3 with `az` at 13:51 UTC.

Smallest cause fixed: the SQL tier (job settings unchanged: simulator `0,7,15,22,30,37,45,52 * * * *`, `ZF_SIM_FAILURE_RATE` 0.1, receiver `*/30 * * * *`, `--seconds 1500`).

## Read back at 18:30 UTC

* `retrofit`: Standard, 100 DTU (S3), Online.
* DTU in 15 minute buckets 17:35 to 18:50 UTC: average 18.1 to 20.0 percent, maximum 82 to 87 percent. The earlier ceiling of 100 percent no longer binds.
* Receiver executions 17:00, 17:30 and 18:00 `Succeeded`.

## Sample series

Method: a throwaway Container Apps job (`job-tmp-sampler2191b`, receiver image and identity, `mssql_python`, read only) counted `COUNT(DISTINCT home_id)` of `sensor_reading` rows with `observed_at` in the last 15 minutes, every 2 minutes, against 443 homes. Target: 222 homes (50 percent). Raw lines are in `.copilot-tracking/evidence/2026-11-22/issue-2191-halfhomes/samples.txt`.

| Time (UTC) | Fresh homes | Percent of 443 |
| --- | --- | --- |
| 18:35:33 | 231 | 52.1 |
| 18:37:33 | 233 | 52.6 |
| 18:39:33 | 259 | 58.5 |
| 18:41:33 | 259 | 58.5 |
| 18:43:33 | 259 | 58.5 |
| 18:45:33 | 236 | 53.3 |
| 18:47:33 | 256 | 57.8 |
| 18:49:33 | 256 | 57.8 |
| 18:51:33 | 228 | 51.5 |
| 18:53:33 | 247 | 55.8 |
| 18:55:33 | 256 | 57.8 |
| 18:57:33 | 256 | 57.8 |
| 18:59:33 | 256 | 57.8 |
| 19:01:33 | 249 | 56.2 |
| 19:03:33 | 259 | 58.5 |

All 15 samples met the target; minimum 228, maximum 259, mean 249.3 homes (56.3 percent). The sampler was deleted afterwards and the job list read back without it.

## Remaining risks

* The measure is the 15 minute window used by the employee freshness badge. Counts inside 5 minutes swing from 0 to 236 because the simulator runs every 7 to 8 minutes in bursts; this is the intended intermittent pattern, not a failure.
* Receiver logs for finished executions stay unreadable; DTU and execution history are the evidence.
* S3 costs about USD 5 a day; a measured step down to S2 is a later owner decision.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Cohort covers at least half of all homes with fresh readings | Proven for the demo | 15 of 15 samples at 51.5 to 58.5 percent, mean 56.3 percent, 18:35 to 19:03 UTC |
| Configurable intermittent failure rate | Proven | `ZF_SIM_FAILURE_RATE` 0.1 read back on `job-live-simulator`; sparse 5 minute counts show skipped cycles |
| Consent mix preserved | Proven (prior evidence) | 261 granted, 27 declined in the [readings note](./issue-2191-live-readings-2026-11-22.md); consent data untouched here |
| Unit tests | Not rerun | No source change; recorded in the earlier notes |
| Refs #184, #165 | Not changed | Referenced only |
