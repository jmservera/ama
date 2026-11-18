---
title: Issue 222 decision criteria changes
ms.date: 2026-11-14
---

## Changes

* Added `src/core/src/zava_forward/core/ai_decision.py`.
* Added `src/core/tests/test_ai_decision.py` (9 tests).

## Validation

* `mypy` (whole core project): no issues in 316 files.
* `ruff check` and `ruff format --line-length 100 --check` on both files: clean.
* `PYTHONPATH=src:tests python3 -m unittest tests/test_ai_decision.py`: 9 tests OK.
* Hosted CI, the complete local gate and independent review were not run.

## Not delivered

Approved real thresholds per feature, registry or API wiring and feeding observed values from
`rai_metrics` remain open.
