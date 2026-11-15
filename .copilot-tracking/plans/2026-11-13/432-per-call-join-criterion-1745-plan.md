---
title: Issue 432 Criterion 6 per-call join plan
ms.date: 2026-11-13
---

## Plan

* [ ] Phase 1: add a `call_join` helper and `test_every_model_call_is_fully_joined_without_case_content` to `src/api/tests/test_ai_consumption_api.py`.
* [ ] Phase 2: run `test_ai_consumption*` (core, api), ruff, mypy in `/tmp/venv-432j-1745`; remove venv.
* [ ] Phase 3: independent code-review; commit locally.

Details: `.copilot-tracking/details/2026-11-13/432-per-call-join-criterion-1745-details.md`. No source change unless the test exposes a missing field.
