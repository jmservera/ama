# Issue 189 details

Phase 1: in `src/api/src/zava_forward/api/live_control.py`, import `accountable_text` from `sensor_stream`; replace the `type(v) is not str or not v.strip()` clause with `not accountable_text(v)` while keeping the `PLACEHOLDERS` membership test.
Phase 2: add `test_owner_and_approval_must_be_accountable_text` using `document(owner=...)` and CLI start.
Phase 3: `python3 -m unittest tests.test_live_control tests.test_simulator_admin` from `src/api` with `PYTHONPATH=../core/tests:../agents/tests`; mypy; ruff.
