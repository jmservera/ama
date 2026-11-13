# Research: issue 80 criterion 2, every list offers a one-way read-only export

* Task: `80-every-list-export-2035`. Branch `feat/demo-80-every-list-export-2035`. Date 2026-11-13.
* Research disposition: executed. Planning Readiness: Ready.

## Issue evidence (`gh issue view 80`)

* Criterion 2 is unmet: "Every list offers an Excel or CSV export; Excel stays one-way read-only".
* 2026-11-05 audit comment: keep scope to remaining authorised list exports plus regression evidence; XLSX is not required where CSV satisfies the criterion. RULE-026/AC-096 forbids exporting individual conversation or memory content; role, row, field and suppression contracts must be preserved.

## Existing exports (before this task)

* `server.py` `LIST_EXPORTS` and `list_rows`: packages, workorders, handoffs, visits, funding, finance, stock queue, checklists, form schemas.
* Dedicated routes: `/api/cases.csv` (ranked home list), `/api/closed-cases.csv`, `/api/handoffs/unaccepted.csv`, `/api/resident/choice-queue.csv`.
* Browser-built file: exception register visible summary (`role-screens.js`).
* Core `list_export.safe_cell` neutralises `=`, `+`, `-`, `@`, tab and CR prefixes. The importer `export.py` writes a values-only workbook with a Read me sheet and history.

## Inventory of lists the workbench reads (`web/*.js` api/get/fetch calls)

* Exported: cases, closed cases, handoffs, unaccepted handoffs, visits, funding, packages, work orders, checklists, finance, stock queue, choice queue, form schemas, exception summary.
* Gaps found: time entries (mine) and time totals (report), law sources list, assistant proposals, aftercare concerns.
* Not row lists or must not leave the application (reason recorded in the test inventory): ai/priority, facets, stats, coordinator, ai/report, finance/exposure, assistants registry, simulation quality, chat and regulatory chat threads (RULE-026), law alerts and search, briefing, time status, me, login, logout, import-check.

## Read-only and write-back evidence

* `store.import_check` is a preview that states "Your file has not been changed".
* Importer `build_preview` of an exported workbook was not refused: the Read me sheet could be previewed as a list. Gap for "refused or preview-only".

## Guard rails read

* `test_content_standard.py`: banned words gate, hold, provenance, trace, snapshot, envelope in audited web files.
* `test_accessibility_baseline.py` pins `aria-invalid`, `h("table"` and `position:fixed` counts; new links are anchors only.
* `test_role_endpoint_inventory.py` pins role behaviour per endpoint.

## Sources not used

No regulatory claim is made; no private dataset read.
