---
title: Issue 2244 live run 6 research (opening)
ms.date: 2026-11-24
---

Opening record. Scope: the issue has no tick-box list; criteria C1 to C5 come from the first run note (retry with backoff, read-only schema check, live start without crash-loop, concurrent writer cannot take the demo down, lock holder identified). Prior runs 1 to 5 sit on other branches; this base lacks the start-up fast paths for `_seed`, `_migrate_recommendations` and `_ensure_queue_membership` (commit b580955913). Evidence to follow below.

## Findings (read-only, 2026-11-24 UTC)

* Latest and ready revision `ca-cutover-test-demo-api--0000059` (created 00:14:20Z), Healthy, Running, 3 replicas; three `/healthz` probes returned 200.
* Probes: StartUp 40 x 3 s (initial delay 1 s), Readiness 3 x 5 s, Liveness 6 x 10 s.
* Deployed md5 prefixes (read-only `md5sum` via `az containerapp exec`): `sqlstore.py` 7ba7c82b8cee, `mssqlstore.py` 3cfaa6ff4557, `lawstore.py` 55343f798f45; identical to this checkout, so the revision carries this base.
* This base lacks `_recommendations_current` and the `_seed` / `_ensure_queue_membership` fast paths, so a populated store still takes the write lock three more times at start-up. That is the real remaining defect against the issue's "skip the write lock when the schema is current" suggestion (runs 4 and 5 recorded it; commit b580955913 on another branch).
* Planning Readiness: Ready. Disposition: executed.
