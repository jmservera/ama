# Plan 2244 live (2026-11-23)

## Phases
* [ ] P1 Add `_tables_current`, `_chat_memory_current`, `_indexes_current`, `_queues_current` read-only checks to `src/core/src/zava_forward/core/mssqlstore.py` and use them before the locked sections.
* [ ] P2 Unit tests in `src/core/tests/test_mssql_startup_lock.py`: fast path takes no BEGIN; a missing object takes the locked path.
* [ ] P3 Run core tests and mypy, ruff on changed files; changes record with per-criterion table.

## Critique (executed once, 2026-11-23, final candidate)
* Verdict: proceed with narrowed scope. Skipping `_migrate` and `_migrate_recommendations` is correct: they repair data and must stay serialised.
* Risk: a racing first-open sees tables present while another instance is mid-create. Creation is one transaction under the lock, so tables become visible atomically only after commit; the check then sees either none or all of that transaction. Ledger-kind and trigger checks keep the locked path for anything unusual.
* Disposition: apply directly; no user decision needed. No source change to the probe (production setting).
