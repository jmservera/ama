---
title: Issue 432 Criterion 6 per-call join audit research
ms.date: 2026-11-13
---

Research disposition: executed. Planning Readiness: Ready.

## Evidence

* Criterion 6 of #432: each model call joined to capability, case type, model and configuration version, prompt version, input/output/cached tokens, retries, failures, outcome and output record, with no raw case content.
* `ai_consumption.py` EVENT_FIELDS: `reserved` carries id, root, attempt, capability, case_type, configuration, prompt, retry, model; `completed` carries tokens (prompt, completion, total, cached), outcome, held; `output` joins root to output id.
* Callers: worker (`dispatch.py` CallContext, retry = fence-1), chat (`chat_panel.py`, retry 0, output `chat:{tid}:{seq}` published eligible=False including fallback/withheld per #1517).
* Existing API tests: `provenance()` asserts root, attempt, configuration, prompt, cached tokens only; chat test asserts configuration, prompt, output join. Not asserted per call anywhere for worker and chat: capability, case_type, model, input and output tokens, outcome, retry, held. Canary check exists only for the assistant worker path.

## Finding

Data model already carries every field; the gap is proof. No test asserts the full per-call join for both paths, including failure and no raw content. No source change needed.

## Plan direction

Add one API test asserting the full join for a worker call and for chat returned, revoked and provider-failure calls, plus a content-free scan.
