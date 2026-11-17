<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue 130 Plain-Language Explanation and Dual-Route API/Workbench Slice

## Metadata

* Task ID: nomination-api-routes-130
* Task slug: nomination-api-routes-130
* Related plan: .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/nomination-api-routes-130-research.md, .copilot-tracking/reviews/2026-11-14/nomination-challenge-130-2142-review.md, docs/brds/agentic-retrofit-programme-brd.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
|----------|------|--------|-----------------|
| P01 | Core Plain-Language Explanation and Dual-Route Channel Contracts | Ready | P01, P01-T01, P01-T02 |
| P02 | `src/api` Route Boundary and Accessible Keyboard-Operable Workbench Views | Ready | P02, P02-T01, P02-T02 |
| P03 | Focused Unit, API, Permission, Non-Leakage, and Keyboard/Accessibility Tests | Ready | P03, P03-T01, P03-T02 |
| P04 | Focused Tier Validation and Clean Local Verification | Ready | P04, P04-T01 |

<!-- rpi:phase id=P01 -->
## P01: Core Plain-Language Explanation and Dual-Route Channel Contracts

### Context

`src/core/src/zava_forward/core/nomination_route.py` and `resident_decisions.py` already implement nomination intake, acknowledgement, supplied correction, stale-review flagging (`re_review_set`), hazard fail-closed routing (`HazardRouted`), and challenge trails, but lack (1) a deterministic `plain_language_explanation` structure stating AI involvement, permitted sources and policy reasons, uncertainty, and named human decision ownership, and (2) `channel="digital"` and `channel="staff_recorded_non_digital"` support across `nomination_acknowledge`, `challenge_open`, and `nomination_correct`.

### Intent

Establish pure, strict-typed domain contracts in `nomination_route.py` and wire them through `resident_decisions.py` and `store.py` so every API and workbench surface consumes one single source of truth with fail-closed role, owner, and field permissions.

### Boundaries

* Included: `src/core/src/zava_forward/core/nomination_route.py`, `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/src/zava_forward/core/store.py`, `src/core/src/zava_forward/core/projection.py`.
* Excluded: Web JavaScript files (P02) and test files (P03).

### Likely Targets

* src/core/src/zava_forward/core/nomination_route.py: Add `normalize_route_channel`, `scrub_nomination_restricted_fields`, `nomination_explanation`, `challenge_explanation`, and `filter_explanation_for_viewer` under `mypy --strict`.
* src/core/src/zava_forward/core/resident_decisions.py: Wire `normalize_route_channel` into `_res_nomination_acknowledge`, `_res_challenge_open`, `_res_nomination_correct`, and `_res_nomination_record`; enforce `_split_optional`, closed-schema field checks, and 3-arg `_owner_rights(self, user, ...)` + `_same_person`; attach `plain_language_explanation` in `followup_view` and `challenge_catalog`.
* src/core/src/zava_forward/core/store.py: Source case-matching `self.data.get("recommendations", ())` inside `with self.lock:`, scrub restricted vulnerability keys, and attach role-scoped `plain_language_explanation` on `affected_challenges` plus `nomination_permissions` (including confirmed `Communicate` representative authorities) on `Store.detail`.
* src/core/src/zava_forward/core/projection.py: Ensure `redact_staff_detail` pops `nomination_permissions` and `challenge_assurance` whenever `not appointment_evidence_visible(user)`.

### Dependencies

* None.

### Validation Expectations

* `mypy --strict` cleanliness on `nomination_route.py`, package `mypy` cleanliness across `src/core`, `ruff check`, `ruff format --check .` inside `src/core` (honoring legacy excludes on `resident_decisions.py`, `store.py`, `projection.py`), and `ruff format --isolated --line-length 100 --check` on `nomination_route.py`.

### Completion Evidence

* `nomination_records[*]`, `nomination_records[*]["follow_up"]`, `affected_challenges[*]`, and `challenge_targets[*]` carry deterministic, role-filtered `plain_language_explanation` mappings, and all nomination/challenge write routes accept both `digital` and `staff_recorded_non_digital`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add plain-language explanation and dual-channel helpers in `nomination_route.py`

#### Context

`nomination_route.py` is enforced under `[tool.mypy] overrides` with `strict = true`. Explanations must never read or emit restricted internal vulnerability fields (`resident.reason`, `resident.adjustment`, `resident.support`, `resident.priority_support`, `contacts[*].note`, `hazards[*].note`, `internal_vulnerability_note`, `health_detail`, `safeguarding_note`, or any `permitted=False` note).

#### Intent

Provide deterministic pure functions for dual-route channel normalization and plain-language explanation synthesis plus role/field visibility filtering.

#### Boundaries

* Included:
  * `ROUTE_MODES = ("digital", "staff_recorded_non_digital")` and `ASSISTED_NON_DIGITAL_CHANNELS` mapping (`phone` -> `"Phone"`, `paper` -> `"Paper"`, `letter` -> `"Letter"`, `in_person` -> `"In person"`, `trusted_intermediary` -> `"Trusted intermediary"`).
  * `normalize_route_channel(channel, *, assisted_channel=None, allow_intermediary=True)` returning `(stored_channel, route_mode, normalized_assisted_channel)`:
    * Accepts `"digital"` -> `("digital", "digital", None)` and `"Digital"` -> `("Digital", "digital", None)`; rejects non-empty `assisted_channel` when `route_mode == "digital"`.
    * Accepts `"staff_recorded_non_digital"` -> `("staff_recorded_non_digital", "staff_recorded_non_digital", normalized_assisted)` where omitted `assisted_channel` deterministically returns `"Assisted non-digital intake"` (never fabricating `"Phone"`), and maps legacy non-digital labels (`"Phone"`, `"Paper"`, `"Letter"`, `"In person"`, and `"Trusted intermediary"` when `allow_intermediary=True`) -> `(label, "staff_recorded_non_digital", label)`; raises `ValueError` whenever `allow_intermediary is False` and either `channel` or `assisted_channel` resolves to `"Trusted intermediary"`.
  * `scrub_nomination_restricted_fields(value)`: Recursively strips restricted internal vulnerability keys (`internal_vulnerability_note`, `health_detail`, `safeguarding_note`, `vulnerability_reason`) and filters out sub-entries with `permitted is False` across projected nomination, follow-up, target, and challenge payloads.
  * `nomination_explanation(record, *, follow_up=None, recommendations=(), can_view_intake=True, can_view_reason=True)` and `challenge_explanation(item, *, recommendations=(), can_view_intake=True, can_view_reason=True)` returning `{ "permitted": True, "human_decision_owner": str, "ai_involvement_explanation": str, "sources": list[str], "policy_reasons": list[str], "uncertainty_note": str }`:
    * `human_decision_owner`: Names the assigned human owner (for example `"Sam Patel — a named person owns every review and follow-up decision; no decision is taken automatically"`) or explicitly flags `"Unassigned — a named human owner is required before review; no decision is taken automatically"`.
    * `ai_involvement_explanation`: Inspects only allowlisted linked recommendation metadata (`proposal_id`, `ai_details.source`, `ai_details.model`) when `linked_proposal_id` or `target_id` matches a priority suggestion; states clearly when no AI was involved in recording, acknowledging, correcting, or reviewing the referral/challenge, or when an AI suggestion contributed to cohort ranking without deciding eligibility, inferring vulnerability/support needs, or overriding human review.
    * `sources`: Allowlisted source labels only (record `source` when permitted and `can_view_intake and can_view_reason`, linked `proposal_id` / `target_id`, channel route mode, and latest correction source; stripped of any restricted internal vulnerability keys and emptied when `not (can_view_intake and can_view_reason)`).
    * `policy_reasons`: Deterministic plain-language policy basis covering staffed nomination/self-referral access without relying solely on recorded flags (`FR-037`), non-retaliation, hazard safety continuity, and independent human review/complaints access (`RULE-005`), stale-review re-review protection after corrections (`FR-043`), and—only when `can_view_intake and can_view_reason`—recorded human review outcome rationale.
    * `uncertainty_note`: Plain-language summary of unverified or unknown items (`Identity status: Unknown`, `Support needs: Unknown`, `Risk flags: Unknown`, `Acknowledgement delivery: Not verified by this system`, pending `missing_before_review` steps, or pending stale-review re-review, explicitly noting `Unknown is never treated as None`).
  * `filter_explanation_for_viewer(explanation, *, can_view_intake, can_view_reason)` returning `None` when `not can_view_intake` and redacting intake-specific `sources` and case-specific review rationale when `not can_view_reason`.
* Excluded: Mutating case dictionaries in place outside `resident_decisions.py` / `store.py`.

#### Likely Targets

* src/core/src/zava_forward/core/nomination_route.py: Pure helper functions and module `__all__`.

#### Dependencies

* None.

#### Validation Expectations

* Unit coverage in `src/core/tests/test_nomination_route.py` and `mypy --strict`.

#### Completion Evidence

* Pure functions pass strict type checking and deterministic unit assertions.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Wire dual-route channels, field permissions, and explanation projections in `resident_decisions.py`, `store.py`, and `projection.py`

#### Context

`_res_nomination_acknowledge` currently accepts only `{case_id, id, expected_version, acknowledgement_ref, owner, non_digital_route, next_update}` (plus optional `owner_reassignment_reason`), `_res_challenge_open` accepts only `("Digital", "Phone", "Letter", "In person")`, and `_res_nomination_correct` accepts only `INTAKE_CHANNELS`. Furthermore, case-level priority recommendations reside on `self.data["recommendations"]` (not `d["recommendations"]`), and `Store.detail` projects `nomination_records`, `affected_challenges`, and `challenge_targets` only when `challenge_references_visible(self, user)` holds.

#### Intent

Accept `channel="digital"` and `channel="staff_recorded_non_digital"` (and optional `assisted_channel`) across acknowledgement, challenge submission, correction, and intake; enforce role/owner/field permissions fail-closed; and project scrubbed `plain_language_explanation` and `nomination_permissions` on case details.

#### Boundaries

* Included:
  * `_res_nomination_acknowledge`: Extract optional `("channel", "assisted_channel", "owner_reassignment_reason")` via `_split_optional` (defaulting omitted `channel` from `record["original"]["channel"]` before `"digital"` so existing callers stay 100% compatible); normalize via `normalize_route_channel`; store `channel`, `route_mode`, and `assisted_channel` on `acknowledgement` and `acknowledgement_history`; enforce 3-arg `_owner_rights(self, user, record["owner"])` whenever `record.get("owner")` is already assigned AND enforce `user["role"] in MANAGERS or _same_person(user, owner)` when assigning `owner` to a colleague (`PermissionError` when a non-manager assigns another person).
  * `_res_challenge_open`: Extract optional `("assisted_channel",)` alongside existing optional keys, normalize `channel` via `normalize_route_channel(..., assisted_channel=..., allow_intermediary=False)`, and store `channel`, `route_mode`, and `assisted_channel` on the opened challenge record and audit detail while rejecting server-derived keys.
  * `_res_nomination_correct` and `_res_nomination_record`: Extract optional `("assisted_channel",)` via `_split_optional`, normalize via `normalize_route_channel(..., allow_intermediary=True)`, and store `channel`, `route_mode`, and `assisted_channel` on nomination and correction records while keeping 3-arg `_owner_rights(self, user, rec.get("owner"))` and `HazardRouted` fail-closed guards intact.
  * `followup_view`, `challenge_catalog`, `Store.detail`, and `projection.redact_staff_detail`: Inside `Store.detail` under `with self.lock:`, filter `self.data.get("recommendations", ())` to case-matching priority suggestions (`rec.get("kind") != "ai_task" and _priority_includes_case(rec, case_id)`), scrub restricted vulnerability keys via `scrub_nomination_restricted_fields`, attach `plain_language_explanation` to each nomination record, `follow_up` block, `challenge_targets[*]` entry, and `affected_challenges[*]` entry, attach `nomination_permissions` (`can_write`, `can_reassign_owner`, `editable_nomination_ids` keyed on `r["id"]`, `staff_owners`, `representative_authorities` for confirmed in-date `Communicate` authorities, `channels`, `assisted_channels`) when `challenge_references_visible(self, user)` holds, and pop `nomination_permissions` and `challenge_assurance` in `projection.redact_staff_detail` whenever `not appointment_evidence_visible(user)`.
* Excluded: Adding new `/api/...` route URL literals to `server.py`.

#### Likely Targets

* src/core/src/zava_forward/core/resident_decisions.py: Action handlers and `followup_view` / `challenge_catalog`.
* src/core/src/zava_forward/core/store.py: `Store.detail` recommendation lookup, scrubbing, explanation, and permission projection.
* src/core/src/zava_forward/core/projection.py: `redact_staff_detail` cleanup of `nomination_permissions` and `challenge_assurance`.

#### Dependencies

* P01-T01.

#### Validation Expectations

* Existing and new tests in `test_resident_decisions.py`, `test_resident_api.py`, and `test_role_endpoint_inventory.py`.

#### Completion Evidence

* `Store.detail` and `Store.resident_action` enforce all role/field rules and return complete `plain_language_explanation` and dual-route metadata.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: `src/api` Route Boundary and Accessible Keyboard-Operable Workbench Views

### Context

The live workbench HTTP server (`server.py`) serves `GET /api/cases/<cid>` and `POST /api/cases/<cid>/resident` and renders Resident-tab views via `web/app.js` and `web/panels.js`. Static guards require `9` `setAttribute("aria-invalid", "true")` sites, `14` `<table>` elements, unchanged `AUDITED_FILES` under `web/`, zero banned internal words in `web/*.js`, standalone 1-arg `nominationPanel(c)` compatibility, and `#nominations summary` as the first Tab stop after `#nominations-title`.

### Intent

Provide a clean strictly typed `src/api/src/zava_forward/api/nomination_routes.py` module for API-layer route, permission, explanation, and HTML view helpers, and wire `web/panels.js` + `web/app.js` to display plain-language explanations and keyboard-operable digital + staff-recorded non-digital acknowledgement, challenge, and correction forms.

### Boundaries

* Included: `src/api/src/zava_forward/api/nomination_routes.py`, surgical delegation in `src/api/src/zava_forward/api/server.py`, `src/api/src/zava_forward/api/web/panels.js`, `src/api/src/zava_forward/api/web/app.js`.
* Excluded: Adding new `/api/...` route URL literals in `server.py`, `resident_demo`, `resident_preview`, and creating new `.js`/`.html` files under `web/`.

### Likely Targets

* src/api/src/zava_forward/api/nomination_routes.py: New strictly typed API module for route payload construction/validation, role/field-permission enforcement, viewer-filtered explanation payloads, and server-side accessible HTML view rendering helpers.
* src/api/src/zava_forward/api/server.py: Delegate `GET /api/cases/<cid>` projection through `nomination_routes.project_case_nomination_routes` and `POST /api/cases/<cid>/resident` nomination/challenge route payloads through `nomination_routes.build_route_action_payload` before `s.resident_action`.
* src/api/src/zava_forward/api/web/app.js: Pass `(c, id, refresh)` to `nominationPanel(c, id, refresh)` in the Resident tab.
* src/api/src/zava_forward/api/web/panels.js: Render `plain_language_explanation` `<dl>` sections in `nominationPanel` and `affectedChallengePanel`; share conditional-field `nominationPanel._routeForm` (preserving the 1 counted `aria-invalid` site and Epic 149 substrings); add keyboard-operable digital + `staff_recorded_non_digital` forms for `nomination_acknowledge`, `nomination_correct`, and `challenge_open` keyed on `r.id` with `{case_id, id, expected_version}` and representative `Communicate` controls; route orphaned `nomination-*` drafts to `#nominations` in `restoreChallengeDrafts`.

### Dependencies

* P01.

### Validation Expectations

* `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_content_standard.py`, `test_nomination_screen.py`, `test_nomination_api_routes.py`, `ruff`, `mypy`, and `web-design-guidelines` `file:line` audit.

### Completion Evidence

* Both Python API helpers/endpoints and workbench HTML panels render deterministic plain-language explanations and execute digital + staff-recorded non-digital acknowledgement, challenge, and correction flows with full keyboard operability and field-permission enforcement.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Create typed `src/api/src/zava_forward/api/nomination_routes.py` and delegate from `server.py`

#### Context

Adding a dedicated, 100-column `ruff format` clean, strictly typed module in `src/api` and delegating live `GET /api/cases/<cid>` and `POST /api/cases/<cid>/resident` traffic through it in `server.py` ensures `nomination_routes.py` executes in production HTTP traffic without introducing new `/api/...` route literals (`test_role_endpoint_inventory.py`).

#### Intent

Implement `nomination_routes.py` in `src/api/src/zava_forward/api/` (`mypy --strict` clean) and wire surgical delegation in `server.py`.

#### Boundaries

* Included:
  * `nomination_field_permissions(user, record=None, *, staff_owners=(), representative_authorities=())`: Computes role and field-level permissions (`can_view`, `can_acknowledge`, `can_correct`, `can_challenge`, `can_reassign_owner`, `allowed_fields`, `forbidden_fields`).
  * `build_route_action_payload(action, body, *, user)`: Validates and normalizes `nomination_acknowledge`, `challenge_open`, `nomination_correct`, and `nomination_record` HTTP requests across `channel="digital"` and `channel="staff_recorded_non_digital"`, enforcing role/field permissions fail-closed (`PermissionError` -> `403`, `ValueError` -> `400`) before `Store.resident_action` in `server.py`.
  * `project_case_nomination_routes(detail, *, user)`: Scrubs restricted vulnerability keys and verifies role-filtered `plain_language_explanation` and `nomination_permissions` on `GET /api/cases/<cid>` and `POST /api/cases/<cid>/resident` responses in `server.py`.
  * `render_accessible_nomination_route_html(detail, *, user)`: Produces accessible, keyboard-operable HTML (`<section>`, `<dl>`, `<details>/<summary>`, `<form>`, explicit `<label for>`, `aria-describedby` status hooks, role-filtered owner and representative `Communicate` controls, and plain-language explanation blocks).
* Excluded: Registering new `/api/...` route string literals in `server.py`.

#### Likely Targets

* src/api/src/zava_forward/api/nomination_routes.py: New module.
* src/api/src/zava_forward/api/server.py: Surgical delegation on `GET /api/cases/<cid>` and `POST /api/cases/<cid>/resident`.

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* `ruff check`, `ruff format --isolated --line-length 100 --check`, `mypy --cache-dir=/tmp/mypy-130`, and `test_nomination_api_routes.py`.

#### Completion Evidence

* `nomination_routes.py` passes `mypy` and `ruff` with `0` warnings and proves API/HTML parity with `Store` and `panels.js`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Wire plain-language explanations and dual-route keyboard-operable forms in `web/panels.js` and `web/app.js`

#### Context

`test_nomination_screen.py` slices `panels.js` from `function nominationPanel` to `\nfunction affectedChallengePanel` and calls `nominationPanel(c)` with one argument, asserting `controls == []`. Meanwhile, `test_accessibility_baseline.py` and `test_epic149_form_error_summary_associations.py` require exact `9` `setAttribute("aria-invalid", "true")` calls across `web/*.js`, exact `14` `<table>` elements, and `"before recording this challenge."` in `panels.js`; `nomination_browser_check.py` requires `#nominations summary.first` to be the first Tab stop after `#nominations-title`; and `test_content_standard.py` forbids `gate`, `hold`, `provenance`, `trace`, `snapshot`, and `envelope` anywhere in `web/*.js`.

#### Intent

Render plain-language explanation `<dl>` blocks and keyboard-operable digital + `staff_recorded_non_digital` forms in `nominationPanel` and `affectedChallengePanel` while preserving every existing static, Node-slice, and Playwright DOM invariant.

#### Boundaries

* Included:
  * Update `web/app.js` Resident tab call from `nominationPanel(c)` to `nominationPanel(c, id, refresh)`.
  * Inside `function nominationPanel(c, id, refresh)`:
    * Keep standalone 1-argument `nominationPanel(c)` completely self-contained (using only `h` when `!id || !refresh || !c.nomination_permissions?.can_write`, rendering `0` form controls so `test_nomination_screen.py`'s existing `shown()` helper sees `controls == []`).
    * Render a `"Plain-language decision and AI explanation"` `<dl>` block inside each nomination record card displaying `Human decision owner`, `AI involvement`, `Permitted sources`, `Policy reasons`, and `Uncertainty and missing items` from `r.plain_language_explanation` or `r.follow_up?.plain_language_explanation`, using `"Not recorded"` / `"Unknown"` fallbacks that never begin with `"None"` (`test_nomination_screen.py` `": None"` guard) and avoiding all `BLOCKED_WORDS` (`cannot`, `could not`, `unavailable`, `failed`, `refused`, etc.).
    * Update the bottom summary paragraph so it shows interactive route guidance when `Boolean(id && refresh && c.nomination_permissions?.can_write)` is true and read-only wording otherwise.
    * When `Boolean(id && refresh && c.nomination_permissions?.can_write)` holds and `(c.nomination_permissions.editable_nomination_ids || []).includes(r.id)`, render `<details>` disclosure forms at the bottom of each `<details class="nomination-record">` card (strictly after its `<summary>` and `<dl>` data lists so `#nominations summary` remains the first Tab stop after `#nominations-title`), submitting `{ case_id: id, id: r.id, expected_version: r.version, ... }` for:
      1. Route acknowledgement (`action: "nomination_acknowledge"`, `channel` options `digital` and `staff_recorded_non_digital` plus existing labels, conditional `assisted_channel` required only when `channel === "staff_recorded_non_digital"`, `owner` select restricted to self unless `can_reassign_owner` is true, conditional `owner_reassignment_reason` required only when `r.owner?.email` changes, `acknowledgement_ref`, `non_digital_route`, `next_update`).
      2. Supplied correction (`action: "nomination_correct"`, `channel` options `digital` and `staff_recorded_non_digital` plus existing labels, conditional `assisted_channel`, `raised_by` including `"Representative"`, conditional `representative_ref` populated from `c.nomination_permissions.representative_authorities` and required only when `raised_by === "Representative"`, `reported_subject_ref`, `account`, `source`, optional nullable `challenge_id`, `next_update`).
  * Share one conditional-field form builder `nominationPanel._routeForm` between `nominationPanel` and `affectedChallengePanel` without duplicating `input.setAttribute("aria-invalid", "true")`:
    * Parameterize `listId` (removing closure over `targetOptions`), support `optional` and `requiredWhen(values)` per field (omitting blank optional/non-applicable keys or mapping `emptyAsNull` fields like `challenge_id` to `null`), attach `input.addEventListener` only when `typeof input.addEventListener === "function"`, guard `caseSession` / `bindCaseMutationForm` / `panelOwned` for isolated Node slice harnesses, and preserve every Epic 149 exact substring and line-window invariant (`input.setAttribute("aria-invalid", "true")`, `"aria-describedby": status.id`, `id: `${key}-feedback``, `.focus()` within 4 lines, `tabindex: -1`, and `"before recording this challenge."` with zero `RAW_ERROR` tokens in the trailing 200 chars).
  * Inside `affectedChallengePanel(c, id, refresh)`:
    * Render `plain_language_explanation` `<dl>` fields on challenge targets and recorded challenges (`Human decision owner`, `AI involvement`, `Policy reasons`, `Uncertainty and missing items`).
    * Support `channel` options covering canonical `"digital"` and `"staff_recorded_non_digital"` (with conditional `assisted_channel` selector for phone, paper, letter, in person) alongside `"Digital"`, `"Phone"`, `"Letter"`, `"In person"`, plus `raised_by` and conditional `representative_ref` for confirmed `Communicate` representatives.
  * Keep `form[data-challenge-case][data-unsaved=true]` in `captureChallengeDrafts` and update `restoreChallengeDrafts` so orphaned `nomination-*` drafts restore into `#nominations` rather than `#affected-challenges`.
* Excluded: Adding `<table>` elements, adding new `.js`/`.html` files, or using any banned term (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`) in code or comments.

#### Likely Targets

* src/api/src/zava_forward/api/web/panels.js: `nominationPanel`, `affectedChallengePanel`, `captureChallengeDrafts`, `restoreChallengeDrafts`.
* src/api/src/zava_forward/api/web/app.js: Resident tab `nominationPanel(c, id, refresh)` wiring.

#### Dependencies

* P01-T02, P02-T01.

#### Validation Expectations

* `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_content_standard.py`, `test_nomination_screen.py`, and `test_nomination_api_routes.py`.

#### Completion Evidence

* Node DOM evaluation proves keyboard focus/label/error semantics, plain-language explanation rendering, role-based field hiding, and exact static counts (`9` `aria-invalid`, `14` `table`, `0` banned words).

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Focused Unit, API, Permission, Non-Leakage, and Keyboard/Accessibility Tests

### Context

Every new behavior introduced by P01 and P02 requires focused semantic tests that would fail without this slice, alongside existing regression suites.

### Intent

Extend `src/core` and `src/api` test suites and add `src/api/tests/test_nomination_api_routes.py` with worktree path bootstrapping so tests run cleanly both directly and under `unittest discover`.

### Boundaries

* Included: `src/core/tests/test_nomination_route.py`, `src/core/tests/test_resident_decisions.py`, `src/api/tests/test_nomination_screen.py`, `src/api/tests/test_resident_api.py`, `src/api/tests/test_nomination_api_routes.py`.
* Excluded: Weakening or altering assertions in `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, or `test_content_standard.py`.

### Likely Targets

* src/core/tests/test_nomination_route.py: Unit tests for `normalize_route_channel`, `nomination_explanation`, `challenge_explanation`, and `filter_explanation_for_viewer` (including vulnerability canary non-leakage and AI vs non-AI determinism).
* src/core/tests/test_resident_decisions.py: Unit tests for `digital` and `staff_recorded_non_digital` acknowledgement, challenge, and correction actions, owner/field permission refusals, and `followup_view` / `challenge_catalog` explanation wiring.
* src/api/tests/test_nomination_screen.py: DOM tests for plain-language explanation rendering on read-only `nominationPanel(c)` and interactive `nominationPanel(c, id, refresh)` keyboard/permission behavior.
* src/api/tests/test_resident_api.py: Live HTTP tests for `channel="digital"` and `channel="staff_recorded_non_digital"` across `nomination_acknowledge`, `challenge_open`, and `nomination_correct`.
* src/api/tests/test_nomination_api_routes.py: Focused API + UI + permission + vulnerability non-leakage + keyboard error-association suite covering `nomination_routes.py`, live `ThreadingHTTPServer`, and `panels.js` (`nominationPanel` + `affectedChallengePanel`).

### Dependencies

* P01, P02.

### Validation Expectations

* All targeted `src/core` and `src/api` test modules pass with `0` failures and pass `mypy` and `ruff`.

### Completion Evidence

* Focused test runs prove AC-1, AC-2, AC-3, and AC-4 end-to-end.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Extend `src/core` nomination and resident-decision unit tests

#### Context

`src/core/tests/test_nomination_route.py` already includes `_bootstrap_worktree_paths()` so worktree edits are imported first. `src/core/tests/test_resident_decisions.py` tests core resident decision actions.

#### Intent

Add focused unit cases covering plain-language explanations, vulnerability redaction, dual-route channel normalization, and owner/field permission enforcement.

#### Boundaries

* Included: `src/core/tests/test_nomination_route.py`, `src/core/tests/test_resident_decisions.py`.
* Excluded: `src/api` HTTP tests (P03-T02).

#### Likely Targets

* src/core/tests/test_nomination_route.py: Explanation and channel normalization tests.
* src/core/tests/test_resident_decisions.py: Dual-channel action and permission tests (with worktree bootstrap helper).

#### Dependencies

* P01.

#### Validation Expectations

* `python3 -m unittest tests/test_nomination_route.py tests/test_resident_decisions.py -q` inside `src/core` exits `0`.

#### Completion Evidence

* Passing unit suite in `src/core`.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Extend `src/api` screen/resident API tests and add `test_nomination_api_routes.py`

#### Context

`src/api` tests exercise live `ThreadingHTTPServer` HTTP calls (`ResidentApi` pattern) and Node.js DOM rendering (`test_nomination_screen.py` pattern).

#### Intent

Verify end-to-end HTTP API and HTML/DOM behavior for plain-language explanations, vulnerability non-leakage across roles, `digital` and `staff_recorded_non_digital` routes across acknowledgement/challenge/correction, per-role field permissions, and keyboard operability (`<label for>`, first-Tab `<summary>`, `aria-invalid` + `aria-describedby` + `.focus()`).

#### Boundaries

* Included: `src/api/tests/test_nomination_screen.py`, `src/api/tests/test_resident_api.py`, `src/api/tests/test_nomination_api_routes.py`.
* Excluded: Modifying `test_accessibility_baseline.py` thresholds.

#### Likely Targets

* src/api/tests/test_nomination_screen.py: Add explanation and interactive `(c, id, refresh)` assertions while keeping existing read-only tests green.
* src/api/tests/test_resident_api.py: Add dual-channel acknowledgement/challenge/correction HTTP checks.
* src/api/tests/test_nomination_api_routes.py: Comprehensive Issue #130 API/UI/permission/keyboard/non-leakage test module.

#### Dependencies

* P02.

#### Validation Expectations

* `python3 -m unittest` across new and existing `src/api` test modules exits `0`, and `mypy`/`ruff` pass on all test modules.

#### Completion Evidence

* Passing `src/api` unit, HTTP, DOM, accessibility-baseline, and content-standard suites.

#### Unresolved Items

* None.

<!-- rpi:phase id=P04 -->
## P04: Focused Tier Validation and Clean Local Verification

### Context

The caller specifies the Focused validation tier: targeted unit tests in `src/core` and `src/api` (including `test_accessibility_baseline.py`), `python3 -m ruff check`, `ruff format` checks (`ruff format --check` respecting `pyproject.toml` legacy excludes plus `python3 -m ruff format --isolated --line-length 100 --check` on newly added and non-legacy-excluded modified files), and bare `python3 -m mypy` inside `src/core` and `src/api` (`--cache-dir=/tmp/mypy-130`).

### Intent

Execute every required check using the Python 3.12 toolchain and worktree source paths (`PYTHONPATH` / `MYPYPATH`) without creating `/tmp` virtual environments, confirm zero errors, and verify `git status --short` contains only intended files.

### Boundaries

* Included: Running validation commands and recording exact command outputs for `.copilot-tracking/changes/2026-11-15/nomination-api-routes-130-changes.md`.
* Excluded: Pushing to git remotes, opening pull requests, or creating `/tmp` virtualenvs.

### Likely Targets

* .copilot-tracking/changes/2026-11-15/nomination-api-routes-130-changes.md: Record exact verification evidence during implementation.

### Dependencies

* P03.

### Validation Expectations

* Exit code `0` on all targeted `unittest`, `ruff check`, `ruff format --check`, `ruff format --isolated --line-length 100 --check`, and `mypy --cache-dir=/tmp/mypy-130` commands.

### Completion Evidence

* Clean exit codes and reconciled plan checkboxes ready for `rpi-review`.

### Unresolved Items

* None.

<!-- rpi:task id=P04-T01 -->
### P04-T01: Execute focused `unittest`, `ruff`, and `mypy` verification suites

#### Context

Both `src/core/pyproject.toml` and `src/api/pyproject.toml` declare `mypy_path`, and passing `MYPYPATH="../agents/src"` (or worktree `PYTHONPATH`) allows bare `python3 -m mypy --cache-dir=/tmp/mypy-130` to check all files in `src/core` and `src/api` directly against worktree sources without creating any `/tmp` virtualenv.

#### Intent

Run and verify every focused-tier test, lint, format, and type-check command to green.

#### Boundaries

* Included: `unittest`, `ruff check`, `ruff format --check .`, `ruff format --isolated --line-length 100 --check` on non-legacy-excluded modified/added Python files, `mypy --cache-dir=/tmp/mypy-130`, and `git status --short` inspection.
* Excluded: Modifying CI workflows or branch protection.

#### Likely Targets

* Validation execution only (no source edits unless fixing a caught defect).

#### Dependencies

* P03-T01, P03-T02.

#### Validation Expectations

* All commands exit `0`.

#### Completion Evidence

* Recorded command outputs in `.copilot-tracking/changes/2026-11-15/nomination-api-routes-130-changes.md`.

#### Unresolved Items

* None.
