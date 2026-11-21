# Changes: issue 1288 live pass (2026-11-21)

Tier: FOCUSED (docs and evidence only; no file under src/ changed). Plan: [plan](../../plans/2026-11-21/issue-1288-live-plan.md).

## Files

* docs/reference/research/issue-1288-live-r6-quality-sensor-evidence-2026-11-21.md (new)
* docs/reference/README.md (one index line), docs/reference/log.md (one entry)
* .copilot-tracking/evidence/2026-11-21/issue-1288-live6/ (probe script, scrubbed JSON, Home sensors screenshot)
* .copilot-tracking RPI artifacts for this task

## Validation run

* Local tests, six quality sensor modules from src/api: 465 tests OK, 179 skipped (SQL Server and browser prerequisites).
* Live read-only: simulator job succeeding every five minutes, two homes with fresh retained readings, ten homes consent-withheld, Quality model refused at release admission, model counters 0.
* No git push, no PR, no Azure write, no model call, no secret printed.

## Per-criterion table (unticked criteria)

| Criterion | Status | Basis |
| --- | --- | --- |
| 3. Snapshot uses identical IDs and values as the UI | Proven locally (mock); unproven live | Local tests; no live model request |
| 4. Release-admitted deduplicated bounded proactive flag | Unproven | No approved release record (OQ-017); forecast proactive false, allowance 0; local dedup and bounds proven |
| 5. Employee sees finding, cited IDs, time, model/version, unapproved status | Proven locally; unproven live | No live model output |
| 6. Explicit insufficient, blocked and unavailable states with human route | Proven locally and observed live | consent-withheld with zero readings, suspended assistants with manual route |
| 7. Focused SQL, API and browser correlation tests | Proven as local engineering evidence | 465 tests OK; earlier SQL Server and browser runs stand, no source change |
| 8. Live simulator to model to visible attributed flag | Unproven | Simulator, Hub, SQL, UI legs observed; model leg blocked by missing approved release |

No tick or closure is claimed. Criteria 1, 2 and 9 stay ticked.
