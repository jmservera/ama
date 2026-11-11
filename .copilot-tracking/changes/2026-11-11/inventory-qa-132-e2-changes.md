---
title: Inventory-managed staff intake and independent QA 132 extension E2 changes
ms.date: 2026-11-11
---

Extension E2 of five. Refs #132, #131, #440. Test-only; no application, permission, manifest, infrastructure, memory, pack or shared-log change.

## Change

* `src/api/tests/test_staff_intake_api.py`: import `TENURE_HOLD` from Core; helpers `declare_inventory` (real `tenure_inventory_record` route, `Unknown`) and `assert_held`; two cases:
  * `test_inventory_hold_after_capture_is_not_cleared_by_acknowledgement_or_qa`
  * `test_inventory_hold_after_acceptance_refuses_handover_and_a_later_capture_stays_held`
* No existing assertion changed. The existing non-inventory positive control `test_recorder_is_denied_and_independent_qa_accepts` is reused unchanged.

## Observed behaviour asserted (not invented)

* Capture while held is not refused; it records a `Submitted` receipt. Acknowledgement while held returns 200 and leaves `Submitted`. Independent accept and handover are refused 409 with the inventory-Unknown reason and `TENURE_HOLD`.

## Validation (venv `/tmp/venv-132-inv-qa-1111`, editable core, agents, api from this worktree, import origins asserted; HOME `/tmp/home-132-1111`)

| Check | Exit | Result |
| --- | --- | --- |
| API `test_staff_intake_api` (final, includes both new cases on the SQLite base class and the JSON subclass) | 0 | 96 run, OK, 36 skipped (32 MSSQL class, 4 SQL-store-contract tests on JSON) |
| Core `-k inventory test_resident_decisions` | 0 | 48 run, OK, 17 skipped (opt-in loopback SQL Server) |
| Core gate selectors `test_resident_acceptance_never_clears_technical_or_hazard_gates`, `test_quality_dependencies_are_scoped_and_unknown_evidence_cannot_release` | 0 | 6 run, OK, 2 skipped |
| API `-k inventory test_resident_api` | 0 | 1 run, OK |
| API `test_role_endpoint_inventory test_dependency_rule` | 0 | 26 run, OK |
| `ruff check .`, `ruff format --check .`, `mypy` (api) | 0 | clean, 228 source files |
| `git diff --check` | 0 | clean |
| Staff intake browser and axe (`ZF_STAFF_INTAKE_BROWSER=1`, pinned axe 4.10.3, SHA-256 `880970c0...8a68bb`, `flock -n` heavy lock free) | 0 | 2 run, OK, no axe violations in 5 observed states |

## Retained failed attempts

* `python -m unittest tests.test_staff_intake_api` from `src/api`: import error (modules are top-level via `PYTHONPATH=tests`); documented invocation used.
* Core gate selector with a guessed class name: error 1, retained as `core-gate1-wrongname`; rerun with `-k`.
* Negative control with `_inventory_managed` patched False (in-process, no source edit): both new cases error at the inventory view assertion, which shows they depend on the gate but is a weak control. It is not a mutation-test claim.

## Limits

* JSON and SQLite only; MSSQL, hosted CI, human QA, resident consent and Legal tenure review unobserved. The browser observation is independent of the API/QA cases.
