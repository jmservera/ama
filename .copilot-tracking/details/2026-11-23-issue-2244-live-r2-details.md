# Details 2244 live r2

* `src/core/src/zava_forward/core/lawstore.py`: import `LOCK_RETRY_ATTEMPTS`; set retries in `MssqlDb.__init__`; add `end_startup`; try/finally in `LawStore.__init__`.
* `src/core/tests/test_mssql_startup_lock.py`: new `LawStoreStartupRetryTests`.
* Docs: `docs/reference/research/issue-2244-live-r2-2026-11-23.md`, README index, `docs/reference/log.md`.
