---
title: Issue 82 round 2 changes
ms.date: 2026-11-04
---

* Changed `src/core/src/zava_forward/core/gates.py`: `booking_gates`, `BOOKING_RULES`.
* Changed `src/core/src/zava_forward/core/store.py`: `require_booking_gates`, called in `advance`.
* Changed `src/core/tests/test_gates.py`: booking gate tests.

Divergence: none. Validation: unit tests for gates, buildings, consultation, finance, governance, hazard, progress, procurement, resident and stock suites passed; ruff and mypy (cache /tmp/mypy-530) clean on touched files. Not run: complete gate, full suites, benchmarks, SQL store suite.
