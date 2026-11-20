---
title: Issue 360 live changes
ms.date: 2026-11-20
---

## Changes

* src/core/src/zava_forward/core/assistants.py: `Assistants.authorize` now uses `identity.verified(user)` as the current actor for Entra principals (role must still match REGISTRY roles; unscoped case_ids/areas) and keeps the roster lookup for other users. `sensors`, `map_sensors`, `listing`, proposal, review and task paths all use `authorize`, so they inherit the fix.
* src/api/tests/test_map_sensors.py: three regression tests (Entra Programme Manager and Quality Inspector read `sensors` and `map_sensors`; other, Application Administrator-only and view-only roles denied; forged or revoked keys denied).

## Validation

* `python3 -m unittest test_map_sensors` (src/api): 16 tests OK with the fix; without the fix the Entra read test errors.
* `test_entra_authoritative` and `test_assistants`: 175 tests OK (60 skipped, SQL Server fixtures).
* ruff check src/core and the test file: clean. mypy in src/core and src/api: 23 and 7 errors, identical to the baseline before the change (missing opentelemetry stubs, unused-ignore in device_provision.py); none in changed files.
* Not run: rpi-checks.py (coordinator gate), live Azure browser proof (the defect needs a deployed rebuild; this commit is local only and nothing was deployed).

## Acceptance criteria status (issue #360)

| Criterion | Status |
| --- | --- |
| a, b, f | Already ticked in the issue; not re-proven here. |
| c, d, e | Ticked as "moved to #2121"; not proven for the demo here: they need owner-approved migration, live ingress and Front Door retirement, outside this defect fix. |
| Defect: Entra Programme Manager/Quality Inspector read sensors | Proven by the new tests (fail before, pass after). Live confirmation is unproven until the fix is deployed. |
| Wrong role, admin/view-only, revoked keys denied | Proven by the new tests. |
| Roster behaviour unchanged | Proven by the passing existing suites (test_assistants, test_map_sensors). |

Tier: src change, so the full tier applies; the coordinator runs the gate.
