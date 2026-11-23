# Plan: issue 114 live re-verification (2026-11-23)

Tier: focused (test and documentation only; no src change).

* [x] Phase 1: research and live probe on the demo database (read-only throwaway job, deleted).
* [ ] Phase 2: add one test to src/core/tests/test_recovery.py for the reliance-gate report content and no-seal single-year run.
* [ ] Phase 3: run tests.test_recovery, tests.test_sqlstore, tests.test_ledger_digest_blob sequentially; ruff check on the test file.
* [ ] Phase 4: research note under docs/reference/research/, index entry, log entry.
* [ ] Phase 5: changes record with per-criterion table, review, local commit (no push).
