---
title: Issue 2191 live SQL capacity and fresh coverage, 2026-11-22
description: Why batched receiver writes still left fresh coverage near 38 percent, the Azure SQL tier raised from S0 to S3 with az, and a 30 minute sample series above half of all homes
ms.date: 2026-11-22
---

Refs #2191. Synthetic demo, desktop only. Live Azure in resource group `ama` under the owner decisions of 2026-11-18. No Bicep change, no push, simulator and receiver left running.

## Diagnosis

The receiver already ran with `ZF_RECEIVER_BATCH_SIZE=10` and `ZF_RECEIVER_LOOKBACK_SECONDS=360` (read back from `job-live-receiver`). Fresh coverage still averaged 37.7 percent.

| Candidate | Finding |
| --- | --- |
| SQL tier | `retrofit` database was Standard S0 (10 DTU, `autoPauseDelay` null, so not serverless and never paused, online). The `dtu_limit` metric read 10. |
| DTU use | `dtu_consumption_percent` maximum was 100 in every 15 minute bucket over the preceding 3 hours; the average was 99.95 and 99.75 in the buckets with heavy receiver activity (12:10, 12:40, 13:10 UTC). This is the binding limit. |
| Connection errors | `connection_failed` and `deadlock` metrics were 0, so the `SQL_UNAVAILABLE` seen at larger batches is throttling at the DTU ceiling, not an outage. |
| Simulator rate | `job-live-simulator`: schedule `0,7,15,22,30,37,45,52 * * * *`, `replicaTimeout` 270, `ZF_SIM_FAILURE_RATE` 0.1; runs succeeded in about 2 minutes each. About 440 to 480 readings are sent per two runs in the 15 minute window. Not binding. |
| Receiver | `job-live-receiver`: `*/30 * * * *`, window `--seconds 1500`. Batching only reduces round trips; each stored row still costs DTU. |
| Logs | The Log Analytics workspace `log-cutover-test` denies public queries (`NspValidationFailedError`) and finished job executions keep no replica logs, so receiver logs could not be read after the fact. DTU and execution history are the evidence. |

## Change

One live change, made with `az sql db update -g ama -s sql-cutover-test-rzsrg -n retrofit --service-objective S3` (13:51:29 to 13:53:49 UTC; read back SKU Standard, capacity 100, Online). S3 is 100 DTU. At about USD 5 a day it is well inside the USD 700 cap. No other setting changed.

The scale dropped the connections of the running receiver, so `job-live-receiver-29922570` ended `Failed` and the stored count stalled at 45 from 13:55 to 13:59 until the 14:00 run started.

## Samples

Method: a throwaway Container Apps job (`job-tmp-sampler2191`, same image and identity as the receiver, read only SQL) counted `COUNT(DISTINCT home_id)` of `sensor_reading` rows with `observed_at` in the last 15 minutes, against 443 total homes. The job was deleted afterwards and the job list read back without it.

Before the change (S0, 13:43 to 13:51 UTC):

| Time (UTC) | Fresh homes | Total homes | Percent |
| --- | --- | --- | --- |
| 13:43:05 | 239 | 443 | 54.0 |
| 13:45:05 | 102 | 443 | 23.0 |
| 13:47:05 | 147 | 443 | 33.2 |
| 13:49:06 | 191 | 443 | 43.1 |
| 13:51:06 | 4 | 443 | 0.9 |

Mean of the five samples: 30.8 percent. The series is a sawtooth driven by the receiver falling behind the simulator.

Transition (S3 applied, receiver interrupted): 13:53 35, 13:55 45, 13:57 45, 13:59 45 fresh homes (7.9 to 10.2 percent).

After the change (S3, 30 minute sample from the 14:00 receiver start):

| Time (UTC) | Fresh homes | Total homes | Percent |
| --- | --- | --- | --- |
| 14:01:00 | 18 | 443 | 4.1 |
| 14:03:00 | 237 | 443 | 53.5 |
| 14:05:00 | 237 | 443 | 53.5 |
| 14:07:00 | 237 | 443 | 53.5 |
| 14:09:00 | 255 | 443 | 57.6 |
| 14:11:00 | 260 | 443 | 58.7 |
| 14:13:00 | 260 | 443 | 58.7 |
| 14:15:00 | 260 | 443 | 58.7 |
| 14:17:01 | 256 | 443 | 57.8 |
| 14:19:01 | 258 | 443 | 58.2 |
| 14:21:01 | 229 | 443 | 51.7 |
| 14:23:01 | 242 | 443 | 54.6 |
| 14:25:01 | 256 | 443 | 57.8 |
| 14:27:01 | 256 | 443 | 57.8 |
| 14:29:01 | 256 | 443 | 57.8 |
| 14:31:01 | 246 | 443 | 55.5 |

The 14:01 sample precedes the first stored batch of the new receiver window. Over the 15 samples from 14:03 to 14:31 the mean is 56.4 percent (minimum 51.7, maximum 58.7); including 14:01 the mean of all 16 is 53.1 percent. Every sample after the first met the half-of-all-homes target (221.5 homes). DTU in the same period: 5 minute maxima of 81 and 89 percent, averages 14.6 to 21.4 percent per 15 minutes (13:54 to 14:31).

## Remaining risks

* The receiver window restarts every 30 minutes; a restart shows as a short dip (the 14:01 sample). A scale or restart mid window fails the running execution.
* S3 stays in place. Returning to S0 would bring the saw tooth back; a later owner decision can step down to S2 after a measured trial.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Cohort covers at least half of all homes with fresh readings | Proven for the demo | 15 of 16 samples in the table, 51.7 to 58.7 percent, mean 56.4 percent over 14:03 to 14:31 UTC on S3. |
| Configurable intermittent failure rate | Proven | `ZF_SIM_FAILURE_RATE` 0.1 read back on `job-live-simulator`. |
| Consent mix preserved | Proven (prior evidence) | 261 granted, 27 declined in the [2026-11-22 readings note](./issue-2191-live-readings-2026-11-22.md); no consent data changed here. |
| Unit tests | Not rerun | No source change; the tests are recorded in the earlier note. |
| Refs #184, #165 | Not changed | Referenced only. |
