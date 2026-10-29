---
title: Both demo sites redeployment plan critique
description: Independent final-candidate operational plan assessment
ms.date: 2026-10-29
---

## Metadata

* Task ID: 3897222c-2d62-4e25-a059-eecfbdce51d0
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/both-demo-sites-redeploy-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/both-demo-sites-redeploy-phase-details.md
* Critique execution status: Complete
* Assessment: Exactly one independent final-candidate critique. Original verdict and complete finding set follow; no second critique is requested.

## Inputs and Criterion Boundary

* Caller requirements: Refresh only ca-cutover-test-demo-api and ca-resident-demo in ama / cae-cutover-test-demo from fetched main d70ee60ab3d7346a9991cf64382d9985f4d09f2e. Create one forward image-only revision per app, preserve full current configuration and min0, retain old manifests, and use only the approved local Docker / VM-IP / expose-token ACR route with exact restoration.
* Evidence: The supplied plan, phase details and .copilot-tracking/research/2026-10-29/both-demo-sites-redeploy-research.md, including C1-C8. Relevant historical records read: .copilot-tracking/changes/2026-10-28/employee-redeploy-changes.md; .copilot-tracking/details/2026-10-28/employee-redeploy-phase-details.md:80-190; .copilot-tracking/changes/2026-10-27/deploy-resident-474-changes.md:35-150; .copilot-tracking/changes/2026-10-27/resident-live-acceptance-changes.md:1-170.
* Repository context: Read the original case study, addendum, reference index and owner memory. They do not expand operational authorization.
* Decisions and dependencies: No cost query, gh, push, secret-value/.env/private-data access, image deletion, SQL/role/other-app changes, authenticated probes or model calls. Baselines and both builds precede pushes; manifest proof and ACR restoration precede app writes. Actual unhealthy revision/startup errors alone authorize failure recovery. One independent Review and local evidence handoff remain separate from publication and authenticated acceptance.
* Assessment boundary: Credibility of the supplied operational plan across AC1-AC6 and P01-P03, not actual cloud health, a new source-code review, legal approval or publication admission. No cloud commands, credential reads, source edits or open-ended research were performed. Existing untracked parent artifacts were left untouched on ops/sites-redeploy-20261029.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Caller scope; C1-C4/C7; P01-T01 | Covered | Correct Dockerfiles/src context, pinned source/tree, private backups, nonblocking build lock, no infrastructure helper. |
| Approved route; AC2; P01-T02 | Partial | Historical route is appropriate, including bare-IP normalization and private-first restoration; PC-001 addresses deadline enforcement. |
| AC1-AC2; P01-T02 | Partial | Immutable source and new tags are planned; PC-003 separates manifest and config digest relationships. |
| AC3-AC4; P01-T01; P02-T01-T03 | Partial | Complete preservation is required, but the canonical comparison boundary is not defined; PC-002. |
| AC3/AC5; P02 recovery | Partial | Correct failure-only rollback trigger, but recovery completion evidence is unspecified; PC-004. |
| AC5; C2/C5; P02-T01-T03 | Partial | Correct log selectors and positive target-startup requirement; PC-005 addresses anonymous HTTP assertions. |
| AC6; P03-T01-T02 | Covered | One critique/Review, retained original outcomes, evidence-only local commit, explicit no-gh identity deviation and no publication claim. |
| Concurrency and ambiguity controls | Covered | Fresh pre-write baseline comparison; no blind update retry or overwriting another actor's drift. |

## Verdict

* Verdict: Revise
* Severity summary: 3 High, 2 Medium, 0 Critical, 0 Low.
* Rationale: The selected route and authorization are credible. Before mutation, make the bounded-restoration mechanism, exact comparison contract, digest binding, recovery postconditions and anonymous assertions executable and unambiguous. These are direct-compatible corrections, not reasons to revisit the user's chosen route or request costs/secrets.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: ACR deadline lacks an enforcement and cleanup budget contract

* Related IDs: P01-T02, AC2, non-functional time bounds.
* Evidence: .copilot-tracking/plans/2026-10-29/both-demo-sites-redeploy-plan.md:73-76 bounds policy calls, pushes, exception duration and readback. .copilot-tracking/details/2026-10-29/both-demo-sites-redeploy-phase-details.md:38-53 adds token/login/manifest operations and a finally block without specifying how these operations share that deadline. Historical .copilot-tracking/details/2026-10-28/employee-redeploy-phase-details.md:137-144 explicitly bounded token/login/digest operations and interruption handling.
* Concern: The 600-second ceiling is stated, but a stalled token/login/HEAD operation or a push begun without sufficient remaining budget can overrun it. A finally block alone does not interrupt an in-flight child process. The additional 120 seconds is described as readback, not a complete bounded restoration/retry allowance.
* Impact: Public/export exceptions or local credential material could outlive the intended window, with recovery status uncertain.
* Smallest useful change: Define one monotonic per-window deadline starting at the first policy mutation, remaining-budget limits for every child/network call, an early restoration reserve, and a separately bounded restoration/readback path. State handled timeout/interruption behavior, exact-owned child/config cleanup, no whole-process-group or image cleanup, and the stop/escalation state if restoration cannot be confirmed.
* Action owner: Planning parent; implementation executor enforces the contract.
* Exact resolving evidence: Revised P01-T02 deadline/cleanup recipe with explicit operation and restoration bounds; execution receipt records opening/closure times, timeout/exit classification, exact policy equality, and exact-owned credential cleanup before any app write.
* Decision route: Direct-compatible planner correction. No significant/divergent user decision required; do not extend the approved route.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Exact-equality projection is not yet a reproducible contract

* Related IDs: P01-T01, P01-T02, P02-T01-T03, AC2-AC4.
* Evidence: .copilot-tracking/details/2026-10-29/both-demo-sites-redeploy-phase-details.md:37,47-49,94-97 uses "stable" fields and observational exclusions without enumerating paths. The plan requires equality except image/suffix, although app revision pointers and operational state necessarily change.
* Concern: Different ad hoc projections can either fail on expected revision/status changes or silently omit protected fields. Hashes and env counts do not establish which complete fields were compared.
* Impact: The executor cannot produce independently reproducible proof of exact env/secretref, auth, identity, registry, ingress, scale and other configuration preservation.
* Smallest useful change: Specify the canonical projection and explicit JSON-path exclusions before mutation. Keep complete configuration, identity, auth metadata and template protected, allowing only the named container image and revisionSuffix to differ in the template. List derived runtime/revision-pointer fields separately and assert their expected transitions instead of ignoring them broadly. Use the same frozen comparison contract for pre-write drift, final readback and recovery; define ACR exclusions equally narrowly.
* Action owner: Planning parent.
* Exact resolving evidence: Revised details identify the projection/exclusion paths and canonicalization rules; sanitized receipts identify comparator version/hash and report zero unexpected changed paths, intended image/suffix changes, required revision-pointer transitions and separate auth/ACR equality. Never publish protected values.
* Decision route: Direct-compatible planner correction. No significant/divergent user decision required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Manifest digest and local image config digest must be compared separately

* Related IDs: P01-T01-T02, AC1-AC2.
* Evidence: .copilot-tracking/details/2026-10-29/both-demo-sites-redeploy-phase-details.md:41-43 says to verify the new push digest against "local RepoDigest/config digest". .copilot-tracking/changes/2026-10-28/employee-redeploy-changes.md explicitly corrects the earlier confusion between Docker image ID/config digest and registry manifest digest.
* Concern: RepoDigest and config digest are different identifiers. The slash wording leaves their relationship undefined, repeating a documented historical evidence gap.
* Impact: A valid push can be rejected by an invalid equality assertion, or the wrong locally built image can be asserted as the deployed artifact without a proven binding.
* Smallest useful change: Require push digest = remote manifest Docker-Content-Digest = local pushed RepoDigest. Fetch that exact manifest and separately require its config.digest = the built local Docker image ID. If an index is returned, resolve and record the intended platform manifest before comparing config.digest. Preserve source-label binding without exposing build logs.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P01-T02 specifies both distinct comparisons; each image receipt records source SHA/tree, local config ID, remote manifest/index and selected-platform digests as applicable, and both equality results.
* Decision route: Direct-compatible planner correction. No significant/divergent user decision required; no new build/push route is needed.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Recovery action lacks bounded verified terminal postconditions

* Related IDs: P02-T01-T03, AC3-AC5, Dependencies and Recovery.
* Evidence: .copilot-tracking/plans/2026-10-29/both-demo-sites-redeploy-plan.md:139-146 and .copilot-tracking/details/2026-10-29/both-demo-sites-redeploy-phase-details.md:97-99 authorize restoration of the old image, but do not require recovery convergence, startup/HTTP proof, revision accounting or ambiguity handling for that recovery update.
* Concern: Issuing an old-image update is not proof of restored service. Forward-only AC3 cannot represent the allowed extra recovery revision. Full target-startup and preservation checks are also placed in final P02-T03 rather than expressly gating completion of each app's update.
* Impact: Recovery could be reported as completed while the app remains unhealthy, or another app could be mutated before the preceding app's full outcome is classified.
* Smallest useful change: Apply the existing preservation, positive target-startup, health and revision-set checks immediately per app. Define a single bounded image-only recovery attempt for a demonstrated runtime failure, inspect ambiguous recovery results without retry, and verify old digest, ready/active service, expected traffic, health/startup and exact protected-field equality. Define recovered-but-redeploy-failed and recovery-unverified terminal states. Do not recover for tooling-only failures, retry forward deployment, change SQL/configuration, or revert a successful other app.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P02 has per-app acceptance and recovery gates plus an explicit convergence bound; any recovery receipt records trigger evidence, command outcome, forward/recovery revision sets, restored old digest, equality and positive runtime/HTTP observations, or an explicit unresolved blocker.
* Decision route: Direct-compatible planner correction using already-authorized failure recovery. No significant/divergent user decision required.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Anonymous status collection does not prove all AC5 assertions

* Related IDs: P02-T01-T03, AC5.
* Evidence: .copilot-tracking/plans/2026-10-29/both-demo-sites-redeploy-plan.md:88-90 requires employee protection and a resident public page without anonymous case data. .copilot-tracking/details/2026-10-29/both-demo-sites-redeploy-phase-details.md:68-69,79-80 specifies status collection but no resident page-content assertion or explicit per-route expected-status gate.
* Concern: HTTP 200 alone could be a generic/error/login response, and status alone cannot establish that case data is absent. A redirect followed automatically could also obscure the original employee protection response.
* Impact: AC5 could be marked passed without evidence for the stated anonymous boundary.
* Smallest useful change: Define bounded anonymous curl requests with explicit timeouts, no cookies/credentials and no automatic redirect following; enumerate expected statuses per route. For resident root, inspect only the public response in memory for known sign-in/public-page markers and absence of case payload/rendered case content using an explicit bounded predicate. Persist only statuses, assertion booleans and non-sensitive hashes/counts, never response bodies or case values. Narrow the resulting claim to those checks, not exhaustive data-leak prevention.
* Action owner: Planning parent.
* Exact resolving evidence: Revised AC5 recipe names routes, status assertions and resident content predicates; sanitized probe receipt reports each assertion and target host with the successful revision/traffic evidence, and explicitly excludes authenticated acceptance.
* Decision route: Direct-compatible planner correction within anonymous curl authorization. No significant/divergent user decision required.

## Strengths and Residual Risk

* Prior execution supports local Docker plus VM-only expose-token push; remote ACR task widening is correctly rejected.
* Private-first restoration, exact returned bare-IP removal, unique tags, no deletion, no blind forward retry, fresh drift checks and min0 preservation directly address historical failures.
* Correct system/console CLI selector distinctions avoid the earlier tooling-induced rollback. Positive revision-specific startup/readiness is correctly required rather than inferring success from absent errors or ARM Healthy.
* Existing employee e6b6e744... and resident fab6a853... baselines, current resident ingress/expiry and exact main/src tree are stated, rather than restoring obsolete resident settings.
* Cost headroom is unknown by explicit no-query direction, not a missing permission to query. Authenticated features, human acceptance and publication remain unproved and separately gated.

## Questions or Blocking Evidence Gaps

* No unresolved user choice is needed for these five corrections.
* Fresh baselines, token availability, real build/push results, policy restoration and actual new-revision health remain implementation evidence, not facts established by this critique.

## Limitations

* Historical private backups and raw receipts were not opened; research's live summaries and installed-help claims were assessed as supplied evidence, not re-executed.
* No fresh Azure, Docker, HTTP, test-suite or publication-gate execution occurred. Documentation-only critique validation is scope/diff review.
* This original verdict must remain unchanged after parent disposition. Compatible corrections are finalized by the planning parent without another critique.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Define enforceable ACR deadline/restoration handling, then dispose PC-002 through PC-005 in the plan/details and finalize before implementation.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/both-demo-sites-redeploy-plan.md](.copilot-tracking/plans/2026-10-29/both-demo-sites-redeploy-plan.md) | Assessed candidate plan. |
| [.copilot-tracking/details/2026-10-29/both-demo-sites-redeploy-phase-details.md](.copilot-tracking/details/2026-10-29/both-demo-sites-redeploy-phase-details.md) | Assessed execution details. |
| [.copilot-tracking/research/2026-10-29/both-demo-sites-redeploy-research.md](.copilot-tracking/research/2026-10-29/both-demo-sites-redeploy-research.md) | Supplied operational research. |
| [.copilot-tracking/reviews/plans/2026-10-29/both-demo-sites-redeploy-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/both-demo-sites-redeploy-plan-critique.md) | Original Complete / Revise critique. |

## Next Steps

Active planning parent applies and records the five direct-compatible corrections, preserves this original critique, and finalizes without a second critique. Implementation remains gated on that disposition. No user action is required.
