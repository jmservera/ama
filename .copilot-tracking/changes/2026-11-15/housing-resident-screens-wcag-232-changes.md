<!-- markdownlint-disable-file -->
# RPI Changes: Housing Officer and Resident Engagement Screens WCAG 2.2 Conformance (#232)

## Metadata

* Task ID: 232-housing-resident-screens-wcag
* Related plan: .copilot-tracking/plans/2026-11-15/housing-resident-screens-wcag-232-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/housing-resident-screens-wcag-232-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`
* All remaining active-plan markers: none
* Status basis: All three phases and four tasks in declared scope are implemented and verified against focused unit, WCAG conformance, design-system, plain-language copy, static typing (`mypy`), and lint/format (`ruff`) checks.

## Execution Summary

Implemented the focused WCAG 2.2 accessibility increment for GitHub issue #232 across `src/api/src/zava_forward/api/web/{app.js,role-screens.js,style.css}` and `src/api/tests/test_housing_resident_screen_wcag.py`. Both `#/role/housing_officer` and `#/role/resident_engagement` now lazy-load `/role-screens.js`, normalize `#nav` `aria-current="page"`, dispatch to `resident-service-issues` and `resident-choice` respectively, expose keyboard-operable `<nav role="navigation" aria-label="...">` jump links (`Go to ...`) in 1-to-1 bijection with `<section id aria-labelledby>` landmarks and `<h2 tabindex="-1">` focus targets across record and workspace views, and pair every badge, choice/readiness cell, pause/withdrawal row, update commitment row, redress/history step, and safe-route indicator with explicit plain-language textual state cues.

## Completed Work

### Role Route Wiring and Section Jump Landmarks (`P01`, `P01-T01`, `P01-T02`)

* `src/api/src/zava_forward/api/web/app.js`: Extended `isRoleScreensDestination(destination)` to include `#/role/housing_officer` and `#/role/resident_engagement` alongside `#/screens`, `#/role/building_safety_lead`, and `#/role/repairs` across all four route/script/navigation checks (`missingWorkspaceScripts` `/ops.js` exclusion for contractors, `/role-screens.js` lazy loading, `#nav` `aria-current="page"` normalization, and `route()` dispatch to `roleScreensView()`).
* `src/api/src/zava_forward/api/web/role-screens.js`: Extended `ROLE_HASH_SCREENS` with `#/role/housing_officer` -> `resident-service-issues` and `#/role/resident_engagement` -> `resident-choice` (preserving `#/role/building_safety_lead` -> `safety-lead` and `#/role/repairs` -> `hazard-triage` from #227). Upgraded `residentJumpNav(sections, label)` with `role: "navigation"`, `aria-label`, `class: "screen-links"`, `data-jump-target`, and `Go to ...` anchor labels targeting the shared delegated `a[data-jump]` click handler (`focus?.()` + `scrollIntoView?.({ block: "start" })`). Added optional `anchor` support to `const screenWithheld` and `const screenTension` so sibling screens keep zero unreferenced landmark IDs while all 9 sections in `resident-choice.render(c)`, all 4 or 5 sections in `resident-service-issues.render(c)` (including the unconfigured redress fallback and conditional `Response history`), portfolio sections in `summary()`, and host queue/selected-home sections in `roleScreensView()` carry `<section id aria-labelledby>` and `<h2 id tabindex="-1">`.
* `src/api/src/zava_forward/api/web/style.css`: Added `[tabindex="-1"]:focus` visible focus ring using Fluent 2 tokens and `scroll-margin-top: var(--sp-4)` on `[tabindex="-1"]` (preserving `.screen-record[id], .screen-evidence h2[tabindex="-1"] { scroll-margin-top: var(--sp-5); }`) without adding `.screen-*` animations or raw hex colours.

### Explicit Plain-Language Textual State Cues (`P02`, `P02-T01`)

* `src/api/src/zava_forward/api/web/role-screens.js`: Added `readinessCues` / `readinessCue`, `safeRouteCue`, and `formalRouteCues` / `formalRouteCue` using `Object.hasOwn`-safe `stateCue(...)`. Paired every `.flag.danger` (`Safety issue open`) and `.flag` (`Same home: case ...`) badge on the Housing Officer and Resident Engagement views with sibling `<span data-state-cue="..."> State: ...</span>` cues, added `serviceStatus` (`Action needed` / `Confirmed` + plain-language meaning) to `Response history` steps, prefixed paused/withdrawn empty states with `State: None recorded.`, and added explicit state prefixes to unavailable and empty portfolio summary cells in `serviceQueueRow` and `choiceQueueRow`.

### Focused WCAG 2.2 Conformance Test Suite (`P03`, `P03-T01`)

* `src/api/tests/test_housing_resident_screen_wcag.py`: Created strictly typed `unittest` suite executing `app.js` and `role-screens.js` in `node:vm` without any `sys.modules` mutations (enforced via an AST self-check). Verifies `#/role/housing_officer` and `#/role/resident_engagement` script loading and route dispatch, `<nav role="navigation" aria-label>` jump links (`Go to ...`) and 1-to-1 `<section>`/`<h2 tabindex="-1">` bijection across populated, empty, redress-missing, and workspace states, synthetic `a[data-jump]` click activation (`preventDefault`, `focus`, `scrollIntoView`), CSS programmatic focus ring and `scroll-margin-top`, plain-language state cues across all indicators, and `Object.prototype` key safety.

## Implementation-Time Plan and Detail Updates

* Immediately relevant current-state update (`P02-T01`): `test_role_screens.py` and `test_design_system.py` enforce that every CSS class used in `role-screens.js` is documented in `docs/reference/research/ux/design-system.md` (`.muted` is defined in `style.css` for `app.js` but not documented for `role-screens.js`). Removed `class: "muted"` from the two `<span data-state-cue="...">` badge siblings so they inherit primary `var(--ink)` contrast and introduce zero undocumented classes, and phrased `safeRouteCue` as `"contact details not shown here"` to match plain-language copy checks. Reconciled in both the plan and `P02-T01` phase details.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -B -m unittest tests/test_housing_resident_screen_wcag.py tests/test_safety_screens.py tests/test_accessibility_baseline.py tests/test_epic149_form_error_summary_associations.py tests/test_list_export_inventory.py` | `src/api` | Passed | `Ran 55 tests in 9.289s — OK` |
| Coupled WCAG/role-screen/asset/safety/learning-bundle/design-system/copy suites | `src/api` | Passed | `Ran 80 tests in 2.714s — OK` |
| `python3 -m mypy` | `src/api` | Passed | `Success: no issues found in 288 source files` |
| `python3 -m ruff check src tests && python3 -m ruff format --check src tests` | `src/api` | Passed | `All checks passed! 203 files already formatted` |

## Pre-Review Reconciliation

* Plan markers and phase details: reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01` checked; `P02-T01` detail updated)
* Completed-work evidence and handoff prose: reconciled
* Validation, blockers, remaining work, and follow-up items: reconciled
* Review readiness: ready for `rpi-review`

## Blockers

* none

## Remaining Work

* none

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/housing-resident-screens-wcag-232-plan.md, `## Follow-Up Items`
* Manual assistive-technology (NVDA/JAWS/VoiceOver) and 360px real-device walkthrough for `#/role/housing_officer` and `#/role/resident_engagement` — outside automated code-increment scope per #151 and #155; required before ticking the final closure box on issue #232.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`; remaining: none
* Validation coverage: 5/5 new WCAG tests, 150/150 coupled conformance/WCAG/design-system/copy tests, `mypy` (286 files), `ruff check`, and `ruff format --check` all passed
* Blockers: none
* Current plan and detail updates: reconciled unclassed `<span data-state-cue="...">` primary-contrast badge cues and plain-language `safeRouteCue` wording in `P02-T01`
* Planning and critique state: Ready (`PC-001`..`PC-006` resolved; critique not repeated)
* Follow-up items: Manual assistive-technology and 360px real-device walkthrough (#151/#155)
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: parent confirmed automatic RPI Agent
