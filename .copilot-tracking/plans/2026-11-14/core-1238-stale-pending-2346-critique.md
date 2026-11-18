<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #1238 Stale Pending Supersession and Retry/Receipt Verification

## Metadata

* Task ID: issue-1238
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-14/core-1238-stale-pending-2346-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/core-1238-stale-pending-2346-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver the remaining acceptance criterion of Issue #1238 (`(low F3) Mark a stale Pending attempt superseded`) on branch `fix/core-1238-stale-pending-2346` targeting `feat/demo-164-chat-grounding-provenance-0900` in `/home/azureuser/source/ama-demo-wt/feat-1238-stale-pending-2346`, while verifying ACs 1-4 (single outcome-write retry after `Acknowledged` receipt, `receipt_ref` warning log when outcome write still fails, failed-write regression test coverage, and `reservation_id`-bound lookup instead of `attempts[-1]`), prohibiting bulk `del sys.modules[...]` in tests, validating in `src/core` (`mypy`, `ruff check . && ruff format --check .`, focused `unittest`), and committing locally with `Closes #1238` and the Copilot `Co-authored-by` trailer without pushing.
* Research and evidence considered: .copilot-tracking/research/2026-11-14/core-1238-stale-pending-2346-research.md, .copilot-tracking/plans/2026-11-14/core-1238-stale-pending-2346-plan.md, .copilot-tracking/details/2026-11-14/core-1238-stale-pending-2346-phase-details.md, src/core/src/zava_forward/core/resident_decisions.py, src/core/tests/test_resident_decisions.py, src/core/README.md.
* Decisions, dependencies, and acceptance criteria considered: FR-1 through FR-4, NFR-1, AC-1 through AC-5, Owner Decision Q6 (`manual_verified` two-person `service_supersede_authorize` without resending, 2026-11-08), focused validation tier classification under repository instructions, and local Python 3.12.3 `src/core` toolchain (`mypy`, `ruff`, `unittest` + `sqlite3`).
* Assessment boundary: Evaluates plan and phase-detail accuracy, state-machine completeness, JSON/SQLite atomicity and `validate_sql` replay safety, audit/idempotency/retention invariants, test isolation, and documentation consistency solely from the supplied artifacts and three target `src/core` files. Does not execute live test suites or inspect external SQL Server (`AzureResidentDecisions`) infrastructure.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| AC-1, AC-2, AC-3, AC-4, FR-4 (`C5`-`C9`) | Covered  | Verified directly in src/core/src/zava_forward/core/resident_decisions.py (`_forward` lines 822-852, `_record_outcome` lines 853-881, `_outcome_recorded` lines 884-891) and src/core/tests/test_resident_decisions.py (lines 3840-3849, 4006-4102); preserved by P02-T01 and P03-T01. |
| FR-1, FR-2, AC-5, P01, P01-T01 (`C3`, `C10`, `C11`) | Covered | In-place transition of prior `status == "Pending"` attempts to `"Superseded"` (`superseded_from="Pending"`, `superseded_at=now`, `superseded_by_attempt=attempt`) inside `_res_service_forward` runs under `store.lock` after all preconditions, replays cleanly on detached JSON row bodies in `validate_sql` (lines 540-559), rolls back cleanly on save/audit failure in `_operation` (lines 727-804), and leaves `"Unconfirmed"`, `"Failed"`, and `manual_verified` `"Superseded"` attempts untouched. |
| FR-3, P02, P02-T01 (`C12`, `C13`, `C14`) | Partial  | Multi-backend JSON/SQLite test plan (`JsonResidentDecisions` / `SqlResidentDecisions`), post-retry `["Superseded", "Acknowledged"]` update at line 4028, audit/idempotency assertions, and late-outcome fencing checks are thorough, but FR-3, P02, and P02-T01 reference a nonexistent method name `resident_retention_delete` instead of `delete_resident_records` (`PC-001`). |
| AC-5, P02-T02 (`C1`, `C10`, `C11`)       | Partial  | Targets src/core/README.md formal-route supersession prose, but does not call out qualifying the unconditional paragraph-2 sentences at lines 536-539 (`"stays Pending"` and omitting `"Superseded"` from the unresolved set) so consecutive paragraphs do not contradict each other (`PC-002`). |
| NFR-1, P03, P03-T01                      | Covered  | Enforces zero `del sys.modules[...]` usage and runs `python3 -m mypy`, `python3 -m ruff check . && python3 -m ruff format --check .`, focused `test_resident_decisions.py`, and full `src/core` `unittest` discovery. |
| Caller git/artifact constraints          | Covered  | Dated `.copilot-tracking/.../2026-11-14/core-1238-stale-pending-2346*` paths and post-review local commit on `fix/core-1238-stale-pending-2346` with `Closes #1238` and Copilot `Co-authored-by` trailer without pushing are recorded in User Decisions and Requirements and Scope. |

## Verdict

* Verdict: Revise
* Rationale: The core design for Issue #1238 AC 5 (low F3) is technically sound, surgical, and verified compatible with `_operation` rollback, SQLite `validate_sql` detached replay, `reservation_id` binding, `route_key` idempotency, late-outcome `receipt_ref` fencing, and Owner Decision Q6 (`manual_verified` dual-approval `service_supersede_authorize`). Two low-severity direct planner corrections (`PC-001` fixing the retention-deletion method name in FR-3 and P02/P02-T01, and `PC-002` aligning paragraph 2 and paragraph 3 wording in `src/core/README.md` under P02-T02) should be applied directly during plan readiness finalization before handing off to implementation. Neither finding requires user input or another critique pass.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Low]: Retention-deletion method symbol in FR-3 and P02-T01 is `delete_resident_records`, not `resident_retention_delete`

* Related IDs: FR-3, P02, P02-T01, C13
* Evidence: .copilot-tracking/plans/2026-11-14/core-1238-stale-pending-2346-plan.md, .copilot-tracking/details/2026-11-14/core-1238-stale-pending-2346-phase-details.md, src/core/src/zava_forward/core/resident_decisions.py:1084, src/core/tests/test_resident_decisions.py:4499
* Concern: FR-3, P02, and P02-T01 (following C13's summary label) name `resident_retention_delete` as the retention-scrubbing API to exercise in unit tests, whereas `ResidentDecisionMixin` defines `delete_resident_records(self, user, case_id, today=None)` at src/core/src/zava_forward/core/resident_decisions.py:1084 (which records audit action `"resident_retention_deleted"` at line 1103) and adjacent tests invoke `self.store.delete_resident_records(self.pam, "ZF-1", "2040-01-01")` at src/core/tests/test_resident_decisions.py:4499 and 4510.
* Impact: Implementing P02-T01 literally against `resident_retention_delete` raises `AttributeError` in test execution and leaves an inaccurate API identifier in FR-3's observable acceptance criterion.
* Smallest useful change: Replace `resident_retention_delete` with `delete_resident_records` in FR-3 and P02-T01 of .copilot-tracking/plans/2026-11-14/core-1238-stale-pending-2346-plan.md and in P02 and P02-T01 of .copilot-tracking/details/2026-11-14/core-1238-stale-pending-2346-phase-details.md.
* Action owner: planning_parent
* Exact resolving evidence: FR-3 and P02-T01 in .copilot-tracking/plans/2026-11-14/core-1238-stale-pending-2346-plan.md and P02 and P02-T01 in .copilot-tracking/details/2026-11-14/core-1238-stale-pending-2346-phase-details.md reference `delete_resident_records`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Low]: P02-T02 should reconcile paragraph 2 (`stays Pending` and unresolved statuses) alongside paragraph 3 in `src/core/README.md`

* Related IDs: AC-5, P02-T02, C1, C10, C11
* Evidence: .copilot-tracking/details/2026-11-14/core-1238-stale-pending-2346-phase-details.md, src/core/README.md:536-540, src/core/README.md:555-591, src/core/src/zava_forward/core/resident_decisions.py:1699
* Concern: P02-T02 describes adding prose on explicit `service_forward` (`retry_unresolved=True`) marking stale `Pending` attempts `Superseded`, but src/core/README.md:536-539 in the immediately preceding paragraph states unconditionally `"A send whose outcome could not be saved stays Pending. Pending, Unconfirmed and legacy Failed attempts without not_sent are unresolved"` (omitting `"Superseded"` from the unresolved list enforced at src/core/src/zava_forward/core/resident_decisions.py:1699 and leaving `"stays Pending"` unqualified).
* Impact: Appending retry-supersession prose solely in the `Pending supersession` paragraph without updating lines 536-539 leaves adjacent paragraphs in `src/core/README.md` making conflicting statements about whether a failed-outcome `Pending` attempt stays `Pending` after an explicit `retry_unresolved` reservation and which statuses count as unresolved.
* Smallest useful change: Clarify in P02-T02 of .copilot-tracking/details/2026-11-14/core-1238-stale-pending-2346-phase-details.md that both paragraph 2 (src/core/README.md:536-540) and paragraph 3 (src/core/README.md:555-595) are synchronized so paragraph 2 notes that a failed outcome save stays `Pending` until superseded (via `service_supersede_authorize` or an explicit `retry_unresolved` send reservation) and includes `Superseded` among unresolved statuses, while paragraph 3 contrasts `manual_verified` two-person supersession (no resend, records `supersession`) with explicit `retry_unresolved` reservation supersession (reserves superseding attempt and sets `superseded_by_attempt`).
* Action owner: planning_parent
* Exact resolving evidence: P02-T02 in .copilot-tracking/details/2026-11-14/core-1238-stale-pending-2346-phase-details.md explicitly scopes updating both src/core/README.md:536-540 and src/core/README.md:555-595.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Direct source verification confirms ACs 1-4 are intact and covered across JSON and SQLite backends (`_forward` `reservation_id` lookup, `_record_outcome` bounded two-attempt write loop without re-contacting the receiver, `_outcome_recorded` lost-commit reconciliation, and `WARNING` logging of `receipt_ref`).
* Placing the `"Pending"`-to-`"Superseded"` transition inside `_res_service_forward` after all version, route, closed-status, `Acknowledged`, `retry_unresolved is True`, `not in_flight`, actor-identity/independence, and `resident_request_ref` guards ensures atomic persistence, clean rollback under `_operation`, clean detached replay under `validate_sql`, immediate fencing of late `_res_service_forward_outcome` calls, and strict provenance separation from `manual_verified` `service_supersede_authorize` (`attempt["supersession"]`).
* Locked test-update scope in P02 (`test_forward_outcome_save_failure_leaves_pending_and_blocks_silent_resend` post-retry expectation updated from `["Pending", "Acknowledged"]` to `["Superseded", "Acknowledged"]`, plus at most 4 focused methods on `JsonResidentDecisions` inherited by `SqlResidentDecisions` with zero `del sys.modules[...]` usage) provides deterministic coverage across both local store backends, and new test methods should maintain full `mypy` type annotations consistent with `src/core/tests/test_resident_decisions.py`.
* Accepted residual risk: Per-instance `_IN_FLIGHT` tracking remains single-process as documented in `src/core/README.md:540` and `591`, and external SQL Server (`AzureResidentDecisions`) remains environment-gated locally while sharing `ResidentDecisionMixin` and `validate_sql` with `SqlResidentDecisions`.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Critique is read-only and evaluated static code, tests, documentation, research, plan, and phase details without executing `mypy`, `ruff`, or `unittest` or modifying repository files outside this critique artifact.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Apply direct planner corrections for PC-001 (`delete_resident_records` symbol in FR-3 and P02/P02-T01) and PC-002 (`src/core/README.md:536-540` and `555-595` synchronization in P02-T02), record the critique disposition, and finalize the plan as `ready` without another critique pass.
* User response required: no
