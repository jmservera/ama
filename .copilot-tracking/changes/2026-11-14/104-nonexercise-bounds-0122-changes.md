---
title: Issue 104 criterion 5 changes
ms.date: 2026-11-14
---

* `src/core/src/zava_forward/core/ai_consumption.py`: guard in `authorize` and `reserve_in`, optional authority alert fields.
* `src/api/tests/test_nonexercise_capability_bounds.py`: five tests; failing-first confirmed against HEAD core (errors on missing `alert` parameter), passing after.
* `src/agents/tests/test_epic104_bounded_ai_invariants.py`, `src/api/tests/test_resident_ledger_meter.py`: billable fixtures now bind an alert and owner.

## Divergence

Core tests have no billable authority fixtures; the full core suite was not run (focused tier).

## Validation

* `ruff check`, `ruff format --check`: clean in `src/core`, `src/api`; `mypy`: clean in both.
* Passed: `test_nonexercise_capability_bounds` (5), `test_ai_consumption_api` (40), core `test_ai_consumption`, `test_ai_consumption_safety`, `test_scenario_manifest` (48), agents `test_epic104_bounded_ai_invariants` (22), `test_resident_ledger_meter` (25).
* Tests ran with PYTHONPATH pointing at this worktree because the installed distributions point at another checkout.
* Not run: hosted CI, full core/api suites, infra tests.
