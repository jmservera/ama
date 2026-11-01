---
title: Issue 222 cohort and missing-data evaluation changes
ms.date: 2026-11-01
---

## Changes

* Added `src/core/src/zava_forward/core/cohort_eval.py`.
* Added `src/core/tests/cohort_eval_fixture.py` and `src/core/tests/test_cohort_eval.py` (11 tests).

## Validation (focused tier, from `src/core`)

* `PYTHONPATH=src:tests python3 -m unittest test_cohort_eval test_dependency_rule`: OK.
* `ruff check`, `ruff format --check`, `mypy`: clean.
* Heavy local gate not run; CI is the evidence.

## Divergences

None.
