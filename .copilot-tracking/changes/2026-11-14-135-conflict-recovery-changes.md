---
title: "Changes: #135 controlled recovery request"
ms.date: 2026-11-14
task_slug: 135-conflict-recovery-1844
---

## Files

* `src/core/src/zava_forward/core/exception_register.py`: shared queue builder, recovery overlay, `request_exception_recovery`, updated note.
* `src/api/src/zava_forward/api/server.py`: `POST /api/exceptions/recovery`.
* `src/api/tests/test_exception_register.py`: three recovery tests.
* `src/api/tests/test_role_endpoint_inventory.py`: route listed.

## Validation

* `python3 -m ruff check src/core src/api` and `ruff format --line-length 100 --check`: pass.
* Unit tests run with source paths: `test_exception_register`, `test_exception_register_screen`, `test_role_endpoint_inventory`, `test_role_matrix` (99 tests) and core `test_exception_queue`, `test_exception_feeds` (24 tests): pass.
* Not run: complete local gate, browser harness, hosted CI. Not pushed.

## Divergences

None. Remaining on #135: failed-import producer coverage, named roles, runbooks, screen wiring for the recovery action, operational acceptance. Do not close #135.
