---
title: Issue 109 live run research (handover non-finite guard)
ms.date: 2026-11-23
---

Refs #109. Research disposition: executed. Planning Readiness: Ready.

## Evidence

* Issue #109 has one unticked criterion (the #440 stabilization checkpoint), an owner and coordinator process outcome that code cannot satisfy.
* Earlier notes (2026-11-18 live probe, 2026-11-19 research gate guard, 2026-11-17 closure audit) cover live hub behaviour and the R1 to R3 guard. The handover continuity check in `sensor_ingest.py` was not covered.
* New angle: `handover_continuity` accepts caller-supplied rows. A probe showed `temperature_c="NaN"` raises `decimal.InvalidOperation` (not the documented `ValueError` reason codes), `"abc"` does the same, and `"Infinity"` yields `passed: False` with infinite metrics instead of a refused observation.

## Decision

Validate each channel value as a finite Decimal in `_indoor_series` and raise `INVALID_HANDOVER_OBSERVATION`. Regression test in `src/core/tests/test_sensor_ingest.py`. Tier FULL not run by the worker (`rpi-checks.py --all` forbidden); focused tests plus mypy and ruff are recorded.

## Live Azure

No Azure change is needed; the defect is pure code. The 2026-11-18 live evidence stands.
