---
title: Issue 187 anomaly injector changes
ms.date: 2026-11-14
---

## Changes

* Added `src/core/src/zava_forward/core/synthetic/sensor_injector.py`.
* Added `src/core/tests/test_sensor_injector.py`.

## Validation

* `ruff check` and `ruff format --line-length 100 --check` on `src/core`: pass.
* `PYTHONPATH=src python3 -m unittest tests.test_sensor_injector tests.test_sensor_scenarios tests.test_sensor_faults`: 32 tests OK. The installed package resolves to another checkout, hence PYTHONPATH.
* Not run: full local gate, hosted CI, independent review.

## Divergences

None. Wiring the injector into `sensor_backfill` and fixing the `resident_showcase` `injected_fault` allowance are not done.
