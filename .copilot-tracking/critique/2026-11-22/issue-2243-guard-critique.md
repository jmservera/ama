---
title: Critique for issue 2243 plan
ms.date: 2026-11-22
---

Executed once as a self-critique. Verdict: approve with direct dispositions.

* Raising from `reserve` changes the opt-in SQL test `assertIsNone` assertions: applied directly, tests updated.
* The deployed procedure is owner-run infra; Python must tolerate the old one-column result: applied (falls back to `usage_limit`).
* Rolling the image or changing the live SQL row is out of scope (SQL is private; no production change authorised): recorded as unproven criteria.
