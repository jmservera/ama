---
title: "#184 post-policy validation changes"
ms.date: 2026-11-09
---

Plan: [plan](../plans/2026-11-09-live-simulator-postpolicy-184-plan.md). Critique: [critique](../plans/2026-11-09-live-simulator-postpolicy-184-critique.md). Local only; no push, PR, issue or board write. Logs are in /home/azureuser/logs-184-pp (not committed).

## Identity and ordering

* Frozen start 14ce745448bf0b63d80e89af3bd952ddb48c7c81. Prospective records committed first (90d3ee293), then the pinned main merge d8a8b909c (origin/main 76db469b16e7ac0ae862e8c9b19873fc66b04f0e, clean, only src/README.md and docs/policy paths arrive), then the correction commit 6c449cc68.
* Ancestry verified: 14ce745 and 76db469 are both ancestors of HEAD. No rebase, force, remote write or sibling import.
* Since the pin, origin/main moved to 1f28d0913 (#1222 paired_equity, unrelated core module, plus docs and a rubric score). `git merge-tree` against it is clean; overlaps are only docs/reference/README.md, docs/reference/log.md and src/core/README.md. It is not merged here (the brief pins 76db469); the coordinator decides a later local merge and rerun.

## Source changes of this pass (no behavior change)

* tools/test_rpi_checks.py: ruff format of two long lines (E501 at 668 and 740) in the earlier recovery edit. See plan A1.
* src/core/src/zava_forward/core/sensor_sql.py: `# type: ignore[no-untyped-call]` on the calls into the untyped mssqlstore helpers (3 mypy errors). See plan A2.
* src/api/tests/test_live_control.py: typing comments on the SensorIngestion monkeypatch lines (attr-defined) and one unused ignore removed (5 mypy errors).
* RPI runner tuple growth against the pinned base is exactly two names: test_live_weather_rows_are_not_indoor_input and test_weather_only_window_is_insufficient_with_explicit_reason (diff verified; no runner logic change).

## Environment

Python 3.12.3 in /home/azureuser/venv-184; editable zava_forward core, api and agents resolve to this worktree's src/*/src; mssql-python 1.15.0; ruff 0.17.1 and mypy 2.4.0 absent at first (observed), then installed pinned into that venv only. az Bicep CLI 0.48.1.

## Test outcomes at final head 6c449cc68 (logs under final/)

| Command (cwd) | Tests | Exit | Skips |
| --- | --- | --- | --- |
| core unittest discover -p test_sensor*.py | 192 | 0 | 11 offline opt-in SQL (10 analysis tests needing ZF_SENSOR_MSSQL, 1 sensor_privacy owned-SQL test) |
| core -p test_device*.py | 48 | 0 | 0 |
| core -p test_live*.py | 22 | 0 | 0 |
| core -p test_resident_sensors.py | 10 | 0 | 0 |
| core -p test_historical_backfill.py | 10 | 0 | 0 |
| core -p test_retrofit_scenarios_retained_store.py | 3 | 0 | 0 |
| api -p test_live*.py (PYTHONPATH=../core/tests:../agents/tests) | 66 | 0 | 2 test_live_receiver_sql (needs task-owned SQL) |
| api -p test_iot*.py | 49 | 0 | 0 |
| api -p test_sensor*.py | 103 | 0 | 0 |
| tools -p test_rpi_checks.py | 102 | 0 | 0 |
| infra test_iothub_module / test_bicep_policy / test_container_contract (REQUIRE_AZ_BICEP=1) | 23 / 57 / 7 | 0 | 0 |

The 13 offline skips are not SQL proof; SQL proof is the owned run below.

## Owned disposable SQL (task-owned loopback mssql container, harness-removed)

Heavy lock admitted non-queued with `flock -n -E 99`; 22 default attempts returned 99 while other lanes held it (1288 e1, 1292 vc); no other lane's SQL was stopped; no Docker prune.

| Selector | Result | Exit |
| --- | --- | --- |
| default (six selectors) | Ran 70 tests, OK, no skip text in the log; the harness validates exit only for this selector, so the log was parsed | 0 |
| analysis (--selector analysis) | Ran 10 tests, OK, no skips, "Selector analysis: accepted"; the ten discovered names equal the ten Mssql names in SENSOR_MSSQL_REQUIRED_TESTS | 0 |

The earlier recorded analysis run that executed ten tests but was rejected (exit 1) before the harness correction, and the corrected exit 0, remain in the earlier recovery records and the original adverse evidence; this pass does not recreate or replace them. Post-run docker ps shows no task container left.

## Lint, type and Bicep (previously unrun; not inherited)

* ruff check and format --check under the runner contract (`--isolated --select E,F,I,B,UP --target-version py312 --line-length 100`) on tools/rpi-checks.py and tools/test_rpi_checks.py: first run failed (2 E501 plus format), passes after A1. mypy --strict on both: pass.
* src/core `ruff check .`, `ruff format --check .`, `python -m mypy`: pass after A2 (first mypy run had 3 errors).
* src/api `ruff check .` and `ruff format --check .`: pass. `python -m mypy`: first 53 errors, 48 after A2. Remaining 48 are not parent code: 46 are missing optional playwright.sync_api stubs (prerequisite absent in this venv; hosted CI installs it) and 2 are in unchanged main tests (test_workbench_live_defaults.py:123, test_atlas_tensions_checker.py:66). Not waived: recorded as environment and pre-existing, to be confirmed by hosted CI.
* az bicep build and lint pass for live-receiver-job, live-simulator-job, iot-hub-live, modules/iothub and modules/iothub-scope-guard. No infra unit test references the two live job templates, so template-specific assertions are build and lint only. No deployment, what-if or Azure sign-in.

## Finding F1 (unfixed, not waived)

test_iot_stream PublisherTests.test_actual_send_rate_after_connect_and_preparation_across_devices failed once in the first api iot run (0.04998 not >= 0.05, time.monotonic jitter under shared load, load average about 3.8) and passed on three isolated reruns and in the final-head run. The test and iot_stream.py are unchanged by the parent. A flake fix needs its own draft (for example a small tolerance or a fake clock); none is made here.

## Guard table (executed tests; backend)

| Guard | Test | Backend |
| --- | --- | --- |
| receiver cap 100 homes | test_live_control test_one_hundred_homes_is_the_largest_cohort | offline unit, passed |
| 14 day expiry, all readers | test_readers_refuse_an_expiry_beyond_fourteen_days, test_window_must_be_future_and_at_most_fourteen_days, test_rewrite_beyond_fourteen_days_during_window_stops | offline, passed |
| stop, expiry, owner, invalid file | test_stop_and_expiry_are_final_decisions, test_stopped_expired_and_invalid_control_never_reach_persistence, test_stop_during_window_signals_the_receiver | offline, passed |
| admin cohort grant (cohort is homes present in store, removal refused) | test_cohort_is_the_control_homes_present_in_the_store, test_cohort_removal_is_refused_not_cached, test_cohort_changed_to_absent_homes_sends_nothing_more | offline, passed |
| rejected data-quality (consumer) | test_sensor_consumer_live test_rejections_are_durable_data_quality_exceptions, test_declined_consent_and_late_slot_are_rejected | core store plus default owned SQL run, passed |
| replay, dedup, window | test_accepts_and_replays_without_duplicate, test_same_slot_with_other_values_is_a_conflict, LiveEnvelopeReplayTests, test_composed_joint_query_statistics_and_reopened_window_replay, test_raw_replay_keeps_live_envelope_exact_beside_backfill | offline plus owned SQL, passed |
| weather exclusion and weather-only insufficiency | test_live_weather_rows_are_not_indoor_input, test_weather_only_window_is_insufficient_with_explicit_reason | analysis owned SQL, passed |
| receiver minimum grants | test_live_receiver_sql ReceiverMinimumGrantTests (two tests) | owned SQL in the 70 default run, passed |
| no secret in changed source and infra | targeted pattern scan (SharedAccessKey, AccountKey, private key blocks, password literal) of the changed non-test source and two job templates | zero hits |

## Original C5 Low gaps: status confirmed open

test_live_receiver_sql.py contains only the minimum-grant startup and write test and the missing-schema refusal test. It never calls `live_receiver.main` under the exact-grant principal and has no rejected data-quality write under the receiver grants. Both gaps remain open and are not closed by this pass or claimed closed by independent review.

## Not run or not claimed

rpi-checks --all or --changed and any receipt; hosted CI; browser checks (no web asset, route or template changed; Playwright not installed here); deployment, what-if, Azure auth; any real Hub, model, credential or billable message; independent exact-head review; actual simulator to Hub to SQL to UI to Quality model proof.
