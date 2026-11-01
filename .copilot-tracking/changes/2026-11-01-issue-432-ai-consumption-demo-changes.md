# Changes: #432 AI consumption demo slice

* Added `src/core/src/zava_forward/core/ai_consumption_demo.py` (constructed SQLite ledger walk-through, synthetic-labelled).
* Added `src/core/tests/test_ai_consumption_demo.py` (5 tests).
* Documented the command in `src/core/README.md`; appended a `docs/reference/log.md` entry.
* Validation: `test_ai_consumption` and `test_ai_consumption_demo` pass (35 tests); `ruff check`, `ruff format --check` and `mypy` clean for the touched module.
* Divergence: none from plan. Plan phases 1 to 4 complete; phase 5 follows review.
