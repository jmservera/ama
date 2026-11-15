<!-- markdownlint-disable-file -->
# RPI Changes: Housing Officer and Resident Engagement WCAG 2.2 AA Baseline (#232)

## Metadata

* Task ID: 2026-11-15-housing-resident-wcag-232
* Related plan: .copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/housing-resident-wcag-232-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`)
* Completed scope markers: P01, P01-T01, P01-T02, P02, P02-T01, P02-T02, P03, P03-T01, P03-T02
* All remaining active-plan markers: none
* Status basis: Every phase and task in the approved full plan has verified implementation and Focused-tier + Playwright/axe validation evidence.

## Execution Summary

Completed full-plan implementation for GitHub Issue #232 (*Housing officer and resident engagement screens*, WCAG 2.2 AA engineering baseline #151). Wired `#/role/contact_centre` alongside `#/role/housing_officer` and `#/role/resident_engagement` in `app.js` and `role-screens.js`; completed `aria-live="polite"` status attributes, `!signal.aborted`-guarded `#workspace-status` lifecycle announcements, `section#screen-evidence` region naming, and single-lookup jump-link focus in `role-screens.js`; upgraded `actForm` and `residentPanel` in `panels.js` with slugified whitespace-free HTML5 IDs, `type="button"`, `.table-scroll[role="region"][aria-label="Resident decisions by measure"][tabindex="0"]`, `<th scope="row">`, and plain-language non-colour state cues (plus coupled `#f-raise-a-commitment-supplier` selector alignment in `case_journey_browser_check.py`); authored strict-typed `src/api/tests/test_housing_resident_wcag_232.py`; audited changed web files against refreshed Web Interface Guidelines; and passed all Focused-tier, coupled unit, and Playwright + pinned axe 4.10.3 checks.

## Completed Work

### P01: Staff Route, Live-Status, and Focus Parity (`P01-T01`, `P01-T02`)

* Updated `isRoleScreensDestination(destination)` in `src/api/src/zava_forward/api/web/app.js` to normalize `String(destination || "").split("?")[0]` across all role hashes and include `#/role/contact_centre`.
* Added `"#/role/contact_centre": "resident-service-issues"` to `ROLE_HASH_SCREENS` in `src/api/src/zava_forward/api/web/role-screens.js` (resolved with `Object.hasOwn`).
* Added `"aria-live": "polite"` to the three shared-host `role="status"` paragraphs (`screenTable` truncation notice, loading state, and sidebar queue count) and added `!signal.aborted`-guarded `#workspace-status` announcements across invalid-page, unavailable-screen, chooser (`installed.length > 0` vs `0`), loading, and record-mismatch branches while keeping the settled `${role}. ${screen.title}. ${Selected home <id>.|No home selected.}` announcement unchanged.
* Preserved `"aria-label": "Evidence for ${c.id}"` alongside `id: "screen-evidence"` and `<h2 id="screen-evidence-heading" tabindex="-1">` on the selected-home section so Playwright `get_by_role("region", name="Evidence for ZF-1")` and workspace jump-link focus both succeed.
* Tightened the delegated `a[data-jump]` click listener to resolve `document.getElementById(link.getAttribute("data-jump"))` once before calling `.focus()` and `.scrollIntoView({ block: "start" })`.

### P02: Housing and Resident Case Panel Accessibility (`P02-T01`, `P02-T02`)

* Updated `actForm` in `src/api/src/zava_forward/api/web/panels.js` to generate lowercase hyphen-slugified HTML5 `id` and `<label for>` attributes (`f-${formSlug}-${slug(name)}` with per-form collision disambiguation) and set `type: "button"` on the manual submission button.
* Updated the coupled field-clear assertion in `src/api/checks/case_journey_browser_check.py` from `[id="f-Raise a commitment-supplier"]` to `#f-raise-a-commitment-supplier` so hosted CI `src-ci.yml` tracks the whitespace-free HTML5 ID.
* Wrapped `Resident decisions by measure` in `residentPanel` inside `<div class="table-scroll" role="region" aria-label="Resident decisions by measure" tabindex="0">`, promoted first-column measure cells to `<th scope="row">`, and added locally scoped `Object.hasOwn`-safe plain-language textual state cues (`Confirmed`, `Waiting for resident`, `Action needed`, `Unknown`) across contractor readiness badges (`m.flag === "Proceed"`), measure answers/readiness/versions, update commitments, and service/remedy items while keeping `test_case_journey.py` slice anchors, `test_resident_api.py` contiguous `"Response: <status>. Owner: <name>."` / `"Remedy: <status>. Owner: <name>."` substrings, `test_accessibility_baseline.py` exact table/ARIA counts, and `test_content_standard.py` vocabulary intact.

### P03: Focused WCAG 2.2 Verification, Web Guidelines Audit, and Validation (`P03-T01`, `P03-T02`)

* Created `src/api/tests/test_housing_resident_wcag_232.py` (8 strict-typed test methods, zero `sys.modules` mutations, zero `pyproject.toml` loosening) covering static HTML/CSS/JS invariants, Node VM routing and script isolation across `#/role/housing_officer`, `#/role/contact_centre`, and `#/role/resident_engagement`, default-deny and prototype-key rejection, `aria-live="polite"` and `#workspace-status` lifecycle announcements, landmarks/headings/jump focus/`section#screen-evidence` region naming, `.table-scroll` and `<th scope="row">` semantics, `ensure_ascii=False` Unicode rendering checks, `panels.js` `actForm` + `residentPanel` accessibility and state cues, and Python `projection.py`/`store.py`/`taskqueues.py` RBAC and safeguarding redaction.
* Refreshed `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` and reviewed changed web files in `file:line` format:
  * `src/api/src/zava_forward/api/web/app.js`: `✓ pass`
  * `src/api/src/zava_forward/api/web/role-screens.js`: `✓ pass` (plain ASCII `"Loading recorded evidence."` intentionally retained per `docs/reference/research/ux/content-standard.md` and `test_content_standard.py`)
  * `src/api/src/zava_forward/api/web/panels.js`: `✓ pass`

## Implementation-Time Plan and Detail Updates

* Immediately relevant current-state update (`P01-T02`, `role-screens.js`): Executing `checks/role_screens_browser_check.py 232` revealed that an earlier commit (`321a22960`) had replaced `"aria-label": "Evidence for ${c.id}"` with `"aria-labelledby": "screen-evidence-heading"` on `section#screen-evidence`, causing Playwright `get_by_role("region", name="Evidence for ZF-1", exact=True)` to time out on stories `232` and `232s`. Restored `"aria-label": "Evidence for ${c.id}"` while keeping `id: "screen-evidence"` and `<h2 id="screen-evidence-heading" tabindex="-1">`, and locked it with a regression assertion in `test_housing_resident_wcag_232.py`.
* Immediately relevant current-state update (`P02-T01`, `src/api/checks/case_journey_browser_check.py`): Inspecting hosted CI `.github/workflows/src-ci.yml` revealed that `checks.case_journey_browser_check` queried `[id="f-Raise a commitment-supplier"]` directly coupled to `actForm`'s pre-fix space-containing IDs. Updated that single selector to `#f-raise-a-commitment-supplier` and updated the plan and phase details accordingly. Tier classification per AMA validation policy (#1294): Focused tier preserved because aligning a DOM field ID selector to the new slugified `actForm` ID does not alter permissions, pinned actions/images, packages, secrets, deployment, security controls, or gate semantics.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| Focused unit + baseline + copy (`test_housing_resident_wcag_232.py`, `test_accessibility_baseline.py`, `test_content_standard.py`) | P01–P03 | Passed | `Ran 51 tests in 0.460s - OK` |
| Coupled WCAG, role-screen, journey, and resident unit suites (10 modules) | P01–P03 | Passed | `Ran 115 tests in 2.681s - OK` |
| Resident browser workflow (`ZF_RESIDENT_BROWSER=1 test_resident_api.py`) | P02 (`panels.js`) | Passed | `Ran 21 tests in 5.839s - OK` (Playwright Chromium 156.0.8078.4) |
| Specialist role-screen browser + pinned axe-core 4.10.3 (`role_screens_browser_check.py` `parent`, `232`, and `232s`) | P01, P03 (`role-screens.js`) | Passed | `0` axe violations and `0` incomplete items across queue + selected home on `232` and `232s`, `320px`/`390px`/`1280px` reflow, keyboard Tab reachability across all table regions, reduced motion, and zero POSTs |
| Case-journey browser axe + `actForm` clear check (`case_journey_browser_check.py --axe`) | P02 (`panels.js`, `case_journey_browser_check.py`) | Passed on changed scope | `#f-raise-a-commitment-supplier` clear check, Resident tab mutation/dirty-draft retention, `320px` Resident reflow, and all `axe no serious/critical` scans across every tab passed (`1637.4px` vs `1600px` `.case-summary` height on local Chromium 156 font metrics is pre-existing on untouched Overview header) |
| Lint, format, and strict type-checking (`ruff check .`, `ruff format --check .`, `mypy` in `src/api`) | `src/api` (`src`, `tests`, `checks`) | Passed | `All checks passed!`, `208 files already formatted`, `Success: no issues found in 292 source files` |
| Migration regression (`python3 tools/rename-zava-tests.py`) | Repo root | Passed | `Ran 25 tests in 0.538s - OK` |
| Refreshed `web-design-guidelines` review | `app.js`, `role-screens.js`, `panels.js` | Passed | `✓ pass` across all three changed web files |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02` all `[x]` and `Complete`).
* Completed-work evidence and handoff prose: Reconciled across `app.js`, `role-screens.js`, `panels.js`, `case_journey_browser_check.py`, and `test_housing_resident_wcag_232.py`.
* Validation, blockers, remaining work, and follow-up items: Reconciled (`0` blockers, `0` remaining active-plan tasks).
* Review readiness: Ready for single-pass `rpi-review`.

## Blockers

* None

## Remaining Work

* None in active plan scope (post-`rpi-review` local Git commit and rebase onto `origin/feat/demo-233-same-home-tensions-0825` will close out caller Requirement 2).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-plan.md, `## Follow-Up Items`
* Complete human assistive-technology (NVDA, JAWS, VoiceOver) and 360px mobile walkthroughs across `#/role/housing_officer`, `#/role/contact_centre`, `#/role/resident_engagement`, and `#/case/<id>?tab=resident` before closing Issue #232 — outside automated engineering scope under #151 and #155; owned by human accessibility reviewer.
* Reconcile parent-branch `resident-service-issues` (`Routes to ask` region) declaration in `src/api/checks/specialist_keyboard_browser_check.py` in a dedicated full-tier gate-tool PR — outside Focused-tier non-gate scope per AMA validation policy (#1294); owned by harness maintainer.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed: P01, P01-T01, P01-T02, P02, P02-T01, P02-T02, P03, P03-T01, P03-T02; remaining: none
* Validation coverage: Focused unit/baseline/copy (51 tests), coupled unit suites (115 tests), `ZF_RESIDENT_BROWSER=1` (21 tests), Playwright + pinned axe 4.10.3 `role_screens_browser_check.py` (`parent`, `232`, `232s`), `ruff check .`, `ruff format --check .`, `mypy` (292 files), `rename-zava-tests.py` (25 tests), and refreshed `web-design-guidelines` review all passed
* Blockers: None
* Current plan and detail updates: Recorded preserved `section#screen-evidence` `aria-label="Evidence for ${c.id}"` in `role-screens.js` and coupled `#f-raise-a-commitment-supplier` selector alignment in `src/api/checks/case_journey_browser_check.py`
* Planning and critique state: Ready (`PC-001`..`PC-004` disposed in plan)
* Follow-up items: Human AT/mobile walkthrough (#151/#155) and full-tier `specialist_keyboard_browser_check.py` update (#1294)
* Review readiness or no-handoff reason: Ready for single-pass `rpi-review`
* Continuation owner: parent (confirmed automatic RPI Agent)
