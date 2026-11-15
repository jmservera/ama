# Details: issue 80 criterion 2 list exports

## Phase 1: routes in `src/api/src/zava_forward/api/server.py`

* `_csv(filename, rows)` helper over `list_export.to_csv` (formula-safe, attachment).
* `/api/time/mine.csv` and `/api/time/report.csv` share the JSON branch, so the manager-only and notice-acknowledged checks and the suppression apply unchanged.
* `/api/law/sources.csv` from `law_source_rows` (sources held, then topics with no source held).
* `/api/assistants/proposals.csv` limited to `PROPOSAL_EXPORT_FIELDS`, from the same `listing` call.
* `/api/aftercare/concerns.csv` through `app.aftercare.handle` with `concern_export_row` (tracking fields; no statement, history or sensor context).
* Role gating is the existing `projection.allowed` kind of the matching JSON path.

## Phase 2: screens

* `timecapture.js`, `law.js`, `assistants.js` (case panel and queue), `aftercare.js`: anchor with `download` plus "The file is a read-only copy; changes in it are not imported back."

## Phase 3: `src/importer`

* `mapping.is_read_only_copy` reads the Read me notice; `build_preview` returns a blocking conflict, so `QuarantineStore.stage` refuses.

## Phase 4: tests

* `src/api/tests/test_list_export_inventory.py`; importer test in `test_excel_transition.py`.

## Phase 5: validation

* ruff check and format, mypy in core and api, api unittest discover, core export and queue tests, importer tests.
