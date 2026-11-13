# Changes: Epic #89 unit verification (89-delivery-quality-verify-1222)

Base 74a93a137a983e0a87418e3321a6847ba9bcd278. Refs #89, #92, #132, #133. Tracking-only; no src/ or docs/ edits.

## Environment

* Scratch venv /tmp/venv-89-1222 (system site packages), setuptools and wheel upgraded, editable --no-deps --no-build-isolation installs of src/core, src/agents, src/api: all exit 0.
* Verified package paths inside the worktree: zava_forward.core, .agents, .api under /home/azureuser/source/ama-demo-wt/child-89-delivery-1222/src/*/src/.
* Run with HOME=/tmp/zf-home-89, PYTHONDONTWRITEBYTECODE=1, ZF_DATA and ZF_TEST_MSSQL unset, proxy set to an unreachable address with loopback excluded. No Docker, MSSQL, browser, cloud or model calls.
* Producer exit codes captured directly with `$?` into files. The first API pass used a proxy that also blocked loopback and a non-discover invocation; those results (connection refused, missing helper imports) were invalid and the failing modules were rerun with `unittest discover -s tests -p <module>.py`. Only the rerun is reported below.

## Results (sha256 is the first 16 hex characters of each log)

| Suite | Module | Exit | Ran | Skipped | Result | Log sha256 |
| --- | --- | --- | --- | --- | --- | --- |
| core | test_aftercare | 0 | 23 | 0 | OK | daecfec5259362e9 |
| core | test_aftercare_intake | 0 | 44 | 0 | OK | 489a2a8b21632b09 |
| core | test_aftercare_store | 0 | 42 | 15 | OK | b62a4bf84f663332 |
| core | test_consultation_controls | 0 | 45 | 16 | OK | cde0fe7717394877 |
| core | test_job_pack | 0 | 10 | 0 | OK | dfd4b40ba6df3379 |
| core | test_quality_procurement | 0 | 136 | 0 | OK | afec50b3dea4931a |
| core | test_resident_decisions | 0 | 419 | 149 | OK | e444a425aa9260b3 |
| core | test_progress_event_capture | 0 | 51 | 18 | OK | 402caa872c876651 |
| api | test_aftercare_screen | 0 | 13 | 0 | OK | 99a8ddd6d5e069a3 |
| api | test_aftercare_served | 0 | 8 | 0 | OK | a132bdc581487968 |
| api | test_staff_intake_api | 0 | 96 | 36 | OK | fe91256337dfee93 |
| api | test_procurement_api | 0 | 36 | 0 | OK | 4edfdb380f216a79 |
| api | test_procurement_screens | 0 | 14 | 0 | OK | 7feeaa01b9eeb8c0 |
| api | test_resident_api | 0 | 21 | 1 | OK | 81eaf2433a5f61c0 |
| api | test_resident_callbacks_page | 1 | 0 (import load error only) | 0 | NOT RUN: ModuleNotFoundError azure (azure.core not installed in the scratch environment) | 438bdf51db76ca0d |
| api | test_technical_quality_screens | 0 | 16 | 0 | OK | d9f01499a50fa47e |
| api | test_resident_preview_api | 0 | 15 | 0 | OK | 3a4bae18f3578d49 |

Totals for the 16 modules that ran: 989 tests ran, 235 skipped, 0 failures, 0 errors. Executed passing tests (ran minus skipped): 754. Skips are not passes.

## Skips (explicit, not reported as passed)

* 161 skips: opt-in owned loopback SQL Server (MSSQL); 32: staff intake MSSQL opt-in (ZF_STAFF_INTAKE_MSSQL=1); 18: opt-in task-owned MSSQL; 15: needs task-owned SQL Server; 4: SQL-store contract read dependency; 1: opt-in local browser. Reason counts come from grepping six verbose logs and sum to 231 of the 235 skips; the other 4 were not categorised.
* Excluded by design: test_capacity_browser_check and test_staff_intake_browser (Chromium); sensor modules (covered in #1288).

## Gaps

* test_resident_callbacks_page was not verified: the azure SDK is missing from the scratch environment (no network install permitted). Appointment and resident update callback coverage is partial; resident appointment and remedy paths are otherwise exercised through test_resident_api and test_resident_preview_api.
* All MSSQL-backed coverage is unverified here (skips above).
* No module is named for provider capacity apart from the excluded browser check; capacity, work order and consultation behaviour is exercised through procurement, job pack, consultation, quality procurement and staff intake modules by keyword grep of the test bodies.

## Cleanup

Scratch venv, /tmp logs and /tmp/zf-home-89 removed before commit; no untracked source or egg-info files remained.
