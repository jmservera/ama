---
title: Issue 126 round 1 changes
ms.date: 2026-11-03
---

* Modified `src/core/src/zava_forward/core/governance.py`, `src/api/src/zava_forward/api/server.py`, `src/core/tests/test_governance.py`, `src/core/README.md`, `docs/reference/log.md`.

## Validation

Run: `test_governance.py` (69 tests, 16 skipped opt-in MSSQL), `src/api/tests/test_governance*.py` (10 pass), ruff check (pass), mypy on `zava_forward.core` with cache /tmp/mypy-126 (pass).

Not run: the gate, benchmarks, full suites, MSSQL opt-in tests, browser checks. `ruff format --check` on governance.py reports it unformatted both before and after (pre-existing, not changed). `test_role_endpoint_inventory` has one failure (`/api/ai/report` 500) that also fails on unmodified main in this environment.

## Divergence

None from the plan.
