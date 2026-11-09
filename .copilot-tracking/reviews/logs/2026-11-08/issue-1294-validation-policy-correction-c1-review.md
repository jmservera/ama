<!-- markdownlint-disable-file -->
# Review: issue-1294-validation-policy-correction-c1

## Scope and Evidence

* Task ID: issue-1294-validation-policy-correction-c1
* Review date: 2026-11-08
* Review scope: full correction task (independent review findings F1-F4 against HEAD 397ce435ae4dddfcf9279179656049b8b670b720)
* Assessed boundary: wording-only edits to src/README.md, .github/copilot-instructions.md, .github/agents/ama-backlog-delivery-coordinator.agent.md and docs/reference/log.md, plus the correction RPI and HVE evidence; the earlier review, plan, changes, behavior report 1, first-attempt research and tools/__pycache__ preserved. No workflow, tool, source, SQL, infrastructure or dependency file changed.
* Plan: .copilot-tracking/plans/2026-11-08/issue-1294-validation-policy-correction-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-08/issue-1294-validation-policy-correction-c1-phase-details.md
* Plan critique: .copilot-tracking/plans/critiques/2026-11-08/issue-1294-validation-policy-correction-c1-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-08/issue-1294-validation-policy-correction-c1-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-correction-c1-research.md, .copilot-tracking/hve-builder/2026-11-08/issue-1294-validation-policy-behavior-report-2.md, .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-2, the earlier review .copilot-tracking/reviews/logs/2026-11-08/issue-1294-validation-policy-review.md (preserved unchanged)

## Opening Review State

* Interpreted review goal: confirm findings F1-F4 of the independent review are corrected without widening policy.
* Review scope: full correction task
* Evidence readiness: all artifacts present; plan markers P01-P02 ticked; changes record complete.
* Acceptance basis: plan AC1-AC5 and critique dispositions PC-001..PC-006.
* First comparison boundary: plan scope versus git diff against HEAD 397ce435a.
* Active read-only boundaries: this review record only.
* Initial blockers: none.

## Execution Status

* Execution status: Complete
* Review execution evidence: 2026-11-08; lead compared plan, details, critique dispositions, changes record, diff, runner and workflow lines, and behavior report 2. No bounded subagent lens used beyond the behavior-test design and grading subagents.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|---|---|---|---|
| P01-T01 | README coverage sections and direct-check contract | Reconciled | none |
| P01-T02 | Impact-based classification in three files | Reconciled | none |
| P01-T03 | Log correction entry | Reconciled | none |
| P02-T01 | Link, diff, ASCII, stale-phrase and selection checks | Reconciled | ci-affected docs/reference output noted as not Source CI evidence |
| P02-T02 | Behavior run 2 | Reconciled with limits | proxy profile; post-grade edits not re-simulated (RV-001) |
| P03 | Changes record, this review, commit | Reconciled by the commit that follows this record | commit follows this review |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|---|---|---|---|---|---|
| P01 | src/README.md, .github/copilot-instructions.md, .github/agents/ama-backlog-delivery-coordinator.agent.md, docs/reference/log.md | F1 contract, F2 labels, F3 impact classification | git diff vs 397ce435a | diff check exit 0, ASCII 0, stale grep none, links no new break | reconciled |
| P02 | .copilot-tracking/hve-builder/2026-11-08/issue-1294-validation-policy-behavior-report-2.md | F4 independent design, honest profile, independent grading, retained sandbox | behavior report 2 and sandbox | simulation Revise (proxy), one Medium correction applied | reconciled with limits |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state |
|---|---|---|---|---|
| P01-T01 / README table row | `--changed` description narrowed to the actual tooling selection | Read-only reproduction of changed_groups; no user decision | changes record Divergence | not needed |
| P01-T01 / README Shared bullet | Working-data guard placement corrected after grader finding 1 | Behavior report 2 finding 1; no user decision | changes record Post-grade correction | not needed |

## Critique and Material Revision Assessment

* Latest critique dispositions: PC-001..PC-006 applied directly in plan and details; none needed a user decision; no second critique.
* Material revisions: none.
* Dependent-work pause assessment: no early resumption.
* Justification assessment: supported.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|---|---|---|---|
| Single wrapper or CI hosting for the direct employee-chat check | Needs owner direction and workflow change | Owner | open, distinct follow-up |
| Rubric workflow applicability, disabled what-if status, approved-control-change procedure, shared-check expectation for focused tier | Policy widening beyond F1-F4 | Owner | open, distinct follow-up |
| #470 full-gate timing | Separate unmeasured criterion | #470 | open |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Behavior evidence is proxy and the final wording was not re-simulated

* Related scope: P02-T02
* Evidence: .copilot-tracking/hve-builder/2026-11-08/issue-1294-validation-policy-behavior-report-2.md
* Impact: executed model unknown (host forbids a model override), so no intended-profile claim; grader verdict Revise; three post-grade wording edits were verified only by reading the workflow and runner, not by a second simulation.
* Destination: follow_up
* Smallest useful next action: rerun the behavior test with an explicit Medium model when permitted and re-simulate S12 and S05.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: ci-affected output for docs-only paths is not Source CI evidence

* Related scope: P02-T01
* Evidence: /tmp/c1-evidence/selection.txt (ci-affected reports all projects for docs/reference/README.md while the guide says that path is outside the workflow path filter)
* Impact: the guide's path-filter statement rests on the workflow `paths:` filter, which was read and not observed on GitHub; hosted CI is unobserved.
* Destination: follow_up
* Smallest useful next action: confirm on the first published PR which workflows start.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Executor-identified policy gaps remain open

* Related scope: Follow-Up Items
* Evidence: behavior report 2 Findings section
* Impact: ambiguity about rubric applicability, disabled what-if, approved control change and shared local checks for the focused tier.
* Destination: follow_up
* Smallest useful next action: owner decision before any further policy edit.

## Defects

* none

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---|---|---|---|
| RV-001 | follow-up | Coordinator or owner | evidence limit, not a wording defect |
| RV-002 | follow-up | Coordinator at publication | hosted observation |
| RV-003 | follow-up | Owner | policy widening |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Intended-profile behavior rerun, hosted CI observation, wrapper or CI hosting of the direct harness check.

## Blockers and Remaining Work

* Blockers: none for the local candidate. Publication requires independent exact-head assessment, human approvals and observed hosted CI.
* Remaining active work: none.

## Validation Evidence

| Command | Scope | Status | Summary |
|---|---|---|---|
| git diff --check | changed files | Passed | exit 0 |
| relative link and anchor scan (PYTHONDONTWRITEBYTECODE=1) | four changed files | Passed | no new broken link; pre-existing historical breaks in docs/reference/log.md untouched |
| ASCII scan of added lines | git diff | Passed | 0 non-ASCII lines |
| stale-phrase grep | .github, src/README.md, docs/reference/method | Passed | no matches |
| changed_groups and ci-affected select reproduction | nine synthetic paths | Passed | /tmp/c1-evidence/selection-local.txt and selection.txt |
| HVE behavior test run 2 (simulation, proxy) | three policy files | Revise | independent grader; one Medium correction applied |
| tools/rpi-checks.py --changed or --all | not run | Skipped | focused tier; no blanket run claimed |
| hosted CI | not observed | Unavailable | no push or PR |

## Outcome

* Outcome: Residual work
* Outcome rationale: F1-F4 are corrected in wording and checked against the runner, harness and workflow; remaining items are evidence limits (proxy behavior profile, unobserved hosted CI) and owner policy follow-ups, none a defect in the correction.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
|---|---|---|
| Implementation defect | none | none |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | RV-001 intended-profile rerun is a distinct follow-up |
| Non-blocking residual work | distinct follow-up | RV-001, RV-002, RV-003 |

* Execution status: Complete
* Outcome: Residual work
* Validation coverage: focused local checks plus proxy-profile behavior simulation; no hosted CI
* Blockers: none
