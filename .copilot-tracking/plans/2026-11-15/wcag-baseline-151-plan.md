<!-- markdownlint-disable-file -->
# RPI Plan: WCAG 2.2 Conformance Baseline for the Workbench (#151)

## Task Metadata

* Task ID: 2026-11-15-wcag-baseline-151
* Task slug: wcag-baseline-151
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/wcag-baseline-151-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/wcag-baseline-151-plan-critique.md

## Executive Summary

This plan completes the engineering and source-audit deliverables for GitHub issue `#151` ("WCAG 2.2 conformance baseline for the workbench") and its paired accessible-equivalents requirement (`#119`) on branch `feat/ux-151-wcag-baseline` targeting `feat/demo-233-same-home-tensions-0825`. It fixes concrete accessible-equivalent, table-reflow, row-header, `<meter>` naming, and target-size gaps across six workbench web assets (`app.js`, `progress.js`, `ops.js`, `panels.js`, `role-screens.js`, `style.css`), adds deterministic static plus Node `vm` DOM verification tests in `src/api/tests/test_wcag_workbench_baseline_151.py` alongside `src/api/tests/test_accessibility_baseline.py`, and expands `docs/reference/research/ux/wcag-conformance-baseline.md` into a complete structured 8-dimension WCAG 2.2 AA workbench audit and visual-widget/table register (with synchronized knowledge-base index and log updates).

### User Decisions and Requirements Highlights

* Complete accessible equivalents for the workbench map, charts, and tables (`#119` / `#151`) so every visual map, chart, or distribution widget has a synchronized, keyboard-reachable, screen-reader-accessible tabular or list equivalent with explicit headings, captions/`aria-label`s, and textual state meaning.
* Record a structured 8-dimension WCAG 2.2 AA workbench audit in `docs/reference/research/ux/wcag-conformance-baseline.md` (covering keyboard, focus order and visibility, name/role/value, status messages, contrast, reflow and zoom, target size, and error identification) and update `docs/reference/README.md` plus `docs/reference/log.md`.
* Add deterministic automated tests in `src/api/tests/` under the Focused validation tier (`ruff`, `mypy`, `node --check`, `src/core` + `src/api` focused unit tests, `tools/rename-zava-tests.py`), then commit all code, docs, tests, and `.copilot-tracking/` artifacts on `feat/ux-151-wcag-baseline` without pushing to `main`.

### What You May Not Know

* `src/api/checks/employee_acceptance_check.py` compares `.maplist li` `textContent` directly against `expected.labels` (`[]` on zero-home filters). Therefore, the zero-home accessible explanation inside `<details class="maplist">` must be rendered as a sibling `<p class="muted" data-maplist-empty>` outside `<ul class="plainlist">` (initialized with boolean `hidden: true`), leaving `.maplist li` unchanged.
* `src/api/tests/test_epic149_form_error_summary_associations.py` pins the exact 9 `setAttribute("aria-invalid", "true")` sites and asserts that `"self.assertEqual(sites, 9,"` appears verbatim in `test_accessibility_baseline.py`; `src/api/tests/test_content_standard.py` pins the exact 19 `.html`/`.js` filenames in `web/` and forbids specific internal jargon (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`) even inside comments; and `src/api/tests/test_epic149_ux_journey_requirement_traceability.py` requires every `test_*.py` module cited in `docs/reference/research/ux/*.md` to exist and contain zero `@unittest.skip` decorators.
* Automated static and Node `vm` checks establish deterministic engineering evidence, not WCAG 2.2 AA conformance or human assistive-technology sign-off; human screen-reader/zoom rows stay `Not run` and the commit uses `Refs #151, #119` rather than a closing keyword.

### Unresolved Decisions or Blockers

* None blocking this engineering and audit slice. Owner confirmation `O-1` and named human screen-reader/zoom testing remain tracked post-slice governance gates (`Refs #151`).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Execute the full RPI loop in order (`research`, `plan`, `implement`, `review`), writing dated artifacts under `.copilot-tracking/` (`research`, `plans`, `details`, `changes`, `reviews`) for issue `#151` without skipping phases (user prompt).
* Work in `/home/azureuser/source/ama-demo-wt/feat-151-wcag-baseline` on branch `feat/ux-151-wcag-baseline` targeting `feat/demo-233-same-home-tensions-0825` (`PR #1639`, `6510b6fbc38533a16b9492cacd3ab7e7331c1610`) under the Focused validation tier (user prompt).
* Verify and complete accessible equivalents for the workbench map, charts, and tables (`#119` / `#151`), ensuring every visual map, chart, or visual distribution widget has a synchronized, keyboard-reachable, screen-reader-accessible tabular/list equivalent with explicit headings, captions/`aria-label`s, and textual state meaning (user prompt; issue `#151`, issue `#119`).
* Complete and record the structured WCAG 2.2 AA workbench audit in `docs/reference/research/ux/wcag-conformance-baseline.md` (and update `docs/reference/README.md` + `docs/reference/log.md` on material change) covering all 8 required dimensions: keyboard operation, focus order and visibility, name/role/value, status messages, contrast, reflow and zoom, target size, and error identification (user prompt; `.github/copilot-instructions.md`).
* Preserve the owner-selected Fluent 2 design system, WCAG baseline non-conformance disclaimer (`Not run` for human assistive-technology testing), plain-language content standard (`#153`), counted baseline guards, and `scenario-manifest.json` integrity (`.github/copilot-instructions.md`; research `C19`-`C24`).
* Add deterministic automated verification tests in `src/api/tests/` asserting both 8-dimension WCAG 2.2 audit coverage and map/chart/table accessible equivalents across the workbench HTML/JS templates, run focused validation (`ruff check`, `mypy`, `node --check`, `src/core` + `src/api` tests, `python3 tools/rename-zava-tests.py`), and commit all changes and `.copilot-tracking/` artifacts on `feat/ux-151-wcag-baseline` with the Copilot trailer without pushing to `main` (user prompt).

## Goals

* Ensure every visual map, chart, meter bar distribution, journey stepper, and script-built data table in `src/api/src/zava_forward/api/web/` provides complete programmatic names/headers, synchronized keyboard-reachable tabular/list equivalents, explicit empty-state text, and 320 CSS px keyboard-scrollable reflow containment.
* Harden workbench CSS target sizes and focus-visible coverage across disclosure summaries, checkboxes/radios, and Leaflet zoom controls while preserving Fluent 2 tokens and reduced-motion rules.
* Deliver a complete, traceable 8-dimension WCAG 2.2 AA workbench source audit and accessible-equivalents inventory in `docs/reference/research/ux/wcag-conformance-baseline.md` (plus `docs/reference/README.md` and `docs/reference/log.md`) that distinguishes automated engineering checks from `Not run` human assistive-technology validation.
* Prove both `#151` criteria automatically via unskipped, deterministic unit and Node `vm` DOM tests in `src/api/tests/`.

## Scope and Non-Goals

### In Scope

* Surgical accessible-equivalent, table semantics, reflow, `<meter>` naming, and target-size updates in `src/api/src/zava_forward/api/web/app.js`, `progress.js`, `ops.js`, `panels.js`, `role-screens.js`, and `style.css`.
* Updates to `src/api/tests/test_accessibility_baseline.py` and creation of `src/api/tests/test_wcag_workbench_baseline_151.py` (created before citing in UX docs so `test_epic149_ux_journey_requirement_traceability.py` passes deterministically).
* Structured 8-dimension WCAG 2.2 AA workbench audit and map/chart/distribution/table accessible-equivalents register in `docs/reference/research/ux/wcag-conformance-baseline.md`, plus `docs/reference/README.md` and `docs/reference/log.md`.
* Focused validation (`ruff`, `mypy`, `node --check`, focused `src/core` and `src/api` unit suites, `tools/rename-zava-tests.py`) and local commit on `feat/ux-151-wcag-baseline`.

### Non-Goals

* Claiming WCAG 2.2 AA conformance, owner confirmation `O-1`, or completed human NVDA/JAWS/VoiceOver/TalkBack/browser-zoom testing.
* Adding new files under `src/api/src/zava_forward/api/web/` (keeping `AUDITED_FILES` at 19) or modifying the four SHA-pinned `scenario-manifest.json` files.
* Altering `.maplist li` DOM items or adding a 10th `setAttribute("aria-invalid", "true")` site.
* Visual redesigns outside Fluent 2 tokens or pushing commits to `main`.

## Functional Requirements

* Overview SVG horizontal bar charts (`bars` in `app.js`) must expose a per-chart disambiguated disclosure summary (`Show this chart as a table` + `.sr-only` chart title), wrap their synchronized `<table>` in `.table-scroll` (`role="region"`, `tabindex="0"`, `aria-label`), and render an explicit `"No cases recorded."` fallback row when `data` is empty.
  * Observable acceptance criteria: Executing `bars()` in Node `vm` with populated and empty data yields matching `<svg role="img" aria-label>` and `<details class="chart-data">` table rows, `.sr-only` chart title in `<summary>`, `.table-scroll` keyboard region, `<caption class="sr-only">`, `<th scope="col">`, `<th scope="row">`, and `"No cases recorded."` on empty input.
* Workbench Leaflet map (`mapPanel` in `app.js`) must preserve its synchronized live status region, `"Show these as a list"` link, and `<details class="maplist">` cluster/point items while showing a plain-language sibling notice (`<p class="muted" data-maplist-empty>`) whenever zero mapped homes are in view.
  * Observable acceptance criteria: Executing `mapPanel` / `renderList` across cluster, point, and zero-item payloads renders synchronized counts/links/non-colour `MAP_SIGNALS` text, toggles `[data-maplist-empty]` visible (`hidden === false` and no `hidden` attribute) only when `items.length === 0`, and keeps `.maplist li` empty (`0` `<li>` nodes) when `items.length === 0` so `employee_acceptance_check.py` remains satisfied.
* Progress dashboard `<meter>` bar charts (`ProgressViews` on `#/progress` and `#/closed` in `progress.js`) must provide an explicit multi-series-accurate programmatic `aria-label` on every `<meter>` element (`row[0]`, `columns[index + 1]`, formatted `count`, and formatted `max`) inside `div.progress-bars[aria-hidden="true"]`, paired with the existing `div.table-scroll[role="region"][tabindex="0"]` `<table>` disclosure and `"No recorded data for this view."` empty state.
  * Observable acceptance criteria: Executing `ProgressViews.dashboard()` / `ProgressViews.closed()` in Node `vm` produces named `<meter aria-label="...">` elements matching every series column (`Opened`, `Closed`, `Reopened`, etc.) and every `<caption>` / `<th scope="col">` / `<th scope="row">` row in its paired `<details>` `table()`, and preserves `"No recorded data for this view."` when `rows` is empty.
* All 15 script-built data-table builders across `web/*.js` (`ops.js`, `panels.js`, `app.js`, `aftercare.js`, `role-screens.js`, `progress.js`) must provide a programmatic `<caption>`, `<th scope="col">` column headers, `<th scope="row">` row headers on data rows (including `screenTable` `rowHeader = true` default in `role-screens.js` covering all specialist and `staff-intake.js` tables), and a keyboard-focusable horizontal scroll container (`.table-scroll` with `role="region"`, `tabindex="0"`, `aria-label`).
  * Observable acceptance criteria: Automated inspection verifies all 15 `h("table", {}, h("caption", ...)` builders across `web/*.js` include captions, scoped column and row headers, and focusable `.table-scroll` region wrappers without duplicate nesting, with `ops.js` `sensorTable` no longer excluded.
* Workbench styles (`style.css`) must guarantee `>= 24x24 CSS px` (`1.5rem`) minimum target dimensions on disclosure `<summary>` controls and checkboxes/radios, `2.5rem` (`40x40 CSS px`) on both `.leafmap .leaflet-bar a` and `.leafmap.leaflet-touch .leaflet-bar a` zoom controls, and Fluent 2 token contrast (`var(--muted)` on `.focus dt`) without modifying `:root` token definitions.
  * Observable acceptance criteria: Automated CSS assertions confirm `min-height >= 24px` (`1.5rem`) across buttons, nav links, `details>summary`, `.chart-data summary`, `.linkbtn`, `input[type=checkbox]`, and `>= 40px` (`2.5rem`) on `.leafmap .leaflet-bar a` and `.leafmap.leaflet-touch .leaflet-bar a`, with zero `outline:none/0` rules and `2` bounded `position:fixed` rules.
* `docs/reference/research/ux/wcag-conformance-baseline.md` must document the structured 8-dimension WCAG 2.2 AA workbench audit across all 22 web assets and the complete map/chart/distribution/table accessible-equivalents inventory, synchronized with `docs/reference/README.md` and `docs/reference/log.md`.
  * Observable acceptance criteria: Automated tests verify all 8 dimension sections/rows, WCAG 2.2 SC references, complete widget/table inventory, valid relative links, valid requirement IDs, unskipped cited test modules, and preserved non-conformance disclaimers.

## Non-Functional Requirements

* Deterministic offline test execution
  * Objective threshold or evaluation condition: 100% of tests in `test_accessibility_baseline.py` and `test_wcag_workbench_baseline_151.py` pass locally in `< 10s` with `0` `@unittest.skip` decorators and zero network calls.
  * Operating condition or verification approach, if needed: Run via `unittest` and Node `vm` in `src/api`.
  * Observable acceptance criteria: `unittest` reports `OK` with zero skipped tests in both modules, satisfying `test_epic149_ux_journey_requirement_traceability.py`.
* Plain-language and repository guard preservation
  * Objective threshold or evaluation condition: Zero violations in `test_content_standard.py`, `test_epic149_*.py`, `test_finance_exposure_screen.py`, `test_scenario_manifest.py`, `test_needs_inventory.py`, `ruff check`, `mypy`, `node --check`, and `tools/rename-zava-tests.py`.
  * Operating condition or verification approach, if needed: Execute all focused-tier checks across `src/core`, `src/api`, and repository root.
  * Observable acceptance criteria: Every focused validation command exits `0`.

## Acceptance Criteria

* Every visual map, chart, `<meter>` bar widget, stepper, and data table across `src/api/src/zava_forward/api/web/` has a verified, synchronized, keyboard-reachable, screen-reader-accessible equivalent with explicit headings/captions/`aria-label`s, scoped headers, textual state meaning, and 320 CSS px scroll-region containment (`#119`, `#151`).
* `docs/reference/research/ux/wcag-conformance-baseline.md` records a complete structured audit across all 8 required dimensions (keyboard, focus order and visibility, name/role/value, status messages, contrast, reflow and zoom, target size, error identification) without claiming conformance or human assistive-technology completion, and `docs/reference/README.md` + `docs/reference/log.md` are updated (`#151`).
* `src/api/tests/test_accessibility_baseline.py` and `src/api/tests/test_wcag_workbench_baseline_151.py` deterministically assert all 8 audit dimensions and all map/chart/table accessible equivalents with zero skips, and all focused-tier linters, type checks, JS syntax checks, and regression suites pass.
* All code, documentation, tests, and `.copilot-tracking/` RPI artifacts are committed cleanly on `feat/ux-151-wcag-baseline` with `Refs #151, #119` and the Copilot trailer, without pushing to `main`.

## Implementation Context Record

| Context item | Current artifact or record |
|---|---|
| Plan | .copilot-tracking/plans/2026-11-15/wcag-baseline-151-plan.md |
| Phase details | .copilot-tracking/details/2026-11-15/wcag-baseline-151-phase-details.md |
| Latest critique | .copilot-tracking/reviews/plans/2026-11-15/wcag-baseline-151-plan-critique.md with `Revise` verdict; all 5 planner-owned findings (`PC-001`..`PC-005`) applied and resolved |
| Relevant research | .copilot-tracking/research/2026-11-15/wcag-baseline-151-research.md |
| Changes-record role | .copilot-tracking/changes/2026-11-15/wcag-baseline-151-changes.md is created by implementation as its evidence record |
| Planning execution and readiness | Complete and `Ready` for `rpi-implement` |
| Continuation context | Automatic continuation to `Implement` by confirmed automatic RPI Agent |

## Sources

* .copilot-tracking/research/2026-11-15/wcag-baseline-151-research.md: Complete 22-file codebase audit (`C1`-`C24`) and external standards evidence (`W1`-`W2`).
* docs/reference/research/ux/wcag-conformance-baseline.md: Existing WCAG 2.2 AA baseline, contrast computations, error/table counts, manual role script, and non-conformance boundaries.
* docs/reference/research/ux/design-system.md: Owner-selected Fluent 2 tokens, status signals, and component rules.
* docs/reference/research/ux/content-standard.md: Plain-language vocabulary and structure rules enforced by `test_content_standard.py`.
* src/api/tests/test_accessibility_baseline.py: Existing static WCAG 2.2 baseline test suite and counted invariants.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Workbench Accessible Equivalents and WCAG 2.2 AA Web Hardening

* Intent: Complete map, chart, `<meter>`, and table accessible equivalents plus 320 CSS px table reflow wrappers and 24px/40px target-size CSS rules across existing workbench assets without violating repository guards.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Harden Overview chart, Leaflet map, and Progress meter accessible equivalents

* Requirement and evidence: Issue `#151` / `#119`; research `C7`, `C8`, `C9`, `C19`, `C22`, `C23`; critique `PC-001`, `PC-005`.
* Expected result: `bars()` in `src/api/src/zava_forward/api/web/app.js` disambiguates `<summary>` via `.sr-only` chart title, wraps its table in `.table-scroll` (`role="region"`, `tabindex="0"`, `aria-label`), and handles empty data; `mapPanel()` toggles a sibling `<p class="muted" data-maplist-empty>` (initialized `hidden: true` with synchronized `[hidden]` attribute and `.hidden` property) on 0 mapped items without altering `.maplist li`; `ProgressViews` `chart()` in `src/api/src/zava_forward/api/web/progress.js` adds multi-series-accurate `"aria-label": `${row[0]}, ${columns[index + 1]}: ${number(count)} (highest shown: ${number(max)})`` on `<meter>` elements while preserving `"No recorded data for this view."` and its `div.table-scroll` table disclosure.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/wcag-baseline-151-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Complete captions, row headers, and focusable scroll regions across all 15 script-built table builders

* Requirement and evidence: Issue `#151` / `#119`; WCAG 1.3.1 & 1.4.10; research `C10`, `C11`, `C12`, `C21`, `C22`, `C23`; critique `PC-002`, `PC-003`.
* Expected result: Add `.table-scroll` (`role="region"`, `tabindex="0"`, `aria-label`) to the 5 unwrapped tables (`ops.js:38` `sensorTable` with `<caption class="sr-only">` keeping `r.reading_id`, `panels.js:143` `technicalPanel`, `panels.js:232` `residentPanel`, `panels.js:591` `financeQueueView`, and `app.js:2925` `fundingView` keeping `r.resident`), upgrade column-0 cells to `<th scope="row">` in `ops.js:477` (`packagesView`, keeping its existing `Capacity for ${p.id}` `.table-scroll`), `panels.js:143,232,594`, and `app.js:2899,2904,2927`, and default `rowHeader = true` in `role-screens.js:50` `screenTable` so all specialist and `staff-intake.js` tables emit `<th scope="row">`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/wcag-baseline-151-phase-details.md

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Harden disclosure, checkbox/radio, Leaflet zoom target sizes, welcome.html skip link, and token contrast

* Requirement and evidence: Issue `#151`; WCAG 1.4.3, 2.4.1, 2.4.7, 2.4.11, 2.5.8; research `C1`, `C3`, `C14`, `C15`, `W1`, `W2`; critique `PC-005`.
* Expected result: `src/api/src/zava_forward/api/web/welcome.html` adds a visible-on-focus `.skip-link` (`href="#welcome-main"`) targeting `<main id="welcome-main" tabindex="-1">` matching `index.html`; `src/api/src/zava_forward/api/web/style.css` guarantees `>= 1.5rem` (`24px`) target height on `details>summary`, `.chart-data summary`, and `input[type=checkbox],input[type=radio]`, upgrades both `.leafmap .leaflet-bar a` and `.leafmap.leaflet-touch .leaflet-bar a` to `2.5rem` (`40x40px`) with inherited two-tone `:focus-visible`, uses `var(--muted)` on `.focus dt` without changing `:root` tokens, and preserves `2` `position:fixed` rules and reduced-motion invariants.
* Detail section: P01-T03 in .copilot-tracking/details/2026-11-15/wcag-baseline-151-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Deterministic Automated Verification Tests

* Intent: Create `src/api/tests/test_wcag_workbench_baseline_151.py` (with zero `@unittest.skip`) and update `src/api/tests/test_accessibility_baseline.py` before citing the new test module in `docs/reference/research/ux/wcag-conformance-baseline.md`, preventing `test_epic149_ux_journey_requirement_traceability.py` ordering failures (`PC-004`).
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Update test_accessibility_baseline.py and add test_wcag_workbench_baseline_151.py

* Requirement and evidence: Issue `#151` / `#119`; research `C19`-`C24`; critique `PC-001`..`PC-005`.
* Expected result: `src/api/tests/test_accessibility_baseline.py` checks all 3 HTML files (`index.html`, `welcome.html`, `law.html`), `15` captioned script tables, and expanded target-size selectors while preserving `self.assertEqual(sites, 9, ...)`; `src/api/tests/test_wcag_workbench_baseline_151.py` (zero `@unittest.skip`) verifies all 8 WCAG 2.2 dimensions in source + docs and executes `bars()`, `mapPanel()`/`renderList()`, and `ProgressViews.dashboard()`/`ProgressViews.closed()` in Node `vm` (with `.hidden`/`[hidden]` sync) plus all 15 script-built table builders' `.table-scroll`/`<caption>`/`<th scope="col">`/`<th scope="row">` contracts.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/wcag-baseline-151-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Structured 8-Dimension WCAG 2.2 AA Workbench Audit, Knowledge Base Update, and Focused Validation

* Intent: Record the complete 8-dimension WCAG 2.2 AA workbench audit and visual-widget/table accessible-equivalents inventory in `docs/reference/research/ux/wcag-conformance-baseline.md`, synchronize `docs/reference/README.md` and `docs/reference/log.md`, and run all focused-tier validation checks.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Author structured 8-dimension WCAG 2.2 AA audit and accessible-equivalents inventory in wcag-conformance-baseline.md, README.md, and log.md

* Requirement and evidence: Issue `#151`; `.github/copilot-instructions.md` Knowledge Base Conventions; research `C1`-`C18`, `C24`, `W1`, `W2`; critique `PC-001`, `PC-002`, `PC-004`.
* Expected result: `docs/reference/research/ux/wcag-conformance-baseline.md` documents all 8 required dimensions across all 22 workbench files plus the complete map/chart/`ProgressViews` `<meter>`/stepper/15-table accessible-equivalents register, preserves `SURFACES`, `## Recorded gaps`, `## Automated checks` (citing the already-created `test_wcag_workbench_baseline_151.py`), and all guarded non-conformance phrases, and updates `docs/reference/README.md` + appends a dated entry to `docs/reference/log.md`.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/wcag-baseline-151-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Execute focused validation suite across src/core, src/api, JS syntax, and branding checks

* Requirement and evidence: Caller prompt item 4; `.github/copilot-instructions.md` Focused validation tier.
* Expected result: `ruff check` and `mypy` in `src/core` and `src/api`, `node --check` on modified JS files, unit tests in `src/core` (`test_scenario_manifest.py`, `test_needs_inventory.py`) and `src/api` (`test_accessibility_baseline.py`, `test_wcag_workbench_baseline_151.py`, `test_epic149_*.py`, `test_design_system.py`, `test_role_screens.py`, `test_role_screens_conformance.py`, `test_content_standard.py`, `test_finance_exposure_screen.py`, `test_progress_dashboard.py`, `test_programme_coordinator_wcag_230.py`), and `python3 tools/rename-zava-tests.py` all exit `0`.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/wcag-baseline-151-phase-details.md

## Dependencies

* Node.js (`node`) and Python 3 (`unittest`, `ruff`, `mypy`) in local environment: Required to run `node --check`, Node `vm` DOM tests, and Python validation suites.
* Existing repository guard tests (`test_epic149_*.py`, `test_design_system.py`, `test_content_standard.py`, `test_finance_exposure_screen.py`, `test_scenario_manifest.py`): Constrain counted invariants (`sites == 9`, `19` `AUDITED_FILES`, `:root` token definitions, `.maplist li` structure, banned jargon, zero `@unittest.skip` in cited UX test modules, and untouched SHA-pinned manifest files).

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|---|---|---|
| `PC-001` (`progress.js` variable names, multi-series indexing, IIFE contract, and empty copy) | resolved | Updated `FR-3`, `P01-T01`, `P02-T01`, and `P03-T01` to target `ProgressViews` (`#/progress`, `#/closed`), `row[0]`, `columns[index + 1]`, `div.progress-bars[aria-hidden="true"]`, `div.table-scroll`, and existing `"No recorded data for this view."`. |
| `PC-002` (`role-screens.js:50` `screenTable` `rowHeader = false` default across 19 tables) | resolved | Added `role-screens.js` (`screenTable` `rowHeader = true` default) to `P01-T02` and added `test_role_screens.py` / `test_role_screens_conformance.py` to validation. |
| `PC-003` (`P01-T02` exact row fields `r.resident`/`r.reading_id` and 5 missing `.table-scroll` wrappers without re-wrapping `ops.js:474`) | resolved | Corrected `P01-T02` to keep `r.reading_id` in `ops.js:40`, `r.resident` in `app.js:2927`, and `Capacity for ${p.id}` `.table-scroll` in `ops.js:474`, wrapping only the 5 unwrapped tables. |
| `PC-004` (`P02`/`P03` ordering inversion on `test_epic149_ux_journey_requirement_traceability.py`) | resolved | Reordered `P02` (create `test_wcag_workbench_baseline_151.py` and update `test_accessibility_baseline.py`) before `P03` (cite the module in `wcag-conformance-baseline.md` and run traceability checks). |
| `PC-005` (`.leaflet-touch .leaflet-bar a` specificity and `hidden: true` boolean attribute sync) | resolved | Added `.leafmap.leaflet-touch .leaflet-bar a` alongside `.leafmap .leaflet-bar a` in `P01-T03`, used `class: "muted", "data-maplist-empty": "", hidden: true` in `P01-T01` (respecting `test_design_system.py`), and specified `.hidden`/`[hidden]` sync in `P02-T01`. |

## Follow-Up Items

* Execute manual assistive-technology and browser zoom walkthroughs (NVDA, JAWS, VoiceOver, TalkBack, 200% zoom, 400% reflow) and record owner confirmation `O-1` on issue `#151` — outside automated engineering scope; owned by human testers and repository owner before closing `#151`.
* Author `a11y-runtime.config.json` and integrate live-browser axe-core / Playwright probes into hosted CI (`#155`) — separate backlog issue outside `#151` focused baseline slice.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/wcag-baseline-151-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: None
