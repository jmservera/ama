# Changes: #228 procurement screens WCAG 2.2

* `src/api/src/zava_forward/api/web/role-screens.js`: jump nav, panel anchors, `stateCue` prefixes for work-order state, checklist evidence and invoice status.
* `src/api/tests/test_procurement_screen_wcag.py`: new, 5 tests.
* `src/api/tests/test_procurement_screens.py`: `CONTROLS` no longer lists `a`.
* Validation: `tests.test_procurement_screen_wcag`, `test_procurement_screens`, `test_procurement_qa_screen_wcag`, `test_role_screens_conformance`, `test_connected_home_check`, `test_content_standard`, `test_design_system`, `test_accessibility_baseline`, `test_dependency_rule` pass (105 tests, worktree `src` on PYTHONPATH, `TMPDIR=/dev/shm/zf-tmp`); `ruff check` and `mypy` clean.
* Not run: browser keyboard harness and full local gate; engineering checks are not WCAG conformance acceptance (#151).
