---
title: Issue 79 details, slice 2
ms.date: 2026-11-04
---

* Phase 1: `Store._ranking_archive` (folder `ranking-archive` beside live data), `ranking_publication_status` (verify, overdue, SCHEDULE, `policy_signed` false), `publish_ranking_snapshot` (calls `ranking_snapshot`, then `publish` with `controls.today()`, audit entry).
* Phase 2: `server.py` GET `/api/ranking/publication`, POST `/api/ranking/publish`; both added to the route label table and role inventory.
* Phase 3: tests in `src/api/tests/test_ranking_publication_wiring.py` over real HTTP; README and log.
