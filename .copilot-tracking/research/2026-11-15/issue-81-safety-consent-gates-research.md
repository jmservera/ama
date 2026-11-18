<!-- markdownlint-disable-file -->

# Task Research: issue-81-safety-consent-gates

| Field              | Value                                                                               |
|--------------------|-------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                          |
| Researcher / agent | rpi-research (RPI Agent automatic loop)                                             |
| Status             | Complete                                                                            |
| Artifact path      | .copilot-tracking/research/2026-11-15/issue-81-safety-consent-gates-research.md     |

## Research Brief

* What to research: How Zava Forward `src/core` represents controlled lifecycle transitions, hazard/safety holds and referrals (`RULE-001`, `FR-008`), resident consent/agreement and authorised exceptions (`RULE-002`, `FR-011`), and seeded/synthetic exercise scenarios (`synthetic/`, `store.py`, `workflows.py`, `learning_test_bundles.py`), so we can design a deterministic exercise-scenario gate verifier proving both exercise-scenario Acceptance Criteria of `#81`.
* Why it matters: Issue `#81` ("Epic: Safety, resident consent and controlled lifecycle") has two unticked exercise-scenario Acceptance Criteria requiring deterministic proof across all exercise scenarios that (1) no controlled progression occurs with unresolved safety evidence, and (2) no work starts without valid resident agreement or an explicitly authorised exception.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` phases in this automatic RPI session, plus `src/core` maintainers reviewing `PR` evidence for `#81`.
* Scope: `src/core/src/zava_forward/core/` (gates, hazard, resident_decisions, workflows, store, procurement/job_pack/appointments/forms/home_case, synthetic scenarios, learning_test_bundles), `src/core/tests/`, `src/core/README.md`, and governing BRD/PRD sections (`RULE-001`, `RULE-002`, `FR-008` to `FR-015`).
* Non-goals: Closing epic `#81` overall (`#440` stabilization checkpoint and child-issue closure remain separate epic criteria), modifying `src/api` web screens, pushing to remote, or claiming legal/live operational sign-off for exercise rules.
* Criteria: Every controlled progression path, safety-hold representation, resident-agreement/authorised-exception contract, and exercise-scenario source in `src/core` is mapped with exact `path:line` evidence (`C#`), contrarian bypass vectors are tested against code reality, and one deterministic verifier architecture is converged upon.
* Requested outputs: Converged design recommendation for `safety_consent_exercise_gate.py` (or equivalent `src/core` verifier), comprehensive test coverage plan for `test_safety_consent_exercise_scenarios_81.py`, and `src/core/README.md` documentation scope.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                                                              |
|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | Q1-Q5 covering exercise scenario inventories, controlled progression transitions, unresolved safety evidence semantics, resident agreement/exception semantics, and bypass edge cases |
| Codebase scope                       | `src/core/src/zava_forward/core/`, `src/core/tests/`, `src/core/README.md`, `docs/brds/agentic-retrofit-programme-brd.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md` |
| External scope                       | none (repository-internal requirement, domain rules, and codebase contracts)                                                                                       |
| Initial internal candidate areas     | `src/core/src/zava_forward/core/gates.py`, `hazard.py`, `resident_decisions.py`, `workflows.py`, `store.py`, `synthetic/scenario_manifest.py`, `learning_test_bundles.py`, `src/core/README.md` |
| Initial external candidate areas     | none                                                                                                                                                               |
| Research posture                     | balanced                                                                                                                                                           |
| Posture provenance                   | default (bounded internal task with named source targets, plus adjacent lifecycle/scenario modules across `src/core` that could hold exercise cases or progression entrypoints) |
| Explicit limits / deadline           | Focused validation tier (`ruff check`, `mypy`, `unittest` in `src/core`); non-interactive session; do not push                                                     |
| Posture-specific completion basis    | balanced scope coverage and adequate evidence across all exercise scenario sources and controlled lifecycle/work-start entrypoints                                  |
| Edits allowed during research?       | no, research-only                                                                                                                                                  |
| Resolved evidence root               | `.copilot-tracking/` default                                                                                                                                       |
| Known constraints / excluded sources | Never read private datasets outside repo fixtures; preserve exercise-fixture rule disclaimers (`Unreviewed exercise rule`); do not reference `.copilot-tracking/` in code or commits |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                                      | Match and provenance                                              | Scoped authority or output contract                                      | Selected / skipped reason                                                                 |
|---------------------|------------------------------------------------|-------------------------------------------------------------------|--------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` (AMA repo)   | `applyTo: "**"` matches all repository and tracking paths         | Enforces `src/core` test/mypy/ruff rules, BRD/PRD authority boundaries, and Markdown style | Selected: mandatory repository guidance                                                   |
| Skill               | `rpi-research`                                 | Direct phase skill for Research                                   | Primary research artifact and three-wave cycle protocol                  | Selected: active RPI phase skill                                                          |
| Skill               | `python-foundational`                          | Semantic match for Python package design/testing                  | Optional Python conventions                                              | Skipped: existing `src/core` module conventions are directly inspectable and authoritative |
| Research specialist | `hve-core-all:rpi-researcher`                  | Host-registered general research lane worker                      | Writes subagent lane markdown under `.copilot-tracking/research/subagents/` | Skipped (inline preferred): tightly coupled `src/core` modules read faster and more accurately inline |
| Research specialist | `Housing Building Safety Lead` / `Housing Resident Engagement Lead` | Host-registered company profile role agents | Exploratory company-perspective Q&A                                      | Skipped: task verifies deterministic executable `src/core` contracts rather than eliciting new requirements |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                     | Answers / unanswered | Resulting decision or selected further research                                                       |
|------------------|---------------------------------------------------------------------------------------------------------------------------|----------------------|-------------------------------------------------------------------------------------------------------|
| Intake           | Non-interactive session with explicit scope, files to inspect, target branch, validation tier, and commit/no-push instructions | N/A (non-interactive) | Proceed with `balanced` convergence research across `src/core` lifecycle, safety, consent, and scenarios |
| Direction change | None required during Cycle 1                                                                                              | N/A                  | Scope remained bounded to `src/core` exercise-scenario gates and tests                                |
| Convergence      | Cycle 1 answered Q1-Q5 with code-backed `C1`-`C18` evidence and uncovered three fail-closed hardening opportunities       | N/A (automatic mode) | Converged on `safety_consent_exercise_gate.py` plus fail-closed `gates.py`, `store.py`, and `resident_decisions.py` hardening |

## Scope and Success Criteria

* Scope: Inspect `src/core` lifecycle/workflow transitions, safety/hazard holds, resident consent/decisions and authorised exceptions, and all exercise scenario definitions (`store.py` seed cases, `synthetic/` scenario manifest & fixtures, `journey_register.py` / `resident_showcase.py` / `learning_test_bundles.py` where applicable) to specify a complete deterministic verifier for `#81`.
* Assumptions:
  * `lifecycle.py`, `safety.py`, and `consent.py` named as examples in the prompt may map to `workflows.py` / `home_case.py` / `gates.py`, `hazard.py`, and `resident_decisions.py` in `src/core` (to verify via exact file inventory).
  * Exercise scenarios may span both seeded case fixtures (`store.py` / `seed_merge.py` / `factory.py`) and synthetic scenario manifests (`synthetic/scenario_manifest.py` / `learning_test_bundles.py`); we must verify every exercise scenario collection in `src/core`.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs and one converged recommendation is selected.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  1. Inspect `lifecycle.py` (or actual lifecycle modules), `safety.py` (`hazard.py` / `gates.py`), `consent.py` (`resident_decisions.py` / stage gates), and exercise scenarios in `synthetic/` / `learning_test_bundles.py` (note prompt spelled `learning_bundles.py` and `lifecycle.py`/`safety.py`/`consent.py`).
  2. Design a deterministic exercise-scenario gate verifier (e.g., `verify_exercise_safety_and_consent_gates` in `src/core/src/zava_forward/core/safety_consent_exercise_gate.py`) across all exercise scenarios proving both `#81` invariants (`RULE-001`/`FR-008` safety refusal on unresolved safety evidence; `RULE-002`/`FR-011` consent refusal on work start without valid active resident agreement or authorised exception).
  3. Plan `src/core/tests/test_safety_consent_exercise_scenarios_81.py` and `src/core/README.md` update.
* Inferred research questions:
  * Which exact modules own controlled state progression and work-start transitions in `src/core`?
  * What constitutes "all exercise scenarios" in `src/core` (seed cases, synthetic scenario manifest, showcase/journey scenarios, learning bundles)?
  * How are `RULE-001`/`FR-008` and `RULE-002`/`FR-011` represented in existing store/workflow/gate APIs, and do any progression or work-start methods currently allow bypasses or lack a unified exercise-scenario audit?
* Caller constraints and non-goals: Focused validation tier in `src/core`; commit locally with Copilot trailer; do NOT push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                                  |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|------------------------------------------------------------------------------------|
| narrow                                                   | Prove the two exercise-scenario Acceptance Criteria of `#81` in `src/core` with focused validation tier | Caller prompt       | Scopes implementation to `src/core` verifier, unit/integration test, and README    |
| exclude                                                  | Do not push to remote; leave a clean frozen HEAD                                                        | Caller prompt       | Restricts final git action to local commit verification                            |

## Research Questions

|  # | Sub-question                                                                                                                                      | Type            | Priority | Status |
|---:|---------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|--------|
| Q1 | Which modules in `src/core` implement controlled lifecycle progression, stage transitions, contractor work-order activation, and work start?       | breadth         | H        | answered |
| Q2 | How is unresolved safety evidence (`hazard`, open safety referral, unreleased hold, missing/unknown safety state) represented and gated (`RULE-001` / `FR-008`)? | depth           | H        | answered |
| Q3 | How are valid active resident agreements and explicitly authorised exceptions represented and gated before starting work (`RULE-002` / `FR-011`)? | depth           | H        | answered |
| Q4 | What is the complete inventory of "exercise scenarios" in `src/core` (seeded cases, synthetic scenario manifest, showcase/journey fixtures, learning bundles)? | breadth         | H        | answered |
| Q5 | Are there any bypass paths, missing gate checks, edge states (`unknown`, expired/withdrawn/scope-changed consent, self-released safety hold), or scenario gaps that would violate either `#81` invariant? | depth           | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: Issue `#81` body via `gh issue view 81`; `docs/case_study_48_original.md`; `docs/case_study_48_addendum.md`; `src/core/src/zava_forward/core/gates.py`; `hazard.py`; `learning_test_bundles.py`; `.copilot-tracking/rpi-sessions/2026-11-03/issue-82-r1-state.json`.
* Reused (verified) findings:
  * `gates.py` already defines `GateRule`, `GateResult`, `PASS`/`FAIL`/`UNKNOWN`, `safety_release_gate`, `booking_gates` (`BOOKING_RULES["safety"]` citing `RULE-001; PRD FR-008` and `BOOKING_RULES["resident"]` citing `RULE-002; PRD FR-008`).
  * `learning_test_bundles.py` defines constructed-case effort comparison bundles (`BUNDLES`), including `story-once` with zero-measure `authority_or_consent_breaches`.
  * Exact filenames in `src/core/src/zava_forward/core/` do not include `lifecycle.py`, `safety.py`, or `consent.py`; instead `src/core` has `gates.py`, `hazard.py`, `resident_decisions.py`, `workflows.py`, `home_case.py`, `store.py`, `procurement.py`, `job_pack.py`, `appointments.py`, etc.
* Superseded / stale: Issue `#81` body mentions legacy `mvp/` directory, which was retired at cut-over in favour of `src/core` (`docs/case_study_48_addendum.md` and `.github/copilot-instructions.md`).

## Research Cycle Log

### Cycle 1

* Active direction controls: Caller scope narrowing to `#81` exercise-scenario invariants in `src/core`; no remote push.
* Active research posture and completion basis: `balanced`; cover all `src/core` exercise scenario definitions and controlled lifecycle/work-start entrypoints with code-backed `C#` evidence.
* Explicit limits or deadline effect: Focused validation tier in `src/core`; inline investigation keeps context tight and exact.

#### Wave 1: Wider

* Mapped the prompt's illustrative module names (`lifecycle.py`, `safety.py`, `consent.py`, `learning_bundles.py`) to the authoritative `src/core` modules:
  * Controlled lifecycle and stage/work-order gates: `gates.py`, `store.py`, `procurement.py`, `appointments.py`, `signoffs.py`, `quality.py`, `workflows.py`, `buildings.py`, and `sqlstore.py` (`C1`–`C6`).
  * Safety holds, hazard referrals, and standalone safeguarding items: `hazard.py`, `workflows.py`, `taskqueues.py`, and `gates.py` (`C1`, `C2`, `C7`, `C8`).
  * Resident consent, representative authority, and scoped exceptions: `resident_decisions.py`, `resident_journey_design.py`, and `data_protection.py` (`C9`–`C11`).
  * Exercise scenario suites and learning bundles: `learning_test_bundles.py`, `synthetic/resident_preview_fixture.py`, `synthetic/sensor_scenarios.py`, `synthetic/scale_fixture.py`, `scenario_manifest.py`, and constructed workbench fixture `src/core/tests/dataset.py` (`C12`–`C16`).
* Traced issue `#81` Acceptance Criteria directly to BRD business goals `BG-003` ("Controlled progressions with unresolved safety evidence" -> target `Zero`) and `BG-005` ("Work started without valid agreement or authorised exception" -> target `Zero`), governed by `BRD FR-001`, `BRD FR-002`, `BRD RULE-001`, `BRD RULE-002`, `BRD RULE-003`, `BRD FR-008`, `BRD FR-011` (`AC-015`), `BRD FR-014` (`AC-018`), and `PRD FR-008`, `PRD FR-014`, `PRD FR-015`, `PRD FR-045`, `PRD FR-046` (`C17`, `C18`).

#### Wave 2: Deeper

* **Q1 — Controlled progression and work-start entrypoints**:
  1. `Store.advance(user, case_id)` (`Final checks before ordering` -> `Install booked`, `store.py:1022-1068`): enforces `gate_reasons`, `buildings.blockers`, `require_safety_clear`, `require_resident_clear`, `require_booking_gates` (`gates.booking_gates` + `gates.evidence_gate`), and `require_booked_capacity` (`C2`).
  2. `SignoffMixin.technical_action(user, case_id, {"action": "signoff_give", ...})` (`signoffs.py:92-120`): calls `self.require_safety_clear(c)` before recording any technical or Retrofit Coordinator sign-off (`C5`).
  3. `ProcurementMixin.issue_work_order(user, pid, case_id, scope, resident_bindings)` (`procurement.py:402-430`): enforces `require_safety_clear(c)`, `require_resident_clear(c, bindings)`, and `require_building_clear(c, pid)` (`C3`).
  4. `ProcurementMixin.reissue_work_order(user, wid, scope, reason, resident_bindings)` (`procurement.py:446-460`): enforces `require_safety_clear`, `require_resident_clear`, and `require_building_clear` (`C3`).
  5. `ProcurementMixin.record_wo_appointment(user, wid, "Booked", when)` (`procurement.py:462-488`, contractor work-order activation `Issued` -> `Appointed`): enforces `require_appointment_commitment`, `require_safety_clear`, `_resident_work_order_clear`, and `require_building_clear` (`C3`).
  6. `AppointmentMixin.appointment_control(user, wid, {"action": "confirm", ...})` (`appointments.py:360-416`, transitions `Issued` -> `Appointed` once `"resident"`, `"staff"`, and `"capacity"` confirmations reach `"Committed"`): enforces `require_safety_clear`, `_resident_work_order_clear`, and `require_building_clear` before `_wo_move(w, "Appointed", ...)` (`C4`).
  7. `ProcurementMixin.complete_work_order(user, wid, note)` (`procurement.py:490-502`) and `correct_work_order(user, wid, reason, scope, resident_bindings)` (`procurement.py:504-518`): both enforce `require_safety_clear` and resident clearance (`C3`).
  8. `QualityMixin.accept_quality(user, case_id, index)` (`quality.py:313-329`) and `hand_over_quality(user, case_id, index, ...)` (`quality.py:378-391`): both enforce `require_safety_clear` and `require_resident_clear` (`C6`).
* **Q2 — Safety hold and release semantics**:
  * Unresolved safety evidence includes any hazard with `released is not True` (raised, referred, received, accepted, or repaired-but-unreleased), any open safeguarding item (`safeguarding_items` or item-shaped `safeguarding` via `taskqueues.is_open_safety_item`), and missing/malformed safety state (`C1`, `C7`, `C8`).
  * `release_hazard` requires `SAFETY_ROLES`, `accepted_at` + non-sensor/non-memory `repair_evidence`, `gates.safety_release_gate` pass, and `hazard.require_independent` (`C7`). Emergency referral (`raise_hazard`, `refer_hazard`, `receive_hazard`, `accept_hazard`, `record_repair`) remains open during a hold (`BRD FR-002`).
* **Q3 — Resident agreement and representative authority semantics**:
  * `resident_gate(c, bindings)` requires verified home tenure (`_inventory_managed` / `_home_tenure_recorded`), non-expired retention (`retention_schedule`), explicit measure `bindings` matching `current_context` (`technical.design_version`), current `measure_decisions[measure][-1]` with `status == "Accepted"` on `context["revision"]`, no `"Needs human review"` in `resident_reviews`, and for representative answers a `Confirmed` `representative_authorities` entry granting `"Works decision"` within `[authority_date, review_date)` and `< expires_at` (`C9`, `C10`).
  * Contact logs, silence, legacy case-wide `c["decision"]["status"] = "Accepted"`, survey access, appointment offers, or `Attend`/`Receive information`/`Communicate` representative permissions never satisfy `resident_gate` (`C9`, `C10`).
* **Q4 — Exercise scenario inventory in `src/core`**:
  1. Constructed core/workbench seed dataset (`ZF-1`..`ZF-5` in `src/core/tests/dataset.py`, mapped in `scenario_manifest.py` `SOURCES["fixture"]`, `C16`).
  2. Resident preview exercise fixture (`synthetic/resident_preview_fixture.py`: `SYN-C1`, `SYN-C2`, `SYN-C3`, `C13`).
  3. Sensor and damp retrofit exercise scenarios (`synthetic/sensor_scenarios.py`: `retrofit_exercise_scenarios()` `SYNTH-RETRO-001`..`005` and `generate()` damp-risk homes, `C14`).
  4. Scale-fixture matrix (`synthetic/scale_fixture.py`: `CONSENT_STATES`, `REP_STATES`, and `open_safety_issue` across seeded homes and households, `C15`).
  5. Journey learning-test bundles (`learning_test_bundles.py`: `BUNDLES`, including `story-once` zero-target `authority_or_consent_breaches` and `change-impact` zero-target `approvals_wrongly_carried_over`, `C12`).

#### Wave 3: Contrarian

Challenged existing gate implementations and exercise scenario fixtures for edge-case bypasses, crashes, or missing contracts (`Q5`):

1. **Contrarian Finding 1 — Standalone `safeguarding_items` in `gates.booking_gates` (`gates.py:249-260`)**:
   * `Store._open_safety_items` checks both `c["hazards"]` and `taskqueues.raw_safeguarding_items(c)` (added in `#76`), whereas `gates.booking_gates` only inspected `case.get("hazards")`. Evaluating `gates.booking_gates` directly on a case with `"hazards": []` and an open `safeguarding_items` record (or malformed `safeguarding_items: None`) yielded `PASS` on `BOOKING_RULES["safety"]` instead of `FAIL`/`UNKNOWN`.
   * Disposition: Accept and harden `gates.booking_gates` so standalone `safeguarding_items` and item-shaped `safeguarding` entries fail closed (`None`/non-list -> `UNKNOWN`; non-dict or `is_open_safety_item` -> `FAIL`; absent key -> unchanged for hazard-only unit fixtures).
2. **Contrarian Finding 2 — Missing or malformed `hazards` / `safeguarding_items` in `Store._open_safety_items` (`store.py:234-257`)**:
   * `Store._open_safety_items` iterated `c.get("hazards", [])` directly. Setting `c["hazards"] = None` or `["corrupt"]` raised `TypeError`/`AttributeError` instead of a clean `GateError`, and omitting `"hazards"` returned `[]` in `require_safety_clear`.
   * Disposition: Accept and harden `Store._open_safety_items` so missing/non-list `hazards`, non-dict hazard elements, or malformed `safeguarding_items` fail closed with `("Unverified safety evidence", "Building Safety Liaison")`, causing `require_safety_clear` to emit a clean `GateError`.
3. **Contrarian Finding 3 — Explicit authorised exception contract (`BG-005`, `RULE-002`, `FR-011`, `FR-014` `AC-018`)**:
   * Issue `#81` AC 2 requires proving that no work starts without valid resident agreement **or an explicitly authorised exception (`RULE-002` / `FR-011`)**. Previously `resident_decisions.py` had no structured validator for an authorised works exception (`data_protection.validate_necessity_exception` covers only external-model document reading under `FR-027`).
   * Disposition: Accept and add a strict, fail-closed `validate_authorised_works_exception(case, measure, context, *, now=None)` in `resident_decisions.py` (consulted by `_resident_decision_gate` only when `authorised_works_exceptions` is explicitly present for the measure) requiring: `status == "Authorised"`, exact `measure` + `context_revision` + `design_version` binding (`FR-008`), dated rule provenance (`reference`, `rule_source`, `effective_date <= check_day < review_date`, optional ISO UTC `expires_at > now_utc` per `RULE-002` `AC-004`), named human approver in `{"Building Safety Liaison", "Retrofit Programme Manager"}` rejecting automated/AI tokens, and `resident_notified is True` with non-blank `notification_ref` (`FR-014` `AC-018`). Unverified, expired, AI-approved, unnotified, scope-drifted, or revoked exceptions fail closed, and an authorised exception never clears tenure holds, `"Needs human review"`, or safety holds (`RULE-001`).
4. **Contrarian Finding 4 — `SYN-C3` in `resident_preview_fixture.py`**:
   * `SYN-C3` is seeded at display stage `"Works under way"` with an active P1 `Damp` hazard (`released=False`), `decision.status == "Waiting"`, and **zero issued or appointed work orders** (`SYN-C1` is the sole `Appointed` order and has valid scoped acceptance). Verifying static work-order activation invariants plus dynamic transition refusals on `SYN-C3` proves `SYN-C3` is stopped and refuses every progression and work-start transition on both `RULE-001` and `RULE-002`/`FR-011`.

## Evidence Log

| ID | Location | Finding |
| --- | --- | --- |
| `C1` | `src/core/src/zava_forward/core/gates.py:148-274` | `SAFETY_RELEASE_RULE` (`RULE-001; PRD FR-008`), `BOOKING_RULES` (`safety` -> `RULE-001; PRD FR-008`, `resident` -> `RULE-002; PRD FR-008`), `safety_release_gate`, and `booking_gates`. |
| `C2` | `src/core/src/zava_forward/core/store.py:234-272` | `Store._open_safety_items`, `gate_reasons`, `require_safety_clear` (`939-947`), `require_resident_clear` (`949-952`), `require_booking_gates` (`961-973`), and `advance` (`1022-1068`). |
| `C3` | `src/core/src/zava_forward/core/procurement.py:402-541` | `issue_work_order`, `reissue_work_order`, `record_wo_appointment` (`Booked` -> `Appointed`), `complete_work_order`, `correct_work_order`, and `_resident_work_order_clear`. |
| `C4` | `src/core/src/zava_forward/core/appointments.py:360-416` | `_appointment_confirm` transitions `Issued` -> `Appointed` only when all three confirmations are `Committed` and `require_safety_clear`, `_resident_work_order_clear`, and `require_building_clear` pass. |
| `C5` | `src/core/src/zava_forward/core/signoffs.py:92-120` | `_tech_signoff_give` calls `self.require_safety_clear(c)` before recording any technical or coordinator sign-off. |
| `C6` | `src/core/src/zava_forward/core/quality.py:313-391` | `accept_quality` and `hand_over_quality` enforce `require_safety_clear(c)` and `require_resident_clear(c)`. |
| `C7` | `src/core/src/zava_forward/core/workflows.py:1053-1196` | Hazard lifecycle (`raise_hazard`, `refer_hazard`, `receive_hazard`, `accept_hazard`, `record_repair`, `release_hazard`) enforces `SAFETY_ROLES`, non-sensor/non-memory repair evidence, and `gates.safety_release_gate`. |
| `C8` | `src/core/src/zava_forward/core/taskqueues.py:165-204` | `raw_safeguarding_items`, `is_open_safety_item`, and `has_open_safety` evaluate open hazard and standalone safeguarding items. |
| `C9` | `src/core/src/zava_forward/core/resident_decisions.py:965-1060` | `current_context`, `require_context`, `authority_for`, `resident_gate`, and `_resident_decision_gate` enforce tenure, retention, design-bound measure scope, explicit `Accepted` decisions, human-review holds, and `Works decision` representative authority. |
| `C10` | `src/core/src/zava_forward/core/resident_journey_design.py:27-88` | `AUTHORITY_TASKS` (`Receive information`, `Communicate`, `Attend`, `Works decision`); only `Works decision` permits measure consent decisions. |
| `C11` | `src/core/src/zava_forward/core/data_protection.py:224-370` | `validate_necessity_exception` rejects `_AUTOMATED_APPROVERS`, wildcard scopes, and expired dates. |
| `C12` | `src/core/src/zava_forward/core/learning_test_bundles.py:38-184` | `BUNDLES` and `evaluate_bundle` enforce zero-target stop rules on `story-once` (`authority_or_consent_breaches`) and `change-impact` (`approvals_wrongly_carried_over`). |
| `C13` | `src/core/src/zava_forward/core/synthetic/resident_preview_fixture.py:120-290` | Seeds `SYN-C1`, `SYN-C2`, and `SYN-C3`. |
| `C14` | `src/core/src/zava_forward/core/synthetic/sensor_scenarios.py:182-227` | `retrofit_exercise_scenarios()` and `generate()` define synthetic damp/condensation and retrofit exercise homes. |
| `C15` | `src/core/src/zava_forward/core/synthetic/scale_fixture.py:13-66` | Defines `CONSENT_STATES`, `REP_STATES`, and `open_safety_issue` across seeded synthetic homes and households. |
| `C16` | `src/core/tests/dataset.py:1-130` | Constructed workbench fixture `DATA` (`ZF-1`..`ZF-5`) referenced in `scenario_manifest.py`. |
| `C17` | `docs/brds/agentic-retrofit-programme-brd.md:636-638` | `BG-003` and `BG-005` zero-target metrics backed by `FR-001`, `FR-002`, `RULE-001`, `RULE-002`, `FR-008`, `FR-011`, and `FR-014` (`1508-1536`). |
| `C18` | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:1383-1390` | `PRD FR-008` (`AC-011`), `FR-014` (`AC-017`), and `FR-015` (`AC-018`). |

## Synthesis and Recommendation

### Selected Recommendation (`convergence`)

1. **Fail-closed safety and authorised-exception hardening (`gates.py`, `store.py`, `resident_decisions.py`)**:
   * Harden `gates.booking_gates` (`gates.py`) to inspect standalone `safeguarding_items` and item-shaped `safeguarding` alongside `hazards` (`C1`, `C8`).
   * Harden `Store._open_safety_items` (`store.py`) so missing/non-list `hazards`, non-dict hazard elements, or malformed `safeguarding_items` return `("Unverified safety evidence", "Building Safety Liaison")` (`C2`).
   * Add `validate_authorised_works_exception` in `resident_decisions.py` and integrate it into `_resident_decision_gate` (`C9`, `C11`, `C17`).
2. **Deterministic exercise-scenario gate verifier (`src/core/src/zava_forward/core/safety_consent_exercise_gate.py`)**:
   * Implement `verify_exercise_safety_and_consent_gates(...)` executing deterministic checks across all exercise scenario suites (`constructed_workbench`, `resident_preview`, `sensor_retrofit`, `scale_matrix`, `authorised_exception_controls`, and `learning_bundles`) on `Store` (and optionally `SqlStore` / custom scenarios), verifying:
     * Every controlled progression attempt on a case with unresolved safety evidence (`hazard`, open safety referral, repaired-but-unreleased hazard, open safeguarding item, or missing/malformed safety state) is blocked with an explicit safety-gate refusal (`RULE-001` / `FR-008`) with zero case/work-order/audit mutation, while emergency hazard referral remains open (`FR-002`).
     * Every attempt to start work (`issue_work_order`, `appointment_control("confirm")` -> `Appointed`, `record_wo_appointment("Booked")` -> `Appointed`, `advance` -> `Install booked`) without a valid active resident agreement or a valid explicitly authorised exception is blocked with an explicit consent-gate refusal (`RULE-002` / `FR-008` / `FR-011`) with zero case/work-order/audit mutation.
3. **Dedicated test suite and documentation (`src/core/tests/test_safety_consent_exercise_scenarios_81.py`, `src/core/README.md`)**:
   * Prove both `#81` exercise-scenario invariants across JSON `Store` and SQLite `SqlStore`, including adversarial bypass attempts and tamper-detection tests on the verifier itself.
   * Document `safety_consent_exercise_gate` and its evidence boundaries in `src/core/README.md`.

### Alternatives Rejected

* **Duplicate `lifecycle.py` state machine**: Rejected because testing a parallel state machine would not verify the authoritative runtime controls in `Store`, `SqlStore`, `gates.py`, `procurement.py`, `appointments.py`, `signoffs.py`, `quality.py`, and `resident_decisions.py` (`C1`–`C9`).
* **Static-only fixture inspection**: Rejected because static snapshots alone do not prove that runtime transitions raise explicit `GateError` refusals and leave state and audit chains unchanged.

## Readiness and Handoff

* **Research Execution Status**: Complete (Cycle 1 Wider, Deeper, Contrarian completed).
* **Research Disposition**: `executed`
* **Planning Readiness**: `Ready`
* **Research-Only Constraint Status**: Preserved (no source/test files edited during Research).
* **Self-Check**: All questions Q1–Q5 answered; `C1`–`C18` `path:line` citations recorded; alternatives evaluated; parent automatic RPI continuation eligible.
