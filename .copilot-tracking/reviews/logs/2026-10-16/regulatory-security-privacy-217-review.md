---
title: Regulatory security and privacy review
description: One post-implementation evidence review for issue 217
ms.date: 2026-10-16
---

## Scope and Evidence

Task 217 / regulatory-security-privacy-217. Review scope: P01/P02 source and
evidence; P03 publication remains pending. Date: 2026-10-16.

* Plan: .copilot-tracking/plans/2026-10-16/regulatory-security-privacy-217-plan.md
* Details: .copilot-tracking/details/2026-10-16/regulatory-security-privacy-217-phase-details.md
* Critique: .copilot-tracking/plans/2026-10-16/regulatory-security-privacy-217-critique.md
* Research: .copilot-tracking/research/2026-10-16/regulatory-security-privacy-217-research.md
* Changes: .copilot-tracking/changes/2026-10-16/regulatory-security-privacy-217-changes.md

## Opening Review State

Goal: compare locally implemented controls against issue 217 without claiming
human, legal, tenant, deployed-service or operational acceptance.
Evidence readiness: P01/P02 complete with focused test, lint, type and loopback
results. Acceptance basis: user synthetic-only direction, ADR 0005, all seven
issue criteria and recorded critique dispositions.
First comparison: trusted role/ownership and SQL transaction boundaries, then
retention/reasons and documentary acceptance qualifications.
Read-only boundary: source, tests, documentation and planning evidence. Only
this review record is review-owned. No initial source-review blocker.

## Execution Status

Complete. One direct post-implementation review of P01/P02 on 2026-10-16.
No second Review or source correction cycle is part of this record.

## Plan-to-Change Reconciliation

| Plan scope | Changes evidence | Reconciliation | Assessment |
| --- | --- | --- | --- |
| P01-T01 capabilities and scope | API/auth, regulatory_chat, infra declarations | Complete | Separate capability does not substitute for staff role; generic reads/writes and own-role metadata are covered |
| P01-T01 SQL audit | RegulatoryChat transaction and existing chain primitive | Complete | Same SQL transaction includes paired messages/referral receipt and audit; rollback/reopen/idempotency covered |
| P01-T01 retention/reasons | regulatory_privacy and engine version 2 | Complete | Unknown/simulated status is explicit; no purge, approval or legal period inferred; evidence IDs no longer substitute for reasons |
| P02-T01 tests | Ten new methods and extended existing assertions | Complete | Within maximum 20; no removed tests or changed generated reports |
| P02-T02 documentation/validation | READMEs, existing DPIA, index/log and changes | Complete | Every issue criterion has evidence and unmet boundary; DPO sign-off deliberately unchecked |
| P03-T01 publication | Pending outside source review | Reconciled | Publish after recording this result; not claimed complete here |

## Completed Work Assessment

Direct diff comparison confirmed the role claim cannot be restored from a wider
staff-register role in retrieval or generic archive/delete. Existing own-thread
and case projection remain, with generic metadata filtered by current role.
Trusted capabilities still require unique provisioned principal binding; an
author/owner capability alone does not permit chat. Infra definitions match the
API maps without creating actual tenant roles.

SQL ask/doubt append audit inside repo.txn before commit, under existing store
and database locks. Fault-after-append tests assert rollback of the ledger head,
messages, receipt and inbox. Durable audit contains actor/role, IDs and hashes,
not answer/question/source/health text. JSON intentionally retains separate
files and a documented post-commit limitation, rather than a false atomicity
claim. Rule/card/check/alert append-only tests preserve existing audit behavior.

Retention review is read-only, current-user/current-role filtered, includes
archives and never loads messages. It reports unknown periods instead of
choosing defaults, distinguishes SYNTH references from DPO review, validates
configuration and tests the exact due instant. It does not satisfy operational
retention or rights requirements, which remain explicitly unmet.

The significant-decision change checks an explicit nonempty reasons field and
bumps the engine version, preventing old checkpoints from bypassing that
changed evidence contract. It does not validate human professional authority or
find a statutory duty satisfied. The offline composer has no inference/tool/
write path; passing injection tests cannot imply actual-model assurance.

## Implementation-Time Update and Critique Assessment

PC-001 was appropriately rejected: existing evidence identifier SYN-HUMAN
contains no reason, as demonstrated by the original test. A distinct reasons
requirement is a real contract change, so checkpoint invalidation is justified.
PC-002 wording was clarified to distinguish principal binding from pre-existing
thread ownership. There is one critique, with no unresolved finding requiring
a new user policy decision.

P03 publication was split from implementation evidence to avoid premature
completion claims. Generic claim-role preservation and own-role metadata
filtering are in-scope consequences of role separation, with negative/positive
HTTP evidence. These updates preserve confirmed synthetic-only intent; no
unapproved scope expansion or human-review substitution was found.

## Findings and Routed Work

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: DPO approval and operational retention remain unavailable

* Scope: issue 217 DPIA and retention criteria, not a defect in bounded P01/P02.
* Evidence: docs/reference/research/chat-memory-dpia.md has unchecked DPO gates;
  regulatory_privacy returns dpo_reviewed=false and unknown per-class periods.
* Impact: live staff/resident processing remains unauthorized; deletion/hold/
  immutable history/backup alignment is not an approved retention workflow.
* Destination: distinct human-owned DPO follow-up.
* Next action: Juan Manuel Servera reviews the exercise draft; actual operational
  DPO/record owners must approve periods, rights, holds and residual risks before
  live use. An agent cannot complete that review.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Local proof does not establish hosted or model controls

* Evidence: no actual Entra assignment/revocation, trusted ingress, Azure SQL
  ledger/archive or regulatory Foundry query was executed.
* Impact: Entra, provider minimisation and operational audit criteria remain
  partial; synthetic human evidence is not statutory compliance.
* Destination: distinct authorized platform/model evidence follow-up.
* Next action: verify actual owners, ingress/roles, SQL and provider terms under
  separate authorization. Do not deploy or call providers merely to fill this list.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: JSON file storage is not transactionally audit-atomic

* Evidence: JSON post-commit audit regression retains the documented two-file
  limitation; SQL rollback-after-audit tests establish the stronger SQL boundary.
* Impact: JSON development tests cannot establish durable operational audit.
* Destination: distinct follow-up only if JSON becomes a delivery authority;
  the current architecture uses SQL, so this is not an active source defect.
* Next action: retain the boundary; do not present JSON as SQL-equivalent proof.

## Defects

No material source defect identified in the assessed P01/P02 boundary. The
findings above are explicit unmet acceptance/residual work, not claims that
required reviews or platform checks have passed.

## Validation Evidence

All commands used installed editable distributions in a pip-created session
venv with absolute project test PYTHONPATH; no private data was read.

| Scope | Status | Evidence |
| --- | --- | --- |
| Core focused suites | Passed | 99 regulatory/privacy/rule/storage tests, 59 source-monitor/panel/memory tests |
| API focused suites and local app run | Passed | 44 regulatory/auth/alert tests and 72 isolation/panel/ledger/role tests; final seven regulatory HTTP tests rerun after role-metadata filtering |
| Agents composer | Passed | Seven exact-excerpt, refusal, comparator and injection tests; no provider calls |
| Infra identity/staff scripts | Passed | 22 offline tests and bash syntax check; no tenant changes |
| Ruff and mypy | Passed | Full core/API/agents projects; 98/45/19 typed files respectively |
| JS syntax and diff whitespace | Passed | node --check chat.js; git diff --check |
| DPIA/legal/actual owners | Not performed | Human review cannot be supplied by an agent |
| Azure SQL, tenant, provider and human trials | Not performed | Outside requested local evidence and not necessary to prove the bounded changes |

Initial failures and their pre-Review dispositions are retained in the changes
record; they are not presented as successful first attempts.

## Outcome and Closeout Routing

Execution: Complete for the P01/P02 review. Outcome: Residual work.
The bounded local implementation has supporting evidence, but all seven issue
criteria are not fully met. DPO and hosted/model/human evidence remain open.

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None identified | No source correction cycle |
| Decision gap | None invented | Existing owner direction preserved |
| Human approval/retention | RV-001 distinct follow-up | Named exercise DPO and future real record owners |
| Hosted/provider/human evidence | RV-002 distinct follow-up | Authorized technical and legal owners |
| JSON authority limitation | RV-003 conditional follow-up | Only if architecture changes to deliver JSON authority |
| Remaining active plan work | P03-T01 | Commit, push and open evidence-qualified PR; no merge or issue checkbox update |
