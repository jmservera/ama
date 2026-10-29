<!-- markdownlint-disable-file -->
# RPI Phase Details: Expanded map filters

## Metadata

* Task ID: 551
* Task slug: map-filters-551
* Plan: .copilot-tracking/plans/2026-10-29/map-filters-551-plan.md
* Evidence: .copilot-tracking/research/2026-10-29/map-filters-551-research.md

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Implement shared compact filters | Complete | P01-T01, P01-T02 |
| P02 | Verify acceptance and regressions | Complete | P02-T01 |

<!-- rpi:phase id=P01 -->
## P01: Implement shared compact filters

Context: Overview owns the tiles and area selection; mapPanel owns modal state.
Intent: share existing nodes across the header and modal rather than duplicate
state. Boundaries: optional Overview controls only; Coordinator unchanged.
Dependencies: final-candidate critique. Completion: source diff plus P02 evidence.
Unresolved: none.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Reparent existing controls and preserve selected-button focus

* Targets: app.js overviewView and mapPanel.
* Add an optional filter-group argument and an original header slot returned
  with the panel. Construct the Overview filters before panel creation.
* On expand insert the group between map heading and workspace. On collapse
  return it to its original slot, including disposal paths.
* Keep all six button elements stable. Update aria-pressed and the existing
  tile-selection span without replaceChildren after activation.
* Keep one mapArea ID and original handler, and preserve existing ovState.
  Change both handlers to start draw(true) without returning its promise:
  use existing map-region progress and error handling so AsyncAction does not
  disable the active control or append per-control loading text. Ignore an
  already selected flag; distinct controls remain usable during reads.
* Reuse all existing request sequencing, error and selected-card handling.
* Preserve the geographic centre while moving/resizing the controls with
  invalidateSize({pan:true, animate:false}); the first browser run demonstrated
  that pan:false displaces the viewport. Update its existing source assertion.
* Reserve bottom fitting padding for wrapped attribution: 60px bottom versus
  30px top. The short-height scan demonstrated the directly coupled obstruction.
* Completion: no duplicate controls/state and filter focus survives updates.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add compact responsive styles and usage documentation

* Targets: style.css and src/api/README.md expanded-map section.
* Restrict compact styles to dialog descendants. Use existing tokens, readable
  wrapping grid, normal-size compact counts and visible selection words.
* Hide only the noninteractive Completed tile while expanded.
* Keep area selector labelled and narrow-safe, and preserve at least a usable
  map workspace at all required widths/text size.
* Expanded filter group: maximum 45% panel height, overflow:auto,
  overscroll-behavior:contain and padding for focus rings. Workspace minimum
  14rem height and width >80px. Allow the containing panel to scroll at extreme
  text sizes; exit/manual paths remain keyboard reachable.
* No new animation or framework; preserve forced-colours and focus styling.
* Completion: actual geometry, screenshots and usage/validation documentation.
* Dependencies: P01-T01.

<!-- rpi:phase id=P02 -->
## P02: Verify acceptance and regressions

Context: real local app is available through the existing harness. Intent:
prove behavior rather than rely on source string tests alone.
Boundaries: constructed local data only, external app requests aborted.
Dependencies: P01. Completion: exact commands, outputs and limits in Changes.
Unresolved: complete publication gate is intentionally not run because az is
forbidden and no push is requested.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Extend and execute local automated checks

* Test source contracts: optional filter slot and movement; stable button update.
* Update the existing exact-signature MAP extractor for the new optional
  parameter, preserving every existing test and assertion.
* Add one helper to the existing Playwright harness; execute before its existing
  interactions and reset to the original fixture state afterward.
* At desktop, record original node handles, expand, check controls above map,
  compact count size and hidden Completed; use Space/Enter to select flags and
  verify marker identities/counts and retained focus.
* Change area in expanded mode; collapse and verify original node identity,
  selected words/aria-pressed and area; change header, expand again and verify.
* Exercise all six flags including zero-result filters. Restore open cases and
  Point examples before returning so old regression tests remain valid.
* At 320/390/1280, check every filter label fits, no horizontal overflow,
  keyboard reachability, 40px targets and usable map space; scan with axe.
* Add 390x568 with map height >=14rem and width >80px, filter scroll bounds
  and keyboard reachability of exit/manual list. Include pending progress.
* Hold a flag response while asserting activeElement, stable identity, enabled
  controls, map aria-busy, Tab order and toolbar geometry. Change a distinct
  filter or area while the first read is held, release out of order and verify
  the latest flag/area wins. Use existing failure/recovery cases as regressions.
* Extend the existing 640px/32px-font browser check for filter bounds, map height
  >=14rem and keyboard reachability through the scrollable filter region.
* Run from src/api with /tmp/mv: unittest test_map_fullscreen,
  test_accessibility_baseline, test_design_system, test_content_standard,
  test_loading_feedback, test_workspace_scripts; node --check app.js.
* Execute checks.map_fullscreen_browser_check against the real loopback app,
  with the existing integrity-pinned axe. Retain reports/screenshots externally.
* Run existing Ruff/mypy selectors for changed Python where available.
* After implementation, reconcile all checklist markers and evidence, then
  activate exactly one independent Review; do not loop back after Review.

## Completion Evidence

P01-P02 complete: 35 targeted unittest tests, node syntax, Ruff and mypy pass.
The final local real-server Chromium run passed 247 assertions and 14 axe
states with zero violations/uncaught errors, including 390x568 and 640px with
32px browser-default text. Commands, original failed attempts, measured
geometry and external report locations are in the Changes artifact.
No required human acceptance or publication checkbox is marked complete.
