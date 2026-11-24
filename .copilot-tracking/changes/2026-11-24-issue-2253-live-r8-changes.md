# Changes: issue 2253 live r8

Files added: docs/reference/research/issue-2253-live-r8-2026-11-24.md, its probe_r8.py, live-r8-0000030.json and .png. No src change; no deploy; no Azure change; tier focused.

Validation: live Playwright probe on ca-resident-demo--0000030; `unittest tests.test_epic149_child_ux_contracts` 17 OK.

| Criterion | Status |
| --- | --- |
| Axis labels sized like body text | Proven (live, 12 px x 1.396 vs 16 px body) |
| No overlap | Proven live for axis ticks (0 overlaps); "Latest stored" overlap proven locally only |
| Circle markers on stored readings | Proven live (17 circles, 0 touching) |
| Not one thick stroke | Proven live |
| Forecast squares render normally | Unproven live: stored data older than 24 h so no forecast; proven by local tests only |
