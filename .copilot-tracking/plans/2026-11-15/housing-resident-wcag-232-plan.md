<!-- markdownlint-disable-file -->
# RPI Plan: Housing Officer and Resident Engagement WCAG 2.2 AA Baseline (#232)

## Task Metadata

* Task ID: 2026-11-15-housing-resident-wcag-232
* Task slug: housing-resident-wcag-232
* Planning status: Ready for implementation
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/housing-resident-wcag-232-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/housing-resident-wcag-232-plan-critique.md

## Executive Summary

This plan completes the engineering accessibility implementation for GitHub Issue #232 (*Housing officer and resident engagement screens* — sole remaining criterion: *Accessible per the WCAG 2.2 baseline (#151) with textual state meaning and keyboard navigation*) on branch `feat/ux-232-resident-wcag` targeting `feat/demo-233-same-home-tensions-0825` (#1639).

Research across the live web UI (`app.js`, `role-screens.js`, `panels.js`, `index.html`, `style.css`), core projections (`projection.py`, `store.py`, `taskqueues.py`), and peer `#228`/`#231` WCAG suites confirmed that earlier iterations (`#1763`, `#1764`) established jump navigation and `screenRecordTable` semantics on `resident-choice` and `resident-service-issues`, while leaving three concrete WCAG 2.2 AA gaps across the three staff perspectives (neighbourhood housing officer, contact-centre officer, and resident engagement officer):
1. `#/role/contact_centre` is missing from `isRoleScreensDestination` in `app.js` and `ROLE_HASH_SCREENS` in `role-screens.js`.
2. `roleScreensView()` in `role-screens.js` announces `#workspace-status` only at the settled home/chooser render, omitting `aria-live` status updates on loading, chooser, invalid-page, unavailable-screen, and record-ID mismatch states, and omits explicit `aria-live="polite"` on three inline `role="status"` elements.
3. The housing/contact-centre/resident-engagement case workspace panel (`residentPanel` and `actForm` in `panels.js`) generates invalid whitespace-containing HTML `id`/`for` attributes, omits `type="button"` on manual action buttons, lacks a keyboard-focusable `.table-scroll[role="region"][tabindex="0"]` wrapper and `<th scope="row">` headers on the `Resident decisions by measure` table, and omits plain-language non-colour state cues on contractor readiness, measure answers, update commitments, and service/remedy items.

The plan closes all three engineering gaps surgically across `app.js`, `role-screens.js`, and `panels.js`, adds focused behavioral and static verification in `src/api/tests/test_housing_resident_wcag_232.py`, refreshes and audits against Web Interface Guidelines, runs all required Focused-tier validation commands, and commits locally with `Refs #232` without pushing.

### User Decisions and Requirements Highlights

* Complete the full RPI loop (`research`, `plan`, `implement`, `review`) with dated artifacts under `.copilot-tracking/` on branch `feat/ux-232-resident-wcag` targeting `feat/demo-233-same-home-tensions-0825` (#1639).
* Ensure all neighbourhood housing officer, contact-centre, and resident engagement queue and detail elements satisfy the WCAG 2.2 AA engineering baseline (#151): explicit textual state meaning (no colour-only badges/status), semantic landmarks/headings/tables, keyboard focusability and operable controls, programmatic focus management, and `aria-live` status announcements, with zero outbound resident contact triggers and zero role simulators.
* Deliver focused verification in `src/api/tests/test_housing_resident_wcag_232.py` (updating `src/api/pyproject.toml` mypy overrides only if required; strict typing requires zero loosening), pass all three user-specified validation commands, and commit locally with `Refs #232` and the Copilot trailer without pushing.

### What You May Not Know

* Static repository baseline guards strictly pin exact counts and lexical rules across `web/`: `test_accessibility_baseline.py` requires `h("table", {}, ...)` count `== 14`, `aria-invalid` count `== 9`, zero bare `h("th", {}`, and `position:fixed` count `== 2`; `test_content_standard.py` bans `\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b` across all served `.js` and `.html` files (meaning `panels.js` must check `m.flag === "Proceed"` rather than embedding the literal word `"Hold"`).
* `specialist_keyboard_browser_check.py` pins the exact settled `#workspace-status` string (`"{role}. {screen.title}. {Selected home X.|No home selected.}"`), and `test_resident_api.py` (`ZF_RESIDENT_BROWSER=1`) matches contiguous substrings `"Response: Open. Owner: <name>."`, `"Response: Closed."`, `"Response: Open."`, `"Response: Resolved."`, `"Remedy: Open."`, and `"Remedy: Resolved."` in `residentPanel`. Our updates place plain-language state cues outside those exact contiguous substrings while closing every intermediate `aria-live` and textual state-meaning gap.
* Automated DOM, Node VM, and unit tests establish engineering conformance only; human assistive-technology testing (NVDA, JAWS, VoiceOver) and 360px real-device checks (#151, #155) remain open, which is why the commit uses `Refs #232` rather than `Closes #232`.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Execute the full RPI loop in order (`research`, `plan`, `implement`, `review`), writing dated artifacts under `.copilot-tracking/` (`research`, `plans`, `details`, `changes`, `reviews`) for Issue #232 in `/home/azureuser/source/ama-demo-wt/feat-232-resident-wcag` on branch `feat/ux-232-resident-wcag` targeting `feat/demo-233-same-home-tensions-0825` (#1639) (caller prompt).
* Inspect neighbourhood housing officer, contact-centre, and resident engagement staff screens (`resident_choice_queue` / resident engagement views in `app.js`, `index.html`, `style.css` [caller wrote `styles.css`], `role-screens.js`, `panels.js`, `taskqueues.py`, and `projection.py`) and compare with `#228` and `#231` accessibility implementations (caller Requirement 1; `.copilot-tracking/research/2026-11-15/housing-resident-wcag-232-research.md`).
* Ensure all housing-officer, contact-centre, and resident-engagement queue/detail elements satisfy the WCAG 2.2 AA baseline (#151): explicit textual state meaning (no colour-only badges/status), semantic landmarks/headings/tables, keyboard focusability and operable controls, programmatic focus management, and `aria-live` status announcements without any resident contact trigger or role simulator (caller Requirement 2; `docs/reference/research/ux/wcag-conformance-baseline.md`).
* Add focused verification in `src/api/tests/test_housing_resident_wcag_232.py`, updating `src/api/pyproject.toml` mypy overrides only if needed (caller Requirement 3).
* Run the three required Focused-tier validation commands (`unittest` on `test_housing_resident_wcag_232.py` + `test_accessibility_baseline.py` + `test_content_standard.py`; `ruff check`, `ruff format --check`, and `mypy` in `src/api`; and `python3 tools/rename-zava-tests.py`), stage all implementation and `.copilot-tracking/` files, commit locally with exact title `feat(ux): add WCAG 2.2 keyboard jump nav, row headers and state cues for housing and resident screens (Refs #232)` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, fetch and rebase cleanly onto `origin/feat/demo-233-same-home-tensions-0825`, leave `git status --short` empty, exit `0`, and do NOT push (caller Requirements 1 and 2).

## Goals

* Provide complete, consistent route, landmark, table, focus, `aria-live`, and non-colour state-meaning parity across neighbourhood housing officer (`#/role/housing_officer`), contact-centre (`#/role/contact_centre`), resident engagement (`#/role/resident_engagement`), specialist screens (`resident-choice`, `resident-service-issues`), and the case workspace Resident panel (`residentPanel` / `actForm`).
* Preserve every repository safety, privacy, plain-language, design-system, and static/browser baseline invariant without adding outbound resident contact triggers, automatic consent inference, or role simulators.
* Prove behavior and regressions with deterministic, `sys.modules`-clean, strictly typed automated tests in `src/api/tests/test_housing_resident_wcag_232.py`.

## Scope and Non-Goals

### In Scope

* Route wiring for `#/role/contact_centre` -> `"resident-service-issues"` alongside `#/role/housing_officer` and `#/role/resident_engagement` in `src/api/src/zava_forward/api/web/app.js` and `src/api/src/zava_forward/api/web/role-screens.js`.
* Complete `aria-live="polite"` status attributes and `#workspace-status` lifecycle announcements (loading, screen chooser, invalid page, unavailable screen, record-ID mismatch, and settled screen/home state) plus single-lookup jump-link focus management in `src/api/src/zava_forward/api/web/role-screens.js`.
* Valid whitespace-free slugified HTML `id`/`for` attributes and explicit `type="button"` in `actForm`, plus a keyboard-focusable `.table-scroll[role="region"][aria-label="Resident decisions by measure"][tabindex="0"]` wrapper, `<th scope="row">` measure headers, and plain-language non-colour state cues in `residentPanel` in `src/api/src/zava_forward/api/web/panels.js`.
* Focused verification in `src/api/tests/test_housing_resident_wcag_232.py` covering static HTML/CSS/JS invariants, Node VM rendered DOM semantics/keyboard/focus/`aria-live` transitions across all three staff route perspectives and `residentPanel`, and Python core `resident_choice_queue` / default-deny / safeguarding role gates.
* Refreshed `web-design-guidelines` review, Focused-tier validation execution, `rpi-review` assessment, and local Git commit (`Refs #232`) with clean working tree.

### Non-Goals

* Outbound resident communications (SMS, email, letter, call triggers), resident-facing portal views (#154), or in-screen role simulators.
* Modifying gate/harness semantics, workflows, Dockerfiles, or pinned `style.css` `[tabindex="-1"]:focus` selectors asserted by sibling `#229`/`#231` WCAG suites (note: updating the hardcoded `[id="f-Raise a commitment-supplier"]` selector in `src/api/checks/case_journey_browser_check.py` to `#f-raise-a-commitment-supplier` is an immediately coupled selector alignment with `P02-T01` that preserves identical assertion semantics).
* Claiming human assistive-technology sign-off (#151, #155) or closing Issue #232 (`Closes #232` is forbidden while human AT validation remains open).
* Pushing commits to any remote or opening/updating a pull request.

## Functional Requirements

* FR-1: Navigating to `#/role/housing_officer`, `#/role/contact_centre`, or `#/role/resident_engagement` lazy-loads `/role-screens.js` (never `/ops.js`), marks `#nav a[href="#/screens"]` with `aria-current="page"`, resolves `#/role/housing_officer` and `#/role/contact_centre` to `resident-service-issues` and `#/role/resident_engagement` to `resident-choice`, honours `?case=` and `?page=`, and renders `role="alert"` `"Screen unavailable"` for unauthorized roles (such as `Contractor` or `Application Administrator`).
  * Observable acceptance criteria: Node VM routing tests verify all three `#/role/*` hashes, `?case=`/`?page=` propagation, `aria-current="page"`, `/ops.js` non-loading, and default-deny `role="alert"` behavior.
* FR-2: `roleScreensView()` and `screenTable()` emit polite live announcements across every screen state without altering the settled `#workspace-status` contract or out-of-scope specialist screens.
  * Observable acceptance criteria: When `!signal.aborted`, `#workspace-status` (`role="status" aria-live="polite" aria-atomic="true"`) updates on loading (`${role}. ${screen.title}. Loading recorded evidence.`), screen chooser (`${role}. Specialist screens. Choose a screen.` when `installed.length > 0`, or `${role}. Specialist screens. No specialist screens installed.` when `installed.length === 0`), invalid page (`${role}. Invalid screen page.`), unavailable screen (`${role}. Screen unavailable.`), and record mismatch (`${role}. ${screen.title}. Record mismatch.`), and settles to exact `"${role}. ${screen.title}. ${Selected home <id>.|No home selected.}"`; shared-host inline `role="status"` nodes (`role-screens.js` `screenTable` truncation, loading notice, and queue count) and all `role="status"` nodes rendered on `#232` screens (`resident-choice`, `resident-service-issues`) include `aria-live="polite"`.
* FR-3: Section jump links (`residentJumpNav` / `a[data-jump]`) and SPA route/home/reset transitions (`show()`) manage programmatic focus deterministically for keyboard users without trapping Tab/Shift+Tab or stealing focus from open chat widgets.
  * Observable acceptance criteria: Activating any `a[data-jump]` link calls `preventDefault()`, moves focus to the matching `<h2 id="...-heading" tabindex="-1">`, and calls `scrollIntoView({ block: "start" })`; route/home/reset navigation moves focus to `<main id="app" tabindex="-1">`.
* FR-4: `actForm` and `residentPanel` in `panels.js` provide valid programmatic form label bindings, keyboard-scrollable measure decision table semantics, and explicit plain-language textual state cues without colour-only indicators, banned jargon, resident contact triggers, or broken API/Playwright copy contracts.
  * Observable acceptance criteria: Every `<label for>` in `residentPanel` matches a unique whitespace-free control `id` (`actForm` IDs match `^[a-z0-9-]+$`); every `actForm` submit button sets `type="button"`; `Resident decisions by measure` is wrapped in `<div class="table-scroll" role="region" aria-label="Resident decisions by measure" tabindex="0">` with `<caption>`, `<th scope="col">`, and `<th scope="row">`; contractor readiness, measure answers, update commitments, and service/remedy items include textual state cues (`Confirmed`, `Waiting for resident`, `Action needed`) placed outside the contiguous `"Response: <status>. Owner: <name>."` and `"Remedy: <status>. Owner: <name>."` substrings required by `test_resident_api.py`.
* FR-5: Server-side `resident_choice_queue` and case projections preserve default-deny access (`STAFF_ROLES` only) and safeguarding redaction (`DEFAULT_REASON_ROLES` / `NOTE_HELD`), and specialist views render zero write controls, outbound message triggers, or role switchers.
  * Observable acceptance criteria: `test_housing_resident_wcag_232.py` proves `can_get(..., "resident_choice_queue")` allows staff roles, denies `Contractor` and `Application Administrator`, redacts adjustment reasons for unauthorized roles, and renders zero `<input>`, `<select>`, `<textarea>`, `<button>`, `<form>`, `mailto:`, `tel:`, or simulator controls inside `resident-choice` and `resident-service-issues`.

## Non-Functional Requirements

* NFR-1: Baseline guard and content-standard preservation.
  * Objective threshold or evaluation condition: `h("table", {}, ...)` count remains `14`, `aria-invalid` count remains `9`, bare `h("th", {}` count remains `0`, `position:fixed` count remains `2`, `role-screens.js` CSS classes remain documented in `docs/reference/research/ux/design-system.md`, and `test_content_standard.py` reports `0` banned jargon matches or em dashes across served web assets.
  * Operating condition or verification approach, if needed: Verified via `test_accessibility_baseline.py`, `test_content_standard.py`, `test_role_screens.py`, and `test_role_screens_conformance.py`.
  * Observable acceptance criteria: All baseline and conformance unit suites exit `0`.
* NFR-2: Static lint, format, strict type-checking, and test-isolation quality.
  * Objective threshold or evaluation condition: `0` `ruff check` errors, `0` `ruff format --check` diffs, `0` `mypy` errors under `strict = true` without adding permissive `pyproject.toml` overrides, `0` `sys.modules` mutations in `test_housing_resident_wcag_232.py`, and `0` migration regressions in `tools/rename-zava-tests.py`.
  * Operating condition or verification approach, if needed: Verified via the user-specified Focused-tier commands from repo root and `src/api`.
  * Observable acceptance criteria: All three user-specified validation commands exit `0`.

## Acceptance Criteria

* AC-1: `#/role/housing_officer`, `#/role/contact_centre`, and `#/role/resident_engagement` route cleanly through `app.js` and `role-screens.js` with `aria-current="page"`, `?case=`/`?page=` support, `/ops.js` isolation, and default-deny `"Screen unavailable"` `role="alert"` enforcement.
* AC-2: All housing-officer, contact-centre, and resident-engagement specialist queue/detail elements (`resident-choice`, `resident-service-issues`) and case workspace elements (`residentPanel`, `actForm`) expose explicit textual state meaning (`Confirmed`, `Waiting for resident`, `Action needed`, `Unknown`), semantic landmarks (`skip-link`, `main#app`, labelled `<nav>`, `role="region"` `.table-scroll`), heading hierarchy (`h1` -> `h2` -> `h3`), accessible tables (`<caption>`, `<th scope="col">`, `<th scope="row">`), whitespace-free `<label for>`/`id` pairs, programmatic focus (`main#app` and `<h2 tabindex="-1">`), and `aria-live="polite"` status announcements, with zero resident contact triggers or role simulators.
* AC-3: `src/api/tests/test_housing_resident_wcag_232.py` exists (maximum test file additions: `1`; test removals: `none`), exercises real `app.js`, `role-screens.js`, `panels.js`, `index.html`, `style.css`, `projection.py`, `store.py`, and `taskqueues.py` contracts (both positive semantic assertions and negative/sabotage regression checks), and passes strict `mypy` without loosening `src/api/pyproject.toml`.
* AC-4: All Focused-tier validation commands (`unittest`, `ruff check`, `ruff format --check`, `mypy`, `rename-zava-tests.py`), coupled WCAG/resident unit suites, and refreshed `web-design-guidelines` review pass cleanly.
* AC-5: All implementation files and dated `.copilot-tracking/` RPI artifacts are staged and committed locally on `feat/ux-232-resident-wcag` using privacy-safe GitHub noreply email, exact title `feat(ux): add WCAG 2.2 keyboard jump nav, row headers and state cues for housing and resident screens (Refs #232)`, and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, cleanly fetched and rebased onto `origin/feat/demo-233-same-home-tensions-0825`, and verified with `git status --short` empty without pushing.

## Test Ownership and Boundaries

* Canonical production and coupled harness targets:
  * `src/api/src/zava_forward/api/web/app.js`
  * `src/api/src/zava_forward/api/web/role-screens.js`
  * `src/api/src/zava_forward/api/web/panels.js`
  * `src/api/checks/case_journey_browser_check.py` (coupled `#f-raise-a-commitment-supplier` selector alignment for `P02-T01`)
* Read-only verified targets (expected unchanged unless implementation reveals a defect):
  * `src/api/src/zava_forward/api/web/index.html`
  * `src/api/src/zava_forward/api/web/style.css`
  * `src/core/src/zava_forward/core/projection.py`
  * `src/core/src/zava_forward/core/store.py`
  * `src/core/src/zava_forward/core/taskqueues.py`
  * `src/api/pyproject.toml`
* Test ownership:
  * Exact test removals: `none`
  * Maximum new test files: `1` (`src/api/tests/test_housing_resident_wcag_232.py`)
  * Semantic vs regression coverage: Semantic behavioral tests execute real `app.js`, `role-screens.js`, and `panels.js` in Node VM and real `Store`/`projection`/`taskqueues` in Python; regression guards verify HTML/CSS baseline selectors, banned jargon absence, exact table/header invariants, and `sys.modules` cleanliness.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-plan.md                                                                     |
| Phase details                    | .copilot-tracking/details/2026-11-15/housing-resident-wcag-232-phase-details.md                                                          |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/housing-resident-wcag-232-plan-critique.md (`Revise` resolved via direct planner dispositions `PC-001`..`PC-004`) |
| Relevant research                | .copilot-tracking/research/2026-11-15/housing-resident-wcag-232-research.md                                                              |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md is created by implementation as its evidence record            |
| Planning execution and readiness | Complete; Ready for implementation                                                                                                       |
| Continuation context             | Confirmed automatic RPI Agent session; parent continues to `rpi-implement` after critique disposition and readiness gates pass           |

## Sources

* `.copilot-tracking/research/2026-11-15/housing-resident-wcag-232-research.md`: Cycle 1 Wider/Deeper/Contrarian findings (`C1`–`C17`, `W1`) and Option B convergence decision.
* `docs/reference/research/ux/wcag-conformance-baseline.md`: WCAG 2.2 AA engineering baseline (#151) and honest assistive-technology boundary.
* `docs/reference/research/ux/design-system.md`: Fluent 2 token and documented component class inventory enforced by `test_role_screens.py`.
* `docs/reference/research/ux/content-standard.md`: Plain-language copy standard enforced by `test_content_standard.py`.
* `docs/prds/zava-forward-retrofit-programme-demonstrator.md`: FR-055 housing officer, contact-centre officer, and resident engagement workbench boundaries.
* `src/api/tests/test_housing_resident_screen_wcag.py`, `src/api/tests/test_procurement_screen_wcag.py`, and `src/api/tests/test_technical_quality_screens_wcag.py`: Peer WCAG 2.2 AA test harnesses (`#228`, `#231`, `#232`) and pinned CSS/DOM invariants.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Complete Staff Route, Live-Status, and Focus Parity in Web Host

* Intent: Wire `#/role/contact_centre` alongside `#/role/housing_officer` and `#/role/resident_engagement`, complete polite `aria-live` status announcements across `roleScreensView()` and `screenTable()`, and tighten jump-link heading focus lookup without breaking settled `#workspace-status` or static guards.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add `#/role/contact_centre` route support in `app.js` and `role-screens.js`

* Requirement and evidence: FR-1, AC-1; research `C1`, `C2`, `C15` (`app.js:370-376`, `role-screens.js:91-96`, PRD line 822).
* Expected result: `isRoleScreensDestination(raw)` strips `?query` across all role hashes and returns `true` for `#/role/contact_centre` (including query suffixes), and `ROLE_HASH_SCREENS["#/role/contact_centre"]` maps to `"resident-service-issues"` via `Object.hasOwn`, preserving `aria-current="page"`, `/ops.js` non-loading, and default-deny `"Screen unavailable"` alerts.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/housing-resident-wcag-232-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Complete `aria-live="polite"` announcements and jump-heading focus in `role-screens.js`

* Requirement and evidence: FR-2, FR-3, AC-2; research `C4`, `C6`, `C13` (`role-screens.js:51,99-186,304-311`, `specialist_keyboard_browser_check.py:68-70`).
* Expected result: Shared-host inline `role="status"` elements (`screenTable` truncation at line 51, loading state at line 129, queue count at line 145) and rendered `#232` screens include `"aria-live": "polite"`; `roleScreensView()` guards `!signal.aborted` and updates `#workspace-status` across loading, chooser (branched on `installed.length`), invalid-page, unavailable-screen, and record-ID mismatch states while keeping the settled `${role}. ${screen.title}. ${Selected home X.|No home selected.}` announcement unchanged; `a[data-jump]` resolves the target heading once before `.focus()` and `.scrollIntoView({ block: "start" })`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/housing-resident-wcag-232-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Upgrade Housing and Resident Case Panel Accessibility in `panels.js`

* Intent: Eliminate invalid space-containing HTML control IDs in `actForm` and bring `residentPanel` (`Resident decisions by measure`, contractor fallback, update commitment, and service/remedy states) to full WCAG 2.2 AA table, keyboard-region, and textual state-meaning parity within all counted and lexical guards.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Slugify `actForm` field IDs and set explicit button `type="button"` in `panels.js`

* Requirement and evidence: FR-4, AC-2; research `C8` (`panels.js:43-64`).
* Expected result: `actForm` generates deterministic, lowercase hyphen-slugified HTML5 `id` and `<label for>` attributes with zero whitespace (plus unique disambiguation if needed) and sets `type: "button"` on the manual submission button while preserving `aria-invalid` count `== 9` and all `test_case_journey.py` interactions.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/housing-resident-wcag-232-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Add keyboard-scrollable table region, `<th scope="row">`, and textual state cues in `residentPanel`

* Requirement and evidence: FR-4, NFR-1, AC-2; research `C9`, `C14`, `C16` (`panels.js:169-290`, `test_accessibility_baseline.py`, `test_content_standard.py`, `test_resident_api.py`).
* Expected result: `Resident decisions by measure` is wrapped in `<div class="table-scroll" role="region" aria-label="Resident decisions by measure" tabindex="0">` (keeping `h("table", {}, ...)` count `== 14`), uses `h("th", { scope: "row" }, ...)` for measure names, keeps helpers locally scoped inside `actForm`/`residentPanel` to preserve `test_case_journey.py` slice anchors, and surfaces plain-language state cues (`Confirmed`, `Waiting for resident`, `Action needed`) across contractor readiness, measure answers, update commitment status, and service/remedy items without using banned jargon words or breaking contiguous `"Response: <status>. Owner: <name>."` / `"Remedy: <status>. Owner: <name>."` substrings.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/housing-resident-wcag-232-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Focused WCAG 2.2 Verification, Web Guidelines Audit, and Local Validation

* Intent: Author `src/api/tests/test_housing_resident_wcag_232.py`, audit changed web files against refreshed Web Interface Guidelines, run all Focused-tier and coupled validation commands, and verify zero regressions.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Create `src/api/tests/test_housing_resident_wcag_232.py` covering routes, semantics, state text, keyboard/focus, `aria-live`, and safety boundaries

* Requirement and evidence: FR-1 through FR-5, NFR-1, NFR-2, AC-3; research `C1`–`C17`.
* Expected result: `src/api/tests/test_housing_resident_wcag_232.py` provides comprehensive, strictly typed, `sys.modules`-clean verification across `app.js`, `role-screens.js`, `panels.js`, `index.html`, `style.css`, `projection.py`, `store.py`, and `taskqueues.py`, including Unicode-unmasked (`ensure_ascii=False`) rendered text checks, `section#screen-evidence` `aria-label="Evidence for <id>"` region preservation, negative/unauthorized role tests, and zero outbound contact or simulator controls.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/housing-resident-wcag-232-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Refresh Web Interface Guidelines, execute Focused-tier and coupled test suites, and reconcile implementation evidence

* Requirement and evidence: NFR-1, NFR-2, AC-4; AMA Web Development Guidance (`W1`) and caller Requirement 4.
* Expected result: Refreshed `web-design-guidelines` review reports zero open findings across `app.js`, `role-screens.js`, and `panels.js`; all three required Focused validation commands, coupled resident/WCAG suites (`ZF_RESIDENT_BROWSER=1`), and Playwright + pinned axe 4.10.3 `232`/`232s` scans exit `0`; `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md` records complete implementation and validation evidence.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/housing-resident-wcag-232-phase-details.md

## Dependencies

* Node.js (`node`) and Python 3 (`unittest`, `ruff`, `mypy`) in local environment: required to execute Node VM DOM harnesses, static guards, linters, type-checkers, and `tools/rename-zava-tests.py`.
* Existing static and copy guards (`test_accessibility_baseline.py`, `test_content_standard.py`, `test_role_screens.py`, `test_role_screens_conformance.py`): constrain table counts, `th` scopes, CSS classes, and plain-language vocabulary.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Single-pass `rpi-plan-critique` (`PC-001`, High) | Applied directly (`planner`) | Updated `What You May Not Know`, `FR-4`, `P02-T02`, and `P03` so `residentPanel` prepends state cues outside the contiguous `"Response: <status>. Owner: <name>."` and `"Remedy: <status>. Owner: <name>."` substrings required by `test_resident_api.py:875-916`, added a direct Node VM regression assertion in `P03-T01`, and included `test_resident_api.py` (`ZF_RESIDENT_BROWSER=1` when Playwright Chromium is available) in `P03-T02`. |
| Single-pass `rpi-plan-critique` (`PC-002`, High) | Applied directly (`planner`) | Scoped `FR-2`, `P01-T02`, and `P03-T01` `role="status"` `aria-live="polite"` requirements to the shared specialist-screen host (`role-screens.js:51,129,145`) and rendered `#232` screens (`resident-choice`, `resident-service-issues`) without touching out-of-scope specialist screens, branched `!screen` `#workspace-status` text on `installed.length`, and guarded `!signal.aborted`. |
| Single-pass `rpi-plan-critique` (`PC-003`, Medium) | Applied directly (`planner`) | Recorded the caller-mandated commit subject `feat(ux): add WCAG 2.2 keyboard jump nav, row headers and state cues for housing and resident screens (Refs #232)` and post-review `git fetch origin feat/demo-233-same-home-tensions-0825` + clean rebase onto `origin/feat/demo-233-same-home-tensions-0825` in `User Decisions and Requirements`, `AC-5`, and `P03-T02`. |
| Single-pass `rpi-plan-critique` (`PC-004`, Low) | Applied directly (`planner`) | Specified `split("?")[0]` query-suffix normalization across all role hashes in `isRoleScreensDestination` (`P01-T01`) and local helper scoping inside `actForm` and `residentPanel` preserving `test_case_journey.py:698-706,990` slice anchors (`P02-T01`, `P02-T02`). |

## Follow-Up Items

* Complete human assistive-technology (NVDA, JAWS, VoiceOver) and 360px mobile walkthroughs across `#/role/housing_officer`, `#/role/contact_centre`, `#/role/resident_engagement`, and `#/case/<id>?tab=resident` before closing Issue #232 — outside immediate automated engineering scope under #151 and #155; owned by human accessibility reviewer.
* Reconcile parent-branch `resident-service-issues` (`Routes to ask` region) declaration in `src/api/checks/specialist_keyboard_browser_check.py` in a dedicated full-tier gate-tool PR — outside Focused-tier non-gate scope per AMA validation policy (#1294); owned by harness maintainer.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: None
