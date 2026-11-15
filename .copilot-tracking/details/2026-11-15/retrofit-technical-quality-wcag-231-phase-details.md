<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #231 Retrofit Technical and Quality Screens WCAG 2.2 Baseline

## Metadata

* Task ID: 2026-11-15-retrofit-technical-quality-wcag-231
* Task slug: retrofit-technical-quality-wcag-231
* Related plan: .copilot-tracking/plans/2026-11-15/retrofit-technical-quality-wcag-231-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/retrofit-technical-quality-wcag-231-research.md, docs/reference/research/ux/wcag-conformance-baseline.md, docs/reference/research/ux/design-system.md, docs/reference/research/ux/content-standard.md

## Phase Index

| Phase ID | Name                                                               | Status | Detail sections        |
|----------|--------------------------------------------------------------------|--------|------------------------|
| P01      | Keyboard Section Navigation, Focus Styling, and Table Semantics    | ready  | P01, P01-T01, P01-T02  |
| P02      | Explicit Non-Colour Textual State Cues and Fluent 2 Banners        | ready  | P02, P02-T01           |
| P03      | Focused WCAG 2.2 Test Suite, Baseline Verification, Web Guidelines | ready  | P03, P03-T01           |

<!-- rpi:phase id=P01 -->
## P01: Keyboard Section Navigation, Focus Styling, and Table Semantics

### Context

Research (`C1`–`C4`, `C6`, `C11`, `C16`) established that `technical-queue` renders `<nav class="screen-links"><ul><li><a href="#${id}">` without `data-jump` (causing clicks/Enter to rewrite `location.hash` and navigate out of `#/screens?...` in `app.js`, and breaking `.screen-links` flex layout via `<ul>`), while `quality-queue` has no `nav.screen-links` or anchored `<section>`/`<h2 tabindex="-1">` targets at all. In addition, all five tables across both screens call `screenTable` rather than `screenRecordTable`, omitting `<th scope="row">` row headers, and programmatic `.focus()` on `<h2 tabindex="-1">` lacks an explicit `:focus` rule in `style.css` when triggered by pointer click.

### Intent

Provide consistent, SPA-safe `nav.screen-links` jump navigation, labelled `<section>` landmarks, programmatically focusable `<h2>` headings with visible Fluent 2 focus rings, and `<th scope="row">` table semantics across both `technical-queue` and `quality-queue`.

### Boundaries

* Included: `pasJumpNav` helper, `technicalSections` (including `technical-boundary`), `qualityRecordAnchor` and dynamic `qualitySections`, `screenRecordTable` upgrades in `role-screens.js`, and `:focus` / `tabular-nums` rules in `style.css`.
* Excluded: Changing `app.js` routing, changing `h("table", {}, ...)` literal count in `role-screens.js`, or adding any CSS `transition`/`animation` to `.screen-*`.

### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`: Jump nav helper, section anchors on `technical-queue` and `quality-queue`, and `screenRecordTable` calls.
* `src/api/src/zava_forward/api/web/style.css`: `.screen-record h2[tabindex="-1"]:focus` focus indicator and `.screen-evidence th` `tabular-nums`.

### Dependencies

* None.

### Validation Expectations

* `test_assessor_screen_wcag.py`, `test_role_screens_conformance.py`, `test_design_system.py`, `test_connected_home_check.py`, and `test_specialist_keyboard_check.py` pass without regressions.

### Completion Evidence

* Rendered trees for `technical-queue` and `quality-queue` show direct `<a href="#${id}" data-jump="${id}-heading" data-jump-target="${id}-heading">` links matching every `<section id="${id}" aria-labelledby="${id}-heading">` and `<h2 id="${id}-heading" tabindex="-1">`, and every table body row starts with `<th scope="row">`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Upgrade `technical-queue` and `quality-queue` jump navigation, section anchors, and `screenRecordTable` semantics in `role-screens.js`

#### Context

`test_assessor_screen_wcag.py` (`C11`) asserts `nav["attrs"]["aria-label"] == "Sections on this screen"` and `{a["attrs"]["href"][1:] for a in walk(nav) if a["tag"] == "a"} == {s["attrs"]["id"] for s in sections_with_id}` on `technical-queue`, while `role-screens.js`'s delegated click listener (`C4`) reads `link.getAttribute("data-jump")` to focus `document.getElementById(...)` and call `scrollIntoView({ block: "start" })`. `test_connected_home_check.py` (`C14`) statically checks literal `screenPanel("...", ...)` titles and forbids home-field reads in `"Evidence boundary"`. `specialist_keyboard_browser_check.py` (`C13`) requires `"Sign-off validity after design changes"` on `technical-queue` and zero tables on `quality-queue` when `records` is empty.

#### Intent

Wire `pasJumpNav` and section anchors cleanly across all substantive panels of `technical-queue` and `quality-queue`, and upgrade all five tables to `screenRecordTable`.

#### Boundaries

* Included:
  * Define `pasJumpNav(sections)` emitting `h("nav", { "aria-label": "Sections on this screen", class: "screen-links" }, sections.map(([id, label]) => h("a", { href: `#${id}`, "data-jump": `${id}-heading`, "data-jump-target": `${id}-heading` }, label)))`.
  * On `technical-queue`, anchor `"Evidence boundary"` with `{ anchor: "technical-boundary" }` and include `["technical-boundary", "Evidence boundary"]` first in `technicalSections` alongside `technical-readiness`, `technical-source-facts`, `technical-design`, `technical-signoffs`, `technical-returns`, and `technical-missing` (leaving `screenWithheld` un-anchored so `targets == set(sections)` holds identically).
  * On `quality-queue`, define `qualityRecordAnchor(r, index)` (`quality-measure-${String(screenValue(r.measure)).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "item"}-${index + 1}`), build `qualitySections` with `["quality-boundary", "Evidence boundary"]`, `["quality-readiness", "Handover readiness"]`, and either `records.map((r, i) => [qualityRecordAnchor(r, i), `${screenValue(r.measure)}: ${screenValue(r.state)}`])` when `records.length` is non-zero or `[["quality-evidence", "Quality evidence"]]` when empty, pass matching `{ anchor: ... }` objects to each `screenPanel(...)`, and render `pasJumpNav(qualitySections)` at top of `quality-queue`.
  * Switch the 4 `screenTable(...)` calls in `technical-queue` and the 1 `screenTable(...)` call in `quality-queue` to `screenRecordTable(...)`.
* Excluded: Modifying `screenWithheld` or adding tables when `records` is empty.

#### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`: `technicalSections`, `technical-queue`, `quality-queue`.

#### Dependencies

* None.

#### Validation Expectations

* Node VM checks confirm `targets == set(sections)` on both screens (with 0, 1, and multiple duplicate-named quality measures), delegated click calls `preventDefault()` and focuses `${id}-heading`, and all 5 tables render `<th scope="row">`.

#### Completion Evidence

* Diff in `role-screens.js` and passing `test_assessor_screen_wcag.py` + `test_connected_home_check.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add programmatic heading `:focus-visible` ring and `<th scope="row">` tabular-nums rule in `style.css`

#### Context

In `style.css` (`C6`, `C10`), `:focus-visible` provides the Fluent 2 dual-ring indicator, and `.screen-evidence td` sets `font-variant-numeric: tabular-nums`. When `a[data-jump]` triggers `heading.focus({ preventScroll: true })` from keyboard activation (`Enter`), Chromium matches `:focus-visible` on `<h2 tabindex="-1">` while avoiding unwanted click focus rings (`W1` Web Interface Guidelines). `test_role_screens_conformance.py` (`C10`) inspects every `^\.screen-[^{]*\{[^}]*\}` rule and forbids `animation` and `transition`.

#### Intent

Ensure keyboard-triggered programmatic heading focus displays the high-contrast Fluent 2 focus ring and row-header cells keep tabular figure alignment.

#### Boundaries

* Included: Add `.screen-record h2[tabindex="-1"]:focus-visible { outline: var(--focus-w) solid var(--focus-ink); outline-offset: var(--focus-off); box-shadow: 0 0 0 var(--focus-off) var(--focus); }` and extend `.screen-evidence th, .screen-evidence td { font-variant-numeric: tabular-nums; }` in `style.css`.
* Excluded: Any new CSS custom properties (`test_design_system.py` requires every `--*` token in `:root` to be documented) or any `transition`/`animation` in `.screen-*`.

#### Likely Targets

* `src/api/src/zava_forward/api/web/style.css`: Specialist screen rule block at end of file.

#### Dependencies

* None.

#### Validation Expectations

* `test_design_system.py` and `test_role_screens_conformance.py` pass cleanly.

#### Completion Evidence

* Updated `style.css` verified by unit and CSS-guard assertions.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Explicit Non-Colour Textual State Cues and Fluent 2 Readiness Banners

### Context

Research (`C2`, `C3`, `C5`, `C8`, `C12`, `C14`–`C16`) identified every remaining state surface on `technical-queue` and `quality-queue` where status meaning was unprefixed, relied on bare `class: "ok"`, or marked non-independently accepted check rows as `"Verified"`.

### Intent

Provide unambiguous, plain-language textual prefixes (`Verified:`, `Recorded:`, `Pending review:`, `Withdrawn:`, `Action needed:`, `Ready on record:`) and documented `.status-line.ok` readiness banners across both screens without breaking any pinned field value, substring, or plain-language vocabulary rule.

### Boundaries

* Included: `Evidence boundary` non-colour state explanation, `.status-line.ok` on both ready banners, `Source facts` `stateCue(assetConflictCues, ...)`, `Design version` `Design state` row, `Missing references` and `Returns and routing` `State` columns, `qualityMeasureCues` / `qualityMeasureState(r)`, `!qualityAcceptanceGap(r)` guard on per-check `"Verified: Evidence noted"`, ownerless `Defect owner` `Action needed:` cue, and `Reinspection state` row.
* Excluded: Using banned internal words (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`) or altering exact `<dd>` values of `Current design version`, `Recorded by`, `Submitted by`, `Accepted by`, `Handed over by`, or `Reinspection` (`"Passed"`).

### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`: `technical-queue` and `quality-queue` state helpers and panel definitions.

### Dependencies

* P01.

### Validation Expectations

* `test_technical_quality_screens.py`, `test_assessor_screen_wcag.py`, `test_learning_test_bundle_scenarios.py`, `test_content_standard.py`, `test_design_system.py`, and `test_connected_home_check.py` pass without regressions.

### Completion Evidence

* Every status cell, state field, and readiness banner on `technical-queue` and `quality-queue` renders an explicit plain-text prefix verified under normal, incomplete, non-independent, and prototype-key inputs.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Complete `Object.hasOwn`-safe textual state cues and `.status-line.ok` readiness banners on `technical-queue` and `quality-queue`

#### Context

See Research `C2`, `C3`, `C5`, `C8`, `C12`, `C14`–`C16`:
* `Evidence boundary` panels in `test_connected_home_check.py` (`C14`) may only read `c.id` and constant literals. Adding a constant literal paragraph `"Every state on this screen is written in words first; colour is never the only signal."` introduces zero case-field reads.
* Positive readiness `<p role="status">` elements in `role_screens_browser_check.py` (`C16`) are queried via `p.ok[role="status"]`; `class: "status-line ok"` satisfies both `p.ok[role="status"]` and Fluent 2 `.status-line.ok` (`✓ ` glyph + border/background tokens).
* `Current design version` `<dd>`, `Recorded by` `<dd>`, and `Reinspection` `"Passed"` `<dd>` are pinned by `atlas_tensions_browser_check.py`, `connected_home_browser_check.py`, and `test_technical_quality_screens.py`, so companion `<dt>`/`<dd>` rows (`Design state`, `Measure state`, `Reinspection state`) carry the prefixed cues cleanly.

#### Intent

Update `technical-queue` and `quality-queue` in `role-screens.js` so every state signal has explicit non-colour textual meaning and PAS 2035 independence integrity.

#### Boundaries

* Included:
  * In both `Evidence boundary` panels, add `h("p", {}, "Every state on this screen is written in words first; colour is never the only signal.")`.
  * Change both positive readiness `<p>` elements from `class: "ok"` to `class: "status-line ok"`, prefixing `technical-queue`'s ready banner with `"Ready on record: Recorded evidence is complete: every sign-off is valid, none is awaiting reassessment, and nothing is missing. This screen does not approve the stage."` (`quality-queue` already starts with `"Ready on record. Every measure has accepted evidence..."`).
  * In `technical-queue` `Source facts`, replace raw `assetStatus(c, q)` with `stateCue(assetConflictCues, assetStatus(c, q))`.
  * In `technical-queue` `Design version` (when `t` is truthy), prepend `["Design state", t.design_version !== null && t.design_version !== undefined && t.design_version !== "" && qualityName(t.design_name) ? `Recorded: Design version ${screenValue(t.design_version)} on record (not stage approval)` : "Action needed: Design record is incomplete"]` before `["Current design version", t.design_version]`.
  * In `technical-queue` `Returns and routing`, include `"State"` column (`["Sign-off", "State", "Route to", "Why", "Returned by"]`) populated with `evidenceLabel(x)`.
  * In `technical-queue` `Missing references`, include `"State"` column (`["Missing item", "State", "Owner"]`) populated with `"Action needed: Missing on record"`.
  * In `quality-queue`, add `qualityMeasureCues = { Submitted: "Pending review", Returned: "Action needed", "Fixed, awaiting reinspection": "Pending review", Accepted: "Verified", "Handed over": "Verified" }` and `qualityMeasureState(r)` returning `` `Action needed: ${screenValue(r.state)} (${gap})` `` when `(r.state === "Accepted" || r.state === "Handed over") && gap` (`gap = qualityAcceptanceGap(r)`), otherwise `stateCue(qualityMeasureCues, r.state)`. Prepend `["Measure state", qualityMeasureState(r)]` to each measure panel's top `screenFields([...])`.
  * In `quality-queue` `Per-check evidence for ${r.measure}`, compute `qualityCheckState(r, i)`: if `!String(i.evidence || "").trim()` return `"Action needed: No evidence"`; if `r.state === "Accepted" || r.state === "Handed over"` return `qualityAcceptanceGap(r) ? "Action needed: Evidence noted (acceptance incomplete)" : "Verified: Evidence noted"`; otherwise return `"Pending review: Evidence noted"`.
  * In `quality-queue` `r.defect` fields, render `["Defect owner", qualityName(r.defect.owner) ? r.defect.owner : "Action needed: Unassigned (no defect owner named)"]` and add `["Reinspection state", qualityReinspectionState(r)]` after `["Reinspection", ...]` where `qualityReinspectionState(r)` checks `r.state === "Fixed, awaiting reinspection"` first (`"Pending review: Awaiting independent reinspection"`), then checks `if (r.state === "Accepted" || r.state === "Handed over")` returning `qualityAcceptanceGap(r) ? "Action needed: Reinspection lacks independent named inspector" : "Verified: Independent reinspection passed"`, and returns `"Action needed: Not yet possible until fix is recorded"` otherwise.
  * Keep all UI strings and JS comments strictly plain ASCII (zero `\u2014` em dashes per `docs/reference/research/ux/content-standard.md:27`) and free of banned words scanned line-by-line by `test_content_standard.py` (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`).
* Excluded: Any banned vocabulary from `test_content_standard.py`, any `\u2014` Unicode em dashes, or undocumented CSS classes.

#### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`: `technical-queue` and `quality-queue` helpers and renderers.

#### Dependencies

* P01-T01.

#### Validation Expectations

* `test_content_standard.py`, `test_technical_quality_screens.py`, `test_assessor_screen_wcag.py`, `test_procurement_qa_screen_wcag.py`, `test_learning_test_bundle_scenarios.py`, and `test_connected_home_check.py` all pass.

#### Completion Evidence

* Updated `role-screens.js` passing all existing copy, conformance, and screen tests.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Focused WCAG 2.2 Test Suite, Baseline Guard Verification, and Web Guidelines Review

### Context

The caller requested focused WCAG 2.2 tests in `src/api/tests/test_technical_quality_screens_wcag.py`, verification of counted baseline guards (`test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_list_export_inventory.py`), `ruff check`, `ruff format --check`, `mypy`, compatibility with browser checks, and compliance with Web Development Guidance (`web-design-guidelines` refreshed before review with `file:line` audit).

### Intent

Lock in comprehensive automated verification for all new keyboard, focus, textual-state, table-semantics, and simulator-absence guarantees on `technical-queue` and `quality-queue`, and verify zero regressions across the Focused tier.

### Boundaries

* Included: Authoring `src/api/tests/test_technical_quality_screens_wcag.py`, running all targeted `unittest` suites, `ruff check`, `ruff format --check`, `mypy`, probing local browser checks (`specialist_keyboard_browser_check.py` / `role_screens_browser_check.py`), and performing a refreshed Web Interface Guidelines audit.
* Excluded: Modifying unrelated test files or inflating counted baseline guards.

### Likely Targets

* `src/api/tests/test_technical_quality_screens_wcag.py`: New focused WCAG 2.2 test module.

### Dependencies

* P01, P02.

### Validation Expectations

* All targeted unit/guard suites, `ruff check`, `ruff format --check`, and `mypy` pass with exit code `0`.

### Completion Evidence

* Recorded command outputs and refreshed Web Interface Guidelines check in `.copilot-tracking/changes/2026-11-15/retrofit-technical-quality-wcag-231-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Author `src/api/tests/test_technical_quality_screens_wcag.py` and run Focused-tier validation + refreshed Web Interface Guidelines audit

#### Context

Following the pattern in `test_ux_asset_executive_screens.py` (#226), `test_procurement_qa_screen_wcag.py` (#228), and `test_resident_screen_wcag.py` (#232), `test_technical_quality_screens_wcag.py` executes the real `role-screens.js` inside Node `vm` with a simulated `document` click-delegation harness and inspects `style.css`.

#### Intent

Prove every WCAG 2.2 engineering guarantee introduced in P01 and P02 with focused tests that would fail without our changes, then execute the full Focused validation battery.

#### Boundaries

* Included:
  * Test keyboard jump navigation and delegated click focus/scroll (`preventDefault`, `focus()`, `scrollIntoView({ block: "start" })`, missing-target safety, non-jump anchor ignored, dynamic duplicate-measure anchors on `quality-queue`, empty-quality anchor, `targets == set(sections)` on both screens, no `<button>` inside `nav.screen-links`).
  * Test CSS focus ring rules (`:focus-visible` and `.screen-record h2[tabindex="-1"]:focus-visible`) and absence of focus-outline removal or `.screen-*` motion.
  * Update `check_readonly_accessibility` and `run_browser` in `src/api/checks/role_screens_browser_check.py` to read `positive_text(page)` across `content-visibility: auto` `.screen-record` panels after bottom-scroll and run `check_design_system_use`, `check_table_headers`, and 320px `reach_table_regions` across `STORY_231` and `STORY_POSITIVE`.
  * Test non-colour textual state cues across:
    * `technical-queue` ready (`status-line ok`, `"Ready on record:"`) vs blocked (`"Cannot confirm readiness"`), `Source facts` (`Recorded:`, `Withdrawn:`, `Action needed:`, prototype status `"constructor"`), `Design state` (`Recorded:` vs incomplete `Action needed:`), `Separate sign-offs` and `Returns and routing` (`Verified:`, `Pending review:`, `Action needed:`, prototype status `"constructor"`), and `Missing references` (`Action needed: Missing on record`).
    * `quality-queue` ready (`status-line ok`, `"Ready on record."`) vs blocked, `Measure state` (`Pending review:`, `Action needed:`, `Verified:`, prototype state `"constructor"`, self-accepted / unnamed inspector downgraded to `Action needed:`), per-check `State` (`Verified: Evidence noted` only when accepted by an independent named person; `Action needed: Evidence noted (acceptance incomplete)` when self-accepted/unnamed; `Pending review: Evidence noted`; `Action needed: No evidence`), `Defect owner` (`Action needed: Unassigned` when blank/missing vs named owner preserved), `Reinspection state` (`Pending review:`, `Verified:` on independently accepted defect, `Action needed: Reinspection lacks independent named inspector` on non-independently accepted defect, and `Action needed: Not yet possible until fix is recorded` on open `Returned` defect while preserving exact `"Passed"` in `Reinspection`), and plain ASCII punctuation (`self.assertNotIn("\u2014", ...)` across rendered trees).
  * Test table semantics (`<caption>`, `<th scope="col">`, `<th scope="row">` on cell 0 of every body row, `div.table-scroll[role="region"][tabindex="0"]`) across all 5 tables, plus zero write controls (`button`, `input`, `select`, `textarea`, `form`), zero `onclick` / `aria-invalid`, and zero role simulator wording.
  * Run Focused-tier commands from `src/api`:
    * `PYTHONPATH=src:tests:../core/src:../agents/src:../orchestrator/src:../importer/src:../core/tests:../agents/tests python3 -B -m unittest tests/test_accessibility_baseline.py tests/test_epic149_form_error_summary_associations.py tests/test_list_export_inventory.py tests/test_technical_quality_screens_wcag.py tests/test_assessor_screen_wcag.py tests/test_technical_quality_screens.py tests/test_procurement_qa_screen_wcag.py tests/test_resident_screen_wcag.py tests/test_role_screens_conformance.py tests/test_role_screens.py tests/test_connected_home_check.py tests/test_specialist_keyboard_check.py tests/test_content_standard.py tests/test_design_system.py tests/test_learning_test_bundle_scenarios.py -v`
    * `ruff check src/ tests/ checks/` and `ruff format --check src/ tests/ checks/`
    * `mypy`
    * Probe browser checks via `-m checks.*` with worktree `PYTHONPATH` if Chromium is installed: `python3 -m checks.specialist_keyboard_browser_check`, `python3 -m checks.connected_home_browser_check`, `python3 -m checks.atlas_tensions_browser_check`, and `python3 -m checks.role_screens_browser_check` across default plus `231`, `231q`, `231p`, `231qp`.
    * Re-fetch `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` and audit `role-screens.js` and `style.css` against every rule.
* Excluded: Claiming manual screen-reader conformance.

#### Likely Targets

* `src/api/tests/test_technical_quality_screens_wcag.py`: Created test file.

#### Dependencies

* P01-T01, P01-T02, P02-T01.

#### Validation Expectations

* Zero test failures, zero ruff/mypy issues, zero Web Interface Guidelines violations.

#### Completion Evidence

* Recorded command exit statuses and outputs in `.copilot-tracking/changes/2026-11-15/retrofit-technical-quality-wcag-231-changes.md`.

#### Unresolved Items

* None.
