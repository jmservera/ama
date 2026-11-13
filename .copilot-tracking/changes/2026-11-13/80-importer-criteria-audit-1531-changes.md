<!-- markdownlint-disable-file -->
# Changes: Issue #80 importer and export criteria audit (2026-11-13)

Task `80-importer-criteria-audit-1531`. Pinned source `34b11967b93df40b653d384ab3b136bb1fb842f9`, branch `docs/demo-80-importer-criteria-audit-1531`. Tracking-only change: no source, test, issue or remote edit; focused tier; no hosted CI, browser, SQL or image run is claimed. All evidence is synthetic demo data. Issue text read with `gh issue view 80` on 2026-11-13; the issue checkboxes are not treated as evidence.

Path shorthand: `web/` means `src/api/src/zava_forward/api/web/`, `server.py` means `src/api/src/zava_forward/api/server.py`. Independent `code-review` found two citation issues: one corrected (`:383`), one rejected (`server.py:178-179` is correct, verified by grep).

Related artifacts: research `.copilot-tracking/research/2026-11-13/80-importer-criteria-audit-1531-research.md`, plan `.copilot-tracking/plans/2026-11-13/80-importer-criteria-audit-1531-plan.md`, details, critique (one `rubber-duck` run, findings applied) and state under the same task slug. The earlier audit `.copilot-tracking/audits/2026-11-10/issue-80-qualified-audit-1110-supplement.md` is superseded for control locations by this table; it is not edited.

## Commands run (venv `/tmp/venv-80-1531`, `--system-site-packages`, pip only, removed before commit)

| Command | Result |
| --- | --- |
| `cd src/importer && python -m unittest discover -s tests -q` | 85 tests, OK |
| `cd src/api && PYTHONPATH=../core/tests:../agents/tests:tests python -m unittest tests.test_list_export_api tests.test_exception_register tests.test_exception_register_screen tests.test_continuity_epoch_export tests.test_resident_choice_export -q` | 175 tests, OK, 38 skipped (`owned local MSSQL opt-in`) |

A first API run without `tests` on `PYTHONPATH` raised two import errors (`No module named 'test_assistants'`); this was a path-setup error, corrected by the command above, not a product defect. The 38 skips are SQL Server tests that did not run, so SQL-backed behaviour is unobserved here. Passing unit tests do not satisfy human approval or hosted CI.

## Per-criterion proof table

| Criterion and clause | Verdict | Evidence | Missing evidence or gate |
| --- | --- | --- | --- |
| C1 Import shows mapping (workbook importer) | PROVEN | `mapping.py:100-127` (`match_columns`); `test_excel_transition.py:120-128` (alias mapping, ready rows); CLI prints mapping `__main__.py:209-218` | Synthetic bytes only |
| C1 Import shows conflicts | PROVEN | `mapping.py:107-125` (conflict text); `test_excel_transition.py:130-136` (several columns, missing required, duplicates) | Synthetic bytes only |
| C1 Row-level preview with lineage | PROVEN | `mapping.py:130-190`; `test_excel_transition.py:123-128` (lineage row and SHA-256), `:138-141` (per-row problems); CLI row lines `__main__.py:221-223` | None for the module |
| C1 Source file never changed | PROVEN | `mapping.py:3-5,201-212`; `test_excel_transition.py:143-153` (read-only file, hash and mtime identical) | Local filesystem only; no hosted or live-share evidence |
| C1 Reachable by a user in the application | NOT FULLY PROVEN | Web screen takes CSV text only (`app.js:1756-1774`, `server.py:1417-1418`); it lists ready count, column match and rows to fix, not every row or lineage; the workbook importer is not imported by the API (no `zava_forward.importer` reference under `src/api/src`); `src/importer/README.md` "Not built" paragraph names the HTTP or web import surface | No workbook upload or row-level preview in the product; role and live-acceptance evidence absent |
| C1 Whole criterion as written | NOT FULLY PROVEN | Module-level proof above; user-facing screen is a reduced CSV check | Row-level preview through the product; human acceptance |
| C2 Every list offers an export | NOT FULLY PROVEN | Registered CSV routes `server.py:178-179`, test `test_list_export_api.py:75-79`; controls at `app.js:764,765,875,2280,2290`, `ops.js:246,490,494`, `panels.js:575`, `progress.js:189`, `role-screens.js:225,701,1489`; exception summary is a browser-built four-column CSV `role-screens.js:907-948`, tested in `test_exception_register_screen.py:285,545` | See list matrix: no canonical "every list" enumeration; several displayed JSON lists have no CSV route; owner must define scope and approve any operational export |
| C2 Excel or CSV format | PROVEN | CSV served for each registered route (`test_list_export_api.py:81-90,137-146`); formula neutralisation `:148-151` | CSV only; no Excel file is served by the API (`to_xlsx` unreferenced outside `src/importer`) |
| C2 Excel stays one-way read-only | NOT FULLY PROVEN | Module proof: `export.py:1-6,15-18,64-77` (values-only, Read me note), `test_excel_transition.py:374-383`; CSV export read-only `test_list_export_api.py:160-164` | Excel export is not reachable from the application; one-way read-only is proven for the library file only |
| C3 History retained: version, source, approval, supersession | PROVEN for the importer module | `export.py:20-33,45-61` (History columns), `quarantine.py:168-203`, `test_excel_transition.py:177-186` (named human approval), `:196-209` (supersession, version 2 in history row), `:374-383` (approved, decided by) | Synthetic data; `:374-383` asserts status and approver columns only; version and supersession are asserted in `:196-209` |
| C3 Independent of the AI provider | PROVEN | History fields come from the quarantine record (`export.py:45-61`); `test_excel_transition.py:383` asserts no "provider" header; approval refuses `AI` and `system` (`:177-186`) | None for the module |
| C3 Retained in an export a user can obtain | NOT FULLY PROVEN | History sheet only via `to_xlsx`, not wired to API or web; API list CSVs do not carry batch history (`test_list_export_api.py` compares rows and roles only) | Product path for the history export; role-scoped access decision; real-data approval |
| C3 Whole criterion as written | NOT FULLY PROVEN | Module proven; product reach not | As above |
| C4 Owners set staged transition thresholds | NOT FULLY PROVEN | ADR 0001 `docs/adrs/0001-azure-architecture.md:216` "proposed, thresholds to be set by owners"; stage 1 exit "owner-set targets for N consecutive cycles" (`:221`) | Owner-approved threshold record, named owners, quarantine age limit, rollback and data-protection sign-off. Human or policy gate; code and tests cannot prove it |

## C2 list-to-control matrix at the pin

| List or surface | CSV route | Control located | Note |
| --- | --- | --- | --- |
| Cases | `/api/cases.csv` | `app.js:875,913` | Progress variant `?report=progress` not located by literal search |
| Closed cases | `/api/closed-cases.csv` | `progress.js:189` | Current page slice |
| Handoffs, unaccepted handoffs | `/api/handoffs.csv`, `/api/handoffs/unaccepted.csv` | `app.js:764,765` | |
| Visits, funding | `/api/visits.csv`, `/api/funding.csv` | `app.js:2280,2290` | |
| Finance queue | `/api/finance.csv` | `panels.js:575` | |
| Stock queue | `/api/asset/stock-queue.csv` | `role-screens.js:225` | |
| Checklists | `/api/checklists.csv` | `ops.js:246` | |
| Form schemas | `/api/form-schemas.csv` | `role-screens.js:1489` | |
| Packages, work orders | `/api/packages.csv`, `/api/workorders.csv` | `ops.js:490,494` | Shown only when the page total is non-zero |
| Resident choice queue | `/api/resident/choice-queue.csv` | `role-screens.js:701` | |
| Exception register | none (browser-built) | `role-screens.js:907-948` | Four columns, demonstrator only, no file when state is partial |
| Not assessed for a control | none | none located | `/api/assistants/proposals`, `/api/assistants/releases`, `/api/aftercare`, `/api/law/alerts`, `/api/time/report`, `/api/briefing`, `/api/coordinator`, `/api/governance`, `/api/retention`, `/api/continuity/export` (JSON); whether each is a "list" is an owner scope decision |

Static literal search cannot exclude generic or dynamically built controls; absence from this table is not UI absence.

## Unresolved human and policy gates

* Owner definition of "every list" and which operational exports are approved.
* Owner-set staged transition thresholds, owners, rollback and data-protection approval for real data (ADR 0001 `:216-223`).
* Live-data access, retention and suppression approvals for any operational use; nothing here approves real-record use.
* Independent exact-head review, hosted CI, and browser/SQL acceptance of any product path remain required before publication or any issue tick; none is claimed.

## Outcome

C1 and C3 are proven at the importer-module level only; C2 and C4 are not proven. No issue criterion should be ticked, unticked or closed on this audit alone; the owner decides how to read the existing ticks.
