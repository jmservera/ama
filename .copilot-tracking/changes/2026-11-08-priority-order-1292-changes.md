---
title: Issue 1292 priority recommendation creation order changes
description: Changes, exact local commands and outcomes, source identities and pending SQL Server evidence for the creation-order fix
ms.date: 2026-11-08
---

## Identities

* Base (main): 6354b13f7abf1441a815e92f2b01dc184ce0b0ac. Branch fix/priority-reload-1292. Research and plan commit 0fbd4058b (before any code or test change). Implementation commit 656bacb56fbf90b89f76b75420e1c19dd593e79f, tree 017bb96e6fc59a4bb73b1eed8733e4118940c59c.
* Blobs at 656bacb56: `sqlstore.py` 50ff4e781fb4452a72fcbdabcb3dba3e39e61d70 (base d790455892b6965cc7506713f14b9315ea2dd641), `mssqlstore.py` 7209533808dd993e28aa1ca7e618b8d47d0532a8, `store.py` a99948569d64b3f0c2e0a34d409a5d810651dd06 (unchanged), `tests/test_priority_order.py` 4258e65f13bf232c9236a848ee03478133d4a961.
* Tools: Python 3.12.3, ruff 0.17.3 (system, not the 0.17.1 project pin), mypy 2.4.0 (project pin, isolated venv `/tmp/ama-1292-scratch/venv`, the only install, task-owned). Core has no runtime dependencies, so no package install was needed for tests. All runs used `PYTHONDONTWRITEBYTECODE=1`, `HOME=/tmp/ama-1292-scratch`, `ZF_DATA=/tmp/ama-1292-scratch/none.json` (absent, so no private data is read) and synthetic fixtures only.

## Changes

* `src/core/src/zava_forward/core/sqlstore.py`: `recommendations.created_ord` column; `_migrate_recommendations` (add column, index, deterministic legacy backfill, `meta.rec_order_legacy`, one new `seq` for backfilled rows and `meta.seq`); ordinal assigned once at insert (current maximum plus one, read once per save under the serialised write); `_sync` reads `ORDER BY created_ord, id`; `_rec_ord` map and `_order_recs()` re-sort the cached list after loads and saves (critique C-1); dialect hooks `_has_rec_order`, `_create_rec_order_index`.
* `src/core/src/zava_forward/core/mssqlstore.py`: DDL column and the two hook overrides.
* `src/core/tests/test_priority_order.py`: 24 test executions (in-memory class 4; SQLite class 10 = 4 inherited + 6 SQL-only; SQL Server class 10, skipped without the opt-in); `src/core/pyproject.toml`: mypy override entry for the new test module, same pattern as `test_resident_decisions`.
* `src/core/README.md`: ordering contract, legacy transition, rolling deployment limit.
* `store.py` (`latest_priority`) is unchanged. No review, approval, consent or ranking rule changed; `test_decision_boundary_unchanged_by_ordering` asserts a proposal stays Proposed with no resolver.

## Commands and outcomes (from `src/core` unless stated)

Common environment `PYTHONDONTWRITEBYTECODE=1 ZF_DATA=/tmp/ama-1292-scratch/none.json HOME=/tmp/ama-1292-scratch`.

1. Reproduction, base source, SQLite (`repro-sqlite.py.txt`): in-memory latest `aaa000000003`, cold reload after edit of oldest `zzz000000001`. Observation, exit 0.
2. Red: `PYTHONPATH=/tmp/ama-1292-scratch/base/src/core/src:tests python3 -m unittest test_priority_order -v` against a `git archive` of base source, final test file. Exit 1. Ran 24, failures 2, errors 3, skipped 10 (log `changes/logs/1292-2026-11-08/red-final.log`). Failing for the stated reason: `test_edit_of_older_proposal_does_not_make_it_newest` (`'zzz000000001' != 'aaa000000003'`, SQLite cold reload after an edit) and `test_interleaved_writer_commit_does_not_displace_the_later_local_proposal` (`'zzz000000001' != 'mmm000000002'`). Three errors are `no such column: created_ord` (fresh, legacy and running-reader cases exercise the new column, so they cannot run on base). The same-`seq` batch case passes on base SQLite because the `ix_recs_seq` index returns rowid order; it is the SQL Server failure (random-id clustered scan from the issue) and has no native red yet (PENDING).
3. Green: `PYTHONPATH=src:tests python3 -m unittest test_priority_order -v`. Exit 0. Ran 24, OK, skipped 10 (all `MssqlPriorityOrder`: "opt-in owned loopback SQL Server", i.e. not run; not a pass) (`green-final.log`). 14 executed (4 in-memory, 10 SQLite), all passing.
4. Original selectors on available engines, each `python3 -m unittest <dotted name>`, exit 0, 1 test OK: `test_resident_decisions.SqlResidentDecisions.test_challenge_source_exact_dependency_manifest_and_original_reviews`, `...SqlResidentDecisions.test_failed_priority_accept_edit_remove_disposition_and_audit` (SQLite), and the two `JsonResidentDecisions` counterparts. The two `MssqlResidentControls` selectors ran as skipped (1 skipped each, exit 0): PENDING native SQL Server.
5. Related suites: `python3 -m unittest test_resident_decisions test_sqlstore test_sqlreads test_sqlqueues test_seed_merge test_taskqueues test_recovery test_priority_order`. Exit 0, Ran 384, OK, skipped 103 (opt-in SQL Server, Azure and scale cases; none claimed as passes) (`related.log`). An earlier launch of this command was stopped by me after I briefly stashed `src` to run a lint comparison; it was discarded and rerun cleanly.
6. API: from `src/api`, `PYTHONPATH=../core/tests:../agents/tests:../core/src:../agents/src:src python3 -m unittest discover -s tests -p test_mssqlstore.py -q`. Exit 0, Ran 226, OK, skipped 217 (opt-in). A first attempt with a different `PYTHONPATH` order failed on test-module name collision (`test_buildings`), preserved as a wrong command, not a code failure.
7. Lint and types: `ruff check tests/test_priority_order.py` and `ruff format --check` pass; `ruff check` on `sqlstore.py` and `mssqlstore.py` pass (per-file ignores apply); project `mypy` (`MYPYPATH=src:tests mypy`, config `strict`, `files = ["src","tests"]`) 270 files, no issues. First mypy attempt failed for 8 untyped-call errors before the pyproject override was added; kept as history.
8. `git diff --check` clean. No file outside the repository changed except `/tmp/ama-1292-scratch`.

## Acceptance status at the local frozen candidate

* [x] Ordering contract defined and implemented (immutable ordinal, ordered cold reload, cache re-sort); SQLite and in-memory parity executed. SQL Server execution PENDING.
* [x] Same-second batch, edit of older proposal, interleaved writer, multiple users plus `ai_task`, legacy backfill and running reader covered on SQLite; the legacy transition is documented in README and `meta.rec_order_legacy`.
* [ ] Native SQL Server red and green with zero skips, including the two original `MssqlResidentControls` selectors: PENDING coordinator admission to `/tmp/ama-rpi-heavy.lock` (not started by this task).
* [x] Review and approval boundary unchanged.
* [ ] PR: not opened (coordinator publishes).

## Open items and uncertainties

* SQL Server T-SQL paths (column add, index, backfill, ledger variant) are reviewed by reading only; unproven until the native run. The ledger-enabled database variant is not exercised even then unless the native database is ledger-enabled.
* Legacy ordering is a documented heuristic. A named data owner decides whether a live database needs review of same-second or edited legacy rows.
* Older writers after migration insert ordinal 0 until the next start of the new binary.
* The complete local gate and `rpi-checks.py --changed` were not run (heavy-lock rule).
