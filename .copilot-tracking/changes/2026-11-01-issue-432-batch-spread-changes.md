# Changes: #432 batch spread slice

* `src/core/src/zava_forward/core/ai_consumption.py`: `batch_spread` and `report(batch=)`.
* `src/core/tests/test_ai_consumption_demo.py`: 2 tests.
* Validation: 37 consumption tests pass (PYTHONPATH=src); ruff check, ruff format --check, mypy clean. CI is the remaining evidence.
* Divergence: none.

## Correction cycle 1

* `ai_consumption.py`: `batch_spread(totals, batch, roots)`; `report` passes `len(roots)`. Tests extended (null/empty references, missing-usage over-limit batch).
* Validation: ruff check, ruff format --check, mypy clean; tests see below in PR.
