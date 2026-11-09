<!-- markdownlint-disable-file -->
# Review: issue 1292 recovery validation (2026-11-09)

**Executed**: once, by the implementing agent (not independent). Boundary: whole candidate vs origin/main `b46a9ad9a`, demo-targeted tier. Source and base: see the state file. Original independent C2/C4 "Revise" findings are preserved and not superseded by this self-review.

## Commands (worktree `.venv`, `src/core`, `PYTHONPATH=../agents/tests:tests`)

| Check | Result |
| --- | --- |
| `unittest discover -s tests -p test_priority_order.py`, SQLite/memory | 93 run, OK, 19 skipped (MSSQL class, opt-in) |
| Same module with `ZF_RESIDENT_MSSQL=1` on owned SQL Server 2022 | 93 run, OK, 0 skipped (181 s) |
| `test_resident_decisions` SQLite | 256 run, OK, 93 skipped (MSSQL opt-in) |
| `test_resident_decisions` with MSSQL | 256 run, 1 failure, 3 skips; failure pre-existing and identical on origin/main (see research) |
| Two originally failing resident tests, 10 fresh-database runs each batch | base (origin/main) 7/10 runs failing; head 0/10 |
| Adjacent: sqlstore, sqlreads, sqlqueues, recovery, form/list export, ranking, challenges, taskqueues, ai_consumption, cutover_audit, data_protection (SQLite) | 210 run, OK |
| `src/api` discover (`../core/tests:../agents/tests`) | 1994 run, 7 errors (unrelated module import errors in browser/acceptance scripts, as C4 noted), 365 skips |
| `ruff check src/core src/api`; `ruff format --check`; `mypy src` (core) | clean; 95 files formatted; 128 files no issues |

## Findings

* No new defect in the candidate. Actual SQL Server now passes the creation-order, cold/incremental reload, BEGIN-recovery, export and ledger-fixture tests in the module.
* Open and not claimed: the single MSSQL resident fixture failure (pre-existing, unrelated, needs a separate fix); API-suite import errors; SQL scale, ledger-enabled migration, the data-owner resolution mechanism, rolling-release fence, the full gate, independent review and hosted CI.
* Outcome: conformant for the demo-targeted tier with the open items above; the MSSQL resident failure is not waived.
