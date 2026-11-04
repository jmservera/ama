---
title: Issue 92 r2 changes
ms.date: 2026-11-04
---

* src/core/src/zava_forward/core/procurement.py: add request_contract_event; exclude contract_event from authority lookup.
* src/core/tests/test_consultation_controls.py: two behavioural tests.
* Validation run: test_consultation_controls (45 tests OK, 16 SQL Server skipped; PYTHONPATH=src:tests), ruff check, mypy with /tmp/mypy-92.
* Not run: gate, benchmarks, full suites, SQL Server tests (not available).
