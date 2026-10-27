---
title: Resident live acceptance plan critique
description: Independent final-candidate critique of bounded resident access restoration and partial acceptance publication
ms.date: 2026-10-27
---

## Metadata

* Task ID: 462-resident-live-2026-10-27
* Critique date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/resident-live-acceptance-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/resident-live-acceptance-phase-details.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate critique; no second critique requested or performed.

## Inputs and Criterion Boundary

* Caller requirements: ordered Research, Plan, Implement, Review; restore only ca-resident-demo--0000002 with external HTTPS until 2026-10-31T23:59Z and min0/max1; preserve the 1000-mapping guard, employee login, SQL S0, other app minima and eight Manual jobs; no secret/.env reads, new RBAC or endpoints. USD30 additional remains inside the renewed USD700 cap through 2026-12-31. Publication requires the requested scoped changed-path gate, timeout-zero shared lock, committed evidence, independent exact-head assessment and a main-target PR without closing keywords.
* Supplied evidence: .copilot-tracking/research/2026-10-27/resident-live-acceptance-research.md, including C1-C4/W1-W4; the plan and phase details above; caller context about credential custody, PR #478 and deployed main-based source.
* Targeted corroboration: infra/resident-demo.bicep for the explicitly requested actual target port; src/api/src/zava_forward/api/resident_demo/__main__.py for startup context; src/README.md and tools/rpi-checks.py for the cited publication contract. Required project context was consulted in docs/case_study_48_original.md, the relevant addendum framing, docs/reference/README.md and docs/reference/memory.md.
* Decisions and dependencies: existing tested image only; no rebuild, password bypass, credential rotation or fabricated session; positive authentication/isolation/natural expiry remain B1-blocked. P01 admission precedes mutation, P02 requires actual health, P03 requires original Review and the committed exact candidate.
* Boundary: assess operational planning, cost/expiry control, truthful acceptance and safe publication. This is not a generic source/security audit, fresh cloud verification, UI conformance review, implementation Review or publication approval. No cloud mutations or credential access were performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| G1, A1, P01-T02 | Partial | Exact revision/digest, HTTPS and rollback are specified, but the planned target port contradicts Bicep; PC-001. |
| A2, P01-T01, C4/W4 | Covered | Baseline/final comparisons preserve app projections, limits, SQL SKU and Manual jobs; no template redeployment or identity mutation. Runtime preservation remains to be demonstrated. |
| G2, A3/A4, P02-T01, C2/C3 | Covered | Real negative/browser scenarios are separated from individually blocked authenticated journeys. No credential-free login, forged expiry or whole-task acceptance is invented. |
| Budget requirement, P01-T01/P02-T02, W3 | Partial | USD30 allocation arithmetic is explicit, but October MTD and resident compute alone do not reconcile the renewed cap through December; PC-003. |
| Expiry requirement, P02-T02, C3/W4 | Partial | Application expiry and manual ARM closure are distinguished, but accountable closure/readback and missed-deadline handling are incomplete; PC-004. |
| G3, P02-T02, W1/W2 | Covered | Preserve PR #478 by immutable reference; map whole composite criteria and avoid closing keywords or copying evidence into the main-based branch. |
| A5, P03-T01, C1 | Partial | Original Review, clean commit, external receipt, fresh base and independent exact-head assessment are ordered; gate syntax and identity resolution need correction; PC-002/PC-005. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 2 High, 3 Medium, 0 Low.
* Rationale: The partial-acceptance strategy is credible and respects the no-secret-read constraint. However, the proposed ingress port would prevent the intended restoration, the written gate option is not executable, and cost/expiry/publication details need the bounded corrections below before implementation. These are direct planner corrections, not grounds to invent another approval or broaden scope.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Planned ingress target does not match the resident listener

* Related IDs: G1, A1, P01-T01, P01-T02.
* Evidence: .copilot-tracking/plans/2026-10-27/resident-live-acceptance-plan.md:126 specifies port8080. .copilot-tracking/details/2026-10-27/resident-live-acceptance-phase-details.md:41 incorrectly calls 8080 the template port. infra/resident-demo.bicep specifies ingress targetPort 8089 and container PORT value 8089.
* Concern: The proposed ingress mutation would send requests to the wrong port. Activating the right immutable revision does not correct a misrouted ingress.
* Impact: Owner feedback access remains unavailable and the ten-minute rollback can deactivate the otherwise valid tested revision.
* Smallest useful change: Correct both operational instructions to 8089. Add a pre-mutation comparison of safe live ingress and the allowlisted non-secret PORT value with Bicep, stopping on unexpected disagreement rather than rewriting the revision.
* Action owner: Planning parent; implementation operator records the readback.
* Exact resolving evidence: Revised P01-T01/P01-T02 consistently name 8089; planned safe baseline includes PORT/targetPort comparison, and subsequent implementation evidence must show external=true, targetPort=8089, allowInsecure=false, intended revision traffic and actual HTTPS /healthz plus sign-in responses.
* Decision route: Direct planner correction. No user decision is required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Publication gate command does not encode the requested executable contract

* Related IDs: A5, P03-T01, C1.
* Evidence: .copilot-tracking/plans/2026-10-27/resident-live-acceptance-plan.md:156 says to run --changed --lock-timeout0. tools/rpi-checks.py:2194-2202 defines --changed, --lock-timeout with a separate integer value, and --required-scope with default full. src/README.md explicitly requires --required-scope partial when verifying a partial receipt.
* Concern: --lock-timeout0 is not a valid runner option. Although the details mention partial verification, neither artifact provides the unambiguous corresponding verification invocation.
* Impact: The requested scoped publication gate can fail before execution, or partial evidence can be rejected by default full-scope verification. Removing the lock or treating an unverified receipt as sufficient would not resolve this.
* Smallest useful change: Specify the execution argv as python3 tools/rpi-checks.py --changed --lock-timeout 0 --base <reviewed-main-sha> --out <new-authorized-external-directory>, and verification as python3 tools/rpi-checks.py --verify-receipt <receipt.json> --required-scope partial --base <fresh-origin-main-sha>. Preserve runner-owned locking, exact HEAD/base, clean inputs and the existing stop-on-main-movement rule.
* Action owner: Planning parent; publication operator executes the corrected contract.
* Exact resolving evidence: P03-T01 contains valid execution/verification argv and explicitly requires successful receipt verification before independent exact-head assessment and push. Final implementation evidence must retain a real partial receipt and verification outcome, not a full-tier claim.
* Decision route: Direct planner correction. The owner already chose scoped --changed validation; do not substitute a full gate or seek renewed approval for that choice.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Cost admission does not yet reconcile the renewed cap period

* Related IDs: Budget requirement, P01-T01, P02-T02, W3.
* Evidence: .copilot-tracking/research/2026-10-27/resident-live-acceptance-research.md reports October MTD ActualCost USD315.535491423131 and billing delay. Plan lines77-80 and details lines31-34/76-78 allocate USD5+USD1+USD20+USD4 within USD30 but do not specify reconciliation of spend/reservations against the renewed USD700 cap through 2026-12-31.
* Concern: A valid resident compute estimate and the additional USD30 allocation do not establish remaining headroom for the entire authorized cap period. October MTD is not the December-period total or forecast, and an unspecified existing baseline cannot be mechanically admitted.
* Impact: The operator could admit the resident allocation using an incomplete denominator or double-count existing reservations while claiming the renewed cap is satisfied.
* Smallest useful change: Define the admission ledger fields and comparison: owner-authorized cap period/scope, available actuals and their dates, existing committed/reserved amounts, remaining-period baseline estimate, the non-duplicated USD30 allocation, uncertainty and resulting headroom. Unknown material inputs block admission; do not silently reuse the addendum's older monthly authorization or manufacture forecasts.
* Action owner: Planning parent defines the ledger contract; implementation operator supplies permitted cost metadata and available budget evidence.
* Exact resolving evidence: P01-T01 specifies a dated cap reconciliation and an explicit admit/stop calculation; P02-T02 retains that same accounting in cost-ledger.json, labels estimates and delayed billing, and shows the USD30 allocation counted exactly once inside the renewed USD700 authorization.
* Decision route: Direct planner correction. A new user decision is needed only if implementation discovers genuinely unavailable budget scope/headroom evidence or requires expenditure beyond the already authorized bounds.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Expiry closure lacks an accountable handoff and missed-deadline cost treatment

* Related IDs: Expiry requirement, P01-T02, P02-T02, follow-up items.
* Evidence: Plan lines173-175 assign closure to an unspecified expiry operator. Details lines80-81 require operator-run close/deactivate commands but no named handoff, completion readback or missed-deadline response. Research explicitly says application expiry does not remove ARM ingress, while the compute estimate ends at 2026-10-31T23:59Z.
* Concern: Recording commands does not establish that someone owns execution after this session ends. Application refusal protects content but does not establish inactive revision/no ingress, or eliminate compute and ancillary costs from requests after expiry.
* Impact: Public ingress and an activatable workload can persist beyond the intended operational window, with unbounded-by-this-estimate residual cost despite fail-closed serving.
* Smallest useful change: Make the expiry handoff an explicit deliverable to the owner or an actually designated operator: exact UTC deadline, resource-scoped close/deactivate commands, safe final readback expectations and a missed-deadline escalation/closure instruction. Record handoff/closure as pending until evidenced. Include potential post-expiry residual cost in uncertainty; add no scheduler or job and do not shorten the approved feedback window.
* Action owner: Planning parent defines the handoff; owner or explicitly designated existing operator performs expiry closure.
* Exact resolving evidence: Revised P02-T02 assigns the handoff and records its delivery status, identifies closure proof as disabled/null resident ingress and inactive ca-resident-demo--0000002, preserves other workloads, and states that application expiry alone is not closure or a zero-cost guarantee. Future closure evidence is marked pending rather than claimed now.
* Decision route: Direct planner correction. No new cloud authority is required; if no operator can accept the future action, return that operational gap without inventing an appointment or automatic shutdown.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Commit identity is frozen instead of resolved at the commit boundary

* Related IDs: P03-T01, privacy-safe publication requirement.
* Evidence: .copilot-tracking/details/2026-10-27/resident-live-acceptance-phase-details.md:96-97 prescribes account8036360+jmservera@users.noreply.github.com. Repository instructions require gh api user before committing and deriving the repository-local author/committer address from its returned id/login.
* Concern: A previously resolved literal is not a commit-time authenticated account check. The details omit the required resolution step and can misattribute commits if the authenticated account differs.
* Impact: Publication can use a stale identity despite retaining a privacy-safe email format.
* Smallest useful change: Replace the fixed address with the gh api user step immediately before commit, derive {id}+{login}@users.noreply.github.com, configure only repository-local user.email, and ensure both author and committer use it with the required Copilot trailer.
* Action owner: Planning parent; commit operator resolves the account.
* Exact resolving evidence: Revised P03-T01 specifies dynamic account resolution and local configuration; eventual commit metadata confirms the resolved noreply author/committer and trailer without recording private email or credentials.
* Decision route: Direct planner correction. No user response is required.

## Strengths and Residual Risk

* B1 is correctly retained as an unmet requirement, not a waiver. The plan does not invent credential-free login, obtain owner secrets, forge a valid session, shorten natural expiry or substitute anonymous UI for authenticated acceptance.
* The exact tested digest, min0/max1, bounded readiness polling and target-only rollback are explicit. Existing employee, SQL and Manual-job preservation is within the intended operational boundary.
* The planned one original independent Review, immutable prior evidence, exact-head publication assessment, no-closing-keyword PR and separation from hosted/human approval are appropriate.
* Genuine positive login, own-data UI, authenticated isolation, logout and natural session expiry remain owner-dependent after these planner corrections. Neither this critique nor a later scoped gate establishes full live acceptance.

## Questions or Blocking Evidence Gaps

* No unresolved user choice prevents the direct revisions above.
* The owner-held password remains deliberately unavailable. Keep B1 blocked and use the existing secure owner custody route for later positive evidence; do not seek secret reads or create a login bypass.
* Fresh cost admission, protected-resource comparisons and actual live health remain implementation evidence to collect, not observations established by this critique.

## Limitations

* No fresh Azure, billing, GitHub lifecycle, browser or receipt execution was performed. W1-W4 and the supplied branch/PR history are assessed as recorded evidence, not independently refreshed cloud facts.
* Source inspection was restricted to the explicitly requested Bicep port and the supplied startup/gate evidence pointers. No broad source, security, accessibility or regulatory audit was performed.
* Only this critique artifact was written. Plan, phase details, research, original evidence and source were not edited.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Correct the target port to 8089, dispose PC-002 through PC-005 directly in the existing plan/details, then continue the ordered parent workflow without another critique.
* User response required: No for these revisions. Owner-held authenticated testing and future expiry closure remain explicitly separate owner/operator actions.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-27/resident-live-acceptance-research.md](.copilot-tracking/research/2026-10-27/resident-live-acceptance-research.md) | Supplied operational and acceptance evidence. |
| [.copilot-tracking/plans/2026-10-27/resident-live-acceptance-plan.md](.copilot-tracking/plans/2026-10-27/resident-live-acceptance-plan.md) | Final-candidate plan assessed without modification. |
| [.copilot-tracking/details/2026-10-27/resident-live-acceptance-phase-details.md](.copilot-tracking/details/2026-10-27/resident-live-acceptance-phase-details.md) | Phase details assessed without modification. |
| [.copilot-tracking/reviews/plans/2026-10-27/resident-live-acceptance-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/resident-live-acceptance-plan-critique.md) | Single complete independent critique and actionable finding set. |

## Next Steps

The active planning parent should revise and disposition PC-001 through PC-005 directly, finalize without a second critique, and continue to P01-T01 only after those corrections. No user response is required for planner-owned changes. Preserve B1 and the partial outcome; obtain no additional cloud authority or secrets by implication.
