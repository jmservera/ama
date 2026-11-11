---
title: Issue 80 capacity browser check aftercare route, critique
description: Single critique of the C2 plan
ms.date: 2026-11-10
---

Executed once on the final candidate (native author critique, not independent). Verdict: proceed with direct amendments.

* K1 (Medium, applied): registering the request in `expected_failures` would also silence a 200 or a different status; the plan therefore records every response for that exact URL and asserts exactly one with status 403 and the exact error text.
* K2 (Medium, applied): the allowlist is scoped to scenario `#/aftercare`, GET and the exact origin plus path, so the same request elsewhere stays fatal.
* K3 (Low, applied): assert no POST during the route and no recording form or submit button, so "read-only" is observed, not inferred.
* K4 (Low, accepted): the console filter drops only errors located at that exact URL; if attribution is missing the run fails and is reported.
* No conflict with a confirmed Root decision.
