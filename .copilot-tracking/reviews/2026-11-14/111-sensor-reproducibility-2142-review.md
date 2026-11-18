---
title: "Review: Deterministic Versioned Sensor Analysis and Review Task"
description: "Post-implementation RPI review for Task ID 111-sensor-reproducibility-2142 in src/core (Refs #111)"
ms.date: 2026-11-14
---

## Scope and Evidence

* Task ID: 111-sensor-reproducibility-2142
* Review date: 2026-11-14
* Review scope: full task (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`)
* Assessed boundary: Locally verifiable reproducibility, version provenance, digest collision resistance, non-authority and privacy guarantees, downstream `sensor_review_draft` / `src/api` compatibility, documentation, and bare `mypy` / `ruff` / `unittest` verification in `src/core` on branch `feat/iot-111-sensor-reproducibility-2142` without pushing.
* Plan: .copilot-tracking/plans/2026-11-14/111-sensor-reproducibility-2142-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-phase-details.md
* Plan critique: .copilot-tracking/critiques/2026-11-14/111-sensor-reproducibility-2142-critique.md
* Changes: .copilot-tracking/changes/2026-11-14/111-sensor-reproducibility-2142-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-14/111-sensor-reproducibility-2142-research.md, `git diff` across `src/core/src/zava_forward/core/sensor_analysis.py`, `src/core/src/zava_forward/core/sensor_analysis_store.py`, `src/core/README.md`, `src/core/tests/test_sensor_analysis.py`, `src/core/tests/test_sensor_analysis_store.py`, `src/core/tests/test_sensor_analysis_reproducibility.py`, and downstream `src/api/tests/test_sensor_analysis_reproducibility.py` + `test_sensor_non_authority_boundary.py`.

## Opening Review State

* Interpreted review goal: Verify that `src/core` deterministically reproduces versioned sensor analysis signals and `SENSOR_REVIEW_DUE` human review task candidates with complete, privacy-preserving `VersionProvenance` from retained readings alone, resolves all plan-critique items (`PC-001`..`PC-004`), preserves downstream draft and API contracts, and passes bare `mypy`, `ruff check`, `ruff format --check`, and sensor unit tests.
* Review scope: full task (`P01` and `P02`)
* Evidence readiness: Ready; research, plan, phase details, critique, changes record, and clean verification outputs are complete and reconciled.
* Acceptance basis: FR-1 through FR-5, NFR-1, NFR-2, AC-1 through AC-6, ADR 0003 decision 6, PRD FR-050 / AC-067 / AC-068, and critique findings `PC-001`..`PC-004`.
* First comparison boundary: Local `src/core` pure and SQLite-retained reproducibility plus `src/api` test compatibility; live SQL Server (`ZF_SENSOR_MSSQL=1`), full external gate (`tools/rpi-checks.py --all`), hosted CI, and R1-R3 analytics research sign-off are explicitly outside this no-push slice.
* Active read-only boundaries: Review creates only this canonical review record without modifying source code, plan, details, critique, research, or changes artifacts.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed 2026-11-14 across reconciled RPI artifacts, line-by-line `git diff` inspection of all 6 changed `src/core` files, and executed bare `mypy`, `ruff`, `src/core` sensor unit tests (291 run, 0 failed), and `src/api` sensor tests (10 run, 0 failed).

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| `P01` / `P01-T01` | Pure `VersionProvenance`, Bound Digests, and Reproduction Helpers (`sensor_analysis.py`) | Reconciled | Checked in plan, marked `complete` in phase details, and evidenced in `sensor_analysis.py`. |
| `P01` / `P01-T02` | Read-Only Retained-Store Reproduction (`sensor_analysis_store.py`) | Reconciled | Checked in plan, marked `complete` in phase details, and evidenced in `sensor_analysis_store.py`. |
| `P02` / `P02-T01` | Focused Reproducibility, Collision, and Subprocess Tests (`src/core/tests/`) | Reconciled | Checked in plan, zero test removals/renames, 4 focused test methods added (within <= 7 lock), zero `# type: ignore`. |
| `P02` / `P02-T02` | Component Documentation and Bare Isolated Verification (`src/core/README.md`) | Reconciled | Checked in plan, `src/core/README.md` updated cleanly, bare `mypy`/`ruff`/`unittest` passed, `.venv-verify-111` removed. |
| `Follow-Up Items` | Full SQL external gate (`rpi-checks.py --all` + `ZF_SENSOR_MSSQL=1` + hosted CI) and R1-R3 analytics research | Reconciled | Preserved distinctly in plan and changes `## Follow-Up Items` outside active `P01`/`P02` claims. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| `P01-T01` | `src/core/src/zava_forward/core/sensor_analysis.py` | Added `VersionProvenance`, `TypedDict` payloads, `policy_digest`, `output_digest`, `version_provenance`, per-row bound `_row_digest_tuples` / `_schema_marker` inside `_digest`, hardened `_home_and_window`, `analysis_version` + `threshold_label` candidate checks, and aligned `reproduce_sensor_analysis` and `reproduce_review_task`. | `git diff` on `sensor_analysis.py` | Passed (`mypy` across 316 files, `ruff`, `test_sensor_analysis.py`, `test_sensor_review_draft.py`, `src/api` tests) | Reconciled |
| `P01-T02` | `src/core/src/zava_forward/core/sensor_analysis_store.py` | Added read-only fail-closed `reproduce_retained(consumer, home_id, window, as_of, policy=None)` returning canonical `ReproducedReviewTask`. | `git diff` on `sensor_analysis_store.py` | Passed (`mypy`, `ruff`, `test_sensor_analysis_store.py`, `test_sensor_analysis_reproducibility.py`) | Reconciled |
| `P02-T01` | `src/core/tests/test_sensor_analysis.py`, `src/core/tests/test_sensor_analysis_store.py`, `src/core/tests/test_sensor_analysis_reproducibility.py` | Expanded `VersionProvenance` assertions and added empty-window/home validation, duplicate-timestamp cross-row swap collision, SQLite read-only/fail-closed `reproduce_retained`, and `PYTHONHASHSEED` fresh-process reproduction tests. | `git diff` on `src/core/tests/test_sensor_analysis*.py` | Passed (`Ran 291 tests in 138.952s — OK (skipped=34)`) | Reconciled |
| `P02-T02` | `src/core/README.md` | Documented `VersionProvenance`, `version_provenance`, `reproduce_review_task`, `reproduce_sensor_analysis`, and window-bounded `reproduce_retained` while preserving non-authority and R1-R3 caveats. | `git diff` on `src/core/README.md` | Passed (Markdown/ASCII review, `ruff`, `mypy`, `unittest`) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| None during implementation | No implementation-time scope or requirement divergence occurred; implementation followed the post-critique plan directly. | None | Checklist markers, phase index statuses, handoff prose, and changes log synchronized. | Ready (`PC-001`..`PC-004` resolved prior to `Implement`) | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All four findings in `.copilot-tracking/critiques/2026-11-14/111-sensor-reproducibility-2142-critique.md` (`PC-001` per-row bound digest + `isinstance(v, str)` + cross-row swap test; `PC-002` canonical `candidate` resolution/validation, `threshold_label` check, `reproduce_sensor_analysis` parity, float normalization, and `TypedDict` strict typing; `PC-003` worktree-local `.venv-verify-111` cleanup without `/tmp` or `~/.local` mutation; `PC-004` `"sensor-fault-input-v1"` constant, window-bounded `observed_series` parity, and keeping `test_digest_changes_with_calibration_flag` unrenamed) are fully implemented and verified.
* Material revisions: None required during implementation.
* Dependent-work pause assessment: No premature resumption occurred; `P01` completed before `P02` verification and reconciliation.
* Justification assessment: Supported by primary code inspection and passing verification runs.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Full SQL external gate (`tools/rpi-checks.py --all` with `ZF_SENSOR_MSSQL=1` and verified external receipt) plus hosted CI | Caller explicitly instructed `Do NOT push`, whereas `src/README.md` requires the full external SQL gate and hosted CI immediately prior to PR publication/merge for `sensor_analysis.py`. | Branch owner before `git push` / PR publication | Open distinct follow-up route (`follow-up`) |
| Analytics research phases R1 to R3 (`docs/reference/research/iot-sensor-analytics-research-plan.md`) | Issue #111 criterion 3 and PRD AC-068 require primary-standards research and named domain sign-off before approving any non-exercise rule; current code intentionally keeps `EXERCISE VALUE: fictional, not sourced`. | Research and domain reviewer (`rpi-research`) | Open distinct follow-up route (`follow-up`) |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `P01` or `P02` implementation, completion, or acceptance scope.

## Findings

No implementation defects, decision gaps, or evidence gaps were found within the assessed `src/core` boundary. One low-severity residual follow-up record documents the pre-publication SQL gate boundary:

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Live SQL Server (`ZF_SENSOR_MSSQL=1`) and external `rpi-checks.py --all` receipt remain required prior to PR publication

* Related scope: Plan `## Follow-Up Items` (publication boundary outside local no-push `P01`/`P02`)
* Evidence: `src/README.md` (`sensor_analysis.py` SQL tier classification) and `.copilot-tracking/changes/2026-11-14/111-sensor-reproducibility-2142-changes.md` (`OK (skipped=34)` live-MSSQL tests skipped locally without `ZF_SENSOR_MSSQL=1`).
* Impact: Does not affect local SQLite/pure determinism or the caller's no-push acceptance criteria, but blocks PR publication/merge until a live SQL Server run and verified external receipt complete on the exact head.
* Destination: follow-up
* Smallest useful next action: Before pushing `feat/iot-111-sensor-reproducibility-2142` or opening a PR, start the local SQL Server prerequisite (`ZF_SENSOR_MSSQL=1`) and run `python3 tools/rpi-checks.py --all --base <reviewed-main-sha> --out <external-dir>` followed by `--verify-receipt`.

## Defects

* None.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| `RV-001` | `follow-up` | Run `tools/rpi-checks.py --all` with `ZF_SENSOR_MSSQL=1` and verify external receipt before pushing or opening a PR | Publication-tier gate outside caller's no-push local `src/core` boundary |

Later implementation of a routed finding does not require another Review.

## Residual Work

* `RV-001`: Execute the Full SQL external gate (`tools/rpi-checks.py --all` + `ZF_SENSOR_MSSQL=1`) and hosted CI prior to PR publication.
* Complete analytics research phases R1 to R3 in `docs/reference/research/iot-sensor-analytics-research-plan.md` before replacing `EXERCISE VALUE` thresholds or approving an operational sensor rule (keep `Refs #111` rather than `Closes #111`).

## Blockers and Remaining Work

* Blockers: none for local `src/core` acceptance and local commit.
* Remaining active work: none (`P01` and `P02` complete).

## Validation Evidence

| Command | Scope | Status | Summary |
| --- | --- | --- | --- |
| `python3 -m mypy` | `src/core` (316 source files) | Passed | `Success: no issues found in 316 source files` |
| `python3 -m ruff check .` | `src/core` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/core` (263 files) | Passed | `263 files already formatted` |
| `python3 -m unittest discover -s tests -p 'test_*sensor*.py' -v` | `src/core/tests` | Passed | `Ran 291 tests in 138.952s — OK (skipped=34)` |
| `python3 -m unittest tests/test_sensor_analysis_reproducibility.py tests/test_sensor_non_authority_boundary.py -q` | `src/api/tests` | Passed | `Ran 10 tests in 12.318s — OK` |
| `python3 tools/rpi-checks.py --all` + `ZF_SENSOR_MSSQL=1` + hosted CI | Repository SQL publication gate | Skipped | Deferred per caller no-push boundary (`RV-001`) |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every active requirement (`FR-1`..`FR-5`, `NFR-1`, `NFR-2`), acceptance criterion (`AC-1`..`AC-6`), and plan-critique correction (`PC-001`..`PC-004`) is satisfied with zero defects, zero `# type: ignore` suppressions, zero `.copilot-tracking/` leaks in `src/`, full backwards compatibility across `sensor_review_draft` and `src/api`, and clean bare `mypy`, `ruff`, and `unittest` execution in `src/core`. Pre-publication SQL/CI gates and R1-R3 standards research are transparently routed as distinct follow-ups (`Refs #111`).

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | none | none |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | distinct follow-up (`RV-001` + R1-R3 research) | Run `tools/rpi-checks.py --all` (`ZF_SENSOR_MSSQL=1`) before PR push; complete R1-R3 before operational rule approval |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Bare `mypy` (316 files), `ruff check .`, `ruff format --check .` (263 files), `src/core` `test_*sensor*.py` (291 run, 34 live-MSSQL skipped, 0 failed), and `src/api` sensor reproducibility/non-authority tests (10/10 passed)
* Blockers: none
