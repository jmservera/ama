---
title: Issue 921 plan
ms.date: 2026-11-03
---

* Phase 1: set `_response_started` before the flush in `end_headers`.
* Phase 2: silent path only when ConnectionError and response started; otherwise log and answer 500.
* Phase 3: regression tests for both cases in src/api/tests/test_error_logging.py.
* Details: [details](../../details/2026-11-03/issue-921-r1-details.md)
* Critique: executed once inline; verdict compatible. Residual risk: a client reset while reading the request now logs a 500 attempt (undeliverable response is logged, not raised).
