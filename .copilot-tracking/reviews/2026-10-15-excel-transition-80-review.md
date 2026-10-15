---
title: Review for issue 80
description: One-pass review of the Excel transition library
ms.date: 2026-10-15
---

Review executed once. Outcome: library slice conformant to plan; issue not closable.

## Checks

* ADR 0006: new code only in `src/importer`; imports `core` only (dependency-rule test passes); no `mvp/` change.
* Source never modified: opened `rb`, hashed, size and mtime compared; tested with a read-only file.
* Human gate: named approver, different from stager, AI and system refused; rows with problems need explicit acceptance.
* SQL portable: no upsert, identity or PRAGMA; verified by test; real SQL Server evidence pending CI/owner.
* Export: formulas neutralised, history has no provider field.

## Routed findings (later work)

* Build web import and per-list export after #144 (api boundary).
* Owners set thresholds (ADR 0001).
* AI-assisted mapping with approval gate; importer image and limited SQL role; Azure SQL evidence.
* Row-key uses the first declared field; revisit when more structures are declared.

## PR #303 code-review fixes (applied)

* Parsing failures (missing rels part, malformed XML, bad cell reference or shared-string index) become `WorkbookError`; CLI exits 2 with "Cannot import".
* Entity guard hardened (UTF-8 only, case-insensitive), with caps on total uncompressed bytes and sheet count.
* Quarantine: unique (structure, version), conditional decide UPDATE with rowcount check so concurrent approve/reject cannot both succeed, retry then clean failure on duplicate version. Portable SQL kept.
* Evidence: 34 unittest OK, ruff and mypy clean; see the changes artifact.

## PR #303 re-review fix (applied)

* Stage retry is driver-agnostic: injected `integrity_errors` plus matching by DB-API class name `IntegrityError`, so SQL Server (`pyodbc.IntegrityError`) collisions on `UNIQUE (structure, version)` are retried; exhaustion raises a clear `ImportError_`.
* Evidence: 39 unittest OK, ruff and mypy clean; see the changes artifact.
