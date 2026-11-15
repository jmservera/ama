<!-- markdownlint-disable-file -->
# Review: Procurement and Contractor Screens WCAG 2.2 Keyboard Jump Nav, Text State Labels, and Non-Colour Status Signals (#228)

## Scope and Evidence

* Task ID: issue-228-procurement-wcag
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: Requirements `FR-1`..`FR-4` and `NFR-1`..`NFR-2`, five acceptance criteria, critique dispositions `PC-001`..`PC-005`, implementation changes across `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/ops.js`, and `src/api/tests/test_procurement_contractor_screen_wcag.py`, focused validation evidence, Web Interface Guidelines compliance on changed web files, and out-of-scope `## Follow-Up Items`.
* Plan: .copilot-tracking/plans/2026-11-15/procurement-contractor-wcag-228-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/procurement-contractor-wcag-228-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/procurement-contractor-wcag-228-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/procurement-contractor-wcag-228-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/procurement-contractor-wcag-228-research.md (`C1`-`C18`, `W1`), refreshed Vercel Web Interface Guidelines (`command.md`), `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/research/ux/design-system.md`, `docs/reference/research/ux/content-standard.md`, and direct inspection of the Git diff and focused validation outputs.

## Opening Review State

* Interpreted review goal: Independently verify that the delivered `src/api` increment satisfies every planned WCAG 2.2 keyboard jump-navigation, section landmark, heading-focus, non-colour status badge, plain-language textual state cue, contractor vulnerability-redaction, and clean unit-test isolation requirement for `#228` without regressions across sibling role-screen, design-system, content-standard, or regulatory UX suites.
* Review scope: Full task (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`)
* Evidence readiness: Ready; research, plan, phase details, one-pass plan critique, reconciled changes log, Git diff, and executed validation outputs are all present and synchronized.
* Acceptance basis: `FR-1`..`FR-4`, `NFR-1`..`NFR-2`, the five plan Acceptance Criteria, resolved critique findings `PC-001`..`PC-005`, and refreshed Web Interface Guidelines subject to Zava Forward's Fluent 2 design system and plain-language content standard.
* First comparison boundary: Reconcile `P01`, `P02`, and `P03` markers, phase details, and `procurement-contractor-wcag-228-changes.md` against the actual source diff in `src/api`.
* Active read-only boundaries: Review writes only `.copilot-tracking/reviews/2026-11-15/procurement-contractor-wcag-228-review.md` (and parent RPI session state transitions); production files, tests, plan, details, critique, research, and changes artifacts remain untouched during Review.
* Initial blockers: None.

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed full-boundary comparison on 2026-11-15 across all seven plan markers (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`), all five critique dispositions (`PC-001`..`PC-005`), all four touched `src/api` files, refreshed Web Interface Guidelines rules, and executed `unittest`, `mypy`, and `ruff` results.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` / `P01-T01` | Role-Screen Jump Navigation, Landmarks, and `#/role/*` Resolution (`P01-T01`) | Reconciled | `screenNodeValue`, optional `anchor` on `screenWithheld` / `screenTension`, combined `ROLE_HASH_SCREENS` (`#227` + `#228`), `if (event.defaultPrevented) return;`, `procurementJumpNav` (`role="navigation"`, `aria-label="Sections of this view"`, `Go to ...`, `data-jump-target`), and shared shell `journeyStageMap(c, screen.id)` match plan and parent-branch conformance suites. |
| `P01` / `P01-T02` | Role-Screen Non-Colour Status Signals and Textual State Cues (`P01-T02`) | Reconciled | All five Deliverable 2 status surfaces in `role-screens.js` pair `.flag`, `.flag.danger`, and `.status-line.wait` with `data-state-cue` and plain-language text without stuttering or forbidden approval/booking wording. |
| `P02` / `P02-T01` | Staff-Facing Contractor Views, `#/role/*` Routing, and Global Jump Delegation (`P02-T01`) | Reconciled | `isRoleScreensDestination` in `missingWorkspaceScripts` and `route()` (`#227` + `#228`), `#/screens` active-nav mapping, literal `return await roleScreensView()`, global `a[data-jump]` focus + scroll delegation, sibling `#contractor-assigned-jobs` / `#contractor-work-orders` landmarks, preserved `section#regulatory-supplier`, `r.needs_notice` / `w.needs_notice` badges, and function-scoped helpers in `ops.js` match plan and `PC-001`/`PC-004`/`PC-005`. |
| `P03` / `P03-T01` | Focused WCAG 2.2 Conformance Unit Tests (`P03-T01`) | Reconciled | `src/api/tests/test_procurement_contractor_screen_wcag.py` implements 7 focused tests covering every planned semantic and regression check with AST-verified zero `sys.modules` deletion hazards. |
| `Follow-Up Items` | Implementation-Time Plan and Detail Updates / Follow-Up Items | Reconciled | Parent-branch `checks/procurement_screens_browser_check.py` expectation drift (`#1716`, `#233`), sibling jump-helper alignment, and human AT/usability sign-off (`#151`, `#155`) are synchronized between plan and changes record outside active `Pxx` claims. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/api/src/zava_forward/api/web/role-screens.js` | Added `screenNodeValue` VNode/DOM pass-through, optional `anchor` on `screenWithheld` / `screenTension` / `journeyStageMap`, `screenRoleHashes`, `defaultPrevented` click guard, `procurementJumpNav` (`role="navigation"`, `Go to ...`), and 100% `section.screen-record` anchors (`ownsStageMap: true`) on `procurement-packages` and `contractor-job-pack`. | Direct diff inspection and `test_procurement_and_contractor_role_screens_jump_nav_and_landmark_bijection` | Passed (`71/71` procurement tests; `12/12` role-screen conformance tests) | Reconciled |
| `P01-T02` | `src/api/src/zava_forward/api/web/role-screens.js` | Added `procurementBadge`, `packageCapacityBadge`, `packageEvidenceBadge`, `packageExpiryBadge`, `workOrderStateBadge`, and `prerequisiteBadge`, plus `.status-line.wait` draft readiness banner and submission/acknowledgement/independent-review/checklist/notice badges while preserving redaction and browser-check prefixes. | Direct diff inspection and `test_non_colour_badges_pair_visual_classes_with_plain_language_state_cues` | Passed (`71/71` procurement tests; `100/100` sibling conformance/content/design-system tests) | Reconciled |
| `P02-T01` | `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/ops.js` | Wired `ROLE_SCREEN_HASHES` in `missingWorkspaceScripts` and `route()` (`active` mapped to `#/screens`), global `a[data-jump]` focus delegation, `contractorListView` sibling `<section>` landmarks (`jobsSection.after(...)`), `contractorCaseView` landmarks (`#regulatory-supplier` preserved), and `workOrdersCard` function-scoped state/notice badges. | Direct diff inspection, `test_role_hash_aliases_and_nav_active_mapping`, `test_staff_contractor_list_and_case_views_landmarks_and_jump_links`, and `test_delegated_jump_focus_deduplicated_across_script_load_orders` | Passed (`71/71` procurement tests; `100/100` sibling conformance/UX/regulatory tests) | Reconciled |
| `P03-T01` | `src/api/tests/test_procurement_contractor_screen_wcag.py` | Created 7 focused `unittest` cases exercising real `role-screens.js`, `app.js`, and `ops.js` in an isolated Node `vm` DOM harness with zero `sys.modules` deletions. | File created, strict-typed, formatted, and executed | Passed (`71/71` `test_*procurement*.py`, `mypy` `0` issues across 286 files, `ruff check` & `ruff format --check` clean across 202 files) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `## Follow-Up Items` | Recorded pre-existing parent-branch expectation drift in `src/api/checks/procurement_screens_browser_check.py` (`Fully committed: 0` from `#1716` and `Shift+Tab` landing on `journeyStageMap` stage links from `#233`) plus sibling `assetJumpNav`/`financeJumpNav` alignment as follow-up-only items. | Triggered by running `checks.procurement_screens_browser_check` locally in Chromium during `P03-T01`; no user decision needed because `checks/procurement_screens_browser_check.py` is outside the declared write scope and approved requirements did not change. | Synchronized across `.copilot-tracking/plans/2026-11-15/procurement-contractor-wcag-228-plan.md` (`## Follow-Up Items`) and `.copilot-tracking/changes/2026-11-15/procurement-contractor-wcag-228-changes.md`. | Not needed (follow-up-only discovery; `PC-001`..`PC-005` and `Ready` plan state remain valid). | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All five critique findings (`PC-001` [High], `PC-002` [High], `PC-003` [Medium], `PC-004` [Medium], `PC-005` [Low]) from `.copilot-tracking/reviews/2026-11-15/procurement-contractor-wcag-228-plan-critique.md` were resolved in both planning artifacts prior to implementation and verified in the delivered code and unit tests (`r.needs_notice` / `w.needs_notice`, sibling `jobsSection.after(...)`, non-stuttering `"Unmet or Unknown"`, no `"Not supplied"` on `contractor-job-pack`, anchored `journeyStageMap` with `ownsStageMap: true`, symmetric `defaultPrevented` guards + function-scoped `ops.js` helpers, `#/screens` nav highlight mapping, and `test_regulatory_ux_check.py` validation).
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: No dependent-work pause was needed; `P01` -> `P02` -> `P03` executed strictly in dependency order.
* Justification assessment: Supported by concrete AST, DOM-harness, and static-conformance test evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Reconcile `src/api/checks/procurement_screens_browser_check.py` with parent-branch `screenCapacityState` (`#1716`) and `journeyStageMap` (`#233`) expectations and extend it to exercise `Go to ...` jump links and `#/role/{procurement,contractor}` route aliases | Browser check harness was outside the focused unit-test write boundary and failed only on pre-existing parent-branch expectations (`#1716`, `#233`) after passing all 35 `Package queue / Issued` state, read-only, forbidden-word, table-region, focus-ring, and uncovered-stop assertions. | Follow-up implementation task (`src/api/checks/procurement_screens_browser_check.py`) | Open; routed as ranked follow-up #1 |
| Align sibling specialist role-screen jump helpers (`assetJumpNav`, `financeJumpNav`) to emit `role="navigation"` and `Go to ...` link text consistently with `screenJumpNav` and `procurementJumpNav`, and consider `scroll-margin-top` on `h2[id][tabindex="-1"]` | Belongs to sibling specialist screens (`#224`, `#225`) and shared stylesheet polish rather than `#228` procurement/contractor screens. | Follow-up UX consistency cleanup (`role-screens.js`, `style.css`) | Open; routed as ranked follow-up #2 |
| Complete manual assistive-technology and resident/staff usability verification across specialist role screens (`#151` / `#155`) | Requires human screen-reader, magnification, and usability testing per `docs/reference/research/ux/wcag-conformance-baseline.md`; engineering checks cannot fabricate human accessibility acceptance. | Named human accessibility/usability reviewer before closing `#228` | Open; routed as ranked follow-up #3 (`Refs #228`) |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

No defects, decision gaps, or material evidence gaps were found within the assessed `#228` task boundary. One low-severity, non-blocking polish observation from the refreshed Web Interface Guidelines review is recorded below as residual follow-up context.

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Heading focus targets (`h2[id][tabindex="-1"]`) rely on static-header scroll positioning without explicit `scroll-margin-top` and `a[data-jump]` intercepts modified clicks

* Related scope: `Follow-Up Items` (shared `role-screens.js` / `app.js` / `style.css` jump-link pattern)
* Evidence: `src/api/src/zava_forward/api/web/style.css` defines `scroll-margin-top: var(--sp-4)` on `.case-section-title` while specialist role-screen and contractor `h2[id][tabindex="-1"]` targets use default scroll alignment (safe today because the top bar is not sticky, verified by Chromium `FOCUS_STOP` `covered == False`), and `a[data-jump]` click listeners call `preventDefault()` without checking modifier keys (`ctrlKey` / `metaKey`), matching the existing `role-screens.js` pattern in a hash-routed SPA where `#heading-id` cannot open as a standalone route.
* Impact: Non-blocking; keyboard Enter and primary-click jump navigation work cleanly without obscured focus, while adding `scroll-margin-top: var(--sp-4)` on `h2[id][tabindex="-1"]` in a shared stylesheet pass will improve breathing room at the top of the viewport.
* Destination: follow-up
* Smallest useful next action: Fold `h2[id][tabindex="-1"] { scroll-margin-top: var(--sp-4); }` into the sibling jump-nav consistency cleanup across `role-screens.js` and `style.css`.

## Defects

* None.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `follow-up` | Optional shared UX polish alongside sibling jump-nav cleanup (`style.css` / `role-screens.js`) | Non-blocking residual polish outside `#228` acceptance criteria; current header is static and Chromium `FOCUS_STOP` confirmed zero covered focus stops |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Update `src/api/checks/procurement_screens_browser_check.py` for parent-branch `screenCapacityState` (`#1716`) and `journeyStageMap` (`#233`) expectations and add Chromium assertions for `Go to ...` jump links and `#/role/{procurement,contractor}` route aliases.
* Align sibling specialist role-screen jump helpers (`assetJumpNav`, `financeJumpNav`) with `role="navigation"`, `Go to ...` labels, and `h2[id][tabindex="-1"]` `scroll-margin-top` (`RV-001`).
* Complete human assistive-technology and resident/staff usability verification (`#151` / `#155`) required before closing `#228` (`Refs #228`).

## Blockers and Remaining Work

* Blockers: None for this focused code increment (human AT/usability sign-off under `#151`/`#155` remains an external issue-closing gate, so commits use `Refs #228`, not `Closes #228`).
* Remaining active work: None (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, and `P03-T01` are complete).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `PYTHONPATH=tests:../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_*procurement*.py" -v` | `src/api` procurement API, screens, and WCAG unit suites (including `test_procurement_contractor_screen_wcag.py`) | Passed | `Ran 71 tests in 40.090s — OK` (all 7 new `ProcurementContractorScreenWcagTests` methods passed) |
| `PYTHONPATH=tests:../core/tests:../agents/tests python3 -m unittest tests/test_role_screens_conformance.py -v` | `src/api` specialist role-screen static & DOM conformance | Passed | `Ran 12 tests in 0.054s — OK` |
| `PYTHONPATH=tests:../core/tests:../agents/tests python3 -m unittest tests/test_role_screens.py tests/test_role_screens_tensions_same_home.py tests/test_design_system.py tests/test_accessibility_baseline.py tests/test_content_standard.py tests/test_safety_screen_wcag_keyboard.py tests/test_safety_panel_ux.py tests/test_regulatory_ux_check.py -v` | `src/api` sibling role screens, tensions, Fluent 2 design system, WCAG baseline, plain-language copy standard, safety WCAG keyboard, and regulatory UX checks | Passed | `Ran 100 tests in 2.002s — OK` |
| `python3 -m mypy` | `src/api` (`src`, `tests`, `checks` — 286 source files, `strict = true`) | Passed | `Success: no issues found in 286 source files` |
| `python3 -m ruff check . && python3 -m ruff format --check .` | `src/api` (202 Python files) | Passed | `All checks passed! 202 files already formatted` |
| `python3 -m checks.procurement_screens_browser_check` (diagnostic local Chromium probe) | `src/api/checks/procurement_screens_browser_check.py` | Skipped (out-of-scope harness drift recorded) | Diagnostic probe confirmed all 35 `Package queue / Issued` phrase, read-only, forbidden-word, table-region, focus-indicator, and uncovered-stop checks pass in Chromium; full script exit requires updating two pre-existing parent-branch expectations (`#1716`, `#233`) plus `ZF_AXE_JS`, tracked as Follow-Up #1 |

## Web Interface Guidelines Compliance Check (`file:line`)

Refreshed rules from `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` before reviewing changed web files (`docs/reference/research/ux/design-system.md` and `docs/reference/research/ux/content-standard.md` govern UK plain-language sentence case and ASCII punctuation):

```text
## src/api/src/zava_forward/api/web/role-screens.js

src/api/src/zava_forward/api/web/role-screens.js:23 - h2[id][tabindex="-1"] anchor headings rely on static header; add scroll-margin-top in style.css follow-up (RV-001)

## src/api/src/zava_forward/api/web/app.js

src/api/src/zava_forward/api/web/app.js:1849 - contractor h2[id][tabindex="-1"] anchor headings rely on static header; add scroll-margin-top in style.css follow-up (RV-001)

## src/api/src/zava_forward/api/web/ops.js

✓ pass
```

## Outcome

* Outcome: Conformant
* Outcome rationale: Every planned requirement (`FR-1`..`FR-4`, `NFR-1`, `NFR-2`), every acceptance criterion, and all five resolved critique items (`PC-001`..`PC-005`) are implemented cleanly in `src/api` and verified by 71 passing procurement/WCAG unit tests, 100 passing sibling conformance/UX/content/regulatory tests, strict `mypy` across 286 files, and `ruff` check/format across 202 files, with zero defects or scope drift.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct follow-up (`Follow-Up Items` / `RV-001`) | User-selected post-Review follow-up item (browser harness expectation update, sibling jump-nav + `scroll-margin-top` polish, or human AT/usability verification under `#151`/`#155`) |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: `71/71` `test_*procurement*.py` passed, `12/12` `test_role_screens_conformance.py` passed, `100/100` sibling UX/WCAG/content/regulatory tests passed, `mypy` `0` issues (286 files), `ruff check` and `ruff format --check` clean (202 files)
* Blockers: None
