<!-- markdownlint-disable-file -->
# Changes: every list offers a read-only export (issue #80 criterion 2)

## Added

* `GET /api/time/mine.csv`, `/api/time/report.csv` (report keeps the minimum-group suppression).
* `GET /api/law/sources.csv`, `/api/assistants/proposals.csv` (follows every page, up to 200), `/api/aftercare/concerns.csv` (tracking fields only; the resident's own words, history and sensor context are left out).
* Download links on the time, law, assistants and aftercare screens, in plain housing language.
* `src/api/tests/test_list_export_inventory.py`: list inventory with reasons for each exemption, end-to-end export checks per permitted role (stored state, including the law store, is identical before and after), contractor 403 and anonymous 401, formula neutralisation, paging, concern canary and link checks.
* Importer refusal of an exported workbook (`is_read_only_copy`, preview shows a blocking conflict, staging raises).

## Changed

* `safe_cell` also neutralises formulas hidden behind leading space, tab, CR or LF.
* Exported workbook note built from one shared `READ_ONLY_COPY_NOTICE`.
* `test_role_endpoint_inventory.py` lists the four new routes.

## Divergences and amendments

* Implementation started before the independent critique ran. The strict order was not kept; critique findings were applied afterwards (see critique file).
* Law provisions and the aftercare evaluator are exempt, with reasons, rather than exported.

## Validation (scratch venv, pip only)

* ruff check and format check clean for core, api and importer; mypy clean for core and api.
* Importer: 86 tests OK. Api guards (inventory, export, content standard, accessibility baseline, design system, role inventory and matrix): OK. Core and full api suites: see state file for final result.
* Scratch venv removed before commit. Nothing pushed; GitHub not edited.
