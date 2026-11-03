---
title: Issue 93 R1 RULE-010 boundary changes
ms.date: 2026-11-03
---

## Changes

* Added `src/core/tests/test_funding_automation_boundary.py` (8 tests). No production code changed.
* Added dated RPI evidence under `.copilot-tracking/`.

## Validation (focused tier)

Run:

* New test module: 8 tests OK.
* `test_grant_lifecycle_controls` 44 tests OK (16 skipped, SQL Server selectors); `test_finance_match_controls` 49 OK (19 skipped).
* `ruff check`, `ruff format --check`, `mypy --cache-dir=/tmp/mypy-93` on the new file: clean.
* Mutation checks: removing the grant approval authority check fails the matrix; adding a `grant_action` reference to an agents module fails the static scan.

Not run: complete local gate, full suites, benchmarks, SQL Server or browser selectors, live model, Azure.

## Epic acceptance criteria

* Criterion 1 (#440 checkpoint): unmet.
* Criterion 2 (all children closed or deferred): unmet; #96, #98, #99 open.
* Criterion 3: evidence strengthened (RULE-010 boundary test) but the criterion is also a design-level claim for the whole demonstrator and for later children (#96 export, #99 limits); not proven for the epic. Uses `Refs #93`.
