<!-- markdownlint-disable-file -->
# RPI Changes: Rebase Housing and Resident WCAG (#232) onto Programme Coordinator WCAG (#230)

## Metadata

* Task ID: 2026-11-15-housing-resident-wcag-232-c1
* Related plan: .copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/housing-resident-wcag-232-c1-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`)
* Completed scope markers: P01, P01-T01, P02, P02-T01, P02-T02
* All remaining active-plan markers: none
* Status basis: Every phase and task in the approved Cycle 1 plan has verified rebase, conflict-resolution, automated test, lint, strict `mypy`, migration, and Web Interface Guidelines evidence.

## Execution Summary

Completed full-plan Cycle 1 implementation (`P01-T01`, `P02-T01`, `P02-T02`) for Issue #232 (`PR #1786`). Configured repository-local privacy-safe Git identity (`8036360+jmservera@users.noreply.github.com`), fetched and rebased `feat/ux-232-resident-wcag` (`e2528cc63` and `af9fcb891` from `184b828e1` and `cffec920a`) onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`, including merged `PR #1784` for Issue #230), resolved the `isRoleScreensDestination` conflict in `app.js` and verified clean preservation of all `#230` and `#232` specialist-screen hunks in `role-screens.js`, extended `test_housing_resident_wcag_232.py` with `#230` + `#232` coexistence assertions, passed all Focused-tier, coupled WCAG, lint, format, strict `mypy`, migration, and refreshed `web-design-guidelines` checks, and reconciled all `.copilot-tracking/` artifacts for single-pass `rpi-review` and post-review atomic commit.

## Completed Work

### Rebase onto `origin/feat/demo-233-same-home-tensions-0825` and `#230` + `#232` Conflict Resolution (`P01`, `P01-T01`)

* Related phase or task: `P01`, `P01-T01`
* Files: `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/role-screens.js`
* What changed and why: Resolved GitHub noreply email (`8036360+jmservera@users.noreply.github.com`) via `gh api user` and configured `git config --local user.email` / `user.name`; ran `git fetch origin feat/demo-233-same-home-tensions-0825` and `git rebase origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`); resolved the three-way conflict in `isRoleScreensDestination(destination)` in `app.js` using `const target = String(destination || "").split("?")[0];` across `#/screens` and all nine `#/role/*` routes (`building_safety_lead`, `repairs`, `housing_officer`, `contact_centre`, `resident_engagement`, `procurement`, `contractor`, `programme_manager`, `retrofit_coordinator`); and verified clean auto-merge of `role-screens.js` preserving all nine `ROLE_HASH_SCREENS` aliases, `#230` (`programme-shared-queue`, `programme-funnel` ["Lifecycle and funnel"], `programmeCell`, `programmeQueue`, `programmeFunnel`, `programmeStepCell`, `programmeJumpNav`), and `#232` (`screenTable` `aria-live="polite"`, `roleScreensView` `announce()`, `#screen-queue`, `section#screen-evidence` with `aria-label="Evidence for ${c.id}"`, `data-state-cue="scope"` gated by `isResidentRoleScreen`, `resident-choice`, `resident-service-issues`, and `af9fcb891`'s inline two-line `document.getElementById` jump listener).
* Completion evidence: `git merge-base --is-ancestor origin/feat/demo-233-same-home-tensions-0825 HEAD` exited `0` (`af9fcb891` <- `e2528cc63` <- `6510b6fbc` <- `a1d0be5f6`), clean `git diff origin/feat/demo-233-same-home-tensions-0825...HEAD -- src/api/`, and zero conflict markers across `src/api`.
* Validation: Passed (`64` Focused unit tests + `65` coupled specialist WCAG tests).

### Post-Rebase `#230` + `#232` Coexistence Tests, Focused Validation, and Web Guidelines Audit (`P02`, `P02-T01`)

* Related phase or task: `P02`, `P02-T01`
* Files: `src/api/tests/test_housing_resident_wcag_232.py`
* What changed and why: Extended `verifyRouter()`, the `roleSource` VM context (`globalThis.__roleHashScreens = ROLE_HASH_SCREENS; globalThis.__programmeOverviewSections = programmeOverviewSections;`), and `test_contact_centre_housing_and_resident_routes_and_script_isolation` in `src/api/tests/test_housing_resident_wcag_232.py` to assert post-rebase coexistence of `#230` (`#/role/programme_manager`, `#/role/retrofit_coordinator`, registered screen `"programme-queue"`, and overview jump-target section IDs `"programme-shared-queue"` and `"programme-funnel"`) alongside `#232` (`#/role/housing_officer`, `#/role/contact_centre`, `#/role/resident_engagement`, `"resident-choice"`, and `"resident-service-issues"`). Refreshed `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` and audited changed web files in `file:line` format:
  * `src/api/src/zava_forward/api/web/app.js`: `✓ pass`
  * `src/api/src/zava_forward/api/web/role-screens.js`: `✓ pass` (plain ASCII `"Loading recorded evidence."` intentionally retained per `docs/reference/research/ux/content-standard.md` and `test_content_standard.py`)
  * `src/api/src/zava_forward/api/web/panels.js`: `✓ pass`
* Completion evidence: `64` Focused tests (`OK`), `65` coupled WCAG tests (`OK`), `ruff check` (`All checks passed!`), `ruff format --check` (`27 files already formatted`), `mypy` (`Success: no issues found in 294 source files`), `rename-zava-tests.py` (`Ran 25 tests - OK`), and `✓ pass` Web Interface Guidelines audit.
* Validation: Passed.

### Cycle 1 Tracking Artifacts and Cycle 0 Post-Rebase Addendum Reconciliation (`P02-T02`)

* Related phase or task: `P02`, `P02-T02`
* Files: `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-c1-changes.md`, `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md`, `.copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-c1-plan.md`, `.copilot-tracking/details/2026-11-15/housing-resident-wcag-232-c1-phase-details.md`
* What changed and why: Reconciled all `[x]` plan markers and `Complete` phase-detail statuses, recorded Cycle 1 changes evidence, and appended a concise Cycle 1 post-rebase addendum to `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md` while keeping Cycle 0 critique (`housing-resident-wcag-232-plan-critique.md`) and review (`housing-resident-wcag-232-review.md`) verdicts immutable.
* Completion evidence: Reconciled plan, details, and changes files ready for single-pass `rpi-review` and post-review atomic Conventional Commit (`Refs #232` + Copilot trailer, clean `git status --short`, no `git push`).
* Validation: Passed (Markdown/link and diff review).

## Implementation-Time Plan and Detail Updates

### Local Toolchain Runner Resolution (`P02-T01`)

* Affected plan area or markers: `## Dependencies` in `.copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-c1-plan.md` (`P02-T01`)
* What changed: Recorded that `/home/azureuser/source/ama/.venv` is an empty directory on this host while `/usr/bin/python3` (`python3`), `/home/azureuser/.local/bin/ruff` (`ruff 0.17.3`), and `/home/azureuser/.local/bin/mypy` (`mypy 2.4.1`) provide the active Python, linter, and type-checker binaries on `PATH` for the exact three caller selector sets.
* Why: Ordinary validation-command runner resolution without altering selector scope, flags, or coverage.
* Triggering evidence: `ls -la /home/azureuser/source/ama/.venv` and `which python3 ruff mypy`.
* User answer or decision: none needed (ordinary local validation-command runner alignment).
* Reconciliation performed: Updated `## Dependencies` in `housing-resident-wcag-232-c1-plan.md` and recorded exact commands and outputs in `## Validation Record`.
* Planning and critique state: Not needed (`Ready`, `PC-001` already applied).

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| Focused 5-module `unittest` (`PYTHONPATH=../core/src:../agents/src:src:../core/tests:../agents/tests python3 -m unittest tests/test_housing_resident_wcag_232.py tests/test_programme_coordinator_wcag_230.py tests/test_accessibility_baseline.py tests/test_content_standard.py tests/test_procurement_contractor_screen_wcag.py -v`) | P01–P02 (`#232` + `#230` + baselines) | Passed | `Ran 64 tests in 5.577s - OK` |
| Coupled specialist WCAG & conformance suites (`test_asset_exec_screen_wcag.py`, `test_technical_quality_screens_wcag.py`, `test_programme_screen_wcag.py`, `test_housing_resident_screen_wcag.py`, `test_data_steward_screen_wcag.py`, `test_role_screens.py`, `test_role_screens_conformance.py`) | P01–P02 | Passed | `Ran 65 tests in 3.745s - OK` |
| Ruff lint & formatting (`ruff check src/zava_forward/api tests/test_housing_resident_wcag_232.py checks/case_journey_browser_check.py` + `ruff format --check`) | `src/api` | Passed | `All checks passed!`, `27 files already formatted` |
| Strict type-checking (`mypy` in `src/api`) | `src/api` (`src`, `tests`, `checks`) | Passed | `Success: no issues found in 294 source files` |
| Migration regression (`python3 tools/rename-zava-tests.py`) | Repo root | Passed | `Ran 25 tests in 1.063s - OK` |
| Refreshed `web-design-guidelines` review (`command.md`) | `app.js`, `role-screens.js`, `panels.js` | Passed | `✓ pass` across all three changed web files in `file:line` format |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02` all `[x]` and `Complete`).
* Completed-work evidence and handoff prose: Reconciled across `app.js`, `role-screens.js`, `test_housing_resident_wcag_232.py`, and tracking artifacts.
* Validation, blockers, remaining work, and follow-up items: Reconciled (`0` blockers, `0` remaining active-plan tasks).
* Review readiness: Ready for single-pass `rpi-review`.

## Blockers

* None

## Remaining Work

* None in active plan scope (single-pass `rpi-review` and post-review parent-owned local Conventional Commit without `git push` complete the automatic RPI loop).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-c1-plan.md, `## Follow-Up Items`
* Align `NO_REGION_GAPS` for `resident-service-issues` (`Routes to ask` region from `#86`) in `src/api/checks/specialist_keyboard_browser_check.py` in a dedicated full-tier gate-tool PR (`#1294`) — outside Focused-tier non-gate scope; owned by harness maintainer.
* Complete human assistive-technology (`NVDA`, `JAWS`, `VoiceOver`) and `360px` mobile walkthroughs across `#/role/housing_officer`, `#/role/contact_centre`, `#/role/resident_engagement`, and `#/case/<id>?tab=resident` before closing Issue #232 (`#151`, `#155`) — owned by human accessibility reviewer.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan (`P01`, `P02`); completed: P01, P01-T01, P02, P02-T01, P02-T02; remaining: none
* Validation coverage: Focused 5-module `unittest` (`64` tests), coupled specialist WCAG suites (`65` tests), `ruff check`, `ruff format --check`, `mypy` (`294` files), `rename-zava-tests.py` (`25` tests), and refreshed `web-design-guidelines` review all passed
* Blockers: None
* Current plan and detail updates: Recorded host `PATH` toolchain binaries (`python3`, `ruff`, `mypy`) in `## Dependencies`
* Planning and critique state: Ready (`PC-001` applied directly)
* Follow-up items: Full-tier `specialist_keyboard_browser_check.py` update (`#1294`) and human AT/mobile walkthrough (`#151`, `#155`)
* Review readiness or no-handoff reason: Ready for single-pass `rpi-review`
* Continuation owner: parent (confirmed automatic RPI Agent)
