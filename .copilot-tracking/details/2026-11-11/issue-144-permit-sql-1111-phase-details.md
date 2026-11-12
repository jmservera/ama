---
title: Issue 144 permit SQL boundary phase details
description: Phase details, selectors and receipts for the prospective real-MSSQL permit boundary validation
ms.date: 2026-11-11
task_id: issue-144-permit-sql-1111
---

## Phase 1: Admission (Root-controlled, future)

* Root decides D1 to D3 in the plan and arranges the independent prospective assessment. This launch performs none of it.
* Probes at run time, inside the driver: actual holder of `/tmp/ama-rpi-heavy.lock` (`flock -n` fails fast), free memory at least 6 GiB available, free disk at least 20 GiB, no listener on the chosen loopback port (the Docker publish uses a random port), image id and digest match, `docker` talks to the default local unix socket. Any failure stops with the exact blocker and no cloud or SQLite substitute.
* Success: a recorded admission receipt before any container exists.

## Phase 2: Test module (Option T only)

* File: `src/api/tests/test_permit_sql.py`. One class, seven methods in the plan, each deterministic by database clock and observed blocking.
* Imports: `unittest`, `os`, `threading`, `time` (only the poll interval), `sqlguard.require_task_owned_loopback`, `test_assistants.Base` and `MssqlFixture`, `test_ai_consumption_api as base` for the helper bodies, `zava_forward.core.assistants`, `ai_consumption.reference`.
* Success: ruff, format and mypy strict clean; with the flag unset all seven are skipped with the single tolerated reason and the module imports without a connection.

## Phase 3: Real-SQL observation

Receipts per run (unique names under the external ROOT): driver stdout and stderr, exit file per producer, `docker inspect` JSON (id, image id, labels, ports, State, memory), SQL Server version, sqlguard manifest hash (never the password), DMV observation records (holder SPID, claimant SPID, wait type, wait resource, applock held, database times for L0, observation, release, permit `issued_at`), framework output with `Ran 7 tests`.

Success: the seven ids are `ok`; all database times are monotonic as designed; none of the records contain a credential.

## Phase 4: Controls

* N1 stale-clock and N2 attribution mutants as in the plan; receipts: mutant diff, sha256 of mutant and original files, import origin assertion of the mutant core, framework output, exits.
* Success: observed outcome recorded per case against the prediction; a mismatch is reported, not adjusted.

## Phase 5: Cleanup and readback

* Exact container id only; `docker inspect <id>` must fail afterwards; the owned manifest and directories removed after hashing; the heavy lock released; `git status --short --ignored` equals the intended state.

## Selector inventory

Existing SQLite carry-forward, class `test_ai_consumption_api.ConsumptionApi`, exact methods: `test_permit_reserves_once_marks_and_fences_the_attempt`, `test_permit_denials_reserve_nothing`, `test_permit_reads_database_time_after_the_blocking_update_for_every_use`, `test_a_lock_wait_that_crosses_the_lease_margin_refuses_without_a_reservation`, `test_a_lock_wait_that_crosses_authority_expiry_refuses_without_a_reservation`, `test_a_short_authority_shortens_the_window_and_too_short_is_refused_unreserved`, `test_suspension_after_claim_denies_the_permit_and_refunds_once`, `test_consent_withdrawal_and_captured_readings_fail_closed_to_manual`, `test_an_unavailable_send_fence_refuses_without_a_reservation_or_a_marker`, `test_marker_blocks_reclaim`, `test_settlement_binds_to_the_marker_and_late_results_settle_the_meter_only`, `test_permitted_result_binds_attribution_to_the_stored_reservation_root`, `test_permitted_result_rejects_conflicting_attribution_without_settling`, `test_permitted_failure_without_root_settles_the_meter_and_publishes_no_output`, `test_result_without_a_permit_closes_the_task_against_a_later_permit`.

New real-SQL (class `test_permit_sql.MssqlPermitBoundary`): the seven methods named in the plan.

## Process note

No canonical phase-witness chain was requested for this launch and none was created. The state record is the only marker artifact. This is recorded, not regraded.
