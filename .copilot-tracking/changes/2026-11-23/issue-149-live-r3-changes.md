---
title: Changes, issue 149 live r3
ms.date: 2026-11-23
---

Tier: FULL classification (src change under `src/api`). Targeted local checks only; `rpi-checks.py --all` was not run (coordinator's gate).

## Files

* `src/api/checks/map_tile_status_browser_check.py`: `tile_notice` no longer uses an adjacent-sibling selector.
* `src/api/tests/test_map_status_locators.py`: new test for the tile locator.
* `docs/reference/research/issue-149-map-check-locator-2026-11-23.md`, README index row, log entry.
* Evidence: `.copilot-tracking/evidence/2026-11-23/issue-149-live-r3/*.png`.

## Validation

* Check failed before (0 of 1 match), passes after in both tile states. 4 locator tests OK; ruff check and format clean; mypy clean (375 files).
* Live Playwright desktop render of both demo apps: 200, one h1, one main, no overflow.
* Not done: web-design-guidelines refetch (no web file changed); `map_fullscreen_browser_check` (needs axe bundle); signed-in live screens; person-run AT testing (not needed).

## Per-criterion table

| # | Criterion | Result |
| --- | --- | --- |
| 1 | #440 stabilization checkpoint | Unproven: owner-gated triage and deferrals; one open finding fixed |
| 2 | Child features are accepted | Unproven: owner decision; #155 SA-010 staff agreement pending |
| 3 | Accessibility, content and usability evidence recorded | Proven locally (already ticked) |
| 4 | Design artefacts traceable | Not re-executed (already ticked) |
