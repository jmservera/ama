---
title: Plan for issue 2245 round 2
ms.date: 2026-11-23
---

Scope: add one regression test in `src/api/tests/test_error_logging.py` that a non-lock driver error on `POST /api/chat/threads` still answers 500 with no `Retry-After`; record live evidence and the per-criterion table. No src change, so focused tier; no Azure change.

* [ ] Phase 1: add the test and run `test_error_logging.py`, ruff, mypy in `src/api`.
* [ ] Phase 2: research note, changes record, review.

## Critique (executed once)

Verdict: proceed. Compatible advice applied: keep the test next to the sibling tests; do not edit server code (the 503 mapping is correct and narrow); do not clear the suspension (human restart action).
