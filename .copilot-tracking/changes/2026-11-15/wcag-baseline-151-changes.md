<!-- markdownlint-disable-file -->
# RPI Changes: WCAG 2.2 Conformance Baseline for the Workbench (#151)

## Metadata

* Task ID: 2026-11-15-wcag-baseline-151
* Related plan: .copilot-tracking/plans/2026-11-15/wcag-baseline-151-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/wcag-baseline-151-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01` (`P01-T01`, `P01-T02`, `P01-T03`), `P02` (`P02-T01`), `P03` (`P03-T01`, `P03-T02`)
* All remaining active-plan markers: none
* Status basis: All planned workbench accessible-equivalent fixes, CSS target-size and contrast hardenings, `welcome.html` bypass link, deterministic static and Node-VM test suites, structured eight-dimension WCAG 2.2 AA baseline documentation, knowledge-base index/changelog updates, and focused validation checks completed and passed.

## Execution Summary

Delivered the full approved plan (`P01` through `P03`) for issue `#151` ("WCAG 2.2 conformance baseline for the workbench") and `#119`: hardened visual-widget and table accessible equivalents across `app.js`, `progress.js`, `ops.js`, `panels.js`, `role-screens.js`, `welcome.html`, and `style.css`; updated `test_accessibility_baseline.py` and added `test_wcag_workbench_baseline_151.py`; recorded the structured eight-dimension WCAG 2.2 AA workbench audit and accessible-equivalents register in `docs/reference/research/ux/wcag-conformance-baseline.md` alongside `docs/reference/README.md` and `docs/reference/log.md`; and verified `ruff`, `mypy`, `node --check`, `src/core` + `src/api` unit suites, and `tools/rename-zava-tests.py`.

## Completed Work

### Overview Chart, Leaflet Map, and Progress Meter Accessible Equivalents

* Related phase or task: `P01-T01`
* Files: `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/progress.js`
* What changed and why: Disambiguated `bars()` `<summary>` disclosures via `.sr-only` chart titles, wrapped `bars()` disclosure tables in focusable `.table-scroll` regions (`role="region"`, `tabindex="0"`), added an empty-state `<tr>` for 0-row charts, added a sibling `data-maplist-empty` `<p class="muted">` inside `mapPanel()` `.maplist` that toggles both `.hidden` and `[hidden]` on empty map views without touching `.maplist li`, and added multi-series-accurate `aria-label` attributes (`${row[0]}, ${columns[index + 1]}: ${number(count)} (highest shown: ${number(max)})`) on `ProgressViews` `<meter>` elements.
* Completion evidence: Updated `app.js` and `progress.js`; verified syntax via `node --check` and Node `vm` assertions in `test_wcag_workbench_baseline_151.py`.
* Validation: Passed (`node --check`, `test_content_standard.py`, `test_design_system.py`, `test_wcag_workbench_baseline_151.py`).

### Captions, Row Headers, and Focusable Scroll Regions Across All 15 Script-Built Table Builders

* Related phase or task: `P01-T02`
* Files: `src/api/src/zava_forward/api/web/ops.js`, `src/api/src/zava_forward/api/web/panels.js`, `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/role-screens.js`
* What changed and why: Added `<caption class="sr-only">` and a focusable `.table-scroll` region to `ops.js` `sensorTable` (bringing captioned `h("table", {},` builders across `web/*.js` to `15`), wrapped unwrapped tables in `panels.js` (`technicalPanel`, `residentPanel`, `financeQueueView`) and `app.js` (`fundingView`) in focusable `.table-scroll` regions, upgraded column-0 cells to `<th scope="row">` across `ops.js` (`packagesView`), `panels.js`, and `app.js` (`overviewView` Contractors/Team workload and `fundingView`), and defaulted `rowHeader = true` in `role-screens.js` `screenTable`.
* Completion evidence: Updated `ops.js`, `panels.js`, `app.js`, and `role-screens.js`.
* Validation: Passed (`node --check`, `test_finance_exposure_screen.py`, `test_role_screens.py`, all 18 `test_*wcag*.py` modules).

### Target-Size Minimums, Welcome Skip Link, and Tokenized Contrast

* Related phase or task: `P01-T03`
* Files: `src/api/src/zava_forward/api/web/style.css`, `src/api/src/zava_forward/api/web/welcome.html`
* What changed and why: Added `<a class="skip-link" href="#welcome-main">Skip to main content</a>` and `id="welcome-main" tabindex="-1"` on `<main>` in `welcome.html` to give both in-scope workbench pages consistent WCAG 2.4.1 bypass blocks; added `>= 1.5rem` (`24px`) target-size rules for `details>summary`, `.chart-data summary`, and `input[type=checkbox],input[type=radio]`, upgraded `.leafmap .leaflet-bar a` and `.leafmap.leaflet-touch .leaflet-bar a` to `2.5rem` (`40x40px`), and replaced raw `#555` in `.focus dt` with `var(--muted)` without altering `:root` tokens or `position:fixed` count.
* Completion evidence: Updated `style.css` and `welcome.html`.
* Validation: Passed (`test_design_system.py`, `test_static_assets.py`, `test_accessibility_baseline.py`, `test_wcag_workbench_baseline_151.py`).

### Deterministic Automated Baseline and Accessible-Equivalent Tests

* Related phase or task: `P02-T01`
* Files: `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_wcag_workbench_baseline_151.py`
* What changed and why: Updated `test_accessibility_baseline.py` to check `index.html`, `welcome.html`, and `law.html` language/zoom meta, `15` captioned script tables, and 8 target-size selectors while preserving `sites == 9` on `aria-invalid`; created `test_wcag_workbench_baseline_151.py` (with zero `@unittest.skip`) testing `bars()`, `mapPanel()`/`renderList()` (`clusters`, `points`, and empty-list `[data-maplist-empty]`), `ProgressViews.dashboard()`/`ProgressViews.closed()`, all 15 script-built table builders, all 8 WCAG 2.2 source invariants, and the baseline audit document.
* Completion evidence: Updated `test_accessibility_baseline.py` and created `test_wcag_workbench_baseline_151.py`.
* Validation: Passed (`ruff check`, `mypy`, `unittest`).

### Structured Eight-Dimension WCAG 2.2 AA Audit and Knowledge Base Update

* Related phase or task: `P03-T01`, `P03-T02`
* Files: `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/README.md`, `docs/reference/log.md`
* What changed and why: Recorded the structured eight-dimension WCAG 2.2 AA workbench audit (`### 1. Keyboard operation` through `### 8. Error identification`), the complete accessible-equivalents table (`## Accessible equivalents for maps, charts, and tables (#119, #151)`), `## Recorded gaps` (covering `G-1`..`G-3` and `/law.html`), and updated `## Automated checks` in `wcag-conformance-baseline.md`; synchronized the `docs/reference/README.md` index row and appended a dated `[2026-11-15]` entry to `docs/reference/log.md` while preserving all guarded non-conformance and traceability invariants.
* Completion evidence: Updated `wcag-conformance-baseline.md`, `docs/reference/README.md`, and `docs/reference/log.md`.
* Validation: Passed (`test_epic149_ux_evidence_results.py`, `test_epic149_ux_journey_requirement_traceability.py`, `test_screen_design_traceability.py`, `test_wcag_workbench_baseline_151.py`, `tools/rename-zava-tests.py`).

## Implementation-Time Plan and Detail Updates

* Immediately relevant current-state update (`P01-T03`): Added `<a class="skip-link" href="#welcome-main">Skip to main content</a>` and `id="welcome-main" tabindex="-1"` on `<main>` in `src/api/src/zava_forward/api/web/welcome.html` so both in-scope workbench pages (`index.html` and `welcome.html`) expose consistent WCAG 2.4.1 bypass links while leaving out-of-scope `/law.html` recorded under `## Recorded gaps`. Reflected in `P01-T03` of the plan and phase details.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `ruff check src/core src/api` | Python lint across `src/core` and `src/api` | Passed | `All checks passed!` (exit `0`) |
| `mypy` (`src/core` `src` + `tests`; `src/api` `src` + baseline tests) | Static type checking | Passed | `Success: no issues found in 317 source files` and `Success: no issues found in 30 source files` (exit `0`) |
| `node --check src/api/src/zava_forward/api/web/*.js` | JS syntax across all 16 web scripts | Passed | Exit `0` across all 16 files |
| `src/core` targeted unit tests (`test_scenario_manifest.py`, `test_needs_inventory.py`) | Manifest hashes and core invariants | Passed | `Ran 19 tests in 0.143s - OK` (full non-SDK core suite also passed 3,382 tests; only optional `azure-iot-hub` `SDK_MISSING` tests require Azure extras) |
| `src/api` accessibility, epic149, design-system, content-standard, role-screen, and all 18 `test_*wcag*.py` suites | WCAG baseline, DOM equivalents, KB link/ID traceability, and UX guards | Passed | `Ran 270 tests in 40.621s - OK` + `Ran 142 tests in 10.947s - OK` across all 18 `*wcag*.py` suites |
| `python3 tools/rename-zava-tests.py` | Zava North Homes migration & naming guard | Passed | `Ran 25 tests in 0.629s - OK` |

## Pre-Review Reconciliation

* Plan markers and phase details: aligned (`P01`, `P02`, `P03` and all `P01-T01`..`P03-T02` checked `[x]`)
* Completed-work evidence and handoff prose: aligned
* Validation, blockers, remaining work, and follow-up items: aligned
* Review readiness: ready for `rpi-review`

## Blockers

* none

## Remaining Work

* none (all `P01`, `P02`, and `P03` tasks in declared full-plan scope are complete)

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/wcag-baseline-151-plan.md, `## Follow-Up Items`
* Execute manual assistive-technology and browser zoom walkthroughs (NVDA, JAWS, VoiceOver, TalkBack, 200% zoom, 400% reflow) and record owner target confirmation `O-1` before closing `#151` (`#155`, `#619`).
* Author `a11y-runtime.config.json` and integrate live-browser axe-core / Playwright probes into hosted CI (`#155`).
* Optional follow-up slice for standalone `/law.html` legal register viewer: add a `.skip-link` bypass anchor before `#law` and a polite status region if `/law.html` is brought into workbench conformance scope.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed: `P01`, `P01-T01`, `P01-T02`, `P01-T03`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P03-T02`; remaining: none
* Validation coverage: `ruff check`, `mypy`, `node --check`, `src/core` unit tests, `src/api` WCAG/accessibility/UX/traceability unit tests, and `tools/rename-zava-tests.py` all passed
* Blockers: none
* Current plan and detail updates: `P01-T03` updated with `welcome.html` `.skip-link` alignment
* Planning and critique state: ready (`PC-001`..`PC-005` resolved)
* Follow-up items: manual assistive-technology/zoom walkthroughs and owner confirmation (`#151`/`#155`); live-browser CI harness (`#155`); standalone `/law.html` skip-link slice
* Review readiness or no-handoff reason: ready for `rpi-review`
* Continuation owner: parent (confirmed automatic RPI Agent)
