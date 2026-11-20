---
title: Issue 360 live plan
ms.date: 2026-11-20
---

## Plan

* Phase 1: in `Assistants.authorize`, after the REGISTRY role check, if `identity.is_entra(user)` set `current = identity.verified(user)` (None denies); otherwise keep the roster lookup. Keep the role-match, disabled and scope checks; Entra principals have no case_ids/areas, so they stay unscoped. The roster email equality check is replaced for Entra by the verified keys (verified already binds code and email).
* Phase 2: regression tests in src/api/tests/test_map_sensors.py: Entra Programme Manager and Quality Inspector read `sensors` and `map_sensors`; wrong role denied; Application Administrator-only role denied; tampered/revoked keys denied; roster behaviour unchanged (existing tests).
* Phase 3: mypy, ruff, affected api tests. Src change means the full tier applies; the coordinator runs the gate, never `--all` here.
* Details: .copilot-tracking/details/2026-11-20-issue-360-live-details.md
