---
title: "#184 recovery research: current-main reconciliation and the ten-test sensor gate contract"
ms.date: 2026-11-09
---

Prospective recovery record for the demo push. Original C1 to C5 evidence is preserved unchanged and no earlier phase is backfilled.

## Start identity

* Branch feat/demo-recovery-sensors-184-1109, seed 57d152760 (unpublished C5 candidate from feat/live-simulator-integration-184). Remote parent lags at 9476dc961 and no parent PR is open.
* Fetched origin/main b46a9ad9a9619db535368d1b2cbbddec8110e122 (#1299, delivers #1297). Merge base fa7ae0c97; main is one commit ahead and changes only tools/rpi-checks.py, tools/test_rpi_checks.py and #1297 tracking records. No src/ or infra/ overlap.

## Stale statements checked against evidence

* Issue body says "Not started. No IoT Hub module exists in infra/modules": stale. infra/modules/iothub.bicep and iothub-scope-guard.bicep exist (merged #273, #498, #557); the owner records an observed existing Hub on 2026-11-08. No second Hub is provisioned or proposed. The issue body is not edited here (no issue writes); the correction is proposed in the handoff.
* Main already holds the simulator container (#1088), device provisioning (#647, #849, #1205), ingestion and handover (#587, #698, #645, #847), consumer (#508) and credential hygiene (#704). The unpublished parent adds cohort control, receiver, expiry control, weather exclusion and live replay coverage; none of that is on main.
* Dependencies: #177 CLOSED; #140 and #110 still OPEN although their modules/consumer are merged; #185 and #188 OPEN although their PRs merged. Parent merges are not acceptance of those issues.

## Findings from running the candidate against current main

* Owner comment 2026-11-08T23:41Z records two gate defects: (1) core skip contract, now fixed on main by #1299; (2) test_sensor_sql_check default-selection test expects two selectors while the candidate has six. Both reproduce as follows.
* Default selector: the candidate harness is correct at six selectors; only its unit test is stale. Fix is test-only.
* Analysis selector: main pins eight MssqlRetainedAnalysisTests. The candidate's test_sensor_analysis_store.py adds two inherited tests (test_live_weather_rows_are_not_indoor_input, test_weather_only_window_is_insufficient_with_explicit_reason), so the owned-SQL run executes ten. The harness (ANALYSIS_TESTS 8) rejected a clean 10 test run; main's gate pins (SENSOR_MSSQL_REQUIRED_TESTS) and its unit tests hardcode eight. Reconciliation is to pin ten without relaxing zero-skip or exact-count checks.
* Browser: the parent changes no web asset, route or template. Admin start/stop/cohort control is the live_control CLI plus Azure RBAC on the certificate share; README states an in-app admin screen is not delivered. There is no browser or API admin surface changed, so no browser check applies. Playwright is not installed in this venv, so unrelated browser checks could not run and are not claimed.

## Environment finding

The pre-installed editable zava-forward distributions point at the primary checkout. A worktree-local venv (/home/azureuser/venv-184, outside the repository) with editable installs of src/core, src/agents and src/api is used so the candidate, not the primary checkout, is imported.

## Gaps kept open

Low exact-grant entrypoint and rejected data-quality SQL gap (carried from C5); all live criteria; credential and log evidence; child closure and deferral acceptance. Receiver supports at most 100 bindings (MAX_COHORT 100 in live_control.py); 60000 devices are not assumed.

Ordering disclosure: findings come from actual runs made before this record was written (merge, selector SQL run, tool test failures). Nothing here is backfilled to an earlier date.

Planning readiness: Ready. Disposition: executed.
