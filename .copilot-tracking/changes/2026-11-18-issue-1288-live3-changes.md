# Changes: issue 1288 live run 3 (2026-11-18)

Refs #1288. Docs and evidence only; no src change (FOCUSED tier; rpi-checks.py --all not run). Nothing created in Azure; nothing to delete.

## Files

* `docs/reference/research/issue-1288-live-r3-quality-sensor-evidence-2026-11-18.md` (new note), `docs/reference/log.md` (entry).
* `.copilot-tracking/evidence/2026-11-18/issue-1288-live3/`: `live_probe.py` and `live_probe.json` (GET-only), `live-sensor-panel.png` (the wider page screenshot was deleted because it showed names), `azure_readonly.txt`, `focused_tests.txt`.
* RPI artifacts: research, plan, details, critique, this record, review, state file.

## Per-criterion result (unticked criteria of issue 1288)

| # | Criterion | Result | Evidence |
| --- | --- | --- | --- |
| 3 | Quality snapshot consumes same IDs/values as UI | PROVEN locally (mock provider); UNPROVEN live | 304 tests OK, 85 skipped; live `tokens` 0 |
| 4 | Release-admitted durable deduplicated bounded flag | UNPROVEN for demo (local dedup/bounds proven) | forecast `proactive: false`, `call_allowance: 0`; no release record (OQ-017) |
| 5 | Visible finding with cited IDs, time, model, unapproved | PROVEN locally; UNPROVEN live | first-note browser check (33 passed); no live model output |
| 6 | Explicit missing/stale/unavailable states with human route | PROVEN locally; stale and unavailable OBSERVED live | `live-sensor-panel.png`, simulation lane `unavailable` |
| 7 | Focused SQL/API/browser correlation tests | PROVEN as local engineering evidence | `focused_tests.txt`; SQL Server and browser runs from first note (source unchanged) |
| 8 | Finite live walkthrough with actual model | UNPROVEN, cannot be proven for the demo | no simulator job, no release, no model call |

Production-only items (separate): OQ-017 release approver and residual-risk holder, admitted finite simulator run (#184/#189), calibrated sensors and thresholds, real-resident consent and DPO/Legal approval.

## Adverse and process notes

* The phase witness refused the first `implement-start` (reason: "missing persisted artifact evidence: changes") because the state file lacked the changes pointer; the pointer was added and the second call succeeded. Both records remain in the witness log.
* The first probe screenshot was clipped by the 900 px viewport; a taller viewport was used for the retained image.
* Revision changed to `--0000032` during the day by another worker's deployment.
* No tick or closure claimed; independent review and hosted CI outstanding.
