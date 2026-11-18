---
title: Issue 110 device identity hardening review
ms.date: 2026-11-14
---

Review executed once after implementation. Outcome: Conformant for the bounded objective, with routed follow-ups.

* Non-canonical `observed_at` forms no longer pass the envelope check: evidenced by new tests.
* Existing valid v1 and v2 envelopes still verify; consumer and API IoT tests pass.
* Follow-up 1: criterion 1 of #110 stays open until real distinct Hub identities and live Azure SQL acceptance are approved and evidenced (tier, cost, network, credential owner).
* Follow-up 2: run the complete gate and hosted CI before publication; no push or PR was made.
* Limit: unit tests use fixture identities, not real Hub identities.
