---
title: Issue 1292 C4 correction details
description: Phase details for the proof rules, history review, projection, adapter recovery, committed outcome, quarantine, bounded work, admission and anchors
ms.date: 2026-11-08
---

## sqlstore.py

* `_proven_later(earlier, later)`: pair proof only when audit positions are both present and ordered, both `seq` values are present (unedited rows) and strictly ordered the same way. `created` is ignored.
* `_unproven_latest(recs, only)`: unchanged shape; used for in-batch rows and for the one-time review.
* `_backfill_zero_ordinals`: group batch rows per employee; for each employee fetch the newest eligible prior row (`ORDER BY created_ord DESC` on `ix_recs_user_ord`, bounded pages of 20, skipping `ai_task` bodies) and its `rec_unres:<id>` flag. The batch latest is flagged when that flag exists or when it is not proven later than every other eligible batch row of the employee. No prior row means no boundary condition. `_prior_for` is removed.
* `_suspect_ranges`: read `rec_order_legacy`, the list `rec_order_backfills` (validated: list of dicts with positive integer `first_ord <= last_ord`; any malformed entry or value returns an all-ordinal range) and one query over `meta` keys `rec_order_batch:%`; coalesce ranges sorted by start. `_review_priority_order` sweeps ordinal-ordered rows once with an index into the coalesced ranges.
* `_create_rec_order_index`: also creates `ix_recs_user_ord (user, created_ord)`; the SQL Server `INDEXES` translation already handles two-column indexes.
* `_anchor_fingerprint`: tuple of (name, sha256 of the bytes or `None` when unreadable); `_audit_evidence` treats an unreadable file as unusable evidence and invalidates on any change.
* `_valid_digests(digests)`: object, integer count at least 1 (not bool), non-empty string head, algorithm absent or `sha256`; used by the full and incremental paths; otherwise `ok=False`, reason "independent digests are malformed".
* `CommittedReloadError(RuntimeError)`: raised by `save` when the post-COMMIT `_sync` exhausts retries; carries `committed=True`; the store state is left to reload on the next call (`_seq=-1`).
* `_drop_unsaved_recommendations`: drop pending `ai_run_end` priority events and `ai_record` events whose detail names a dropped id, nothing else.

## store.py and continuity.py

* `order_view(rec)` (single projection): returns the extra keys for an unresolved newest eligible record (`order_confirmed` False, `actionable` False, `relied_on` False, `order_note`). `_rec_view` and `continuity_export` apply it to every exported record (full and limited bundle; the limited export keeps the four keys).

## mssqlstore.py

* `_Conn.execute("BEGIN IMMEDIATE")`: on any failure run `IF @@TRANCOUNT > 0 ROLLBACK TRAN` on the existing raw connection; if that fails, close and discard the connection; keep `in_tran` False; re-raise the original error.

## api/server.py and web/app.js

* `/api/ai/priority`: catch `CommittedReloadError`, return 409 with `outcome` `committed` and plain text advising a reload.
* `app.js`: the initial priority GET keeps `order_note` for every status and renders it as `p.flag.danger[role=status]` for Proposed, Accepted and Edited; the committed outcome shows the same message with a reload action. Fluent 2, reduced motion, native semantics and non-colour text unchanged.

## tests/sqlguard.py

* `_verify_container(container, host, port, password, inspect, env)`: some binding's `HostIp` must equal the connecting literal address (`localhost` is refused because it is not a literal); IPv4 and IPv6 are not interchangeable. `DOCKER_HOST` set to anything but `unix://` and a `DOCKER_CONTEXT` other than `default` are refused before inspection.
