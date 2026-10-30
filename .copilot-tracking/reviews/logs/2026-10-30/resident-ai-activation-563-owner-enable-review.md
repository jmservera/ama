---
title: Resident AI activation 563 owner enable - independent RPI Review
description: One bounded post-implementation review of owner-authorized activation and rollback evidence
ms.date: 2026-10-30
---

## Scope and Evidence

* Task: Task563-owner-enable-20261030T1710Z; issue #563.
* Branch: ops/resident-ai-activation-563.
* Review scope: complete continuation artifact boundary for resident-ai-activation-563-owner-enable, dated 2026-10-30.
* Evidence inventory: research, plan, phase details, changes, plan critique and state at their exact dated slug paths; only the six explicitly permitted private script/result projections.

## Opening Review State

* Interpreted review goal: independently assess authorized execution, safeguards, rollback limits, acceptance gaps and local closeout without equating rollback with activation.
* Evidence readiness: six exact continuation artifacts located; contents and safe external projections not yet compared.
* Acceptance basis: supplied owner decision and limits, current plan and criteria, critique dispositions and recorded implementation/validation evidence.
* First comparison boundary: reconcile current plan/detail markers with changes/state, then inspect safe execution projections and narrowly necessary source.
* Active read-only boundaries: only this review record may be written. No cloud, network, browser, model, SQL, fixes, commits, gates, further login or other artifact writes. Private external reads limited to the six user-listed projections; no raw configuration, credentials, stderr, datasets or other sessions.
* Initial blockers: none to beginning evidence comparison; live outcome and remaining acceptance not predetermined.

## Execution Status

* Review execution status: Complete. Exactly one independent post-implementation Review was performed on 2026-10-30; no nested delegation or second Review.
* Implementation execution status: P01 and P02-T01 Complete through the failed-verification/mandatory-rollback branch. Overall continuation Partial because P02-T02 local persistence and full gate remain pending.
* Outcome: Not accepted for activation. The restored baseline is a supported safety outcome, not delivery of the owner's activation request.
* Evidence readiness reconciliation: current plan markers, phase details, changes, state blocker B1 and handoff consistently report activation Unmet, two exhausted sign-ins and local closeout pending. No stale marker prevents this Review.

## Scope and Acceptance Basis

The binding owner decision at 2026-10-30T17:10Z is:
"Enable AI, I will take care of checking the cost and will warn you if there's a problem".
This waives the live cost-ledger pre-read only. Runtime accounting, the USD20
ceiling and exclusive 2026-11-01 expiry remain binding. Redeploy authority through
2026-11-15 does not extend the inference expiry or authorize a third sign-in.

Assessed requirements: FR1-FR6, non-functional credential/recording/request
limits, AC1-AC6, C1-C10, every P01/P02 task, both critique dispositions,
implementation-time refinements and all four plan Follow-Up Items.
Only the resident app's two assistant environment variables were authorized;
existing model/MI/narrow role, image, min0, Manual jobs and employee configuration
must remain unchanged. No secret, role, network, resource or SQL changes follow
from the activation decision.

The six exact continuation artifacts were read completely. The four allowed
helper sources and both sanitized receipts were read, with full receipt
command/result coverage. Their SHA256 values match the changes annex:

| Permitted projection | Verified SHA256 |
|---|---|
| activate.py | 3d25178578372860b644654c84b484c9588890b4675ece670e3c289ebe099809 |
| retry_verified_rollout.py | a58fcc3bcfc09be34f5321cb5c31639129118550ea06474fd860d3a9be7b7ee4 |
| restore_exact.py | 6286fa9c2991cbad2ee19acb8573c09d5651a3aacd69edc36a91241aaf78b1c1 |
| template_patch.py | 220a3356b05414ff24fe1bd1237a213f321b1b3c7a30231fe9e0b4783c07fe05 |
| sanitized-results.json | ea049deb101fc2015694939d4e39750a36f06aa1bd59c05657574e86a2460a33 |
| attempt2/sanitized-results.json | 4273681cbbb2d2afab1d17170111309a7bad03296766c6b374206a24328ae2e4 |

These are safe private projections under the user-authorized
current-session files/resident-owner-enable root, not passing gate receipts.
Raw backups, credential files, command stderr, datasets and every other
private external file were excluded. No helper was imported or executed.
Narrow source reads covered advisor accounting/configuration/answer behavior,
host consent/routing, the expiry constant and SQL procedure definitions only;
reading SQL source did not execute SQL.

## Plan-to-Change Reconciliation

| Current scope | Changes and completion evidence | Reconciliation | Assessment |
|---|---|---|---|
| P01-T01; FR1; AC1 | Missing Playwright restored externally; protected original backups precede mutation; hashes in first receipt | Reconciled | Hash references match; private file permissions and raw bytes are executor evidence, not independently reopened |
| P01-T02; FR2; AC2 | Both runs record baseline health200, anonymous403, client no-request, server no-consent400, disabled rules/manual route | Reconciled | Passed baseline only; one login200 per run, total2/2 |
| P01-T03; FR3/FR4 | Two-variable enable commands; second run waits seven readiness reads before enabled capture | Reconciled | Enabled configuration invariants passed; no actual enabled answer observed |
| P01-T03; FR5; AC3/AC4 | enabled_live TimeoutError; no enabled_rat or out_of_scope result | Reconciled, acceptance unmet | No AI, grounding, thin-label or enabled out-of-scope acceptance; RV-001 |
| P01-T03; FR6; AC5 | Initial restoration failed; later supported rollback removes only two variables and waits four readiness reads | Reconciled | Effective baseline restoration supported, not byte-identical revision restoration or activation success |
| P02-T01 | Original-to-final equality reported; receipt corroborates attempt2 baseline-to-final invariant checks | Reconciled with evidence limit | Raw original-to-final comparison not independently rerun under permitted boundary |
| P02-T02; AC6 | One critique with dispositions, this one Review; local commits/gate absent | Correctly pending | Review portion completes here; remaining authorized parent closeout is RV-002 |
| Follow-Up Items 1-4 | Timeout investigation, human acceptance, conditional local SQL gate setup and conditional runtime accounting investigation | Reconciled | Distinct later work; no expansion of active execution |

## Completed Work Assessment

### Authorized operations and safeguards

The receipts' mutation argv sets/removes exactly
ZF_DEMO_ASSISTANT_ENABLED and ZF_DEMO_ASSISTANT_ENDPOINT on ca-resident-demo
in ama, with unique suffixes. No image, scale, identity, auth, secrets, job,
employee, RBAC or network mutation flags appear. Capture operations for both
employee apps are reads only. Second-run enabled/restored checks preserve
environment, template, shared configuration, workload profile, identity,
auth, jobs, employee configuration, min0/max1 and Manual triggers.
Existing account/model/narrow-role observations are supplied research evidence;
this Review did not re-query Azure or prove an exhaustive cloud activity log.
No evidence supports unauthorized resource creation, SQL access or scope
expansion.

Source inspection confirms that only ENABLED/ENDPOINT assistant settings are
accepted, the existing SQL MI supplies model credentials, reservation precedes
token/transport and failed accounting does not permit unmetered transport.
SQL definitions enforce the 2000-cent permanent reservation ceiling and
exclusive November1 expiry; the Python expiry constant agrees. These are
unchanged source contracts, not proof of deployed accounting objects,
remaining headroom or an actual successful reservation.

### Credential safeguards

activate.py masks both fields before automation reads credentials, validates
the two-line shape, persists a login counter before submission, clears form
values after response, disables core dumps/debug flags, uses a clean browser
context without trace/HAR/video/storage export and sanitizes exceptions.
The wrapper copies the prior counter and records attempt2 as login2/200;
there is no blind password retry. Both receipts report contexts closed and
recordings false. umask077 and the recorded root/file protection support the
private-storage design.

The in-process credential list is retained for exclusion checks until process
exit; form clearing is not secure memory erasure. No password, token, cookie,
header or private case payload was observed in the inspected projections.
This is bounded source/receipt assurance, not a forensic guarantee about
unopened files or machine memory. No credential file or raw output was read
to strengthen the claim, and no new login is permissible.

### Adverse history and rollback

The first run's environment equality failed before any enabled-model
verification. Its receipt retains environment_preserved=false,
activation_verified=false and rollback_verified=false. Removing variables
exited0; original activation exited1. The supplied
RevisionAlreadyInRequestedState explanation does not make restoration pass.
Health200 in that run could have been served by an old ready revision.

Changes preserve rejected REST requests containing SDK-only imageType/null
fields, accepted asynchronous normalized PATCH followed by reused-suffix
provisioning failure, JSONDecodeError on an empty response, later old-revision
activation and rejected Single-mode traffic targeting. The two allowed REST
helper sources support their bounded template-restoration purpose. Their
raw requests/results were not permitted reads; exact service errors and the
earlier evolving template helper versions therefore remain supplied evidence,
not independently reconstructed command transcripts. None is counted as a
successful restoration or erased by the final pass.

The wrapper narrows normalization to value="" alongside a nonempty secretRef;
it does not ignore changed references, nonempty values, image or other template
members. It waits for latestRevisionName==latestReadyRevisionName and
Succeeded provisioning. Final restoration captures configuration, checks
effective equality, health and denial, and requires one 100%-traffic revision
matching latestReady. The final receipt supports
ca-resident-demo--owner-safe-173404, rollback_verified=true, health200 and
anonymous403. The changes record additionally reports original-to-final
effective equality. The raw comparison was not independently rerun.

Thus final restoration is supported within the supplied evidence boundary:
the effective original template modulo suffix/inert secretRef empty value,
with shared config/identity/auth/jobs and employee state preserved. It is not
the original revision's identity or byte-for-byte SDK serialization. It does
not prove ongoing availability, successful model transport, no paid call,
ledger headroom or resident acceptance.

## Implementation-Time Plan and Detail Update Assessment

| Affected scope | Change and trigger | Reconciliation and planning state | Assessment |
|---|---|---|---|
| FR5/AC3; P01-T03 | PC-001 required claim-to-source decisions, not recognized labels alone | Plan/details require actual limited in-memory case/host guidance, safe evidence and rollback on unsupported/indeterminate claims | Applied at acceptance-contract level; never exercised on an actual answer |
| FR6/AC5; P01-T03 | SDK adds inert empty value to unchanged secretRefs | Current plan/details restrict normalization and preserve all effective values/references | Justified execution refinement; no weakening of secret equality |
| FR4/FR6; P01-T03 | Exit0/health did not establish new readiness; Single mode cannot target old traffic | Plan/details/changes require fresh ready effective-baseline revision and unique suffix | Justified supported rollback, not revision-mode or owner-intent change |
| P01/P02 markers; B1 | Second ready rollout reaches only coarse enabled_live timeout | Plan/details/changes/state mark rollback complete, activation Unmet,2/2 sign-ins and later investigation | Current-state reconciliation complete; no unsupported success claim |
| P02-T02 | PC-002 rejected on parent-boundary premise | Original critique remains Revise; plan records rejection, native shared600s lock and actual future gate outcome | No new owner choice or second critique required |

The refinements preserve the confirmed two-variable authority, runtime
accounting and mandatory failure-to-rollback direction. No significant
unaccepted design decision or early resumption across an unresolved owner
decision is evidenced. P01 completion denotes execution of its rollback
alternative, not satisfaction of AC3/AC4.

## Critique and Material Revision Assessment

* Original critique: Complete / Revise, two Medium findings. Its verdict and
  findings are preserved, not converted to a passing critique.
* PC-001: applied to FR5/AC3/details. The helper has an executor-assessment
  gate rather than accepting source labels alone. No actual generated answer
  reached that gate, so no successful claim-to-source evaluation is credited.
* PC-002: rejected with an explicit rationale. The binding supplied parent
  boundary lacks the worker-local filesystem prohibition assumed by the
  critique and explicitly requires /tmp/ama-rpi-heavy.lock for heavy gates.
  The rejection is supported for that parent scope; this reviewer neither
  accesses that path nor runs a gate. No gate success or changed-tooling
  authority follows from rejecting the finding.
* No fresh critique was performed. Readiness/serialization fixes are bounded
  implementation refinements with recorded causes and reconciled plan/details;
  they do not justify another Review or historical evidence replacement.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Activation acceptance is unmet and timeout evidence cannot establish dispatch or cost

* Related scope: FR4/FR5, AC3/AC4, P01-T03, B1 and Follow-Up Item1.
* Evidence: exact continuation plan/details/changes/state; second permitted
  sanitized receipt has failure.stage=enabled_live, type=TimeoutError,
  activation_verified=false and no enabled assistant HTTP result. The helper
  groups reload, authenticated content, launcher, consent and send/response
  under that stage, with request events retained only in memory.
* Impact: no actual AI response, grounded pest prose, thin AI label, collapsed
  enabled sources or enabled out-of-scope rules/manual route is established.
  The precise substep, dispatch, server outcome, reservation, paid completion
  and spend are unknown. Neither SQL/model failure nor zero paid calls can be
  inferred. Final safe rollback cannot satisfy the owner's activation request
  or support issue closure.
* Destination: later rpi-research in the distinct timeout follow-up, not a
  current fix, another model probe or a repeat Review.
* Smallest useful next action: retain the existing failure evidence; scope
  safe finite substep/status/dispatch diagnostics and a separately authorized
  sign-in allowance before any live reproduction. Any helper correction can
  then go to a later rpi-implement invocation within established authority.
  A request after the exclusive November1 expiry also requires a new owner
  decision; November15 redeploy authority is not such a decision. Do not
  reinstate the waived ledger pre-read or bypass runtime accounting.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Authorized local persistence and full-gate closeout remain pending

* Related scope: P02-T02, AC6.
* Evidence: plan checkbox remains open; details/changes/state explicitly
  hand off Review before local commit/full gate. Initial git status shows the
  six continuation artifacts untracked; no current continuation gate result
  is supplied.
* Impact: this one Review completes the Review portion only. There is no
  committed continuation candidate or exact-head gate evidence and no basis
  for an overall completed/passing-loop or publication claim.
* Destination: distinct parent-owned local-closeout residual item, not an
  implementation defect or a reason to run Review again.
* Smallest useful next action: preserve this original Not accepted outcome
  and all original evidence, then let the authorized parent perform the
  local-only identity-safe commit and ordered full-gate attempt, recording
  actual failures. This reviewer does neither. No push, PR, issue checkbox
  change, issue closure, merge or receipt fabrication is authorized.

## Defects

No separate unresolved application/source defect is established by this
boundary. The serializer/readiness/Single-mode restoration defects encountered
during execution are recorded and addressed in the final bounded wrapper.
The timeout is an evidence gap, not a diagnosed SQL/model/source defect.
There is no unsupported activation-success claim to correct.

## Plan Follow-Up Assessment and Routed Findings

| Item | Why outside immediate scope | Owner / destination / next action |
|---|---|---|
| RV-001 / plan Follow-Up1 |2/2 sign-ins exhausted; activation failed and baseline restored | Parent scopes distinct rpi-research timeout investigation; obtain new login authority before reproduction |
| Plan Follow-Up2 | No actual generated content exists here; structural checks cannot establish human or resident acceptance | Owner/human content and operational/resident reviewers in a distinct later acceptance exercise |
| Plan Follow-Up3 | Local SQL gate setup is conditional on a future actual local-gate failure, not a live SQL prerequisite | Parent local-closeout owner records actual gate result; separate local integration setup work only if reproduced, with no live-SQL/skip substitute |
| Plan Follow-Up4 | Runtime admission failure has not been observed; SQL migration is outside authority | Owner separately authorizes private accounting investigation only if supported by later evidence; no pre-read revival or assumed migration |
| RV-002 | Ordered post-Review local persistence/gate work is still due | Active parent local-closeout item; preserve original Review and report actual gate status |

These follow-ups remain outside active implementation completion and activation
acceptance claims. No item is silently added to P01, converted into a defect
or used to authorize a third login. No current rpi-plan decision gap is found.
Later authorized implementation of routed work does not require this Review
to run again.

## Validation Evidence

| Check | Status | Evidence and limit |
|---|---|---|
| Local git status and branch | Passed | Requested topic; existing continuation files retained; no staging/commit |
| Six permitted projection SHA256 comparisons | Passed | All helper/result hashes match changes annex; no helper execution |
| FR1 original private backup | Passed as supplied evidence | First receipt records six captures before mutation and exact hashes; raw bytes/permissions not independently reopened |
| Disabled, anonymous and no-consent baseline | Passed as recorded | Both receipts: health200, anonymous403, login200, client no-request, server400, disabled rules/manual route |
| First enabled serialization comparison and original activation | Failed | Original equality false; original activation exit1; original rollback flag remains false |
| Supplementary REST/traffic recovery | Failed as supplied history | Schema rejection, reused suffix failure and Single-mode traffic rejection retained; async acceptance is not completion |
| Second enabled configuration and readiness | Passed as recorded | Seven readiness reads plus all enabled invariant Booleans; source enforces wait criteria |
| Enabled authenticated browser | Failed | TimeoutError at enabled_live; no observed enabled response; substep/dispatch/spend unknown |
| Actual AI, entailment, thin label, enabled collapsed sources and out-of-scope response | Unavailable | No observed response; cannot accept FR5/AC3/AC4 |
| Final rollback/config/readiness/traffic/health | Passed as recorded | Four readiness reads; all restored invariants; owner-safe-173404 ready100%; health200/anonymous403 |
| Original-to-final raw equality | Not independently rerun | Explicit executor/user reconciliation accepted as supplied; allowed final receipt directly compares attempt2 baseline |
| Existing runtime accounting/cap/expiry source contract | Passed source inspection only | Reservation before transport;2000 cents; exclusive2026-11-01; no live accounting/headroom assertion |
| Live SQL, model, cloud, browser or another login during Review | Skipped | Prohibited; no live revalidation or extra paid probing |
| Human content, resident, WCAG acceptance | Not performed | Outside this operational evidence and no actual generated answer |
| Current continuation local commit/full gate | Pending | Must follow this original Review and local candidate commit; previous failed gate is historical |

No source tests or gate were run by this Review. There are no source changes
to validate, and mocked tests would not replace the missing actual-AI proof.

## Blockers and Remaining Work

* Activation blocker: RV-001 and state B1; no further login or live retry under
  the exhausted allowance. Root cause, dispatch and spend remain unknown.
* Review blocker: none; the bounded evidence supports a credible Complete
  Review and Not accepted activation verdict.
* Remaining active work: parent P02-T02 local-closeout portion, RV-002. The
  original Review must remain before commit/gate; any current gate result
  must be recorded truthfully without changing this Review's original verdict.
* No publication, hosted approval or whole-issue completion is established.

## Outcome and Closeout Routing Record

* Review execution: Complete.
* Implementation execution: P01/P02-T01 Complete through rollback; full
  continuation Partial pending local closeout.
* Outcome: Not accepted. Authorized scope and final effective restoration are
  supported, but actual activation and AC3/AC4 are unmet; AC6 remains partial.
* Severity counts: Critical0, High1, Medium0, Low1.

| Finding class | Destination | Owner / next action |
|---|---|---|
| Implementation defect | None established | Do not diagnose or fix an unknown SQL/model issue |
| Decision gap or invalid assumption | None currently unresolved | Any new sign-in/expired-pilot authority is a future explicit owner decision |
| Material evidence gap | RV-001: distinct later rpi-research | Parent timeout follow-up with bounded diagnostic plan and new authority before live work |
| Non-blocking residual work | RV-002: parent local closeout | Preserve original evidence/Review; authorized local commit then full-gate actual outcome |
| Other existing residual follow-ups | Plan Follow-Up2-4, distinct owners above | Human acceptance and conditional local/runtime SQL work remain separate |

## Artifacts

| Artifact | Description |
|---|---|
| [.copilot-tracking/research/2026-10-30/resident-ai-activation-563-owner-enable-research.md](.copilot-tracking/research/2026-10-30/resident-ai-activation-563-owner-enable-research.md) | C1-C10 research and binding decision |
| [.copilot-tracking/plans/2026-10-30/resident-ai-activation-563-owner-enable-plan.md](.copilot-tracking/plans/2026-10-30/resident-ai-activation-563-owner-enable-plan.md) | Current FR/AC, markers, critique dispositions and follow-ups |
| [.copilot-tracking/details/2026-10-30/resident-ai-activation-563-owner-enable-phase-details.md](.copilot-tracking/details/2026-10-30/resident-ai-activation-563-owner-enable-phase-details.md) | Detailed execution and local-closeout boundary |
| [.copilot-tracking/changes/2026-10-30/resident-ai-activation-563-owner-enable-changes.md](.copilot-tracking/changes/2026-10-30/resident-ai-activation-563-owner-enable-changes.md) | Preserved adverse history, safe annex and final reconciliation |
| [.copilot-tracking/reviews/plans/2026-10-30/resident-ai-activation-563-owner-enable-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/resident-ai-activation-563-owner-enable-plan-critique.md) | Original Complete / Revise critique |
| [.copilot-tracking/rpi-sessions/2026-10-30/resident-ai-activation-563-owner-enable-state.json](.copilot-tracking/rpi-sessions/2026-10-30/resident-ai-activation-563-owner-enable-state.json) | Automatic parent state and blocker B1 |
| [src/api/src/zava_forward/api/resident_demo/aoai.py](src/api/src/zava_forward/api/resident_demo/aoai.py) | Narrow accounting, configuration and answer contract inspection |
| [src/api/src/zava_forward/api/resident_demo/app.py](src/api/src/zava_forward/api/resident_demo/app.py) | Consent and assistant routing contract |
| [src/api/src/zava_forward/api/resident_demo/assistant.py](src/api/src/zava_forward/api/resident_demo/assistant.py) | Exclusive expiry constant |
| [infra/sql/resident-assistant.sql](infra/sql/resident-assistant.sql) | Source-only reservation ceiling and expiry |
| [.copilot-tracking/reviews/logs/2026-10-30/resident-ai-activation-563-owner-enable-review.md](.copilot-tracking/reviews/logs/2026-10-30/resident-ai-activation-563-owner-enable-review.md) | This single independent Review |

## Next Steps

Return this one Review to the active parent. The parent may complete authorized
local persistence/full-gate closeout, retaining the original Not accepted
activation outcome and all failures. Route RV-001 to a distinct later
rpi-research timeout follow-up with new authority before any live retry.
No current fix, repeated Review, third login, push, PR or issue closure.
