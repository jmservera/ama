<!-- markdownlint-disable-file -->
# RPI Plan: Issue #128 RAI Cohort Evaluation Slice (`ai-128-cohort-ai-eval`)

## Task Metadata

* Task ID: issue-128-cohort-ai-eval
* Task slug: ai-128-cohort-ai-eval
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/ai-128-cohort-ai-eval-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/ai-128-cohort-ai-eval-plan-critique.md

## Executive Summary

This plan delivers the remaining local Responsible AI Cohort Evaluation slice of Issue #128 (`Accessibility, equity and journey ownership testing`, `Refs #128`) inside `zava_forward.core.paired_equity` and `zava_forward.core.cohort_eval`, proven with failing-first unit tests in `src/core/tests/test_paired_equity.py` and `src/core/tests/test_cohort_eval.py`. It extends paired constructed-cohort checks and versioned cohort evaluation records to cover both deterministic prioritisation and AI tasks with transparent non-AI baseline comparison, predeclared contrasts for missing/declined sensors, accessibility/contact needs, provider-versus-resident appointment history and non-response, optional approved geography and archetype dimensions, lawful minimum-necessary gating on protected-characteristic fields, prohibited-inference and service-lowering guards, sensor anti-provisioning and anti-threshold-invention guards, and full retention of cohort/version definitions, reconciled `eligible`/`tested`/`abstained`/`failed` counts, sufficiency, subgroup errors/exclusions, review burden, Wilson uncertainty, and human disposition.

### User Decisions and Requirements Highlights

* Execute all 5 RPI stages continuously (`rpi-research` -> `rpi-plan` -> `rpi-plan-critique` -> `rpi-implement` -> `rpi-review`) on `feat/ai-128-cohort-ai-eval`, commit all code, tests, documentation, and dated `2026-11-15` `.copilot-tracking/` artifacts with `Refs #128`, and leave a clean frozen local candidate without pushing or opening a PR.
* Enforce `fairness_evidence=False` and `activation_allowed=False` whenever independent human/policy/threshold approval is absent or any subgroup, sample, or threshold check fails, and ensure generated cohorts never establish population fairness.
* Use Focused validation: failing-first unit tests in `test_paired_equity.py` and `test_cohort_eval.py`, `ruff check`, `ruff format --isolated --line-length 100 --check`, and bare `python3 -m mypy --cache-dir=/tmp/mypy-128` inside `src/core`.

### What You May Not Know

* Earlier `cohort_eval.py` checked only `MEASUREMENT_BLOCKERS` when computing `fairness_evidence`, which allowed `fairness_evidence=True` on non-synthetic manifests even when `threshold_exceeded` or `unjustified_exclusion` blockers fired; this plan closes that gap by requiring zero blockers and non-generated provenance before `fairness_evidence` can ever be `True`.
* Sibling branch commit `20af48b5e` (#1735) modifies `journey_register.py`; keeping `journey_register.py` untouched and calling `journey_register.human_review_route(case)` with its existing 1-argument contract avoids merge conflicts across stacked branches while preserving compatibility with `src/agents` (`cohort_ranking_eval.py`, `cohort_ai_eval.py`, `ai_eval.py`) and `src/api` (`test_ai_tasks.py`).

### Unresolved Decisions or Blockers

* None within engineering scope. Real human approvals for live cohorts, lawful analysis fields, operational thresholds (`OQ-018`), and ranking policy rule-order sign-off remain external human governance decisions and stay ungranted (`False` / `blocked` / `pending_owner_approval`) in all repository fixtures.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the complete RPI loop in order (`rpi-research`, `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, `rpi-review`) in `/home/azureuser/source/ama-demo-wt/feat-128-cohort-ai-eval` on branch `feat/ai-128-cohort-ai-eval` stacked on `origin/feat/demo-164-chat-grounding-provenance-0900` (`36aeddae345426fdf8ee53565fef1540979de967`) without stopping between phases, and do not push or open a PR (caller prompt).
* Predeclare independently expected paired constructed cohorts differing in source/sensor completeness, accessibility/contact needs, and provider-versus-resident appointment history while holding relevant facts constant (Issue #128 RAI Cohort AC1).
* Evaluate deterministic prioritisation and AI tasks; preserve named ranking-policy ownership, hash/order approval, and transparent non-AI comparison (Issue #128 RAI Cohort AC2).
* Missing/declined sensors and non-response never lower service or priority; do not infer vulnerability, refusal, or protected characteristics (Issue #128 RAI Cohort AC3).
* Retain cohort/version definitions and `eligible`, `tested`, `abstained`, and `failed` counts, sufficiency, subgroup errors/exclusions, review burden, uncertainty, and human disposition (Issue #128 RAI Cohort AC4).
* Detect every seeded unjustified exclusion/deprioritisation defect; a failing subgroup cannot be averaged away (Issue #128 RAI Cohort AC5).
* Unapproved thresholds, missing/small samples, or exceeded thresholds block affected activation pending human disposition (Issue #128 RAI Cohort AC6).
* Use protected-characteristic fields only with lawful minimum-necessary approval; generated cohorts do not establish population fairness (Issue #128 RAI Cohort AC7).
* Include geography/archetype where approved and relevant; sensor completeness fixtures do not provision devices or invent hazard/dew-point thresholds (Issue #128 RAI Cohort AC8).
* Keep `fairness_evidence=False` and `activation_allowed=False` whenever independent human/policy/threshold approval is absent or any subgroup/sample/threshold check fails (caller prompt).
* Write failing-first unit tests in `src/core/tests/test_paired_equity.py` and `src/core/tests/test_cohort_eval.py`, pass `ruff check`, `ruff format --isolated --line-length 100 --check`, and bare `python3 -m mypy --cache-dir=/tmp/mypy-128` in `src/core`, and commit code, tests, docs, and `.copilot-tracking/` `2026-11-15` artifacts with the Copilot `Co-authored-by` trailer and `Refs #128` (caller prompt).

## Goals

* Deliver complete, pure `src/core` enforcement of all 8 RAI Cohort Acceptance Criteria of Issue #128 across `paired_equity.py` and `cohort_eval.py` while preserving backward compatibility with existing callers in `src/core`, `src/agents`, and `src/api`.
* Prove every criterion with failing-first unit tests before production edits, then pass all unit tests, `ruff`, and strict `mypy` checks cleanly.

## Scope and Non-Goals

### In Scope

* `src/core/src/zava_forward/core/paired_equity.py`: predeclared contrast profiles and expectations, deterministic + AI-task evaluation, ranking-policy ownership/hash/rule-order verification, transparent non-AI comparison, service-lowering and prohibited-inference checks, protected-characteristic minimum-necessary approval gate, optional approved geography/archetype dimensions, sensor anti-provisioning and anti-threshold-invention guard, retained cohort/version definitions, `eligible`/`tested`/`abstained`/`failed` counts, and human disposition retention.
* `src/core/src/zava_forward/core/cohort_eval.py`: `"abstained"` outcome, retained `cohort_definitions` and `version_definitions`, reconciled `eligible`/`tested`/`abstained`/`failed` counts, ranking-policy sign-off/hash verification and transparent non-AI baseline comparison, prohibited-inference and service-lowering guards, protected-characteristic minimum-necessary approval gate, geography/archetype relevance and approval gate, sensor anti-provisioning and anti-threshold-invention guard, and tightened `fairness_evidence` / `export_record` invariants.
* `src/core/tests/test_paired_equity.py` and `src/core/tests/test_cohort_eval.py`: failing-first unit tests covering all 8 RAI Cohort Acceptance Criteria.
* `src/core/README.md`: concise documentation updates for `paired_equity` and `cohort_eval`.

### Non-Goals

* Modifying `src/core/src/zava_forward/core/journey_register.py` (kept unchanged to preserve clean stacked-branch compatibility with #1735).
* Provisioning synthetic or live IoT Hub devices, inventing hazard or dew-point thresholds, calling external LLM endpoints, conducting live screen-reader or human-participant studies, or granting live owner/DPO/policy approvals.
* Pushing to `origin` or opening a pull request.

## Functional Requirements

* **FR-1 (Predeclared Paired Constructed Cohorts)**: `paired_equity` exposes predeclared contrast definitions and independent expectations (`PREDECLARED_CONTRASTS` and `predeclared_cohorts(...)`) across `source_completeness` (`missing`, `partial`, `stale`), `sensor_completeness` (`declined`, `missing`), `support_or_contact_need` (`accessibility_adjustment` bundle, `contact_channel_need`), `appointment_history` (`prior_no_access`, `provider_vs_resident`, `provider_vs_resident_no_response`, `non_response`), plus optional `geography` and `archetype` contrasts, rejecting confounded, partial-bundle (`wrong_contrast`), no-contrast, or expectation-weakening pairs.
  * Observable acceptance criteria: AC-1, AC-8.
* **FR-2 (Deterministic & AI Task Evaluation with Policy & Non-AI Comparison)**: Both `paired_equity.evaluate` and `cohort_eval.evaluate` evaluate deterministic prioritisation and AI tasks, verify ranking-policy ownership, `content_hash`, and `rule_order_hash` via `ranking.policy_hash`, `ranking.rule_order_hash`, and `ranking.signoff_problems`, ensure AI execution never mutates deterministic order, and emit a `non_ai_comparison` structure comparing AI outcomes/ranks/exclusions/abstentions against the deterministic non-AI baseline.
  * Observable acceptance criteria: AC-2, AC-6.
* **FR-3 (Non-Demotion & Prohibited-Inference Guard)**: Missing or declined sensors and resident non-response never lower priority or `service_level`; deterministic or AI outputs that lower service or infer `vulnerability`, `refusal`, or protected characteristics fail closed with non-disposable blockers (`service_lowered`, `prohibited_inference`).
  * Observable acceptance criteria: AC-3, AC-5.
* **FR-4 (Retained Definitions, Counts, Sufficiency, Uncertainty & Disposition)**: `cohort_eval.evaluate` (and `paired_equity.evaluate` where applicable) retains `cohort_definitions`, `version_definitions`, reconciled `eligible`, `tested`, `abstained`, and `failed` counts per subgroup and overall (`OUTCOMES` extended with `"abstained"`), sample sufficiency, subgroup error/exclusion/abstention rates, review burden, 95% Wilson intervals, and human disposition.
  * Observable acceptance criteria: AC-4, AC-6.
* **FR-5 (Seeded Defect Detection, Non-Averaging & Fail-Closed Activation/Fairness)**: Every declared seeded unjustified exclusion/deprioritisation/service-lowering defect must be detected (`seeded_defect_undetected` blocks non-disposably if missed), every subgroup is gated independently without cross-cohort averaging, and `fairness_evidence=False` and `activation_allowed=False` hold whenever independent human/policy/threshold approval is absent or any subgroup/sample/threshold check fails (with disposable threshold exceedances clearing `activation_allowed` only when thresholds/samples/approvals are valid and named human disposition accepts, while keeping `fairness_evidence=False`).
  * Observable acceptance criteria: AC-5, AC-6, AC-7.
* **FR-6 (Protected-Characteristic Minimum-Necessary Gate, Context Dimension Gate & Sensor Fixture Guard)**: Protected-characteristic fields (`PROTECTED_CHARACTERISTIC_FIELDS`) require digest-bound DPO/lawful-basis minimum-necessary approval covering exact fields; `geography` and `archetype` dimensions require named-human relevance and scope approval; generated/synthetic cohorts never establish population fairness (`population_fairness_established=False`, `fairness_evidence=False`); and any sensor fixture or manifest containing device-provisioning keys (`device_id`, `iot_hub`, `connection_string`, `sas_token`, `symmetric_key`, `x509`, `SYN-` bindings) or invented hazard/dew-point thresholds (`dew_point*`, `mould_risk_index`, `hazard_threshold`, `damp_threshold`, `rh_hazard_threshold`) fails closed.
  * Observable acceptance criteria: AC-7, AC-8.

## Non-Functional Requirements

* **NFR-1 (Pure Deterministic Core & Backward Compatibility)**
  * Objective threshold or evaluation condition: Zero store, clock, or network imports; 100% pass rate across existing `src/core` and `src/agents` cohort/equity unit tests without editing `src/agents`.
  * Operating condition or verification approach: Run `unittest` across `src/core/tests` and `src/agents/tests/test_cohort_*.py`.
  * Observable acceptance criteria: AC-2, AC-4, AC-9.
* **NFR-2 (Strict Static Typing & Formatting)**
  * Objective threshold or evaluation condition: Zero errors from bare `python3 -m mypy --cache-dir=/tmp/mypy-128` inside `src/core`, `python3 -m ruff check`, and `python3 -m ruff format --isolated --line-length 100 --check` on all modified Python files.
  * Operating condition or verification approach: Focused tier local validation commands.
  * Observable acceptance criteria: AC-9.

## Acceptance Criteria

* **AC-1**: Predeclared independently expected paired constructed cohorts cover source/sensor completeness (including missing and declined), accessibility/contact needs, and provider-versus-resident appointment history (and non-response) while holding relevant facts constant and rejecting confounded or partial contrasts.
* **AC-2**: Both `paired_equity` and `cohort_eval` evaluate deterministic prioritisation and AI tasks, verify ranking-policy named ownership, `content_hash`, and `rule_order_hash` sign-off, and emit transparent non-AI baseline comparisons proving AI never mutates deterministic ranking.
* **AC-3**: Missing/declined sensors and resident non-response never lower priority or service level, and outputs inferring vulnerability, refusal, or protected characteristics are detected and blocked non-disposably.
* **AC-4**: Evaluation records retain `cohort_definitions` and `version_definitions`, reconciled `eligible`, `tested`, `abstained`, and `failed` counts, sample sufficiency, subgroup errors/exclusions, review burden, Wilson uncertainty intervals, and human disposition.
* **AC-5**: Every seeded unjustified exclusion/deprioritisation defect is detected (blocking if missed), and a failing subgroup is never averaged away by larger passing subgroups.
* **AC-6**: Unapproved thresholds, unapproved ranking policy, missing/small samples, or exceeded thresholds keep `activation_allowed=False` and `fairness_evidence=False`, with human disposition restricted strictly to triaging disposable threshold/defect exceedances when base approvals and sample floors are already met (and never creating `fairness_evidence=True`).
* **AC-7**: Protected-characteristic fields without digest-bound lawful minimum-necessary DPO approval fail closed (`unapproved_protected_characteristic`), and generated/constructed/synthetic cohorts always report `fairness_evidence=False` and `population_fairness_established=False`.
* **AC-8**: `geography` and `archetype` dimensions are evaluated when explicitly approved as relevant and blocked when unapproved/irrelevant; sensor completeness fixtures carrying device-provisioning keys or invented hazard/dew-point thresholds fail closed.
* **AC-9**: Failing-first tests are proven to fail before P02 edits and pass afterward alongside existing suites, `ruff check`, `ruff format --isolated --line-length 100 --check`, and bare `python3 -m mypy --cache-dir=/tmp/mypy-128` inside `src/core`.

## Test Ownership and Validation Lock

* Canonical test owners:
  * `src/core/tests/test_paired_equity.py`: Paired constructed-cohort semantics, predeclared contrasts, deterministic + AI-task evaluation, ranking-policy sign-off/hash checks, transparent non-AI comparison, service-lowering/prohibited-inference blocks, protected-field & context-dimension approval gates, and sensor-fixture guard (exact removals: `none`; maximum additions: `12` test methods).
  * `src/core/tests/test_cohort_eval.py`: Versioned cohort record retention (`cohort_definitions`, `version_definitions`, `eligible`/`tested`/`abstained`/`failed` counts), `"abstained"` outcome, ranking-policy & non-AI baseline comparison, prohibited-inference & service-lowering non-disposable blocks, non-averaging & tightened `fairness_evidence` guard, protected-characteristic minimum-necessary gate, geography/archetype context gate, sensor-fixture guard, and `export_record` verification (exact removals: `none`; maximum additions: `12` test methods).
* Generated targets: `none`.
* Semantic vs regression coverage: New tests assert behavioral failure and approval gates across AC-1..AC-8 (failing first against unmodified `paired_equity.py` and `cohort_eval.py`), while existing tests in `test_paired_equity.py`, `test_cohort_eval.py`, `test_rai_threshold_live_approval_guard.py`, `test_heldout_eval.py`, `test_cohort_ranking_eval.py`, `test_cohort_ai_eval.py`, and `test_ai_eval.py` remain untouched as regression guards.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/ai-128-cohort-ai-eval-plan.md                                                                         |
| Phase details                    | .copilot-tracking/details/2026-11-15/ai-128-cohort-ai-eval-phase-details.md                                                              |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/ai-128-cohort-ai-eval-plan-critique.md with Revise disposition; all 6 findings (`PC-001`..`PC-006`) resolved directly |
| Relevant research                | .copilot-tracking/research/2026-11-15/ai-128-cohort-ai-eval-research.md                                                                  |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/ai-128-cohort-ai-eval-changes.md is created or continued by implementation as its evidence record   |
| Planning execution and readiness | Complete and Ready for `rpi-implement`                                                                                                   |
| Continuation context             | Confirmed automatic RPI Agent parent continues directly to `rpi-implement`                                                               |

## Sources

* `.copilot-tracking/research/2026-11-15/ai-128-cohort-ai-eval-research.md`: Codebase evidence `C1`–`C12`, compatibility constraints, and converged pure-core design.
* `docs/prds/zava-forward-retrofit-programme-demonstrator.md`: `FR-054`, `AC-073`, and `OQ-018` cohort, missing-data, non-averaging, and owner-approval requirements.
* `docs/reference/research/ux/equity-journey-test-plan.md` and `docs/reference/research/evaluation/cohort-evaluation-review-pack.md`: Issue #128 / #222 cohort evaluation boundaries and non-fairness invariants.
* `src/core/src/zava_forward/core/paired_equity.py`, `cohort_eval.py`, `ranking.py`, `journey_register.py`, `rai_release.py`, `sensor_view.py`, `data_protection.py`: Target modules and pure core contracts.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Author failing-first unit tests for all 8 RAI Cohort Acceptance Criteria

* Intent: Lock observable behavioral contracts across AC-1 through AC-8 in `test_paired_equity.py` and `test_cohort_eval.py` and verify the new tests fail against unmodified `src/core` before implementation.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add failing-first paired cohort and AI-task tests in `test_paired_equity.py`

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4, FR-5, FR-6; research `C1`, `C4`, `C5`, `C7`, `C8`, `C10`.
* Expected result: Focused test methods added to `src/core/tests/test_paired_equity.py` covering AC-1..AC-8 fail cleanly before P02 edits while existing tests continue to run.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/ai-128-cohort-ai-eval-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add failing-first cohort evaluation and governance tests in `test_cohort_eval.py`

* Requirement and evidence: FR-2, FR-3, FR-4, FR-5, FR-6; research `C2`, `C4`, `C6`, `C7`, `C8`, `C9`, `C12`.
* Expected result: Focused test methods added to `src/core/tests/test_cohort_eval.py` covering AC-1..AC-8 fail cleanly before P02 edits while existing tests continue to run.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/ai-128-cohort-ai-eval-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Implement pure `src/core` RAI Cohort Evaluation controls

* Intent: Extend `paired_equity.py` and `cohort_eval.py` to satisfy all 8 RAI Cohort Acceptance Criteria while maintaining 100% backward compatibility with existing `src/core`, `src/agents`, and `src/api` callers.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Extend `paired_equity.py` for predeclared contrasts, AI-task comparison, and RAI/privacy/sensor guards

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4, FR-5, FR-6; research `C1`, `C3`, `C4`, `C5`, `C8`, `C10`, `C11`.
* Expected result: `paired_equity.py` passes all new and existing `test_paired_equity.py` tests with strict typing.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/ai-128-cohort-ai-eval-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Extend `cohort_eval.py` for abstentions, retained definitions/counts, policy/non-AI comparison, and RAI/privacy/sensor guards

* Requirement and evidence: FR-2, FR-3, FR-4, FR-5, FR-6; research `C2`, `C4`, `C6`, `C7`, `C8`, `C9`, `C11`, `C12`.
* Expected result: `cohort_eval.py` passes all new and existing `test_cohort_eval.py`, `test_rai_threshold_live_approval_guard.py`, `test_heldout_eval.py`, and `src/agents` cohort evaluation tests.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/ai-128-cohort-ai-eval-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Update component documentation and run Focused validation

* Intent: Synchronize `src/core/README.md` with the delivered capabilities and boundaries, and pass unit tests, `ruff`, and strict `mypy` validation.
* Dependencies: P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Update `src/core/README.md` and run Focused test, lint, format, and `mypy` checks

* Requirement and evidence: NFR-1, NFR-2, AC-9; `.github/copilot-instructions.md` Focused validation tier.
* Expected result: `src/core/README.md` accurately documents `paired_equity` and `cohort_eval` capabilities and non-fairness/human-approval boundaries; all targeted unit tests, `ruff check`, `ruff format --isolated --line-length 100 --check`, and bare `python3 -m mypy --cache-dir=/tmp/mypy-128` inside `src/core` pass with zero errors.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/ai-128-cohort-ai-eval-phase-details.md

## Dependencies

* `zava_forward.core.ranking`: Provides `CURRENT`, `rank`, `policy_hash`, `rule_order_hash`, `signoff_problems`, and `is_signed` for deterministic baseline and policy ownership/hash/order verification.
* `zava_forward.core.journey_register`: Provides `human_review_route(case)` (`rank_effect == "none"`) without requiring edits to `journey_register.py`.
* `zava_forward.core.rai_release`: Provides `digest`, `named`, and `named_human` for deterministic SHA-256 binding and human-approver verification.

## Critique Disposition

One-pass final-candidate critique completed in `.copilot-tracking/reviews/plans/2026-11-15/ai-128-cohort-ai-eval-plan-critique.md` (`Revise`, 4 High, 2 Medium, all planner-owned direct refinements). All six findings are resolved directly without user-decision conflicts:

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` [High] (`named_human` & placeholder/date guards on `_thresholds_approved` and `disposition`) | Resolved | Updated `P01-T02`, `P02-T01`, and `P02-T02` so `_thresholds_approved` and `disposition["by"]` enforce `named_human(...)`, reject placeholder/expired approvals, validate optional `max_abstention_rate`/`max_abstention_gap` limits, and gate `fairness_evidence` on `owner_approval_status != "unapproved"`. |
| `PC-002` [High] (mandatory `ranking_policy` on AI/ranking tasks, per-case/per-subgroup non-AI regression, bound `policy` ranker & `ai_task` return contracts) | Resolved | Updated `P01-T01`, `P01-T02`, `P02-T01`, and `P02-T02` to require `ranking_policy` whenever `task_kind in {"ai_task", "ranking", "prioritisation"}` or `non_ai_observed`/`non_ai_baseline` is supplied, detect per-case and per-subgroup AI regressions vs `non_ai_observed`, bind validated `policy` in `paired_equity` default `ranking.rank`, and accept both `Sequence` and envelope `Mapping` `ai_task` outputs. |
| `PC-003` [High] (approval-envelope exclusion in `manifest_digest`, `paired_equity.input_digest`, exact `PROTECTED_CHARACTERISTIC_FIELDS`, `_is_generated_cohort`) | Resolved | Updated `P02-T01` and `P02-T02` to exclude `"approval"`, `"protected_characteristic_approval"`, and `"context_dimension_approvals"` from `cohort_eval.manifest_digest`, expose `paired_equity.input_digest(pairs, anchors)`, lock the exact UK Equality Act `PROTECTED_CHARACTERISTIC_FIELDS` set (excluding operational `priority_support`/`adjustment`/`notes`), and enforce `_is_generated_cohort` across `_owner_approval_status`, `_live_gaps`, `export_record`, and unconditional `population_fairness_established: False`. |
| `PC-004` [High] (`case["cohorts"]` lookup for `service_lowered` and unified per-case `errors`/`failed`/`detected_defects` accounting) | Resolved | Updated `P02-T02` so `service_lowered` inspects `case["cohorts"]` as well as case/input attributes, per-case failures (`actual != expected or service_lowered or prohibited_inference`) feed `_cohort_row` `errors`/`failed`/`error_rate`/`error_interval`, and `service_lowered` counts toward `detected_defects` while keeping `service_lowered` and `prohibited_inference` blockers non-disposable. |
| `PC-005` [Medium] (typed `Callable` wrappers for untyped `ranking.*` helpers, preserved `RECORD_VERSION`, and default-ranker `record_hash` parity) | Resolved | Updated `P01-T01`, `P01-T02`, `P02-T01`, and `P02-T02` to bind untyped `ranking.*` helpers via typed `Callable` aliases for strict `mypy`, keep `paired_equity.RECORD_VERSION = "paired-equity-check-v1"`, and preserve identical metadata when `rank is None or rank is ranking.rank`. |
| `PC-006` [Medium] (`paired_equity` AC-4/AC-6 subgroup metrics/thresholds, per-profile `review_route`, and `{dim}:missing_dimension` alignment) | Resolved | Updated `P01-T01` and `P02-T01` to emit per-dimension `eligible`/`tested`/`abstained`/`failed`/`excluded`/`deprioritised`/`review`/`review_burden`/`error_interval`/`sufficient`, validate optional `thresholds` and `expectation_approval`, lock `review_route` expectations against `journey_register.INCOMPLETE_APPOINTMENT` (`"none"` on `provider_vs_resident`), and emit `{dim}:missing_dimension` on zero-pair approved optional dimensions. |

## Follow-Up Items

* External human governance and live user-research items on Issue #128 (human screen-reader runs, staffed missing-data workflow, agreed user-research protocol, DPO/owner OQ-018 live cohort/threshold approvals, and human ranking-policy sign-off) remain owner/human actions outside pure `src/core` engineering scope.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/ai-128-cohort-ai-eval-changes.md
* Ready phase or task: P01 (`P01-T01`, `P01-T02`)
* Remaining provisional question or blocker: None
