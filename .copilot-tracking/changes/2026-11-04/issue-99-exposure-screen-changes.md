---
title: Changes for #99 Finance queue exposure screen
ms.date: 2026-11-04
---

* Changed `src/api/src/zava_forward/api/web/panels.js`: Investment limits section on the Finance queue.
* Added `src/api/tests/test_finance_exposure_screen.py`.
* Appended `docs/reference/log.md` entry.
* Validation run: new screen tests, `test_finance_exposure_api`, `test_role_endpoint_inventory`, `test_workspace_scripts` (33 tests OK); `ruff check`, `ruff format --check`, `mypy --cache-dir=/tmp/mypy-99` in `src/api` (tests included).
* Not run: gate, full suites, benchmarks, browser harness (design-system and real-browser checks), web-design-guidelines source fetch.
