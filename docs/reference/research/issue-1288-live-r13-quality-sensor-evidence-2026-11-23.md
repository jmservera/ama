---
title: Quality sensor values and review flag, thirteenth audit (Refs #1288)
description: Thirteenth audit of the demo Quality sensor integration; closes a gap where physically impossible retained readings reached the Quality model and could back an autonomous flag, with the per-criterion proven or unproven table
ms.date: 2026-11-23
---

Scope: synthetic demo, desktop only. Follows the [twelfth audit](./issue-1288-live-r12-quality-sensor-evidence-2026-11-23.md). No Azure change; live legs are carried from that audit and were not re-probed.

## Finding and fix

The employee view marks a missing or impossible latest reading (outside 0 to 100 %RH or -40 to 60 degC) as "do not rely on it", but the snapshot sent to the Quality model carried no such marker, and only conflicting readings blocked the proactive request and the autonomous flag. An impossible reading could therefore be cited in an automatic L4 flag. The captured sensor source now carries `implausible_readings` and `implausible_notice`; no proactive request is made for it, and a returned finding is labelled `implausible-readings` (not autonomous, route to the ordinary quality check). Only implausibility present at capture time is handled.

## Result per unticked criterion

| Criterion | Result for the demo | Evidence and limit |
| --- | --- | --- |
| 3 | Proven locally (mock provider); not live | New grounding test compares the API view and the model request |
| 4 | Unproven | Release record not approved, owner not appointed (OQ-017); owner-only |
| 5 | Proven locally; not live | Existing flag tests |
| 6 | Proven locally, now including impossible readings | New test; earlier live states per r12 |
| 7 | Proven as local engineering evidence | 275 tests OK, 94 skipped (SQL Server and browser prerequisites) |
| 8 | Unproven | Blocked by criterion 4; no mock or fabricated release used |

Criteria 1, 2 and 9 are already ticked. No tick or closure is claimed.
