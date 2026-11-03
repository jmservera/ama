# Details: issue #228 withheld-items panels

* `src/api/src/zava_forward/api/web/role-screens.js`: both procurement screens end with `screenWithheld`. Manager list: resident contact and access history, household and vulnerability details, contract rates and invoice values, contractor submissions (recorded elsewhere). Contractor list: resident contact history, household details and any reason behind a notice, contract rates, other contractors' capacity.
* `src/api/tests/test_procurement_screens.py`: `test_withheld_items_listed_as_text`, `test_withheld_items_listed_without_reason`.
