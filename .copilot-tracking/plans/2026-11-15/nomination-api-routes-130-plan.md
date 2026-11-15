<!-- markdownlint-disable-file -->
# RPI Plan: Issue 130 Plain-Language Explanation and Dual-Route API/Workbench Slice

## Task Metadata

* Task ID: nomination-api-routes-130
* Task slug: nomination-api-routes-130
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/nomination-api-routes-130-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/nomination-api-routes-130-plan-critique.md

## Executive Summary

This plan delivers the remaining `src/api` and plain-language explanation slice of Issue #130 (`Nomination, self-referral, acknowledgement and challenge route`, `Refs #130`) on top of the `src/core` domain primitives merged in PR #1710 and PR #1742. It exposes deterministic, permitted plain-language explanations (`human_decision_owner`, `ai_involvement_explanation`, `sources`, `policy_reasons`, `uncertainty_note`) across nomination, follow-up, and challenge API payloads and workbench views—grounded in live `Store.data["recommendations"]` AI involvement metadata and recursive restricted-vulnerability scrubbing—and wires both digital (`channel="digital"`) and equivalent staff-recorded non-digital (`channel="staff_recorded_non_digital"` with phone, paper, letter, in-person, and permitted intermediary assisted intake) routes for nomination acknowledgement, challenge submission, and nomination correction across `src/api` endpoints (`server.py` delegating to typed `nomination_routes.py` and `Store`) and keyboard-operable HTML forms with per-role field-permission and representative `Communicate` authority checks.

### User Decisions and Requirements Highlights

* Continuous five-stage RPI execution (`rpi-research` through `rpi-review`) in isolated worktree `/home/azureuser/source/ama-demo-wt/feat-130-api-routes` on branch `feat/ux-130-api-routes`, ending in a clean frozen local commit with dated `2026-11-15` `.copilot-tracking/` artifacts and no push or pull request.
* Plain-language explanation contract (`Refs #130` AC1) requires deterministic `human_decision_owner`, `ai_involvement_explanation`, `policy_reasons` (with permitted `sources`), and `uncertainty_note` on nomination, follow-up, and challenge API payloads and UI views, filtered by role and field visibility so restricted internal vulnerability data never leaks.
* Dual-route and accessibility contract (`Refs #130` AC2) requires exercising both `channel="digital"` and `channel="staff_recorded_non_digital"` for nomination acknowledgement, challenge submission, and correction across `src/api` endpoints and accessible HTML forms, enforcing per-role field permissions and keyboard operability without breaking any counted `aria-invalid` guard in `src/api/tests/test_accessibility_baseline.py`.
* Focused validation tier runs targeted unit tests in `src/core` and `src/api` (including `test_accessibility_baseline.py`), `ruff check`, `ruff format` checks (`ruff format --check` respecting legacy excludes on `resident_decisions.py`, `store.py`, `projection.py`, and `server.py` plus `ruff format --isolated --line-length 100 --check` on all newly added and non-legacy-excluded modified files), and bare `mypy --cache-dir=/tmp/mypy-130` in `src/core` and `src/api`.

### What You May Not Know

* Static WCAG baseline suites (`src/api/tests/test_accessibility_baseline.py` and `src/api/tests/test_epic149_form_error_summary_associations.py`) hard-pin exact counts across `src/api/src/zava_forward/api/web/*.js`: `9` occurrences of `setAttribute("aria-invalid", "true")` (`1` inside `panels.js`), `14` `h("table", {}, ...)` elements, and verbatim `"before recording this challenge."` recovery copy within strict line-window rules. Sharing a single conditional-field `nominationPanel._routeForm` helper in `panels.js` provides genuine `aria-invalid`, `aria-describedby`, and programmatic `.focus()` error recovery across nomination acknowledgement, nomination correction, and challenge forms while allowing optional/conditional fields (`assisted_channel` on digital routes, unlinked `challenge_id`, non-representative `representative_ref`, unchanged `owner_reassignment_reason`) and preserving all pinned baseline counts.
* `src/api/tests/test_content_standard.py` enforces an exact `AUDITED_FILES` set under `web/`, forbids `BANNED` internal jargon (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`) on every line including JS comments, and enforces `BLOCKED_WORDS` (`cannot`, `could not`, `unavailable`, `failed`, `refused`, etc.) on non-error UI copy, while `test_nomination_screen.py` forbids `": None"` in legacy fallback `<dd>` values.
* `src/api/src/zava_forward/api/server.py` delegates `GET /api/cases/<cid>` and `POST /api/cases/<cid>/resident` surgically through strictly typed `src/api/src/zava_forward/api/nomination_routes.py` without introducing new `/api/...` route string literals, keeping `test_role_endpoint_inventory.py` green while ensuring `nomination_routes.py` executes on live HTTP requests.
* `src/api/tests/test_nomination_screen.py` evaluates an isolated slice of `panels.js` calling `nominationPanel(c)` with one argument and plain `{tag, attrs, kids}` nodes and asserts `controls == []`, while `src/api/checks/nomination_browser_check.py` asserts pressing `Tab` from `#nominations-title` focuses the first nomination `<summary>`. Keying record actions on `r.id`, guarding DOM helpers in isolated slice mode, and placing interactive `<details><summary>` action forms inside each nomination `<details>` card below its `<summary>` and `<dl>` lists preserves both invariants.

### Unresolved Decisions or Blockers

* Human governance open decisions `OD-41` and `OD-42` and authorized human representative comprehension sign-off remain external human gates on Issue #130 (`Refs #130`, never a closing keyword). No engineering blockers prevent local delivery and verification of AC1 and AC2.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Execute all five RPI stages (`rpi-research`, `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, `rpi-review`) continuously in `/home/azureuser/source/ama-demo-wt/feat-130-api-routes` on branch `feat/ux-130-api-routes` stacked on `origin/feat/demo-233-same-home-tensions-0825` (`a1d0be5f611eeb1f3b5bb88f996bb9448a6e72b0`), commit code, tests, and dated `2026-11-15` `.copilot-tracking/` artifacts with the Copilot `Co-authored-by` trailer and `Refs #130`, and do not push or open a pull request (caller prompt).
* Expose and render a deterministic, permitted plain-language explanation on nomination, follow-up, and challenge views and API payloads stating whether AI was involved, which sources and policy reasons apply, any uncertainty or missing-evidence notes, and that a named human owns every decision (`human_decision_owner`, `ai_involvement_explanation`, `policy_reasons`, `uncertainty_note`), with role and field-level visibility filtering so restricted internal vulnerability details are never leaked (caller prompt AC1; Issue #130; `docs/brds/agentic-retrofit-programme-brd.md` FR-037, FR-041, AC-065, RULE-005).
* Wire both the digital route (`channel="digital"`) and the equivalent staff-recorded non-digital route (`channel="staff_recorded_non_digital"` with phone, paper, letter, or in-person assisted intake) for nomination acknowledgement, challenge submission, and correction in `src/api` endpoints and accessible HTML forms/views, enforcing per-role field-permission checks and keyboard operability without breaking any counted `aria-invalid` guard in `src/api/tests/test_accessibility_baseline.py` (caller prompt AC2; Issue #130; `docs/prds/zava-forward-retrofit-programme-demonstrator.md` FR-037, FR-043, FR-052, AC-071).
* Validate at the focused tier using targeted unit tests in `src/core` (`test_nomination_route.py`, `test_resident_decisions.py`) and `src/api` (nomination and challenge route API, UI, keyboard, and permission tests plus `test_accessibility_baseline.py`), `python3 -m ruff check`, `python3 -m ruff format --isolated --line-length 100 --check` on modified files, and bare `python3 -m mypy` inside `src/core` and `src/api` with `--cache-dir=/tmp/mypy-130` (caller prompt).

## Goals

* Deliver deterministic, role- and field-filtered plain-language explanation objects across nomination, follow-up, and challenge API responses and Resident-tab UI panels with provable non-leakage of restricted internal vulnerability data.
* Enable both `channel="digital"` and `channel="staff_recorded_non_digital"` (assisted phone, paper, letter, in-person, and permitted intermediary intake) across nomination acknowledgement, challenge submission, and nomination correction in both `src/core` / `src/api` HTTP endpoints and accessible workbench HTML forms while preserving backward compatibility with existing channel labels.
* Enforce role, named-owner, representative-authority, and closed-schema field permissions across API and UI surfaces, while preserving every repository WCAG 2.2, plain-language content-standard, focus-order, formatting, and strict-typing invariant.

## Scope and Non-Goals

### In Scope

* Pure strict-typed plain-language explanation builders, recursive restricted-key scrubbers, viewer visibility filters, and dual-route channel normalization in `src/core/src/zava_forward/core/nomination_route.py`.
* Workflow action and detail projection wiring in `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/src/zava_forward/core/store.py`, and `src/core/src/zava_forward/core/projection.py` (`nomination_acknowledge`, `challenge_open`, `nomination_correct`, `nomination_record`, `followup_view`, `challenge_catalog`, `Store.detail` reading `self.data["recommendations"]`, `projection.redact_staff_detail`).
* Strictly typed API boundary helpers in `src/api/src/zava_forward/api/nomination_routes.py`, surgical delegation from `src/api/src/zava_forward/api/server.py` (`GET /api/cases/<cid>` and `POST /api/cases/<cid>/resident`), and accessible Resident-tab HTML views and keyboard-operable forms in `src/api/src/zava_forward/api/web/panels.js` and `src/api/src/zava_forward/api/web/app.js`.
* Focused unit, live-HTTP API, role/field-permission, representative `Communicate` authority, vulnerability non-leakage, plain-language explanation, and keyboard/DOM accessibility tests in `src/core/tests/` and `src/api/tests/`.

### Non-Goals

* Pushing branches, opening or updating GitHub pull requests, or claiming closure of Issue #130 (`OD-41`, `OD-42`, and human representative sign-off remain open).
* Altering counted `aria-invalid` (`9`) or `table` (`14`) totals in `src/api/tests/test_accessibility_baseline.py`, adding new `.js`/`.html` files outside `AUDITED_FILES` in `src/api/tests/test_content_standard.py`, or mass-reformatting legacy-excluded files (`resident_decisions.py`, `store.py`, `projection.py`, `server.py`).
* Converting separate read-only showcase apps (`resident_demo`, `resident_preview`) into write-capable staff endpoints.

## Functional Requirements

* FR-1 (Deterministic plain-language explanation): Nomination records, nomination `follow_up` views, `affected_challenges`, and `challenge_targets` expose a `plain_language_explanation` mapping with `permitted` (`True`), `human_decision_owner`, `ai_involvement_explanation`, `sources`, `policy_reasons`, and `uncertainty_note`, constructed solely from allowlisted workflow fields and rendered in plain language in `nominationPanel` and `affectedChallengePanel`.
  * Observable acceptance criteria: API `GET /api/cases/<cid>` and `POST /api/cases/<cid>/resident` responses and rendered `#nominations` and `#affected-challenges` DOM sections display deterministic `human_decision_owner`, `ai_involvement_explanation`, `policy_reasons`, `sources`, and `uncertainty_note` reflecting no-AI versus AI-assisted priority-suggestion involvement and preserving `Unknown` status values without fabricating `None`.
* FR-2 (Role and field-level vulnerability redaction): Restricted internal vulnerability, health, adjustment, safeguarding, and contact/hazard note fields (`resident.reason`, `resident.adjustment`, `resident.support`, `resident.priority_support`, `contacts[*].note`, `hazards[*].note`, `internal_vulnerability_note`, `health_detail`, `safeguarding_note`, and `permitted=False` records) are excluded from `plain_language_explanation` and redacted or omitted across unauthorized roles (`Contractor`, `Building Safety Liaison`, `Retrofit Coordinator`, `Quality Inspector`, `Grants and Evidence Officer`, `Programme Support Officer` without reason role, and view-only `Application Administrator`).
  * Observable acceptance criteria: Canary strings planted in restricted vulnerability fields and private intake accounts never appear in `plain_language_explanation` for any viewer and never appear anywhere in `GET /api/cases/<cid>` or rendered HTML for unauthorized roles.
* FR-3 (Digital and staff-recorded non-digital routes): `nomination_acknowledge`, `challenge_open`, and `nomination_correct` (plus `nomination_record`) accept `channel="digital"` and `channel="staff_recorded_non_digital"` (with optional `assisted_channel` for phone, paper, letter, in-person, and permitted intermediary intake, rejecting `assisted_channel` on digital submissions) alongside existing channel labels, persisting `channel`, `route_mode`, and `assisted_channel` and exposing both routes in workbench HTML forms.
  * Observable acceptance criteria: Submitting both `channel="digital"` and `channel="staff_recorded_non_digital"` via `POST /api/cases/<cid>/resident` and through the workbench HTML form payloads succeeds (`200`) for authorized roles on nomination acknowledgement, challenge submission, and nomination correction, recording auditable route metadata and triggering stale-review re-review (`re_review_pending`) on correction while rejecting `HazardRouted` content fail-closed (`400`) without state mutation.
* FR-4 (Field-permission checks and keyboard-operable UI): Server validation and UI rendering enforce role and field permissions (`appointment_evidence_visible`, `_owner_rights` for colleague-owned records and `owner` reassignment, confirmed `Communicate` representative authority, and refusal of client-supplied server-derived fields such as `recorded_by`, `verification`, `identity_status`, `support_needs`, `risk_flags`, `plain_language_explanation`), and every form control is keyboard-operable with explicit `<label for>`, unique `id`, `autocomplete="off"`, and inline status/error association (`role="status"`, `tabindex="-1"`, `aria-invalid="true"`, `aria-describedby`, `.focus()`).
  * Observable acceptance criteria: Unauthorized roles and non-owner peers attempting restricted field mutations receive `403`/`400` with zero state change, UI controls omit or restrict unpermitted owner-reassignment/write controls per `nomination_permissions`, `#nominations summary` remains the first Tab stop after `#nominations-title`, and empty required inputs trigger inline `aria-invalid="true"` + `aria-describedby` + `.focus()` recovery.

## Non-Functional Requirements

* NFR-1 (WCAG 2.2 and plain-language static guard preservation): Web changes preserve repository accessibility and content-standard invariants.
  * Objective threshold or evaluation condition: `setAttribute("aria-invalid", "true")` count across `web/*.js` remains `9`, `h("table", {}, ...)` count remains `14`, `AUDITED_FILES` set is unchanged, and `0` matches of banned words (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`) occur across `web/*.js` and `web/*.html`.
  * Operating condition or verification approach, if needed: Verified via `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_content_standard.py`, and `web-design-guidelines` review.
  * Observable acceptance criteria: All three static guard test modules pass with zero modifications to their baseline thresholds.
* NFR-2 (Type safety and formatting cleanliness): Modified and added Python files satisfy strict/package `mypy` and `ruff` lint/format checks.
  * Objective threshold or evaluation condition: `0` errors from `python3 -m ruff check`, `python3 -m ruff format --check .` in `src/core` and `src/api` (respecting `pyproject.toml` `[tool.ruff.format] exclude` on legacy-formatted `resident_decisions.py`, `store.py`, `projection.py`, and `server.py`), `python3 -m ruff format --isolated --line-length 100 --check` on all newly added and non-legacy-excluded modified files (`nomination_route.py`, `nomination_routes.py`, and modified/added test files), and bare `python3 -m mypy --cache-dir=/tmp/mypy-130` inside `src/core` and `src/api`.
  * Operating condition or verification approach, if needed: Executed using Python 3.12 with worktree package paths (`MYPYPATH` / workspace toolchain) without creating scratch virtualenvs in `/tmp`.
  * Observable acceptance criteria: `ruff check`, `ruff format` checks, and both `mypy` invocations exit `0`.

## Acceptance Criteria

* AC-1: Nomination, follow-up, and challenge API payloads and Resident-tab views expose and render deterministic `plain_language_explanation` fields (`human_decision_owner`, `ai_involvement_explanation`, `sources`, `policy_reasons`, `uncertainty_note`) sourced from live `Store.data["recommendations"]` with recursive restricted-key scrubbing and role/field-level visibility filtering so restricted internal vulnerability details never leak (`Refs #130`).
* AC-2: Digital (`channel="digital"`) and equivalent staff-recorded non-digital (`channel="staff_recorded_non_digital"`, phone/paper/letter/in-person assisted intake) routes are wired and proven across live `server.py` / `nomination_routes.py` HTTP endpoints and accessible HTML workbench forms for nomination acknowledgement, challenge submission, and nomination correction, including representative `Communicate` authority (`Refs #130`).
* AC-3: Per-role and per-owner field-permission checks fail closed (`403`/`400`) on unauthorized roles, peer-owned records (`_owner_rights` / `_same_person`), unconfirmed representatives, `allow_intermediary=False` challenge channels, and server-derived fields, and `HazardRouted` content fails closed (`400`) with zero nomination or challenge persistence.
* AC-4: Workbench HTML forms and explanation panels are keyboard-accessible (explicit `<label for>`, native `<details>/<summary>` and `<button>` controls, conditional required-field validation via shared `_routeForm`, preserved first-Tab `#nominations summary` focus order, inline `aria-invalid` + `aria-describedby` + `.focus()` validation) while `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, and `test_content_standard.py` pass unchanged.
* AC-5: Targeted `src/core` and `src/api` unit suites, `ruff check`, `ruff format` checks, and bare `mypy --cache-dir=/tmp/mypy-130` in `src/core` and `src/api` pass, and all changes plus dated `2026-11-15` `.copilot-tracking/` artifacts are committed locally on `feat/ux-130-api-routes` without pushing or opening a PR.

## Test Ownership and Validation Lock

* Canonical test targets to update: `src/core/tests/test_nomination_route.py`, `src/core/tests/test_resident_decisions.py`, `src/api/tests/test_nomination_screen.py`, `src/api/tests/test_resident_api.py`.
* Canonical test targets to add (maximum additions: `1` test module): `src/api/tests/test_nomination_api_routes.py` covering `nomination_routes.py`, live HTTP digital + `staff_recorded_non_digital` acknowledgement/challenge/correction routes, role/field-permission matrices, restricted vulnerability non-leakage, and interactive keyboard/validation DOM harness behavior.
* Exact test removals: `none`.
* Generated targets: `none`.
* Semantic-versus-regression coverage: Semantic tests prove plain-language AI/sources/policy/uncertainty/human-owner explanation semantics, vulnerability canary non-leakage, `digital` vs `staff_recorded_non_digital` parity, role/owner/field permission refusals, and keyboard focus/error recovery; regression suites (`test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_content_standard.py`, `test_role_endpoint_inventory.py`, `test_challenge_non_retaliation_hazard_guard.py`) guard counted `aria-invalid`/`table` sites, plain-language copy, and endpoint role security.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-plan.md                                                                     |
| Phase details                    | .copilot-tracking/details/2026-11-15/nomination-api-routes-130-phase-details.md                                                          |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/nomination-api-routes-130-plan-critique.md with Revise findings `PC-001`..`PC-006` resolved directly in plan and details |
| Relevant research                | .copilot-tracking/research/2026-11-15/nomination-api-routes-130-research.md                                                              |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/nomination-api-routes-130-changes.md is created by implementation as its evidence record            |
| Planning execution and readiness | Complete and `Ready` for `rpi-implement`                                                                                                 |
| Continuation context             | Confirmed automatic RPI Agent parent continues directly to `rpi-implement`                                                               |

## Sources

* .copilot-tracking/research/2026-11-15/nomination-api-routes-130-research.md: Primary Cycle 1 synthesis (`C1`..`C13`, `W1`, `D1`..`D6`) establishing actual `src/api` layout, plain-language explanation and channel contracts, and static baseline constraints.
* .copilot-tracking/reviews/2026-11-14/nomination-challenge-130-2142-review.md: Prior `src/core` review confirming verified domain primitives (`nomination_acknowledge`, `challenge_open`, `nomination_correct`, `challenge_trail`, `re_review_set`, `HazardRouted`) and remaining Issue #130 slice boundaries.
* docs/brds/agentic-retrofit-programme-brd.md and docs/prds/zava-forward-retrofit-programme-demonstrator.md: Canonical requirements `FR-037`, `FR-041`, `FR-043`, `FR-052`, `AC-065`, `AC-071`, `RULE-005`, and `CON-003`.
* docs/reference/research/ux/design-system.md, docs/reference/research/ux/wcag-conformance-baseline.md, and docs/reference/research/ux/content-standard.md: Fluent 2, WCAG 2.2 AA, and plain-language content standards.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Core Plain-Language Explanation and Dual-Route Channel Contracts

* Intent: Add deterministic, role/field-safe plain-language explanation builders and `digital` / `staff_recorded_non_digital` route channel normalization in `src/core`, wired through resident decisions and case detail projections.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add plain-language explanation and dual-channel helpers in `nomination_route.py`

* Requirement and evidence: FR-1, FR-2, FR-3; research findings Q2 and Q3 (`C4`, `C5`, `C6`).
* Expected result: `src/core/src/zava_forward/core/nomination_route.py` provides strict-typed `normalize_route_channel`, `nomination_explanation`, `challenge_explanation`, and `filter_explanation_for_viewer` using only allowlisted non-vulnerability inputs while preserving `Unknown` status honesty and backward-compatible channel labels.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/nomination-api-routes-130-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Wire dual-route channels, field permissions, and explanation projections in `resident_decisions.py`, `store.py`, and `projection.py`

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4; research findings Q2, Q3, and Q4 (`C3`, `C4`, `C6`, `C7`) and critique `PC-001`, `PC-002`.
* Expected result: `_res_nomination_acknowledge`, `_res_challenge_open`, `_res_nomination_correct`, and `_res_nomination_record` accept `channel="digital"` and `channel="staff_recorded_non_digital"` (plus `assisted_channel` where non-digital) with `_split_optional`, 3-arg `_owner_rights(self, user, ...)` + `_same_person`, and closed-schema role/field checks; `Store.detail` passes case-matching `self.data["recommendations"]` into `followup_view` and `challenge_catalog`, scrubs restricted vulnerability keys, and attaches `plain_language_explanation` and `nomination_permissions` (also cleaned up in `projection.redact_staff_detail`).
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/nomination-api-routes-130-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: `src/api` Route Boundary and Accessible Keyboard-Operable Workbench Views

* Intent: Provide strictly typed `src/api` route/permission/explanation boundary helpers wired into live `server.py` case/resident handlers and wire accessible plain-language explanation displays and keyboard-operable digital + staff-recorded non-digital forms in the Resident workbench tab without breaking static accessibility or content guards.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Create typed `src/api/src/zava_forward/api/nomination_routes.py` and delegate from `server.py`

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4, NFR-2; research findings Q1, Q4 (`C1`, `C7`, `C12`, `C13`) and critique `PC-003`.
* Expected result: `src/api/src/zava_forward/api/nomination_routes.py` exposes strictly typed API request validators, per-role field-permission evaluators, role-filtered plain-language explanation projectors, and accessible HTML fragment renderers, and `server.py` delegates `GET /api/cases/<cid>` and `POST /api/cases/<cid>/resident` nomination/challenge actions through `nomination_routes.py` without introducing new `/api/...` route literals.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/nomination-api-routes-130-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Wire plain-language explanations and dual-route keyboard-operable forms in `web/panels.js` and `web/app.js`

* Requirement and evidence: FR-1, FR-3, FR-4, NFR-1; research findings Q2, Q3, Q5, and `D1`..`D3` (`C2`, `C8`..`C11`, `W1`).
* Expected result: `web/app.js` mounts `nominationPanel(c, id, refresh)`, and `web/panels.js` renders plain-language explanations (`Human decision owner`, `AI involvement`, `Sources and policy reasons`, `Uncertainty and missing evidence`) plus keyboard-operable digital and `staff_recorded_non_digital` forms for nomination acknowledgement, nomination correction, and challenge submission using one shared `formFor` `aria-invalid` site (`sites == 9`, `tables == 14`, zero banned words, preserved standalone `nominationPanel(c)` read-only slice and `#nominations summary` first-Tab focus stop).
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/nomination-api-routes-130-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Focused Unit, API, Permission, Non-Leakage, and Keyboard/Accessibility Tests

* Intent: Prove AC-1 through AC-4 across `src/core` and `src/api` unit, live HTTP, role/field-permission, vulnerability non-leakage, and DOM/keyboard suites.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Extend `src/core` nomination and resident-decision unit tests

* Requirement and evidence: AC-1, AC-2, AC-3; Test Ownership and Validation Lock.
* Expected result: `src/core/tests/test_nomination_route.py` and `src/core/tests/test_resident_decisions.py` cover deterministic plain-language explanations (no-AI, AI-linked, rule-based, `Unknown` uncertainty, vulnerability canary exclusion), `normalize_route_channel` (`digital` and `staff_recorded_non_digital`), dual-route acknowledgement/challenge/correction workflows, owner/field permission refusals, and `HazardRouted` fail-closed behavior.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/nomination-api-routes-130-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Extend `src/api` screen/resident API tests and add `test_nomination_api_routes.py`

* Requirement and evidence: AC-1, AC-2, AC-3, AC-4; Test Ownership and Validation Lock (`C8`..`C12`).
* Expected result: `src/api/tests/test_nomination_screen.py`, `src/api/tests/test_resident_api.py`, and `src/api/tests/test_nomination_api_routes.py` verify HTTP and HTML/DOM plain-language explanations, zero restricted vulnerability leakage across roles, `channel="digital"` and `channel="staff_recorded_non_digital"` acknowledgement/challenge/correction submissions, per-role field permissions, label/status/focus-order keyboard operability, and unchanged `aria-invalid` baseline compliance.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/nomination-api-routes-130-phase-details.md

<!-- rpi:phase id=P04 -->
### [x] P04: Focused Tier Validation and Clean Local Verification

* Intent: Run all focused-tier validation gates (`unittest`, `ruff check`, `ruff format`, `mypy --cache-dir=/tmp/mypy-130`) and verify zero regressions across static accessibility, content-standard, and role-endpoint guards.
* Dependencies: P03

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Execute focused `unittest`, `ruff`, and `mypy` verification suites

* Requirement and evidence: AC-5, NFR-1, NFR-2; research finding `D6` (`C13`) and critique `PC-003`, `PC-006`.
* Expected result: Targeted `src/core` and `src/api` unit suites (including `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_content_standard.py`, `test_role_endpoint_inventory.py`, and `test_challenge_non_retaliation_hazard_guard.py`), `ruff check`, `ruff format --check` plus `ruff format --isolated --line-length 100 --check` on non-legacy-excluded modified files, and bare `mypy --cache-dir=/tmp/mypy-130` inside `src/core` and `src/api` pass with `0` errors.
* Detail section: P04-T01 in .copilot-tracking/details/2026-11-15/nomination-api-routes-130-phase-details.md

## Dependencies

* Existing `src/core/src/zava_forward/core/nomination_route.py` and `resident_decisions.py` primitives from PR #1710 and PR #1742 on parent branch `origin/feat/demo-233-same-home-tensions-0825`.
* Node.js runtime on `PATH` for DOM rendering and interaction harness tests in `src/api/tests/test_nomination_screen.py` and `src/api/tests/test_nomination_api_routes.py`.
* Worktree source paths (`PYTHONPATH` / `MYPYPATH` / `_bootstrap_worktree_paths()`) so bare `python3 -m mypy --cache-dir=/tmp/mypy-130` and `unittest` resolve sibling typed packages cleanly without creating `/tmp` virtual environments.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `2026-11-15` `PC-001` (Critical: conditional `_routeForm` fields, `r.id` + `{case_id, id, expected_version}`, representative `Communicate` controls, 3-arg `_owner_rights` + `_same_person`) | Resolved | Updated P01-T02 and P02-T02 so `_routeForm` supports optional/conditional predicates (`assisted_channel`, `representative_ref`, `owner_reassignment_reason`, nullable `challenge_id`), exposes `raised_by` + `representative_ref`, keys records on `r.id`, and uses `_split_optional` + 3-arg `_owner_rights(self, user, ...)` + `_same_person`. |
| `2026-11-15` `PC-002` (High: `self.data["recommendations"]` lookup and recursive restricted-vulnerability scrubbing + `redact_staff_detail` cleanup) | Resolved | Updated P01-T01 and P01-T02 so `Store.detail` sources case-matching `self.data.get("recommendations", ())` inside `with self.lock:`, recursively strips restricted vulnerability keys and `permitted is False` entries on projected records, and cleans up `nomination_permissions` in `projection.redact_staff_detail`. |
| `2026-11-15` `PC-003` (High: live `server.py` delegation to `nomination_routes.py` and legacy `ruff format` exclude alignment) | Resolved | Updated P02-T01 to wire `nomination_routes.py` into `server.py` (`GET /api/cases/<cid>` and `POST /api/cases/<cid>/resident`) without new `/api/...` route literals, and updated NFR-2/P04-T01 to pair `ruff format --check .` with `ruff format --isolated --line-length 100 --check` on non-legacy-excluded files. |
| `2026-11-15` `PC-004` (High: deterministic `"Assisted non-digital intake"` default and `allow_intermediary=False` check on `assisted_channel`) | Resolved | Updated P01-T01 so omitted `assisted_channel` on `staff_recorded_non_digital` returns `"Assisted non-digital intake"` and `allow_intermediary=False` rejects `"Trusted intermediary"` on both `channel` and `assisted_channel`. |
| `2026-11-15` `PC-005` (High: `BLOCKED_WORDS`, no `": None"` fallbacks, isolated Node-slice guards, Epic 149 line-window rules, and `restoreChallengeDrafts` target routing) | Resolved | Updated P02-T02 and P03-T02 to enforce all five `panels.js` static, slice, copy, and draft-restore invariants explicitly. |
| `2026-11-15` `PC-006` (Medium: avoid creating `/tmp/venv-130`) | Resolved | Removed `/tmp/venv-130` creation from NFR-2, Dependencies, and P04-T01 while keeping caller-confirmed `--cache-dir=/tmp/mypy-130`. Accepted Focused Tier residual risk that Playwright browser scripts are verified statically/via Node DOM harness while full local gate runs upon future PR publication. |

## Follow-Up Items

* Resolve human governance open decisions `OD-41` and `OD-42` with Zava North Homes operations and compliance owners, obtain authorized human representative comprehension sign-off, and run hosted PR CI plus independent exact-head review when ready for publication (`Refs #130`).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/nomination-api-routes-130-changes.md
* Ready phase or task: Review (`P01` through `P04` complete)
* Remaining provisional question or blocker: None
