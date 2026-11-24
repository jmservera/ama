---
title: Epic 149 map tile-note check locator defect and fix (Refs #149)
description: A stale adjacent-sibling selector made the map tile status browser check fail against a correct page; fix, tests and per-criterion status for the synthetic desktop demo
ms.date: 2026-11-23
---

Refs #149. Scope: synthetic desktop demo under the owner decisions of 2026-11-18. This note ticks nothing.

## Defect

The #440 comments record a retained map browser-check failure. Reproduced on 2026-11-23 from `src/api` with `PYTHONPATH=src:.:../core/src:../agents/src python3 -m checks.map_tile_status_browser_check`: `.map-info [role=status] + [role=status]` resolved to 0 elements, expected 1.

Cause: `app.js` builds the sidebar as `info, retry, tileNote`. A hidden retry button (commit `5dfa7312d5`) sits between the two status paragraphs, so the adjacent-sibling selector no longer matched. The page was correct; the check was stale.

## Fix and evidence

* `tile_notice` in `src/api/checks/map_tile_status_browser_check.py` now selects the status that does not match the count pattern, independent of sibling order.
* `tests/test_map_status_locators.py` gains a test that the tile locator excludes the count and uses no sibling combinator (4 tests OK).
* The browser check now prints "All checks passed!" in both tile states. `ruff check`, `ruff format --check` and `mypy` (375 files) are clean. The workbench recipe SHA is unaffected.
* Live desktop render (Playwright, 1280x800, no sign-in): `ca-cutover-test-demo-api` revision 0000058 and `ca-resident-demo` revision 0000028 both return 200, one `h1`, one `main`, `lang` en-GB, no horizontal overflow. Screenshots under `.copilot-tracking/evidence/2026-11-23/issue-149-live-r3/`.

## Per-criterion table

| # | Criterion | Result | Why |
| --- | --- | --- | --- |
| 1 | #440 stabilization checkpoint | Unproven | #440 has two unticked criteria; triage and deferrals need owner approval. One of its open findings (this check) is now fixed locally. |
| 2 | Child features accepted | Unproven | Acceptance is an owner decision; closed is not accepted. #155 awaits the SA-010 staff agreement. |
| 3 | Accessibility, content, usability evidence as test results | Already ticked | Map check, locator test and live render recorded here; person-run assistive technology testing out of demo scope. |
| 4 | Design artefacts traceable | Already ticked | Not re-executed. |

## Limits

Only the tile-state check was run for the map; `map_fullscreen_browser_check.py` needs an axe bundle and was not run. The live render was unauthenticated, so signed-in screens were not covered.
