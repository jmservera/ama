# Details: admin-only case-data routes (Refs #920)

* `src/api/src/zava_forward/api/web/app.js`: guard moved before case routes; duplicated tail guard removed.
* `src/api/checks/expected_denials_browser_check.py`: CASE_ROUTES and CASE_API assertions.
* `src/api/tests/test_expected_denials.py`: 403 pins for stats, visits, funding, finance.
* Human approval and resident consent boundaries untouched; no AI feature involved; manual route text unchanged.
