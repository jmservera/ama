<!-- markdownlint-disable-file -->

# Task Research: nomination-api-routes-130

| Field              | Value                                                                    |
|--------------------|--------------------------------------------------------------------------|
| Date               | 2026-11-15                                                               |
| Researcher / agent | rpi-research (RPI Agent automatic session)                               |
| Status             | Completed                                                                |
| Artifact path      | .copilot-tracking/research/2026-11-15/nomination-api-routes-130-research.md |

## Research Brief

* What to research: Remaining `src/api` and plain-language explanation slice of Issue #130 (`Nomination, self-referral, acknowledgement and challenge route`, `Refs #130`), covering (1) deterministic, role/field-filtered plain-language explanation of AI involvement, sources/policy reasons, uncertainty, and named human decision ownership (`human_decision_owner`, `ai_involvement_explanation`, `policy_reasons`, `uncertainty_note`) on nomination/follow-up/challenge views and API payloads without leaking restricted internal vulnerability details, and (2) wiring both digital (`channel="digital"`) and equivalent staff-recorded non-digital (`channel="staff_recorded_non_digital"` / phone/paper/in-person assisted intake) routes for nomination acknowledgement, challenge submission, and correction across `src/api` endpoints and accessible HTML forms/views with role field-permission checks and keyboard operability.
* Why it matters: Connects the verified `src/core` nomination/challenge domain controls (`PR #1710`, `PR #1742`) to staff/resident-facing API and HTML workbench surfaces while honoring strict role boundaries, plain-language content rules, and WCAG 2.2 baseline invariants (`test_accessibility_baseline.py`, `test_content_standard.py`, `test_epic149_form_error_summary_associations.py`).
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` in this continuous automatic RPI execution.
* Scope: `src/core/src/zava_forward/core/nomination_route.py`, `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/src/zava_forward/core/store.py`, `src/api/src/zava_forward/api/server.py`, `src/api/src/zava_forward/api/nomination_routes.py` (new typed API helper module), `src/api/src/zava_forward/api/web/panels.js`, `src/api/src/zava_forward/api/web/app.js`, and targeted unit/API/UI/keyboard/permission/accessibility/content tests in `src/core/tests/` and `src/api/tests/`.
* Non-goals: Pushing to remote, opening a PR, fabricating human governance ratification (`OD-41`, `OD-42`) or authorized human representative comprehension acceptance, altering branch protection/CI workflows, or breaking counted `aria-invalid` (`9`) or `table` (`14`) static guards in `test_accessibility_baseline.py`.
* Criteria: Every acceptance criterion in the caller brief mapped to exact `path:line` contracts, role/field visibility masks, channel mapping rules (`digital` vs `staff_recorded_non_digital`), keyboard/label/status accessibility rules, and focused-tier validation commands (`unittest`, `ruff check`, `ruff format --isolated --line-length 100 --check`, `mypy`).
* Requested outputs: Converged architectural and contract recommendation ready for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                   |
|----------------------------------|-------------------------------------------------------------------------|
| Research question(s)             | Q1-Q5 covering actual `src/api` module mapping, deterministic plain-language explanation schema and role/field vulnerability redaction, digital vs `staff_recorded_non_digital` channel contracts across acknowledgement/challenge/correction, per-role field permissions and `HazardRouted` API handling, and WCAG/plain-language/worktree static invariants. |
| Codebase scope                   | `src/core/`, `src/api/`, `docs/brds/`, `docs/prds/`, `docs/reference/research/ux/`, `.copilot-tracking/reviews/2026-11-14/` |
| External scope                   | Vercel Web Interface Guidelines (`raw.githubusercontent.com/vercel-labs/web-interface-guidelines`) per repository Web Development Guidance |
| Initial internal candidate areas | `src/core/src/zava_forward/core/nomination_route.py`, `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/src/zava_forward/core/projection.py`, `src/core/src/zava_forward/core/store.py`, `src/api/src/zava_forward/api/server.py`, `src/api/src/zava_forward/api/web/panels.js`, `src/api/src/zava_forward/api/web/app.js`, `src/api/tests/test_nomination_screen.py`, `src/api/tests/test_resident_api.py`, `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_content_standard.py`, `src/api/tests/test_epic149_form_error_summary_associations.py`, `src/api/tests/test_role_endpoint_inventory.py` |
| Initial external candidate areas | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` |
| Research posture                 | balanced                                                                |
| Posture provenance               | default (bounded multi-package slice with adjacent accessibility/content-standard/permission invariants) |
| Explicit limits / deadline       | Focused validation tier; single continuous run ending in frozen local commit without push or PR |
| Posture-specific completion basis| Balanced scope coverage and adequate evidence across `src/core` and `src/api` contracts and static UI/a11y guards |
| Edits allowed during research?   | no, research-only                                                       |
| Resolved evidence root           | `.copilot-tracking/` default                                            |
| Known constraints / excluded sources | Never read private datasets; preserve Fluent 2 tokens, WCAG 2.2 baseline (`test_accessibility_baseline.py`), and plain-language content standard (`test_content_standard.py`) over generic aesthetics |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                              | Scoped authority or output contract          | Selected / skipped reason      |
|---------------------|----------------------------------|---------------------------------------------------|----------------------------------------------|--------------------------------|
| Instruction         | `.github/copilot-instructions.md` (AMA Repository Instructions) | `applyTo: "**"` matches workspace and tracking paths | Adds Web Development Guidance, plain-language content standard, WCAG baseline, and focused-tier validation rules | Selected: governs repo conventions, web skill checks, and test/commit rules |
| Skill               | `redesign-existing-projects`     | Existing-app web UI improvement guidance in repository instructions | Scoped UI audit subordinated to Fluent 2 tokens, WCAG baseline, and plain-language content standard | Selected: loaded at intake; aesthetic overhaul options subordinated to repo Fluent 2/WCAG/plain-language rules |
| Skill               | `web-design-guidelines`          | Required by repository Web Development Guidance before web edits and review | Fetches current Vercel Web Interface Guidelines rules (`W1`) for implementation and `file:line` review | Selected: loaded and source fetched (`W1`) |
| Research specialist | `hve-core-all:rpi-researcher`    | Registered general RPI research worker            | Independent research lane artifact           | Skipped for inline fallback: tightly coupled `src/core` + `src/api` contracts fit direct fast reads with zero cross-lane overhead |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                       | Answers / unanswered      | Resulting decision or selected further research    |
|------------------|-------------------------------------------------------------|---------------------------|----------------------------------------------------|
| Intake           | Non-interactive continuous execution explicitly instructed by caller with concrete AC1, AC2, target files, and focused validation commands. | N/A (sufficient brief; non-interactive runtime) | Proceed directly in `balanced` posture with `convergence` output mode. |
| Direction change | None triggered during research.                             | N/A                       | Maintain caller scope (`Refs #130`).               |
| Convergence      | All 5 research questions resolved from repository code and tests without ambiguity requiring human input. | N/A (non-interactive runtime) | Converge on unified `src/core` + `src/api` contract and advance automatically to `rpi-plan`. |

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint  | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|-----------------------|----------------------|---------------------------------------------------|
| narrow                                                   | Deliver remaining `src/api` and plain-language explanation slice (`AC1`, `AC2`) under `Refs #130`; keep `aria-invalid` guard intact in `test_accessibility_baseline.py` | Caller intake prompt | Constrains implementation and contrarian alternatives to compliant server/UI patterns |
| exclude                                                  | Do NOT push or open a PR; leave clean frozen local commit with `2026-11-15` tracking artifacts | Caller intake prompt | Prohibits remote git/GitHub write actions |

## Research Questions

* Q1: How do the prompt's conceptual `app.py`, `web.py`, and `workbench_views.py` references map onto actual files in `src/api/src/zava_forward/api/`?
* Q2: How should deterministic, permitted plain-language explanations (`human_decision_owner`, `ai_involvement_explanation`, `policy_reasons`, `uncertainty_note`) be derived and role/field-filtered across nomination, follow-up, and challenge payloads and UI views so restricted internal vulnerability details never leak?
* Q3: How are channels currently validated across `nomination_acknowledge`, `challenge_open`, and `nomination_correct` (and `nomination_record`), and how can both `channel="digital"` and `channel="staff_recorded_non_digital"` (with phone/paper/letter/in-person/intermediary assisted intake) work alongside existing channel labels?
* Q4: Which per-role and per-field permissions, server-derived field refusals, and `HazardRouted` fail-closed responses must be enforced across API endpoints and workbench forms?
* Q5: Which static engineering guards, browser focus-order assertions, plain-language copy checks, formatting exclusions, and worktree `mypy`/`unittest` isolation constraints govern `src/core` and `src/api`?

## Prior Knowledge Gate

* Reviewed `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `docs/brds/agentic-retrofit-programme-brd.md` (`FR-037`, `FR-041`, `AC-065`, `RULE-005`, `CON-003`), `docs/prds/zava-forward-retrofit-programme-demonstrator.md` (`FR-037`, `FR-043`, `FR-052`, `AC-071`), `docs/reference/research/ux/design-system.md`, `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/research/ux/content-standard.md`, Issue #130 (`gh issue view 130`), and parent review `.copilot-tracking/reviews/2026-11-14/nomination-challenge-130-2142-review.md`.

## Research Cycle Log

### Cycle 1

* Wider wave: Inventoried all 292 Python files and web assets under `src/api` plus `src/core` modules (`nomination_route.py`, `resident_decisions.py`, `projection.py`, `challenges.py`, `store.py`) and fetched live Vercel Web Interface Guidelines (`W1`). Confirmed `resident_demo/app.py` and `resident_preview/app.py` are isolated read-only resident showcase/preview servers, while the staff/resident-liaison HTTP API and Resident-tab UI live in `src/api/src/zava_forward/api/server.py`, `workbench.py`, `web/panels.js`, and `web/app.js`.
* Deeper wave: Inspected exact payload schemas, `store.detail` projection (`followup_view`, `challenge_catalog`, `redact_staff_detail`), `server.py` `do_GET`/`do_POST` (`/api/cases/<cid>`, `/api/cases/<cid>/resident`), `panels.js` (`nominationPanel`, `affectedChallengePanel`, `formFor`, `captureChallengeDrafts`), and existing tests (`test_resident_api.py`, `test_nomination_screen.py`, `nomination_browser_check.py`, `challenge_browser_check.py`).
* Contrarian wave: Probed five potential failure modes against repository static/type/lint suites (`test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_content_standard.py`, `test_role_endpoint_inventory.py`, `ruff format --isolated`, and bare `mypy` in `src/core` and `src/api`), uncovering critical constraints `D1`-`D6` documented below.
* Re-entry check: Every research question (`Q1`-`Q5`) and acceptance criterion (`AC1`, `AC2`) is backed by verified `path:line` evidence and contrarian checks. No second cycle is required.

## Evidence Log

### Codebase Evidence

* `C1` (`src/api/src/zava_forward/api/server.py:981-983` and `1622-1646`): The main HTTP API serves `GET /api/cases/<cid>` via `s.detail(cid, u)` and `POST /api/cases/<cid>/resident` via `s.resident_action(u, cid, body)` returning `200` with refreshed `s.detail(cid, u)`, `403` on `PermissionError`, `409` on `ConflictError`/`ResidentCommittedError`, and `400` on `ValueError` (including `HazardRouted`, which subclasses `ValueError`). `resident_demo/app.py:1-18` and `resident_preview/app.py:1-15` are separate read-only servers that import no staff routes.
* `C2` (`src/api/src/zava_forward/api/web/app.js:1197` and `src/api/src/zava_forward/api/web/panels.js:301-495`): The Resident tab mounts `[residentPanel(c, id, refresh), nominationPanel(c), call, write, affectedChallengePanel(c, id, refresh)]`. `nominationPanel` (`panels.js:301-393`) currently takes only `(c)` and renders read-only `<details class="nomination-record">` cards without plain-language AI/policy/uncertainty/human-owner blocks or interactive acknowledgement/correction forms; `affectedChallengePanel` (`panels.js:395-495`) renders challenge targets, open/resolve forms via `formFor`, and `challenge_guarantees`.
* `C3` (`src/core/src/zava_forward/core/store.py:463-521` and `src/core/src/zava_forward/core/projection.py:48-245`): `store.detail` populates `followup_view(d)` and, only when `challenge_references_visible(self, user)` holds (requiring current registered staff with `appointment_evidence_visible(user)`, i.e., `role in RESIDENT_VIEW_ROLES and can_see_reason(user)`), attaches `challenge_targets`, `challenge_guarantees`, and `challenge_assurance`; otherwise `INTAKE_FIELDS` (`nomination_records`, `tenure_reports`, etc.) and `affected_challenges` are stripped. `projection.redact_staff_detail` additionally strips `resident["reason"]` and contact/hazard free-text `note`s when `not can_see_reason(user)`.
* `C4` (`src/core/src/zava_forward/core/resident_decisions.py:534-565` and `src/core/src/zava_forward/core/nomination_route.py:31-185`): `nomination_follow_up` computes `route_ready`, `missing`, `next_update_overdue`, `re_review_pending`, `dependent_review_versions_stale`, `review_current`, `review_owner`, and `not_inferred`, and `followup_view` attaches `follow_up` and `challenge_trail`, but neither `nomination_records`, `follow_up`, `affected_challenges`, nor `challenge_targets` exposes a deterministic `plain_language_explanation` structure (`human_decision_owner`, `ai_involvement_explanation`, `policy_reasons`, `uncertainty_note`).
* `C5` (`src/core/src/zava_forward/core/challenges.py:10-35` and `279-287`): `ChallengeRegister` defines `ROUTES = ("digital", "staff_recorded")`, `NON_DIGITAL_CHANNELS = ("phone", "in_person", "paper", "assisted_visit")`, and filters `explanations` to `e["permitted"] is True` in `ChallengeRegister.view`.
* `C6` (`src/core/src/zava_forward/core/resident_decisions.py:70`, `1207-1325`, and `1666-1700`): `_res_nomination_record` and `_res_nomination_correct` accept only `INTAKE_CHANNELS = ("Digital", "Phone", "Letter", "In person", "Trusted intermediary")`; `_res_challenge_open` accepts only `("Digital", "Phone", "Letter", "In person")`; and `_res_nomination_acknowledge` (`1240-1276`) does not accept `channel` or `assisted_channel` at all. Passing `channel="digital"` or `channel="staff_recorded_non_digital"` currently fails closed with `400 ValueError` on all three actions.
* `C7` (`src/core/src/zava_forward/core/resident_decisions.py:258-287`, `485-531`, `1248-1255`, `1286-1293`, and `1668-1686`): Role and field permissions require `projection.appointment_evidence_visible(user)` for all intake and challenge actions (`PermissionError` -> `403`), enforce closed-schema field sets (`_intake_fields` / `set(body) == fields`) so server-derived fields (`recorded_by`, `version`, `verification`, `identity_status`, `support_needs`, `risk_flags`, `assurance`, `human_decision`) cannot be supplied by any role, require `_owner_rights` (current named owner or `MANAGERS`) to acknowledge an already-owned record, record a correction, or resolve a challenge, and require confirmed in-date `Communicate` authority via `_raiser` when `raised_by == "Representative"`.
* `C8` (`src/api/tests/test_accessibility_baseline.py:86-119` and `src/api/tests/test_epic149_form_error_summary_associations.py:18-137`): Static WCAG baseline tests pin exact counts across `web/*.js`: `setAttribute("aria-invalid", "true")` MUST equal `9` (`panels.js:466` inside `formFor` is the 1 counted site in `panels.js`, paired with `id: `${key}-feedback`` and `"before recording this challenge."` in `RECOVERY_COPY`), and `h("table", {}, ...)` MUST equal `14`. Reusing one shared form validation helper in `panels.js` gives every nomination and challenge form real `aria-invalid="true"`, `aria-describedby`, and `.focus()` error recovery while keeping `sites == 9` and `tables == 14`.
* `C9` (`src/api/tests/test_content_standard.py:16-95`): `AUDITED_FILES` asserts an exact file set over `web/*.js` and `web/*.html`, and `BANNED` forbids `\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b` on every line (including JS comments and identifiers) of every web file unless explicitly allowlisted.
* `C10` (`src/api/tests/test_nomination_screen.py:11-31` and `94-164`): Slices `panels.js` from `function nominationPanel` to `\nfunction affectedChallengePanel`, calls `nominationPanel(c)` with only `(c)` (`id` and `refresh` undefined), and asserts `out["controls"] == []` on read-only case dictionaries while checking exact strings (`"Named owner: Unknown"`, `"Support needs: Unknown"`, `"Risk flags: Unknown"`, `"Delivery unverified"`, etc.).
* `C11` (`src/api/checks/nomination_browser_check.py:128-145` and `src/api/checks/challenge_browser_check.py:67-116`): Browser harness focuses `#nominations-title`, presses `Tab` once, and asserts `#nominations summary` (first nomination record `<summary>`) receives focus (`nomination_browser_check.py:131-133`), and asserts `non_get == []` while passively viewing. In `challenge_browser_check.py`, `Digital` and `Phone` options in `#challenge-open-channel` are exercised along with draft preservation across tab switches via `captureChallengeDrafts` / `restoreChallengeDrafts`.
* `C12` (`src/api/tests/test_role_endpoint_inventory.py:18-62`): Scans `SERVER_SRC` (`server.py`) with regexes for `"/api/..."` literals and requires every discovered route to appear in `GET_ENDPOINTS` or `POST_ENDPOINTS` and pass all-role canary checks (`REASON`, `PHONE`, `RESIDENT`, `NOTE_CANARY`, `OUTCOME_CANARY`).
* `C13` (`src/api/pyproject.toml:35-65` and `tools/rpi-checks.py:974-985`): `server.py` and `test_role_endpoint_inventory.py` are legacy-formatted files excluded in `[tool.ruff.format] exclude`. Running `ruff format --isolated --line-length 100 --check` on modified files requires every file we modify in Python to conform cleanly to 100-column `ruff format`! Furthermore, `src/api` `mypy` expects sibling `zava-forward-core` and `zava-forward-agents` distributions installed in an isolated worktree venv (per `rpi-checks.py:974-985`) so `test_ai_consumption_api.py`'s `# type: ignore[import-untyped]` comments remain valid while checking all 292 files in `src/api` and 317 files in `src/core`.

### External Evidence

* `W1` (`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`, retrieved 2026-11-15): Live Vercel Web Interface Guidelines require explicit `<label>` associations for every form control, keyboard operability (`<button>`, `<summary>`, native inputs), programmatic focus and inline error feedback instead of `window.alert()`, `autocomplete="off"` on non-personal workflow inputs, visible `:focus-visible` states, `overflow-wrap: anywhere` / `min-width: 0` container resilience at 320px, and sentence-case plain copy without raw technical errors.

### Contradictions / Conflicts

* Prompt shorthand (`app.py`, `web.py`, `workbench_views.py`) versus repository layout (`server.py`, `nomination_routes.py`, `web/panels.js`, `web/app.js`, `workbench.py`): resolved from `C1` and `C2` by wiring the live HTTP endpoints and Resident-tab workbench scripts actually served by `zava_forward.api` plus a clean, strictly typed `src/api/src/zava_forward/api/nomination_routes.py` API boundary module so `src/api` owns typed route/permission/explanation helpers without reformatting legacy `server.py` (`C13`).

## Findings Mapped to Questions and Evidence

* Q1 (`C1`, `C2`, `C12`, `C13`): The workbench API and HTML UI for nominations and challenges are served by `server.py` (`/api/cases/<cid>` and `/api/cases/<cid>/resident`) and rendered by `web/panels.js` (`nominationPanel`, `affectedChallengePanel`) mounted in `web/app.js:1197`. Adding a strictly typed `src/api/src/zava_forward/api/nomination_routes.py` module for API-layer route/channel/permission/explanation helpers while wiring `src/core` (`nomination_route.py`, `resident_decisions.py`, `store.py`) and `src/api/src/zava_forward/api/web/{panels.js,app.js}` delivers live HTTP endpoints and HTML views while keeping every modified Python file 100% compliant with `ruff format --isolated --line-length 100 --check` and `mypy --strict`.
* Q2 (`C3`, `C4`, `C5`): Add deterministic plain-language explanation builders in `nomination_route.py` (`nomination_explanation`, `challenge_explanation`, and `filter_explanation_for_viewer`) producing `{human_decision_owner, ai_involvement_explanation, sources, policy_reasons, uncertainty_note, permitted: True}` from allowlisted provenance fields only:
  * Never read or echo restricted internal vulnerability details (`resident.reason`, `resident.adjustment`, `resident.support`, `resident.priority_support`, `contacts[*].note`, `hazards[*].note`, or unpermitted internal notes / `internal_vulnerability_note` / `health_detail` / `safeguarding_note`).
  * Keep unknown `identity_status`, `support_needs`, `risk_flags`, and unverified acknowledgement delivery explicitly noted in `uncertainty_note` (`"Unknown"`, never `"None"`).
  * State deterministically whether AI was involved (`"No AI was used..."` for unlinked referrals or workflow-only proposals; `"An AI suggestion was involved in linked priority suggestion ...; AI did not decide eligibility, infer health or support needs, or change priority"` when linked to `source == "ai"`), list permitted sources and policy reasons (`FR-037`, `FR-043`, `RULE-005`), and name the human decision owner.
  * Attach `plain_language_explanation` to `nomination_records[*]`, `nomination_records[*]["follow_up"]`, `affected_challenges[*]`, and `challenge_targets[*]` for `appointment_evidence_visible` readers, while keeping those collections completely omitted for unauthorized roles (`C3`) and providing field-level redaction in `filter_explanation_for_viewer` for restricted/non-reason contexts.
* Q3 (`C5`, `C6`, `C11`): Add `nomination_route.normalize_route_channel(channel, *, assisted_channel=None, allow_intermediary=True)` supporting both canonical route tokens (`"digital"` and `"staff_recorded_non_digital"` with optional `assisted_channel` in phone/paper/letter/in_person/trusted_intermediary) and existing UI labels (`"Digital"`, `"Phone"`, `"Letter"`, `"In person"`, `"Trusted intermediary"`, `"Paper"`):
  * Preserve exact submitted `"Digital"` / `"Phone"` / `"Letter"` / `"In person"` / `"Trusted intermediary"` in `channel` when those labels are passed (preserving `test_resident_api.py` and `challenge_browser_check.py`), and store `"digital"` or `"staff_recorded_non_digital"` in `channel` when canonical tokens are passed, alongside normalized `route_mode` (`"digital"` | `"staff_recorded_non_digital"`) and `assisted_channel` (`None` for digital; normalized non-digital medium for staff-recorded non-digital).
  * Wire `normalize_route_channel` across `_res_nomination_acknowledge` (optional `channel` and `assisted_channel`, persisted on `acknowledgement` and `acknowledgement_history`), `_res_challenge_open`, `_res_nomination_correct`, and `_res_nomination_record`. Reject `assisted_channel` when `route_mode == "digital"` and reject any unlisted channel value (`400 ValueError`).
* Q4 (`C1`, `C7`): Enforce role and field permissions on both API and UI:
  * Only `appointment_evidence_visible(user)` roles (`Resident Liaison Officer`, `Retrofit Programme Manager` by default) can view or submit nomination/challenge routes; non-reason/non-resident roles (`Retrofit Coordinator`, `Programme Support Officer` without reason role, `Building Safety Liaison`, `Quality Inspector`, `Grants and Evidence Officer`, `Contractor`, and `view_only` `Application Administrator`) are refused (`403`) and receive zero intake/challenge fields.
  * Server-derived fields (`recorded_by`, `at`, `version`, `verification`, `identity_status`, `support_needs`, `risk_flags`, `plain_language_explanation`, `human_decision`, `assurance`, `re_review`) are rejected if supplied by any caller (`400`), and non-owner non-manager officers (`_owner_rights`) are refused (`403`) from re-acknowledging/reassigning `owner` or recording corrections on another named officer's referral.
  * Attach `c["nomination_permissions"]` (per-case `can_write`, `can_reassign_owner`, `staff_options` filtered to `appointment_evidence_visible` colleagues, and per-record `can_edit`) in `store.detail` so `panels.js` renders interactive acknowledgement/correction controls only for permitted fields/actors while server validation enforces all rules independently.
* Q5 (`C8`, `C9`, `C10`, `C11`, `C13`, `W1`):
  * Share a single `residentRouteForm` helper in `panels.js` (placed above `function nominationPanel` or shared cleanly so `test_nomination_screen.py`'s slice and read-only `nominationPanel(c)` call with no `id` still pass with `controls == []`!) containing the ONE counted `input.setAttribute("aria-invalid", "true")` site (`sites == 9`) and retaining `"before recording this challenge."` for `RECOVERY_COPY`.
  * Render interactive `<details>` forms for nomination acknowledgement and nomination correction INSIDE each `<details class="nomination-record">` card BELOW its `<summary>` and `<dl>` data lists so `#nominations summary.first` remains the very first Tab stop after `#nominations-title` (`nomination_browser_check.py:131-133`), zero `<table>` elements are added (`tables == 14`), zero new `.js`/`.html` files are created (`AUDITED_FILES`), and zero banned internal words (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`) appear anywhere in `web/panels.js` or `web/app.js`.
  * Use an isolated `/tmp/venv-130` virtual environment with editable installs of worktree `src/core`, `src/agents`, and `src/api` (without touching shared `.local` site-packages) plus `_bootstrap_worktree_paths()` in new test files so bare `mypy --cache-dir=/tmp/mypy-130` and `unittest` validate this worktree cleanly.

## Key Discoveries

* `D1`: `test_accessibility_baseline.py` and `test_epic149_form_error_summary_associations.py` hard-pin `9` occurrences of `setAttribute("aria-invalid", "true")`, `14` `h("table", {}, ...)` sites, and `"before recording this challenge."` in `panels.js` (`C8`). Sharing one form helper in `panels.js` satisfies keyboard error association across all nomination and challenge forms without altering baseline counts.
* `D2`: `test_content_standard.py` scans every line (including JS comments and variable names) of `web/*.js` for `gate`, `hold`, `provenance`, `trace`, `snapshot`, and `envelope` (`C9`).
* `D3`: `test_nomination_screen.py` slices `panels.js` between `function nominationPanel` and `\nfunction affectedChallengePanel`, evaluates `nominationPanel(c)` with no `id`/`refresh`, and asserts `controls == []` (`C10`); `nomination_browser_check.py` asserts `Tab` from `#nominations-title` focuses `#nominations summary.first` (`C11`).
* `D4`: `_res_nomination_acknowledge`, `_res_challenge_open`, and `_res_nomination_correct` currently reject `channel="digital"` and `channel="staff_recorded_non_digital"` (`C6`).
* `D5`: `server.py` is excluded from `ruff format` in `src/api/pyproject.toml` (`C13`); keeping `server.py` untouched (since `GET /api/cases/<cid>` and `POST /api/cases/<cid>/resident` already route through `Store.detail` and `Store.resident_action`) and adding typed API helpers in a new 100-col-formatted `src/api/src/zava_forward/api/nomination_routes.py` module guarantees `ruff format --isolated --line-length 100 --check` passes on every modified Python file.
* `D6`: Bare `mypy` in `src/api` requires sibling worktree packages (`core`, `agents`, `api`) installed in an isolated venv (matching `tools/rpi-checks.py:974-985`) so `test_ai_consumption_api.py`'s `type: ignore[import-untyped]` annotations stay consistent across all 292 checked files (`C13`).

## Alternatives and Decision State

### Selected Recommendation

* Extend `src/core/src/zava_forward/core/nomination_route.py` (`mypy --strict`) with deterministic plain-language explanation builders (`nomination_explanation`, `challenge_explanation`, `filter_explanation_for_viewer`) and closed-vocabulary route/channel normalization (`normalize_route_channel` supporting `"digital"`, `"staff_recorded_non_digital"`, and assisted non-digital channels alongside existing labels).
* Wire `src/core/src/zava_forward/core/resident_decisions.py` and `store.py` so `nomination_acknowledge`, `challenge_open`, `nomination_correct`, and `nomination_record` accept both digital and staff-recorded non-digital routes with strict role/owner/field permission enforcement, and `store.detail` projects `plain_language_explanation` and `nomination_permissions` only to authorized roles with zero restricted vulnerability leakage.
* Add strictly typed `src/api/src/zava_forward/api/nomination_routes.py` exposing API-layer explanation projection, channel/payload validation, and per-role field-permission checks over `App`/`Store` payloads, and wire `src/api/src/zava_forward/api/web/app.js` (`nominationPanel(c, id, refresh)`) + `src/api/src/zava_forward/api/web/panels.js` to render plain-language explanations (`human_decision_owner`, `ai_involvement_explanation`, `policy_reasons`, `uncertainty_note`) and keyboard-operable digital + staff-recorded non-digital forms for nomination acknowledgement, nomination correction, and challenge submission using a single shared `formFor` validation helper (`sites == 9`, `tables == 14`, zero banned words).

### Alternative: Duplicate `setAttribute("aria-invalid", "true")` per form and bump `test_accessibility_baseline.py` count from 9 to 11

* Rejected: Explicitly prohibited by caller instruction (`without breaking any counted aria-invalid guard in src/api/tests/test_accessibility_baseline.py`) and would also break `SITES` mapping in `test_epic149_form_error_summary_associations.py` (`C8`). Sharing `formFor` in `panels.js` gives genuine `aria-invalid` + `aria-describedby` + `.focus()` on every form with `sites == 9`.

### Alternative: Add bespoke `/api/cases/<cid>/nominations/...` routes directly inside `server.py`

* Rejected: `server.py` already exposes `GET /api/cases/<cid>` and `POST /api/cases/<cid>/resident` used by every Resident-tab workflow (`C1`, `C2`), is excluded from `ruff format` so editing it conflicts with `ruff format --isolated --line-length 100 --check` (`C13`), and any new route literal in `server.py` triggers regex coupling in `test_role_endpoint_inventory.py` (`C12`). Keeping HTTP transport on `/api/cases/<cid>` + `/api/cases/<cid>/resident` and housing new `src/api` Python helpers in `src/api/src/zava_forward/api/nomination_routes.py` is cleaner, strictly typed, and backward-compatible.

## Open Questions, Risks, and Residual Uncertainty

* Governance ratifications `OD-41` and `OD-42` and authorized human representative comprehension testing remain open human gates on Issue #130 (`Refs #130`, never `Closes #130`).
* In `test_nomination_screen.py` (`C10`), `src.slice(start, end)` extracts only `function nominationPanel` up to `\nfunction affectedChallengePanel`; therefore any helper invoked inside `nominationPanel` when `id` is provided must either live inside `nominationPanel` or be passed/resolved safely so read-only `nominationPanel(c)` (`id === undefined`) continues to evaluate standalone with zero external dependencies beyond `h`!

## Current Decisions

* Use `Refs #130` on commits; preserve all human governance gates (`OD-41`, `OD-42`, human representative evidence).
* Implement deterministic plain-language explanation and `digital` / `staff_recorded_non_digital` channel contracts in `nomination_route.py` + `resident_decisions.py` + `store.py`, surface API-level route/permission/explanation helpers in `src/api/src/zava_forward/api/nomination_routes.py`, and wire Resident-tab views/forms in `web/panels.js` + `web/app.js`.
* Preserve `sites == 9`, `tables == 14`, `AUDITED_FILES`, banned-word rules, `test_nomination_screen.py` standalone slice behavior, and `#nominations summary.first` first-Tab focus order.

## Unresolved Decisions

* `OD-41`, `OD-42`, and human representative participation/comprehension acceptance remain human-owned outside engineering automation.

## Potential Next Research

* Post-ratification policy-owner configuration once Zava North Homes ratifies `OD-41` and `OD-42`.

## Planning Readiness

* Planning Readiness: `Ready`
* Research disposition: `executed`

## Closeout Record

* Completed full 3-wave (`Wider`, `Deeper`, `Contrarian`) read-only research cycle with `C1`..`C13` codebase evidence and `W1` fetched Web Interface Guidelines evidence. Zero production or test files edited during Research.

## Advisory Next Step

* Advance automatically to `rpi-plan` in this active automatic RPI Agent session.

## Artifact Self-Check

* Complete 3-wave cycle (`Wider`, `Deeper`, `Contrarian`) recorded in order: Yes.
* Every codebase claim backed by `C#` `path:line` and external rule backed by `W1` URL + date: Yes (`C1`..`C13`, `W1`).
* Research-only constraint honored (zero source/test edits during Research): Yes.
* Planning Readiness (`Ready`) and Research disposition (`executed`) recorded: Yes.
