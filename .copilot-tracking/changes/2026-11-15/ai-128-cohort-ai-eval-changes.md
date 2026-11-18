<!-- markdownlint-disable-file -->
# RPI Changes: Local RAI Cohort Evaluation Slice of Issue #128

## Metadata

* Task ID: 2026-11-15-ai-128-cohort-ai-eval
* Related plan: .copilot-tracking/plans/2026-11-15/ai-128-cohort-ai-eval-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/ai-128-cohort-ai-eval-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`
* All remaining active-plan markers: None
* Status basis: Full plan (`P01`..`P03`) implemented, documented in `src/core/README.md`, and verified under Focused validation (`107` `src/core` tests + `45` `src/agents` cohort/AI eval tests passing, `ruff check` and `ruff format --isolated --line-length 100 --check` clean, and bare `python3 -m mypy --cache-dir=/tmp/mypy-128` passing across `342` source files).

## Execution Summary

Executing full-plan implementation (`P01` -> `P02` -> `P03`) on `feat/ai-128-cohort-ai-eval` inside `src/core` without modifying `journey_register.py`.

## Completed Work

### Failing-first RAI cohort evaluation test suites (`P01`)

* Related phase or task: `P01`, `P01-T01`, `P01-T02`
* Files: `src/core/tests/test_paired_equity.py`, `src/core/tests/test_cohort_eval.py`
* What changed and why: Added 7 focused tests in `test_paired_equity.py` and 7 focused tests in `test_cohort_eval.py` covering all 8 RAI Cohort Acceptance Criteria (`Refs #128`) and critique refinements (`PC-001`..`PC-006`) before modifying production code.
* Completion evidence: `PYTHONPATH=src:tests python3 -m unittest test_paired_equity test_cohort_eval` ran 69 tests (`failures=10, errors=4` on all 14 new tests; all 55 existing tests continued passing).
* Validation: Passed failing-first verification (`FAILED (failures=10, errors=4)` prior to `P02`).

### Pure `src/core` RAI cohort evaluation controls (`P02`)

* Related phase or task: `P02`, `P02-T01`, `P02-T02`
* Files: `src/core/src/zava_forward/core/paired_equity.py`, `src/core/src/zava_forward/core/cohort_eval.py`
* What changed and why:
  * Extended `paired_equity.py` (`P02-T01`) with `PREDECLARED_CONTRASTS` (`provider_cancelled`, `provider_delayed`, `no_response`, `prior_no_access`), `predeclared_cohorts()`, `input_digest()`, optional `geography`/`archetype` relevance approvals, DPO minimum-necessary protected-characteristic gating, signed ranking-policy ownership/hash/order verification, AI-task paired evaluation and transparent `non_ai_comparison`, safe abstention vs service-lowering/prohibited-inference distinction, sensor anti-provisioning and anti-threshold-invention guards, retained `cohort_definitions`/`version_definitions`/`counts`/sufficiency/Wilson intervals, and fail-closed `disposition` handling.
  * Extended `cohort_eval.py` (`P02-T02`) with `"abstained"` outcome, retained `cohort_definitions`, `version_definitions`, `counts` (`eligible`, `tested`, `abstained`, `failed`, `missing`), `approve_protected_characteristics()`, `approve_context_dimensions()`, approval-envelope exclusion in `manifest_digest()`, human-approver/placeholder/ISO-date checks on thresholds and dispositions, `ranking_policy` and `non_ai_comparison` checks, `service_lowered` and `prohibited_inference` defect accounting, sensor fixture provisioning/invented-threshold blockers, generated-cohort non-fairness invariants (`fairness_evidence: False`), and `export_record()` enforcement.
* Completion evidence: 107 targeted unit tests in `src/core` and 25 cohort evaluation unit tests in `src/agents` passed (`OK`).
* Validation: Passed unit test suites across `src/core` and `src/agents`; passed `mypy` and `ruff` checks in `P03-T01`.

### Component documentation and Focused validation (`P03`)

* Related phase or task: `P03`, `P03-T01`
* Files: `src/core/README.md`
* What changed and why: Updated the `#222 and #128 cohort evaluator` and `paired_equity.evaluate` sections in `src/core/README.md` to document predeclared contrasts, AI-task and transparent non-AI comparison, signed ranking-policy ownership/hash/order verification, safe abstention retention, service-lowering and prohibited-inference blockers, DPO minimum-necessary protected-characteristic gating, geography/archetype relevance gating, sensor fixture anti-provisioning and anti-threshold-invention guards, retained definitions/counts/dispositions, and fail-closed non-fairness invariants.
* Completion evidence: Markdown links in `src/core/README.md` verified intact; Focused validation passed with zero errors.
* Validation:
  * `ruff check`: `All checks passed!`
  * `ruff format --isolated --line-length 100 --check`: `4 files already formatted`
  * `python3 -m mypy --cache-dir=/tmp/mypy-128` in `src/core`: `Success: no issues found in 342 source files`
  * `unittest`: `107` tests in `src/core` (`OK`) and `45` tests in `src/agents` (`OK`).

## Implementation-Time Plan and Detail Updates

None.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| Failing-first `unittest` | `src/core/tests/test_paired_equity.py`, `src/core/tests/test_cohort_eval.py` | Passed (verified failing before `P02`) | `Ran 69 tests`: `FAILED (failures=10, errors=4)` on 14 new tests; 55 existing tests passed |
| Post-implementation `unittest` | `src/core/tests` (`test_paired_equity`, `test_cohort_eval`, `test_journey_register`, `test_rai_threshold_live_approval_guard`, `test_heldout_eval`) & `src/agents/tests` (`test_cohort_ranking_eval`, `test_cohort_ai_eval`, `test_ai_eval`) | Passed | `Ran 107 tests in 0.788s: OK` (`src/core`); `Ran 45 tests in 14.153s: OK` (`src/agents`) |
| `ruff check` & `ruff format --isolated --line-length 100 --check` | `paired_equity.py`, `cohort_eval.py`, `test_paired_equity.py`, `test_cohort_eval.py` | Passed | `All checks passed!`, `4 files already formatted` |
| Bare `python3 -m mypy --cache-dir=/tmp/mypy-128` | `src/core` (`342` source files) | Passed | `Success: no issues found in 342 source files` |
| Documentation & tracking hygiene | `src/core/README.md` and `src/` | Passed | Relative links intact; zero `.copilot-tracking/` strings in `src/` |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P02`, `P03` and all tasks `P01-T01`..`P03-T01` checked complete; aligned with phase details)
* Completed-work evidence and handoff prose: Reconciled
* Validation, blockers, remaining work, and follow-up items: Reconciled
* Review readiness: Ready (`Full plan` complete under Focused validation tier)

## Blockers

* None

## Remaining Work

* None

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/ai-128-cohort-ai-eval-plan.md, `## Follow-Up Items`
* Operational/population fairness evidence harness once approved real operational datasets and live DPO/RAI sign-offs exist (out of scope for local synthetic/constructed demonstrator slice; owner: Data Lead / DPO / RAI Owner).
* Post-merge integration of sibling `#1735` appointment-status expansions (`reschedule_requested`, `cancelled`) once `#1735` merges upstream (`journey_register.py` intentionally untouched here; owner: backlog coordinator).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan; completed: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`; remaining: None
* Validation coverage: Focused tier passed (`unittest` across `src/core` and `src/agents`, `ruff check`, `ruff format --isolated --line-length 100 --check`, bare `mypy` across 342 files, documentation review)
* Blockers: None
* Current plan and detail updates: All phase and task markers checked complete in plan
* Planning and critique state: Ready (`PC-001`..`PC-006` resolved and verified in tests and implementation)
* Follow-up items: 2 deferred items retained in plan
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Parent automatic RPI Agent transitioning to `Review`
