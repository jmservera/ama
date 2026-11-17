# Changes: resident demo agenda guard (#1053)

Date: 2026-11-14.

* `src/api/src/zava_forward/api/resident_demo/app.py`: `agenda_available` in the view; `callbacks_available` kept as alias.
* `src/api/src/zava_forward/api/resident_demo/web/demo.js`: uses `agenda_available`; unconfigured lede notice replaces the invitation.
* `src/api/tests/test_resident_callbacks_page.py`, `test_resident_demo_api.py`: updated.

Validation (worktree sources on PYTHONPATH): `test_resident*` 275 tests OK, `test_accessibility_baseline.py` 13 OK, mypy, ruff check and format rc=0.
