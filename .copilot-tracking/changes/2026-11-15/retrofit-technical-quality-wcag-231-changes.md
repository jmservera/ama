<!-- markdownlint-disable-file -->
# RPI Changes: Issue #231 Retrofit Technical and Quality Screens WCAG 2.2 Baseline

## Metadata

* Task ID: 2026-11-15-retrofit-technical-quality-wcag-231
* Related plan: .copilot-tracking/plans/2026-11-15/retrofit-technical-quality-wcag-231-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/retrofit-technical-quality-wcag-231-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`)
* Completed scope markers: P01, P01-T01, P01-T02, P02, P02-T01, P03, P03-T01
* All remaining active-plan markers: none
* Status basis: Every in-scope phase and task marker has verified code, test, static-analysis, browser-check, and Web Interface Guidelines completion evidence.

## Execution Summary

Delivered full WCAG 2.2 baseline engineering upgrades across `technical-queue` and `quality-queue` in `src/api/src/zava_forward/api/web/role-screens.js` and `src/api/src/zava_forward/api/web/style.css`, added focused Node VM and CSS verification in `src/api/tests/test_technical_quality_screens_wcag.py`, aligned `src/api/checks/role_screens_browser_check.py` with `content-visibility: auto` panel scrolling and row-header/design-system/320px-Tab checks across `231`, `231q`, `231p`, and `231qp`, and verified zero counted-baseline-guard drift across all Focused-tier suites plus pinned axe 4.10.3.

## Completed Work

### Keyboard Section Navigation, Focus Styling, and Table Semantics (`P01`, `P01-T01`, `P01-T02`)

* Added `pasJumpNav(sections)` in `src/api/src/zava_forward/api/web/role-screens.js` emitting `<nav aria-label="Sections on this screen" class="screen-links">` with direct `<a href="#${id}" data-jump="${id}-heading" data-jump-target="${id}-heading">` links so delegated click handling focuses `<h2 id="${id}-heading" tabindex="-1">` and scrolls into view without clobbering `#/screens?...` SPA routing.
* Anchored `Evidence boundary` (`technical-boundary`) alongside all six existing `technical-queue` sections (`targets == set(sections)`) and added `qualityRecordAnchor(r, index)` plus `qualitySections` on `quality-queue` covering `quality-boundary`, `quality-readiness`, dynamic duplicate-safe per-measure panels, and the empty `quality-evidence` fallback.
* Switched all five tables across `technical-queue` (`Source facts and conflicts`, `Sign-off validity after design changes`, `Returned or reassessment sign-offs`, `Missing references`) and `quality-queue` (`Per-check evidence for ${r.measure}`) from `screenTable` to `screenRecordTable` (`rowHeader: true`), adding `<th scope="row">` on column 0 without adding raw `h("table", {}, ...)` literals (`13` count preserved).
* Added `.screen-record h2[tabindex="-1"]:focus-visible` Fluent 2 dual-ring focus styling and extended `.screen-evidence th, .screen-evidence td { font-variant-numeric: tabular-nums; }` in `src/api/src/zava_forward/api/web/style.css` without introducing custom properties or `.screen-*` animations/transitions.

### Explicit Non-Colour Textual State Cues and Fluent 2 Readiness Banners (`P02`, `P02-T01`)

* Added `"Every state on this screen is written in words first; colour is never the only signal."` to both `Evidence boundary` panels (constant literal only, preserving `test_connected_home_check.py` `EVIDENCE_ID_ONLY` case-field constraints) and upgraded positive readiness `<p role="status">` banners on both screens to `class: "status-line ok"` with explicit `"Ready on record"` text and stage/handover non-approval boundaries.
* Added `Object.hasOwn`-safe textual cues across all #231 PAS 2035 domains in `src/api/src/zava_forward/api/web/role-screens.js` without mutating pinned `<dd>` values (`Current design version`, `Recorded by`, `Reinspection` `"Passed"`):
  * `Source facts`: `stateCue(assetConflictCues, assetStatus(c, q))` (`Recorded:`, `Withdrawn:`, `Action needed:`).
  * `Design version`: companion `Design state` row via `technicalDesignState(t)` (`Recorded: Design version ... on record (not stage approval)` vs `Action needed: Design record is incomplete`).
  * `Returns and routing`: added `State` column populated via `evidenceLabel(x)`.
  * `Missing references`: added `State` column with `"Action needed: Missing on record"`.
  * `quality-queue`: added `Measure state` (`qualityMeasureState(r)` downgrading non-independent or unnamed acceptance to `Action needed:`), independence-guarded `qualityCheckState(r, item)` refusing `"Verified: Evidence noted"` when `qualityAcceptanceGap(r)` is non-empty, explicit `"Action needed: Unassigned (no defect owner named)"` when `defect.owner` is blank/missing, and companion `Reinspection state` (`qualityReinspectionState(r)` distinguishing `Pending review:`, `Verified:`, non-independent `Action needed:`, and open-defect `Action needed: Not yet possible until fix is recorded`).

### Focused WCAG 2.2 Test Suite, Browser Harness Alignment, and Web Guidelines Review (`P03`, `P03-T01`)

* Created `src/api/tests/test_technical_quality_screens_wcag.py` with five focused `unittest` methods exercising real `role-screens.js` execution inside Node `vm` and `style.css` invariants across jump links, delegated click focus, `:focus-visible` styling, every #231 PAS 2035 textual state cue (including prototype-key inputs `"constructor"` and self-accepted non-independent quality records), `<th scope="row">` table semantics, plain ASCII punctuation, and absence of write or role-simulator controls.
* Updated `src/api/checks/role_screens_browser_check.py` (`check_readonly_accessibility` and `run_browser`) to read panel text via `positive_text(page)` across `content-visibility: auto` panels after bottom scrolling and to assert `check_design_system_use`, `check_table_headers`, and 320px `reach_table_regions` across `STORY_231` and `STORY_POSITIVE`.

## Implementation-Time Plan and Detail Updates

* Immediately relevant current-state update (`src/api/checks/role_screens_browser_check.py`): Increasing the vertical height of `technical-queue` (`231`) and `quality-queue` (`231q`) pushed the top readiness panel past Chromium's `.screen-record { content-visibility: auto }` skip margin after `run_browser`'s bottom-scroll loop, causing an unscrolled `evidence.inner_text()` call in `check_readonly_accessibility` to miss offscreen text. Switching `check_readonly_accessibility` to `positive_text(page)` and enabling `check_design_system_use`, `check_table_headers`, and 320px `reach_table_regions` for `STORY_231` and `STORY_POSITIVE` aligned `role_screens_browser_check.py` with `#232` (`e5cb78fb6`) and updated `plan.md` and `phase-details.md` accordingly.
* Local judgment refinement (`src/api/src/zava_forward/api/web/style.css`): Refined `.screen-record h2[tabindex="-1"]:focus` to `:focus-visible` after refreshed `web-design-guidelines` review (`Use :focus-visible over :focus (avoid focus ring on click)`) and verified in headless Chromium that keyboard `Enter` on `a[data-jump]` matches `:focus-visible` on `<h2 tabindex="-1">`.
* Follow-up-only discovery (unrelated parent-branch checks): Full-run `specialist_keyboard_browser_check.py` and `atlas_tensions_browser_check.py` hit pre-existing failures on `resident-service-issues` (`Routes to ask` region introduced by parent commit `f26290cd1`, #1758) and `programme-queue` write controls, respectively. Left untouched per scope rules and recorded in `## Follow-Up Items`; verified via targeted Chromium execution that all five roles serving `technical-queue` and `quality-queue` plus all 15 `negative_controls` mutations pass `specialist_keyboard_browser_check.py`.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| Focused `unittest` battery (16 modules: `test_accessibility_baseline`, `test_epic149_form_error_summary_associations`, `test_list_export_inventory`, `test_technical_quality_screens_wcag`, `test_assessor_screen_wcag`, `test_technical_quality_screens`, `test_procurement_qa_screen_wcag`, `test_resident_screen_wcag`, `test_role_screens_conformance`, `test_role_screens`, `test_connected_home_check`, `test_specialist_keyboard_check`, `test_content_standard`, `test_design_system`, `test_learning_test_bundle_scenarios`, `test_safety_screen_wcag_keyboard`) | P01-P03 | Passed | Exit code `0`; counted baseline guards unchanged (`aria-invalid` = 8, `h("table", {}, ...)` = 13, list/export inventory unchanged) |
| `python3 -m ruff check src/ tests/ checks/` and `python3 -m ruff format --check src/ tests/ checks/` | `src/api` | Passed | `All checks passed!`, `203 files already formatted` |
| `python3 -m mypy src/ tests/ checks/` | `src/api` | Passed | `Success: no issues found in 288 source files` |
| `python3 -B -m checks.role_screens_browser_check` across default (`parent`), `231`, `231q`, `231p`, and `231qp` with pinned `ZF_AXE_JS=/tmp/axepk/package/axe.min.js` (axe 4.10.3) | Headless Chromium 156.0.8078.4 | Passed | All selectors exited `0`; `axe finds no violations: []` (`wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa`), `check_design_system_use` = `[]` undocumented classes, `check_table_headers` = `[]` problems across all tables, 320px/390px/1280px reflow and 320px Tab reach passed |
| `python3 -B -m checks.connected_home_browser_check` and `python3 -B -m checks.simulator_control_browser_check` | Headless Chromium 156.0.8078.4 | Passed | Both exited `0` with zero errors |
| `specialist_keyboard_browser_check.walk_screen` + `negative_controls` across all roles serving `technical-queue` and `quality-queue` | Headless Chromium 156.0.8078.4 | Passed | `Retrofit Programme Manager`, `Retrofit Coordinator`, `Building Safety Liaison`, `Quality Inspector`, and `Programme Support Officer` passed `technical-queue` and `quality-queue` walks plus all 15 negative sabotage controls (`negatives=15`); unrelated parent-branch `resident-service-issues` region drift tracked as follow-up |
| Refreshed `web-design-guidelines` (`command.md` fetched from `vercel-labs/web-interface-guidelines`) | `role-screens.js`, `style.css` | Passed | `src/api/src/zava_forward/api/web/role-screens.js`: `✓ pass`; `src/api/src/zava_forward/api/web/style.css`: `✓ pass` |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01` checked `[x]` and aligned with phase details)
* Completed-work evidence and handoff prose: Reconciled
* Validation, blockers, remaining work, and follow-up items: Reconciled
* Review readiness: Ready for `rpi-review`

## Blockers

* None for implementation or engineering review. Human assistive-technology and role-representative sign-off (#151, #155) remains an external post-review closure gate on Issue #231 (`Refs #231`).

## Remaining Work

* None within active plan scope (`P01`–`P03` complete).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/retrofit-technical-quality-wcag-231-plan.md, `## Follow-Up Items`
* Parent-branch `resident-service-issues` (`Routes to ask` evidence region in `specialist_keyboard_browser_check.py`) and `programme-queue` write-control expectation (`atlas_tensions_browser_check.py`) from parent commit `f26290cd1` (#1758): reconcile on the parent/aftercare workstream.
* Human assistive-technology and role-representative walkthrough for #231 (#151, #155): outside automated engineering scope; owner/human reviewer must complete before Issue #231 can transition from `Refs #231` to closed.
* Dedicated PAS 2035 lodgement workflow screen: outside #231's registered screen set (`technical-queue` and `quality-queue`); apply `pasJumpNav`, `screenRecordTable`, and `Object.hasOwn` `stateCue` when a lodgement screen backlog item is implemented.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed: P01, P01-T01, P01-T02, P02, P02-T01, P03, P03-T01; remaining: none
* Validation coverage: 16 Focused-tier `unittest` suites, `ruff check`, `ruff format --check`, `mypy`, `role_screens_browser_check` (`parent`, `231`, `231q`, `231p`, `231qp` + pinned axe 4.10.3), `connected_home_browser_check`, `simulator_control_browser_check`, `specialist_keyboard_browser_check` (#231 roles + 15 negative controls), and refreshed `web-design-guidelines` all passed
* Blockers: none
* Current plan and detail updates: Recorded `role_screens_browser_check.py` `content-visibility: auto` + table-header assertions update and `.screen-record h2[tabindex="-1"]:focus-visible` refinement
* Planning and critique state: ready (`PC-001`, `PC-002`, `PC-003` applied directly in Plan phase)
* Follow-up items: Parent-branch `resident-service-issues`/`programme-queue` browser-check alignment; human assistive-technology/usability sign-off (#151, #155); future dedicated PAS 2035 lodgement screen
* Review readiness or no-handoff reason: Ready for single-pass `rpi-review`
* Continuation owner: parent (confirmed automatic RPI Agent)
