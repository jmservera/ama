---
title: Changes for issue 691 API error diagnosis
ms.date: 2026-11-02
---

* Edited `src/api/src/zava_forward/api/server.py`: `handle_one_request` guard and `_unhandled` (plain 500 body, structured `http-error` log with method, path, exception class, raising frame; client disconnects logged at warning).
* Added `src/api/tests/test_error_logging.py`.
* No documentation change, so no `log.md` entry. `tools/rpi-checks.py` not run (coordinator queues the gate).
* Validation: full `src/api` unit suite with `PYTHONPATH=../core/tests:../agents/tests` ran 1631 tests, 3 errors, all `ModuleNotFoundError: playwright` import errors in browser-dependent modules (`test_browser_asset_urls`, `test_employee_acceptance_check`, `test_employee_live_acceptance`), 323 skipped; no failures. Those 3 modules were not run here.
