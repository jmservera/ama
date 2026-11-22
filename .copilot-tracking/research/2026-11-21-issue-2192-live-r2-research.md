---
title: Issue 2192 live research (round 2)
date: 2026-11-21
---

Research disposition: executed. Planning Readiness: Ready.

## Findings so far

* Main already holds the checkbox (commit a53ec6ce0e, #2197) and the local proof note `docs/reference/research/issue-2192-live-2026-11-21.md`.
* Prior round left one criterion unproven: live walkthrough on Azure. The live ca-resident-demo now serves `demo.js` with `sensor-consent` and carries the `ZF_DEMO_SENSOR_CONSENT*` settings, so a live proof is possible.
* Open question: does the live walkthrough reveal a defect (consent store reachable, SQL principal rights, employee view on ca-cutover-test-demo-api)?

## Live probe findings (2026-11-21, 23:50 to 00:10Z)

Script and output: `docs/reference/research/issue-2192-live-r2-2026-11-21/live_probe.py`, `live_probe.json`.

* Live resident page: native checkbox present (`type=checkbox`, wrapped in its `label`, `aria-describedby` to status and "does not change your repairs" text), starts unticked, Space toggles it, status text updates, focus stays on the checkbox, state survives reload. Restored to the initial (declined) state afterwards.
* Employee API (`ca-cutover-test-demo-api`, `GET /api/cases/{id}/sensors`, all 50 cases, before, after grant, after restore): no case changed state. Cause found in code: the employee view reads home id = case id (`Assistants.sensors` calls `sensor_view.view(db, case_id, ...)`), while the resident checkbox writes consent for `sensor_home_id` (`SYN-NE-001458-FLAT1`, seeded for issue 1072). The resident's case is ZF-2025-0031 or 0032 (the case search for the seeded home matched ZF-2025-0030, 0031, 0032 and 0041, which share the building anchor). The two keys never meet, so withdrawal on the live resident page cannot change the employee view. This is a real defect against criterion 3.
* Resident-side and audit behaviour are proven; audit rows on Azure SQL are not directly readable by this role (no SQL principal for the operator), so the audit criterion stays proven locally only unless the fix route exposes it.

Planning Readiness: Ready. Fix scope: the resident consent change must also apply to the home key the employee view reads (the resident's case id) when controls exist for it.
