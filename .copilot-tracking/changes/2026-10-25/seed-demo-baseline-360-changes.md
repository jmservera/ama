# Changes: seed demo baseline merge (issue 360)

Date: 2026-10-25. Phase order actually followed: research (`research/2026-10-25/seed-demo-baseline-360-research.md`), plan and details (`plans/`, `details/`), independent critique (appended to the plan, PASS-WITH-CHANGES, all seven findings accepted), then implementation. No source edit preceded the plan or critique.

## Source
* `src/core/src/zava_forward/core/sqlstore.py`: `SeedMergeError`, `SqlStore.merge_seed` (insert-only, one transaction, audit chain verified against its head before any write, semantic case comparison, document policy with `continuity` preserved, no staff, `as_of` untouched, one `seed_merge` audit entry only when something is inserted, batches of 50, `expect_added` checked before any write). `_seed`, `save` and the schema are unchanged.
* `src/core/src/zava_forward/core/seed_merge.py`: CLI, dry run by default, counts-only JSON, exit 2 (not a SQL store), exit 3 (refused).
* `src/core/README.md`: merge section under Azure SQL store.

## Tests
* `src/core/tests/test_seed_merge.py` (15 tests, SQLite): dry run, insert-only preservation (cases, audit prefix, recommendations, staff, `as_of`), replica visibility, idempotent second apply without audit, semantic compare, collision abort, differing document abort and `continuity` preserved, expect-count mismatch, injected failure rollback then retry, stale head and tampered audit entry refusal, staff never inserted, CLI dry run, apply, mismatch, privacy and non-SQL store.
* `src/api/tests/test_mssqlstore.py`: `MssqlLedgerMigration.test_seed_merge_on_ledger_database` and `..._on_plain_database` (real SQL Server, local-server guard unchanged and applies before any connection).
* Local results: `test_seed_merge` and `test_sqlstore` 33 OK; `MssqlLedgerMigration` plus guard 8 OK against my own throwaway SQL Server container (removed afterwards; the #350 container untouched).

## Rehearsal (throwaway SQL Server, ledger database, one-case shape with two audit rows)
Seed: generator seed 20260901, as-of 2026-10-13, 980 cases (443 open, 38 booked visits), 10 staff, SHA-256 `2d9ca5c4...ba7e1f` (full hash 2d9ca5c45d8bd42f2dc55b98c000d8ebd613c34488fed163606dd1be43ba7e1f), reproduced identically on a second generation. Held privately in `/tmp/ama-360-live/seed/`, not in the repository. The generator emits 10 staff, not the 11 in older documents; the generator output is the authority, and the merge never inserts staff.
* Dry run: to_insert 980, conflicts 0, docs_inserted procurement.
* Apply with `--expect-added 980`: 6.3 s wall time including store open; cases 981, open 444, audit 3 (2 prior plus one `seed_merge`), head count 3.
* Repeat apply `--expect-added 0`: 0 inserted, identical 980, no audit entry.
* Seed `as_of` 2026-10-13 differs from the stored as_of; the merge preserves the stored value and reports both.

## Deviations and limits
* A small scripted edit added the import and exception class to `sqlstore.py`; content was reviewed in the diff.
* Lint, format and type checks run inside the full gate; not run separately.
* Live execution needs coordinator exact-head release, a reviewed image and the existing job route; none is done in this phase.

## Independent review (code-review agent, one record; read-only, tests not run by the reviewer)
Verdict PASS-WITH-FINDINGS, no data-loss or atomicity defect found. Findings and dispositions:
* Medium: the CLI opened the store with the real seed as `ZF_DATA`, so an empty or wrong target would be first-start seeded (staff, as_of) before any guard. Fixed: the CLI now opens the store with an empty private temporary seed and refuses an empty target (exit 2); test `test_cli_refuses_an_empty_target_without_seeding_it`.
* Low: derived queue columns and queue meta are recomputed on apply, and opening runs normal schema checks. Documented in the README; new assertion that every stored column of pre-existing cases is unchanged after apply (passes).
* Low: missing tests for omitted default fields and for output privacy on conflict and mismatch paths. Added `test_seed_case_without_default_fields_matches_stored_case` and `test_cli_outputs_carry_no_case_content_on_any_path` (stdout and stderr).
Re-run after fixes: `test_seed_merge` and `test_sqlstore` 36 OK. The real SQL Server tests were run before these CLI-only changes and do not exercise the CLI.
