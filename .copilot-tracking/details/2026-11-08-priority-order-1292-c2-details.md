---
title: Issue 1292 C2 correction details
description: Phase details for the reader protocol, queue sync, audit evidence, unresolved state, batch records, C0 review and fixture manifest
ms.date: 2026-11-08
---

## sqlstore.py

* `_sync`: loop up to a small bound. Read `seq` (s1), return when unchanged and loaded. Fetch changed cases and recommendations into locals, read `seq` (s2); on mismatch retry. If any fetched `created_ord` is 0, call `_repair_zero_ordinals()` (own `BEGIN IMMEDIATE`, re-checks under the lock, bumps `meta.seq`) and retry. Only then apply to the cache and publish `_seq`. Exhaustion raises.
* `_queue_candidates`: call `_sync` before the transaction; inside `BEGIN IMMEDIATE` compare `meta.seq` with `_seq`, rollback and retry (bounded) when different. Remove the thread-local `writing` flag and the `in_transaction` parameter.
* `_audit_evidence()`: returns a dict (`ok`, `anchored`, `reason`, `positions` by recommendation id, `count`, `head`, `last_seq`). Reads `audit_head` first; reuses a cached result for the same head; extends incrementally from the cached head when entries were appended; otherwise a full verify with `ledger.read_digests` and `ledger.verify_years` against `read_year_digests`. Digest mismatch, unreadable digest or broken chain gives `ok=False`. Called outside the writer section where possible; under the lock only the delta is verified.
* `_backfill_zero_ordinals(seq)`: for rows with `created_ord = 0` build keys with audit position first when the row is audited and not contradicted by `seq` (unedited rows: `rowversion = 1` and an earlier audit position must not have a later insertion `seq`); unaudited rows are merged by `(created, seq, id)` into the audited sequence by timestamp. Ambiguity is computed per employee, non-`ai_task`, same created second, for rows without proof, and for every unaudited row when audited rows show a timestamp inversion. Writes ordinals through `executemany`, merges unresolved ids into `meta.rec_order_unresolved`, writes one `rec_order_batch:<n>` key with counts and the evidence description (`proven`, `audit_supported`, `heuristic`, `anchored`, `audit_chain`, `order` text matching the code) and bumps `rec_order_batches`. `rec_order_legacy` and any existing `rec_order_backfills` are left untouched.
* `_review_c0_backfill()` in migration: when `rec_order_legacy` exists and no `rec_order_batches` or `rec_order_backfills` key exists, review rows with ordinal `<= rows`: add unresolved ids for same-employee same-second groups not proven by audit in their current order; ordinals untouched; one `source=c0-review` batch.
* `_initialize`: assign `digest_dir` before `_migrate_recommendations`.
* `save`: in the non-conflict rollback branch drop unsaved recommendations and pending events naming them (`_drop_unsaved_recommendations`).
* `rec_order_unresolved(rec_id)` override reading meta each call.

## store.py

* `Store.rec_order_unresolved(rec_id)` default `False`. `latest_priority` adds `order_confirmed=False`, `order_note` and `actionable=False` to the returned view only when the newest eligible record is unresolved. No other path or filter changes.

## tests

* `tests/sqlguard.py`: manifest-based admission plus `write_manifest` for the admitted setup; the two SQL fixtures call it first.
* `tests/test_priority_order.py`: new classes for barriers, queue rollback, clock reversal, unresolved API view, orphan event, digest rechain, C0-opened database, bounded audit work and guard negatives. SQLite-only cases stay out of the SQL Server subclass; SQL execution remains pending.

## Boundaries preserved

Employee and `ai_task` filters, human review and approval, resident consent and ranking policy are unchanged. Bodies are never rewritten and no historical ordinal is silently reordered. Synthetic data only; no cloud, model, private data or SQL Server.
