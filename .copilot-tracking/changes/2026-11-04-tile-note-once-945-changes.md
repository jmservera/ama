---
title: Changes for #945
ms.date: 2026-11-04
---

* `src/api/src/zava_forward/api/web/app.js`, `src/api/tests/test_ui_support.py`, `docs/reference/log.md`.
* Run: `unittest tests.test_ui_support` (12 OK), ruff check on the test file, `node --check app.js`, a throwaway node simulation (3 errors, 1 write; clean load clears). mypy on src/api reports 9 pre-existing errors in 2 files, identical to main.
* Not run: browser check with a real failing tile server, screen reader testing, gate, benchmarks, full suites.
