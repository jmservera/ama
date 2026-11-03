---
title: Issue 531 derive retry counts changes
ms.date: 2026-11-03
---

* Base: origin/main e10766a70.
* Changed: `src/api/checks/loading_briefing_browser_check.py` (attempt count derived from `app.js`), `docs/reference/log.md`, this RPI record set.
* Validation (synthetic loopback, Chromium 156.0.8078.4, no live AI, SQL or Azure; `PYTHONDONTWRITEBYTECODE=1`):
  * `unittest tests.test_loading_feedback tests.test_workspace_scripts`: 8 tests OK.
  * `checks.loading_briefing_browser_check` with axe-core 4.10.3 (pinned hash 880970c0...): all stages PASS.
  * `ruff check` and `mypy --cache-dir=/tmp/mypy-531` on the changed check: clean.
* Not run: the gate, benchmarks, full suites, live employee-site verification, screen-reader and voice-control testing. Axe automation does not establish accessibility acceptance.
* Divergences: none.
