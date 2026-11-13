# Changes: 113-platform-auth-verify-1222

Epic #113 offline unit verification at `74a93a137a983e0a87418e3321a6847ba9bcd278` (Refs #113, #114, #116, #117, #119, #120, #121, #122, #350). No `src/` or `docs/` edits.

## Method

* Venv `/tmp/venv-113-1222` (system site packages), setuptools/wheel upgraded, editable `--no-deps --no-build-isolation` installs of `src/core`, `src/agents`, `src/api`; import paths verified inside this worktree `src/`. Venv and logs removed afterwards.
* One `python -m unittest -v <module>` per module, run from each `tests` directory (API `PYTHONPATH=../../core/tests:../../agents/tests`), with `ZF_DATA`, `ZF_TEST_MSSQL`, `ZF_BROWSER_TESTS`, `ZF_DOCUMENT_RESCAN_MSSQL`, `ZF_SENSOR112_MSSQL`, `ZF_CONTINUITY_MSSQL` unset and an isolated temporary `HOME`. No Docker, MSSQL, Chromium or external network; API tests may use loopback only. Exit codes captured directly with `$?`.
* Plan critique (rubber-duck) changes applied: bare module names, opt-in env unset, bytecode disabled, `git status --ignored` checked clean.

## Results (first pass)

| Module | Ran | Skipped | Result | sha256 (16) | Skip reason |
|---|---|---|---|---|---|
| api-test_auth | 41 | 0 | OK | 1542990bf0b93e24 |  |
| api-test_chat_fixture_roles | 1 | 0 | OK | 4348276f923d3fff |  |
| api-test_continuity | 22 | 0 | OK | 3d9ac9d5f518e374 |  |
| api-test_continuity_epoch_export | 75 | 38 | OK (skipped=38) | c8bff72a3b04ebaa | owned local MSSQL opt-in |
| api-test_document_controls | 17 | 0 | OK | 3acc946b44f60184 |  |
| api-test_entra_authoritative | 36 | 0 | OK | 6ddaa10365c69916 |  |
| api-test_expected_denials | 3 | 0 | OK | 9edc6e7394f9a906 |  |
| api-test_lawstore | 34 | 16 | OK (skipped=16) | 0295fb9fa48e7315 | azure-core not installed; needs a SQL Server (ZF_TEST_MSSQL=1) |
| api-test_ledger | 9 | 0 | OK | 1d8e6459ac08b264 |  |
| api-test_list_export_api | 11 | 0 | OK | 8e7ad5c2969ad1e4 |  |
| api-test_map_fullscreen | 8 | 0 | OK | 5617e4c2f4265de5 |  |
| api-test_mssqlstore | 1 | 0 | FAILED (errors=1) | 18d5baa1efd5e127 |  |
| api-test_resident_choice_export | 30 | 0 | OK | d2cb67cec5f3e3e7 |  |
| api-test_resident_ledger_meter | 1 | 0 | FAILED (errors=1) | 2c5edd7f0f82d512 |  |
| api-test_role_endpoint_inventory | 24 | 0 | OK | b1a79dc1584f1491 |  |
| api-test_role_matrix | 13 | 0 | OK | da066b94fa62bff2 |  |
| api-test_role_screens | 9 | 0 | OK | 0774842dac63dfb9 |  |
| api-test_role_screens_conformance | 12 | 0 | OK | bccfee3deef7341a |  |
| api-test_timecapture | 26 | 0 | OK | 0389b63dc7017471 |  |
| api-test_timecapture_copy | 12 | 5 | OK (skipped=5) | 64afc32b9ae5ba14 | opt-in local Chromium |
| api-test_version | 3 | 0 | OK | ea53af50a800a80e |  |
| core-test_chat_dpia_record | 4 | 0 | OK | fdd69c02fada7e44 |  |
| core-test_chat_privacy | 29 | 0 | OK | 80b8eecf0df96732 |  |
| core-test_data_protection | 18 | 0 | OK | 70827d1d6218845d |  |
| core-test_document_rescan | 38 | 19 | OK (skipped=19) | 7a2257328d6edd33 | requires owned loopback SQL Server |
| core-test_documents | 10 | 0 | OK | a8ad1b2dd2989828 |  |
| core-test_form_export | 11 | 0 | OK | ea293d23ba60f1a3 |  |
| core-test_list_export | 4 | 0 | OK | 711cce5cbd8aacdb |  |
| core-test_regulatory_privacy | 18 | 0 | OK | fada75f62b932ea3 |  |
| core-test_resident_documents | 5 | 0 | OK | 2146b58f3877cf93 |  |
| core-test_sensor_privacy | 17 | 1 | OK (skipped=1) | 4aee49c001b634f3 | opt-in own local SQL |
| core-test_sqlstore | 18 | 0 | OK | 44b571452a7e4cc8 |  |
| core-test_version | 3 | 0 | OK | 6d3ba8772947e1a4 |  |

Total ran 563, skipped 79.

## Failures and reruns

* `api-test_mssqlstore` exit 1 in first pass: harness-path error (`No module named 'tests'`), not a product failure. Rerun from `src/api` as `tests.test_mssqlstore` with `PYTHONPATH=tests:../core/tests:../agents/tests`: exit 0, 240 tests, 231 skipped (MSSQL opt-in; not verified coverage), log sha256 prefix `8a2bb481d16dc36a`. Two earlier rerun logs failed on import path only (`400c78d16fabff9a` missing `role_matrix_fixture`).
* `api-test_resident_ledger_meter` exit 1: `ModuleNotFoundError: No module named 'azure'` (azure-core not installed; `--no-deps` install). Environmental blocker, left unresolved; #114 resident ledger meter coverage is NOT verified here.

## Coverage notes

* Skipped tests (MSSQL, Chromium opt-in, azure-core) are not verified coverage: core document_rescan 19, sensor_privacy 1; api continuity_epoch_export 38, lawstore 16, timecapture_copy 5, mssqlstore 231.
* Excluding the unresolved `resident_ledger_meter` import error, all other selected modules exited 0. Effective total: 561 first-pass tests (563 minus the two 1-error import failures, mssqlstore and resident_ledger_meter) plus 240 mssqlstore tests from the rerun.
* Anonymous 401 parity (#350) exercised via `test_auth`, `test_expected_denials`, `test_role_endpoint_inventory` (all exit 0). Node prerequisite not separately checked.
