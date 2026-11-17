---
title: Issue 135 exception queue changes
ms.date: 2026-11-14
---

* `src/core/src/zava_forward/core/exception_queue.py`: new item fields and recovery flags.
* `src/core/tests/test_exception_queue.py`, `src/api/tests/test_exception_register.py`: focused tests.
* Passed: core test_exception_queue and test_exception_feeds (24), api test_exception_register and screen (59), importer test_import_exceptions (43), ruff, mypy.
