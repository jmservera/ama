<!-- markdownlint-disable-file -->
# RPI Changes: Procurement and Contractor Screens WCAG 2.2 Keyboard Jump Nav, Text State Labels, and Non-Colour Status Signals (#228)

## Metadata

* Task ID: procurement-contractor-wcag-228
* Related plan: .copilot-tracking/plans/2026-11-15/procurement-contractor-wcag-228-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/procurement-contractor-wcag-228-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`
* All remaining active-plan markers: none
* Status basis: Every phase and task in the approved full plan has been implemented, checked off immediately upon completion evidence, and verified against focused unit tests, sibling conformance suites, `mypy`, and `ruff`.

## Execution Summary

Delivered full WCAG 2.2 keyboard section jump navigation (`role="navigation"`, `aria-label`, `Go to ...` links, 100% `<section>` landmark coverage, `<h2 tabindex="-1">` focus targets, and symmetric `defaultPrevented`-deduplicated `a[data-jump]` focus delegation), `#/role/procurement` and `#/role/contractor` hash route aliases, and paired documented Fluent 2 non-colour visual status badges/lines (`.flag`, `.flag.danger`, `.status-line`, `.wait`) + `data-state-cue` + explicit plain-language textual state labels across Procurement (`procurement-packages`) and Contractor (`contractor-job-pack`, `contractorListView`, `contractorCaseView`, and `workOrdersCard`) surfaces while preserving contractor vulnerability-reason redaction. Added 7 focused conformance test methods in `src/api/tests/test_procurement_contractor_screen_wcag.py` with zero `sys.modules` deletion hazards.

## Completed Work

### Role-Screen Jump Navigation, Landmarks, and `#/role/*` Resolution (`P01-T01`)

* Updated `src/api/src/zava_forward/api/web/role-screens.js`:
  * Added `screenNodeValue(value)` pass-through in `screenFields` and `screenTable` so DOM and virtual-DOM badge elements render without `String(...)` coercion.
  * Added optional `anchor` support to `screenWithheld` and `screenTension` while preserving the exact `5` `screenTension(` occurrences enforced by `test_role_screens_tensions_same_home.py` and shared shell `journeyStageMap(c, screen.id)` ownership enforced by `test_role_screens_connected_journey.py` and `test_role_screens_stage_map_focus.py`.
  * Extended `ROLE_HASH_SCREENS` in `roleScreensView()` to preserve both `#227` aliases (`#/role/building_safety_lead` -> `safety-lead`, `#/role/repairs` -> `hazard-triage`) and `#228` aliases (`#/role/procurement` -> `procurement-packages`, `#/role/contractor` -> `contractor-job-pack`), and guarded `if (event.defaultPrevented) return;` in the `a[data-jump]` click handler alongside `focus?.()` and `scrollIntoView?.({ block: "start" })`.
  * Updated `procurementJumpNav` to emit `role: "navigation"`, `aria-label: "Sections of this view"`, `data-jump`, `data-jump-target`, and `Go to ${title}` link labels, with complete anchors on every screen-owned `section.screen-record` panel for `procurement-packages` and `contractor-job-pack`.

### Role-Screen Non-Colour Status Signals and Textual State Cues (`P01-T02`)

* Updated `src/api/src/zava_forward/api/web/role-screens.js`:
  * Added `procurementBadge`, `packageCapacityBadge`, `packageEvidenceBadge`, `packageExpiryBadge`, `workOrderStateBadge`, and `prerequisiteBadge` pairing `.flag` / `.flag.danger` and `data-state-cue` with plain-language textual labels across package queue rows, insurance/certification expiry fields, work-order tables, corrections/completion/independent-review cells, draft readiness banners (`status-line wait`, `role="status"`, `State: Draft readiness only. This is not a release or approval.`), prerequisite rows, named-reviewer fields, contractor submission/acknowledgement/review rows, and contractor job pack checklist/notice fields.
  * Preserved all `procurement_screens_browser_check.py` cell prefixes, single `[role="status"]` per package (`0` when empty), `FORBIDDEN` substring exclusions, and contractor vulnerability redaction.

### Staff-Facing Contractor Views, `#/role/*` Routing, and Global Jump Delegation (`P02-T01`)

* Updated `src/api/src/zava_forward/api/web/app.js` and `src/api/src/zava_forward/api/web/ops.js`:
  * Extended `isRoleScreensDestination(destination)` in `app.js` `missingWorkspaceScripts` and `route()` to include `#/role/procurement` and `#/role/contractor` alongside `#/screens`, `#/role/building_safety_lead`, and `#/role/repairs`, mapping all role-screen routes to `#/screens` for `#nav` `aria-current="page"` and `routeStatus` while preserving literal `return await roleScreensView();`.
  * Added `if (e.defaultPrevented) return;` and `a[data-jump]` heading focus + `scrollIntoView({ block: "start" })` delegation in `app.js`'s global click listener with null-safe `#account` handling.
  * Upgraded `contractorListView()` (mounting `jobsSection.after(await contractorOrders())` as sibling `<section>` landmarks and using `r.needs_notice`), `contractorCaseView(id)` (preserving `section#regulatory-supplier`), and `workOrdersCard(rows, mine)` in `ops.js` (function-scoped badge helpers) with `contractorJumpLinks`, `<h2 tabindex="-1">`, and paired `.flag` / `.flag.danger` / `.status-line` + `data-state-cue` + plain-language labels while redacting resident vulnerability reasons.

### Focused WCAG 2.2 Conformance Unit Tests (`P03-T01`)

* Created `src/api/tests/test_procurement_contractor_screen_wcag.py` with 7 focused test methods covering:
  * `procurement-packages` and `contractor-job-pack` jump-nav `role="navigation"`, `aria-label`, `Go to ...` links, 100% `section.screen-record` landmark bijection (including `Journey stages` and sanitised multi-package draft anchors), `<h2 tabindex="-1">`, and click-driven heading focus.
  * `#/role/procurement` and `#/role/contractor` hash routing, `missingWorkspaceScripts(...) == []`, `#nav` `aria-current="page"` mapping to `#/screens`, and host shell landmark preservation.
  * `contractorListView` sibling landmarks (`#contractor-assigned-jobs`, `#contractor-work-orders`) and `contractorCaseView` landmarks (including `#regulatory-supplier`) + jump focus.
  * Symmetric `defaultPrevented` click-focus deduplication (`focusCount === 1`) across all four `app.js` / `role-screens.js` load permutations plus missing-target safety.
  * Paired `.flag` / `.flag.danger` / `.status-line.wait` + `data-state-cue` + plain-language text across all five Deliverable 2 status surfaces without prefix stuttering or forbidden approval/booking wording.
  * Contractor vulnerability canary redaction across `contractor-job-pack`, `contractorListView`, and `contractorCaseView`.
  * Pairwise disjoint top-level lexical declarations across `app.js`, `ops.js`, and `role-screens.js`, plus AST verification of zero `sys.modules` deletions/mutations.

## Implementation-Time Plan and Detail Updates

* Follow-up-only discovery recorded in `.copilot-tracking/plans/2026-11-15/procurement-contractor-wcag-228-plan.md` (`## Follow-Up Items`): running `checks.procurement_screens_browser_check` locally in Chromium confirmed all state phrases, read-only rules, forbidden-word checks, table regions, focus indicators, and uncovered stops on `Package queue / Issued`, while exposing two pre-existing parent-branch expectation drifts in `src/api/checks/procurement_screens_browser_check.py` (`| 0 |` vs `| Fully committed: 0 |` from `#1716` and `Shift+Tab` landing on `journeyStageMap` stage links before `"Open existing case workspace"` from `#233`). Kept outside active write scope and recorded as a ranked follow-up item.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| Focused procurement & WCAG unit tests | `python3 -m unittest discover -s tests -p "test_*procurement*.py" -v` (`src/api`) | Passed | `Ran 71 tests in 40.090s — OK` (including all 7 new tests in `test_procurement_contractor_screen_wcag.py`) |
| Role-screen conformance suite | `python3 -m unittest tests/test_role_screens_conformance.py -v` (`src/api`) | Passed | `Ran 12 tests in 0.054s — OK` |
| Sibling UX, design-system, baseline, content-standard, safety & regulatory suites | `test_role_screens.py`, `test_role_screens_tensions_same_home.py`, `test_design_system.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, `test_safety_screen_wcag_keyboard.py`, `test_safety_panel_ux.py`, `test_regulatory_ux_check.py` (`src/api`) | Passed | `Ran 100 tests in 2.002s — OK` |
| Static typing (`mypy`) | `python3 -m mypy` (`src/api`, worktree packages) | Passed | `Success: no issues found in 286 source files` |
| Linting and formatting (`ruff`) | `python3 -m ruff check . && python3 -m ruff format --check .` (`src/api`) | Passed | `All checks passed! 202 files already formatted` |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01` all checked `[x]`; zero unchecked markers remain)
* Completed-work evidence and handoff prose: Reconciled across `role-screens.js`, `app.js`, `ops.js`, and `test_procurement_contractor_screen_wcag.py`
* Validation, blockers, remaining work, and follow-up items: Reconciled (`0` blockers, `0` remaining work items, `3` evidence-grounded follow-up items)
* Review readiness: Ready for review

## Blockers

* None

## Remaining Work

* None in active plan scope.

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/procurement-contractor-wcag-228-plan.md, `## Follow-Up Items`
* Reconcile `src/api/checks/procurement_screens_browser_check.py` with parent-branch `screenCapacityState` (`#1716`) and `journeyStageMap` (`#233`) expectations and extend it to exercise `Go to ...` jump links and `#/role/{procurement,contractor}` route aliases (`Refs #228`).
* Align sibling specialist role-screen jump helpers (`assetJumpNav`, `financeJumpNav`) to emit `role="navigation"` and `Go to ...` link labels consistently with `screenJumpNav` and `procurementJumpNav`.
* Complete manual assistive-technology and resident/staff usability acceptance on `#228` (`#151`, `#155`).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan (`P01`, `P02`, `P03`); completed: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`; remaining: none
* Validation coverage: 71/71 procurement/WCAG tests passed, 100/100 sibling conformance/UX tests passed, `mypy` clean across 286 files, `ruff check` and `ruff format --check` clean across 202 files
* Blockers: None
* Current plan and detail updates: Checked off `P03` and `P03-T01`; recorded follow-up-only `procurement_screens_browser_check.py` drift item in `## Follow-Up Items`
* Planning and critique state: Ready (`PC-001`..`PC-005` resolved)
* Follow-up items: 3 current, evidence-grounded follow-up items synchronized with plan
* Review readiness or no-handoff reason: Ready for review
* Continuation owner: Parent automatic RPI Agent (transitions automatically to Review)
