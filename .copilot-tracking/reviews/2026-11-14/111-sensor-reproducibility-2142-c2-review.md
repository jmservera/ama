---
title: "Review: Pin Sensor MSSQL Retained Reproduction Test in Local Gate"
description: "Post-implementation Cycle-2 RPI review for Task ID 111-sensor-reproducibility-2142-c2 in tools/ (PR #1741, Refs #111)"
ms.date: 2026-11-14
---

## Scope and Evidence

* Task ID: 111-sensor-reproducibility-2142-c2
* Review date: 2026-11-14
* Review scope: full task (`P01`, `P01-T01`, `P01-T02`)
* Assessed boundary: Pinned `SENSOR_MSSQL_REQUIRED_TESTS` contract in `tools/rpi-checks.py`, AST and explicit membership test assertions in `tools/test_rpi_checks.py`, `src-namespace` unit/lint/format/strict-type validation (`test_rpi_checks.py`, `test_ci_affected.py`, `ruff`, `mypy --strict`), and `project-core` MSSQL skip-discovery compatibility on branch `feat/iot-111-sensor-reproducibility-2142` without pushing.
* Plan: .copilot-tracking/plans/2026-11-14/111-sensor-reproducibility-2142-c2-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-c2-phase-details.md
* Plan critique: .copilot-tracking/critiques/2026-11-14/111-sensor-reproducibility-2142-c2-critique.md
* Changes: .copilot-tracking/changes/2026-11-14/111-sensor-reproducibility-2142-c2-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-14/111-sensor-reproducibility-2142-c2-research.md, `git diff tools/`, `src/core/tests/test_sensor_analysis_store.py`, `src/core/tests/test_sensor_analysis_mssql.py`, and `.github/workflows/src-ci.yml`.

## Opening Review State

* Interpreted review goal: Verify that `SENSOR_MSSQL_REQUIRED_TESTS` in `tools/rpi-checks.py` and `GateTests.test_pinned_sensor_mssql_tests_match_the_real_suite` in `tools/test_rpi_checks.py` match the 11-method `MssqlRetainedAnalysisTests` suite introduced in Cycle 1 (`79b9cd1be`), preserve fail-closed gate semantics (`SENSOR_MSSQL_DISCOVERY_SKIPS`, `required_sql_tests`, `required_sql_count = 11`), and pass every `src-namespace` `tools/` check cleanly without pushing.
* Review scope: full task (`P01`)
* Evidence readiness: Ready; research, plan, phase details, single-pass critique (`Pass`), changes record, and clean validation outputs are complete and reconciled.
* Acceptance basis: FR-1 through FR-3, NFR-1, NFR-2, AC-1 through AC-4, `.github/workflows/src-ci.yml` `src-namespace` step commands, and `src/README.md` local RPI gate rules.
* First comparison boundary: Local `tools/` gate contract, `ci-affected` selection, `ruff`, `mypy --strict`, and 11-test `project-core` skip discovery; live SQL Server (`ZF_SENSOR_MSSQL=1`), full external receipt (`tools/rpi-checks.py --all`), and hosted CI on the updated head remain outside this no-push slice.
* Active read-only boundaries: Review creates only this canonical review record without modifying source code, plan, details, critique, research, or changes artifacts.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed 2026-11-14 across reconciled Cycle-2 RPI artifacts, `git diff tools/` inspection of `tools/rpi-checks.py` and `tools/test_rpi_checks.py`, and verified outputs from `test_rpi_checks.py` (103/103 passed), `test_ci_affected.py` (19/19 passed), isolated `ruff check` + `ruff format --check`, `mypy --strict`, and live `gate.check_skips` discovery (11/11 skips matched).

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| `P01` / `P01-T01` | Pin Retained Reproduction MSSQL Test in Local Gate and Gate Contract Suite | Reconciled | Checked in plan, marked `complete` in phase details, and verified in `tools/rpi-checks.py` and `tools/test_rpi_checks.py`. |
| `P01` / `P01-T02` | Validate `src-namespace` Gate Orchestration, Affected Selection, Linting, Typing, and Skip Discovery | Reconciled | Checked in plan, marked `complete` in phase details, and evidenced across all 6 validation checks. |
| `Follow-Up Items` | Full SQL external gate (`rpi-checks.py --all` + `ZF_SENSOR_MSSQL=1` + `--verify-receipt` + hosted CI) and R1-R3 analytics research | Reconciled | Preserved distinctly in plan and changes `## Follow-Up Items` outside active `P01` claims. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| `P01-T01` | `tools/rpi-checks.py`, `tools/test_rpi_checks.py` | Added `"test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only"` in alphabetical order to `SENSOR_MSSQL_REQUIRED_TESTS` (raising derived `SENSOR_MSSQL_DISCOVERY_SKIPS` and `required_sql_count` from 10 to 11) and added an explicit `self.assertIn(...)` assertion in `GateTests.test_pinned_sensor_mssql_tests_match_the_real_suite`. | `git diff tools/` | Passed (`test_rpi_checks.py`: 103/103 OK; `ruff`; `mypy --strict`) | Reconciled |
| `P01-T02` | `tools/rpi-checks.py`, `tools/test_rpi_checks.py`, `tools/ci-affected.py`, `tools/test_ci_affected.py` | Executed all `src-namespace` commands from `.github/workflows/src-ci.yml` plus live `project-core` MSSQL skip-discovery check from the worktree root. | Changes record validation table | Passed (`test_rpi_checks.py` 103 OK, `test_ci_affected.py` 19 OK, `ruff check` + `ruff format --check` OK, `mypy --strict` OK, `check_skips` 11/11 OK) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| None during implementation | Implementation followed the `Pass`-critiqued plan directly with zero scope or design divergence. | None | Checklist markers, phase index status, and changes record synchronized. | Ready (`Pass` critique, 0 `PC-xxx` findings) | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: `.copilot-tracking/critiques/2026-11-14/111-sensor-reproducibility-2142-c2-critique.md` returned `Verdict: Pass` with 0 `PC-xxx` findings; non-blocking accuracy refinements (`19` tests in `test_ci_affected.py` and `PYTHONPATH=src/core/src:src/core/tests` for live `check_skips` verification) were reflected in the plan/details prior to implementation and confirmed by execution.
* Material revisions: None required during implementation.
* Dependent-work pause assessment: No premature resumption occurred; `P01-T01` completed prior to `P01-T02` verification.
* Justification assessment: Supported by `git diff tools/` and clean command execution.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Full SQL external gate (`tools/rpi-checks.py --all` with `ZF_SENSOR_MSSQL=1` and `--verify-receipt`) plus hosted CI on the updated PR #1741 head | Caller explicitly instructed `Do NOT push`; `src/README.md` classifies `sensor_analysis.py` and gate-contract changes under the Full SQL tier prior to PR merge. | Branch owner before pushing and merging PR #1741 | Open distinct follow-up route (`follow-up`) |
| Analytics research phases R1 to R3 (`docs/reference/research/iot-sensor-analytics-research-plan.md`) | Issue #111 criterion 3 and PRD AC-068 require primary-standards research and named domain sign-off before replacing `EXERCISE VALUE` labels or approving an operational rule. | Research and domain reviewer (`rpi-research`) | Open distinct follow-up route (`follow-up`) |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `P01` implementation, completion, or acceptance scope.

## Findings

No implementation defects, decision gaps, or evidence gaps were found within the assessed Cycle-2 `tools/` boundary. One low-severity residual follow-up record carries forward the pre-merge Full SQL gate and hosted CI boundary on the updated head:

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Execute external Full SQL gate (`tools/rpi-checks.py --all` with `ZF_SENSOR_MSSQL=1`, now enforcing all 11 pinned sensor SQL tests) and hosted CI before merging PR #1741

* Related scope: Plan `## Follow-Up Items` (publication/merge boundary outside caller's no-push instruction)
* Evidence: `src/README.md` (`Local RPI Gate` Full SQL tier classification) and `tools/rpi-checks.py` (`SENSOR_MSSQL_REQUIRED_TESTS` now pinning 11 `MssqlRetainedAnalysisTests` methods).
* Impact: Does not affect local `src-namespace` resolution or the caller's no-push acceptance criteria, and strengthens the Full SQL gate so the 11th retained-reproduction test is fail-closed when `ZF_SENSOR_MSSQL=1` runs prior to merge.
* Destination: follow-up
* Smallest useful next action: When ready to publish the Cycle-2 commit to PR #1741, run `python3 tools/rpi-checks.py --all --base <reviewed-main-sha> --out <new-external-dir>` with `ZF_SENSOR_MSSQL=1`, verify the external receipt with `--verify-receipt`, push, and observe green `src-namespace` and `src-mssql` hosted CI checks.

## Defects

* None.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| `RV-001` | `follow-up` | Run external Full SQL gate (`ZF_SENSOR_MSSQL=1` + `--verify-receipt`), push, and verify hosted CI on PR #1741 before merge | Publication/merge gate outside caller's explicit `Do NOT push` boundary |

Later implementation of a routed finding does not require another Review.

## Residual Work

* `RV-001`: Execute the external Full SQL gate (`tools/rpi-checks.py --all` with `ZF_SENSOR_MSSQL=1` and `--verify-receipt`), push to PR #1741, and confirm green hosted CI (`src-namespace`, `src-mssql`).
* Complete analytics research phases R1 to R3 in `docs/reference/research/iot-sensor-analytics-research-plan.md` before replacing `EXERCISE VALUE` thresholds or approving an operational sensor rule (`Refs #111`).

## Blockers and Remaining Work

* Blockers: none for Cycle-2 local fix and clean commit on `feat/iot-111-sensor-reproducibility-2142`.
* Remaining active work: none (`P01` complete).

## Validation Evidence

| Command | Scope | Status | Summary |
| --- | --- | --- | --- |
| `python3 -m unittest discover -s tools -p test_rpi_checks.py -v` | `tools/rpi-checks.py`, `tools/test_rpi_checks.py` | Passed | `Ran 103 tests in 21.822s — OK` (`test_pinned_sensor_mssql_tests_match_the_real_suite ... ok`) |
| `python3 -m unittest discover -s tools -p test_ci_affected.py -v` | `tools/ci-affected.py`, `tools/test_ci_affected.py` | Passed | `Ran 19 tests in 0.093s — OK` |
| `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` | `tools/{rpi-checks,test_rpi_checks,ci-affected,test_ci_affected}.py` | Passed | `All checks passed!` |
| `ruff format --isolated --line-length 100 --check` | `tools/{rpi-checks,test_rpi_checks,ci-affected,test_ci_affected}.py` | Passed | `4 files already formatted` |
| `mypy --strict` | `tools/rpi-checks.py`, `tools/test_rpi_checks.py` | Passed | `Success: no issues found in 2 source files` |
| Live `gate.check_skips(..., group="project-core")` on `test_sensor_analysis_mssql.py` | `src/core/tests/test_sensor_analysis_mssql.py` + `tools/rpi-checks.py` | Passed | `SENSOR_MSSQL_REQUIRED_TESTS count: 11`; `OK (skipped=11)` |
| `python3 tools/rpi-checks.py --all` + `ZF_SENSOR_MSSQL=1` + hosted CI | Full SQL publication gate | Skipped | Deferred per caller `Do NOT push` instruction (`RV-001`) |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every active requirement (`FR-1`..`FR-3`, `NFR-1`, `NFR-2`) and acceptance criterion (`AC-1`..`AC-4`) is satisfied with zero defects, zero gate-weakening shortcuts, zero `.copilot-tracking/` references in `tools/`, and passing results across all 103 `test_rpi_checks.py` tests, all 19 `test_ci_affected.py` tests, isolated `ruff check` + `ruff format --check`, `mypy --strict`, and 11-skip `project-core` discovery verification. Pre-merge Full SQL gate execution and R1-R3 research remain routed cleanly as distinct follow-up items (`Refs #111`).

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | none | none |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | distinct follow-up (`RV-001` + R1-R3 research) | Run `tools/rpi-checks.py --all` (`ZF_SENSOR_MSSQL=1` + `--verify-receipt`), push, and verify hosted CI before PR #1741 merge; complete R1-R3 before operational rule approval |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: `test_rpi_checks.py` (103/103 OK), `test_ci_affected.py` (19/19 OK), isolated `ruff check` + `ruff format --check` (4 files OK), `mypy --strict` (2 files OK), and live 11-skip `project-core` discovery check (OK)
* Blockers: none
