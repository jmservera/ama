---
title: Issue 153 formatting and type-check correction plan
ms.date: 2026-11-12
task_id: 153-check-correction-1112
---

* [x] Remove the unused ignore at `test_case_journey.py:560` (no cast, no config change). Details: [details](../details/2026-11-12-proposal-card-check-correction-153-1112-details.md).
* [x] Run `ruff format` on the touched Python files; verify AST equality before and after.
* [x] Run ruff check/format/mypy, the 180-test unit selection and one axe-enabled browser check. Prospective plan: coordinator `files/153-check-correction-1112/plan.md`.

Critique: author self-check only, not independent. Out of scope: JS, waits, routes, behaviour, other files.
