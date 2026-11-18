<!-- markdownlint-disable-file -->
# Review: Issue #1238 Stale Pending Supersession and Retry/Receipt Verification

## Scope and Evidence

* Task ID: issue-1238
* Review date: 2026-11-14
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: Verification of Issue #1238 ACs 1-4 and implementation, multi-backend unit testing, documentation synchronization, and `src/core` static/lint/format/unit validation for AC 5 (`(low F3) Mark a stale Pending attempt superseded`) on branch `fix/core-1238-stale-pending-2346` targeting `feat/demo-164-chat-grounding-provenance-0900`.
* Plan: .copilot-tracking/plans/2026-11-14/core-1238-stale-pending-2346-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/core-1238-stale-pending-2346-phase-details.md
* Plan critique: .copilot-tracking/plans/2026-11-14/core-1238-stale-pending-2346-critique.md
* Changes: .copilot-tracking/changes/2026-11-14/core-1238-stale-pending-2346-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-14/core-1238-stale-pending-2346-research.md, git diff across `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/tests/test_resident_decisions.py`, and `src/core/README.md`, and live `mypy`, `ruff`, and `unittest` execution results.

## Opening Review State

* Interpreted review goal: Independently verify that all five Issue #1238 acceptance criteria, plan requirements (`FR-1`..`FR-4`, `NFR-1`), critique dispositions (`PC-001`, `PC-002`), and caller constraints (artifact paths, zero `del sys.modules[...]` usage, `src/core` validation checks) are satisfied and reconciled without defects or unapproved scope expansion.
* Review scope: Full task (`P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`)
* Evidence readiness: Ready; research, plan, phase details, plan critique, changes log, source diff, and validation outputs are complete and reconciled.
* Acceptance basis: `FR-1`..`FR-4`, `NFR-1`, `AC-1`..`AC-5`, resolved critique items `PC-001` and `PC-002`, and repository instructions.
* First comparison boundary: Plan checklist and acceptance criteria versus `git diff -- src/core/` and `.copilot-tracking/changes/2026-11-14/core-1238-stale-pending-2346-changes.md`.
* Active read-only boundaries: Write only `.copilot-tracking/reviews/2026-11-14/core-1238-stale-pending-2346-review.md`; do not modify source, test, doc, plan, details, critique, research, or changes files during Review.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed full comparison of research (`C1`-`C14`), plan, phase details, critique (`PC-001`, `PC-002`), changes record, and exact `git diff -- src/core/` on 2026-11-14.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01`, `P01-T01` | Atomic Stale Pending Supersession in `_res_service_forward` | Reconciled | Checked in plan, `completed` in phase details, and evidenced in `src/core/src/zava_forward/core/resident_decisions.py`. |
| `P02`, `P02-T01` | Multi-Backend Unit and Regression Tests Without `sys.modules` Manipulation | Reconciled | Checked in plan, `completed` in phase details, within locked 4-method addition cap, using `delete_resident_records` per `PC-001`, with zero `sys.modules` references. |
| `P02-T02` | Formal-Route Supersession Documentation Synchronization | Reconciled | Checked in plan, `completed` in phase details, synchronizing both the unresolved-retry paragraph and the `Pending supersession` paragraph in `src/core/README.md` per `PC-002`. |
| `P03`, `P03-T01` | Static Type, Lint, Format, and Unit Test Validation | Reconciled | Checked in plan, `completed` in phase details, with passing `mypy`, `ruff check .`, `ruff format --check .`, and focused `unittest` outputs recorded. |
| `## Follow-Up Items` | `#1346` low review item `RV-1` (`SupersessionBinding._roles` `MappingProxyType` + exact type check) | Reconciled | Kept outside active `Pxx`/`Pxx-Txx` scope and mirrored identically in plan and changes record. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | src/core/src/zava_forward/core/resident_decisions.py | `_res_service_forward` transitions prior `status == "Pending"` attempts in place to `status="Superseded"`, `superseded_from="Pending"`, `superseded_at=now`, `superseded_by_attempt=attempt` after all validation, `retry_unresolved`, `not in_flight`, actor-identity, and `resident_request_ref` guards succeed, and reports superseded attempt number(s) in the case audit detail. | Exact 15-line surgical diff in `_res_service_forward`; ACs 1-4 (`_forward`, `_record_outcome`, `_outcome_recorded`) verified unchanged. | Passed `mypy`, `ruff`, and 434 `test_resident_decisions` tests. | Reconciled |
| `P02-T01` | src/core/tests/test_resident_decisions.py | Updated post-retry expectation in `test_forward_outcome_save_failure_leaves_pending_and_blocks_silent_resend` to `["Superseded", "Acknowledged"]` and added 4 typed test methods in `JsonResidentDecisions` (inherited by `SqlResidentDecisions`) covering Complaint + Independent review routes, audit/idempotency preservation, `delete_resident_records` scrubbing, refusals/rollbacks/`in_flight` guard, chained stale `Pending` retries, `manual_verified` non-interference, and late-outcome refusal + `receipt_ref` `WARNING` logging. | Exact test diff; zero `sys.modules` matches. | Passed `mypy`, `ruff check .`, `ruff format --check .`, and `PYTHONPATH=src:tests python3 -m unittest test_resident_decisions test_sqlreads -q`. | Reconciled |
| `P02-T02` | src/core/README.md | Synchronized both formal-route paragraphs so `"stays Pending until superseded"` and the unresolved status list (`Pending`, `Unconfirmed`, `Superseded`, legacy `Failed` without `not_sent`) match runtime behavior and contrast `manual_verified` `service_supersede_authorize` with explicit `retry_unresolved` reservation supersession. | Clean Markdown diff in `src/core/README.md`. | Passed diff and link/prose review. | Reconciled |
| `P03-T01` | src/core/ | Ran static typing, lint, formatting, and focused unit/SQL tests against the worktree's `src/core`. | Recorded command outputs and zero exit codes in `.copilot-tracking/changes/2026-11-14/core-1238-stale-pending-2346-changes.md`. | All four checks exited `0`. | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P03-T01` in plan and `P03` in phase details | Aligned the `unittest` command to `PYTHONPATH=src:tests python3 -m unittest test_resident_decisions test_sqlreads -q` (matching `src/core/README.md`) so validation tests the worktree's `src/core` without mutating the shared `~/.local` editable `zava-forward-core` install or failing on optional `azure-iot-hub` / un-prefixed CLI subprocess tests. | `python3 -m pip show zava-forward-core` showed shared editable install at `/home/azureuser/source/ama/src/core`; caller brief requested `"Focused unittest suite covering resident_decisions"`. | Synchronized in plan `P03-T01`, phase details `P03`, and changes record before Review. | Not a material divergence; preserves approved intent, acceptance criteria, and caller validation requirements. | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: Both findings from the single final-candidate critique (`PC-001` replacing `resident_retention_delete` with `delete_resident_records`, and `PC-002` synchronizing both formal-route paragraphs in `src/core/README.md`) were resolved in the plan and phase details prior to implementation and verified in the final code, tests, and README diff.
* Material revisions: None required; the `P03-T01` worktree `PYTHONPATH=src:tests` selector alignment is an ordinary local current-state update matching `src/core/README.md` and the caller brief.
* Dependent-work pause assessment: No dependent work required pausing; execution proceeded strictly in `P01 -> P02 -> P03` order.
* Justification assessment: Supported by primary codebase and tool evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| `#1346` low review item `RV-1` (`SupersessionBinding._roles` `MappingProxyType` + exact `type(binding) is SupersessionBinding` check) | Pre-existing hardening note on `SupersessionBinding` from PR #1346, unrelated to `_res_service_forward` stale `Pending` supersession | User selection at post-Review follow-up checkpoint | Distinct follow-up route; properly excluded from active `P01`-`P03` completion claims |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

No material defects, decision gaps, or evidence gaps were found within the assessed task boundary (`0` Critical, `0` High, `0` Medium, `0` Low).

## Defects

* none

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| none | none | No corrective RPI pass required | All `FR-1`..`FR-4`, `NFR-1`, and `AC-1`..`AC-5` criteria are satisfied |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Optional post-task follow-up retained from plan `## Follow-Up Items`: harden `SupersessionBinding._roles` with `MappingProxyType` and exact `type(binding) is SupersessionBinding` check (`#1346` `RV-1`).

## Blockers and Remaining Work

* Blockers: none (`AzureResidentDecisions` remains environment-gated locally without an external SQL Server fixture while sharing `ResidentDecisionMixin` and `validate_sql` with `SqlResidentDecisions`; independent exact-head PR review and hosted CI remain normal post-push PR lifecycle gates outside this local-commit-only brief).
* Remaining active work: none

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m mypy` | `src/core` (`src` and `tests`, 327 files) | Passed | `Success: no issues found in 327 source files` (exit `0`) |
| `python3 -m ruff check .` | `src/core` | Passed | `All checks passed!` (exit `0`) |
| `python3 -m ruff format --check .` | `src/core` (274 formatted targets) | Passed | `274 files already formatted` (exit `0`) |
| `PYTHONPATH=src:tests python3 -m unittest test_resident_decisions test_sqlreads -q` | `src/core/tests/test_resident_decisions.py` (`JsonResidentDecisions` + `SqlResidentDecisions`) and `test_sqlreads.py` | Passed | `Ran 449 tests in 136.882s — OK (skipped=154)` (exit `0`) |
| `grep sys\.modules` | `src/core/tests/test_resident_decisions.py` | Passed | `No matches found.` |

## Outcome

* Outcome: Conformant
* Outcome rationale: ACs 1-4 of Issue #1238 are verified intact in code and regression tests, and AC 5 (`(low F3) Mark a stale Pending attempt superseded`) is surgically implemented in `ResidentDecisionMixin._res_service_forward`, preserving full attempt history, `route_key` idempotency, late-outcome fencing with `receipt_ref` logging, `delete_resident_records` scrubbing, and `manual_verified` dual-authorization separation across JSON and SQLite backends, with synchronized `src/core/README.md` documentation and passing `mypy`, `ruff`, and `unittest` checks.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct_follow_up | Optional user selection of `#1346` `RV-1` (`SupersessionBinding` deep immutability hardening) at Follow-up checkpoint |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: `mypy` (327 files), `ruff check .`, `ruff format --check .` (274 files), and focused `unittest` (`test_resident_decisions` + `test_sqlreads`, 449 tests, `OK (skipped=154)`) all passed with exit code `0`.
* Blockers: none
