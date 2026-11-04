---
title: Issue 164 call authorization details
ms.date: 2026-11-04
---

* Add `call_authorization(auth, calls, tokens, now, used_calls, used_tokens)` returning `blocked` with reasons or `within-limit`.
* Require authorised_by, max_calls, max_tokens, max_budget with budget_currency, and expires_at later than now (ISO date strings).
* `enablement_decision` adds `actual_calls`, currently `blocked` because no authorisation exists.
* Tests: ten blocked cases, one allowed, prior-use exhaustion. Focused tier; no security, infrastructure, SQL or deployment change.
