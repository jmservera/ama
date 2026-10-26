<!-- markdownlint-disable-file -->
# Review: Offline demo-feedback acceptance harness (Refs #350)

## Scope and Evidence

* Task ID: issue-350-demo-feedback-harness
* Review date: 2026-10-22
* Review scope: full task (P01, P02 complete; P03 validation and publication follow this review)
* Assessed boundary: tools/check-demo-feedback.py and tools/test_check_demo_feedback.py at commit 3861547f against the plan requirements; offline only, no deployed acceptance, #349/#360/#350 criteria unmet.
* Plan: .copilot-tracking/plans/2026-10-22/issue-350-demo-feedback-harness-plan.md
* Phase details: .copilot-tracking/details/2026-10-22/issue-350-demo-feedback-harness-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-22/issue-350-demo-feedback-harness-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-22/issue-350-demo-feedback-harness-changes.md
* Other evidence considered: .copilot-tracking/research/2026-10-22/issue-350-demo-feedback-harness-research.md; runtime sources src/core/src/zava_forward/core/{projection,taskqueues,ledger,store}.py and src/api/src/zava_forward/api/{server,workbench}.py read for schema fidelity.

## Opening Review State

* Interpreted review goal: judge whether the checker honours the contract (four states, no denial-as-success, real schemas, no broad catches, offline) and whether artifacts reconcile.
* Review scope: full task
* Evidence readiness: all artifacts and the committed diff available.
* Acceptance basis: plan Functional/Non-Functional requirements and Acceptance Criteria.
* First comparison boundary: plan requirements versus code and tests.
* Active read-only boundaries: this review record only.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: 2026-10-22, direct read of both new files, the changes record, plan, details and runtime sources; focused tests re-run (45 OK). Full gate is run after this review, as planned in P03-T01.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|---|---|---|---|
| P01-T01 | Offline checker | Reconciled | Loader, report, exit codes implemented |
| P01-T02 | Offline checker | Reconciled | Five checks plus two permanent gaps |
| P02-T01 | Focused tests | Reconciled | See RV-001 on fixture provenance |
| P03-T01 | not yet in scope | Partial | Gate, receipt, PR follow this review |
| Follow-Up Items | none | Reconciled | Plan lists none |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|---|---|---|---|---|---|
| P01 | tools/check-demo-feedback.py | New standalone checker | CLI no-evidence exits 3 | Ruff targeted passed | Reconciled |
| P02 | tools/test_check_demo_feedback.py | 45 tests incl. AST handler check | 45 OK | Passed | Reconciled with RV-001 gap |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|---|---|---|---|---|---|
| P01-T02 image_identity | Pass needs an independent expected digest | PC-003; none | Plan text consistent | Not needed | Reconciled; plan prose could state it explicitly (RV-004) |
| P03-T01 Ruff | Isolated rule selection instead of environment defaults | Ruff output; none | Recorded in changes | Not needed | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: PC-001..PC-007 all resolved in the plan; code follows PC-001 (bare POST record), PC-002 (no pass exit), PC-003, PC-004 (80-char truncation, held outcome, counts/staff), PC-005 (AST test), PC-006 (lazy import).
* Material revisions: none; no user decision required.
* Dependent-work pause assessment: no early resumption.
* Justification assessment: supported.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|---|---|---|---|
| none | n/a | n/a | n/a |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Case-write and AI fixtures are hand-assembled, not produced by the runtime

* Related scope: P02-T01
* Evidence: tools/test_check_demo_feedback.py builds `case_write()` contacts and `ai_record()` as literals; only `/api/me`, navigation, work queues, ledger report and `Store.REC_LABEL` come from runtime builders. The plan acceptance criterion asked for runtime builders.
* Impact: a runtime change to the contact or recommendation shape would not break these fixtures, so schema drift would go unnoticed.
* Destination: rpi-implement (later, user-selected)
* Smallest useful next action: drive a real `Store` over a tiny synthetic dataset through `log_call`, `detail` and `ai_priority` (template path only, no paid AI) to generate the fixtures.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Per-check `pass` for fixture origin is shape-only but the report does not say so per check

* Related scope: P01-T02
* Evidence: tools/check-demo-feedback.py `build_report` emits `status: pass` for fixture checks; scope is conveyed only by `evidence_origin`, `acceptance` and `self_declared`.
* Impact: a reader of one check row could mistake a fixture pass for a deployed pass.
* Destination: rpi-implement
* Smallest useful next action: add a per-check `scope` (`contract-shape-only` or `captured`).

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Write response and a few edge cases are not fully checked

* Related scope: P01-T02
* Evidence: `check_case_write` counts the write response contacts but does not compare its last contact to the request; the loader accepts JSON `NaN` and reads the file after a separate size check.
* Impact: marginal false-pass or robustness gaps; none lets denial count as success.
* Destination: rpi-implement
* Smallest useful next action: compare the write-response last contact, reject non-finite constants and read with a bounded `read(MAX+1)`.

<!-- rpi:review id=RV-004 -->
### RV-004 [Low]: Test module is not discovered by the unchanged gate

* Related scope: P03-T01
* Evidence: plan "What You May Not Know" and src/README.md local gate matrix; the module is run directly and recorded.
* Impact: future regressions in the checker are not caught by the gate.
* Destination: follow-up (a deliberate change to tools/rpi-checks.py is outside this slice's ownership)
* Smallest useful next action: owner decides whether to register the module in the gate matrix.

## Defects

* None blocking. RV-002 and RV-003 are low-severity improvements routed to rpi-implement.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---|---|---|---|
| RV-001 | rpi-implement | Generate fixtures from a real Store | evidence-fidelity improvement |
| RV-002 | rpi-implement | Add per-check scope | clarity of report |
| RV-003 | rpi-implement | Tighten write check and loader | robustness |
| RV-004 | follow-up | Owner decision on gate registration | ownership boundary |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Live capture, spend-bound evidence, fixed administrator account and deployed parity depend on #349 and #360 and stay not-run; all original #350 acceptance criteria remain unmet.

## Blockers and Remaining Work

* Blockers: none for this slice.
* Remaining active work: P03-T01 (full gate, receipt verification, push, draft PR).

## Validation Evidence

| Command | Scope | Status | Summary |
|---|---|---|---|
| python -m unittest tools.test_check_demo_feedback -q (venv) | new tools | Passed | 45 tests OK |
| ruff check --isolated --select E,F,W,B,BLE,I --ignore E501 (0.17.1) | new tools | Passed | clean |
| tools/rpi-checks.py --all and --verify-receipt | repository | Unavailable at review time | run after this review on the committed head |

## Outcome

* Outcome: Residual work
* Outcome rationale: the implemented contract matches the plan with no blocking defect; low-severity findings and fixture provenance are routed to later work, and deployed acceptance remains blocked on #349/#360.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
|---|---|---|
| Implementation defect | rpi-implement (RV-001..RV-003, non-blocking) | user-selected follow-up |
| Decision gap or invalid assumption | none | n/a |
| Material evidence gap | none | n/a |
| Non-blocking residual work | RV-004 and #349/#360 dependent evidence | owner |

* Execution status: Complete
* Outcome: Residual work
* Validation coverage: focused tests and targeted Ruff passed; full gate pending
* Blockers: none
