---
description: "Primary evidence artifact for Issue #128 RAI Cohort Evaluation slice"
---
<!-- markdownlint-disable-file -->

# Task Research: ai-128-cohort-ai-eval

| Field              | Value                                                                    |
|--------------------|--------------------------------------------------------------------------|
| Date               | 2026-11-15                                                               |
| Researcher / agent | rpi-research (RPI Agent automatic session)                               |
| Status             | Completed                                                                |
| Artifact path      | .copilot-tracking/research/2026-11-15/ai-128-cohort-ai-eval-research.md  |

## Research Brief

* What to research: Remaining local RAI Cohort Evaluation slice of Issue #128 (`Accessibility, equity and journey ownership testing`, `Refs #128`) across `zava_forward.core.paired_equity`, `zava_forward.core.cohort_eval`, and `zava_forward.core.journey_register`, plus existing callers in `src/core`, `src/agents`, and `src/api`.
* Why it matters: Earlier PRs (#1174, #1211, #1222, #1481, #1735, #1751) added deterministic paired-cohort checks and human-review routing, leaving AI-task paired evaluation with transparent non-AI comparison, provider-versus-resident appointment history contrast, geography/archetype cohort dimensions, protected-characteristic minimum-necessary gating and non-inference checks, and full cohort/version/eligible/tested/abstained/failed/disposition retention incomplete.
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` in this continuous RPI loop on `feat/ai-128-cohort-ai-eval`.
* Scope: `src/core/src/zava_forward/core/paired_equity.py`, `src/core/src/zava_forward/core/cohort_eval.py`, `src/core/src/zava_forward/core/journey_register.py` (inspection and compatibility), `src/core/tests/test_paired_equity.py`, `src/core/tests/test_cohort_eval.py`, `src/core/tests/cohort_eval_fixture.py` (compatibility check), `src/core/README.md`, and downstream callers (`heldout_eval.py`, `cohort_ranking_eval.py`, `cohort_ai_eval.py`).
* Non-goals: Adding a separate governance service, live Azure OpenAI inference, IoT Hub device provisioning, inventing hazard/dew-point thresholds, claiming population fairness from synthetic cohorts, or granting human/legal/DPO/ranking-owner approvals.
* Criteria: All 8 RAI Cohort Acceptance Criteria of Issue #128 (`FR-054`, `AC-073`, `OQ-018`) satisfied and proven locally while preserving `fairness_evidence=False` and `activation_allowed=False` whenever independent human/policy/threshold approval is absent or any subgroup/sample/threshold check fails, without breaking existing `src/core` or `src/agents` callers.
* Requested outputs: Converged design recommendation with codebase evidence (`C#`), alternatives analysis, compatibility verification, and `Ready` planning readiness.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                   |
|----------------------------------|-------------------------------------------------------------------------|
| Research question(s)             | How should `paired_equity` and `cohort_eval` be extended cleanly in `src/core` to satisfy all 8 RAI Cohort Acceptance Criteria of Issue #128 while preserving existing callers and strict typing? |
| Codebase scope                   | `src/core/`, `src/agents/` (read-only caller verification), `docs/prds/`, `docs/brds/` |
| External scope                   | none (bounded internal repository contract task)                        |
| Initial internal candidate areas | `paired_equity.py`, `cohort_eval.py`, `journey_register.py`, `ranking.py`, `ai_registry.py`, `data_protection.py`, `stock.py` |
| Initial external candidate areas | none                                                                    |
| Research posture                 | focused                                                                 |
| Posture provenance               | caller-specified bounded local slice with named target modules and tests |
| Explicit limits / deadline       | Single continuous run; Focused validation tier; no push or PR           |
| Posture-specific completion basis | focused scope and materiality across all 8 Issue #128 RAI Cohort criteria |
| Edits allowed during research?   | no, research-only                                                       |
| Resolved evidence root           | `.copilot-tracking/`                                                    |
| Known constraints / excluded sources | Keep pure `zava_forward.core` modules free of store, clock, and network dependencies; preserve compatibility with `heldout_eval`, `cohort_ranking_eval`, and `cohort_ai_eval` |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                              | Scoped authority or output contract          | Selected / skipped reason      |
|---------------------|----------------------------------|---------------------------------------------------|----------------------------------------------|--------------------------------|
| Instruction         | `.github/copilot-instructions.md` | `applyTo: "**"` matches repository and tracking paths | AMA repository rules, focused validation tier, RAI/privacy boundaries, Markdown style | Selected: mandatory repo contract |
| Skill               | `rai-standards` / `privacy-standards` | Topic overlaps Responsible AI and lawful minimum-necessary fields | Advisory assessment reference only           | Skipped: PRD `FR-054`/`AC-073`/`OQ-018` and caller prompt specify exact local contract |
| Research specialist | `hve-core-all:rpi-researcher`    | Host-registered general research worker           | Independent lane investigation               | Skipped (inline): tightly coupled 3-module internal inspection fits <=10 direct reads |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                       | Answers / unanswered      | Resulting decision or selected further research    |
|------------------|-------------------------------------------------------------|---------------------------|----------------------------------------------------|
| Intake           | Non-interactive continuous execution with explicit 8-point acceptance criteria and target files | No interaction needed     | Proceed in focused convergence mode across `paired_equity.py` and `cohort_eval.py` |
| Direction change | None                                                        | Unchanged                 | Maintain pure `src/core` boundary and focused test/lint/mypy validation |
| Convergence      | Cycle 1 Wider, Deeper, and Contrarian waves completed       | No blockers or questions  | Selected unified pure-core extension of `paired_equity.py` and `cohort_eval.py` without touching `journey_register.py`; `Planning Readiness: Ready` |

## Scope and Success Criteria

* Scope: Pure offline RAI cohort evaluation and paired constructed-cohort checks in `src/core/src/zava_forward/core/paired_equity.py` and `src/core/src/zava_forward/core/cohort_eval.py`, their unit tests, and `src/core/README.md`.
* Assumptions:
  * Existing `src/agents` callers (`cohort_ranking_eval.py`, `cohort_ai_eval.py`, `ai_eval.py`) and `src/core` callers (`heldout_eval.py`, `test_rai_threshold_live_approval_guard.py`) must remain backward-compatible.
  * `journey_register.py` already covers journey ownership and `human_review_route` (verify whether any small extension is needed for provider-vs-resident appointment history or non-response).
* Success criteria:
  * Every research question is answered with exact `path:line` evidence (`C#`).
  * All 8 RAI Cohort Acceptance Criteria map to concrete module gaps and verified invariants.
  * Compatibility and contrarian edge cases (averaging bypasses, abstention accounting, protected-characteristic leakage, inference of vulnerability/refusal, sensor provisioning/threshold invention, ranking policy ownership/hash/order approval) are stress-tested.

## Task Research Requests

* Explicit requests: Inspect `paired_equity.py`, `cohort_eval.py`, `journey_register.py` and their tests; identify and close gaps across all 8 RAI Cohort Acceptance Criteria of Issue #128 (`Refs #128`).
* Inferred research questions: Q1-Q6 below.
* Caller constraints and non-goals: Do not stop between phases; do not push or open a PR; keep `fairness_evidence=False` and `activation_allowed=False` whenever independent human/policy/threshold approval is absent or any subgroup/sample/threshold check fails.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint  | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|-----------------------|----------------------|---------------------------------------------------|
| narrow                                                   | Pure `src/core` RAI Cohort Evaluation slice (`paired_equity`, `cohort_eval`, `journey_register` check) + focused tests | Caller prompt / Intake | Keep scope inside `src/core` and `src/core/README.md` while verifying downstream caller compatibility |
| exclude                                                  | No device provisioning, no invented hazard/dew-point thresholds, no population fairness claims, no live approvals | Caller prompt / Issue #128 | Enforce explicit rejection/guard checks in code and tests |

## Research Questions

|  # | Sub-question     | Type (depth / breadth / straightforward) | Priority  | Status                    |
|---:|------------------|------------------------------------------|-----------|---------------------------|
| Q1 | What did earlier PRs (#1174, #1481, #1735, #1751) deliver, and what remains missing across the 8 RAI Cohort criteria? | breadth | H | answered (C1-C6) |
| Q2 | How should `paired_equity.py` predeclare independent contrasts for source/sensor completeness (including missing/declined and no device/threshold invention), accessibility/contact needs, provider-vs-resident appointment history (and non-response), and optional approved geography/archetype while holding relevant facts constant? | depth | H | answered (C1, C3, C8, C10) |
| Q3 | How should `paired_equity.py` and `cohort_eval.py` evaluate both deterministic prioritisation and AI tasks, preserve named ranking-policy ownership and hash/order approval (`ranking.signoff_problems` / `rule_order_hash` / `policy_hash`), check prohibited inferences (vulnerability, refusal, protected characteristics), and provide transparent non-AI comparison? | depth | H | answered (C1, C2, C4, C5, C11) |
| Q4 | What fields are missing in `cohort_eval.py` to retain full cohort/version definitions, `eligible`, `tested`, `abstained`, and `failed` counts, sufficiency, subgroup errors/exclusions, review burden, Wilson uncertainty, and human disposition without breaking existing callers? | depth | H | answered (C2, C7, C12) |
| Q5 | How should protected-characteristic minimum-necessary gating and geography/archetype approval gating work in `cohort_eval.py` and `paired_equity.py`? | depth | H | answered (C2, C9) |
| Q6 | Under what exact conditions could `activation_allowed` or `fairness_evidence` currently slip to `True` when independent human/policy/threshold approval is absent, and how must that be tightened compatibly? | depth | H | answered (C2, C6) |

## Prior Knowledge Gate

* Existing artifacts reviewed: `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/reference/research/evaluation/cohort-evaluation-review-pack.md`, `docs/reference/research/ux/equity-journey-test-plan.md`, `src/core/README.md`.
* Reused (verified) findings:
  * `cohort_eval.py` OQ-018 owner-approval and `live_activation_allowed` contract from #1751 (`03a680f5e`) must remain intact for `src/agents` (`cohort_ranking_eval.py`, `cohort_ai_eval.py`, `ai_eval.py`) and `src/api` (`test_ai_tasks.py`).
  * Commit `20af48b5e` (#1735) modifies `journey_register.py` on sibling stacked branches (`feat/demo-233-same-home-tensions-0825`); calling `journey_register.human_review_route(case)` with its single-argument signature without editing `journey_register.py` preserves clean merge compatibility across stacked branches.
* Superseded / stale: `src/core/README.md:1042` states `"AI task cohorts are not covered"` in `paired_equity`, which this slice supersedes by adding pure AI-task paired evaluation and transparent non-AI comparison while keeping human/policy/threshold approvals ungranted.

## Executed Research Cycles

### Cycle 1

#### Wave 1: Wider

* Scope investigated: `paired_equity.py`, `cohort_eval.py`, `journey_register.py`, `ranking.py`, `rai_release.py`, `ai_registry.py`, `data_protection.py`, `sensor_view.py`, `synthetic/device_provision.py`, `heldout_eval.py`, `docs/reference/research/ux/equity-journey-test-plan.md`, and `docs/reference/research/evaluation/cohort-evaluation-review-pack.md`.
* Breadth findings:
  * `paired_equity.py` (`C1`) checks only 4 single-profile deterministic contrasts (`source_completeness`, `sensor_completeness` present->declined, `support_or_contact_need` support+adjustment bundle, `appointment_history` confirmed->prior_no_access) with no AI-task runner, no ranking-policy hash/order/owner preservation, no provider-vs-resident appointment contrast or missing-sensor/non-response service-level checks, no optional geography/archetype dimensions, no protected-characteristic approval gate, and no sensor anti-provisioning/threshold-invention check.
  * `cohort_eval.py` (`C2`) supports 4 outcomes (`ranked`, `deprioritised`, `excluded`, `review`), lacks `"abstained"`, omits explicit `eligible`, `tested`, `abstained`, and `failed` fields per subgroup and overall, omits retained `cohort_definitions` and `version_definitions`, lacks ranking-policy ownership/hash/rule-order checks and transparent non-AI baseline comparison, lacks protected-characteristic minimum-necessary gating and geography/archetype context-approval gating, lacks prohibited-inference and sensor-fixture guards, and allows `fairness_evidence=True` on non-synthetic manifests even when `threshold_exceeded` or `unjustified_exclusion` blockers exist because `MEASUREMENT_BLOCKERS` excludes them (`C6`).
  * `journey_register.py` (`C3`) already routes missing source/sensor, unknown priority support, and `INCOMPLETE_APPOINTMENT` (`unconfirmed`, `no_response`, `prior_no_access`, `unknown`) to `human_review` with `rank_effect == "none"`.

#### Wave 2: Deeper

* Detailed contract trace:
  * **Predeclared contrasts and backward compatibility (`C1`, `C7`)**: `test_paired_equity.py` asserts exact error codes `wrong_contrast` on partial support bundles (`priority_support` changed without `adjustment`) and `confounded` when an extra nested attribute (`resident.contact_preference`) is mutated alongside a declared bundle. Organizing `PREDECLARED_CONTRASTS` as named non-overlapping contrast profiles per dimension (with predeclared independent expectations `rank_relation`, `service_level`, `review_route`, `ai_outcome`) and matching exact field-key sets first, then superset-key sets (`confounded`), preserves every existing test while adding missing sensor (`present -> missing`), contact-need (`digital -> assisted_non_digital`), provider-versus-resident appointment history (`provider_cancelled -> resident_rescheduled` and `provider_cancelled -> no_response`), non-response (`confirmed -> no_response`), and optional approved `geography` and `archetype` contrasts.
  * **Deterministic ranking policy & transparent non-AI comparison (`C4`, `C5`, `C11`)**: `ranking.py` exposes `CURRENT`, `policy_hash(policy)`, `rule_order_hash(policy)`, `signoff_problems(policy)`, and `is_signed(policy)`. Note `ranking.CURRENT["owner"]` is `"to be named"`, so `is_signed(ranking.CURRENT)` is `False` while `policy_hash(ranking.CURRENT) == ranking.CURRENT["content_hash"]` is `True`. Recording `ranking_policy` provenance in both `paired_equity` and `cohort_eval`, blocking on tampered `content_hash` / malformed rules / unsigned policy when policy approval is required, and computing a side-by-side `non_ai_comparison` (deterministic rank, review route, and subgroup rates vs AI task rank/outcome/service/abstention/fallback) satisfies Criterion 2 without mutating deterministic priority.
  * **Non-demotion of missing/declined sensors & non-response + prohibited inference detection (`C5`, `C9`)**: Neither missing/declined sensors nor resident non-response may lower rank or `service_level`, and neither deterministic adapters nor AI task outputs may infer `vulnerability`, `refusal` (e.g., treating sensor decline or appointment silence as works refusal), or UK Equality Act / UK GDPR special-category protected characteristics (`PROTECTED_CHARACTERISTIC_FIELDS`).
  * **Retained definitions, counts, sufficiency, and uncertainty (`C2`, `C12`)**: Adding `"abstained"` to `OUTCOMES`, retaining `cohort_definitions` and `version_definitions`, and emitting `eligible`, `tested`, `abstained`, and `failed` alongside existing `n`, `missing`, `errors`, `excluded`, `deprioritised`, `review`, `defects`, `error_rate`, `exclusion_rate`, `abstention_rate`, `review_burden`, `error_interval` (`wilson`), and `sufficient` preserves 100% compatibility with `cohort_ranking_eval.py`, `cohort_ai_eval.py`, `ai_eval.py`, and `test_ai_tasks.py`.
  * **Sensor completeness fixture guard (`C8`, `C10`)**: `sensor_view.NOT_RETAINED = ("dew_point_c", "mould_risk_index")` and `synthetic/device_provision.py` establish exact forbidden keys. Rejecting device-provisioning fields (`device_id`, `iot_hub`, `connection_string`, `sas_token`, `symmetric_key`, `x509`, `provision_device`, `SYN-` device bindings) and invented hazard/dew-point thresholds (`dew_point*`, `mould_risk_index`, `hazard_threshold`, `damp_threshold`, `rh_hazard_threshold`) fail-closed in both modules guarantees Criterion 8.

#### Wave 3: Contrarian

* Challenges and counter-evidence tested:
  1. *Could tightening `fairness_evidence` and `activation_allowed` break existing offline tests in `test_cohort_eval.py` and `test_rai_threshold_live_approval_guard.py`?*
     * Checked `test_cohort_eval.py:14` (`test_clean_run_is_ready_but_never_fairness_evidence`), `test_cohort_eval.py:246` (`test_unmeasured_non_synthetic_run_is_not_fairness_evidence`), and `test_cohort_eval.py:330` (`test_dated_real_human_owner_approval_requires_non_synthetic_and_bound_lawful_fields`) (`C7`).
     * Finding: In `cohort_eval.py:492`, `fairness_evidence` previously checked only `MEASUREMENT_BLOCKERS`, which let `fairness_evidence=True` slip through on `synthetic=False` even when `threshold_exceeded`, `unjustified_exclusion`, or `seeded_defect_undetected` fired! Tightening `fairness_evidence` to require `not blockers` (zero blockers before disposition), `not generated_cohort` (`not synthetic` and `cohort_origin` not `"generated"`/`"constructed"`), `_thresholds_approved(manifest)`, `fields_valid`, and all new policy/protected-field/context gates keeps both legitimate non-synthetic clean approved tests passing while closing the subgroup-failure `fairness_evidence` loophole completely.
  2. *Could a failing small subgroup be masked by a large passing cohort or high abstentions?*
     * Verified: Evaluating every `(dimension, cohort_label)` independently (`aggregation_rule: "per_cohort_unaveraged"`), blocking on `tested < min_sample` (`insufficient_sample`), counting unexpected abstentions as errors (`actual != expected`), and optionally gating `max_abstention_rate` (plus requiring non-abstained `usable_tested >= min_sample` when substantive decisions are expected and `require_usable_sample` / non-abstention expectations hold—Wait: if `expected != "abstained"` and `actual == "abstained"`, `actual != expected` ALREADY counts as an error in `errors`/`failed`, breaching `max_error_rate`! And if `tested < min_sample`, `insufficient_sample` blocks non-disposably!).
  3. *Could human `disposition` wave through unapproved protected characteristics, unapproved geography/archetype, unapproved ranking policy, prohibited inferences, or sensor provisioning violations?*
     * Verified: Keep `DISPOSABLE` strictly limited to threshold/seeded-defect triage (`{"seeded_defect_unexpected", "threshold_exceeded", "unjustified_exclusion"}`) so structural, governance, privacy, policy-signoff, sample-sufficiency, prohibited-inference, non-AI-baseline, and sensor-guard blockers can NEVER be cleared by `disposition`.

## Codebase Evidence Register

| ID  | Path and lines | Verified fact |
|-----|----------------|---------------|
| C1  | `src/core/src/zava_forward/core/paired_equity.py:20-167` | Current `paired_equity` checks 4 fixed deterministic contrasts only, lacks AI task evaluation, ranking-policy provenance, provider-vs-resident appointment contrast, optional geography/archetype, protected-field gating, prohibited-inference checks, and sensor-fixture guards. |
| C2  | `src/core/src/zava_forward/core/cohort_eval.py:20-568` | Current `cohort_eval` lacks `"abstained"` outcome, explicit `eligible`/`tested`/`abstained`/`failed` counts, retained `cohort_definitions`/`version_definitions`, ranking-policy sign-off & non-AI comparison, protected-characteristic minimum-necessary gate, context-dimension approval gate, prohibited-inference gate, and sensor-fixture guard. |
| C3  | `src/core/src/zava_forward/core/journey_register.py:37-127` | `human_review_route(case)` routes missing source/sensor, unknown priority support, and `INCOMPLETE_APPOINTMENT` (`unconfirmed`, `no_response`, `prior_no_access`, `unknown`) to `human_review` with `rank_effect == "none"`. |
| C4  | `src/core/src/zava_forward/core/ranking.py:25-40,148-177` | `ranking.CURRENT` is unsigned (`owner: "to be named"`), and `policy_hash`, `rule_order_hash`, `signoff_problems`, and `is_signed` verify policy integrity and human rule-order ownership. |
| C5  | `src/core/src/zava_forward/core/ai_registry.py:28-55` | Registered AI capabilities forbid mutating deterministic ranking and forbid `"inferring refusal or vulnerability from silence or missing sensors"`. |
| C6  | `src/core/src/zava_forward/core/cohort_eval.py:38-45,492-498` | `fairness_evidence` checked only `MEASUREMENT_BLOCKERS`, allowing `fairness_evidence=True` on non-synthetic runs even when `threshold_exceeded` or `unjustified_exclusion` blockers fired. |
| C7  | `src/core/tests/test_paired_equity.py:58-240` and `src/core/tests/test_cohort_eval.py:14-420` | Existing unit tests pin exact `wrong_contrast`/`confounded` comparability behaviour in `paired_equity` and OQ-018 offline vs live approval invariants in `cohort_eval`. |
| C8  | `src/core/src/zava_forward/core/sensor_view.py:46` | `NOT_RETAINED = ("dew_point_c", "mould_risk_index")` confirms dew-point and mould-risk indices are never retained or invented. |
| C9  | `src/core/src/zava_forward/core/data_protection.py:159` | `SPECIAL_FIELDS` identifies special-category attributes (`health`, `disability`, `ethnicity`, `religion`, `safeguarding`, `vulnerability`, `notes`) requiring strict lawful handling. |
| C10 | `src/core/src/zava_forward/core/synthetic/device_provision.py:18-58` | Synthetic `SYN-` device provisioning belongs strictly to `device_provision` / `device_identity` (#185) and must never occur inside sensor-completeness equity fixtures. |
| C11 | `src/core/src/zava_forward/core/rai_release.py:48-77` | `digest`, `named`, and `named_human` provide pure canonical SHA-256 binding and human-approver validation rejecting system/agent/placeholder attributions. |
| C12 | `src/agents/src/zava_forward/agents/cohort_ai_eval.py:1-95` and `cohort_ranking_eval.py:1-95` | Downstream `src/agents` callers read `dimensions[dim]["cohorts"][label]["n"|"missing"|"errors"|"review"|"sufficient"]` and validate exports through `cohort_eval.export_record`. |

## Parent Synthesis

### Accepted Recommendations

1. **Extend `paired_equity.py` (`RECORD_VERSION = "paired-cohort-equity-v1"`, preserving existing callers)**:
   * Add `PREDECLARED_CONTRASTS` and `predeclared_cohorts(...)` covering predeclared independent expectations across `source_completeness` (`missing`, `partial`, `stale`), `sensor_completeness` (`declined`, `missing`), `support_or_contact_need` (`accessibility_adjustment` bundle, `contact_channel_need`), `appointment_history` (`prior_no_access`, `provider_vs_resident`, `provider_vs_resident_no_response`, `non_response`), and optional `OPTIONAL_DIMENSIONS = ("geography", "archetype")` gated by named-human relevance + scope approval (`context_approvals`).
   * Preserve `DIMENSIONS` and `CONTRASTS` and exact `_comparability` semantics (`wrong_contrast` vs `confounded` vs `no_contrast` vs `contradicts_predeclared_expectation`).
   * Support evaluating deterministic `rank` AND optional `ai_task` with `policy` verification (`ranking.policy_hash`, `ranking.rule_order_hash`, `ranking.signoff_problems`, `ranking.is_signed`), side-by-side `non_ai_comparison` (verifying deterministic ranking is unmutated and comparing deterministic rank/route vs AI rank/outcome/service/abstention), service-lowering detection on missing/declined sensors and non-response, prohibited inference detection (`vulnerability`, `refusal`, protected characteristics), protected-characteristic minimum-necessary approval gating (`protected_fields_approval`), sensor-fixture anti-provisioning and anti-threshold-invention checks, retained `cohort_definitions` & `version_definitions`, `eligible`/`tested`/`abstained`/`failed` counts, and optional `disposition` retention while keeping `fairness_evidence=False` on generated cohorts and `activation_allowed=False` whenever independent human/policy/threshold/expectation approval is absent or any check fails.
2. **Extend `cohort_eval.py` (preserving 100% compatibility with `src/core`, `src/agents`, and `src/api`)**:
   * Add `"abstained"` to `OUTCOMES`; retain `cohort_definitions` and `version_definitions`; emit `eligible`, `tested`, `abstained`, and `failed` counts per subgroup and in top-level `counts` (reconciling `eligible == tested + missing` across every dimension while preserving `n` and `errors`).
   * Verify optional `ranking_policy` ownership, `content_hash`, and `rule_order_hash` sign-off (`unapproved_ranking_policy` / `invalid_ranking_policy_hash`), and compute `non_ai_comparison` when `non_ai_observed` (or `manifest["non_ai_baseline"]`) is provided or required (`task_kind == "ai_task"`), blocking if missing or if AI introduces unjustified exclusions/deprioritisations over the deterministic non-AI baseline.
   * Detect lowered service on missing/declined sensors or non-response (`service_lowered`) and prohibited inferences of `vulnerability`, `refusal`, or protected characteristics (`prohibited_inference`) as non-disposable errors and blockers.
   * Gate any protected-characteristic field in `cohorts`, `lawful_analysis_fields`, or cases behind digest-bound `protected_characteristic_approval` (real named human DPO/lawful-basis owner, `lawful_basis`, `minimum_necessary_justification`, exact `approved_fields`, valid `approved_at`); otherwise block with non-disposable `unapproved_protected_characteristic`.
   * Gate `"geography"` and `"archetype"` dimensions in `cohorts` behind digest-bound `context_dimension_approvals` (`approved_by` named human, `relevant: True`, non-empty `rationale`); otherwise block with non-disposable `unapproved_context_dimension`.
   * Reject device-provisioning payloads and invented hazard/dew-point thresholds in manifests, thresholds, cases, or observations (`sensor_fixture_provisions_device` / `sensor_fixture_invents_threshold`).
   * Tighten `fairness_evidence` so any blocker (`bool(blockers)`), any generated/constructed/synthetic cohort (`generated_cohort`), or any missing policy/threshold/field approval forces `fairness_evidence = False` (`population_fairness_established = False` on generated cohorts).
3. **Leave `journey_register.py` unchanged**:
   * `journey_register.human_review_route(case)` already satisfies `paired_equity`'s 1-argument contract and avoids merge conflicts with sibling stacked branch commit `20af48b5e` (#1735).

### Alternatives Considered and Rejected

* **Alternative A: Create a third module `ai_cohort_eval.py` instead of extending `paired_equity.py` and `cohort_eval.py`**: Rejected because the caller explicitly scoped target modules and tests to `paired_equity.py` / `test_paired_equity.py` and `cohort_eval.py` / `test_cohort_eval.py`, and duplicating manifest/digest/OQ-018 logic would split governance invariants across modules.
* **Alternative B: Modify `journey_register.py` to add appointment-history constants**: Rejected because `journey_register.py` already handles `no_response` and `prior_no_access` with `rank_effect == "none"`, and sibling branch #1735 (`20af48b5e`) edits `journey_register.py` extensively; keeping changes in `paired_equity.py`, `cohort_eval.py`, their tests, and `src/core/README.md` eliminates stacked-branch conflict risk.

### Risks, Open Items, and Readiness

* **Risks mitigated**: Strict `mypy` typing in `src/core`; exact `ruff` 100-column formatting; preserving `export_record` invariants used by `src/agents` and `src/api`.
* **Further research needed**: None; Cycle 1 saturated all internal contracts and caller surfaces.
* **Research disposition**: `executed`
* **Planning Readiness**: `Ready`

