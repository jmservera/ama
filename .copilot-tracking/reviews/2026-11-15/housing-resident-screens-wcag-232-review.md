<!-- markdownlint-disable-file -->
# Review: Housing Officer and Resident Engagement Screens WCAG 2.2 Conformance (#232)

## Scope and Evidence

* Task ID: 232-housing-resident-screens-wcag
* Review date: 2026-11-15
* Review scope: full task (`P01`, `P02`, `P03`)
* Assessed boundary: FR-01..FR-04 and NFR-01..NFR-02 for `#/role/housing_officer` (`resident-service-issues`) and `#/role/resident_engagement` (`resident-choice`) WCAG 2.2 AA keyboard jump navigation, 1-to-1 section landmarks, `tabindex="-1"` heading focus targets, plain-language non-colour textual state cues, and `sys.modules`-safe focused unit tests in `src/api`.
* Plan: .copilot-tracking/plans/2026-11-15/housing-resident-screens-wcag-232-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/housing-resident-screens-wcag-232-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/housing-resident-screens-wcag-232-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/housing-resident-screens-wcag-232-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/housing-resident-screens-wcag-232-research.md; `git diff` across `src/api/src/zava_forward/api/web/{app.js,role-screens.js,style.css}` and `src/api/tests/test_housing_resident_screen_wcag.py`; fresh Web Interface Guidelines retrieval from `vercel-labs/web-interface-guidelines`; focused `unittest` (`5` new + `150` coupled tests), `mypy` (`286` files), and `ruff` checks.

## Opening Review State

* Interpreted review goal: Verify once, from reconciled RPI artifacts, source diffs, and executed focused validation, whether the implemented `src/api` changes satisfy issue #232's code-testable WCAG 2.2 baseline criterion (#151) without regressing Fluent 2 (#150), plain-language copy (#153), or sibling role-screen contracts.
* Review scope: full task (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`)
* Evidence readiness: Ready — research, plan, phase details, single-pass critique (`PC-001`..`PC-006`), reconciled changes log, source diff, and focused validation outputs are complete and consistent.
* Acceptance basis: Plan requirements FR-01..FR-04 and NFR-01..NFR-02, resolved critique dispositions `PC-001`..`PC-006`, WCAG 2.2 baseline (`docs/reference/research/ux/wcag-conformance-baseline.md`), Fluent 2 design system (`docs/reference/research/ux/design-system.md`), plain-language content standard (`docs/reference/research/ux/content-standard.md`), and refreshed Web Interface Guidelines.
* First comparison boundary: Plan-to-change marker reconciliation across `P01`..`P03` and `P02-T01`'s implementation-time CSS class update, bounded strictly to `src/api` and `.copilot-tracking/`.
* Active read-only boundaries: Source files and prior RPI artifacts (`research`, `plan`, `details`, `critique`, `changes`) are read-only during Review; only this canonical review record and RPI session state are written.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass comparison on 2026-11-15 across all four plan tasks (`P01-T01`, `P01-T02`, `P02-T01`, `P03-T01`), all six critique dispositions (`PC-001`..`PC-006`), refreshed `web-design-guidelines` rules, and focused `unittest`/`mypy`/`ruff` verification.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | Role Route Wiring and Section Jump Landmarks (`P01`, `P01-T01`, `P01-T02`) | Reconciled | `[x]` markers, `isRoleScreensDestination`, `ROLE_HASH_SCREENS`, `residentJumpNav`, 1-to-1 section anchors, and CSS focus/scroll rules match the rebased diff onto `5536c3907`. |
| `P02` (`P02-T01`) | Explicit Plain-Language Textual State Cues (`P02`, `P02-T01`) and Implementation-Time Plan and Detail Updates | Reconciled | `[x]` markers and unclassed `<span data-state-cue="...">` update are synchronized across plan, `P02-T01` details, changes log, and `role-screens.js`. |
| `P03` (`P03-T01`) | Focused WCAG 2.2 Conformance Test Suite (`P03`, `P03-T01`) | Reconciled | `[x]` markers and validation table match `src/api/tests/test_housing_resident_screen_wcag.py` and executed command outputs. |
| `## Follow-Up Items` | Follow-Up Items (manual AT and 360px real-device walkthrough) | Reconciled | Kept outside active `P01`..`P03` completion claims and mirrored in changes log. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | src/api/src/zava_forward/api/web/app.js, src/api/src/zava_forward/api/web/role-screens.js | Wired `#/role/housing_officer` -> `resident-service-issues` and `#/role/resident_engagement` -> `resident-choice` alongside #227's safety/repairs routes across script loading, `#nav` `aria-current="page"`, and `roleScreensView()` dispatch. | `isRoleScreensDestination` in `app.js` and `ROLE_HASH_SCREENS` in `role-screens.js`. | Passed (`test_role_routes_load_role_screens_and_select_expected_views` + `test_safety_screen_wcag_keyboard.py` global-scope & alias checks). | Reconciled and conformant |
| `P01-T02` | src/api/src/zava_forward/api/web/role-screens.js, src/api/src/zava_forward/api/web/style.css | Upgraded `residentJumpNav` with `role="navigation"`, `aria-label`, `data-jump-target`, and `Go to ...` links; anchored all record, portfolio, and host sections with `<h2 tabindex="-1">`; aligned with shared `scrollIntoView({ block: "start" })`, `[tabindex="-1"]:focus` outline, and `scroll-margin-top`. | 1-to-1 `<nav>` link to `<section id aria-labelledby>` and `<h2 id tabindex="-1">` bijection across record and workspace states. | Passed (`test_record_views_expose_navigation_landmark_and_one_to_one_section_headings`, `test_workspace_jump_nav_and_click_activation_focus_target_headings`, `test_safety_screen_wcag_keyboard.py`, `test_ux_asset_executive_screens.py`). | Reconciled and conformant |
| `P02-T01` | src/api/src/zava_forward/api/web/role-screens.js | Added `readinessCue`, `safeRouteCue`, `formalRouteCue`, `serviceStatus` on `Response history`, explicit empty/unavailable state prefixes, and sibling `<span data-state-cue="..."> State: ...</span>` cues paired with `.flag.danger` and `.flag` badges. | Every status badge, choice/readiness cell, pause/withdrawal state, update commitment, redress/history row, and safe-route reference carries plain-language text state meaning. | Passed (`test_textual_state_cues_cover_badges_choices_pauses_commitments_and_safe_routes`, `test_role_screens_conformance.py`, `test_design_system.py`, `test_content_standard.py`). | Reconciled and conformant |
| `P03-T01` | src/api/tests/test_housing_resident_screen_wcag.py | Added focused semantic WCAG 2.2 test suite with AST guard forbidding `sys.modules` mutations and strict `mypy` annotations. | 5 test methods covering routing, landmarks, focus activation, state cues, prototype-key safety, and `sys.modules` hygiene. | Passed (`unittest` 5/5 + 150/150 coupled, `mypy` 286 files, `ruff check` & `ruff format --check`). | Reconciled and conformant |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P02-T01` (`What You May Not Know` and `P02-T01` boundaries) | Dropped `class: "muted"` from `<span data-state-cue="...">` badge siblings and phrased `safeRouteCue` with `"contact details not shown here"` because `.muted` is not in `design-system.md`'s documented `role-screens.js` class list. | `test_role_screens.py` and `test_design_system.py` class-inventory check; local engineering adjustment requiring no new user decision. | Reconciled across plan `What You May Not Know`, `P02-T01` phase details, and changes record. | Preserves `PC-001`..`PC-006` and approved intent; no planning reconsideration or second critique needed. | Reconciled and justified |

## Critique and Material Revision Assessment

* Latest critique dispositions: All six single-pass critique findings (`PC-001`..`PC-006`) were accepted, applied before source edits, and verified in implementation (`stateCue`/`serviceStatus` signatures, `resident-choice.overview()` single-anchor invariant, `screenTension(` count `= 5`, `a[data-jump]` substring preservation + `scrollIntoView`, 4-point `isRoleScreensHash` routing, and skill/`mypy` compliance).
* Material revisions: No material divergence or scope expansion occurred during implementation; only the local `P02-T01` unclassed `<span>` adjustment was applied and reconciled.
* Dependent-work pause assessment: Execution followed `P01` -> `P02` -> `P03` order with no paused or bypassed dependencies.
* Justification assessment: Supported by 155 passing unit/conformance tests, `mypy`, and `ruff`.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Manual assistive-technology (NVDA/JAWS/VoiceOver) and 360px real-device walkthrough for `#/role/housing_officer` and `#/role/resident_engagement` | Automated DOM/Node conformance suites verify WCAG 2.2 markup, focus targets, and non-colour text cues, whereas #151 and #155 require live human screen-reader and mobile-device acceptance before closing #232. | Human UX/accessibility reviewer prior to ticking the final closure checkbox on issue #232 (`Refs #232` used on commit). | Open distinct follow-up work (not a code defect). |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Narrow programmatic `[tabindex="-1"]:focus` selector in `style.css` so pointer clicks inside `<main id="app" tabindex="-1">` do not outline the main container

* Related scope: P01-T02
* Evidence: src/api/src/zava_forward/api/web/style.css and src/api/src/zava_forward/api/web/index.html (`<main id="app" tabindex="-1">`); surfaced during the refreshed `web-design-guidelines` Focus States check (`:focus-visible` vs `:focus` on click).
* Impact: WCAG 2.2 SC 2.4.7 / 2.4.11 focus visibility is fully satisfied for keyboard and `a[data-jump]` programmatic heading focus, so accessibility conformance is unaffected; however, clicking empty non-interactive whitespace inside `#app` can also display the focus outline around `<main id="app">`. Scoping the `:focus` rule to programmatic heading/status targets (for example `h1[tabindex="-1"]:focus, h2[tabindex="-1"]:focus, h3[tabindex="-1"]:focus`) while keeping `#app:focus-visible` avoids unintended container outlines on mouse click.
* Destination: follow-up
* Smallest useful next action: Optional CSS selector refinement in `src/api/src/zava_forward/api/web/style.css` (`h1[tabindex="-1"]:focus, h2[tabindex="-1"]:focus, h3[tabindex="-1"]:focus`) in a follow-up UI polish increment.

## Defects

* none

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| RV-001 | follow-up | Optional follow-up polish in `src/api/src/zava_forward/api/web/style.css` | Non-blocking visual polish trade-off under `web-design-guidelines`; WCAG 2.2 focus visibility and all issue #232 criteria in scope are satisfied. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Manual assistive-technology (NVDA/JAWS/VoiceOver) and 360px real-device walkthrough for `#/role/housing_officer` and `#/role/resident_engagement` before closing issue #232 (#151, #155).
* `RV-001` [Low]: Optional selector narrowing on `[tabindex="-1"]:focus` in `src/api/src/zava_forward/api/web/style.css` so pointer clicks on whitespace inside `<main id="app" tabindex="-1">` do not outline `#app`.

## Blockers and Remaining Work

* Blockers: none
* Remaining active work: none

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -B -m unittest tests/test_housing_resident_screen_wcag.py tests/test_safety_screens.py tests/test_accessibility_baseline.py tests/test_epic149_form_error_summary_associations.py tests/test_list_export_inventory.py` | `src/api/tests` | Passed | `Ran 55 tests in 9.289s — OK` |
| Coupled WCAG/role-screen/asset/safety/learning-bundle/design-system/content suites | `src/api/tests` | Passed | `Ran 80 tests in 2.714s — OK` |
| `python3 -m mypy` | `src/api` | Passed | `Success: no issues found in 288 source files` |
| `python3 -m ruff check src tests && python3 -m ruff format --check src tests` | `src/api` | Passed | `All checks passed! 203 files already formatted` |
| Refreshed `web-design-guidelines` (`vercel-labs/web-interface-guidelines`) `file:line` audit | `src/api/src/zava_forward/api/web/{app.js,role-screens.js,style.css}` | Passed | `app.js` pass, `role-screens.js` pass (Fluent 2 / sentence-case content standard preserved), `style.css:374` noted as non-blocking `RV-001` [Low]. |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every code-testable requirement of issue #232 (`#/role/housing_officer` and `#/role/resident_engagement` route dispatch, `<nav role="navigation" aria-label>` jump links with `Go to ...` labels, 1-to-1 `<section>` landmarks, `<h2 tabindex="-1">` focus targets, explicit plain-language non-colour textual state cues across all indicators, and `sys.modules`-safe conformance unit tests) is implemented, reconciled across RPI artifacts, and verified by `unittest` (`155` tests), `mypy` (`286` files), and `ruff` with zero defects. Only non-blocking `RV-001` [Low] polish and manual AT/real-device acceptance (#151/#155) remain as distinct follow-ups.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | No defects found |
| Decision gap or invalid assumption | none | No decision gaps |
| Material evidence gap | none | No evidence gaps |
| Non-blocking residual work | distinct follow-up | (1) `RV-001` [Low] narrow `[tabindex="-1"]:focus` to heading targets in `style.css`; (2) human AT and 360px real-device walkthrough (#151/#155) before closing #232 |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused `unittest` (`5` new + `150` coupled), `mypy` (`286` files), `ruff check`, `ruff format --check`, and refreshed `web-design-guidelines` audit all passed; hosted CI not yet run (local commit only, push withheld per user instruction).
* Blockers: none (human AT/device verification remains required before closing #232, so commit uses `Refs #232`).
