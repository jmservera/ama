---
title: "RPI Phase Details: Pin Sensor MSSQL Retained Reproduction Test in Local Gate"
description: "Phase and task implementation details for Cycle-2 CI fix on PR #1741 (Refs #111)"
ms.date: 2026-11-14
---

## Metadata

* Task ID: 111-sensor-reproducibility-2142-c2
* Task slug: 111-sensor-reproducibility-2142-c2
* Related plan: .copilot-tracking/plans/2026-11-14/111-sensor-reproducibility-2142-c2-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-14/111-sensor-reproducibility-2142-c2-research.md, .github/workflows/src-ci.yml, src/README.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
| --- | --- | --- | --- |
| P01 | Update Pinned Sensor MSSQL Gate Contract and Verify `tools/` Suite | complete | P01, P01-T01, P01-T02 |

<!-- rpi:phase id=P01 -->
## P01: Update Pinned Sensor MSSQL Gate Contract and Verify `tools/` Suite

### Context

In Cycle 1 (`79b9cd1be`), `RetainedAnalysisTests.test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` was added to `src/core/tests/test_sensor_analysis_store.py` (`C3`). Because `MssqlRetainedAnalysisTests` in `src/core/tests/test_sensor_analysis_mssql.py` inherits from `RetainedAnalysisTests` (`C4`), the live SQL sensor suite grew from 10 to 11 tests, while `SENSOR_MSSQL_REQUIRED_TESTS` in `tools/rpi-checks.py` remained at 10 entries (`C1`), causing `GateTests.test_pinned_sensor_mssql_tests_match_the_real_suite` in `tools/test_rpi_checks.py` to fail in `src-namespace` CI (`C2`).

Test ownership locked prior to critique:
* Canonical test targets: `tools/test_rpi_checks.py` (`GateTests.test_pinned_sensor_mssql_tests_match_the_real_suite`), `tools/test_ci_affected.py`.
* Generated targets: `none`.
* Exact removals: `none`.
* Maximum additions: `0` net new test methods (1 explicit `assertIn` assertion added in `test_pinned_sensor_mssql_tests_match_the_real_suite` covering both semantic membership and exact-set regression).

### Intent

Synchronize `SENSOR_MSSQL_REQUIRED_TESTS` with the 11-method `MssqlRetainedAnalysisTests` suite, strengthen the explicit pin assertion in `tools/test_rpi_checks.py`, and verify all `src-namespace` `tools/` unit, lint, format, and strict type checks.

### Boundaries

* Included: `tools/rpi-checks.py`, `tools/test_rpi_checks.py`, and read-only validation of `tools/ci-affected.py`, `tools/test_ci_affected.py`, and `check_skips` compatibility.
* Excluded: Modifying `src/core` files, `.github/workflows/*`, or pushing to `origin`.

### Likely Targets

* `tools/rpi-checks.py`: Add `"test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only"` to `SENSOR_MSSQL_REQUIRED_TESTS`.
* `tools/test_rpi_checks.py`: Add explicit `self.assertIn(...)` for `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` in `test_pinned_sensor_mssql_tests_match_the_real_suite`.

### Dependencies

* None.

### Validation Expectations

* `python3 -m unittest discover -s tools -p test_rpi_checks.py -v` (103/103 pass)
* `python3 -m unittest discover -s tools -p test_ci_affected.py -v` (19/19 pass)
* `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 tools/rpi-checks.py tools/test_rpi_checks.py tools/ci-affected.py tools/test_ci_affected.py`
* `ruff format --isolated --line-length 100 --check tools/rpi-checks.py tools/test_rpi_checks.py tools/ci-affected.py tools/test_ci_affected.py`
* `mypy --strict tools/rpi-checks.py tools/test_rpi_checks.py`

### Completion Evidence

* Clean diff in `tools/rpi-checks.py` and `tools/test_rpi_checks.py` plus zero-error validation outputs recorded in `.copilot-tracking/changes/2026-11-14/111-sensor-reproducibility-2142-c2-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` to `SENSOR_MSSQL_REQUIRED_TESTS` and `test_rpi_checks.py`

#### Context

`SENSOR_MSSQL_REQUIRED_TESTS` in `tools/rpi-checks.py` lists `MssqlRetainedAnalysisTests` method names alphabetically via `_sql_tests(SENSOR_MSSQL_SELECTOR, "MssqlRetainedAnalysisTests", ...)` (`C1`). `SENSOR_MSSQL_DISCOVERY_SKIPS`, `required_sql_tests`, and `required_sql_count` compute directly from `SENSOR_MSSQL_REQUIRED_TESTS`.

#### Intent

Insert `"test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only"` immediately after `"test_reopened_store_reproduces_signal_without_writes"` in `tools/rpi-checks.py` and add an explicit `self.assertIn(...)` check in `GateTests.test_pinned_sensor_mssql_tests_match_the_real_suite` in `tools/test_rpi_checks.py`.

#### Boundaries

* Included: `SENSOR_MSSQL_REQUIRED_TESTS` tuple in `tools/rpi-checks.py` and `test_pinned_sensor_mssql_tests_match_the_real_suite` in `tools/test_rpi_checks.py`.
* Excluded: Changing skip logic, SQL selectors, or `SENSOR_MSSQL_DIRECT_DEPENDENCIES`.

#### Likely Targets

* `tools/rpi-checks.py`
* `tools/test_rpi_checks.py`

#### Dependencies

* None.

#### Validation Expectations

* `test_pinned_sensor_mssql_tests_match_the_real_suite`, `test_sensor_mssql_discovery_skip_is_exact_and_fail_closed`, `test_sensor_mssql_execution_evidence_rejects_missing_substituted_skipped_or_failed`, and `test_sensor_mssql_receipt_rejects_tampered_or_incomplete_evidence` all pass with 11 required tests.

#### Completion Evidence

* Updated `tools/rpi-checks.py` and `tools/test_rpi_checks.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Execute `test_rpi_checks.py`, `test_ci_affected.py`, `ruff`, and `mypy --strict` validation

#### Context

`.github/workflows/src-ci.yml` (`src-namespace`, "Local gate orchestration contracts and strict checks") runs `unittest discover` on `test_rpi_checks.py` and `test_ci_affected.py`, isolated `ruff check` and `ruff format --check` with `--select E,F,I,B,UP --target-version py312 --line-length 100`, and `mypy --strict tools/rpi-checks.py tools/test_rpi_checks.py` (`C5`).

#### Intent

Run every `src-namespace` check covering the modified files plus a sanity check (using `PYTHONPATH=src/core/src:src/core/tests`) that `gate.check_skips(..., group="project-core")` accepts live `src/core` sensor discovery skip output without raising `GateError`.

#### Boundaries

* Included: Local command execution from `/home/azureuser/source/ama-demo-wt/feat-111-sensor-reproducibility-2142`.
* Excluded: Networked or Docker-dependent full-gate runs or remote Git operations.

#### Likely Targets

* Read-only verification against `tools/rpi-checks.py`, `tools/test_rpi_checks.py`, `tools/ci-affected.py`, and `tools/test_ci_affected.py`.

#### Dependencies

* P01-T01.

#### Validation Expectations

* All commands return exit code `0` with zero lint, format, type, or test errors.

#### Completion Evidence

* Exact command outputs recorded in the Cycle-2 changes artifact.

#### Unresolved Items

* None.
