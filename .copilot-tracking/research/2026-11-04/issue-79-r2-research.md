---
title: Issue 79 research, slice 2
ms.date: 2026-11-04
---

* Research disposition: executed (repository and merged-PR inspection). Planning Readiness: Ready.
* Merged: #896 (slice 1, pure `ranking_publication` module, nothing calls it). Criteria 1 and 2 already ticked on the issue.
* Gap: `publish` is not reachable from the store or API, so criterion 4 has no operable manual path.
* Blocked, human or deployment: named owner and signature (criterion 3), scheduler and retention (Legal, deployment).
* Smallest coherent slice: manager-only store methods plus `POST /api/ranking/publish` and `GET /api/ranking/publication`, audited, using the existing archive dir beside the data.
* Evidence: `store.py` `ranking_snapshot`, `server.py` ranking routes, `test_role_endpoint_inventory.py` route inventory.
