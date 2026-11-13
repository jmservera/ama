# Changes: 149 UX parent C1 fix

Status: implemented; verified locally (no Chromium run, per brief).

* programme_paging_browser_check.py: F-1 asserts Next disabled and focus on programme-prev after reaching the last page, with no extra request; the stale Enter is removed. After Previous returns to page 1 it asserts focus on programme-next (syncPager) and presses Enter instead of Tab. F-2 removed the `True` check.
* role-screens.js: F-3 HELD_CHECK_UNREADABLE now carries `Owner: you, the signed-in reviewer.`
* test_content_standard.py: new test for reason, Owner:, Next action:, banned words on HELD_CHECK_UNREADABLE.
* Manifest digests unchanged (none of the hashed sources were touched).

Validation: test_programme_screen, test_content_standard, test_design_system, test_workbench (60 OK); test_scenario_manifest, test_needs_inventory (19 OK); ruff check, ruff format --check, mypy from src/api (236 files, 0 errors); node --check.
Not run: browser check (Chromium out of scope).
