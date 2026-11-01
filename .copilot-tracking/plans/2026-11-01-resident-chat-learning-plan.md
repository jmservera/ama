---
title: Resident chat learning plan
ms.date: 2026-11-01
---

* Phase 1: add `chat_log.py` (bounded SQLite record, pseudonymous session id, masking, summary CLI) and wire `app.py` and `__main__.py`.
* Phase 2: extend the router (docs, forms and status synonyms, pause and contact topics) and replace the flat refusal with closest-topic suggestions only for harmless questions; keep refusals for injection and boundary requests.
* Phase 3: tests for each failing phrasing, refusal negatives, AI-enabled grounding, the log and its bounds. Visible UI note on the chat page.
* Phase 4: docs note, index, log, README setting; focused validation (resident unit tests, ruff check, ruff format --check, mypy src/api).
* Critique (executed once, direct dispositions): fallback must stay a refusal for injection, other-record and action requests, so the fallback is allowed only when every part reads as a question or short topic phrase. New topics never call AI.
