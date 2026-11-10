---
title: Issue 135 C3 served import refusal research
description: Research for connecting one durable synthetic refused-file record to the existing exception register
ms.date: 2026-11-10
---

* Continuation C3 of five total. C1 (lint and type) and C2 (importer identity, digest, CLI) are spent; C4 and C5 remain. No reset and no fresh allowance. Research recorded 2026-11-10T03:44Z (actual), disposition `executed`. Original and adverse records of C1 and C2 (worktree `issue-135-import-exception-1109`, protected handoff `handoff-135-c2-import-identity-1109.md`) are preserved and unchanged.
* Worktree `issue-135-served-c3-1110`, branch `feat/demo-served-import-refusal-135-1110`, base `a61bebe6b71e7f33560e2dee74b38834e4f55c0e`, declared target `feat/demo-served-exceptions-73-1110`. The C2 importer component is already in this base (through #1334 and #1341); it is not rebuilt.
* Process note, recorded honestly: reading and a first source draft (new Core module, register hook, importer adapter) began before this artifact was written. The critique and Review below assess that draft, and nothing was validated before the plan and critique existed.

## Inputs read

* Packet `issue135-served-current-1110.json` (issue body and all comments), `demo-next-capacity-1110.md` (last narrow #135 disposition supersedes the earlier budget block), protected C2 handoff, case study original, repository instructions. The addendum and knowledge-base index were scanned only for the exception register; they were not read end to end.
* Code in this worktree: `core/exception_register.py`, `core/exception_feeds.py`, `core/exception_queue.py`, `core/store.py`, `core/sqlstore.py`, `core/factory.py`, `importer/exceptions.py`, `importer/__main__.py`, API route `/api/exceptions` in `api/server.py`, and the existing screen `role-screens.js` (`exceptionRegisterPanel`).

## Findings

| Id | Finding | Evidence |
| --- | --- | --- |
| R1 | `GET /api/exceptions` already calls `Store.exception_register(user, staff_from_env(os.environ))`; the failed-import source is a constant `NOT_CONNECTED` text and no code reads refusals | `server.py:667`, `exception_register.py` |
| R2 | The register builds an ephemeral `ExceptionQueue` per read. Item ids (`EX-nnn`) are positional, so the stable identity is the feed `ref` (`file:<sha256>` or, hashless, `file:<name carrying the opaque identity>`) | `exception_queue.py:94`, `exception_feeds.py:158-174` |
| R3 | `feed_failed_imports(queue, [], owner, refusals)` already keeps source name, digest (None when unknown), reason, time and Unknown eligibility, and is idempotent by ref within a queue | `exception_feeds.py` |
| R4 | JSON `Store` persists the whole `self.data` to `live.json`, so a new top-level key survives restart. `SqlStore` persists only the cases, recommendations and the `DOCS` tuple (meta rows). An unknown key is silently lost on SQL reload, so the key must be listed in `SqlStore.DOCS`. `MssqlStore` inherits `DOCS` but is not exercised here | `store.py:113`, `sqlstore.py` `DOCS`, `_proc_sync`, `_proc_write` |
| R5 | `SqlStore` re-reads `DOCS` on every lock entry, so a second process writing a transfer is visible to a running SQLite-backed server. The JSON `Store` has no reload: a running server would overwrite an external write | `sqlstore.py` `_SyncLock`, `store.py` |
| R6 | The existing screen shows `ref`, the summary and `Reason:` text, owner as configuration-not-appointment, and eligibility. It does not show `original_source.at`, so the refusal time must be in the reason text unless the screen is edited | `role-screens.js` `exceptionHappened`, `exceptionReference` |
| R7 | The API package must not import the importer; the importer may import Core (`test_dependency_rule`). Core already gives the importer `feed_inputs`-shaped data | `importer/tests/test_dependency_rule.py` |
| R8 | A Core-owned reader of the importer SQLite ledger would need a configured path, containment and deployment contract that is not established. It is not chosen | issue packet, capacity note |

## Design decision

* An explicit, bounded Core projection document `import_exceptions` (list of refusals: source name, digest or empty, reason, time) held in the store, added to `SqlStore.DOCS`.
* A Core mixin method `record_import_refusals` that is idempotent by feed ref and keeps the first copy.
* The register reads the projection and feeds it through the existing `feed_failed_imports` for the configured synthetic steward; the source line says connected only when a projection exists, otherwise NOT_CONNECTED. No request supplies a path.
* Importer adds a `transfer(ledger, target)` adapter and a `transfer DB` CLI command that opens the store from the existing `ZF_STORE`, `ZF_DATA`, `ZF_STATE` configuration.
* No web edit: the refusal time is appended to the displayed reason inside the register.

## Out of scope and unproven

* Rejected batches, other failure classes, recovery or replay, real roles, appointments, SQL Server, assistive-technology acceptance, hosted CI.
* Procurement validation, quality receipt, aftercare and concern hooks are not touched or required.

## Planning Readiness

Ready.
