---
title: Changes for issue 80 round 1
description: Files changed and validation for the per-list CSV export slice
ms.date: 2026-11-03
---

## Changed

* New: `src/core/src/zava_forward/core/list_export.py`, `src/core/tests/test_list_export.py`, `src/api/tests/test_list_export_api.py`.
* Edited: `core/store.py` (formula-safe cases CSV), `core/projection.py` (export kinds), `api/server.py` (routes), `api/web/app.js` (links), `api/README.md`, `api/tests/test_role_endpoint_inventory.py`.

## Validation (focused tier; PYTHONPATH to this worktree because the installed editable packages point at another worktree)

* unittest: test_list_export (3), test_list_export_api (5), test_role_endpoint_inventory, test_task_queue_api, test_dependency_rule: OK.
* ruff on changed files: clean. mypy `--cache-dir=/tmp/mypy-80` on list_export.py: clean; the api test file only reports import-untyped for the api package.
* `node --check app.js`: OK.
* Not run: gate, benchmarks, full suites, browser/accessibility run of the new links, hosted CI.
