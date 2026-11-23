---
title: Issue 109 live changes
ms.date: 2026-11-23
---

Refs #109. Status: complete. Synthetic demo, desktop only; no Azure change made, no browser proof (no UI touched).

## Changes

* `src/core/src/zava_forward/core/sensor_ingest.py`: `_indoor_series` now refuses non-finite or non-numeric channel values with `INVALID_HANDOVER_OBSERVATION`. Before, `"NaN"` and `"abc"` leaked `decimal.InvalidOperation` and `"Infinity"` produced a failed report with infinite metrics.
* `src/core/tests/test_sensor_ingest.py`: `test_non_finite_channel_value_is_refused` (NaN, Infinity, -Infinity, text, both channels).

## Validation (focused tier; src change but `rpi-checks.py --all` is coordinator-owned)

* `PYTHONPATH=src:tests python3 -m unittest test_sensor_ingest test_sensor_handover test_sensor_non_authority -q` in `src/core`: 25 tests OK.
* ruff format and check on both files: clean. `python3 -m mypy`: 3 errors in 2 files (`telemetry.py` optional stubs, `device_provision.py` unused ignore), none in changed files.

## Per-criterion result

| Criterion | Result | Evidence or reason |
| --- | --- | --- |
| #440 stabilization checkpoint | Unproven | Owner and coordinator process outcome (BRD/PRD/ADR reconcile, bug disposition, residuals, defer decision). This run adds one bug fix and test as regression input only; merged children alone do not satisfy it. |
| All child features closed or deferred | Ticked already | Not re-proven here. |
| No sensor signal diagnoses a hazard, starts a clock, releases a hold or changes ranking | Ticked already | `test_sensor_non_authority` re-run and passing. |
