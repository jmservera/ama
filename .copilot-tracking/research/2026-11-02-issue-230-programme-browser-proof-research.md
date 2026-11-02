# Research: issue 230 programme screen browser proof

Disposition: executed (reuses the 2026-11-01 issue-230 research). Planning Readiness: Ready.

## Evidence

* PR 662 (merged 2026-11-01) delivered the `programme-queue` role screen in `src/api/src/zava_forward/api/web/role-screens.js` with node tests only. Its review routed follow-up 1: browser keyboard and axe proof, because criterion 4 (WCAG 2.2 baseline, textual state, keyboard navigation) is unproven.
* `src/api/checks/role_screens_browser_check.py` is the existing real-browser pattern. Child stories register a `SCENARIOS` entry (232 exists). It uses an owned synthetic loopback server and the shared fixture in `role_screens_fixtures.py`, which already holds a `returns` record (SYN-RETURN-230).
* `src/api/checks/case_journey_browser_check.py` shows the pinned axe 4.10.3 scan (`AXE_SHA256` in `regulatory_ux_check.py`, wcag2a/aa, wcag21, wcag22aa tags).
* Baseline `python -m checks.role_screens_browser_check` passes locally (Chromium 156).

## Scope of this slice

Add a `230` scenario to the browser check: real-browser proof for the programme screen of keyboard operation (Tab order reaches scope select, Apply, Reset; Enter and Space operate them; focus visible), non-mutating filter and reset (no POST, no record change), textual state in the queue and the five-gate table (Blocked or missing gates), reflow at 320, 390 and 1280 px, and an axe scan when a pinned axe file is supplied.

## Out of scope

* Planner role (not in the codebase; assumption recorded, not invented).
* Portfolio-level returned-work endpoint (follow-up 2).
* Fluent component adoption (#150) and assistive-technology testing (#155).
