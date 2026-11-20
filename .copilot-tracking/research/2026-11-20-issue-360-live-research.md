---
title: Issue 360 live research (Entra authorize defect)
ms.date: 2026-11-20
---

## Scope

Owner-reported defect on the live demo: an Entra principal with ZavaForward.ProgrammeManager sees "Your staff account is not linked to your role" on Home sensors. Issue #360 itself (direct HTTPS ingress) has every acceptance criterion ticked (c, d, e moved to #2121), so no unticked criterion remains; the defect is the work item.

## Findings

* `Assistants.authorize()` (src/core/src/zava_forward/core/assistants.py, ~1495) reads `staff` by `user["email"]`. Entra principals carry `e-<hash>@entra.invalid` (identity.email_for) and have no staff row, so every Entra user raises "Current staff role has changed or been revoked."
* `sensors`, `map_sensors` (per-case loop catches PermissionError and returns "restricted"), `listing`, proposal, review and task paths all route through `authorize`, so one fix covers them.
* Sibling modules (coordinator.py ~163, chat_privacy, resident_decisions) use `identity.verified(user) if identity.is_entra(user) else roster`. `identity.verified` returns a copy only when code and email still match the tenant/object keys or the verified roster binding; it returns None otherwise (revoked or forged).
* The REGISTRY roles check precedes the lookup, so an Application Administrator or view-only principal (role not in REGISTRY roles) is already denied.
* Entra principals carry no case_ids/areas scope, so scope is unrestricted (None), as in the roster rows without scope.

## Planning Readiness

Ready. Disposition: executed. Evidence: code reading above; existing tests in src/api/tests/test_map_sensors.py and test_assistants.py provide fixtures.
