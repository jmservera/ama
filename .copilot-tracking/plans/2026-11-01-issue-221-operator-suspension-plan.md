---
title: Issue 221 plan
ms.date: 2026-11-01
---

* Scope: one focused test in `src/api/tests/test_operator_suspension.py`: breach record names restart authority, restart denied without proposal/authority, manual casework continues, unnamed authority recorded as Unavailable.
* No source change; no mvp/ or prototype/ changes.
* Validation: operator suspension tests, ruff check, ruff format --check, mypy (baseline 6 pre-existing errors, unchanged).
* Critique (single pass): the test must not claim human appointment or witnessed drill; criteria 5 and 6 stay unticked. Applied.
* Publish: PR with `Refs #221` naming unmet criteria 5 and 6.
