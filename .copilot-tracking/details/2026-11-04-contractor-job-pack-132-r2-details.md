---
title: Issue 132 round 2 details
ms.date: 2026-11-04
---

* `procurement.py`: `work_order_job_pack(user, work_order_id)` rejects contractors, checks the registered actor, builds the view with `_wo_view` and calls `job_pack.build_job_pack`.
* `projection.py`: `job_pack` added to `STAFF_GET` only; `CONTRACTOR_GET` unchanged.
* `server.py`: `get_kind` maps `/api/workorders/{id}/job-pack`; handler returns 200, 403 or 404.
* No AI feature, so no AI-unavailable path. Manual path: staff read the pack from the order and brief the worker.
