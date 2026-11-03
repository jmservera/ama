---
title: Issue 104 round 1 details
ms.date: 2026-11-03
---

## Phase 1: boundary test

* Script the model to return hostile text (approval, submission, stage move, owner change, rank first, consent claims) and a hostile priority list.
* Snapshot cases (minus `funding.draft`, `funding.status`, `documents[].summary`) and the ranking before and after briefing, message, summary, funding draft and priority runs; assert equal and that the audit chain verifies.
* Assert funding approval fields, history and `funding_ok` are untouched and the status never passes Draft ready.
* Assert accept, edit and reject of AI records, and priority accept, change no controlled record; unregistered task and wrong reviewer are refused.
* Add the module to the existing mypy override list in `src/api/pyproject.toml` like its sibling AI task tests.

## Phase 2: focused validation

* `test_ai_boundary`, `test_ai_tasks`, `test_assistants`; `ruff check`, `ruff format --check`, `mypy --cache-dir=/tmp/mypy-104` from `src/api`.
