---
title: Issue 151 telemetry consent changes
ms.date: 2026-11-14
---

## Changes

* Added `src/core/src/zava_forward/core/telemetry_consent.py`.
* Added `src/core/tests/test_telemetry_consent.py` (4 tests).

## Validation

* `ruff check` and `ruff format --line-length 100 --check` on `src/core`: pass.
* Unit tests `test_telemetry_consent`, `test_sensor_consumer`, `test_sensor_view_health`: 44 pass.
* Not run: full local RPI gate, hosted CI, MSSQL path, API/UI wiring.
