---
title: Issue 162 plan
ms.date: 2026-10-15
---

* [x] Phase 1: add `chat_isolation.py` (re-authorise, projected context, untrusted blocks, reply checks, break-glass audit).
* [x] Phase 2: wire `/api/chat/*` in `server.py`; add `chat` kind to the staff allow-list (contractors and unknown roles denied).
* [x] Phase 3: `tests/test_chat_isolation.py` extending the role matrix, injection set, break-glass, fixture replay.
* [x] Phase 4: README section and knowledge-base log entry.
* Critique (single pass, self-run): break-glass content access must not be invented, so it returns metadata only and stays refused until a policy reference is recorded. Applied.
