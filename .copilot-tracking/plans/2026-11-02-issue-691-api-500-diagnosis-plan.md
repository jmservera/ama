---
title: Plan for issue 691 API error diagnosis
ms.date: 2026-11-02
---

* [x] Add `handle_one_request` guard and `_unhandled` structured logging in `src/api/src/zava_forward/api/server.py`.
* [x] Add `src/api/tests/test_error_logging.py` (500 body and log hygiene, disconnect, 403/503 classification, concurrent burst).
* [x] Run the full `src/api` unit suite; no docs change, so no `log.md` entry.
* [x] Commit, push, open PR with `Refs #691`.

Critique: executed once (see details); verdict proceed. Risks: guard changes dropped connection to a plain 500 body for escaped exceptions only; no other status changes.
