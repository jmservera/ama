# Issue 687 IO contention plan (2026-11-01)

* [x] Add opt-in `ZF_BENCH_IO_CONTENTION=N` fsync writer processes to `Scale.test_sql_reads_at_60000`.
* [x] Measure at 4 and 16 writers; record the bound.
* [x] Keep the 1,500 ms threshold unchanged; no query or index change.
* [x] Validate: test_sqlreads, ruff check, ruff format --check, mypy for src/core.
* Critique: executed once, inline; no significant finding (opt-in, test-only, default unchanged).
