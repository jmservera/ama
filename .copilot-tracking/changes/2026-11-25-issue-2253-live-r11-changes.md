# Changes: issue 2253 r11 (2026-11-25)

* src/api/tests/test_epic149_child_ux_contracts.py: added test_resident_sensor_chart_every_metric_in_node (temperature and humidity; tick count, plot clamping, marker gap, label clear of tick column). No src change; focused tier, no rpi-checks --all.
* docs/reference/research/issue-2253-live-r11-2026-11-25.md and issue-2253-live-r11-2026-11-25/ (probe, JSON, PNG).
* Validation: 66 tests OK (3 modules); ruff check, ruff format, mypy clean.

| Criterion | Status |
| --- | --- |
| Axis labels body-sized | Proven live |
| Circle markers, no thick stroke | Proven live |
| No tick overlap | Proven live |
| "Latest stored" label sized, no overlap | Unproven live (forecast hidden, data over 24 h old); proven by local tests on deployed-identical code |
| Forecast squares | Unproven live now (proven live in r10); proven by local tests |
| Narrow screens | Not applicable (desktop demo) |
