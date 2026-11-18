---
title: Issue 111 live3 research
ms.date: 2026-11-18
---

Task: issue-111-live3 (session rpi-111-live). Refs #111. Synthetic demo, desktop, docs/evidence only, Tier FOCUSED. Earlier same-day runs (live, live2) are preserved unchanged.
Research disposition: executed. Planning Readiness: Ready.

Open criterion: C3 R1 to R3 complete before a derived measure is used beyond an exercise rule. C1 and C2 are ticked.

## Findings

* 26 core sensor tests pass (1 expected failure), SQLite only.
* Signed-in demo (revision 0000032): sensors payload `retained-reading-view-v2`, calibrated false, stale; repeat read same content; drafts routes 403 for employee role; no task created.
* C3 needs R2 reviewer/Asset sign-off, R3 agreed limits, R1 standards texts; runtime gate sits in parent topic PR #1641, not main (no gate in `sensor_analysis.py`).
* Evidence: docs/reference/research/issue-111-live3-sensor-evidence-2026-11-18.md and issue-111-live3-raw/.
