---
title: Issue 216 live research
ms.date: 2026-11-18
---

Task: issue-216-live. Refs #216. Synthetic demo, desktop only, live Azure authorised (rg ama, cap USD 700, no drills, no Key Vault rotation, no production change). Research disposition: executed.

## Unticked criterion

"Citation validity and refusal accuracy gates set with owners and measured on a graded and adversarial set". The other issue criteria are ticked and are not re-proven.

## Findings

* Offline gates exist: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (owners `LEGAL_GATE_OWNER`, `COMPLIANCE_GATE_OWNER`, `PROVISIONAL_THRESHOLDS` 1.0/1.0). They grade the deterministic `offline-extractive` regulatory chat, which makes no model call.
* The regulatory chat route needs the `regulatory_chat` rule role; the available staff account gets 403 (`/api/chat/regulatory/status`). It is also model-free, so it is not the "live demo AI".
* The live AI surface is the case chat (`/api/chat/threads/{id}/ask`, `ChatPanel`): model `azure-openai` (gpt-4.1-nano deployment `standard`), storage approved (demo-only), answers carry `citations[{id,text}]`, out-of-scope asks return `kind=refused` with 0 model calls. Verified with one probe turn (1,182 tokens).
* Staff POSTs from a Playwright request context get an Easy Auth 403 without body; the same POST from in-page `fetch` (as the UI does) with `X-ZF-CSRF: 1` works.
* Judgement: measure citation validity and refusal accuracy of the live case chat on a graded set and an adversarial set, within an owner-authorised finite model limit (45 calls, 80,000 tokens, USD 0.05, expiry 2026-11-19T00:00Z), deleting every throwaway thread. Thresholds stay at the existing provisional 1.0 values; owner sign-off beyond the owner's 2026-11-18 demo decision cannot be shown.

Planning Readiness: Ready.
