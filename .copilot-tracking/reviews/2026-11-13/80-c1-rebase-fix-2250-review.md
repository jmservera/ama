<!-- markdownlint-disable-file -->
# Review: C1 correction (#80 list exports)

* Execution: one Review, by running the Focused tier in `/tmp/venv-80-c1` (pip, no uv) at the rebased head. Not repeated.
* Outcome: all four independent-review items resolved; no open material findings.
* Tier: Focused. The complete local gate and an external receipt were not run and are not claimed. Hosted CI and human approval are outstanding (not pushed).

## Commands run and results

* src/core `test_list_export` 4 OK; `test_needs_inventory` 11 OK; `test_scenario_manifest` 8 OK; `test_retrofit_scenario*` 13 OK. The full core suite was not run (not in the selected tier).
* src/importer full unit suite: 89 OK (86 plus 3 new `test_xlsx_safe_cell`).
* src/api (each run with `PYTHONPATH=../core/tests:../agents/tests`): `test_list_export_inventory` 15 OK (rerun after format, still 15 OK); `test_list_export_api` 11 OK; `test_role_endpoint_inventory` 24 OK; `test_role_matrix` 13 OK; `test_accessibility_baseline` 13 OK; `test_content_standard` 29 OK; `test_lawstore` 34 OK (14 skipped); `test_assistants` 136 OK (59 skipped); `test_aftercare_served` 8 OK; `test_timecapture` 26 OK.
* One first-run failure: my new link-count assertion compared with all 18 exports; the screens carry 16 literal `href` lines. Changed to the 5 new links; rerun OK. The fixed regex otherwise matched no real link line.
* `ruff check` and `ruff format --check`: core, importer clean; api had 7 line-length errors and 1 format diff in my new test code, fixed with `ruff format`; clean on rerun.
* `mypy`: core 300 files clean; importer 13 files clean; api 66 errors in 61 files, none in `server.py`, `test_list_export_inventory.py` or `test_role_endpoint_inventory.py`. They are missing `playwright` stubs (not installed in the Focused venv), `no-any-return` in checks/ and one unused ignore in `test_atlas_tensions_checker.py`; same count as the independent review's run at the old base.

## Item check

* Rebase and conflict: done; inventory, role, accessibility and content tests pass at the rebased head, so the screen scan covers main's changed `web/*.js` and the `proposal-freshness` endpoint.
* Regex and tautology: fixed and self-checked; importer `safe_cell` aligned with core and tested against it.
* Criterion 4 metadata: law and proposal rows carry source, timestamps, approval state and supersession where the store has them; tests show no reviewer email, note, output or snapshot leaks. Supersession is derived from `historical` status only; the store has no explicit supersession link.
* Residual: CSV re-import is previewed, not detected (existing follow-up); api mypy playwright noise.
