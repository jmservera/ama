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
* `src/core/src/zava_forward/core/projection.py` (`exceptions` added to staff GET kinds; the route was unreachable)

## Validation run

* `test_exception_register` (12), `test_exception_queue`, `test_exception_feeds`, `test_continuity`, `test_error_logging`, `test_role_endpoint_inventory`: pass.
* ruff check and format, mypy (`--cache-dir=/tmp/mypy-135`) on the new module: pass.

## Not run

Complete gate, full suites, benchmarks, browser checks, hosted CI. No divergence from the plan.

## Review follow-up

* Feeds are guarded per case and per recommendation; failures are listed in `unrouted`.
* Empty-staff view and refusal are audited.
* `access.roles` shows only the caller's own entry (decision: other staff emails are not exposed; owner may widen).
* API-level tests cover 200 for named staff, 403 for others, audit and scoped content.
