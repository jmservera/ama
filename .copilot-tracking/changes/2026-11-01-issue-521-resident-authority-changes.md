# Changes: issue 521

* `src/api/checks/resident_demo_browser_check.py`: removed `SQL_AUTHORIZATION_END`; fixture uses `rs.AUTHORITY_END`.
* `src/api/tests/test_resident_demo_check.py`: asserts 2027-02-01 window end, not 2026-11-01.
* `infra/README.md`: coordinator steps for live SQL constraint, row renewal, redeploy.
* Validation: api resident_demo tests (47), core resident_showcase tests (89, 27 skipped for SQL), infra resident_demo tests (32) OK; ruff check and mypy pass on touched files. `ruff format --check` flags pre-existing formatting in resident_demo_browser_check.py (untouched lines).
* Not applied: any Azure/SQL change.
