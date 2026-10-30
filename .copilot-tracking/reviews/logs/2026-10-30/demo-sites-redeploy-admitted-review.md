---
title: "Review: admitted demo sites redeployment"
description: "One post-implementation evidence-based review of the admitted redeployment."
ms.date: "2026-10-30"
---

## Scope and Evidence

* Task ID: 8053a799-0279-4f5c-b23b-adea3537291b.
* Review date: 2026-10-30.
* Scope: full admitted redeployment and tightly coupled empty-sensor SQL fix.
* Plan: .copilot-tracking/plans/2026-10-30/demo-sites-redeploy-admitted-plan.md.
* Phase details: .copilot-tracking/details/2026-10-30/demo-sites-redeploy-admitted-phase-details.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-30/demo-sites-redeploy-admitted-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-30/demo-sites-redeploy-admitted-changes.md.
* Research: .copilot-tracking/research/2026-10-30/demo-sites-redeploy-admitted-research.md.
* Machine evidence: .copilot-tracking/changes/2026-10-30/demo-sites-redeploy-admitted-evidence.json.
* Source: infra/sql/resident-showcase.sql,
  src/core/tests/test_resident_showcase_sql.py, infra/README.md.

## Opening Review State

* Goal: assess whether delivered images/SQL/apps meet the explicitly admitted
  deployment scope without overstating authenticated acceptance or rollback.
* Evidence readiness: P01/P02/P03-T01 reconciled before Review;679 private
  command records exported with hashes and direct raw browser result provenance.
* Acceptance basis: owner2026-10-30 08:36Z limited cost admission, standing
  redeploy/IoT/init authority, plan requirements, preserved zero-finding critique
  and documented implementation amendments.
* First comparison boundary: independently test receipt/source/executor hash
  consistency, actual SQL transaction/preservation evidence and anonymous
  browser attribution; then reconcile the complete task and follow-ups.
* Read-only boundaries: no Azure mutations, sign-in/model call, source fixes,
  plan/detail/changes edits, repeated critique or second Review. This canonical
  Review record is the only Review-owned artifact.
* Initial blockers: none identified; outcome not yet assessed.

## Execution Status

* Execution status: Complete.
* One parent-owned Review, with independent read-only operational-provenance/
  SQL-correctness lens by redeploy-evidence-lens. No worker artifact, file
  mutation, additional critique or second Review.
* Outcome: Conformant with justified divergence.

## Plan-to-Change Reconciliation

| Plan scope | Changes and actual evidence | Reconciliation | Rationale |
| --- | --- | --- | --- |
| P01-T01 backups/publication | Build/push/restoration proofs and command journal | Complete | Retained config/index/platform and source bindings, both old manifests retained; exact ACR restored |
| P02-T01 initializer | Failed/rehearsal/diagnostic and two committed transaction receipts | Complete, justified amendment | Ledger defaults diagnosed without disabling ledger; empty-history projection fixed and evaluated |
| P02-T02 rollout | Both roll proofs and actual ARM/revision snapshots | Complete | One forward PATCH/new revision per app; resident dependency repair plus same-revision reset |
| P03-T01 curl/browser/invariants | final-proof and direct raw browser tool event/native trace | Complete | Health/source bytes/anonymous denials and target readiness are distinct assertions |
| P03-T02 Review/local handoff | This record; local commit remains administrative next action | Review complete | Pre-Review plan marker intentionally does not certify its own future Review/commit |
| Follow-Up Items | Owner-held semantic acceptance and public console residuals | Explicitly outside delivered acceptance | No feature closure or clean-console claim |

## Completed Work Assessment

| Scope | Files/evidence | Assessment |
| --- | --- | --- |
| Images and preservation | Machine evidence build/push/registry_restore/final; private before/final snapshots | Published immutable targets match actual saved config bytes and source; exact protected app/auth/history/jobs/ACR/Hub/role comparisons corroborated |
| SQL correction | infra/sql/resident-showcase.sql; src/core/tests/test_resident_showcase_sql.py; infra/README.md | Minimal COALESCE preserves filter/order and yields valid empty arrays; regression queries under restricted resident principal and exercises real projection |
| Live SQL | sql_initial_commit/sql_final_commit and raw journal-bound request/console outputs | Distinct actual executed batches: final six counts0, view/allowlist522, valid arrays522; no row values or seeding |
| Rollout | Resident/employee latest=ready Healthy/Provisioned, active100%, ready replicas and digest receipts | Final target verified, not inferred from old-fallback HTTP200; all four app minima0 |
| Public browser | browser raw event binding, four screenshots, native trace32 snapshots | Four200/no-overflow observations; resident widget script/runtime/launcher/dialog present; Entra navigation explicitly after trace stop |

## Implementation-Time Plan and Detail Update Assessment

| Amendment | Triggering evidence | Current reconciliation | Assessment |
| --- | --- | --- | --- |
| Explicit repeated bounded SQL executions, not replay | Initial rollback, rejected null-default guard, read-only diagnostic, rollback-only rehearsal, wrong ledger-code rollback | Plan/detail/changes preserve each failure and corrected local ledger reproduction | Within approved schema/view initialization; retry0 and full job restoration maintained |
| One source fix and one real-SQL regression, no removals | Actual resident startup failure, counts-only522 NULL projections, local reproduced failure | Actual separately hashed corrected view batch applied transactionally; images still original main-pin builds | Tightly coupled correctness fix, not image rebuild or new feature |
| Resident restart/reactivation instead of recovery-image PATCH | Corrected SQL dependency but failed activation persisted at zero replicas | Same exact target revision reset, configuration/auth/minima unchanged; final complete readiness checked | Justified operational recovery, not proof of unexercised image rollback |

## Critique and Material Revision Assessment

* Original final-candidate critique remains Complete/Pass, zero findings,
  unchanged. No claim that it separately certified later implementation
  amendments; no repeated critique.
* Current plan/detail reconciliation records SQL scope/test ownership changes
  and startup recovery before this Review. These preserve the owner's approved
  image/SQL/redeploy intent; no unresolved significant owner decision found.
* Employee forward rollout did not proceed while resident target was failed.
  Corrective SQL was locally reproduced, tested and transactionally verified
  before target readiness/employee continuation.
* Original parent's Not accepted Review remains historical and unmodified;
  this newly admitted task is independently evidenced, not a rewritten verdict.

## Plan Follow-Up Assessment

| Item | Why outside acceptance | Owner/next action | Route |
| --- | --- | --- | --- |
| Employee chat/map/case semantics | Owner-held Entra credentials required; anonymous401/sign-in does not prove private behavior | Owner-run signed-in acceptance, Refs #550/#556/#551/#553/#552/#554 | Distinct follow-up, RV-001 |
| Resident consent/error/chat/grounding | Public runtime/SQL projection does not prove authenticated interaction or model grounding | Owner-run authenticated journey, Refs #503/#550/#556 | Distinct follow-up, RV-002 |
| Public console resource/CSP residuals | Shared widget assets independently200/source-equal; no clean-console requirement/claim | Separate attribution before any scoped fix | Distinct follow-up, RV-003 |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Employee semantic acceptance remains owner-run

* Scope: P03-T01 and existing Follow-Up Items.
* Evidence: machine final anonymous401 routes and direct browser Entra sign-in.
* Impact: no private chat selector, expanded-map marker/header/filter or
  single-case icon/step/blocker/tab acceptance can be asserted.
* Destination: distinct owner-held authenticated follow-up, not a deployment
  defect or additional active implementation.
* Next action: owner signs in and records those feature outcomes.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Resident authenticated/model acceptance remains owner-run

* Scope: P03-T01 and existing Follow-Up Items.
* Evidence: resident assets200/runtime/launcher/dialog, /demo/view401 and522
  valid SQL arrays; no authenticated interaction/model execution.
* Impact: consent/error/input/conversation/grounding is intentionally unproven.
* Destination: distinct owner-held authenticated follow-up.
* Next action: owner records resident sign-in/consent/errors and, only if
  separately desired, authorized model/grounding acceptance.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Public console residuals need separate attribution

* Scope: public Playwright observation, not shared-asset repair acceptance.
* Evidence: direct browser result reports one unattributed resident resource404
  and employee image CSP errors, while required widget assets return200.
* Impact: no clean-console claim; exact failed resource/cause not established.
* Destination: distinct low-impact follow-up, not broad redesign or active fix.
* Next action: attribute exact resources and agree a minimal separate remedy.

## Defects

* No substantive high-confidence implementation defect or blocking provenance
  gap found. No material open finding prevents the scoped deployment outcome.

## Routed Findings

| Finding | Destination | Owner/next action |
| --- | --- | --- |
| RV-001 | Distinct employee authenticated acceptance | Owner; rank1 by feature-acceptance value |
| RV-002 | Distinct resident authenticated acceptance | Owner; rank2 by restored-runtime/SQL follow-through |
| RV-003 | Distinct public console triage | Future scoped implementation owner; rank3, lower impact |

Later work does not require this task's Review to run again.

## Residual Work

* RV-001..003 are outside this delivered deployment boundary and are not issue
  closure evidence. No child work selected or started.
* Complete publication gate, human/hosted approval and exact-head external
  assessment remain prerequisites for any future publication, not claimed.
* Old-image rollback failure path remains unexercised; code/retained baseline
  availability is not certified runtime rollback testing.

## Blockers and Remaining Work

* Deployment/Review blockers: none.
* Remaining administrative action: privacy-safe local Conventional Commit,
  Refs only, exact requested trailer, no push. Commit had not occurred at
  assessment; no reviewer claim about its future hash.
* Live state beyond retained observations and authenticated semantic outcomes
  not independently re-queried or inferred.

## Validation Evidence

| Check | Status | Evidence |
| --- | --- | --- |
| Executor/proof/source hash consistency | Passed | Independent lens:21 executors,205 proof files,three canonical sources |
| Journal/raw output provenance | Passed | All679 records equal journal,1330 output hashes,74 outer command/result bindings |
| Protected before/final cloud snapshots | Passed | Actual normalized app/auth/revision/job/ACR/Hub/role comparisons, not assertion-only text |
| Published image/source and old manifest bindings | Passed | Journal hashes/config/index/platform references; old manifests retained |
| SQL transactions/projection/schema | Passed final; earlier failures preserved | Actual request and raw console markers match worker/input hashes; final counts0/522 valid arrays |
| Selected real-SQL/sensor tests | Passed |44 tests,0 skips; sql-regression-all-1793351401569394162 retained log |
| Targeted Ruff lint/format | Passed | Retained pinned-tool success outputs |
| Curl health/source/anonymous denials | Passed | final-proof, exact source-byte checks and protected target checks separate |
| Playwright provenance/native assets | Passed | Exact tool event/raw result, five hashes and32 trace snapshots; Entra observed after trace |
| Clean browser console | Not passed or claimed | RV-003 observed residuals |
| Owner-authenticated semantics/model call | Skipped | Owner-held sign-in and no paid-model action, RV-001/002 |
| Runtime old-image rollback failure path | Unexercised | No recovery-image PATCH occurred; do not infer pass |
| Heavy test rerun/cloud calls during Review | Not performed | Existing actual evidence checked read-only; no mutation/repetition |
| Local/hosted publication approval gate | Not performed | Explicit local-only/no-push task; future publication remains separately gated |

## Outcome

* Execution status: Complete.
* Outcome: Conformant with justified divergence.
* Both deployments and counts-only SQL boundary meet admitted scope. Minimal
  tested SQL repair and same-revision recovery are evidenced and reconciled.
  Three low nonblocking residual follow-ups remain explicitly unaccepted
  outside scoped deployment acceptance; no material open defect/gap found.

## Closeout Routing Record

| Finding class | Destination | Owner/next action |
| --- | --- | --- |
| Implementation defect | None | None found |
| Decision gap/invalid assumption | None unresolved | Ledger/null assumptions corrected before Review and preserved historically |
| Material evidence gap | None in admitted deployment scope | No unrun semantic/rollback/publication claim |
| Nonblocking residual | RV-001/002/003 distinct follow-ups | Owner-authenticated employee, resident, then separate console triage |

* Validation coverage: retained actual command/hash/snapshot/SQL/browser source
  evidence independently checked; exact unperformed boundaries listed above.
* Blockers: none for local-only task completion.
