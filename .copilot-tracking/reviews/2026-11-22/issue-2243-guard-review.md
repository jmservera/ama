---
title: Review for issue 2243 diagnosable ledger refusal
ms.date: 2026-11-22
---

Review executed once, outcome: conformant with open items routed to follow-up (no material finding open in the code).

* Behaviour: a successful reserve is unchanged; refusal reasons are allowlisted in `FALLBACK_REASONS`, carry no resident data, and an old one-column procedure falls back to `usage_limit`. Order of SQL gates now puts expiry before budget; both still refuse.
* Risk: the SQL procedure change is untested against a real SQL Server here (opt-in test skipped). Route: owner or coordinator runs the loopback SQL test before applying.
* Not delivered: image roll and live model reply (owner extends `resident_ai.budget.expires_at`; then re-run the probe). Issue 2243 is not closed by this commit: use `Refs #2243`.
