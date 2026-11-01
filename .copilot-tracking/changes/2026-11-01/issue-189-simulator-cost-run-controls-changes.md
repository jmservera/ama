---
title: Issue 189 changes
ms.date: 2026-11-01
task_id: issue-189
---

## Added

* `src/core/src/zava_forward/core/synthetic/run_plan.py`: `RunPlan`, `Estimate`, `record`, `RunController`, CLI.
* `src/core/tests/test_run_plan.py`: 12 tests.

## Modified

* `src/core/README.md`: "Cost estimate and run controls (#189)" section.

## Validation (focused tier, venv with pip)

* `unittest tests.test_run_plan tests.test_sensor_stream`: 26 tests OK.
* `ruff check`, `ruff format --check`, `mypy` in `src/core`: clean.
* No heavy local gate; CI is the evidence.

## Divergences

None from the plan.
