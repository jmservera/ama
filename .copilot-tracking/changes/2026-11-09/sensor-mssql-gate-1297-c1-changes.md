---
title: Changes - #1297 correction C1
date: 2026-11-09
---

## P01 Selection rule and tests (complete)

* tools/rpi-checks.py: `changed_groups` selects `mssql` when `project == "core"` and the lowercase path contains `sensor`; the `mssql` entry of `SKIP_REASONS` now reads "no store, schema, SQL, core sensor or SQL dependency path changed" (PC-001). check_skips, matrix and receipt contract are unchanged.
* tools/test_rpi_checks.py: two tests added, none removed or edited.
  * test_changed_core_sensor_paths_select_mssql_and_the_flagged_command: five paths (analysis, consumer, synthetic fault, shared fixture, mssql test) select mssql; `required_checks` for those executed groups contains exactly one sensor command with flag "1" and `required_sql_count` 8. This proves the contract, not execution.
  * test_unrelated_paths_do_not_select_mssql_through_the_sensor_rule: core non-sensor, api sensor and agents sensor paths do not select mssql; skip reason text asserted.
* Per critique PC-003: static import closure checked; residual accepted in the plan disposition.

## Validation (resource-light; no SQL, Docker, browser or gate)

* `cd tools && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest test_rpi_checks`: exit 0, Ran 99 tests OK (97 before plus 2).
* `ruff check --isolated --no-cache --select E,F,I,B,UP --target-version py312 --line-length 100 tools/rpi-checks.py tools/test_rpi_checks.py`: exit 0.
* `python3 -m mypy --strict --cache-dir=/tmp/mypy-1297-c1 tools/rpi-checks.py tools/test_rpi_checks.py`: exit 0, no issues.
* Pre-fix reproduction (single-path changed_groups calls) recorded in research C3.

## Adverse observations

* My reproduction script, run before PYTHONDONTWRITEBYTECODE was set, created ignored `tools/__pycache__/` in the worktree. Caches must not be deleted, so it was left; it is ignored and uncommitted.
* The tools tests print fixture "VERIFIED ... gate" lines and a preflight KeyboardInterrupt trace from a test; final result is OK.
* The critique subagent did not read the test file or matrix; those facts were supplied in the disposition.
* Research, plan and details artifacts were written with bash heredocs and a python text replace, not the create/edit tools.
