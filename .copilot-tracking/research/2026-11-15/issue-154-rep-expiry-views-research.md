<!-- markdownlint-disable-file -->

# Task Research: issue-154-rep-expiry-views

| Field              | Value                                                                          |
|--------------------|--------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                     |
| Researcher / agent | rpi-research (under RPI Agent)                                                 |
| Status             | Complete                                                                       |
| Artifact path      | .copilot-tracking/research/2026-11-15/issue-154-rep-expiry-views-research.md   |

## Research Brief

* What to research: How Zava Forward currently models, projects, and enforces representative authority, task-limited views, and authority expiry across `src/core` (`resident_decisions.py`, `resident_preview.py`, `resident_showcase.py`, `resident_journey_design.py` if present) and `src/api` (`app.py`, resident session/showcase/preview endpoints, and tests), and what exact gap remains for Issue #154 Criterion 3 (`Representative views show only task-limited authority and expire as recorded`).
* Why it matters: Closure audit for Issue #154 identified Criterion 3 as unmet specifically due to resident-session/request-time enforcement of representative expiry and task-limited view projection (`FR-045`, `FR-046`, `NFR-008`, `NFR-009`).
* Audience or intended use: Planning (`rpi-plan` + `rpi-plan-critique`), implementation (`rpi-implement`), and verification (`rpi-review`) on branch `feat/ux-154-rep-expiry-views`.
* Scope: `src/core/src/zava_forward/core/` resident modules, `src/api/src/zava_forward/api/` resident/staff endpoints, `src/core/tests/test_resident_journey_design.py`, `src/api/tests/`, `docs/reference/research/ux/customer-journeys/residents.md`, `docs/brds/agentic-retrofit-programme-brd.md`, and `docs/prds/zava-forward-retrofit-programme-demonstrator.md`.
* Non-goals: Conflicting edits to `src/api/src/zava_forward/api/web/role-screens.js`, live outbound resident communication, usability programme execution (#155), OD-41/OD-42 policy sign-off, or pushing commits to remote.
* Criteria: Every codebase claim grounded in `path:line`; clear mapping to `FR-045`, `FR-046`, `NFR-008`, `NFR-009`, and R1 in `residents.md`; concrete convergence recommendation covering `src/core` and `src/api` without `role-screens.js` conflicts.
* Requested outputs: Converged architecture and API/core contract recommendation for task-limited representative view projection and request/session-time expiry transition.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                                                                           |
|----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | How are representative authority scopes and `expires_at` / `review_date` currently stored, projected, and enforced across resident sessions and staff/resident views, and where must Python `core` and `api` enforce task-limited projection and mid-session expiry? |
| Codebase scope                   | `src/core/`, `src/api/`, `docs/reference/research/ux/customer-journeys/residents.md`, `docs/brds/agentic-retrofit-programme-brd.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `.copilot-tracking/` prior #154 records |
| External scope                   | none                                                                                                                                                                            |
| Initial internal candidate areas | `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/src/zava_forward/core/resident_preview.py`, `src/core/src/zava_forward/core/resident_showcase.py`, `src/core/tests/test_resident_journey_design.py`, `src/api/src/zava_forward/api/app.py`, `src/api/tests/test_resident_demo_api.py`, `src/api/tests/test_resident_api.py` |
| Initial external candidate areas | none                                                                                                                                                                            |
| Research posture                 | balanced                                                                                                                                                                        |
| Posture provenance               | default (bounded internal task with named targets plus adjacent resident session/showcase/preview contracts to reconcile)                                                       |
| Explicit limits / deadline       | Keep Python changes in `src/core` and `src/api`; avoid conflicting edits to `src/api/src/zava_forward/api/web/role-screens.js`; do not push.                                   |
| Posture-specific completion basis| balanced scope coverage and adequate evidence across core models, resident session/API routes, and requirement specifications                                                   |
| Edits allowed during research?   | no, research-only                                                                                                                                                               |
| Resolved evidence root           | `.copilot-tracking/`                                                                                                                                                            |
| Known constraints / excluded sources | Read-only during research; preserve existing resident/staff contracts; no private datasets; no `.copilot-tracking/` references in production code or commit messages.       |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                                      | Match and provenance                                             | Scoped authority or output contract                                              | Selected / skipped reason                                                                 |
|---------------------|------------------------------------------------|------------------------------------------------------------------|----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` (AMA repo)   | `applyTo: "**"` matches workspace and tracking inputs            | Enforces KB reading, evidence labeling, Python test commands, validation tiers   | Selected: mandatory repository instructions                                               |
| Skill               | `web-design-guidelines` / `redesign-existing-projects` | Web UI skills in `.agents/skills/`                       | Applies to web HTML/CSS/JS edits; backend-only/Python work is exempt             | Skipped for research/backend scope unless web edits become unavoidable (caller prefers Python-only) |
| Skill               | `accessibility`                                | Consolidated accessibility skill                                 | WCAG 2.2 / Section 508 guidance                                                  | Skipped: no frontend UI component redesign requested; R1 plain-language/status rules inspected directly |
| Research specialist | `hve-core-all:rpi-researcher`                  | Registered general research lane subagent                        | Writes bounded subagent lane artifact                                            | Skipped (inline preferred): tightly coupled 5-8 file Python/doc trace fits direct inspection cleanly |
| Research specialist | `Housing Resident Engagement Lead`             | Company role agent for resident consent/trust                    | Sector-informed hypothesis elicitation                                           | Skipped: requirements FR-045, FR-046, NFR-008, NFR-009, and R1 are already specified in repo docs |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                     | Answers / unanswered | Resulting decision or selected further research                                         |
|------------------|---------------------------------------------------------------------------------------------------------------------------|----------------------|-----------------------------------------------------------------------------------------|
| Intake           | Non-interactive execution with explicit caller scope, target modules, requirements, validation commands, and commit rule. | N/A (non-interactive)| Proceed directly with Cycle 1 balanced codebase research.                               |
| Direction change | None at intake.                                                                                                           | N/A                  | Retain caller boundaries (Python `src/core` + `src/api`, avoid `role-screens.js` edits).|
| Convergence      | Non-interactive convergence: evidence across `residents.md`, `resident_decisions.py`, `resident_preview.py`, `resident_showcase.py`, `resident_demo/app.py`, and `server.py` uniquely selects a shared `zava_forward.core.resident_journey_design` enforcement module wired into `resident_decisions`, `resident_demo`, and `server.py` without editing `role-screens.js`. | Converged | Proceed to `rpi-plan` + `rpi-plan-critique` with `Planning Readiness: Ready`. |

## Scope and Success Criteria

* Scope: Representative authority modeling, task-limited view projection, and request/session-time expiry enforcement across `src/core` and `src/api` for Issue #154 C3.
* Assumptions:
  * `resident_journey_design.py` may not yet exist as a module in `src/core/src/zava_forward/core/` (only `test_resident_journey_design.py` appeared in initial glob), which must be verified.
  * Resident sessions (`resident_showcase.py` / `resident_preview.py` / `app.py`) may validate grants at sign-in or preview time without full mid-session `expires_at` transition or dedicated task-limited view projection across resident/staff API surfaces.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs when the design space and output mode require it. A recommendation is selected only in convergence mode.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Inspect `resident_journey_design.py` (or `resident_decisions.py` / `portal.py`), `app.py`, `role-screens.js` (read-only if avoiding edits), `test_resident_journey_design.py`, and `src/api/tests/`; determine how to implement and enforce task-limited representative view projection and session/request-time representative expiry (`FR-045`, `FR-046`, `NFR-008`, `NFR-009`).
* Inferred research questions: How do `resident_decisions.py`, `resident_preview.py`, and `resident_showcase.py` (plus SQL showcase if applicable) interact with `app.py` resident/staff endpoints, and how did the Issue #154 status record (`2026-11-04`) define the remaining C3 gap?
* Caller constraints and non-goals: Convergence mode preparing `rpi-plan`; avoid conflicting edits to `role-screens.js` if possible; do not push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                      | Source / checkpoint | Effect on active brief, evidence, or revalidation                                  |
|----------------------------------------------------------|------------------------------------------------------------------------------------------------------------|---------------------|------------------------------------------------------------------------------------|
| narrow                                                   | Prefer placing API/core view projection and `resident_journey_design` enforcement in `src/core` and `src/api` Python modules + tests rather than editing `role-screens.js`. | Caller intake       | Constrains recommendation and contrarian alternatives to Python core/API surfaces. |
| exclude                                                  | Do not push commits to remote.                                                                             | Caller intake       | Local commit only after review/validation.                                         |

## Research Questions

|  # | Sub-question                                                                                                                                      | Type (depth / breadth / straightforward) | Priority | Status   |
|---:|---------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------|----------|----------|
| Q1 | What exact requirements do `FR-045`, `FR-046`, `NFR-008`, `NFR-009`, `residents.md` (R1), and the 2026-11-04 #154 status audit set for C3?       | breadth                                  | H        | answered |
| Q2 | What representative authority models, task scopes, and expiry checks already exist in `src/core` (`resident_decisions.py`, `resident_preview.py`, `resident_showcase.py`, `resident_showcase_sql.py`)? | depth                                    | H        | answered |
| Q3 | How does `src/api/src/zava_forward/api/app.py` (and `role-screens.js` / `resident.js`) currently authenticate, project, and expire representative views and actions during a session? | depth                                    | H        | answered |
| Q4 | What is the cleanest architecture in `src/core` (including `resident_journey_design.py`) and `src/api` to enforce task-limited projection and request/session-time `expires_at` expiry with safe renewal routing and zero regression to existing tests? | depth                                    | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/research/2026-11-01-issue-154-rep-expiry-research.md`, `.copilot-tracking/research/2026-11-04/issue-154-status-record-research.md`, `.copilot-tracking/plans/2026-11-01/issue-154-rep-expiry-plan.md`, `.copilot-tracking/reviews/2026-11-04/issue-154-status-record-review.md`, `.copilot-tracking/rpi-sessions/2026-10-27/resident-content-153-154-state.json`.
* Reused (verified) findings:
  * `docs/reference/research/ux/customer-journeys/residents.md` defines J1-J6 and R1 (`Task-limited representative briefing and actions`), pinned by `src/core/tests/test_resident_journey_design.py`.
  * `src/core/src/zava_forward/core/resident_decisions.py` implements `AUTHORITY_TASKS`, `AUTHORITY_STATUSES`, `authority_for()`, `_res_representative_record`, and `_res_disclosure_check`, using `authority_date <= k.today() < review_date`.
  * `src/core/src/zava_forward/core/resident_preview.py` implements a loopback-only read-only synthetic preview (`Grant`, `resolve_grant`, `resident_view`), which omits `home`, checks `_authority_current`, and maps `Receive information` and `Attend` only.
* Superseded / stale:
  * `src/core/src/zava_forward/core/resident_journey_design.py` and `src/api/src/zava_forward/api/app.py` do not exist yet; the HTTP servers are `src/api/src/zava_forward/api/server.py`, `src/api/src/zava_forward/api/resident_demo/app.py`, and `src/api/src/zava_forward/api/resident_preview/app.py`.
  * The 2026-11-04 status record left Criterion 3 unmet specifically because `resident_preview.py` is only a static read-only preview boundary (`Receive information` + `Attend` fields, returning a generic 403 `"You cannot see this page."` on expiry with no recorded expiry timestamp or renewal route), and neither a dedicated `resident_journey_design.py` representative view/action projection with timestamped `expires_at` enforcement nor resident-session / API representative view & action expiry transition exists.

## Research Cycle Log

### Cycle 1

* Active direction controls: caller narrow (`src/core` and `src/api` Python modules + tests; avoid `role-screens.js` edits), caller exclude (no push).
* Active research posture and completion basis: `balanced`; balanced scope coverage and adequate evidence across core models, resident session/API routes, and requirement specifications.
* Explicit limits or deadline effect: none beyond caller file-conflict avoidance and no-push boundary.

#### Wave 1: Wider

* Plan and independent lanes: Inline breadth sweep across Issue #154 specification (`residents.md`, `agentic-retrofit-programme-brd.md`, `zava-forward-retrofit-programme-demonstrator.md`), prior #154 tracking artifacts, and full `src/core` + `src/api` module inventory.
* Worker evidence relationships or inline fallback: Inline (5-8 tightly coupled files):
  * Q1 -> `residents.md:293-336` (R1 wireframe & table), `agentic-retrofit-programme-brd.md:1539-1540,1634,1646` (`FR-045`, `FR-046`, `NFR-008`, `NFR-009`), `zava-forward-retrofit-programme-demonstrator.md:1420-1421,2151-2160` (`FR-045`, `FR-046`, `AC-055`, `AC-056`, `AC-064`).
  * Q2 -> `resident_decisions.py:40-41,984-997,1645-1684`, `resident_preview.py:24-31,182-419`, `resident_showcase.py:139-550`, `projection.py:165-215`.
  * Q3 -> `server.py:884-902,1636-1662`, `resident_demo/app.py:107-260`, `resident_preview/app.py:55-150`. Confirmed `resident_journey_design.py` does not yet exist in `src/core/src/zava_forward/core/`.
* Reflection: Wave 1 revealed the exact structural gap! `resident_decisions.py` only stores day-granular `authority_date`/`review_date` and throws a plain `ValueError` during staff writes; `resident_preview.py` only covers `Receive information` and `Attend` (ignoring `Communicate` and `Works decision`, omitting recorded scope/version/wishes/expiry metadata, and returning generic 403 on expiry rather than transitioning a session/view to an expired/held state with recorded expiry timestamp and safe renewal route); `resident_showcase.py` / `resident_demo/app.py` only models household `resident` rows (no task-limited representative view/session projection or `expires_at` authority enforcement), and `server.py` has no dedicated representative view/session projection endpoint! Wave 2 must inspect `resident_decisions.py` (decision/appointment interactions), `appointments.py`, `resident_demo/app.py` (all routes), `resident_showcase_sql.py`, `role-screens.js` (to ensure zero conflict), and existing tests (`test_resident_api.py`, `test_resident_demo_api.py`, `test_resident_preview.py`).

#### Wave 2: Deeper

* Prioritized lanes and why: Inline deep inspection of (1) domain authority schemas and date/timestamp boundaries across `resident_decisions.py`, `appointments.py`, `resident_preview.py`, and `resident_showcase.py`, and (2) HTTP session/API handlers and strict typing/linting contracts in `server.py`, `resident_demo/app.py`, `src/core/pyproject.toml`, and `src/api/pyproject.toml`.
* Worker evidence relationships or inline fallback: Inline:
  * Q2 -> `resident_decisions.py:40-41` defines `AUTHORITY_TASKS = ("Receive information", "Communicate", "Attend", "Works decision")` and `AUTHORITY_STATUSES = ("Confirmed", "Unclear", "Disputed", "Revoked")`. `authority_for()` (`resident_decisions.py:984-997`) validates latest version, `status == "Confirmed"`, `task in a["tasks"]`, `measure`, `context_revision`, `safe_contact_ref`, `safe_contact_revision`, and `authority_date <= k.today() < review_date`, without timestamped `expires_at` support. `_res_representative_record` (`resident_decisions.py:1645-1672`) stores day strings `authority_date` and `review_date`.
  * Q2 -> `appointments.py:345-356` validates appointment-specific authority (`task="Appointment agreement"`, timezone-aware UTC `valid_from <= now < valid_to`, `not revoked`) bound to a specific offer, measure, and `context_revision`.
  * Q2 -> `resident_preview.py:402-419` projects only `progress` (`Receive information`) and `appointments` (`Attend`) for static preview grants and raises `GrantDenied("no_current_authority")` (`test_resident_preview.py:217-240`) with message `"You cannot see this page."`.
  * Q3 -> `resident_demo/app.py:106-280` implements cookie-signed (`__Host-zfdemo`) sessions via `SessionCodec` (`resident_showcase.py:390-465`) over `/demo/session`, `/demo/login`, `/demo/view`, `/demo/assistant`, `/demo/agenda`, and `/demo/logout`, admitting only household `ShowcaseRow` entries (`resident_showcase.py:187-215`).
  * Q3 -> `role-screens.js:1585-1625` only renders `r.representative_ref` in a read-only staff service-issues table and explicitly notes `"Resident-facing screens are designed separately"` (`role-screens.js:1592`), confirming zero edits to `role-screens.js` are required.
  * Q4 -> `src/core/pyproject.toml:26-44` and `src/api/pyproject.toml:30-60` enforce `ruff` (`line-length = 100`, `E,F,I,B,UP`) and `mypy --strict` on all non-exempt modules (including new modules such as `resident_journey_design.py`, `resident_showcase.py`, `resident_demo/app.py`, and new tests).
* Reflection: Wave 2 confirmed all domain invariants and typing constraints. Before converging, Wave 3 (Contrarian) must probe hidden test/contract invariants that could break if we mutate existing schemas or add routes carelessly.

#### Wave 3: Contrarian

* Challenge lanes and in-scope alternatives:
  1. Challenge mutating `ShowcaseRow` (`ROW_KEYS`) in `resident_showcase.py` vs keeping `ShowcaseRow` frozen and introducing an explicit representative session/grant contract.
  2. Challenge adding routes to `src/api/src/zava_forward/api/server.py` against repository-wide role/route inventory tests.
  3. Challenge surfacing `expires_at` on missing/unknown subjects vs recorded-grant expiry/revocation (information-leak counter-check under R1 `"No case details in denied response"`).
* Worker evidence relationships or inline fallback: Inline:
  * Counter-finding 1 (`test_resident_showcase.py:38-40,115-120` and `resident_showcase_sql.py`): `parse_row` strictly rejects any extra or missing keys outside `rs.ROW_KEYS`. Mutating `ShowcaseRow` required keys would break SQL reader and strict row-parsing tests. Therefore, `ShowcaseRow` and `ROW_KEYS` must stay unchanged; representative sessions in `ResidentDemo` should use an explicit, optional `RepresentativeSessionBinding` / representative authority resolver alongside `ShowcaseReader`.
  * Counter-finding 2 (`src/api/tests/test_role_endpoint_inventory.py:18-68`): `RoleEndpointInventory.test_inventory_covers_every_route_in_the_server` regex-scans `server.py` for `/api/...` string literals and tests every staff/contractor/mystery role against every endpoint, asserting zero `500`s, `403` for contractors/unauthorized roles, and zero canary leaks (`REASON`, `PHONE`, `RESIDENT`, `NOTE_CANARY`, `OUTCOME_CANARY`). Any new route in `server.py` (such as `/api/cases/<id>/representative-view`) must be gated by `projection.allowed(u, "case")` and `RESIDENT_VIEW_ROLES`, and added to `GET_ENDPOINTS` / `POST_ENDPOINTS` in `test_role_endpoint_inventory.py`.
  * Counter-finding 3 (`residents.md:298`, `test_resident_preview.py:231-239`): Surfacing case data or fabricating an expiry timestamp when a representative was never recorded on a case would violate `"No case details in denied response"`. When a representative's recorded grant expires or is held (`Revoked`, `Disputed`, `Unclear`, `safe_contact_changed`, `scope_changed`, `missing_expiry`), the expired/held transition must strip all case/measure/appointment/complaint/decision/home fields, return `expires_at` only from the representative's own recorded grant (or `None` when unrecorded/missing), and surface the generic safe staff/resident renewal route with zero household PII or canary text.
* Reflection: Contrarian checks uncovered two critical repository invariants (`ROW_KEYS` strictness and `test_role_endpoint_inventory.py` route regex + canary sweep) and sharpened the non-disclosure contract for expired/held transitions. Cycle 1 evidence is complete and saturated; no Cycle 2 is needed.

#### Cycle 1 Parent Synthesis

* Accepted into parent synthesis:
  * Create `src/core/src/zava_forward/core/resident_journey_design.py` (fully `mypy --strict` and `ruff` clean) as the single source of truth for task-limited representative view projection (`project_representative_view`), live authority & timestamped `expires_at` evaluation (`evaluate_representative_authority`), session state transitions (`RepresentativeSession`, `RepresentativeSessionStore`), and task-scoped action enforcement (`enforce_representative_action`) (`C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C11`).
  * Extend `src/core/src/zava_forward/core/resident_decisions.py` (`_res_representative_record`, `authority_for`) with optional timezone-aware UTC `expires_at` support alongside `review_date` (`YYYY-MM-DD`, whose start-of-day `00:00:00Z` remains the hard upper bound per R1) and expose `Store.representative_view` / `Store.representative_action_check` (`C5`, `C6`, `C7`).
  * Wire both HTTP surfaces in `src/api`:
    1. Resident-session enforcement in `src/api/src/zava_forward/api/resident_demo/app.py` (backed by typed representative bindings in `resident_showcase.py` without altering `ShowcaseRow` / `ROW_KEYS`) so representative sessions project only task-limited views on `/demo/view`, enforce task scope on `/demo/assistant` and `/demo/agenda`, and immediately transition mid-session to `expired` / `held` state (blocking actions, stripping disclosures, surfacing recorded `expires_at` and safe renewal route) the moment `clock` passes `expires_at` or authority becomes missing/revoked/disputed/unclear (`C9`, `C10`, `C13`, `C15`).
    2. Staff/case API projection and session-action check in `src/api/src/zava_forward/api/server.py` (`/api/cases/<id>/representative-view` GET/POST, gated by `projection.allowed(u, "case")` and `RESIDENT_VIEW_ROLES`, registered in `test_role_endpoint_inventory.py`) (`C12`, `C14`).
* Rejected with rationale:
  * Editing `src/api/src/zava_forward/api/web/role-screens.js`: rejected per caller constraint and `C16` (`role-screens.js:1592` explicitly separates resident-facing screens from staff read-only tables).
  * Mutating `ShowcaseRow` / `ROW_KEYS` in `resident_showcase.py`: rejected because `parse_row` and `resident_showcase_sql.py` enforce exact `ROW_KEYS` (`C13`, `C15`).
  * Replacing `GrantDenied` in `resident_preview.py`: rejected because `test_resident_preview.py:217-240` pins the static grant-file `GrantDenied` message `"You cannot see this page."` (`C8`).
* Deferred / re-entry decision: No re-entry required; all four research questions are answered with direct `path:line` evidence.

## Synthesized Findings

### Q1: Requirements and Issue #154 C3 Scope

* **R1 contract (`C1`, `C2`)**: `residents.md` Journey R1 (`Task-limited representative briefing and actions`) requires every representative screen/response to verify recorded authority first, state `"You may [recorded task] for [scope/version] until [recorded date]"`, show authority source/review/expiry and the resident's stated wishes, project only task-scoped content, never imply works consent without `Works decision` authority, treat authority as unavailable from its review date (`00:00:00Z`) or recorded `expires_at` timestamp, and deny/hold missing, unclear, disputed, expired, or revoked authority with `"We cannot share this task's details until a person checks your permission. Ask the named officer to confirm it safely with the resident."` plus a non-digital resident/staff confirmation route and zero case details in the denied response.
* **BRD/PRD alignment (`C3`, `C4`)**:
  * `FR-045` (`AC-087` / PRD `AC-055`, `AC-064`): task-limited authority (`Receive information`, `Communicate`, `Attend`, `Works decision`) bound to measure, scope, design version, safe contact, resident wishes, and expiry/review timestamp; expired, unclear,puted, or revoked authority immediately holds disclosure and consent actions; multiple representatives never receive the union of each other's permissions; changed safe contact or scope invalidates reliance until re-confirmed.
  * `FR-046` (`AC-088` / PRD `AC-056`): offered appointment slots remain visibly labelled as offers (`Offered - not booked`) distinct from confirmed commitments (`Visit confirmed`), and pause/withdrawal stays scoped to the authorized measure without mutating sibling measures.
  * `NFR-008` & `NFR-009`: accessible plain-language status/renewal messaging with non-digital phone/letter/visit fallback, deterministic least-privilege projection (positive allowlist), and no leakage of sensitive household notes, safe-contact values, or out-of-scope records into views or AI assistant prompts.

### Q2 & Q3: Existing Codebase State and Exact Engineering Gap

* `src/core/src/zava_forward/core/resident_journey_design.py` does not exist yet; `src/core/tests/test_resident_journey_design.py` (`C11`) currently asserts only Markdown text in `residents.md`.
* `resident_decisions.py` (`C5`, `C6`) stores `authority_date` and `review_date` (`YYYY-MM-DD`) without timestamped `expires_at` and validates authority only inside staff write mutations (`_res_disclosure_check`, `_res_decision_record`), returning a generic string error rather than projecting a task-limited representative view or structured expired/held state.
* `resident_preview.py` (`C8`) is a loopback static preview covering only `Receive information` and `Attend` on synthetic grant files, omitting `Communicate` and `Works decision` task projections, omitting recorded `expires_at` and renewal routes on expiry, and lacking session lifecycle state.
* `resident_showcase.py` (`C9`) and `resident_demo/app.py` (`C10`) authenticate only household `resident` `ShowcaseRow` principals; there is no representative session support, no task-limited view/assistant/agenda scoping, and no mid-session transition to an expired/held representative view surfacing recorded `expires_at` and safe renewal routes.
* `server.py` (`C12`) exposes `/api/cases/<id>/resident` for staff mutations and `/api/cases/<id>/home-case` for full staff case views, but has no task-limited `/api/cases/<id>/representative-view` projection or representative session/action expiry endpoint.

### Q4: Selected Convergence Architecture

| Alternative | Summary | Trade-offs | Disposition |
|---|---|---|---|
| **Option A (Selected): Canonical `resident_journey_design.py` + `resident_decisions` `expires_at` + `resident_demo` & `server.py` integration** | Implement positive-allowlist task projection, `expires_at` parsing/enforcement, and `RepresentativeSession` expired/held state machine in `src/core/src/zava_forward/core/resident_journey_design.py`; add backwards-compatible optional `expires_at` enforcement in `resident_decisions.py`; wire mid-session representative view/action expiry in `resident_demo/app.py` (with separate `RepresentativeBinding` preserving `ShowcaseRow`) and staff/case `/api/cases/<id>/representative-view` in `server.py`. | Covers both resident-session (`/demo/*`) and case-store (`/api/cases/<id>/representative-view` + `Store`) surfaces; zero edits to `role-screens.js`; preserves all `ShowcaseRow` and `GrantDenied` invariants. | **Selected** |
| Option B: Modify `resident_preview.py` and `ShowcaseRow` in-place | Add `Communicate`/`Works decision` and `expires_at`/held payloads directly into `resident_preview.py` and add representative columns to `ShowcaseRow` (`ROW_KEYS`). | Breaks `test_resident_preview.py` (`GrantDenied` contract) and `test_resident_showcase.py` / `resident_showcase_sql.py` (`ROW_KEYS` strict schema). | Rejected |
| Option C: Core-only helper without HTTP session/API wiring | Implement `resident_journey_design.py` only in `src/core` without `src/api` route/session enforcement. | Fails caller Scope #1/#2/#3 requiring `src/api` enforcement and `src/api/tests/` proving session/request-time representative expiry. | Rejected |

## Evidence Log

| ID  | Source (`path:line`) | Kind | Verified claim |
|-----|----------------------|------|----------------|
| C1  | `docs/reference/research/ux/customer-journeys/residents.md:280-292` | Design spec | Journey R1 defines task-limited representative wireframe (`Helping with this task`, `You may [recorded task] for [scope/version] until [recorded date]`), forbids inferring works consent from interpreter/scheduling authority, and specifies authority unavailability from the review date. |
| C2  | `docs/reference/research/ux/customer-journeys/residents.md:293-312` | Design spec | R1 specifies held/denied handling for missing, unclear, disputed, expired, or revoked authority (`We cannot share this task's details until a person checks your permission. Ask the named officer to confirm it safely with the resident.`, zero case details, non-digital confirmation route). |
| C3  | `docs/brds/agentic-retrofit-programme-brd.md:1539-1540` | Requirement | `FR-045` (`AC-087`) and `FR-046` (`AC-088`) define task-limited representative authority, source, scope, expiry/review date, resident wishes, immediate stop on expired/unclear/disputed authority, non-union across multiple representatives, safe-contact change invalidation, and offer-vs-confirmed commitment separation. |
| C4  | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:1420-1421,1517-1525` | Requirement | PRD `FR-045`, `FR-046`, `NFR-008`, and `NFR-009` require exact home/measure/scope/design-version bindings, holding disclosure and consent on expired/unclear/disputed authority, measure-scoped pause/withdrawal, non-digital/interoperable parity, and least-privilege context boundaries. |
| C5  | `src/core/src/zava_forward/core/resident_decisions.py:40-41,984-997` | Code | Defines `AUTHORITY_TASKS`, `AUTHORITY_STATUSES`, and `authority_for()`, checking `Confirmed` status, task membership, measure, `context_revision`, `safe_contact_ref`, `safe_contact_revision`, and `authority_date <= k.today() < review_date` (no timestamped `expires_at` check yet). |
| C6  | `src/core/src/zava_forward/core/resident_decisions.py:1645-1709` | Code | `_res_representative_record`, `_res_disclosure_check`, and `_res_decision_record` record day-granular `authority_date`/`review_date` and gate representative works decisions on `authority_for()`. |
| C7  | `src/core/src/zava_forward/core/appointments.py:345-356` | Code | Appointment-specific representative authority (`task="Appointment agreement"`) checks timezone-aware UTC `valid_from <= now < valid_to` and `not revoked` against a specific offer and measure binding. |
| C8  | `src/core/src/zava_forward/core/resident_preview.py:402-419` | Code | Static loopback preview `resident_view` projects only `progress` and `appointments`, raising generic `GrantDenied` pinned by `src/core/tests/test_resident_preview.py:217-240`. |
| C9  | `src/core/src/zava_forward/core/resident_showcase.py:187-215,390-465` | Code | `ShowcaseRow` and `SessionCodec` implement signed cookie sessions for household residents only, with strict `ROW_KEYS` parsing. |
| C10 | `src/api/src/zava_forward/api/resident_demo/app.py:106-280` | Code | `ResidentDemo` serves `/demo/session`, `/demo/login`, `/demo/view`, `/demo/assistant`, `/demo/agenda`, and `/demo/logout` for household `ShowcaseRow` sessions without representative task projection or representative `expires_at` transition. |
| C11 | `src/core/tests/test_resident_journey_design.py:1-78` | Test | Currently checks Markdown phrases in `residents.md` only; `src/core/src/zava_forward/core/resident_journey_design.py` does not yet exist. |
| C12 | `src/api/src/zava_forward/api/server.py:884-902,1636-1662` | Code | Main HTTP server dispatches `/api/cases/<id>/resident` and `/api/cases/<id>/home-case` with role checks; lacks `/api/cases/<id>/representative-view`. |
| C13 | `src/core/tests/test_resident_showcase.py:38-40,115-120` | Test | Enforces strict `rs.ROW_KEYS` schema validation in `rs.parse_row()`, ruling out in-place mutation of `ShowcaseRow` required fields. |
| C14 | `src/api/tests/test_role_endpoint_inventory.py:18-68` | Test | Regex-scans `server.py` for all `/api/...` routes and asserts role authorization (`403` for contractor/mystery) and zero canary leaks across all endpoints. |
| C15 | `src/api/tests/test_resident_demo_api.py:251-284,502-512` | Test | Verifies `Cache-Control: no-store`, zero `@example.com` disclosure on `/demo/session`, and immediate request-time denial on resident row revocation/expiry. |
| C16 | `src/api/src/zava_forward/api/web/role-screens.js:1585-1625` | Web JS | Displays `representative_ref` only in a staff service-issues table and notes resident-facing screens are separate; requires no edits. |

## Decisions, Risks, and Further Research

* **Confirmed / Converged Decisions**:
  * **D1 (Canonical Core Module)**: Create `src/core/src/zava_forward/core/resident_journey_design.py` implementing positive-allowlist task-scoped view projection, `expires_at` (ISO-8601 UTC) + `review_date` (`00:00:00Z` UTC ceiling) evaluation, immediate `expired` / `held` session and view transitions, task-scoped action enforcement, recorded `expires_at` surfacing, and non-digital/staff safe renewal routing (`C1`-`C7`, `C11`).
  * **D2 (Backwards-Compatible Domain `expires_at`)**: Support optional timezone-aware UTC `expires_at` on `_res_representative_record` and `authority_for(..., now=None)` in `resident_decisions.py` so existing `authority_date`/`review_date` callers remain 100% compatible while timestamped `expires_at` expires strictly at `now >= expires_at` (`C5`, `C6`).
  * **D3 (Dual API Enforcement — Resident Session + Case API)**: Enforce representative view projection and request/session-time expiry in both `ResidentDemo` (`resident_demo/app.py` + `resident_showcase.py` `RepresentativeGrant` without mutating `ShowcaseRow`) and `server.py` (`/api/cases/<id>/representative-view` GET/POST gated by `RESIDENT_VIEW_ROLES` and registered in `test_role_endpoint_inventory.py`), with zero edits to `role-screens.js` (`C9`, `C10`, `C12`-`C16`).
* **Open Questions / Residual Risks**:
  * Ensure naive or malformed `expires_at` timestamps fail closed (`held` / `ValueError` on record creation) rather than raising unhandled `TypeError` during UTC comparison.
  * Ensure `/demo/session` for representative sessions never echoes `@example.com` email addresses (`C15`) and `/api/cases/<id>/representative-view` never echoes case canaries to unauthorized roles or when authority is expired/held (`C2`, `C14`).
* **Further Research**: None needed for Issue #154 C3. Downstream empirical resident usability testing remains tracked under Issue #155.

## Readiness and Handoff

* **Research execution status**: Complete (Cycle 1 Wider, Deeper, Contrarian, and Parent Synthesis completed).
* **Research disposition**: `executed`
* **Planning Readiness**: `Ready`
* **Self-check**:
  * [x] Brief, parameters, extension registry, participation, direction controls, and prior-knowledge gate recorded.
  * [x] Cycle 1 completed Wider, Deeper, and Contrarian waves in order before synthesis.
  * [x] Every sub-question Q1-Q4 is answered and backed by `C1`-`C16` `path:line` evidence.
  * [x] Alternatives compared and single convergence recommendation selected with evidence-based rejections.
  * [x] No source files were modified during Research.


