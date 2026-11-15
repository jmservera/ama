<!-- markdownlint-disable-file -->
# RPI Plan: Usability Testing Programme with Representative Users (Issue #155)

## Task Metadata

* Task ID: issue-155-usability-programme-1507
* Task slug: ux-155-usability-programme
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/ux-155-usability-programme-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/ux-155-usability-programme-plan-critique.md

## Executive Summary

This plan completes the engineering and UX research specification slice for **Issue #155** (*Usability testing programme with representative users*) on stacked branch `feat/ux-155-usability-programme`. It introduces a pure, strictly typed evaluator module (`src/core/src/zava_forward/core/usability_programme.py`) and upgrades `docs/reference/research/ux/usability-test-programme-plan.md` in place so that Zava North Homes' usability testing protocol is directly derived from the repository's executable journey contracts and guarded by deterministic privacy, reporting, and honesty checks.

Specifically, the implementation wires canonical task scripts (`T0`, `T1`-`T8`, `R-J1`..`R-J6`, `R-R1`, and `B1-story-once`..`B5-funding-evidence`) directly to the five-element profile journey contract (`profile_journey_contract.py` and `perspective_walkthroughs.py` across all 11 PRD perspectives, `SIX_STAFF_PROFILES` same-home walk, `PROXY_ONLY` / `unmet` register metadata, `UX-01`..`UX-08`, and `journey_register.JOURNEYS`) and the five two-arm learning-test bundles (`learning_test_bundles.py` including `run_report`, `reconcile_o16`, `OUT_OF_SCOPE` exclusions, and Atlas failure scenarios), defines **5 to 8 participants per role** across staff, contractor, and voluntary resident/representative cohorts (plus a 2-3 proxy pilot), enforces **SA-010** aggregate-only reporting with full sub-5 `None` masking gated on prior `named_human` staff representative agreement (`date.fromisoformat`), validates severity-tagged (`1..4`) findings linked to GitHub backlog issues, preserves negative (`not_supported`) and `inconclusive` outcomes across four `evidence_source` classes (`moderated_participant`, `proxy_participant`, `proxy_pilot`, `synthetic_walkthrough`), and hard-labels every synthetic walkthrough with `not_user_validation=True` (`"Synthetic walkthrough - not user validation"`).

### User Decisions and Requirements Highlights

* **Stacked branch & no-push boundary**: Work stays on `feat/ux-155-usability-programme` (stacked onto `feat/demo-233-same-home-tensions-0825`, PR #1639) and commits cleanly with `.copilot-tracking/` artifacts and the Copilot trailer without pushing or opening a PR.
* **Focused validation tier**: Validation runs `src/core` unit tests, targeted `src/api` UX traceability unit tests, `ruff check`, `ruff format --check`, and `mypy` without invoking `tools/rpi-checks.py --all`.
* **Honest human vs synthetic boundary**: Synthetic walkthroughs verify contract wiring and script completeness only (`not_user_validation=True`, `"Synthetic walkthrough - not user validation"`), never claiming human usability sign-off or ticking human-only acceptance gates.

### What You May Not Know

* `docs/reference/research/ux/usability-test-programme-plan.md` already exists from a prose-only 2026-11-04 draft (before `profile_journey_contract.py` #134 and enriched `learning_test_bundles.py` #129 landed on 2026-11-15) and is already linked by `docs/reference/README.md` and `docs/reference/research/ux/design-system.md`. Updating it in place preserves Knowledge Base link integrity and Epic #149 automated traceability tests (`test_epic149_ux_journey_requirement_traceability.py` and `test_ux_design_traceability.py`).
* Every `(FR|NFR|AC|SA|OD)-\d+` identifier and every `test_*.py` filename referenced inside `docs/reference/research/ux/*.md` is automatically verified against the BRD/PRD and `src/*/tests/` by `test_epic149_ux_journey_requirement_traceability.py`.
* Because `/usr/bin/python3` on this shared host resolves an editable install in another checkout (`/home/azureuser/source/ama`), validation uses a gitignored worktree-local `.venv` so tests and CLI subprocess checks import strictly from this worktree.

### Unresolved Decisions or Blockers

* **None for engineering and specification delivery.** Live participant recruitment, named staff representative sign-off on the `SA-010` audit-use statement, owner ratification, and DPO retention approval remain external human governance gates and stay explicitly recorded as `Not agreed` / `Not run` (`Refs #155`).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Execute the full RPI loop in order (`rpi-research`, `rpi-plan` with independent plan critique, `rpi-implement`, `rpi-review`) writing dated 2026-11-15 tracking artifacts for Issue #155 (user prompt).
* Work in `/home/azureuser/source/ama-demo-wt/feat-155-usability-programme` on stacked branch `feat/ux-155-usability-programme` based on `feat/demo-233-same-home-tensions-0825` / PR #1639 (user prompt).
* Deliver the complete usability testing programme specification in `docs/reference/research/ux/` (updating `docs/reference/README.md` and `docs/reference/log.md`) and deterministic validation/evaluator support in `src/core` (user prompt, Objective 2).
* Define tasks, 5-8 participants per role, accessibility needs support, informed consent, and data handling in both the specification and deterministic validator (Issue #155 AC1; Objective 2).
* Derive task scripts directly from the profile journey contract (`profile_journey_contract.py` / `profile-journey-contract.md`) and learning-test bundles (`learning_test_bundles.py` / `journey-learning-test-bundles.md`), incorporating `zava-forward-prototype-profile-review.md` and `customer-journey-atlas.md` (Issue #155 AC2; Objectives 1-2).
* Enforce aggregate-only usability measures (`SA-010`) and require prior staff agreement on the non-surveillance audit-use statement before recording or reporting measures (Issue #155 AC3; PRD `SA-010`; Objective 2).
* Log usability findings with severity and valid links to backlog issues (Issue #155 AC4; Objective 2).
* Record negative and inconclusive outcomes without suppression, and explicitly label synthetic walkthroughs with `not_user_validation=True` (`"Synthetic walkthrough - not user validation"`), never claiming real human usability sign-off (Issue #155 AC5; Objective 2).
* Use the focused validation tier (`src/core` / `src/api` unit tests, `ruff check`, `ruff format --check`, `mypy`; do not run `tools/rpi-checks.py --all`) and commit all changes plus `.copilot-tracking/` artifacts cleanly on `feat/ux-155-usability-programme` with the Copilot trailer without pushing or opening a PR (user prompt, Validation tier & Objective 3).

## Goals

* Provide a canonical, executable usability testing programme contract in `zava_forward.core.usability_programme` that deterministically derives task scripts from `profile_journey_contract`, `perspective_walkthroughs`, `journey_register`, and `learning_test_bundles` and enforces `SA-009` / `SA-010` / `NFR-009` invariants.
* Upgrade `docs/reference/research/ux/usability-test-programme-plan.md` in place into the complete Issue #155 specification aligned 1:1 with the executable `src/core` contract while preserving honest `Not agreed` / `Not run` human governance gates.
* Verify contract invariants, refusal paths, and UX documentation traceability through focused automated unit tests, `ruff`, and `mypy --strict`.

## Scope and Non-Goals

### In Scope

* New pure Python module `src/core/src/zava_forward/core/usability_programme.py` implementing plan validation, live task-script derivation from `profile_journey_contract` + `learning_test_bundles`, `SA-010` staff audit-use gating and aggregate-only role measure evaluation, severity-tagged backlog-linked finding validation, negative/inconclusive outcome reporting, and `not_user_validation=True` synthetic walkthrough generation.
* In-place upgrade of `docs/reference/research/ux/usability-test-programme-plan.md` plus synchronized updates to `docs/reference/research/ux/design-system.md`, `docs/reference/README.md`, `docs/reference/log.md`, and `src/core/README.md`.
* Focused unit test suite `src/core/tests/test_usability_programme.py` and verification against existing `src/core/tests/` and `src/api/tests/` UX traceability suites, `ruff`, and `mypy`.
* Clean local commit on `feat/ux-155-usability-programme` including `.copilot-tracking/` artifacts and `Refs #155`.

### Non-Goals

* Conducting or fabricating live human participant sessions, staff representative `SA-010` sign-off, owner ratification, or DPO retention approval.
* Modifying existing `journey_register.aggregate_usability` (#128), `learning_test_bundles` (#129), or `profile_journey_contract` (#134) public signatures in ways that break existing callers.
* Changing web UI templates/CSS, running `tools/rpi-checks.py --all`, pushing to `origin`, or opening/updating a GitHub pull request.

## Functional Requirements

* **Programme plan contract and validation** (`default_programme_plan`, `validate_programme_plan`): Represent and validate the complete usability test plan covering tasks, role cohorts sized at `5..8` participants per role across staff roles (`SA-009`), contractor roles, and voluntary resident/representative cohorts (plus `2..3` proxy pilot), accessibility needs support (channel choice, own device/AT including screen reader/keyboard-only/magnification/zoom, advance plain-language briefing, interpreter/trusted person, extra time, voluntary-only need notes, break/stop freedom, non-digital parity per `NFR-009`), voluntary separate informed consent, and synthetic-only aggregate data handling.
  * Observable acceptance criteria: `validate_programme_plan(default_programme_plan())` returns `valid=True` with zero errors, and mutating any cohort outside `5..8` or omitting required accessibility, consent, or synthetic-data clauses returns deterministic validation errors.
* **Direct task-script derivation** (`derive_task_scripts`, `validate_task_scripts`): Deterministically derive moderated task scripts (`T0`, `T1`-`T8`, `R-J1`..`R-J6`, `R-R1`, `B1-story-once`..`B5-funding-evidence`) from `profile_journey_contract.ELEMENTS` (`entry`, `evidence`, `safe_endpoint`, `recovery`, `handoff`) across all 11 PRD perspectives in `perspective_walkthroughs.EVIDENCE` and `perspective_walkthroughs.register()` (preserving `PROXY_ONLY` and `partial`/`unmet` coverage notes, mapping `SIX_STAFF_PROFILES` to perspective slugs, retaining `T8` contractor submission from `suppliers.md`, `T0` `SA-009` core staff task, `UX-01`..`UX-08` checks, and `J1`-`J6` + `R1` resident/representative journeys from `journey_register.JOURNEYS`) and all 5 two-arm bundles in `learning_test_bundles.BUNDLES` (`story-once`, `pre-visit-pack`, `change-impact`, `handover-aftercare`, `funding-evidence`, preserving `comparator`, `atlas_ids`, `zero_measures`, `stop_rule`, `O16` single-count attribution, `OUT_OF_SCOPE` exclusions, and constructed Atlas failure scenarios).
  * Observable acceptance criteria: Derived scripts cover all 11 perspective IDs, all 5 contract elements, `T0` + `T1`-`T8`, `UX-01`..`UX-08`, `R-J1`..`R-J6` + `R-R1`, and all 5 bundle IDs while rejecting any `OUT_OF_SCOPE` (`O10`, `O18`-`O20`) bundle inclusion.
* **SA-010 audit-use gate and aggregate-only measures** (`validate_audit_use_agreement`, `evaluate_role_measures`): Require a valid `AuditUseAgreement` (`agreed_with_staff=True`, `named_human`-validated `staff_representatives`, explicit non-disciplinary/non-performance-audit `statement_text`, and ISO-parsed `agreed_date <= measurement_date` whenever any cohort has `participant_count > 0`) before recording or reporting staff usability measures; reject any payload containing individual-level identifiers (`FORBIDDEN_MEASURE_FIELDS`); suppress role cells where `0 < participant_count < 5` (`MIN_CELL_FLOOR = 5`) by masking `participant_count` (`n`) and all numeric metrics to `None`; report raw counts alongside coarse percentages plus SUS median/range, accessible SUS alternative count, manual fallback count, and target-zero `stop_rule_or_consent_blur_count` (`H4`); scope `T0` (`H1`) to staff/workbench cohorts; treat `< 5` numeric SUS responses caused by accessible-alternative selection as `"inconclusive"`; and evaluate `SA-009` (`>=80%` unaided `<5m` across `5..8` participants, `SUS >= 70`) strictly as hypothesis checks (`thresholds_are_hypotheses=True`).
  * Observable acceptance criteria: Calling `evaluate_role_measures` without prior `named_human` staff agreement, with invalid/missing ISO dates or `agreed_date > measurement_date`, or with individual-level fields raises `ValueError`; cells with `0 < participant_count < 5` mask `participant_count` and all metrics to `None`; nonzero `stop_rule_or_consent_blur_count` flags an `H4` breach; `5..8` role aggregates compute hypothesis status without setting human sign-off.
* **Severity-tagged, backlog-linked findings log** (`log_finding`, `validate_findings_log`): Validate findings with `UF-###` IDs, severities `1` (`note`), `2` (`minor`), `3` (`major`), or `4` (`blocker`), valid task/perspective/bundle references, anonymised observations free of participant identity fields, required GitHub backlog issue links (`#NNN` or repository issue URL, removing `"no issue yet"`), mandatory `named_human`-validated `risk_owner` + rationale when `status == "accepted_risk"`, and refusal of `status == "retested"` when `evidence_source in {"synthetic_walkthrough", "proxy_pilot"}`.
  * Observable acceptance criteria: Findings missing severity `1..4` or a valid backlog issue reference fail validation; `synthetic_walkthrough` and `proxy_pilot` evidence cannot mark a finding `retested`.
* **Negative/inconclusive outcome preservation and synthetic walkthrough labelling** (`evaluate_programme_results`, `build_synthetic_walkthrough_report`): Support `supported`, `not_supported` (negative), `inconclusive`, and `not_run` outcomes across four `evidence_source` classes (`moderated_participant`, `proxy_participant`, `proxy_pilot`, `synthetic_walkthrough`), preserving counts and records for negative and inconclusive outcomes without filtering; enforce `not_user_validation=True` and `validation_label="Synthetic walkthrough - not user validation"` on `"synthetic_walkthrough"` (and non-validation flags on `"proxy_pilot"` / `"proxy_participant"`), keep `human_usability_signoff=False` in automated outputs, and execute `profile_journey_contract.validate()`, `profile_journey_contract.validate_same_home_walk()`, `learning_test_bundles.run_report()`, and `learning_test_bundles.reconcile_o16()` inside `build_synthetic_walkthrough_report()`.
  * Observable acceptance criteria: Mixed result sets retaining `not_supported` and `inconclusive` outcomes report accurate counts and never claim user validation; synthetic walkthrough reports carry `not_user_validation is True` and `"Synthetic walkthrough - not user validation"`, and passing `not_user_validation=False` for a synthetic run raises `ValueError`.
* **Canonical UX specification and KB registration**: Update `docs/reference/research/ux/usability-test-programme-plan.md`, `docs/reference/research/ux/design-system.md`, `docs/reference/README.md`, `docs/reference/log.md`, and `src/core/README.md` so documentation and code reflect identical cohorts, scripts, `SA-010` rules, findings schema, negative/inconclusive outcome slots, and labelled synthetic walkthrough evidence while human sessions remain `Not run`.
  * Observable acceptance criteria: All relative Markdown links, BRD/PRD requirement IDs, and `test_usability_programme.py` references pass `test_epic149_ux_journey_requirement_traceability.py` and `test_ux_design_traceability.py`.

## Non-Functional Requirements

* **Strict static typing and lint cleanliness**
  * Objective threshold or evaluation condition: Zero `ruff check`, `ruff format --check`, and `mypy` (`strict = true`, Python 3.12, 100-char lines) errors across `src/core`.
  * Operating condition or verification approach, if needed: Verified in worktree-local `.venv` against `src/core/pyproject.toml`.
  * Observable acceptance criteria: `ruff check .`, `ruff format --check .`, and `mypy` exit `0` in `src/core`.
* **Core package dependency isolation**
  * Objective threshold or evaluation condition: `zava_forward.core.usability_programme` imports only Python stdlib and `zava_forward.core.*`.
  * Operating condition or verification approach, if needed: Verified via `src/core/tests/test_dependency_rule.py`.
  * Observable acceptance criteria: `test_dependency_rule.py` passes with zero cross-package imports.
* **Test discipline and bounded suite size**
  * Objective threshold or evaluation condition: Exact test file removals = `none`; maximum test file additions = `1` (`src/core/tests/test_usability_programme.py`, <= 30 focused semantic/edge-case test methods, zero `@unittest.skip` or trivial constant-restatement tests).
  * Operating condition or verification approach, if needed: `unittest` discovery in `src/core` and targeted UX traceability suites in `src/api`.
  * Observable acceptance criteria: All `src/core` unit tests and targeted `src/api` UX traceability tests pass with deterministic execution under 5 seconds.

## Acceptance Criteria

* [ ] AC1: `usability-test-programme-plan.md` and `zava_forward.core.usability_programme` define tasks (`T0`, `T1`-`T8`, `R-J1`..`R-J6`, `R-R1`, `B1-story-once`..`B5-funding-evidence`), 5-8 participants per role cohort (plus 2-3 proxy pilot), accessibility needs support, voluntary separate informed consent, and synthetic-only aggregate data handling.
* [ ] AC2: `derive_task_scripts()` and `usability-test-programme-plan.md` derive task scripts directly from `profile_journey_contract` (`ELEMENTS`, `SIX_STAFF_PROFILES` mapped to perspective slugs, 11 perspectives in `perspective_walkthroughs.EVIDENCE` + `register()` `PROXY_ONLY`/`unmet` metadata, `UX-01`..`UX-08`, `T8` contractor submission, `J1`-`J6`/`R1`) and `learning_test_bundles.BUNDLES` (`story-once`, `pre-visit-pack`, `change-impact`, `handover-aftercare`, `funding-evidence`, including comparators, stop rules, zero-target measures, `OUT_OF_SCOPE` exclusions, Atlas failure cases, and `O16` single-counting).
* [ ] AC3: `evaluate_role_measures()` enforces `SA-010` aggregate-only reporting (`MIN_CELL_FLOOR = 5` masking `participant_count` and all metrics to `None`, zero individual identifiers/quotes) and blocks recording/reporting unless `AuditUseAgreement` was agreed with `named_human` staff representatives on or before ISO `measurement_date`; `SA-009` thresholds (`>=80%` `<5m` for staff/workbench cohorts, `SUS >= 70` with accessible-SUS fallback) and `H4` target-zero stop-rule checks are evaluated strictly as hypotheses.
* [ ] AC4: `log_finding()` / `validate_findings_log()` require `UF-###` IDs, severity `1..4`, anonymised plain-language observations, and valid GitHub backlog issue links (`#NNN` or repo issue URL, removing `"no issue yet"`), plus `named_human` risk owners for `accepted_risk` and non-synthetic/non-pilot retest rules.
* [ ] AC5: `evaluate_programme_results()` and `build_synthetic_walkthrough_report()` record negative (`not_supported`) and `inconclusive` outcomes without suppression across all four `evidence_source` classes, execute `validate()`, `validate_same_home_walk()`, `run_report()`, and `reconcile_o16()`, and force `not_user_validation=True` (`"Synthetic walkthrough - not user validation"`), `user_validation_established=False`, and `human_usability_signoff=False` on synthetic walkthroughs while `usability-test-programme-plan.md` keeps human participant validation `Not run`.
* [ ] AC6: `docs/reference/README.md`, `docs/reference/log.md`, `docs/reference/research/ux/design-system.md` (column 5 `path::Class::method` syntax), and `src/core/README.md` are updated cleanly, focused validation (`src/core` + `src/api` UX traceability `unittest` including `test_production_ux_acceptance_protocol.py`, `ruff check`, `ruff format --check`, `mypy`) passes in worktree `.venv`, and all changes + `.copilot-tracking/` artifacts are committed locally on `feat/ux-155-usability-programme` (`Refs #155` + privacy-safe email + Copilot trailer) without pushing or opening a PR.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/ux-155-usability-programme-plan.md                                                                    |
| Phase details                    | .copilot-tracking/details/2026-11-15/ux-155-usability-programme-phase-details.md                                                         |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/ux-155-usability-programme-plan-critique.md with Revise verdict; PC-001..PC-005 resolved      |
| Relevant research                | .copilot-tracking/research/2026-11-15/ux-155-usability-programme-research.md                                                             |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/ux-155-usability-programme-changes.md is created or continued by implementation as its evidence record |
| Planning execution and readiness | Complete and Ready                                                                                                                       |
| Continuation context             | Confirmed automatic RPI Agent parent continues automatically to `rpi-implement`                                                          |

## Sources

* .copilot-tracking/research/2026-11-15/ux-155-usability-programme-research.md: Primary Cycle 1 Wider/Deeper/Contrarian evidence (`C1`-`C14`) and selected Option 1 architecture.
* docs/reference/research/ux/usability-test-programme-plan.md: Existing 2026-11-04 #155 draft plan to upgrade in place (`C1`).
* docs/prds/zava-forward-retrofit-programme-demonstrator.md: `SA-009` (5-8 users per role, `<5m` >=80% & SUS >=70 hypotheses), `SA-010` (aggregate-only & prior staff audit-use agreement), `OQ-004`, `OQ-005`, `OQ-011` (`C2`).
* docs/brds/agentic-retrofit-programme-brd.md: `NFR-009` / `AC-071` manual/non-digital parity and accountable ownership (`C3`).
* src/core/src/zava_forward/core/profile_journey_contract.py & src/core/src/zava_forward/core/perspective_walkthroughs.py: 5-element journey contract, 6-staff same-home contract, and 11 PRD perspectives (`C4`, `C5`).
* src/core/src/zava_forward/core/learning_test_bundles.py: 5 two-arm learning-test bundles, comparators, stop rules, zero-target measures, and `O16` single-counting (`C6`).
* src/core/src/zava_forward/core/journey_register.py: `JOURNEYS` (`J1`-`J6`, `R1`), `IDENTITY_FIELDS`, and `MIN_CELL_FLOOR = 5` (`C7`).
* docs/reference/research/ux/zava-forward-prototype-profile-review.md, docs/reference/research/ux/customer-journeys/customer-journey-atlas.md, & docs/reference/research/ux/customer-journeys/residents.md: `UX-01`..`UX-08`, 5 Atlas learning-test rows, and resident/representative scripts (`C8`, `C10`, `C11`).
* src/api/tests/test_epic149_ux_journey_requirement_traceability.py & src/api/tests/test_ux_design_traceability.py: Automated UX link, requirement ID, test-module, and pending-human-gate guardrails (`C12`).

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement deterministic usability programme contract and evaluator in `src/core`

* Intent: Deliver `zava_forward.core.usability_programme` with plan validation, live contract-derived task scripts, `SA-010` audit-use + aggregate-only evaluation, severity/backlog findings validation, negative/inconclusive outcome preservation, and `not_user_validation=True` synthetic walkthrough reporting.
* Dependencies: None (`profile_journey_contract`, `perspective_walkthroughs`, `journey_register`, and `learning_test_bundles` already exist in `src/core`).

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Bootstrap isolated worktree `.venv` and create `src/core/src/zava_forward/core/usability_programme.py`

* Requirement and evidence: Issue #155 AC1-AC5; Objectives 2a-2e; Research `C2`-`C11`, `C13`-`C14`; Critique `PC-001`..`PC-004`.
* Expected result: Gitignored worktree-local `.venv` installed (`-e src/core -e src/agents -e src/api` with `--no-build-isolation --no-deps`); pure, strictly typed `usability_programme.py` exporting canonical constants, frozen dataclasses, plan validator, `T0`/`T1`-`T8`/`R-J*`/`B1`-`B5` script derivation, `SA-010` `named_human`/ISO-date/masked-cell evaluator, findings logger/validator, four-class `evidence_source` outcome evaluator, and synthetic walkthrough generator calling `validate()`, `validate_same_home_walk()`, `run_report()`, and `reconcile_o16()`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/ux-155-usability-programme-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Document `usability_programme` in `src/core/README.md`

* Requirement and evidence: Repository component documentation rule; Research `C4`, `C6`, `C7`.
* Expected result: `src/core/README.md` lists `zava_forward.core.usability_programme` and its evidence boundary alongside existing journey/bundle modules.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/ux-155-usability-programme-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Upgrade UX usability testing programme specification and knowledge base

* Intent: Upgrade `docs/reference/research/ux/usability-test-programme-plan.md` in place to complete the #155 specification and synchronize `design-system.md`, `docs/reference/README.md`, and `docs/reference/log.md`.
* Dependencies: P01-T01 (exact module symbols, task script IDs, and synthetic walkthrough summary).

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Upgrade `docs/reference/research/ux/usability-test-programme-plan.md` in place

* Requirement and evidence: Issue #155 AC1-AC5; Objective 2; Research `C1`, `C2`, `C3`, `C8`-`C12`.
* Expected result: Updated `ms.date: 2026-11-15` specification covering 5-8 participants per role cohort, accessibility support, informed consent & data handling, direct derivation matrices to the 5-element `profile_journey_contract` (11 perspectives + same-home contract) and 5 `learning_test_bundles`, `SA-010` gate, severity/backlog findings contract, negative/inconclusive outcome slots, and an explicit `"Synthetic walkthrough - not user validation"` (`not_user_validation=True`) section distinct from `Not run` human sessions.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/ux-155-usability-programme-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Update `design-system.md`, `docs/reference/README.md`, and `docs/reference/log.md`

* Requirement and evidence: Objective 2; KB conventions; Research `C12`; Critique `PC-001`.
* Expected result: `design-system.md` Usability programme row preserves column 3 (`usability-test-programme-plan.md`) and column 6 (`pending human test: ...`) and appends `` `src/core/tests/test_usability_programme.py::UsabilityProgrammeTests::test_markdown_specification_matches_contract_and_keeps_human_sessions_not_run` `` alongside `test_production_ux_acceptance_protocol.py::...` in column 5; `docs/reference/README.md` updates Task Routing and the UX index row; `docs/reference/log.md` appends a dated 2026-11-15 entry without altering prior entries.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/ux-155-usability-programme-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Add comprehensive unit tests, run focused validation, and prepare local commit governance

* Intent: Verify every contract invariant, edge/refusal case, and cross-package UX traceability guardrail in the worktree `.venv` using the focused validation tier, and configure privacy-safe local commit metadata (`Refs #155`, no push/PR) coordinated with `rpi-review` closeout.
* Dependencies: P01, P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Create `src/core/tests/test_usability_programme.py`

* Requirement and evidence: Objective 3; Issue #155 AC1-AC5; Research `C12`, `C13`, `C14`; Critique `PC-001`..`PC-004`.
* Expected result: Focused `unittest.TestCase` suite (`UsabilityProgrammeTests`, 1 new file, 0 removals, <= 30 test methods, no `@unittest.skip`) testing plan bounds, live `T0`/`T1`-`T8`/`R-J*`/`B1`-`B5` derivation + `OUT_OF_SCOPE` exclusion, `SA-010` `named_human`/ISO-date/masked-`None` sub-5/`H4` stop-rule/cohort-scoped `T0` & accessible-SUS rules, severity/backlog findings validation, four-class `evidence_source` negative/inconclusive outcome anti-suppression, `not_user_validation=True` + `validate_same_home_walk()`/`run_report()`/`reconcile_o16()` enforcement, and `usability-test-programme-plan.md` contract alignment.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/ux-155-usability-programme-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Execute focused-tier tests, `ruff`, and `mypy` in isolated worktree `.venv`

* Requirement and evidence: Validation tier instruction & Objective 3; Research `C12`, `C13`; Critique `PC-001`.
* Expected result: `src/core` unit tests, `src/api` UX traceability unit tests (`test_epic149_ux_journey_requirement_traceability.py`, `test_epic149_ux_evidence_results.py`, `test_ux_design_traceability.py`, `test_production_ux_acceptance_protocol.py`), `ruff check`, `ruff format --check`, and `mypy` all exit `0` inside `.venv`.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/ux-155-usability-programme-phase-details.md

<!-- rpi:task id=P03-T03 -->
#### [x] P03-T03: Configure privacy-safe Git author email and verify staged local commit readiness (`Refs #155`, no push/PR)

* Requirement and evidence: Objective 3; AC6; Branch & PR instructions; Critique `PC-005`.
* Expected result: Repository-local `user.email` configured from `gh api user` (`{id}+{login}@users.noreply.github.com`), branch verified as `feat/ux-155-usability-programme`, `.venv` and caches verified gitignored/unstaged, and commit message (`Refs #155` + unmet human-gate note + Copilot trailer, zero closing keywords) prepared for single clean local commit immediately after `rpi-review` writes its final tracking artifacts (no push, no PR).
* Detail section: P03-T03 in .copilot-tracking/details/2026-11-15/ux-155-usability-programme-phase-details.md

## Dependencies

* `src/core/src/zava_forward/core/profile_journey_contract.py` & `perspective_walkthroughs.py` (#134): Canonical 5-element journey contract, 6-staff same-home contract, and 11 PRD perspectives from which profile task scripts derive.
* `src/core/src/zava_forward/core/learning_test_bundles.py` (#129): Canonical 5 two-arm learning-test bundles, comparators, stop rules, and `O16` single-count rule from which bundle task scripts derive.
* `src/core/src/zava_forward/core/journey_register.py` (#128): Canonical `JOURNEYS` (`J1`-`J6`, `R1`), `IDENTITY_FIELDS`, and `MIN_CELL_FLOOR = 5`.
* `src/api/tests/test_epic149_ux_journey_requirement_traceability.py` & `test_ux_design_traceability.py` (#149): Automated documentation link, requirement-ID, test-file, and pending-human-gate checks over `docs/reference/research/ux/`.

## Critique Disposition

Single-pass `rpi-plan-critique` completed in `.copilot-tracking/reviews/plans/2026-11-15/ux-155-usability-programme-plan-critique.md` (Verdict: `Revise`; 0 Critical, 2 High, 3 Medium, 0 Low). All five findings were direct planner corrections within confirmed caller direction and have been applied in full:

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` [High] (Circular `P02-T01 <-> P03-T01` dependency, premature `P02` traceability test gates, late `.venv` bootstrap, `design-system.md` column-5 `ast.parse` syntax) | resolved | Moved `.venv` bootstrap into `P01-T01`, broke `P02-T01 -> P03-T01` cycle so `P01 -> P02 -> P03` is strictly acyclic with `src/api` traceability tests executing in `P03-T02` (including `test_production_ux_acceptance_protocol.py`), and specified exact `src/core/tests/test_usability_programme.py::UsabilityProgrammeTests::test_markdown_specification_matches_contract_and_keeps_human_sessions_not_run` append in `design-system.md` column 5 while keeping column 3 unchanged |
| `PC-002` [High] (Missing `T8` contractor script, `SIX_STAFF_PROFILES` / `PROXY_ONLY` / `unmet` / `OUT_OF_SCOPE` / Atlas failure metadata, and `validate_same_home_walk()` + `run_report()` + `reconcile_o16()` wiring) | resolved | Standardized script IDs (`T0`, `T1`-`T8`, `R-J1`..`R-J6`, `R-R1`, `B1-story-once`..`B5-funding-evidence`), mapped `SIX_STAFF_PROFILES` to perspective slugs, read `perspective_walkthroughs.register()`/`PROXY_ONLY`, attached Atlas `C10` failure scenarios + `OUT_OF_SCOPE` checks, and wired `validate_same_home_walk()`, `run_report()`, and `reconcile_o16()` into `build_synthetic_walkthrough_report()` |
| `PC-003` [Medium] (`SA-010`/`SA-009` ISO date, `named_human`, full sub-5 `None` masking, `H4` stop-rule & SUS range fields, staff-only `T0` / accessible-SUS fallback) | resolved | Enforced `date.fromisoformat`, `rai_release.named_human`, mandatory `measurement_date` when `participant_count > 0`, full `None` masking on `participant_count` + metrics for `0 < n < 5`, complete `snake_case` `H1`-`H4` fields, staff/workbench `T0` scoping, and `"inconclusive"` SUS fallback when `< 5` numeric SUS scores exist due to accessible-alternative selection |
| `PC-004` [Medium] (Four-class `evidence_source` vocabulary, strict `human_usability_signoff=False`, `named_human(risk_owner)`, removal of `"no issue yet"` in `usability-test-programme-plan.md`) | resolved | Standardized on `evidence_source` in `("moderated_participant", "proxy_participant", "proxy_pilot", "synthetic_walkthrough")`, disallowed `"retested"` from synthetic/pilot runs, enforced `human_usability_signoff=False` in automated outputs and `named_human(risk_owner)`, and scheduled removal of `"no issue yet"` in `P02-T01` |
| `PC-005` [Medium] (Missing `AC6` local Git commit task, `gh api user` privacy-safe email, `Refs #155` non-closing rule, `.copilot-tracking/` staging, post-`rpi-review` commit coordination) | resolved | Added `P03-T03` for privacy-safe `git config --local user.email` via `gh api user`, `.gitignore`/`.venv` verification, and `Refs #155` + Copilot trailer local commit preparation, coordinated in Handoff so the final commit captures both implementation changes and the completed `rpi-review` tracking artifacts without pushing or opening a PR |
| Accepted residual risk (External human governance gates) | accepted_with_risk | Live human recruitment, owner ratification, named staff `SA-010` sign-off, and DPO retention approval remain external human work honestly recorded as `Not agreed` / `Not run` (`Refs #155`) |

## Follow-Up Items

* Obtain named staff representative sign-off on the `SA-010` non-surveillance audit-use statement and owner ratification of the usability test plan: external human governance gate required before recording live staff session measures (`Refs #155`, `#150`).
* Record DPO lawful-basis, optional-recording, and retention decision for usability study consent/notes: external data-protection gate required before recruiting participants (`Refs #155`, `#128`).
* Execute 2-3 proxy pilot followed by moderated 5-8 participant sessions per role including assistive-technology users: external human research execution after governance gates clear (`Refs #155`, `#151`).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/ux-155-usability-programme-changes.md
* Ready phase or task: Complete (`P01`-`P03` checked; ready for `rpi-review`)
* Commit coordination note: `P03-T03` configures privacy-safe Git email and verifies clean branch staging; the single local commit (`Refs #155` + Copilot trailer, no push/PR) executes after `rpi-review` writes `.copilot-tracking/reviews/logs/2026-11-15/ux-155-usability-programme-review.md` and updates session state so zero `.copilot-tracking/` files remain dirty on `feat/ux-155-usability-programme`.
* Remaining provisional question or blocker: None
