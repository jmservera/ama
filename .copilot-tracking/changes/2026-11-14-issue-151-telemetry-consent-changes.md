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

## Cycle 2 changes

* `src/core/tests/test_telemetry_consent.py`: typed `process` with `Mapping[str, object]` and `Receipt`, clearing all 5 mypy errors.

### Cycle 2 validation

* `python3 -m mypy` (316 files), `ruff check .` and `ruff format --check .` in `src/core`: pass.
* `PYTHONPATH=src:tests python3 -m unittest tests/test_telemetry_consent.py -v`: 4 pass. The bare `python3 -m unittest tests/test_telemetry_consent.py` fails in this worktree on import because `zava_forward` is not installed (environment, pre-existing; same for other tests).
* Not run: full local RPI gate, hosted CI.
