<!-- markdownlint-disable-file -->
# RPI Plan: Housing Officer and Resident Engagement Screens WCAG 2.2 Conformance (#232)

## Task Metadata

* Task ID: 232-housing-resident-screens-wcag
* Task slug: housing-resident-screens-wcag-232
* Planning status: Implemented — ready for review
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/housing-resident-screens-wcag-232-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/housing-resident-screens-wcag-232-plan-critique.md

## Executive Summary

This plan delivers the focused code-testable WCAG 2.2 accessibility increment for GitHub issue #232 across the Housing Officer (`#/role/housing_officer`, backed by `resident-service-issues`) and Resident Engagement (`#/role/resident_engagement`, backed by `resident-choice`) screens in `src/api`. It wires both `#/role/*` routes across all four `#/screens` route/script/nav checks in `app.js` and `role-screens.js`, completes keyboard-operable section jump navigation (`role="navigation"`, `aria-label`, and `Go to ...` links covering rendered `<section>` landmarks in both record and host/portfolio states with `<h2 tabindex="-1">` focus targets, programmatic focus visibility, and `scrollIntoView`), pairs every status badge, resident choice/readiness cell, pause/withdrawal state, update commitment row, redress/history step, and safe-route indicator with explicit plain-language textual state cues so state is never conveyed by colour alone, and verifies everything in `src/api/tests/test_housing_resident_screen_wcag.py` without `sys.modules` deletion hazards.

### User Decisions and Requirements Highlights

* Wire and harden both `#/role/housing_officer` and `#/role/resident_engagement` so each exposes a keyboard-operable section jump navigation (`role="navigation"`, `aria-label`) with `Go to ...` links for every section landmark and moves focus to the target heading (`tabindex="-1"`) on activation.
* Pair every status badge, resident choice indicator, pause/withdrawal state, update commitment row, and safe-route indicator on both views with an explicit plain-language textual state cue (`State:` / `Meaning:` / `Confirmed:` / `Waiting for resident:` / `Action needed:`) compliant with the plain-language content standard (#153).
* Add focused conformance tests in `src/api/tests/test_housing_resident_screen_wcag.py` with zero `sys.modules` deletions, validate under the focused tier (`unittest`, `mypy`, `ruff`), record dated RPI artifacts under `.copilot-tracking/{research,plans,details,changes,reviews}/2026-11-15/`, and commit locally with `Refs #232` without pushing.

### What You May Not Know

* **Design-system CSS class gate**: `src/api/tests/test_design_system.py` and `src/api/tests/test_role_screens.py` require every CSS class token used in `role-screens.js` to be documented in `docs/reference/research/ux/design-system.md` (`.muted` is in `style.css` for `app.js` but not documented for `role-screens.js`). Expressing textual state cues with explicit `State:` / `Meaning:` plain-language prefixes, documented classes (`flag`, `screen-links`, `screen-record`), and primary-contrast `<span data-state-cue="...">` siblings keeps the increment strictly inside `src/api` while passing all design-system checks.
* **Choice-before-capacity ordering invariant**: `src/api/tests/test_role_screens.py` verifies that the words `capacity`, `utilisation`, and `headroom` never appear in any node (including top jump-navigation links) before the `"Choice comes before offered capacity"` section on `resident-choice`. Jump-link labels for the trailing policy/tension sections therefore use concise plain-language labels (`"Go to Choice precedence rule"` and `"Go to Design tension on resident choice"`), matching `hazardJump` in `role-screens.js`.
* **Optional landmark anchors and summary anchor-count invariants**: Sibling conformance tests (`test_assessor_screen_wcag.py`) assert a strict bijection between `<nav>` jump links and `<section id>` landmarks on `technical-queue`, `test_resident_choice_screen.py` asserts `len(anchors_of(tree)) == 1` on `resident-choice.overview()` (and `0` on invalid pages), and `test_role_screens_stage_map_focus.py` forbids `tabindex` inside `journeyStageMap`. Keeping `screenTension` as a `const` arrow function (`const screenTension = (kind, anchor = null) => ...`) preserves the exact `screenTension(` match count (`5`) in `test_role_screens_tensions_same_home.py`, anchoring portfolio sections without adding anchors inside `resident-choice.summary()` preserves the CSV anchor-count contract, and rendering workspace-level jump navigation in `roleScreensView()` alongside record-level `residentJumpNav()` inside `render(c)` provides keyboard jump navigation in both unselected-home and selected-home states.
* **Web Development Guidance skill compliance**: Per `.github/copilot-instructions.md`, `redesign-existing-projects`, `accessibility`, and `web-design-guidelines` (fetched from `vercel-labs/web-interface-guidelines`) govern existing-app web edits; `web-design-guidelines` will be refreshed before `rpi-review` with `file:line` compliance reporting while preserving Zava North Homes' Fluent 2 (#150), WCAG 2.2 (#151), and plain-language (#153) standards.

### Unresolved Decisions or Blockers

* None. Live assistive-technology (screen-reader) and real-device verification remain tracked as manual acceptance work under #151 and #155, which is why the commit references `Refs #232` rather than closing #232.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`rpi-research` -> `rpi-plan` -> `rpi-plan-critique` -> `rpi-implement` -> `rpi-review`) in worktree `/home/azureuser/source/ama-demo-wt/feat-232-housing-res-wcag` on branch `feat/ux-232-housing-res-wcag` targeting `feat/demo-233-same-home-tensions-0825` (caller prompt).
* Deliver a clean, focused, local-testable increment in `src/api` addressing the remaining WCAG 2.2 baseline (#151) code-testable criterion of issue #232 (caller prompt; GitHub issue #232).
* Ensure Housing Officer (`#/role/housing_officer`) and Resident Engagement (`#/role/resident_engagement`) screens in `src/api/src/zava_forward/api/web/role-screens.js` and `app.js` expose keyboard-operable section jump navigation (`role="navigation"`, `aria-label`) with `Go to ...` links for every section landmark, focusing target headings (`tabindex="-1"`) on click/activation (caller prompt).
* Ensure every status badge, resident choice indicator, pause/withdrawal state, update commitment row, and safe-route indicator on both views pairs its badge/colour with an explicit plain-language textual state cue (`State:` / `Meaning:` text or state-cue markup) so state is never conveyed by colour alone, preserving Fluent 2 (#150), WCAG 2.2 (#151), and plain-language content rules (#153) without adding resident contact controls (#154) (caller prompt; `.github/copilot-instructions.md`).
* Add focused unit tests in `src/api/tests/test_housing_resident_screen_wcag.py` without `sys.modules` deletion hazards (caller prompt).
* Validate with focused `unittest` (`test_*housing*.py` and `test_role_screens_conformance.py` plus directly coupled resident/role-screen suites), `python3 -m mypy`, and `python3 -m ruff check . && python3 -m ruff format --check .` in `src/api` (caller prompt).
* Write all dated RPI artifacts under `.copilot-tracking/{research,plans,details,changes,reviews}/2026-11-15/` and commit all changes and `.copilot-tracking/` artifacts cleanly with `Refs #232` and the Copilot trailer; do NOT push (caller prompt).

## Goals

* Connect `#/role/housing_officer` (`resident-service-issues`) and `#/role/resident_engagement` (`resident-choice`) in the workbench router and specialist screen host so direct route navigation loads `/role-screens.js` and opens the matching view.
* Guarantee complete 1-to-1 keyboard jump navigation (`<nav role="navigation" aria-label="...">` with `Go to ...` anchor links) and labelled `<section>` landmarks with focusable `<h2 tabindex="-1">` headings across both summary and selected-home states on both screens.
* Eliminate colour-only or ambiguous raw-code state presentation across all status badges, choice/readiness indicators, paused/withdrawn records, update commitments, redress/history rows, and safe-route references on both views.
* Prove route wiring, landmark bijection, heading focus behaviour, and non-colour textual state cues in a `sys.modules`-safe unit test suite (`src/api/tests/test_housing_resident_screen_wcag.py`) with zero regressions across existing suites, `mypy`, and `ruff`.

## Scope and Non-Goals

### In Scope

* Route-alias recognition (`isRoleScreensHash`) across all four `#/screens` checks in `src/api/src/zava_forward/api/web/app.js` (contractor `/ops.js` exclusion, `/role-screens.js` lazy load, `#nav` `aria-current="page"` + `me.navigation` lookup, and `roleScreensView()` dispatch) and default screen selection in `src/api/src/zava_forward/api/web/role-screens.js` (with zero top-level identifier collisions between `app.js` and `role-screens.js`).
* Upgrading `residentJumpNav`, optional `anchor` support on `const screenTension` and `const screenWithheld`, host-level workspace jump navigation in `roleScreensView()` plus 1-to-1 record-level section landmark anchoring across `resident-choice` and `resident-service-issues`, delegated `scrollIntoView({ block: "nearest" })` on `a[data-jump]` activation, and programmatic `[tabindex="-1"]:focus` outline + `scroll-margin-top` rules in `src/api/src/zava_forward/api/web/style.css`.
* Plain-language textual state cues (`State:` / `Meaning:` / `Confirmed:` / `Waiting for resident:` / `Action needed:` plus `data-state-cue` attributes) on every status badge, measure choice/readiness cell, paused/withdrawn row, update commitment row, safe-route indicator, redress formal-route cell, response history step, and summary queue row on both views.
* Focused automated conformance tests in `src/api/tests/test_housing_resident_screen_wcag.py` (max 1 new test file; exact test removals: `none`).

### Non-Goals

* Modifying `docs/` files, backend API schemas, SQL stores, or unrelated role screens' rendered DOM.
* Adding any interactive form controls (`<button>`, `<form>`, `<input>`, `<select>`, `<textarea>`) or resident contact/messaging actions (#154) to `resident-choice` or `resident-service-issues`.
* Mutating or deleting entries in `sys.modules` in any test.
* Claiming live screen-reader / assistive-technology acceptance (#151/#155) or pushing commits to `origin`.

## Functional Requirements

* **FR-01 — Role Route Dispatch**: Navigating to `#/role/housing_officer` or `#/role/resident_engagement` (with optional `?case=` / `?page=` parameters) skips contractor `/ops.js` loading, loads `/role-screens.js`, normalizes `#nav` active destination to `#/screens` (`aria-current="page"` and `workspaceStatus` scope), and renders `resident-service-issues` for `#/role/housing_officer` and `resident-choice` for `#/role/resident_engagement` when `screen=` is not explicitly overridden.
  * Observable acceptance criteria: `missingWorkspaceScripts("#/role/housing_officer", false)` and `missingWorkspaceScripts("#/role/resident_engagement", false)` require `/role-screens.js` without requiring `/ops.js` for contractors, `#nav` marks `#/screens` `aria-current="page"`, and `roleScreensView()` selects `resident-service-issues` and `resident-choice` respectively.
* **FR-02 — Complete Keyboard Jump Navigation & Section Landmarks**: In `render(case)` (populated and empty/partial cases), both `resident-choice` and `resident-service-issues` render `<nav role="navigation" aria-label="Sections of this view" class="screen-links">` containing `<a href="#<id>-heading" data-jump="<id>-heading">Go to ...</a>` links in exact 1-to-1 correspondence with every record `<section id="<id>" aria-labelledby="<id>-heading">` landmark and its `<h2 id="<id>-heading" tabindex="-1">` heading; at the `roleScreensView()` host shell level on both views, `<nav role="navigation" aria-label="Workspace sections" class="screen-links">` exposes `Go to ...` links to `#screen-queue-heading`, portfolio `<section>` headings (`#choice-portfolio-heading`, `#choice-portfolio-withheld-heading`, `#service-portfolio-heading`), and `#screen-evidence-heading` without adding extra anchors inside `resident-choice.summary()` or adding `tabindex` inside `journeyStageMap`.
  * Observable acceptance criteria: In every rendered record state (`resident-choice` populated & empty; `resident-service-issues` with/without `redress_route` and `history`), `nav` has `role="navigation"` and non-empty `aria-label`, every link starts with `"Go to "`, zero `<button>` elements exist, and link targets equal the exact set of record `<section>` heading IDs (`tabindex="-1"`); full `roleScreensView()` renders on `#/role/housing_officer` and `#/role/resident_engagement` expose workspace jump links to queue, portfolio, and selected-home headings while keeping `resident-choice.overview()` anchor count at `1` (`0` on invalid pages).
* **FR-03 — Keyboard/Click Heading Focus Activation**: Activating any `a[data-jump]` jump link calls `preventDefault()`, focuses the target `<h2 tabindex="-1">` element, and scrolls it into view (`block: "nearest"`), while `style.css` applies the Fluent focus ring to `[tabindex="-1"]:focus` and `scroll-margin-top` to `.screen-record h2, [tabindex="-1"]`.
  * Observable acceptance criteria: Dispatching a click event on a rendered `a[data-jump]` link calls `preventDefault()`, calls `.focus()` and `.scrollIntoView({ block: "nearest" })` on the matching heading element, and `style.css` includes `[tabindex="-1"]:focus` and `scroll-margin-top` without CSS transitions/animations or raw hex literals.
* **FR-04 — Explicit Plain-Language Textual State Cues**: Every status badge (`.flag.danger`, `.flag`), resident choice status and readiness cell, paused/withdrawn row, linked update commitment row, safe-route indicator (`safe_contact_ref` present or missing), redress reviewable/formal-route status, response history step state, and summary status cell on Housing Officer and Resident Engagement views includes an explicit plain-language textual state cue (`State:` / `Meaning:` / `Confirmed:` / `Waiting for resident:` / `Action needed:`).
  * Observable acceptance criteria: Automated tests verify explicit textual state cues across every listed indicator (including safe-route recorded vs unrecorded and `Object.prototype` key edge cases like `constructor`/`toString`) while preserving all existing plain-language and substring contracts.

## Non-Functional Requirements

* **NFR-01 — Design-System, Content-Standard, and Read-Only Conformance**: Zero undocumented CSS classes, zero banned glossary words (`gate(s)`, `hold(s)`, `provenance`, `trace(s)`, `snapshot(s)`, `envelope(s)`), zero inline styles/handlers/timers/extra `fetch` calls, and unchanged table counts and control-free read-only trees.
  * Objective threshold or evaluation condition: 100% pass across `test_role_screens_conformance.py`, `test_design_system.py`, `test_content_standard.py`, `test_accessibility_baseline.py`, `test_role_screens.py`, `test_role_screens_tensions_same_home.py`, `test_connected_home_check.py`, `test_resident_choice_screen.py`, `test_resident_service_screen.py`, `test_resident_screen_wcag.py`, and `test_frontline_screen_wcag.py`.
  * Operating condition or verification approach: Run `unittest` suites in `src/api`.
  * Observable acceptance criteria: Zero failures or errors across all conformance and regression suites.
* **NFR-02 — Test Isolation, Static Typing, and Formatting**: New test module `src/api/tests/test_housing_resident_screen_wcag.py` mutates zero `sys.modules` entries and passes strict `mypy` and `ruff`.
  * Objective threshold or evaluation condition: Zero `sys.modules` deletions/assignments in `test_housing_resident_screen_wcag.py`; `mypy`, `ruff check .`, and `ruff format --check .` exit `0`.
  * Operating condition or verification approach: Static check + `python3 -m mypy` + `python3 -m ruff check . && python3 -m ruff format --check .` in `src/api`.
  * Observable acceptance criteria: Clean `0` exit codes on all commands.

## Acceptance Criteria

* `#/role/housing_officer` and `#/role/resident_engagement` load `/role-screens.js` via `app.js` and render `resident-service-issues` and `resident-choice` respectively via `roleScreensView()`.
* Both views expose `<nav role="navigation" aria-label="...">` with `Go to ...` links matching 100% of rendered `<section>` landmarks (`id`, `aria-labelledby`), and activating any jump link focuses its target `<h2 tabindex="-1">`.
* Every status badge, resident choice/readiness indicator, pause/withdrawal state, update commitment row, redress/history state, and safe-route indicator on both views pairs visual presentation with explicit plain-language state text (`State:` / `Meaning:` / `Confirmed:` / `Waiting for resident:` / `Action needed:`).
* `src/api/tests/test_housing_resident_screen_wcag.py` covers semantic behaviour (route resolution, landmark/jump-nav bijection across populated/empty/summary states, click-to-heading focus activation, and state cues across all indicators) with zero `sys.modules` mutations, exact test removals = `none`, and max 1 new test file.
* Focused validation (`unittest`, `mypy`, `ruff check`, `ruff format --check`) passes 100% in `src/api`, dated RPI artifacts exist under `.copilot-tracking/{research,plans,details,changes,reviews}/2026-11-15/`, and changes are committed locally on `feat/ux-232-housing-res-wcag` with `Refs #232` without pushing.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/housing-resident-screens-wcag-232-plan.md                                                             |
| Phase details                    | .copilot-tracking/details/2026-11-15/housing-resident-screens-wcag-232-phase-details.md                                                  |
| Latest critique                  | .copilot-tracking/reviews/2026-11-15/housing-resident-screens-wcag-232-plan-critique.md (`Verdict: Revise`; all 6 planner-owned findings `PC-001`..`PC-006` applied and closed) |
| Relevant research                | .copilot-tracking/research/2026-11-15/housing-resident-screens-wcag-232-research.md                                                      |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/housing-resident-screens-wcag-232-changes.md is created by implementation as its evidence record    |
| Planning execution and readiness | Ready — single-pass `rpi-plan-critique` completed and all findings (`PC-001`..`PC-006`) incorporated; ready for automatic `Implement`    |
| Continuation context             | Confirmed automatic RPI Agent parent return; transitions automatically to `Implement`                                                    |

## Sources

* .copilot-tracking/research/2026-11-15/housing-resident-screens-wcag-232-research.md: Verified codebase evidence `C1`-`C12` and external Web Interface Guidelines `W1`.
* src/api/src/zava_forward/api/web/role-screens.js: Specialist screen host, `screenPanel`, `residentJumpNav`, `stateCue`, `resident-choice`, `serviceMeaning`, `redressRoutePanel`, and `resident-service-issues`.
* src/api/src/zava_forward/api/web/app.js: Hash router (`route`) and lazy script loader (`missingWorkspaceScripts`).
* src/api/src/zava_forward/api/web/style.css: Fluent 2 tokens, `.screen-links`, and `.screen-record h2:focus` rules.
* docs/reference/research/ux/wcag-conformance-baseline.md, docs/reference/research/ux/design-system.md, and docs/reference/research/ux/content-standard.md: WCAG 2.2 AA (#151), Fluent 2 (#150), and plain-language glossary (#153) constraints.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Wire role routes, complete section landmarks, and harden keyboard jump navigation

* Intent: Connect `#/role/housing_officer` and `#/role/resident_engagement` in `app.js` and `role-screens.js`, anchor every `<section>` landmark across both screens (`render` and `summary`), and expose `<nav role="navigation" aria-label="...">` with `Go to ...` links focusing `<h2 tabindex="-1">` headings.
* Dependencies: None.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Wire `#/role/housing_officer` and `#/role/resident_engagement` route dispatch and script loading

* Requirement and evidence: FR-01; `C1`, `C2`, `C3` in .copilot-tracking/research/2026-11-15/housing-resident-screens-wcag-232-research.md.
* Expected result: `app.js` loads `/role-screens.js` and calls `roleScreensView()` for `#/role/housing_officer` and `#/role/resident_engagement`, highlighting `#/screens` in `#nav`, and `roleScreensView()` defaults those routes to `resident-service-issues` and `resident-choice` respectively while preserving `?case=` / `?page=` parameters and canonical `screenHref` links.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/housing-resident-screens-wcag-232-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Complete `residentJumpNav` (`role="navigation"`, `Go to ...`) and 1-to-1 `<section>` landmarks with `tabindex="-1"` headings

* Requirement and evidence: FR-02, FR-03; `C1`, `C2`, `C4`, `C5`, `C7`, `C10`, `C11`, `W1` in .copilot-tracking/research/2026-11-15/housing-resident-screens-wcag-232-research.md.
* Expected result: `residentJumpNav` emits `role="navigation"`, `aria-label`, and `Go to ...` links matching every rendered `<section id aria-labelledby>` landmark and `<h2 id tabindex="-1">` heading across `resident-choice` and `resident-service-issues` (`render` and `summary`), keeping choice-before-capacity label rules and sibling screen landmarks intact, with `scroll-margin-top` on `.screen-record h2` in `style.css`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/housing-resident-screens-wcag-232-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Add explicit plain-language textual state cues across all indicators

* Intent: Pair every status badge, resident choice/readiness indicator, pause/withdrawal row, update commitment row, redress/history state, and safe-route indicator on Housing Officer and Resident Engagement views with explicit plain-language textual state cues without undocumented CSS classes or banned glossary terms.
* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add plain-language textual state cues (`State:` / `Meaning:` / `stateCue`) and `data-state-cue` markers across `resident-choice`, `resident-service-issues`, and queue/header badges

* Requirement and evidence: FR-04, NFR-01; `C5`, `C6`, `C8`, `C9`, `C11`, `C12` in .copilot-tracking/research/2026-11-15/housing-resident-screens-wcag-232-research.md.
* Expected result: Safe-route references (`safeRouteCue`), measure readiness (`readinessCue`), paused/withdrawn status cells, redress reviewable & formal-route status (`formalRouteCue`), response history steps (`serviceMeaning`), summary rows, and `.flag` / `.flag.danger` badges on both views carry explicit plain-language state cues while preserving every existing substring and CSS inventory test.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/housing-resident-screens-wcag-232-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Add focused WCAG 2.2 conformance unit tests and run focused validation

* Intent: Author `src/api/tests/test_housing_resident_screen_wcag.py` (without `sys.modules` deletion) covering semantic route, jump-nav, landmark, heading-focus, and textual-state conformance, and verify all focused unit, conformance, typing, and lint gates.
* Dependencies: P01, P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Create `src/api/tests/test_housing_resident_screen_wcag.py` and pass focused `unittest`, `mypy`, and `ruff` checks

* Requirement and evidence: FR-01..FR-04, NFR-01, NFR-02; `C8`-`C12` in .copilot-tracking/research/2026-11-15/housing-resident-screens-wcag-232-research.md.
* Expected result: `test_housing_resident_screen_wcag.py` verifies `#/role/housing_officer` and `#/role/resident_engagement` routing, `role="navigation"` jump links (`Go to ...`) and 1-to-1 section/heading focus targets (`tabindex="-1"`), click-to-focus activation, and explicit textual state cues across all indicators with zero `sys.modules` mutations; focused `unittest`, `mypy`, and `ruff` exit `0`.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/housing-resident-screens-wcag-232-phase-details.md

## Dependencies

* Node.js runtime (`node` on `PATH`): Required by existing and new Python `unittest` suites in `src/api/tests/` to execute `app.js` and `role-screens.js` inside `node:vm` contexts.
* Sibling worktree Python packages (`PYTHONPATH=src:.:../core/src:../agents/src:../core/tests:../agents/tests` when running multi-module discovery in `src/api`): Ensures tests resolve this worktree's `zava_forward.api`, `core`, and `agents` packages cleanly without `sys.modules` manipulation.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Single-pass critique (`PC-001`, High — helper signatures and already-present state cues in `role-screens.js`) | Accepted and applied | Updated `P02-T01` in phase details to use actual two/three-arg `stateCue(table, status, detail)` and `serviceStatus({ status })` signatures, preserve already-present cues in `Paused or withdrawn by the resident`, `redressRoutePanel.reviewable_decisions`, and `serviceQueueRow` open issues, and add `safeRouteCue`, `readinessCue`, `formalRouteCue`, `serviceStatus` on `Response history`, unavailable/empty cues, and sibling `State:` cues on `.flag.danger`/`.flag`. |
| Single-pass critique (`PC-002`, High — `resident-choice.overview()` single-anchor invariant and host/portfolio jump nav) | Accepted and applied | Updated FR-02 and `P01-T02` so `resident-choice.summary()` keeps its exact single CSV download anchor (`0` on invalid pages) with inline `screenPanel` titles (`choice-portfolio`, `choice-portfolio-withheld`), while `roleScreensView()` renders host-level `<nav role="navigation" aria-label="Workspace sections">` jump links to queue, portfolio, and selected-home `<h2 tabindex="-1">` headings without adding `tabindex` inside `journeyStageMap`. |
| Single-pass critique (`PC-003`, Medium — `screenTension(` declaration token count = `5`) | Accepted and applied | Kept `const screenTension = (kind, anchor = null) => ...` arrow-expression form in `P01-T02` so `re.findall(r"screenTension\(", SCREENS)` remains `5` (`test_role_screens_tensions_same_home.py`). |
| Single-pass critique (`PC-004`, Medium — `scrollIntoView` and programmatic `[tabindex="-1"]:focus` outline) | Accepted and applied | Updated FR-03 and `P01-T02` after direct inspection of `role-screens.js`, `app.js`, and `style.css`: keep `'closest?.("a[data-jump]")'` and `"event.preventDefault();\n    document.getElementById"` literal substrings for `test_asset_exec_screen_wcag.py` while adding `scrollIntoView?.({ block: "nearest" })`, `[tabindex="-1"]:focus` focus ring using Fluent tokens, and `scroll-margin-top: var(--sp-4)`. |
| Single-pass critique (`PC-005`, Medium — complete 4-point route normalization in `app.js`) | Accepted and applied | Updated FR-01 and `P01-T01` to apply `isRoleScreensHash` across all four `#/screens` checks in `app.js` (contractor `/ops.js` exclusion, `/role-screens.js` lazy load, `#nav` active-link normalization, and `roleScreensView()` route dispatch) with zero global identifier collisions with `role-screens.js`. |
| Single-pass critique (`PC-006`, Low — Web Development Guidance skill governance & strict `mypy`) | Accepted and applied | Recorded `redesign-existing-projects`, `accessibility`, and `web-design-guidelines` governance in plan and phase details (with fresh `web-design-guidelines` fetch and `file:line` review in `rpi-review`) and strict `mypy` annotations on all `test_housing_resident_screen_wcag.py` helpers. |

## Follow-Up Items

* Manual assistive-technology (NVDA/JAWS/VoiceOver) and 360px real-device walkthrough for `#/role/housing_officer` and `#/role/resident_engagement` — outside automated code-increment scope per #151 and #155; required before ticking the final closure box on issue #232.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/housing-resident-screens-wcag-232-changes.md
* Ready phase or task: Complete (`P01`, `P02`, `P03` checked; ready for `rpi-review`)
* Remaining provisional question or blocker: None
