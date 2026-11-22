---
title: Issue 2201 live7 changes
ms.date: 2026-11-22
---

No source change; focused tier. Azure read only; no throwaway resource created.

## Files

* `docs/reference/research/issue-2201-live-receiver-s3-streak-2026-11-22.md` (new note)
* `docs/reference/README.md` (index paragraph), `docs/reference/log.md` (entry)
* `.copilot-tracking/evidence/2026-11-22/issue-2201-live7/` (command outputs, probe, screenshot)

## Per-criterion table

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Root cause recorded with evidence (logs, exit code) | Partly proven | SQL cause proven in earlier notes; 13:30 `IOT_CALLBACK_FAILED` exception class not logged; no exit code in execution records |
| Fix merged and deployed | Proven | #2231, #2234 on main; job on digest 541068 |
| Three consecutive scheduled runs Succeeded | Proven | nine, 14:00 to 18:00 UTC, `receiver-executions.json` |
| Readings from IoT Hub in store and map, with timestamps | Proven for the demo | map 200; readings to 18:30:00Z fresh; hub hop inferred |
| SQL DTU healthy on S3 (goal) | Proven | Standard 100 DTU; max 89 percent after 14:00; connection_failed 0 |

## Validation

Link and diff review; sloptrim detector unavailable in this environment (not scored). Hosted CI for the exact head is not observed (local only, not pushed).
