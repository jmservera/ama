# Research: issue 233 atlas UX findings and role journeys to screens (2026-11-01)

Task: issue-233-atlas-screen-trace. Disposition: executed (focused). Planning Readiness: Ready.

## Evidence

* PRD "Profile Journey Contract for the Next Prototype" lists eleven perspectives (entry, evidence, safe endpoint, recovery/handoff) and says separate home examples must not be relabelled as stages of one home. New fixtures may replace them if checks stay reproducible.
* Atlas "Five design themes and tensions" lists five themes; "One connected service journey" lists eight stages. Tensions named: continuity vs disclosure (theme 1 constraint), utilisation vs choice (theme 2 and closing paragraph).
* Profile review row for #233 states theme-to-state resolutions and the same-home walkthrough are NOT SUPPLIED. Existing T01-T11 rows trace perspectives to journeys, not to built screens.
* Screens: `role-screens.js` on main registers only `asset-board` (#226). Open PRs add `resident-choice` (652), `safety-lead` and `hazard-triage` (653), `data-operator` (654), `procurement-packages` and `contractor-job-pack` (655), `technical-queue` and `quality-queue` (656), `finance-invoices` and `finance-funding` (657), `programme-queue` with a connected home view (662). None merged at 2026-11-01.
* Prior checker pattern: `tools/check-design-trace.py` (offline, reports state only, never records acceptance).

## Decisions

* Deliver a dated UX trace document plus an offline checker in `src/core` with tests, so completeness (11 perspectives, 5 themes, 2 tensions, walkthrough of 8 stages on one constructed home) is reproducible.
* Screens in unmerged PRs are cited as "proposed in PR N", never as delivered.
* Same-home walkthrough uses one newly constructed fixture home id (not one of the eight existing examples), design-level only; no code or fixture claim.
* Everything labelled hypothesis until #155; accessibility and design-system criteria stay unproven (no AT or browser evidence here).

## Not in scope

New screens, fixtures, observed validation (#155), human acceptance.

* Correction cycle 2026-11-01: two PR 713 review threads accepted as valid; no research change.
