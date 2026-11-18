<!-- markdownlint-disable-file -->
# RPI Changes: Issue #1238 Stale Pending Supersession and Retry/Receipt Verification

## Metadata

* Task ID: issue-1238
* Related plan: .copilot-tracking/plans/2026-11-14/core-1238-stale-pending-2346-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/core-1238-stale-pending-2346-phase-details.md
* Implementation date: 2026-11-14

## Execution Status

* Status: Complete
* Declared invocation scope: full_plan
* Completed scope markers: P01, P01-T01, P02, P02-T01, P02-T02, P03, P03-T01
* All remaining active-plan markers: none
* Status basis: All planned tasks (`P01-T01`, `P02-T01`, `P02-T02`, `P03-T01`) completed and verified in `src/core`.

## Execution Summary

Implemented Issue #1238's final remaining acceptance criterion (`(low F3) Mark a stale Pending attempt superseded`) in `ResidentDecisionMixin._res_service_forward` while keeping ACs 1-4 intact and verified. Recording an authorized explicit retry (`service_forward` with `retry_unresolved=True` when no send is in flight) now atomically transitions any stale `"Pending"` attempt in `route["attempts"]` to `"Superseded"` (`superseded_from="Pending"`, `superseded_at`, `superseded_by_attempt`) inside the reservation transaction without forging `manual_verified` `supersession` dual-approval metadata, preserving full attempt history, `route_key` idempotency, late-outcome fencing, and `delete_resident_records` personal-reference scrubbing across JSON and SQLite stores. Added four focused multi-backend test methods (8 test runs across `JsonResidentDecisions` and `SqlResidentDecisions`) with zero `sys.modules` manipulation, synchronized `src/core/README.md`, and passed `mypy`, `ruff check`, `ruff format --check`, and `unittest`.

## Completed Work

### Atomic Stale Pending Supersession in `_res_service_forward`

* Related phase or task: P01, P01-T01
* Files: src/core/src/zava_forward/core/resident_decisions.py
* What changed and why: Updated `ResidentDecisionMixin._res_service_forward` so that after all version, route, closed-status, `Acknowledged`, `retry_unresolved is True`, `not in_flight`, actor-identity/independence, and `resident_request_ref` checks pass, every prior attempt in `route["attempts"]` with `status == "Pending"` updates in place to `status="Superseded"`, `superseded_from="Pending"`, `superseded_at=now`, and `superseded_by_attempt=attempt` (sharing `now = _time()` with the newly appended attempt's `reserved_at`), and the returned `resident_service_forward` audit detail reports the superseded attempt number(s).
* Completion evidence: Diff in `src/core/src/zava_forward/core/resident_decisions.py` and passing `JsonResidentDecisions` + `SqlResidentDecisions` unit tests.
* Validation: Passed (`mypy`, `ruff`, `unittest`).

### Multi-Backend Unit and Regression Tests Without `sys.modules` Manipulation

* Related phase or task: P02, P02-T01
* Files: src/core/tests/test_resident_decisions.py
* What changed and why: Updated `test_forward_outcome_save_failure_leaves_pending_and_blocks_silent_resend` to assert `["Superseded", "Acknowledged"]` after `self.forward(retry_unresolved=True)` (retaining pre-retry `"Pending"` assertions) and added four focused methods on `JsonResidentDecisions` (inherited by `SqlResidentDecisions`): `test_forward_explicit_retry_marks_stale_pending_superseded_and_keeps_audit` (Complaint + Independent review routes, no `SupersessionBinding` required, preserved reservation fields, `route_key` idempotency, case audit detail, durable reopen, and `delete_resident_records` scrubbing), `test_forward_refused_or_rolled_back_retry_keeps_stale_pending_untouched` (refusals, audit rollback, and `in_flight` guard), `test_forward_chained_retries_preserve_prior_supersession_and_non_pending_history` (`1 -> 2 -> 3` chained stale `Pending` retries plus `manual_verified` `service_supersede_authorize` non-interference), and `test_late_outcome_for_retry_superseded_attempt_is_refused_and_logs_the_receipt` (late `_record_outcome` refusal and `receipt_ref` `WARNING` log).
* Completion evidence: Diff in `src/core/tests/test_resident_decisions.py`; `grep` confirmed zero matches for `sys.modules`; 434 tests in `test_resident_decisions` ran cleanly (`OK (skipped=154)`).
* Validation: Passed (`mypy`, `ruff check .`, `ruff format --check .`, `unittest`).

### Formal-Route Supersession Documentation Synchronization

* Related phase or task: P02, P02-T02
* Files: src/core/README.md
* What changed and why: Synchronized both the unresolved-retry paragraph and the `Pending supersession` paragraph under `Formal complaints and independent review forwarding` (`PC-002`) to document single outcome-write retry and `receipt_ref` logging, list `Pending`, `Unconfirmed`, `Superseded`, and legacy `Failed` without `not_sent` as unresolved, and contrast `service_supersede_authorize` (`manual_verified` two-person supersession without resending) with explicit `service_forward` (`retry_unresolved=True` when not in flight, recording `superseded_by_attempt`).
* Completion evidence: Clean Markdown diff in `src/core/README.md`.
* Validation: Passed manual Markdown/link and diff review.

### Static Type, Lint, Format, and Unit Test Validation

* Related phase or task: P03, P03-T01
* Files: src/core/
* What changed and why: Executed `python3 -m mypy`, `python3 -m ruff check .`, `python3 -m ruff format --check .`, and `PYTHONPATH=src:tests python3 -m unittest test_resident_decisions test_sqlreads -q` from `src/core`, verifying worktree import resolution (`src/core/src/zava_forward/core/resident_decisions.py`).
* Completion evidence: All commands exited `0` (`327` source files clean under `mypy`, `All checks passed!` under `ruff check`, `274 files already formatted` under `ruff format --check`, `Ran 449 tests in 136.882s — OK (skipped=154)`).
* Validation: Passed.

## Implementation-Time Plan and Detail Updates

### Focused Worktree `unittest` Selector Alignment

* Affected plan area or markers: P03-T01 in .copilot-tracking/plans/2026-11-14/core-1238-stale-pending-2346-plan.md and P03 in .copilot-tracking/details/2026-11-14/core-1238-stale-pending-2346-phase-details.md
* What changed: Recorded `PYTHONPATH=src:tests python3 -m unittest test_resident_decisions test_sqlreads -q` (matching `src/core/README.md`) as the focused `unittest` selector rather than whole-package `unittest discover` across unrelated CLI-subprocess and optional `azure-iot-hub` test modules.
* Why: In this shared environment, `~/.local` site-packages holds an editable `zava-forward-core` install pointing at `/home/azureuser/source/ama/src/core` without the optional `iothub` extra, so three unrelated modules (`test_device_registry_azure`, `test_discovery_assistant_demo`, `test_learning_test_bundles`) that either require `azure-iot-hub` or spawn un-prefixed subprocesses reflect the shared site-packages environment rather than this worktree; every in-process `src/core` store, SQL, governance, and `resident_decisions` module passed without touching shared site-packages.
* Triggering evidence: `python3 -m pip show zava-forward-core` and full discovery probe output.
* User answer or decision: Matches caller brief (`Focused unittest suite covering resident_decisions`) and repository validation-tier rules (`focused tier` without mutating shared environment installs).
* Reconciliation performed: Updated P03-T01 in the plan and P03 Validation Expectations in phase details.
* Planning and critique state: Current and ready; preserves approved scope and intent.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m mypy` | `src/core` (`src` + `tests`, 327 files) | Passed | `Success: no issues found in 327 source files` (exit `0`) |
| `python3 -m ruff check .` | `src/core` | Passed | `All checks passed!` (exit `0`) |
| `python3 -m ruff format --check .` | `src/core` (274 formatted targets) | Passed | `274 files already formatted` (exit `0`) |
| `PYTHONPATH=src:tests python3 -m unittest test_resident_decisions test_sqlreads -q` | `resident_decisions` (JSON + SQLite) and SQL read/replay harness | Passed | `Ran 449 tests in 136.882s — OK (skipped=154)` (`AzureResidentDecisions` skipped without external SQL Server fixture; exit `0`) |
| `grep sys\.modules` | `src/core/tests/test_resident_decisions.py` | Passed | `No matches found.` |

## Pre-Review Reconciliation

* Plan markers and phase details: Current; all markers `P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01` checked and phase statuses set to `completed`.
* Completed-work evidence and handoff prose: Current and synchronized across plan, phase details, and changes record.
* Validation, blockers, remaining work, and follow-up items: Current; zero blockers, zero remaining active items, `#1346` `RV-1` retained as follow-up only.
* Review readiness: Ready for single post-implementation `rpi-review`.

## Blockers

* none

## Remaining Work

* none

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-14/core-1238-stale-pending-2346-plan.md, `## Follow-Up Items`
* `#1346` low review item `RV-1` (`SupersessionBinding._roles` `MappingProxyType` + exact `type(binding) is SupersessionBinding` check): outside Issue #1238 AC 5 surgical scope; retained as post-Review follow-up candidate.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full_plan; completed: P01, P01-T01, P02, P02-T01, P02-T02, P03, P03-T01; remaining: none
* Validation coverage: `mypy`, `ruff check .`, `ruff format --check .`, and `PYTHONPATH=src:tests python3 -m unittest test_resident_decisions test_sqlreads -q` all passed (`0` exit code)
* Blockers: none
* Current plan and detail updates: Aligned P03-T01 worktree `PYTHONPATH=src:tests` focused `unittest` selector
* Planning and critique state: Ready (`PC-001` and `PC-002` resolved and implemented)
* Follow-up items: `#1346` `RV-1` retained outside active scope
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: parent (confirmed automatic RPI Agent)
