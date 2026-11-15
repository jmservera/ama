<!-- markdownlint-disable-file -->
# RPI Phase Details: Housing Officer and Resident Engagement Screens WCAG 2.2 Conformance (#232)

## Metadata

* Task ID: 232-housing-resident-screens-wcag
* Task slug: housing-resident-screens-wcag-232
* Related plan: .copilot-tracking/plans/2026-11-15/housing-resident-screens-wcag-232-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/housing-resident-screens-wcag-232-research.md, src/api/src/zava_forward/api/web/role-screens.js, src/api/src/zava_forward/api/web/app.js, src/api/src/zava_forward/api/web/style.css, docs/reference/research/ux/wcag-conformance-baseline.md, docs/reference/research/ux/design-system.md, docs/reference/research/ux/content-standard.md

## Phase Index

| Phase ID | Name                                                                               | Status | Detail sections        |
|----------|------------------------------------------------------------------------------------|--------|------------------------|
| P01      | Wire role routes, complete section landmarks, and harden keyboard jump navigation  | Ready  | P01, P01-T01, P01-T02  |
| P02      | Add explicit plain-language textual state cues across all indicators               | Ready  | P02, P02-T01           |
| P03      | Add focused WCAG 2.2 conformance unit tests and run focused validation             | Ready  | P03, P03-T01           |

## Test Ownership and Guardrail Lock

* Canonical production targets: `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/style.css`. Generated targets: `none`.
* Applicable test ownership:
  * Exact test removals: `none`.
  * Maximum new test files: `1` (`src/api/tests/test_housing_resident_screen_wcag.py`).
  * Semantic coverage in `test_housing_resident_screen_wcag.py`: route dispatch and script loading for `#/role/housing_officer` (`resident-service-issues`) and `#/role/resident_engagement` (`resident-choice`); `<nav role="navigation" aria-label>` jump navigation with `Go to ...` links matching 100% of `<section id aria-labelledby>` landmarks and `<h2 id tabindex="-1">` headings in both `render(case)` (populated and empty/partial cases) and `summary(...)`; synthetic click activation on `a[data-jump]` verifying `preventDefault()`, heading `.focus()`, and `.scrollIntoView({ block: "nearest" })`; explicit plain-language textual state cues across status badges, measure choice & readiness, paused/withdrawn rows, update commitment rows, safe-route indicators (present vs missing), redress formal-route & reviewable rows, response history steps, summary rows, and prototype-property edge cases (`constructor`, `toString`); static check that `test_housing_resident_screen_wcag.py` performs zero `sys.modules` deletions/mutations.
  * Regression coverage preserved unchanged: `test_role_screens_conformance.py`, `test_resident_screen_wcag.py`, `test_frontline_screen_wcag.py`, `test_resident_choice_screen.py`, `test_resident_service_screen.py`, `test_role_screens.py`, `test_role_screens_tensions_same_home.py`, `test_connected_home_check.py`, `test_design_system.py`, `test_accessibility_baseline.py`, `test_content_standard.py`.

<!-- rpi:phase id=P01 -->
## P01: Wire role routes, complete section landmarks, and harden keyboard jump navigation

### Context

`app.js` currently recognizes `#/screens` in `missingWorkspaceScripts` and `route()`, leaving `#/role/housing_officer` and `#/role/resident_engagement` unhandled (`C3`). Inside `role-screens.js`, `residentJumpNav` omits `role="navigation"` and the `Go to ` link prefix, covers only 4 of 9 `<section>` panels on `resident-choice.render(c)`, omits `Evidence boundary` and conditional `Response history` on `resident-service-issues.render(c)`, leaves a broken `#service-redress-heading` jump target when `c.redress_route` is absent (`screenUnknown` returns a `<div>` rather than an anchored `<section>`), and omits jump navigation in `summary(...)` when no home is selected (`C1`, `C2`, `C5`, `C6`).

### Intent

Make `#/role/housing_officer` and `#/role/resident_engagement` first-class routes into `resident-service-issues` and `resident-choice`, and guarantee a strict 1-to-1 bijection between `<nav role="navigation" aria-label="...">` `Go to ...` links and `<section id aria-labelledby>` landmarks with `<h2 id tabindex="-1">` focus targets across all rendered states.

### Boundaries

* Included: `app.js` route/script-loader predicates for `#/role/housing_officer` and `#/role/resident_engagement`; `roleScreensView()` default screen resolution from hash path; optional `anchor` parameter on `screenTension` and `screenWithheld`; `residentJumpNav` upgrade; anchoring all `<section>` landmarks in `resident-choice` and `resident-service-issues` (`render` and `summary`); `scroll-margin-top` on `.screen-record h2` in `style.css`.
* Excluded: Changing `screenHref` canonical `#/screens?...` format (`test_role_screens.py` / `connected_home_browser_check.py`), adding `id` attributes to sibling role screens' `screenWithheld`/`screenTension` sections (`test_assessor_screen_wcag.py`), or adding CSS motion to `.screen-*` selectors (`test_role_screens_conformance.py`).

### Likely Targets

* src/api/src/zava_forward/api/web/app.js: Add role-screen route helper used in `missingWorkspaceScripts` and `route()`.
* src/api/src/zava_forward/api/web/role-screens.js: Map `#/role/housing_officer` -> `resident-service-issues` and `#/role/resident_engagement` -> `resident-choice` in `roleScreensView()`; add optional `anchor` to `screenWithheld` and `screenTension`; update `residentJumpNav`, `resident-choice`, and `resident-service-issues`.
* src/api/src/zava_forward/api/web/style.css: Add `scroll-margin-top:var(--sp-4)` on `.screen-record h2`.

### Dependencies

* None.

### Validation Expectations

* Every `<nav>` in `resident-choice` and `resident-service-issues` (`render` and `summary`, populated and empty cases) has `role="navigation"`, non-empty `aria-label`, and `<a href="#...-heading" data-jump="...-heading">Go to ...</a>` links matching 100% of rendered `<section>` landmarks and `<h2 tabindex="-1">` headings.
* Existing `test_role_screens.py`, `test_role_screens_tensions_same_home.py`, `test_connected_home_check.py`, `test_assessor_screen_wcag.py`, and `test_procurement_screen_wcag.py` remain green.

### Completion Evidence

* Clean diff in `app.js`, `role-screens.js`, and `style.css` verified by Node VM DOM inspection and unit tests.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Wire `#/role/housing_officer` and `#/role/resident_engagement` route dispatch and script loading

#### Context

`app.js` checks `destination === "#/screens"` in `missingWorkspaceScripts` and `hash.split("?")[0] === "#/screens"` in `route()`. `roleScreensView()` reads `location.hash.split("?")[1]` for `screen`, `case`, and `page` query parameters (`C3`).

#### Intent

Route `#/role/housing_officer` to `resident-service-issues` and `#/role/resident_engagement` to `resident-choice` while preserving query parameters (`?case=`, `?page=`, and explicit `?screen=` override) and `#nav` `aria-current="page"` state.

#### Boundaries

* Included: `isRoleScreensHash` helper in `app.js` (distinct from all top-level identifiers in `role-screens.js` per `test_safety_screen_wcag_keyboard.py`) applied at all four `#/screens` checks: contractor `/ops.js` exclusion (`!isRoleScreensHash(destination)`), `/role-screens.js` lazy loader (`Boolean(me) && isRoleScreensHash(destination)`), `#nav` active destination normalization (`isRoleScreensHash(...) ? "#/screens" : ...`), and `route()` dispatch (`if (isRoleScreensHash(hash.split("?")[0])) return await roleScreensView();`); `roleRouteScreens` lookup in `role-screens.js` (`roleScreensView()`).
* Excluded: Changing server-returned `workbench.py` navigation list (`test_role_screens.py::test_staff_and_contractor_navigation_retains_scoped_screen_link` pins `links[-1]["href"] == "#/screens"`).

#### Likely Targets

* src/api/src/zava_forward/api/web/app.js: Update `missingWorkspaceScripts` and `route()`.
* src/api/src/zava_forward/api/web/role-screens.js: Resolve default screen ID from `location.hash.split("?")[0]` when `params.get("screen")` is unset.

#### Dependencies

* None.

#### Validation Expectations

* `missingWorkspaceScripts("#/role/housing_officer", false)` and `missingWorkspaceScripts("#/role/resident_engagement", false)` return `["/role-screens.js"]` when `roleScreensView` is not yet loaded.
* `roleScreensView()` selects `resident-service-issues` for `#/role/housing_officer` and `resident-choice` for `#/role/resident_engagement`.

#### Completion Evidence

* Automated route and host tests in `src/api/tests/test_housing_resident_screen_wcag.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Complete `residentJumpNav` (`role="navigation"`, `Go to ...`) and 1-to-1 `<section>` landmarks with `tabindex="-1"` headings

#### Context

`screenPanel` attaches `id`, `aria-labelledby="${id}-heading"`, and `<h2 id="${id}-heading" tabindex="-1">` whenever `{ anchor: id }` is passed (`C4`). On `resident-choice.render(c)`, 5 of 9 `<section>` elements currently lack `{ anchor }`; furthermore, `test_role_screens.py` prohibits `"capacity"`, `"utilisation"`, and `"headroom"` from appearing in any element before `"Choice comes before offered capacity"` (`C11`). On `resident-service-issues.render(c)`, `Evidence boundary` lacks `{ anchor }`, `redressRoutePanel(null)` returns a non-section `<div>` while `"service-redress"` stays in `serviceSections`, and conditional `Response history` lacks `{ anchor }` and a jump link (`C2`, `C6`).

#### Intent

Ensure every `<section>` landmark on both screens (`render` and `summary`) has an explicit `{ anchor }`, `aria-labelledby`, and `<h2 tabindex="-1">`, and `residentJumpNav` renders `<nav role="navigation" aria-label="...">` with `Go to ...` links in exact 1-to-1 correspondence across all data states.

#### Boundaries

* Included:
  * `const screenWithheld = (items, anchor = null) => screenPanel("Not shown for this role", ...(anchor ? [{ anchor }] : []), ...)` and `const screenTension = (kind, anchor = null) => screenPanel(screenTensionText[kind][0], ...(anchor ? [{ anchor }] : []), ...)` keeping `const` arrow form so `re.findall(r"screenTension\(", SCREENS)` stays `5` and zero banned tokens appear in the tension block (`C10`).
  * `const residentJumpNav = (sections, label = "Sections of this view") => h("nav", { role: "navigation", "aria-label": label, class: "screen-links" }, sections.map(([id, title]) => h("a", { href: `#${id}-heading`, "data-jump": `${id}-heading` }, `Go to ${title}`)))`.
  * Delegated `a[data-jump]` click handler in `role-screens.js` preserving literal `'closest?.("a[data-jump]")'` and `"event.preventDefault();\n    document.getElementById"` substrings (`test_asset_exec_screen_wcag.py`) while invoking `scrollIntoView?.({ block: "nearest" })` on the resolved heading target.
  * Host-level workspace jump navigation in `roleScreensView()` when `screen.id === "resident-choice" || screen.id === "resident-service-issues"` (`residentJumpNav(workspaceSections, "Workspace sections")`), targeting `#screen-queue-heading` (`<section id="screen-queue" aria-labelledby="screen-queue-heading"><h2 id="screen-queue-heading" tabindex="-1">Choose a home</h2>`), portfolio headings (`#choice-portfolio-heading` + `#choice-portfolio-withheld-heading` on `resident-choice`; `#service-portfolio-heading` on `resident-service-issues` when rendered), and `#screen-evidence-heading` (`<section id="screen-evidence" class="screen-evidence" aria-labelledby="screen-evidence-heading"><h2 id="screen-evidence-heading" tabindex="-1">Selected home ${c.id}</h2>` when `c` is selected), while dropping the duplicate fallback `overview` child on `: h("div", {}, h("p", ...))` and leaving `journeyStageMap` free of `tabindex` (`test_role_screens_stage_map_focus.py`).
  * Inline `screenPanel("Choice and update commitments across open homes (portfolio scope, not this home)", { anchor: "choice-portfolio" }, ...)` and `screenWithheld([...], "choice-portfolio-withheld")` inside `resident-choice.summary(queue)` with zero extra anchors inside `summary(queue)` (`test_resident_choice_screen.py` `len(anchors_of(tree)) == 1`, `0` on invalid pages, and `test_connected_home_check.py` `screen_block`).
  * Inline `screenPanel("Open service issues across this page of homes", { anchor: "service-portfolio" }, ...)` inside `resident-service-issues.summary(entries)`.
  * All 9 anchored sections on `resident-choice.render(c)` (`choice-boundary`, `choice-measures`, `choice-stopped`, `choice-update`, `choice-service`, `choice-precedence` with jump label `"Choice precedence rule"`, `choice-tension-choice` with jump label `"Design tension on resident choice"`, `choice-tension-disclosure` with jump label `"Design tension on continuity and disclosure"`, and `choice-withheld`), preserving literal `screenPanel("Choice for each measure", ...)` and `screenPanel("Paused or withdrawn by the resident", ...)` prefixes (`C9`, `C12`).
  * All anchored sections on `resident-service-issues.render(c)`: `service-boundary` (`Evidence boundary`), `service-issues` (`Service issues`, literal prefix preserved), `service-redress` (`redressRoutePanel` returning `screenPanel("Independent human review and formal complaints, without detriment", { anchor: "service-redress" }, ...)` in both `!route` and `route` branches so zero extra tables/controls are added and the landmark always exists), conditional `service-history` (`Response history`, included in `sections` iff `hasHistory` is true), and `service-update` (`Linked update commitment`).
  * Extending `:focus-visible,[tabindex="-1"]:focus` and adding `.screen-record h2,[tabindex="-1"]{scroll-margin-top:var(--sp-4)}` in `style.css` using Fluent 2 tokens only (zero raw hex literals, zero `.screen-*` animations/transitions) (`C7`, `W1`).
* Excluded: Buttons in jump nav; modifying sibling screens' `nav` or `<section>` sets; adding `tabindex` inside `journeyStageMap`.

#### Likely Targets

* src/api/src/zava_forward/api/web/role-screens.js: `screenWithheld`, `screenTension`, `residentJumpNav`, `choiceOverviewPanel`, `resident-choice`, `redressRoutePanel`, `resident-service-issues`.
* src/api/src/zava_forward/api/web/style.css: `.screen-record h2` scroll-margin rule.

#### Dependencies

* P01-T01.

#### Validation Expectations

* 1-to-1 equality between jump-nav link targets and `<section>` heading IDs (`tabindex === -1`) across populated, empty, redress-present, redress-missing, history-present, history-missing, and summary states.
* `test_role_screens.py::test_resident_choice_states_choice_precedence_after_choice_panels` and `test_role_screens_tensions_same_home.py` pass unchanged.

#### Completion Evidence

* Passing conformance and WCAG unit assertions.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Add explicit plain-language textual state cues across all indicators

### Context

While `stateCue()` and `serviceMeaning()` cover basic measure/update/service status cells (`C5`, `C6`), several indicators on Housing Officer (`resident-service-issues`) and Resident Engagement (`resident-choice`) still lack explicit textual state cues: `safe_contact_ref` safe-route cells render bare `"SC-77"` or `"Unknown"`, `m.readiness` renders bare `"Needs human review"` / `"Resident decision current"`, `stoppedChoiceRows` status cells lack a `State:` prefix, `redressRoutePanel` renders bare `formal_route_status` and reviewable `d.status`, `Response history` renders bare `x.status`, `serviceQueueRow` renders bare issue statuses, and `.flag` / `.flag.danger` badges in `roleScreensView` have no paired `State:` cue (`C5`, `C6`, `C8`, `C11`).

### Intent

Ensure every status badge, resident choice/readiness indicator, pause/withdrawal state, update commitment row, redress/history row, and safe-route indicator on both views carries an explicit plain-language textual state cue (`State:` / `Meaning:` / `Confirmed:` / `Waiting for resident:` / `Action needed:`) and `data-state-cue` metadata where appropriate, using only documented design-system CSS classes and plain-language glossary terms.

### Boundaries

* Included: `safeRouteCue`, `readinessCue`, `formalRouteCue`, paused/withdrawn `State:` cue in `stoppedChoiceRows`, `stateCue` on redress `reviewable_decisions`, `serviceMeaning` on `Response history` steps, `stateCue` in `serviceQueueRow`, and sibling `<span data-state-cue="..."> State: ...</span>` cues paired with `.flag.danger` and `.flag` badges when the active screen is `resident-choice` or `resident-service-issues`.
* Excluded: Inventing new CSS classes not listed in `docs/reference/research/ux/design-system.md` (`C8`); altering the inner text of `<span class="flag danger">Safety issue open</span>` (`C11`); using any banned glossary word (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`) (`C12`).

### Likely Targets

* src/api/src/zava_forward/api/web/role-screens.js: Queue/header badge pairing in `roleScreensView()`, state-cue helpers and table cells in `resident-choice` and `resident-service-issues`.

### Dependencies

* P01.

### Validation Expectations

* Every existing string assertion in `test_resident_choice_screen.py`, `test_resident_service_screen.py`, `test_resident_screen_wcag.py`, `test_frontline_screen_wcag.py`, `test_connected_home_check.py`, `test_role_screens.py`, `test_design_system.py`, and `test_content_standard.py` passes unchanged, and every indicator on both views exposes explicit textual state meaning.

### Completion Evidence

* Node VM output and unit assertions confirming explicit state text on every badge, row, and cell.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add plain-language textual state cues (`State:` / `Meaning:` / `stateCue`) and `data-state-cue` markers across `resident-choice`, `resident-service-issues`, and queue/header badges

#### Context

All existing tests assert substrings (`assertIn`) on resident table cells except `test_role_screens.py:240` (which asserts `text(marker) == "Safety issue open"` on `<span class="flag danger">`) and `connected_home_browser_check.py` (which checks substring containment in `Choice for each measure` cells) (`C9`, `C11`, `C12`).

#### Intent

Pair every state/route/badge signal on Housing Officer and Resident Engagement views with plain-language textual state cues while preserving 100% of existing substring and badge invariants and guarding against `Object.prototype` keys (`Object.hasOwn`).

#### Boundaries

* Included (guided by `redesign-existing-projects`, `accessibility`, and `web-design-guidelines`):
  * Use existing two/three-arg `stateCue(table, status, detail = status)` (`Object.hasOwn(table, status)`) and `serviceStatus(r)` (`stateCue(serviceCues, r.status)` + `serviceMeaning` lookup).
  * `safeRouteCue(ref)`: truthy string -> `` `Confirmed: ${screenValue(ref)} (safe route reference only; contact details not shown here)` ``; missing/blank -> `"Action needed: Unknown (safe route not recorded)"`. Applied in `resident-choice` `Linked update commitment`, `choiceQueueRow`, `resident-service-issues` `Linked update commitment`, and `serviceQueueRow`.
  * `readinessCues` (`{ "Resident decision current": "Confirmed", "Needs human review": "Action needed" }`) and `readinessCue(value)` (`value ? stateCue(readinessCues, value) : "Waiting for resident: Unknown"`). Applied to `choiceMeasure` Readiness column.
  * `Paused or withdrawn by the resident`: preserve existing `stateCue(choiceCues, ...)` in column 2 and `"Action needed: Human review before any restart"` in column 4 (`test_resident_choice_screen.py`), and prefix the empty-state `<p class="empty">` with `"State: None recorded. No measure is currently paused or withdrawn in the recorded answers."`.
  * `redressRoutePanel`: preserve existing `stateCue(choiceCues, x.status)` on `reviewable_decisions` and `stateCue(serviceCues, x.status)` on `formal_requests` State; replace bare `screenValue(x.formal_route_status)` in Formal route status with `formalRouteCue(x.formal_route_status)` (`formalRouteCues = { Acknowledged: "Confirmed" }`; `stateCue(formalRouteCues, value || "Unknown")` -> `"Action needed: Unconfigured"`, `"Confirmed: Acknowledged"`, `"Action needed: Unknown"`).
  * `Response history` (`resident-service-issues`): State column uses `serviceStatus({ status: x.status })` (`"Action needed: In progress. The named owner is dealing with it."`).
  * `serviceQueueRow`: preserve existing `stateCue(serviceCues, r.status, ...)` on open issues; use `"Confirmed: No open request recorded"` when `open.length === 0`, `safeRouteCue(u.safe_contact_ref)` on commitment rows, `"Action needed: No commitment recorded"` when `!u`, and `["Action needed: Unavailable. Open the home to check.", "Waiting for resident: Unavailable", "Action needed: Unavailable"]` when `!c`.
  * `roleScreensView`: When `isResidentRoleScreen` (`screen.id === "resident-choice" || screen.id === "resident-service-issues"`), pair `row.hazard` (`span.flag.danger`, inner text preserved verbatim as `"Safety issue open"`) with sibling `h("span", { "data-state-cue": "safety" }, " State: Action needed - open safety issue.")` and pair header `Same home: case ${c.id}` (`span.flag`) with sibling `h("span", { "data-state-cue": "scope" }, " State: Confirmed - single-home record scope.")` (using unclassed `<span>` so primary `var(--ink)` contrast is preserved and no undocumented CSS class is introduced into `role-screens.js`).
* Excluded: Unrelated role screens; banned glossary terms; undocumented CSS classes.

#### Likely Targets

* src/api/src/zava_forward/api/web/role-screens.js: `roleScreensView`, `resident-choice` helpers/renderer, `resident-service-issues` helpers/renderer.

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* Every badge and state cell on both views carries an explicit plain-language state prefix, and all existing resident/frontline/design-system/content-standard tests pass.

#### Completion Evidence

* Unit test coverage in `test_housing_resident_screen_wcag.py` and existing conformance suites.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Add focused WCAG 2.2 conformance unit tests and run focused validation

### Context

The caller requested focused unit tests in `src/api/tests/test_housing_resident_screen_wcag.py` (without `sys.modules` deletion hazards) verifying keyboard jump navigation, section landmarks, heading focus targets, and textual state cues across `#/role/housing_officer` and `#/role/resident_engagement`, validated with `unittest`, `mypy`, and `ruff`.

### Intent

Provide deterministic, fast, `sys.modules`-clean automated verification for all #232 WCAG 2.2 deliverables and run the full focused validation suite in `src/api`.

### Boundaries

* Included: Creating `src/api/tests/test_housing_resident_screen_wcag.py`; running focused `unittest`, `mypy`, `ruff check .`, and `ruff format --check .` in `src/api`.
* Excluded: Deleting or mutating `sys.modules`; modifying unrelated test files.

### Likely Targets

* src/api/tests/test_housing_resident_screen_wcag.py: New focused WCAG 2.2 test module.

### Dependencies

* P01, P02.

### Validation Expectations

* `python3 -m unittest discover -s tests -p "test_*housing*.py" -v` passes.
* `PYTHONPATH=src:.:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest` passes across `test_housing_resident_screen_wcag.py`, `test_role_screens_conformance.py`, `test_resident_screen_wcag.py`, `test_frontline_screen_wcag.py`, `test_resident_choice_screen.py`, `test_resident_service_screen.py`, `test_role_screens.py`, `test_role_screens_tensions_same_home.py`, `test_connected_home_check.py`, `test_design_system.py`, `test_accessibility_baseline.py`, and `test_content_standard.py`.
* `PYTHONPATH=src:.:../core/src:../agents/src python3 -m mypy` passes.
* `python3 -m ruff check . && python3 -m ruff format --check .` passes.

### Completion Evidence

* Recorded command outputs and exit codes in `.copilot-tracking/changes/2026-11-15/housing-resident-screens-wcag-232-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Create `src/api/tests/test_housing_resident_screen_wcag.py` and pass focused `unittest`, `mypy`, and `ruff` checks

#### Context

Sibling WCAG tests (`test_resident_screen_wcag.py`, `test_frontline_screen_wcag.py`, `test_procurement_screen_wcag.py`, `test_finance_screens_wcag_225.py`) evaluate `role-screens.js` and `app.js` in isolated `node:vm` contexts via `subprocess.run(["node", "-e", ...])` with full `mypy` annotations and zero `sys.modules` side effects.

#### Intent

Verify end-to-end route resolution (`#/role/housing_officer`, `#/role/resident_engagement`), keyboard jump-nav attributes (`role="navigation"`, `aria-label`, `Go to ...`), 1-to-1 section/heading landmark bijection (`tabindex="-1"`), delegated click-to-heading focus activation (`preventDefault`, `focus`, `scrollIntoView`), CSS focus/scroll-margin rules, and explicit textual state cues across all indicators and edge cases.

#### Boundaries

* Included: `src/api/tests/test_housing_resident_screen_wcag.py` with full type annotations (`from __future__ import annotations`) and focused validation runs.
* Excluded: Any `sys.modules` deletion or mutation.

#### Likely Targets

* src/api/tests/test_housing_resident_screen_wcag.py: New test file.

#### Dependencies

* P01, P02.

#### Validation Expectations

* All test cases pass under `python3 -m unittest discover -s tests -p "test_*housing*.py" -v`; `mypy` and `ruff` pass with zero warnings/errors.

#### Completion Evidence

* Passing test, typecheck, and lint execution logs.

#### Unresolved Items

* None.
