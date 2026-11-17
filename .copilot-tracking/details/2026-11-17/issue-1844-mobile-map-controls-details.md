---
title: Issue 1844 phase details
ms.date: 2026-11-17
---

## Phase 1 and 2

CSS: `@media(max-width:600px){.map-home-card{position:static;width:auto;max-height:none;margin-top:var(--sp-3)}}` placed before `.map-home-header`. Desktop above 600 px and the expanded dialog rules are unchanged.

Check: `check_narrow_summary_clearance` and `check_served_source_identity` in `src/api/checks/map_fullscreen_browser_check.py`, called from `run_browser` before the existing checks.

## Phase 3

Commands are listed in the changes file.
