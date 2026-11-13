# Plan: #152 devices and widths (details: .copilot-tracking/details/2026-11-13/152-devices-widths-manifest-1408-details.md)

1. RED: add `DesignSystem` tests in `test_design_system.py`: doc has "Supported devices and widths" section naming 1280/768/360, 2026-11-13 owner decision, manual real-device/AT acceptance kept separate, 320px reflow retained; CSS has a `.layout` collapse at <=900px and a <=600px mobile block; manifest `152-ia-v1` covers all three roles with own-queue navigation and no role simulator; AC-034/AC-043 stay "not claimed".
2. GREEN: add the section to `design-system.md` Layout rules.
3. Validate: unittest design_system, workbench, queue_empty_state, accessibility_baseline; ruff check/format; mypy.
4. Do not touch role-screens.js, chat.js, log.md, manifest JSON, browser check. No criterion ticks.

## Critique dispositions (rubber-duck, Revise, applied directly)
* PC-001: also update `workbench-manifest.json` supported_devices to decided (desktop 1280, tablet 768, mobile 360; 1024/390/320 stay checked-only), add 360 to widths, update `supported-devices-proposal.md` status, and replace `test_supported_devices_stay_proposed...` in test_workbench.py.
* PC-002: 360 added to the browser-check width loop through the manifest; the Chromium check is not run here, so 360 is labelled unverified in the doc and review.
* PC-003: simulator-absence test checks each role's manifest navigation (no `#/simulator`) with a negative control.
