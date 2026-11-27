---
title: Issue 1830 live r15 details (2026-11-27)
ms.date: 2026-11-27
---

Phase 1: edit the `button.evaluate` call in the `filter label and focus fit` loop of `src/api/checks/map_fullscreen_browser_check.py` to await a stable bounding box (button and filter panel) over five animation frames, at most 120, then apply the unchanged assertion.

Phase 2: validation: 12 sequential runs with the pinned axe-core 4.10.3 (sha256 prefix `880970c081707360`), ruff check, ruff format check, mypy in `src/api`, 62 tool tests, preflight accept and reject.

Phase 3: docs: research note, README index row, log entry, changes and review records.
