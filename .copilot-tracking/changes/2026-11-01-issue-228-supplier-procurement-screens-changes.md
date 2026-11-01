# Changes: issue 228 supplier, contractor and procurement screens (2026-11-01)

* Added: `procurement-packages` (Package queue, managers) and `contractor-job-pack` (Contractor) read-only role screens appended to `src/api/src/zava_forward/api/web/role-screens.js`.
* Added: `src/api/tests/test_procurement_screens.py` (4 node-vm tests).
* Validation: new, role_screens, asset_board_screen, design_system and accessibility_baseline tests pass (28); `ruff check`, `ruff format --check` clean; mypy reports only pre-existing untyped-import errors outside touched files. Browser and axe keyboard checks not run locally (no playwright); CI is the evidence.
* Review fixes (PR #655 threads): resident-scope prerequisite now excludes withdrawn orders, compares work-order scope_version to the package (added `scope_version` to the work-order projection in core), reports Unknown when unavailable; queue shows recorded counts with capacity evidence status; checklist and review state derive from records or show Unknown. Tests added.
* Divergence: none from plan.
