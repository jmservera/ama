---
title: Demo sites live correction final-candidate plan critique
description: Independent assessment of the bounded SQL-first deployment candidate
ms.date: 2026-10-29
---

## Metadata

* Task ID: 5a7ca259-9fe8-407c-accf-fc965757c10e
* Task: demo-sites-live-correction
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/demo-sites-live-correction-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/demo-sites-live-correction-phase-details.md
* Critique execution status: Complete
* Assessment: One final-candidate independent critique; no implementation.

## Inputs and Criterion Boundary

* Current owner direction authorizes live az execution by the parent, the
  existing private initializer for the view, one resident forward revision
  retaining rollback, one employee forward revision from exact latest main,
  and conditional #521 authority after both are healthy, otherwise exact parking.
* Current direction supersedes the earlier no-az session boundary. That
  historical restriction is not a present implementation blocker.
* Full raw backups are accepted as captured, as instructed. Historical local
  validation is accepted for reuse, not repeated or represented as fresh live
  acceptance.
* Primary inputs are the research, plan and phase-details paths above and
  .copilot-tracking/research/2026-10-29/demo-sites-live-correction-research.md.
* Supplied evidence pointers inspected:
  .copilot-tracking/changes/2026-10-29/demo-sites-correction-changes.md,
  .copilot-tracking/changes/2026-10-29/demo-sites-correction-evidence.json,
  .copilot-tracking/changes/2026-10-29/both-demo-sites-redeploy-changes.md,
  .copilot-tracking/details/2026-10-29/both-demo-sites-redeploy-phase-details.md,
  infra/sql/resident-showcase.sql, infra/scripts/resident_showcase_sql.py,
  src/core/src/zava_forward/core/resident_showcase_sql.py and the supplied
  startup-compatibility section of src/api/README.md.
* Criterion boundary: SQL-only transactional execution, unchanged Manual jobs,
  exact protected configuration, rollback and log order, bounded VM-only ACR
  exception, immutable main/source/image binding, dependent rollout acceptance,
  authority parking and evidence persistence.
* No az, gh, cloud changes, tests, authenticated requests, secret retrieval,
  private backup inspection or source edits were performed. Only this critique
  artifact is written. Repository context reads do not constitute fresh
  operational or regulatory approval.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Current owner direction / research readiness | Covered | Authorized live continuation; prior no-az artifacts correctly historical; completed backups accepted. |
| P01-T01 | Covered | Private full backups, explicit absent resident auth, full history and eight Manual jobs recorded. |
| P01-T02 / acceptance 3 | Partial | Correct third GO batch and counts-only output; transaction, execution retry and effective projection proof need PC-001. |
| P02-T01 / source binding | Partial | Tracked src, source label and config-byte digest proof present; mutable export ref needs PC-003. |
| P02-T01 / ACR exception | Partial | 600/420/180-second bounds and private-first exact restore are credible; fresh no-drift preflight needs PC-005. |
| P02-T02 / resident | Covered | Raw-template update, exact absent/null handling, retained rollback, target latest=ready, full-history accounting and logs before recovery. |
| P02-T02 / employee | Partial | Ordered after resident success; failure/recovery disposition needs PC-002. |
| Acceptance 2 / exact preservation | Partial | Full app and job comparison specified; separate auth resource comparison needs PC-004. |
| P03-T01 / acceptance 5 | Covered | Current main cannot accept January authority; parking is authorized, not a rollout failure or permission to mix sources. |
| P03-T02 / acceptance 6 | Covered | Original evidence retained, fresh independent operational Review, local sanitized persistence and no publication claim. |
| Locked test ownership | Covered | No source/test changes or validation rerun; historical results remain separately attributed. |

## Verdict

* Verdict: Revise
* Severity summary: 2 High, 3 Medium, 0 Critical, 0 Low.
* Rationale: The ordered delivery approach is credible, but five bounded
  planner corrections are needed before execution. They do not reopen the
  owner's authorization, require new tests or justify expanding operational
  scope. No separately withheld findings remain within this supplied boundary.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Make the SQL transaction and single-execution contract explicit

* Related IDs: P01-T02, acceptance 3.
* Evidence: The phase details promise transactional DDL and no ambiguous-write
  retry, but do not specify transaction control or execution retry/parallelism
  gates. The referenced core connector uses autocommit=True, and the standalone
  infra apply helper also uses autocommit=True. The details name the
  connection-string helper, not necessarily either connector, so this is an
  unresolved worker contract, not a claim that the proposed worker already
  autocommits. The supplied principal verifier checks a permitted-rights
  ceiling; it does not itself prove a successful SELECT grant/effective read.
* Concern: Reusing a connector or relying on defaults can commit the view
  before verification. An inherited job retry can repeat an ambiguous write
  even when the operator does not retry the start command. Ordered column
  metadata under the initializer identity plus the rights verifier is not
  proof that the resident principal can run the exact projection.
* Impact: Failed verification can leave a committed change or produce false
  SQL-readiness evidence before the only resident forward revision.
* Smallest useful change: Specify explicit transaction entry with rollback on
  every pre-commit failure, with column shape, unchanged permissions/SID and
  allowlist checks before commit. Use only the third batch, never the default
  initialization/apply entry point. Inspect the captured initializer retry,
  parallelism, completion and timeout settings; require a single non-retrying
  execution or stop if the existing execution interface cannot safely provide
  it without persistent job changes. Require a reviewed effective-principal
  read-only projection check returning only shape/counts, with execution
  context reliably restored. On uncertain commit acknowledgement, inspect
  execution/definition state read-only and stop rather than reapply.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P01-T02 states the transaction and retry
  settings, effective projection check and ambiguous outcome path. Execution
  handoff must require the worker hash, commit/rollback disposition, execution
  ID and attempt count, ordered 17-column proof, count-only result and exact
  unchanged job GETs. No live execution is required to resolve this critique.
* Decision route: Direct planner correction; no new user decision.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Define employee failure recovery without touching the healthy resident

* Related IDs: P02-T02, acceptance 1, 2 and 4.
* Evidence: Current phase details specify resident logs-before-recovery,
  failure-only recovery to its captured digest and no second forward attempt.
  Employee receives only "Then employee only after resident success"; the
  plan promises identical preservation, not an explicit employee recovery
  and terminal-state contract. Supplied earlier redeployment details define
  recovery for each app, with no reversal of a successful other app.
* Concern: There is no unambiguous instruction for employee startup failure,
  accepted-but-uncertain PATCH, or tooling-only verification failure.
* Impact: The operator could leave employee failed, repeat a forward update,
  or unnecessarily revert the successfully corrected resident.
* Smallest useful change: Explicitly apply the failure contract to employee:
  inspect ambiguous writes read-only; collect available failed-target console
  and system evidence before recovery; permit one failure-only raw-template
  recovery to that app's captured digest on actual runtime failure; prohibit
  forward retry. Specify bounded convergence and the same exact preservation,
  full-history and old-digest readiness proofs. Tooling-only uncertainty is
  verification-blocked, not automatic rollback. Keep resident unchanged.
* Action owner: Planning parent.
* Exact resolving evidence: P02-T02 names employee terminal states, recovery
  timeout, log order and one-forward-attempt rule, and reconciles successful
  versus recovery revision counts in acceptance 2. A recovered employee is
  explicitly non-delivery; authority stays parked.
* Decision route: Direct planner correction within the existing recovery
  boundary; no new user decision.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Export the pinned main object, not the movable tracking ref

* Related IDs: P02-T01, research main baseline, goal of exact-main images.
* Evidence: Research and details identify
  77c87e0d76b827544fde9b2f2ce7dfbd9d879232, while P02-T01 says
  "git archive origin/main src only" and labels must match exact main.
* Concern: A tracking ref can move between research, archive and separate
  builds. An OCI source label is asserted metadata; config-digest equality
  binds image bytes but does not independently bind the archived source.
* Impact: Images could be accurately digest-bound yet built from a different
  source than the reused local validation or each other.
* Smallest useful change: Define the current fetched-main SHA once, assert its
  equality with the reviewed/validated SHA, archive that immutable object and
  bind both builds and the SQL batch to it. Record source-tree/archive hashes.
  If a later fetch changes the required latest-main candidate, stop and
  reconcile evidence instead of silently relabeling or rerunning old checks.
* Action owner: Planning parent.
* Exact resolving evidence: P01/P02 name the immutable SHA used for SQL and
  archive, the equality gate and drift-stop rule; sanitized build receipts
  are required to carry that SHA, source hash and both remote image digests.
* Decision route: Direct planner correction; no new user decision.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Compare auth resources separately from complete app responses

* Related IDs: P01-T01, P02-T02, acceptance 2.
* Evidence: Auth backups are captured separately, including explicit resident
  AuthConfigNotFound. Current preservation instructions compare complete app
  responses and unchanged job GETs, but do not require before/after equality
  of the separate auth resource. Earlier supplied frozen contracts do.
* Concern: App GET equality cannot prove that a separate auth resource is
  unchanged, and absent resident auth must not become an empty object or a
  generic successful/missing read.
* Impact: Exact authentication preservation could be claimed without the
  required readback, especially during failure recovery.
* Smallest useful change: Require separate auth equality before each write
  and after each forward/recovery operation: exact employee auth content and
  resident absence specifically confirmed as AuthConfigNotFound. Unexpected
  read failures or auth drift block dependent work.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P02-T02 and acceptance 2 explicitly require
  both separate auth comparisons, with sanitized hashes/status and zero
  unexpected differences in execution receipts.
* Decision route: Direct planner correction; no new user decision.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Gate each ACR exception on fresh baseline equality

* Related IDs: P02-T01, acceptance 2.
* Evidence: Full ACR backup and exact final restoration are specified.
  Immediate pre-write no-concurrent-drift equality is explicit for apps but
  absent for ACR. Earlier supplied ACR execution details require a fresh
  complete stable projection comparison before opening the exception.
* Concern: The first registry write can operate on a stale baseline, and
  restoration can overwrite a legitimate intervening policy/network change.
  Exact equality after restoring stale values would not detect that overwrite.
* Impact: A bounded VM-only route could still make an unauthorized concurrent
  policy change and falsely report preservation.
* Smallest useful change: Before the first policy write of each exception,
  compare fresh full stable ACR state with the approved captured baseline.
  Refuse any unexpected drift. Track only this execution's expected
  intermediate changes; on unexpected drift during the window, stop forward
  operations, close public access first and escalate the restoration conflict
  rather than silently overwrite unrelated fields. Block app writes until
  exact restoration is proven.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P02-T01 requires timestamped baseline
  equality before each opening and explicit drift handling within the existing
  600-second/private-first deadline; receipts require opening, closure,
  duration and complete stable equality results.
* Decision route: Direct planner correction; no new user decision.

## Strengths and Residual Risk

* SQL-first ordering addresses the documented pre-HTTP documents_json failure
  mode without pretending it proves the historical Azure failure's cause.
* Execution-only overrides preserve the eight Manual job definitions and avoid
  reseeding, table/grant batches, allowlist extension and infrastructure changes.
* Raw API template handling preserves env absence/null/value distinctions and
  avoids the previously observed CLI secretRef normalization.
* Resident acceptance correctly requires the new target latest=ready,
  expected digest, Healthy/Provisioned and active traffic, not merely an old
  revision's anonymous health response. Failed-revision logs precede recovery;
  unavailable console evidence must remain an explicit limitation.
* The previously approved local-Docker-to-ACR VM /32 route is not mislabeled
  as hosted Tasks. No Tasks bypass, broad network expansion, RBAC/server
  change, tag/image deletion or policy-timestamp normalization is authorized.
* Authority is correctly conditional and presently parkable: current main's
  December cap cannot accept #521's January authority. The parent must list
  source integration and the single-revision conflict, owner-private credential
  rotation/exact-version Modify, individually approved existing synthetic
  rows, expiry/alert/rollback windows and applicable funding prerequisites.
  The detailed supplied parking steps in
  .copilot-tracking/changes/2026-10-29/demo-sites-correction-changes.md remain
  useful requirements, not fresh operational outcomes. No secret operation,
  January config, row renewal or second forward revision is inferred.
* Anonymous health and source/digest/config evidence cannot establish resident
  login, cross-case denial, accessibility, actual model behavior or operational
  authority acceptance. Those limitations are compatible with the explicitly
  bounded owner request; no authenticated smoke is proposed.
* Local evidence commits and a fresh independent operational Review do not
  satisfy publication, hosted checks or human approval. The existing original
  critiques and Review outcomes must remain unchanged.

## Questions or Blocking Evidence Gaps

* No unresolved user choice prevents these planner corrections.
* Raw backup contents and initializer execution settings were not independently
  inspected. Their existence is accepted; PC-001 requires the necessary
  execution-setting gate rather than asserting unsafe current values.
* The local source evidence supports an assessment of this plan, not a claim
  that any live SQL/app/ACR operation has succeeded.

## Limitations

* Read-only document/source assessment only. No tests or cloud operations.
* Historical validation was reused as instructed, not rerun or independently
  reproduced. Private credentials, row data and backup bodies were not read.
* No implementation changes, commits, publication or peer review were performed.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Revise the SQL transaction/single-execution contract,
  then resolve PC-002 through PC-005 directly in the existing plan/details.
* User response required: No.
* Return this single complete finding set to the active parent. Do not start
  implementation from this critique or request another critique pass.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-29/demo-sites-live-correction-research.md](.copilot-tracking/research/2026-10-29/demo-sites-live-correction-research.md) | Supplied current research |
| [.copilot-tracking/plans/2026-10-29/demo-sites-live-correction-plan.md](.copilot-tracking/plans/2026-10-29/demo-sites-live-correction-plan.md) | Assessed plan |
| [.copilot-tracking/details/2026-10-29/demo-sites-live-correction-phase-details.md](.copilot-tracking/details/2026-10-29/demo-sites-live-correction-phase-details.md) | Assessed operational contracts |
| [.copilot-tracking/reviews/plans/2026-10-29/demo-sites-live-correction-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/demo-sites-live-correction-plan-critique.md) | Complete independent critique; Revise |

## Next Steps

Active planning parent: resolve PC-001 through PC-005 directly and record their
disposition before finalizing the candidate under existing authorization.
No user action or additional critique is required. This critic stops here.
