---
title: Issue 206 implementation changes
description: Lifecycle guard, exact-SHA recording and local validation evidence
ms.date: 2026-10-17
---

## Scope and Status

Task 206, issue-206-rubric-deleted-head. Full plan P01/P02 is authorized.
Implementation completed after Research and Plan completed, with PC-001..004
direct-compatible corrections applied. No source change predates these gates.

## P01: Recording Boundary

P01-T01/P01-T02 complete. Workflow checks current PR state before immutable
event-SHA checkout, before recording and before publication. Explicit closure
emits notices and skips all verdict effects. API errors/malformed responses
fail visibly. Initial/late movement and incomplete outcomes cannot pass.
Publication expects the bot SHA after push, otherwise the scored SHA only
after a successful no-commit path.

Recording installs an isolated workflow-owned pre-push hook and uses normal
non-force push to the explicit full branch ref. The hook accepts exactly one
update with correct local SHA/ref and advertised remote scored SHA. Local
temporary-remote experiments prove deletion, forward and backward movement
both before advertisement and after the hook's input are rejected without
recreation/overwrite/new_sha. Main remains unchanged.

The new single test module executes extracted source and compiled Node/shell
steps. Initial source-only test run: 68 passed, two fixture errors because a
synthetic forward commit was absent from the bare remote. Corrected the fixture
to transfer that object before moving its ref; no runtime workaround.
Intermediate focused run: 140 passed. Final expanded run: 159 passed in 21.55s.
Includes malformed API data, 404/403/500, closed boundaries, incomplete outcomes,
successful/no-commit publication, original/bot SHA targets and source/lock parity.

## P02: Compilation and Validation

Baseline before source edits:
`python3 -m pytest .github/rubric/scripts -q --tb=short`:
21 failed, 117 passed, 7 skipped in 3.55s.
Failures: eight historical gate-seed expectations, one prepare/gate seed
expectation, ten historical source-path workflow-filter fixtures, and two
adapter/seed expectations. Seven real MCP runtime tests skip without the
external pinned runtime. No failure will be silently suppressed or repaired
outside scope.

P02-T01 complete. Updated `.github/rubric/README.md` with exact lifecycle,
API-error and push-race behavior, limitations and focused test command. No KB
file was added or changed, so KB index/log changes are not applicable.

| Validation | Result |
| --- | --- |
| `gh aw compile rubric-score --no-check-update` | Passed with installed v0.89.21; source and generated lock both included |
| Compiler repeatability | Passed: lock SHA-256 f71a65912be7d5fb949b86d7a23701b50ecae820c8172ef89bdc31d8ffb8658b before/after repeat |
| Focused `python3 -m pytest .github/rubric/scripts/test_record_workflow.py -q --tb=short` | 159 passed in 21.55s |
| Full `python3 -m pytest .github/rubric/scripts -q --tb=short` | 21 failed, 276 passed, 7 skipped in 22.26s |
| Exact failing-node baseline comparison | Passed: identical 21 failure IDs; no new failures, 159 added passing cases |
| Parsed baseline/source/lock invariant audit | Passed: all other jobs, names, permissions, pins/container/secret manifest, prompt/model, scoring inputs, trusted tool loading and gate execution unchanged |
| `git diff --check` | Passed |
| Live scoring / workflow dispatch | Not run, prohibited for validation |
| Real pinned MCP runtime | Seven existing tests skipped because external runtime unavailable; generated schema tests did run |

Compiler emitted existing action-version upgrade notices; pins were deliberately
preserved. It reported one compilation succeeded, zero compiler warnings.

### Exact Pre-existing Failing Node IDs

All paths below are under `.github/rubric/scripts/`; these IDs match the
pre-edit run exactly:

```text
test_gate.py::test_given_seed_baseline_when_summed_then_total_is_66
test_gate.py::test_given_equal_scores_when_evaluated_then_passes
test_gate.py::test_given_unknown_criterion_when_evaluated_then_fails_with_actionable_error
test_gate.py::test_given_supported_drop_when_evaluated_then_fails_with_warning
test_gate.py::test_given_change_without_changed_evidence_when_evaluated_then_baseline_kept
test_gate.py::test_given_closed_criterion_when_agent_changes_it_then_carried_forward
test_gate.py::test_given_drop_citing_removed_file_when_evaluated_then_fails
test_gate.py::test_given_increase_citing_removed_file_when_evaluated_then_baseline_kept
test_prepare.py::test_given_pr_deleting_scored_file_when_gated_then_drop_counts
test_safe_output_runtime.py::test_tracking_only_changes_do_not_trigger_workflows[pull_request-infra-plan.yml]
test_safe_output_runtime.py::test_tracking_only_changes_do_not_trigger_workflows[pull_request-mvp-ci.yml]
test_safe_output_runtime.py::test_tracking_only_changes_do_not_trigger_workflows[pull_request-mvp-validation.yml]
test_safe_output_runtime.py::test_tracking_only_changes_do_not_trigger_workflows[pull_request-src-ci.yml]
test_safe_output_runtime.py::test_tracking_only_changes_do_not_trigger_workflows[pull_request-src-deploy.yml]
test_safe_output_runtime.py::test_tracking_only_changes_do_not_trigger_workflows[push-infra-plan.yml]
test_safe_output_runtime.py::test_tracking_only_changes_do_not_trigger_workflows[push-mvp-ci.yml]
test_safe_output_runtime.py::test_tracking_only_changes_do_not_trigger_workflows[push-mvp-validation.yml]
test_safe_output_runtime.py::test_tracking_only_changes_do_not_trigger_workflows[push-src-ci.yml]
test_safe_output_runtime.py::test_tracking_only_changes_do_not_trigger_workflows[push-src-deploy.yml]
test_scorecard_adapter.py::test_complete_card_round_trips_without_mutating_baseline
test_scorecard_adapter.py::test_gate_incremental_carry_forward_and_calibration_leave_baseline_unchanged
```

## Criterion and Evidence Audit

| Criterion | Result | Exact evidence |
| --- | --- | --- |
| AC1 | Met | Research C1/W2/W3: #204 closed before failure, current mutable checkout not fixed |
| AC2 | Met locally | `test_lifecycle_classifies_explicit_state`, `test_closed_at_publication_has_no_verdict_side_effects`, `test_conditions_wire_obsolete_and_error_outcomes` |
| AC3 | Met locally | `test_publication_requires_valid_checks_and_exact_resulting_head`, `test_successful_no_commit_record_keeps_scored_head`, unchanged real-push cases |
| AC4 | Met locally | `test_real_record_push_never_recreates_or_overwrites_moved_head`, `test_verification_retains_initial_moved_signal_and_exact_checkout`, hook invalid-input cases |
| AC5 | Met locally | `test_api_failure_is_not_obsolete_or_success`, `test_malformed_api_success_fails_closed`, incomplete-outcome publication cases |
| AC6 | Met | Parsed invariants audit and `test_canonical_and_generated_recording_code_match`; gate source and baseline untouched |
| AC7 | Met with existing suite failures disclosed | Compiler/targeted/full run and exact failing-node comparison above |
| AC8 | Pending Review and publication | Required next stages, not inferred from implementation |

## Amendments, Divergences and Blockers

No material divergence or implementation blocker. No live scoring, paid inference, private data, environment files,
Azure changes or excluded workstreams.

## Review Handoff

P02-T02 complete. Full implementation scope P01/P02 is complete; no remaining
active-plan implementation task. Plan markers, details, changes, blockers,
baseline follow-up and validation are current. Ready for one Review. Existing
fixture failures remain a separate follow-up, not an overall green suite.
Residual boundary: PR closure/head movement after the last API read is not
atomic with a Git write or publication; exact ref compare-and-update and exact
status/review SHAs are tested. No live-run success or human approval claimed.

## P03 Integration Opening (2026-10-17)

Bounded caller-authorized continuation: preserve reviewed febd357 feature bytes,
rebase the run-owned branch onto fetched d890e3d, validate and inspect integration,
then publish once using an explicit old-head lease. Research/Plan verification
reuses prior repair evidence and critique; no executable changes are planned.
Initial worktree was clean. A local preflight checkpoint preserves phase state
without stashing or moving uncommitted work across rebase.

## P03 Integration Results (2026-10-17)

Rebased cleanly onto d890e3de29e24cb26c2eff35af9a6e125a3b541e.
No conflicts or conflict resolution. Original repair 4fe3b31 became c29c118;
delivery record febd357 became 1dda6cc. Range-diff marks both equal, with only
the new preflight checkpoint a8fc10f added. No executable changes were needed.
All inherited main files remain byte-identical to d890e3d; the integrated diff
is restricted to the original four feature paths and this task's tracking.

Canonical bytes are exactly identical to reviewed febd357, including the entire
.github/rubric directory. Recorded SHA-256 values:

| Path | SHA-256 |
| --- | --- |
| .github/workflows/rubric-score.md | a3f4cf3f41c0feb196dbac6013d8dbcf8ce33baa54e3b60d9549584fda7524f3 |
| .github/workflows/rubric-score.lock.yml | f71a65912be7d5fb949b86d7a23701b50ecae820c8172ef89bdc31d8ffb8658b |
| .github/rubric/scripts/test_record_workflow.py | 4150668f6423119a600b07f15f29c13d299b6a84b717fe88263be73fb433a63a |
| .github/rubric/README.md | e2280262bca358b230f8fcb47d4e8ca432b5cda40f4b5b3a945c6541a9cc259a |

| Integration validation | Result |
| --- | --- |
| Focused test_record_workflow | 159 passed in 15.26s |
| Full rubric suite | 21 failed, 276 passed, 7 skipped in 18.28s |
| Exact baseline failing-node comparison | Identical set of all 21 IDs listed above; no new or removed failures |
| gh aw compile rubric-score --no-check-update --no-emit | Passed |
| Two gh aw compile rubric-score --no-check-update executions | Passed; lock hash above unchanged after each |
| Parsed source/lock comparison against d890e3d | Names, permissions, action refs, inputs, prompt, other jobs and top-level settings preserved |
| git diff --check | Passed |
| Hosted final-head CI / live scoring dispatch | Not run; prior successful run 39017650712 targets old febd357 only |

Compiler retained existing newer-action notices; no pins were upgraded.
The first ad hoc invariant probe incorrectly used the compiled underscore job
key in canonical YAML and asserted; the corrected probe used canonical
record-rubric-score and passed. No product change or weakened assertion.
No fixture failure was fixed or suppressed. External-runtime skips remain
limitations, not passes. Score semantics, permissions and safety boundaries
are unchanged. No live inference, Azure, credentials/private-data access or
external source upload was used for validation; gh identity lookup was the
explicitly authorized authenticated-account metadata check.

P03-T01/T02 and all local implementation markers are reconciled. No remaining
implementation item or blocker. Integration Review assesses only the new
base/replay boundary; the original repair Review and critique remain historical.
Parent publication and final remote/PR verification follow that assessment.
