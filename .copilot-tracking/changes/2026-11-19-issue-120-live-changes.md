# Changes: issue 120 live

## Source changes

* `src/api/src/zava_forward/api/timecapture.py`: MSSQL upgrade now adds `notice_version` as `NULL` with no default (Azure SQL ledger tables refuse NOT NULL/DEFAULT additions); `request()` and `activation()` read `COALESCE(notice_version, '')`, so legacy rows never match the current notice version (fail closed).
* `src/api/tests/test_timecapture.py`: `MssqlUpgradeTest` asserts the nullable ALTER and the COALESCE read.

## Validation (focused local; FULL tier REQUIRED before publication, not run: SQL change, owner forbids rpi-checks.py --all)

* `python3 -m unittest tests.test_timecapture tests.test_timecapture_copy tests.test_content_standard -q` from `src/api`: 69 tests OK (5 skipped).
* `python3 -m mypy` (src/api): 7 errors in `src/core/tests/telemetry_support.py` (missing opentelemetry stubs), identical with and without the change (pre-existing).
* `ruff check`: pass. `ruff format --check` on timecapture.py: file was already unformatted before the change; src-ci only enforces it for infra/ files.
* Live (ca-cutover-test-demo-api, revision 0000033, staff test account, credentials unprinted): before fix `GET /api/time/status` 500; `az containerapp exec` reproduction gave ledger-table ProgrammingError. Fix is NOT deployed (no production changes by this worker); live post-fix proof is therefore pending redeploy.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Capture impossible without recorded DPIA reference | Proven (ticked, tests) | `test_timecapture.py` DPIA tests pass |
| Reports aggregate only with minimum group size | Proven (ticked, tests) | min_group tests pass |
| Staff notice approved and enabling action audited | Proven locally (notice-version gate, separated request/enable, audit entries; tests `test_notice_approval_and_audited_enabling_are_required`, `test_enabling_is_manager_only_and_audited_through_the_api`). Unproven live: status endpoint 500 on the deployed image until this fix is redeployed; real notice approval reference is a production item (deferred) | research note, logs |
