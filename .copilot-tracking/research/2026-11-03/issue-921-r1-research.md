---
title: Issue 921 research, _unhandled hides backend ConnectionError
ms.date: 2026-11-03
---

* Disposition: executed. Planning Readiness: Ready.
* Prior merged PRs: #691 introduced the 500 path; #796 added the client-disconnect branch. No merged PR delivered #921 (git log on main, gh search).
* Code: src/api/src/zava_forward/api/server.py `_unhandled` returned silently for every ConnectionError; `end_headers` set `_response_started` after the flush.
* Slice: single slice covers all three acceptance criteria; no stacking needed.
* Not security/infrastructure/SQL/deployment: focused tier.
