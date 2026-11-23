---
title: Issue 2201 live10 plan
ms.date: 2026-11-23
---

* [ ] Phase 1: in `live_receiver.main`, print `Cannot run: RECEIVER_FAILED error_type=<ClassName>` and keep return code 4.
* [ ] Phase 2: add a test in `src/api/tests/test_live_control.py` that forces a non-StreamError from persistence and checks the stderr line and exit code 4, with no message text.
* [ ] Phase 3: run the focused tests, mypy and ruff for `src/api`.
