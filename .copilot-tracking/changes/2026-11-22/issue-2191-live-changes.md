---
title: Issue 2191 changes record
ms.date: 2026-11-22
---

Refs #2191. Tier FULL for the `src/api` edit (focused checks run; `rpi-checks.py --all` deliberately not run per the brief). Evidence: [research note](../../../docs/reference/research/issue-2191-live-readings-2026-11-22.md).

## Source changes

* `tools/demo_consent_mix.py`, `tools/test_demo_consent_mix.py`: reading-share cohort (`select_reading_cohort`, `plan(..., granted=)`, `select-readings`, `--granted`); 443 homes give 288 in the cohort, 261 granted.
* `src/api/src/zava_forward/api/iot_stream.py`, `src/api/tests/test_iot_stream.py`: optional `ZF_RECEIVER_LOOKBACK_SECONDS` for bounded windows (default unchanged).

## Live changes (image and job configuration only)

Simulator job secrets (577), cron `0,7,15,22,30,37,45,52 * * * *`; receiver image `sha256:01f67a01...` with lookback 360 s and the new control; 54 devices registered, 122 deleted; consent 261 granted and 27 declined. Temporary role removed, throwaway jobs deleted, registry `Disabled`, keys shredded.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| At least half of homes with a fresh stored reading | Unproven (steady state) | 20 samples: 14.9 to 56.7 percent, mean 39.9, 7 at or above 50; limited by receiver SQL write throughput |
| Cohort sized for at least half the homes | Proven | 261 granted of 443 (58.9 percent) read back |
| Configurable intermittent failure rate | Proven | `ZF_SIM_FAILURE_RATE` 0.1 on the live job |
| Consent mix preserved | Proven | 261 granted, 27 declined; withheld homes shown in the staff app |
| Unit tests | Proven (targeted) | consent mix 7 tests; iot_stream, live_control, live_simulator and receiver tests 158 OK (2 skipped); mypy and ruff clean. A full `src/api` discover run hit its 1500 s timeout with no summary, so it is not claimed. |
| Refs #184, #165 | Not changed | referenced only |
