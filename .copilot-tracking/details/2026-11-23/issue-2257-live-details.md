---
title: Issue 2257 live details (run 084412Z)
ms.date: 2026-11-23
---

Phase 1: edit `mapPanel` in `app.js`: `retry` button, `retryFit`, `autoRetries`, `retryTimer`; set `retry.hidden` in `draw`; schedule one redraw in the catch block when `!error.status`.
Phase 2: add a node test in `test_workspace_scripts.py` that extracts the map draw failure branch and drives it with fake timers.
Phase 3: run the focused tests and record evidence.
