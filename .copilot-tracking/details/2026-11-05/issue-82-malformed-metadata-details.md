---
title: Issue 82 malformed quality metadata details (2026-11-05, correction)
ms.date: 2026-11-05
---

* Tests in `Flows` (`test_quality_procurement.py`): for label `[]` and checklist `{}`, persist corruption with `save()`, reopen, then assert `accept_quality` raises `GateError` (not `TypeError`), the record state is unchanged, quality-role replacement supersedes it with original items kept and the replacement needs independent acceptance. Controls: valid record accepts; unknown checklist string still falls back.
* Code: `evidence_gaps` in `quality.py`.
* Final gate selectors (pending admission): `test_gates`, `test_quality_procurement` (`JsonFlows`, `SqlFlows`), `api/tests/test_mssqlstore.MssqlProcurement`, `test_hazard_referral`.
