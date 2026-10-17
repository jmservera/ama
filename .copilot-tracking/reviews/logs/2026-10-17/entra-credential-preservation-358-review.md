---
title: Issue 358 credential preservation review
description: Single postimplementation RPI Review and residual acceptance routing
ms.date: 2026-10-17
---

## Scope and Evidence

Task ID: 358. Slug: entra-credential-preservation-358. Date: 2026-10-17.
Single full-task postimplementation Review of source commit
40e6835be682e1aeffab8ca78a10184889e5e3b4 against base
abaca7881e2a4a77eacf865fe235d4af9196643f.

* Plan: .copilot-tracking/plans/2026-10-17/entra-credential-preservation-358-plan.md
* Details: .copilot-tracking/details/2026-10-17/entra-credential-preservation-358-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-17/entra-credential-preservation-358-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-17/entra-credential-preservation-358-changes.md
* Research: .copilot-tracking/research/2026-10-17/entra-credential-preservation-358-research.md

## Opening Review State

Goal: assess expiry, KV/app-reference preservation, recovery safety, legacy
compatibility, proof quality and acceptance honesty once. Full-task boundary:
owner requirements, P01/P02 completion, PC-001-PC-003 dispositions, source/tests,
documentation and remaining P03 publication work. Evidence ready: dated artifacts
and committed implementation; 313 infra tests, seven killed mutations and
offline quality gates recorded. First comparison: requirements against narrow
credential functions and actual behavioral test oracles. Review may write only
this record; parent separately maintains lifecycle state. No source edits,
new implementation, cloud/secret reads or second Review. Initial blocker:
actual non-production preservation UNMET, already explicitly scoped as residual
by the owner; does not prevent a credible offline review.

## Execution Status

Complete. One Review executed inline over the complete supplied boundary; no
independent review subagent or second Review claimed.

## Plan-to-Change Reconciliation

| Scope | Evidence | Assessment |
| --- | --- | --- |
| P01-T01 | Five new ordinary methods in the canonical setup suite, fixed clock/mixed inventories, recorded original-source failures | Reconciled; no removals, within ten-method limit |
| P01-T02 | Named inventory validation/reconciliation, reference digest, pre-reuse/readback verification | Reconciled; narrow source change, no expiry guard relaxation |
| P02-T01 | 313 infra tests, 101 setup tests, 17 callback-helper tests, seven assertions-only mutation kills, lint/types/Bicep | Reconciled; dependency installation only in own venv after missing-dependency probes |
| P02-T02 | Existing runbook/evidence/index updated, log appended, owner memory untouched | Reconciled; accurate partial acceptance and #360 overlap |
| P03-T01 | This single Review; publication pending parent | Correctly still active; no premature full-plan completion |
| Follow-Up Items | Authorized non-production proof and #360 broader readiness | Correctly outside active implementation and routed distinctly |

## Completed Work Assessment

The code reconstructs a named union of configured and listed secrets, validates
uniqueness and value availability before addPassword, and preserves KV pairs
without replacing them by a returned resolved value. Empty ordinary strings are
valid. KV conflicts/incomplete pairs and missing ordinary values fail sanitized.
The immutable expected reference digest accompanies the same PATCH as the new
secret; it contains no secret value. Before auth activation, metadata-only
readback must match all names and KV pairs. The pending tag blocks later reuse
after a missing/altered reference; successful matching retry clears it without
another password. Existing verified-pair reuse remains idempotent.

Test assertions inspect the actual captured configuration PATCH, backing store,
unchanged env secretRef/tokenStore and write sequence. The positive GET projection
removes ordinary values, preventing an echoing fake from masking value-readback
assumptions. Persisted mismatch tests prove auth remains unchanged on both first
failure and rerun. List/PATCH failures retain configuration/auth and remove
temporary files. Expiry tests exercise generated and legacy selected names at
past/exact/missing/future boundaries; old credentials remain. Mutation tests
require behavioral assertion failures and reject runner errors.

The diff does not change initialize-api-auth.py, staff_azure.py, worker/job
logic, Bicep, workflows, crypto, identity/network guards or source packages.
Merged #370 and abaca788 ancestry remain intact. Both author and committer use
the authenticated account's noreply email; required trailers are present.

## Implementation-Time Update and Critique Assessment

PC-001: directly resolved in the candidate and implementation by the atomic
pending reference digest, pre-reuse verification and persisted-mismatch/
transport-recovery behavioral oracles.

PC-002: directly resolved by metadata-only GET projection with independent exact
PATCH/backing-store value assertions; both empty and nonempty values covered.

PC-003: directly resolved by the offline-readiness gate. No in-scope correctness
defect was found in this Review; publication may be ready for offline review,
but must disclose residual live acceptance and must not close the issue as met.

There was one critique, no new significant/divergent user decision, no unapproved
scope expansion and no early dependent-work resumption. Ordinary fixture and
mutation-harness corrections were implementation judgment; initial runner errors
were not counted as mutation kills. Current plan/details/changes agree.

## Plan Follow-Up Assessment

| Follow-up | Why outside implementation | Owner and route |
| --- | --- | --- |
| Actual non-production preservation | Owner explicitly prohibits writes/secret reads and permits partial delivery if safe scope unavailable | Owner/coordinator to establish separately permitted existing scope; RV-001 |
| Broader setup/job readiness | Separate loop #360 owns job/image/live tenant/browser/SQL acceptance | #360 coordinator to sequence narrow shared setup/test changes; RV-002 |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Actual existing-resource preservation remains unproved

* Scope: issue acceptance, not an implementation defect.
* Evidence: docs/architecture/cutover-evidence-pack.md, Credential Preservation
  Offline Follow-Up (2026-10-17); research W1/W6; explicit owner controls.
* Impact: passing mocked payload/readback tests and public schema cannot prove a
  real Container App rebuild preserves KV pairs or app-value usability.
* Destination: distinct owner/coordinator follow-up; establish authorization and
  safe scope before later rpi-research/live evidence. Do not execute cloud work now.
* Smallest action: arrange an already authorized existing non-production target
  and safe verification that does not alter/delete real secrets or expose
  private services. Retain sanitized reference-level evidence only. Until then,
  criterion UNMET, issue delivery partial and no acceptance checkbox ticked.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Shared setup/test changes need #360 sequencing

* Scope: existing plan follow-up, not an implementation defect.
* Evidence: narrow setup/test diff versus unchanged merged #370 staff-job/CI work;
  separate #360 scope and runbook/evidence coordination note.
* Impact: concurrent broader setup edits can conflict if this narrow change is
  not reconciled first; this task cannot assert broader setup readiness.
* Destination: distinct #360 coordinator follow-up.
* Smallest action: reconcile these credential helpers/tests before proceeding
  with that loop; do not merge, rewrite branches or infer deployment approval.

## Defects and Routed Findings

No material in-scope implementation defect or unaccepted decision gap found.

| Finding | Destination | Reason |
| --- | --- | --- |
| RV-001 | Owner/coordinator authorized non-production evidence follow-up | Accepted residual live evidence gap, not repairable by offline code |
| RV-002 | #360 coordinator | Separate existing workstream/shared-file sequencing |

No finding routes this completed task back to Implement or another Review.

## Validation Evidence

| Validation | Status | Boundary |
| --- | --- | --- |
| Original-source behavioral red | Passed as evidence | 15 assertion failures, zero errors; expiry/delegate baseline passing, not alleged bugs |
| Targeted setup and legacy | Passed | 101 setup and 17 callback-helper tests; seven killed mutations in canonical suite |
| Full infra with REQUIRE_AZ_BICEP=1 | Passed | 313 tests, no skips/errors; simulated health/denial stdout is offline test output, not live probes |
| Bicep build/lint | Passed | All existing infra entry/module templates, offline Bicep 0.48.1 |
| Ruff/mypy/compile/CLI | Passed | Exact scope in changes record; setup's existing formatting preserved |
| Documentation | Passed | New relative links/heading targets exist, KB log append-only, no original specification/memory changes |
| Live preservation/browser/SQL | Not run | Prohibited/unauthorized safe scope; public schema is not live proof |
| Hosted PR checks | Unavailable at Review | PR not yet opened; parent must not claim hosted passes |

## Outcome

* Execution status: Complete.
* Outcome: Residual work.
* Severity summary: zero implementation defects; one Medium and one Low residual.
* Rationale: completed offline scope is supported by red/green/mutation evidence,
  narrow source and retained compatibility. Full issue acceptance cannot be
  declared while actual non-production preservation is UNMET.
* Publication readiness: ready for review of the **partial offline delivery**,
  not live acceptance. No merge or deployment approved.

## Closeout Routing Record

| Finding class | Destination | Next owner/action |
| --- | --- | --- |
| Implementation defect | None | No source correction required by this Review |
| Decision gap | None | Confirmed owner controls preserved |
| Live evidence gap | RV-001 distinct follow-up | Owner/coordinator establishes separately permitted safe scope |
| Coordination residual | RV-002 distinct follow-up | #360 coordinator sequences shared changes |

Parent may commit this record and publish the topic PR, explicitly reporting
UNMET live criterion. The owner explicitly requested stop after push/PR, so do
not select or start a child follow-up automatically.

## Explicit Phase Log

* 2026-10-17 Review opened once after committed P01/P02 and pre-Review reconciliation.
* 2026-10-17 Review completed once: execution Complete, outcome Residual work; RV-001/RV-002 routed to owner/#360 coordinator, not another review loop.
