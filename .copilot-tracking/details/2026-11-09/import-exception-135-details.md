---
title: Issue 135 failed-import producer phase details
description: Phase details and the proposed shared-hook contract for the importer failed-import producer
ms.date: 2026-11-09
---

## Critique amendments (2026-11-09T22:30Z, supersede conflicting text below)

* Ledger primary key is `ref = file:<sha256 or name>`, matching the unchanged feed; structure is kept in the ledger, not in the queue item.
* Reasons are allowlisted fixed phrases with declared field names only. Rejected-batch notes stay as human-entered originals (limit recorded).
* The `exceptions` CLI is a local diagnostic, reading through `queue.queue(actor)`.
* Integrity errors on insert are caught and the existing row re-read. Fallback hashing only for stable files at or under the size limit.

## Phase 1: ledger and producer

* Table `import_refusals(source_sha256, source_name, structure, reason, refused_at, refused_by, data_label)`, primary key `(structure, source_sha256, source_name)`. SQL is qmark, no upsert; insert only when a select finds no row, so the first reason stays and a repeat is a no-op.
* `RefusalLedger(conn, data_label="synthetic-demo")` with `create_schema`, `record`, `all`.
* `submit_file(store, ledger, path, staged_by, structure)`: blank `staged_by` raises `ImportError_` (user error, not a file refusal). `WorkbookError` or `OSError` from `preview_file`, or a blocking preview, records a refusal and returns `Submission(batch=None, refusal=...)`. Otherwise `store.stage`. The digest comes from the preview, else a streamed read-only hash, else empty.
* Reasons never carry row values: duplicate-key conflict text has the key value removed; reasons are capped at 400 characters.

## Phase 2: adapter and CLI

* `feed_inputs(store, ledger)`: rejected `import_batches` (all structures) and refusals as the dict shapes `feed_failed_imports` reads, sorted deterministically.
* `route(queue, store, ledger, owner)`: owner `None` or blank raises nothing and returns an `unrouted` line with the count and owner `Unassigned (Unknown)`; a configured owner that the queue refuses (`ValueError`) is also reported, not raised. Otherwise `feed_failed_imports`. Returns `Routing(items, unrouted, owner_label, data_label)`; `owner_label` states configured synthetic demo steward.
* CLI `stage FILE --db DB --staged-by NAME [--structure]`: exit 0 staged, 1 refused and recorded, 2 error. CLI `exceptions DB`: opens the file read-only (`mode=ro`), uses the first `data_steward` from `ZF_EXCEPTION_STAFF` via core `staff_from_env`, prints each item and the unrouted lines. No replay, no approval, no network.

## Phase 3: tests (`test_import_exceptions.py`)

* Refused (non-workbook, scanner refusal, too large via patched limit, blocking conflicts) writes one durable row; the source bytes, size and mtime are unchanged.
* Same file refused twice leaves one ledger row and one queue item; feeding the queue twice leaves one item.
* Restart: close the connection, reopen the file database, rebuild a new queue; items equal in kind, ref, source name, hash and reason.
* Rejected batch path (`stage` then `reject`) yields one item with batch id, version, source hash and note; row values absent.
* Item fields: `eligibility` is `Unknown`, `original_source` keeps source name, sha and structure, `owner_role` is `data_steward`, no `recovery`, status `open`.
* Role scope: operator-only actor is refused the item; unnamed actor is denied.
* Unassigned: no owner raises no item, returns the unrouted line, ledger still holds the record.
* No writes on view: database file hash before and after `exceptions`; `total_changes` unchanged for `route`.
* CLI end to end in a subprocess across two processes.

## Phase 4: docs and contract

* Importer README: new capability, boundary and what is not connected.

## Contract (proposed shared hook, not implemented here)

Owner: #132 integrator or coordinator serialisation. Needed only for the served screen.

1. Record source: the register reads `self.data.get("import_exceptions", {"batches": [], "refusals": []})` where both lists use the exact dict shapes `feed_inputs` returns (the shapes `feed_failed_imports` documents). The importer cannot be imported by the api until #144, so the store needs an ingestion path (an owned local adapter or a store method fed from the importer SQLite file) and persistence for that key in `store.py`, `sqlstore` and the schema.
2. Register change in `exception_register.py`: when a steward is named, call `feed_failed_imports(queue, batches, steward, refusals)`; when none is named, append one `unrouted` line with the count (same text as `route` returns) so the item shows as Unassigned, not as healthy. Replace the NOT_CONNECTED source line with a truthful count-based line only after the hook lands.
3. Tests owned by the integrator: register output contains the `failed_import` item for a steward and not for an operator-only viewer; cross-home projection returns source identity and reason only; viewing writes only the existing audit entry.
4. Served evidence (actual SQL and browser) needs the single non-queued shared-heavy-resource admission and is not claimed here.
5. Optional feed extension (core, coordinator decision): carry `structure`, `version` and `data_label` into the refusal `original_source` so the served detail shows the synthetic label; today they live only in the importer ledger and `Routing`.
