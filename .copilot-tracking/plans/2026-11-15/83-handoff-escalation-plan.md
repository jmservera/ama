<!-- markdownlint-disable-file -->
# RPI Plan: Issue 83 Unaccepted Handoff Visibility and SLA Escalation (BG-010)

## Task Metadata

* Task ID: 83-handoff-escalation
* Task slug: 83-handoff-escalation
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/83-handoff-escalation-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/83-handoff-escalation-plan-critique.md

## Executive Summary

Deliver the remaining acceptance criterion of Issue #83 (`Unaccepted handoffs are visible and escalated within approved times (BG-010)`) across `zava_forward.core` and `zava_forward.api` without touching `web/role-screens.js`. The plan introduces deterministic, owner-approved `BG-010` SLA evaluation (`approved_handoff_policy` and `handoff_sla`), surfaces escalation status, elapsed/overdue hours, escalation target, accountable owner, and escalation next action in both case (`detail["handoff"]`) and shared queue (`work["handoff"]`, `work["overdue"]`, `work["queues"]`, `work["next_action"]`) projections, provides shared/role-owned queue views (`unowned_handoffs`, `unaccepted_handoffs`, `escalated_handoffs`), and adds an idempotent, audited overdue escalation sweep (`escalate_overdue_handoffs`).

### User Decisions and Requirements Highlights

* Deliver `- [ ] Unaccepted handoffs are visible and escalated within approved times (BG-010)` on branch `feat/ux-83-handoff-escalation` without pushing.
* Deterministically evaluate `sent` (`Offered`) and `received` (`Received`) unaccepted handoffs against approved `BG-010` SLA thresholds and per-handoff `due_at` deadlines, exposing escalation status, elapsed/overdue hours, escalation target/accountable owner, and next action in case and queue projections.
* Surface unaccepted work across shared/role queues (`unowned_handoffs`, `unaccepted_handoffs`, `escalated_handoffs`) so no handoff sits unaccepted silently.
* Avoid modifying `src/api/src/zava_forward/api/web/role-screens.js` to prevent counted WCAG baseline conflicts.
* Validate under the Focused tier (`ruff check`, `ruff format --check`, `mypy`, `unittest` in `src/core` and `src/api`) with focused tests in `src/core/tests/test_handoff_escalation_83.py` and `src/api/tests/`.

### What You May Not Know

* `test_unaccepted_handoff_csv_api.py`, `test_handoff_api.py`, and `web/app.js` enforce exact 13-column CSV parity on `handoff_ageing` and require `approved_limit_hours` to stay `None` (`"Approved escalation time not set (OD-09)"`) when no approved `handoff_policy` is present on `store.data`. Policy-gating (`status == "Approved"`, named human `owner`, positive finite `acceptance_hours`) satisfies both `BG-010` and `OD-09`.
* `SqlStore` and `MssqlStore` persist 6 fixed `queue_*` columns (`QUEUE_COLS`); wiring `effective_due_at` (`due_at` or `sla_due_at`) into `taskqueues.overdue_tasks` and adding `handoff_policy` to `sqlstore._queue_fingerprint` (with bumped `taskqueues.MEMBERSHIP_REVISION`) keeps SQLite and in-memory queue memberships identical without DDL schema changes.
* `test_role_endpoint_inventory.py` inspects `server.py` for every `/api/...` route and runs 9-role free-text canary checks (`PR-002`, Issue #116). Every new `/api/handoffs/*` endpoint must apply `projection.hold_notes` for roles outside `reason_roles()` and be registered in `GET_ENDPOINTS` / `POST_ENDPOINTS`.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Deliver the remaining unchecked acceptance criterion on Issue #83: `Unaccepted handoffs are visible and escalated within approved times (BG-010)` (caller prompt; GitHub Issue #83).
* Inspect and extend role-owned handoffs (`sent`, `received`, `accepted`, `rejected`, `escalated`, `completed`) and `BG-010` SLA/escalation windows in `src/core/src/zava_forward/core/` and `src/api/src/zava_forward/api/` (caller prompt).
* Ensure unaccepted handoffs (`sent` or `received` and not yet `accepted`/`rejected`/`completed` within the approved SLA window) are deterministically evaluated against the approved handoff acceptance time threshold (`BG-010`), automatically or explicitly flagged/transitioned as overdue/escalated with visible escalation status, elapsed/overdue hours, escalation target/accountable owner, and next action in queue and case projections, and visible in shared/role queues (`unowned_handoffs`, `unaccepted_handoffs`, `escalated_handoffs`) (caller prompt; `.copilot-tracking/research/2026-11-15/83-handoff-escalation-research.md`).
* Avoid modifying `src/api/src/zava_forward/api/web/role-screens.js` so counted baseline guards do not conflict with active role-screen WCAG branches (caller prompt).
* Add focused unit tests in `src/core/tests/test_handoff_escalation_83.py` and `src/api/tests/` proving visibility and timely escalation of unaccepted handoffs (`BG-010`), and run `ruff check`, `ruff format --check`, `mypy`, and `unittest` across modified projects (caller prompt).
* Commit all changes and `.copilot-tracking/` artifacts on `feat/ux-83-handoff-escalation` with `Refs #83` and Copilot co-author trailer without pushing, leaving `git status --short` empty (caller prompt).

## Goals

* Provide deterministic `BG-010` SLA threshold resolution and breach evaluation for unaccepted handoffs without fabricating unapproved limits on datasets where `OD-09` remains open.
* Surface actionable SLA and escalation fields (`escalation_status`, `elapsed_hours`, `overdue_hours`, `approved_limit_hours`, `sla_due_at`, `effective_due_at`, `escalation_target`, `accountable_owner`, and deterministic `escalation_next_action`) in case detail and shared work-queue projections without colliding with `projection.NOTE_KEYS` redaction on `next_action`.
* Eliminate silent unaccepted handoffs by providing role-scoped and manager-visible `unowned_handoffs`, `unaccepted_handoffs`, and `escalated_handoffs` queues plus an idempotent, audited overdue escalation transition sweep (`escalate_overdue_handoffs`).
* Maintain 100% compatibility with existing CSV exports, `SqlStore` queue parity, `PR-002` role-based note redaction, and `web/role-screens.js` WCAG guards.

## Scope and Non-Goals

### In Scope

* `src/core/src/zava_forward/core/workflows.py`: `approved_handoff_policy`, `approved_handoff_limit_hours`, `handoff_sla`, enriched `handoff_view`, policy-aware `handoff_ageing` (retaining exact 13 `FIELDS`), `unaccepted_handoffs`, `unowned_handoffs`, `escalated_handoffs`, and `escalate_overdue_handoffs`.
* `src/core/src/zava_forward/core/taskqueues.py`, `store.py`, `sqlstore.py`, `exception_register.py`, and `src/api/src/zava_forward/api/progress.py`: SLA-backed overdue task evaluation, enriched `work["handoff"]` and overdue/escalated `work["next_action"]`, `MEMBERSHIP_REVISION` bump, `_queue_fingerprint` policy inclusion, and policy-backed `ExceptionRegister` stranded-handoff feeding.
* `src/api/src/zava_forward/api/server.py`: `GET /api/handoffs/unowned`, `GET /api/handoffs/escalated`, and `POST /api/handoffs/escalate-overdue`.
* Focused core and API unit test suites (`src/core/tests/test_handoff_escalation_83.py`, `src/api/tests/test_handoff_escalation_api_83.py`) and route registration in `src/api/tests/test_role_endpoint_inventory.py`.

### Non-Goals

* Modifying `src/api/src/zava_forward/api/web/role-screens.js` or other frontend JS bundles.
* Adding new DDL columns to `SqlStore` / `MssqlStore` `QUEUE_COLS`.
* Inventing a hardcoded SLA threshold when `handoff_policy` is absent or unapproved (`OD-09`).
* Transferring accountable case ownership (`c["owner"]`) during escalation prior to explicit receiver acceptance (`accept_handoff`).
* Pushing commits or opening/updating remote GitHub pull requests.

## Functional Requirements

* **FR-1 (Approved BG-010 SLA Resolution)**: Resolve approved handoff acceptance limits from `handoff_policy` only when `status == "Approved"`, `owner` names a real person (not blank, `"Unknown"`, or `"to be named"`), and `acceptance_hours` is a positive finite number (using `urgent_acceptance_hours` when `urgency == "Urgent"` and configured); allow explicit `max_age_hours` query override and preserve `None` / `"Approved escalation time not set (OD-09)"` when unapproved.
  * Observable acceptance criteria: Approved routine and urgent `BG-010` windows evaluate deterministically; draft/unowned/missing policies return `approved_limit_hours=None` and keep existing `OD-09` tests passing.
* **FR-2 (Deterministic SLA & Case/Queue Projections)**: Compute `escalation_status`, `elapsed_hours`, `overdue_hours`, `approved_limit_hours`, `sla_due_at`, `effective_due_at` (earlier UTC instant of `due_at` and `sla_due_at`), `overdue` (using exact elapsed seconds `> limit * 3600`), `needs_escalation`, `escalation_target`, `escalation_target_code`, `escalation_target_role`, `accountable_owner`, and deterministic `escalation_next_action` in `handoff_view` and `taskqueues.context` (`work["handoff"]`), add breached `effective_due_at` handoffs to `taskqueues.overdue_tasks` (`work["overdue"]` and `overdue` queue), persist `"handoff_policy"` in `SqlStore.DOCS` / `_refresh_queue_membership` / `save` / `_queue_fingerprint` and `Store._queue_candidates` with `MEMBERSHIP_REVISION = 4`, and surface `escalation_next_action` in default pending-handoff `work["next_action"]` when overdue or escalated.
  * Observable acceptance criteria: Both `store.detail(cid, user)` and `store.list_cases(user, ...)` (`Store` and `SqlStore`, across seed/save/reopen) display consistent SLA status, elapsed/overdue hours, escalation target, accountable sender ownership, `unowned` + `overdue` queue flags, unredacted `escalation_next_action` for coordinators/PSO, and redacted `NOTE_HELD` on staff free-text `next_action`/`answer_note`.
* **FR-3 (Shared/Role Handoff Queues & Exception Feed)**: Provide `unowned_handoffs`, `unaccepted_handoffs`, and `escalated_handoffs` on `WorkflowMixin` (and `GET /api/handoffs/unowned`, `GET /api/handoffs/escalated` registered in `server.get_kind` as `"handoffs"`), scoping visibility to sender (`from_code`), proposed receiver (`to_code`), destination role (`to_role` on `unowned_handoffs`/`escalated_handoffs`, and role-only `not to_code and to_role == user["role"]` on `pending_handoffs`/`unaccepted_handoffs`), escalation target (`escalation_owner_code` / `escalation_target_role`), and `MANAGER_ROLES`, while keeping `handoff_ageing` / `/api/handoffs/unaccepted(.csv)` at its exact 13 `FIELDS` and feeding policy-breached handoffs into `ExceptionRegister`.
  * Observable acceptance criteria: Colleagues in the destination role, escalation targets, and managers see unowned and overdue/escalated handoffs via core methods and HTTP endpoints; named-colleague `unaccepted_handoffs` privacy and 13-column `/api/handoffs/unaccepted.csv` parity remain intact.
* **FR-4 (Controlled Overdue Escalation Sweep)**: Provide `WorkflowMixin.escalate_overdue_handoffs(user, *, as_of=None, max_age_hours=None, reason=None)` and `POST /api/handoffs/escalate-overdue` (verifying `MANAGER_ROLES` before body parameter validation) to deterministically transition all overdue `Offered`/`Received` handoffs to `state == "Escalated"` using `change_provenance.controlled`, `answer_note`, `self._handoff_event(..., auto_escalated=True)`, and `self._save_workflow(..., "handoff_escalated", ...)` without changing `c["owner"]` or re-escalating already-`Escalated` handoffs.
  * Observable acceptance criteria: Overdue `Sent` and `Received` handoffs transition to `Escalated` in one deterministic sweep, audit hash chain remains valid, `c["owner"]` remains the sender, and a repeat sweep at the same `as_of` transitions zero additional cases.

## Non-Functional Requirements

* **NFR-1 (Role-Based Privacy & Canary Redaction - PR-002)**: All new projection fields and HTTP endpoints enforce default-deny staff gating and `projection.hold_notes` redaction for roles outside `projection.reason_roles()`.
  * Objective threshold or evaluation condition: Zero leakage of `NOTE_CANARY`, `OUTCOME_CANARY`, `REASON`, `PHONE`, or `RESIDENT` across all 9 roles in `test_role_endpoint_inventory.py`.
  * Operating condition or verification approach, if needed: Run `RoleEndpointInventory` and new API role-redaction tests.
  * Observable acceptance criteria: Restricted staff roles receive `NOTE_HELD` on free-text keys, contractors receive `403`, and structured `escalation_action` never echoes raw staff free text.
* **NFR-2 (Determinism, Store Parity, and Static Type/Lint Hygiene)**: Time evaluation requires valid `YYYY-MM-DD` snapshot dates or timezone-aware ISO timestamps (`ValueError` on naive datetimes with time components), `Store` and `SqlStore` produce identical queue memberships, and modified projects pass type-checking and linting cleanly.
  * Objective threshold or evaluation condition: Zero errors in `ruff check`, `ruff format --check`, `mypy`, and `unittest` across `src/core` and `src/api`; zero edits to `web/role-screens.js`.
  * Operating condition or verification approach, if needed: Focused-tier local verification commands and `git diff --name-only`.
  * Observable acceptance criteria: All core and API unit tests, `mypy`, and `ruff` checks exit `0`, and `web/role-screens.js` is untouched.

## Acceptance Criteria

* Unaccepted handoffs (`Sent`/`Offered` and `Received`) are deterministically evaluated against approved `BG-010` acceptance windows (including urgency-specific limits when configured) and per-handoff `due_at` deadlines, while unconfigured datasets retain `OD-09` null limits.
* Overdue unaccepted handoffs automatically project `escalation_status`, `elapsed_hours`, `overdue_hours`, `escalation_target`, `accountable_owner`, `overdue` + `unowned` queue memberships, and escalation `next_action` across `detail["handoff"]` and `work["handoff"]` in both `Store` and `SqlStore`, and raise `stranded_task` items in `ExceptionRegister`.
* `escalate_overdue_handoffs` (and `POST /api/handoffs/escalate-overdue`) deterministically transitions overdue `Sent`/`Received` handoffs to `Escalated` with audit/provenance/history, preserves sender case ownership, and is idempotent.
* `unowned_handoffs`, `unaccepted_handoffs`, and `escalated_handoffs` (plus `GET /api/handoffs/unowned` and `GET /api/handoffs/escalated`) expose unaccepted and overdue/escalated handoffs to responsible parties, destination roles, escalation targets, and managers with `PR-002` note redaction, while preserving the 13-column `/api/handoffs/unaccepted.csv` contract.
* `src/api/src/zava_forward/api/web/role-screens.js` has zero modifications.
* Focused tests in `src/core/tests/test_handoff_escalation_83.py` and `src/api/tests/test_handoff_escalation_api_83.py`, plus full `src/core` and `src/api` `unittest`, `mypy`, `ruff check`, and `ruff format --check` runs, pass cleanly.

## Test Ownership and Validation Lock

* **Canonical test targets**:
  * Exact removals: `none`
  * Maximum new test files: `2` (`src/core/tests/test_handoff_escalation_83.py` for core SLA evaluation, projections, `Store`/`SqlStore` queue parity, shared/role queues, exception register integration, and sweep idempotency; `src/api/tests/test_handoff_escalation_api_83.py` for HTTP endpoints, role scoping, redaction, and CSV compatibility), plus route registration in existing `src/api/tests/test_role_endpoint_inventory.py`.
* **Semantic vs regression coverage**:
  * Semantic coverage (`test_handoff_escalation_83.py`, `test_handoff_escalation_api_83.py`): Tests deterministic `BG-010` routine/urgent threshold evaluation, unapproved `OD-09` non-fabrication, boundary exact-match vs +1s breach, `detail["handoff"]` and `work["handoff"]` escalation fields, `SqlStore` queue fingerprint refresh, destination-role visibility in `unowned_handoffs` and `escalated_handoffs`, `ExceptionRegister` auto-raise, and `escalate_overdue_handoffs` transition + ownership retention + audit integrity + idempotency.
  * Regression coverage: Existing `test_handoff_lifecycle.py`, `test_taskqueues.py`, `test_sqlqueues.py`, `test_exception_register.py`, `test_handoff_api.py`, `test_unaccepted_handoff_csv_api.py`, `test_handoff_waiting_view.py`, `test_role_endpoint_inventory.py`, and `test_list_export_inventory.py`.
* **Planned validation commands (Focused tier)**:
  * `ruff check src/core src/api && ruff format --check src/core src/api`
  * `mypy src/core/src src/core/tests/test_handoff_escalation_83.py src/api/src src/api/tests/test_handoff_escalation_api_83.py`
  * `cd src/core && python3 -m unittest discover -s tests -q`
  * `cd src/api && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -q`

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/83-handoff-escalation-plan.md                                                                         |
| Phase details                    | .copilot-tracking/details/2026-11-15/83-handoff-escalation-phase-details.md                                                              |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/83-handoff-escalation-plan-critique.md with Revise disposition (PC-001..PC-005 resolved directly) |
| Relevant research                | .copilot-tracking/research/2026-11-15/83-handoff-escalation-research.md                                                                  |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/83-handoff-escalation-changes.md is created by implementation as its evidence record                |
| Planning execution and readiness | Complete and Ready for implementation                                                                                                    |
| Continuation context             | Confirmed automatic RPI Agent parent continues to `rpi-implement` after single critique disposition                                      |

## Sources

* `.copilot-tracking/research/2026-11-15/83-handoff-escalation-research.md`: Primary three-wave research synthesis (`C1`..`C21`) establishing exact code contracts, invariants, and convergence architecture.
* `docs/case_study_48_addendum.md`: `EXA-008` operational timing model and sender accountability boundary.
* `docs/brds/agentic-retrofit-programme-brd.md` and `docs/prds/zava-forward-retrofit-programme-demonstrator.md`: `BG-010`, `FR-057`, `FR-011`, and `AC-014` requirements.
* `src/core/src/zava_forward/core/workflows.py`, `taskqueues.py`, `store.py`, `sqlstore.py`, `projection.py`, `exception_register.py`, and `src/api/src/zava_forward/api/server.py`: Target implementation modules.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Core BG-010 Handoff SLA Evaluation, Projections, Queues, and Overdue Sweep

* Intent: Implement policy-gated `BG-010` SLA evaluation, enrich case and shared work-queue projections, add `unowned_handoffs` and `escalated_handoffs` queues, wire `ExceptionRegister` and `SqlStore` queue refresh, and add `escalate_overdue_handoffs`.
* Dependencies: None.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement BG-010 SLA helpers, enriched handoff views, role queues, and overdue escalation sweep in workflows.py

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4, NFR-1 (`C1`..`C6`, `C12`..`C15`, `C18`).
* Expected result: `workflows.py` provides `approved_handoff_policy`, `approved_handoff_limit_hours`, `handoff_sla`, enriched `handoff_view`, policy-aware 13-key `handoff_ageing`, `pending_handoffs`, `unaccepted_handoffs`, `unowned_handoffs`, `escalated_handoffs`, and `escalate_overdue_handoffs` with full sender-ownership retention, audit/provenance recording, and `NOTE_HELD` redaction.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/83-handoff-escalation-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Wire BG-010 SLA deadlines and escalation fields into taskqueues, store, sqlstore, progress, and exception_register

* Requirement and evidence: FR-2, FR-3, NFR-1, NFR-2 (`C7`..`C10`, `C16`..`C18`).
* Expected result: `taskqueues.overdue_tasks` flags `effective_due_at` (`due_at` or `sla_due_at`) breaches, `taskqueues.context` projects full SLA/escalation metadata under `work["handoff"]` and escalation guidance in `work["next_action"]`, `store.py` / `progress.py` / `exception_register.py` pass dataset `as_of`, `handoff_policy`, and `staff`, and `sqlstore._queue_fingerprint` + bumped `MEMBERSHIP_REVISION` keep SQLite queue columns synchronized.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/83-handoff-escalation-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: HTTP API Handoff Queue and Escalation Sweep Routes

* Intent: Expose `unowned_handoffs`, `escalated_handoffs`, and `escalate_overdue_handoffs` via `zava_forward.api.server` under `PR-002` role gating without modifying `web/role-screens.js`.
* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add GET /api/handoffs/unowned, GET /api/handoffs/escalated, and POST /api/handoffs/escalate-overdue and register in role inventory

* Requirement and evidence: FR-3, FR-4, NFR-1 (`C11`, `C18`..`C20`).
* Expected result: `server.py` serves `GET /api/handoffs/unowned` and `GET /api/handoffs/escalated` (supporting optional `?max_age_hours=` and `?as_of=` query parameters with `400` validation on invalid inputs) for `STAFF_ROLES` and `POST /api/handoffs/escalate-overdue` for `MANAGER_ROLES` (`403` for non-manager staff and contractors), and `test_role_endpoint_inventory.py` covers all three routes with zero canary leaks.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/83-handoff-escalation-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Focused Unit Tests and Static/Runtime Verification

* Intent: Prove `BG-010` visibility, timely escalation, queue parity, redaction, and backward compatibility with focused core and API unit tests and Focused-tier checks.
* Dependencies: P01, P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Author focused unit tests in src/core/tests/test_handoff_escalation_83.py and src/api/tests/test_handoff_escalation_api_83.py

* Requirement and evidence: FR-1..FR-4, NFR-1, NFR-2 (caller requirement 4).
* Expected result: Comprehensive unit tests verify deterministic routine/urgent `BG-010` SLA evaluation, `OD-09` unapproved null preservation, boundary timing, `detail["handoff"]` and `work["handoff"]` projections, `Store` vs `SqlStore` `overdue`/`unowned` parity, `unowned_handoffs` / `unaccepted_handoffs` / `escalated_handoffs` role visibility and redaction, `ExceptionRegister` stranded-task feed, and `escalate_overdue_handoffs` sweep idempotency and audit integrity.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/83-handoff-escalation-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Execute Focused-tier validation across src/core and src/api and verify role-screens.js guard

* Requirement and evidence: NFR-2 (caller requirements 3 and 5).
* Expected result: `ruff check`, `ruff format --check`, `mypy`, and full `unittest` suites in `src/core` and `src/api` pass with zero errors, and `git diff --name-only` confirms `src/api/src/zava_forward/api/web/role-screens.js` is untouched.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/83-handoff-escalation-phase-details.md

## Dependencies

* `zava_forward.core` editable/installed distribution in environment: Required so `src/api` imports updated `workflows` and `taskqueues` functions seamlessly.
* Existing `projection.py` (`NOTE_KEYS`, `hold_notes`, `can_see_reason`) and `change_provenance.py` (`operation`): Reused directly for redaction and provenance enforcement.

## Critique Disposition

Single final-candidate critique completed (`.copilot-tracking/reviews/plans/2026-11-15/83-handoff-escalation-plan-critique.md`, verdict `Revise`); all five planner-owned findings were applied directly with no user decision required.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Run 1: PC-001 [Critical] (`SqlStore.DOCS` / queue refresh / `MEMBERSHIP_REVISION`) | Resolved | Added `"handoff_policy"` to `SqlStore.DOCS`, `_refresh_queue_membership`, `SqlStore.save` shared invalidation, `_queue_fingerprint`, `Store._work_context` (`data.get("handoff_policy")`), and `Store._queue_candidates`; bumped `taskqueues.MEMBERSHIP_REVISION` from `3` to `4`. |
| Run 1: PC-002 [High] (`escalate_overdue_handoffs` provenance, audit, and `answer_note`) | Resolved | Replaced `change_provenance.operation`, `self._audit`, and `escalation_reason` with `change_provenance.controlled`, `answer_note` (covered by `projection.NOTE_KEYS`), `self._handoff_event(..., auto_escalated=True)`, and `self._save_workflow(..., "handoff_escalated", ...)`. |
| Run 1: PC-003 [High] (`server.get_kind` registration and `_parse_max_age_hours` / role gate order) | Resolved | Specified `get_kind` entries (`"handoffs"`), `_max_age_hours(url)`, shared `_parse_max_age_hours(raw)`, and `MANAGER_ROLES` check before body parsing on `POST /api/handoffs/escalate-overdue`. |
| Run 1: PC-004 [High] (`escalation_next_action` vs `NOTE_KEYS` and `handoff_policy` / role-only visibility) | Resolved | Renamed deterministic SLA guidance to `escalation_next_action`, passed `handoff_policy` in `Store.unaccepted_handoffs`, `Store.pending_handoffs`, and `exception_register.py`, and added role-only (`not to_code`) + `escalation_owner_code` visibility predicates. |
| Run 1: PC-005 [Medium] (Exact-second `+1s` comparison, `min(due_at, sla_due_at)`, `_now()` defaults, missing-`offered_at` split) | Resolved | Specified exact elapsed-second SLA breach checks, full-precision `sla_due_at`, chronological `min(due_at, sla_due_at)` for `effective_due_at`, `_now()` defaults on live handoff queues/sweep, preserved `float(limit)` reason formatting, and tolerant `handoff_view` vs strict `handoff_ageing` missing-`offered_at` behavior. Accepted residual risk: default `DATA` remains without an active `handoff_policy` so `web/app.js` `waitingRows` (`approved_limit_hours === null`) stays untouched. |

## Follow-Up Items

* Owner sign-off of live operational escalation timings (`OD-09`) and human usability/accessibility journey validation (`NFR-008`, `NFR-009`) remain programme-level items outside Issue #83's software capability slice; if a live `ZF_DATA` deployment activates `handoff_policy` globally, relax `approved_limit_hours === null` in `web/app.js` `waitingRows` in a web-scoped change.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/83-handoff-escalation-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: None
