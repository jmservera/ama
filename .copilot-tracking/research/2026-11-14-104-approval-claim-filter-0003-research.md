---
title: Issue 104 approval claim filter research
ms.date: 2026-11-14
---

## Task

Issue #104, reviewer finding: the assistant output filter `FORBIDDEN` blocked only send claims. Approval and record-change claims could pass.

## Evidence

* `src/core/src/zava_forward/core/ai.py` defines `FORBIDDEN`, applied in `Ai.run` (template fallback) and in `assistants.py` output validation.
* Entry points: `Ai._request` raises `DispatchHeld` when no meter exists and calls `Consumption.reserve` before token or socket use; the resident demo assistant calls `self.reserve(envelope)` before `self.token()`.
* Existing `src/api/tests/test_ai_consumption_api.py` (40 tests) covers metered paths.

Research disposition: executed. Planning readiness: Ready.
