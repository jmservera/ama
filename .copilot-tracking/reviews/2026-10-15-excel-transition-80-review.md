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
