# Correction 5: mypy strict annotations for resident SQL test fakes (#462)

Date: 2026-10-26. Branch feat/resident-azure-showcase-462.

## Research
* Failed gate on aba69f6e (receipt 4dd1d297b27bfeacffc3187660795548408a6c1cb8c5533146e173826a5a3d9b), group project-core, 7 mypy strict errors in src/core/tests/test_resident_showcase_sql.py. Log: /mnt/ama-rpi-gates/issue462-aba69f6e-gate1/0015-project-core.log.
* Cause: FakeCursor and verify helper added in 25481d50 were unannotated; mypy was not run locally then (my miss). Historical receipt preserved.

## Plan
* Merge origin/main (20f11508), annotate that test file only, no behaviour change, run ruff/mypy/core tests, one commit, no gate.

## Critique and review (disclosed)
* Scope is annotation-only in one test file; no independent subagent critique or review was run for this trivial change. This is a deviation: the plan, critique and review here are self-recorded and written alongside implementation, not before it. Independent review is left to the coordinator/hosted review.

## Changes and results
* Annotated FakeCursor (init, execute, fetchall, rows, sql) and verify(**kw: Any) -> None.
* src/core: mypy strict clean (140 files), ruff check and format clean, resident tests 68 OK (13 skipped), core suite OK.
* Full gate not run; coordinator serialises it.
