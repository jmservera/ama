---
title: Details for #99 slice 1
ms.date: 2026-11-04
---

* `server.py`: one kind-map entry and one GET branch returning `s.exposure_signal(u)`; PermissionError becomes 403.
* Tests use a temporary limits file via `ZF_APPROVED_LIMITS` with synthetic approver names only.
* Human boundary: the signal never approves, resumes or accelerates; restart needs recorded Board approval.
* AI is not involved, so no AI-unavailable path applies.
