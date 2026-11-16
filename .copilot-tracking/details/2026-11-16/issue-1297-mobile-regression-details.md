---
title: "Issue 1297 320px summary-bottom regression details"
ms.date: 2026-11-16
---

## Phase 1

Changes artifact opens with the independent finding (blocking medium, `case_journey_browser_check.py:1546`) and the reproduction command: copy the journey check with `bottom <= 1600`, run with `PYTHONPATH=../core/src:../agents/src:src:.` from `src/api` and the SHA-verified axe 4.10.3 file; observed `AssertionError: 320x800 summary within one viewport scroll (1637.40625)`.

## Phase 2

At the 320 branch, assert `bottom <= 1600` and replace the comment with a short note that the compact narrow navigation is what makes the limit hold. Add a check that every `#nav a` has a bounding box at least 24px wide and 40px tall (the existing `min-height:2.5rem`), proving the compaction did not shrink touch targets.

## Phase 3

Append to the `@media(max-width:600px)` rule that already holds `.top nav{row-gap:.125rem}`: `#nav{column-gap:var(--sp-1)}#nav a{padding-inline:var(--sp-1)}`. `#nav a` has specificity above `nav a`, so it overrides the earlier `padding:var(--sp-2)` only inside the narrow query. Estimated saving: about three nav rows (126px), more than the 37px needed.

## Phase 4

`test_narrow_navigation_is_compact_and_targets_preserved` in `test_design_system.py`: parse the max-width 600px media block, assert the two compaction declarations, that `#nav a` min-height 2.5rem still exists, and that `.screen-evidence p>a:only-child` still has `min-height:1.5rem`. It must fail before the CSS change. Run the real journey check (limit 1600) and `python3 -m unittest` for the touched test module plus related UX tests; ruff format/check on the changed Python.
