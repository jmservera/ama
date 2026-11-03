---
title: Issue 531 retry-check drift changes
ms.date: 2026-11-03
---

* Base: origin/main 2c2eb4615.
* Changed: `src/api/checks/loading_briefing_browser_check.py` (retry counts), `src/api/README.md` (retry paragraph), `docs/reference/log.md` (entry), this RPI record set.
* Before the fix, `checks.loading_briefing_browser_check` failed at `companion_failure_check` (4 requests, 3 expected).
* Validation (synthetic loopback, Chromium 156.0.8078.4, no live AI, SQL or Azure; `PYTHONDONTWRITEBYTECODE=1`):
  * `unittest test_loading_feedback test_workspace_scripts test_ai_tasks test_static_assets test_browser_asset_urls`: 86 tests OK.
  * `checks.loading_briefing_browser_check` with axe-core 4.10.3 (pinned hash): all PASS after the fix; axe reports had 0 violations.
  * `checks.employee_briefing_browser_check`: all PASS.
  * `ruff check` and `mypy --cache-dir=/tmp/mypy-531` on the changed check: clean.
* Not run: the gate, benchmarks, full suites, live employee-site verification, screen-reader and voice-control testing. Axe automation does not establish accessibility acceptance.
* Divergences: none.
