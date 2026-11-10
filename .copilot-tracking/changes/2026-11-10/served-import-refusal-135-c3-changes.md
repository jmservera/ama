---
title: Changes, served import refusal projection (#135 C3/5)
ms.date: 2026-11-10
---

* Added `core/import_refusals.py`: bounded Core-shaped projection (`import_exceptions` document) and idempotent `record_import_refusals` on `Store`.
* `core/exception_register.py`: steward branch routes projected refusals through `feed_failed_imports`; a damaged projection becomes unrouted; the sources line is NOT_CONNECTED until a valid projection exists.
* `core/sqlstore.py` `DOCS` gains `import_exceptions` so SQLite keeps it; `core/store.py` adds the mixin.
* `importer/exceptions.py`: `transfer`; `importer/__main__.py`: `transfer DB` command; README updated.
* Tests: importer `TransferTests` and CLI test; API `ImportRefusalRegister` (SQLite), `ImportRefusalRegisterJson` and endpoint test.
* No web, role, permission, model, Bicep or other-issue file touched.

## Divergence

* Implementation was drafted before the research and plan artifacts were written; recorded in the research artifact.
* Browser render check attempted and abandoned (sign-in did not persist in the page); unperformed. Node screen tests still pass.
* SQL Server not run: 16 SQL tests skipped as opt-in loopback SQL.
