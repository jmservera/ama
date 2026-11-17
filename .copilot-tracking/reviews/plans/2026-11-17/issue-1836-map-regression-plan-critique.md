<!-- markdownlint-disable-file -->
# RPI Plan Critique: issue-1836-map-regression

## Metadata

* Task ID: issue-1836-map-regression
* Plan: .copilot-tracking/plans/2026-11-17/issue-1836-map-regression-plan.md
* Phase details: .copilot-tracking/details/2026-11-17/issue-1836-map-regression-phase-details.md
* Critique run: once, by a fresh rubber-duck worker, on the final candidate. No second critique runs for this task.
* Worker verdict: Revise
* Persistence note: the worker reported that it could not write this file under its read-only constraint. The planner persisted its returned finding set here unchanged in substance, with dispositions added below. The worker also stated it found no other actionable findings.

## Findings

### PC-001 Blocking: network interception does not specify fail-closed routing

* Evidence: phase details P01-T01 required recording and checking external URLs but did not say unexpected requests are aborted before they leave.
* Impact: a post-hoc assertion could notice an external request only after it was sent.
* Action owner: planner.
* Resolving action: install routing before navigation that continues only the owned loopback origin, fulfils or aborts tile requests by state, aborts every other request, records every non-loopback URL and fails the check when any is not on the tile host.
* Application: direct; no user decision needed.

### PC-002 Blocking: the successful tile state lacks a settlement criterion

* Evidence: plan functional requirement said "after loaded tiles are observed"; app.js clears the note asynchronously on the Leaflet `load` event, and one loaded tile does not mean the layer finished.
* Impact: a premature hidden-notice assertion could pass vacuously.
* Action owner: planner.
* Resolving action: before asserting the note is empty and hidden, require a non-empty tile set with at least one `.leaflet-tile-loaded` and zero `.leaflet-tile:not(.leaflet-tile-loaded)`.
* Application: direct; no user decision needed.

## Verdict

Revise: both findings are planner-owned and applied directly below; no user decision is required and no further critique runs.

## Disposition

| Finding | Disposition | Where applied |
|---|---|---|
| PC-001 | Accepted and applied | Phase details P01-T01 Boundaries; plan Non-Functional Requirements |
| PC-002 | Accepted and applied | Phase details P01-T01 Boundaries; plan Functional Requirements |
