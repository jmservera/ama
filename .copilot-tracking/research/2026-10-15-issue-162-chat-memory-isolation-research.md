---
title: Issue 162 chat and memory isolation research
ms.date: 2026-10-15
---

* Task: `issue-162-chat-memory-isolation`; Research disposition: executed; Planning Readiness: Ready.
* Sources read: issue 162 and parent 157, ADR 0004 (decisions 3, 5, 6 and the Isolation model), `mvp/zavaforward_mvp/chatthreads.py` (owner-filtered repository, #160), `chat_privacy.py` (approval gate, memory, rights, #163), `projection.py`, `server.py` routing, `tests/test_role_matrix.py`, `test_role_endpoint_inventory.py`, `chat_fixture.py` isolation cases (#172).
* Finding 1: no chat or memory HTTP endpoint exists, so the role matrix cannot cover one until endpoints are added. Smallest change: one `/api/chat/*` handler keyed on the authenticated user.
* Finding 2: the repository already filters every query on the owner key; no new tables are needed (owner rule: no colliding tables).
* Finding 3: `store.detail(case_id, user)` is the existing field-level projection; chat context reuses it.
* Finding 4: ADR 0004 says administrator or break-glass policy is BRD OD-46 and not decided. Record as open; implement default-deny with audit.
* Unknown or unverified: live-model injection behaviour, contractor use of chat, break-glass policy, retention.
