<!-- markdownlint-disable-file -->
# RPI Changes: Issue #230 Programme Manager and Coordinator Screens WCAG 2.2 Baseline

## Metadata

* Task ID: 2026-11-15-issue-230-programme-mgr-wcag
* Related plan: .copilot-tracking/plans/2026-11-15/issue-230-programme-mgr-wcag-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-230-programme-mgr-wcag-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan
* Completed scope markers: P01, P01-T01, P01-T02, P02, P02-T01, P02-T02
* All remaining active-plan markers: none
* Status basis: All planned phases and tasks (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`) completed and verified against Focused Tier unit, conformance, browser, type-checking, lint/format, and Web Interface Guidelines checks.

## Execution Summary

Delivered WCAG 2.2 baseline (#151) keyboard jump navigation and explicit non-colour textual state labels across both surfaces (`overview()` and `render()`) of the `programme-queue` specialist screen in `src/api/src/zava_forward/api/web/role-screens.js`, updated `src/api/tests/test_programme_screen.py`, and expanded `src/api/tests/test_programme_screen_wcag.py` with comprehensive semantic VDOM and delegated-event tests across all three installed roles (`Retrofit Programme Manager`, `Programme Support Officer`, and `Retrofit Coordinator`).

## Completed Work

### P01 (`P01-T01`, `P01-T02`): `programme-queue` WCAG 2.2 Keyboard Jump Navigation and Textual State Labels

* Updated `src/api/src/zava_forward/api/web/role-screens.js`:
  * Added `programmeJumpNav` (`<nav aria-label="..." class="screen-links">` with `<a href="#<id>" data-jump="<id>">Go to <section></a>`), `programmeOverviewSections` (`programme-overview-boundary`, `programme-shared-queue`, `programme-funnel`, `programme-overview-withheld`), and `programmeSections` (`programme-summary`, `programme-steps`, `programme-journey`, `programme-withheld`) using disjoint IDs and distinct link text when `overview()` and `render()` are co-mounted.
  * Wired `programmeJumpNav` and `screenJumpTarget` (`tabindex="-1"`) across `overview()` and `render()`, preserving ``screenPanel(`Connected view for ${c.id}`, ...)`` around sibling `#programme-summary` and `#programme-steps` targets, keeping `journeyStageMap(c)` free of internal `tabindex` attributes, and removing the superseded `<div role="group">` jump `<button>` bar and `programmeJump` inline handler so read-only `render()` renders zero `<button>` elements.
  * Added explicit `"aria-live": "polite"` alongside `role: "status"` on `#programme-filter-status` and `#programme-page-status` in `programmeQueue()`.
  * Added explicit non-colour textual state prefixes in `programmeRow()` (`"State: Returned. ..."`, `"State: Not returned. Handoff state: ..."`, `"State: Not returned"`), `programmeFunnel()` (`"State: Unknown. Lifecycle and funnel counts are Unknown. No record was supplied."`, `"State: Recorded stage history (not a pass). ..."`), and `programme-queue.render()` (`"State: Warning. No blocker is recorded, which does not confirm readiness."` when unblocked, plus `Action needed:` / `Warning:` prefixes in `State summary in words`).

### P02 (`P02-T01`, `P02-T02`): WCAG 2.2 Unit/Accessibility Tests and Focused Tier Validation

* Updated `src/api/tests/test_programme_screen.py`:
  * Replaced two obsolete `button == 4` assertions on read-only `render()` with `self.assertNotIn("button", tags(node))`.
* Expanded `src/api/tests/test_programme_screen_wcag.py`:
  * Updated `SCRIPT` to wire document-level `click` delegation, render `overview()` alongside `render()` across roles and queue/funnel/step states, and exercise pager boundary focus handoff.
  * Retained `test_blocked_steps_start_with_action_needed`, `test_clear_steps_are_a_warning_never_a_pass`, and `test_existing_state_cells_are_unchanged`, and added six focused semantic tests verifying overview and connected-home `<nav aria-label>` jump bars, co-mounted disjoint IDs and distinct link labels, delegated `a[data-jump]` `preventDefault()` + `.focus()` + missing-target safety, returned/handoff/funnel textual state prefixes, `aria-live="polite"` status regions, focusable table scroll regions, and Previous/Next pager focus handoff (9 tests total).

## Implementation-Time Plan and Detail Updates

* Local judgment / immediately relevant current-state update reconciled in `FR-01`, `FR-02`, `FR-04`, `AC-01`, and `P01-T01`:
  * Used `programmeJumpNav` (`class="screen-links"`, matching `asset-board` #226 and `safety_repairs` #227) and placed the connected-home jump `<nav>` inside ``screenPanel(`Connected view for ${c.id}`, ...)`` immediately below the intro paragraph. In real Chromium 156 (`1280x900`), `.screen-record` uses `content-visibility: auto`; keeping the compact `.screen-links` jump bar and keeping the connected-home jump bar inside ``Connected view for ${c.id}`` keeps ``Connected view for ZF-1`` within Chromium's initial layout margin (`top < 2250px`), so `checks/role_screens_browser_check.py 230` passes cleanly with zero modifications to `checks/*.py` or `style.css`.
  * Used `"State: Recorded stage history (not a pass)."` in `programmeFunnel()` to avoid introducing `"readiness"` while preserving `"not a pass"` for `test_programme_screen.py`.

## Validation Record

* Validation tier classification: **Focused Tier** (owner decision D4 / #1294: scoped specialist-screen web UI and unit-test change touching `role-screens.js`, `test_programme_screen.py`, and `test_programme_screen_wcag.py`; zero changes to infrastructure, deployment, SQL, security controls, workflows, Dockerfiles, or dependency manifests). Hosted CI has not run because pushing is prohibited by user instructions (`Do NOT push; leave a clean frozen local commit`).

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `test_*programme*.py` (`unittest`) | `test_programme_screen.py` + `test_programme_screen_wcag.py` | Passed | `Ran 33 tests in 2.925s - OK` |
| Cross-cutting conformance suites (`unittest`) | 12 modules (`test_accessibility_baseline`, `test_role_screens`, `test_role_screens_conformance`, `test_role_screens_connected_journey`, `test_role_screens_same_home_identity`, `test_role_screens_stage_map_focus`, `test_role_screens_tensions_same_home`, `test_specialist_keyboard_check`, `test_connected_home_check`, `test_atlas_tensions_checker`, `test_design_system`, `test_content_standard`) | Passed | `Ran 133 tests in 1.810s - OK (skipped=3)` |
| `python3 -m mypy` | `src/api` strict typing (285 source files) | Passed | `Success: no issues found in 285 source files` |
| `python3 -m ruff check src tests && python3 -m ruff format --check src tests` | `src/api` lint and formatting | Passed | `All checks passed!` and `200 files already formatted` |
| `python3 -m checks.programme_paging_browser_check` | Real Chromium 156.0.8078.4 (`1280px` + `320px`) | Passed | Pager Tab order, boundary focus handoff, scope filter/reset, read-only connected view, and zero horizontal overflow all `PASS` |
| `python3 -m checks.role_screens_browser_check 230` | Real Chromium 156.0.8078.4 (`pam@example.test` + `coordinator@example.test`, `320px`/`390px`/`1280px`) | Passed (axe skipped) | All DOM, keyboard Tab/Shift+Tab/Reset, 5 textual step states, non-readiness, reflow, and read-only checks `PASS`; `PARTIAL: axe scan skipped for 4 views (ZF_AXE_JS unset)` disclosed honestly |
| `python3 -m checks.connected_home_browser_check` | Real Chromium 156.0.8078.4 cross-role journey | Passed | All `programme-queue` (`ZF-1` + `ZF-2`) and cross-role connected-home checks `PASS` |
| `specialist_keyboard_browser_check.walk_screen` + 8 jump links | Real Chromium 156.0.8078.4 (`Retrofit Programme Manager`, `Retrofit Coordinator`, `Programme Support Officer`) | Passed | Full keyboard walk plus visible focus, `Enter` target focus (`document.activeElement.id`), and SPA hash route preservation verified across all 8 `a[data-jump]` links |
| `web-design-guidelines` (`command.md` fresh `web_fetch`) | `src/api/src/zava_forward/api/web/role-screens.js` | Passed | `✓ pass` (0 `file:line` violations; owner-selected Fluent 2 / plain-language sentence-case standards preserved) |
| Hosted GitHub Actions CI | Exact head on remote | Not run (by instruction) | User explicitly instructed `Do NOT push; leave a clean frozen local commit` |

## Pre-Review Reconciliation

* Plan markers and phase details: reconciled (`[x]` on `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`; `complete` in `Phase Index`)
* Completed-work evidence and handoff prose: reconciled
* Validation, blockers, remaining work, and follow-up items: reconciled
* Review readiness: Ready for `rpi-review`

## Blockers

* none

## Remaining Work

* none in declared implementation scope

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/issue-230-programme-mgr-wcag-plan.md, `## Follow-Up Items`
* Live assistive-technology (NVDA/JAWS/VoiceOver) and user walkthrough validation across specialist screens remains outside this engineering slice and is tracked under #155 per `docs/reference/research/ux/wcag-conformance-baseline.md`.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed: P01, P01-T01, P01-T02, P02, P02-T01, P02-T02; remaining: none
* Validation coverage: Focused Tier complete (`test_*programme*.py` 33/33, 12 conformance suites 133/133, `mypy` 285 files, `ruff check` + `ruff format --check`, real Chromium `programme_paging_browser_check`, `role_screens_browser_check 230` [with `ZF_AXE_JS` unset disclosed], `connected_home_browser_check`, `specialist_keyboard_browser_check` `programme-queue` + 8 jump links, and fresh `command.md` audit); hosted CI unrun because push is prohibited
* Blockers: none
* Current plan and detail updates: reconciled `programmeJumpNav` (`class="screen-links"`, connected-view placement inside ``Connected view for ${c.id}``) and `"State: Recorded stage history (not a pass)."` funnel prefix
* Planning and critique state: Ready (PC-001 through PC-004 resolved)
* Follow-up items: #155 live assistive-technology and user walkthrough validation
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: parent for confirmed automatic RPI Agent

