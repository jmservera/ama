---
title: Critique issue 2314 plan
ms.date: 2026-11-23
---

Executed once. Verdict: accept.

* Scope is right: alerts and runbooks already exist and are tested; only the saved query resource is missing. Do not duplicate rules.
* The saved search must not claim reconciliation: it keeps `Unreconciled, not zero` and unknown billed cost, matching the workbook.
* Deployment stays owner-authorised; no `az deployment`, so no live change. Disposition: applied directly.
