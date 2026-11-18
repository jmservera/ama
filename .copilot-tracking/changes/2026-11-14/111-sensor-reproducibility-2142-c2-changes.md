---
title: "RPI Changes: Pin Sensor MSSQL Retained Reproduction Test in Local Gate"
description: "Cycle-2 implementation evidence record for Issue #111 / PR #1741 in tools/"
ms.date: 2026-11-14
---

## Metadata

* Task ID: 111-sensor-reproducibility-2142-c2
* Related plan: .copilot-tracking/plans/2026-11-14/111-sensor-reproducibility-2142-c2-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-c2-phase-details.md
* Implementation date: 2026-11-14

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`
* All remaining active-plan markers: none
* Status basis: Both tasks in `P01` completed with all `src-namespace` unit, lint, format, strict type, and skip-discovery checks passing.

## Execution Summary

Pinned `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` in `SENSOR_MSSQL_REQUIRED_TESTS` (`tools/rpi-checks.py`) so all 11 `MssqlRetainedAnalysisTests` methods match the AST-discovered SQL sensor suite, added an explicit `assertIn` membership check in `GateTests.test_pinned_sensor_mssql_tests_match_the_real_suite` (`tools/test_rpi_checks.py`), and verified all `src-namespace` `tools/` gate orchestration, CI selection, `ruff`, `mypy --strict`, and `project-core` skip-discovery checks.

## Completed Work

### Pin Retained Reproduction MSSQL Test in Local Gate and Gate Contract Suite

* Related phase or task: `P01-T01`
* Files: `tools/rpi-checks.py`, `tools/test_rpi_checks.py`
* What changed and why: Added `"test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only"` in alphabetical order to `SENSOR_MSSQL_REQUIRED_TESTS` in `tools/rpi-checks.py` (automatically propagating to `SENSOR_MSSQL_DISCOVERY_SKIPS`, `required_sql_tests`, and `required_sql_count = 11` for `project-core-mssql`), and added an explicit `self.assertIn(...)` check for its expanded `unittest -v` test ID in `GateTests.test_pinned_sensor_mssql_tests_match_the_real_suite` in `tools/test_rpi_checks.py`. Resolves the `src-namespace` failure caused when Cycle 1 (`79b9cd1be`) added the method to `RetainedAnalysisTests` (`MssqlRetainedAnalysisTests`'s base class).
* Completion evidence: `len(gate.SENSOR_MSSQL_REQUIRED_TESTS) == 11` and `GateTests.test_pinned_sensor_mssql_tests_match_the_real_suite` reports `ok`.
* Validation: Passed (`python3 -m unittest discover -s tools -p test_rpi_checks.py -v`).

### Validate `src-namespace` Gate Orchestration, Affected Selection, Linting, Typing, and Skip Discovery

* Related phase or task: `P01-T02`
* Files: `tools/rpi-checks.py`, `tools/test_rpi_checks.py`, `tools/ci-affected.py`, `tools/test_ci_affected.py`
* What changed and why: Executed the exact `src-namespace` CI commands defined in `.github/workflows/src-ci.yml` from the worktree root plus a live `gate.check_skips(..., group="project-core")` smoke check against `src/core/tests/test_sensor_analysis_mssql.py` without `ZF_SENSOR_MSSQL=1`.
* Completion evidence: 103/103 tests passed in `tools/test_rpi_checks.py`, 19/19 tests passed in `tools/test_ci_affected.py`, `ruff check` and `ruff format --check` exited 0 across all 4 `tools/` files, `mypy --strict` exited 0 across `tools/rpi-checks.py` and `tools/test_rpi_checks.py`, and `gate.check_skips` accepted all 11 skipped `MssqlRetainedAnalysisTests` methods.
* Validation: Passed across all 6 checks.

## Implementation-Time Plan and Detail Updates

None.

## Validation Record

| Check | Scope | Status | Evidence or reason |
| --- | --- | --- | --- |
| `python3 -m unittest discover -s tools -p test_rpi_checks.py -v` | `tools/rpi-checks.py`, `tools/test_rpi_checks.py` | Passed | `Ran 103 tests in 21.822s — OK` (`test_pinned_sensor_mssql_tests_match_the_real_suite ... ok`) |
| `python3 -m unittest discover -s tools -p test_ci_affected.py -v` | `tools/ci-affected.py`, `tools/test_ci_affected.py` | Passed | `Ran 19 tests in 0.093s — OK` |
| `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` | `tools/{rpi-checks,test_rpi_checks,ci-affected,test_ci_affected}.py` | Passed | `All checks passed!` |
| `ruff format --isolated --line-length 100 --check` | `tools/{rpi-checks,test_rpi_checks,ci-affected,test_ci_affected}.py` | Passed | `4 files already formatted` |
| `mypy --strict` | `tools/rpi-checks.py`, `tools/test_rpi_checks.py` | Passed | `Success: no issues found in 2 source files` |
| Live `gate.check_skips(..., group="project-core")` on `test_sensor_analysis_mssql.py` | `src/core/tests/test_sensor_analysis_mssql.py` + `tools/rpi-checks.py` | Passed | `SENSOR_MSSQL_REQUIRED_TESTS count: 11`; `OK (skipped=11)` |
| Full local external SQL gate (`tools/rpi-checks.py --all` with `ZF_SENSOR_MSSQL=1`) | Full repository + SQL Server container | Skipped | Tracked as pre-merge Full-tier validation item once the Cycle-2 branch head is reviewed and ready for publication (instructions forbid pushing in this turn). |

## Pre-Review Reconciliation

* Plan markers and phase details: current (`P01`, `P01-T01`, `P01-T02` checked; phase `P01` marked `complete`)
* Completed-work evidence and handoff prose: current
* Validation, blockers, remaining work, and follow-up items: current
* Review readiness: ready for Review (`rpi-review`)

## Blockers

* None

## Remaining Work

* None within declared Cycle-2 plan scope (`P01`).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-14/111-sensor-reproducibility-2142-c2-plan.md, `## Follow-Up Items`
* Run the complete external SQL gate (`python3 tools/rpi-checks.py --all --base <reviewed-main-sha> --out <external-dir>` with `ZF_SENSOR_MSSQL=1` and `--verify-receipt`) and hosted CI on the updated branch head before final PR merge, per the Full SQL tier classification in `src/README.md`.
* Complete analytics research phases R1 to R3 in `docs/reference/research/iot-sensor-analytics-research-plan.md` before replacing `EXERCISE VALUE` thresholds or approving an operational rule (`Refs #111`).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan (`P01`); completed `P01`, `P01-T01`, `P01-T02`; remaining `none`
* Validation coverage: 103 `test_rpi_checks.py` tests, 19 `test_ci_affected.py` tests, isolated `ruff check` + `ruff format --check`, `mypy --strict`, and 11-skip `project-core` discovery check all passed
* Blockers: none
* Current plan and detail updates: `P01`, `P01-T01`, `P01-T02` marked complete
* Planning and critique state: ready (`Pass` critique)
* Follow-up items: Full SQL external gate + hosted CI before merge; R1-R3 analytics research
* Review readiness or no-handoff reason: ready for review
* Continuation owner: parent (confirmed automatic RPI Agent)
