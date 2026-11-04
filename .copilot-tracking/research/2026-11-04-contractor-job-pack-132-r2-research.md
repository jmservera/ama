---
title: Issue 132 round 2 research
ms.date: 2026-11-04
---

Research disposition: executed (narrow). Planning Readiness: Ready.

* Merged for #132: PR 873 (slice 1, pure core rules in `job_pack.py`). PRs 900 and 869 are unrelated unmerged work and not counted.
* Open: criterion 6 (owner decision on staff-mediated intake or portal, identity via #116) and persistence of receipts, acknowledgements and escalations.
* Issue comment 2026-11-03: the owner has not authorised a persistence slice. A read-only staff job pack adds no contractor identity, writes or SQL, so it needs no waiver.
* Existing seams: `ProcurementMixin._wo_view` and `list_work_orders`, `projection.allowed` default deny, `server.get_kind`. Contractors cannot reach new kinds by default.
* Smallest coherent slice: staff-only `GET /api/workorders/{id}/job-pack`, advancing criterion 1 end to end at API level.
