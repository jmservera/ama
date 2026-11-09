---
title: Issue 1292 priority recommendation creation order research
description: Research for preserving the newest priority recommendation after SQL reload, covering creation order versus mutable seq, ties, edits, cold and incremental reload, legacy rows and migration
ms.date: 2026-11-08
---

## Scope and disposition

Task `1292-priority-order-reload`, worktree `/home/azureuser/source/ama-wt/issue-1292-priority-order`, branch `fix/priority-reload-1292`, PR target `main`, base `6354b13f7abf1441a815e92f2b01dc184ce0b0ac`. Research disposition: executed (source reading plus one throwaway SQLite reproduction under `/tmp/ama-1292-scratch`, synthetic data only). Planning Readiness: Ready, with one named legacy-data limitation (see Legacy rows).

Read first: `docs/case_study_48_original.md` (Stock Prioritisation Agent L2 recommend, line 27), `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md` (context only, not evidence), `src/core/README.md`. Requirement anchors: original case-study L2 recommend and draft PRD PR-007 (AI recommendation, human review, no consequential ranking change, `docs/prds/proper-warm-retrofit-programme-demonstrator.md` line 367). The issue is a data-ordering defect; it changes no ranking policy, approval or consent rule.

## Source identities (blob at base 6354b13f)

* `src/core/src/zava_forward/core/sqlstore.py`: `_sync` lines 549-576 (recommendations load), `save` insert/update lines 703-717, schema `recommendations` lines 72-75, migration hooks `_migrate` / `_migrate_queues` lines 286-326, init order lines 172-175. Issue pin: blob `d790455892b6965cc7506713f14b9315ea2dd641`.
* `src/core/src/zava_forward/core/store.py`: `latest_priority` lines 1021-1024 (`mine[-1]` of the in-memory list filtered by `user` and `kind != "ai_task"`); creation `publish` appends to `self.data["recommendations"]` with `created` at second resolution (line ~965). Issue pin: blob `a99948569d64b3f0c2e0a34d409a5d810651dd06`.
* `src/core/src/zava_forward/core/mssqlstore.py`: DDL `TABLES["recommendations"]` line 45, `_rewrite` of `user`, `_add_column_default`, `_create_schema_serialized`, `_create_indexes`. Writes take `sp_getapplock zavaforward_write` exclusive inside `BEGIN IMMEDIATE`.

## Findings

* The in-memory (`Store`) definition of "newest" is list append order. Recommendations are only ever appended (publish) and mutated in place (resolve, quarantine, AI task), never reordered. This is the semantics SQL must reproduce.
* `recommendations` rows have `id` (random 12 hex), `rowversion`, `seq`, `user`, `body`. `seq` is the global write counter in `meta`; every `save` that changes a row sets `seq = cur + 1`. Insert and every later update both write it, so `seq` records the last write, not creation.
* `_sync` runs `SELECT id, rowversion, body FROM recommendations WHERE seq > ?` with no `ORDER BY` and appends unseen rows to the list in the order returned. Updated known rows keep their list position (`old[1].update`).
* Observed ordering by engine (reproduction below and issue evidence): SQL Server returns the clustered primary-key scan, so ties on `seq` follow random `id` order (issue: 13/13 failures followed ID order, cached plan is a clustered PK scan). SQLite uses `ix_recs_seq`, so a cold reload returns `seq` order with rowid tie-break, which hides the defect for creation-only data but exposes it after edits.
* Same-second or same-transaction creations: `created` is `datetime.now().isoformat(timespec="seconds")`; several rows saved in one transaction share one `seq`. Neither `created` nor `seq` can order them. Only the in-memory list position, which is the insertion order inside the save loop, carries creation order.
* Updates: editing an older proposal gives it a higher `seq`. With any `ORDER BY seq` rule it becomes the newest on reload. `ORDER BY seq` alone therefore changes the visible recommendation after accept, edit or reject of an older proposal (the user-visible bug on SQLite). It is not a fix.
* Cold versus incremental reload: cold reload loads all rows with `seq > 0`; incremental reload loads only rows touched since `self._seq`, which can mix brand-new rows with updated old rows. New rows are appended after existing ones, so a creation-ordered query over the changed rows keeps newest-last only if new rows are ordered among themselves by creation. Updated rows must not move.
* Multiple users: `latest_priority` filters by `user` and excludes `ai_task`, so a single global creation ordinal is sufficient; no per-user counter is needed and the existing filters stay in place. `ai_task` rows share the table and the ordinal.
* Concurrency: SQL writes are serialised (SQLite `BEGIN IMMEDIATE`, MSSQL application lock), so `MAX(ordinal)+1` computed in the insert is race-free across processes. Each pending recommendation in one `save` is inserted in list order, so a batch gets consecutive ordinals in creation order.
* Other readers: `continuity.py` line 270 and `resident_decisions.py` line 313 read bodies by id or unordered for scanning; neither depends on order. No other writer inserts into `recommendations` (grep over `src/` at the base).

## Reproduction (SQLite, synthetic, throwaway script, not committed)

`PYTHONPATH=src/core/src:src/core/tests python3 /tmp/ama-1292-scratch/repro.py` with ids patched to `zzz...`, `mmm...`, `aaa...` created in that order for one synthetic user, then `resolve_priority(accept)` on the oldest:

* created in order `zzz000000001, mmm000000002, aaa000000003`; in-memory and cold reload latest `aaa000000003` (correct before the edit);
* after the edit of the oldest: in-memory latest `aaa000000003`, cold reload latest `zzz000000001` (wrong; `seq` of oldest is now 5);
* SQLite plan for the `_sync` query: `SEARCH recommendations USING INDEX ix_recs_seq (seq>?)`.

On SQL Server the same reload also fails without any edit when ids sort against creation order (issue evidence; to be reproduced natively when the heavy lock is admitted).

## Options considered

* `ORDER BY seq, id`: rejected. Mutable, reorders after edits, ties by random id.
* `ORDER BY json created, id`: rejected. Second resolution, string from body, ties by random id, and a body timestamp is editable data.
* Add sub-second `created`: rejected. Changes recommendation shape and views, does not recover legacy rows, still not durable against clock steps.
* SQL Server `IDENTITY` or SQLite `AUTOINCREMENT` column: rejected. The two dialects differ, an IDENTITY column cannot be added to an existing table, and insert order across one `save` loop would depend on engine behaviour.
* Ordinal stored in `body`: rejected. Would be copied into views and exports and can be rewritten with body updates.
* Chosen: a dedicated immutable column `created_ord BIGINT NOT NULL DEFAULT 0`, assigned once at insert as `COALESCE(MAX(created_ord),0)+1` inside the serialised write, never updated, with index and `ORDER BY created_ord, id` on load. It is dialect neutral (`BIGINT` is valid in SQLite), small, additive and backwards compatible (older readers ignore the column).

## Legacy rows and migration

* Existing databases have no creation order. What is recoverable: body `created` (seconds), `seq` (last write, so biased towards later edits) and `id` (random). The original same-second order of rows that share a `created` value and the original order of rows edited after creation cannot be recovered.
* Transition: when the column is added, or whenever rows with `created_ord = 0` exist (for example written by an older binary during a rolling deployment), backfill ordinals after the current maximum in the order `created`, `seq`, `id`. This is deterministic and honest best effort. The first backfill records the number of legacy rows and of rows in same-second groups in `meta` key `rec_order_legacy` so the ambiguity is queryable. No data is invented: ordinals are derived only from existing fields, bodies and `seq` are untouched.
* Rolling deployment limit: an older binary running after migration inserts `created_ord = 0`; those rows sort first until the new binary next starts and backfills them. Deployment should stop old writers before the new binary serves; recorded as a limitation, not engineered around.
* Decision for a named human or database owner (not blocking this fix): whether any legacy same-second or edited-before-reload ambiguity on the live SQL database needs manual review. This task runs only on synthetic data and does not touch any live or private database.

## Test and environment observations

* `zava_forward` is not installed for system Python. Core has no runtime dependencies (`dependencies = []`), so selected tests run with `PYTHONPATH=src/core/src:src/core/tests`; no install is needed. `ruff` and `mypy` exist in `~/.local/bin` (versions recorded in the changes record, not the project pins).
* The shared lock `/tmp/ama-rpi-heavy.lock` exists and #184 has first admission. SQL Server, Docker, browser and image work are not started by this task; the MSSQL regression is written but its execution is PENDING coordinator admission.
* Existing MSSQL harness: `MssqlResidentControls` (opt-in `ZF_RESIDENT_MSSQL=1`, creates `zf_resident88_<uuid>` per test, drops it on cleanup). The new regression reuses the same opt-in and the same per-test fresh-database pattern.

## Risks and unknowns

* The old-behaviour SQL Server failure is unreproduced locally; it relies on issue evidence until the admitted run.
* The legacy backfill order is a heuristic; documented, not proven to equal original order.
* Mutating the recommendations schema on a ledger-enabled database: `recommendations` is not a ledger table (only `audit`), and `_add_column_default` already handles ledger tables, so no new branch is needed.

## Conclusions

Fix `SqlStore` only: add an immutable creation ordinal with migration and ordered reload. `Store.latest_priority` and every review, approval, consent and ranking rule stay unchanged.
