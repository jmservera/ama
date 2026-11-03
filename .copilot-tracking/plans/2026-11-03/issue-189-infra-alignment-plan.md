---
title: Issue 189 infra alignment plan
ms.date: 2026-11-03
task_id: issue-189-infra-alignment
---

## Plan

* [x] Add `InfraAlignmentTests` to `src/core/tests/test_run_plan.py`: tier/units match Bicep defaults, cost allocation covers the list price, 80 percent actual notification equals the default alert threshold, budget is resource-scoped.
* [x] Note the test in `src/core/README.md`.
* [x] Run `tests.test_run_plan`, ruff check, ruff format --check, mypy (`--cache-dir=/tmp/mypy-189`).

Details: [details](../../details/2026-11-03/issue-189-infra-alignment-details.md)

## Critique

Single pass 2026-11-03: test-only, reads Bicep text, no infra edit, no gate. Compatible; no change needed. Slice is not security, SQL, infrastructure or deployment work, so the focused tier applies.
