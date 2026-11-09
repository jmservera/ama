<!-- markdownlint-disable-file -->
# Review: issue-1294-validation-policy

## Scope and Evidence

* Task ID: issue-1294-validation-policy
* Review date: 2026-11-08
* Review scope: full task
* Assessed boundary: wording-only reconciliation of the local validation policy in four guide files plus log and issue record; candidate commit 8a5cab9f9cde3cc29d97a7b07faf12a338392ad9 on base fa7ae0c9770e890f82482456bfcb8e97f1e05429; evidence files added after it.
* Plan: .copilot-tracking/plans/2026-11-08/issue-1294-validation-policy-plan.md
* Phase details: .copilot-tracking/details/2026-11-08/issue-1294-validation-policy-phase-details.md
* Plan critique: .copilot-tracking/plans/critiques/2026-11-08/issue-1294-validation-policy-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-08/issue-1294-validation-policy-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-retry-research.md, .copilot-tracking/hve-builder/2026-11-08/issue-1294-validation-policy-behavior-report-1.md, .copilot-tracking/github-issues/issue-1294.md, first-attempt adverse research file (unchanged, SHA-256 7305e775...bf12d)

## Opening Review State

* Interpreted review goal: confirm the five issue acceptance criteria are met by the committed wording and evidence.
* Review scope: full task
* Evidence readiness: all artifacts present; plan markers ticked; changes record complete.
* Acceptance basis: issue #1294 criteria and plan PC-001..PC-009 dispositions.
* First comparison boundary: plan scope versus the diff against base.
* Active read-only boundaries: this review record only.
* Initial blockers: none.

## Execution Status

* Execution status: Complete
* Review execution evidence: 2026-11-08; lead compared plan, details, critique dispositions, changes record, git diff and behavior report. No bounded subagent lens was used.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|---|---|---|---|
| P01 | Policy edits, issue record, log entry | Reconciled | none |
| P02 | Checks, HVE static/behavior/host, freeze | Reconciled | Review and final evidence commit follow behavior-test commit (RV-002) |
| Follow-Up Items | Not changed section | Reconciled | CI harness hosting, zero-skip hosted selector, #470 timing remain open |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|---|---|---|---|---|---|
| P01 | .github/copilot-instructions.md, src/README.md, .github/agents/ama-backlog-delivery-coordinator.agent.md, docs/reference/method/tracking-retention-policy.md, docs/reference/log.md, .copilot-tracking/github-issues/issue-1294.md | Two-tier policy, CI-versus-local coverage section, examples | git diff vs base | diff check exit 0, link scan clean | reconciled |
| P02 | .copilot-tracking/hve-builder/2026-11-08/issue-1294-validation-policy-behavior-report-1.md | Static, behavior, host evidence | behavior report | simulation Pass (proxy) | reconciled with limits |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state |
|---|---|---|---|---|
| P02-T03 | Review and evidence commit ordered after behavior-test commit | Tester needs fixed revision; no user decision | Recorded in changes Divergences and plan task title | not needed; no material revision |

## Critique and Material Revision Assessment

* Latest critique dispositions: PC-001..PC-009 recorded in the plan; none needed a user decision; no second critique.
* Material revisions: none after critique.
* Dependent-work pause assessment: no early resumption.
* Justification assessment: supported.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|---|---|---|---|
| Host employee-chat harness in CI | Workflow change excluded by scope | owner/coordinator | open; distinct follow-up |
| Zero-skip verification of hosted chat selector | Workflow change excluded | owner/coordinator | open; distinct follow-up |
| Full-gate timing (#470) | Not delivered here | owner | open; distinct follow-up |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Behavior evidence is proxy-profile simulation

* Related scope: P02-T02
* Evidence: .copilot-tracking/hve-builder/2026-11-08/issue-1294-validation-policy-behavior-report-1.md
* Impact: supports wording conformance only; not intended-profile or native behavior. Scenarios were lead-authored; grader did not read the examples table; interrupted-receipt, workflow-change and resume paths untested.
* Destination: follow_up
* Smallest useful next action: optional native or higher-profile rerun including interrupted-run and workflow-change scenarios.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Commit sequencing deviates from plan

* Related scope: P02-T03
* Evidence: the plan expected review before the commit; the behavior-test commit preceded it so the tester had a fixed revision. Two commits result.
* Impact: none on content; the final HEAD, not 8a5cab9, is the candidate.
* Destination: follow_up
* Smallest useful next action: coordinator assesses the final exact head.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Hosted CI not observed

* Related scope: AC4/AC5
* Evidence: nothing pushed by design.
* Impact: applicable hosted CI result unknown; a documentation-only PR may have no Source CI run, and the ruleset lists no required checks (retrieved 2026-11-08).
* Destination: follow_up
* Smallest useful next action: record actual PR checks after publication; do not claim a pass if none ran.

## Defects

* none

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---|---|---|---|
| RV-001 | follow_up | owner | evidence-limit |
| RV-002 | follow_up | coordinator | process divergence |
| RV-003 | follow_up | coordinator | external observation |

Later implementation of a routed finding does not require another Review.

## Residual Work

* CI harness hosting, hosted zero-skip selector verification, #470 timing measurement, optional deeper behavior rerun.

## Blockers and Remaining Work

* Blockers: none
* Remaining active work: none

## Validation Evidence

| Command | Scope | Status | Summary |
|---|---|---|---|
| git diff --check | changed files | Passed | exit 0 |
| relative-link scan (python, no bytecode) | four changed guides | Passed | no broken links |
| read-only changed_groups / ci-affected.select reproduction | examples table | Passed | matched table |
| hve-builder-tester simulation plus independent grader | six scenarios | Passed (proxy) | 0 fix findings |
| hosted CI, full gate, native behavior | n/a | Unavailable | not pushed; focused tier; not run |

## Outcome

* Outcome: Residual work
* Outcome rationale: all five acceptance criteria are delivered by wording, no defects; residual items are distinct follow-ups and evidence limits.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
|---|---|---|
| Implementation defect | none | none |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | distinct follow-up | RV-001..003 and plan follow-ups |

* Execution status: Complete
* Outcome: Residual work
* Validation coverage: documentation checks and contained simulation only
* Blockers: none
