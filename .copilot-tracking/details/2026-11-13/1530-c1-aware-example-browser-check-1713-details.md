---
title: Issue 1530 C1 fix details
description: Phase details
ms.date: 2026-11-13
---

## Phase 1

Append the example sentence to the end of the `hz-aware` hint string; add one assert line in the existing panel-hint test block (line 235).

## Phase 2

Fixture hazards copy the `base`/`referred`/`legacy` shapes from `test_safety_panel_ux.py`. The scan reuses `scan_state` (axe, wcag2a to wcag22aa, 0 violations). Overflow: `scrollWidth <= innerWidth`. 200% zoom is the root font size at 320 px, matching the existing enlarged-text check. Results are recorded under `results["populated_safety"]`.

## Phase 3

Digest bound to `workbench_browser_check.py` only; the changed check is not hashed, so no manifest edit unless `test_scenario_manifest` demands it.
