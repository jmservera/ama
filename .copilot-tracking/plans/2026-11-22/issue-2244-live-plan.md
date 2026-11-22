# Plan: issue 2244

1. Add start-up lock retry with exponential backoff to `_Conn.execute("BEGIN IMMEDIATE")` in mssqlstore.py, enabled only by `MssqlStore._initialize`.
2. Add focused regression tests (fake driver) in src/core/tests.
3. Run core targeted tests, mypy, ruff.
4. Changes record with per-criterion table; review; commit locally (no push).

Details: .copilot-tracking/details/2026-11-22/issue-2244-live-details.md
