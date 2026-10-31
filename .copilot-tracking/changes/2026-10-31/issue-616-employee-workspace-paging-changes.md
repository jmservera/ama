# Changes: issue 616

* `src/core/src/zava_forward/core/procurement.py`: paged `list_work_orders` and `list_packages`.
* `src/api/src/zava_forward/api/server.py`: `limit`/`offset` parsing and 400 validation.
* `src/api/src/zava_forward/api/web/ops.js`: paged capacity view with pager controls.
* `src/api/tests/test_workspace_paging.py` (new) and `test_case_journey.py` (mock envelope).

Validation: unittest test_workspace_paging, test_procurement_api, test_case_journey, test_role_matrix and test_role_endpoint_inventory pass; `node --check ops.js` and `ruff check` pass; mypy reports only pre-existing errors; `ruff format --check` flags server.py and procurement.py at baseline too. Heavy gate not run; CI is the evidence.
