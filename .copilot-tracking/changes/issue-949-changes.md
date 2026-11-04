---
title: Issue 949 changes
ms.date: 2026-11-04
---

* `src/core/tests/test_resident_decisions.py`: derived version helper, default in `review_body`, new assertions in the hold test, explicit pin in the binding test.
* `docs/reference/log.md`: entry appended.
* Validation run: `python3 -m unittest test_resident_decisions` in `src/core` (226 tests, OK, 83 skipped), ruff check and format check, mypy strict with `--cache-dir=/tmp/mypy-949` on the test file.
* Not run: gate, benchmarks, full suites, other projects.
