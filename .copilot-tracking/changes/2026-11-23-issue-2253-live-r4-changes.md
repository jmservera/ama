---
title: Issue 2253 live r4 changes
ms.date: 2026-11-23
---

Refs #2253. Tier FULL (src changed); `rpi-checks.py --all` not run, the coordinator runs gates. The web-design-guidelines source was not re-fetched; this is unperformed.

Changes: `src/api/src/zava_forward/api/resident_demo/web/demo.js` (forced latest marker replaces a too-close neighbour, so no touching pair; "Latest stored" flips to the divider's right when under 90 units of room, so it cannot reach the 45 tick) and a regression test in `src/api/tests/test_epic149_child_ux_contracts.py`.

Validation: `test_epic149_child_ux_contracts`, `test_accessibility_baseline`, `test_content_standard`, `test_resident_demo_api` (98 tests) pass; `resident_sensors_browser_check.py` all PASS; mypy clean in src/api; ruff clean; `node --check` passes. Live baseline: [json](../../docs/reference/research/issue-2253-live-2026-11-23/live-r4-before.json), [png](../../docs/reference/research/issue-2253-live-2026-11-23/live-r4-before.png).

| Criterion (issue "Expected") | Status | Evidence |
| --- | --- | --- |
| Axis and marker labels sized like body text | Proven live | 16.8 px against 16 px, revision 0000027 |
| No overlap of "Latest stored" and the 45 tick | Proven live (no label on live data); fix guards it by code | 0 overlaps; static test; the fix is not deployed |
| Circle markers on stored readings | Proven live | 18 circles |
| Stored readings not one thick stroke | Proven live, touching pair fixed in code only | 1 touching pair live; fix not deployed, no deploy authorised |
| Legend and forecast squares | Unproven live in this probe | local browser check passes forecast-point count 12 |
| Narrow-screen rule | Unproven | desktop-only demo |
