---
title: Issue 135 failed-import producer research
description: Research for a minimal importer producer that turns a refused or rejected synthetic import into a durable exception record
ms.date: 2026-11-09
---

* Task: `import-exception-135` (issue #135, parent #73 integration topic `feat/demo-exception-workflows-73-1109`)
* Base: `a04668ae94b5c2f38e6c55ed789db245e8c71d16`
* Research started 2026-11-09T22:28Z (actual); disposition `executed`.

## Inputs read

* Issue #135 JSON (`ready-demo-issue-135.json`), treated as requirement data: the employee exception view is already delivered by #1257/#1260 (main `38990b19`). It is not duplicated. Named operator and steward authorisations stay an owner boundary.
* `exception_feeds.py`, `exception_queue.py`, `exception_register.py`, `role-screens.js` (renders `failed_import` label, owner, runbook, `eligibility`), `src/importer` (`mapping.py`, `quarantine.py`, `__main__.py`), core README register section, importer README.
* Repository instructions and the demo-capacity common brief.

## Findings

| Id | Finding | Evidence |
| --- | --- | --- |
| R1 | `feed_failed_imports` already turns importer batch dicts (status `rejected`) and refusal dicts (`source_name`, `source_sha256`, `reason`, `at`) into `failed_import` queue items with ref-based idempotency, `Unknown` eligibility and no row values. | `exception_feeds.py:121-173` |
| R2 | No importer code calls it. The register states failed imports are NOT_CONNECTED. | `exception_register.py:24`, issue comment 2026-11-05 |
| R3 | A rejected batch is durable (`import_batches`, SQL-portable, `status='rejected'`, decision note, source hash). A refused file (`WorkbookError` from size, scan, malformed workbook, source changed; or a blocking preview that `stage` refuses) leaves nothing durable. | `quarantine.py`, `mapping.preview_file`, `__main__.py` |
| R4 | `ExceptionQueue` is in-memory and rebuilt on each read; `failed_import` needs a named `data_steward` owner or `_owner` raises. With none configured the register shows `roles_not_named`. | `exception_queue.py:88`, `exception_register.py:80-95` |
| R5 | The api may not import `importer` until #144; `Store.data` is the only record source the register reads. Showing a producer exception on the served screen therefore needs a register/store hook, which is shared integration territory owned by the sibling #132 integrator. | `importer/README.md`, `exception_register.py:112-150` |
| R6 | Role scope: `failed_import` is steward-owned, so a digital-operator-only actor cannot see it. | `OWNER_ROLE` |
| R7 | The importer depends on `zava_forward.core` only; the adapter can use core feeds and queue without new dependencies. | `test_dependency_rule.py` |

## Scope decision (evidence-led)

* Own: importer module `exceptions.py` (durable refusal ledger, producer wrapper, adapter to the core feed, detail view), `stage` and `exceptions` CLI subcommands over a local SQLite file, dedicated tests, importer README, core-free.
* Not edited: `server.py`, `role-screens.js`, `store.py`, `sqlstore`, `exception_register.py`, endpoint inventory, schema. The register hook is a contract proposal for coordinator serialisation.
* Evidence will be component-only and explicitly partial: producer, durable store, restart, adapter to the real core queue item. Not a served path.

## Planning Readiness

`Ready` for a component-level plan. Served-detail continuation is `Blocked` on the shared hook admission.

## Open or unknown

* Owner naming of steward and operator: unknown, owner decision. A configured synthetic owner is the only assignment used.
* Real SQL Server: not exercised; SQL stays portable by construction only.
