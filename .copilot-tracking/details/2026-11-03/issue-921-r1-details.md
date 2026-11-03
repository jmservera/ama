---
title: Issue 921 phase details
ms.date: 2026-11-03
---

* Phase 1-2: server.py `end_headers` and `_unhandled` (3 changed lines).
* Phase 3: replace the disconnect test with a backend ConnectionResetError test (expects 500 and an error log without the message) and a BrokenPipeError-on-flush test (expects silent client-disconnect warning, no 500).
