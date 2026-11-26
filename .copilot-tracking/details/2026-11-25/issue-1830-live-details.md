---
title: Issue 1830 live r14 details (2026-11-25)
ms.date: 2026-11-25
---

Phase 1: one line added in `run_browser` of `src/api/checks/map_fullscreen_browser_check.py` before `scan(page, axe, reports, f"expanded-{width}")`. Phase 2: before and after stress with 18 parallel runs, pinned axe. Phase 3: lint, type check, scenario-manifest recipe hash check, docs. No assertion is removed.
