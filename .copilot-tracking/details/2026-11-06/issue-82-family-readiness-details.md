---
title: Issue 82 remaining gate family readiness details (2026-11-06)
ms.date: 2026-11-06
---

* Input: a case whose single active work order is Appointed; output: `GateResult(gate="capacity")` with outcome pass, fail or unknown, reason, owner (contract manager), correction and `rule` provenance (source, effective date, version, reviewer).
* Pass: the existing checks all succeed (evidenced committed capacity, covered home, period contains the appointment date, no deficit, named authorised accepting manager with current contract authority).
* Fail: capacity or authority present but unmet (outside period, deficit, authority changed/revoked). Existing message is the reason.
* Unknown: capacity or authority record missing, legacy, unreadable or hash-mismatched. Never passes; booking still refuses.
* `advance` keeps its order (safety, resident, booking gates, capacity) and its exception types.
* Tests that must fail first (shared flows so Json, SQLite and MssqlProcurement inherit): (1) capacity gate result for a covered booking is a pass with the capacity rule provenance and unreviewed marker; (2) outside-period date, deficit and revoked authority give fail with the existing reason; (3) legacy/corrupt capacity details give unknown and `advance` still refuses with no state change; (4) valid booking unchanged.
* Dependencies and boundary: reuse `procurement.py` helpers and `gates.check`; target parent 81; main integration via later ordinary merge; no persisted shape change.
* Not activation: the rule is an unreviewed exercise fixture; no named professional approval is implied.
