<!-- markdownlint-disable-file -->
# Review: Both demo sites redeploy

## Opening Review State

* Task ID: 3897222c-2d62-4e25-a059-eecfbdce51d0.
* Review date: 2026-10-29.
* Interpreted review goal: independently assess the entire supplied redeployment task once, preserving failures and separating safety from requested delivery.
* Review scope: AC1-AC6, all plan phases and implementation-time updates, PC001-PC005, evidence quality and distinct follow-ups.
* Evidence readiness: the six supplied artifacts exist; detailed comparison and independent receipt/config comparison are pending.
* Acceptance basis: confirmed two-app, exact-main, exact-configuration boundary and the current plan; no assumption of success from the handoff.
* First comparison boundary: reconcile plan, details, critique and changes before comparing safe receipts and private baseline/final projections.
* Active read-only boundaries: write only this record; no nested agents, fixes, cloud mutation, gh, SQL, secret-value reads/printing, private configuration output or expanded security audit.
* Initial blockers: none to starting the review; resident delivery failure and unavailable diagnosis require assessment, not repair.

## Scope and Evidence

* Task: both-demo-sites-redeploy, ID 3897222c-2d62-4e25-a059-eecfbdce51d0.
* Assessed boundary: the entire supplied task, including AC1-AC6, P01-P03, PC-001 through PC-005, operational changes and failure recovery. This is the task's one independent post-implementation Review, not a second implementation or a security audit.
* Plan: .copilot-tracking/plans/2026-10-29/both-demo-sites-redeploy-plan.md.
* Details: .copilot-tracking/details/2026-10-29/both-demo-sites-redeploy-phase-details.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-29/both-demo-sites-redeploy-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-29/both-demo-sites-redeploy-changes.md.
* Research: .copilot-tracking/research/2026-10-29/both-demo-sites-redeploy-research.md.
* Machine evidence: .copilot-tracking/changes/2026-10-29/both-demo-sites-redeploy-evidence.json.
* Additional evidence: the supplied external redeploy.py executor and safe receipts; private baseline/final app and ACR backups compared only in memory without values in output; retained revision inventories compared in memory. The external evidence root is identified in the supplied machine evidence, not copied into the repository.
* Context: original case study, addendum purpose/resident-governance context, reference index and owner memory; historical sixteen-column deployment evidence in .copilot-tracking/changes/2026-10-27/deploy-resident-474-changes.md; current src/core/src/zava_forward/core/resident_showcase_sql.py. No regulatory, product, UX or whole-repository audit is implied.
* Review writes: only this record. Existing untracked parent artifacts on ops/sites-redeploy-20261029 were neither changed nor committed.

## Execution Status

* Review execution status: Complete.
* Implementation execution status: Partial, independently consistent with the unchecked resident-main task and pending parent-only local commit.
* Outcome: Not accepted for the requested two-sites-on-latest-main result.
* Review execution evidence: one direct comparison of all supplied artifacts, receipt integrity/source checks, a separately written type-strict configuration comparator, and bounded read-only auth/revision checks on only the two authorized apps. No nested agents, fixes, retries, authenticated/model requests or cloud mutations occurred during Review.
* Review is not blocked: the evidence supports a credible negative verdict and a bounded positive safety assessment even though the resident root cause is unknown.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Baselines and both clean local builds complete | Reconciled | Exact source archive independently matches all 388 tracked src files; employee original revision inventory was active-only, not a prospective complete inventory. |
| P01-T02 | Successful pushes/admission; three short ACR windows restored | Reconciled with RV-003 | Actual restoration passed; executable restoration sub-deadlines do not fully implement PC-001's frozen contract. |
| P02-T01 | One successful employee forward revision | Reconciled | Final digest, exact protected fields, auth, readiness and anonymous evidence support completion. Read-only tooling corrections did not create a second revision. |
| P02-T02 | One resident forward failure and one verified old-image recovery | Correctly incomplete | Requested new-main readiness and exact forward refs failed; recovery is safety success, not completion of this task. RV-001 and RV-002. |
| P02-T03 | Final app/ACR safety proof and retained failures | Reconciled | Both latest/ready final revisions are healthy; only employee is latest main. |
| P03-T01 | One Review pending at handoff | Completed by this record | Parent owns recording this original result; no repeated Review is required or authorized. |
| P03-T02 | Parent-only local evidence commit pending | Correctly pending | No commit, push or publication acceptance was performed by Review. |
| Follow-Up Items | Resident diagnosis/new authorization, authenticated review, publication | Reconciled as separate work | None is silently added to active implementation or used to mark resident completion. |

### Acceptance Criteria

| Criterion | Assessment | Evidence and limits |
| --- | --- | --- |
| AC1 | Passed | Local HEAD and origin/main both d70ee60ab3d7346a9991cf64382d9985f4d09f2e; src tree 6684959daaa64df7f8768c4fddb24406f198a308. Export hash matches receipt and archive contents exactly match tracked main. Both successful build receipts identify correct Dockerfiles, src context, platform and source labels. Builds were not repeated. |
| AC2 | Passed at recorded execution boundary | Unique-tag new index/platform/config chains are separately recorded, both old manifests were fetched successfully, and every window reports exact restoration/credential cleanup. Independent comparison of saved employee/resident post-window and final ACR responses finds zero protected differences using only the listed exclusions. No fresh registry reopening, manifest fetch or deletion was performed by Review. |
| AC3 | Failed for full task | Employee one forward revision is latest/ready, Healthy/Provisioned, active100%, on new digest 41db94689ae934e3daa6c7f8fb57d8de5cc58a53995efd50217189231ac1f0c1. Resident forward digest 1c0881a9855ce7ffcaad26da06422a7c7be7d9cf536073ec9c5d955889882354 failed activation. Final resident rollback is healthy on old fab6a85318f65db006bc610f3b3aff8ae799046d1b9a1813662b3b315c1b6fc7. The allowed failure-only extra revision is justified, not a second forward attempt or satisfaction of latest-main acceptance. |
| AC4 | Final preservation passed; forward preservation failed | Independent complete app comparisons and live auth equality pass for both final apps. min0/max4 and min0/max1, configuration, identity, registry and ingress are exact. Resident forward comparison reproduces precisely two added empty value keys beside secretRefs; these were restored, never normalized away. Continuous exact preservation therefore cannot be claimed. |
| AC5 | Employee passed; resident target failed; recovery passed bounded checks | Employee health/root200, main-welcome byte equality and protected app/JS401 are recorded with ready-container/console proof. Resident forward had no ready container and root was not main-shell-equal despite HTTP200. Recovery has healthy ready-container evidence, public/health200 and known synthetic sign-in markers; current-main equality is explicitly false. No authenticated feature, exhaustive data-isolation or human acceptance is established. |
| AC6 | Partial at this handoff | Ordered evidence, original Complete/Revise critique with dispositions, and this one Complete Review exist. Parent-only local commit, trailer/identity verification and final handoff reconciliation remain pending. No gh or push was used by Review; no publication receipt or hosted/human approval is claimed. |

## Completed Work Assessment

| Related marker | Evidence/files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | Research, changes and evidence JSON | Full management backups and exact-main builds, no app source changes | Source-export and two build records | Archive/hash/main checks passed; private backup root0700 and private configuration backups0600 | Delivery artifacts built; RV-004 records local lock-path nonconformance. |
| P01-T02 | Evidence records employee-push-attempt1-result, employee-push-result, resident-push-result | Push two unique images and restore private registry policy | Windows21.70s,18.81s,19.80s; zero reported cleanup errors | Exact ACR comparison passed; owned credential/export files absent | Actual safety result supported; RV-003 remains an executor-contract defect, not an observed restoration failure. |
| P02-T01 | employee-deploy-result, employee-final-log-summary and final-result | Employee image/suffix-only update | emp-main-20261029-072248, one added revision | Protected app/auth equality and recorded runtime/HTTP proof pass | Accepted bounded employee result; no rollback. |
| P02-T02 | resident-deploy-result and resident-recovery-result | Failed new-main activation, then authorized old-image recovery | res-main-20261029-072628 failed; rollback-20261029-073718 ready | Forward refs/startup failed; final exact equality and recovery readiness passed | Recovered-but-redeploy-failed; do not mark complete. |
| P02-T03 | final-result, saved final app/ACR responses | Cross-check final protected state and retained revisions | requested_redeploy_complete=false, safety_checks_passed=true | Independent comparison and fresh authorized revision/auth reads agree | Final safety accepted within evidence limits; no product acceptance. |
| P03 | This review and parent handoff | Preserve original outcome and route later work | This one record | Review-only diff/format validation; local commit remains parent-owned | Review complete, task/publication not complete. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01 digest binding | Distinguish Docker29 Id/index from actual saved config bytes | Initial employee post-push proof failed; no app mutation had occurred | Details PC-003 correction, original failure, local-config receipt and separate digest chains retained | Compatible technical correction; no new deployment authority needed | Justified read-only admission continuation, not a rebuild/re-push or rollback trigger. |
| P02 employee root assertion | Root200/main welcome instead of treating root as protected app | Actual source route and HTTP200 contradicted initial assertion | Current AC5, details and receipt require byte equality; protected /app and JS still401 | Compatible assertion correction within anonymous-only boundary | No authentication setting was loosened. |
| P02 cross-schema templates | Explicit app/revision defaults, null suffix/scale representation, original revision probes | Revision GET differs from app GET | Details list paths; complete app-to-baseline contract unchanged | Compatible evidence correction; not permission to normalize refs or whole templates | Final independent strict app comparison avoids reliance on these cross-resource accommodations. |
| P02 revision history | Use --all; prospectively capture resident, retrospectively partition employee | Installed default list was active-only | Original inventory and failures retained; method and immutable createdTime boundary disclosed | Compatible read-only repair of evidence, not prospective evidence equivalence | Current retained-set accounting credible; inability to prove historical absence of deleted inactive revisions remains explicit below. |
| P02 min0 | Anonymous health request wakes revision | Activation waits with min0 and request-driven startup | Details preserve min0 and separate wake from metadata | Within authorized curl boundary | No scale mutation or authenticated/model request. |
| P02 resident failure | Classify actual ActivationFailed rather than infer health from HTTP200 | Repeated Warning ContainerTerminated, zero replicas, old latestReady | Plan resident marker remains unchecked; changes retain original runtime failure | Existing failure-only recovery authority applies | Recovery justified; two actual forward refs differences are separate defects, not mere tooling. |
| P02 recovery method | ARM PATCH original writable template and restore own two empty-value paths | Installed image-only CLI changed ref records; preflight refused unexpected drift | Details explicitly permit only identified own-update repair; auth/other fields independently protected | Technical recovery method materially changed, but approved safety intent did not; no SQL, new forward attempt or wider repair authority inferred | Compatible restoration of baseline; RV-002 routes future executor correction rather than treating drift as accepted. |
| P02 raw-schema correction | Remove CLI-only customMetricsSettings(null) from request | First PATCH definitively rejected with no new revision; raw API schema differs | Failed-command receipt, corrected schema receipt and final exact GET retained | Not an ambiguous-write retry; same recovery suffix, one created recovery revision | Supported by supplied no-revision check and six-revision final set; no further mutation here. |
| P02 bounded logs | Parse Msg, not just Log; distinguish stopped-console unavailability | Initial system-pattern results unreliable | Original receipts retained; corrected employee summary and resident limits explicit | Compatible read-only validation correction | Zero matched errors is not exhaustive absence; failed resident cause remains unknown. |
| P02/P03 status | Partial deployment, exact final safety and separate follow-ups | Resident new main not ready despite successful rollback | Plan/details/changes agree; current source/reference evidence is labelled hypothesis | No second critique/Review or success waiver | Changes wording "No material divergence" is read as no divergence from approved intent, not denial of the substantial recovery-method change. |
| P03 identity/publication | No fresh gh identity lookup; parent local-only commit | Explicit no-gh/no-push instruction | Details document deviation and use of existing privacy-safe evidence | No new owner decision needed to obey the narrower instruction | Actual identity/trailer/commit remains unverified until parent performs it. |

## Critique and Material Revision Assessment

| Critique | Recorded disposition | Independent assessment |
| --- | --- | --- |
| PC-001 High | Applied directly | Partially realized. Actual three windows closed well inside600s with exact equality and cleanup. Current executor has start+420 forward/start+600 total deadlines, but no restoration-start+180 deadline or separate120s readback bound. RV-003. The initial local Docker inspect in verify-only admission also uses a fixed timeout rather than remaining-budget capping. |
| PC-002 High | Applied directly | Final exact-preservation proof independently reproduced with precisely the listed exclusions, strict types, ordered arrays and absent/null/empty distinctions. Resident forward failure is honestly detected and final recovery restores it. Cross-schema normalization was not allowed to leak into app-baseline comparison. |
| PC-003 Medium | Applied directly | Initial implementation still encountered Docker29 Id semantics. Subsequent docker-save config hashing and OCI platform selection correct the evidence chain; source binding, index/platform/config and local RepoDigest relationships are recorded separately. Original failed proof is preserved. |
| PC-004 High | Applied directly | Employee acceptance preceded resident update. Actual resident failure, not tool failure, triggered a single created recovery revision. Final old-image config/auth, latest/ready/active100%, ready container and HTTP proof support recovery. Schema rejection is distinguishable from ambiguous mutation. No second forward/reversion of successful employee app. |
| PC-005 Medium | Applied directly | Corrected employee welcome-byte equality and protected statuses meet the final bounded assertion; resident forward shell equality failed as it should. Recovery markers are intentionally weaker than current-main equality and cannot satisfy new-main AC5. No broad security assurance is inferred. |

* Original critique remains Complete / Revise, not rewritten to Approved. The plan records compatible dispositions; there was no second critique.
* Significant user intent was preserved: latest fetched main, exactly two apps, exact baseline settings, only failure-triggered recovery and no unauthorized schema/SQL repair.
* Dependent-work pause: employee tooling mismatches led to read-only checks, not rollback/re-update. Resident own drift caused recovery preflight to stop before overwrite; raw request rejection was checked before a corrected request. Evidence supports preservation of the successful other deployment.
* Technical corrections were described in the current details and changes. Their historical executor versions are represented by hashes, not retained replayable source versions in the supplied artifact set; do not overstate historical executable reproducibility.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Resident startup/CLI diagnosis | Cause unisolated; no SQL, secret or additional forward authorization | Parent routes RV-001 to later rpi-research | Open; research must distinguish schema and ref hypotheses without implying a live diagnosis. |
| Separately authorized resident retry | One forward allowance already consumed | Parent/owner chooses distinct rpi-plan work after research, including a new allowance and exact-template route | Valid separate follow-up, not a new P02 task or an invitation to retry now. |
| Authenticated employee/resident feature review | Anonymous deployment proof cannot establish feature/human acceptance; resident remains old image | Owner supplies a separately authorized authenticated acceptance exercise | Non-blocking to recorded safety; distinct owner follow-up, not an implementation defect. |
| Publication and Refs-only PR | Parent/coordinator owns local evidence commit and full publication/hosted/human gates | Parent completes P03-T02; coordinator satisfies required gates before any publication | Explicitly open; this Review neither runs nor waives the complete local gate, exact-head assessment or hosted/human approval. |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: The resident latest-main deployment failed and the cause remains unisolated

* Related scope: P02-T02, AC3 and AC5, resident research follow-up.
* Evidence: .copilot-tracking/changes/2026-10-29/both-demo-sites-redeploy-evidence.json records resident-deploy-result: ActivationFailed, replicas0, latest not ready, no ready container and main-shell mismatch. Changes preserve repeated Warning ContainerTerminated and unavailable stopped-revision console. final-result deliberately has latest_main_deployed=false and requested_redeploy_complete=false for the recovered old image.
* Impact: The user's central two-sites-latest-main outcome is not delivered. HTTP200 from the old ready route and successful recovery do not accept the failed new revision.
* Destination: rpi-research, later work.
* Smallest useful next action: establish the smallest separately authorized evidence plan to isolate startup failure. Current static COLUMNS has17 entries including documents_json; historical deployment describes16. This is a credible compatibility question, not proof of the live schema or root cause. Isolate that question from empty-value/ref behavior without SQL, secret access or a new rollout unless explicitly authorized later.
* Status: Open; no diagnosis/fix attempted by Review.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: Image-only CLI execution violated literal secretRef preservation

* Related scope: P02-T02, AC4, exact-template execution contract.
* Evidence: Independent strict comparison of resident-app-before against resident-app-after, allowing only image/suffix and the frozen observational exclusions, reproduces exactly properties.template.containers[0].env[3].value and properties.template.containers[0].env[4].value. Both keys were absent before and empty strings after. Ref names are unchanged; no secret values were accessed or printed. Exact final recovery comparison passes after restoration.
* Impact: The selected forward executor cannot safely be reused as an exact-preservation recipe merely because its flags name only image and suffix. Drift may be relevant to startup, but causality is unproven. Current recovery removes the active defect; it does not repair the future forward method.
* Destination: rpi-implement, later bounded executor/test correction under the accepted exact-preservation direction, following any required planning/authorization.
* Smallest useful next action: reproduce serialization with synthetic refs and validate an exact writable-template request/round-trip contract that preserves absent/value/ref distinctions. Do not retry either cloud app as part of this finding and do not treat absent and empty as equivalent.
* Status: Active cloud drift recovered; executor defect remains open for later work.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: The PC-001 restoration sub-deadline contract is not fully executable

* Related scope: P01-T02, PC-001, frozen deadline/restoration requirements.
* Evidence: .copilot-tracking/details/2026-10-29/both-demo-sites-redeploy-phase-details.md promises a180s restoration absolute bound and120s equality-readback maximum. The supplied hash-matching redeploy.py push function defines only forward_deadline=start+420 and absolute_deadline=start+600. Its cleanup remaining() uses the latter; there is no restoration-start deadline or readback deadline. A restoration begun early could consume more than180s while still staying inside600s. Its verify-only initial inspect also lacks remaining-budget capping.
* Impact: Recorded fast restoration is valid, but the assertion that every frozen PC-001 enforcement correction was applied is too strong. A later slow/error path could exceed its advertised restoration budget.
* Destination: rpi-implement, later local executor correction.
* Smallest useful next action: add explicit restoration/readback deadlines capped by the total deadline, consistently cap every child by remaining budget, and test slow/error paths with synthetic/local mocks. Preserve private-first cleanup and owned-child/config boundaries. No registry reopening or live failure injection is authorized.
* Status: No observed restoration failure; open contract defect, not grounds to undo healthy apps.

<!-- rpi:review id=RV-004 -->
### RV-004 [Low]: The build executor uses a prohibited temporary-directory lock path

* Related scope: P01-T01, local execution boundary.
* Evidence: The supplied hash-matching redeploy.py build function opens /tmp/ama-rpi-heavy.lock for its nonblocking shared lock. Builds completed through that function. This is a local file operation outside the task's permitted non-temporary artifact locations, even though build output/export were kept under the owned evidence directory.
* Impact: Actual cloud scope and final safety are unaffected, but local execution did not fully respect the file-location restriction. Simply dropping the shared lock would also weaken the concurrency safeguard.
* Destination: rpi-implement, later executor hygiene correction.
* Smallest useful next action: agree a permitted shared non-temporary lock location with the coordinating executor and retain cross-task nonblocking exclusion. Do not delete, relocate or interfere with an existing shared lock during this Review.
* Status: Historical deviation retained; no corrective file operation performed.

## Defects

* RV-002: confirmed forward secretRef representation drift; final cloud state recovered, future executor correction remains.
* RV-003: frozen deadline enforcement does not fully match executable implementation; no actual restoration failure observed.
* RV-004: historical local lock-path violation; no cloud configuration effect.
* RV-001 is a delivery-blocking outcome/evidence gap, not an invented diagnosis of a source-code or SQL defect.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 High | rpi-research | Parent commissions bounded resident startup diagnosis under later explicit permissions | Material evidence gap blocks choosing a safe correction. |
| RV-002 High | rpi-implement | Later executor owner adds synthetic exact-ref request/round-trip coverage | Proven operational preservation defect; recovery did not make the forward CLI recipe safe. |
| RV-003 Medium | rpi-implement | Later executor owner enforces/test-mocks all restoration deadlines | Concrete mismatch with accepted PC-001 direction. |
| RV-004 Low | rpi-implement | Later executor coordinator chooses permitted shared lock location | Concrete local execution-boundary violation. |

Later implementation of routed findings does not require this Review to run again. Routes are recommendations for later work, not new implementation authority.

## Residual Work

* Separate resident retry planning/new forward authorization follows diagnosis; do not reuse this task's exhausted allowance. This is the existing distinct rpi-plan follow-up, not an unresolved present user-decision gap.
* Owner authenticated feature review remains distinct. Neither recorded public shells nor an exact-source image prove those journeys.
* Parent completes P03-T02 locally with original evidence, truthful Partial/Not accepted handoff, privacy-safe identity and mandated trailer. Coordinator alone handles publication and all required fresh gates/approvals. No push or PR was attempted.

## Blockers and Remaining Work

* Resident latest-main acceptance is blocked by actual failed activation and unisolated cause; further forward retry is outside authorization.
* No active service-recovery blocker remains in supplied final evidence or fresh authorized revision metadata. Both final apps are healthy/latest/ready and exact protected state is preserved.
* P02-T02 must remain unchecked for the requested result. P03-T02 remains pending parent action. This Review completes only P03-T01.
* No new source, plan, details, changes, state, other review record or cloud fix was written by Review.

## Validation Evidence

| Command/check | Scope | Status | Summary |
| --- | --- | --- | --- |
| Independent in-memory Python type-strict comparator | Saved complete app baseline/final and resident forward responses | Passed for finals; Failed for resident forward | Only exact six app exclusions used; expected image/suffix adjusted explicitly. No array sorting, absent/null conflation or ref normalization. Final differences empty; forward differences exactly two empty value additions. |
| Independent ACR projection comparison | Saved employee/resident post-window and final against original | Passed | Only systemData, provisioningState and status excluded. All policy/network/identity fields protected; zero differences. First failed employee proof window's exact restoration is supported by its receipt; later post-window snapshot represents admission continuation. |
| az containerapp auth show, both named apps only | Current auth versus private original auth in memory | Passed | Two exit0 reads; exact equality, no raw auth/config output. |
| az containerapp revision list --all, both named apps only | Fresh revision sets/readiness, no mutation | Passed | Employee11 revisions, resident6; exactly expected additions; no baseline names missing; only final revision active on each, both Healthy/Provisioned100%. |
| Saved revision accounting | Prospective resident and reconstructed employee baseline | Passed with limitation | Employee original active-only count1, reconstructed historical count10; final11. Resident prospective full baseline4; final6. Earlier recovery snapshot still had transitional activity, whereas final-result/fresh read prove final-only activity. Do not mistake the earlier snapshot for final state. |
| SHA256 and safe-record equality | All declared private backup hashes, external executor, supplied safe JSON records | Passed | All declared hashes match; every embedded safe record matches external counterpart; current executor hash matches supplied executor_sha256. Older per-step source hashes do not supply archived historical executor source. |
| git refs and archive comparison | Exact main/src export | Passed | Archive hash and all388 tracked file bytes match stated main. HEAD/origin/main match source SHA at Review; no extra fetch was needed or claimed by Review. Parent's final fetch is recorded separately in changes. |
| Build, push, manifest/config binding | Existing execution receipts | Passed, not rerun | Both builds/pushes succeeded; first employee identifier proof failed then read-only admission passed. Old manifest presence is bounded to recorded approved windows. |
| Runtime/HTTP | Existing per-app receipts | Employee Passed; resident forward Failed; recovery Passed | Positive ready-container/console or system evidence and route predicates are kept separate from HTTP200 alone. Review did not reissue HTTP probes or authenticated/model requests. |
| Local artifact access/cleanup | File modes and exact owned paths | Passed with narrow observation and RV-004 | Root0700; private JSON/config/revision backups and build logs0600; no owned credential directory or local-image export tar left. One sanitized non-secret resident-isolated-startup.json is0664 inside root0700, so no blanket all-JSON0600 assertion is made. Shared temporary lock deviation is RV-004. |
| Static resident source/historical comparison | Current COLUMNS and historical deployment record | Passed as hypothesis check only | Source requires17 columns including documents_json; historical evidence records16. No live SQL/server/schema check or actual-startup-console cause was available/performed. |
| Full tests/build/scanner/publication gate | No changed application code; parent publication boundary | Skipped | Existing local builds are evidence; Review did not rebuild, run SQL/browser/scanners or the complete publication gate. No full-gate pass, exact-head publication approval or hosted/human acceptance claimed. |
| Review record diff/format and sole-write check | This one new review file | Passed | Record inspected for complete sections, four unique RV findings, concrete routes and no placeholder text; git diff --no-index --check passed for this untracked file. Final status contains original parent inputs plus this review only. |

### Evidence Limitations

* Saved backups/receipts are execution evidence, not continuous monitoring. Fresh auth/revision reads support present metadata but do not replay runtime startup, rebuild images or prove authenticated journeys.
* Employee inactive-history baseline is explicitly retrospective. Partitioning surviving --all records by createdTime verifies retained additions and the old active revision, but cannot independently prove that no previously inactive historical revision disappeared before reconstruction. No deletion command exists in the inspected executor; no deletion was observed or authorized. Do not equate this evidence with a prospectively captured full baseline.
* Original failed system parsing is not error absence. Corrected final employee system tail has no target records; its positive console/ready-container evidence is the useful startup support.
* Failed resident console was unavailable after replicas stopped. Current fresh metadata describes that historical forward revision as inactive/Stopped, not a reason to erase its earlier ActivationFailed evidence or to declare its runtime repaired.
* Recovery root markers/hash are bounded public-shell observations, not exact-current-main content, full case-data non-disclosure proof or authenticated security testing.
* The supplied executor and receipts are not a complete shell/activity audit. No prohibited gh, SQL, secret retrieval, other-app mutation, role/network/subscription change or image/revision deletion appears in inspected executor/evidence; absence of such operations is not independently proved across all possible external actors.

## Outcome

* Outcome: Not accepted.
* Rationale: One of the two requested latest-main app results failed. A justified and verified failure-only rollback, exact restored app/auth/ACR configuration and successful employee deployment are important safety successes, not a substitute for resident acceptance.
* Severity summary: 2 High, 1 Medium, 1 Low. No Critical finding; no ongoing final protected-state mismatch found.
* Original failures preserved: initial employee digest assertion; employee route/schema/list-scope verification failures; resident ActivationFailed/termination and two empty-value additions; first rejected recovery request; initial bounded recovery ProbeFailed event; unavailable failed-console and bounded-log limitations. None is rewritten as a pass.
* Review execution Complete is independent from implementation Partial and outcome Not accepted.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | Later rpi-implement: RV-002, RV-003, RV-004 | Executor owner corrects exact refs, bounded cleanup and shared lock path with local synthetic tests; no live redeploy authority. |
| Decision gap or invalid assumption | No unresolved current owner choice; distinct later rpi-plan retry work | Parent/owner considers a new resident forward allowance and exact-template route only after diagnosis. |
| Material evidence gap | Later rpi-research: RV-001 | Establish actual startup cause within newly agreed read permissions. |
| Non-blocking residual work | Distinct authenticated acceptance and publication follow-ups | Owner/coordinator; parent completes only its local evidence handoff now. |

* Execution status: Complete for Review; Partial for implementation.
* Outcome: Not accepted for both-sites latest-main delivery.
* Validation coverage: independent exact saved-state/source/integrity comparisons, fresh two-app auth/revision reads, recorded anonymous/runtime/build/registry evidence; no SQL, authenticated/model validation or publication gates.
* Blockers: resident startup cause unknown and no remaining forward-retry authorization; publication remains gated separately.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-29/both-demo-sites-redeploy-research.md](.copilot-tracking/research/2026-10-29/both-demo-sites-redeploy-research.md) | Supplied operational research. |
| [.copilot-tracking/plans/2026-10-29/both-demo-sites-redeploy-plan.md](.copilot-tracking/plans/2026-10-29/both-demo-sites-redeploy-plan.md) | Current acceptance criteria and correctly partial implementation plan. |
| [.copilot-tracking/details/2026-10-29/both-demo-sites-redeploy-phase-details.md](.copilot-tracking/details/2026-10-29/both-demo-sites-redeploy-phase-details.md) | Frozen contracts and implementation-time corrections. |
| [.copilot-tracking/reviews/plans/2026-10-29/both-demo-sites-redeploy-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/both-demo-sites-redeploy-plan-critique.md) | Original Complete/Revise critique. |
| [.copilot-tracking/changes/2026-10-29/both-demo-sites-redeploy-changes.md](.copilot-tracking/changes/2026-10-29/both-demo-sites-redeploy-changes.md) | Execution, failures, recovery and handoff. |
| [.copilot-tracking/changes/2026-10-29/both-demo-sites-redeploy-evidence.json](.copilot-tracking/changes/2026-10-29/both-demo-sites-redeploy-evidence.json) | Sanitized machine evidence and external backup pointers/hashes. |
| [.copilot-tracking/reviews/logs/2026-10-29/both-demo-sites-redeploy-review.md](.copilot-tracking/reviews/logs/2026-10-29/both-demo-sites-redeploy-review.md) | This original, single Review and complete finding set. |

## Next Steps

Active parent preserves this original Review verbatim, records Complete Review / Partial implementation / Not accepted outcome, and completes the authorized local evidence-only handoff. Route RV-001 to later rpi-research and RV-002/RV-003/RV-004 to later rpi-implement; keep a newly authorized resident rpi-plan/retry, authenticated owner acceptance and coordinator publication as distinct follow-ups. Do not execute fixes, more forward attempts or another Review under this request.
