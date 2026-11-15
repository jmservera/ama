<!-- markdownlint-disable-file -->
# RPI Changes: Issue #228 Cycle 1 Parent Rebase onto Updated Parent (#1639)

## Metadata

* Task ID: issue-228-c1-parent-rebase
* Related plan: .copilot-tracking/plans/2026-11-15/228-procurement-wcag-c1-rebase-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/228-procurement-wcag-c1-rebase-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01`
* All remaining active-plan markers: none
* Status basis: Rebased `feat/ux-228-procurement-wcag` (`0486e2ca1` -> `e9f74e39c`) onto `origin/feat/demo-233-same-home-tensions-0825` (`fe63981978970e38cafed5ebe3d38eb7f9a13cf8`), upgraded all 6 `#228` tables in `role-screens.js` to `screenRecordTable` (`scope="row"`), expanded `test_procurement_contractor_screen_wcag.py` for 6-alias coexistence (`PC-001`) and row-header scopes, passed all Focused Tier checks (`node --check`, `ruff`, `mypy`, and 183 unit tests across 16 modules), and prepared the clean pre-review commit.

## Execution Summary

Completed the Cycle 1 parent rebase of `feat/ux-228-procurement-wcag` onto `origin/feat/demo-233-same-home-tensions-0825` (`fe63981978970e38cafed5ebe3d38eb7f9a13cf8`, incorporating merged PRs `#1759` (`#134`), `#1762` (`#230`), `#1763` (`#232`), `#1757` (`#135`), and `#1764` (`#229`)). Resolved the two `#/role/*` routing conflicts in `app.js` and `role-screens.js`, normalized `route()` onto a single `baseHash` binding, upgraded all six `#228` specialist tables (`procurement-packages` x4, `contractor-job-pack` x2) from `screenTable` to `#232`'s `screenRecordTable` (`<th scope="row">`) while preserving `#228`'s `screenNodeValue` DOM badge support, confirmed `test_accessibility_baseline.py` and `wcag-conformance-baseline.md` remain exact (`sites=9`, `tables=14`, `fixed=2`), and verified 183 tests across 16 unit test modules alongside `node --check`, `ruff`, and `mypy`.

## Completed Work

### Parent Rebase and `#/role/*` Routing Reconciliation

* Related phase or task: `P01`, `P01-T01`
* Files: `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/role-screens.js`
* What changed and why: Configured local privacy-safe noreply Git identity (`8036360+jmservera@users.noreply.github.com`), fetched `origin/feat/demo-233-same-home-tensions-0825` (`fe63981978970e38cafed5ebe3d38eb7f9a13cf8`), rebased `0486e2ca1` (`-> e9f74e39c`), unioned all six `#/role/*` routes (`building_safety_lead`, `repairs`, `housing_officer`, `resident_engagement`, `procurement`, `contractor`) in `app.js` `isRoleScreensDestination` and `role-screens.js` `ROLE_HASH_SCREENS`, and unified `hashBase` / `baseHash` onto a single `const baseHash = hash.split("?")[0];` in `app.js` `route()`.
* Completion evidence: `git merge-base --is-ancestor fe63981978970e38cafed5ebe3d38eb7f9a13cf8 HEAD` exited `0`; `ops.js` and `#228` files replayed cleanly with zero remaining conflict markers.
* Validation: Passed (`node --check` on `app.js`, `ops.js`, `role-screens.js`; `test_role_hash_aliases_and_nav_active_mapping`).

### `screenRecordTable` Row-Header Alignment and Coexistence Tests

* Related phase or task: `P02`, `P02-T01`
* Files: `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/tests/test_procurement_contractor_screen_wcag.py`
* What changed and why: Upgraded all 4 tables in `procurement-packages` (`Packages with period, scope, version and capacity`, `Work-order references for the selected home`, `Work-order corrections, recorded completion and review for the selected home`, `Unmet prerequisites for ${wording(p.id)}`) and both tables in `contractor-job-pack` (`Your work orders for this home`, `Evidence checklist for this job pack`) from `screenTable` to `screenRecordTable` so column 0 emits `<th scope="row">` while preserving DOM `procurementBadge` cues via `screenNodeValue`. Extended `test_role_hash_aliases_and_nav_active_mapping` to exercise all 6 `#/role/*` aliases (using `"Resident Liaison Officer"` and `aria-labelledby="screen-evidence-heading"` for `#232`'s two resident routes per `PC-001`) and added `test_procurement_and_contractor_tables_use_col_and_row_header_scopes`. Verified `test_accessibility_baseline.py` and `docs/reference/research/ux/wcag-conformance-baseline.md` required zero count edits (`9 / 14 / 2`).
* Completion evidence: All 6 `#228` tables verified in Node VM DOM tests with `thead th[scope="col"]` and `tbody tr > th:first-child[scope="row"]`; zero test removals; zero edits to `#232`'s `roleScreensView`.
* Validation: Passed (`tests.test_procurement_contractor_screen_wcag`, `tests.test_procurement_screens`, `tests.test_accessibility_baseline`, `tests.test_content_standard`).

### Focused Tier Static Analysis, 6-Issue Unit Test Matrix, and Clean Local Commit

* Related phase or task: `P03`, `P03-T01`
* Files: `.copilot-tracking/changes/2026-11-15/228-procurement-wcag-c1-rebase-changes.md`, `.copilot-tracking/plans/2026-11-15/228-procurement-wcag-c1-rebase-plan.md`, `.copilot-tracking/details/2026-11-15/228-procurement-wcag-c1-rebase-phase-details.md`, `.copilot-tracking/rpi-sessions/2026-11-15/228-procurement-wcag-c1-rebase-state.json`
* What changed and why: Executed `node --check`, `ruff check`, `ruff format --check`, `mypy`, and the 16-module `unittest` suite inside `src/api` via `/usr/bin/python3` (no `uv`), reconciled plan and detail markers, and staged all rebased source/test updates and implementation-phase tracking files for the clean pre-review local commit.
* Completion evidence: All Focused Tier checks exited `0` (`183` unit tests `OK`, `291` `mypy` source files clean, `206` `ruff` formatted files clean).
* Validation: Passed.

## Implementation-Time Plan and Detail Updates

### Include `tests` Directory on `PYTHONPATH` for Explicit Module Invocation Parity

* Affected plan area or markers: `P03`, `P03-T01`
* What changed: Appended `:tests` to `PYTHONPATH` (`PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src:tests`) in `P03` and `P03-T01` when running explicit `tests.*` targets via `/usr/bin/python3 -m unittest`.
* Why: Existing `src/api/tests/test_procurement_screen_wcag.py` uses `from test_procurement_screens import ORDER, PACKAGE, SCRIPT, WEB` (relying on `tests/` being on `sys.path` during `unittest discover -s tests`). Including `:tests` matches `unittest discover -s tests` without touching sibling test files.
* Triggering evidence: `ImportError` on bare `from test_procurement_screens import ...` when invoking explicit dotted module names without `:tests` on `PYTHONPATH`; resolved immediately with `183` tests `OK`.
* User answer or decision: None needed (ordinary local current-state update preserving approved `/usr/bin/python3` runner intent).
* Reconciliation performed: Updated `P03` and `P03-T01` in `228-procurement-wcag-c1-rebase-plan.md` and `228-procurement-wcag-c1-rebase-phase-details.md`.
* Planning and critique state: Current and ready (`PC-001` and `PC-002` preserved).

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `node --check` | `app.js`, `ops.js`, `role-screens.js` | Passed | Exited `0` on all three web scripts |
| `/usr/bin/python3 -m ruff check src tests checks` | `src/api` | Passed | `All checks passed!` |
| `/usr/bin/python3 -m ruff format --check src tests checks` | `src/api` | Passed | `206 files already formatted` |
| `/usr/bin/python3 -m mypy` | `src/api` (`291` source files) | Passed | `Success: no issues found in 291 source files` |
| `/usr/bin/python3 -m unittest` (16 modules) | `#228`, `#229`, `#230`, `#232`, `#135`, `#134`, `test_accessibility_baseline`, `test_content_standard`, `test_role_screens_conformance`, `test_design_system` | Passed | `Ran 183 tests in 18.256s — OK` |
| Browser Playwright + axe harness | `specialist_keyboard_browser_check.py` | Skipped | Opt-in browser-tier check outside Focused Tier scope; tracked in `## Follow-Up Items` |

## Pre-Review Reconciliation

* Plan markers and phase details: Current (`P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01` checked `[x]` and marked `Complete`)
* Completed-work evidence and handoff prose: Current
* Validation, blockers, remaining work, and follow-up items: Current (`0` blockers, `0` remaining items, `2` follow-ups mirrored from plan)
* Review readiness: Ready for single-pass `rpi-review` after clean pre-review commit (`git status --short` empty)

## Blockers

* None

## Remaining Work

* None

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/228-procurement-wcag-c1-rebase-plan.md, `## Follow-Up Items`
* Execute Chromium Playwright + axe runtime checks (`src/api/checks/specialist_keyboard_browser_check.py`) across `#/role/procurement` and `#/role/contractor` when a browser-tier validation gate runs (`owner: follow-up UX browser check`).
* Complete human assistive-technology testing (`#151`) and participant perspective walkthroughs (`#155`) before claiming WCAG 2.2 AA conformance acceptance or ticking human criteria on `#228` (`owner: #151 / #155`).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan (`P01`, `P02`, `P03`); completed: `P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01`; remaining: none
* Validation coverage: Focused Tier passed (`node --check` x3, `ruff check`, `ruff format --check` on 206 files, `mypy` on 291 files, and `unittest` 183 tests across 16 modules covering `#228`, `#229`, `#230`, `#232`, `#135`, `#134`, `test_accessibility_baseline`, `test_content_standard`, `test_role_screens_conformance`, `test_design_system`)
* Blockers: None
* Current plan and detail updates: Appended `:tests` to `PYTHONPATH` in `P03` / `P03-T01` for `unittest discover -s tests` import parity
* Planning and critique state: Ready (`PC-001` and `PC-002` resolved and honored)
* Follow-up items: 2 mirrored from plan (`specialist_keyboard_browser_check.py`; human `#151/#155` validation)
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: parent (`confirmed automatic RPI Agent`)
