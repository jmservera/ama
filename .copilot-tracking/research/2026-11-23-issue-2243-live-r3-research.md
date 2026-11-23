---
title: Issue 2243 research r3 (AI reply unverified)
ms.date: 2026-11-23
---

Disposition: executed. Planning Readiness: Ready. Full evidence: docs/reference/research/issue-2243-live-r3-2026-11-23.md.

Findings:

* Ledger is no longer the blocker (live reserve expiry 2027-07-01).
* Deployment `resident-mini` exists (gpt-4.1-mini 2025-04-14, Standard, capacity 1) and the endpoint env `ZF_DEMO_ASSISTANT_ENDPOINT` matches the account. Model calls succeed (usage log lines).
* Deployment rate limits are 1 request and 1000 tokens per 60 seconds. Azure metrics show HTTP 429 and 200 each twice in the 11:30 UTC bucket.
* In `aoai.py` an `HTTPError` (an `OSError`) is caught by `answer`/`answer_question`, and `_fallback` maps any exception that is not a listed `AssistantUnavailable` reason to the generic label "the AI service could not provide a verified reply". The 429 is not a verification failure; the label is misleading and the exception class is not logged.
* Fix scope: classify 429 and transport failures in `_fallback`, log the exception class only. Raising the deployment capacity is an owner estate change, not made here.
