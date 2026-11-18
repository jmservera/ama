# Changes: chat keyboard and live announcement (Refs #159)

Date: 2026-11-14.

* `src/api/src/zava_forward/api/web/chat-widget.js`: transcript log `aria-relevant` now `additions text`.
* `src/api/tests/test_chat_origin_badge_a11y.py`: assertion updated to the new value.
* `src/api/tests/test_workbench_chat_keyboard_live_announce.py`: new focused static checks.

## Validation

* `discover -p test_chat_*.py` 147 tests OK (1 skipped); `test_case_journey` 31 OK; `test_accessibility_baseline` 13 OK; new module OK.
* mypy, ruff check and ruff format --check clean in `src/api` with `/tmp` caches.
* Run with `PYTHONPATH` set to this worktree's `src/*` (the installed core pointed at another checkout and lacked `CommittedReloadError`). Not run: `rpi-checks.py --all`, hosted CI, real screen reader.
