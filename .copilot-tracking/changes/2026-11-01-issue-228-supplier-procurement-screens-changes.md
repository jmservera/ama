# Changes: issue 228 supplier, contractor and procurement screens (2026-11-01)

* Added: `procurement-packages` (Package queue, managers) and `contractor-job-pack` (Contractor) read-only role screens appended to `src/api/src/zava_forward/api/web/role-screens.js`.
* Added: `src/api/tests/test_procurement_screens.py` (4 node-vm tests).
* Validation: new, role_screens, asset_board_screen, design_system and accessibility_baseline tests pass (28); `ruff check`, `ruff format --check` clean; mypy reports only pre-existing untyped-import errors outside touched files. Browser and axe keyboard checks not run locally (no playwright); screen-specific browser, keyboard, reflow and axe validation for these two screens remains unproven (no registered scenarios in `role_screens_browser_check.py`; tracked as follow-up).
* Review fixes (PR #655 threads): resident-scope prerequisite now excludes withdrawn orders, compares work-order scope_version to the package (added `scope_version` to the work-order projection in core), reports Unknown when unavailable; queue shows recorded counts with capacity evidence status; checklist and review state derive from records or show Unknown. Tests added.
* Review fixes (round 3): resident-scope test now asserts the State cell of that prerequisite row; browser/axe claim corrected to state validation is unproven.
* Divergence: none from plan.
