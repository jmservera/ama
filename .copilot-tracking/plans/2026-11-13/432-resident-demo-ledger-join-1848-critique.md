---
title: Issue 432 resident demo ledger join plan critique
description: Independent rubber-duck critique and dispositions
ms.date: 2026-11-13
---

Execution: one rubber-duck critique before code. Verdict: Revise.

| Finding | Disposition |
| --- | --- |
| PC-001 host wiring open | Accepted in part: add injectable `meters` to `configured_advisor` with a test of that route; the host `__main__` still has no ledger, price or authority source, so activation stays an owner decision (recorded, not claimed closed). Classification stays unchanged. |
| PC-002 completed has only id | Accepted: join on `id`; context asserted on the reservation, usage and outcome on completion. |
| PC-003 orphaned reservations | Accepted: close the reservation as `provider-unavailable` on credential/expiry exits in `aoai._request` and `assistant.select`; add tests. |
| PC-004 vacuous canary | Accepted: assert canary reached the fake transport, then absent from all ledger records and captured logs; include guidance and an alert-producing failure. |
| PC-005 drift guard | Accepted: replace name scan with a behaviour test of the configured-advisor seam; keep inventory notes accurate. |
