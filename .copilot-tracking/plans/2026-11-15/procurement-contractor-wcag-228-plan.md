<!-- markdownlint-disable-file -->
# RPI Plan: Issue #228 Procurement and Contractor WCAG 2.2 Keyboard Jump Nav, Landmarks, and Textual State Signals

## Task Metadata

* Task ID: issue-228-procurement-wcag
* Task slug: procurement-contractor-wcag-228
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/procurement-contractor-wcag-228-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/procurement-contractor-wcag-228-plan-critique.md

## Executive Summary

This plan delivers the focused, local-testable WCAG 2.2 increment in `src/api` for GitHub issue `#228` covering the Procurement and Contracts Manager (`#/role/procurement` and `#/screens?screen=procurement-packages`) and staff-facing Contractor (`#/role/contractor`, `#/screens?screen=contractor-job-pack`, `#/`, and `#/case/:id`) surfaces. Every section landmark across those screens gains a keyboard-operable jump navigation (`role="navigation"`, `aria-label`, `Go to ...` links) with delegated focus movement to target section headings (`tabindex="-1"`), and all five status surfaces (package queue rows, draft readiness cards, unmet prerequisite badges, contractor job pack submission/acknowledgement items, and independent review status badges) pair documented Fluent 2 visual status badges/lines with explicit plain-language textual state cues while preserving strict contractor vulnerability-reason redaction.

### User Decisions and Requirements Highlights

* Deliver a focused, local-testable increment inside `src/api` on branch `feat/ux-228-procurement-wcag` targeting `feat/demo-233-same-home-tensions-0825`, then commit locally with `Refs #228` and the Copilot `Co-authored-by` trailer without pushing.
* Expose keyboard-operable section jump navigation (`role="navigation"`, `aria-label`, `Go to ...` links) for every section landmark on the Procurement and Contracts Manager and staff-facing Contractor screens in `role-screens.js` and `app.js` (plus `ops.js` for the contractor work-orders section rendered inside `contractorListView`), wiring delegated focus movement to target section headings (`tabindex="-1"`).
* Pair visual styling with explicit plain-language textual state labels across package queue rows, draft readiness cards, unmet prerequisite badges, contractor job pack submission/acknowledgement items, and independent review status badges while preserving contractor vulnerability-reason redaction.
* Add focused unit tests in `src/api/tests/test_procurement_contractor_screen_wcag.py` without `sys.modules` deletion hazards, and validate with `test_*procurement*.py`, `test_role_screens_conformance.py`, `mypy`, and `ruff`.

### What You May Not Know

* **Documented design-system class inventory guard**: `test_role_screens.py` and `test_design_system.py` reject any CSS class in `role-screens.js` not listed in `docs/reference/research/ux/design-system.md`. `.ux-state-cue` is not in the design system; reusing the documented `.flag`, `.flag.danger`, `.status-line`, `.wait`, and `.screen-links` classes (which already include CSS `:before` non-colour warning/hourglass glyphs) paired with `data-state-cue` attributes and explicit plain-language textual labels satisfies `#228` cleanly within `src/api`.
* **Browser-harness Tab-stop and status-region contracts**: `src/api/checks/procurement_screens_browser_check.py` asserts Tab-stop `aria-label` values match `.table-scroll[role="region"]` labels, `[role="status"]` count equals `1` per package (`0` when empty), and exact row/text substrings remain intact. Therefore `aria-label` belongs on `<nav role="navigation">` (never on individual `<a>` jump links, whose visible `Go to ...` text provides their accessible name), and no extra `role="status"` elements are added inside `.screen-evidence`.
* **Cross-cutting static and multi-script guards**: `test_content_standard.py` bans internal words (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`) even in comments; `test_role_screens_tensions_same_home.py` enforces exact count `5` of `screenTension(`; `test_role_screens.py` requires literal `return await roleScreensView()`; `test_safety_panel_ux.py` slices `app.js` up to `async function contractorListView`; and `app.js`, `ops.js`, and `role-screens.js` share one browser global lexical scope requiring pairwise disjoint top-level identifiers and symmetric `defaultPrevented` focus deduplication (`PC-004`).

### Unresolved Decisions or Blockers

* None. All design choices are resolved by repository governance and verified Cycle 1 research evidence (`C1`-`C18`, `W1`).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`rpi-research` -> `rpi-plan` -> `rpi-plan-critique` -> `rpi-implement` -> `rpi-review`) for GitHub issue `#228` in worktree `/home/azureuser/source/ama-demo-wt/feat-228-procurement-wcag` on branch `feat/ux-228-procurement-wcag` targeting `feat/demo-233-same-home-tensions-0825` (user prompt).
* Deliver keyboard-operable section jump navigation (`role="navigation"`, `aria-label`) with `Go to ...` links for all section landmarks on Procurement and Contracts Manager and staff-facing Contractor screens (`src/api/src/zava_forward/api/web/role-screens.js` and `app.js`), and wire delegated focus movement to target section headings (`tabindex="-1"`) (user prompt; `#228`; `#151`).
* Pair visual styling with explicit plain-language textual state cues across package queue rows, draft readiness cards, unmet prerequisite badges, contractor job pack submission/acknowledgement items, and independent review status badges while preserving contractor vulnerability-reason redaction (user prompt; `#228`; `#150`; `#151`; `#153`).
* Add focused unit tests in `src/api/tests/test_procurement_contractor_screen_wcag.py` without `sys.modules` deletion hazards (user prompt).
* Run focused validation in `src/api`: `python3 -m unittest discover -s tests -p "test_*procurement*.py" -v`, `test_role_screens_conformance.py`, `python3 -m mypy`, and `python3 -m ruff check . && python3 -m ruff format --check .` (user prompt).
* Write all dated RPI artifacts under `.copilot-tracking/{research,plans,details,changes,reviews}/2026-11-15/` and commit all changes and `.copilot-tracking/` artifacts locally with `Refs #228` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing (user prompt).

## Goals

* Expose complete WCAG 2.2 bypass-block and landmark navigation (`<nav role="navigation" aria-label="...">` with `Go to ...` links and `<section aria-labelledby="..."><h2 id="..." tabindex="-1">`) across Procurement and Contractor screens, including `#/role/procurement` and `#/role/contractor` route aliases and staff-authenticated Contractor views.
* Pair non-colour visual styling (`.flag`, `.flag.danger`, `.status-line`, `.status-line.wait`) with explicit plain-language textual state cues (`data-state-cue` and plain-language labels) across all five `#228` status surfaces without leaking resident vulnerability reasons to contractors.
* Prove keyboard jump navigation, focus delegation, landmark parity, textual state cues, and contractor redaction via isolated, deterministic unit tests free of `sys.modules` deletion hazards.

## Scope and Non-Goals

### In Scope

* `src/api/src/zava_forward/api/web/role-screens.js`: `screenCell` VNode/DOM pass-through in `screenFields` and `screenTable`; optional anchor support on `screenWithheld` and `screenTension`; `role="navigation"`, `data-jump-target`, and `Go to ...` labels on `procurementJumpNav`; 100% section landmark anchor coverage on `procurement-packages` and `contractor-job-pack`; `#/role/procurement` and `#/role/contractor` hash resolution in `roleScreensView()`; `event.defaultPrevented` guard on `a[data-jump]` click delegation; and paired `.flag` / `.flag.danger` / `.status-line.wait` + explicit plain-language state cues across package queue rows, draft readiness cards, unmet prerequisite badges, contractor submission/acknowledgement items, evidence checklist items, and independent review status badges.
* `src/api/src/zava_forward/api/web/app.js` and `src/api/src/zava_forward/api/web/ops.js`: `#/role/procurement` and `#/role/contractor` script-loading and route dispatch (preserving literal `return await roleScreensView()`); global `a[data-jump]` click delegation (`preventDefault()` + `focus()`); section jump navigation (`role="navigation"`, `aria-label`, `Go to ...`), `aria-labelledby` landmarks, `<h2 tabindex="-1">` focus targets, and paired non-colour badges + explicit textual state cues on `contractorListView()`, `contractorCaseView(id)`, and contractor `workOrdersCard(rows, true)` while preserving `#regulatory-supplier` and vulnerability redaction.
* `src/api/tests/test_procurement_contractor_screen_wcag.py`: New focused unit test module (canonical addition; exact file removals: `none`; maximum file additions in `src/api`: `1`).

### Non-Goals

* External provider portal, contractor self-approval, booking or mutation endpoints, or role-simulator controls.
* Changes outside `src/api` and `.copilot-tracking/` (no edits to `docs/`, `src/core/`, `src/agents/`, or CI workflows).
* Claiming human screen-reader or live end-user accessibility sign-off (`#151` / `#155` remain separate; commit uses `Refs #228`).
* Pushing to any git remote.

## Functional Requirements

* **FR-1 (Procurement & Contractor Jump Navigation and Landmarks in `role-screens.js`)**: `procurement-packages` and `contractor-job-pack` set `ownsStageMap: true` and render `<nav role="navigation" aria-label="Sections of this view" class="screen-links">` containing `Go to <Section>` links (`href="#<anchor>-heading"`, `data-jump="<anchor>-heading"`, `data-jump-target="<anchor>-heading"`) for 100% of `section.screen-record` landmarks inside `.screen-evidence` (including dynamic `Draft readiness <pkg.id>` sections, `"Evidence boundary"`, `"Tension: utilisation versus choice"`, `"Contractor submission and review"`, `"Not shown for this role"`, and `"Journey stages"`), while `roleScreensView()` retains its two named host shell landmarks (`#screen-queue-heading` and `section.screen-evidence[aria-label]`); every panel `<section>` binds `aria-labelledby="<anchor>-heading"` to an `<h2 id="<anchor>-heading" tabindex="-1">`.
  * Observable acceptance criteria: Every `section.screen-record` panel on `procurement-packages` and `contractor-job-pack` (isolated `screen.render()` and mounted `roleScreensView()`) has a 1-to-1 matching `Go to ...` link in `nav[role="navigation"]` whose `data-jump` ID matches its `<h2 tabindex="-1">` ID.
* **FR-2 (Route Aliases, Staff-Facing Contractor Screens, and Focus Delegation in `app.js` / `ops.js`)**: `app.js` maps `#/role/procurement` (`procurement-packages`) and `#/role/contractor` (`contractor-job-pack`) to `#/screens` for primary `#nav` `aria-current="page"` and `routeStatus` announcement, loads `/role-screens.js`, and dispatches `roleScreensView()`; wires symmetric `defaultPrevented`-guarded `a[data-jump]` click handling (`preventDefault()` + `document.getElementById(...).focus()`) across `app.js` and `role-screens.js`; and equips `contractorListView()`, `contractorCaseView(id)`, and contractor `workOrdersCard(rows, true)` with `<nav role="navigation" aria-label="...">` `Go to ...` links, sibling `aria-labelledby` `<section>` landmarks (`jobsSection.after(await contractorOrders())`), and `<h2 tabindex="-1">` focus targets.
  * Observable acceptance criteria: Navigating to `#/role/procurement` or `#/role/contractor` highlights `#nav a[href="#/screens"]` and renders the matching role screen; every `<section>` in `contractorListView` and `contractorCaseView` is a non-nested landmark with a matching `Go to ...` link and `<h2 tabindex="-1">`; clicking any `a[data-jump]` prevents default navigation and focuses the target heading once regardless of script load order.
* **FR-3 (Paired Non-Colour Visual Styling and Explicit Plain-Language State Cues)**: Package queue capacity/evidence cells, draft readiness cards (`status-line wait` + named-reviewer state), unmet prerequisite badges, contractor job pack submission/acknowledgement/checklist/notice items, contractor case/list status and visit-notice items, and independent review status badges pair documented Fluent 2 classes (`.flag`, `.flag.danger`, `.status-line`, `.wait`) with `data-state-cue` metadata and explicit plain-language textual state cues.
  * Observable acceptance criteria: None of the five status surfaces rely on colour alone; unmet/blocked/pending/unknown/over-committed/needs-notice states pair `.flag.danger` or `.status-line.wait` styling with explicit plain-language words (`Unmet`, `Blocked`, `Unknown`, `Pending independent review`, `Not recorded`, `Over-committed`, `Visit notice required: Needs notice`, `State: Draft readiness only...`).
* **FR-4 (Contractor Vulnerability Redaction Preservation)**: All contractor views (`contractor-job-pack`, `contractorListView`, `contractorCaseView`) continue to derive notice cues exclusively from `needs_notice` and `named_contact`, withholding all resident vulnerability reasons, notes, and household details.
  * Observable acceptance criteria: Canary values in `vulnerability_reason`, `vulnerability_notes`, `household`, and work-order `vulnerability_reason` never appear in any contractor DOM output.

## Non-Functional Requirements

* **NFR-1 (Design-System, Content-Standard, and WCAG Static Conformance)**: All modified web files preserve 100% compliance with existing static conformance suites.
  * Objective threshold or evaluation condition: Zero undocumented CSS classes; zero banned internal vocabulary matches (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`); exact preserved counts for `screenTension(` (`5`), `setTimeout` in `role-screens.js` (`2`), `aria-invalid` (`8`), `position:fixed` (`2`), literal `h("table", {},` (`13`), `[role="status"]` per package (`1`), and pairwise disjoint top-level identifiers across `app.js`, `ops.js`, and `role-screens.js`.
  * Operating condition or verification approach, if needed: Verified via `test_role_screens_conformance.py`, `test_role_screens.py`, `test_role_screens_tensions_same_home.py`, `test_design_system.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, `test_safety_screen_wcag_keyboard.py`, `test_safety_panel_ux.py`, and `test_regulatory_ux_check.py`.
  * Observable acceptance criteria: All static and conformance unit tests pass with `0` failures.
* **NFR-2 (Clean Test Isolation, Type Safety, and Lint Hygiene)**: `src/api/tests/test_procurement_contractor_screen_wcag.py` executes deterministically without mutating/deleting `sys.modules` and passes strict typing and linting.
  * Objective threshold or evaluation condition: Zero `del sys.modules` / `sys.modules.pop` calls; `mypy` reports `Success: no issues found`; `ruff check .` and `ruff format --check .` exit `0`.
  * Observable acceptance criteria: Focused `unittest`, `mypy`, and `ruff` commands all pass cleanly from `src/api`.

## Acceptance Criteria

* `#/role/procurement` (`procurement-packages`) and `#/role/contractor` (`contractor-job-pack`) render `<nav role="navigation" aria-label="Sections of this view">` with `Go to ...` links matching 100% of `section.screen-record` panel landmarks (including `Journey stages`) while `roleScreensView()` retains its two named host shell landmarks (`#screen-queue-heading` and `section.screen-evidence[aria-label]`), and staff-authenticated `contractorListView` and `contractorCaseView` render `<nav role="navigation" aria-label="...">` with `Go to ...` links matching 100% of their sibling `<section>` landmarks.
* Every target panel `<section>` exposes `aria-labelledby` pointing to an `<h2 id="..." tabindex="-1">`, and clicking any `a[data-jump]` link prevents hash navigation and focuses the target heading once via symmetric `defaultPrevented`-guarded listeners in `app.js` and `role-screens.js` under either script load order.
* Package queue rows, draft readiness cards, unmet prerequisite badges, contractor job pack submission/acknowledgement items, contractor work-order/job notice items, and independent review status badges pair documented visual status classes (`.flag`, `.flag.danger`, `.status-line`, `.wait`) with `data-state-cue` and explicit plain-language textual state cues without prefix duplication or browser-check substring regressions.
* Contractor views never expose resident `vulnerability_reason`, `vulnerability_notes`, or `household` strings.
* `src/api/tests/test_procurement_contractor_screen_wcag.py` verifies both semantic WCAG behavior and regression guardrails without `sys.modules` deletion hazards, and `test_*procurement*.py`, `test_role_screens_conformance.py`, `test_regulatory_ux_check.py`, `mypy`, and `ruff` pass.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/procurement-contractor-wcag-228-plan.md                                                               |
| Phase details                    | .copilot-tracking/details/2026-11-15/procurement-contractor-wcag-228-phase-details.md                                                    |
| Latest critique                  | .copilot-tracking/reviews/2026-11-15/procurement-contractor-wcag-228-plan-critique.md with Revise verdict; PC-001..PC-005 resolved       |
| Relevant research                | .copilot-tracking/research/2026-11-15/procurement-contractor-wcag-228-research.md                                                        |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/procurement-contractor-wcag-228-changes.md is created by implementation as its evidence record      |
| Planning execution and readiness | Complete and Ready for implementation (all five critique findings PC-001..PC-005 resolved in plan and phase details)                     |
| Continuation context             | Automatic RPI Agent parent return; transitions automatically to Implement (P01-T01)                                                      |

## Sources

* `.copilot-tracking/research/2026-11-15/procurement-contractor-wcag-228-research.md`: Cycle 1 evidence log (`C1`-`C18`, `W1`) and Option A convergence recommendation.
* `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/research/ux/design-system.md`, and `docs/reference/research/ux/content-standard.md`: WCAG 2.2 AA baseline (`#151`), Fluent 2 component inventory (`#150`), and plain-language rules (`#153`).
* `docs/reference/research/ux/customer-journeys/suppliers.md` and `docs/reference/research/ux/screen-design-traceability.md`: Procurement and contractor journey boundaries, role visibility, and vulnerability redaction rules (`#228`).
* `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/ops.js`, and `src/api/tests/test_procurement_screens.py`: Current implementation and regression expectations.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Upgrade Role-Screen Jump Navigation, Landmarks, and Non-Colour State Badges (`role-screens.js`)

* Intent: Complete keyboard jump navigation (`role="navigation"`, `aria-label`, `Go to ...` links), 100% `<section>` landmark anchor parity, `#/role/{procurement,contractor}` alias resolution, deduplicated `a[data-jump]` focus delegation, and paired `.flag` / `.flag.danger` / `.status-line.wait` + explicit plain-language textual state cues across `procurement-packages` and `contractor-job-pack`.
* Dependencies: None.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add DOM/VNode cell pass-through, section anchors, jump nav `Go to ...` links, and `#/role/*` alias resolution in `role-screens.js`

* Requirement and evidence: FR-1, FR-2, NFR-1 (`C1`-`C6`, `C13`, `C15`, `C17`, `C18`).
* Expected result: `screenFields` and `screenTable` pass DOM/VNode badge nodes through cleanly; `screenWithheld` and `screenTension` accept optional `anchor` while keeping exact `5` `screenTension(` occurrences and zero banned substrings; `procurementJumpNav` sets `role: "navigation"`, `aria-label: "Sections of this view"`, `data-jump`, `data-jump-target`, and `Go to ${title}` text covering every `<section>` on `procurement-packages` and `contractor-job-pack`; `roleScreensView()` resolves `#/role/procurement` and `#/role/contractor`; and `role-screens.js`'s `a[data-jump]` listener guards `if (event.defaultPrevented) return;`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/procurement-contractor-wcag-228-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Pair visual status styling with explicit plain-language state cues across `procurement-packages` and `contractor-job-pack`

* Requirement and evidence: FR-3, FR-4, NFR-1 (`C4`-`C9`, `C11`, `C12`, `C16`, `C18`).
* Expected result: Package queue capacity headroom and capacity evidence status cells, draft readiness status banner (`status-line wait` + `State: Draft readiness only...`) and named-reviewer row, prerequisite state badges (`.flag` vs `.flag.danger`), contractor submission/acknowledgement/completion/checklist/notice items, and independent review status cells/rows render documented non-colour visual badges/lines paired with `data-state-cue` and explicit plain-language state text while preserving all existing regression substrings and contractor vulnerability redaction.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/procurement-contractor-wcag-228-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Wire Staff-Facing Contractor Views, `#/role/*` Route Aliases, and Global Jump Focus Delegation (`app.js` & `ops.js`)

* Intent: Ensure `#/role/procurement` and `#/role/contractor` route and script-load cleanly in `app.js`, wire global `a[data-jump]` heading focus delegation, and bring `contractorListView()`, `contractorCaseView(id)`, and contractor `workOrdersCard(rows, true)` to the same WCAG 2.2 jump-nav, landmark, heading-focus, and non-colour textual state-cue baseline without exposing resident vulnerability reasons.
* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add `#/role/{procurement,contractor}` route/script support, global `a[data-jump]` delegation, and Contractor view WCAG landmarks & state cues in `app.js` and `ops.js`

* Requirement and evidence: FR-2, FR-3, FR-4, NFR-1 (`C7`, `C8`, `C10`, `C11`, `C15`, `C17`, `C18`).
* Expected result: `missingWorkspaceScripts` and `route()` in `app.js` support `#/role/procurement` and `#/role/contractor` while preserving literal `return await roleScreensView()`; global click listener in `app.js` prevents default and focuses `document.getElementById(jump.getAttribute("data-jump"))` for any `a[data-jump]`; `contractorListView()`, `contractorCaseView(id)`, and `workOrdersCard(rows, true)` expose `<nav role="navigation" aria-label="...">` `Go to ...` links for every `<section>`, `<h2 tabindex="-1">` focus targets (preserving `#regulatory-supplier`), and paired `.flag`/`.flag.danger`/`.status-line` + explicit textual state labels while redacting vulnerability reasons and keeping zero identifier overlap with `role-screens.js`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/procurement-contractor-wcag-228-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Add Focused Conformance Unit Tests and Run Validation Gate (`test_procurement_contractor_screen_wcag.py`)

* Intent: Lock in semantic and regression coverage for `#228` in `src/api/tests/test_procurement_contractor_screen_wcag.py` without `sys.modules` deletion hazards, and verify all focused unit tests, sibling conformance suites, `mypy`, and `ruff`.
* Dependencies: P01, P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Create `src/api/tests/test_procurement_contractor_screen_wcag.py` and execute focused validation suite

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4, NFR-1, NFR-2 (`C12`-`C18`).
* Expected result: `src/api/tests/test_procurement_contractor_screen_wcag.py` (canonical new test file; `0` removals; `1` file addition; `0` `sys.modules` deletions) verifies keyboard jump navigation (`role="navigation"`, `aria-label`, `Go to ...`), 100% `<section>` landmark parity and `<h2 tabindex="-1">` focus targets, delegated `a[data-jump]` focus movement (`preventDefault` + single `focus()`), `#/role/procurement` and `#/role/contractor` route aliases, `contractorListView`/`contractorCaseView` landmarks and state cues, paired visual badges + explicit textual state labels across all five Deliverable 2 surfaces, and contractor vulnerability-reason redaction; all focused unit tests, conformance suites, `mypy`, and `ruff` pass.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/procurement-contractor-wcag-228-phase-details.md

## Dependencies

* Node.js (`node`) on `PATH`: Used by existing and new `src/api/tests/test_*_wcag.py` harnesses to evaluate `role-screens.js`, `app.js`, and `ops.js` inside isolated `vm` contexts.
* Worktree `PYTHONPATH` (`src:../core/src:../agents/src:../core/tests:../agents/tests` from `src/api`): Ensures Python test runners resolve the current worktree rather than editable installs in the shared environment.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Run 1 `PC-001` [High]    | resolved    | Updated `P02-T01` and `P03-T01`: use `r.needs_notice` (fixing `ReferenceError`), mount `jobsSection.after(await contractorOrders())` so `#contractor-work-orders` is a sibling `<section>` landmark rather than nested inside `#contractor-assigned-jobs`, and add documented `.flag` / `.flag.danger` + `data-state-cue` + explicit notice text (`Visit notice required: Needs notice` / `Standard visit: No extra notice needed`) to `w.needs_notice` in `ops.js`. |
| Run 1 `PC-002` [High]    | resolved    | Updated `P01-T02` and `P03-T01`: deduplicate state prefixes so `"Unmet or Unknown"` never stutters, avoid `"Not supplied"` inside `contractor-job-pack`, and preserve exact sentence punctuation and cell prefixes inside `.flag` / `.flag.danger` badges (`"Not recorded. An acknowledgement is not acceptance."`, `"Unknown. Review data is not available here. Done by someone other than you."`, and `workOrderRecordRows` cells) for `procurement_screens_browser_check.py`. |
| Run 1 `PC-003` [Medium]  | resolved    | Updated `FR-1`, `P01-T01`, and `P03-T01`: pass optional `anchor` to `journeyStageMap`, set `ownsStageMap: true` on `procurement-packages` and `contractor-job-pack` with `package-journey` / `jobpack-journey` jump links, and scope 100% landmark-to-jump-link bijection to `section.screen-record` panels alongside the two named host shell landmarks in `roleScreensView()`. |
| Run 1 `PC-004` [Medium]  | resolved    | Updated `FR-2`, `NFR-1`, `P02-T01`, and `P03-T01`: guard `if (e.defaultPrevented) return;` symmetrically in both `app.js` and `role-screens.js`, guard `if (menu && !menu.contains(e.target))` in `app.js`, keep `ops.js` state-cue helpers function-scoped inside `workOrdersCard`, and test both listener load orders plus pairwise disjoint top-level lexical declarations across `app.js`, `ops.js`, and `role-screens.js`. |
| Run 1 `PC-005` [Low]     | resolved    | Updated `FR-2`, `NFR-1`, `P02-T01`, and `P03`: map `#/role/procurement` and `#/role/contractor` to `#/screens` for `#nav` `aria-current="page"` and `routeStatus`, and include `tests/test_regulatory_ux_check.py` in `P03` validation. |

## Follow-Up Items

* Update `src/api/checks/procurement_screens_browser_check.py` for pre-existing assertion drift introduced on the parent branch (`| 0 |` vs `| Fully committed: 0 |` from `#1716` and `Shift+Tab` landing on `journeyStageMap` stage links before `"Open existing case workspace"` from `#233`), and add Chromium checks for `Go to ...` jump links and `#/role/{procurement,contractor}` hash aliases (`Refs #228`).
* Align sibling specialist role-screen jump helpers (`assetJumpNav`, `financeJumpNav`) to emit `role="navigation"` and `Go to ...` link text consistently with `screenJumpNav` and `procurementJumpNav`.
* Manual assistive-technology and resident/staff usability verification across specialist role screens remains tracked under `#151` / `#155` outside this focused unit-tested increment (`Refs #228`).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/procurement-contractor-wcag-228-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: None
