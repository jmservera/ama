---
title: Issue 350 feedback correction4 review
description: One review of strict JSON types and explicit publication blockers
ms.date: 2026-10-22
---

## Scope and Evidence

Task ID: issue-350-demo-feedback-correction4.
Scope: the complete bounded correction4 task, not whole issue #350.

* Research: .copilot-tracking/research/2026-10-22/issue-350-demo-feedback-correction4-research.md
* Plan: .copilot-tracking/plans/2026-10-22/issue-350-demo-feedback-correction4-plan.md
* Details: .copilot-tracking/details/2026-10-22/issue-350-demo-feedback-correction4-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-22/issue-350-demo-feedback-correction4-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-22/issue-350-demo-feedback-correction4-changes.md
* Source: tools/check-demo-feedback.py and tools/test_check_demo_feedback.py.
* Runtime authority: server `/api/me`/tile_config and auth provider account methods.
* Local validation: external synthetic test log and full-gate console.

## Opening Review State

Goal: assess field typing against actual runtime without expanding content
policy or acceptance. Initial boundary: FR1-FR4 and regression/positive matrix,
then gate evidence and critique dispositions. Available artifacts are reconciled;
P01/P02 markers record source work, focused validation and one gate attempt,
not gate success. P03 is this Review. Only this review record is review-writable.
Initial blocker B1: gate-before-commit conflicts with clean committed HEAD.
Independent coordinator assessment remains later work, not this self-review.

## Execution Status

Complete: one postimplementation self-review executed against the final diff,
current artifacts and actual validation logs. This is not the coordinator's
independent exact-head assessment. No source corrections or second Review.

## Plan-to-Change Reconciliation

| Scope | Evidence and assessment |
| --- | --- |
| P01-T01 / FR1 | Only seven guard lines added. Account name/email require str without stripping, coercion or format rules. |
| P01-T01 / FR2 | Existing exact account keys, nonempty provider and deployed trusted-proxy rule unchanged. |
| P01-T01 / FR3 | Tiles explicitly allows None or str; attribution requires str. Exact map keys unchanged. |
| P01-T01 / FR4 | New wrong-type cases raise existing Verdict FAIL with account/map and field diagnostic. No new exception handlers. |
| P01-T02 | Six methods, below eight-method budget; both roles, all invalid JSON types, positive string/null cases. No removed tests. |
| P02-T01 | 64 focused tests and targeted Ruff pass on corrected working-tree source. No ignored inputs regenerated. |
| P02-T02 | Exactly one gate command; preflight failure honestly recorded. No full-gate result or receipt verification claimed. |
| P03 | This single Review records findings and routes blocked publication without further correction. |

The focused negative matrix has 88 subtests across five fields and both roles;
the 70 before-fix failures correspond precisely to the four formerly unchecked
fields. Provider's 18 type subtests already passed, consistent with the unchanged
guard. Positive assertions require `me_contract` PASS, not merely an aggregate
blocked verdict. Existing synthetic case-write durability remains blocked.
No widening of account/map contents policy or other checker behavior found.

## Critique and Implementation-Time Update Assessment

One independent critique executed before checker or test source edits. Its
original Revise verdict and full findings are preserved.
PC-001 rejection is supported by explicit owner authorization for unique `/tmp`
output; worker-local scratch restrictions did not govern parent execution.
PC-002 was applied before implementation: field diagnostics and explicit
positive `me_contract` assertions, including empty-string tiles.
Only local test formatting and evidence/checklist updates occurred afterward;
no significant design deviation or additional critique was needed.

Plan/details/changes preserve B1 consistently. Completed P02 work markers mean
attempt completed, not passing full gate. P03 final marker synchronization is a
parent closeout action. No original issue criteria or historical RPI outcomes
were rewritten.

## Validation Evidence

| Check | Status | Exact boundary |
| --- | --- | --- |
| Before-fix wrong-type regressions | Failed as expected | 2 methods, 70 failing subtests; external regression-before.log |
| Corrected focused suite | Passed | 64 tests, 0.158s; external focused-tests.log |
| Ruff 0.17.1 lint | Passed | Both named tools; isolated E,F,W,B,BLE,I, E501 ignored, no cache |
| Ruff format check | Passed | Both named tools, isolated/no cache |
| Git diff whitespace and ignored inputs | Passed | No whitespace errors or ignored files |
| Full gate | Failed at preflight | Exit 1: BLOCKED: Candidate has tracked modifications or untracked inputs |
| Gate checks and receipt verification | Unavailable | No checks ran; output directory/receipt not created |
| Commit and independent exact-head assessment | Not run | Failed prerequisite; no new HEAD |
| Deployed, SQL durable, AI-live, Azure, tenant, human acceptance | Not run | Explicitly excluded; not inferable from synthetic tests |

External evidence root: `/tmp/ama-350-correction4-20261022-Qdq0J7/`.
Gate console: `full-gate-console.log`; SHA-256:
447e1c2c4544d9b67cdd60b7bf0e0cda04acd06a952d7b8006ec99bd523fae29.
HEAD remains 05b5b7d2b754ae0e7134df8db1a867861726a821; local origin/main
is b4d467cad84535ed106cffa1ae9aa303db7bfed2. Remote freshness was not fetched
or independently verified under the no-network boundary.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Required exact-new-HEAD gate and receipt remain unavailable

* Scope: P02-T02 / publication.
* Evidence: unchanged clean_identity rejects tracked modifications and untracked
  inputs before gate checks; the single actual attempt exited 1 for that exact
  reason. The owner forbids committing before successful gate and receipt.
* Impact: corrected source cannot have a passing exact-new-HEAD receipt under
  the authorized sequence. Commit/publication is blocked. This is a sequencing
  constraint, not a new checker defect or permission to alter the gate.
* Destination: later rpi-plan decision with owner/coordinator.
* Smallest next action: explicitly reconcile commit/gate sequencing before any
  commit or further gate. No additional source correction or repeated gate is
  authorized by this Review.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Independent coordinator assessment is still pending

* Scope: handoff/publication, outside this bounded local self-review.
* Evidence: coordinator independent review and publication are explicitly
  reserved in the owner request; no new HEAD or complete receipt exists.
* Impact: local source/tests do not establish independent or human acceptance.
* Destination: distinct coordinator follow-up after RV-001 is resolved.
* Smallest next action: coordinator assesses the exact authorized committed
  candidate and its own gate evidence; keep PR #436 draft and issue #350 open.

## Defects and Plan Follow-Ups

No additional code defect identified in the seven-line guard change.
B1 maps to RV-001 once. Prior correction3 residual findings remain distinct
with their original owners/outcomes; they were not resolved or accepted here.
The original issue's acceptance criteria remain unticked. No external writes,
identity queries, deployment, credential access, push or PR update occurred.

## Outcome and Closeout Routing

Execution: Complete. Outcome: Not accepted for publication; source correction
and focused engineering checks passed, but full-gate/receipt requirements did
not. No conformant or whole-issue acceptance outcome is asserted.

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | None found | No further source work in this loop |
| Decision gap | Later rpi-plan, RV-001 | Owner/coordinator resolves sequencing |
| Material evidence gap | No new research needed | Runtime contract already established |
| Residual work | Distinct follow-up, RV-002 | Coordinator independent exact-head assessment |

Rank 1 is RV-001 because it is the immediate publication prerequisite and
requires no speculative source work. Rank 2 is RV-002, dependent on rank 1.
No child task or second Review begins. Required human/hosted acceptance remains
outside this evidence boundary.
