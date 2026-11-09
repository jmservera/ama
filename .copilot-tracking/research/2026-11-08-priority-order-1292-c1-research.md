---
title: Issue 1292 C1 correction research after independent source review
description: Verification against source of the two High and three Medium findings from the independent review of candidate 16375e3ca, with the evidence and limits for each correction
ms.date: 2026-11-08
---

## Scope and disposition

Correction C1 of task `1292-priority-order-reload`, same worktree and branch (`fix/priority-reload-1292`), head `641c11ffd26d03549e1e174179efc8b01b8e3544`, tree `7faf00ae6d96f548b8cda1802fd5b2b3decbafb6`, product source unchanged from reviewed `16375e3ca`. Research disposition: executed (source reading only; no SQL Server, Docker or shared heavy lock). The original research, plan, critique, review, SQL logs and addenda are unchanged and remain the historical record. The earlier native SQL red/green results describe the pre-correction source and are historical, not validation of C1.

Input: the independent functional review `functional-findings.json` (verdict request_changes, 2 High, 3 Medium). Each claim was checked against the actual source at this head. None of the review's claims were taken from its summary alone.

## Verification of findings

* F1 (High, confirmed). `_migrate_recommendations` runs only inside `_initialize` (`sqlstore.py` 165-176). `created_ord` defaults to 0, so any pre-fix writer that inserts after that scan leaves a zero ordinal. `_sync` selects `ORDER BY created_ord, id` and never inspects zeros, so the zero row sorts first and `latest_priority` (last eligible row) returns an older recommendation. A later new-binary `save` allocates `MAX(created_ord)+1`, and the next startup backfills the zero row after it, so the older-binary row ends up permanently after a newer row. Stopping old writers after startup does not help. Both writers use the same exclusive write section (SQLite `BEGIN IMMEDIATE`, SQL Server `sp_getapplock zavaforward_write`), so a fence taken inside that section is cross-process.
* F2 (High, confirmed). The legacy sort key is `(body.created, seq, id)`. For A then B in one second, editing A gives A a higher `seq` than B, so B sorts first and A is selected. Creation writes `ai_run_end ... priority_recommendation <id>` through `self.audit` before `self.save()` (`store.py` 985-986), and `save` appends pending audit entries in the same transaction with an increasing `audit.seq` (`sqlstore.py` `_append_audit`). The chained hashes (`ledger.verify_entries`, already used by `merge_seed`) show whether that evidence is intact. Limits: only AI priority proposals created through `ai_priority` write this event; rows created by other paths, rows whose audit was lost, and overlapping creations (object creation versus commit order) have no trustworthy event, so they remain ambiguous.
* F3 (Medium, confirmed). `rec_order_legacy` is written only when `start == 0` (no positive ordinal). A rollback batch (new DB, positive ordinals, old binary writes zeros) is backfilled with no record, and an existing record is neither extended nor identifiable.
* F4 (Medium, confirmed). `seconds.count(c)` inside a loop over `set(seconds)` is quadratic in the number of distinct timestamps, and one `UPDATE` is issued per row, all inside the global writer lock. A three-row fixture cannot show this.
* F5 (Medium, confirmed, with an out-of-scope observation also confirmed). `MssqlPriorityOrder.setUp` and the pre-existing `MssqlResidentControls.setUp` (`test_resident_decisions.py` 4154-4170) connect to `master` and run `CREATE DATABASE` and `DROP DATABASE` using whatever `ZF_SQL_*` is inherited, with no loopback check.

## Design findings

* A fence must not rely on startup. The invariant to enforce is: no new-binary read serves, and no new-binary insert allocates, while a zero ordinal exists. Cheap check: an indexed `WHERE created_ord = 0` probe only when `_sync` actually has new sequence data (an old writer always bumps `meta.seq`, so a mixed-version insert is always followed by a sync).
* Zero rows are repaired, never guessed in the reader: `_sync` runs the repair under the writer lock (nested use inside an existing write transaction must not start a second transaction), and `save` repairs before allocating the first new ordinal in its own transaction. If repair cannot run, the read raises, so a wrong newest recommendation is never served (fail closed).
* Repair places an old-writer insert after every positive ordinal. This is correct for the cutover and rollback windows because old and new writers serialise on the same write lock, so a zero row committed before a later new write is repaired before that write receives its ordinal.
* The unresolvable residue is the same as before: same-second rows with no verified audit evidence. They stay recorded for the named data owner; nothing is invented.
* Audit-derived order key for repaired rows: `(created, audited-first, audit seq or seq, id)`. A same-second group is recovered only when every member has a verified audit event; otherwise the whole group is recorded as ambiguous with row identifiers.
* Metadata: keep `rec_order_legacy` exactly as the first-batch record (compatibility, nothing discarded) and add an append-only `rec_order_backfills` JSON list, one entry per batch, with row counts, method counts, same-second group count, ordinal range and a bounded list of ambiguous ids.
* Cost: one `Counter` pass, `executemany` updates, and the audit read and chain verification only when zero rows exist.

## Evidence limits

* SQL Server behaviour (including the ledger-enabled table path and large-table timing there) is unproven and needs a separately admitted run. The SQLite and in-memory results are the only evidence from this correction.
* The audit trail is evidence only when the chain verifies against `audit_head`; a broken chain falls back to the previous heuristic and records that fact.
* A named data owner must still decide whether any live database with recorded ambiguity needs manual review. No approval is claimed.
