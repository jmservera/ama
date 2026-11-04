---
title: Issue 79 changes, slice 2
ms.date: 2026-11-04
---

* `src/core/src/zava_forward/core/store.py`: archive path, status and publish methods.
* `src/api/src/zava_forward/api/server.py`: two routes.
* `src/api/tests/test_ranking_publication_wiring.py` (5 tests), `test_role_endpoint_inventory.py` entries.
* `src/core/README.md`, `docs/reference/log.md`.

No divergence from plan. Run: new wiring tests, `test_role_endpoint_inventory`, `test_role_matrix`, `test_ranking_policy` (all pass), ruff on core/api sources and new test, mypy `--cache-dir=/tmp/mypy-530` on `ranking_publication`. Not run: complete gate, full suites, benchmarks, hosted CI, mypy on store.py/server.py.
