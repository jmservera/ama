<!-- markdownlint-disable-file -->
# RPI Plan: Map count and tile-fallback regression (issue 1836)

## Task Metadata

* Task ID: issue-1836-map-regression
* Task slug: issue-1836-map-regression
* Planning status: ready
* Plan date: 2026-11-17
* Phase details: .copilot-tracking/details/2026-11-17/issue-1836-map-regression-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-17/issue-1836-map-regression-plan-critique.md

## Executive Summary

The map shows two adjacent `role=status` paragraphs: the result count ("0 homes shown") and the tile-fallback note. The old test locator `.map-info [role=status]` matched both, so Playwright strict mode rejected it. Main already works around that with `.first`, which is positional and untested against the tile states. This plan adds a focused, committed browser regression with synthetic tile responses, one shared unambiguous count locator that the full map harness now uses, a small unit and static guard that fails when the bare selector returns, and a README note. No production code changes.

### User Decisions and Requirements Highlights

* Test-only scope: no UI redesign, no production change, no duplicate of the existing `.first` fix.
* The old locator is reproduced only as a labelled, intentional demonstration that passes when the strict-mode violation is observed.
* Axe stays on, with no skips, no relaxed contrast and no changed network policy.

### What You May Not Know

* The old locator fails in both tile states, not only when the fallback shows: the fallback paragraph always exists and is merely empty and hidden when tiles load.
* The unmodified full harness fails here at 390x568 by 0.17px under the container's default `system-ui` font (WenQuanYi Zen Hei). Under a dedicated Liberation Sans fontconfig it passes. The font is a runtime qualification, not a check change.
* The independent exact-head review and hosted CI are coordinator work and remain pending.

### Unresolved Decisions or Blockers

* None blocking. Independent review and hosted checks are pending with the coordinator.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements).

## User Decisions and Requirements

* Issue 1836 only; branch `test/map-tile-status-regression-1836`, target `main`, pinned origin/main 9da3fcd0dbc0f148ccc2abc350de3bfd96757392 (task brief).
* No dependency on unpublished 440 or 1641; do not touch their candidates (task brief).
* Current source already has the `.first` fix; do not duplicate an implementation fix (task brief).
* Reproduce the strict-mode failure by deliberately applying the old locator to a synthetic zero-result filter, and distinguish it from any failure of the current harness (task brief item 1).
* Assert exact "0 homes shown" with a precise unambiguous locator; independently assert the fallback is visible on tile failure and hidden on successful synthetic tile responses (item 2).
* Add a focused committed regression in existing patterns that fails if the old selector is restored, covers both tile states and never reaches external services or real resident data (item 3).
* Run `checks.map_fullscreen_browser_check` with axe, zero unexpected skips, the focused regression, and affected unit and static checks; preserve failed attempts; no no-op axe, relaxed contrast, suppression, network-policy change or scenario-integrity bypass (item 4).
* Commit original RPI evidence and test changes with qualified results; independent review and hosted checks stay pending (item 5).
* Validation tier FOCUSED while test-only; escalate if scope changes; no blanket full gate (task brief).

## Goals

* Give the count-versus-fallback relationship durable regression coverage.
* Replace the positional `.first` in the full harness with one named unambiguous locator.
* Exercise the tile-available state, which the full harness never reaches.

## Scope and Non-Goals

### In Scope

* New `src/api/checks/map_tile_status_browser_check.py`.
* `src/api/checks/map_fullscreen_browser_check.py`: import the shared count locator in place of three `.first` uses.
* New `src/api/tests/test_map_status_locators.py`.
* `src/api/README.md`: document the focused check next to the map harness.
* RPI evidence under `.copilot-tracking`.

### Non-Goals

* `app.js`, CSS, server, workflows, Dockerfiles, dependency pins, gate tools, the scenario manifest.
* Fixing the container's font fallback in the repository, or relaxing the 390x568 geometry check.
* Full gate, SQL, cloud or model activity.

## Functional Requirements

* The focused check signs in with synthetic data, reaches the zero-result support filter, and runs once with tiles fulfilled and once with tiles aborted.
  * Observable acceptance criteria: both runs assert exactly one count notice reading "0 homes shown".
* The fallback note is checked separately from the count.
  * Observable acceptance criteria: visible with the fallback text when tiles abort; empty and hidden when tiles are fulfilled, asserted only after the tile set is non-empty with at least one `.leaflet-tile-loaded` and no `.leaflet-tile:not(.leaflet-tile-loaded)` (critique PC-002).
* The old locator is applied deliberately in both states.
  * Observable acceptance criteria: the demonstration check passes only when Playwright reports "strict mode violation" with two matched elements, and its name states it is intentional.
* The full harness uses the shared count locator.
  * Observable acceptance criteria: no bare `.map-info [role=status]` remains in `map_fullscreen_browser_check.py`.

## Non-Functional Requirements

* No external reach or real data.
  * Objective threshold or evaluation condition: routing is installed before navigation, continues only the loopback origin, fulfils or aborts tile requests by state and aborts everything else; every non-loopback URL is recorded and only the tile host may appear (critique PC-001).
* Type and lint clean.
  * Objective threshold or evaluation condition: `ruff check`, `ruff format --check` and strict `mypy` in `src/api` exit 0.

## Acceptance Criteria

* The focused check exits 0 with the intentional-demonstration checks passing in both states.
* Mutation evidence: restoring the bare selector in the shared locator makes the focused check fail; restoring it in the harness makes the static guard fail.
* `checks.map_fullscreen_browser_check` with pinned axe passes with zero skip lines, under the documented font qualification.
* New unit tests, `test_map_viewport_premise`, and Core `scenario_manifest` and `needs_inventory` tests pass.
* Evidence, changes record and review are committed in one clean local commit with the Copilot trailer.

## Implementation Context Record

| Context item | Current artifact or record |
|---|---|
| Plan | .copilot-tracking/plans/2026-11-17/issue-1836-map-regression-plan.md |
| Phase details | .copilot-tracking/details/2026-11-17/issue-1836-map-regression-phase-details.md |
| Latest critique | .copilot-tracking/reviews/plans/2026-11-17/issue-1836-map-regression-plan-critique.md |
| Relevant research | .copilot-tracking/research/2026-11-17/issue-1836-map-regression-research.md |
| Changes-record role | .copilot-tracking/changes/2026-11-17/issue-1836-map-regression-changes.md is created by implementation |
| Planning execution and readiness | Planning executed; ready after critique dispositions |
| Continuation context | Confirmed automatic mode: parent continues to Implement |

## Sources

* .copilot-tracking/research/2026-11-17/issue-1836-map-regression-research.md: findings, spike and baseline runs.
* src/api/tests/test_map_viewport_premise.py: existing unit pattern for map checks.
* src/api/pyproject.toml: lint and strict mypy configuration.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Focused regression and shared locator

* Intent: add the browser regression and the shared unambiguous locator, and use it in the full harness.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add the focused tile-status browser check

* Requirement and evidence: item 1-3; research spike.
* Expected result: new module with locators, intentional demonstration and two tile-state scenarios.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-17/issue-1836-map-regression-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Use the shared count locator in the full harness

* Requirement and evidence: item 2; harness lines 288, 338, 342.
* Expected result: three `.first` uses replaced.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-17/issue-1836-map-regression-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Guard tests and documentation

* Intent: make restoration of the old selector fail without a browser, and document the check.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add unit and static guard tests

* Requirement and evidence: item 3.
* Expected result: three focused tests that fail on restoration.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-17/issue-1836-map-regression-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Update the component README

* Requirement and evidence: directly related documentation.
* Expected result: command and behaviour note beside the map harness section.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-17/issue-1836-map-regression-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Validation and mutation evidence

* Intent: run the focused tier and prove the regression bites.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Run checks and mutation demonstrations

* Requirement and evidence: item 4.
* Expected result: logs under the external evidence directory; failures preserved.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-17/issue-1836-map-regression-phase-details.md

## Dependencies

* Heavy lock `/tmp/ama-rpi-heavy.lock`, taken non-blocking, for browser runs.
* Dedicated venv, pinned axe and fontconfig under the external evidence directory.

## Follow-Up Items

* Decide whether the 390x568 focus-geometry check should tolerate sub-pixel differences or CI fonts should be pinned; out of scope here because it would relax a check.
* Consider distinct ids or test ids on the two status paragraphs in `app.js`; a production change outside this test-only scope.

## Critique Disposition

One critique ran on the final candidate (reviews/plans/2026-11-17/issue-1836-map-regression-plan-critique.md), verdict Revise.

| Finding | Disposition |
|---|---|
| PC-001 fail-closed routing | Accepted; applied to Non-Functional Requirements and P01-T01 |
| PC-002 tile settlement criterion | Accepted; applied to Functional Requirements and P01-T01 |

No finding conflicted with user direction, none needed a user decision, residual risk none beyond the pending independent review. No second critique runs.
