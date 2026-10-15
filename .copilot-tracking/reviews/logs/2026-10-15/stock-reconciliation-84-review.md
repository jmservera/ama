---
title: Issue 84 implementation review
description: One post-implementation assessment with separate execution and outcome
ms.date: 2026-10-15
---

## Review state and boundary

Task 84, stock-reconciliation-84. Execution: Complete. Outcome: Residual work.
One post-implementation Review only; no correction/re-review cycle.
Boundary: owner's four issue criteria, current src-only implementation, human
authority, unknown evidence, recorded local validation and external acceptance.
No source/plan/evidence changes are authorized by this review phase.

## Compared artifacts

* .copilot-tracking/research/2026-10-15/stock-reconciliation-84-research.md
* .copilot-tracking/plans/2026-10-15/stock-reconciliation-84-plan.md
* .copilot-tracking/details/2026-10-15/stock-reconciliation-84-phase-details.md
* .copilot-tracking/reviews/2026-10-15/stock-reconciliation-84-plan-critique.md
* .copilot-tracking/changes/2026-10-15/stock-reconciliation-84-changes.md

P01/P02 and P03 validation/documentation are reconciled. P03-T03 (review and
publication) is correctly still pending, not an implementation-readiness gap.
One critique executed with direct dispositions PC-001..PC-004; no owner decision
was silently overridden. Final source/test assessment is complete.

## Plan-to-change reconciliation

| Scope | Evidence | Assessment |
| --- | --- | --- |
| P01-T01 | stock.py, Store.stock_reconcile, technical missing_items; JSON/SQL tests | Both competing values and full metadata/owner retained; unknown authority and eligibility; no home overwrite or exclusion. Conflict gate works with/without design. |
| P01-T02 | signoffs.py and existing/new sign-off/hazard tests | Four distinct professional-role decisions, authenticated names/email/role/version, no self-approval, affected-only returns and explicit reapproval. Existing hazard/building controls reused. |
| P01-T03 | stock support helpers; ranking/projection/insights/AI facts; SQL support_encoding refresh | Unknown and positive coverage separated, independent ranking factors retained; JSON/SQL lists, filters, rank keys, cursors and repeated upgrade agree. |
| P02-T01 | server route, app/panels DOM | Authenticated staff-only comparison input; contractor default-deny projection; text-node rendering, labelled source groups and version column. |
| P02-T02 | Two new test modules, 13 methods; one tightly coupled existing fixture updated | Semantic JSON/SQL ownership remains core; actual HTTP/rendered app tests remain API. No test removed; budget respected. |
| P03-T01 | Changes command ledger; 964 discovered tests across five suites; 99 skips | Full src suite evidence plus separately passing opt-in Chromium. Ruff lint/format/mypy all five; JS syntax passes. Docker/SQL Server unavailable locally. |
| P03-T02 | Core/API README, reference index and appended log | Durable contracts and evidence limits filed; no original case, memory, legal snapshot or protected-path changes. |
| P03-T03 | This one Review complete; publication still parent-owned | Correctly not claimed delivered before commit/push/PR. No merge authorized. |

## Critique and implementation decisions

PC-001 is resolved by the explicit tri-state/coverage contract and common
consumer helpers; no truthy Unknown string is used as a Boolean.
PC-002 is resolved by versioned derived-data refresh and repeated upgrade
comparisons against JSON lists and cursors. No business-policy weight changed.
PC-003 is resolved by conflict evaluation before the no-design return and
approval/progression guards, with late-conflict preservation of signed history.
PC-004 is resolved by real Chromium execution of the loopback SQL application,
not merely 200 asset responses. Both source values/metadata/owner, explicit
Unknown support, heading/keyboard access and clean second-case navigation pass.

The new registered-human check intentionally rejects forged-role store callers.
The hazard race fixture now uses its registered Building Safety Liaison for a
building sign-off; it still proves a concurrently reported emergency blocks
commit and discards pending audit. This is a justified fixture correction,
not weakened approval enforcement. The new panel's nested-array rendering and
test-route errors were found/fixed during Implementation, before this Review.
No divergent architecture or owner decision was introduced; no critique repeated.

## Acceptance assessment

The four engineering criteria have local synthetic evidence. This does not
attest professional competence, live source authority, real AI benefit,
SQL Server/Azure behavior or direct human usability acceptance. The broader
BRD AC-065 cohort benchmark/nomination contract is not represented as completed;
nomination/challenge belongs to #130 by owner comment. Pass/fail eligibility
rules and source resolution cannot be invented from a synthetic conflict.

## Findings and routing

### RV-001 [Medium]: Live platform/model acceptance remains unevidenced

* Evidence: changes artifact records Docker socket permission denied, local
  SQLite only and no permitted real model invocation.
* Impact: local tests cannot establish image, SQL Server, Azure or AI benefit.
* Destination: distinct validation follow-up; CI image/mssql jobs first,
  rpi-research for approved access/evaluation evidence if unavailable.
* Smallest action: consume PR checks, then use an authorized synthetic Azure
  environment and approved release/evaluation evidence. No deployment here.

### RV-002 [Medium]: Source authority, resolution and eligibility require ownership

* Evidence: stock.comparison preserves Unknown states and exposes unresolved
  holds; no approved authoritative-source/rule register is supplied.
* Impact: queries intentionally remain held; this is not a complete operational
  reconciliation/resolution process.
* Destination: distinct rpi-plan follow-up after named owner confirms source
  authority, resolution rights and eligibility criteria.
* Smallest action: approve a versioned synthetic source-authority contract,
  without silently selecting latest values or transferring resident consent.

### RV-003 [Medium]: Professional and direct-human acceptance remains open

* Evidence: signoffs.py keeps exercise role mappings; browser checks are
  engineering tests, not competent-professional or resident/staff validation.
* Impact: named synthetic actors do not certify competence/delegation or human
  accessibility/comprehension. No operational activation follows.
* Destination: distinct human acceptance follow-up, returning to rpi-plan only
  if approved mappings or journey expectations change.
* Smallest action: obtain named professional delegation/scope and human
  task/accessibility review, preserving independent approvals and resident choice.

## Defects and residual work

The original Review identified no high-confidence implementation defect.
That conclusion was superseded by the owner's PR #318 finding below.
RV-001..003 are explicitly unmet acceptance/follow-up gates, not silently
completed criteria or requirements added to the engineering slice. There is no
second Review and no return to Implement in this task. Source code was not
changed during Review. Existing sensor test ResourceWarnings remain unrelated.

## Validation and outcome

Execution: Complete. Outcome: Residual work, not unconditional Conformant or
full issue acceptance. Reviewed the current implementation diff/new stock
module, storage hooks, projections, ranking/support consumers and CSV scope
(CSV does not export support flags), and reconciled recorded tests.
`git diff --check` passed during Review; no separate security audit is claimed.
All actual executable commands/results remain in the changes artifact.

No blocker prevents a reviewable topic PR using Refs #84. Full operational
acceptance remains blocked by RV-001..003. Parent next action: persist outcome,
commit the artifacts/code/docs, push the named branch and open a PR to main;
do not merge or imply issue closure. Ranked future choices: CI/live evidence,
source-authority policy, professional/direct-human acceptance.

## Owner-selected PR #318 finding and implementation disposition

The subsequent owner review identified a High defect: every comparison was
permanently Unresolved, all technical sign-off types were blocked, and any
staff role could raise a query on any case. RV-002 did not justify that
permanent lockout. This section records the requested correction, not a
second Review execution or an operational policy approval.

| Finding | Disposition and evidence |
| --- | --- |
| Permanent unresolved hold | Separate immutable SQE-n withdrawal/reconciliation events derive effective status. Original assertions and prior events are never edited. All four sign-offs fail while unresolved and succeed after authorised withdrawal in JSON and SQLite. |
| Overbroad opening rights | Registered case owner or existing programme/manager role only; unrelated roles/cases and forged identities are denied in core and authenticated HTTP tests. |
| Human authority and audit | Original raiser or manager withdrawal; named human programme-role resolution with reason/evidence. Query owner alone cannot withdraw another raiser's query. No agent resolution/sign-off, selected source or changed home/eligibility decision. Original query and terminal event provenance/audit survive restart. |
| SQL concurrency | Existing case-body rowversion plus audit transaction; concurrent terminal event loses with ConflictError, no duplicate event/audit. Sign-off rechecks fresh stock and safety gates within writer transaction. No added dialect syntax or driver-specific IntegrityError handling. |
| Regression credibility | Before production edits, JSON-first and SQL-first core runs failed with missing event method and unrestricted opening; HTTP tests failed with 200 instead of 403 and missing 404 lifecycle route. See changes ledger for red/green and complete required validation commands/results. |

Operational source-authority, resolution/eligibility policy and actual
competence/delegation remain Unknown/owner-approval-needed. Reconciled is a
human-attested query disposition, not a selected authoritative value or
technical sign-off. RV-001 and RV-003 external/human acceptance remain open.
The historical Review outcome remains Residual work; no second critique,
Review, deployment, merge or issue closure is implied.
