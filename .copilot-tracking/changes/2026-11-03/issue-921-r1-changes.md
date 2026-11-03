---
title: Issue 921 changes
ms.date: 2026-11-03
---

* src/api/src/zava_forward/api/server.py: flag set before flush; silent only if started.
* src/api/tests/test_error_logging.py: two regression tests.
* Validation run: test_error_logging (6 tests OK), ruff OK, mypy with --cache-dir=/tmp/mypy-921 reports only pre-existing unused type-ignore notes on untouched lines. Not run: full suites, gate, benchmarks.
