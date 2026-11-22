---
title: Issue 2201 live6 changes
ms.date: 2026-11-22
---

Tier: focused (no source change). Azure read only; no resource created.

## Files

* Added `docs/reference/research/issue-2201-live-receiver-streak-2026-11-22.md`
* Edited `docs/reference/README.md` (index paragraph) and `docs/reference/log.md` (entry)
* Added evidence under `.copilot-tracking/evidence/2026-11-22/issue-2201-live6/`

## Per-criterion table

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Root cause recorded with evidence (logs, exit code) | Partly proven | SQL failures and the 11:32 argument error proven; the 13:30 `IOT_CALLBACK_FAILED` exception unproven (no recurrence; the handler drops the exception type); exit codes not logged |
| Fix merged and deployed | Proven | #2231 and #2234 per earlier notes; runs Succeeded on the deployed image |
| Three consecutive scheduled runs Succeeded | Proven | receiver 14:00, 14:30, 15:00 UTC |
| Readings from IoT Hub appear in the store and the employee map, with timestamps | Proven for the demo | map 200, 443 items; case sensors fresh, latest 2026-11-22T15:20:00Z; hub-to-store hop inferred |

## Validation

Documentation link and diff review; no unit tests apply. Hosted CI not observed (nothing pushed).
