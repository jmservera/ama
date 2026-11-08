---
title: Issue 1292 C3 correction details
description: Phase details for the order proof, historical review, unresolved storage, server boundary, anchors, BEGIN failure and fixture provisioning
ms.date: 2026-11-08
---

## sqlstore.py

* `_assess(rows, seq_signal)`: rows are dicts of `id, user, created, pos, seq, version, ord`. Group eligible rows by employee, take the highest ordinal as latest L and compare with every other R (ordinal below L). Signals for R before L: timestamp (`created` strictly ordered, equal is no signal), audit (both positions present and evidence ok), seq (`seq_signal` and both `version == 1`, strictly ordered; ties are no signal). A pair is proven when at least two signals agree and none disagrees. Returns the employee latest ids that are not proven. Linear per employee.
* `_backfill_zero_ordinals`: keep ordering rules; replace the ambiguity list by `_assess` over the batch rows with seq signal; drop the global-inversion shortcut; `ambiguous_ids` are the unproven batch latest per employee; the batch also assesses nothing against earlier ordinals (insertion position is their commit order).
* `_review_history()`: when meta `rec_order_review:3` is absent and recommendations with a positive ordinal exist, assess all positive-ordinal rows without seq signal, flag unproven per-employee latest, write one `source=review` batch (`ordinals_changed=False`), set the marker. Runs in the migration transaction before `_backfill_zero_ordinals`. Replaces `_review_c0_backfill` and `_c0_review_pending`; `_rec_order_pending` is true when the marker is absent and rows exist.
* Unresolved storage: `_flag_unresolved(ids)` writes `rec_unres:<id>` rows only; `rec_order_unresolved(id)` reads one key. A one-time copy of the old `rec_order_unresolved` list into per-record rows under marker `rec_unres_index:1` runs in migration; the old key is left untouched.
* `_audit_evidence`: cache key adds the anchor fingerprint (sorted names and sizes and mtimes of digest files); equal head plus equal fingerprint reuses the cache; the incremental branch also runs `verify_years` over the cumulative entries only when year digests exist, otherwise falls back to a full verification; any failure gives `ok=False`.
* `save`: set `opened=False` before; `BEGIN IMMEDIATE` inside the try; mark `opened=True` after it; the handlers call `ROLLBACK` only when `opened` and always `_drop_unsaved_recommendations`.

## store.py

* `_rec_view`: after computing flags, when the record is the employee's current latest eligible row and `rec_order_unresolved(id)` is true, set `order_confirmed=False`, `actionable=False`, `relied_on=False`, `order_note`. `latest_priority` returns the view unchanged.
* `resolve_priority`: before accept or edit, a flagged latest record raises `PermissionError` with the manual-route wording; reject is unchanged.

## web/app.js

* In the proposed-state panel append a `p` with `role="status"` and the `order_note` text when `rec.order_note` exists. No style change.

## tests/sqlguard.py

* `require_task_owned_loopback(env, inspect=None)`: keep loopback, password and manifest checks; additionally require manifest `container` (64-hex id) and verify through `inspect(container)` (default `docker inspect` argument list, no shell, no network): running, label `zf.task=1292-sql-disposable`, a `1433/tcp` binding on host `127.0.0.1` with `HostPort == ZF_SQL_PORT`, `MSSQL_SA_PASSWORD` env equal to `ZF_SQL_PASSWORD`, created within 24 hours, `Id` equal to the manifest. `write_manifest` takes the container id. A refusal happens before any connection.

## Docs and records

* `src/core/README.md` section "Priority recommendation creation order (#1292)" updated for the proof model, review marker, per-record unresolved rows, server boundary and provisioning check.
* C3 changes, one original review and state JSON written after observations.
