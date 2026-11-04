---
title: Changes for #99
ms.date: 2026-11-04
---

* `src/api/src/zava_forward/api/server.py`: `GET /api/finance/exposure`.
* `src/api/tests/test_finance_exposure_api.py`: four loopback tests.
* `src/api/tests/test_role_endpoint_inventory.py`: route added.
* `src/api/README.md`: route documented.
* Run: unittest for the new test, `test_finance_match_api`, `test_role_endpoint_inventory` (24 OK) and core `test_exposure_limits` (14 OK); ruff; mypy with `--cache-dir=/tmp/mypy-99` on the new test.
* Not run: gate, benchmarks, full suites, mypy on server.py.
