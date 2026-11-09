# Issue 80 r6 changes: schema CSV denial coverage

Chronology: r6 research, plan and details were written before the test edit. r5 records are unchanged and keep their own chronology.

## Changes

* `src/api/tests/test_form_staging_api.py`: imports `controls` and `projection`; adds a `register_staff` helper and `test_schema_csv_denies_admin_unknown_role_and_finance_without_resident_rights`.
  * Actors: Application Administrator, "Unregistered Role", and Grants and Evidence Officer (in `projection.FINANCE_VIEW`, not in `controls.RESIDENT_VIEW_ROLES`), all synthetic.
  * Each gets 403 on `GET /api/form-schemas.csv` and the JSON schemas route, with no attachment or CSV content type and no schema, digest, evidence, case or resident canary in the body.
  * `form_schemas`, cases and the `audit_head` count and hash are unchanged; the AI chat path raises if called.
* Production route, `forms.list_schemas`, `list_export.to_csv`, core policy, roles, UI, quality.py and dependencies are unchanged. The test did not reproduce a bug, so no guard fix was made.

## Commands (worktree src paths, bytecode disabled, external caches)

Imported modules proven in this worktree: `src/api/src/zava_forward/api/server.py` and `src/core/src/zava_forward/core/forms.py`.

* Tools: Python 3.12.3, ruff 0.17.3, mypy 2.4.1.
* `python3 -B -m unittest tests.test_form_staging_api tests.test_list_export_api tests.test_role_endpoint_inventory tests.test_loading_feedback` from `src/api`: rc 0, 51 tests, OK, no skips reported.
* `ruff check --no-cache .`: rc 0.
* `ruff format --no-cache --check .`: rc 0, 115 files formatted.
* `mypy --cache-dir /tmp/r6-80-mypy`: rc 0, 186 source files including tests.
* Initial failure: the first edit referenced `forms.projection` and `forms.RESIDENT_VIEW_ROLES`, which `forms` does not expose as attributes. It was corrected to import `projection` and `controls` before the first run, so no run failed.
* The new test passed on its first run. It is regression coverage for existing behaviour, not a fix, so there is no test-before-fix evidence.

## Not done

* No FULL, partial heavy, browser, SQL, Docker or cloud run; #96 holds the heavy lane.
* No push, PR, merge, retarget or criterion tick.
