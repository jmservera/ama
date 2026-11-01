---
title: Issue 572 chat-panel gate changes
ms.date: 2026-11-01
---

Plan: [plan](../plans/2026-11-01-issue-572-chat-panel-gate-plan.md)

* Added: research, plan, changes and review artifacts for #572 (tracking only).
* No source, test, workflow or tool change; JS not touched, so `node --check` is not applicable.

Validation:

* `python3 -m unittest tools.test_rpi_checks`: 55 tests OK.
* `ruff check` and `ruff format --check` on `tools/rpi-checks.py` and `tools/test_rpi_checks.py` report pre-existing findings (16 errors, 2 files to reformat) on unchanged files; not fixed, out of scope. `tools/` is not a mypy project.
* No Azure resources touched.
