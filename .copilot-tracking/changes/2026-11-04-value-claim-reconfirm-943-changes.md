---
title: Changes for #943
ms.date: 2026-11-04
---

* `src/core/src/zava_forward/core/governance.py`: refusal of confirm unless pre-booked; `CAPACITY_ONLY` constant.
* `src/core/tests/test_governance.py`: Booked-case regression test.
* `docs/reference/log.md`: entry appended.
* Validation run: `unittest tests.test_governance` (69 tests, OK, 16 skipped for SQL prerequisites), ruff check, mypy strict with `--cache-dir=/tmp/mypy-943`.
* Not run: gate, benchmarks, full suites, SQL-backed skipped tests.
