<!-- markdownlint-disable-file -->
# RPI Phase Details: WCAG 2.2 Conformance Baseline for the Workbench (#151)

## Metadata

* Task ID: 2026-11-15-wcag-baseline-151
* Task slug: wcag-baseline-151
* Related plan: .copilot-tracking/plans/2026-11-15/wcag-baseline-151-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/wcag-baseline-151-research.md, docs/reference/research/ux/wcag-conformance-baseline.md, src/api/tests/test_accessibility_baseline.py

## Phase Index

| Phase ID | Name | Status | Detail sections |
|---|---|---|---|
| P01 | Workbench Accessible Equivalents and WCAG 2.2 AA Web Hardening | ready | P01, P01-T01, P01-T02, P01-T03 |
| P02 | Deterministic Automated Verification Tests | ready | P02, P02-T01 |
| P03 | Structured 8-Dimension WCAG 2.2 AA Workbench Audit, Knowledge Base Update, and Focused Validation | ready | P03, P03-T01, P03-T02 |

<!-- rpi:phase id=P01 -->
## P01: Workbench Accessible Equivalents and WCAG 2.2 AA Web Hardening

### Context

Research Cycle 1 (`C7`-`C15`) and plan critique (`PC-001`..`PC-005`) verified concrete accessible-equivalent, table-reflow, row-header, `<meter>` accessible-name, and target-size gaps in six files (`app.js`, `progress.js`, `ops.js`, `panels.js`, `role-screens.js`, `style.css`), along with exact guard invariants that edits must preserve.

### Intent

Ensure every visual map, chart, `ProgressViews` `<meter>` bar widget, and script-built table in the workbench has complete accessible naming, synchronized keyboard-reachable tabular/list equivalents with empty-state clarity, 320 CSS px scroll-region containment, and `>= 24x24 CSS px` (`40x40 CSS px` on primary/map controls) target sizing.

### Boundaries

* Included: `src/api/src/zava_forward/api/web/app.js`, `progress.js`, `ops.js`, `panels.js`, `role-screens.js`, and `style.css`.
* Excluded: Creating new files under `web/` (`AUDITED_FILES == 19`), editing SHA-pinned `scenario-manifest.json` files, changing `.maplist li` item strings, adding `setAttribute("aria-invalid", "true")` calls (`sites == 9`), changing `:root` token definitions, or introducing banned plain-language terms (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`).

### Likely Targets

* src/api/src/zava_forward/api/web/app.js: Disambiguate `bars()` `<summary>`, wrap chart table in `.table-scroll`, add empty-data chart row, add `[data-maplist-empty]` `<p class="muted">` sibling (`hidden: true`) in `mapPanel()`, and wrap/row-header `fundingView` + `overviewView` tables.
* src/api/src/zava_forward/api/web/progress.js: Add multi-series-accurate `"aria-label": `${row[0]}, ${columns[index + 1]}: ${number(count)} (highest shown: ${number(max)})`` to `<meter>` inside `ProgressViews` `chart()`, keeping `div.progress-bars[aria-hidden="true"]`, `div.table-scroll`, and `"No recorded data for this view."`.
* src/api/src/zava_forward/api/web/ops.js: Add `<caption class="sr-only">` and `.table-scroll` region to `sensorTable()` (keeping `r.reading_id` `<th scope="row">`), and upgrade `k.contractor` to `<th scope="row">` in `packagesView` (keeping its existing `Capacity for ${p.id}` `.table-scroll`).
* src/api/src/zava_forward/api/web/panels.js: Add `.table-scroll` region and `<th scope="row">` to `technicalPanel`, `residentPanel`, and `financeQueueView` tables.
* src/api/src/zava_forward/api/web/role-screens.js: Change `screenTable` default `rowHeader = false` to `rowHeader = true` (`line 50`) so all specialist and `staff-intake.js` tables emit `<th scope="row">`.
* src/api/src/zava_forward/api/web/style.css: Add `details>summary`, `.chart-data summary`, `input[type=checkbox],input[type=radio]`, `.leafmap .leaflet-bar a,.leafmap.leaflet-touch .leaflet-bar a` target sizes, and `var(--muted)` on `.focus dt`.

### Dependencies

* None.

### Validation Expectations

* `node --check` passes on `app.js`, `progress.js`, `ops.js`, `panels.js`, and `role-screens.js`; `test_content_standard.py`, `test_design_system.py`, `test_role_screens.py`, `test_role_screens_conformance.py`, and `test_finance_exposure_screen.py` pass.

### Completion Evidence

* Clean diff in the six target files verified by `node --check` and Phase P02 Node `vm` + static tests.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Harden Overview chart, Leaflet map, and Progress meter accessible equivalents

#### Context

1. `bars(title, data, link)` in `app.js` renders 5 SVG horizontal bar charts on `#/overview`. Each disclosure currently uses `<summary>Show this chart as a table</summary>` without naming `title`, omits `.table-scroll` around its `<table>`, and renders an empty `<tbody>` if `data` is empty (`C8`). `test_accessibility_baseline.py` asserts `"Show this chart as a table"` is in `app.js` (`C22`).
2. `mapPanel(coordinator, filters)` in `app.js` renders `<details class="maplist">` with `<ul class="plainlist">`. When `d.items` is empty, `listUl` has zero children and no explanatory copy (`C7`). `employee_acceptance_check.py` checks `[...panel.querySelectorAll('.maplist li')].map(e => e.textContent)` equals `expected.labels` (`[]` when 0 items, `C19`).
3. `ProgressViews` (`#/progress` and `#/closed`) in `progress.js` renders `<meter min="0" max="..." value="..." tabindex="-1">` inside `div.progress-bars[aria-hidden="true"]` without an `aria-label` (`C9`, `PC-001`), while `table()` already provides `div.table-scroll[role="region"][tabindex="0"]` and `"No recorded data for this view."`.

#### Intent

Give every Overview SVG chart, Leaflet map list equivalent, and `ProgressViews` `<meter>` chart unambiguous accessible names, keyboard-scrollable table wrappers, and explicit empty-state text without breaking `employee_acceptance_check.py`, `test_design_system.py`, or `test_accessibility_baseline.py`.

#### Boundaries

* Included: `bars()` and `mapPanel()` in `src/api/src/zava_forward/api/web/app.js`; `chart()` in `src/api/src/zava_forward/api/web/progress.js`.
* Excluded: Modifying `.maplist li` item markup or strings, replacing `"No recorded data for this view."` in `progress.js`, or using banned jargon words.

#### Likely Targets

* src/api/src/zava_forward/api/web/app.js: Update `bars()` (`summary` with `"Show this chart as a table"` + `h("span", { class: "sr-only" }, `: ${title}`)`, `.table-scroll` `role="region"` `tabindex="0"` `"aria-label": `${title} table``, empty fallback row `"No cases recorded."`) and `mapPanel()` (`const listEmpty = h("p", { class: "muted", "data-maplist-empty": "", hidden: true }, "No mapped homes in this view. Choose Show these as a list for all selected cases.");`, toggled via synchronized `[hidden]` attribute and `listEmpty.hidden = d.items.length > 0` in `renderList`).
* src/api/src/zava_forward/api/web/progress.js: Update `chart()` `<meter>` with `"aria-label": `${row[0]}, ${columns[index + 1]}: ${number(count)} (highest shown: ${number(max)})``.

#### Dependencies

* None.

#### Validation Expectations

* `node --check` passes on `app.js` and `progress.js`; Node `vm` tests confirm populated and empty rendering for `bars()`, `mapPanel()`, and `ProgressViews.dashboard()`/`ProgressViews.closed()`.

#### Completion Evidence

* Updated `app.js` and `progress.js` passing syntax, content-standard, and Node `vm` assertions.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Complete captions, row headers, and focusable scroll regions across all 15 script-built table builders

#### Context

Five multi-column tables across `ops.js`, `panels.js`, and `app.js` lack `.table-scroll` (`role="region"`, `tabindex="0"`, `aria-label`), causing horizontal viewport overflow at 320 CSS px (`ops.js:38`, `panels.js:143`, `panels.js:232`, `panels.js:591`, `app.js:2925`; `PC-003`). In addition, `ops.js:38` `sensorTable` lacks `<caption>` (it already renders `h("th", { scope: "row" }, r.reading_id)`), seven table builders in `ops.js`/`panels.js`/`app.js` use `<td>` on column 0, and `role-screens.js:50` `screenTable` defaults `rowHeader = false` across 19 specialist and `staff-intake.js` call sites (`PC-002`). `test_finance_exposure_screen.py` slices `panels.js` up to `\n}\n` after `async function financeQueueView` (`C21`).

#### Intent

Bring all 15 script-built table builders across `web/*.js` to 100% conformance with `<caption>`, `<th scope="col">`, `<th scope="row">`, and single non-nested keyboard-focusable `.table-scroll` scroll regions.

#### Boundaries

* Included: `sensorTable` and `packagesView` in `ops.js`; `technicalPanel`, `residentPanel`, and `financeQueueView` in `panels.js`; `overviewView` (`Contractors`, `Team workload`) and `fundingView` in `app.js`; `screenTable` (`line 50`) in `role-screens.js`.
* Excluded: Re-wrapping `ops.js:474` `packagesView` (which already has `Capacity for ${p.id}` `.table-scroll`), changing `financeQueueView`'s closing `\n}\n` alignment, or using banned vocabulary.

#### Likely Targets

* src/api/src/zava_forward/api/web/ops.js: Wrap `sensorTable` in `.table-scroll` (`role="region"`, `tabindex="0"`, `"aria-label": `${title} table``) with `h("table", {}, h("caption", { class: "sr-only" }, title), ...)` keeping `h("th", { scope: "row" }, r.reading_id)`; in `packagesView` (`line 477`), keep existing `.table-scroll` and upgrade `k.contractor` cell from `<td>` to `<th scope="row">`.
* src/api/src/zava_forward/api/web/panels.js: Wrap `technicalPanel` table (`"aria-label": "Technical sign-offs table"`), `residentPanel` table (`"aria-label": "Resident decisions by measure table"`), and `financeQueueView` table (`"aria-label": "Invoices waiting for a decision table"`) in `.table-scroll` (`role="region"`, `tabindex="0"`) and upgrade column-0 cells (`label`, `${m.measure}: ...`, and `h("a", ..., r.address)`) to `<th scope="row">`.
* src/api/src/zava_forward/api/web/app.js: Upgrade column-0 cells (`c.name`, `t.name`) in `overviewView` `Contractors` and `Team workload` tables to `<th scope="row">`; wrap `fundingView` table in `.table-scroll` (`role="region"`, `tabindex="0"`, `"aria-label": "Homes where funding is not yet confirmed table"`) and upgrade column-0 cell (`h("a", { href: `#/case/${encodeURIComponent(r.id)}` }, r.resident)`) to `<th scope="row">`.
* src/api/src/zava_forward/api/web/role-screens.js: Change `rowHeader = false` to `rowHeader = true` in `function screenTable` (`line 50`).

#### Dependencies

* None.

#### Validation Expectations

* `node --check` passes on `ops.js`, `panels.js`, `app.js`, and `role-screens.js`; `test_finance_exposure_screen.py`, `test_role_screens.py`, `test_role_screens_conformance.py`, and `test_content_standard.py` pass; counted `h("table", {},` reaches `15` across `web/*.js` with zero uncaptioned tables.

#### Completion Evidence

* Updated `ops.js`, `panels.js`, `app.js`, and `role-screens.js` verified by static and Node `vm` tests.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Harden disclosure, checkbox/radio, Leaflet zoom target sizes, welcome.html skip link, and token contrast

#### Context

In `welcome.html`, `<main class="welcome">` lacked a `.skip-link` bypass anchor matching `index.html`. In `style.css`, bare `<details> > <summary>` elements lack an explicit `min-height: 1.5rem` (`24px`) rule (and `.case-summary` sets `line-height: 1.35` at `<=600px`), standalone checkboxes/radios outside `.regulatory-mode` lack `1.5rem` sizing, Leaflet `.leaflet-bar a` (`26px`) and `.leaflet-touch .leaflet-bar a` (`30px`) in `vendor/leaflet.css` are smaller than the workbench `2.5rem` (`40x40px`) button target (`C14`, `C15`, `PC-005`), and `.focus dt` uses raw `#555`.

#### Intent

Enforce WCAG 2.4.1 bypass parity on `welcome.html` and WCAG 2.5.8 (`>= 24x24 CSS px` minimum; `40x40 CSS px` on desktop and touch Leaflet zoom buttons) and Fluent 2 token consistency in `style.css` without modifying `:root` tokens or violating the 2-rule `position:fixed` cap, zero `outline:none/0` guard, or reduced-motion guard.

#### Boundaries

* Included: `src/api/src/zava_forward/api/web/welcome.html` and `src/api/src/zava_forward/api/web/style.css`.
* Excluded: Changing `:root` tokens (`test_design_system.py`), adding `position:fixed`, `outline:none/0`, or unguarded `transition`/`animation` declarations.

#### Likely Targets

* src/api/src/zava_forward/api/web/welcome.html: Add `<a class="skip-link" href="#welcome-main">Skip to main content</a>` and `id="welcome-main" tabindex="-1"` on `<main>`.
* src/api/src/zava_forward/api/web/style.css: Add `details>summary{cursor:pointer;min-height:1.5rem;padding-block:var(--sp-1)}`, `input[type=checkbox],input[type=radio]{min-width:1.5rem;min-height:1.5rem;vertical-align:middle}`, `.chart-data summary{cursor:pointer;font-weight:600;min-height:1.5rem}`, `.leafmap .leaflet-bar a,.leafmap.leaflet-touch .leaflet-bar a{width:2.5rem;height:2.5rem;min-width:2.5rem;min-height:2.5rem;line-height:2.5rem;color:var(--ink)}`, and update `.focus dt{color:var(--muted)}`.

#### Dependencies

* None.

#### Validation Expectations

* `test_design_system.py`, `test_accessibility_baseline.py`, and `test_wcag_workbench_baseline_151.py` verify CSS rules, contrast ratios, reduced-motion coverage, focus indicator, and `position:fixed` count (`2`).

#### Completion Evidence

* Clean `style.css` diff passing all CSS static and token-contrast tests.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Deterministic Automated Verification Tests

### Context

Caller requirement 3 requires deterministic automated verification tests in `src/api/tests/` asserting both the 8-dimension WCAG 2.2 audit coverage and map/chart/table accessible equivalents across the workbench HTML/JS templates. Creating `src/api/tests/test_wcag_workbench_baseline_151.py` (with zero `@unittest.skip`) in P02 before P03 cites it in `docs/reference/research/ux/wcag-conformance-baseline.md` guarantees `test_epic149_ux_journey_requirement_traceability.py` passes without ordering failure (`C24`, `PC-004`).

### Intent

Lock Test Ownership: update counted/HTML/target-size assertions in `src/api/tests/test_accessibility_baseline.py` (exact test removals: `none`) and add one focused suite `src/api/tests/test_wcag_workbench_baseline_151.py` (maximum new test modules: `1`, maximum test methods: `<= 16`, `0` `@unittest.skip`) combining semantic runtime Node `vm` DOM checks of `bars()`, `mapPanel()`, and `ProgressViews.dashboard()`/`ProgressViews.closed()` with deterministic 8-dimension source/CSS/audit-doc verification.

### Boundaries

* Included: `src/api/tests/test_accessibility_baseline.py` and `src/api/tests/test_wcag_workbench_baseline_151.py`.
* Excluded: Modifying `self.assertEqual(sites, 9,` in `test_accessibility_baseline.py` (`C20`), using `@unittest.skip` (`C24`), or modifying SHA-pinned `scenario-manifest.json` files.

### Likely Targets

* src/api/tests/test_accessibility_baseline.py: Add `law.html` to `lang`/zoom check, update captioned table count `14 -> 15`, and assert new target-size selectors while preserving `self.assertEqual(sites, 9, ...)`.
* src/api/tests/test_wcag_workbench_baseline_151.py: Deterministic 8-dimension WCAG 2.2 audit + Node `vm` DOM accessible-equivalent verification suite.

### Dependencies

* P01.

### Validation Expectations

* `test_accessibility_baseline.py` passes immediately after P02-T01; `test_wcag_workbench_baseline_151.py` passes all web-code assertions immediately and passes all documentation assertions once P03-T01 updates `wcag-conformance-baseline.md`.

### Completion Evidence

* Updated `test_accessibility_baseline.py` and created `test_wcag_workbench_baseline_151.py` compiling cleanly with zero `@unittest.skip`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Update test_accessibility_baseline.py and add test_wcag_workbench_baseline_151.py

#### Context

* Test ownership lock:
  * Canonical targets: `src/api/src/zava_forward/api/web/*.html`, `*.css`, `*.js`, and `docs/reference/research/ux/wcag-conformance-baseline.md`.
  * Generated targets: `none`.
  * Exact test removals: `none`.
  * Maximum additions: `1` new test file (`src/api/tests/test_wcag_workbench_baseline_151.py`) plus targeted assertions in `src/api/tests/test_accessibility_baseline.py`.
  * Semantic vs regression coverage: Semantic Node `vm` DOM execution tests verify actual DOM trees produced by `bars()`, `mapPanel()`/`renderList()` (clusters, points, zero-home empty state with `.hidden`/`[hidden]` synchronized in the DOM stub), and `ProgressViews.dashboard()`/`ProgressViews.closed()` (`<meter aria-label>` across multi-series columns + synchronized `div.table-scroll` tables); deterministic static checks verify all 8 WCAG 2.2 dimensions across HTML/CSS/JS and `wcag-conformance-baseline.md`, including all 15 script-built table builders' `.table-scroll`/`<caption>`/`<th scope="col">`/`<th scope="row">` wrappers and relative-luminance contrast math.

#### Intent

Provide fast, unskipped, high-signal regression and semantic DOM coverage that fails immediately if any visual chart/map/meter/table loses its accessible equivalent or if any of the 8 WCAG 2.2 audit dimensions regresses.

#### Boundaries

* Included: `src/api/tests/test_accessibility_baseline.py` and `src/api/tests/test_wcag_workbench_baseline_151.py`.
* Excluded: `@unittest.skip`, external network/browser calls, or `.copilot-tracking/` string references in test code/docstrings.

#### Likely Targets

* src/api/tests/test_accessibility_baseline.py: Expand HTML list to `("index.html", "welcome.html", "law.html")`, update table count `14 -> 15`, add `details>summary` / `.leafmap .leaflet-bar a` target-size assertions.
* src/api/tests/test_wcag_workbench_baseline_151.py: Create suite covering:
  1. `wcag-conformance-baseline.md` structured 8-dimension audit + widget/15-table inventory + non-conformance guard.
  2. Overview `bars()` Node `vm` DOM parity (SVG `role="img"` + `.sr-only` chart-named `<summary>` + `.table-scroll` region + `<caption>` + `<th scope="col">`/`<th scope="row">` + empty state).
  3. `mapPanel()` Node `vm` DOM parity (`clusters`, `points`, and `0`-item `[data-maplist-empty]` state preserving `0` `.maplist li` nodes on empty, non-colour `MAP_SIGNALS`, `"Show these as a list"` href sync, keyboard handlers).
  4. `ProgressViews.dashboard()` & `ProgressViews.closed()` Node `vm` DOM parity (`<meter aria-label>` multi-series naming using `row[0]` and `columns[index + 1]`, `tabindex="-1"`, `div.progress-bars[aria-hidden="true"]`, synchronized `div.table-scroll[role="region"][tabindex="0"]` table, `"No recorded data for this view."` empty state).
  5. Complete 15-table-builder workbench sweep verifying every `h("table"` across `web/*.js` (including `role-screens.js` `screenTable` with `rowHeader = true`) has `<caption>`, `<th scope="col">`, `<th scope="row">` on data rows, and `.table-scroll` `role="region"` `tabindex="0"`.
  6. 8-dimension source invariants across all 22 web files (keyboard no-positive-tabindex/no-drag, focus order & `:focus-visible`/reduced-motion, name/role/value landmarks & labels, polite status/log live regions, WCAG relative-luminance contrast including alpha-composited header subtitle & welcome aside pairs, reflow/zoom scalable viewport + `2` `position:fixed` cap, 24px/40px/44px target sizes including `.leafmap.leaflet-touch .leaflet-bar a`, and 9 `aria-invalid` + `aria-describedby` error sites).

#### Dependencies

* P01.

#### Validation Expectations

* `test_accessibility_baseline.py` passes immediately; full `test_wcag_workbench_baseline_151.py` passes as soon as P03-T01 updates `wcag-conformance-baseline.md`.

#### Completion Evidence

* Both test files compiled and passing with zero `@unittest.skip`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Structured 8-Dimension WCAG 2.2 AA Workbench Audit, Knowledge Base Update, and Focused Validation

### Context

With all web fixes (P01) and test modules (P02) in place on disk, `docs/reference/research/ux/wcag-conformance-baseline.md` can accurately record the complete structured 8-dimension WCAG 2.2 AA workbench audit and 15-table/visual-widget inventory, cite `test_wcag_workbench_baseline_151.py`, synchronize `docs/reference/README.md` + `docs/reference/log.md`, and pass every UX traceability and focused validation check.

### Intent

Complete the knowledge-base audit deliverable for `#151` / `#119` and verify 100% green focused validation across `src/core`, `src/api`, JS syntax, and branding checks.

### Boundaries

* Included: `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/README.md`, `docs/reference/log.md`, and focused validation runs.
* Excluded: Claiming WCAG 2.2 conformance, marking human assistive-technology tests as passed, removing `SURFACES` or `## Recorded gaps` (naming `/law.html` and `skip`), rewriting historical entries in `docs/reference/log.md`, or citing `.copilot-tracking/` paths in KB docs.

### Likely Targets

* docs/reference/research/ux/wcag-conformance-baseline.md: Structured 8-dimension workbench audit, map/chart/`ProgressViews` `<meter>`/stepper/15-table accessible-equivalents inventory, updated table count (`15`), `law.html` inclusion, and `test_wcag_workbench_baseline_151.py` reference.
* docs/reference/README.md: Update row for `wcag-conformance-baseline.md`.
* docs/reference/log.md: Append dated `[2026-11-15]` entry for `#151` / `#119`.

### Dependencies

* P01 and P02.

### Validation Expectations

* Every focused validation command exits `0`.

### Completion Evidence

* Recorded command outputs and zero-failure test results in `.copilot-tracking/changes/2026-11-15/wcag-baseline-151-changes.md`.

### Unresolved Items

* Owner confirmation `O-1` and manual human AT/zoom sessions remain explicitly recorded as `Not run` / `Pending owner confirmation`.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Author structured 8-dimension WCAG 2.2 AA audit and accessible-equivalents inventory in wcag-conformance-baseline.md, README.md, and log.md

#### Context

Issue `#151` requires an audit covering (1) keyboard, (2) focus order and visibility, (3) name/role/value, (4) status messages, (5) contrast, (6) reflow and zoom, (7) target size, and (8) error identification, plus verified accessible equivalents for map, charts, and tables (`#119`), tracked in `docs/reference/README.md` and `docs/reference/log.md`.

#### Intent

Expand `docs/reference/research/ux/wcag-conformance-baseline.md` with the structured 8-dimension workbench audit and complete visual-widget/15-table accessible-equivalents register while preserving `SURFACES`, `## Recorded gaps`, `## Automated checks`, and every guarded non-conformance phrase, then update `docs/reference/README.md` and append to `docs/reference/log.md`.

#### Boundaries

* Included: `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/README.md`, and `docs/reference/log.md`.
* Excluded: Removing guarded disclaimers, editing earlier log entries or `docs/reference/memory.md`, using em dashes or bolded-prefix list items, or citing `.copilot-tracking/`.

#### Likely Targets

* docs/reference/research/ux/wcag-conformance-baseline.md: Structured 8-dimension audit table and subsections, map/chart/`ProgressViews` (`#/progress`, `#/closed`)/stepper/15-table accessible-equivalents register, updated `## Automated checks`, and preserved `## Recorded gaps` + disclaimers.
* docs/reference/README.md: Update `wcag-conformance-baseline.md` index description.
* docs/reference/log.md: Append `## [2026-11-15] update | Workbench 8-dimension WCAG 2.2 baseline audit and accessible equivalents (Refs #151, #119)` entry.

#### Dependencies

* P01 and P02.

#### Validation Expectations

* `test_accessibility_baseline.py`, `test_wcag_workbench_baseline_151.py`, `test_epic149_ux_evidence_results.py`, and `test_epic149_ux_journey_requirement_traceability.py` all pass.

#### Completion Evidence

* Updated KB files passing all automated checks and diff review.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Execute focused validation suite across src/core, src/api, JS syntax, and branding checks

#### Context

Focused validation tier requires `ruff check` and `mypy` in `src/core` and `src/api`, `node --check` on modified JS files, relevant `src/core` and `src/api` unit tests, and `python3 tools/rename-zava-tests.py`.

#### Intent

Confirm zero lint, type, JS syntax, manifest, plain-language, design-system, role-screen, UX traceability, or runtime test regressions before Review.

#### Boundaries

* Included: Local read/execute validation commands in `src/core`, `src/api`, and repo root.
* Excluded: Modifying unrelated test baselines or skipping failing checks.

#### Likely Targets

* `src/core`: `ruff check`, `mypy`, `unittest` (`test_scenario_manifest.py`, `test_needs_inventory.py`).
* `src/api`: `ruff check`, `mypy`, `node --check` on modified `web/*.js`, `unittest` (`test_accessibility_baseline.py`, `test_wcag_workbench_baseline_151.py`, `test_epic149_*.py`, `test_design_system.py`, `test_role_screens.py`, `test_role_screens_conformance.py`, `test_content_standard.py`, `test_finance_exposure_screen.py`, `test_progress_dashboard.py`, `test_programme_coordinator_wcag_230.py`).
* Repo root: `python3 tools/rename-zava-tests.py`.

#### Dependencies

* P03-T01.

#### Validation Expectations

* Every command exits `0` with clean output.

#### Completion Evidence

* Exact command outputs recorded in `.copilot-tracking/changes/2026-11-15/wcag-baseline-151-changes.md`.

#### Unresolved Items

* None.
