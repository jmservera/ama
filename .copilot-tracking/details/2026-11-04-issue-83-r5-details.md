---
title: Issue 83 r5 details
ms.date: 2026-11-04
---

* P01: `server.py` route beside `/api/handoffs`; `get_kind` maps it to `handoffs` so projection role gating applies; limit must be 0 < n < 1e6.
* P02: `test_handoff_api` covers sender, receiver, manager, unrelated staff, contractor 403, POST 404, invalid limits, no owner or state change; inventory lists the route.
