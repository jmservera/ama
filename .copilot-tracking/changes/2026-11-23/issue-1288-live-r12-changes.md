---
title: Issue 1288 live audit r12, changes
ms.date: 2026-11-23
---

Status: complete. Tier FOCUSED; no src change. No Azure change, nothing to delete.

Files: `docs/reference/research/issue-1288-live-r12-quality-sensor-evidence-2026-11-23.md`, `docs/reference/README.md` (index), `docs/reference/log.md`, evidence folder `.copilot-tracking/evidence/2026-11-23/issue-1288-live12/` (probe script, scrubbed JSON, two screenshots, test log: 531 OK, 179 skipped), and the r12 RPI artifacts and state file.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| 1 Bounded read model | Proven (ticked) | Live: 7 of 12 cases `ok`, 12 readings cap, IDs, units, UTC, provenance |
| 2 UI shows values and context | Proven (ticked) | `live-sensor-panel.png`; outdoor weather labelled, not conflated |
| 3 AI snapshot uses identical IDs | Proven locally; unproven live | `focused_tests.txt` (mock provider) |
| 4 Release-admitted proactive durable flag | Unproven | Release record missing (OQ-017); forecast proactive false, allowance 0 |
| 5 Visible finding, IDs, model, unapproved status | Proven locally; unproven live | No live model output; AI tab shows no suggestions |
| 6 Explicit insufficient/unavailable states | Proven locally; seen live | `consent-withheld`, simulation `unavailable`/`not-configured`; stale not seen; one unretried 503 |
| 7 Focused tests correlate UI and snapshot | Proven as local engineering evidence | `focused_tests.txt`; SQL/browser cases skipped |
| 8 Live walkthrough to visible attributed flag | Unproven | Model leg blocked; `rai-metrics` consumption 0 |
| 9 Human acceptance and controls intact | Proven (ticked) | Unchanged source; tests OK |
