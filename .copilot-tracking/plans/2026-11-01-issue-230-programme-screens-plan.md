# Plan: issue 230 programme manager and coordinator screens

1. Core: add `returned` (reason, sender, from_stage, to_stage, at, next_action) and handoff `sender` to the work context in `core/taskqueues.py`; test in `src/core/tests`.
2. Web: extend `role-screens.js` with an optional per-screen `overview` hook (rendered with or without a selected home) and register `programme-queue` for managers and `Retrofit Coordinator`:
   * shared queue table: home, return reason, sender, current owner, proposed receiver; chase owner and resident-update owner in separate columns;
   * scope filter (`select`) with Apply and Reset; Reset restores defaults and changes no record;
   * lifecycle and funnel table from `/api/coordinator` with Unknown for missing values;
   * connected same-home gate table: technical, resident, delivery, quality, finance, each with textual state and Blocked when a gate is missing.
3. Tests: `src/api/tests/test_programme_screen.py` (node harness).
4. Validate: unit tests plus ruff check, ruff format --check, mypy for src/api and src/core.

Critique (inline, once): keep the slice read-only and reuse existing helpers; do not add a planner role that the codebase lacks (record as an assumption). Accepted.
* Correction cycle 2: restore main-side files; fix two finance gate cases with tests.
* Correction cycle 3: three further thread fixes with tests.
