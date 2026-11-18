<!-- markdownlint-disable-file -->

# Task Research: rai-218-release-discipline

| Field              | Value                                                                       |
|--------------------|-----------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                  |
| Researcher / agent | rpi-research (via RPI Agent)                                                |
| Status             | Complete (Planning Readiness: Ready; Disposition: executed)                 |
| Artifact path      | .copilot-tracking/research/2026-11-15/rai-218-release-discipline-research.md |

## Research Brief

* What to research: Responsible AI release, challenge, and incident control surfaces across `src/core` and `src/api` for Epic #218, specifically: (1) deterministic rejection and audit emission when attempting live AI task activation without a non-empty named human approver (`OQ-017`), (2) machine-readable requirement-to-acceptance traceability covering `FR-051` to `FR-054`, `NFR-014`, `AC-069` to `AC-073`, `OQ-017` to `OQ-019`, `RULE-024`, and `RULE-020` (mapping each to passing acceptance/unit checks or recorded live/owner deferrals), and (3) separating `rai_exercise_acceptance` from `real_ai_delivery_gate` in `src/core` and `src/api` readiness/status payloads.
* Why it matters: Proves the three executable Epic #218 acceptance criteria so operators and reviewers can verify deterministic named-approval gating (`OQ-017`), complete requirement traceability, and independent exercise-level RAI readiness versus live-model delivery gates.
* Audience or intended use: Planning (`rpi-plan`), implementation (`rpi-implement`), and review (`rpi-review`) stages in this RPI loop, plus coordinator verification on `feat/rai-218-release-discipline`.
* Scope: `src/core/src/zava_forward/core/` (`rai_release.py`, `assistant_release.py`, `assistants.py`, `gates.py`, `governance.py`, `rai_metrics.py`, `challenges.py`, `cohort_eval.py`, `human_review_effectiveness.py`, `restart_authority.py`, `ai_decision.py`, etc.), `src/api/src/zava_forward/api/` (`server.py`, `workbench.py`, `live_control.py`, etc.), `src/core/tests/`, `src/api/tests/`, and source requirement specifications in `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/brds/agentic-retrofit-programme-brd.md`, `docs/case_study_48_addendum.md`, and `docs/adrs/0002-pilot-readiness-architecture.md`.
* Non-goals: Running `tools/rpi-checks.py`, modifying infrastructure/Bicep/workflows, pushing or opening a PR, or claiming live production/owner sign-off for deferred live gates.
* Criteria: Every requirement in scope (`FR-051`..`FR-054`, `NFR-014`, `AC-069`..`AC-073`, `OQ-017`..`OQ-019`, `RULE-024`, `RULE-020`) and every existing RAI/gate/status module must be inspected with exact `path:line` evidence so the convergence recommendation integrates cleanly without breaking existing API/test contracts.
* Requested outputs: Primary research artifact with convergence design recommendation for Plan/Implement.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                                                              |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | How do `src/core` and `src/api` currently enforce live AI task activation approval (`OQ-017`), trace RAI requirements, and report exercise RAI checks vs real-AI delivery gates? |
| Codebase scope                   | `src/core/`, `src/api/`, `docs/prds/`, `docs/brds/`, `docs/adrs/`, `docs/case_study_48_addendum.md`                                                                |
| External scope                   | none (internal repository requirements and executable Python codebase)                                                                                             |
| Initial internal candidate areas | `src/core/src/zava_forward/core/rai_release.py`, `assistant_release.py`, `assistants.py`, `gates.py`, `governance.py`; `src/api/src/zava_forward/api/server.py`; PRD/BRD/ADR docs |
| Initial external candidate areas | none                                                                                                                                                               |
| Research posture                 | balanced                                                                                                                                                           |
| Posture provenance               | default (bounded internal task with named modules and adjacent readiness/status callers across `src/core` and `src/api`)                                           |
| Explicit limits / deadline       | Focused validation tier only; do not run `tools/rpi-checks.py`; do not push or open PR                                                                             |
| Posture-specific completion basis| Caller task and scope covered, material claims and questions backed by `path:line` evidence, adjacent callers checked for compatibility                            |
| Edits allowed during research?   | no, research-only                                                                                                                                                  |
| Resolved evidence root           | `.copilot-tracking/`                                                                                                                                               |
| Known constraints / excluded sources | Preserve existing API payload keys required by existing unit/browser tests while adding/exposing distinct `rai_exercise_acceptance` and `real_ai_delivery_gate` sections |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                              | Scoped authority or output contract          | Selected / skipped reason      |
|---------------------|----------------------------------|---------------------------------------------------|----------------------------------------------|--------------------------------|
| Instruction         | `.github/copilot-instructions.md` (AMA Repository Instructions) | `applyTo: "**"` matches workspace and tracking paths | Enforces problem-spec orientation, named human approval boundaries, Markdown style, and focused validation rules | Selected: mandatory repository instruction |
| Skill               | `rpi-research`                   | Active phase skill for RPI Research               | Three-wave research cycle and primary evidence artifact contract | Selected: active phase skill   |
| Skill               | `rai-standards` / `python-foundational` | Semantic match to RAI controls and Python modules | Background domain guidance only              | Skipped: repository PRD/BRD/ADR and existing `src/core` patterns define exact contracts |
| Research specialist | `hve-core-all:rpi-researcher`    | Host-registered general research subagent         | Bounded independent research lane            | Skipped (inline preferred): tightly coupled `src/core` + `src/api` + PRD/BRD trace fits direct `grep`/`view` with lower latency |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                       | Answers / unanswered      | Resulting decision or selected further research    |
|------------------|-------------------------------------------------------------|---------------------------|----------------------------------------------------|
| Intake           | Non-interactive session with explicit scope, acceptance criteria, branch, base, and validation tier | N/A (non-interactive) | Proceed directly with `balanced` convergence research across `src/core`, `src/api`, and docs |
| Direction change | None at intake                                              | N/A                       | Retain active caller brief                         |
| Convergence      | Non-interactive automatic RPI mode; Cycle 1 evidence complete | N/A (automatic mode)      | Converged on `src/core/src/zava_forward/core/rai_control_plane.py` wired into `assistant_release.py`, `assistants.py`, `ai_tasks.py`, `governance.py`, and `store.py` |

## Scope and Success Criteria

* Scope: Inspect existing RAI control-plane/release modules, live AI activation paths, audit ledger/event emission, PRD/BRD/ADR requirement definitions (`FR-051`..`FR-054`, `NFR-014`, `AC-069`..`AC-073`, `OQ-017`..`OQ-019`, `RULE-024`, `RULE-020`), and status/readiness/gate endpoints in `src/core` and `src/api`.
* Assumptions:
  * The prompt mentions `rai_control_plane.py` (or `assistants.py` / `release_governance.py`); actual repository modules may be named `rai_release.py`, `assistant_release.py`, `assistants.py`, `gates.py`, `governance.py`, etc., which must be verified before deciding whether to extend existing modules and/or expose a clean module/re-export.
  * Existing status/readiness endpoints in `src/api` may already have tests asserting specific top-level keys, so additive/compatible payload structuring must be verified.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs and one convergence recommendation is selected.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  1. Ensure any attempt to activate a live AI task without a non-empty named human approver (`approved_by` / `named_approval_id`) is deterministically rejected (`OQ-017`), with audit record emission.
  2. Provide a machine-readable requirement-to-acceptance traceability table/helper covering `FR-051` to `FR-054`, `NFR-014`, `AC-069` to `AC-073`, `OQ-017` to `OQ-019`, `RULE-024`, and `RULE-020`, mapping each to its passing unit/acceptance test or explicit live/owner deferral.
  3. Ensure the exercise acceptance / RAI readiness report (`src/core` and `src/api` status/readiness payload) emits a distinct `rai_exercise_acceptance` section separated from `real_ai_delivery_gate`.
* Inferred research questions:
  * Which exact modules own RAI release records, live AI task activation, and audit logging today, and are there any bypasses or missing `approved_by` / `named_approval_id` / audit checks?
  * What are the exact definitions of `FR-051`..`FR-054`, `NFR-014`, `AC-069`..`AC-073`, `OQ-017`..`OQ-019`, `RULE-024`, and `RULE-020` in the PRD/BRD/ADR, and which existing tests already cover child features (#219, #220, #221, #222, #223, #217) versus what requires live/owner deferral?
  * How are exercise acceptance, RAI readiness, and real-AI delivery gate currently computed and exposed in `src/core` and `src/api` HTTP endpoints?
* Caller constraints and non-goals: Focused validation only (`unittest`, `mypy`, `ruff check`, `ruff format --isolated --line-length 100 --check` on `src/core` and `src/api`); do not run `tools/rpi-checks.py`; do not push or open PR.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint  | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|-----------------------|----------------------|---------------------------------------------------|
| narrow                                                   | Focused validation tier on `src/core` and `src/api`; exclude `tools/rpi-checks.py`, `git push`, and `gh pr create` | Caller prompt / Intake | Constrain implementation and validation plan to `src/core` and `src/api` plus `.copilot-tracking/` artifacts |

## Research Questions

|  # | Sub-question     | Type (depth / breadth / straightforward) | Priority  | Status                    |
|---:|------------------|------------------------------------------|-----------|---------------------------|
| Q1 | What do PRD (`FR-051`..`FR-054`, `NFR-014`, `AC-069`..`AC-073`, `OQ-017`..`OQ-019`), BRD (`RULE-020`, `RULE-024`), Addendum, and ADR-0002 specify for Epic #218 and child issues (#219-#223, #440)? | breadth | H | answered (`C1`..`C4`) |
| Q2 | How do `rai_release.py`, `assistant_release.py`, `assistants.py`, `live_control.py`, and related `src/core`/`src/api` modules handle live AI task activation, named approval (`approved_by` / `named_approval_id`), and audit emission (`OQ-017`)? | depth | H | answered (`C5`..`C9`, `C15`, `C16`) |
| Q3 | Which existing core/api modules and unit tests already prove each requirement (`FR-051`..`FR-054`, `NFR-014`, `AC-069`..`AC-073`, `OQ-017`..`OQ-019`, `RULE-024`, `RULE-020`) and which parts are live/owner deferrals? | breadth | H | answered (`C1`..`C3`, `C10`..`C14`) |
| Q4 | Where are exercise acceptance, RAI readiness, and real-AI delivery gate payloads constructed in `src/core` and served in `src/api`, and how should `rai_exercise_acceptance` and `real_ai_delivery_gate` be structured cleanly and compatibly? | depth | H | answered (`C3`, `C8`, `C13`, `C17`, `C18`) |

## Cycle 1 Execution (Wider, Deeper, Contrarian)

### Wave 1: Wider

* Investigated inline across product/business/architecture docs (`docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/brds/agentic-retrofit-programme-brd.md`, `docs/case_study_48_addendum.md`, `docs/adrs/0002-pilot-readiness-architecture.md`) and codebase module layout under `src/core/src/zava_forward/core/` and `src/api/src/zava_forward/api/` (`C1`..`C8`).
* Confirmed that `src/core/src/zava_forward/core/rai_control_plane.py` does not yet exist; RAI release, challenge, incident suspension, cohort evaluation, human review effectiveness, monitoring coverage, privacy/Art. 22 guards, and phase/breach governance are distributed across `rai_release.py`, `assistant_release.py`, `assistants.py`, `challenges.py`, `continuity.py`, `restart_authority.py`, `cohort_eval.py`, `human_review_effectiveness.py`, `monitoring_coverage.py`, `regulatory_privacy.py`, and `governance.py` (`C5`..`C14`).

### Wave 2: Deeper

* Inspected live activation and release recording in `rai_release.py` (`named_human`, `missing_binding`), `assistant_release.py` (`assessment`, `record`, `change`), `assistants.py` (`record_release`, `registry`), `store.py` (`release_block`, `audit`, `ai_live_report`), and `sqlstore.py` (`release_block`, `release_assessment`) (`C5`..`C9`).
* Found two concrete gaps against AC 1 (`OQ-017`):
  1. Neither a dedicated `rai_control_plane` activation gate nor `assistant_release.record(..., evidence_class="actual")` currently requires both a non-empty named human `approved_by` and a non-empty `named_approval_id` (nor rejects fictional/placeholder owner tokens on live task activation).
  2. When `assistants.record_release()` or `assistant_release.record()` rejects an invalid live release/activation attempt by raising `PermissionError` or `ValueError`, the SQL transaction rolls back and `store.audit(...)` is never called, leaving zero audit record of the rejected live activation attempt (`C6`, `C7`, `C8`).
* Inspected all 15 requirement IDs (`FR-051`..`FR-054`, `NFR-014`, `AC-069`..`AC-073`, `OQ-017`..`OQ-019`, `RULE-024`, `RULE-020`) and verified concrete existing test modules/classes in `src/core/tests/` and `src/api/tests/` plus exact live/owner deferrals (`C1`, `C2`, `C10`..`C14`).
* Inspected status/readiness payloads in `ai_tasks.live_report`, `governance.governance_view`, `assistants.registry`, and `server.py` (`GET /api/ai/report`, `GET /api/governance`, `GET /api/assistants`) (`C7`, `C8`, `C13`, `C14`).

### Wave 3: Contrarian

* Tested hypotheses against existing test suites to identify hidden compatibility traps before planning (`C15`..`C18`):
  1. `src/core/tests/test_rai_threshold_live_approval_guard.py:130-141` calls `rai_release.missing_binding(record, {"model_version": "m1"}, [], NOW, True)` with a minimal dict lacking `approved_by` and `named_approval_id` keys and asserts `== []` (`C15`). Mutating `missing_binding` to unconditionally fail when those keys are omitted on synthetic bare dicts would break `LiveReleaseApprover.test_named_human_approver_passes_live`. Instead, `rai_control_plane.activate_live_task(...)` and `assistant_release.record()` (for `evidence_class == "actual"` or `live=True`) must strictly require both `approved_by` and `named_approval_id`, while `rai_release.missing_binding(..., live=True)` validates `approved_by` / `named_approval_id` whenever present on a record, and `src/core/tests/release_support.py` populates synthetic `approved_by` and `named_approval_id` when `cls == "actual"` so `src/api/tests/test_assistant_release.py:1020` continues to pass (`C15`, `C16`).
  2. `src/api/tests/test_heldout_eval_api.py:107-112` strictly asserts `set(report) == {"evaluation", "chat_evaluation", "live", "registry", "consumption"}` on `GET /api/ai/report` (`C17`). Adding top-level keys directly to `/api/ai/report` would break that test. Placing distinct `rai_exercise_acceptance` and `real_ai_delivery_gate` sibling sections inside `report["live"]` (`ai_tasks.live_report` / `store.ai_live_report`), as well as top-level on `GET /api/governance` (`store.governance_view`), `GET /api/assistants` (`assistants.registry`), and `store.rai_readiness_report()`, preserves the 5-key contract of `/api/ai/report` without adding uninventoried URL routes that would trip `src/api/tests/test_role_endpoint_inventory.py:72-77` or `src/api/tests/test_list_export_inventory.py:51` (`C17`, `C18`).
  3. `src/api/tests/test_content_standard.py:14` bans words `gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope` only inside `src/api/src/zava_forward/api/web/*.{js,html}`; backend JSON keys in `src/core` and `src/api/server.py` are unaffected as long as web assets are untouched.

* Cycle re-entry evaluation: No further research cycle needed. Every question `Q1`..`Q4` is backed by exact `path:line` evidence and contrarian regression checks are resolved.

## Evidence Log

| ID  | Source (`path:line`)                                                                 | Summary of verified fact                                                                                                    |
|-----|--------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| C1  | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:1426-1429`                | Defines `FR-051` (versioned RAI release record), `FR-052` (affected-person challenge/correction route), `FR-053` (operator suspension & manual/hazard continuity), and `FR-054` (cohort & missing-data evaluation record). |
| C2  | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:1550,2165-2169,2941-2943` | Defines `NFR-014` (per-task RAI monitoring/change control), `AC-069`..`AC-073` (acceptance criteria), and open questions `OQ-017` (named human release/risk/incident/review authority; no live activation without named approval), `OQ-018` (representative cohorts, lawful fairness fields, thresholds; synthetic scenarios do not prove fairness), and `OQ-019` (UK automated-decision safeguards & conditional EU AI Act legal screening). |
| C3  | `docs/case_study_48_addendum.md:1019`                                                | Specifies that exercise acceptance continues to require real Azure/SQL/AI under existing authority/budget, with RAI checks reported separately so disabled assistance preserves manual access without masquerading as a passing real-AI delivery gate. |
| C4  | `docs/brds/agentic-retrofit-programme-brd.md:1632-1633`                              | Defines `RULE-020` (evidence-based phase/tranche/authority release within approved cost/risk envelope) and `RULE-024` (guardrail breach pauses affected scope until authorized restart under OD-35 and RULE-020 while emergency/statutory hazard response continues). |
| C5  | `src/core/src/zava_forward/core/rai_release.py:13-76,211-251`                        | Defines `AUTHORITY_GAP` (`OQ-017`), `authority_register()`, `named_human()`, and `missing_binding(..., live=False)`. Checks `approver` and threshold `approved_by` on `live=True`, but does not enforce `named_approval_id` + `approved_by` on live task activation. |
| C6  | `src/core/src/zava_forward/core/assistant_release.py:107-182`                        | `record()` checks `missing_contract(rec, spec)` and inserts into `assistant_releases` + `release-recorded` event, but does not enforce `approved_by` / `named_approval_id` or live threshold approvals when `cls == "actual"`, and emits no audit event when validation fails. |
| C7  | `src/core/src/zava_forward/core/assistants.py:1218-1235,1351-1365,1534-1635`         | `record_release()` wraps `rel.record()` inside `self.transaction()` which rolls back on `PermissionError`/`ValueError` without calling `store.audit()` or persisting a rejection event; `registry()` returns assistant and registered-task status for `GET /api/assistants`. |
| C8  | `src/core/src/zava_forward/core/store.py:137-146,183-188,2125-2126`                  | `Store.audit()` appends hash-chained tamper-evident ledger entries; `Store.release_block()` audits `ai_release_denied`; `Store.ai_live_report()` delegates to `ai_tasks.live_report()`. |
| C9  | `src/core/src/zava_forward/core/sqlstore.py:226-245`                                 | `SqlStore.release_block()` runs `rel.assessment(..., live=True)` for legacy tasks when `self.ai.configured` is True and audits `ai_release_denied` on denial. |
| C10 | `src/core/src/zava_forward/core/challenges.py:1-145`                                 | Implements `FR-052` / `AC-071` store-independent challenge/correction register with accessible/non-digital routes and fail-closed `ChallengeSafeguardError` against retaliation, inferred refusal, or hazard delay (tested in `test_challenges.py` and `test_issue_220_challenge_route.py`). |
| C11 | `src/core/src/zava_forward/core/continuity.py:1-145`                                 | Implements `FR-053` / `AC-072` / `RULE-024` task/global suspension, epoch quarantine, distinct human restart drill, and uninterrupted manual/hazard continuity (tested in `test_operator_suspension_drill.py`, `test_operator_suspension.py`, `test_rai_harm_threshold_incident.py`). |
| C12 | `src/core/src/zava_forward/core/cohort_eval.py:1-158`                                | Implements `FR-054` / `AC-073` / `OQ-018` per-cohort evaluation record, missing-data indicators, measurement blockers, and explicit `OQ_018_GAP` non-fairness guard (tested in `test_cohort_eval.py`, `test_paired_equity.py`, `test_rai_threshold_live_approval_guard.py`). |
| C13 | `src/core/src/zava_forward/core/monitoring_coverage.py:1-155`                        | Implements `NFR-014` alert register and per-task monitoring declaration validation; `human_review_effectiveness.py` implements `AC-070` seeded-defect review check (`test_human_review_effectiveness_223.py`); `regulatory_privacy.py:1-160` implements `OQ-019` Art. 22A-22C human-decision guard & readiness gates (`test_regulatory_privacy_audit_217.py`). |
| C14 | `src/core/src/zava_forward/core/governance.py:710-780,930-995`                       | Implements `RULE-020` (`release_record`) and `RULE-024` (`breach_record`, `breach_restart`, `governance_view`), tested in `src/core/tests/test_governance.py` and `src/api/tests/test_governance_evidence_api.py`. |
| C15 | `src/core/tests/test_rai_threshold_live_approval_guard.py:130-141`                   | `LiveReleaseApprover.test_named_human_approver_passes_live` calls `rai_release.missing_binding` with `live=True` on a minimal dict containing `approver` without `approved_by`/`named_approval_id` keys and asserts `[]`. |
| C16 | `src/core/tests/release_support.py:10-37` and `src/api/tests/test_assistant_release.py:1020-1026` | `release_support.fixture(..., cls="actual")` populates synthetic named human threshold approvals and is passed into `rel.record()` in `test_assistant_release.py:1024`. |
| C17 | `src/api/src/zava_forward/api/server.py:933-975` and `src/api/tests/test_heldout_eval_api.py:107-112` | `GET /api/ai/report` returns `{"evaluation", "chat_evaluation", "live", "registry", "consumption"}` and `test_heldout_eval_api.py:107` strictly asserts that exact top-level key set; `report["live"]` comes from `s.ai_live_report(u)` (`ai_tasks.live_report`, `ai_tasks.py:567-598`). |
| C18 | `src/api/tests/test_role_endpoint_inventory.py:72-77` and `src/api/tests/test_list_export_inventory.py:51-78` | Every `/api/...` route in `server.py` is enforced against explicit endpoint inventories, favoring enriching existing readiness/status payloads (`/api/ai/report` `live`, `/api/governance`, `/api/assistants`) rather than adding unrequested routes. |

## Synthesis and Findings

### Answering Q1 & Q3: Complete Requirement-to-Acceptance & Deferral Map

Every required identifier (`FR-051`..`FR-054`, `NFR-014`, `AC-069`..`AC-073`, `OQ-017`..`OQ-019`, `RULE-024`, `RULE-020`) has an authoritative specification in PRD/BRD (`C1`, `C2`, `C4`), local executable verification in `src/core` and `src/api` (`C5`..`C14`), and where live human authority, participant fairness/review trials, or Legal/DPO sign-off cannot be fabricated in code, an explicit owner/live deferral:

1. `FR-051` & `AC-069`: Task-bound versioned RAI release record and fail-closed reactive/proactive dispatch denial (`rai_release.py`, `assistant_release.py`, `rai_control_plane.py`; tested in `test_rai_release.py`, `test_rai_release_invalidation.py`, `test_assistant_release.py`, plus new `test_rai_control_plane_218.py`).
2. `FR-052` & `AC-071`: Affected-person challenge/correction register with accessible/non-digital routes, transitive staleness, and non-retaliation/non-refusal/no-hazard-delay safeguards (`challenges.py`; tested in `test_challenges.py` and `test_issue_220_challenge_route.py`; live participant equity trials remain explicitly owner-deferred with `OQ-018`).
3. `FR-053` & `AC-072`: Operator suspension, impact/proposal reconstruction, epoch quarantine, distinct human restart drill, and uninterrupted manual/hazard routes (`continuity.py`, `restart_authority.py`, `assistants.py`; tested in `test_operator_suspension_drill.py`, `test_operator_suspension.py`, `test_rai_harm_threshold_incident.py`; witnessed live operational drill deferred to named owner under `OQ-017`).
4. `FR-054` & `AC-073`: Versioned per-cohort and missing-data evaluation record with denominators, subgroup error/exclusion/review-burden indicators, uncertainty, thresholds, and human disparity disposition (`cohort_eval.py`, `paired_equity.py`; tested in `test_cohort_eval.py`, `test_paired_equity.py`, `test_rai_threshold_live_approval_guard.py`; live fairness sign-off deferred under `OQ-018`).
5. `AC-070`: Seeded wrong/stale/unsupported/incomplete proposal detection vs control scenarios, rejecting default-accept and citation-only verification (`human_review_effectiveness.py`; tested in `test_human_review_effectiveness_223.py`; live staff review trials deferred to owner under `OQ-017`).
6. `NFR-014`: Per-task RAI monitoring declaration, observation windows, response thresholds, named owner roles, and suspend/restart reconstruction (`monitoring_coverage.py`, `rai_metrics.py`; tested in `test_monitoring_coverage.py`, `test_rai_threshold_live_approval_guard.py`, `test_rai_restart_sql_reconstruction.py`).
7. `OQ-017`: Named human RAI release, residual-risk, suspension/restart, and review authority; deterministic rejection + audit record emission on any live activation attempt without non-empty named human `approved_by` and `named_approval_id` (`rai_control_plane.py`, `assistant_release.py`, `assistants.py`; tested in `test_rai_control_plane_218.py`; live organizational role appointment remains an explicit owner deferral).
8. `OQ-018`: Representative cohorts, lawful fairness-analysis fields, sample sufficiency, and live disparity thresholds; synthetic results explicitly blocked from acting as fairness evidence (`cohort_eval.py`; tested in `test_cohort_eval.py`, `test_rai_threshold_live_approval_guard.py`, `test_ai_tasks.py`; live owner/DPO approval explicitly deferred).
9. `OQ-019`: UK automated-decision safeguards (Art. 22A-22C human decision guard) and conditional EU AI Act role/classification legal screening (`regulatory_privacy.py`; tested in `test_regulatory_privacy_audit_217.py`; formal Legal/DPO screening determination explicitly deferred).
10. `RULE-020`: Evidence-based phase/tranche/authority release decisions within approved cost/risk envelope (`governance.py`; tested in `test_governance.py`; live pilot phase release decision explicitly deferred to programme owner).
11. `RULE-024`: Guardrail breach pauses affected home, work package, archetype, or workstream until authorized restart under OD-35 and `RULE-020` while emergency/statutory hazard response continues (`governance.py`, `restart_authority.py`; tested in `test_governance.py` and `test_operator_suspension_drill.py`).

### Answering Q2 & Q4: Alternatives and Convergence Selection

* **Option A (Selected): Introduce `src/core/src/zava_forward/core/rai_control_plane.py` as the canonical Epic #218 control-plane module and wire it into `assistant_release.py`, `assistants.py`, `ai_tasks.py`, `governance.py`, and `store.py`.**
  * Provides `LiveActivationApprovalError(PermissionError)` (`code="OQ-017"`), `validate_live_task_approval(...)`, and `activate_live_task(...)` enforcing non-empty named human `approved_by` (rejecting blank, non-human/system/bot/agent/AI, and placeholder/fictional/unapproved tokens) plus non-empty `named_approval_id`, and deterministically emitting a hash-chained `store.audit(..., "rai_live_activation_rejected", ...)` entry (and committed `assistant_events` record when SQL is active) on every rejected live activation attempt (`C5`..`C8`).
  * Also wires `assistant_release.record()` and `assistants.record_release()` (which backs `POST /api/assistants/releases`) so recording an `evidence_class="actual"` (or `live=True`) release enforces the exact same `OQ-017` `approved_by` + `named_approval_id` + live monitoring threshold check and emits both `store.audit` and `assistant_events` records when rejected (`C6`, `C7`, `C16`).
  * Provides machine-readable `REQUIREMENT_TRACEABILITY` / `requirement_traceability()` / `traceability_summary()` covering all 15 required IDs with verifiable test target references and explicit deferral metadata.
  * Provides `exercise_acceptance_report(store, *, user=None, assistants_service=None)` returning distinct sibling `rai_exercise_acceptance` and `real_ai_delivery_gate` sections, surfaced in `store.rai_readiness_report()`, `store.ai_live_report()` (`GET /api/ai/report` -> `body["live"]`), `store.governance_view()` (`GET /api/governance`), and `assistants.registry()` (`GET /api/assistants`) without breaking `test_heldout_eval_api.py:107` or route inventories (`C3`, `C17`, `C18`).
* **Option B (Rejected): Modify only `rai_release.missing_binding` and add a new `GET /api/rai/readiness` endpoint.**
  * Rejected because: (1) `rai_release.py` is pure/store-free and cannot emit `store.audit` records on rejected live activation attempts (`C5`, `C8`); (2) altering `missing_binding` unconditionally for bare dicts without `named_approval_id` breaks `test_rai_threshold_live_approval_guard.py:139` (`C15`); and (3) adding a new endpoint triggers route-inventory failures unless `test_role_endpoint_inventory.py` and `test_list_export_inventory.py` are modified unnecessarily (`C18`), whereas enriching existing readiness/status payloads satisfies callers of `/api/ai/report`, `/api/governance`, and `/api/assistants`.

## Decisions, Risks, and Open Items

* **Current confirmed decisions**:
  * Implement `src/core/src/zava_forward/core/rai_control_plane.py` and integrate with `rai_release.py`, `assistant_release.py`, `assistants.py`, `ai_tasks.py`, `governance.py`, and `store.py` (`C5`..`C18`).
  * Update `src/core/tests/release_support.py` when `cls == "actual"` to include synthetic `approved_by` and `named_approval_id` fixtures (matching existing `threshold["approved_by"]` precedent at `release_support.py:13-19`, `C16`) while testing missing/blank/non-human/placeholder `approved_by` and `named_approval_id` rejections directly in `src/core/tests/test_rai_control_plane_218.py` and `src/api/tests/test_rai_release_readiness_api_218.py`.
* **Risks and mitigations**:
  * *Risk*: SQL transaction rollback on `PermissionError`/`ValueError` in `assistants.record_release` could erase an `assistant_events` rejection row. *Mitigation*: Emit `self.store.audit(...)` on the tamper-evident audit ledger AND write/commit the `live-activation-rejected` `assistant_events` row in its own short committed write when `rel.record` raises on a live activation attempt.
  * *Risk*: Disabled assistance (`ZF_AI=off`, unconfigured `Ai`, or missing SQL store) could accidentally report `real_ai_delivery_gate.passed = True`. *Mitigation*: `real_ai_delivery_gate["passed"]` requires `ai_configured and not workflow_only and sql_available and live_releases_ready and not active_suspension`, explicitly setting `disabled_assistance_cannot_masquerade_as_pass: True` (`C3`).
* **Potential further research**: None required for Epic #218 scope.

## Handoff and Readiness

* **Research disposition**: `executed`
* **Planning Readiness**: `Ready`
* **Self-check**:
  * [x] Research Brief, Parameters, Extension Registry, Participation, Scope, and Direction Controls recorded.
  * [x] Cycle 1 completed Wider, Deeper, and Contrarian waves in order.
  * [x] Every question `Q1`..`Q4` answered and mapped to `C1`..`C18` with workspace-relative `path:line` citations.
  * [x] Alternatives compared and Option A selected with evidence-backed rationale.
  * [x] Research remained strictly read-only on repository source files.

