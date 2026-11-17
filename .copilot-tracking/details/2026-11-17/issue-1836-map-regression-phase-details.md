<!-- markdownlint-disable-file -->
# RPI Phase Details: Map count and tile-fallback regression (issue 1836)

## Metadata

* Task ID: issue-1836-map-regression
* Task slug: issue-1836-map-regression
* Related plan: .copilot-tracking/plans/2026-11-17/issue-1836-map-regression-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-17/issue-1836-map-regression-research.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
|---|---|---|---|
| P01 | Focused regression and shared locator | ready | P01, P01-T01, P01-T02 |
| P02 | Guard tests and documentation | ready | P02, P02-T01, P02-T02 |
| P03 | Validation and mutation evidence | ready | P03, P03-T01 |

Test ownership lock: additions are one new check module, one new test file with three tests, one README paragraph; removals are exactly the three `.first` expressions in the full harness. Canonical targets only; nothing generated. Semantic coverage comes from the browser check; the static guard is the only regression-style test and exists because the bare selector can reappear in a file the browser check does not run.

<!-- rpi:phase id=P01 -->
## P01: Focused regression and shared locator

### Context

The app builds `info` and `tileNote` as adjacent `role=status` paragraphs inside `.map-info`. Strict mode rejects the bare selector in both tile states. The full harness aborts all external requests so it only sees the fallback state.

### Intent

One named count locator, one named fallback locator, both exactly one element, exercised under fulfilled and aborted tiles.

### Boundaries

* Included: new check module; harness import and three replacements.
* Excluded: any production file; axe step; other checks.

### Likely Targets

* src/api/checks/map_tile_status_browser_check.py: new.
* src/api/checks/map_fullscreen_browser_check.py: three one-line edits and an import.

### Dependencies

* None.

### Validation Expectations

* Focused check and full harness pass under the heavy lock.

### Completion Evidence

* Logs in the external evidence directory; changes record.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add the focused tile-status browser check

#### Context

Spike `diag/spike_tiles.py` proved the approach. Playwright calls a route handler with `(route, request)`, so the handler must take one parameter and close over the mode rather than use a defaulted second argument.

#### Intent

Module exports `MAP_STATUSES`, `count_notice(page)`, `tile_notice(page)`, `COUNT_NOTICE`; runs `main(run_browser)` from `design_system_browser_check` with a real loopback API and synthetic data.

#### Boundaries

* Included: sign in as the synthetic user; area Point examples; assert "3 homes shown"; click the support tile for zero homes; for each of tiles available and tiles unavailable use a fresh context whose route is installed before navigation, continues only the loopback origin, fulfils (available) or aborts (unavailable) OSM tile requests and aborts every other request, recording each non-loopback URL; fail unless the record is non-empty and all on the OSM tile host (PC-001); in the available state assert the count and then, before asserting the note is empty and hidden, wait for at least one `.leaflet-tile-loaded` and zero `.leaflet-tile:not(.leaflet-tile-loaded)` (PC-002); assert count text exactly "0 homes shown" with count 1; fallback assertions per state; the intentional old-locator demonstration.
* Excluded: axe, screenshots, any production edit.

#### Likely Targets

* src/api/checks/map_tile_status_browser_check.py

#### Dependencies

* None.

#### Validation Expectations

* Exit 0; PASS lines include the intentional-demonstration checks for both states.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Use the shared count locator in the full harness

#### Context

Lines 288, 338 and 342 use `.first`.

#### Intent

Replace with `count_notice(page)`; behaviour and expectations unchanged.

#### Boundaries

* Included: import and three replacements.
* Excluded: other harness logic, thresholds, axe.

#### Likely Targets

* src/api/checks/map_fullscreen_browser_check.py

#### Dependencies

* P01-T01.

#### Validation Expectations

* Full harness with axe passes under the font qualification, zero skips.

<!-- rpi:phase id=P02 -->
## P02: Guard tests and documentation

### Context

`test_map_viewport_premise.py` shows the fake-page unit pattern under mypy strict.

### Intent

Browser-free failure when the bare selector or an unfiltered helper returns.

### Boundaries

* Included: new test file; README paragraph.
* Excluded: tests restating constants.

### Likely Targets

* src/api/tests/test_map_status_locators.py
* src/api/README.md

### Dependencies

* P01.

### Validation Expectations

* Unit tests pass; mutation makes them fail.

### Completion Evidence

* Logs.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add unit and static guard tests

#### Context

Three tests: the helper narrows the shared selector with the count pattern (fake page); the pattern accepts "0 homes shown" and "1 home shown" and rejects the fallback and cluster texts; neither `map_fullscreen_browser_check.py` nor any other map check contains the bare literal, and the new module contains it once in its labelled constant.

#### Intent

Fail when the old selector is restored.

#### Boundaries

* Included: typed fakes.
* Excluded: browser use.

#### Likely Targets

* src/api/tests/test_map_status_locators.py

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* `python -m unittest` for the file; ruff format and check; strict mypy.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Update the component README

#### Context

Map harness section begins around line 1005.

#### Intent

State the new command, what it proves, that it never reaches external services, and that the full harness uses the shared locator.

#### Boundaries

* Included: one paragraph and command block.
* Excluded: acceptance claims about axe or hosted CI.

#### Likely Targets

* src/api/README.md

#### Dependencies

* P01-T01.

#### Validation Expectations

* Diff review; plain ASCII.

<!-- rpi:phase id=P03 -->
## P03: Validation and mutation evidence

### Context

FOCUSED tier. Runs use the dedicated venv, pinned axe, `flock -n` on the heavy lock and, for browsers, `FONTCONFIG_FILE` pointing at the Liberation Sans override.

### Intent

Prove pass, prove the regression bites, preserve failures.

### Boundaries

* Included: focused check, full harness, unit tests, ruff, mypy, Core scenario_manifest and needs_inventory tests, `git diff --check`.
* Excluded: blanket gate.

### Likely Targets

* /mnt/tmp/ama-run-74bd1fe9-20261117/evidence-1836/runs/

### Dependencies

* P01, P02.

### Validation Expectations

* All pass; mutations fail as expected; skip lines are zero.

### Completion Evidence

* Changes record table.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Run checks and mutation demonstrations

#### Context

Mutations are temporary edits reverted immediately and verified with `git diff`.

#### Intent

Show the focused check fails with the bare locator in `count_notice`, and the static guard fails with the bare selector in the harness.

#### Boundaries

* Included: reverts verified.
* Excluded: committed mutations.

#### Likely Targets

* Logs only.

#### Dependencies

* P01, P02.

#### Validation Expectations

* Mutation runs fail for the stated reason.
