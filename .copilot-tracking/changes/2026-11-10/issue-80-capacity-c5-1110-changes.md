---
title: Issue 80 capacity C5 changes
description: Prospective and actual record for the test stub alignment
ms.date: 2026-11-10
---

## Prospective (written before implement-start)

* One test-only edit: `src/api/tests/test_case_journey.py` line 435, the `show` stub filters `null` and non-node children as production `show` does. No application, checker, ops.js or fixture-data change.
* Checks listed in the details file; results appended after execution.

## Actual (after implement-start)

* Edited `src/api/tests/test_case_journey.py` (`show` stub now filters null and non-node children as production `show` does; split over two lines).
* Direct exits (evidence `phase80-capacity-c5-evidence-1110/`): failing test 0; `tests.test_case_journey` 31 tests 0 (rerun `journey-r2` 0 after the line split); API list export 11 tests 0; static 60 tests 0; `node --check ops.js` 0 (file unchanged); Ruff format 0.
* Adverse, preserved: first Ruff check (`ruffcheck.log`) exited 1 with E501 on my first one-line edit; fixed by splitting the line; `ruffcheck-r2` exited 0. Baseline Ruff on the unmodified file passed.
* Carried, not rerun: C4 validation whole `capacity_browser_check --axe` PASS (about 84 s) on source `2cc34027`. Valid only because no served web file or checker changed; the only diff is the test file.
* No browser run, no app edit, no checker edit. C5 used, no C6. Child 1419 must adopt this fix before its validation chain; its worktree was not touched.
