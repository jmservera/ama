---
title: Issue 92 r1 changes
ms.date: 2026-11-03
---

* Added `contract_event_gate` to src/core/src/zava_forward/core/procurement.py.
* Added test_letting_and_renewal_gate_stays_blocked_while_unknown to src/core/tests/test_consultation_controls.py.
* Validation run: test_consultation_controls (39 tests OK, 14 skipped SQL Server) with PYTHONPATH=src:tests because the installed zava_forward points at another worktree; ruff check clean; mypy (cache /tmp/mypy-92) clean on procurement.py. ruff format reports procurement.py unformatted before and after (pre-existing).
* Not run: gate, benchmarks, full suites, SQL Server tests.
