---
title: Issue 190 retained-store scenario changes
ms.date: 2026-11-04
---

* Added `src/core/tests/test_retrofit_scenarios_retained_store.py` (3 tests).
* Appended a `docs/reference/log.md` entry.
* No production code changed.

Validation run (focused only, `PYTHONPATH=src:tests` from `src/core`): the 3 new tests pass (about 73 s); ruff check and format clean; mypy with `--cache-dir=/tmp/mypy-190` reports no error in the new file. Not run: gate, full suites, benchmarks, SQL Server, hosted CI.
