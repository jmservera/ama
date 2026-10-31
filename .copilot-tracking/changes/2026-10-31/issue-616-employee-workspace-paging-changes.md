# Changes: issue 616

* `src/core/src/zava_forward/core/procurement.py`: paged `list_work_orders` and `list_packages`.
* `src/api/src/zava_forward/api/server.py`: `limit`/`offset` parsing and 400 validation.
* `src/api/src/zava_forward/api/web/ops.js`: paged capacity view with pager controls.
* `src/api/tests/test_workspace_paging.py` (new) and `test_case_journey.py` (mock envelope).

Validation: unittest test_workspace_paging, test_procurement_api, test_case_journey, test_role_matrix and test_role_endpoint_inventory pass; `node --check ops.js` and `ruff check` pass; mypy reports only pre-existing errors; `ruff format --check` flags server.py and procurement.py at baseline too. Heavy gate not run; CI is the evidence.

## Correction cycle 1 (PR 618 review)

* `server.py`: paging parameters parsed with `keep_blank_values=True`; blank `limit`/`offset` return 400, a lone `offset` is validated with default limit 50.
* `ops.js`: confirm before changing the work order page while appointment drafts are unsaved; each capacity load snapshots page state and a load sequence rejects superseded responses before offset correction or render.
* `capacity_browser_check.py`: consumes the `items` envelope and matches paged request URLs with a regex helper.
* `test_workspace_paging.py`: blank-value 400 regressions and source guards for the pager.

Validation: test_workspace_paging and test_capacity_browser_check pass; `node --check`, `ruff check`, `ruff format --check` pass; mypy shows only the 4 pre-existing errors. The Playwright capacity check was updated but not executed (no browser/SQL prerequisites here). Heavy gate not run.
