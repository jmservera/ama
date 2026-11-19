<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #154 Representative Task-Limited Views and Session Expiry

## Metadata

* Task ID: issue-154-rep-expiry-views
* Task slug: issue-154-rep-expiry-views
* Related plan: .copilot-tracking/plans/2026-11-15/issue-154-rep-expiry-views-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/issue-154-rep-expiry-views-research.md, docs/reference/research/ux/customer-journeys/residents.md, docs/brds/agentic-retrofit-programme-brd.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md

## Phase Index

| Phase ID | Name                                                            | Status      | Detail sections                |
|----------|-----------------------------------------------------------------|-------------|--------------------------------|
| P01      | Core Representative View Projection and Expiry Enforcement      | Ready       | P01, P01-T01, P01-T02, P01-T03 |
| P02      | HTTP Resident-Session and Case API Representative Expiry Enforcement | Ready  | P02, P02-T01, P02-T02          |
| P03      | Unit, API, Role-Inventory Tests and Static Analysis Gate        | Ready       | P03, P03-T01, P03-T02, P03-T03 |

<!-- rpi:phase id=P01 -->
## P01: Core Representative View Projection and Expiry Enforcement

### Context

Research (`C1`-`C9`, `C11`, `C13`) established that `resident_decisions.py` only enforces day-granular `authority_date <= today < review_date` inside staff write mutations, `resident_preview.py` is a static read-only loopback preview covering only two tasks with generic `GrantDenied` errors, and `resident_journey_design.py` does not yet exist. A dedicated typed core module lets both case-backed and showcase-session-backed HTTP flows enforce identical positive-allowlist task projection and timestamped `expires_at` transitions.

### Intent

Provide the complete domain model, positive-allowlist view projection, timestamped `expires_at` + `review_date` evaluator, session state machine, and showcase binding in `src/core`.

### Boundaries

* Included: `resident_journey_design.py`, optional `expires_at` + helper methods in `resident_decisions.py`, and `RepresentativeShowcaseGrant` in `resident_showcase.py`.
* Excluded: Mutating `ShowcaseRow` / `ROW_KEYS`, changing `resident_preview.py` `GrantDenied` strings, or editing HTTP servers (handled in P02).

### Likely Targets

* src/core/src/zava_forward/core/resident_journey_design.py: New typed module for task-limited projection, expiry evaluation, session transitions, and action gating.
* src/core/src/zava_forward/core/resident_decisions.py: Optional `expires_at` timestamp validation/enforcement and `Store` representative projection/action methods.
* src/core/src/zava_forward/core/resident_showcase.py: Additive `RepresentativeShowcaseGrant` and showcase representative view/action projection helpers.
* src/core/pyproject.toml: Add `test_resident_journey_design` override for `disallow_untyped_calls = false` only if tests instantiate untyped `Store`.

### Dependencies

* None.

### Validation Expectations

* `ruff check`, `ruff format --check`, and `mypy` pass in `src/core`; existing `test_resident_decisions.py`, `test_resident_preview.py`, and `test_resident_showcase.py` continue to pass.

### Completion Evidence

* `resident_journey_design.py` exported and callable from both `Store` (`resident_decisions.py`) and `resident_showcase.py` with strict typing.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Create `resident_journey_design.py` projection and session expiry state machine

#### Context

Journey R1 (`residents.md`) and `FR-045`/`FR-046`/`NFR-008`/`NFR-009` require positive-allowlist representative views by task (`Receive information`, `Communicate`, `Attend`, `Works decision`) and immediate transition to an `expired` or `held` state when `expires_at` passes or authority is missing, unclear, disputed, revoked, or invalidated by changed safe contact or measure scope.

#### Intent

Implement `src/core/src/zava_forward/core/resident_journey_design.py` with pure, strictly typed functions and session state classes.

#### Boundaries

* Included:
  * `parse_iso_utc(value)` and `format_iso_utc(dt)`: strict timezone-aware ISO-8601 UTC parsing/formatting; naive or malformed strings return `None` (fail closed).
  * `effective_authority_expiry(record)`: computes UTC `datetime` ceiling from `record.get("expires_at")` and/or `record.get("review_date")` (`YYYY-MM-DD` -> `00:00:00Z` UTC per R1 unavailability on review date), taking `min(...)` when both are present. If `"expires_at"` is explicitly present on `record` with `None` or a naive/malformed value, returns `None` (`missing_expiry`); if `"expires_at"` is omitted on a legacy domain record, derives `review_dateT00:00:00Z`, returning `None` if `review_date` is missing/invalid or `review_date <= authority_date`.
  * `TASK_JOURNEY_STAGES`, `TASK_PERMITTED_ACTIONS`, and `TASK_ASSISTANT_TOPICS`: explicit per-task mappings:
    * `Receive information`: stages `("R1", "J4")`, actions `("view_task_briefing",)`, assistant topics `("progress", "next_step", "regulations", "safety", "documents")`
    * `Communicate`: stages `("R1", "J4", "J6")`, actions `("view_task_briefing", "send_scoped_message", "request_scoped_callback")`, assistant topics `("progress", "next_step", "regulations", "safety", "documents", "appointments")`
    * `Attend`: stages `("R1", "J3")`, actions `("view_visit_arrangements",)` (plus `"confirm_appointment"` only when an unrevoked `appointment_authorities` grant matches the offer, binding, and inclusive `valid_from`..`valid_to` window on that authorized measure), assistant topics `("appointments", "safety")`
    * `Works decision`: stages `("R1", "J1", "J2")`, actions `("submit_measure_decision", "pause_measure", "withdraw_measure")`, assistant topics `("consents", "regulations", "safety")`
  * `evaluate_representative_authority(case, representative_ref, *, now=None, today_str=None)`: rejects blank or `"Unknown"` (case-insensitive) `representative_ref` immediately as `missing_authority`, inspects only `versions[-1]` of `case["representative_authorities"].get(representative_ref)` (matching `authority_for()` precedence and never combining permissions across representatives), checks retention schedule if present, checks against live `resident_safe_contact` + `safe_contact_revision`, live `resident_scopes` `context_revision`, `status == "Confirmed"`, `authority_date <= check_date`, and `now_utc < effective_expiry`. Classifies inactive outcome precisely as `state="expired"` (`reason="expired"`) when a confirmed/recorded grant reached or passed `effective_expiry`, vs `state="held"` (`reason` in `"revoked"`, `"disputed"`, `"unclear"`, `"missing_authority"`, `"missing_expiry"`, `"safe_contact_changed"`, `"scope_changed"`, `"not_yet_valid"`, `"retention_expired"`).
  * `project_representative_view(case, representative_ref, *, now=None, work_orders=(), include_case_id=True)`:
    * When active: returns allowlisted dictionary with `viewer`, optional `case_id` (included when `include_case_id=True` on staff API, omitted when `include_case_id=False` on `ResidentDemo`), `state="active"`, `active=True`, `expires_at` (active grant ISO timestamp), `authority_scope` (measure grant summary including `"You may ... for ... until ..."` banner, `source`, `resident_wishes`, `expires_at`), `journey_stages`, `permitted_actions`, `tasks_not_shown`, `measures` (strictly the authorized `(measure, context_revision)` only, with task-filtered fields: stage/progress for `Receive information`/`Communicate`; current measure decision without internal/safe-contact fields for `Works decision`; measure-bound appointments matched via `resident_bindings` on `w["state"] in ("Issued", "Appointed")`, stripping `offer["binding"]["home"]`, and labelling `"Visit confirmed"` only when `w["state"] == "Appointed"` and all three `confirmations` `resident`, `staff`, `capacity` match `offer["id"]`, else `"Offered - not booked"` for `Attend`), optional `communications` (only when `Communicate` is active, projecting only `service_requests` with valid non-`"Unknown"` `r.get("representative_ref") == representative_ref` and redacting `contact_needs`, `safe_contact_ref`, and staff `history` notes), and `renewal_route`. Never includes `home`, `sensors`, out-of-scope measures, unrelated complaints/handover/decisions, other representatives, or household/hazard/contact notes.
    * When expired or held: returns only safe shell (`viewer`, zero `case_id` disclosure, `state`, `active=False`, `reason`, `expires_at` from the representative's recorded grant if available else `None`, `journey_stages=[]`, `permitted_actions=[]`, `authority_scope=[]`, plain-language `notice`, and `renewal_route` with R1 headline, staff confirmation route, and non-digital resident renewal route).
  * `RepresentativeSession`, `RepresentativeSessionStore`, `RepresentativeAccessBlockedError`, `RepresentativeScopeDeniedError`, and `enforce_representative_action(...)`: tracks representative sessions, re-evaluates live case state and `now` on every `view(...)` and `perform_action(...)`, mutates `session.state` immediately to `"expired"` or `"held"` when invalid/expired, blocks task-scoped actions when expired/held (`RepresentativeAccessBlockedError` carrying `state`, `reason`, `expires_at`, `renewal_route`) or when outside granted tasks/measures (`RepresentativeScopeDeniedError`).
* Excluded: Direct HTTP transport or SQL query wiring.

#### Likely Targets

* src/core/src/zava_forward/core/resident_journey_design.py: Create module.

#### Dependencies

* None.

#### Validation Expectations

* Passes `mypy` under strict mode and `ruff check` / `ruff format --check` in `src/core`.

#### Completion Evidence

* Module created with full type annotations and clean lint/type check.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Extend `resident_decisions.py` with optional UTC `expires_at` and store projection helpers

#### Context

`_res_representative_record` (`resident_decisions.py`) currently stores `authority_date` and `review_date` (`YYYY-MM-DD`), and `authority_for()` checks `authority_date <= k.today() < review_date`. Adding optional ISO-8601 UTC `expires_at` lets staff/callers record sub-day timestamped expiry while preserving every existing `authority_date`/`review_date` record and test.

#### Intent

Support optional `expires_at` on representative authority records, enforce it in `authority_for(..., now=None)`, and expose `representative_view` and `representative_session_action` helpers on `ResidentDecisionMixin`.

#### Boundaries

* Included:
  * In `_res_representative_record`: reject `"Unknown"` (case-insensitive) as `representative_ref`; if `"expires_at"` is present in `body`, require a non-empty valid timezone-aware ISO-8601 UTC timestamp via `parse_iso_utc` strictly after `datetime.fromisoformat(f"{start}T00:00:00+00:00")` and `<= datetime.fromisoformat(f"{review}T00:00:00+00:00")`, storing canonical `"expires_at": format_iso_utc(parsed)` on `rec`.
  * In `authority_for(c, ref, task, measure, context, version=None, now=None)`: resolve `now_utc = now if now is not None else datetime.now(UTC)` (never naive `controls.now()`) and `today = now.date().isoformat() if now is not None else k.today()`; check `"expires_at"` against `now_utc` (`parsed is not None and now_utc < parsed`) whenever `"expires_at"` is present on `a`, in addition to `a["authority_date"] <= today < a["review_date"]`.
  * On `ResidentDecisionMixin`: add `representative_view(self, user, cid, representative_ref, *, now=None)` and `representative_action_check(self, user, cid, body, *, now=None)` acquiring `with self.lock:`, checking `k.require_role(user, k.RESIDENT_VIEW_ROLES, "current resident-workflow staff")` before `self._case(cid)`, and delegating to `resident_journey_design` with the case's work orders from `self._proc()`.
* Excluded: Changing existing keys on records created without `expires_at` (so deep-equality snapshot tests in `test_resident_decisions.py` pass unchanged).

#### Likely Targets

* src/core/src/zava_forward/core/resident_decisions.py: Update `_res_representative_record`, `authority_for`, and `ResidentDecisionMixin`.

#### Dependencies

* P01-T01.

#### Validation Expectations

* Existing `src/core/tests/test_resident_decisions.py` passes completely alongside new `expires_at` tests.

#### Completion Evidence

* `authority_for` and `_res_representative_record` enforce `expires_at` cleanly with zero regressions.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Add `RepresentativeShowcaseGrant` session binding in `resident_showcase.py`

#### Context

`ResidentDemo` uses `resident_showcase.py` (`ShowcaseRow`, `IdentityMap`, `SessionCodec`). Contrarian research (`C13`) proved `ShowcaseRow` (`ROW_KEYS`) must not change. Adding a separate frozen dataclass `RepresentativeShowcaseGrant` in `resident_showcase.py` lets `ResidentDemo` bind representative accounts (`email`, `case_id`, `representative_ref`, `status`, `tasks`, `measure`, `scope`, `design_version`, `authority_date`, `expires_at`, `source`, `resident_wishes`, `documents`) and project/expire them through `resident_journey_design`.

#### Intent

Define `RepresentativeShowcaseGrant` and helper projection/evaluation functions in `resident_showcase.py` without touching `ShowcaseRow` or `ROW_KEYS`.

#### Boundaries

* Included:
  * Frozen dataclass `RepresentativeShowcaseGrant` with `case_id`, `email`, `representative_ref`, `status`, `tasks`, `measure`, `scope`, `design_version`, `authority_date`, `expires_at` (`datetime | None`), `source`, `resident_wishes`, `provenance`, `documents: tuple[ShowcaseDocument, ...] = ()`, `revoked: bool = False`, `safe_contact_valid: bool = True`, `scope_current: bool = True`, and a deterministic codec subject helper `principal_subject` (`f"rep:{case_id}:{representative_ref}"`) disjoint from resident `case_id` subjects (`PC-001`).
  * `representative_showcase_view(grant, row, now, *, callbacks_available=False)` and `enforce_representative_showcase_action(grant, row, action, now, *, topic=None)` delegating to `resident_journey_design` constructs (with `include_case_id=False`, `TASK_ASSISTANT_TOPICS` enforcement, and `grant.documents` isolation rather than household `row.documents`, `PC-005`/`PC-006`) so `ResidentDemo` projects only authorized tasks/measures/documents (never `home` or `sensors` or out-of-scope measures/documents) and transitions to `expired`/`held` with recorded `expires_at` and `renewal_route` when `now >= grant.expires_at`, `grant.expires_at is None`, `grant.revoked`, `grant.status != "Confirmed"`, `not grant.safe_contact_valid`, or `not grant.scope_current` (or when the underlying case `ShowcaseRow` is unavailable).
* Excluded: Modifying `ShowcaseRow`, `ROW_KEYS`, `parse_row`, or `resident_showcase_sql.py`.

#### Likely Targets

* src/core/src/zava_forward/core/resident_showcase.py: Add `RepresentativeShowcaseGrant` and helpers.

#### Dependencies

* P01-T01.

#### Validation Expectations

* `src/core/tests/test_resident_showcase.py` and `mypy` / `ruff` pass.

#### Completion Evidence

* `RepresentativeShowcaseGrant` and projection/expiry helpers available and type-checked.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: HTTP Resident-Session and Case API Representative Expiry Enforcement

### Context

Research (`C10`, `C12`, `C14`, `C15`, `C16`) identified two HTTP surfaces in `src/api`: `resident_demo/app.py` (cookie-authenticated resident sessions) and `server.py` (role-gated case endpoints). Enforcing task-limited views and request/mid-session representative expiry on both closes the Issue #154 C3 resident-session and API gap completely without touching `role-screens.js`.

### Intent

Wire `resident_journey_design` and `RepresentativeShowcaseGrant` into `resident_demo/app.py` and `server.py`.

### Boundaries

* Included: `src/api/src/zava_forward/api/resident_demo/app.py` and `src/api/src/zava_forward/api/server.py`.
* Excluded: `src/api/src/zava_forward/api/web/role-screens.js` and `resident_preview/app.py`.

### Likely Targets

* src/api/src/zava_forward/api/resident_demo/app.py: Support optional representative bindings on `ResidentDemo` and enforce mid-session view/action expiry and task scoping.
* src/api/src/zava_forward/api/server.py: Add `GET` and `POST` `/api/cases/<id>/representative-view`.

### Dependencies

* P01.

### Validation Expectations

* All existing `test_resident_demo_api.py`, `test_resident_api.py`, and `test_role_endpoint_inventory.py` tests pass, plus new representative session/API tests.

### Completion Evidence

* HTTP endpoints return `Cache-Control: no-store`, enforce positive-allowlist task projections, and transition immediately on `expires_at` / status invalidation at view and action time.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Enforce representative views, task actions, and mid-session expiry in `resident_demo/app.py`

#### Context

`ResidentDemo` authenticates users at `/demo/login`, issues an HMAC-signed cookie (`__Host-zfdemo`) carrying `(case_id, canonical_email)`, and serves `/demo/session`, `/demo/view`, `/demo/assistant`, `/demo/agenda`, and `/demo/logout`. Currently, only household `ShowcaseRow` emails can log in, and expiry drops to generic `401`. For representative principals, C3 requires task-limited view projection while active and immediate transition to an `expired`/`held` representative session/view state (blocking task-scoped actions, withholding case disclosures, and surfacing recorded `expires_at` and safe renewal route) when `expires_at` passes or authority is missing/revoked/disputed mid-session.

#### Intent

Extend `ResidentDemo` with optional `representatives` lookup (e.g., mapping or callable by canonical email, or optional `get_representative(case_id, email)` on the reader) while keeping resident-principal behavior 100% unchanged.

#### Boundaries

* Included:
  * Issue representative session cookies via `codec.issue(grant.principal_subject)` (`f"rep:{grant.case_id}:{grant.representative_ref}"`) mapped in a separate `rep_by_handle` table completely disjoint from resident `self.by_handle` so a household resident and multiple representatives on the same case never share handles (`PC-001`). Record representative session lifecycle transitions in an in-memory `RepresentativeSessionStore` on `ResidentDemo`.
  * `GET /demo/session`: preserve `csrf`, `signed_in` (`True` when active, `False` when expired/held), `session_id` (valid cookie token preserved while cookie TTL is valid so `_session_bound()` `X-Resident-Session` verification passes across mid-session expiry and `/demo/view`, `/demo/assistant`, `/demo/agenda`, and `/demo/logout` return `403` expired/held or `200` logout instead of `409`, `PC-001`), and `banner`, while adding `viewer_kind: "representative"`, `state`, `reason` (when inactive), `expires_at`, and `renewal_route` (when inactive) — never echoing `@example.com` (`C15`).
  * `GET /demo/view`: for a representative session, return `200` with the task-limited representative view (omitting `case_id`, `home`, `sensors`, out-of-scope measures, and household `row.documents`) when active, and transition immediately to `expired`/`held` returning `403` (with JSON body `{ "viewer": ..., "state": "expired"|"held", "active": False, "reason": ..., "expires_at": ..., "permitted_actions": [], "journey_stages": [], "notice": ..., "renewal_route": ... }` and zero case details) when `now >= expires_at` or grant is missing/revoked/disputed/unclear/invalidated.
  * `POST /demo/assistant` and `POST /demo/agenda`: re-evaluate representative authority at action time. If expired/held, block immediately with `403` and the `{ "error": ..., "state": ..., "reason": ..., "expires_at": ..., "renewal_route": ... }` payload (zero case disclosures, zero assistant invocation, zero callback mutation). If active, `/demo/agenda` requires `"Communicate"` or `"Attend"` and isolates callback ownership with `resident_key(grant.principal_subject)` (`PC-001`), and `/demo/assistant` resolves `Topic` / `chat.route(question)` first, checks `TASK_ASSISTANT_TOPICS` (refusing `"home"`, `"repair"`, and out-of-scope topics with `403` before `chat.answer`), and builds `CaseProgress` strictly from `grant.documents` rather than `row.documents` (`PC-005`).
* Excluded: Changing any response code, payload key, or behavior for household resident `ShowcaseRow` principals.

#### Likely Targets

* src/api/src/zava_forward/api/resident_demo/app.py: Extend `ResidentDemo` with optional representative bindings and session/request-time enforcement.

#### Dependencies

* P01-T01, P01-T03.

#### Validation Expectations

* `test_resident_demo_api.py` passes 100% unchanged; new representative session tests pass `mypy` and `ruff`.

#### Completion Evidence

* `ResidentDemo` handles active and mid-session expired/revoked/disputed representative sessions across `/demo/session`, `/demo/view`, `/demo/assistant`, and `/demo/agenda`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Add `/api/cases/<id>/representative-view` GET/POST enforcement in `server.py`

#### Context

Staff and case-integrated callers interact with `server.py` (`Store` / `SqlStore` / `MssqlStore`). Exposing `GET /api/cases/<id>/representative-view?representative_ref=<ref>` and `POST /api/cases/<id>/representative-view` (supporting session open, session-bound view, and task-scoped action enforcement against `Store` case authorities and work orders) makes `resident_journey_design` directly enforceable over the main case API without modifying `role-screens.js`.

#### Intent

Add role-gated GET/POST `/api/cases/<id>/representative-view` handlers in `server.py` backed by `Store.representative_view` / `RepresentativeSessionStore`.

#### Boundaries

* Included:
  * Gate `GET /api/cases/<id>/representative-view` in `do_GET` (matched before the `url.path.startswith("/api/cases/")` `s.detail` catch-all alongside `/home-case`) with `projection.allowed(u, "case", "GET")` and `u.get("role") in controls.RESIDENT_VIEW_ROLES`, and gate `POST /api/cases/<id>/representative-view` in `do_POST` (matched before `s._case(cid)` alongside `sensor-draft` with an explicit `return`) with `projection.allowed(u, "case", "POST")` and `u.get("role") in controls.RESIDENT_VIEW_ROLES` (`PC-003`), returning `403` before any case lookup for contractors, mystery roles, or non-resident-view roles (`C14`).
  * `GET /api/cases/<id>/representative-view?representative_ref=<ref>` (optional `session_id`): returns `200` with task-limited representative projection when active, or `200` safe expired/held shell (`state="expired"|"held"`, `active=False`, `expires_at`, `renewal_route`, zero `case_id`/case details/canaries) when `representative_ref` is expired/revoked/disputed/missing.
  * `POST /api/cases/<id>/representative-view`: supports opening/refreshing a `RepresentativeSession` (`mode="open"` or `"view"`) and checking/executing a task-scoped representative action (`action` in permitted actions for `measure`), returning `403` with `{ "error": ..., "state": "expired"|"held"|"scope_denied", "reason": ..., "expires_at": ..., "renewal_route": ... }` whenever authority is expired/held or the requested action/measure is outside the representative's recorded task scope.
* Excluded: Editing `src/api/src/zava_forward/api/web/role-screens.js`.

#### Likely Targets

* src/api/src/zava_forward/api/server.py: Add GET and POST route dispatch for `/api/cases/<id>/representative-view` and attach a `RepresentativeSessionStore` instance on `App`.

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* `test_role_endpoint_inventory.py` and `test_resident_api.py` pass with zero `500` responses and zero canary leaks across all roles.

#### Completion Evidence

* Route active, role-gated, session-aware, and non-disclosing on denial/expiry.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Unit, API, Role-Inventory Tests and Static Analysis Gate

### Context

Caller Scope #3 and #4 require comprehensive tests in `src/core/tests/test_resident_journey_design.py` and `src/api/tests/` proving task-limited representative view projection and mid-session / as-recorded expiry enforcement, validated by `ruff check`, `ruff format --check`, `mypy`, and affected unit tests in `src/core` and `src/api`.

### Intent

Author focused, high-signal tests covering all positive allowlists, redactions, edge cases, and mid-session expiry transitions, then run all static analysis and test gates.

### Boundaries

* Included: `src/core/tests/test_resident_journey_design.py`, `src/api/tests/test_representative_expiry_api.py`, `src/api/tests/test_role_endpoint_inventory.py`, and `pyproject.toml` typed-test overrides where calling untyped `Store`/`App`.
* Excluded: Unrelated test suites or browser Playwright harnesses untouched by Python-only changes.

### Likely Targets

* src/core/tests/test_resident_journey_design.py: Add executable projection, `expires_at`, and `RepresentativeSession` tests.
* src/api/tests/test_representative_expiry_api.py: New HTTP test suite for `ResidentDemo` representative sessions and `server.py` `/api/cases/<id>/representative-view`.
* src/api/tests/test_role_endpoint_inventory.py: Register `/api/cases/ZF-1/representative-view` in `GET_ENDPOINTS` and `POST_ENDPOINTS`.
* src/core/pyproject.toml and src/api/pyproject.toml: Add `disallow_untyped_calls = false` override for typed test modules calling untyped `Store`/`App`.

### Dependencies

* P01, P02.

### Validation Expectations

* `ruff check`, `ruff format --check`, `mypy`, and unit tests pass in both `src/core` and `src/api`.

### Completion Evidence

* Command exit codes `0` recorded in `.copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Expand `src/core/tests/test_resident_journey_design.py` with domain projection and expiry tests

#### Context

`test_resident_journey_design.py` currently contains `class ResidentJourneyDesign` checking `residents.md`. Expanding this file preserves doc checks while testing `zava_forward.core.resident_journey_design` and `resident_decisions` `expires_at` integration end to end.

#### Intent

Add comprehensive core unit tests for task-limited projection, cross-measure/representative redaction, and request/session-time expiry.

#### Boundaries

* Included:
  * Keep `class ResidentJourneyDesign` untouched.
  * Test each `AUTHORITY_TASKS` profile (`Receive information`, `Communicate`, `Attend`, `Works decision`), including a real `Store`-issued work order with `resident_bindings`, appointment offers vs three-party `Visit confirmed` state, `appointment_authorities` gating, and `"Unknown"` `representative_ref` rejection (`PC-004`, `PC-006`), verifying exact `journey_stages`, `permitted_actions`, and redaction/omission of out-of-scope sibling measures, unrelated `service_requests`/complaints, handover/checklists, unrelated measure decisions, `home` (including `offer["binding"]["home"]`), `sensors`, `resident_safe_contact`, and household/vulnerability/hazard notes.
  * Test multiple representatives on the same case never receive the union of each other's permissions.
  * Test `_res_representative_record` and `authority_for` with ISO-8601 UTC `expires_at` (`expires_at - 1s` allowed; exact `expires_at` blocked; naive/malformed rejected; `review_date` `00:00:00Z` ceiling enforced).
  * Test `RepresentativeSession` & `RepresentativeSessionStore` mid-session transitions: active session at `T0` -> clock advances to `expires_at` -> immediate transition to `state="expired"`, `active=False`, `permitted_actions=[]`, case disclosures stripped, `expires_at` and `renewal_route` surfaced, task-scoped actions blocked via `RepresentativeAccessBlockedError`; likewise test `Revoked`, `Disputed`, `Unclear`, missing `expires_at`, changed `resident_safe_contact`, and bumped measure `context_revision` transitioning immediately to `state="held"`.
* Excluded: HTTP socket tests (covered in P03-T02).

#### Likely Targets

* src/core/tests/test_resident_journey_design.py: Add core unit test classes.
* src/core/pyproject.toml: Add `test_resident_journey_design` to `disallow_untyped_calls = false` override if calling `Store`.

#### Dependencies

* P01.

#### Validation Expectations

* `python3 -m unittest discover -s tests -p 'test_resident*.py' -q` in `src/core` passes.

#### Completion Evidence

* All core resident tests pass and are strict-typed.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Add HTTP representative session/API expiry tests and update role endpoint inventory

#### Context

HTTP verification must cover both `ResidentDemo` cookie-bound sessions (`/demo/*`) and `server.py` case routes (`/api/cases/<id>/representative-view`), plus `RoleEndpointInventory`.

#### Intent

Create `src/api/tests/test_representative_expiry_api.py` and register `/api/cases/ZF-1/representative-view` in `src/api/tests/test_role_endpoint_inventory.py`.

#### Boundaries

* Included:
  * `ResidentDemo` tests: same-case household resident + two sibling representatives handle and `Agenda` callback isolation (`PC-001`); representative login; task-limited `/demo/view` omitting `case_id`, `home`, `sensors`, out-of-scope measures, and household `row.documents`; `/demo/session` preserving `csrf`/`session_id` while omitting `@example.com`; `/demo/agenda` and `/demo/assistant` (`TASK_ASSISTANT_TOPICS` + `grant.documents`, `PC-005`) allowed only for in-scope tasks/topics; mid-session clock advance to `expires_at` (while session cookie TTL and `X-Resident-Session` remain valid) immediately transitioning `/demo/view` (`403`) and `/demo/session` (`state="expired"`), blocking `/demo/agenda` and `/demo/assistant` (`403`, never `409`), disclosing zero case canaries, and surfacing recorded `expires_at` and `renewal_route`; mid-session revocation/dispute/missing-expiry transitioning to `state="held"`.
  * `server.py` tests: `GET` and `POST` `/api/cases/<id>/representative-view` returning task-limited projections for authorized staff roles, blocking out-of-scope and expired/revoked/disputed POST actions (`403` with `expires_at` and `renewal_route`), withholding sensitive household/contact/complaint/handover canaries, and denying contractors (`403`).
  * `test_role_endpoint_inventory.py`: add `/api/cases/ZF-1/representative-view?representative_ref=SYN-REP` to `GET_ENDPOINTS`, `("/api/cases/ZF-1/representative-view", {"representative_ref": "SYN-REP", "action": "view_task_briefing"})` to `POST_ENDPOINTS`, and `"representative-view"` to `test_inventory_covers_dynamic_case_actions_added_by_integration` (`PC-003`).
* Excluded: Unrelated UI browser suites.

#### Likely Targets

* src/api/tests/test_representative_expiry_api.py: Create HTTP test module.
* src/api/tests/test_role_endpoint_inventory.py: Add route entries.
* src/api/pyproject.toml: Add `test_representative_expiry_api` to `disallow_untyped_calls = false`.

#### Dependencies

* P02.

#### Validation Expectations

* `test_representative_expiry_api.py`, `test_resident_demo_api.py`, `test_resident_api.py`, and `test_role_endpoint_inventory.py` all pass.

#### Completion Evidence

* Passing test output across both HTTP servers and full role matrix inventory.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T03 -->
### P03-T03: Run `ruff check`, `ruff format --check`, `mypy`, and unit test suites in `src/core` and `src/api`

#### Context

Caller Scope #4 mandates `ruff check`, `ruff format --check`, `mypy`, and affected unit tests in `src/core` and `src/api`.

#### Intent

Execute all four validation gates in `src/core` and `src/api` and record exact commands and outcomes.

#### Boundaries

* Included: `ruff check`, `ruff format --check`, `mypy`, and `unittest` discovery in `src/core` and `src/api`, plus `python3 tools/rename-zava-tests.py` sanity check if applicable.
* Excluded: Pushing to remote.

#### Likely Targets

* No code changes unless fixing a lint/type/test defect surfaced by the gate.

#### Dependencies

* P03-T01, P03-T02.

#### Validation Expectations

* Exit status `0` for every check.

#### Completion Evidence

* Recorded command logs in `.copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-changes.md`.

#### Unresolved Items

* None.
