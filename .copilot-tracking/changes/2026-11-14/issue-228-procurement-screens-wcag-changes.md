# Changes: #228 procurement screens WCAG 2.2

* `src/api/src/zava_forward/api/web/role-screens.js`: jump nav, panel anchors, `stateCue` prefixes for work-order state and checklist evidence on the procurement and contractor screens.
* `src/api/tests/test_procurement_screen_wcag.py`: new, 5 tests.
* `src/api/tests/test_procurement_screens.py`: `CONTROLS` no longer lists `a`.
* Validation: `tests.test_procurement_screen_wcag`, `test_procurement_screens`, `test_procurement_qa_screen_wcag`, `test_role_screens_conformance`, `test_connected_home_check`, `test_content_standard`, `test_design_system`, `test_accessibility_baseline`, `test_dependency_rule` pass (105 tests, worktree `src` on PYTHONPATH, `TMPDIR=/dev/shm/zf-tmp`); `ruff check` and `mypy` clean.
* Not run: browser keyboard harness and full local gate; engineering checks are not WCAG conformance acceptance (#151).

## Cycle 2 correction

* Scope: jump nav and heading anchors only on procurement and contractor screens. Finance screens (#225) are untouched: no anchors, no jump nav, plain match status text.
* `workOrderCues` gains `Appointed`; `invoiceCues` gains `Matched` (queue cell only).
* `package-draft` anchor ids are sanitised and indexed so they stay valid and unique.
* `procurement_screens_browser_check.py` expectations updated to the prefixed text; browser run not performed.
* Tests: finance guard and Appointed and anchor tests added; 65 tests across procurement and finance screen suites and `test_connected_home_check` pass; `ruff check` and `ruff format --check` clean.
