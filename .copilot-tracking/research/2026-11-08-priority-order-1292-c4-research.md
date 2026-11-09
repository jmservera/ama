---
title: Issue 1292 C4 correction research after fourth independent source review
description: Verification against source of the thirteen findings (4 High, 9 Medium) from the independent review of candidate dd8c71ca0, with the revised proof model and remaining evidence limits
ms.date: 2026-11-08
---

## Scope and disposition

Correction C4 of task `1292-priority-order-reload`, same worktree and branch (`fix/priority-reload-1292`), head `dd8c71ca04e793b3c953c32d13e6ebbd5e90fc6d`, tree `ec90d255fd3e351d6645680f82cb397363a53522`. C4 is the final correction currently authorized; it authorizes no production, legacy-data or release decision. Research disposition: executed (source reading of `review-1292-dd8c-c3-functional/functional-findings.json` and of `sqlstore.py`, `store.py`, `continuity.py`, `mssqlstore.py`, `ai_tasks.py`, `ledger.py`, `tests/sqlguard.py`, `web/app.js`). Only light SQLite, fake-adapter and static tests are used; no SQL Server, Docker, browser, full gate or heavy lock. All earlier research, plans, critique, reviews, addenda, failed runs, logs and SQL results are unchanged and describe earlier source.

## Findings verified against current source

All thirteen findings are true in the head source.

| No | Severity | Verification |
| --- | --- | --- |
| 1 | High | `_proven_later` accepts `audit > 0 and (seq > 0 or (clock > 0 and seq >= 0))`. A tied or absent `seq` plus a strictly later `created` and a verified audit position is proven, although an orphan creation event and a wall clock are both independent of the commit. An edited older row has `seq=None`, so an orphan A, committed B, later insertion and edit of A reads as A before B. |
| 2 | High | `_suspect_ranges` reads `rec_order_legacy` and `rec_order_batch:<n>` only. The C1 candidate wrote the JSON list `rec_order_backfills` (entries with `first_ord`, `last_ord`; commit `6fcf8368a`), which is never read, and `rec_order_review` marks the database reviewed with empty ranges. The C3 fixture runs current code, so it creates current keys, not C1 shape. |
| 3 | High | `_rec_view` is the only place that applies the unresolved projection; `continuity_export` copies raw recommendations and `_export_record` recomputes `actionable` and `relied_on` without `_order_unresolved`. |
| 4 | High | `_Conn.execute("BEGIN IMMEDIATE")` runs `BEGIN TRAN; ...sp_getapplock...; THROW` in one batch with autocommit on and `XACT_ABORT` off. A lock timeout `THROW`s after `BEGIN TRAN`, leaving `@@TRANCOUNT` 1 while `in_tran` stays False; the C3 handler only drops records. A real server run is needed to observe it. |
| 5 | Medium | `_prior_for` gives every prior row `seq=None`, so a singleton zero row repaired after native rows can never be proven even though the writer fence orders it after them. |
| 6 | Medium | `_sync` raises `RuntimeError("Reload could not settle ...; retry.")` after COMMIT in `save` (`else: self._sync()`); the server returns generic 500 and the panel offers a retry that creates a second proposal. |
| 7 | Medium | `app.js` renders `order_note` only in the Proposed branch and the first GET discards other statuses. |
| 8 | Medium | `_verify_container` checks that some binding publishes `ZF_SQL_PORT` on some loopback address, not that the binding's `HostIp` equals the connecting host; a remote Docker context is not refused. |
| 9 | Medium | `_drop_unsaved_recommendations` filters `ai_run_end` events only; `ai_tasks.add_record` queues an `ai_record` event (`<task> <id> mode=...`) before `save`. |
| 10 | Medium | `_prior_for` decodes every earlier row of every touched employee per repair: 1+2+...+N rows. |
| 11 | Medium | `_review_priority_order` tests each row against every range with `any(...)` and reads one meta row per batch. |
| 12 | Medium | `_anchor_fingerprint` uses name, size and mtime only; readability and content are not part of the key. |
| 13 | Medium | `ledger.read_digests` returns raw JSON; `verify_entries` defaults a missing `count` to 0, so `{}` passes and a list raises `AttributeError`. |

## Revised proof model (conclusion)

* Within one repair batch (rows that all had no ordinal when the writer lock was taken), a pair is proven only when both rows are unedited (`rowversion == 1`, so the insertion `seq` is intact), the `seq` values differ and agree with a verified audit position. A wall clock never proves anything and a tied `seq`, an edit, an orphan or a missing event leaves the pair unproven. A backward clock step still confirms when `seq` and the audit position agree.
* Across the cutover boundary, ordering is established by the writer fence, not by a signal: every save repairs all zero rows inside its own write transaction before it assigns an ordinal (`save` calls `_backfill_zero_ordinals` before the first insert), and `_sync` repairs before it serves. A zero row found by a repair therefore committed after every row that already had an ordinal when the repair began. A batch row is proven later than every prior row whenever the employee's previous newest eligible record is itself not flagged (the `rec_unres:<id>` row is absent). This replaces the full-history rescan with one indexed lookup and a primary-key read per employee.
* Invariant: an employee's newest eligible record without a `rec_unres` row is provably later than that employee's other eligible records. The one-time review establishes it for existing databases; native inserts and repairs maintain it.
* Where proof is absent, ordinals are not changed, the newest record is flagged and the named data owner remains the decision-maker. No resolution mechanism or owner policy is invented.

## Design conclusions

* F2: read `rec_order_backfills` (list of objects with integer `first_ord` and `last_ord`) as well as C0 and current keys; any malformed value yields an all-ordinal suspect range (conservative).
* F11: read all `rec_order_batch:%` rows in one query, coalesce ranges, sweep once over ordinal-ordered rows.
* F10: add `ix_recs_user_ord (user, created_ord)` and look up only the newest eligible prior row per touched employee in bounded pages.
* F3/F7: one shared projection (`order_view`) used by `_rec_view` and the continuity export for both full and limited bundles.
* F4: the adapter abandons a partially opened transaction (rolls it back, or discards the connection if that fails) and re-raises the original error; the SQLite path never rolls back an unopened transaction. Real timeout, `@@TRANCOUNT` and cross-connection evidence need a separately admitted SQL run.
* F6: a distinct `CommittedReloadError` after COMMIT; the priority endpoint and panel report a committed outcome and ask for a reload rather than a retry.
* F9: quarantine any pending creation event naming a dropped record (`ai_run_end` priority and `ai_record`).
* F8: bind admission to the connecting host (exact `HostIp` match, IPv4 versus IPv6 distinct, no name resolution) and refuse a remote Docker engine (`DOCKER_HOST` not a local unix socket, `DOCKER_CONTEXT` set to other than `default`, TLS or SSH) before any connection.
* F12/F13: fingerprint includes a content digest and an unreadable marker; digest shapes are validated (object, integer `count` at least 1, non-empty string `head`, optional `algorithm` equal to sha256) before verification; any invalid anchor makes the evidence unusable.

## Evidence limits

SQL Server behaviour (lock timeout, `@@TRANCOUNT`, cross-connection visibility, scale), the real Docker and listener binding, the ledger-enabled migration, the full gate and receipt, independent review, hosted CI and current-base integration with #184 and #1288 are not exercised here. The #1288 branch also edits `src/core/README.md` and the priority UI; the coordinator owns ordering and conflict resolution.
