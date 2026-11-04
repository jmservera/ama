---
title: Issue 130 nomination overdue queue changes
ms.date: 2026-11-04
---

## Changes

* `src/core/src/zava_forward/core/taskqueues.py`: overdue nomination or self-referral next updates appear as overdue tasks; definition text updated.
* `src/core/tests/test_taskqueues.py`: new boundary and non-mutation test.

## Validation run

* `unittest` test_taskqueues, test_exception_feeds, test_resident_decisions (256 tests, OK, 83 skipped for missing SQL prerequisites).
* `ruff check`, `ruff format --check`, `mypy --cache-dir=/tmp/mypy-530` on the two files: clean.

## Not run

* Local gate, full suites, benchmarks, API/browser tests, SQL-backed tests (skipped).

## Acceptance criteria

No criterion is newly proven. C2-C5, C8-C11 and C14 remain unmet. This PR uses Refs #130.
