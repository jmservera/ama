# Plan: #105

1. Add `ai_registry.py`: 11 registered tasks with scope, capability, source permissions, accountable function, approval state, impact record, prohibited purposes, unknown individual/delegation/authority; `authorizes_live` stays false; `envelope()` builder.
2. Wire envelope into `ai_tasks.finish` records and results; deny unregistered tasks before any model call; bind task/case/source into assistant provider envelopes.
3. Expose registry on the manager-only `/api/ai/report`.
4. Tests in `tests/test_ai_tasks.py`; run full mvp suite.

Critique: one pass, no conflicts. Knowledge base unchanged, so no index/log update.
