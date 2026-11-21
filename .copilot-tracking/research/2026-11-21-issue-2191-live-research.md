---
title: Issue 2191 live research (2026-11-21)
ms.date: 2026-11-21
---

Research disposition: executed. Planning Readiness: Ready.

## Findings

* The cohort is the `homes` list of the `live-sim-control-v1` document (`src/api/src/zava_forward/api/live_control.py`), capped by `MAX_COHORT = 100`; `tools/demo_consent_mix.py` `plan()` repeats the 100 cap and builds the 10 granted and 10 declined controls (first half granted). The live store holds at least ZF-2025-0331, so half of all homes exceeds 100; the cap blocks the goal.
* `send_slot` in `live_simulator.py` sends one reading per cohort home per slot; there is no way for a device to skip or fail. Capacity limits (`check_capacity`: 1,250 homes at 5 minutes, 10 messages per second) allow several hundred homes.
* Device identities are registered per home out of band, so cohort growth on live Azure needs provisioning, which this task must not do.

## Design

* `select_cohort(all_homes, coverage)` in `tools/demo_consent_mix.py`: deterministic, evenly spread, at least half of all homes, with an alternating consent split.
* `MAX_COHORT` 100 to 500 in the control and the planner.
* Intermittent failures: `--failure-rate` / `ZF_SIM_FAILURE_RATE` (0 to 0.9, default 0), a seeded per home per slot decision; the device sends nothing and the slot summary counts it as `skipped` with code `DEVICE_SKIPPED`.

## Not provable offline

Live coverage on `ca-cutover-test-demo-api`, device registration and job env changes (the brief forbids touching live Azure).
