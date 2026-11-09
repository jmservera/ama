---
title: Issue 1292 C3 correction research after third independent source review
description: Verification against source of the five High and four Medium findings from the independent review of candidate f8e9ea7da, with the proof model, design conclusions and remaining evidence limits
ms.date: 2026-11-08
---

## Scope and disposition

Correction C3 of task `1292-priority-order-reload`, same worktree and branch (`fix/priority-reload-1292`), head `f8e9ea7da2534600f1cc9932e8a27b5905d56372`, tree `f27ead2e2d0ca578321b34c47d6d22115b296542`. The owner authorized C3 and at most one later C4; this does not authorize production, legacy-data or release decisions. Research disposition: executed (source reading of the review file `review-1292-f8e9-functional/functional-findings.json` and of `sqlstore.py`, `store.py`, `tests/sqlguard.py`, `web/app.js`). No SQL Server, Docker, browser or heavy lock is used. All earlier research, plans, critique, reviews, addenda, failed runs and logs are unchanged. Earlier actual SQL results and the C2 light results describe earlier source and are historical.

## Findings verified against current source

All nine findings are true in the head source.

| No | Severity | Verification |
| --- | --- | --- |
| 1 | High | `_backfill_zero_ordinals` computes `inversions` only between audited rows and merges rest by timestamp; an audited A (10:00) and unaudited B (09:59) are ordered B, A with neither flagged. `latest_priority` then returns A as ordinary. Fully unaudited rows with different timestamps are never flagged. |
| 2 | High | `_contradicted` keeps only `rowversion == 1` rows and accepts equal `seq`; an edited A, an orphan creation event, or a batch tie is treated as proven. An orphan event proves nothing about commit alignment. |
| 3 | High | `_c0_review_pending` is false once `rec_order_batches` or `rec_order_backfills` exists; `_migrate_recommendations` calls `_backfill_zero_ordinals` first, which creates `rec_order_batches`, so the later review is skipped. A C1-migrated database is never reassessed. |
| 4 | High | `_review_c0_backfill` groups by equal created second only; cross-timestamp audit versus ordinal inversions are not visited. |
| 5 | High | The marking is only in `latest_priority`. `resolve_priority` accepts and edits a flagged id; `_rec_view` returns flags without the marking and an already accepted row can show `relied_on` true with `actionable` false. `app.js` disables Accept and Edit from `actionable` but never renders `order_note`. |
| 6 | Medium | `_audit_evidence` returns the cache on an equal head before reading digests; the incremental branch checks daily digests but never `verify_years`. |
| 7 | Medium | `save` runs `BEGIN IMMEDIATE` before the `try`; a failing BEGIN keeps the unsaved recommendation and pending `ai_run_end`, so a later flush or save commits an orphan and a later insertion. |
| 8 | Medium | `require_task_owned_loopback` accepts any caller-written manifest naming a reachable loopback listener and its password; `write_manifest` is public. |
| 9 | Medium | `_flag_unresolved` parses, sorts and rewrites the whole `rec_order_unresolved` list per ambiguous batch; `rec_order_unresolved` parses it per lookup. |

## Proof model (conclusion)

Legacy rows carry no durable transaction-aligned provenance, so no single signal proves relative creation order. Available signals for an earlier row R and a later row L (ordinal order): body `created` (seconds, wall clock, can step back), verified audit position of the creation event (the event can be an orphan; the row can be edited later), and insertion `seq` (valid only for unedited rows that have not been restamped by a backfill; ties are unordered). Order is treated as proven only when at least two independent signals agree and none disagrees. This is a policy of this correction, not a new owner decision: it only decides when a result is shown as confirmed. Where proof is absent, ordinals are not changed and the data owner remains the named decision-maker.

Only the per-employee latest eligible (non `ai_task`) row decides what `latest_priority` returns, so only that row needs a verdict. The latest row is unresolved unless it is proven later than every other eligible row of the same employee in the assessed set. Rows created after the fix are assigned a serialised immutable ordinal at insert and are confirmed by construction; a stale unresolved mark on a row that is no longer the latest has no effect because the marker applies only while the row is the latest.

Consequences for storage: flagging the latest per employee per batch bounds unresolved growth to the employee count per batch instead of all group members; membership is stored as one `meta` row per record (`rec_unres:<id>`, primary-key lookup) and the earlier `rec_order_unresolved` list is copied once into per-record rows under a dedicated versioned marker, never rewritten.

## Design conclusions per finding

* F1, F2, F4: one assessment function used by repair batches and the review; the fallback never states confirmed without two agreeing signals. Mixed and unaudited backward clocks, edited rows, tied seq and orphan events are scenarios.
* F3, F4: a dedicated marker meta key `rec_order_review:3` decides whether the historical review ran, independent of batches. The review runs inside the migration transaction before any new repair, over every positive ordinal (seq is not used because earlier candidates restamped it), flags the per-employee latest when unproven, never rewrites an ordinal, and records a `review` batch.
* F5: `_rec_view` applies unresolved to every priority view when the record is the employee's current latest (`order_confirmed` false, `actionable` false, `relied_on` false, `order_note`). `resolve_priority` refuses accept and edit with `PermissionError` for such a record; reject stays allowed, as does the manual route. The existing priority panel renders the note in a status paragraph; no Fluent token, colour, motion or control change.
* F6: cache validity includes the identity of the independent anchors (digest file listing fingerprint); incremental extension runs the full daily and sealed-year checks; any doubt falls back to full verification.
* F7: `BEGIN IMMEDIATE` moves inside the guarded block with an `opened` flag; failure before the transaction opened quarantines unsaved recommendations and their pending events without a ROLLBACK.
* F8: admission requires verifiable provisioning evidence: a Docker container created for the task, running, labelled `zf.task=1292-sql-disposable`, with the loopback-only port binding equal to `ZF_SQL_PORT` and `MSSQL_SA_PASSWORD` in its environment equal to `ZF_SQL_PASSWORD`, recently created and identified in the manifest by full container id. The check reads container metadata only (`docker inspect`, argument list, no shell) and never connects to the listener; a missing or mismatching container is refused before any connection. The manifest alone is not accepted. Execution against a real container is deferred.
* F9: per-record rows and indexed lookup, with a scale test of repeated ambiguous batches and a lookup-count bound.

## Evidence limits and open decisions

* Actual SQL Server, the ledger-enabled migration, SQL Server scale, the Docker provisioning path, the FULL local gate with verified receipt, independent exact-head review and hosted CI remain pending and unrun.
* The seq signal does not exist for restamped rows, so reviews of C1 and C2 databases flag more employees than a fresh migration would. This is conservative, documented and reversible by the data owner.
* The named data owner decides how flagged records are resolved; no resolution mechanism is added. The rolling-release boundary remains a release decision.
* Overlap: the running #1288 branch also edits `src/core/README.md` and may edit the priority panel. This correction edits the README section "Priority recommendation creation order (#1292)" and `web/app.js` priority panel lines only; ordering and conflict resolution are left to the coordinator.
