# Changes: issue 2256

Tier FULL (src change); no rpi-checks --all run (coordinator owns gates). Refs #2256.

## Files

* src/core/src/zava_forward/core/workflows.py: `handoff_ageing` uses `_optional_tz_instant`; a timezone-less or missing `offered_at`/`due_at` no longer raises; row kept with `age_hours` null; `unaccepted_handoffs` no longer swallows errors, sorts unknown ages last.
* src/api/src/zava_forward/api/web/app.js: waiting view accepts null age and shows "Unknown. The offered time has no recorded timezone."
* src/core/tests/test_handoff_escalation_83.py, src/api/tests/test_handoff_waiting_view.py: regression tests (offer with naive offered_at is listed; Node view renders Unknown).
* docs/reference/research/issue-2256-handoff-waiting-2026-11-22.md: live probe and cause.

## Validation

* core `test_handoff*.py` (PYTHONPATH to worktree): 33 OK. api `test_handoff*.py`: 34 OK, 11 opt-in browser skipped.
* Web UI: test_accessibility_baseline, test_content_standard, test_handoff_waiting_view: 58 OK, 4 browser skipped (ZF_BROWSER_TESTS not set).
* mypy src/api clean; src/core mypy shows 3 errors in telemetry.py and device_provision.py, not touched by this change. ruff check clean; workflows.py was already unformatted before the change.
* Note: the default editable install points at the main checkout, so tests need the worktree PYTHONPATH.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Offered handoff appears in waiting list with due time and chase owner | Proven by regression tests; not proven on deployed host (not deployed, no push) |
| Cause identified in src | Proven: live probe (/api/handoffs 4 rows, unaccepted 0) plus code trace |
| Web UI tests run after web change | Proven for non-browser tests; browser tests (ZF_BROWSER_TESTS) not run |
| Live fix verification | Unproven: needs deploy of this commit |
