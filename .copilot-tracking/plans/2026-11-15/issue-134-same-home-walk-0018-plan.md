<!-- markdownlint-disable-file -->
# RPI Plan: Issue #134 Profile Journey Contract and Connected Same-Home Journey Acceptance

## Task Metadata

* Task ID: issue-134-same-home-walk-0018
* Task slug: issue-134-same-home-walk-0018
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/issue-134-same-home-walk-0018-phase-details.md
* Plan critique: .copilot-tracking/critiques/2026-11-15/issue-134-same-home-walk-0018-critique.md

## Executive Summary

This plan delivers the bounded code-testable slice for Issue #134 (`Refs #134`) on branch `feat/ux-134-same-home-walk-0018` targeting `feat/demo-233-same-home-tensions-0825` (`#1639`). It extends `zava_forward.core.profile_journey_contract` with deterministic connected same-home walkthrough and handover invariant validators across all six primary staff profiles, contractor views, and the resident portal; adds plain-language `Current owner` and `Next action` continuity to the selected-home banner on specialist staff screens in `role-screens.js`; establishes the missing canonical UX reference `docs/reference/research/ux/profile-journey-contract.md` (indexed in `docs/reference/README.md` and logged in `docs/reference/log.md`); and adds end-to-end `Store`, HTTP API, resident preview, and Node `role-screens.js` acceptance tests while keeping human approval, resident consent, and live accessibility walkthrough sign-off boundaries explicitly marked `not-established`.

### User Decisions and Requirements Highlights

* Deliver the full automatic RPI loop (`research`, `plan`, `plan-critique`, `implement`, `review`) with dated 2026-11-15 artifacts under `.copilot-tracking/` and leave a clean frozen local commit on `feat/ux-134-same-home-walk-0018` without pushing.
* Verify and complete code-testable profile journey contract and connected same-home walkthrough invariants across the six staff profiles (`Retrofit Programme Manager`, `Retrofit Coordinator`, `Resident Liaison Officer`, `Building Safety Liaison`, `Quality Inspector`, `Grants and Evidence Officer`), contractor view, and resident portal: handover dependencies, shared home facts, role-appropriate redaction of vulnerability reasons on contractor views, and plain-language next-action continuity across same-home transitions.
* Keep human/resident approval and live accessibility walkthrough sign-off boundaries explicit (`Refs #134` rather than `Closes #134`; all 11 PRD perspectives retain `perspective_walkthroughs.check(root)["elements_met"] == 0` and `journey_acceptance.check(root)["passed"] == []`).

### What You May Not Know

* `docs/reference/research/ux/profile-journey-contract.md` did not exist yet (the contract was embedded only in `docs/prds/zava-forward-retrofit-programme-demonstrator.md:2815-2875`). Creating it automatically enrols it into `test_epic149_ux_journey_requirement_traceability.py`, which validates every cited `FR-*`/`NFR-*`/`AC-*` ID against `SPEC_FILES`, dynamically imports every named `test_*.py` module to verify runnable unskipped tests, checks relative links, and rejects premature conformance claims.
* `test_content_standard.py` scans every line of `role-screens.js` (including comments) for banned internal terms (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`), and `test_role_screens_conformance.py` pins CSS classes, native interactive controls, and timer calls. Using a plain `<p data-same-home-next-action="${c.id}">` with no new CSS class, timer, heading, or link preserves every existing static and browser check.
* `scenario-manifest.json` pins hashes for `workbench-manifest.json`, `workbench_browser_check.py`, `dataset.py`, and `test_workbench.py`, not `role_screens_browser_check.py`; `role_screens_browser_check.py` needs no changes, and `test_scenario_manifest.py` plus `test_needs_inventory.py` will run to confirm manifest integrity.

### Unresolved Decisions or Blockers

* None for this code-testable slice. Live user walkthroughs (`#155`, OQ-004/005/011) and assistive-technology conformance sign-off (`#151`) remain explicit human gates outside automation.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `plan-critique`, `implement`, `review`) writing dated artifacts under `.copilot-tracking/` (`research`, `plans`, `details`, `changes`, `reviews`, `critiques`) for Issue #134 (`Refs #134`).
* Work in `/home/azureuser/source/ama-demo-wt/feat-134-same-home-walk-0018` on `feat/ux-134-same-home-walk-0018` targeting `feat/demo-233-same-home-tensions-0825` (stacked child PR under `#1639`).
* Inspect and align `src/core`, `role-screens.js` (`src/api/src/zava_forward/api/web/role-screens.js`), `src/api/checks/role_screens_browser_check.py`, and `docs/reference/research/ux/profile-journey-contract.md`.
* Verify and complete code-testable profile journey contract and connected same-home walkthrough invariants across the six staff profiles and resident portal: handover dependencies, shared facts, role-appropriate redaction of vulnerability reasons on contractor views, and plain-language next-action continuity across same-home transitions.
* Add or strengthen focused unit tests in `src/api/tests/` and `src/core/tests/` verifying connected same-home journey acceptance and handover invariants.
* Keep human/resident approval and live accessibility walkthrough sign-off boundaries explicit.
* Validate under the Focused tier (`mypy`, `ruff check .`, `ruff format --check .`, and targeted unit tests in `src/core` and `src/api`, plus `test_scenario_manifest.py` and `test_needs_inventory.py`).
* Commit all changes and `.copilot-tracking/` artifacts cleanly on `feat/ux-134-same-home-walk-0018` with privacy-safe repository-local `user.email` and trailer `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, and do NOT push.

## Goals

* Provide deterministic, reusable same-home profile journey contract validators in `zava_forward.core.profile_journey_contract` without breaking existing `ELEMENTS`, `validate`, `gaps`, `perspective_walkthroughs`, or `journey_acceptance` contracts.
* Ensure plain-language `Current owner` and `Next action` continuity is rendered inside `section.screen-evidence` across all staff specialist screen transitions on the same home while keeping contractor views strictly redacted to `Needs notice` and `Named contact`.
* Document the canonical profile journey contract and connected same-home invariants in `docs/reference/research/ux/profile-journey-contract.md`, indexed in `docs/reference/README.md` and recorded in `docs/reference/log.md`.
* Prove positive multi-stage walkthroughs and negative mutation rejections across `Store`, live staff/contractor/resident-preview HTTP endpoints, and Node-rendered `role-screens.js` views.

## Scope and Non-Goals

### In Scope

* Extending `src/core/src/zava_forward/core/profile_journey_contract.py` with connected same-home invariants (`SIX_STAFF_PROFILES`, `check_shared_facts`, `check_vulnerability_redaction`, `check_handover_dependencies`, `check_next_action_continuity`, `project_same_home_bundle`, `validate_same_home_walk`).
* Updating `src/api/src/zava_forward/api/web/role-screens.js` (after loading `redesign-existing-projects` and `web-design-guidelines`) so `section.screen-evidence` carries plain-language `Current owner` and `Next action` continuity across staff same-home screen transitions.
* Creating `docs/reference/research/ux/profile-journey-contract.md` and updating `docs/reference/README.md` and `docs/reference/log.md`.
* Strengthening `src/core/tests/test_profile_journey_contract.py` and creating `src/api/tests/test_same_home_profile_journey_acceptance.py`.
* Running focused validation (`mypy`, `ruff`, targeted `src/core` and `src/api` unit tests) and creating a clean local commit without pushing.

### Non-Goals

* Modifying `perspective_walkthroughs.py` or `journey_acceptance.py` to claim `"met"` or `"pass"` on `AC-034` through `AC-043`, or claiming WCAG 2.2 AA conformance or live user sign-off.
* Modifying `role_screens_browser_check.py` or `scenario-manifest.json` (already aligned and verified).
* Pushing commits or opening/updating remote GitHub PRs.

## Functional Requirements

* **Connected same-home shared facts & sibling isolation**: `profile_journey_contract` verifies that all six primary staff profiles (`Store.detail` / `projection.redact_staff_detail`), contractor views (`projection.contractor_detail`, `Store.list_work_orders`, staff-mediated `Store.work_order_job_pack`), and resident portal views (`resident_preview.resident_view(store, grant)`) project identical nested home identity (`home["address"]`, `home["postcode"]`), `id` (on staff/contractor views and work orders `case_id`), `stage` (staff views mapped to `resident_preview.STAGE_TEXT[stage] == (progress, next_step)` and `contractor_detail["status"] == ("Completed" if closed else stage)`), normalized `measures`, and closure state (`closed` bool on staff, `"closed": "This case is recorded as closed."` iff closed on resident preview, `order["state"] == "Completed"` on completed work orders), with zero sibling-home IDs or markers.
  * Observable acceptance criteria: `check_shared_facts` and `validate_same_home_walk` return zero findings on an intact `Store`/HTTP walkthrough and report deterministic findings when any profile disagrees on shared facts or leaks a sibling home marker.
* **Role-appropriate vulnerability redaction**: `profile_journey_contract` verifies that raw `resident.adjustment` reasons appear only for `projection.DEFAULT_REASON_ROLES` (`Resident Liaison Officer`, `Building Safety Liaison`, `Retrofit Programme Manager`); are replaced with `"Extra support noted"` (`projection.REDACTED`) alongside `projection.NOTE_HELD` and `"Safety review"`/`"Safety clock"` (and `taskqueues.HELD` on free-text handoff/return `work.next_action`) for `Retrofit Coordinator`, `Quality Inspector`, `Grants and Evidence Officer`, and `Programme Support Officer`; and are completely absent from contractor views (`contractor_summary`, `contractor_detail`, `list_work_orders`, staff-mediated `work_order_job_pack`, with `GET /api/workorders/{id}/job-pack` returning `403` to `Contractor`) and resident portal views, with contractors receiving only boolean `needs_notice` / `job_pack.ACCESS_NOTICE` (or `job_pack.ACCESS_NONE`) and `named_contact`.
  * Observable acceptance criteria: `check_vulnerability_redaction` passes across all projected roles and `contractor-job-pack` renders `"Needs notice"` and `"The reason for any notice is not shared with contractors."` with zero occurrences of the raw adjustment reason or `"Extra support noted"`.
* **Handover dependencies & non-equivalence**: `profile_journey_contract` verifies that unreleased hazards, unresolved stock queries, unaccepted/stale resident scope bindings, missing checklist evidence, self-acceptance (`accepted_by == submitted_by`), and unaccepted quality states (`Submitted`, `Returned`, `Fixed, awaiting reinspection`) prevent handover; contractor work-order `state == "Completed"` and job-pack receipt `status == job_pack.ACKNOWLEDGED` (`"Receipt acknowledged - not accepted"`, `accepted is False`) never satisfy quality `"Accepted"` or `"Handed over"`; and `journey_trace` causal ordering holds with `user_validation == "not-established"`.
  * Observable acceptance criteria: `check_handover_dependencies` passes across valid multi-stage transitions and rejects each mutated dependency bypass.
* **Plain-language next-action continuity**: `profile_journey_contract` and `role-screens.js` preserve non-empty plain-language `next_action` continuity across same-home transitions (free of banned internal terms `gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`), enforce pending-vs-accepted handoff receiver/chase-owner rules (`d["handoff"]["state"]` / `work["handoff"]["state"]`, `confirmed_receiver is None` on `d["handoff"]` and `"Unknown"` on `work["handoff"]` while pending, `taskqueues.HELD` when free-text handoff/return actions are held for non-reason roles), and match resident portal `(progress, next_step)` to `resident_preview.STAGE_TEXT[stage]` with `read_only is True`, `banner == resident_preview.BANNER`, and `"Consent and decisions"` in `unavailable`.
  * Observable acceptance criteria: `check_next_action_continuity` passes across multi-stage transitions, `role-screens.js` renders `data-same-home-next-action` on staff specialist screens without affecting contractor redaction, and `test_content_standard.py` passes with zero violations.
* **Canonical UX contract documentation**: `docs/reference/research/ux/profile-journey-contract.md` documents the five-element profile journey contract (`ELEMENTS = ("entry", "evidence", "safe_endpoint", "recovery", "handoff")`) across the 11 PRD perspectives, connected same-home invariants, code-verified test mapping, and explicit human/resident/AT boundaries (`AC-034`–`AC-043`, `FR-003`, `FR-004`, `FR-011`, `FR-012`, `FR-014`–`FR-017`, `FR-034`, `FR-035`, `FR-045`, `FR-048`, `FR-049`, `NFR-001`, `NFR-009`, `NFR-018`, `SA-001`–`SA-008`), and is indexed in `docs/reference/README.md` and logged in `docs/reference/log.md`.
  * Observable acceptance criteria: `test_epic149_ux_journey_requirement_traceability.py`, `test_ux_design_traceability.py`, `test_screen_design_traceability.py`, and `test_live_doc_links.py` pass with zero findings.

## Non-Functional Requirements

* **Type safety, lint, and formatting hygiene**
  * Objective threshold or evaluation condition: Zero errors from `mypy`, `ruff check .`, and `ruff format --check .` across modified/added Python files and package targets.
  * Operating condition or verification approach, if needed: Run repository `mypy` and `ruff` commands in the worktree Python environment.
  * Observable acceptance criteria: All static analysis commands exit `0`.
* **Accessibility, Fluent 2, and content-standard preservation on web UI**
  * Objective threshold or evaluation condition: Zero new CSS classes outside `style.css`, zero inline styles, zero timers, zero non-native interactive elements, zero banned vocabulary matches in `role-screens.js` (code or comments), and zero `web-design-guidelines` regressions.
  * Operating condition or verification approach, if needed: Verify with `test_role_screens.py`, `test_role_screens_conformance.py`, `test_content_standard.py`, `test_role_screens_connected_journey.py`, `test_role_screens_same_home_identity.py`, `test_role_screens_stage_map_focus.py`, `test_connected_home_check.py`, and `web-design-guidelines` line review.
  * Observable acceptance criteria: All role-screen conformance and content-standard tests exit `0` and review reports no open findings.
* **Human, resident, and live AT boundary integrity**
  * Objective threshold or evaluation condition: `perspective_walkthroughs.check(root)["elements_met"] == 0`, `journey_acceptance.check(root)["passed"] == []`, and `validate_same_home_walk(...)["boundaries"]` explicitly marks `human_approval`, `resident_approval`, and `accessibility_walkthrough` as `"not-established"`.
  * Operating condition or verification approach, if needed: Verified by `test_perspective_walkthroughs.py`, `test_journey_acceptance.py`, `test_epic149_ux_journey_requirement_traceability.py`, and new contract tests.
  * Observable acceptance criteria: All boundary guard tests exit `0`.

## Acceptance Criteria

* `src/core/src/zava_forward/core/profile_journey_contract.py` preserves `ELEMENTS = ("entry", "evidence", "safe_endpoint", "recovery", "handoff")`, `validate(walkthrough)`, and `gaps(root)` and implements `SIX_STAFF_PROFILES`, `REASON_STAFF_PROFILES`, `REDACTED_STAFF_PROFILES`, `BANNED_INTERNAL_TERMS`, `check_shared_facts`, `check_vulnerability_redaction`, `check_handover_dependencies`, `check_next_action_continuity`, `project_same_home_bundle`, and `validate_same_home_walk` with full `mypy` type annotations.
* `src/api/src/zava_forward/api/web/role-screens.js` renders `<p data-same-home-next-action="${c.id}">` with `Current owner` and plain-language `Next action` inside `section.screen-evidence` when `c.work?.next_action` is present on staff screens, while contractor views omit `c.work` and keep vulnerability reasons withheld.
* `src/core/tests/test_profile_journey_contract.py` and `src/api/tests/test_same_home_profile_journey_acceptance.py` cover end-to-end connected same-home walkthrough transitions and negative mutation controls across all six staff profiles, contractor views, and the resident portal (`ResidentPreview` + `GET /resident/view` + `resident_preview.resident_view`) (`maximum new test files: 1`; `exact test removals: none`).
* `docs/reference/research/ux/profile-journey-contract.md` exists (published after `test_same_home_profile_journey_acceptance.py` is created on disk), follows AMA Markdown and knowledge-base conventions, is indexed in `docs/reference/README.md` and `docs/reference/log.md`, and passes `test_epic149_ux_journey_requirement_traceability.py` and `test_live_doc_links.py`.
* Focused validation (`mypy`, `ruff check .`, `ruff format --check .`, targeted `src/core` and `src/api` unit tests including `test_resident_preview.py` in `src/core` and `test_resident_preview_api.py`, `test_scenario_manifest.py`, and `test_needs_inventory.py` in `src/api`) passes with `0` failures, and after `rpi-review` completes, all code, doc, test, and `.copilot-tracking/` artifacts are committed locally on `feat/ux-134-same-home-walk-0018` (preserving commit `6efbf1d`) with privacy-safe repository-local `user.email` and trailer `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/issue-134-same-home-walk-0018-plan.md                                                                 |
| Phase details                    | .copilot-tracking/details/2026-11-15/issue-134-same-home-walk-0018-phase-details.md                                                      |
| Latest critique                  | .copilot-tracking/critiques/2026-11-15/issue-134-same-home-walk-0018-critique.md with Revise disposition (PC-001 through PC-006 resolved)|
| Relevant research                | .copilot-tracking/research/2026-11-15/issue-134-same-home-walk-0018-research.md                                                          |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/issue-134-same-home-walk-0018-changes.md is created by implementation as its evidence record        |
| Planning execution and readiness | Complete and Ready for implementation (`PC-001` through `PC-006` applied directly)                                                       |
| Continuation context             | Confirmed automatic RPI Agent parent continues directly to `rpi-implement`                                                               |

## Sources

* `.copilot-tracking/research/2026-11-15/issue-134-same-home-walk-0018-research.md`: Primary research artifact (`C1`-`C22`) establishing codebase state, gap analysis, and Option B convergence selection.
* `docs/prds/zava-forward-retrofit-programme-demonstrator.md:2815-2875`: Authoritative PRD definition of the five-element Profile Journey Contract, connected same-home walk, and `AC-034` through `AC-043`.
* `docs/reference/research/ux/content-standard.md`: Plain-language vocabulary rules and blocker structure (`Why it is blocked`, `Owner`, `Next action`).
* `src/core/src/zava_forward/core/profile_journey_contract.py`, `projection.py`, `job_pack.py`, `taskqueues.py`, `quality.py`, `journey_trace.py`, `resident_summary.py`: Existing domain projection, redaction, handover, and audit-trace contracts.
* `src/api/src/zava_forward/api/web/role-screens.js` & `src/api/src/zava_forward/api/resident_preview/app.py`: Specialist staff/contractor screens and resident portal preview surfaces.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Core Connected Same-Home Journey Contract Validators

* Intent: Extend `zava_forward.core.profile_journey_contract` with pure, typed connected same-home walkthrough and handover invariant validators across all six staff profiles, contractor views, and the resident portal while preserving existing exports.
* Dependencies: None.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement same-home shared-facts, redaction, handover-dependency, and next-action continuity validators in `profile_journey_contract.py`

* Requirement and evidence: Caller Scope item 2; Research `C4`, `C7`, `C9`-`C12`, `C14`, `C15`, `C19`.
* Expected result: `profile_journey_contract.py` exports `SIX_STAFF_PROFILES`, `REASON_STAFF_PROFILES`, `REDACTED_STAFF_PROFILES`, `BANNED_INTERNAL_TERMS`, `check_shared_facts`, `check_vulnerability_redaction`, `check_handover_dependencies`, `check_next_action_continuity`, `project_same_home_bundle`, and `validate_same_home_walk`, preserving `ELEMENTS`, `validate`, and `gaps` unchanged.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/issue-134-same-home-walk-0018-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Specialist Screen Continuity and Connected Journey Acceptance Tests

* Intent: Surface plain-language `Current owner` and `Next action` continuity on selected-home staff specialist views in `role-screens.js` under AMA Web Development Guidance, and implement the focused `src/core` and `src/api` connected same-home walkthrough and redaction acceptance tests before publishing UX documentation references to them.
* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Load web design skills and add selected-home plain-language next-action continuity in `role-screens.js`

* Requirement and evidence: Caller Scope items 1 & 2; AMA Web Development Guidance; Research `C3`, `C11`, `C13`, `C16`, `C17`, `C18`; Critique `PC-002`, `PC-003`.
* Expected result: `redesign-existing-projects` and `web-design-guidelines` (with live rules fetched) guide a surgical edit in `src/api/src/zava_forward/api/web/role-screens.js` rendering `<p data-same-home-next-action="${c.id}">` with `Current owner` and `Next action` inside `section.screen-evidence` when `c.work?.next_action` is present (free of `test_content_standard.py` `BANNED` words in code and comments), leaving contractor views redacted and passing all conformance/copy/browser checks.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/issue-134-same-home-walk-0018-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Strengthen `src/core/tests/test_profile_journey_contract.py` with multi-stage Store walkthrough and negative invariant tests

* Requirement and evidence: Caller Scope items 2, 3 & 4; Research `C4`, `C7`, `C9`-`C12`, `C19`; Critique `PC-001`, `PC-002`, `PC-004`.
* Expected result: `test_profile_journey_contract.py` retains existing `ELEMENTS`/`validate`/`gaps(root)` tests and adds positive multi-stage same-home walkthrough coverage (`ZF-1` + sibling `ZF-2` across safeguarding stop/restart, EPC conflict/reconciliation, technical sign-offs, resident choice, pending-to-accepted handoff including `taskqueues.HELD` free-text redaction, work order + staff-mediated job pack + `job_pack.ACKNOWLEDGED` receipt, quality return/fix/reinspect/handover, finance match/disposition/payment, and `resident_preview.resident_view`) plus negative mutation tests for all four invariant groups.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/issue-134-same-home-walk-0018-phase-details.md

<!-- rpi:task id=P02-T03 -->
#### [x] P02-T03: Create `src/api/tests/test_same_home_profile_journey_acceptance.py` for full-stack HTTP, `ResidentPreview` (`GET /resident/view`), and Node `role-screens.js` walkthrough verification

* Requirement and evidence: Caller Scope items 2, 3 & 4; Research `C9`, `C10`, `C13`, `C14`, `C18`, `C20`; Critique `PC-001`, `PC-002`, `PC-003`.
* Expected result: `src/api/tests/test_same_home_profile_journey_acceptance.py` drives one synthetic home (`ZF-1` with sibling `ZF-2` and vulnerability adjustment) through authenticated HTTP endpoints across all six staff profiles, `Programme Support Officer`, assigned/unassigned `Contractor` (`403` on staff-only `/job-pack`), and live loopback `ResidentPreview` (`GET /resident/view`), validates live HTTP payloads via `validate_same_home_walk`, and runs Node `role-screens.js` (with `workSummary` sliced from `app.js` and live App GET routing) across valid screen IDs (`programme-queue`, `technical-queue`, `resident-choice`, `procurement-packages`, `quality-queue`, `finance-invoices`, `safety-lead`, `contractor-job-pack`).
* Detail section: P02-T03 in .copilot-tracking/details/2026-11-15/issue-134-same-home-walk-0018-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Canonical UX Profile Journey Contract Reference and Knowledge Base Index

* Intent: Publish `docs/reference/research/ux/profile-journey-contract.md` after all referenced test modules exist on disk, and update `docs/reference/README.md` and `docs/reference/log.md`.
* Dependencies: P01, P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Author `docs/reference/research/ux/profile-journey-contract.md` and update `docs/reference/README.md` and `docs/reference/log.md`

* Requirement and evidence: Caller Scope items 1, 2 & 4; AMA Knowledge Base & Markdown Style conventions; Research `C1`, `C2`, `C20`, `C21`; Critique `PC-004`, `PC-005`.
* Expected result: `docs/reference/research/ux/profile-journey-contract.md` documents the five-element contract (`ELEMENTS = ("entry", "evidence", "safe_endpoint", "recovery", "handoff")`) across the 11 PRD perspectives, connected same-home invariants across the six staff profiles, contractor view, and resident portal, code-test mappings (including `test_same_home_profile_journey_acceptance.py`), and explicit human/resident/AT non-equivalence boundaries (`AC-034`–`AC-043`, `FR-003`, `FR-004`, `FR-011`, `FR-012`, `FR-014`–`FR-017`, `FR-034`, `FR-035`, `FR-045`, `FR-048`, `FR-049`, `NFR-001`, `NFR-009`, `NFR-018`, `SA-001`–`SA-008`), indexed in `docs/reference/README.md` and logged in `docs/reference/log.md`.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/issue-134-same-home-walk-0018-phase-details.md

<!-- rpi:phase id=P04 -->
### [x] P04: Focused Validation, Guardrail Verification, and Review-Aligned Local Closeout

* Intent: Run static type/lint/format checks, targeted unit and traceability suites in `src/core` and `src/api`, and web-design-guidelines verification before `rpi-review`, followed by privacy-safe local commit including `.copilot-tracking/` review artifacts without pushing.
* Dependencies: P01, P02, P03.

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Execute focused validation suite and record verification outputs

* Requirement and evidence: Caller Validation tier; Research `C16`-`C22`; Critique `PC-005`, `PC-006`.
* Expected result: `mypy`, `ruff check .`, `ruff format --check .`, `src/core` unit tests (including `test_resident_preview.py`), and `src/api` unit/traceability/manifest tests (including `test_resident_preview_api.py`, `test_ux_design_traceability.py`, `test_screen_design_traceability.py`, `test_connected_home_check.py`, `test_scenario_manifest.py`, `test_needs_inventory.py`) pass with `0` failures; post-`rpi-review` closeout commits all code, doc, test, and `.copilot-tracking/` artifacts locally on `feat/ux-134-same-home-walk-0018` (preserving `6efbf1d`) with privacy-safe local `user.email` and `Co-authored-by` trailer without `git push`.
* Detail section: P04-T01 in .copilot-tracking/details/2026-11-15/issue-134-same-home-walk-0018-phase-details.md

## Dependencies

* Existing installed local editable packages (`zava-forward-core`, `zava-forward-agents`, `zava-forward-api`) and Node.js runtime (`node`) used by `src/api/tests/test_role_screens*.py`.
* AMA Web Development Guidance skills (`redesign-existing-projects` and `web-design-guidelines`) before editing `role-screens.js`.
* UX documentation traceability guards (`test_epic149_ux_journey_requirement_traceability.py`, `test_ux_design_traceability.py`, `test_screen_design_traceability.py`, and `test_live_doc_links.py`) resolving requirement tokens against `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/prds/proper-warm-retrofit-programme-demonstrator.md`, and `docs/brds/agentic-retrofit-programme-brd.md`.

## Critique Disposition

Single-pass `rpi-plan-critique` completed (`.copilot-tracking/critiques/2026-11-15/issue-134-same-home-walk-0018-critique.md`, verdict `Revise`). All six findings were compatible planner-owned alignments and have been applied directly.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` [Critical]: Resident portal API/schema mismatch | Resolved | Updated `P01-T01`, `P02-T02`, and `P02-T03` to use `zava_forward.core.resident_preview.resident_view(store, grant)`, 2-tuple `resident_preview.STAGE_TEXT[stage] == (progress, next_step)`, nested `view["home"]`, optional string `view["closed"]`, `read_only`/`banner`/`unavailable`, and live `ResidentPreview` (`GET /resident/view` on loopback with disposable synthetic `grants.json`). |
| `PC-002` [High]: Store projection, job-pack, `taskqueues.HELD`, and quality blocker contracts | Resolved | Aligned `P01-T01` and `P02` to `Store.detail` / `projection.redact_staff_detail`, `projection.DEFAULT_REASON_ROLES`, nested `d["home"]`, `order["state"] == "Completed"`, staff-mediated `Store.work_order_job_pack` (`ACCESS_NOTICE` / `ACCESS_NONE`, `ACKNOWLEDGED`, `403` for Contractor), `taskqueues.HELD` on non-reason roles for free-text handoff/return `work.next_action`, `d["handoff"]["state"]` / `work["handoff"]["state"]`, and `c["quality"]` unaccepted/defect/self-accepted state checks. |
| `PC-003` [High]: Specialist screen ID `safety-lead`, `app.js` `workSummary`, and lexical `BANNED` guard | Resolved | Replaced non-existent `building-safety-queue` with `safety-lead` / `hazard-triage`, specified slicing `workSummary` from `app.js` plus live App GET routing in Node `vm`, and noted the `test_content_standard.py` lexical ban on code and comments in `role-screens.js`. |
| `PC-004` [Medium]: 5-element keys, 11 perspectives, `check(root)`/`gaps(root)` signatures, and `SPEC_FILES` req IDs | Resolved | Aligned plan and `P03-T01` to 11 PRD perspectives, `ELEMENTS = ("entry", "evidence", "safe_endpoint", "recovery", "handoff")`, `perspective_walkthroughs.check(root)`, `journey_acceptance.check(root)`, `profile_journey_contract.gaps(root)`, actual `SPEC_FILES`, and verified PRD/BRD requirement IDs. |
| `PC-005` [Medium]: Sequence test creation before UX doc traceability scan; fix `test_resident_preview.py` path and add traceability suites | Resolved | Reordered `P02` (tests) before `P03` (`profile-journey-contract.md`) so `test_same_home_profile_journey_acceptance.py` exists before `ControlClaimsMapToTests` runs, moved `test_resident_preview.py` to `src/core` tests, and added `test_resident_preview_api.py`, `test_ux_design_traceability.py`, `test_screen_design_traceability.py`, and `test_connected_home_check.py` to `P04-T01`. |
| `PC-006` [Low]: Explicit local commit & post-`rpi-review` artifact sequencing note | Resolved | Documented privacy-safe repository-local `user.email` resolution from `gh api user` and post-`rpi-review` local `Refs #134` commit (preserving `6efbf1d`, including `.copilot-tracking/` review artifacts, without `git push`) in `P04-T01` and Acceptance Criteria. |

## Follow-Up Items

* Live user walkthroughs across the 11 perspectives (`#155`, OQ-004, OQ-005, OQ-011) and assistive-technology conformance verification (`#151`) remain open human-gated acceptance items before `#134` (`AC-034` through `AC-043`) can be closed.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/issue-134-same-home-walk-0018-changes.md
* Ready phase or task: All active plan phases (`P01`, `P02`, `P03`, `P04`) complete; ready for `rpi-review`
* Remaining provisional question or blocker: None
