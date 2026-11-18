<!-- markdownlint-disable-file -->
# RPI Plan: Hazard and Safeguarding Clock and Named Owner Projection (Issue #76)

## Task Metadata

* Task ID: issue-76
* Task slug: ux-76-hazard-clock-owner
* Planning status: Ready for implementation (critique revisions PC-001..PC-005 applied)
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/ux-76-hazard-clock-owner-plan-critique.md

## Executive Summary

This plan delivers the sole remaining unchecked acceptance criterion on Issue #76 ("Role-based task queues, case card and shared work queue"): every hazard and safeguarding item across role-based task queues, `My cases today`, the shared `All open cases` work queue, and case cards explicitly projects and renders both a statutory/operational clock and a non-blank named accountable owner. By building one shared projection helper in `src/core` (`taskqueues.py` and `workflows.py`) and rendering it through `workSummary(work)` and `safetyPanel(...)` in `src/api/src/zava_forward/api/web/app.js`, every queue row and case card stays in exact `FR-034` agreement across JSON and SQLite/MSSQL stores while keeping `web/role-screens.js` untouched.

### User Decisions and Requirements Highlights

* Deliver `- [ ] Hazard and safeguarding items show a clock and named owner` on branch `feat/ux-76-hazard-clock-owner` targeting `feat/demo-164-chat-grounding-provenance-0900` (PR #1641) without pushing, so the branch remains a clean stacked worktree ready for review.
* Every hazard and safeguarding item in queue projections and case card responses must expose and render a statutory/operational clock (`clock_status`, `clock_remaining_hours`, `clock_deadline_utc`, `clock_label`), failing closed with an explicit clock state (`fail_closed_missing_timestamp`) when timestamps are missing or invalid.
* Every hazard and safeguarding item must expose and render a named accountable owner (`named_owner`, `accountable_owner`, `owner_role`, `owner_id`), never blank or anonymous, surfacing the named `escalation_owner` and `unassigned: True` when no direct follow-up owner is allocated.
* Keep `src/api/src/zava_forward/api/web/role-screens.js` unmodified and preserve all counted baseline guards (`test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_list_export_inventory.py`).

### What You May Not Know

* All specialist role screens in `web/role-screens.js` already delegate queue-row safety rendering to `workSummary(row.work)` defined in `web/app.js`, and `safety-lead` / `hazard-triage` inspect `c.hazards` against `row.hazard` (`role-screens.js:875`). Projecting normalized standalone safeguarding items into both `d["safeguarding_items"]` and `d["hazards"]` (with scalar `owner` backfilled from `named_owner` when unallocated) updates every role screen automatically without editing `web/role-screens.js` or triggering a false `"Mismatch"` row.
* Three existing tests impose strict compatibility boundaries that the plan preserves: `test_taskqueues.py` requires legacy `clock["owner"] == "Unknown"` when direct follow-up is unallocated and requires receipt-is-not-acceptance (`sender` stays direct owner until `accepted_at`); `test_role_screens.py` slices `function workSummary(` up to `function workSteps(` into an isolated Node `vm` with legacy clock fixtures; and `test_safety_panel_ux.py` requires `<dl class="safety-facts">` to keep exact 4 `<dt>` rows without `"Unknown"`.
* `resident_preview_fixture.py` attaches a canary-only `safeguarding={"note": "..."}` dict to ordinary cases `SYN-C1` and `SYN-C2` before issuing work orders, so standalone safeguarding item extraction requires an explicit item-identifying key set on `safeguarding` dicts and ignores note-only `{"note": ...}` containers.

### Unresolved Decisions or Blockers

* None. All architectural, regulatory, and test-guard boundaries were verified in `.copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-research.md`.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Complete the ordered RPI loop (`research`, `plan`, `implement`, `review`) with dated artifacts under `.copilot-tracking/` (`research`, `plans`, `details`, `changes`, `reviews`) for Issue #76 (`Caller intake brief`).
* Deliver the remaining unchecked Issue #76 acceptance criterion: `Hazard and safeguarding items show a clock and named owner` across role-based task queues, `my_cases_today` / shared work queue projections, and case cards (`Issue #76`, `Caller intake brief`).
* Explicitly include and display a statutory/operational clock (`clock_status`, `clock_remaining_hours` / `clock_deadline_utc`, `clock_label`, e.g., Awaab's Law 24h emergency / 7d investigation / 14d work-start or safeguarding response clock) that fails closed with an explicit clock state when timestamps are missing (`Caller intake brief`, `SI 2025/1042`, `RULE-003`).
* Explicitly include and display a named accountable owner (`named_owner`, `owner_role`, `owner_id`, `accountable_owner`), never blank or anonymous; if unallocated, explicitly surface `escalation_owner` and `unassigned` flag so a named owner is always visible (`Caller intake brief`, `SA-007`).
* Avoid modifying `src/api/src/zava_forward/api/web/role-screens.js` and do not break counted baseline guards in `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, and `test_list_export_inventory.py` (`Caller intake brief`).
* Add focused unit tests in `src/core/tests/test_hazard_safeguarding_clock_owner_76.py` and `src/api/tests/test_hazard_safeguarding_clock_owner_api_76.py`, validate under the focused tier (`ruff check`, `ruff format --check`, `mypy`, `unittest` across `src/core` and `src/api`), and commit locally with `Refs #76` and the Copilot trailer without pushing (`Caller intake brief`, `.github/copilot-instructions.md`).

## Goals

* Project unified, deterministic clock and named accountable-owner fields on every hazard and safeguarding item across `Store`, `SqlStore`, `MssqlStore`, queue projections, and case card detail responses.
* Render the clock and named accountable owner (including fail-closed missing-timestamp state and unallocated escalation-owner state) across `My cases today`, `All open cases`, specialist role queues, and case cards without modifying `web/role-screens.js`.
* Prove semantic behavior and backward compatibility through focused core and API/UI unit tests while keeping all existing unit, accessibility, and export baseline suites passing.

## Scope and Non-Goals

### In Scope

* Shared hazard and safeguarding item normalization, statutory/operational reference clock calculation, and roster-backed named/escalation owner resolution in `src/core/src/zava_forward/core/taskqueues.py` and `workflows.py`.
* Wiring staff roster and safeguarding summary/detail projection through `store.py`, `sqlstore.py`, `insights.py`, `ranking.py`, and `projection.py` while preserving contractor allowlist redaction and `hold_notes` free-text withholding.
* Self-contained UI display updates in `src/api/src/zava_forward/api/web/app.js` (`HAZ_CATEGORIES`, `workSummary`, `safetyPanel`) after loading `web-design-guidelines`.
* Focused unit tests in `src/core/tests/test_hazard_safeguarding_clock_owner_76.py` and `src/api/tests/test_hazard_safeguarding_clock_owner_api_76.py`, plus concise documentation updates in `src/core/README.md` and `src/api/README.md`.

### Non-Goals

* Modifying `src/api/src/zava_forward/api/web/role-screens.js`.
* Replacing external hazard-service statutory authority (`RULE-003` / `CON-001`) or exposing staff hazard/safeguarding data to contractors or resident preview (`PR-002`).
* Pushing commits or opening/updating a remote pull request.

## Functional Requirements

* FR-1: Unified hazard and safeguarding item extraction and categorisation.
  * Support `"Safeguarding"` in `HAZARD_CATEGORIES` (`workflows.py`) and `HAZ_CATEGORIES` (`web/app.js`), bump `taskqueues.MEMBERSHIP_REVISION` from `3` to `4`, and extract active and recorded safeguarding items from `case["safeguarding_items"]` (`list[dict]`), `case["safeguarding"]` (`list[dict]` or `dict` containing at least one item-identifying key in `{"id", "status", "state", "priority", "category", "kind", "aware_at", "raised_at", "reported_at", "noticed", "response_due_at", "due_at", "owner", "named_owner", "sender", "destination", "accepted_by", "referred", "repaired", "released"}`), and `case["hazards"]` items with `category == "Safeguarding"` or `kind == "safeguarding"`.
  * Observable acceptance criteria: Cases with either hazard items or safeguarding items surface aligned open safety status (`hazard=True`, `safeguarding=True`), `Store.counts()["hazards"] == SqlStore.counts()["hazards"]`, `work["hazard_clocks"]`, `work["safeguarding_clocks"]`, `detail["hazards"]` (appending normalized standalone safeguarding items with `standalone_safeguarding=True` and scalar `owner` backfilled so unmodified `role-screens.js` never shows `"Mismatch"` or `"Owner: Unknown"`), and `detail["safeguarding_items"]` across `Store` and `SqlStore`, while note-only `safeguarding={"note": "..."}` fixtures remain passive.
* FR-2: Deterministic fail-closed statutory/operational clock projection.
  * Every projected hazard and safeguarding item includes `item_kind` (`"hazard"` | `"safeguarding"`), `clock_label`, `clock_status` (`"running"` | `"overdue"` | `"completed"` | `"fail_closed_missing_timestamp"`), `clock_deadline_utc` (ISO-8601 UTC `...Z` or `None`), `clock_remaining_hours` (`float` rounded to 0.1h or `None`), and `clock_basis` (`"recorded_service_deadline"` | `"operational_reference_from_awareness"` | `"missing_timestamp_fail_closed"`). `overdue_tasks(...)` evaluates recorded `response_due_at`/`due_at` and `resident_update_due_at` on open standalone safeguarding items while keeping derived awareness-only clocks out of `overdue_tasks` when `response_due_at` is unrecorded.
  * Target reference windows when external `response_due_at`/`due_at` is absent and `aware_at <= as_of` is valid: 24h for `Emergency`/`P1` hazards (`"Awaab's Law 24h emergency action clock (recorded reference)"`), 168h (7d) for pre-acceptance `Significant` or unrecorded-priority hazards (`"Operational 7d hazard investigation clock (recorded reference)"`), 336h (14d) for accepted `Significant` or `Routine` hazards (`"Operational 14d work-start clock (recorded reference)"`), 24h for `Emergency`/`Immediate`/`Urgent`/`P1` safeguarding items (`"Safeguarding 24h emergency response clock"`), and 48h for standard safeguarding referrals (`"Safeguarding 48h referral response clock"`).
  * Observable acceptance criteria: Valid recorded `response_due_at` takes precedence; valid `aware_at` computes deterministic UTC deadline and remaining hours; `responded_at <= as_of` yields `clock_status == "completed"`; missing, unparseable, naive, or future timestamps yield `clock_status == "fail_closed_missing_timestamp"` with `clock_deadline_utc is None` and `clock_remaining_hours is None`.
* FR-3: Non-blank named accountable owner and escalation owner projection (`FR-003` receipt-is-not-acceptance).
  * Every projected hazard and safeguarding item includes `named_owner`, `accountable_owner`, `owner_role`, `owner_id`, `unassigned` (`bool`), `escalation_owner`, `escalation_owner_role`, and `escalation_owner_id`, while preserving legacy `owner` (`"Unknown"` when direct follow-up is unrecorded) and `owner_named` (`bool`) on `work["hazard_clocks"]`.
  * Direct owner resolution respects `FR-003`: `accepted_by -> (destination only when accepted_at is truthy) -> sender -> follow_up -> owner -> named_owner`. Unaccepted `destination` serves only as the first candidate for `escalation_owner` (`destination -> named case owner -> named safety-role staff member -> named duty-lead fallback`), with `Store._work_context` passing `staff=data.get("staff") or list(self.staff.values())` so `SqlStore` refreshes always see the staff roster.
  * Observable acceptance criteria: Sent or received-but-unaccepted referrals keep `sender` as `named_owner` (`unassigned is False`); unallocated items set `unassigned is True` and promote `escalation_owner` into `named_owner` and `accountable_owner`; neither `named_owner`, `accountable_owner`, `owner_role`, `owner_id`, nor `escalation_owner` is ever empty, `None`, `"Unknown"`, or `"Anonymous"`.
* FR-4: Cross-surface API and plain-language UI rendering without editing `role-screens.js`.
  * `workSummary(work)`, `caseView(id)` (`openHaz` across open `c.hazards` and open `c.safeguarding_items`), and `safetyPanel(c, id, refresh)` (with deduplicated read-only cards for `standalone_safeguarding` items and deterministic client-side fallback `.safety-clock-owner` on raw test fixtures) in `web/app.js` render the clock and named accountable owner across `My cases today`, `All open cases`, specialist role screens, and case cards.
  * Observable acceptance criteria: `page_cases` `work` equals `detail["work"]` (`FR-034`); `workSummary` renders cleanly in Node VM tests without `undefined`/`NaN`; `safetyPanel` preserves 4 `<dt>` rows in `.safety-facts` without `"Unknown"`; all added copy and comments in `web/app.js` exclude every `CopyAudit` banned pattern (`\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b`); `projection.hold_notes` redacts `NOTE_KEYS` plus `summary`/`reason`/`source`/`job` on safety/safeguarding items for non-reason staff; `web/role-screens.js` has zero diff.

## Non-Functional Requirements

* NFR-1: Privacy and role-projection safety (`PR-002`, `SA-007`).
  * Objective threshold or evaluation condition: 0 contractor responses contain `work`, `hazard`, `safeguarding`, `hazards`, or `safeguarding_items`; 0 non-reason staff responses expose raw `safeguarding` free-text `note`/`source`/`job` (replaced with `NOTE_HELD`), while 100% of staff responses retain structured clock and named-owner fields.
  * Operating condition or verification approach, if needed: Unit assertions across contractor, `Grants and Evidence Officer` (`can_see_reason=False`), and `Building Safety Liaison` (`can_see_reason=True`) projections plus `test_resident_preview.py`.
  * Observable acceptance criteria: Contractor and resident-preview allowlists leak zero canary strings while all staff roles see clock and named owner.
* NFR-2: Zero baseline guard and static-analysis regression.
  * Objective threshold or evaluation condition: 0 lint, format, typecheck, or unit-test failures across `src/core` and `src/api`, with exact counted guards preserved (`INVALID_ATTR_FLOOR >= 8`, `DATA_TABLE_COUNT == 13`, `FIXED_RULE_CAP <= 2`, 0 `RAW_ERROR` matches).
  * Operating condition or verification approach, if needed: Run `ruff check`, `ruff format --check`, `mypy`, and `python3 -m unittest discover -s tests -q` in `src/core` and `src/api`.
  * Observable acceptance criteria: All commands exit 0 and `git diff --name-only` excludes `src/api/src/zava_forward/api/web/role-screens.js`.
* NFR-3: Locked test budget and ownership.
  * Objective threshold or evaluation condition: Exact test removals = `none`; maximum new test files = `2` (`src/core/tests/test_hazard_safeguarding_clock_owner_76.py` for core/SQL semantic and edge-case coverage; `src/api/tests/test_hazard_safeguarding_clock_owner_api_76.py` for API endpoint, role-redaction, and `app.js` `workSummary`/`safetyPanel` DOM rendering coverage).
  * Operating condition or verification approach, if needed: Inspect test suite file list and run full `unittest` discovery in both packages.
  * Observable acceptance criteria: Both new test suites fail without the implementation and pass alongside every existing regression suite.

## Acceptance Criteria

* AC-1: Every active hazard and safeguarding item in `Store.page_cases`, `SqlStore.page_cases`, and `Store.detail` exposes `clock_label`, `clock_status`, `clock_deadline_utc`, `clock_remaining_hours`, `named_owner`, `accountable_owner`, `owner_role`, `owner_id`, `unassigned`, `escalation_owner`, `escalation_owner_role`, and `escalation_owner_id`, with exact `FR-034` agreement between queue rows and case detail.
* AC-2: Missing, unparseable, naive, or future timestamps never fabricate an open on-time clock from stage dates; they fail closed with `clock_status == "fail_closed_missing_timestamp"`, `clock_deadline_utc is None`, and `clock_remaining_hours is None`.
* AC-3: Unallocated hazard and safeguarding items never leave `named_owner`, `accountable_owner`, `owner_role`, or `owner_id` blank, `"Unknown"`, or anonymous; they set `unassigned is True` and surface the named `escalation_owner`, while preserving legacy `clock["owner"] == "Unknown"` and `clock["owner_named"] is False`.
* AC-4: `workSummary(work)` and `safetyPanel(c, id, refresh)` in `web/app.js` render both the clock and named accountable owner (including fail-closed and unassigned escalation states and standalone safeguarding items) across `My cases today`, `All open cases`, specialist role queues, and case cards without modifying `web/role-screens.js` or violating `SA-003` plain-language rules.
* AC-5: `ruff check`, `ruff format --check`, `mypy`, and `unittest` pass in `src/core` and `src/api`, including `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_list_export_inventory.py`, `test_role_screens.py`, `test_safety_panel_ux.py`, and `test_resident_preview.py`.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-plan.md                                                                      |
| Phase details                    | .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-phase-details.md                                                           |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/ux-76-hazard-clock-owner-plan-critique.md with Revise disposition (`PC-001`..`PC-005` resolved directly) |
| Relevant research                | .copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-research.md                                                               |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-changes.md is created or continued by implementation as its evidence record |
| Planning execution and readiness | Complete and Ready for implementation (`PC-001`..`PC-005` incorporated)                                                                  |
| Continuation context             | Confirmed automatic RPI Agent parent transitions directly to `rpi-implement`                                                             |

## Sources

* .copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-research.md: Primary Cycle 1 evidence (`C1`–`C18`), contrarian test-guard findings, and convergence selection (Option A).
* docs/prds/zava-forward-retrofit-programme-demonstrator.md: `SA-001`..`SA-003`, `SA-007`, `FR-003`, `FR-004`, `FR-032`, `FR-034`, `CON-001`, and `PR-002` requirements.
* docs/reference/regulatory/building-safety-awaabs-law/2025-10-27-hazards-in-social-housing-prescribed-requirements-england-regulations-2025.xml: Statutory Awaab's Law Phase 1 24h emergency and investigation/make-safe context (`SI 2025/1042`).
* src/core/src/zava_forward/core/taskqueues.py, workflows.py, store.py, sqlstore.py, projection.py: Canonical queue and case-card projection modules.
* src/api/src/zava_forward/api/web/app.js and src/api/tests/: Canonical UI consumer and regression/baseline guard suites.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Core Hazard and Safeguarding Clock and Named-Owner Projection

* Intent: Build the shared clock and accountable-owner projection for hazards and safeguarding items and wire it across `taskqueues.py`, `workflows.py`, `store.py`, `sqlstore.py`, `insights.py`, `ranking.py`, and `projection.py`.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement unified clock, accountable-owner, and safeguarding item helpers in `taskqueues.py` and `workflows.py`

* Requirement and evidence: FR-1, FR-2, FR-3; research `C1`–`C3`, `C8`, `C9`, `C12`, `C16`
* Expected result: `taskqueues.py` exports deterministic safeguarding extraction, open-safety helpers, and `project_safety_clock_and_owner(...)` computing fail-closed clocks and non-blank named/escalation owners; `taskqueues.context(...)` populates enriched `hazard_clocks`, `safeguarding_clocks`, and `safety_items` plus safeguarding overdue deadlines; `workflows.py` adds `"Safeguarding"` to `HAZARD_CATEGORIES` and enriches `hazard_view(...)` and `safeguarding_view(...)`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Wire staff roster, safeguarding case-card detail, redaction, and SQL store parity

* Requirement and evidence: FR-1, FR-4, NFR-1; research `C5`, `C6`, `C10`, `C11`, `C14`, `C16`
* Expected result: `Store.summary`, `Store._work_context`, `Store.focus`, `Store.detail`, `SqlStore._row`, `insights.has_hazard`, `ranking._hazard`, and `projection.hold_notes` consistently project hazard and safeguarding clocks and named owners across JSON and SQLite/MSSQL stores while redacting free-text notes for non-reason staff and withholding safety structures from contractors.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Web Queue and Case Card Display Without Modifying `role-screens.js`

* Intent: Render statutory/operational clocks and named accountable owners on queue rows (`My cases today`, `All open cases`, and all `role-screens.js` queues) and case cards (`safetyPanel`) in `web/app.js` following `web-design-guidelines` and `SA-003`.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Load `web-design-guidelines` and update `workSummary` and `safetyPanel` in `web/app.js`

* Requirement and evidence: FR-4, NFR-2; research `C7`, `C13`, `C14`, `C15`, `C17`, `C18`; `.github/copilot-instructions.md` Web Development Guidance
* Expected result: `HAZ_CATEGORIES` includes `"Safeguarding"`; self-contained `workSummary(work)` renders clock and accountable/escalation owner details cleanly for full and legacy fixtures; `safetyPanel` renders `<p class="safety-clock-owner">` on hazard items (preserving 4 `<dt>` rows in `.safety-facts`) and renders standalone `c.safeguarding_items` when present; `web/role-screens.js` remains untouched.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Focused Core and API/UI Unit Tests and Component Documentation

* Intent: Prove every clock, named-owner, escalation, safeguarding, redaction, `FR-034`, and UI rendering invariant in focused unit tests and update component READMEs.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Add `src/core/tests/test_hazard_safeguarding_clock_owner_76.py`

* Requirement and evidence: AC-1, AC-2, AC-3, NFR-1, NFR-3; research `C8`–`C12`, `C16`
* Expected result: Focused unit tests verify 24h/7d/14d hazard clocks, 24h/48h safeguarding clocks, external `response_due_at` precedence, completed/overdue/running states, fail-closed missing/invalid/future timestamp states, allocated vs unallocated escalation owners, contractor/non-reason redaction, canary passive-note safety, and `Store` vs `SqlStore` `FR-034` parity.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Add `src/api/tests/test_hazard_safeguarding_clock_owner_api_76.py` and update READMEs

* Requirement and evidence: AC-1, AC-4, NFR-2, NFR-3; research `C4`, `C6`, `C7`, `C13`–`C15`
* Expected result: Focused API and Node DOM tests verify `/api/cases` (`mine`, `all`, role queues) and `/api/cases/{id}` responses plus `workSummary` and `safetyPanel` rendering of hazard and safeguarding clocks and named/escalation owners without touching `role-screens.js`; `src/core/README.md` and `src/api/README.md` document the clock and named-owner contract.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-phase-details.md

<!-- rpi:phase id=P04 -->
### [x] P04: Focused-Tier Validation and Guard Verification

* Intent: Run complete focused-tier linters, formatters, typecheckers, and unit test suites across `src/core` and `src/api`, verifying all baseline guards and `role-screens.js` non-modification before Review.
* Dependencies: P01, P02, P03

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Execute `ruff`, `mypy`, and `unittest` across `src/core` and `src/api` and reconcile artifacts

* Requirement and evidence: AC-5, NFR-2; `.github/copilot-instructions.md`; critique `PC-003`, `PC-004`, `PC-005`
* Expected result: `ruff check`, `ruff format --check`, `mypy`, and `unittest` pass with 0 errors across `src/core` and `src/api` (including `test_sqlqueues.py`, `test_resident_preview.py`, `test_resident_preview_api.py`, `test_content_standard.py`, `test_role_endpoint_inventory.py`, `test_role_screens.py`, `test_safety_panel_ux.py`, and the 3 counted baseline suites); `git diff --name-status` confirms `web/role-screens.js` is unchanged, test removals `0`, and new test files `<= 2`; `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-changes.md` and plan checklist markers are reconciled for `rpi-review` and subsequent local `Refs #76` commit (configured with privacy-safe `gh api user` noreply email and Copilot trailer, without pushing).
* Detail section: P04-T01 in .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-phase-details.md

## Dependencies

* `zava_forward.core` editable/installed distribution in environment: `src/api` imports `zava_forward.core.taskqueues`, `store`, `sqlstore`, `workflows`, and `projection`.
* Node.js runtime (`node`): Used by `src/api/tests/test_role_screens.py`, `test_safety_panel_ux.py`, and `test_hazard_safeguarding_clock_owner_api_76.py` to execute real `web/app.js` rendering slices.
* `web-design-guidelines` skill: Must be loaded and checked prior to editing `src/api/src/zava_forward/api/web/app.js` and refreshed/reviewed during `rpi-review`.

## Critique Disposition

Single final-candidate critique completed in `.copilot-tracking/reviews/plans/2026-11-15/ux-76-hazard-clock-owner-plan-critique.md` (`Verdict: Revise`). All five findings were resolved directly in this plan and phase details without requiring user decisions or a second critique pass.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Run 1 / `PC-001` (High)  | Resolved    | Updated `FR-1`, `FR-4`, `P01-T02`, `P02-T01`, and `P03-T02` to project normalized standalone safeguarding items into both `d["safeguarding_items"]` and `d["hazards"]` (`standalone_safeguarding=True`) with scalar `owner` backfilled from `named_owner`, extend `caseView` `openHaz`, and deduplicate read-only rendering in `safetyPanel` so unmodified `role-screens.js` never shows `"Mismatch"` or `"Owner: Unknown"`. |
| Run 1 / `PC-002` (High)  | Resolved    | Updated `FR-3`, `P01-T01`, and `P03-T01` to gate `destination` on `accepted_at` (`accepted_by -> destination if accepted_at -> sender -> follow_up -> owner -> named_owner`), preserving `FR-003` receipt-is-not-acceptance. |
| Run 1 / `PC-003` (High)  | Resolved    | Updated `FR-1`, `FR-2`, `FR-3`, `P01-T01`, `P01-T02`, and `P04-T01` to bump `MEMBERSHIP_REVISION = 4`, pass `staff=data.get("staff") or list(self.staff.values())` in `Store._work_context`, add standalone safeguarding recorded deadlines to `overdue_tasks`, align `Store.counts`/`gate_reasons`/`status_line`/`focus`/`require_safety_clear` with safe lookups, and enforce explicit item-identifying keys on `safeguarding` dicts. |
| Run 1 / `PC-004` (Medium)| Resolved    | Updated `FR-4`, `P01-T02`, `P02-T01`, and `P04-T01` to enforce the full `CopyAudit` banned regex (`\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b`), redact `summary`/`reason`/`source`/`job` in `projection.hold_notes` for non-reason staff, and compute deterministic client-side fallback `.safety-clock-owner` on raw `safetyPanel` fixtures. |
| Run 1 / `PC-005` (Medium)| Resolved    | Updated `P04-T01` and closeout flow to verify diff boundaries and execute the post-Review local commit with `gh api user` noreply email, `Refs #76`, and the Copilot trailer without pushing. |
| Residual risk            | Accepted with risk | Later Awaab's Law 5-working-day written-summary and 12-week preventative-works milestones are not separate timestamps in current synthetic fixtures; displaying recorded service deadlines alongside 24h/7d/14d operational awareness clocks and fail-closed states keeps timing claims transparent without inventing unrecorded statutory dates. |

## Follow-Up Items

* None

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-changes.md
* Ready phase or task: Review (`P01`–`P04` complete)
* Remaining provisional question or blocker: None
