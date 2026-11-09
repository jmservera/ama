---
title: Exception register details (#135)
ms.date: 2026-11-04
---

## Phase 1

`src/core/src/zava_forward/core/exception_register.py`: `staff_from_env` parses `ZF_EXCEPTION_STAFF` (bad input names nobody); `ExceptionRegisterMixin.exception_register` builds an `ExceptionQueue` per read, routes stock conflicts to the first named steward and AI, task and handoff items to the first named operator, audits the view or denial in the store ledger, and returns items, unrouted notes, unconnected sources, banner and visible roles.

## Phase 2

`GET /api/exceptions` in `server.py` returns 200 or 403; entry in `test_role_endpoint_inventory.py`.

## Phase 3

`src/api/tests/test_exception_register.py` (12 tests); README section updated.
