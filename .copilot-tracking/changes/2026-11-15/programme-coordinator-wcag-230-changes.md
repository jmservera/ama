<!-- markdownlint-disable-file -->
# RPI Changes: Programme Coordinator WCAG 2.2 Verification and Screen Enhancements (#230)

## Metadata

* Task ID: 2026-11-15-programme-coordinator-wcag-230
* Related plan: .copilot-tracking/plans/2026-11-15/programme-coordinator-wcag-230-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01` (`P01-T01`, `P01-T02`), `P02` (`P02-T01`), `P03` (`P03-T01`, `P03-T02`)
* All remaining active-plan markers: None
* Status basis: Every phase and task in the critique-reconciled plan (`PC-001` through `PC-005`) has been implemented and verified under Focused validation (`unittest`, `node --check`, `ruff`, `mypy`) while preserving `test_accessibility_baseline.py`, `test_content_standard.py`, and `scenario-manifest.json` recipe inputs unchanged.

## Execution Summary

Delivered WCAG 2.2 AA keyboard jump navigation, row-header semantics (`<th scope="row">`), `aria-describedby` status/error/cutoff associations, and Fluent 2 tri-state non-colour state cues (`Unknown != 0`) across `#/role/programme_manager`, `#/role/retrofit_coordinator`, `programme-queue` (`role-screens.js`), and `#/coordinator` (`app.js`, `style.css`), backed by updated row-header assertions in `test_programme_screen_wcag.py` and the new isolated Node VM conformance suite `src/api/tests/test_programme_coordinator_wcag_230.py`.

## Completed Work

### P01: Programme Queue and Role Route Alias WCAG 2.2 Enhancements (`P01-T01`, `P01-T02`)

* Wired `#/role/programme_manager` and `#/role/retrofit_coordinator` into `ROLE_HASH_SCREENS` (`src/api/src/zava_forward/api/web/role-screens.js`) and `isRoleScreensDestination` (`src/api/src/zava_forward/api/web/app.js`) so both hash routes lazy-load `/role-screens.js`, mark `#/screens` active (`aria-current="page"`), preserve `?case=`, `?page=`, and `?scope=` parameters, and enforce role-based `Screen unavailable` (`role="alert"`) fallbacks.
* Upgraded all three `programme-queue` tables (`Shared queue: returned and handed-off work`, `Lifecycle and funnel by stage`, and `Same-home step states`) in `src/api/src/zava_forward/api/web/role-screens.js` to emit `<th scope="row">` for first-column record labels via `screenTable(..., true)` and `screenRecordTable(...)` without adding `h("table", {},` literals.
* Added `aria-describedby="programme-page-status programme-filter-status"` to `#programme-scope`, added `data-jump-target` alongside `data-jump` on `programmeJumpNav` links, and wrapped returned/handoff/not-returned queue states, funnel stage-history/unavailable banners, unblocked warning prose, and step-state cells in Fluent 2 `.flag` / `.flag.danger` / `.status-line.wait` + `data-state-cue` indicators while keeping exact text strings and zero write controls.

### P02: Coordinator Flow (`#/coordinator`) Keyboard Jump Navigation and Non-Colour State Cues (`P02-T01`)

* Added `contractorJumpLinks` (`<nav role="navigation" aria-label="Jump to a coordinator section" class="screen-links">`) inside `coordinatorView()` (`src/api/src/zava_forward/api/web/app.js`) targeting all seven focusable `h2[tabindex="-1"]` section headings (`#coordinator-filters-heading`, `#coordinator-summary-heading`, `#coordinator-heatmap-heading`, `#coordinator-funnel-heading`, `#coordinator-selection-heading`, `#map-title` in `mapPanel`, and `#coordinator-records-heading`).
* Preserved unique landmark naming by binding `<form>`, `summary` (replacing dual `aria-label` with `aria-labelledby`), `Record selection`, and `section.map-panel` via single `aria-labelledby` attributes while leaving the three `table()` outer `<section class="card">` containers unlabelled so each inner `.table-scroll[role="region"][aria-label=title]` remains a unique `region` landmark (`PC-002`).
* Wired `id="co-filter-error"` (`role="alert"`) via `aria-describedby` to `co-view` and `co-group_by` (clearing stale error text on `change` without changing counted `aria-invalid` sites) and wired `id="co-cutoff-note"` via `aria-describedby` to `co-as_of` and `co-start`.
* Added tri-state (`Unknown != 0`) visible `.flag` / `.flag.danger` + `data-state-cue` badges and accessible link descriptions on heatmap count cells (`present` / `zero` / `unknown` with inset border on `.coordinator .heat-present` in `src/api/src/zava_forward/api/web/style.css`) and `Selected records` `Can move on` cells (`stopped` / `no-stop` / `unknown`), and prepended `.coordinator h2[tabindex="-1"]:focus-visible, ` before `.screen-record h2[tabindex="-1"]:focus-visible {` in `style.css` (`PC-001`, `PC-003`).

### P03: Focused WCAG 2.2 Conformance Tests and Regression Verification (`P03-T01`, `P03-T02`)

* Updated `src/api/tests/test_programme_screen_wcag.py` to assert `<th scope="col">` in `<thead>` and `<th scope="row">` in column 0 of `<tbody>` across `programme-queue` tables.
* Created `src/api/tests/test_programme_coordinator_wcag_230.py` (5 comprehensive tests using subprocess `node -e` `vm` DOM contexts with zero `sys.modules` mutation) proving `#/role/programme_manager` and `#/role/retrofit_coordinator` routing/loader/RBAC contracts, `programme-queue` row headers, `aria-describedby`, jump focus delegation, and state cues, `#/coordinator` 7-target jump focus/scroll delegation, unique landmarks, filter error/cutoff `aria-describedby` + recovery, tri-state (`Unknown != 0`) heatmap and `Selected records` non-colour state cues, and CSS focus-ring/non-colour rules.
* Executed Focused validation suites across `src/api` and `src/core`, `node --check`, `ruff check`, `ruff format --check`, and `mypy`.

## Implementation-Time Plan and Detail Updates

* `P03-T02` scope boundary update (immediately relevant current-state update): Scoped `P03-T02` to the Focused validation gates during `rpi-implement` so `P03` completes cleanly before `rpi-review`, while keeping the single local Git commit and rebase onto `origin/feat/demo-233-same-home-tensions-0825` (`AC-05`) sequenced immediately after `rpi-review` writes the review log and `Follow-up` state record so `git status --short` ends empty.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| JavaScript syntax (`node --check`) | `web/role-screens.js`, `web/app.js` | Passed | Zero syntax errors |
| `#230` WCAG suites (`unittest`) | `test_programme_screen`, `test_programme_screen_wcag`, `test_programme_coordinator_wcag_230` | Passed | `38` tests passed (`OK`) |
| Accessibility, content-standard, coordinator & dependency suites (`src/api`) | `test_accessibility_baseline`, `test_content_standard`, `test_procurement_contractor_screen_wcag`, `test_data_steward_screen_wcag`, `test_technical_quality_screens_wcag`, `test_map_fullscreen`, `test_workspace_scripts`, `test_epic149_form_error_summary_associations`, `test_epic149_role_workbench_heading_hierarchy`, `test_coordinator_api`, `test_dependency_rule` | Passed | `166` tests run across combined Focused sweep (`OK`, `9` optional live-assistant skips) |
| Full specialist-screen & WCAG regression sweep (`src/api`) | `unittest discover -s tests -p 'test_*screen*.py'` (37 modules) | Passed | `345` tests passed in `26.9s` (`OK`) |
| Core manifest, needs inventory & dependency rule (`src/core`) | `test_scenario_manifest`, `test_needs_inventory`, `test_dependency_rule` | Passed | All tests passed (`OK`); `scenario-manifest.json` recipe SHA inputs untouched |
| Python linting & formatting (`ruff`) | `ruff check .` and `ruff format --check` on modified/added tests in `src/api` | Passed | `All checks passed!`; `2 files already formatted` |
| Static typing (`mypy`) | `MYPYPATH=src:../core/src:../agents/src mypy src tests/test_programme_screen_wcag.py tests/test_programme_coordinator_wcag_230.py` | Passed | `Success: no issues found in 30 source files` |
| Complete local gate (`tools/rpi-checks.py`) | Repository-wide full gate | Not run (Focused tier) | Issue `#230` is explicitly classified under the Focused validation tier per owner prompt and issue `#1294` guidance |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P02`, `P03` and all `P01-T01`..`P03-T02` markers checked `[x]`).
* Completed-work evidence and handoff prose: Reconciled against actual diffs in `role-screens.js`, `app.js`, `style.css`, `test_programme_screen_wcag.py`, and `test_programme_coordinator_wcag_230.py`.
* Validation, blockers, remaining work, and follow-up items: Current and complete; zero blockers or remaining active-plan items.
* Review readiness: Ready for `rpi-review`.

## Blockers

* None

## Remaining Work

* None in `rpi-implement` (post-`rpi-review` local Git commit and rebase onto `origin/feat/demo-233-same-home-tensions-0825` follows single-pass Review completion).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/programme-coordinator-wcag-230-plan.md, `## Follow-Up Items`
* Execute manual assistive-technology and screen-reader validation across `programme-queue` (`#/role/programme_manager`, `#/role/retrofit_coordinator`) and `#/coordinator` under issues `#151` and `#155` before transitioning `#230` from `Refs #230` to `Closes #230` (Owner: human accessibility / UX reviewer).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan (`P01`, `P02`, `P03` all complete)
* Validation coverage: Focused validation passed (`345` specialist-screen/WCAG tests, `166` baseline/content/coordinator/manifest tests, `node --check`, `ruff check`, `ruff format --check`, `mypy`)
* Blockers: None
* Current plan and detail updates: `P03-T02` boundary clarified so `P03` closes on Focused validation completion before `rpi-review`, with single-commit rebase closeout immediately following `rpi-review`
* Planning and critique state: Complete and `Ready` (`PC-001`..`PC-005` applied and implemented)
* Follow-up items: Manual AT validation (`#151`, `#155`)
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Parent confirmed automatic `RPI Agent`
