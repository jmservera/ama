---
title: Issue 132 round 2 plan
ms.date: 2026-11-04
---

* [x] Add `ProcurementMixin.work_order_job_pack` (staff only, read only)
* [x] Route `GET /api/workorders/{id}/job-pack`, kind `job_pack` in staff GET list only
* [x] API test: staff read, no resident detail, no writes, 404, contractor 403 (Store and JSON variants)
* [x] README section; ruff, mypy (cache /tmp/mypy-132), focused tests; commit, push, PR with Refs #132

Details: [details](../details/2026-11-04-contractor-job-pack-132-r2-details.md)

Stacked next: slice 3 persistence plus staff routes for receipts and escalations (needs owner waiver or #116); slice 4 staff screen with manual path and accessibility proof; slice 5 decision record.

## Critique (executed once)

Verdict: compatible. Applied: deny contractors in the core method as well as in `projection`; assert the order list is unchanged after the read. Tier: focused (no security, infrastructure, SQL or deployment change; read-only route behind existing default-deny).
