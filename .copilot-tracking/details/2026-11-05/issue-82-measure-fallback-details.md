---
title: Issue 82 non-string measure fallback details (2026-11-05, correction 3)
ms.date: 2026-11-05
---

* Tests in `Flows` (`test_quality_procurement.py`), using the existing `corrupt_stored` helper: `checklist="Unlisted"` with `measure=["Loft insulation"]` raises `GateError` on `accept_quality` and leaves the record unchanged; controls: known checklist with a list measure still accepts; `measure=None` with `checklist="Unlisted"` and full evidence still accepts through the legacy General fallback only if its checks have evidence (the fixture's evidence is Loft labels, so the control asserts a `GateError` naming gaps, proving the fallback is used rather than a crash).
* Code: `evidence_gaps` in `quality.py`.
* Final gate selectors (pending admission): `test_quality_procurement` (`JsonFlows`, `SqlFlows`), `api/tests/test_mssqlstore.MssqlProcurement`, `test_gates`, `test_hazard_referral`.
