<!-- markdownlint-disable-file -->
# RPI Plan: Issue #231 Retrofit Technical and Quality Screens WCAG 2.2 Baseline

## Task Metadata

* Task ID: 2026-11-15-retrofit-technical-quality-wcag-231
* Task slug: retrofit-technical-quality-wcag-231
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/retrofit-technical-quality-wcag-231-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/retrofit-technical-quality-wcag-231-plan-critique.md

## Executive Summary

This plan delivers the engineering portion of the remaining unchecked acceptance criterion on GitHub issue #231 (`Accessible per the WCAG 2.2 baseline (#151) with textual state meaning and keyboard navigation`) across the registered Retrofit Assessor, Retrofit Designer, and Quality Inspector screens (`technical-queue` and `quality-queue`) in `src/api/src/zava_forward/api/web/role-screens.js` and `style.css`, backed by a dedicated WCAG 2.2 verification suite in `src/api/tests/test_technical_quality_screens_wcag.py`.

Today, activating any section jump link on `technical-queue` omits `data-jump`, mutating `location.hash` and navigating out of the specialist screen; `quality-queue` lacks section jump links and labelled section landmarks altogether; positive readiness banners use bare `class: "ok"` instead of the documented Fluent 2 `.status-line.ok`; several PAS 2035 state surfaces (`Source facts`, `Design version`, `Missing references`, `Returns and routing`, per-measure quality state, non-independent check evidence, ownerless defects, and reinspection state) lack complete `Object.hasOwn`-safe textual prefixes; and all five tables omit `<th scope="row">`. Fixing these surgically brings both screens to parity with `#226`, `#227`, `#228`, and `#232` without changing any counted baseline guard (`aria-invalid` remains 8, `h("table", {}, ...)` remains 13, `/api/...` inventory unchanged).

### User Decisions and Requirements Highlights

* Complete the full RPI loop (`research`, `plan`, `implement`, `review`) autonomously on `feat/ux-231-retrofit-wcag` (stacked child of `feat/demo-233-same-home-tensions-0825`, PR #1639) using the Focused validation tier, then commit locally with `Refs #231` and Copilot trailer without pushing.
* Upgrade `technical-queue` and `quality-queue` for keyboard jump navigation (`class="screen-links"`, `tabindex="-1"` focus targets, visible focus rings), explicit non-colour textual state meaning across all #231 PAS 2035 domains, table captions and headers, and zero role simulator controls.
* Preserve 100% compatibility with counted baseline guards (`test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_list_export_inventory.py`) and browser checks (`specialist_keyboard_browser_check.py`, `connected_home_browser_check.py`, `atlas_tensions_browser_check.py`, `role_screens_browser_check.py`, `browser_check.py`).

### What You May Not Know

* `test_assessor_screen_wcag.py` pins `{a.href[1:]}` equal to `{section.id}` on `technical-queue`, while `role-screens.js`'s delegated click handler focuses `document.getElementById(link.getAttribute("data-jump"))`. Pairing `href="#${id}"` with `data-jump="${id}-heading"` and `data-jump-target="${id}-heading"` satisfies both contracts simultaneously while keeping `location.hash` on `#/screens?...`.
* `atlas_tensions_browser_check.py`, `connected_home_browser_check.py`, and `test_technical_quality_screens.py` pin exact `<dd>` values for `Current design version`, `Recorded by`, and `Reinspection` (`"Passed"`). Companion `<dt>`/`<dd>` state rows (`Design state`, `Measure state`, `Reinspection state`) provide explicit textual cues without breaking any pinned field equality.
* Automated Node VM and browser checks prove engineering markup and keyboard/state mechanics only; human assistive-technology and role-representative validation (#151, #155) remain required before #231 can be closed (`Refs #231` is mandatory).

### Unresolved Decisions or Blockers

* None blocking planning or implementation. Human assistive-technology/usability sign-off (#151, #155) is tracked as a post-implementation human boundary (`Refs #231`).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Deliver the engineering portion of `- [ ] Accessible per the WCAG 2.2 baseline (#151) with textual state meaning and keyboard navigation` for Issue #231 ("Retrofit assessor, designer and quality inspector screens") on branch `feat/ux-231-retrofit-wcag` (caller prompt; Issue #231).
* Audit `technical-queue` and `quality-queue` in `src/api/src/zava_forward/api/web/role-screens.js`, `app.js`, and `style.css`, following the WCAG 2.2 pattern established in `#226`, `#227`, and `#232` (caller prompt; research `C1`–`C6`).
* Ensure keyboard navigation (`class="screen-links"` jump navigation bar, programmatic focus targets with `tabindex="-1"`, visible focus indicators), explicit textual state meaning (no colour-only status signals for source facts, design version, missing references, separate sign-offs, per-measure evidence, defect owner, and return/reinspection), table captions/headers, and zero role simulator controls in user views (caller prompt).
* Preserve counted baseline guards (`test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_list_export_inventory.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`) and browser checks (`specialist_keyboard_browser_check.py`, `connected_home_browser_check.py`, `atlas_tensions_browser_check.py`, `role_screens_browser_check.py`, `browser_check.py`) (caller prompt; research `C7`, `C13`–`C16`).
* Add focused WCAG 2.2 tests in `src/api/tests/test_technical_quality_screens_wcag.py` and run Focused-tier validation (`unittest` on baseline guards + existing/new WCAG and screen tests, `ruff check`, `ruff format --check`, `mypy`, and refreshed `web-design-guidelines` review) (caller prompt; `.github/copilot-instructions.md`).
* Commit all source changes and `.copilot-tracking/` artifacts locally with `Refs #231` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, without pushing, leaving `git status --short` empty (caller prompt).

## Goals

* Make every substantive section on `technical-queue` and `quality-queue` reachable via `nav.screen-links` keyboard jump links that move focus programmatically to `<h2 id="...-heading" tabindex="-1">` with a visible Fluent 2 focus indicator and without mutating SPA `location.hash`.
* Guarantee explicit, `Object.hasOwn`-safe plain-language textual state meaning across source facts, design version, missing references, separate sign-offs, returns/routing, positive/blocked readiness banners, per-measure quality states, per-check evidence (including non-independent acceptance guards), defect owner, and reinspection state.
* Expose complete table accessibility semantics (`<caption>`, `<th scope="col">`, `<th scope="row">`, and focusable `div.table-scroll[role="region"][tabindex="0"]`) across all five tables on `technical-queue` and `quality-queue` with zero counted-guard inflation and zero role simulator controls.
* Prove these contracts with semantic and regression tests in `src/api/tests/test_technical_quality_screens_wcag.py` while keeping all existing unit, conformance, content-standard, design-system, and browser-check contracts green.

## Scope and Non-Goals

### In Scope

* Updating `technical-queue` and `quality-queue` in `src/api/src/zava_forward/api/web/role-screens.js` (`pasJumpNav`, `technical-boundary` and `quality-*` panel anchors, `.status-line.ok` ready banners, textual state cues, PAS 2035 acceptance-independence guard on per-check `"Verified"`, and `screenRecordTable` row headers).
* Updating `src/api/src/zava_forward/api/web/style.css` so programmatic keyboard focus on `.screen-record h2[tabindex="-1"]:focus-visible` displays the Fluent 2 focus ring and `.screen-evidence th` shares `font-variant-numeric: tabular-nums`.
* Creating `src/api/tests/test_technical_quality_screens_wcag.py`, updating `src/api/checks/role_screens_browser_check.py` (`positive_text`, `check_design_system_use`, `check_table_headers`, and 320px `reach_table_regions` across `231`/`231q`/`231p`/`231qp` under `content-visibility: auto`), and executing Focused-tier validation plus Web Interface Guidelines review.
* Writing dated RPI artifacts under `.copilot-tracking/` and committing locally (`Refs #231`).

### Non-Goals

* Adding write/mutation controls, forms, `aria-invalid` attributes, raw `h("table", ...)` literals, or new `/api/...` endpoints.
* Introducing role simulator or role-switching UI in user views.
* Creating a standalone PAS 2035 lodgement workflow screen (none exists in the current architecture).
* Claiming human assistive-technology or usability conformance acceptance (#151, #155) or closing Issue #231.
* Pushing commits to a remote repository.

## Functional Requirements

* FR-1: `technical-queue` and `quality-queue` must each render a `<nav aria-label="Sections on this screen" class="screen-links">` containing direct `<a>` links (no `<ul>`/`<li>` flex-breaking wrapper) for every anchored `<section id="..." aria-labelledby="...-heading">`, including dynamic per-measure panels (`qualityRecordAnchor(r, index)`) when quality records exist and `Quality evidence` when none exist.
  * Observable acceptance criteria: Every `<section>` with an `id` on `technical-queue` and `quality-queue` has a matching `<a href="#${id}" data-jump="${id}-heading" data-jump-target="${id}-heading">` in `nav.screen-links`, `aria-labelledby="${id}-heading"`, and `<h2 id="${id}-heading" tabindex="-1">`; clicking/activating any jump link calls `preventDefault()`, focuses the target `<h2>`, calls `scrollIntoView({ block: "start" })`, and preserves `#/screens?...` hash routing.
* FR-2: Both screens must state in `Evidence boundary` that every state is written in words first and colour is never the only signal, and render positive readiness banners with documented Fluent 2 `class: "status-line ok"` and `role="status"`.
  * Observable acceptance criteria: Positive `technical-queue` and `quality-queue` trees render `<p class="status-line ok" role="status">` preserving `"Recorded evidence is complete"` / `"does not approve the stage"` and `"Ready on record. Every measure has accepted evidence and no open defect. This screen does not record the handover."`, while blocked trees render `.blocked` `"Cannot confirm readiness"`.
* FR-3: Every #231 PAS 2035 state surface on `technical-queue` and `quality-queue` must carry an explicit `Object.hasOwn`-safe textual prefix without mutating pinned `<dd>` values (`Current design version`, `Recorded by`, `Reinspection` `"Passed"`):
  * `Source facts`: `stateCue(assetConflictCues, assetStatus(c, q))` (`Recorded:`, `Withdrawn:`, `Action needed:`).
  * `Design version`: companion `["Design state", ...]` field (`Recorded: Design version ... on record (not stage approval)` when version and designer name exist; `Action needed: Design record is incomplete` when incomplete).
  * `Separate sign-offs` and `Returns and routing`: `evidenceLabel(x)` (`Verified:`, `Pending review:`, `Action needed:`, refusing `Verified:` when unnamed or unversioned).
  * `Missing references`: `["Missing item", "State", "Owner"]` with `"Action needed: Missing on record"`.
  * `quality-queue` per-measure records: companion `["Measure state", qualityMeasureState(r)]` (`Pending review:`, `Action needed:`, `Verified:`, refusing `Verified:` when `qualityAcceptanceGap(r)` is non-empty); per-check `State` column refusing `"Verified: Evidence noted"` (falling back to `"Action needed: Evidence noted (acceptance incomplete)"` or `"Pending review: Evidence noted"`) when `qualityAcceptanceGap(r)` is non-empty; ownerless `Defect owner` rendering `"Action needed: Unassigned (no defect owner named)"`; and companion `["Reinspection state", qualityReinspectionState(r)]` alongside pinned `["Reinspection", ...]`.
  * Observable acceptance criteria: Unit/VM tests prove explicit prefixes across valid, missing, returned, reassessment, ownerless, non-independent, and `Object.prototype` key (`"constructor"`, `"toString"`) inputs while `test_technical_quality_screens.py`, `test_assessor_screen_wcag.py`, `test_connected_home_check.py`, and `test_learning_test_bundle_scenarios.py` all pass unchanged.
* FR-4: All five tables across `technical-queue` and `quality-queue` must use `screenRecordTable(...)` so every table renders `<caption>`, `<th scope="col">`, `<th scope="row">` on column 0, and `<div class="table-scroll" role="region" aria-label="..." tabindex="0">`, with zero write controls or role simulator UI.
  * Observable acceptance criteria: Every rendered `<table>` on `technical-queue` and `quality-queue` contains `<caption>`, `<th scope="col">` for all header cells, `<th scope="row">` for cell 0 of each body row, and a parent `.table-scroll[role="region"][tabindex="0"]`.

## Non-Functional Requirements

* NFR-1: Counted baseline guard stability and Fluent 2 CSS conformance.
  * Objective threshold or evaluation condition: `setAttribute("aria-invalid", "true")` count across `web/*.js` equals `8`; `h("table", {}, ...)` count equals `13`; zero undocumented CSS classes; zero `animation` or `transition` properties on `.screen-*` selectors; visible focus indicator (`outline: var(--focus-w) solid var(--focus-ink)`) on `:focus-visible` and `.screen-record h2[tabindex="-1"]:focus-visible`.
  * Operating condition or verification approach, if needed: Verified via `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_list_export_inventory.py`, `test_design_system.py`, `test_role_screens_conformance.py`, and `test_content_standard.py`.
  * Observable acceptance criteria: All six guard suites pass with zero baseline-count edits required.
* NFR-2: Static typing, formatting, lint, and Web Interface Guidelines hygiene.
  * Objective threshold or evaluation condition: Zero errors from `ruff check`, `ruff format --check`, and `mypy`, and zero findings against refreshed Web Interface Guidelines on changed web files.
  * Operating condition or verification approach, if needed: Run from `src/api` with worktree `PYTHONPATH` and review `role-screens.js` + `style.css` line by line against fetched `command.md`.
  * Observable acceptance criteria: Clean exit code `0` on all Python linters/typecheckers/tests and zero open Web Interface Guidelines violations.

## Acceptance Criteria

* AC-1: `technical-queue` and `quality-queue` render `nav.screen-links` with direct `<a href="#${id}" data-jump="${id}-heading" data-jump-target="${id}-heading">` links targeting `<section id="${id}" aria-labelledby="${id}-heading">` and `<h2 id="${id}-heading" tabindex="-1">`, and delegated click activation focuses and scrolls the target heading without changing `location.hash`.
* AC-2: `.screen-record h2[tabindex="-1"]:focus-visible` in `style.css` renders the Fluent 2 focus ring (`--focus-w`, `--focus-ink`, `--focus-off`, `--focus`) without adding motion to `.screen-*`, and `.screen-evidence th, .screen-evidence td` applies `font-variant-numeric: tabular-nums`.
* AC-3: All #231 state surfaces (readiness banners via `.status-line.ok`, source facts, design state, missing references, separate sign-offs, returns/routing, measure state, per-check evidence with independence check, defect owner, and reinspection state) expose explicit `Object.hasOwn`-safe textual prefixes, never relying on colour alone.
* AC-4: Every rendered table on `technical-queue` and `quality-queue` exposes `<caption>`, `<th scope="col">`, `<th scope="row">`, and `<div class="table-scroll" role="region" aria-label="..." tabindex="0">`, and neither screen renders write controls or role simulator UI.
* AC-5: `src/api/tests/test_technical_quality_screens_wcag.py` (max 1 new test file; 0 removed test files) passes alongside `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_list_export_inventory.py`, `test_assessor_screen_wcag.py`, `test_technical_quality_screens.py`, `test_role_screens_conformance.py`, `test_role_screens.py`, `test_connected_home_check.py`, `test_specialist_keyboard_check.py`, `test_content_standard.py`, `test_design_system.py`, `test_learning_test_bundle_scenarios.py`, `ruff check`, `ruff format --check`, and `mypy`.

## Test Ownership and Validation Lock

* Canonical production targets: `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/style.css` (generated targets: `none`; `app.js` verified in research `C4` to need no route edits because `#/screens?screen=technical-queue` and `#/screens?screen=quality-queue` already route cleanly once `a[data-jump]` prevents hash clobbering).
* Exact test removals: `none`.
* Maximum test file additions: `1` (`src/api/tests/test_technical_quality_screens_wcag.py`).
* Counted baseline guard changes: `none` (`aria-invalid` remains `8`, `h("table", {}, ...)` remains `13`, `/api/...` list/export inventory unchanged).
* Semantic coverage (`test_technical_quality_screens_wcag.py`):
  * Delegated `a[data-jump]` click behavior on both `technical-queue` and `quality-queue` (`preventDefault`, target `h2` `.focus()`, `.scrollIntoView({ block: "start" })`, missing-target/non-jump safety, dynamic multi-measure anchors, empty-records anchor).
  * Visible focus indicator rules (`:focus-visible` and `.screen-record h2[tabindex="-1"]:focus`) and absence of outline suppression or `.screen-*` motion in `style.css`.
  * Textual state cues across source facts (`Recorded:`, `Withdrawn:`, `Action needed:`), design state (`Recorded:` vs `Action needed:`), missing references (`Action needed: Missing on record`), sign-offs and returns (`Verified:`, `Pending review:`, `Action needed:`), positive readiness banners (`status-line ok`), per-measure quality states, non-independent/unnamed acceptance blocking `"Verified:"` on both `Measure state` and per-check rows, blank/missing defect owner (`Action needed: Unassigned`), reinspection state (`Pending review:`, `Verified:`, and both open-defect and non-independent `Action needed:` branches), plain ASCII punctuation (`"\u2014"` absent), and `Object.prototype` keys (`"constructor"`, `"__proto__"`, `"toString"`).
  * Table accessibility (`<caption>`, `<th scope="col">`, `<th scope="row">`, `div.table-scroll[role="region"][tabindex="0"]`) and zero write/simulator controls.
* Regression coverage (existing suites run unmodified): `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_list_export_inventory.py`, `test_assessor_screen_wcag.py`, `test_technical_quality_screens.py`, `test_role_screens_conformance.py`, `test_role_screens.py`, `test_connected_home_check.py`, `test_specialist_keyboard_check.py`, `test_content_standard.py`, `test_design_system.py`, `test_learning_test_bundle_scenarios.py`, plus local `-m checks.*` execution check (`python3 -m checks.specialist_keyboard_browser_check`, `python3 -m checks.connected_home_browser_check`, `python3 -m checks.atlas_tensions_browser_check`, and `python3 -m checks.role_screens_browser_check` across default and `231`, `231q`, `231p`, `231qp` selectors) if Chromium is installed.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/retrofit-technical-quality-wcag-231-plan.md                                                           |
| Phase details                    | .copilot-tracking/details/2026-11-15/retrofit-technical-quality-wcag-231-phase-details.md                                                |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/retrofit-technical-quality-wcag-231-plan-critique.md (`Complete`, `Revise` -> PC-001..003 applied) |
| Relevant research                | .copilot-tracking/research/2026-11-15/retrofit-technical-quality-wcag-231-research.md (`C1`–`C16`, `W1`)                                 |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/retrofit-technical-quality-wcag-231-changes.md is created by implementation as its evidence record  |
| Planning execution and readiness | Complete and implementation-ready (`ready`); all single-pass critique findings applied directly                                          |
| Continuation context             | Confirmed automatic RPI Agent parent return                                                                                              |

## Sources

* `.copilot-tracking/research/2026-11-15/retrofit-technical-quality-wcag-231-research.md`: Primary codebase (`C1`–`C16`) and Web Interface Guidelines (`W1`) evidence for all #231 gaps and compatibility constraints.
* `docs/reference/research/ux/wcag-conformance-baseline.md`: WCAG 2.2 AA baseline (#151), counted baseline invariants, and engineering-vs-AT acceptance boundary.
* `docs/reference/research/ux/design-system.md`: Owner-selected Fluent 2 component inventory (#150), including `.status-line.ok`, `.blocked`, `.empty`, `.screen-links`, `.screen-record`, and `.table-scroll`.
* `docs/reference/research/ux/content-standard.md`: Plain-language copy rules and banned internal vocabulary (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`).

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Keyboard Section Navigation, Focus Styling, and Table Semantics

* Intent: Deliver SPA-safe keyboard jump navigation (`nav.screen-links` with `a[data-jump]`), labelled `<section>` landmarks, programmatic heading focus rings (`tabindex="-1"`), and `<th scope="row">` table semantics across `technical-queue` and `quality-queue`.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Upgrade `technical-queue` and `quality-queue` jump navigation, section anchors, and `screenRecordTable` semantics in `role-screens.js`

* Requirement and evidence: FR-1, FR-4; research `C1`–`C4`, `C7`, `C11`, `C13`, `C14`, `C16`.
* Expected result: Both `technical-queue` and `quality-queue` render `<nav aria-label="Sections on this screen" class="screen-links">` with direct `<a href="#${id}" data-jump="${id}-heading" data-jump-target="${id}-heading">` links matching every anchored `<section id="${id}" aria-labelledby="${id}-heading">` (including dynamic per-measure quality anchors), and all 5 tables use `screenRecordTable`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/retrofit-technical-quality-wcag-231-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add programmatic heading `:focus-visible` ring and `<th scope="row">` tabular-nums rule in `style.css`

* Requirement and evidence: FR-1, NFR-1; research `C6`, `C10`, `W1`.
* Expected result: `.screen-record h2[tabindex="-1"]:focus-visible` displays the Fluent 2 focus outline/box-shadow without adding motion to `.screen-*` or click focus rings, and `.screen-evidence th, .screen-evidence td` applies `font-variant-numeric: tabular-nums`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/retrofit-technical-quality-wcag-231-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Explicit Non-Colour Textual State Cues and Fluent 2 Readiness Banners

* Intent: Eliminate every unprefixed or ambiguous state signal on `technical-queue` and `quality-queue` while preserving exact pinned `<dd>` values and substrings.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Complete `Object.hasOwn`-safe textual state cues and `.status-line.ok` readiness banners on `technical-queue` and `quality-queue`

* Requirement and evidence: FR-2, FR-3, NFR-1; research `C2`, `C3`, `C5`, `C8`, `C9`, `C11`, `C12`, `C14`–`C16`.
* Expected result: Both screens state in `Evidence boundary` that colour is never the only signal, render positive readiness banners with `class: "status-line ok"`, and expose explicit textual prefixes across `Source facts`, `Design state`, `Missing references`, `Returns and routing`, `Measure state`, independence-guarded per-check `State`, ownerless `Defect owner`, and `Reinspection state`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/retrofit-technical-quality-wcag-231-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Focused WCAG 2.2 Test Suite, Baseline Guard Verification, and Web Guidelines Review

* Intent: Add focused semantic WCAG 2.2 tests in `src/api/tests/test_technical_quality_screens_wcag.py` and verify all Focused-tier unit, guard, lint, type, browser-check, and Web Interface Guidelines checks.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Author `src/api/tests/test_technical_quality_screens_wcag.py` and run Focused-tier validation + refreshed Web Interface Guidelines audit

* Requirement and evidence: FR-1–FR-4, NFR-1, NFR-2, AC-1–AC-5; research `C7`–`C16`, `W1`.
* Expected result: `test_technical_quality_screens_wcag.py` and all existing guard/screen test suites pass, `ruff check`, `ruff format --check`, and `mypy` exit 0, locally runnable specialist browser checks (`role_screens_browser_check` across default + `231`/`231q`/`231p`/`231qp` with pinned axe 4.10.3, `connected_home_browser_check`, `simulator_control_browser_check`, and `specialist_keyboard_browser_check` across all #231 roles) pass, and refreshed Web Interface Guidelines review finds zero open issues on changed web files.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/retrofit-technical-quality-wcag-231-phase-details.md

## Dependencies

* Existing shared helpers in `src/api/src/zava_forward/api/web/role-screens.js` (`screenPanel`, `screenRecordTable`, `stateCue`, `assetConflictCues`, and delegated `a[data-jump]` click handler): reused directly to avoid duplicate mechanisms or counted-guard changes.
* Fluent 2 tokens and component inventory in `src/api/src/zava_forward/api/web/style.css` and `docs/reference/research/ux/design-system.md`: constrains allowed CSS classes (`status-line`, `ok`, `blocked`, `empty`, `screen-links`, `screen-record`, `table-scroll`).
* Worktree Python package source paths (`PYTHONPATH=src:tests:../core/src:../agents/src:../orchestrator/src:../importer/src:../core/tests:../agents/tests`): ensures unit tests and `mypy` resolve this worktree's code rather than another checkout's editable install.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Single-pass critique (`PC-001`, Medium) | Applied directly by planner | Scoped `qualityAcceptanceGap(r)` inside `qualityReinspectionState(r)` in `P02-T01` to `r.state === "Accepted" \|\| r.state === "Handed over"` so open `Returned` defects correctly render `"Action needed: Not yet possible until fix is recorded"`, and added both independent and non-independent defect assertions to `P03-T01`. |
| Single-pass critique (`PC-002`, Medium) | Applied directly by planner | Enforced plain ASCII punctuation (zero `\u2014` em dashes) and banned-word avoidance across both UI strings and JS comments in `P02-T01`, and added `self.assertNotIn("\u2014", ...)` across rendered trees in `P03-T01`. |
| Single-pass critique (`PC-003`, Medium) | Applied directly by planner | Updated Validation Lock and `P03-T01` browser-check commands to run `python3 -m checks.specialist_keyboard_browser_check`, `python3 -m checks.connected_home_browser_check`, `python3 -m checks.atlas_tensions_browser_check`, and `python3 -m checks.role_screens_browser_check` across default plus `231`, `231q`, `231p`, and `231qp` selectors. |
| Residual risk (AT / usability sign-off) | Accepted residual risk | Automated Node VM, static CSS/HTML guards, and headless Chromium checks prove engineering mechanics only; manual assistive-technology and role-representative sign-off (#151, #155) remain open (`Refs #231`). |

## Follow-Up Items

* Parent-branch `resident-service-issues` (`Routes to ask` evidence region in `specialist_keyboard_browser_check.py`) and `programme-queue` write-control expectation (`atlas_tensions_browser_check.py`) from parent commit `f26290cd1` (#1758): unrelated to #231 `technical-queue` and `quality-queue`; reconcile `EXPECTED_REGIONS["resident-service-issues"]` and `atlas_tensions_browser_check.py` on the parent/aftercare workstream.
* Human assistive-technology and role-representative walkthrough for #231 (#151, #155): outside automated engineering scope; owner/human reviewer must complete before Issue #231 can transition from `Refs #231` to closed.
* Dedicated PAS 2035 lodgement workflow screen: outside #231's registered screen set (`technical-queue` and `quality-queue`); apply `pasJumpNav`, `screenRecordTable`, and `Object.hasOwn` `stateCue` when a lodgement screen backlog item is implemented.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/retrofit-technical-quality-wcag-231-changes.md
* Ready phase or task: Complete (`P01`, `P02`, `P03` checked and verified; ready for `rpi-review`)
* Remaining provisional question or blocker: none
