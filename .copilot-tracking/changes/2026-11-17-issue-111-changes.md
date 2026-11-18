---
title: Issue 111 changes
ms.date: 2026-11-17
---

## Changes

* `src/core/tests/test_sensor_analysis.py`: add `test_policy_identity_binds_threshold` (expectedFailure).
* No source change. Divergence: none. Amendment: none.

## Validation (FOCUSED)

* Five-module targeted set (research artifact): 101 tests OK, 22 skipped (SQL Server opt-in), before the edit.
* `python3 -m unittest tests.test_sensor_analysis`: 12 tests OK, 1 expected failure.
* `mypy --no-incremental tests/test_sensor_analysis.py`: no issues. `ruff format --isolated --line-length 100 --check`: formatted.
* Not applicable: SQL Server, hosted CI, rpi-checks --all (heavy lock held), UI/AT.
