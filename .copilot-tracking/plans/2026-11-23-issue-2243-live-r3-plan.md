---
title: Issue 2243 plan r3
ms.date: 2026-11-23
---

Plan (details: .copilot-tracking/details/2026-11-23-issue-2243-live-r3-details.md)

* [x] 1. `_fallback` in `src/api/src/zava_forward/api/resident_demo/aoai.py`: HTTP 429 maps to `provider_busy`, other `HTTPError`, `URLError` and `TimeoutError` map to `provider_unavailable`; both get plain labels; log the exception class name only.
* [x] 2. Test in `src/api/tests/test_resident_aoai.py` for 429, 503 and timeout labels, no leaked message text.
* [x] 3. Evidence note, changes record with per-criterion table, review.

Tier: FULL (src change) classification recorded; the coordinator runs the gate. Local: targeted tests, mypy, ruff.

## Critique (executed once, final candidate)

Verdict: proceed. Compatible findings applied directly: keep the generic label for unknown errors (the browser check `resident_generated_answer_browser_check.py` asserts it for a mocked plain failure); log class name only because messages may hold data; no retry inside the request because the deployment allows one request a minute and the client timeout is 5 s; no estate change. No conflict with owner decisions; no user decision needed.
