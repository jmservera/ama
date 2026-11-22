---
title: Issue 2191 live research, fresh stored readings for half of homes
ms.date: 2026-11-22
---

Refs #2191, #184, #165. Research disposition: executed. Planning Readiness: Ready.

## Question

Owner measurement: 110 of 441 homes (24.9%) have a fresh stored reading, although the live simulator cohort is 222 of 443 homes. Diagnose cap, failureRate, cohort, batch size and job schedule; fix through code and image-only or env job updates (no Bicep, ACR stays Disabled).

## Live baseline (throwaway read-only job `job-2191-probe`, 2026-11-22 05:17 UTC, deleted after)

* Store homes 443; `sensor_consumer_control` rows 222 (granted 111, declined 111).
* Distinct homes with a stored `sensor_reading` in the last 15, 30 and 60 minutes: 105, 111, 111. Latest stored reading 05:15, probe time 05:17:33.
* `job-live-simulator`: cron `*/5 * * * *`, replicaTimeout 240 s, args `--max-per-second 10`, `ZF_SIM_FAILURE_RATE=0.1`, 445 secrets (222 pem/key pairs plus control.json); last six executions Succeeded in 87 to 112 s.
* `job-live-receiver`: cron `*/30`, window 1500 s, timeout 1620 s, same image digest.

## Diagnosis by suspect

| Suspect | Finding |
| --- | --- |
| Cap | Not binding. `MAX_CONTROLS` and `live_control.MAX_COHORT` are 500; 445 secrets are accepted. Hub device identities are capped at 100 only in the provisioning manifest, not for hand-registered devices. |
| failureRate | Small effect. 0.1 skips about 10% per slot; a home is stale only after three consecutive skipped slots, but ingestion lag makes the instant count 105 of 111 (94.6%). |
| Cohort | Necessary but not sufficient: 222 homes (50.1%) are sending. |
| Consent mix | Root cause. `GRANTED_SHARE = 0.5` in `tools/demo_consent_mix.py` declines half the cohort. A declined home is rejected at the receiver (reason CONSENT) and never stored, so stored coverage is bounded at 111 of 443 = 25.1%. |
| Batch size | Not binding. `batch_size` 50 inside a 1 to 500 limit; runs take about 100 s of 240 s. |
| Schedule | Not binding. Five minute cron matches the slot; freshness window is 15 minutes (three slots). |

## Decision input

To store a fresh reading for at least 222 of 443 homes the granted count must be at least 222 plus headroom for the 94.6% instant freshness and skips. Granted 247 (443 x 0.5 / 0.9) gives an expected 233 fresh. Keep a visible declined minority (10% of granted, 25 homes) so the consent mix stays demonstrable. Cohort 272 homes, 545 secrets (above the tested 449; az rejects an update atomically if a platform limit applies). Run time rises to about 140 s; replicaTimeout moves to 270 s by `az containerapp job update` (no Bicep).

## Planning Readiness

Ready. Code change is confined to `tools/demo_consent_mix.py` and its test. A throwaway probe confirmed the deployed image (`sha256:295164ca...`) has `MAX_CONTROLS = 500`, so the consent run needs no shim.
