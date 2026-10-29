---
title: "Independent Review: demo-sites-live-correction"
description: "Original child-task Review of bounded live correction evidence."
ms.date: 2026-10-29
---

## Opening Review State

* Task: 5a7ca259-9fe8-407c-accf-fc965757c10e, demo-sites-live-correction.
* Interpreted goal: independently compare the child plan, details, critique, changes, state and fresh machine evidence against the owner's bounded live-correction authorization.
* Scope: one original Review of this child task only; parent demo-sites-correction artifacts remain historical and unchanged.
* Evidence readiness: named child artifacts exist; substantive evidence comparison is pending.
* Acceptance basis: current owner instruction, child acceptance criteria and original critique dispositions; execution completion is separate from acceptable outcome.
* First comparison boundary: reconcile plan markers and changes with machine evidence, then inspect executor sources and sanitized external evidence where needed.
* Read-only boundaries: only this review record may be written. No delegation, fixes, tests, gh, push, authenticated HTTP, environment/private-data reads, secrets output, live mutation or parent rerun.
* Initial blockers: none established; local evidence commit and publication gate are explicitly pending, not authorized by this Review.

## Scope and Evidence

* Review date: 2026-10-29.
* This is exactly one original independent child-task Review, not a rerun, amendment or relabelling of the parent Review.
* Compared artifacts:
  * .copilot-tracking/research/2026-10-29/demo-sites-live-correction-research.md
  * .copilot-tracking/plans/2026-10-29/demo-sites-live-correction-plan.md
  * .copilot-tracking/details/2026-10-29/demo-sites-live-correction-phase-details.md
  * .copilot-tracking/reviews/plans/2026-10-29/demo-sites-live-correction-plan-critique.md
  * .copilot-tracking/changes/2026-10-29/demo-sites-live-correction-changes.md
  * .copilot-tracking/changes/2026-10-29/demo-sites-live-correction-evidence.json
  * .copilot-tracking/rpi-sessions/2026-10-29/demo-sites-live-correction-state.json
* Independently inspected external evidence under the task's supplied session files root: live.py, images.py, deploy.py, sql-worker.py; commands.jsonl; retained command outputs; full before/final management responses; separate auth responses; revision and replica inventories; SQL execution/template/results; archive and image inspection receipts; ACR restoration receipt; anonymous probe bodies. Raw configuration, environment and secret-reference values were neither printed nor copied here. Executor code was read, not executed or imported.
* Repository context: docs/case_study_48_original.md, opening context of docs/case_study_48_addendum.md and docs/reference/README.md, and docs/reference/memory.md. Pinned SQL batch and packaged expiry policy were inspected with local git reads. No consequential regulatory or broad UX acceptance is assessed.
* The supplied preserved parent local-validation results are historical, accepted for reuse and not independently rerun. Parent artifacts and original critique remain unchanged by this Review. No claim is made that this Review independently reconstructed their initial byte-for-byte baseline.

## Execution Status

* Review execution status: Complete.
* Implementation execution: P01, P02 and P03-T01 completed; P03-T02 remains administratively incomplete until the coordinator reconciles this Review and performs the authorized local evidence commit. Complete Review execution does not mark that pending commit complete.
* Evidence boundary: recorded operational observations through the final 2026-10-29 10:24Z comparisons, independently checked against retained evidence during this Review. No new Azure query, HTTP request, test, build, commit or publication was performed.

## Plan-to-Change Reconciliation

| Current plan scope | Changes and machine evidence | Reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Full app/auth/history, eight jobs and ACR backups | Reconciled | Full private backups inspected only through sanitized comparisons; explicit resident AuthConfigNotFound preserved. |
| P01-T02 | One successful REST start, h6mm4i9 Succeeded; transactional view worker; 17 columns and 522/522 counts | Reconciled with evidence limitation | Retry0 before start and retry1 restored; planned prior view-definition fingerprint absent, RV-002. |
| P02-T01 | Pinned tracked archive, two local builds and registry receipts; exact ACR restoration | Reconciled | Approved local-to-ACR route correctly distinguished from hosted ACR Tasks. Normalized-rule cleanup completed before app writes. |
| P02-T02 | Resident then employee Healthy, exact digest, latest=ready, one revision each | Reconciled | Resident verification-only continuation followed a local selector error; no repeated deployment or rollback. |
| P03-T01 | January authority precisely parked after both healthy | Reconciled | Conditional parking is an accepted branch, not delivery of #521. |
| P03-T02 | Evidence reconciled for this one independent Review; local commit pending | Partial by design | Coordinator-owned persistence remains; no false publication or full-plan-completion claim. |
| Follow-Up Items | Source/credential/row prerequisites and publication gates | Reconciled | Distinct owner/coordinator work, not new active live operations. |

## Completed Work Assessment

| Marker | Evidence and assessment | Validation |
| --- | --- | --- |
| P01-T01 | Exact before/final app projections and all eight job projections independently compared. Resident auth absence is specific, not a generic failed read; employee auth compared separately. | Passed, retained evidence. |
| P01-T02 | Worker hash matches exported proof. AST-extracted SQL batch exactly equals the third GO batch at 77c87e0d76b827544fde9b2f2ce7dfbd9d879232 and its recorded SHA256. Worker explicitly begins a transaction under XACT_ABORT, checks principal SID/rights ceiling before and after, checks allowlist count/checksum, reads the 17-column projection and count under EXECUTE AS USER, REVERTs before COMMIT, and emits committed status only afterward. | Passed for successful execution; RV-002 limits pre-change fingerprint evidence. |
| P01-T02 | Successful-start preconvergence response proves retry0, Manual and Succeeded provisioning. No Running/Processing execution appears in the retained preflight list. Exactly one successful REST start is journalled, and final execution command equals the hashed worker. Final full job projections match originals, including retry1. | Passed. One start plus retry0 supports the single non-retrying execution contract; no separate platform attempt counter is claimed. |
| P02-T01 | Archive SHA256 independently matches eca35aaab6c6921c0fc898b8d36d17f61ae50a168f2c32ef6ca1ea1b58b2fe4a; tar members are confined to src; pinned git tree matches 22af89af213f65d89011ea264f4f653de35dbeac. Journal records immutable-SHA archive/build commands. Local image source labels and post-push RepoDigests agree with receipt. | Passed locally; registry manifest/config body checks and old-digest presence are executor-observed receipts, not newly reproduced remote reads. |
| P02-T01 | Fresh prewrite ACR projection equals baseline; window readback has public Enabled, default Deny and exactly one VM rule. Restoration readback proves public Disabled before normalized-rule cleanup; final complete stable ACR response equals baseline without policy-timestamp exclusions. Receipt agrees with exported registry evidence: 44.170433 seconds, below 600 seconds. Owned Docker credential directory is absent. | Passed. Cleanup correction was detected by strict equality, not hidden by normalization. |
| P02-T02 resident | ca-resident-demo--res-live-20261029-102142 is Healthy/Provisioned, active with trafficWeight100 and one ready replica; target and app digest match sha256:3ab5febcc40429fd709940b272fc58ab33ff14190494e45c87eb55f307491086. Full protected equality permits only image/suffix plus documented service fields. | Passed; min0/max1 and separate absent auth preserved. |
| P02-T02 employee | ca-cutover-test-demo-api--emp-live-20261029-102306 is Healthy/Provisioned, active with trafficWeight100 and one ready replica; target and app digest match sha256:5215e019a78a8c7ae07987dcd26dbcabbe87eb4b5ecf2077688f7a9ca5f9034e. Employee update follows resident acceptance/log collection in the journal. | Passed; min0/max4 and full separate auth preserved. |
| P02-T02 history | Independently compared full revision-name sets: exactly the named target added for each app, none removed. Resident rollback ca-resident-demo--rollback-20261029-073718 remains. | Passed. No second forward/recovery revision inferred. |
| P02-T02 probes | Stored curl status outputs and body hashes agree with every exported probe. Both /healthz200; /health404 resident and 401 employee. Public shells are byte-equal to their exact archived source files; employee /app, /app.js and /ops.js each401. | Passed for anonymous shell/health/denial scope only. |
| P03-T01 | Local ancestry check confirms exact #521 commit edd7f4dedd4b602a55bf2bc651c81b1b85521aed is not an ancestor of pinned main. Packaged maximum_expiry_utc is 2026-12-31T23:59:59Z. | Parking justified; no January configuration, credential or SQL-row mutation is represented as completed. |

## Implementation-Time Plan and Detail Update Assessment

| Affected scope | Change and trigger | Reconciliation and assessment |
| --- | --- | --- |
| P01-T02 / PC-001 | Inherited retry1 required temporary retry0; empty accepted PATCH response, restore provisioning conflict and locally rejected CLI start required tooling reconciliation. | Revised critique contract and changes preserve no ambiguous SQL reapply. Retained successful sequence shows one REST start after retry0, completed execution, and exact final job restoration. Multiple configuration attempts are not misrepresented as multiple SQL executions. |
| P02-T01 / PC-003 and PC-005 | Immutable source binding and fresh ACR equality added; Azure normalized the owned /32 rule to a bare IP, so initial successful removal command did not restore equality. | Exact-rule cleanup while public Disabled is the bounded original restoration, not a new exception or unrelated network change. Final proof precedes all app writes. Failed wrapper remains recorded as failed. |
| P02-T02 / PC-002 and PC-004 | Separate auth comparisons and employee failure contract made explicit. Resident source-asset selector failed locally after runtime success. | Read-only continuation verified the same target before employee deployment; no speculative rollback, retry or new authorization was inferred. |
| P03-T01 | Both sites healthy but #521/source, private credential and approved-row prerequisites unresolved. | Plan, details, changes and state consistently park authority. Current owner instruction explicitly permits that branch. |
| P03-T02 | Review and local persistence intentionally separated from live delivery. | State correctly has Review active, and plan leaves P03-T02 unchecked. Coordinator must reconcile afterward; Review does not mutate those artifacts. |

These are compatible implementation-time reconciliations of confirmed intent.
No unaccepted significant decision change or new live scope was found.
Nonblocking evidence omissions are recorded below rather than silently treated
as satisfied.

## Critique and Material Revision Assessment

* Original critique remains Complete / Revise, with 2 High and 3 Medium findings. Its historical outcome is not overwritten by later execution evidence.
* PC-001: explicit transaction, effective-principal projection, retry0, single start and final exact job restoration are supported by worker, retained convergence response and execution evidence. Limitation: no separate attempt-counter receipt; the required non-retrying configuration and single successful start are demonstrated.
* PC-002: explicit employee failure/recovery and no-touch-resident contract exists in details and executor. Neither app actually failed startup; failure-only log/recovery correctness is not experimentally established by this successful run.
* PC-003: immutable SHA, archive and tree binding are supported. Pinned main is the recorded fetched main; local fetch is not rerun here.
* PC-004: independent full employee auth equality and exact resident AuthConfigNotFound are supported before/after, separately from app equality.
* PC-005: fresh complete stable prewrite ACR equality, expected-state readbacks, private-first closure and exact final equality are supported.
* Dependent-work order is supported: SQL completion/restoration before image rollout; exact ACR restoration before resident; complete resident acceptance before employee; authority parking after both.
* Direct planner corrections were reconciled in the current plan/details before their affected successful operations. No second critique or second Review is required or performed.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner or next action | Assessment |
| --- | --- | --- | --- |
| January source and authority | #521 is unmerged and this task's single resident forward revision is used | Owner/coordinator: source integration/review and explicit additional revision authorization | Open, accepted parking; not an implementation defect or issue closure. |
| Owner-private credentials and approved existing rows | No operator credential receipt, Create-only helper unsuitable for existing-secret Modify, no individually approved row renewal set | Owner: private password/verifier/signing-key workflow; reviewed exact-version Modify; named synthetic rows and transactional migration | Open, distinct protected follow-up; no permission expansion or blanket renewal authorized. |
| Authority operational prerequisites | January funding/headroom, expiry/alerts, rotation/rollback/reference-refresh and owner sign-in acceptance remain | Owner/coordinator: follow exact five-step parking checklist in changes | Open; no cost query or authenticated test performed. |
| Evidence local persistence | Review must precede the authorized local evidence commit | Active parent: reconcile P03-T02 and persist original/new evidence using existing approved privacy-safe identity and required trailer, without gh/push | Pending by design; not complete. |
| Publication | Complete local gate, exact-head assessment and hosted/human approval are separate | Coordinator, only under later applicable authority | Pending; no gate receipt, approval or push claimed. |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Four historical command output streams are no longer retained

* Related scope: P01-T02 and the command-journal retention requirement.
* Evidence: Independent recomputation against all 189 journal entries confirms four mismatches: entry24 sql-job-preflight stdout; entry27 sql-restore-job stderr; entry35 sql-job-preflight stdout; entry45 job-preservation-job-cutover-test-init stdout. Their repeated-label paths now contain later output. All exported retained_*_matches flags agree with the independent check; the changes appendix explicitly discloses the loss.
* Impact: Original hashes, timestamps and exits remain, but those four historical byte streams cannot be independently re-examined. Do not equate complete journal metadata with complete log-byte retention. Intact successful-start convergence, worker/execution, final job proofs and app/ACR proofs support the present bounded verdict, so this is not a material live-acceptance blocker.
* Destination: Distinct follow-up, evidence-retention tooling owner; not active live correction.
* Smallest useful next action: In a later task, make every command-output filename invocation-unique and append-only. Preserve this disclosure and original hashes; do not fabricate replacement historical bytes or rerun SQL to manufacture them.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Planned pre-change SQL view-definition fingerprint was not captured

* Related scope: P01-T02 phase-details instruction to capture the prior definition hash and column names.
* Evidence: The preserved hashed sql-worker.py reads prior column metadata, not OBJECT_DEFINITION/sys.sql_modules or a definition hash. sql-results.json and exported sql/sql_worker evidence retain the prior 16-column names and the new batch hash, but no prior view-definition fingerprint. The new batch's hash must not be relabelled as the old definition hash.
* Impact: The successful transaction and current shape/count/principal checks are supported, but this specific pre-change provenance requirement is unfulfilled. It limits historical SQL-definition comparison, not the demonstrated current-main startup prerequisite. No SQL row access, grant or allowlist mutation is implied.
* Destination: Distinct follow-up, SQL evidence owner.
* Smallest useful next action: A later task may identify an already-existing trustworthy prior-definition receipt, if available; otherwise preserve the omission explicitly and require a pre-change definition fingerprint for future authorized view operations. Do not query the changed view and present its hash as historical, reapply SQL, or rerun this Review.

## Defects

* No material implementation defect or unaccepted decision gap was established in the successful live-delivery boundary.
* RV-001 and RV-002 are nonblocking historical evidence deficiencies, not permission to repair live resources or rewrite original evidence.

## Routed Findings

| Finding | Destination | Owner or next action | Reason |
| --- | --- | --- | --- |
| RV-001 Low | Distinct evidence-retention follow-up | Evidence-tooling owner, invocation-unique retained logs | Historical traceability deficiency; current acceptance proofs remain retained. |
| RV-002 Low | Distinct SQL-provenance follow-up | SQL evidence owner, existing prior receipt or explicit permanent limitation | Missing nonblocking pre-change fingerprint, not a current SQL fix. |

Later work does not require this original Review to run again.

## Residual Work

* Preserve both findings as separate later-task inputs, without modifying original critique, parent evidence or completed operational history.
* Coordinator must finish P03-T02 local evidence persistence after consuming this Review; no commit is made by this reviewer.
* January authority and publication remain the distinct owner/coordinator follow-ups assessed above, not active task defects.

## Blockers and Remaining Work

* Review blockers: none; retained successful-path evidence is sufficient for a credible bounded verdict.
* January authority blockers: unmerged source/cap, used revision allowance, owner-held private credentials, exact-version Modify and individually approved existing synthetic rows, plus the recorded operational/funding prerequisites.
* Remaining active plan work: P03-T02 administrative reconciliation/local commit only. All live steps authorized for this Review remain read-only.
* Pending publication prerequisites are not failures of an unrun gate and do not authorize a push.

## Validation Evidence

| Check | Scope | Status | Summary |
| --- | --- | --- | --- |
| Read-only Python SHA256/journal comparison | Four executor sources, 189 commands and all available retained stdout/stderr hashes | Passed with disclosed limitation | Source hashes and journal/export core metadata agree; exactly four historical stream mismatches; zero retention-flag disagreements. |
| Read-only Python protected projections | Full before/final apps, separate auth, eight jobs and ACR | Passed | Only documented app runtime/system fields and approved image/suffix differ; jobs restore retry1/Manual; ACR full stable equality. Raw values not printed. |
| Read-only Python revision/replica/probe comparison | Both named apps and retained anonymous HTTP results | Passed | One added revision each, none removed; Healthy/Provisioned/active100, ready replica; probe status/body hashes and archived shell bytes agree. |
| Read-only AST/git/hash comparison | Pinned source, SQL batch, worker and archive | Passed with RV-002 limitation | Exact third batch and source/tree/archive binding; explicit transaction and effective SELECT; prior-definition fingerprint absent. |
| Retained SQL execution/config evidence | Existing private initializer only | Passed | h6mm4i9 Succeeded, one REST start, retry0 before execution, committed17-column result with allowlist/view522, final full job equality. |
| Retained registry receipts and executor inspection | New source/config/remote digests and retained old digests | Passed as recorded evidence | Remote manifest/config verification code and receipts agree with local image bindings; not independently re-fetched remotely. |
| Recorded anonymous /healthz and public shell checks | New named targets | Passed | Both healthz200; health404/401 honestly recorded; employee protected assets401. No authenticated behavior inferred. |
| Bounded startup logs | New revisions | Passed as recorded evidence | Both streams retrieved; no selected error markers, system ContainerStarted. Bounded app-level system logs do not prove exhaustive target-specific error absence. |
| Fresh Azure queries / fresh HTTP / cost queries | Review | Skipped | Existing retained machine evidence suffices; no live query or request needed. |
| Historical core/API/SQL/browser regressions | Parent validation boundary | Skipped | Reused as historical per owner direction, not rerun or relabelled fresh. |
| Authenticated sign-in, cross-case/session, chat/model, accessibility and future recovery execution | Outside authorized Review acceptance | Skipped | Explicitly prohibited or outside scope; anonymous health is not a substitute. |
| Local commit / complete publication gate / hosted and human approval / push | Persistence and publication | Pending / unperformed | Local commit remains parent-owned; publication is not authorized or certified here. |

## Outcome

* Outcome: Residual work.
* Rationale: Ordered live correction and the expressly permitted authority-parking branch are supported by independently compared retained evidence. No material live defect, new decision gap or blocker to this Review was established. Two Low historical evidence deficiencies remain, and the full plan cannot be called complete while its local evidence commit is pending. This verdict neither retracts the demonstrated live success nor certifies January authority, authenticated acceptance or publication.
* Severity summary: 0 Critical, 0 High, 0 Medium, 2 Low.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Material implementation defect | None | No rpi-implement invocation advised for this bounded successful rollout. |
| Significant decision gap or invalid assumption | None | No rpi-plan invocation advised; accepted parking preserves owner intent. |
| Material evidence gap | None | No rpi-research invocation required for present acceptance; limitations remain explicit. |
| Nonblocking evidence deficiencies | Distinct follow-ups RV-001 and RV-002 | Evidence-tooling and SQL evidence owners; later tasks only. |
| Local persistence | Active parent, P03-T02 | Reconcile this record and perform only the previously authorized local evidence commit. |
| January authority and publication | Separate owner/coordinator work | Respect parked prerequisites and later authority; no push is authorized now. |

* Execution status: Complete for this original independent Review.
* Outcome: Residual work.
* Validation coverage: independent sanitized local evidence checks; recorded operational proofs; no repeated suites, authenticated requests or live mutations.
* Stop: this reviewer writes only this record and performs no implementation or second Review.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-29/demo-sites-live-correction-research.md](.copilot-tracking/research/2026-10-29/demo-sites-live-correction-research.md) | Child evidence and authorization basis |
| [.copilot-tracking/plans/2026-10-29/demo-sites-live-correction-plan.md](.copilot-tracking/plans/2026-10-29/demo-sites-live-correction-plan.md) | Acceptance criteria and phase markers |
| [.copilot-tracking/details/2026-10-29/demo-sites-live-correction-phase-details.md](.copilot-tracking/details/2026-10-29/demo-sites-live-correction-phase-details.md) | Operational contracts and critique dispositions |
| [.copilot-tracking/reviews/plans/2026-10-29/demo-sites-live-correction-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/demo-sites-live-correction-plan-critique.md) | Original Complete / Revise critique, preserved |
| [.copilot-tracking/changes/2026-10-29/demo-sites-live-correction-changes.md](.copilot-tracking/changes/2026-10-29/demo-sites-live-correction-changes.md) | Implementation history and precise authority parking |
| [.copilot-tracking/changes/2026-10-29/demo-sites-live-correction-evidence.json](.copilot-tracking/changes/2026-10-29/demo-sites-live-correction-evidence.json) | Fresh machine evidence, receipts and honest retention flags |
| [.copilot-tracking/rpi-sessions/2026-10-29/demo-sites-live-correction-state.json](.copilot-tracking/rpi-sessions/2026-10-29/demo-sites-live-correction-state.json) | Parent continuation state |
| [.copilot-tracking/reviews/logs/2026-10-29/demo-sites-live-correction-review.md](.copilot-tracking/reviews/logs/2026-10-29/demo-sites-live-correction-review.md) | This single independent Review |

## Next Steps

Active parent: consume this Complete / Residual work Review, preserve its original
findings and the critique, finish the authorized P03-T02 local persistence, and
route RV-001/RV-002 to distinct later tasks. Keep #521 parked and publication
pending. No further live operation, push, delegation or second Review is
authorized by this record.
