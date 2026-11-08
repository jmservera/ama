---
title: Research for #184 slice 2, bounded cohort and finite run control
ms.date: 2026-11-08
---

* Research disposition: executed (bounded, inline; no broad programme per the 2026-11-08T19:00Z owner directive). Planning Readiness: Ready. Resumes original session 0e13785f; slice 1 artifacts (2026-11-04) are preserved unchanged.
* Branch lifecycle: parent `feat/live-simulator-integration-184` has no PR of its own; child PRs #1205 (#185) and #1203 (#188) merged into it, #1088 (slice 1) is merged into main. Local `ead177ef` was an ancestor of remote parent `9476dc96`; fast-forwarded, then merged `origin/main` `ecb28815` (one conflict in `src/api/checks/sensor_sql_check.py`, resolved by keeping main's selector structure and the parent's extra default tests). No reset, rebase or force.
* Process note: the merge was committed (`e41546ab`) before this prospective plan was written; the plan was recorded before any source change.
* Existing: sender (`live_simulator`), generator, job template, `device_provision` dry-run (#185), consumer admission of `live-sim-reading-v1` (#1203), `HubReceiver` library (`iot_stream`, at most 100 bindings, bounded run of at most 3600 s). Observed Azure facts supplied by the coordinator: hub `iot-cutover-test-rzsrg` (uksouth, `ama`); only Manual jobs exist, no scheduled simulator.
* Gaps: the sender enumerates every open home (would exceed the 100-binding receiver), has no finite expiry, no stop switch and no admin-written configuration; no hosted receiver entry exists.
* Unresolved, owner or executor: device registration and certificates, SQL grants, app-level admin UI for the controls (not delivered here; control is Azure RBAC on the job and file share), real throttle and prices.
