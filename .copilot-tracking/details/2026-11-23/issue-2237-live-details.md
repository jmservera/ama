# Issue 2237 live details (2026-11-23)

Plan: `.copilot-tracking/plans/2026-11-23/issue-2237-live-plan.md`.

## Phase 2 core helper

File `src/core/src/zava_forward/core/mssqlstore.py`, next to `LOCK_FAILED`:

```python
def is_write_lock_busy(exc: BaseException | None) -> bool:
    """True when exc, or an exception it chains from, is the driver error for a timed-out write lock (SQL 50002)."""
```

Walk `exc`, `__cause__`, `__context__` (bounded, with a seen set). Match when `type(e).__module__` starts with `mssql_python` or `pyodbc` and the class name is `ProgrammingError` or `DatabaseError`, and `LOCK_FAILED in str(e)`. Never log `str(e)`.

## Phase 3 API mapping

File `src/api/src/zava_forward/api/server.py`, function `_unhandled`: after the client-disconnect branch and frame calculation, handle the busy case before the 500 log. Only when `not sent`: log WARNING, then `self._json(503, {...}, extra={"Retry-After": "5"})` inside the same try/except used for 500. If `sent`, fall through to the existing 500 logging so a started response is never double-answered.

## Phase 4 tests

* `src/core/tests/test_mssql_startup_lock.py`: helper cases using its existing fake driver error classes (extend with a class named `ProgrammingError`).
* `src/api/tests/test_error_logging.py`: new tests in `ErrorLoggingTests`.

## Validation

* `cd src/core && python3 -m unittest` for the touched module via `PYTHONPATH=src:tests`.
* `cd src/api` with the documented PYTHONPATH for `test_error_logging`.
* `python3 -m mypy` in `src/core` and `src/api` (api with `PYTHONPATH=../core/src:../agents/src`), `ruff check`, `ruff format --isolated --line-length 100 --check` on touched files.
