---
title: Issue 531 re-verification on main details
ms.date: 2026-11-03
---

* Phase 1: run `tests.test_loading_feedback` and `tests.test_workspace_scripts` from `src/api`.
* Phase 2: run `checks.loading_briefing_browser_check` with the pinned axe-core 4.10.3 file (static shell at 320 and 1280 px, cold start, retries, per-panel loading, briefing, review round trip, axe).
* Phase 3: run ruff and mypy (`--cache-dir=/tmp/mypy-531`) on the check; write the changes, review and state records and the log entry; remove generated caches.
