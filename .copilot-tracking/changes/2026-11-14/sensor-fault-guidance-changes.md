# Changes: sensor fault guidance (Refs #111)

* `src/core/src/zava_forward/core/sensor_view.py`: `reading_health`, plausibility constants, `health` in `view()`.
* `src/api/src/zava_forward/api/sensor_badges.py`: Withheld/fault/out-of-range badges, `next_action`.
* `src/api/src/zava_forward/api/web/ops.js`: next-action line.
* Tests: new core test; extended API badge test.
* Validation: core ruff/format/mypy clean; api ruff/format/mypy clean; 400 focused api tests OK (140 skipped, browser/env), incl. test_accessibility_baseline and quality-sensor suites; new core test OK. Run with worktree PYTHONPATH because the editable install points at the main checkout. No push; full gate not run (focused tier).
