<!-- markdownlint-disable-file -->
# RPI Changes: Issue #154 Representative Task-Limited Views and Session Expiry

## Metadata

* Task ID: issue-154-rep-expiry-views
* Related plan: .copilot-tracking/plans/2026-11-15/issue-154-rep-expiry-views-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-154-rep-expiry-views-phase-details.md
* Implementation date: 2026-11-15
* Rebased base commit: `0c1fa1da4` (`origin/feat/demo-164-chat-grounding-provenance-0900`, incorporating PR #1761 `7f83f4749` and PR #1769 `0c1fa1da4`)
* Rebased feature commit: `3ed0c7deb` (replayed from `99a596629`, zero correction cycles spent)

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`)
* Completed scope markers: P01, P01-T01, P01-T02, P01-T03, P02, P02-T01, P02-T02, P03, P03-T01, P03-T02, P03-T03
* All remaining active-plan markers: none
* Status basis: Every phase and task in the declared full-plan scope has verified source, test, lint, format, and strict type-check completion evidence.

## Execution Summary

Implemented Issue #154 Criterion 3 (`Representative views show only task-limited authority and expire as recorded`, covering `FR-045`, `FR-046`, `NFR-008`, and `NFR-009`) across `src/core` and `src/api` without modifying `src/api/src/zava_forward/api/web/role-screens.js`. Created the canonical domain enforcement module `zava_forward.core.resident_journey_design`, extended `resident_decisions.py` with backwards-compatible UTC `expires_at` support alongside `review_date`, added frozen `RepresentativeShowcaseGrant` support in `resident_showcase.py` while leaving `ShowcaseRow`/`ROW_KEYS` untouched, wired representative session/view/assistant/agenda enforcement and immediate mid-session expiry into `resident_demo/app.py`, added role-gated `GET` and `POST /api/cases/<id>/representative-view` in `server.py`, and verified full domain and HTTP loopback test coverage plus clean `ruff check`, `ruff format --check`, and strict `mypy` runs across `src/core` and `src/api`.

## Completed Work

### Core Representative View Projection, Expiry Evaluation, and Session State Machine (`P01`: `P01-T01`, `P01-T02`, `P01-T03`)

* Created `src/core/src/zava_forward/core/resident_journey_design.py` implementing:
  * Strict UTC ISO-8601 `expires_at` parsing and ceiling comparison (`parse_utc_timestamp`, `utc_now`, `effective_expiry_timestamp`, `evaluate_representative_authority`) where effective expiry is `min(parsed_expires_at, review_dateT00:00:00Z)` when both exist, `review_dateT00:00:00Z` for legacy `review_date`-only domain grants, and fail-closed `missing_expiry` (`state="held"`) when explicit `expires_at` is null/malformed/naive or no expiry ceiling exists.
  * Positive-allowlist task projection (`project_representative_view`) evaluating `versions[-1]` per measure for valid `representative_ref` values (rejecting blank, overlong, and `"Unknown"` sentinels), returning only the allowlisted fields, `permitted_actions`, `journey_stages`, and `TASK_ASSISTANT_TOPICS` for `Receive information` (`R1`, `J4`), `Communicate` (`R1`, `J4`, representative-linked `J6`), `Attend` (`R1`, `J3` matched via `resident_bindings` with `offer["binding"]["home"]` stripped and `Offered - not booked` separated from three-party `Visit confirmed` per `FR-046`, plus `appointment_authorities` date-window check for `confirm_appointment`), and `Works decision` (`R1`, `J1`, `J2`), while omitting `home`, `sensors`, out-of-scope measures, household `documents`, unrelated complaints/handover/decisions, other representatives' permissions, and sensitive household/safe-contact notes.
  * Thread-safe `RepresentativeSession` and `RepresentativeSessionStore` (`open_session`, `record_session`, `session_view`, `session_action`) plus `enforce_representative_action` (`RepresentativeAccessBlockedError`, `RepresentativeScopeDeniedError`), immediately transitioning live sessions to `expired` or `held` (`active=False`, `permitted_actions=()`, `journey_stages=()`) when `now >= effective_expires_at` or authority becomes `Revoked`, `Disputed`, `Unclear`, `missing_expiry`, or invalidated by a changed `resident_safe_contact` or measure `context_revision`, surfacing recorded `expires_at` and plain-language non-digital `renewal_route`.
* Updated `src/core/src/zava_forward/core/resident_decisions.py` (`_res_representative_record`, `authority_for`, `representative_view`, `representative_action_check`, and `attach`) to accept optional UTC `expires_at` alongside `authority_date` and `review_date`, enforce UTC `expires_at` ceilings in `authority_for(..., now=None)` without breaking existing `controls.today()` callers, and expose lock-guarded `store.representative_view(...)` and `store.representative_action_check(...)`.
* Updated `src/core/src/zava_forward/core/resident_showcase.py` with `RepresentativeShowcaseGrant` (including `revoked`), `admit_representative_grant`, `representative_grant_evaluation`, and `representative_showcase_view` without altering `ShowcaseRow` or `ROW_KEYS`.

### HTTP Resident-Session and Case API Representative Expiry Enforcement (`P02`: `P02-T01`, `P02-T02`)

* Updated `src/api/src/zava_forward/api/resident_demo/app.py`:
  * Added `representative_grants`, `representative_resolver`, `rep_by_handle` (keyed by `SessionCodec.handle(grant.principal_subject)` for `rep:<case_id>:<representative_ref>`), `rep_sessions`, and `_live_grant_for_handle` so representative handles never collide with resident handles on the same case.
  * Enforced active unexpired grant admission on `POST /demo/login`, additive representative status fields (`subject_kind`, `representative_state`, `representative_reason`, `expires_at`, `renewal_route`, `permitted_tasks`, `journey_stages`) on `GET /demo/session` while keeping `csrf`, `session_id`, and `signed_in` intact across mid-session expiry so subsequent `POST` calls return `403` `expired`/`held` rather than `409` CSRF failures, task-limited projection on `GET /demo/view` (omitting internal `case_id` and `@example.com`), `TASK_ASSISTANT_TOPICS` and `grant.documents` scoping on `POST /demo/assistant`, and isolated callback owner keys (`resident_key(f"rep:{case_id}:{representative_ref}")`) plus live `authorised()` expiry re-checks on `POST /demo/agenda`.
* Updated `src/api/src/zava_forward/api/server.py` with `GET /api/cases/<id>/representative-view?representative_ref=...` (before generic `/api/cases/<id>`) and `POST /api/cases/<id>/representative-view` (gated by `projection.allowed(u, "case")` and `controls.RESIDENT_VIEW_ROLES` before `s._case(cid)`), returning `200` scoped projections or `expired`/`held` state views on `GET` and `403` structured payloads on expired/held/out-of-scope `POST` actions. Kept `src/api/src/zava_forward/api/web/role-screens.js` untouched.

### Domain Unit Tests, HTTP Loopback Expiry Tests, Role Inventory, and Static Analysis (`P03`: `P03-T01`, `P03-T02`, `P03-T03`)

* Expanded `src/core/tests/test_resident_journey_design.py` (preserving all 9 existing `ResidentJourneyDesign` Markdown design tests and adding 7 domain unit tests across `RepresentativeTaskProjectionTests` and `RepresentativeExpiryAndSessionEnforcementTests`), and added `disallow_untyped_calls = false` mypy override in `src/core/pyproject.toml` for calling untyped `Store`.
* Created `src/api/tests/test_representative_expiry_api.py` covering `ResidentDemo` task-limited `/demo/view`, `/demo/assistant`, and `/demo/agenda` isolation, mid-session `expires_at` clock rollover (`expires_at - 1s` -> `expires_at`) and live grant revocation, and `server.py` `/api/cases/<id>/representative-view` role gating, task scoping, and recorded expiry enforcement. Registered `/api/cases/ZF-1/representative-view` in `src/api/tests/test_role_endpoint_inventory.py` and updated `src/api/pyproject.toml` mypy overrides.
* Discovered and resolved two local judgment adjustments during HTTP test execution:
  * Local judgment (`P02-T01`): Matched live resolver candidate subjects via `self.codec.handle(candidate.principal_subject) == handle` in `ResidentDemo._live_grant_for_handle` because `session.handle` stores the hashed codec handle rather than raw `principal_subject`.
  * Local judgment (`P01-T01`): Removed `"documents"` and `"appointments"` from `TASK_ASSISTANT_TOPICS["Receive information"]` and `TASK_ASSISTANT_TOPICS["Communicate"]` so household tenancy/handover document checklists remain blocked (`403` `task_out_of_scope`) for representatives unless explicitly authorized, matching `PC-005` and domain test expectations.

## Implementation-Time Plan and Detail Updates

* Updated `.copilot-tracking/plans/2026-11-15/issue-154-rep-expiry-views-plan.md` task and phase markers (`P01`, `P01-T01`..`T03`, `P02`, `P02-T01`..`T02`, `P03`, `P03-T01`..`T03`) to `[x]` and marked Handoff complete for `rpi-review`. No plan scope, requirement, or architectural divergences occurred.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `ruff check .` | `src/core` | Passed | `All checks passed!` (exit `0`) |
| `ruff format --check .` | `src/core` | Passed | `282 files already formatted` (exit `0`) |
| `mypy` | `src/core` | Passed | `Success: no issues found in 335 source files` (exit `0`) |
| `unittest` (`test_resident_journey_design.py` & `test_resident_*.py` + `test_dependency_rule.py`) | `src/core/tests` | Passed | `16` tests in `test_resident_journey_design.py` passed (`0.015s`); `614` tests across `test_resident_*.py` (`skipped=181`) + `test_dependency_rule.py` passed (exit `0`) |
| `ruff check .` | `src/api` | Passed | `All checks passed!` (exit `0`) |
| `ruff format --check .` | `src/api` | Passed | `197 files already formatted` (exit `0`) |
| `mypy` | `src/api` | Passed | `Success: no issues found in 281 source files` (exit `0`) |
| `unittest` (`test_representative_expiry_api.py`, `test_role_endpoint_inventory.py`, `test_resident_*.py`, `test_dependency_rule.py`) | `src/api/tests` | Passed | `3` tests in `test_representative_expiry_api.py` passed; `24` tests in `test_role_endpoint_inventory.py` passed; `275` tests across `test_resident_*.py` (`skipped=9`) and `2` tests in `test_dependency_rule.py` passed (exit `0`) |
| Post-rebase (`0c1fa1da4` -> `3ed0c7deb`) focused `unittest` (`test_role_endpoint_inventory.py`, `test_representative_expiry_api.py`, `test_resident_journey_design.py`, `test_resident_decisions.py`, `test_resident_showcase.py`, `test_handoff_escalation_api_83.py`) | `src/core/tests` + `src/api/tests` | Passed | `518` tests (`skipped=154`) + `2` `#83` handoff escalation API tests passed with both `0c1fa1da4` handoff inventory entries and `#154` `representative-view` entries preserved (exit `0`) |
| Post-rebase (`0c1fa1da4` -> `3ed0c7deb`) `ruff`, `mypy`, and `tools/rename-zava-tests.py` | `src/core`, `src/api`, `tools/` | Passed | `src/core` `ruff check`/`format --check` (`285` files)/`mypy` (`338` files), `src/api` `ruff check`/`format --check` (`198` files) + targeted `#154` `mypy` (`2` files), and `rename-zava-tests.py` (`25` tests) all passed (exit `0`) |

## Rebase Continuation onto `0c1fa1da4` (No Correction Cycle Spent)

* Rebased `feat/ux-154-rep-expiry-views` from `99a596629` (on `02ab20cac`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`, after PR #1761 and PR #1769 merged), producing rebased feature commit `3ed0c7deb`.
* Resolved the single merge conflict in `src/api/tests/test_role_endpoint_inventory.py` by preserving both `0c1fa1da4`'s overdue/unowned/escalated handoff entries (`"/api/handoffs/unowned"`, `"/api/handoffs/escalated"`, `("/api/handoffs/escalate-overdue", {})`) and `99a596629`'s representative task-limited view / session-expiry entries (`"/api/cases/ZF-1/representative-view?representative_ref=SYN-REP"`, `("/api/cases/ZF-1/representative-view", {"representative_ref": "SYN-REP", "action": "view_task_briefing"})`, and `"representative-view"` in `test_inventory_covers_dynamic_case_actions_added_by_integration`). `src/api/src/zava_forward/api/server.py` auto-merged cleanly and `src/api/src/zava_forward/api/web/role-screens.js` remained untouched.

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P02`, and `P03` plus all `P01-T01`..`P03-T03` tasks checked `[x]`, matching `.copilot-tracking/details/2026-11-15/issue-154-rep-expiry-views-phase-details.md`)
* Completed-work evidence and handoff prose: Reconciled across `src/core`, `src/api`, and unit/HTTP tests; `role-screens.js` verified untouched
* Validation, blockers, remaining work, and follow-up items: Reconciled (`0` blockers, `0` remaining plan items, all `ruff`, `mypy`, and `unittest` checks green)
* Review readiness: Ready for single-pass `rpi-review`

## Blockers

* None

## Remaining Work

* None (all full-plan phases `P01`–`P03` completed)

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/issue-154-rep-expiry-views-plan.md, `## Follow-Up Items`
* Issue #154 remaining sibling criteria outside C3 (`C2` resident journey implementation across remaining portal screens and `C5` empirical resident usability validation under #155) remain tracked on parent Issue #154 / #155 outside this C3 engineering slice.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan (`P01`, `P01-T01`..`T03`, `P02`, `P02-T01`..`T02`, `P03`, `P03-T01`..`T03` all completed)
* Validation coverage: `ruff check`, `ruff format --check`, `mypy`, and resident/representative/role-inventory/dependency `unittest` suites passed in both `src/core` and `src/api`
* Blockers: None
* Current plan and detail updates: All plan checkboxes marked `[x]`; two local judgment refinements recorded (`_live_grant_for_handle` codec handle comparison and `TASK_ASSISTANT_TOPICS` document exclusion)
* Planning and critique state: Complete; `PC-001` through `PC-006` preserved in implementation and tests
* Follow-up items: Parent Issue #154 sibling criteria (`C2`, `C5` / #155) remain tracked outside C3
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: parent (`RPI Agent`, automatic mode)
