<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #128 RAI Cohort Evaluation Slice (`ai-128-cohort-ai-eval`)

## Metadata

* Task ID: issue-128-cohort-ai-eval
* Task slug: ai-128-cohort-ai-eval
* Related plan: .copilot-tracking/plans/2026-11-15/ai-128-cohort-ai-eval-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/ai-128-cohort-ai-eval-research.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md, docs/reference/research/ux/equity-journey-test-plan.md

## Phase Index

| Phase ID | Name                                                                 | Status | Detail sections        |
|----------|----------------------------------------------------------------------|--------|------------------------|
| P01      | Author failing-first unit tests for all 8 RAI Cohort Acceptance Criteria | Ready  | P01, P01-T01, P01-T02  |
| P02      | Implement pure `src/core` RAI Cohort Evaluation controls             | Ready  | P02, P02-T01, P02-T02  |
| P03      | Update component documentation and run Focused validation            | Ready  | P03, P03-T01           |

<!-- rpi:phase id=P01 -->
## P01: Author failing-first unit tests for all 8 RAI Cohort Acceptance Criteria

### Context

Research (`C1`, `C2`, `C6`, `C7`) verified that existing unit tests in `src/core/tests/test_paired_equity.py` and `src/core/tests/test_cohort_eval.py` pin deterministic 4-pair comparability and OQ-018 owner-approval boundaries, while all 8 new RAI Cohort Acceptance Criteria slices lack test coverage and implementation. Writing failing-first tests before modifying `paired_equity.py` or `cohort_eval.py` proves that each test catches real missing behavior rather than restating constants.

### Intent

Add focused, high-signal failing-first unit test methods in `test_paired_equity.py` (<= 12 additions, 0 removals) and `test_cohort_eval.py` (<= 12 additions, 0 removals) covering AC-1 through AC-8 and capture their pre-implementation failure output.

### Boundaries

* Included: `src/core/tests/test_paired_equity.py` and `src/core/tests/test_cohort_eval.py`.
* Excluded: Modifying existing test assertions or touching `src/core/src/` during P01.

### Likely Targets

* `src/core/tests/test_paired_equity.py`: Add failing-first tests for AC-1..AC-8 on paired constructed cohorts and AI-task comparisons.
* `src/core/tests/test_cohort_eval.py`: Add failing-first tests for AC-1..AC-8 on versioned cohort records, abstentions, policy/non-AI comparisons, and governance/privacy/sensor guards.

### Dependencies

* None.

### Validation Expectations

* Running `PYTHONPATH=src:tests python3 -m unittest tests/test_paired_equity.py tests/test_cohort_eval.py` inside `src/core` shows existing tests passing and every newly added P01 test failing against the unmodified modules.

### Completion Evidence

* Observed pre-implementation failure count and failure reasons recorded in `.copilot-tracking/changes/2026-11-15/ai-128-cohort-ai-eval-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add failing-first paired cohort and AI-task tests in `test_paired_equity.py`

#### Context

`paired_equity.py` (`C1`) currently lacks predeclared multi-profile contrasts (`missing` sensor, `contact_need`, `provider_vs_resident` appointment history, `no_response`), AI-task evaluation and `non_ai_comparison`, ranking-policy hash/order/owner verification, service-lowering and prohibited-inference detection, protected-characteristic minimum-necessary gating, optional approved `geography`/`archetype` dimensions, sensor anti-provisioning/anti-threshold-invention guards, and retained definitions/counts/disposition.

#### Intent

Author <= 12 focused failing-first tests in `src/core/tests/test_paired_equity.py`:
1. `test_predeclared_cohorts_cover_completeness_contact_and_provider_vs_resident_history`: Verifies `predeclared_cohorts()` and `evaluate(...)` accept predeclared missing/declined sensor, partial/stale source, accessibility + contact-channel needs, provider-vs-resident appointment history (`provider_cancelled` -> `resident_rescheduled`), and resident `no_response` contrasts while holding relevant facts constant and rejecting weakened pair expectations (`contradicts_predeclared_expectation`).
2. `test_ai_task_evaluation_preserves_ranking_policy_and_transparent_non_ai_comparison`: Evaluates deterministic `rank` alongside an `ai_task` callable, asserting `ranking_policy` preserves `policy_id`, `version`, `owner`, `content_hash`, `rule_order_hash`, and `signoff_problems`, deterministic order is unmutated, `non_ai_comparison` records side-by-side deterministic vs AI results, and AI demotion/exclusion of missing-sensor or resident-history subjects fails and blocks.
3. `test_tampered_ranking_policy_hash_or_unsigned_policy_blocks_activation`: Verifies tampered `content_hash` or broken `rule_order_hash` blocks with `ranking_policy` blocker, and unsigned `ranking.CURRENT` keeps `activation_allowed=False` and `fairness_evidence=False`.
4. `test_missing_sensor_and_non_response_never_lower_service_or_infer_prohibited_traits`: Verifies AI or ranker outputs that lower `service_level` or infer `vulnerability`, `refusal`, or protected characteristics (`disability`, `ethnicity`, `age`) from declined/missing sensors or `no_response` fail with `service_lowered` / `prohibited_inference` and cannot be averaged away across passing dimensions.
5. `test_retains_cohort_and_version_definitions_abstained_counts_and_disposition`: Verifies retained `cohort_definitions`, `version_definitions`, reconciled `eligible`/`tested`/`abstained`/`failed` counts (safe AI abstention to deterministic manual path increments `abstained` without lowering service, whereas unapproved abstention without fallback or seeded AI exclusion is caught), and retained human `disposition` while keeping `fairness_evidence=False` and `activation_allowed=False` without full independent approvals.
6. `test_protected_characteristic_fields_require_lawful_minimum_necessary_approval`: Verifies pairs carrying protected-characteristic fields (`ethnicity`, `disability`, `age`, `religion`) block with `unapproved_protected_characteristic` unless digest-bound real-human DPO `protected_fields_approval` covers the exact fields with `lawful_basis` and `minimum_necessary_justification`, and generated cohorts always keep `fairness_evidence=False` and `population_fairness_established=False`.
7. `test_geography_and_archetype_included_only_when_approved_and_relevant`: Verifies `geography` and `archetype` pairs block when unapproved or marked `relevant=False`, succeed and enforce non-averaging when approved as relevant by a named human, and block with `missing_dimension` if approved as relevant with zero valid pairs.
8. `test_sensor_completeness_fixtures_reject_device_provisioning_and_invented_thresholds`: Verifies pairs or anchors containing `device_id` / `SYN-` / `iot_hub` / `connection_string` / `sas_token` or `dew_point_c` / `mould_risk_index` / `hazard_threshold` / `damp_threshold` fail closed (`sensor_fixture_provisions_device` / `sensor_fixture_invents_threshold`).

#### Boundaries

* Included: New test methods in `PairedEquityTests` in `src/core/tests/test_paired_equity.py`.
* Excluded: Existing 25 test methods in `test_paired_equity.py` (must remain unaltered).

#### Likely Targets

* `src/core/tests/test_paired_equity.py`: Append focused AC-1..AC-8 test methods.

#### Dependencies

* None.

#### Validation Expectations

* All newly added tests fail prior to P02-T01 because the new attributes, arguments, and guards do not exist yet.

#### Completion Evidence

* Pre-implementation test run output confirming failure of the new `PairedEquityTests` methods.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add failing-first cohort evaluation and governance tests in `test_cohort_eval.py`

#### Context

`cohort_eval.py` (`C2`, `C6`) lacks `"abstained"` in `OUTCOMES`, explicit `eligible`/`tested`/`abstained`/`failed` counts, retained `cohort_definitions` and `version_definitions`, `ranking_policy` sign-off/hash verification and `non_ai_comparison`, prohibited-inference and service-lowering non-disposable blockers, protected-characteristic minimum-necessary approval gating, `geography`/`archetype` context-approval gating, sensor-fixture device/threshold guards, and allows `fairness_evidence=True` on non-synthetic manifests even when `threshold_exceeded` or `unjustified_exclusion` blockers fire.

#### Intent

Author <= 12 focused failing-first tests in `src/core/tests/test_cohort_eval.py`:
1. `test_retains_cohort_and_version_definitions_and_reconciles_eligible_tested_abstained_failed`: Verifies `cohort_definitions`, `version_definitions`, `"abstained"` outcome support, and per-cohort + top-level `counts` (`eligible == tested + missing`, `abstained`, `failed`, `abstention_rate`, `review_burden`, Wilson `error_interval`, `sufficient`) and `export_record` compatibility.
2. `test_ai_task_requires_and_compares_transparent_non_ai_baseline_and_ranking_policy`: Verifies `ranking_policy` hash/rule-order/owner verification (`unapproved_ranking_policy` / `invalid_ranking_policy_hash` when unsigned or tampered) and `non_ai_comparison` on `task_kind="ai_task"` or `non_ai_observed=...`, blocking when baseline is missing or AI degrades subgroup exclusion/deprioritisation relative to the deterministic non-AI baseline.
3. `test_missing_sensor_and_non_response_service_lowering_and_prohibited_inferences_block_non_disposably`: Verifies observed `service_level="lowered"` on missing/declined sensor or `no_response` cases and prohibited inferences (`vulnerability`, `refusal`, protected characteristics) increment subgroup failures, emit non-disposable `service_lowered` / `prohibited_inference` blockers, and cannot be cleared by human `disposition`.
4. `test_failing_small_subgroup_cannot_be_averaged_away_and_denies_fairness_evidence`: Verifies a small failing subgroup alongside a large zero-error cohort blocks activation (`aggregation_rule == "per_cohort_unaveraged"`), and even on `synthetic=False` manifests any threshold/defect/policy/approval failure or dispositioned exceedance keeps `fairness_evidence=False`.
5. `test_protected_characteristic_fields_require_bound_dpo_minimum_necessary_approval`: Verifies protected-characteristic fields in `cohorts`, `lawful_analysis_fields`, or cases block with non-disposable `unapproved_protected_characteristic` unless digest-bound real-human DPO `protected_characteristic_approval` names `lawful_basis`, `minimum_necessary_justification`, `approved_at`, and exact `approved_fields`; also verifies `cohort_origin="generated"` (even with `synthetic=False`) keeps `fairness_evidence=False` and `population_fairness_established=False`.
6. `test_geography_and_archetype_require_bound_relevance_approval`: Verifies `geography` and `archetype` dimensions in `manifest["cohorts"]` block with `unapproved_context_dimension` when unapproved or `relevant=False`, and evaluate per-subgroup cleanly when digest-bound `context_dimension_approvals` record named-human approval, `relevant=True`, and rationale.
7. `test_sensor_completeness_manifest_and_observations_reject_provisioning_and_invented_thresholds`: Verifies device-provisioning keys (`device_id`, `iot_hub`, `sas_token`, `SYN-` device bindings) and invented thresholds (`dew_point_c`, `dew_point_threshold`, `mould_risk_index`, `hazard_threshold`, `damp_threshold`) in manifests, thresholds, cases, or observations block non-disposably (`sensor_fixture_provisions_device` / `sensor_fixture_invents_threshold`).

#### Boundaries

* Included: New test methods in `CohortEvalTests` in `src/core/tests/test_cohort_eval.py`.
* Excluded: Modifying existing test methods in `test_cohort_eval.py` or `cohort_eval_fixture.py`.

#### Likely Targets

* `src/core/tests/test_cohort_eval.py`: Append focused AC-1..AC-8 test methods.

#### Dependencies

* None.

#### Validation Expectations

* All newly added tests fail prior to P02-T02 while existing `CohortEvalTests` pass.

#### Completion Evidence

* Pre-implementation test run output confirming failure of the new `CohortEvalTests` methods.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Implement pure `src/core` RAI Cohort Evaluation controls

### Context

With failing-first tests in place from P01, `paired_equity.py` and `cohort_eval.py` can be extended cleanly using shared pure primitives from `ranking.py`, `journey_register.py`, and `rai_release.py` without introducing store, clock, or network dependencies or breaking downstream `src/agents` and `src/api` callers.

### Intent

Implement complete, fail-closed enforcement of AC-1 through AC-8 in `paired_equity.py` and `cohort_eval.py`.

### Boundaries

* Included: `src/core/src/zava_forward/core/paired_equity.py` and `src/core/src/zava_forward/core/cohort_eval.py`.
* Excluded: `journey_register.py`, `src/agents/`, `src/api/`.

### Likely Targets

* `src/core/src/zava_forward/core/paired_equity.py`: Contrast profiles, AI-task + non-AI comparison, policy verification, privacy/inference/sensor/context guards, retained definitions/counts/disposition.
* `src/core/src/zava_forward/core/cohort_eval.py`: `"abstained"` outcome, retained definitions and `eligible`/`tested`/`abstained`/`failed` counts, policy & non-AI baseline comparison, privacy/inference/sensor/context guards, tightened `fairness_evidence` and `export_record` validation.

### Dependencies

* P01 completed with verified failing-first test evidence.

### Validation Expectations

* All unit tests in `test_paired_equity.py`, `test_cohort_eval.py`, `test_journey_register.py`, `test_rai_threshold_live_approval_guard.py`, `test_heldout_eval.py`, and `src/agents/tests/test_cohort_*.py` pass.

### Completion Evidence

* Passing unit test execution across new and existing test suites.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Extend `paired_equity.py` for predeclared contrasts, AI-task comparison, and RAI/privacy/sensor guards

#### Context

`paired_equity.py` (`C1`) must preserve its existing 4-argument positional signature `evaluate(pairs, anchors, seeded_defects=(), rank=None)` and default `status == "pass"` / `activation_allowed == False` / `fairness_evidence == False` behavior while adding keyword-optional parameters (`policy`, `ai_task`, `ai_task_id`, `context_approvals`, `protected_fields_approval`, `expectation_approval`, `thresholds`, `disposition`) and full AC-1..AC-8 checks.

#### Intent

Implement in `paired_equity.py`:
* Keep `RECORD_VERSION = "paired-equity-check-v1"`, bind untyped `ranking.*` helpers (`rank`, `policy_hash`, `rule_order_hash`, `signoff_problems`, `is_signed`) via typed module-level `Callable` aliases for strict `mypy` (`PC-005`), and treat `rank is None` and `rank is ranking.rank` identically so default-ranker `record_hash` parity holds (`PC-005`).
* Expose `input_digest(pairs, anchors)` (`PC-003`), `PREDECLARED_CONTRASTS`, `OPTIONAL_DIMENSIONS = ("geography", "archetype")`, and `predeclared_cohorts(include_optional=())` returning versioned contrast definitions and independent expectations aligned with `journey_register.INCOMPLETE_APPOINTMENT` (`review_route="human_review"` on `missing`/`partial`/`stale` source, `declined`/`missing` sensor, `prior_no_access`, `provider_vs_resident_no_response`, and `non_response`; `review_route="none"` on `provider_vs_resident`, `accessibility_adjustment`, `contact_channel_need`, `geography`, and `archetype`, `PC-006`), while keeping `DIMENSIONS` and `CONTRASTS` intact.
* `_comparability(dimension, pair)` matching exact predeclared contrast profiles first, flagging supersets as `"confounded"`, empty diffs as `"no_contrast"`, partial/mismatched diffs as `"wrong_contrast"`, unknown explicit contrast names as `"unknown_contrast"`, and pair-level `"expected"` overrides that weaken predeclared expectations as `"contradicts_predeclared_expectation"`.
* Ranking-policy verification (`policy_hash`, `rule_order_hash`, `signoff_problems`, `is_signed`), binding validated `policy` into default `ranking.rank` when `rank is None` (`PC-002`), blocking on tampered `content_hash` or invalid policy rules (`ranking_policy:content_hash_mismatch` / `ranking_policy:invalid_policy`), and keeping `activation_allowed=False` whenever signed human policy, digest-bound `named_human` `expectation_approval`, or digest-bound `named_human` `thresholds` is absent (`PC-001`, `PC-006`).
* AI-task evaluation (`ai_task` callable accepting `Sequence[Mapping[str, Any]]` and returning either a `Sequence[Mapping[str, Any]]` ranked item list or a `Mapping[str, Any]` envelope with `items`, `status`, `abstained`, `fallback_to_non_ai`, `service_level`, `inferences`, `PC-002`) and `non_ai_comparison`: snapshot inputs before calling `ai_task` to verify deterministic `rank` and inputs are unmutated; compare AI order, inclusion, `abstained` fallback, `service_level`, authority claims (`status` other than `"Proposed"`), and prohibited inferences (`vulnerability`, `refusal`, `PROTECTED_CHARACTERISTIC_FIELDS`) against both the AI reference output and the deterministic non-AI baseline.
* Exact `PROTECTED_CHARACTERISTIC_FIELDS` (`age`, `disability`, `gender_reassignment`, `marriage_and_civil_partnership`, `marital_status`, `pregnancy`, `maternity`, `pregnancy_and_maternity`, `race`, `ethnicity`, `ethnic_origin`, `nationality`, `religion`, `belief`, `religion_or_belief`, `sex`, `gender`, `sexual_orientation` — excluding operational `priority_support`, `adjustment`, `notes`, `PC-003`) gated by digest-bound `protected_fields_approval`; `geography`/`archetype` gated by `context_approvals` (emitting `{dim}:missing_dimension` when approved relevant with zero valid pairs, `PC-006`); sensor anti-provisioning & anti-threshold-invention check (`sensor_fixture_provisions_device`, `sensor_fixture_invents_threshold`); retained `cohort_definitions`, `version_definitions`, per-dimension and overall `eligible`/`tested`/`abstained`/`failed`/`excluded`/`deprioritised`/`review`/`review_burden`/`error_interval`/`sufficient` (`PC-006`), `aggregation_rule: "per_cohort_unaveraged"`, `population_fairness_established: False`, `fairness_evidence: False`, and `named_human`-validated `disposition` retention (`PC-001`).

#### Boundaries

* Included: `src/core/src/zava_forward/core/paired_equity.py`.
* Excluded: Any external I/O, clock, or store access.

#### Likely Targets

* `src/core/src/zava_forward/core/paired_equity.py`.

#### Dependencies

* P01-T01.

#### Validation Expectations

* `PYTHONPATH=src:tests python3 -m unittest tests/test_paired_equity.py -q` passes 100%.

#### Completion Evidence

* Clean pass of all existing and newly added `test_paired_equity.py` tests.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Extend `cohort_eval.py` for abstentions, retained definitions/counts, policy/non-AI comparison, and RAI/privacy/sensor guards

#### Context

`cohort_eval.py` (`C2`, `C6`, `C12`) powers offline and live-gated cohort evaluation records across `src/core`, `src/agents`, and `src/api`. All extensions must preserve existing dict keys (`n`, `missing`, `errors`, `excluded`, `deprioritised`, `review`, `defects`, `error_rate`, `exclusion_rate`, `review_burden`, `error_interval`, `sufficient`, `owner_approval_status`, `lawful_analysis_fields`, `lawful_analysis_fields_approved`, `live_activation_allowed`, `synthetic_not_fairness_evidence`, `non_fairness_provenance_notice`) while closing all AC-1..AC-8 gaps.

#### Intent

Implement in `cohort_eval.py`:
* Extend `OUTCOMES = ("ranked", "deprioritised", "excluded", "review", "abstained")` and bind untyped `ranking.*` helpers via typed module-level `Callable` aliases (`PC-005`).
* Exclude `"approval"`, `"protected_characteristic_approval"`, and `"context_dimension_approvals"` from `manifest_digest` so sequential approval bindings never self-invalidate (`PC-003`).
* Upgrade `_thresholds_approved(manifest, now)` and `disposition["by"]` to require `named_human(...)`, reject placeholder tokens (`"todo"`, `"tbd"`, `"to be named"`, `"tbc"`, `"unassigned"`) and `_has_invalid_or_expired_date(approval, now)`, and validate optional rate limits (`max_abstention_rate`, `max_abstention_gap`) (`PC-001`).
* Add `eligible`, `tested`, `abstained`, `failed`, and `abstention_rate` to `_cohort_row` and top-level `counts` (`eligible == tested + missing`, `tested == n`, `failed == errors`, `abstained` counting `actual == "abstained"` or `obs.get("abstained") is True`, with abstentions defaulting `review_required` to `True` unless explicitly `False`, and optional `max_abstention_rate` / `max_abstention_gap` enforcement).
* Retain `cohort_definitions` and `version_definitions` (`record_version`, `manifest_digest`, `cohort_version`, `subject_version`, `policy_version`, `ranking_policy_id`, `ranking_policy_hash`, `ranking_rule_order_hash`, `prompt_version`, `model_version`), `aggregation_rule: "per_cohort_unaveraged"`, and unconditional `population_fairness_established: False` (`PC-003`).
* Require `ranking_policy` whenever `manifest.get("task_kind") in {"ai_task", "ranking", "prioritisation"}` or `non_ai_observed` / `manifest.get("non_ai_baseline")` is present (`PC-002`), verifying via typed `ranking.policy_hash`, `ranking.rule_order_hash`, and `ranking.signoff_problems`, emitting non-disposable `invalid_ranking_policy_hash` or `unapproved_ranking_policy` blockers when missing, tampered, or unsigned, and binding supplied `ranking_policy` / `non_ai_observed` kwargs into `input_digests`.
* Compute `non_ai_comparison` when `non_ai_observed` (or `manifest.get("non_ai_baseline")`) is provided or `manifest.get("task_kind") == "ai_task"`, blocking non-disposably (`missing_non_ai_comparison` / `non_ai_comparison_invalid`) when missing/unreconciled on `ai_task` and blocking (`ai_regression_vs_non_ai`) on per-case or per-subgroup AI regressions vs `non_ai_observed` (`PC-002`).
* Detect lowered `service_level` on missing/declined sensor or `no_response` cases by inspecting `case["cohorts"]`, top-level `case` fields, and `manifest.get("inputs")` (`PC-004`), and detect prohibited inferences of `vulnerability`, `refusal`, or `PROTECTED_CHARACTERISTIC_FIELDS` (`prohibited_inference`) in observations; count per-case policy violations (`actual != expected or service_lowered or prohibited_inference`) in `_cohort_row` `errors`/`failed`/`error_rate`/`error_interval`, include `service_lowered` in `detected_defects`, and emit non-disposable `service_lowered` / `prohibited_inference` blockers (`PC-004`).
* Gate the exact `PROTECTED_CHARACTERISTIC_FIELDS` set (`PC-003`) in `cohorts`, `lawful_analysis_fields`, or cases behind digest-bound real-human DPO `protected_characteristic_approval` (`dpo_owner`/`approved_by`, `lawful_basis`, `minimum_necessary_justification`, `approved_at`, exact `approved_fields`), blocking non-disposably with `unapproved_protected_characteristic` otherwise.
* Gate `"geography"` and `"archetype"` dimensions in `cohorts` behind digest-bound `context_dimension_approvals` (`approved_by` named human, `relevant: True`, non-empty `rationale`), blocking non-disposably with `unapproved_context_dimension` otherwise.
* Reject device-provisioning keys/bindings and invented hazard/dew-point thresholds across `manifest`, `thresholds`, `cases`, and `observed` (`sensor_fixture_provisions_device`, `sensor_fixture_invents_threshold`, non-disposable).
* Enforce `_is_generated_cohort(manifest)` across `_owner_approval_status`, `_live_gaps`, `fairness_evidence`, and `export_record` (`PC-003`), and require `not blockers and owner_approval_status != OWNER_APPROVAL_UNAPPROVED` before `fairness_evidence` can ever be `True` (`PC-001`).

#### Boundaries

* Included: `src/core/src/zava_forward/core/cohort_eval.py`.
* Excluded: Modifying `src/agents` or `src/api`.

#### Likely Targets

* `src/core/src/zava_forward/core/cohort_eval.py`.

#### Dependencies

* P01-T02.

#### Validation Expectations

* `test_cohort_eval.py`, `test_rai_threshold_live_approval_guard.py`, `test_heldout_eval.py`, and `src/agents/tests/test_cohort_*.py` pass 100%.

#### Completion Evidence

* Clean pass of all core and downstream agent cohort tests.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Update component documentation and run Focused validation

### Context

`src/core/README.md` (`C1`) currently states that `paired_equity` covers deterministic ranking only (`"AI task cohorts are not covered"`) and predates the #128 RAI cohort evaluation gates on `paired_equity` and `cohort_eval`. Repository instructions require updating directly related component documentation and passing Focused validation (`unittest`, `ruff check`, `ruff format --isolated --line-length 100 --check`, and bare `python3 -m mypy --cache-dir=/tmp/mypy-128` inside `src/core`).

### Intent

Update `src/core/README.md` concisely and execute all Focused validation checks cleanly.

### Boundaries

* Included: `src/core/README.md` and Focused validation execution.
* Excluded: Unrelated documentation or full local Docker/SQL gate (`rpi-checks.py --all` is not required for this focused pure-`src/core` slice).

### Likely Targets

* `src/core/README.md`: Update the `paired_equity` and `cohort_eval` subsections.

### Dependencies

* P02.

### Validation Expectations

* Unit tests in `src/core` (and downstream `src/agents` cohort callers) pass.
* `python3 -m ruff check` and `python3 -m ruff format --isolated --line-length 100 --check` pass on all modified Python files.
* Bare `python3 -m mypy --cache-dir=/tmp/mypy-128` inside `src/core` passes with 0 issues.

### Completion Evidence

* Recorded command outputs and zero-error exit codes in `.copilot-tracking/changes/2026-11-15/ai-128-cohort-ai-eval-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Update `src/core/README.md` and run Focused test, lint, format, and `mypy` checks

#### Context

Ensure documentation matches delivered code and governance boundaries (`fairness_evidence=False` on generated cohorts, human approvals remain external) and all static/runtime checks pass.

#### Intent

Edit `src/core/README.md` and run the Focused validation commands to verify readiness for `rpi-review`.

#### Boundaries

* Included: `src/core/README.md`; Focused validation checks on `src/core` (plus compatibility run on `src/agents` cohort tests).
* Excluded: Pushing or opening a PR.

#### Likely Targets

* `src/core/README.md`.

#### Dependencies

* P02-T01, P02-T02.

#### Validation Expectations

* Zero test failures, zero `ruff` findings, zero `mypy` errors, and no `.copilot-tracking/` strings in `src/` or `docs/`.

#### Completion Evidence

* Recorded command outputs in `.copilot-tracking/changes/2026-11-15/ai-128-cohort-ai-eval-changes.md`.

#### Unresolved Items

* None.
