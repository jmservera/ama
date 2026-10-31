---
title: Review - demo-sites-redeploy-cache
description: Independent post-implementation operational evidence review
ms.date: 2026-10-31
---

## Scope and Evidence

* Task ID: demo-sites-redeploy-cache / 2c99fa13-81cb-4fd2-af53-81ad16cb565a
* Review date: 2026-10-31
* Review scope: One independent Review of the full supplied operational task.
* Assessed boundary: Local source/build proof, bounded ACR windows, immutable redeployment, restoration, protected baselines, cache and browser evidence, AC1-7 and administrative residual work.
* Plan: .copilot-tracking/plans/2026-10-31/demo-sites-redeploy-cache-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/demo-sites-redeploy-cache-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-31/demo-sites-redeploy-cache-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-31/demo-sites-redeploy-cache-changes.md
* Other evidence considered: Supplied research, evidence export, session state, old #596 changes and retained private executor artifacts.

## Opening Review State

* Interpreted review goal: Independently reconcile delivered operational evidence and route residual acceptance work without repeating operations.
* Review scope: Full supplied artifact set on chore/ops-redeploy-cache at d20bc50c4b664521f72446e5d0c85cc576ef0850.
* Evidence readiness: All seven current task artifacts exist; raw private evidence remains to be inspected in memory.
* Acceptance basis: Current plan AC1-7, phase markers, critique dispositions and confirmed owner constraints.
* First comparison boundary: Plan, phase details, research and changes claims against actual journal, executor, source and retained output hashes.
* Active read-only boundaries: Only this canonical Review record may be written. No cloud, Docker, browser, repeat operational validation, source, plan, state or changes writes. Private data must not be printed.
* Initial blockers: None identified before evidence comparison. AC7 administrative persistence is explicitly pending in the supplied handoff.

## Execution Status

* Execution status: Complete for this one independent Review.
* Review execution evidence: All supplied artifacts compared on 2026-10-31; retained source, executor, journal, actual browser events, raw HTTP outputs and protected baselines reconciled in memory.
* Planned task execution: Partial. P01, P02 and P03-T01 are complete; P03-T02 export is complete, this original Review is now recorded, and local evidence commit remains pending. P03 and AC7 must not be represented as fully complete before that administrative continuation.
* No operational executor, cloud, Docker or browser operation was run by this Review. Read-only Git object inspection and in-memory evidence comparison are not fresh live validation.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 / AC1 | Fresh backups, archived main build and pre-publication packaged proof | Reconciled | Both image identities and 35 packaged web files per image bind to the same tracked archive before the first registry mutation. |
| P01-T02 / AC1-AC2 | Failed first token window, exact restoration, second successful window | Reconciled | First failure is retained, not success-shaped. Two actual token attempts across two windows; second window succeeds immediately. Old manifests checked before and after each push. |
| P02-T01 / AC3-AC4 | No SQL, one pair rollout and full protected readbacks | Reconciled | Cache-only source delta supports no init. Exactly one successful forward PATCH and one added revision per app. |
| P03-T01 / AC5-AC6 | Actual curl and fresh anonymous browser receipts | Reconciled within scoped acceptance | Seven public versioned assets are source-equal and immutable for exactly one year; both HTML shells are no-store. Protected employee widget200 remains literally unmet, not waived by packaged proof. |
| P03-T02 / AC7 | Export complete; Review and local commit pending at handoff | Partial, accurately marked | This record supplies the original Review only. Local commit and its identity/message/path readback remain the parent's work; RV-002. |
| Follow-Up Items | Signed-in acceptance and separately controlled AI activation | Reconciled outside active scope | RV-001 routes identity/widget acceptance distinctly. AI remains OFF; no activation decision is inferred. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | .copilot-tracking/changes/2026-10-31/demo-sites-redeploy-cache-evidence.json; retained private build.py, verify.py and build-context/src | Build exact main and replace the invalid pre-push input with current local build proof | Source archive SHA256 28c7fa1eacee5753a7d815c936a4a1b15b18c55ae102104edcf6fa132dbabd90; src tree 0fd94c69365573bef73426237221180d4a398b3c; 426 archived source files equal both extracted context and current source | Retained build, inspect and packaged-byte outputs reconciled; both sets of 35 hashes equal archived source | Complete; no source repair or application-test claim |
| P01-T02 | Same export; retained publish.py and both restoration proofs | Publish guarded immutable images, then restore exact private baseline | Resident index d3a3a8727b8a65305d2cf3994872477e8542b0383a47bf084fdc36ef368d849a; employee index 0bd3a9030d56ff23403ebc40cb083b3c17d42357148393578ff37ba5c0ee2ec1; both platform/config chains and RepoDigests bound | Actual open readbacks normalize to exactly one IPv4 /32, defaultDeny and admin OFF; complete stable private readbacks equal baseline for both attempts | Complete; registry body hashes are publisher-bound, not independently rehashed raw registry bodies |
| P02-T01 | Same export; retained rollout.py, pair intent, app intents and raw readbacks | Roll resident then employee by new digest without touching SQL | Resident res-live-20261031-023722 and employee emp-live-20261031-023859; one successful PATCH and one added revision each | Healthy, Provisioned, active, ready replica, traffic100, latest=ready, min0; full protected config/auth and all old revision templates preserved | Complete; no recovery or ambiguous-write branch exercised |
| P03-T01 | Same export; retained raw curl bodies/headers and browser-raw.json | Prove source-equal public cache behavior and resident docking without sign-in | Both first warm health200 and shell200; five resident and two employee assets200; desktop1365x900/mobile390x844 | Raw retained status/body/header comparisons; actual event-bound browser code/results, open/dock/undock/Escape poststates | Complete within anonymous boundary; RV-001 and RV-003 remain separate |
| P03-T02 | .copilot-tracking/changes/2026-10-31/demo-sites-redeploy-cache-evidence.json; this Review record | Preserve actual sanitized operational provenance and one original Review | 194 journal records, 20 completed outer command bindings and one actual browser receipt | 358 retained stdout/stderr hashes, 86 retained JSON proof hashes, nine current adapters and eight original executor hashes; private root0700/files0600 | Export and Review complete; local commit not performed or proven |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | Consume build-proof local IDs/config/source/archive instead of requiring nonexistent push-proof | PC-001; approved intent already required local proof before registry writes | Plan disposition, details, adapter and actual pre-mutation output ordering agree | Original Complete / Revise critique retained; compatible direct correction | Applied and proven; no fabricated pre-publication remote digest |
| P01-T02 | Add bounded same-window token acquisition backoffs after first-window token failure and exact restoration | Actual failed token/restoration and private diagnosis; standing owner window/fallback authority unchanged | Changes preserve failure and unestablished cause; current details explicitly disclose retries/fallback unexercised | Immediately relevant adapter update, not source repair or authority widening; no new critique claimed | Justified bounded divergence; actual second window first token succeeded, so neither retries nor fallback is accepted as exercised |
| P02-T01 | Replace historical mandatory SQL success assertions with an actual no-execution disposition and fresh eight-job guard | Owner source-delta condition; full cache delta contains no SQL/DDL/schema/migration change | Research, plan, details, sql-skip and actual command list agree | Within accepted direction | Justified; no historical SQL success or database access substituted |
| P03-T01 / AC6 | Keep employee public-shell proof separate from protected widget/identity acceptance | Source trusted-proxy boundary and actual curl401/browser302; no sign-in authorized | Scoped AC6, handoff and not_proven fields preserve literal live-widget200 gap | Explicit scope reconciliation, not access-control relaxation | Honest scoped pass only; broader acceptance routed by RV-001 |

## Critique and Material Revision Assessment

* Latest critique dispositions: PC-001 applied and independently reconciled to the current adapter, local image identities, archive binding, actual packaged output and pre-registry-write ordering. PC-002 is recorded as rejected; the original Complete / Revise verdict remains unchanged.
* PC-002 authority boundary: The supplied parent direction expressly confirms its shared heavy-operation lock requirement and the parent's rejection of the alleged restriction. This Review does not infer a different parent instruction set from the review worker's restrictions, require a unique lock substitute, or access the lock itself. The historical command evidence retains the shared lock contract; this is not permission for this reviewer to perform temporary-path operations.
* Material revisions: Token acquisition changed only after the failed window's exact restoration and unchanged-app readbacks. The permitted /32/private-restoration/old-digest controls, fallback condition and approved deployment scope remained unchanged. Plan/details/changes reconcile the executed path and disclose unexecuted alternatives.
* Dependent-work pause assessment: Actual packaged proof completed before the first ACR network mutation. The failed window's exact private restoration preceded either image push; the successful window's exact restoration preceded either app PATCH. No early dependent rollout or blind repeated PATCH was found.
* Justification assessment: Current descriptive updates preserve confirmed owner intent. No unresolved decision gap requires rpi-plan, and no second critique or Review is required or authorized.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Owner-run signed-in employee/resident identity/widget acceptance | Anonymous-only operations cannot prove protected live-widget200, identity roles or signed-in behavior | Owner schedules a separately authorized identity/widget acceptance task | Open; RV-001 / FU-SIGNEDIN-ACCEPTANCE, not an application defect or an added active task |
| Resident AI activation | AI must remain OFF and model requests were excluded | Owner decides separately whether activation is authorized | Open distinct follow-up; keep OFF, no activation or model acceptance claim |

Unresolved plan follow-up items remain distinct follow-up work. They are not defects or new active Pxx/Pxx-Txx implementation, completion or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Literal protected employee widget200 and signed-in acceptance remain unproven

* Related scope: AC6, P03-T01, plan Follow-Up Items.
* Evidence: .copilot-tracking/changes/2026-10-31/demo-sites-redeploy-cache-evidence.json final.sites employee_widget_200 is unmet_auth401; actual protected widget JS/CSS curl outputs are401, and actual employee browser /app results are302 to the Entra origin. Packaged employee web bytes are source-equal, but this proves shipping, not authenticated live delivery. Plan Handoff and export not_proven disclose the gap.
* Impact: AC1-6 can pass only under the current explicit anonymous/public acceptance boundary. The original literal employee-widget200 requirement, its protected live cache headers and signed-in employee/resident/identity acceptance cannot be called satisfied.
* Destination: Distinct follow-up FU-SIGNEDIN-ACCEPTANCE, owner-run under separate authorization; not rpi-implement and not an auth-bypass request.
* Smallest useful next action: Retain this gap and schedule authorized signed-in acceptance with a provisioned permitted identity; keep authentication and consent boundaries unchanged.
* Exact resolving evidence: In that later task, actual protected employee widget JS/CSS GET200 at current versioned URLs, cache headers and delivered-byte/source bindings, plus explicitly scoped employee/resident identity/role behavior and sign-out evidence. Record excluded journeys rather than claiming complete signed-in acceptance. No credentials, tokens or authentication-query contents belong in public evidence.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: AC7 local administrative persistence is still pending

* Related scope: P03-T02, P03, AC7.
* Evidence: Current plan/detail markers leave P03-T02 and P03 unchecked; changes/export explicitly retain independent_review_and_local_commit_pending. HEAD remains d20bc50c4b664521f72446e5d0c85cc576ef0850 and the supplied dated artifacts are untracked. This record supplies the single original Review, not a local commit.
* Impact: Operational acceptance is not a completed full-loop delivery or durable local evidence commit. No publication gate, exact-head approval, push, PR or merge is established.
* Destination: Active-parent administrative continuation of P03-T02 / LOCAL-EVIDENCE-PERSISTENCE; no source defect or new Review.
* Smallest useful next action: Parent preserves this original verdict/findings and completes only the authorized privacy-safe local evidence commit and its readback, updating its administrative markers without another Review or closure assessment.
* Exact resolving evidence: Fresh gh api user-derived local noreply author/committer identity, local Conventional Commit containing only the intended dated evidence and this original Review, Refs #568/#520/#570 without closing keywords, exact Copilot trailer, and actual commit identity/message/path/worktree readback. No push. Any future publication requires the separate fresh complete local gate and hosted/human approvals; none are proven here.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Anonymous browser console errors remain diagnostic residual work

* Related scope: P03-T01 browser evidence, not a clean-console or accessibility acceptance criterion.
* Evidence: Actual event-bound browser results disclose resident desktop1/mobile0 and employee1 per viewport; all four pageErrorCount values are0. The capture intentionally stores generic console-error labels/counts, not source/cause details.
* Impact: Required health/cache/docking assertions passed, but a clean-console claim or diagnosis of the errors is unsupported. No source defect can be inferred from these counts alone.
* Destination: Distinct follow-up FU-ANONYMOUS-CONSOLE-DIAGNOSIS, owner or frontend maintainer.
* Smallest useful next action: Retain disclosed counts; optionally authorize a separate anonymous diagnostic capture that classifies expected authentication/resource errors versus application defects without sign-in or submission.
* Exact resolving evidence: Later sanitized originating request/status or script-location evidence for each error category, an explicit expected-error disposition or a demonstrated actionable defect, and that task's scoped result. Only a proven implementation defect should subsequently route to rpi-implement.

## Defects

* None found in the delivered operational boundary. RV-001 is excluded acceptance work, RV-002 is pending administration, and RV-003 is an unclassified diagnostic residual, not evidence of a source defect.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | FU-SIGNEDIN-ACCEPTANCE | Owner authorizes and runs separate protected identity/widget acceptance | Beyond anonymous authority; preserve literal acceptance gap |
| RV-002 | P03-T02 / LOCAL-EVIDENCE-PERSISTENCE | Active parent completes local-only evidence persistence and readback | Pending administrative step, not repair or publication |
| RV-003 | FU-ANONYMOUS-CONSOLE-DIAGNOSIS | Owner/frontend maintainer optionally classifies disclosed errors | Unknown cause; no clean-console claim or demonstrated defect |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Protected employee widget200/cache and signed-in identity acceptance: RV-001, separately authorized owner follow-up.
* Local evidence commit: RV-002, parent administrative continuation.
* Anonymous console-error classification: RV-003, distinct optional diagnostic follow-up.
* Resident AI activation: Existing distinct owner-decision follow-up; remain OFF.
* No ACR-build fallback, propagation retry, recovery or ambiguous-write success is claimed. The actual successful path does not require exercising those branches now.

## Blockers and Remaining Work

* Review blockers: None; credible retained evidence supports this verdict.
* Remaining active work: P03-T02 local evidence commit and its actual readback. AC7 and P03 remain incomplete until the parent performs that continuation.
* Signed-in scope cannot be accepted from anonymous evidence and must not be resolved by auth relaxation, sign-in during this task or fabricated receipts.
* Full publication/hosted/human gates were not run and are not prerequisites being claimed as satisfied by this local-only operational Review.

## Validation Evidence

| Command or evidence comparison | Scope | Status | Summary |
| --- | --- | --- | --- |
| Retained preflight.py / ops.py / locked build.py / verify.py --images | Fresh backups, source archive, local images and packaged bytes | Passed, historical actual execution reconciled | Actual exit0 before first registry mutation; same current archive, local IDs, source labels and 35 packaged hashes per image |
| Retained first publish.py and diagnose_publish.py | First token failure and private restoration | Failed token; passed restoration/diagnosis | Publish exit1 before either push; exact private restoration and unchanged apps verified. Failed root cause is unestablished; acknowledgement-to-disabled 5.346358s is not exact service-side exposure |
| Retained second preflight.py / locked publish.py | Actual successful publication | Passed, historical actual execution reconciled | First token in second window succeeds; both new/old chains bound; exact private baseline restored. Acknowledgement-to-disabled 14.974995s; no retry/fallback success claimed |
| Retained rollout.py | Digest pair rollout without SQL | Passed, historical actual execution reconciled | Exactly two successful forward PATCH commands, one per app; Healthy/Provisioned/ready100/min0 and protected histories/auth/config preserved |
| Retained verify.py raw curl outputs | Actual health, shells, seven public assets and protected denials | Passed, historical actual execution reconciled | Both first warm200, shell bytes reconstructed from archived source, versioned asset bytes/source hashes equal, exact public max-age=31536000 plus immutable, HTML no-store; protected401 preserved |
| Actual Playwright code/result/event binding | Four fresh contexts, desktop/mobile public behavior and resident dock poststates | Passed scoped assertions; console errors disclosed | One actual receipt 02:41:09.407Z-02:41:14.395Z; health/public200, GET-only, dock heights900/844 and widths477.75/320, inverse undock state and Escape asserted; protected employee302; pageerrors0, console counts1/1/0/1 in receipt order |
| Reviewer in-memory raw JSON/hash/event/source comparisons and read-only Git object inspection | Evidence integrity and exact protected baselines | Passed | 194 journal entries; 358 stdout/stderr hashes; 86 JSON proof hashes; nine current and eight original executors syntax/hash-bound; 20 completed outer bindings and one actual browser binding; 426 archived src files equal extracted/current bytes; raw job/history/auth/app outputs bind to saved baselines; all four minima0/eight complete Manual jobs/AI OFF |
| Reviewer representation reconciliation | OCI identity and firewall normalization | Passed after correcting reviewer assumptions | Local Docker IDs are OCI index identities, not necessarily config digests; each index/config chain is consistent. Azure's bare IPv4 rule normalizes to /32. Initial strict representation assertions were not failed deployment evidence |
| Source delta 4cb5964f..d20bc50c, src and infra | SQL disposition | Passed read-only inspection; SQL skipped | Ten changed source/docs/check/test paths implement cache policy only; no SQL/schema/DDL/migration delta. Actual journal has no SQL execution or job start |
| Registry raw-body independent rehash | Old/new manifest and remote config raw bodies | Unavailable | Bodies were not retained; guarded publisher code checks their digests and source/config/platform relationships, with actual journal hashes and successful output. Review does not invent independent raw-body verification |
| New cloud, Docker, browser or repeated operational tests | Review stage | Skipped by explicit authority boundary | Only retained evidence compared; no operations repeated |
| Signed-in/widget200/model/accessibility/screen-reader acceptance | Excluded acceptance scope | Unavailable or not run | RV-001; AI OFF; no clean-console, WCAG or signed-in conformance claim |
| Local evidence commit; full publication/hosted/human gates | Administrative persistence and later publication | Not run | RV-002; local commit pending. No push/PR/merge or publication acceptance |

## Outcome

* Outcome: Residual work.
* Outcome rationale: Delivered P01/P02/P03-T01 operational evidence is conformant within the explicit anonymous/public boundary, with justified compatible adaptations and exact protected restoration. Full task persistence is incomplete and literal protected employee-widget200/signed-in acceptance remains outside proof. Disclosed console errors require no unsupported defect or clean-console claim. No material source defect, unauthorized decision expansion or evidence gap preventing this bounded verdict was found.
* Original verdict: This is the task's one original post-implementation Review. Preserve this outcome and finding set; later administration or follow-up must not overwrite it, repeat Review or create a closure assessment.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None demonstrated | No rpi-implement repair requested by this Review |
| Decision gap or invalid assumption | None unresolved | No rpi-plan handoff |
| Material evidence gap within reviewed operational scope | None blocking | No rpi-research handoff; raw registry limitation retained |
| Non-blocking residual work | FU-SIGNEDIN-ACCEPTANCE; LOCAL-EVIDENCE-PERSISTENCE; FU-ANONYMOUS-CONSOLE-DIAGNOSIS; existing AI decision follow-up | Owner/parent continuation as specified by RV-001/002/003; preserve AI OFF |

* Execution status: Complete Review; planned full task remains Partial pending local commit.
* Outcome: Residual work.
* Validation coverage: Retained source/archive/image/executor/output/event bindings, two ACR windows, exact protected app/auth/job/history/ACR baselines, actual curl cache proof and actual anonymous desktop/mobile browser poststates.
* Blockers: None to this Review. No fresh live, signed-in, model, publication or conformance validation claimed.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-31/demo-sites-redeploy-cache-research.md](.copilot-tracking/research/2026-10-31/demo-sites-redeploy-cache-research.md) | Research and scope decisions |
| [.copilot-tracking/plans/2026-10-31/demo-sites-redeploy-cache-plan.md](.copilot-tracking/plans/2026-10-31/demo-sites-redeploy-cache-plan.md) | Current AC1-7 and markers |
| [.copilot-tracking/details/2026-10-31/demo-sites-redeploy-cache-phase-details.md](.copilot-tracking/details/2026-10-31/demo-sites-redeploy-cache-phase-details.md) | Current phase contracts |
| [.copilot-tracking/reviews/plans/2026-10-31/demo-sites-redeploy-cache-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/demo-sites-redeploy-cache-plan-critique.md) | Original Complete / Revise critique |
| [.copilot-tracking/changes/2026-10-31/demo-sites-redeploy-cache-changes.md](.copilot-tracking/changes/2026-10-31/demo-sites-redeploy-cache-changes.md) | Actual implementation record |
| [.copilot-tracking/changes/2026-10-31/demo-sites-redeploy-cache-evidence.json](.copilot-tracking/changes/2026-10-31/demo-sites-redeploy-cache-evidence.json) | Sanitized actual evidence export |
| [.copilot-tracking/rpi-sessions/2026-10-31/demo-sites-redeploy-cache-state.json](.copilot-tracking/rpi-sessions/2026-10-31/demo-sites-redeploy-cache-state.json) | Parent state at Review intake |
| [.copilot-tracking/changes/2026-10-31/demo-sites-redeploy-1031-changes.md](.copilot-tracking/changes/2026-10-31/demo-sites-redeploy-1031-changes.md) | Old #596 failure/correction boundary |
| [.copilot-tracking/reviews/logs/2026-10-31/demo-sites-redeploy-cache-review.md](.copilot-tracking/reviews/logs/2026-10-31/demo-sites-redeploy-cache-review.md) | This single original Review |

## Next Steps

The active parent preserves this original Review and completes only the authorized P03-T02 local evidence commit/readback. Route RV-001 and RV-003 to their distinct owner follow-ups, keep AI OFF, and retain all unproven acceptance/gate limits. No new operational validation, Review, closure assessment, push or user clarification is required here.
