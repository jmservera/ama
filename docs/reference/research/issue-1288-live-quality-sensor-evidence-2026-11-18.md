---
title: Quality sensor values and grounded review flag live evidence (Refs #1288)
description: Per-criterion proven or unproven record for the six unticked acceptance criteria of issue 1288, from local engineering runs and a live demo read and denial probe on 2026-11-18
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only, docs and evidence only. Owner decisions of 2026-11-18 authorise live Azure in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change) and waive billing reconciliation, DPO and Legal approval and person-run assistive technology testing. No source file changed (FOCUSED tier). Evidence folder: `.copilot-tracking/evidence/2026-11-18/issue-1288-live/`.

## Result per unticked criterion

| Criterion (issue 1288) | Result for the demo | Evidence and limit |
| --- | --- | --- |
| 3. Quality AI snapshot consumes the identical authorised reading IDs and values shown by the UI | Proven locally (mock provider); not proven live | Browser check: "displayed reading IDs and values equal the captured model snapshot". Live shows the UI side only |
| 4. Release-admitted proactive machinery makes a durable, deduplicated, bounded, model-attributed flag without manual invocation | Unproven for the demo (local dedup and bounds proven) | Local: five-minute burst plus restart gives one flag and one call. Live: no approved release record, so no proactive call |
| 5. Employee sees finding, cited IDs, source time, model/version, unapproved status; flag only requests review | Proven locally (mock provider); not proven live | Browser check: attributed unapproved flag cites the readings the model was given, no approval control |
| 6. Missing, stale, conflicting, unavailable states are explicit with a human route; no zero or fixture shown as AI | Proven locally; stale and unavailable also observed live | Live `/sensors` returned `freshness: stale` with a manual route; live invoke returned a disabled proposal with manual route and no envelope |
| 7. Focused SQL, API and browser tests correlate UI values and IDs with the model-request snapshot, incl. role denial, bounds, restart, staleness | Proven as local engineering evidence, with one test-harness note | Below |
| 8. Finite live walkthrough: simulator to Hub to SQL to UI to actual model consumption to visible flag | Unproven, cannot be proven for the demo | Below |

## Live demo observations (2026-11-18, read plus one denied invoke)

* Image `zava-forward-api@sha256:5368f4e4...c17e5fb`, revision `ca-cutover-test-demo-api--0000031` (the only active revision). Employee sign-in as `Retrofit Programme Manager` through Playwright Chromium (1366x900); credentials were read at run time and never printed.
* Of 12 listed cases only ZF-2025-0031 is in scope; the other 11 return 403 "Case is outside your current scope." on `/api/cases/{id}/sensors`.
* `GET /api/cases/ZF-2025-0031/sensors` returned `retained-reading-view-v2`, `kind: synthetic-retained-readings`, units degC and %RH, 12 readings (cap 12 plus 4 context each side), stable reading and sensor IDs (for example `LIVE-S7XBQ3HG3P5-20261118T0740Z`), UTC times, `provenance_class: synthetic-weather-derived`, `calibrated: false`, 12 `citation_keys`, `freshness: stale` (age 12114 s, latest 2026-11-18T07:40Z), and `retrofit_context.available: false` with the text "No installation date or marker is recorded...". Criterion 1 and 2 behaviour holds live.
* The case page text captured with the Quality tab and the AI tab selected (`ui_quality` and `ui_ai` in `live_probe.json`, first 3000 characters of page text) contains the stale message, and the AI tab text contains "Operator authority, finite allowance and expiry are required." The one retained screenshot ([top of the case page](../../../.copilot-tracking/evidence/2026-11-18/issue-1288-live/live-case-top.png)) shows the case header and status cards only; it does not show either tab panel, and the earlier second screenshot was an identical duplicate and was removed. Raw output not retained for the tab panels beyond that text.
* `GET /api/assistants/simulation/quality` returned `status: unavailable`, `reason: not-configured`, label "Public synthetic simulation...", manual route text.
* `POST /api/assistants/quality-evidence/invoke` on ZF-2025-0031: 202, `envelope: null`, `release: null`, `manual_requested: true`, reason "Operator authority, finite allowance and expiry are required." RAI metrics `invocation` 5 to 6, `tokens` 0, `fallback` 16 and `consumption` 16 unchanged. The probe stored one retained denial proposal and no model call was made.
* Env of the app: `AI_DEPLOYMENT=standard`, `AI_MODEL_VERSION=gpt-4.1-nano-2025-04-14`. No simulator job exists now in resource group `ama` (jobs: init, verify, ledger-verify, import, orchestrator, smoke, mi-http, public-audit); the newest retained reading is from the earlier live run.

## Local engineering evidence (criteria 3, 5, 6, 7)

Labelled local engineering evidence: fixture data and a mock provider, not the retained dataset and not a real model.

* From `src/api`: `python3 -m unittest test_quality_sensor_grounding test_quality_sensors_correlation test_quality_sensors_c7 test_quality_sensors_e1 test_quality_sensors_e2 test_quality_simulation_lane test_quality_sensors` with the PYTHONPATH from the repository guide: 497 tests, OK, 179 skipped (the SQL Server classes need `ZF_TEST_MSSQL=1`). Output: `focused_tests.txt`. Named cases include `test_ui_values_ids_and_evidence_equal_the_model_request`, `test_role_denial_reaches_neither_the_read_model_nor_the_snapshot`, `test_read_model_is_bounded_and_generates_nothing`, `test_burst_of_five_minute_readings_and_restart_make_one_flag_and_one_call`, `test_fresh_service_keeps_flag_status_and_a_new_release_marks_it_not_current`, `test_flag_never_approves_and_leaves_human_acceptance_untouched`, `test_missing_and_unavailable_states_give_a_manual_route_and_no_zero`, `test_model_failure_gives_no_flag_and_no_fixture_labelled_as_ai`.
* Browser check `python3 -m checks.quality_sensors_browser_check` (Playwright Chromium, isolated fixture, mock provider): 33 checks passed, exit 0. Output: `browser_check.txt`, `browser_check_results.json`. Covers displayed IDs and values equal to the captured model snapshot, attributed unapproved flag with cited readings and no approval control, stale, unavailable and withheld states, denied role and denied API.
* Actual SQL Server 2022 (throwaway local container, generated one-off password, bound to 127.0.0.1, removed afterwards): `test_quality_sensors.MssqlReadModel` and `MssqlHttp` (94 tests) gave 93 passing and one failure; `test_quality_sensors_c7` and `test_quality_sensors_e1` MSSQL classes passed apart from the same inherited case. Outputs: `mssql_quality_sensors_run2.txt`, `mssql_quality_sensors.txt`.

## Why criteria 4 and 8 cannot be proven for the demo

* A model-attributed flag needs an approved, unexpired release record. #107 evidence records that a release approver and residual-risk holder are not appointed (OQ-017); recording one with the demo account would fabricate authority. Live invoke confirms `release: null` and no provider call.
* The walkthrough needs an admitted finite simulator run. No simulator job exists, simulator-job role grants and run admission are separate authorities (#184, #189) that this task does not hold, and the issue states it does not itself authorise model calls or Azure writes.
* The deterministic and mock outcomes above must not be read as meeting criterion 8.

## Defect and harness notes (no source fix made)

* Note 1: `test_active_chat_memory_is_never_evidence_for_a_chat_proposal` (inherited by the SQL classes) failed on a reused SQL test database with five extra canary memory rows, and passed on a freshly created database (`mssql_memory_canary_fresh_db.txt`). The `MssqlFixture` table drop list in `src/api/tests/test_assistants.py` does not include the chat memory table, so repeated runs against one database accumulate rows. Test hygiene only; not a #1288 product defect.
* Note 2: the first SQL run (`mssql_quality_sensors_run1_login_failures.txt`, 90 errors "Login failed for user 'sa'", 4 failures) hit SQL login errors at the SQL Server side ("An error occurred while evaluating the password"); the cause was not identified. A rerun against the same container logged in normally. Preserved as adverse evidence.
* Note 3: `checks.quality_sensors_browser_check` fails when the working directory path is long (Chrome SingletonSocket path limit, `browser_check_attempt1_socket_path_too_long.txt`); it passed from a short directory. It creates its temp root under the current directory.
* Observation: the live case shows `freshness: stale` because no simulator is running; this is the designed stale state, not a defect.

## Evidence limits

* Azure CLI facts (revision, jobs, env) are operator-observed; raw output was not retained.
* The live probe wrote one retained denial proposal and one metric increment into the demo store.
* Criteria 3, 5 and 6 are not proven against a real model or the live store; only the live read side was observed.
* Independent exact-head review and hosted CI are outstanding. No tick or closure is claimed; criteria 3 to 8 stay unticked.
