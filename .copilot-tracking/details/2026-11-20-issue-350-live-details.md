# Details: issue 350 live (2026-11-20)

Phase 2: in test_sqlreads.py create a SqlStore, close it, edit `cases.owner_code` for one case directly with sqlite, reopen: `page_cases(user mine, limit=50)` total must equal the in-memory `Store.page_cases` (limit None) total and `counts()` must agree.
Phase 3: in `_migrate`, when not already stale, select id, body and the six columns; for each row compare to `_row(json.loads(body))` values; rebuild the full derived row for drifted ids only. Body is canonical; columns are derived.
Phase 4: run `PYTHONPATH` focused tests in src/core (test_sqlreads, test_sql*), mypy in src/core, ruff check.
