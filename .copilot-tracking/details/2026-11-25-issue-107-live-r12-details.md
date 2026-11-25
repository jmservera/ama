---
title: Issue 107 live r12 details
ms.date: 2026-11-25
---

Phase 2: in `src/api/tests/assistant_process_worker.py` add `ROUTE`, applied to the fake provider after construction; kinds `provider`, `endpoint`, `deployment` (`fast`). In `test_assistant_release.py` add three tests calling `check_process_wide_binding(kind, "model", kind)`. Success: each revokes the release in the changed process, a fresh original process stays denied with no provider call or allowance change.
Phase 3: `python3 -m unittest tests.test_assistant_release tests.test_assistant_restart_non_replenishment` from `src/api`; same on a disposable SQL Server 2022 container removed afterwards; `ruff check`, `ruff format --check`, `python3 -m mypy`.
