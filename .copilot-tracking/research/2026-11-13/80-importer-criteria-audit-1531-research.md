<!-- markdownlint-disable-file -->
# Research: Issue #80 importer and export criteria audit (2026-11-13)

Task: `80-importer-criteria-audit-1531`. Pinned source `34b11967b93df40b653d384ab3b136bb1fb842f9` (worktree HEAD, branch `docs/demo-80-importer-criteria-audit-1531`). Research disposition: executed. Planning Readiness: Ready.

## Literal criteria (`gh issue view 80`, read 2026-11-13)

* C1 (ticked): Import shows mapping, conflicts and a row-level preview and never changes the source file.
* C2 (unticked): Every list offers an Excel or CSV export; Excel stays one-way read-only.
* C3 (ticked): Export retains version, source, approval and supersession history independently of the AI provider.
* C4 (unticked): Owners set the staged transition thresholds (ADR 0001 open item).

## Findings

* Importer module (`src/importer/src/zava_forward/importer/`): `mapping.py` (column match, conflicts, per-row preview with lineage, source hashed and never opened for writing), `quarantine.py` (stage, human approve/reject, supersession history), `export.py` (CSV, read-only XLSX with Read me and History sheets, read-only compare), `exceptions.py` (refusal ledger).
* API: `LIST_EXPORTS` at `server.py:178-179`; further CSV routes for cases, closed cases, unaccepted handoffs and resident choice queue. Web controls located by literal search: `app.js:764,765,875,2280,2290`, `ops.js:246,490,494`, `panels.js:575`, `progress.js:189`, `role-screens.js:225,701,1489`; exception register summary is a browser-built four-column CSV (`role-screens.js:907-948`).
* The API serves CSV only. `to_xlsx` is not referenced from `src/api` or other projects; README (`src/importer/README.md`, "Not built" paragraph) states the HTTP or web surface for import and the export buttons on every list are not built.
* The only import screen is `app.js:1756-1774`: CSV text posted to `/api/import-check`; it shows column mapping, ready count and rows to fix, not every row or lineage, and does not use the workbook importer.
* No canonical enumeration of "every list" exists; GET list endpoints without a CSV route include `/api/assistants/proposals`, `/api/aftercare`, `/api/law/alerts`, `/api/time/report` and others (server.py path dispatch). Whether each is a "list" in scope is an owner interpretation.
* ADR 0001 `docs/adrs/0001-azure-architecture.md:216` says "proposed, thresholds to be set by owners"; stage table exit criteria at lines 218-223 hold unset targets ("owner-set targets for N consecutive cycles").
* Prior audit `.copilot-tracking/audits/2026-11-10/issue-80-qualified-audit-1110-supplement.md` predates the Capacity, handoff and exception CSV merges; this audit re-derives from the pinned tree.

## Local test runs (venv `/tmp/venv-80-1531`, `--system-site-packages`, pip only, removed before commit)

* `cd src/importer && python -m unittest discover -s tests -q`: 85 tests, OK.
* `cd src/api && PYTHONPATH=../core/tests:../agents/tests:tests python -m unittest tests.test_list_export_api tests.test_exception_register tests.test_exception_register_screen tests.test_continuity_epoch_export tests.test_resident_choice_export -q`: 175 tests, OK, 38 skipped ("owned local MSSQL opt-in"). A first run without `tests` on PYTHONPATH had 2 import errors (`No module named 'test_assistants'`), a path-setup issue, not a product failure.
* No browser, SQL, image or hosted CI run; none claimed.

## Limits

Static literal search cannot prove absence of generic controls; synthetic data only; no human, owner or policy approval evidence was found or created.
