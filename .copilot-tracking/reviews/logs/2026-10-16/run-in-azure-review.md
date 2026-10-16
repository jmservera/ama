---
title: In-VNet staff initialization review
description: One post-implementation evidence review for Refs #360
ms.date: 2026-10-16
---

## Scope and Evidence

* Task ID: 360-run-in-azure.
* Boundary: full offline implementation, tests, runbook and acceptance audit.
* Plan: .copilot-tracking/plans/2026-10-16/run-in-azure-plan.md.
* Details: .copilot-tracking/details/2026-10-16/run-in-azure-phase-details.md.
* Critique: .copilot-tracking/reviews/2026-10-16/run-in-azure-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-16/run-in-azure-changes.md.
* Research: .copilot-tracking/research/2026-10-16/run-in-azure-research.md.
* Compared final transport/worker/shared initializer/setup integration, image
  copies, Bicep/role matrix/guard, new and existing fake-az/SQL tests, CI gates,
  infra runbook, cut-over acceptance table, reference index and log diff.

## Opening Review State

Implementation and local validation are complete; every source-plan marker is
reconciled. Privacy-safe commit/push/PR publication remains parent-owned.
No live Azure execution, image build, private dataset, tenant modification,
network change or approval is in this review's acceptance boundary.
Read-only review; only this record is authored. One Review, performed directly,
with no review fan-out or second review planned.

## Execution Status

Complete. This is an offline source/evidence assessment, not a deployment,
security certification or accessibility/legal conformance determination.

## Plan-to-Change Reconciliation

| Marker | Evidence | Assessment |
| --- | --- | --- |
| P01-T01 | Shared lazy person resolver preserves SQL validation-before-Graph order; worker uses canonical protected preparation/atomic installation, post-commit reread, MI-only restart adapter and copied manifest/helpers | Reconciled; original local behavior retained by regressions |
| P01-T02 | Explicit mode bypasses local SQL; blocked candidate/check falls back; validation/uncertain apply never retries remotely. Source guards, secretRef, authenticated results, deadlines and owned cleanup are present | Reconciled within stated offline boundary |
| P02-T01 | Fake az covers explicit/automatic paths, generated admin/seed, codes-free output, privacy, job/start/create/log/stop/delete failure, timeout, collision and interruption. Runbook/evidence/index/log updated | Reconciled; no inference of live acceptance |
| P02-T02 | 304 infra tests, 32 responsive local app auth tests, CI-gated Ruff/format, scoped mypy and offline Bicep | Reconciled; publication is parent-owned next action |

## Critique and Implementation-Time Decisions

| Finding | Disposition evidence | Assessment |
| --- | --- | --- |
| PC-001 | Worker restarts through own MI; standalone Bicep assigns only app/revision/replica reads and restart at API scope | Literal job-owned restart retained, no operator token |
| PC-002 | Public CLI source documents explicit execution/replica/container JSON-line log streaming and live-pod requirement. Worker holds encrypted result for 60 seconds; client bounds subprocess and requires terminal success | Feasibility grounded in interface source; live endpoint access remains a prerequisite |
| PC-003 | Exact ama/subscription resource bindings, identity principal/tenant versus SQL admin, matching environment/subnet, private Entra-only SQL/database, pinned source image and allowlisted registry/env | Refusal fixtures cover material guards; no network mutation |
| PC-004 | Only pre-mutation candidate/check fallback; validation returns stop; unknown local apply timeout has regression proving no remote apply | Reconciled |
| PC-005 | Manual one-replica job, retry limit zero, canonical SQL lock/transaction, post-commit drift refusal and restart on SQL no-op | Reconciled locally; not live SQL concurrency proof |
| PC-006 | Collision refusal, run-tag ownership, stop then delete/absence check, uncertain-create refusal and explicit cleanup errors/recovery | Reconciled for normal/handled failures; hard termination remains documented residual |
| PC-007 | AES-GCM fresh key/nonce and AAD bind version/run/operation/input; bounded indexed ciphertext, duplicate/missing/tampered/wrong-key refusal, count/status validation | Reconciled; indexed reconstruction does not rely on log arrival order |
| PC-008 | Pure SQL person-resolver interface; operator resolves complete manual/generated people; image copies initializer/helpers/manifest without altering proof ENTRYPOINT | Reconciled; compatible image not built here |

The initial operator-only restart proposal was corrected before implementation,
not accepted as a divergence. Nullable ARM registry credential fields are
accepted only when empty; forwarded configuration is reconstructed as
server/MI only. Source tags retain governance metadata. The existing built-in
role matrix stays enforced, with a separate explicit custom-role inventory/test.
The reference log diff adds only its new terminal section.

## Findings and Routing

### RV-001 [Medium]: Deployment prerequisites remain unexecuted

* Evidence: infra/cutover-proof.Dockerfile, infra/staff-initializer-rbac.bicep,
  infra/README.md, docs/architecture/cutover-evidence-pack.md.
* Impact: the old image lacks the worker, and the MI cannot restart the API
  without its narrowly scoped assignment. A source-only PR is not a live fix.
* Destination: distinct authorized deployment follow-up, not current source work.
* Next action: reviewed private image build/publication, init image digest update
  and API-scoped role deployment in ama. Do not open services to repair a build.

### RV-002 [Medium]: Live private SQL/log/restart/browser behavior is unproved

* Evidence: infra/tests/test_staff_azure.py and cut-over criterion audit.
* Impact: fake az cannot establish permission propagation, logstream endpoint
  reachability, actual SQL transactions, Azure deletion/retention or real people.
* Destination: distinct authorized validation follow-up after RV-001.
* Next action: execute check then apply using the same private roster, verify
  codes-free outputs/cleanup and authorized browser sign-in. Keep issue criteria
  unchecked until the coordinator has actual evidence.

### RV-003 [Low]: Cross-host serialization and hard-kill cleanup remain manual

* Evidence: existing advisory lock behavior and new leftover-job runbook.
* Impact: no Azure-enforced cross-host mutex or finally guarantee on power loss
  is claimed. SQL transactions protect individual writes, not operator windows.
* Destination: distinct operational rehearsal/hardening follow-up if needed.
* Next action: serialized operator window; inspect exact owned job before
  stop/delete, then check persisted SQL state before retry. Do not regenerate
  an existing immutable roster or delete unowned/source resources.

## Defects and Remaining Work

No known source-blocking defect identified in this one review. All three
findings are explicit live/operational residuals, not silently completed
acceptance criteria. No correction/re-review loop is requested. No source-plan
tasks remain; commit/push/PR publication is still parent-owned.

## Validation Evidence

| Validation | Result | Boundary |
| --- | --- | --- |
| Installed source distributions with pip in session venv after missing-package failure | Passed | No package-manifest or system environment override |
| Absolute-PYTHONPATH unittest discovery, infra/tests | 304 passed, no skips | Final source state, including nullable ARM registry response |
| Absolute-PYTHONPATH test_auth | 32 passed | Responsive loopback app with synthetic fixtures; expected missing-law-store diagnostic, no model call |
| Ruff E/F/I/B/UP and format, all ten CI-gated infra files | Passed | New gates persisted in src-ci.yml; existing workflow/check names unchanged |
| Scoped mypy, worker and transport | Passed | Uses existing dynamic SQL interfaces; not full-repository type coverage |
| Standalone Bicep build/lint and full-suite compiled-template checks | Passed | Local compiler only; no Azure management call |
| Git diff/append-only log/link review | Passed | No mvp/prototype/private dataset/env/editor/issue-tracking edits |
| Azure/image build/tenant/browser/human approval | Not run | Explicitly forbidden or outside offline evidence boundary |

## Outcome

Execution: Complete. Outcome: Residual work.

Offline implementation is consistent with the requested behavior and safety
boundary; it is not a conformant live-deployment acceptance claim while RV-001
through RV-003 remain. No invented approvals, legal activation, resident consent,
safety decisions or financial commitments are introduced. ADR 0005's accepted
synthetic-development-only status is preserved.

## Closeout Routing

Parent publishes the existing topic branch and PR with Refs #360, without
merging or ticking issue criteria. RV-001 is the first authorized follow-up;
RV-002 depends on it. RV-003 remains a separate operational constraint.
