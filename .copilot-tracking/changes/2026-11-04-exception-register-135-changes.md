---
title: Exception register changes (#135)
ms.date: 2026-11-04
---

## Added

* `src/core/src/zava_forward/core/exception_register.py`
* `src/api/tests/test_exception_register.py`

## Modified

* `src/core/src/zava_forward/core/store.py` (mixin)
* `src/api/src/zava_forward/api/server.py` (route)
* `src/api/tests/test_role_endpoint_inventory.py`
* `src/core/README.md`

## Validation run

* `test_exception_register` (12), `test_exception_queue`, `test_exception_feeds`, `test_continuity`, `test_error_logging`, `test_role_endpoint_inventory`: pass.
* ruff check and format, mypy (`--cache-dir=/tmp/mypy-135`) on the new module: pass.

## Not run

Complete gate, full suites, benchmarks, browser checks, hosted CI. No divergence from the plan.
