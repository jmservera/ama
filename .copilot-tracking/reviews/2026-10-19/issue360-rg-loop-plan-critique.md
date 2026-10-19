---
title: Issue360 bounded RG publisher original plan critique
description: One preimplementation assessment of the supplied bounded publisher candidate
ms.date: 2026-10-19
---

## Metadata

* Task ID: 360 / issue360-rg-loop
* Critique date: 2026-10-19
* Plan: .copilot-tracking/plans/2026-10-19/issue360-rg-loop-plan.md
* Phase details: .copilot-tracking/details/2026-10-19/issue360-rg-loop-phase-details.md
* Research: .copilot-tracking/research/2026-10-19/issue360-rg-loop-research.md
* Branch: fix/demo-private-publisher-360
* Inspected HEAD and supplied base: 634a024d97d2da7168b8a7d5f343ab26e6108cf3
* Critique execution status: Complete
* Assessment count: One original preimplementation critique. No repeat critique or postimplementation Review performed.

## Inputs and Criterion Boundary

* Caller direction authorizes necessary resource operations inside the existing ama resource group, including the proposed temporary publisher and its registry-only AcrPush assignment. It does not authorize deleting ama, subscription/tenant operations, public backing access, bypass/policy weakening, unknown/private datasets or approval substitution.
* Assessed all three supplied candidate documents, their requirements, C1-C4 and W1-W6 evidence summaries, P01-P03 and all eight tasks, acceptance criteria 1-7, locked maximum of one new test module and prohibition on test removals.
* Examined relevant existing source: infra/cutover-proof.Dockerfile, infra/.dockerignore, infra/scripts/private-cutover-proof.py, infra/README.md:1790-2100, infra/staff-initializer-rbac.bicep, infra/modules/staff-initializer-guard.bicep, infra/modules/guard.bicep, infra/modules/network.bicep, infra/tests/test_private_cutover_proof.py, infra/tests/test_identity_rbac.py, infra/tests/test_bicep_policy.py, infra/role-assignments.json, src/README.md and the infrastructure-discovery portions of tools/rpi-checks.py.
* Read the original case study and relevant addendum, KB index, owner memory and sector-primer context. These do not supply additional cloud authority or live acceptance evidence.
* Existing API base 111b26226cad06e229bcf1c3174877510c4c68c5a5fefc885167a2b4c821657d and historical initializer ef0058f8f380cc610d4b7113509293b3ed624d22afac95e807b4c69a4266dc72 are candidate inputs, not newly verified registry observations.
* Assessment covers planning credibility, source-bound proof, deployment/pin reversibility, exact owned cleanup and publication gates. It does not certify current Azure state, quota/allocation, retail prices, credential access, image execution, secret equality or demo acceptance.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Caller RG authority and preservation limits; P01-T01/T02 | Partial | Scope is correctly bounded in prose; exact subscription/resource identity and unresolved preview handling need PC-002. |
| C1/C2; P02-T01; acceptance 2-3 | Covered | Seven-file source allowlist agrees with Dockerfile and context exclusions; fixed source/base digests, actual no-network nonroot smoke and digest pull/run are required. |
| C3; P02-T03; tenant/SQL/AI boundaries | Covered | No historical initialize, unknown-data probe, Graph privilege inference, credential upload or real-acceptance substitution is proposed. |
| W1-W4/W6; P01-T02 | Partial | Candidate records SKU, quota, pinned image, outbound route and estimated cost; operator lifetime and interrupted allocation recovery need PC-003. |
| P01-T01; locked tests; acceptance 1 | Partial | Compiled security checks are appropriate, but the existing all-Bicep role parser cannot accommodate the proposed new assignment as currently scoped; PC-004. |
| P01-T02/P03-T01; acceptance 5 | Partial | Owned-only deletion and preservation are explicit; pre-write recovery inventory and bounded failure handling need PC-003. |
| P02-T02; acceptance 4 | Partial | Image-only update and read-visible comparison are strong; rollback actions and concurrency handling need PC-001. |
| P03-T02; acceptance 6 | Covered | Existing runbook/ADR/evidence/KB updates preserve history and distinguish technical evidence from owner/human outcomes. |
| C4; P03-T03; acceptance 7 | Partial | One original later Review, no remote writes and full clean-head gate are preserved; current-main verification and tool/output prerequisites need PC-005. |
| W5; #349/#358 dependencies | Covered | Tenant work remains blocked and #358 follows without shared edits; no tenant or secret-preservation round-trip success is invented. |

## Verdict

* Verdict: Revise
* Severity summary: 4 High, 1 Medium; 0 Critical, 0 Low.
* Rationale: The selected private publisher is a credible bounded route within the newly supplied authority. Its successful path is well constrained, but failed image activation and interrupted resource allocation lack sufficient recovery contracts. Exact-resource authorization, an identifiable existing IAM-test incompatibility and final gate freshness also need direct planning corrections before implementation/cloud writes.
* All findings below are planner-direct corrections under existing direction. No significant or divergent owner decision is required to revise the candidate. No additional critique is requested.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Retaining a rollback digest does not define safe failed-pin recovery

* Related IDs: P02-T02; acceptance 4; settings/MI/secrets preservation.
* Evidence: .copilot-tracking/plans/2026-10-19/issue360-rg-loop-plan.md:63-67 retains the old digest and requires comparison. .copilot-tracking/details/2026-10-19/issue360-rg-loop-phase-details.md:51-57 defines the update but no action for timeout, unexpected starting image, post-update mismatch or concurrent writer. infra/README.md:2081-2093 records the historical initializer shape and limitations of read-visible fingerprints.
* Concern: The plan can detect a failed preservation check only after the existing job has changed. It neither requires the fresh starting image to match the expected rollback digest nor specifies how to determine whether an ambiguous CLI failure applied the new image. A later rollback to the hardcoded historical digest could overwrite an intervening legitimate change.
* Impact: An image-only operation can leave the initializer at an uncertain image, or a recovery can clobber another operator's update. A mismatch could be recorded as blocked without actually restoring the authorized image state.
* Smallest useful change: Add a serialized activation/recovery window or supported concurrency precondition. Freshly assert the exact existing job ID, Manual trigger, expected starting digest and required identity/registry/container shape immediately before writing; stop on unexpected state. Capture the actual verified starting image as the rollback target. On update failure/timeout or failed comparison, independently read back first; if this run's image is present and restoration is safe, restore only that image field with the same container selector and verify the full normalized non-image baseline plus restored image. Do not replay a whole GET body or restore secret/configuration fields. On unrelated drift, failed readback or failed rollback, stop, identify the unresolved state and hand off without blind retry or job execution.
* Action owner: Planning parent, then implementation operator for the bounded activation.
* Exact resolving evidence: Revised P02-T02 specifies starting-state assertions, concurrency mechanism, timeout/readback branches and image-only rollback command shape. The later sanitized activation receipt records the before/published/final image references and comparison result; a failed attempt records the rollback readback or explicit unresolved-state handoff. No cloud write is required to resolve this planning finding.
* Decision route: Direct planner correction; owner input is not required. Any genuinely observed unrelated live drift is a later stop/handoff, not present permission to overwrite it.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Name-only scope protection is insufficient for the exact-resource deployment gate

* Related IDs: P01-T01/P01-T02; acceptance 1 and 5; caller authority inside the existing ama only.
* Evidence: .copilot-tracking/details/2026-10-19/issue360-rg-loop-phase-details.md:14-19 specifies the existing non-ama guard pattern and existing VNet/ACR declarations; lines 27-29 permit changes inside the owned-resource/subnet category. infra/modules/staff-initializer-guard.bicep and infra/staff-initializer-rbac.bicep demonstrate a resource-group-name guard, not a binding to the supplied existing group's full ID.
* Concern: The candidate does not say how the reviewed deployment binds to the exact existing subscription/RG/VNet/ACR IDs rather than another group named ama, or how the apply is proven identical to its preview. An assignment dependent on a not-yet-created system MI may contain unresolved what-if fields; the prose does not distinguish those from known, authorized changes. A broad exception for the new subnet must not permit replacing the VNet's subnet collection or accepting other parent modifications.
* Impact: A correct-looking resource-group name or change-class summary can authorize the wrong target, an unexpected principal/scope, or destructive network changes despite the intended boundary.
* Smallest useful change: Specify a pre-write private authorization record containing the exact existing target IDs, owned resource IDs/names, deployment mode Incremental, template/parameter hashes and baseline subnet/security settings. Require a machine-checked expanded what-if allowlist of exact new resources and narrowly identified child-subnet changes, including guard-deployment metadata separately. Reject unexplained Modify/Delete/Ignore/unsupported or unresolved authorization-relevant results; do not blanket-allow parent VNet changes. Apply the identical reviewed inputs with explicit target subscription. If the future MI prevents resolving the assignment principal, use a bounded staged preview/readback for that assignment after VM identity creation, or stop; do not waive the principal/scope check.
* Action owner: Planning parent; implementation operator produces and checks the private preview.
* Exact resolving evidence: Revised P01-T01/T02 names the target-binding, identical-input and incremental-mode checks, allowed exact resource paths and unresolved-result stop rule. The single permitted new test module includes negative fixtures for wrong target, unrelated Create/Modify/Delete, parent subnet replacement and unresolved/wrong role scope/principal. Later deployment evidence binds sanitized preview/apply hashes and confirms existing subnets/backing controls unchanged.
* Decision route: Direct planner correction. This consumes existing RG-contained authority; it does not request subscription-level operations or wider IAM.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Interrupted provisioning can precede both the watchdog and a usable cleanup inventory

* Related IDs: P01-T02/P03-T01; two-hour lifetime; acceptance 5.
* Evidence: .copilot-tracking/plans/2026-10-19/issue360-rg-loop-plan.md:55-58 correctly distinguishes guest poweroff from deallocation. .copilot-tracking/details/2026-10-19/issue360-rg-loop-phase-details.md:30-32 writes created IDs immediately and requires partial cleanup, while lines 73-77 give final cleanup classes. No allocation-to-deallocation deadline, pre-write recovery manifest, interrupted execution handler or cleanup-failure deadline is specified.
* Concern: VM creation may partially succeed, hang or lose the operator connection before Run Command installs a watchdog or an apply result supplies created IDs. A relative 7200-second guest timer installed later is not an allocation-time bound, does not establish its own successful arming and cannot stop compute billing. Merely placing cleanup in P03 does not establish that all earlier failure paths reach it.
* Impact: A publisher, disk/PIP or registry grant can remain billable or live beyond the bounded window, and an interrupted operator may lack enough evidence to safely identify only owned leftovers.
* Smallest useful change: Persist the planned exact IDs, unique run ownership, deployment name, UTC creation/deallocation deadline and cleanup procedure before the first write; enrich it with actual VM principal/assignment/disk IDs as they become observable. Define a responsible operator and bounded provisioning/Run Command timeouts with sufficient cleanup reserve. Establish and verify the guest timer before package/build work, but require operator deallocation by the absolute deadline whether or not guest setup succeeds. Route every success/failure/interrupt through owned cleanup, with restart-from-inventory instructions for hard interruption. Poll deletion completion and separately verify the OS disk even when Delete-on-VM is selected; report cleanup failure as an unresolved blocker and immediate exact-resource handoff, not a successful bounded run.
* Action owner: Planning parent defines the contract; implementation operator owns the timed window and recovery.
* Exact resolving evidence: Revised P01-T02/P03-T01 contains the pre-write inventory schema, absolute deadline/operator responsibility, timeout/finally and hard-interruption recovery branches. Later evidence records watchdog arming, allocation/deallocation/deletion times, exact resource and assignment absence, and old-stack preservation. If the attended cleanup window cannot be provided, implementation stops before allocation.
* Decision route: Direct planner correction. The caller already accepts operator cleanup rather than a guaranteed unattended billing cap; do not add subscription scheduling or extra MI permissions.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: The new publisher assignment conflicts with the existing all-Bicep IAM contract

* Related IDs: P01-T01/P03-T03; acceptance 1 and 7; locked tests and no removals.
* Evidence: infra/tests/test_identity_rbac.py:12 discovers every infra Bicep file. Its parse_bicep_assignments at lines 43-66 assumes assignments outside the known custom-role files belong to MODULE_FILES and SCOPE_NAMES; the new private-proof-publisher.bicep has no entry. infra/role-assignments.json has production/runtime assignments but no temporary publisher AcrPush entry. tools/rpi-checks.py runs complete infra/tests discovery. The plan's scoped edits/tests do not account for this existing contract.
* Concern: Adding the ordinary registry-scoped VM assignment to the proposed canonical template will be discovered by the existing parser, which cannot resolve its new file/system-MI principal through MODULE_FILES. Depending on expression spelling, parsing fails before or at that lookup; alternatively, adding only a parser mapping still leaves matrix equality unresolved. Running just new-template/proof/setup tests will miss this until the full post-cloud gate.
* Impact: A foreseeable gate failure forces an unplanned IAM-test/matrix correction after live operations or tempts an overbroad exclusion that weakens the existing all-assignment coverage.
* Smallest useful change: Explicitly include a narrow compatibility update to the existing IAM parser/contracts and, if represented there, the role matrix. Model temporary publisher grants separately from unchanged runtime/default grants and require exactly one registry-scoped AcrPush assignment to this VM's system MI. Keep exhaustive assignment accounting and existing production expectations; do not skip the template or remove tests. Add test_identity_rbac to the pre-cloud focused selectors along with the new module and existing proof/setup/staff/auth regressions.
* Action owner: Planning parent, then implementation owner of infra/tests/test_identity_rbac.py.
* Exact resolving evidence: Revised P01-T01 lists the existing parser/matrix integration and selectors. Before cloud writes, the later test result includes passing complete test_identity_rbac, compiled publisher tests and relevant existing regressions, with negative coverage for an extra/broader/wrong-principal assignment. At most infra/tests/test_private_proof_publisher.py is newly added as a test module; none are removed.
* Decision route: Direct planner correction. This is a tightly coupled compatibility change, not permission to expand grants or alter production deployment defaults.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Final gate instructions do not define current-main mismatch or executable prerequisite handling

* Related IDs: C4; P03-T03; acceptance 7.
* Evidence: .copilot-tracking/details/2026-10-19/issue360-rg-loop-phase-details.md:94-97 hardcodes the historical tool directory and supplied base, then says to fetch main and verify. src/README.md requires a fresh external receipt bound to frozen HEAD/base/tools and verification against freshly fetched main immediately before independent exact-head assessment; relevant changes invalidate it.
* Concern: The exact verification command and comparison of freshly fetched origin/main with the approved base are omitted. A fetch after the gate may reveal a moved main without a defined stop path. The specified /tmp/rpi-413-tools path is neither established by the supplied evidence nor compatible with this execution's prohibition on temporary-directory file operations. A generic fresh-external-dir also needs a concrete permitted operator location. These are reproducibility prerequisites, not reasons to reuse another task's receipt or silently alter the reviewed base.
* Impact: The coordinator can receive a receipt for a stale base or unavailable/different toolchain, despite a nominal all-groups pass. Resolving that with a late commit or silent rebase would invalidate the exact-head handoff.
* Smallest useful change: Fetch/resolve origin/main before the gate and explicitly compare it with 634a024d97d2da7168b8a7d5f343ab26e6108cf3. On mismatch, stop and return the base decision to the coordinator under the existing branch safeguards; do not silently rebase. Use a verified permitted toolchain and permitted fresh output location outside the candidate, without prescribing the unsupported temporary path. Specify the literal verify-receipt invocation against freshly fetched main immediately before coordinator handoff, exact frozen HEAD, clean inputs and all required groups passing. If base/HEAD/tools/images/inputs change or prerequisites are missing, block handoff and obtain a new complete receipt after authorized reconciliation.
* Action owner: Planning parent; implementation operator runs the gate; coordinator owns any changed-base decision.
* Exact resolving evidence: Revised P03-T03 records permitted tool/output prerequisites, pre-gate target comparison, exact verification command and mismatch stop rule. Later handoff includes matching frozen HEAD/base/current-main and successful external receipt verification; no push/PR, receipt-copy substitution or post-gate commit occurs.
* Decision route: Direct planner correction now. Only an actually observed changed-base reconciliation may subsequently need the coordinator/owner decision already required by branch safeguards.

## Strengths and Residual Risk

* The plan correctly distinguishes newly authorized RG-contained publisher operations from tenant/subscription authority and historical prohibitions. No new approval request is needed merely to use the authorized VM/PIP/subnet/registry grant.
* Seven allowlisted context files, exact base-source hashes, immutable API base, overridden ENTRYPOINT, network-disabled smoke, nonroot/runtime checks and same-digest pull/run address the prior source-only and stale-image evidence gaps. The existing Dockerfile/context need not be redesigned.
* The proposed dedicated subnet, explicit outbound method, deny-all inbound and Run Command avoid inbound management exposure without weakening private backing services.
* Retail pricing and quota are dated research observations, not guaranteed allocation or a hard cost cap. The operator-cleanup model is explicitly accepted; a guest poweroff must never be presented as Azure deallocation.
* Image GET/configuration fingerprints cannot establish write-only secret equality. Deferring the separate #358 round-trip is appropriate.
* Graph token issuance without roles/scopes and a failed application-read probe does not enable tenant work. #349 credentials/consent, real browser/SQL/AI acceptance, human approvals and Front Door retirement remain separate.
* Full local tests and scans are engineering gates only. They do not establish cloud approval, real data access, actual demo success or hosted/human acceptance.

## Questions or Blocking Evidence Gaps

* No owner question is necessary to make these planning corrections.
* Before cloud writes, implementation must supply the exact target/preview, pre-write recovery manifest, attended cleanup window and passing IAM-compatible focused tests.
* Actual allocation, both private ACR endpoints, MI authorization, the built/pulled runtime and image-only readback remain execution gates, not facts established by this critique.

## Limitations

* No agents were spawned. No source implementation, test execution, Azure probe/write, deployment preview, tenant operation, private-dataset read, publication or git/remote mutation was performed.
* Current research observations, live issue summaries and external-source findings were assessed as supplied. Their underlying raw private Azure responses and live services were not independently re-queried.
* Existing untracked candidate/session inputs were present at intake and left in place. This critique does not commit, move or reconcile them.
* The only authored artifact is this critique. Plan, details, research, historical reviews and executable sources remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Revise P02-T02 to include fresh starting-state/concurrency assertions and verified image-only rollback, then disposition PC-002 through PC-005 in the same plan revision before implementation.
* User response required: No.
* Original outcome preservation: Retain this Revise verdict and all PC findings; append their dispositions in the planning parent's records. Do not repeat this critique. Perform exactly one original postimplementation Review later, followed by the complete frozen-candidate gate and coordinator assessment.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-19/issue360-rg-loop-plan.md](.copilot-tracking/plans/2026-10-19/issue360-rg-loop-plan.md) | Assessed original candidate plan |
| [.copilot-tracking/details/2026-10-19/issue360-rg-loop-phase-details.md](.copilot-tracking/details/2026-10-19/issue360-rg-loop-phase-details.md) | Assessed original phase details |
| [.copilot-tracking/research/2026-10-19/issue360-rg-loop-research.md](.copilot-tracking/research/2026-10-19/issue360-rg-loop-research.md) | Supplied research and evidence boundary |
| [.copilot-tracking/reviews/2026-10-19/issue360-rg-loop-plan-critique.md](.copilot-tracking/reviews/2026-10-19/issue360-rg-loop-plan-critique.md) | This one original critique |

## Next Steps

The active planning parent should revise and disposition PC-001 through PC-005 directly, without another critique or additional research unless an actual material blocker emerges. No user action is required for these corrections. Continue to implementation only after the candidate states the corrected gates; retain the one original independent postimplementation Review for later. Do not perform cloud writes, push or create a PR from this critique stage.
