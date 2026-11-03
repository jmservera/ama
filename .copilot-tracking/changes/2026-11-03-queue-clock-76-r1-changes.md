---
title: Issue 76 round 1 changes
ms.date: 2026-11-03
---

* src/core/src/zava_forward/core/taskqueues.py: `timing` helper and four additive clock fields.
* src/api/src/zava_forward/api/web/app.js: clock sentence shows owner status and deadline states.
* src/core/tests/test_taskqueues.py: new states asserted; new test for an unnamed owner.
* src/api/tests/test_role_screens.py: fixture and phrases for the new text.

Validation run: core `test_taskqueues` (20 tests) and api `test_role_screens` (6 tests) pass; ruff check and format pass; mypy with --cache-dir=/tmp/mypy-76 passes on taskqueues.py.
Not run: complete gate, full suites, benchmarks, browser check (role_screens_browser_check.py needs a live app and browser), hosted CI.
