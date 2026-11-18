---
title: "RPI Plan Critique: Pin Sensor MSSQL Retained Reproduction Test in Local Gate"
description: "Single-pass final-candidate plan critique for Task ID 111-sensor-reproducibility-2142-c2 on PR #1741 (Refs #111)"
ms.date: 2026-11-14
---

<!-- markdownlint-disable-file -->

## Metadata

* Task ID: 111-sensor-reproducibility-2142-c2
* Critique date: 2026-11-14
* Plan: .copilot-tracking/plans/2026-11-14/111-sensor-reproducibility-2142-c2-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-c2-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Execute a Cycle-2 RPI fix for Issue #111 / PR #1741 on branch `feat/iot-111-sensor-reproducibility-2142` (targeting `feat/demo-164-chat-grounding-provenance-0900`) in `/home/azureuser/source/ama-demo-wt/feat-111-sensor-reproducibility-2142` to resolve the hosted `src-namespace` failure in `GateTests.test_pinned_sensor_mssql_tests_match_the_real_suite` (`tools/test_rpi_checks.py:474`) caused by missing `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only (test_sensor_analysis_mssql.MssqlRetainedAnalysisTests.test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only)`; update `tools/rpi-checks.py` and `tools/test_rpi_checks.py`; record Cycle-2 RPI artifacts in `.copilot-tracking/` while preserving Cycle-1 artifacts; validate with `python3 -m unittest discover -s tools -p test_rpi_checks.py -v`, `python3 -m unittest discover -s tools -p test_ci_affected.py -v`, `ruff`, and `mypy`; and commit cleanly without pushing.
* Research and evidence considered: .copilot-tracking/research/2026-11-14/111-sensor-reproducibility-2142-c2-research.md, .copilot-tracking/plans/2026-11-14/111-sensor-reproducibility-2142-c2-plan.md, .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-c2-phase-details.md, tools/rpi-checks.py, tools/test_rpi_checks.py, tools/ci-affected.py, tools/test_ci_affected.py, src/core/tests/test_sensor_analysis_store.py, src/core/tests/test_sensor_analysis_mssql.py, .github/workflows/src-ci.yml, src/README.md.
* Decisions, dependencies, and acceptance criteria considered: FR-1, FR-2, NFR-1, AC-1 through AC-5, Cycle-1 commit `79b9cd1be` (`RetainedAnalysisTests.test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only`), `MssqlRetainedAnalysisTests` SQL Server inheritance and cleanup compatibility, Full SQL tier validation classification under `src/README.md`, privacy-safe Git identity and `Refs #111` commit conventions, and the caller no-push constraint.
* Assessment boundary: Evaluates plan and phase-details completeness, AST set-parity accuracy, downstream local-gate skip/count/dependency effects, SQL Server compatibility of the inherited test, CI command parity against `.github/workflows/src-ci.yml`, and governance compliance from supplied repository files. Live disposable SQL Server execution (`ZF_SENSOR_MSSQL=1`), full external receipt generation (`tools/rpi-checks.py --all`), and post-push hosted CI observation remain outside this local no-push cycle.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| FR-1 (`SENSOR_MSSQL_REQUIRED_TESTS` parity in `tools/rpi-checks.py`) | Covered | Inserting `"test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only"` after `"test_reopened_store_reproduces_signal_without_writes"` in `tools/rpi-checks.py:187-200` brings the tuple to 11 alphabetically ordered tests, matching `RetainedAnalysisTests` (10 `test_*` methods in `src/core/tests/test_sensor_analysis_store.py:39-122`) union `MssqlRetainedAnalysisTests` (1 `test_*` method in `src/core/tests/test_sensor_analysis_mssql.py:39`) and automatically updating `SENSOR_MSSQL_DISCOVERY_SKIPS`, `required_sql_tests`, and `required_sql_count` (`tools/rpi-checks.py:202-204`, `1597-1606`). |
| FR-2 / AC-1 (`GateTests.test_pinned_sensor_mssql_tests_match_the_real_suite` in `tools/test_rpi_checks.py`) | Covered | `P01-T01` preserves exact AST set equality in `tools/test_rpi_checks.py:461-487` and adds an explicit `self.assertIn(...)` membership lock for the new test ID with zero test removals and zero net new test methods (`103` total `test_*` methods in `tools/test_rpi_checks.py`), keeping downstream `names[4]` indexing (`tools/test_rpi_checks.py:707`, `765`) intact. |
| Q2 / `C6` / AC-2 (`tools/ci-affected.py` and `tools/test_ci_affected.py` regression check) | Covered | `tools/ci-affected.py:44-50` already maps `tools/rpi-checks.py` and `tools/test_rpi_checks.py` to `NAMESPACE_ONLY`, and `SENSOR_MSSQL_DIRECT_DEPENDENCIES` (`tools/rpi-checks.py:207-214`) requires no update because `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` only imports `test_sensor_consumer_live`. Minor non-blocking note: `tools/test_ci_affected.py` defines 19 `test_*` methods across 4 classes rather than the 16 noted in `P01-T02` / `P01` prose; `AC-2` and `NFR-1` accurately govern all tests passing with exit code `0`. |
| Q3 / `C3` / `C4` (Inherited MSSQL compatibility on SQL Server) | Covered | Every SQL statement in `src/core/tests/test_sensor_analysis_store.py:122-167` (`snapshot()`, `observed_series`, `configure`, `DELETE FROM sensor_reading`, `DELETE FROM sensor_delivery`, and `DROP TABLE sensor_consumer_control`) matches sibling methods in `RetainedAnalysisTests` (`lines 80-81`, `110-112`) and is restored by `MssqlRetainedAnalysisTests.setUp` cleanup (`src/core/tests/test_sensor_analysis_mssql.py:35`). |
| NFR-1 / AC-3 (`src-namespace` `ruff` and `mypy --strict` parity) | Covered | `P01` and `P01-T02` match `.github/workflows/src-ci.yml:258-267` (`--isolated --select E,F,I,B,UP --target-version py312 --line-length 100` for `ruff check` and `--isolated --line-length 100 --check` for `ruff format`, plus `mypy --strict tools/rpi-checks.py tools/test_rpi_checks.py`), and the added string literals fit well within 100 columns. |
| AC-4 / AC-5 / `C7` (Tracking records, Full SQL tier disclosure, clean no-push commit) | Covered | Preserves Cycle-1 artifacts (`111-sensor-reproducibility-2142-*`), records Full SQL tier impact classification accurately per `src/README.md:102-116` and `182-192` without modifying `src/README.md` (which references `SENSOR_MSSQL_REQUIRED_TESTS` symbolically), and specifies privacy-safe Git author config, `Refs #111`, Copilot trailer, and no remote push. |
| P01 / P01-T01 / P01-T02 | Covered | Cohesive single-phase task breakdown with locked test ownership, clear file boundaries, and complete local verification commands. |

## Verdict

* Verdict: Pass
* Rationale: The candidate plan and phase details are accurate, minimal, and fully grounded in primary codebase evidence (`C1` through `C7`). Adding `"test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only"` to `SENSOR_MSSQL_REQUIRED_TESTS` in `tools/rpi-checks.py` and asserting its membership in `GateTests.test_pinned_sensor_mssql_tests_match_the_real_suite` in `tools/test_rpi_checks.py` reconciles the AST suite check (`10 + 1 = 11` tests), `project-core` discovery-skip verification (`SENSOR_MSSQL_DISCOVERY_SKIPS`), and `mssql` execution count/name verification (`required_sql_tests` and `required_sql_count`) while keeping `MssqlRetainedAnalysisTests` SQL-compatible and satisfying `.github/workflows/src-ci.yml` strict checks. No substantive defects or missing decisions exist.

## Findings

No actionable `PC-xxx` findings. The plan and phase details are ready for implementation without revision.

## Strengths and Residual Risk

* Single-tuple reconciliation in `tools/rpi-checks.py` fixes both the observed `src-namespace` CI failure (`tools/test_rpi_checks.py:474`) and the latent local-gate `GateError` in `project-core` skip checking and `mssql` count/name checking without loosening any gate invariant.
* Research Wave 3 (`C3`, `C4`) verified line by line that `RetainedAnalysisTests.test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` uses only SQL statements already proven on SQL Server and cleaned up by `MssqlRetainedAnalysisTests.setUp`, justifying pinning rather than excluding the test.
* Implementation execution notes (non-blocking): `tools/test_ci_affected.py` contains 19 test methods (4 test classes including `WorkflowTests`), so `P01-T02` will report `Ran 19 tests` rather than `16`; and if `P01-T02` runs live `src/core` sensor test discovery to sanity-check `gate.check_skips(..., group="project-core")`, pass `PYTHONPATH=src/core/src:src/core/tests` so worktree `zava_forward.core` precedes any shared `~/.local` editable install.
* Explicitly accepted residual risk outside this no-push cycle: Full SQL external gate verification (`python3 tools/rpi-checks.py --all --base <reviewed-main-sha> --out <external-dir>` with `ZF_SENSOR_MSSQL=1` and `--verify-receipt`), post-push hosted CI observation on the new head, and Issue #111 R1-R3 threshold research remain tracked pre-merge/open follow-ups (`Refs #111`).

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Critique verified all supplied planning artifacts, Python modules, test suites, workflow definitions, and gate documentation statically without modifying source files, running live SQL Server containers, or observing post-push GitHub Actions runs.

## Recommended Next Action

* Highest-impact finding: none
* Action owner: none (planning parent `rpi-plan` finalizes directly for `rpi-implement`)
* Smallest next action: Finalize `.copilot-tracking/plans/2026-11-14/111-sensor-reproducibility-2142-c2-plan.md` from `candidate` to `ready` with `Pass` critique disposition and proceed to `rpi-implement` (`P01-T01`, `P01-T02`).
* User response required: no
