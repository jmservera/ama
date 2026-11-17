<!-- markdownlint-disable-file -->
# RPI Changes: Map count and tile-fallback regression (issue 1836)

## Metadata

* Task ID: issue-1836-map-regression
* Related plan: .copilot-tracking/plans/2026-11-17/issue-1836-map-regression-plan.md
* Phase details: .copilot-tracking/details/2026-11-17/issue-1836-map-regression-phase-details.md
* Implementation date: 2026-11-17

## Execution Status

* Status: Complete
* Declared invocation scope: full plan
* Completed scope markers: P01, P01-T01, P01-T02, P02, P02-T01, P02-T02, P03, P03-T01
* All remaining active-plan markers: none
* Status basis: all tasks have completion evidence below. Independent review and hosted CI remain with the coordinator.

## Execution Summary

Test-only change. The focused check serves synthetic tile responses (success and abort), reaches "0 homes shown" and asserts count and fallback independently. The full harness now uses the shared unambiguous count locator instead of `.first`. No production code, dependency, permission, network policy or scenario recipe bytes changed, so the FOCUSED tier holds.

## Completed Work

### Focused tile-status browser check (P01-T01)

* Files: src/api/checks/map_tile_status_browser_check.py
* What changed and why: exports MAP_STATUSES (single literal), COUNT_NOTICE, count_notice, tile_notice; route handler fulfils the tile host with a 1x1 PNG or aborts it, aborts all other non-loopback requests and records them (must be non-empty and tile host only). It labels an intentional old-locator demonstration that must raise a strict-mode violation.
* Validation: runs/focused-regression-1.log, exit 0, all PASS.

### Shared locator in the full harness (P01-T02)

* Files: src/api/checks/map_fullscreen_browser_check.py
* What changed and why: three `.first` count assertions replaced by count_notice(page).
* Validation: runs/full-harness-candidate-1.log, exit 0, 332 PASS, no FAIL, no skip (the two "FAIL|SKIP" grep hits are the scenario name "failed-map").

### Unit and static guard (P02-T01)

* Files: src/api/tests/test_map_status_locators.py
* What changed and why: helper narrowing, regex accept/reject, and a guard that the bare selector literal appears only once, in the focused check.

### README (P02-T02)

* Files: src/api/README.md
* What changed and why: short paragraph and command for the focused check.

## Implementation-Time Plan and Detail Updates

None beyond the critique dispositions already in the plan.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|---|---|---|---|
| ruff check, ruff format --check, strict mypy | src/api | Passed | 224 files formatted, 309 sources clean |
| Map unit tests (5 modules, 32 tests) | src/api | Passed | includes new test_map_status_locators |
| Focused browser check | new module | Passed | runs/focused-regression-1.log |
| Full map harness with axe 4.10.3 | candidate | Passed | runs/full-harness-candidate-1.log, 332 PASS, 0 FAIL, 0 skip; run with Liberation Sans fontconfig override |
| Mutation: bare selector in count_notice | focused check | Failed as intended | runs/mutation-bare-selector-focused.log (AssertionError on ambiguous locator) |
| Mutation: bare selector in harness | static guard | Failed as intended | runs/mutation-harness-static.log |
| Mutations reverted | both files | Verified | sha256 identical to pre-mutation (runs/pre-mutation.sha). During revert, `git checkout` briefly reset the harness to main; the edit was reapplied and the hash matched |
| Core scenario_manifest and needs_inventory | src/core | Passed | 19 tests OK; recipe bytes untouched |
| git diff --check | worktree | Passed | no output |
| Full src/api unit discovery | src/api | Skipped | exceeded 700 s runtime and was stopped; targeted map modules ran instead |
| Default-font harness | baseline main | Failed (environmental) | 0.17px at 390x568 with the container's system-ui fallback; not fixed in repo, not relaxed |

## Pre-Review Reconciliation

* Plan markers and phase details: current
* Completed-work evidence and handoff prose: current
* Blockers: none. Follow-ups: 390x568 sub-pixel font sensitivity; distinct ids for the two status paragraphs in app.js.
