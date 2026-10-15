---
title: Issue 83 post-implementation review
ms.date: 2026-10-15
---

Task #83 / src-handoffs-83. Execution: Complete. Outcome: Residual work.
This is the single post-implementation Review.

## Compared Artifacts and Boundary

* `.copilot-tracking/research/2026-10-15/src-handoffs-83-research.md`
* `.copilot-tracking/plans/2026-10-15/src-handoffs-83-plan.md`
* `.copilot-tracking/details/2026-10-15/src-handoffs-83-phase-details.md`
* `.copilot-tracking/reviews/2026-10-15/src-handoffs-83-plan-critique.md`
* `.copilot-tracking/changes/2026-10-15/src-handoffs-83-changes.md`

Assess core workflow, store/projection/AI trigger, API/web integration, tests,
docs and acceptance evidence against issue #83 and accepted ADR 0006. No source
mutation in Review. No new external research or repeated critique.
Publication is intentionally pending until this review finishes.

## Review Evidence

Reviewed final core workflow source, focused integration diff, API/UI source,
both new test modules, SQL Server replay adapter, documentation and supplied
RPI artifacts. Direct review fits one continuous trace; no additional worker or
second review was needed.

## Opening Review State

Goal: assess the bounded implementation against issue #83, FR-009/010/011 and
the accepted src dependency rule. Full supplied task boundary, including
critique dispositions, implementation refinements and residuals. Evidence ready:
plan/details/changes reconciled, P01/P02 and P03-T01 complete. P03-T02 publication
and this review intentionally awaited the lifecycle gate. Initial blockers:
none for source review; owner/live acceptance exclusions remain.

## Requirement and Critique Assessment

| Boundary | Assessment and evidence |
| --- | --- |
| Return/reopen provenance | Source and next action checked before mutation; version/stages/reason/authority/current receiving owner recorded. API-supplied authority/owner cannot override authenticated/current values. Core JSON/SQLite and HTTP tests prove persistence and no reassignment bypass |
| Distinct states/accountability | Legacy Offered/Declined aliases remain, canonical Sent/Rejected plus Received/Accepted/Escalated/Completed are explicit. Only recipient acceptance updates owner. Receipt/escalation retain sender chase; completion requires accepting owner. History uses deep copies and contiguous versions |
| Permission/state integrity | Shared guard covers named recipient and sender/manager actions; receiver cannot self-escalate by receiving alone, nonmanager targets rejected; replay/terminal/wrong-actor checks and audit immutability covered by semantic and HTTP cases |
| Cross-surface context | Pending sender/receiver/manager views and detail expose current/proposed/confirmed/chase/destination separately, with independent urgency/due/next action/update context. Missing values remain explicit. Browser exercised real DOM controls, not only API tests |
| Resident/safety/AI boundaries | Handoffs never write resident decisions, release hazards or send communications. Existing coordination eligibility now includes all unaccepted states; provider/release/human-review boundaries unchanged. Existing role/AI/safety regressions pass |
| Privacy projection | New free-text keys and disposition source/reason held for roles without need; queue uses projection too. Contractor/unknown-role denial and canaries pass. No private fixture used |
| ADR 0006/SQL | All new code/tests under owning src projects; core imports only core/stdlib; API-only endpoints/UI. No SQL/schema/client/dependency/image change; forbidden paths untouched. Five CI-only HTTP replays use existing SQL Server job and guarded destructive test DB setup |
| PC-001 | Resolved by simplifying to existing receiving owner, with no override or assignment in return/reopen; eventual transfer tested through ordinary acceptance only |
| PC-002 | Resolved by explicit state/actor table, guarded core transitions, role inventory and populated HTTP contract |
| PC-003 | Resolved by independent urgency/next-action/resident-update fields, persistent commitment invariant, view-specific queue wording and history snapshots |
| PC-004 | Resolved by explicit source-correctness publication gate; no such blocker found. One-review rule preserved; residual owner/live items not promoted to completed acceptance |

## Implementation Updates and Divergences

Mandatory provenance was strengthened from the planning candidate's API-only
enforcement to every new core disposition. This preserves confirmed intent and
closes a bypass; legacy persisted data remains unchanged. Successful regression
calls now name synthetic provenance rather than fabricate runtime defaults.
Removing the redundant handover form and retaining offer-only legacy endpoint/
suggestion buttons reduces duplicate paths while preserving the human gate.
Both updates are recorded in changes and current details; no material new
owner decision or repeated critique required.

Two new test modules remain within the agreed budget. Existing tests were not
removed; explicit fixture re-export and mypy source resolution support the typed
harnesses. Migrated runtime modules retain pre-existing broad lint/type
exemptions, which are disclosed rather than claimed as newly strict typing.

## Validation Assessment

* Final component discovery: core 277, API 469, agents 70, orchestrator 17,
  importer 39 = 872 total; 775 executed successfully, 97 skipped.
* 92 baseline skips plus five new SQL Server replay skips are explicit.
  They are not local evidence of Azure SQL/SQL Server execution.
* All five project ruff check, format check and mypy gates passed. Changed JS
  syntax passed. Existing migration tests passed 25 after restoring their
  existing pinned dependencies. Diff whitespace check passed.
* Earlier fixture/lint/type/missing-tool failures are recorded with their
  resolutions; no failed final local gate remains.
* Browser showed Sent -> Received -> Escalated -> Accepted -> Completed,
  ownership unchanged until acceptance, manager queue visibility and full return
  provenance after actual UI confirmation. Synthetic test, not human research.
* Docker unavailable: permission denied on the socket. No successful image,
  live inference, Azure deployment, human approval or operational SLA asserted.
* Read-only forbidden-path and added-SQL scan found no excluded-path change and
  no new prohibited SQL syntax.

## Findings and Routing

### RV-001 [Medium] Approved operational escalation timing remains unavailable

Evidence: issue #83 criterion 3, BG-010/OD-09, research C2/C9 and documented
manual escalation boundary. Visible dates/manual escalation do not establish
acceptance/escalation within an approved period.

Impact: the whole issue cannot be closed; operational adoption is not accepted.
This is a known excluded decision gap, not an unexpected implementation defect.
Destination: distinct follow-up owned by Programme/owner; `/rpi-plan` after
approved periods, escalation authority and scheduling expectations are recorded.
Leave criterion 3 unticked and publish with Refs #83.

### RV-002 [Medium] SQL Server/image/live acceptance evidence is not local

Evidence: changes command log, 97 guarded skips, Docker socket denial and no
authorized live service invocation. Five new SQL Server HTTP contracts are
wired into the existing mssql job but not claimed run here.

Impact: merge/release must not treat local SQLite evidence as SQL Server,
container, actual-model or operational acceptance.
Destination: distinct CI evidence follow-up owned by PR maintainer for image/
mssql checks; owner/Digital for separately authorized live AI/Azure and human
acceptance. No deployment or billable evidence collection in this task.

## Outcome and Remaining Work

Execution Complete; outcome Residual work for full issue acceptance. No
in-scope correctness or permission defect identified in the assessed boundary.
Bounded source slice is ready for non-closing PR publication, subject to normal
CI and owner review. RV-001/RV-002 remain open; no full Conformant outcome,
operational authority or issue closure is claimed.

Parent next action: complete authorized commit/push/PR publication, then wait
for CI/owner decisions. No child implementation or second Review in this loop.
