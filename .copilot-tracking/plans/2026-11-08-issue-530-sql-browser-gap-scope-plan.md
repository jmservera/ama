---
title: Issue 530 actual SQL and employee browser gap scope plan
ms.date: 2026-11-08
---

* Research: [.copilot-tracking/research/2026-11-08-issue-530-sql-browser-gap-scope-research.md](../research/2026-11-08-issue-530-sql-browser-gap-scope-research.md)
* Details: [.copilot-tracking/details/2026-11-08-issue-530-sql-browser-gap-scope-details.md](../details/2026-11-08-issue-530-sql-browser-gap-scope-details.md)
* Tier FULL for the eventual candidate; now only code plus LIGHT unit/static checks. Refs #530 only; no closing keyword.

## Phases

* [ ] Phase 1: independent critique of this plan and details before any code.
* [ ] Phase 2: browser wiring in `tools/rpi-checks.py` (plan, execution, verifier) with `tools/test_rpi_checks.py` regressions.
* [ ] Phase 3: actual-MSSQL chat tests in `src/api/tests/test_mssqlstore.py` plus the runner required-test verifier and regressions.
* [ ] Phase 4: LIGHT checks in a new external venv, authored Review, state, commit, freeze.
* [ ] Phase 5 (future, NOT admitted): fresh-Main FULL 17-group gate under the canonical lock, jobs 1, `--lock-timeout 0`, verified receipt, independent exact-head review, hosted CI.

## Stop rules

Stop and route if a change outside `src/*/tests`, `tools/rpi-checks.py`, `tools/test_rpi_checks.py` and directly dependent docs is needed, if Main moved, if a production defect reproduces, or if any execution of runner, SQL, Docker, browser, lock or live endpoint seems required.
