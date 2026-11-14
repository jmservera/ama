# Changes: #233 connected journey

* `src/api/src/zava_forward/api/web/role-screens.js`: `journeyStageMap(c, current)`, `ownsStageMap` on `programme-queue`, shared render in `roleScreensView`.
* `src/api/tests/test_role_screens_connected_journey.py`: new (6 tests, 7 roles).
* `docs/reference/research/ux/atlas-screen-trace.md`, `docs/reference/log.md`: dated updates.

Validation: 282 api tests across role screens, workbench, heading hierarchy (Chromium), accessibility baseline, content standard, connected-home check, role matrix; core atlas trace OK; ruff check/format and mypy clean. Not run: browser checks of the new panel, AT, user validation, full gate.
