---
title: Issue 130 nomination follow-up changes
ms.date: 2026-11-03
---

## Changes

* `src/core/src/zava_forward/core/resident_decisions.py`: `nomination_follow_up`; `followup_view` attaches it.
* `src/core/tests/test_resident_decisions.py`: one new test.
* `src/core/README.md`: documents the view.

## Validation run

* `test_resident_decisions` (from `src/core/tests`): 208 tests OK, 77 skipped (opt-in SQL Server and similar).
* `src/api` `test_resident_api.py`: 16 OK, 1 skipped.
* ruff (src, tests of core) clean; mypy `--cache-dir=/tmp/mypy-130` on resident_decisions.py clean.

## Not run

Gate (`rpi-checks --all`/`--changed`), full suites, benchmarks, opt-in SQL Server, browser or participant checks. Coordinator runs gates.
