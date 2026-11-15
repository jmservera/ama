---
title: Zava Forward Workbench WCAG 2.2 Conformance Baseline
description: Proposed target level and scope, first audit, automated check coverage, manual check record template and accessibility statement draft for the workbench (issue #151)
ms.date: 2026-11-15
ms.topic: reference
---

## Scope and evidence

Implements issue #151 under epic #149, after the design system (#150). Sources:
`src/api/src/zava_forward/api/web/style.css`, `src/api/src/zava_forward/api/web/*.js`, `src/api/src/zava_forward/api/web/*.html`, `src/api/checks/browser_check.py`,
BRD NFR-008, PRD AC-034, SA-009 and the Accessibility engineering row of the
PRD test strategy, and the accessibility requirements in the
[document workspace journey](./program-manager-document-workspace-journey.md).
Standard: W3C WCAG 2.2 (Recommendation, 5 October 2023). The text was not
re-retrieved for this change; check the official W3C page before any external
statement.

This is a first-pass audit by the delivery agent of a synthetic-data
demonstrator. No screen reader, zoom or user test has been run. Nothing here is
a conformance claim.

## Decision: target level and scope

Status: proposed, pending owner confirmation (open item O-1).

| Item | Proposal |
| --- | --- |
| Target | WCAG 2.2 Level AA for every screen a signed-in user reaches, plus the welcome page |
| Beyond AA | Adopt 2.4.13 Focus Appearance (AAA) as a design goal only |
| In scope | Welcome, sign-in, work list, case view, overview (tiles, charts, map), funding, documents, assistants, operations and account panel, for all seven staff roles and the contractor view |
| Out of scope | Third-party map tiles and the vendored Leaflet library internals (recorded as a known gap); documents uploaded by users |
| Platforms | Current desktop Chromium, Firefox and Safari; one screen reader per desktop OS (NVDA with Firefox, VoiceOver with Safari) |
| Viewports | 320, 390 and 1280 CSS px, 200% text resize, 400% zoom where applicable (PRD test strategy) |

## Audit

Result key: Pass (automated or by inspection), Fixed (finding corrected in this
change), Gap (known, not fixed), Not tested.

| Area | WCAG 2.2 criteria | Result | Evidence and finding |
| --- | --- | --- | --- |
| Page language and zoom | 3.1.1, 1.4.4, 1.4.10 | Pass | `lang="en-GB"` and a viewport meta without `user-scalable=no` on both pages (`test_accessibility_baseline.py`). Reflow at 320 px not tested |
| Keyboard | 2.1.1, 2.1.2, 2.4.3 | Not tested | Controls are native buttons, links, inputs and `details`; the map has a list alternative. 2026-11-15 (#159): Node-VM and headless Chromium checks (`src/api/tests/test_assistant_panel_a11y_159.py`) exercise keyboard-only operation, Tab/Shift+Tab order, Enter versus Shift+Enter, IME guard, size/dock controls and Escape focus restoration across `#employee-chat-launcher`, `#employee-chat` and `#chat-panel` without trap. Full keyboard walk-through by role remains a manual check |
| Focus visible | 2.4.7, 1.4.11 | Fixed | The amber outline had 2.01:1 against white. Focus is now a 3px dark outline (13.7:1 on white) with an amber ring, so it also shows on brand-coloured bars. Indicator on the brand header is not yet confirmed visually |
| Name, role, value | 4.1.2 | Pass, partial | Form fields built in `app.js` and `ops.js` carry `aria-label`; tiles use `aria-pressed`; the chart has `role="img"`. 2026-11-15 (#159): Chromium CDP `Accessibility.getFullAXTree` check (`src/api/tests/test_assistant_panel_a11y_159.py`) verifies computed `dialog`, `log`, `textbox`, `combobox`, `button`, `status` and `alert` roles, accessible names, `aria-expanded` / `aria-pressed` states and `aria-describedby` descriptions for the conversational assistant panel; accessible names of every other generated control across all screens are not tested |
| Status messages | 4.1.3 | Pass, partial | `role="status"`, `role="alert"` and `aria-live="polite"` regions exist; announcement behaviour in a screen reader is not tested (AC-034). 2026-11-13 (#215): regulatory alert and cited-lookup states now also carry a glyph and border shape beside their text, and Escape closes the lookup disclosure with focus on its summary; read from source and observed in the local browser check, not screen-reader or assistive-technology tested, no conformance claim. 2026-11-15 (#159): Node-VM and headless Chromium `MutationObserver` + dialog-scoped CDP AXTree checks (`src/api/tests/test_assistant_panel_a11y_159.py`) verify polite live-region updates across `#employee-chat` (`role="log"`, `role="status"` and `role="alert"`), `#chat-panel > p[role="status"]` proposal requests, `#workspace-status` `403` access-loss resets and `app.js` `401` sign-in `role="alert"` recovery across `answer`, `refused`, `withheld`, `fallback` and error turns; actual desktop assistive-technology speech output remains untested, no conformance claim |
| Contrast, text | 1.4.3 | Pass | Computed for the token pairs in the table below. Disabled controls are exempt (1.4.3 inactive components) |
| Contrast, non-text | 1.4.11 | Fixed, gap | Form field border was 2.51:1 and is now 3.77:1. The caution marker colour is 2.61:1 on its tint and the map marker shapes remain colour-only differences (design-system open item); recorded as gap G-2 |
| Target size | 2.5.8 | Fixed, partial | Buttons are padded about 2.5rem tall. `.linkbtn` and the map list summary now set a 1.5rem (24 CSS px) minimum height, guarded by a static rule check (2026-11-03, #151). Rendered measurement of every generated control, including map controls, is not run |
| Error identification | 3.3.1, 3.3.3 | Pass, partial | `.field-error` and `aria-invalid` exist in CSS. Static inventory 2026-11-04 (#151): all seven script sites that set `aria-invalid` (`app.js`, `assistants.js`, `ops.js` x3, `panels.js`, `progress.js`) link the field to a visible text message through `aria-describedby`, and a test fails when a new site is added without one. The messages are role status or alert text, so the error is not colour-only (the field also gets a border and a warning glyph). Not tested: what a screen reader announces, whether every server-side rejection reaches a field-level message, and correction suggestions (3.3.3) beyond the message text. 2026-11-13 (96, C4): the inventory is now eight sites after a hosted `8 != 7` failure. The new site is the saved Held copy checker (`fundingSavedCopyCheck` in `role-screens.js`), read from source: a native file input named by a visible `label for`, `aria-describedby` pointing at a `field-error` element placed beside it, which the script fills and reveals before setting `aria-invalid`, and clears together on a new file choice. The message is visible text with the warning glyph and a next step, so it is not colour-only, and the same text also goes to a `role="status"` live region (markup and intent only). A focused static test now checks that site's label, describedby target and message wiring; the existing browser check observes `aria-invalid` and the message text for the no-file case but was not re-run for this entry. Not tested: what a screen reader announces for this field, assistive technology, manual acceptance. No conformance claim. 2026-11-15 (#135, Cycle 1): the inventory is now nine sites after a hosted `9 != 8` failure. The new site is the exception recovery audit-reason textarea (`renderExceptionRecoveryForm` on `#/exceptions` in `app.js`), read from source: named by a visible `label for`, `aria-describedby` linking its hint and a hidden `field-error` `role="alert"` paragraph; on blank submit the handler sets `aria-invalid`, reveals the paragraph and fills it with plain-language reason, owner and next action before calling `reasonInput.focus()`, and clears both on non-empty input or valid submit. Focused static checks in `src/api/tests/test_accessibility_baseline.py` and `src/api/tests/test_epic149_form_error_summary_associations.py` and Node-VM checks in `src/api/tests/test_exception_queue_ui.py` cover markup and state transitions; not screen-reader, assistive-technology or human tested; no conformance claim |
| Charts | 1.1.1, 1.3.1 | Fixed | Overview SVG charts (`bars()` in `app.js`) and `ProgressViews` `<meter>` charts (`progress.js`) pair visual bars with keyboard-reachable `<details>` table disclosures inside focusable `.table-scroll` regions with disambiguated summaries, captions, scoped column and row headers, and explicit empty-state rows (#119, #151) |
| Map | 1.1.1, 2.1.1 | Fixed, partial | Region label, shape-and-letter markers (`O`, `W`, `!`), keyboard pan/zoom/marker activation, and `"Show the map areas as a list"` disclosure (`#119`) with synchronized cluster buttons, point links, and `[data-maplist-empty]` zero-item notice (#151). Tile imagery is third-party |
| Tables | 1.3.1, 1.4.10, 4.1.2 | Fixed, partial | Static inventory 2026-11-04 (#151): all 11 script-built workbench tables now have a caption and `th scope="col"` headers (funding queue, resident decisions and finance queue were missing scope; five lacked a caption, now screen-reader only), and a test fails when a table is added without a caption or a header without scope. First-column cells in several tables are `td`, not row headers. Not tested: screen-reader table navigation, the resident demo and chart-table pages beyond their existing markup. 2026-11-10 (#133, Stage A, unwired): the inventory is now 12. The synthetic aftercare evaluator table was read from source: first-child caption, six `th scope="col"`, `th scope="row"` home cells, `Unknown` as text, and it sits in a keyboard-focusable `table-scroll` region named by its caption. The static test only counts tables, requires a caption and rejects bare `th`; the scope reading is a manual source audit. Not tested: reflow at 320 px, served page, screen-reader navigation. 2026-11-11 (#83, refs only): the regex-counted inventory is now 13. The new table is the read-only handoff waiting screen (`#/handoff-waiting`, `handoffWaitingView` in `app.js`), read from source: first-child screen-reader-only caption, seven `th scope="col"`, a `th scope="row"` case link per row, status, waiting hours, due, owners and escalation reasons as plain text (no colour-only signal), inside a `table-scroll` region with `tabindex="0"` named "Unaccepted handoffs table" that takes the global `:focus-visible` indicator. Constructed-browser tests in `src/api/tests/test_handoff_waiting_view.py` cover rendering, keyboard reach of the case links and a visible failure state; they are not accessibility tests. Not tested: screen-reader navigation, reflow at 320 px, zoom, assistive technology, manual acceptance. The count excludes the `ops.js` sensor table (`aria-label`, no caption), which the regex does not match and this entry does not audit. No approved global waiting time exists (OD-09 undecided). No conformance claim. 2026-11-15 (#135, Cycle 1): the regex-counted inventory is now 14. The new table is the competing source values table on `#/exceptions` (`exceptionsView` in `app.js`), read from source: first-child screen-reader-only caption, four `th scope="col"` headers (`Value`, `Source`, `Date`, `Version`), `th scope="row"` value cells (`Unknown` as plain text when absent), plain-text source, date and `translate="no"` version cells, inside a keyboard-focusable `table-scroll` region with `tabindex="0"` named for the conflict item. Node-VM tests in `src/api/tests/test_exception_queue_ui.py` cover rendering and structure; they are not accessibility tests. Not tested: screen-reader navigation, reflow at 320 px, zoom, assistive technology, manual acceptance. No conformance claim. 2026-11-15 (#151): the inventory is now 15 after `sensorTable` in `ops.js` gained a `<caption class="sr-only">` and `.table-scroll` wrapper; all 15 script-built table builders now sit inside keyboard-focusable `.table-scroll` (`role="region"`, `tabindex="0"`, `aria-label`) containers and emit both `<th scope="col">` column headers and `<th scope="row">` row headers (`screenTable` in `role-screens.js` defaults `rowHeader = true`). Verified in `src/api/tests/test_accessibility_baseline.py` and `src/api/tests/test_wcag_workbench_baseline_151.py`; screen-reader navigation and human acceptance remain open (#155) |
| Focus not obscured, dragging movements | 2.4.11, 2.5.7 | Fixed, partial | The fixed chat launcher and widget could cover a control that receives focus near the bottom edge. `html` now sets `scroll-padding-block-end: 6rem` (launcher 3.5rem plus inset), and a static test lists every fixed-position rule and fails on a new one (2026-11-04, #151). No script binds drag or touch handlers (static test); the map pans with Leaflet keyboard controls and has a list alternative. 2026-11-15 (#159): Node-VM and Chromium checks (`src/api/tests/test_assistant_panel_a11y_159.py`) verify `revealBeside` vertical and horizontal scroll clearance when an external page control receives focus under the open floating or docked `#employee-chat` panel at 1280 x 900 CSS px. Not tested: sticky sidebar and open chat panel at 400% zoom, 320 px reflow overlap across all screens, Leaflet pointer panning without dragging |
| Redundant entry, consistent help, accessible authentication | 3.2.6, 3.3.7, 3.3.8 | Not tested | Sign-in uses Entra ID or a shared password in the demonstrator; not assessed |

### Contrast results

Computed with the WCAG relative luminance formula from the tokens in
`src/api/src/zava_forward/api/web/style.css`; reproduced by `test_accessibility_baseline.py`.

| Pair | Ratio | Needed |
| --- | --- | --- |
| Ink on page background | 13.7:1 | 4.5:1 |
| Muted text on white | 5.8:1 | 4.5:1 |
| White on brand | 7.5:1 | 4.5:1 |
| White on dark brand | 10.9:1 | 4.5:1 |
| Warning text on warning tint | 5.6:1 | 4.5:1 |
| OK text on OK tint | 5.8:1 | 4.5:1 |
| Field border on white | 3.8:1 | 3:1 |
| Focus outline on white | 13.7:1 | 3:1 |
| Caution marker on caution tint | 2.6:1 | 3:1 (gap G-2) |

## Structured eight-dimension workbench audit (2026-11-15, #151)

Source and deterministic Node-VM audit across the 22 served web assets under `src/api/src/zava_forward/api/web/` (`index.html`, `welcome.html`, `law.html`, `style.css`, `progress.css`, `chat-widget.css`, and the 16 application scripts). All findings below are engineering baseline evidence on synthetic data, not WCAG 2.2 conformance or assistive-technology acceptance (#155).

### 1. Keyboard operation

* Criteria: WCAG 2.2 2.1.1 Keyboard, 2.1.2 No Keyboard Trap, 2.1.4 Character Key Shortcuts, 2.5.7 Dragging Movements.
* Workbench controls use native `<button>`, `<a href>`, `<input>`, `<select>`, `<textarea>`, `<details><summary>`, `<dialog>`, and `[popover="auto"]` elements across `app.js`, `panels.js`, `ops.js`, `assistants.js`, `progress.js`, `role-screens.js`, `staff-intake.js`, `aftercare.js`, `timecapture.js`, and `simulator-control.js`.
* `CaseWorkspace` (`case-workspace.js`) implements roving `tabIndex` (`0` active, `-1` inactive) on `[role="tablist"]` with `ArrowRight`, `ArrowLeft`, `Home`, and `End` keyboard navigation, while `[role="tabpanel"]` containers carry `tabindex="0"`.
* `mapPanel` (`app.js`) exposes keyboard pan (`ArrowLeft`, `ArrowRight`, `ArrowUp`, `ArrowDown`) and zoom (`+`, `=`, `-`) on `#leaflet`, enables `keyboard: true` on Leaflet markers with explicit `Enter` and `Space` activation (`mapAction`), dismisses the open home summary card first on `Escape` (restoring focus to the originating marker or `#leaflet`), and closes the expanded `<dialog class="map-dialog">` on `Escape` (restoring focus to the `Expand map` toggle) with no keyboard trap.
* `chat-widget.js` closes the docked or floating chat panel on `Escape` and returns focus to `#employee-chat-launcher`. No script binds single-character shortcuts or drag-only (`draggable`, `dragstart`, `mousedown`, `touchstart`) handlers.

### 2. Focus order and visibility

* Criteria: WCAG 2.2 2.4.1 Bypass Blocks, 2.4.3 Focus Order, 2.4.7 Focus Visible, 2.4.11 Focus Not Obscured (Minimum).
* Both `index.html` (`<a class="skip-link" href="#app">Skip to main content</a>`) and `welcome.html` (`<a class="skip-link" href="#welcome-main">Skip to main content</a>`) place a visible-on-focus skip link first in DOM order targeting `<main tabindex="-1">`. Specialist role screens (`role-screens.js`) and the coordinator workspace (`app.js`) also render `nav[aria-label]` keyboard jump links targeting section headings with `tabindex="-1"`.
* Route transitions in `app.js` focus `<main id="app">`; case-summary action buttons (`Open next action`, `See all blockers`, `Review AI suggestions`) select the target tab and move focus to its `<h2>`; validation failures move focus to the first invalid control (`focus()`).
* `style.css` defines one global two-tone `:focus-visible` indicator (`outline: var(--focus-w) solid var(--focus-ink); outline-offset: var(--focus-off); box-shadow: 0 0 0 var(--focus-off) var(--focus)`) pairing a `3px` `#1f2933` outline (`14.5:1` against `#ffffff`) with a `2px` `#f2a900` outer ring (`6.5:1` against `--brand-d` `#08434d`), and `.table-scroll:focus-visible` draws an inset two-tone ring so scrollable table regions never clip focus outlines. Zero `outline: none` or `outline: 0` rules exist in CSS.
* `html { scroll-padding-block-end: 6rem }` clears the only two `position: fixed` rules in `web/*.css` (`.chat-widget-launcher` `3.5rem` plus inset and `.chat-widget` in `chat-widget.css`).

### 3. Name, role, value, and non-colour cues

* Criteria: WCAG 2.2 1.1.1 Non-text Content, 1.3.1 Info and Relationships, 1.4.1 Use of Color, 4.1.2 Name, Role, Value.
* Pages expose semantic `<header>`, `<nav aria-label="Workbench">`, `<main>`, `<section>`, `<aside>`, and `<form>` landmarks. Generated controls pair explicit `<label for>` elements or `aria-label` attributes with native inputs.
* Stateful widgets maintain synchronized ARIA state and text cues: Overview filter tiles toggle `aria-pressed` alongside visible `"Selected"` / `"Select filter"` text; the map modal button toggles `aria-expanded` and `"Expand map"` / `"Exit expanded map"`; case tabs sync `aria-selected` and `aria-controls`; both the six-step case stepper (`case-workspace.js`) and the eight-stage home journey map (`role-screens.js`) set `aria-current="step"` alongside plain-text state words.
* Non-colour status signals are enforced across CSS and JS: map markers combine distinct SVG shapes with letter codes (`circle` / `O` for `Normal`, `rect` / `W` for `Waiting 60+ days`, `triangle` / `!` for `Safety issue open`), map clusters print `Safety: N`, `role-screens.js` prepends plain-text prefixes via `stateCue`, CSS status banners prepend `:before` glyphs (`\26A0`, `\2713`, `\25B2`) and double borders, and `@media (forced-colors: active)` preserves high-contrast borders and strokes.

### 4. Status messages

* Criteria: WCAG 2.2 4.1.3 Status Messages.
* `index.html` provides persistent polite status regions (`#startup-status`, `#workspace-status`, `#photo-status` with `role="status"` and `aria-live="polite"`) and an assertive account error region (`#account-error` with `role="alert"`).
* Dynamic views announce state changes without stealing focus: `AsyncAction.feedback` (`async-action.js`) writes polite busy and completion announcements; `mapPanel` (`app.js`) updates `info` (`role="status"`, `aria-live="polite"`, promoted to `role="alert"` on map fetch failure) and `tileNote` (polite fallback notice when background map tiles fail); `CaseWorkspace` updates `[data-case-ai-count]` (`role="status"`, `aria-live="polite"`, `aria-atomic="true"`); `ProgressViews` (`progress.js`) announces loading, active date ranges, and `#closed-results` pagination counts via `role="status"`; `role-screens.js` announces 50-row truncation notices and saved-copy freshness check outcomes via `role="status"`; `aftercare.js` announces receipt confirmation via `role="status"`; `chat-widget.js` exposes polite transcript/status regions and error alerts. Screen-reader announcement timing remains a manual gate (`AC-034`, `#155`).

### 5. Contrast

* Criteria: WCAG 2.2 1.4.3 Contrast (Minimum), 1.4.11 Non-text Contrast.
* Text token pairs in `style.css` exceed the `4.5:1` AA minimum (`--ink` `#242424` on `--surface` `#ffffff` `15.4:1` and `--bg` `#f5f7f8` `14.5:1`; `--muted` `#424242` on `--surface` `10.4:1` and `--bg` `9.5:1`; `--surface` on `--brand` `#0b5d6b` `7.5:1` and `--brand-d` `#08434d` `10.9:1`; `--warn` `#b42318` on `--warn-bg` `#fde8e6` `5.6:1`; `--ok` `#1a6b3a` on `--ok-bg` `#e6f4ea` `5.8:1`; `--ink` on `--caution-bg` `#fff8e1` `14.8:1`). `.focus dt` uses `var(--muted)` rather than raw hex overrides.
* Non-text UI boundaries exceed `3.0:1` (`--field-line` `#7a858d` on `--surface` `3.77:1`; `--focus-ink` `#1f2933` on `--surface` `14.5:1`; `--brand` and `--warn` outlines `>= 5.6:1`). Gap `G-2` remains documented for `--caution` `#d98a00` (`2.61:1` on tint), mitigated by `--focus-ink` stroke on `.map-symbol.long svg`, letter code `W`, and plain-text status labels.

### 6. Reflow and zoom

* Criteria: WCAG 2.2 1.4.4 Resize Text, 1.4.10 Reflow.
* `index.html`, `welcome.html`, and `law.html` declare `lang="en-GB"` and `<meta name="viewport" content="width=device-width, initial-scale=1">` with no `maximum-scale` or `user-scalable=no` locks. Typography uses `rem` tokens and `clamp()` so 200% browser text zoom scales cleanly.
* `style.css`, `progress.css`, and `chat-widget.css` collapse multi-column layouts across `@media (max-width: 1199px)`, `1100px`, `900px`, `899px`, `700px`, and `600px` with `min-width: 0`, `overflow-wrap: anywhere`, and zero horizontal-locking `min-width >= 360px` rules so prose, forms, cards, and modals reflow down to `320 CSS px` (400% zoom from `1280 CSS px`). `@media (prefers-reduced-motion: reduce)` zeroes `--motion` and disables spinner rotation.
* All 15 script-built data tables sit inside `.table-scroll` (`max-width: 100%; overflow-x: auto`, `role="region"`, `tabindex="0"`, `aria-label`) so multi-column relational tables scroll horizontally within their own focusable container (WCAG 1.4.10 two-dimensional data exception) rather than introducing page-level horizontal scrollbars.

### 7. Target size

* Criteria: WCAG 2.2 2.5.8 Target Size (Minimum).
* Primary buttons and `.btn` links enforce `min-height: 2.5rem` (`40 CSS px`); `.chat-widget-launcher` enforces `min-width: 3.5rem; min-height: 3.5rem` (`56x56 CSS px`); `.leafmap .leaflet-bar a` and `.leafmap.leaflet-touch .leaflet-bar a` enforce `2.5rem x 2.5rem` (`40x40 CSS px`); `.map-home-close` enforces `min-width: 2.5rem`; `.chat-widget summary` enforces `min-height: 2rem` (`32 CSS px`).
* Compact interactive controls enforce at least `1.5rem` (`24 CSS px`), meeting the 24x24 CSS px AA minimum: `details > summary`, `.chart-data summary`, `.maplist summary`, `.regulatory summary`, `.linkbtn`, `.coordinator table a`, and `input[type=checkbox], input[type=radio]` (`min-width: 1.5rem; min-height: 1.5rem`).

### 8. Error identification

* Criteria: WCAG 2.2 3.3.1 Error Identification, 3.3.3 Error Suggestion.
* All nine script sites that set `setAttribute("aria-invalid", "true")` (`app.js` AI draft-review reason and `#/exceptions` recovery audit reason; `assistants.js` assistant input validation; `ops.js` quality remediation note, package contract version, and `opsOwned` `oninvalid` controls; `panels.js` nomination and challenge route inputs; `progress.js` `start`/`end` UTC filter inputs; and `role-screens.js` `fundingSavedCopyCheck` file input) pair the invalid control via `aria-describedby` with a visible `.field-error` or `.err` live message (`role="status"` or `role="alert"`), prepend a non-colour warning glyph (`.err:not(:empty):before` / `.field-error`), state what failed alongside the named owner and next action, and move keyboard focus to the invalid field.

## Accessible equivalents for maps, charts, and tables (#119, #151)

Every visual spatial, distribution, or stage-progression surface in the workbench exposes a synchronized, keyboard-reachable, screen-reader-accessible equivalent:

| Visual surface | Module and route | Accessible equivalent and synchronization contract |
| --- | --- | --- |
| Map of open cases (Leaflet cluster and home markers) | `app.js` (`mapPanel` on Overview `#/` and `#/coordinator`) | `<div id="leaflet" role="region" tabindex="0">`, polite `info` and `tileNote` status lines, shape-and-letter markers (`O`, `W`, `!`), and `<details class="maplist">` (`Show the map areas as a list (keyboard and screen reader friendly)`). `renderList()` synchronizes on every filter or viewport update: `clusters` mode renders `<button class="linkbtn">` items naming home count, open safety issues, and `"Zoom in to this area"`; `points` mode renders `#/case/<id>` links naming the home and plain-text `MAP_SIGNALS` status; zero mapped items reveal `<p class="muted" data-maplist-empty>` directing users to `"Show these as a list"` for all selected cases including ungeocoded homes |
| Overview SVG horizontal bar charts (`Cases by stage`, `Cases by local authority`, `How long cases have waited`, `Cases by wave`, `Funding status`) | `app.js` (`bars()` on Overview `#/`) | Each `<svg class="chart" role="img" aria-label="<title>">` is paired in the same card with `<details class="chart-data">`, a disambiguated `<summary>` (`Show this chart as a table` plus `.sr-only` `: <title>`), and a focusable `.table-scroll` (`role="region"`, `tabindex="0"`, `aria-label="<title> table"`) wrapping `<table>` with `<caption class="sr-only">`, `<th scope="col">` (`Group`, `Cases`), `<th scope="row">` per group, exact count parity, and `"No cases recorded."` when empty |
| Progress dashboard `<meter>` distribution and trend charts (six charts including multi-series daily/weekly flow, backlog trend, journey steps, team workload, and AI review outcomes) | `progress.js` (`ProgressViews.dashboard()` on `#/progress`) | Visual bar stacks sit inside `div.progress-bars[aria-hidden="true"]` with `tabindex="-1"` and series-qualified `aria-label` (`<row>, <series>: <count> (highest shown: <max>)`) on every `<meter>`, paired immediately with `<details><summary>Show <title> as a table</summary>` wrapping `ProgressViews` `table()` (`div.table-scroll[role="region"][tabindex=0]`, `<caption>`, `<th scope="col">`, `<th scope="row">`, formatted numeric cells, and `"No recorded data for this view."` when empty) |
| Coordinator stage heatmap and lifecycle funnel | `app.js` (`coordinatorView` on `#/coordinator`) | Rendered natively as semantic `<table>` elements inside focusable `.table-scroll` regions with visible captions, `<th scope="col">`, `<th scope="row">`, plain-text `Present` / `None` / `Unknown` state badges (`data-state-cue`), and keyboard links to filter the underlying `#coordinator-records` table |
| Case lifecycle steppers (six-step case header and eight-stage role-screen home stage map) | `case-workspace.js` (`CaseWorkspace.enhance`) and `role-screens.js` (`Eight journey stages for <home>`) | Semantic `<nav><ol>` ordered lists with decorative icons hidden (`alt=""`, `aria-hidden="true"`), `aria-current="step"` on the active stage, and explicit plain-text stage states (`Done`, `Current`, `Current, blocked`, `Blocked`, `Not started`, `Earlier step not confirmed`) plus native `[popover="auto"]` blocker disclosures |
| Fifteen script-built data table builders (`handoffWaitingView`, `exceptionsView`, `bars`, `coordinatorView`, `overviewView` Contractors and Team workload, `fundingView` in `app.js`; `technicalPanel`, `residentPanel`, `financeQueueView` in `panels.js`; `sensorTable`, `packagesView` in `ops.js`; `table` in `progress.js`; cohort evaluator in `aftercare.js`; `screenTable` in `role-screens.js`) | `app.js`, `panels.js`, `ops.js`, `progress.js`, `aftercare.js`, `role-screens.js` (also consumed by `staff-intake.js`) | All 15 builders wrap `<table>` in `.table-scroll` (`role="region"`, `tabindex="0"`, `aria-label`), provide a first-child `<caption>`, mark every header cell with `<th scope="col">`, and mark row-identifying first cells with `<th scope="row">` |

## Recorded gaps

* `G-1`: Live assistive-technology, screen-reader (NVDA/VoiceOver), 200% text resize, 400% zoom/reflow, and rendered pointer target-size walkthroughs with disabled users and staff roles remain `Not run` (`#151`, `#155`, `#619`).
* `G-2`: `--caution` (`#d98a00`) measures `2.61:1` on `--caution-bg`; mitigated in the workbench by `--focus-ink` SVG stroke, letter code `W`, and plain-text status labels.
* `G-3`: Third-party map tile imagery and vendored `vendor/leaflet.js` / `vendor/leaflet.css` internals remain outside direct source ownership; the workbench overrides `.leaflet-bar a` to `2.5rem x 2.5rem` (`40x40 CSS px`) and provides the synchronized `.maplist` equivalent.
* `/law.html` standalone legal register helper: declares `lang="en-GB"` and zoom-permitting viewport meta (`test_accessibility_baseline.py`), but lacks a `.skip-link` bypass anchor before `#law` and displays unreviewed local regulatory reference copies outside the signed-in case workbench scope.

## Automated checks

`src/api/tests/test_accessibility_baseline.py` and `src/api/tests/test_wcag_workbench_baseline_151.py` run with the existing unit test
discovery in `.github/workflows/mvp-ci.yml` and `.github/workflows/src-ci.yml`. Together they check page language and
viewport across `index.html`, `welcome.html`, and `law.html`, the contrast ratios above, the two-tone focus indicator and fixed-launcher scroll padding, target-size rules, all nine `aria-invalid` error-identification sites, all 15 captioned and `.table-scroll`-wrapped table builders with `<th scope="col">` and `<th scope="row">`, Node-VM DOM parity for `bars()`, `mapPanel()` (`clusters`, `points`, and empty-list `[data-maplist-empty]` states), and `ProgressViews` `<meter>` labels and table disclosures, and that this record
exists and makes no conformance claim. These are static and constructed-DOM checks, not a rendered-page scan or assistive-technology run.

Status at 2026-11-03: rendered axe-core 4.10.3 scans now run in the opt-in
role-screen browser checks and in `.github/workflows/src-ci.yml` for the regulatory and case journey screens
(see the per-screen PRs under #226 to #233); they do not cover every screen or
WCAG criterion. Original note: rendered-page scanning against key screens (axe-core through the existing
Playwright `src/api/checks/browser_check.py`) is not added: the browser check is a
manual script and the dependency choice needs the owner (O-2).

## Manual check record

Each cell holds Not run, or tester, date, tool and browser versions, criteria
checked, result and exceptions. Use one screen reader per OS, keyboard only,
at 320, 390 and 1280 px and 200% text size.

| Role workflow | Keyboard only | Screen reader | Zoom and reflow | Result |
| --- | --- | --- | --- | --- |
| Retrofit Coordinator | Not run | Not run | Not run | Not run |
| Resident Liaison Officer | Not run | Not run | Not run | Not run |
| Building Safety Liaison | Not run | Not run | Not run | Not run |
| Grants and Evidence Officer | Not run | Not run | Not run | Not run |
| Quality Inspector | Not run | Not run | Not run | Not run |
| Retrofit Programme Manager | Not run | Not run | Not run | Not run |
| Programme Support Officer | Not run | Not run | Not run | Not run |
| Contractor view | Not run | Not run | Not run | Not run |

Release rule (proposed, O-3): a release that changes a screen needs the
affected rows re-run and any new failure recorded or fixed.

## Production acceptance for the chat widget and case view (#619)

The production-build screen reader, keyboard, zoom and resident consent
acceptance for the shared chat widget and the single case view has its own
[protocol and blank record](./production-ux-acceptance-protocol.md). Every row
is `Not run` at 2026-11-02; gap G-1 stays open.

## Proposed resident task audit (2026-10-23, #441)

This prospective extension covers the six
[synthetic resident scripts](./customer-journeys/residents.md#proposed-optional-resident-increment-2026-10-23-441),
not an implemented portal, changed historic staff audit or fresh conformance
claim. Existing gaps and manual records above remain. Reuse the proposed
WCAG 2.2 AA engineering target, keyboard and accessible names/status/errors,
320/390/1280 CSS px, 200% text resize and 400% zoom/reflow where applicable.
Test password-manager/paste support and accessible recovery without cognitive
tests, shared-device/session clearing, safe revoked-grant errors, upload
progress/failure, source/as-of/unknown and independently reachable human help.
Third-party identity/file surfaces need end-to-end task assessment, not a
blanket exemption because provider internals are external.

| Proposed task | Keyboard | Screen reader | Resize/reflow | Task result |
| --- | --- | --- | --- | --- |
| Sign-in/recovery and scoped grants | Not run | Not run | Not run | Not run |
| Own case and approved documents | Not run | Not run | Not run | Not run |
| Requested upload and receipt/checks | Not run | Not run | Not run | Not run |
| Appointment response, not confirmation | Not run | Not run | Not run | Not run |
| Grounded answer/unknown and human handoff | Not run | Not run | Not run | Not run |
| Assisted continuity without detriment | Not run | Not run | Not run | Not run |

Record exact build, tester/date, browser/AT versions, criteria, task success
and negative-state results. Direct accessible resident/representative research,
privacy/service approval and acceptance remain required, not supplied by
these proposed scripts or automated tests of the existing staff workbench.
No new legal/W3C-currentness check is claimed by this documentation change.

## Map list alternative screen-reader check (#119)

Status at 2026-10-20: Not run. The unmet gate is a human or assistive-technology
run of the map list alternative; it stays open and is not met by any engineering
check below.

Tools found on the 2026-10-20 local host (Linux, no display, no audio device):
no screen reader is installed (no NVDA, Orca, VoiceOver, JAWS, eSpeak or
speech-dispatcher); `at-spi2-core` is present only as a library. Chromium is
available through Playwright for engineering checks. No axe-core package is
installed. Installing a desktop screen reader on the shared headless host was
judged outside scope, so no screen-reader run was attempted and none is claimed.

Existing engineering evidence is not a screen-reader run. In `src/api`,
`test_charts_and_map_have_accessible_equivalents` only checks that the text
"Show the map areas as a list" is in the script, and `test_status_regions_exist`
only checks that status and alert roles and `aria-live` appear in the page
source. The opt-in real-browser test documented in the API guide for the
coordinator map list exercises a keyboard route through the list. None of
these shows what a screen reader announces, and none establishes accessible
names, focus order after refresh or live-region behaviour.

Protocol for the human run (tester records name, date, tool and browser
versions, and result in the table above or an attached record):

* Use NVDA with Firefox on Windows or VoiceOver with Safari on macOS, with a
  synthetic-data session only, at 1280 px and 320 px and 200 percent text.
* Open Overview, find the map region, then the "Show the map areas as a list"
  disclosure. Check that it is discoverable by heading, landmark or form
  navigation, that its name is announced, and that it opens and closes with
  Enter or Space.
* At low zoom, check each cluster button announces count and safety count and
  "Zoom in to this area", that activating it moves the view, and that focus
  returns to the disclosure summary as designed.
* At high zoom, check each home link announces name and the non-colour signal
  label and opens the case.
* Check the polite status line announces results after a filter or pan, and
  the alert is announced when the map-data request fails (for example, block
  the map-data endpoint). Also block the tile images: since 2026-11-03 the map
  panel shows a polite status note ("The map background could not load. The
  homes and the list of map areas still work...") when a tile fails. Record
  whether the note is announced, once, and whether the list stays usable. The
  note is engineering-tested as present in the script only; what a screen
  reader announces is not established.
* Record anything unclear, such as focus loss after the list refreshes, as a
  finding, and do not treat a pass as WCAG conformance.

## Accessibility statement (draft)

Draft only. Not published and not approved; legal and owner review is needed
before use, and the public-sector accessibility regulations format should be
checked.

The Zava Forward workbench is an internal demonstrator that uses synthetic
data. We aim to meet WCAG 2.2 Level AA. We have not yet tested it with
assistive technology, so we do not claim conformance.

Known gaps at 2026-10-15:

* G-1: No screen reader, zoom, reflow or target size test has been completed.
* G-2: The caution map marker and the map marker shapes depend on colour; the
  key text and list alternative are the equivalent.
* G-3: Map tiles and the Leaflet library are third party and not assessed.
* G-4: Tables other than chart tables and sign-in were not fully audited; form
  error markup was inventoried by script inspection only, not with a screen reader.

To ask for another format or report a problem, contact: owner to supply (O-4).

## Programme screens status (2026-11-04, #230)

Criteria 1, 2, 3 and 5 of #230 are ticked on merged PRs #662, #781, #818, #854, #931 and #969. Criterion 4 (WCAG 2.2 baseline, textual state meaning, keyboard navigation) stays unmet: the automated keyboard and axe checks are merged, but manual WCAG 2.2 review and assistive-technology testing by named people are not done (#151, #155). Automated checks are not conformance evidence. No code slice can supply this.

## Resident engagement screens status (2026-11-13, #232)

Audit of the resident choice and update queue (`resident-choice`) and the resident service issue queue (`resident-service-issues`) for #232 criterion 4. Source read and rendered at 1280 and 320 px in Chromium; no screen-reader, voice-control or human testing.

* Fixed (1.3.1): the first column of every resident-screen table (home, measure, request, issue) is now a `th scope="row"` row header. Before, only column headers existed. Other screens' tables are unchanged.
* Fixed (textual state meaning): the service request table on the resident choice screen now shows "State and meaning" with the same plain-language meaning as the service issue screen, not a bare status word.
* Added checks: rendered header, caption and row-header assertions; a pinned axe 4.10.3 scan of the queue state with no home selected (previously only the selected-home state); Tab reach of every table region at 320 px for both screens. Unit tests assert the same table structure.
* Observed, no change needed: native links and no write or contact controls; skip link and focus on `main`; visible two-tone focus; captions and scoped column headers; status text for pause, withdrawal and commitment; no `aria-invalid` site added.
* Not tested: screen-reader output, table navigation by assistive technology, comprehension of the wording, other browsers. Axe `color-contrast` stays incomplete at 320 px on some states because axe cannot resolve the background; element overlap was checked and not found. The shared sidebar and panel headings use flat `h2` levels and are unchanged.

Automated results are engineering evidence on constructed data, not WCAG 2.2 conformance, assistive-technology acceptance or a tick of the #232 criterion, which only the owner can give. Human validation belongs to #155.

## Conversational assistant panel keyboard and live-region check (2026-11-15, #159)

Focused automated verification of the workbench conversational assistant surfaces (`#employee-chat-launcher` in `src/api/src/zava_forward/api/web/index.html`, `#employee-chat` in `src/api/src/zava_forward/api/web/chat-widget.js` and `src/api/src/zava_forward/api/web/chat.js`, `#chat-panel` inside `#case-panel-ai`, and `#workspace-status`) for #159 criterion 6 (`Panel is keyboard operable, screen-reader tested, and announces new messages`). Existing web scripts and styles already satisfied the engineering controls, so zero production web files were modified; `src/api/tests/test_assistant_panel_a11y_159.py` adds a dual-layer regression suite on constructed synthetic data:

* Unconditional Node-VM + real Python `ChatPanel` integration (`AssistantPanelNodeA11y159Tests`): drives `chat-widget.js` and `chat.js` against real backend `ChatPanel` turn payloads (`answer`, `refused`, `withheld` and `fallback`) and `Assistants.invoke` proposal payloads (`SqlStore` on synthetic `role_matrix_fixture` seed). Verifies keyboard submission (`Enter`), `Shift+Enter` non-submission (`!defaultPrevented`), IME composition guard (`isComposing` and `keyCode === 229`), `Escape` close with un-hide-before-focus when docked, focus preservation when focus starts on `Send`, `role="log"`, `Sources (N)` or an external page control, blank-question error recovery to `#employee-chat-question`, `401`/`403` `deny()` focus recovery to `#app`, `revealBeside` vertical and horizontal `scrollBy` deltas, and polite live-region text mutations across `role="log"`, `role="status"`, `role="alert"`, `#chat-panel > p[role="status"]` and `#workspace-status`.
* Rendered headless Chromium + CDP accessibility tree and live-region suite (`AssistantPanelBrowserA11y159Tests`): serves the real `App` on loopback (`127.0.0.1`, outbound routes aborted, ambient `ZF_SIM_STORE` / `ZF_SIM_KEY_FILE` cleared) and drives keyboard-only workflows (`Tab`, `Shift+Tab`, `Enter`, `Space`, `Shift+Enter`, `ArrowDown`, `ArrowRight`, `Escape`) in separate non-case launcher and `#/case/ZF-1?tab=ai` case-scoped sessions. Verifies the 3px two-tone `:focus-visible` indicator, forward (`Tab` past `Send`) and backward (`Shift+Tab` before `Close chat`) panel exit without focus trap, keyboard `Close chat` activation, `About this chat` and `Chat size` disclosures, `Dock to right edge` toggle (`aria-pressed`), width and height range sliders (`#employee-chat-width`, `#employee-chat-height`), rendered `revealBeside` vertical and horizontal bounding-box scroll clearance, keyboard `#employee-chat-skill` selection (`ArrowDown`) submitted via `Enter` from `#employee-chat-question` (`Skill:` attribution) plus separate `Enter` submission from `Send`, explicit `Shift+Enter` `"\n"` insertion, case-tab `Open chat` and `Request proposal` actions, `Sources (N)` disclosure expansion, non-auth `500` error alert with preserved unsent draft, `403` `deny()` access-loss reset (`#workspace-status` `"Chat access ended. Reopen from a record you can see, or sign in again."` and focus `#app`), `401` `app.js` session-expiry interception (sign-in `role="alert"` `"Your session has ended. Sign in again."` and focus `#app`), Chromium CDP `Accessibility.getFullAXTree` roles/names/descriptions, `expanded` (`False` / `True` on `"Chat"` and `"Chat size"`), `pressed` (`"false"` / `"true"` on `"Dock to right edge"`) and live properties (`live: "polite"`, `atomic: true`, `relevant: "additions"`), and `MutationObserver`-captured live-region announcements including post-`403` `#workspace-status` and post-`401` sign-in `role="alert"`.
* Not tested and still open: human desktop screen-reader execution (NVDA with Firefox on Windows and VoiceOver with Safari on macOS), voice control, 320 px reflow and 400% zoom with the panel open, and multi-role human walkthroughs under [production-ux-acceptance-protocol.md](./production-ux-acceptance-protocol.md) (#151, #155, #619). Automated browser accessibility-tree and DOM live-region checks do not establish what desktop assistive technology speaks aloud, so no WCAG 2.2 conformance claim is made and #159 criterion 6 awaits owner/human screen-reader acceptance before closing #159.

## UX epic status (2026-11-04, #149)

Delivered as engineering evidence: #150 is closed; #496 added the scoped specialist screen foundation; #152, #153, #154, #155 and #156 have merged slices (for example #813, #1016, #1002, #1079, #712, #1004, #811) and tick the criteria those slices prove. #151 has merged CI axe checks, a target-size fix (#857) and a form error guard (#1000).

Unmet epic criteria:

* Stabilization checkpoint (#440): its triage and artifact criteria are still open, and merged children do not satisfy it.
* Child features are accepted: 15 of 16 children are open; #151 to #156 and #225 to #233 each keep unmet criteria.
* Accessibility, content and usability evidence recorded as test results: manual screen-reader and keyboard checks, a named-human copy review and tests with representative users are not done. Synthetic walkthroughs are not user validation.
* Design artefacts traceable to journeys and requirements: partly met; #156 still lacks per-feature links for every screen.

Remaining steps need owner decisions (supported devices, WCAG level, release rule) and named human testers, so no code slice is possible. Nothing was ticked or closed.

## Open items

* O-1: Owner confirms the target level and scope.
* O-2: Owner chooses the rendered-page scanner for CI (axe-core suggested).
* O-3: Owner confirms the release rule and names manual testers, including
  people who use assistive technology.
* O-4: Contact route and enforcement or escalation wording for the statement.
* O-5: Re-retrieve WCAG 2.2 and any applicable accessibility regulation from
  the official source before external use.
