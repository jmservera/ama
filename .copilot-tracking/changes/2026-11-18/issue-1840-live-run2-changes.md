---
title: "Changes: issue 1840 completed() classification"
ms.date: 2026-11-18
---

Refs #1840. Base: pin `510fd90f` (child branch of the #107 topic). Status: implemented, focused tier.

## Changes

* `src/api/checks/old_image_sql_probe.py`: new `execution_gaps()` holds the execution/reinvoke checks formerly inline in `check_step`; `completed(name, step, tids)` now requires status ok plus no gaps (one record for the requested task, boolean `result`, text `after`, matching reinvoke capability/case with text `state`, no errors). `judge` passes the step name and task ids. New `assistant_config()` typed boundary replaces two untyped `config()` calls.
* `src/api/tests/test_old_image_sql_probe.py`: regression `test_incomplete_mismatch_completion_with_an_active_mutated_row_is_insufficient` (six subcases) and `outcome_of` helper.

## Validation (focused tier; no `rpi-checks.py`, no full gate)

* Failing-first: before the source change the six new subcases failed (`VIOLATED != INSUFFICIENT`); the pre-existing SelfTest also failed in the shared environment (editable installs point at the main checkout: `provision: unsupported`). Adverse attempt preserved.
* Shared env after fix: 41 tests, 1 failure (that SelfTest, identical at baseline: 40 tests, 1 failure).
* Isolated venv a private venv with this checkout's `core`, `agents`, `api` installed: `unittest tests.test_old_image_sql_probe` 41 tests OK, 0 skips; self-test ACCEPTED (lower fidelity, not old-image evidence).
* Bare `mypy` from `src/api`: at baseline 2 errors (`config` untyped, lines 1262 and 1424, reproduced); after fix `Success: no issues found in 312 source files` (shared env). In the isolated venv, 71 errors in 66 files, all missing Playwright stubs or unrelated test ignores, 0 in the probe.
* `ruff format --isolated --line-length 100 --check` and `ruff check` on both files: pass.
* Tier: the issue classes diagnostic correctness as security-sensitive (FULL). This run's owner brief mandates focused validation and forbids `rpi-checks.py --all`, so the full gate is NOT satisfied and a verified external receipt is still required before publication.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Failing-first regressions (missing result, missing reinvoke state, active MUTATED row kept) | Proven | Six subcases failed before and pass after. |
| Incomplete/malformed completion yields INSUFFICIENT unless independent adverse evidence | Proven (fixture) | New test asserts INSUFFICIENT and empty violations; existing adverse-precedence tests pass. |
| Preserve positive control, late restoration, active-MUTATED rejection, bound identities, adverse precedence | Proven (fixture) | Existing Judge tests all pass. |
| Run affected tests and strict typing, preserve adverse attempts, record counts and skips | Proven | See validation; 0 skips. |
| Separate RPI loop and independent exact-head review, tier justified | Unproven | Own review done; independent exact-head review and full tier outstanding. |

Live Azure: none used. The defect is in an offline judge; `ca-cutover-test-demo-api`, `ca-resident-demo` and `evhns-cutover-test-demo` do not run it. No throwaway resource exists. Screenshots: not applicable.
