---
title: AI feature register plan (issue 217)
ms.date: 2026-11-14
---

## Plan

* [x] Add `inputs`, `limits`, `owner` to every register entry; add `REQUIRED_FIELDS`, `missing_fields`, `is_registered`, `require_registered` and `UnregisteredFeature`.
* [x] Fail closed in `Ai.run`: an unregistered or incomplete feature returns the template with no model call.
* [x] Route `ai_tasks.require_registered` and the agent dispatch capability check through the register.
* [x] Replace unregistered task names in existing tests with registered ones.
* [x] Add `test_ai_register_completeness.py`.
* [x] Run mypy, ruff check, ruff format check and focused tests.

## Critique

One pass, self-critique: returning a template (not raising) in `Ai.run` matches its existing fall-back contract; raising stays in `require_registered` for task entry points. No conflict with confirmed decisions.
