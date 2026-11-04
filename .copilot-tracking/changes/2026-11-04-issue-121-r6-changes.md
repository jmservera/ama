---
title: Issue 121 r6 changes
date: 2026-11-04
---

* `src/api/src/zava_forward/api/server.py`, `src/core/src/zava_forward/core/projection.py`: read-only `/api/data-protection`.
* `src/api/tests/test_ai_tasks.py`: route test. `src/core/README.md`, `docs/reference/log.md`: documentation.
* Validation run: test_ai_tasks and test_coordinator_api (90 tests OK, 9 skipped), test_data_protection (12 OK), ruff check, mypy on data_protection.py (--cache-dir=/tmp/mypy-530). Not run: complete gate, benchmarks, full suites, hosted CI, mypy on server.py.
* No divergences.
