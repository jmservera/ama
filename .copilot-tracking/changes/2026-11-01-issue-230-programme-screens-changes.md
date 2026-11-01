# Changes: issue 230 programme screens

* `src/core/src/zava_forward/core/taskqueues.py`: work context exposes `returned` (reason, sender, stages, time, next action) and handoff `sender`; reason and sender stay held for restricted roles.
* `src/core/tests/test_taskqueues.py`: test for the new fields.
* `src/api/src/zava_forward/api/web/role-screens.js`: optional `overview` hook; `programme-queue` screen for managers and Retrofit Coordinator (shared queue, separate chase and resident-update owners, scope filter with reset, funnel, five-gate same-home view).
* `src/api/tests/test_programme_screen.py`: node-driven tests.

Divergence: none from plan. No planner role exists, so none was added.

Validation: new and touched tests pass; ruff check, ruff format --check pass for touched files; mypy passes for touched files. Full `src/api` discovery shows 4 failures in untouched areas (missing playwright module, operator suspension); not caused by this change.

Review-thread amendments (PR 662):

* `taskqueues.py`: `returned` is built independently of the primary reason, so a blocker or pending handoff keeps the return metadata; `advance` events are excluded; the current `case.resident_update.owner` is projected as `resident_update_owner`.
* `role-screens.js`: queue shows the recorded handoff state, not an inferred pending label; resident-update owner reads the current commitment; Quality gate derives from non-superseded records per measure (submitted, awaiting reinspection and unchecked measures stay Blocked); funnel requests `view=all`.
* Tests: overlap, advance exclusion and the new gate and state cases added to `test_taskqueues.py` and `test_programme_screen.py`; both pass, ruff clean.

Review-thread amendments (PR 662, round 3):

* `role-screens.js`: the programme screen now has a `load` hook reading the selected home's role-projected `/api/workorders?case=`; Delivery derives from current non-withdrawn orders and `appointment_control` (legacy `appointments` no longer used), and is Blocked with "evidence missing" when orders cannot be loaded or none are active. Finance adds blockers for a budget not `Approved`, active invoice holds (with holder) and unresolved match exceptions; decided invoices are historical and ignored.
* `taskqueues.py`: returned sender falls back to the legacy `by` field, still through `text()`.
* Tests: `test_programme_screen.py` and `test_taskqueues.py` extended; pass, ruff clean.
* CI: `activation` failure is the daily AIC guardrail stopping to preserve API quota (transient, not code); rerun requested.
