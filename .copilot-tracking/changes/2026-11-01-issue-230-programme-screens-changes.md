# Changes: issue 230 programme screens

* `src/core/src/zava_forward/core/taskqueues.py`: work context exposes `returned` (reason, sender, stages, time, next action) and handoff `sender`; reason and sender stay held for restricted roles.
* `src/core/tests/test_taskqueues.py`: test for the new fields.
* `src/api/src/zava_forward/api/web/role-screens.js`: optional `overview` hook; `programme-queue` screen for managers and Retrofit Coordinator (shared queue, separate chase and resident-update owners, scope filter with reset, funnel, five-gate same-home view).
* `src/api/tests/test_programme_screen.py`: node-driven tests.

Divergence: none from plan. No planner role exists, so none was added.

Validation: new and touched tests pass; ruff check, ruff format --check pass for touched files; mypy passes for touched files. Full `src/api` discovery shows 4 failures in untouched areas (missing playwright module, operator suspension); not caused by this change.
