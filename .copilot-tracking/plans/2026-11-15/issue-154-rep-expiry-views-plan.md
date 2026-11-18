<!-- markdownlint-disable-file -->
# RPI Plan: Issue #154 Representative Task-Limited Views and Session Expiry

## Task Metadata

* Task ID: issue-154-rep-expiry-views
* Task slug: issue-154-rep-expiry-views
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/issue-154-rep-expiry-views-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-154-rep-expiry-views-plan-critique.md

## Executive Summary

This plan closes the remaining local engineering gap for **Issue #154 Criterion 3** (*Representative views show only task-limited authority and expire as recorded*) under `FR-045`, `FR-046`, `NFR-008`, and `NFR-009`. It introduces a canonical, strictly typed domain enforcement module (`src/core/src/zava_forward/core/resident_journey_design.py`), extends `resident_decisions.py` with backwards-compatible UTC `expires_at` timestamp enforcement alongside `review_date`, and wires live request-time and mid-session expiry and task-scope projection into both the resident-session server (`src/api/src/zava_forward/api/resident_demo/app.py` + `resident_showcase.py`) and the main case API (`src/api/src/zava_forward/api/server.py`).

When a representative holds confirmed, current, unexpired authority, views project **only** the allowlisted fields, actions, and journey stages (`R1` plus permitted `J1`-`J6` slices) for their authorized measure and task, omitting household addresses (`home`), indoor telemetry (`sensors`), out-of-scope measures, unrelated complaints/handover/decisions, other representatives' permissions, and sensitive household or safe-contact notes. When `expires_at` is in the past (or missing, revoked, unclear, disputed, or invalidated by a safe-contact or scope change) at view or action time, the representative session and view immediately transition to an explicit `expired` or `held` state, block task-scoped actions and unpermitted disclosures, and surface the recorded expiry timestamp alongside a safe staff and non-digital resident renewal route.

### User Decisions and Requirements Highlights

* Implement task-limited representative view projection and session/request-time representative expiry (`FR-045`, `FR-046`, `NFR-008`, `NFR-009`) in `src/core` and `src/api` Python modules and tests so Criterion 3 is executable and verified.
* Avoid conflicting edits to `src/api/src/zava_forward/api/web/role-screens.js`; keep view projection and session/action enforcement in Python `core` and `api` layers.
* Validate with `ruff check`, `ruff format --check`, `mypy`, and unit tests in `src/core` and `src/api`, then commit code, tests, and `.copilot-tracking/` artifacts locally in a single clean commit without pushing.

### What You May Not Know

* `src/core/src/zava_forward/core/resident_journey_design.py` does not exist yet (only `src/core/tests/test_resident_journey_design.py` exists for Markdown checks), and `src/api` splits resident sessions (`resident_demo/app.py`) from the case API (`server.py`). Supporting both surfaces ensures representative sessions in `ResidentDemo` and case projections in `server.py` share one authoritative domain state machine.
* `ShowcaseRow` (`ROW_KEYS`) in `resident_showcase.py` is strictly schema-checked by `test_resident_showcase.py` and `resident_showcase_sql.py`, `SessionCodec.issue(...)` hashes a single subject string (requiring a disjoint `rep:<case_id>:<representative_ref>` handle subject and isolated `Agenda` callback owner key so residents and representatives on the same case never collide), and `server.py` routes are regex-audited across all roles and sensitive canaries by `src/api/tests/test_role_endpoint_inventory.py`. The plan keeps `ShowcaseRow` unchanged via a separate `RepresentativeShowcaseGrant` binding, preserves `/demo/session` `csrf`/`session_id` headers across mid-session expiry, and registers `/api/cases/ZF-1/representative-view` in the role endpoint inventory.

### Unresolved Decisions or Blockers

* None. All architecture and scope boundaries are converged from repository evidence and caller instructions.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Deliver Issue #154 Criterion 3 (`Representative views show only task-limited authority and expire as recorded`) via the full RPI loop (`research`, `plan` with `rpi-plan-critique`, `implement`, `review`) with dated `2026-11-15` artifacts under `.copilot-tracking/` (caller prompt).
* Enforce positive-allowlist representative view projection (`FR-045`, `FR-046`, `NFR-008`, `NFR-009`, `docs/reference/research/ux/customer-journeys/residents.md` Journey R1) so representative views show only fields, actions, and journey stages within the representative's recorded task-limited authority scope and redact/omit out-of-scope measures, unrelated complaints/handover/decisions, and sensitive household notes (caller Scope #2).
* Enforce session/request-time representative expiry so that when recorded `expires_at` is in the past (or missing, revoked, unclear, disputed, or invalidated by changed safe contact or measure scope) at view or action time, the session/view immediately transitions to `expired` or `held` state, blocks task-scoped actions and unpermitted disclosures, and surfaces the recorded expiry timestamp and safe staff/resident renewal route (caller Scope #2; `residents.md` R1).
* Place view projection and enforcement in `src/core` and `src/api` Python modules (`resident_journey_design.py`, `resident_decisions.py`, `resident_showcase.py`, `resident_demo/app.py`, `server.py`) and avoid conflicting edits to `src/api/src/zava_forward/api/web/role-screens.js` (caller Scope #1).
* Add comprehensive unit and HTTP tests in `src/core/tests/test_resident_journey_design.py` and `src/api/tests/`, pass `ruff check`, `ruff format --check`, `mypy`, and affected unit tests in `src/core` and `src/api`, and create one local commit with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing (caller Scope #3-#5).

## Goals

* Establish a single, strictly typed Python domain contract in `zava_forward.core.resident_journey_design` for task-limited representative view projection, live `expires_at` / `review_date` evaluation, immediate `expired` / `held` session state transitions, and task-scoped action gating.
* Support optional ISO-8601 UTC `expires_at` timestamps on domain representative authority records in `resident_decisions.py` while preserving existing `authority_date` / `review_date` behavior and start-of-review-date unavailability.
* Enforce live request-time and mid-session representative expiry and task scoping across both HTTP surfaces (`resident_demo/app.py` resident/representative sessions and `server.py` `/api/cases/<id>/representative-view`) with zero regression to existing resident, showcase, preview, and role-matrix contracts.

## Scope and Non-Goals

### In Scope

* New `src/core/src/zava_forward/core/resident_journey_design.py` module for representative authority evaluation, positive-allowlist task projection (`Receive information`, `Communicate`, `Attend`, `Works decision`), appointment offer-vs-confirmed labelling (`FR-046`), `RepresentativeSession` / `RepresentativeSessionStore` transitions, and `enforce_representative_action`.
* Backwards-compatible `expires_at` timestamp validation and enforcement in `src/core/src/zava_forward/core/resident_decisions.py` (`_res_representative_record`, `authority_for`, and store helper methods).
* Typed `RepresentativeShowcaseGrant` support in `src/core/src/zava_forward/core/resident_showcase.py` and representative session/view/action enforcement in `src/api/src/zava_forward/api/resident_demo/app.py`.
* Role-gated `/api/cases/<id>/representative-view` (`GET` and `POST`) in `src/api/src/zava_forward/api/server.py` plus route registration in `src/api/tests/test_role_endpoint_inventory.py`.
* Executable unit and HTTP tests in `src/core/tests/test_resident_journey_design.py` and `src/api/tests/test_representative_expiry_api.py`.

### Non-Goals

* Editing `src/api/src/zava_forward/api/web/role-screens.js` or frontend JavaScript bundles.
* Altering `ShowcaseRow` / `ROW_KEYS` in `resident_showcase.py` or changing `GrantDenied` behavior in `resident_preview.py`.
* Empirical resident usability testing (#155), governance policy ratifications (`OD-41`, `OD-42`), live outbound messaging, or pushing commits to `origin`.

## Functional Requirements

* **FR-REP-01 (Task-Limited Positive-Allowlist Projection — `FR-045`, `FR-046`, Journey R1)**: Projecting a representative view for `(case, representative_ref, now)` evaluates `versions[-1]` (matching `authority_for()` precedence, rejecting `"Unknown"` or blank `representative_ref` identifiers) and returns only the allowlisted fields, `permitted_actions`, and `journey_stages` covered by that representative's own current, `Confirmed`, unexpired measure grant:
  * `Receive information` -> `R1`, `J4` briefing for authorized measure/scope/design version, resident wishes, source, and `expires_at`; read-only (`view_task_briefing`).
  * `Communicate` -> `R1`, `J4`, and `J6` items explicitly linked to `representative_ref` (excluding `"Unknown"` unrepresented items) only (`view_task_briefing`, `send_scoped_message`, `request_scoped_callback`), omitting unrelated household complaints/remedies and internal staff notes.
  * `Attend` -> `R1`, `J3` visit arrangements matched via `resident_bindings` for the authorized `(measure, context_revision)` only, stripping `offer["binding"]["home"]`, separating `Offered - not booked` slots from three-party confirmed `Visit confirmed` commitments (`FR-046`), allowing `view_visit_arrangements` (and `confirm_appointment` only when an unrevoked `appointment_authorities` grant matches the offer, binding, and inclusive `valid_from`..`valid_to` window).
  * `Works decision` -> `R1`, `J1`, `J2` measure scope/design version, resident wishes, and current measure decision status (`submit_measure_decision`, `pause_measure`, `withdraw_measure`) for the authorized measure/revision only.
  * Hard omissions across all tasks: `home` (address/town/postcode), `sensors`, out-of-scope sibling measures, out-of-scope `row.documents` and assistant topics (`TASK_ASSISTANT_TOPICS`), unrelated complaints/handover/checklists/decisions, other representatives' authorities (no union of permissions), `resident_safe_contact` values, and sensitive household/adjustment/hazard notes. Internal `case_id` is omitted from `ResidentDemo` responses and from all denied/expired/held payloads.
  * Observable acceptance criteria: Unit and API tests verify each task profile projects only its scoped stages, fields, assistant topics/documents, and actions and omits out-of-scope measures, complaints, handover, decisions, `home`, `sensors`, and household canaries.
* **FR-REP-02 (Timestamped `expires_at` and Review-Date Ceiling — `FR-045`, Journey R1)**: Domain authority records accept an optional timezone-aware ISO-8601 UTC `expires_at` timestamp alongside `authority_date` and `review_date` (`YYYY-MM-DD`). Effective expiry is `min(parsed_expires_at, review_dateT00:00:00Z)` when both exist, or `review_dateT00:00:00Z` when `expires_at` is omitted on a legacy domain record; an explicit null/malformed/naive `expires_at` or missing expiry ceiling (`RepresentativeShowcaseGrant(expires_at=None)`) fails closed as `missing_expiry`. `authority_for(..., now=None)` compares `expires_at` against `datetime.now(UTC)` while preserving `controls.today()` date checks.
  * Observable acceptance criteria: `authority_for()` and `evaluate_representative_authority()` permit access at `expires_at - 1s` and reject/expire immediately at `now >= expires_at` and from `00:00:00Z` on `review_date`, while backwards-compatible `review_date`-only domain grants remain active before `review_date`.
* **FR-REP-03 (Immediate Request/Session-Time Expiry and Held State Transition — `FR-045`, `NFR-008`, `NFR-009`)**: Every view and action request re-evaluates live representative authority against current UTC time `now` and current case/grant state. When effective expiry is in the past (`state="expired"`) or authority is missing, `Unclear`, `Disputed`, `Revoked`, missing a valid expiry ceiling (`missing_expiry`), or invalidated by a changed `resident_safe_contact` or bumped measure `context_revision` (`state="held"`), the representative session/view immediately transitions to `expired` or `held` (`active=False`, `permitted_actions=[]`, `journey_stages=[]`), strips all restricted case disclosures (including `case_id`), blocks task-scoped actions (`403` in HTTP APIs / `RepresentativeAccessBlockedError` in core), preserves `ResidentDemo` `csrf` and `session_id` headers so mid-session requests return `403` rather than `409`, and surfaces the recorded `expires_at` timestamp (when recorded for that representative) plus the plain-language staff and non-digital resident renewal route.
  * Observable acceptance criteria: Core session tests and `ResidentDemo` / `server.py` HTTP tests prove a live session opened before `expires_at` transitions on the very next request once the clock reaches `expires_at` (or status flips to `Revoked`/`Disputed`), blocks actions, leaks zero case canaries, and returns `expires_at` and `renewal_route`.

## Non-Functional Requirements

* **NFR-REP-01 (Fail-Closed Least-Privilege & Non-Disclosure — `NFR-009`, Journey R1)**: Unknown subjects, unauthorized staff/contractor roles, malformed timestamps, and expired/held grants disclose zero household PII, case notes, or `@example.com` account identities.
  * Objective threshold or evaluation condition: Zero occurrences of household/contact/note canaries or `@example.com` addresses in denied, expired, held, or `/demo/session` responses across all roles and unauthenticated/expired callers.
  * Operating condition or verification approach: Verified by canary assertions in `test_resident_journey_design.py`, `test_representative_expiry_api.py`, and `test_role_endpoint_inventory.py`.
  * Observable acceptance criteria: All canary non-disclosure assertions pass with `Cache-Control: no-store` on resident/representative demo endpoints.
* **NFR-REP-02 (Accessible Plain-Language & Non-Digital Renewal Parity — `NFR-008`)**: Expired and held responses pair explicit non-colour state fields (`state`, `reason`, `expires_at`) with plain-language guidance naming the human officer check and non-digital resident channels (phone, letter, agreed visit, assisted service).
  * Objective threshold or evaluation condition: 100% of expired/held projections and blocked-action payloads include `state`, `expires_at`, and `renewal_route` with `non_digital_supported: True` and R1-aligned plain-language copy.
  * Operating condition or verification approach: Verified by structural and copy assertions in core and API tests.
  * Observable acceptance criteria: Every expired/held state test asserts explicit state, timestamp, and non-digital renewal route fields.
* **NFR-REP-03 (Static Type, Lint, and Regression Hygiene)**: New and touched files conform to package `ruff` and `mypy --strict` configurations without weakening existing test contracts.
  * Objective threshold or evaluation condition: Zero `ruff check`, `ruff format --check`, `mypy`, or `unittest` failures in `src/core` and `src/api`.
  * Operating condition or verification approach: Direct CLI runs in `src/core` and `src/api`.
  * Observable acceptance criteria: All four validation commands exit `0`.

## Acceptance Criteria

* AC1: `zava_forward.core.resident_journey_design` projects only task-permitted fields, `permitted_actions`, and `journey_stages` per representative grant, omitting `home`, `sensors`, out-of-scope measures, unrelated complaints/handover/decisions, other representatives' permissions, and sensitive household/safe-contact notes.
* AC2: `_res_representative_record` and `authority_for` in `resident_decisions.py` validate and enforce optional UTC `expires_at` timestamps alongside `review_date` without breaking existing `authority_date`/`review_date` callers.
* AC3: When `expires_at` is in the past (or missing, `Revoked`, `Disputed`, `Unclear`, or invalidated by safe-contact/scope change) at view or action time, core `RepresentativeSession`, `ResidentDemo` (`/demo/session`, `/demo/view`, `/demo/assistant`, `/demo/agenda`), and `server.py` (`/api/cases/<id>/representative-view`) immediately transition to `expired`/`held`, block task-scoped actions and unpermitted disclosures, and surface the recorded `expires_at` timestamp and safe staff/resident renewal route.
* AC4: `src/api/src/zava_forward/api/web/role-screens.js` remains untouched, `ShowcaseRow` (`ROW_KEYS`) and `resident_preview.py` `GrantDenied` invariants remain intact, and `test_role_endpoint_inventory.py` passes for all roles.
* AC5: `ruff check`, `ruff format --check`, `mypy`, and unit tests in `src/core` and `src/api` pass cleanly.

## Test Ownership and Change Budget Lock

* Canonical production targets:
  * Create `src/core/src/zava_forward/core/resident_journey_design.py`
  * Edit `src/core/src/zava_forward/core/resident_decisions.py`
  * Edit `src/core/src/zava_forward/core/resident_showcase.py`
  * Edit `src/core/pyproject.toml` (only if `disallow_untyped_calls = false` override is needed for typed tests/modules calling untyped `Store`)
  * Edit `src/api/src/zava_forward/api/resident_demo/app.py`
  * Edit `src/api/src/zava_forward/api/server.py`
  * Edit `src/api/pyproject.toml` (add `test_representative_expiry_api` to `disallow_untyped_calls = false` override alongside `test_resident_api` for calling untyped `App`/`Store`)
* Generated targets: `none`
* Exact test removals: `none` (all existing tests in `test_resident_journey_design.py` and `src/api/tests/` are preserved).
* Maximum test files touched/added: `3` (`src/core/tests/test_resident_journey_design.py` expanded; `src/api/tests/test_representative_expiry_api.py` created; `src/api/tests/test_role_endpoint_inventory.py` updated with the single new case endpoint entry).
* Semantic vs regression coverage:
  * Semantic coverage: task-by-task allowlist projection, cross-measure and cross-representative isolation, exact second-granular `expires_at` boundary (`expires_at - 1s` active -> `expires_at` expired), mid-session revocation/dispute/safe-contact/scope transitions, action blocking (`403` / `RepresentativeAccessBlockedError`), and renewal-route + `expires_at` payload verification.
  * Regression coverage: existing `ResidentJourneyDesign` Markdown tests, `test_resident_decisions.py`, `test_resident_preview.py`, `test_resident_showcase.py`, `test_resident_demo_api.py`, `test_resident_api.py`, and `test_role_endpoint_inventory.py`.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/issue-154-rep-expiry-views-plan.md                                                                    |
| Phase details                    | .copilot-tracking/details/2026-11-15/issue-154-rep-expiry-views-phase-details.md                                                         |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/issue-154-rep-expiry-views-plan-critique.md with Revise disposition resolved (`PC-001` through `PC-006` applied directly) |
| Relevant research                | .copilot-tracking/research/2026-11-15/issue-154-rep-expiry-views-research.md                                                             |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-changes.md is created or continued by implementation as its evidence record |
| Planning execution and readiness | Complete; Ready for implementation                                                                                                       |
| Continuation context             | Automatic RPI Agent parent return; transitions automatically to Implement                                                                |

## Sources

* .copilot-tracking/research/2026-11-15/issue-154-rep-expiry-views-research.md: Converged `C1`-`C16` codebase and specification evidence for Issue #154 Criterion 3.
* docs/reference/research/ux/customer-journeys/residents.md: Journey R1 (`Task-limited representative briefing and actions`) wireframe, review-date boundary, and denied/held safe renewal wording.
* docs/brds/agentic-retrofit-programme-brd.md and docs/prds/zava-forward-retrofit-programme-demonstrator.md: Normative `FR-045`, `FR-046`, `NFR-008`, `NFR-009`, `AC-055`, `AC-056`, `AC-064`, `AC-087`, and `AC-088` requirements.
* src/core/src/zava_forward/core/resident_decisions.py, resident_preview.py, resident_showcase.py, appointments.py: Existing authority, appointment, preview, and showcase session implementations.
* src/api/src/zava_forward/api/resident_demo/app.py, server.py, and src/api/tests/test_role_endpoint_inventory.py: Existing resident-session HTTP server, staff case HTTP server, and role-matrix route inventory checks.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Core Representative View Projection and Expiry Enforcement

* Intent: Deliver strictly typed positive-allowlist representative view projection, UTC `expires_at` + `review_date` authority evaluation, session expiry/held transitions, and task-scoped action enforcement in `src/core`.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Create `resident_journey_design.py` projection and session expiry state machine

* Requirement and evidence: FR-REP-01, FR-REP-02, FR-REP-03, NFR-REP-01, NFR-REP-02; research `C1`-`C7`, `C11`.
* Expected result: `src/core/src/zava_forward/core/resident_journey_design.py` provides `parse_iso_utc`, `effective_authority_expiry`, `evaluate_representative_authority`, `project_representative_view`, `RepresentativeSession`, `RepresentativeSessionStore`, and `enforce_representative_action` with strict positive-allowlist task scoping and immediate `expired`/`held` transitions surfacing `expires_at` and `renewal_route`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/issue-154-rep-expiry-views-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Extend `resident_decisions.py` with optional UTC `expires_at` and store projection helpers

* Requirement and evidence: FR-REP-02, FR-REP-03; research `C5`, `C6`.
* Expected result: `_res_representative_record` validates optional ISO-8601 UTC `expires_at`; `authority_for` enforces `now < expires_at` alongside `authority_date <= today < review_date`; `ResidentDecisionMixin` exposes `representative_view` and `representative_session_action` backed by `resident_journey_design` while preserving all existing callers.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/issue-154-rep-expiry-views-phase-details.md

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Add `RepresentativeShowcaseGrant` session binding in `resident_showcase.py`

* Requirement and evidence: FR-REP-01, FR-REP-03, AC4; research `C9`, `C13`.
* Expected result: `resident_showcase.py` defines frozen `RepresentativeShowcaseGrant` and task-limited showcase view/action helpers delegating to `resident_journey_design` without modifying `ShowcaseRow` or `ROW_KEYS`.
* Detail section: P01-T03 in .copilot-tracking/details/2026-11-15/issue-154-rep-expiry-views-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: HTTP Resident-Session and Case API Representative Expiry Enforcement

* Intent: Enforce task-limited representative views and immediate request/mid-session `expires_at` & status transitions across `ResidentDemo` and `server.py` without touching `role-screens.js`.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Enforce representative views, task actions, and mid-session expiry in `resident_demo/app.py`

* Requirement and evidence: FR-REP-01, FR-REP-03, NFR-REP-01, NFR-REP-02; research `C10`, `C15`.
* Expected result: `ResidentDemo` accepts optional representative grants/resolver, authenticates representative sessions via signed cookies, projects task-limited representative views on `/demo/view`, scopes `/demo/assistant` and `/demo/agenda` to authorized tasks, and immediately transitions expired/revoked/disputed/missing-expiry sessions on `/demo/session`, `/demo/view`, `/demo/assistant`, and `/demo/agenda` to `expired`/`held` state (blocking actions with `403`, omitting case details and `@example.com`, and surfacing recorded `expires_at` and `renewal_route`).
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/issue-154-rep-expiry-views-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Add `/api/cases/<id>/representative-view` GET/POST enforcement in `server.py`

* Requirement and evidence: FR-REP-01, FR-REP-03, NFR-REP-01, AC4; research `C12`, `C14`, `C16`.
* Expected result: `server.py` serves `GET` and `POST` `/api/cases/<id>/representative-view` strictly gated by `projection.allowed(u, "case")` and `RESIDENT_VIEW_ROLES`, returning task-limited projections when active and `expired`/`held` state (with `403` on blocked task-scoped POST actions, recorded `expires_at`, `renewal_route`, and zero case disclosures) when expired/revoked/disputed/missing; `role-screens.js` remains untouched.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/issue-154-rep-expiry-views-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Unit, API, Role-Inventory Tests and Static Analysis Gate

* Intent: Prove task-limited representative projection and request/mid-session expiry across `src/core` and `src/api` and pass `ruff check`, `ruff format --check`, `mypy`, and unit test suites.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Expand `src/core/tests/test_resident_journey_design.py` with domain projection and expiry tests

* Requirement and evidence: AC1, AC2, AC3; caller Scope #3.
* Expected result: `test_resident_journey_design.py` retains all existing Markdown regression tests and adds comprehensive unit tests for every `AUTHORITY_TASKS` slice, offer-vs-confirmed appointments, redaction of out-of-scope measures/complaints/handover/decisions/household notes, non-union of multiple representatives, `resident_decisions` `expires_at` enforcement, and `RepresentativeSession` mid-session expiry/revocation/dispute/safe-contact/scope transitions.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/issue-154-rep-expiry-views-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Add HTTP representative session/API expiry tests and update role endpoint inventory

* Requirement and evidence: AC3, AC4; research `C14`, `C15`; caller Scope #3.
* Expected result: `src/api/tests/test_representative_expiry_api.py` verifies `ResidentDemo` representative login, task-limited `/demo/view`, scoped `/demo/assistant` & `/demo/agenda`, mid-session clock advance past `expires_at` and status change to `Revoked`/`Disputed`/missing, plus `server.py` `/api/cases/<id>/representative-view` GET/POST projection, action blocking, and role isolation; `src/api/tests/test_role_endpoint_inventory.py` includes `/api/cases/ZF-1/representative-view` and passes across all roles.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/issue-154-rep-expiry-views-phase-details.md

<!-- rpi:task id=P03-T03 -->
#### [x] P03-T03: Run `ruff check`, `ruff format --check`, `mypy`, and unit test suites in `src/core` and `src/api`

* Requirement and evidence: NFR-REP-03, AC5; caller Scope #4.
* Expected result: `ruff check`, `ruff format --check`, `mypy`, and `unittest` suites in `src/core` and `src/api` pass with zero errors or regressions.
* Detail section: P03-T03 in .copilot-tracking/details/2026-11-15/issue-154-rep-expiry-views-phase-details.md

## Dependencies

* `zava_forward.core` editable/installed distribution in the active Python environment: `src/api` imports `zava_forward.core.resident_journey_design`, `resident_decisions`, and `resident_showcase`.
* Existing `resident_decisions`, `appointments`, `projection`, and `resident_showcase` invariants: preserved by additive optional `expires_at` and separate `RepresentativeShowcaseGrant` types.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| 2026-11-15 `PC-001` [High]: `ResidentDemo` `SessionCodec` handle collision, shared `Agenda` owner key, and `/demo/session` contract | Resolved (direct planner correction) | Updated `P01-T03`, `P02-T01`, and `P03-T02` to issue distinct `rep:<case_id>:<representative_ref>` handles in `rep_by_handle`, isolate representative callback keys via `resident_key(f"rep:{case_id}:{representative_ref}")`, and keep `/demo/session` `csrf`, `signed_in`, `session_id`, and `banner` additive so `_session_bound()` returns `403` (not `409`) across mid-session expiry. |
| 2026-11-15 `PC-002` [High]: `review_date`-only grants vs `missing_expiry`, `versions[-1]` precedence, and naive `controls.now()` | Resolved (direct planner correction) | Updated `FR-REP-02`, `FR-REP-03`, `P01-T01`, and `P01-T02` so legacy `review_date`-only domain records derive `review_dateT00:00:00Z` while explicit null/malformed/missing expiry triggers `missing_expiry`, `versions[-1]` matches `authority_for()`, and `authority_for(..., now=None)` uses `datetime.now(UTC)` + `controls.today()`. |
| 2026-11-15 `PC-003` [High]: `server.py` `projection.allowed` / `controls.RESIDENT_VIEW_ROLES`, `with self.lock:`, and `do_GET`/`do_POST` ordering | Resolved (direct planner correction) | Updated `P01-T02`, `P02-T02`, and `P03-T02` to acquire `with self.lock:` in `Store` helpers, gate `server.py` `do_GET` (before `/api/cases/` catch-all) and `do_POST` (before `s._case(cid)`) with `projection.allowed` + `controls.RESIDENT_VIEW_ROLES`, and register `"representative-view"` in `test_inventory_covers_dynamic_case_actions_added_by_integration`. |
| 2026-11-15 `PC-004` [Medium]: `Attend` work-order bindings, three-party commitment label, and `appointment_authorities` schema | Resolved (direct planner correction) | Updated `FR-REP-01`, `P01-T01`, and `P03-T01` to match `appointments.py` `resident_bindings`, strip `offer["binding"]["home"]`, require `w["state"] == "Appointed"` plus all three confirmations (`resident`, `staff`, `capacity`) for `"Visit confirmed"`, and validate `appointment_authorities` via `revoked`, `offer`, `binding`, and inclusive `valid_from`..`valid_to`. |
| 2026-11-15 `PC-005` [Medium]: `ResidentDemo` `/demo/assistant` `row.documents` and topic allowlist | Resolved (direct planner correction) | Updated `FR-REP-01`, `P01-T03`, `P02-T01`, and `P03-T02` to enforce `TASK_ASSISTANT_TOPICS` before `CaseProgress`/`chat.answer` and bind `CaseProgress` strictly to `grant.documents` rather than household `row.documents`. |
| 2026-11-15 `PC-006` [Low]: `"Unknown"` `representative_ref` sentinel and `case_id` in denied/expired payloads | Resolved (direct planner correction) | Updated `FR-REP-01`, `FR-REP-03`, `P01-T01`, and `P01-T02` to reject `"Unknown"` and blank `representative_ref` values and omit internal `case_id` from denied/expired/held payloads and `ResidentDemo` responses. |

## Follow-Up Items

* None

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-changes.md
* Ready phase or task: Complete (`P01`, `P02`, and `P03` checked and verified; ready for `rpi-review`)
* Remaining provisional question or blocker: None
