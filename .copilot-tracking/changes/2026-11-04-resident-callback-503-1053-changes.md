---
title: Changes - resident callback 503 (#1053)
ms.date: 2026-11-04
---

## Changed

* `src/api/src/zava_forward/api/resident_demo/app.py`, `web/demo.js`, `web/index.html`
* `src/api/tests/test_resident_demo_api.py`, `src/api/tests/test_resident_chat_api.py`

## Validation run

* `unittest discover -p "test_resident_*.py"`: 207 tests OK (10 skipped); `test_static_assets.py`: 5 OK.
* `ruff check src tests`: pass. `mypy --cache-dir=/tmp/mypy-1053` on `resident_demo`: pass. `node --check demo.js`: pass.

## Not run

Gate, full suites, benchmarks, browser checks (Playwright), live deployment check, web-design-guidelines source refresh.
