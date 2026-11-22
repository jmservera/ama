---
title: Issue 2191 live fresh stored readings for half of the homes, 2026-11-22
description: Why only 24.9 percent of homes had a fresh stored reading, the cohort and receiver fixes applied live, and measured coverage with a per-criterion table
ms.date: 2026-11-22
---

Refs #2191. Synthetic demo, desktop only. Live Azure in resource group `ama` under the owner decisions of 2026-11-18. No Bicep change, registry `crcutovertestrzsrg` read back `Disabled` (export policy `disabled`, default action `Deny`, no IP rules) after the push.

## Diagnosis

The starting figure was 110 of 441 homes (24.9 percent) with a fresh stored reading ([2202 deploy note](./issue-2202-live-deploy-2026-11-22.md)). Two separate limits explain it.

| Candidate | Finding |
| --- | --- |
| Consent mix | The 222 home cohort was half granted, half declined (`GRANTED_SHARE = 0.5` in `tools/demo_consent_mix.py`). The receiver rejects declined homes with reason `CONSENT` and never stores them, so stored coverage could not exceed 111 of 443 (25 percent). This is the root cause. |
| Control cap | Not binding: the deployed image has `MAX_CONTROLS` 500. |
| Batch size, schedule | Not binding at the 5 minute schedule (50 per batch, 272 devices run in about 140 s). |
| `failureRate` 0.1 | Small effect: about 10 percent of a run is skipped. |
| Receiver and SQL throughput | Binding once more homes are granted. The receiver stores 35 to 42 events a minute (one SQL write per event, Standard tier `retrofit` database at 100 percent DTU in several 5 minute buckets). A 5 minute run of 245 events needs about 6.5 minutes to drain. |
| Receiver start position | `starting_position="-1"` with no checkpoint replayed from the oldest retained event on every 30 minute window, spending the window on readings that were already stale. |

## Changes

* `tools/demo_consent_mix.py` (`select_reading_cohort`, `plan(..., granted=)`, CLI `select-readings` and `--granted N`): granted homes at least 50 percent of all homes plus 15 percent headroom for skipped runs and ingest lag, and about 10 percent of the cohort declined so the consent mix is kept. For 443 homes: 261 granted, 27 declined, cohort 288.
* `src/api/.../iot_stream.py`: optional `ZF_RECEIVER_LOOKBACK_SECONDS` (60 to 86400). A bounded window then starts that far back instead of at the oldest retained event; unset keeps the previous behaviour. Tests in `src/api/tests/test_iot_stream.py`.
* Live configuration (no Bicep): `job-live-simulator` secrets for 288 devices plus `control.json` (545 then 577 secrets), `replicaTimeout` 270, `ZF_SIM_FAILURE_RATE` 0.1 unchanged, schedule `0,7,15,22,30,37,45,52 * * * *` (a 7.5 minute cadence so two runs fall in the 15 minute freshness window while the receiver drains one); `job-live-receiver` image `zava-forward-api@sha256:01f67a0140a58725f6c36786a1ac6da2b3a49ab7c0d6391b5233b020c25755b3` (pushed through `/tmp/acr-push.sh`) with `ZF_RECEIVER_LOOKBACK_SECONDS=360` and the new `control.json`.
* Hub devices: 54 registered, 122 retired devices deleted, 0 failures, through throwaway jobs that used a temporary `IoT Hub Registry Contributor` assignment (removed and read back absent). Consent applied through the planner; read back 261 granted, 27 declined.

## Live measurements

Fresh means a stored `sensor_reading` with `observed_at` in the last 15 minutes, counted per distinct home out of 443, sampled every 2 minutes by a throwaway job (08:07 to 08:45 UTC, 20 samples after the final configuration).

* Range 14.9 to 56.7 percent, mean 39.9 percent, 7 of 20 samples at or above 50 percent (peaks 51.7, 50.3, 52.4, 55.1, 52.4, 55.5, 56.7).
* The series is a sawtooth: each run lifts coverage to 51 to 57 percent about 6 to 8 minutes after it starts, then it falls to 15 to 45 percent before the next run is stored.
* The staff app (Playwright, 50 listed cases at 08:55 UTC): 28 `ok` and `fresh`, 2 `ok` and `stale`, 20 `consent-withheld`. Screenshots: [fresh home](./issue-2191-live-readings-fresh-home-2026-11-22.png) ("Recent reading (within 15 minutes)") and [consent-withheld home](./issue-2191-live-readings-withheld-home-2026-11-22.png).

Earlier configurations, for comparison: 5 minute cadence with 272 devices left the receiver 20 minutes behind (stored distinct homes per slot about 105 to 113); a 10 minute cadence with a 600 s lookback gave a peak of 54.6 percent and troughs near 0 to 23 percent.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Cohort covers at least half of all homes, with a fresh stored reading | Unproven as a steady state | Cohort of 288 homes with 261 granted (58.9 percent of 443) is configured and peaks of 51.7 to 56.7 percent were measured, but the mean over 20 samples is 39.9 percent and 13 of 20 samples are below 50. |
| Configurable intermittent failure rate | Proven | `ZF_SIM_FAILURE_RATE` 0.1 read back on the live job; about 10 percent of runs skipped; existing simulator tests. |
| Consent mix preserved | Proven | 261 granted, 27 declined read back from `sensor_consumer_control`; declined homes show `consent-withheld` in the staff app. |
| Unit tests | Proven (local) | `tools/test_demo_consent_mix.py` 7 tests; `src/api/tests/test_iot_stream.py` 47 tests; mypy and ruff clean. |
| Refs #184, #165 | Not changed | Referenced only. |

## Why the main criterion is unproven and what would fix it

The limit is receiver write throughput, not the cohort. Each event is a separate SQL transaction on a Standard tier database that is already at its DTU limit, so the receiver cannot drain 245 events a run inside the part of the 15 minute window that a run stays fresh. Options, in order of effort:

1. Batch the receiver writes (use `receive_batch` and one transaction per batch) in `iot_stream.py` and `SensorConsumer.consume`; this is security-sensitive ledger code and needs the full gate.
2. Raise the SQL service objective (an estate change outside this task's authority).
3. Lower the freshness cost by sending fewer events per run, for example half the cohort per run, which needs a simulator change.

## Cleanup receipts

* Throwaway jobs: none remain (`az containerapp job list` shows the three demo jobs plus `job-live-simulator` and `job-live-receiver`).
* Temporary role assignment on `id-cutover-test-api`: removed, read back absent.
* Private key material and job definitions in `/tmp` shredded.
* Registry restored to `Disabled`; one interrupted push attempt left it open for a few minutes and it was restored and read back with no IP rules.
* Live state left in place: 288 device cohort, 7.5 minute cadence, receiver lookback 360 s.
