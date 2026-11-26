---
title: Issue 1830 live r14 plan (2026-11-25)
ms.date: 2026-11-25
---

Tier: FULL (`src/api/checks/map_fullscreen_browser_check.py` changes).

1. In the `expanded-{width}` loop, call `settle_map_reads(page)` after the resize, card visible and reflow checks and before `scan`.
2. Measure failure rate before (4 of 18 parallel runs red, 2 of 3 early sequential) and after with the same 18-run parallel batch.
3. Check whether the script is in the scenario manifest recipe hash; ruff, mypy, preflight reflow tests.
4. Write the research note, README row, log entry and the per-criterion table.
