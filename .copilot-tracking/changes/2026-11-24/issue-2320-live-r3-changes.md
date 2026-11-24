---
title: Issue 2320 live re-check r3, changes
ms.date: 2026-11-24
---

No src change. Tier: focused (documentation and evidence only). Hosted CI for the exact head and independent review remain required; `rpi-checks.py --all` was not run. Nothing deployed, pushed or created in Azure. Sign-in values were never printed or stored (probe scripts assert this).

Files: docs/reference/research/issue-2320-live-r3-2026-11-24.md and its folder (two probe scripts, two JSON outputs, screenshot); docs/reference/README.md; docs/reference/log.md; `.copilot-tracking/` artifacts and state.

External write: issue #2320 criteria 1 and 4 ticked via the REST API. The issue stays open.

## Per-criterion table

| Criterion | Proven or unproven | Evidence |
| --- | --- | --- |
| #2320 1 Profile briefing time and write-lock wait | Proven | baseline and r2 notes |
| #2320 2 Briefing within 5 s, never 503 on a quiet system | Unproven (system not quiet; first GET after a change untested) | probe-r64.json: 5 of 5 under 0.85 s |
| #2320 3 Test proves read path avoids the write lock | Unproven in full (repeat GET under held denial only) | r2 note |
| #2320 4 Live re-check with elapsed times | Proven | research note table |
| Forecast within 10 s or named state (#2304) | Unproven as a bound: 13 of 14 within 10 s with `stale_seconds`, one 33.77 s outlier | probe JSON, container log |
| Briefing, retention fine | Proven (0.43 to 0.85 s; 2.25 s) | probe-r64.json |
| AI report fine | 200 but 135.17 s; slow | probe-r64.json |
