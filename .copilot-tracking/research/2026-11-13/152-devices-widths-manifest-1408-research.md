# Research: #152 supported devices and widths (2026-11-13)

* Owner decision (Batch-2 Q1): `devices_152_widths=desktop_1280_tablet_768_mobile_360`, 2 cycles.
* `design-system.md` Layout rules: `main` 1320px, `.layout` collapses under 900px; no supported-device statement.
* `style.css` breakpoints: 1100, 900 (`.layout`), 700, 600 (mobile), 1199/899 (case summary).
* `src/api/checks/workbench-manifest.json` (`152-ia-v1`): widths [320,390,768], 3 roles, unknown "Supported devices/browsers". Left untouched (browser check and tests consume it).
* PRD AC-034/AC-043 status "Not run"; PRD NFR table cites 320/390/1280 for accessibility checks. Reflow at 320 stays a separate requirement; owner tiers add 360 and 768.
* Planning Readiness: Ready.
