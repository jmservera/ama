# Changes: issue 226 asset executive and board views (2026-11-01)

* Added: `asset-board` role screen (read-only) appended to `src/api/src/zava_forward/api/web/role-screens.js`, for the two manager roles.
* Added: `src/api/tests/test_asset_board_screen.py` (3 node-vm tests).
* Validation: new, role_screens, workspace_scripts, design_system, accessibility_baseline tests pass; full `src/api` discover run: 1472 tests, 2 errors (missing `playwright` module and `test_resident_demo_api` import path, environment only, in test_browser_asset_urls and test_static_assets, which do not touch this change). ruff check and format clean; mypy reports no error in touched files (37 pre-existing environment errors elsewhere).
* Divergence: none from plan. Browser and axe keyboard checks not run locally (no playwright); CI is the evidence.
