---
title: Issue 116 live round 4 details
ms.date: 2026-11-19
---

* Phase 1: in `projection.reason_roles()` filter `CONTRACTOR` from the parsed override; keep unset and empty semantics.
* Phase 2: tests in `Matrix`-based class of `test_role_matrix.py`: override `Contractor,Retrofit Programme Manager` yields only the manager; `can_see_reason(Contractor)` False; default tuple equals the three confirmed roles.
* Phase 3: `docs/reference/research/issue-116-live-r4-evidence-2026-11-19.md`, README index row, log entry.
* Phase 4: `python3 -m unittest` for the touched test module from `src/api`; `python3 -m mypy` in `src/core` and `src/api`; ruff format check.
