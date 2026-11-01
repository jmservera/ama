# Issue 687 IO contention changes (2026-11-01)

* `src/core/tests/test_sqlreads.py`: added `_churn_io` and opt-in `ZF_BENCH_IO_CONTENTION` writers; default behaviour and the 1,500 ms threshold unchanged.
* Validation: `test_sqlreads` OK at default; ruff check, ruff format --check and mypy clean for src/core. Under 16 writers the benchmark fails by design with the new timing/load context (expected diagnostic).
* Correction cycle (PR #720): merged origin/main; contention writers (CPU and IO) now registered on a `contextlib.ExitStack` nested in the `TemporaryDirectory` scope, so they are terminated and joined before directory removal. Review AC1 corrected to unmet.
