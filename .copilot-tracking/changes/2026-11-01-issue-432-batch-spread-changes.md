---
title: "Changes: #432 batch spread slice"
ms.date: 2026-11-01
---

* `src/core/src/zava_forward/core/ai_consumption.py`: `batch_spread` and `report(batch=)`.
* `src/core/tests/test_ai_consumption_demo.py`: 2 tests.
* Validation: 37 consumption tests pass (PYTHONPATH=src); ruff check, ruff format --check, mypy clean. CI is the remaining evidence.
* Divergence: none.

## Correction cycle 1

* `ai_consumption.py`: `batch_spread(totals, batch, roots)`; `report` passes `len(roots)`. Tests extended (null/empty references, missing-usage over-limit batch).
* Validation: ruff check, ruff format --check, mypy clean; tests see below in PR.

## Correction cycle 2 changes

* `src/core/tests/test_ai_consumption.py`: added `test_report_batch_spread_merges_authority_and_counts_missing_roots`.
* Validation: ruff check, ruff format --check, mypy (src/core) clean; test_ai_consumption and demo tests pass (38).
