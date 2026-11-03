---
title: Changes, issue 176 fictional stock register generator
ms.date: 2026-11-03
---

* Added `src/core/src/zava_forward/core/synthetic/stock_register.py`.
* Edited `determinism_audit.py` (new generator, unavailable note) and `tests/test_determinism_audit.py`.
* Added `src/core/tests/test_stock_register.py`.
* Edited `docs/reference/research/retrofit-synthetic-data/README.md` and `docs/reference/log.md`.

No divergence from the plan. Validation: 28 tests across `test_stock_register`, `test_determinism_audit`, `test_stock_fabric` pass; ruff check and format and mypy clean on changed files. Not run: full suites, the complete gate, benchmarks.
