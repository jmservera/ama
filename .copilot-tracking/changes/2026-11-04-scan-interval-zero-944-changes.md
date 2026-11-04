---
title: Changes for #944
ms.date: 2026-11-04
---

* `src/core/src/zava_forward/core/assistants.py`: forecast guard.
* `src/api/tests/test_assistants.py`: regression test.
* `docs/reference/log.md`: entry appended.
* Run: `unittest tests.test_assistants -k forecast` (10 run, 5 skipped for SQL Server prerequisite; the new test ran on the SQLite store and its MSSQL variant was skipped), ruff check on touched files, mypy `--cache-dir=/tmp/mypy-943` on core (clean).
* api mypy reports 9 errors in 2 files, identical before and after this change (pre-existing, in checks/ and unrelated files).
* Not run: gate, benchmarks, full suites, MSSQL tests.
