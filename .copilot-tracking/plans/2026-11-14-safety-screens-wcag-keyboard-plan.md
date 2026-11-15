---
title: Safety screens WCAG textual state and keyboard plan
ms.date: 2026-11-14
---

Critique: executed once, verdict compatible; no conflicting decisions.

* [x] Label stop-work, SLA clock and escalation state in text (hazardHold, hazardClock, hazardState).
* [x] Add headed sections (aria-labelledby, focusable h2) and a nav of anchor jump links.
* [x] Add tests/test_safety_screen_wcag_keyboard.py; keep test_accessibility_baseline passing.
* [x] Focused validation: mypy, ruff check and format with /tmp caches in src/api.
