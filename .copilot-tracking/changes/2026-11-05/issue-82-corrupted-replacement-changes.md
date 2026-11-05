---
title: Issue 82 corrupted replacement changes (2026-11-05, continuation)
ms.date: 2026-11-05
---

* `quality.py` `submit_quality`: an in-progress record (Submitted, Returned, Fixed) no longer blocks a replacement only when every in-progress record for the measure has corrupted stored evidence (`evidence_gaps` non-empty or None) and the caller holds a quality role. Valid in-progress records keep the refusal. The existing supersession loop preserves originals, history and links; the replacement starts Submitted and needs normal independent acceptance. Fresh evidence validation unchanged.
* `test_gates.py`: three cases (recovery for Submitted/Returned/Fixed with originals kept and independent acceptance; unreadable items; role, malformed replacement and valid in-progress protection). All three errored before the code change.
* Checks (bytecode off, external caches): `test_gates` 20 OK; `test_quality_procurement.JsonFlows` and `test_hazard_referral.JsonHazardReferral` 60 OK; ruff check clean; mypy clean (266 files). SQL selectors (`SqlFlows`, `SqlHazardReferral`) not run: pending final gate. Ruff format reports `quality.py` already needs formatting upstream; not reformatted (unrelated).
* Full gate and independent review pending. No whole-#82 criterion claimed.
