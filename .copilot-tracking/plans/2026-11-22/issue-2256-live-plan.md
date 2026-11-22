# Plan: issue 2256

Tier FULL (src change); targeted tests only, coordinator runs gates.

1. handoff_ageing: tolerate naive offered_at and due_at (age_hours null, reason).
2. unaccepted_handoffs: sort unknown ages last.
3. app.js waitingRows and cell: accept null age, show "Unknown".
4. Regression tests in src/core/tests/test_handoff_escalation_83.py (or API test) and handoff waiting view test.
5. Run core, api targeted tests and web tests; mypy and ruff.
