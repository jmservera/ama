---
title: Final-candidate plan critique for deploy-resident-474
description: Independent assessment of the authorized partial deployment and its operational and publication gates
ms.date: 2026-10-27
---

## Metadata

* Task ID: deploy-resident-474
* Critique date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/deploy-resident-474-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/deploy-resident-474-phase-details.md
* Research: .copilot-tracking/research/2026-10-27/deploy-resident-474-research.md
* Critique execution status: Complete
* Critique count: one independent final-candidate assessment; no further critique requested.

## Inputs and Criterion Boundary

* Caller requirements: ordered RPI; merged PR #474 deployed from latest main on chore/deploy-resident-474; ama only; additional USD30, AI at most USD20; authority through 2026-10-31T23:59Z; managed identity, no keys; no resident/vault/.env secret reads; no broad grants, new groups or private endpoints; preserve all existing apps at min0, eight Manual jobs, SQL and employee login; test-only ingress; timeout-zero shared heavy locking; pip, not uv; scoped changed-path gate; committed evidence and a PR without closing keywords.
* Supplied evidence: the three artifacts above and their necessary repository code/runbook pointers. Read Dockerfile.resident-demo, resident startup and adapter, session/authority constants, resident HTTP dispatch, the supplied prior release changes, the assistant design and relevant local gate implementation/documentation. Project context/index/memory were consulted as required, not treated as fresh operational evidence.
* Decisions: exact merged-code deployment only; deterministic provider retained; no credential rotation, forged positive sessions, mock acceptance, model provisioning without usable wiring, or source/test additions. Credential-dependent journeys and model activation remain UNMET requested requirements.
* Dependencies: P01-T02 follows immutable image release; P02 follows healthy resident revision; P03 follows closure and invariants. Critique precedes mutations. Original Review, clean candidate commit, scoped receipt and independent exact-head assessment remain distinct publication obligations.
* Assessment boundary: planning credibility, authorized subset, preservation, rollback, spending admission, testing and gate ordering. This critique performs no cloud/source mutations and independently verifies no live configuration, billing, credential availability or hosted approval.
* Test scope is locked: parent deployment task owns tests; zero source/test additions and zero removals. All recommendations below use existing tools/contracts and sanitized external evidence plus dated tracking summaries, not new committed tests.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| Ordered RPI and explicit partial acceptance | Covered | Research, candidate plan, independent critique and later Review are distinguished. |
| Requested authenticated journeys and AI activation; C2-C5 | Covered as UNMET | Startup is deterministic; adapter requires host callbacks/durable reservations; owner credential is unavailable. Neither requirement is waived. |
| Existing ama, no grants/keys/SQL writes or employee changes | Covered in scope | Image-only resident update is appropriately narrower than a Bicep deployment; PC-008 clarifies safe capture. |
| P01-T01; C1, W3; ACR restoration | Partial | Exact-state intent is sound, but failure-safe restoration needs PC-001. |
| P01-T01; fresh USD30 and bounded builds | Partial | Allocations are not an evidenced spend upper bound; PC-003. |
| P01-T01/P01-T02; fresh image and immutable identity | Partial | Digest pinning is sound; source CI/scoped tracking gate do not validate the newly built image; PC-007. |
| P01-T02/P02-T02; four apps, eight jobs, SQL and employee preservation | Partial | Correct resource cardinality and metadata-only boundary; PC-008. |
| P02-T01; real negative HTTPS/browser tests | Covered | Source serves static asset bytes directly; hash parity is meaningful for identity, not authenticated feature acceptance. |
| P02-T01/P02-T02; bounded ingress and final closure | Partial | Finally intent needs a deadline mechanism and failure disposition; PC-002. |
| P03-T01; scoped receipt and timeout-zero lock | Partial | Gate runner owns the lock, but explicit flags are missing from the executable sequence; PC-004. |
| P03-T01; fresh main and candidate ancestry | Partial | Re-running alone cannot reconcile a moved base; PC-005. |
| P03-T01; independent exact-head assessment/publication | Partial | Original Review does not explicitly cover final receipt-bound head; PC-006. |
| No source/test additions or removals; external sanitized evidence | Covered | Preserve the locked boundary throughout all dispositions. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 6 High, 2 Medium, 0 Low.
* The supplied evidence supports assessing the plan; this is not a Blocked critique.
* The independently authorized deployment subset can proceed after the relevant operational corrections below are incorporated and their admission checks pass. Missing owner credentials and model-host/ledger wiring do not, by themselves, prohibit deploying the already merged deterministic features.
* Full requested acceptance remains blocked by those missing dependencies. Unauthenticated tests, asset parity, unchanged employee metadata, a successful deployment or a partial local receipt cannot establish authenticated resident acceptance, working employee login, Azure OpenAI activation, human approval or hosted approval.
* Findings are the complete actionable set identified within the supplied boundary. The planning parent should revise directly without commissioning another critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Specify failure-safe ACR restoration, including the known IP-rule removal failure

* Related IDs: P01-T01, P02-T02, research W3.
* Evidence: .copilot-tracking/details/2026-10-27/deploy-resident-474-phase-details.md, P01-T01; .copilot-tracking/changes/2026-10-26/resident-release-462-changes.md, Research summary. The earlier restoration left a rule behind because Azure stored a bare IP while removal used /32.
* Concern: The candidate invokes a historical push route and promises a trap/exact equality but does not state the mutation/restore ordering, stored-rule normalization, restoration-error handling or what happens when restoration cannot be proved. The captured actual baseline can differ from the historical expected state.
* Impact: A failed push, interruption or partial rollback can leave public/export access or an IP rule changed; restoring default Allow before closing public access can widen exposure.
* Smallest useful change: Add the explicit owned-field procedure: save actual public access/export/default action/bypass and complete rule sets before mutation; establish Deny plus the approved VM rule while public access is still closed, then expose only as necessary. In cleanup close public access first, remove only the added rule using its read-back representation, restore captured policies/rules in safe order, and restore any originally enabled access only after its original restrictions are restored. Preserve the original operation error separately. Bound retries, require canonical policy equality and block deployment/publication on unresolved restoration.
* Action owner: Planning parent; deployment implementer executes and records.
* Exact resolving evidence: Revised P01-T01 procedure and a sanitized before/after canonical policy comparison with zero unexpected differences, including public/export/bypass/default/rule fields; explicit cleanup exit status after success or failure.
* Decision route: Direct planner correction; no new user decision or expanded grant.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Make the 30-minute ingress limit enforceable independently of the test runner

* Related IDs: P02-T01, P02-T02.
* Evidence: .copilot-tracking/details/2026-10-27/deploy-resident-474-phase-details.md promises a bounded window, cleanup before exposure and always disabling ingress, but names no deadline mechanism or closure-failure path.
* Concern: A finally/exit trap alone does not enforce the window if the browser or CLI hangs, the controlling process is killed, or the disable request fails. An attempted disable is not proof of disabled ingress.
* Impact: The synthetic endpoint can remain exposed beyond the authorized test-only window.
* Smallest useful change: Specify an independently running, owned closure watchdog using existing authorized tooling, no new Azure resource; arm and verify it before exposure. Use an absolute close deadline no later than 30 minutes or the authority end, bound test/CLI calls, and keep the watchdog until successful disable plus ARM ingress-null readback. On closure failure stop further work except bounded recovery, preserve failure evidence and block publication; do not record a completed restoration.
* Action owner: Planning parent; deployment implementer owns watchdog and recovery.
* Exact resolving evidence: Revised mechanism/ownership/deadlines, watchdog-armed evidence, opening/closing UTC timestamps, successful disable and final ingress-null readback. Confirm HTTPS enforcement, deployed revision identity and final external non-service before closure is counted passed.
* Decision route: Direct planner correction; no extra owner confirmation for ordinary bounded cleanup.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Turn the nominal USD1 reservation into an evidenced admission bound

* Related IDs: P01-T01, P02-T01, P02-T02; research W4.
* Evidence: Both candidate artifacts allocate USD1 to build/test and promise remote-build cancellation after 600 seconds; research correctly says billing is delayed and alerts are not hard caps.
* Concern: No rate/quantity calculation, operation-count limit or cancellation confirmation connects those limits to USD1. A local CLI timeout does not establish that the remote ACR run stopped billing, and failures/retries plus revision startup overlap are not accounted for.
* Impact: The plan can exceed its own build/test allocation while claiming admission passed, even though no model is created.
* Smallest useful change: Before spending, record a conservative bound with rate provenance, remote build count/duration, app resources and possible simultaneous active revisions, test duration and bounded retries. Prefer local build if remote admission cannot be supported. Identify the remote run ID and cancel/confirm terminal status when timed out before fallback. Track outstanding reservations and stop when an unknown upper bound or exhausted allocation prevents admission; do not silently consume the USD20 retained model allocation or USD9 contingency.
* Action owner: Planning parent; deployment implementer maintains the operation ledger.
* Exact resolving evidence: Sanitized preflight calculation and admitted operations, recorded run IDs/terminal states, durations, consumed/reserved estimates and separate unknown delayed charges. This is not a demand to invent actual billing.
* Decision route: Direct planner correction within the chosen allocation; increasing it would require a separately evidenced owner decision.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Use explicit partial-scope verification and timeout-zero gate flags

* Related IDs: P03-T01.
* Evidence: tools/rpi-checks.py:2157-2165 defaults receipt verification to full coverage; tools/rpi-checks.py:2190-2202 defaults lock timeout to 600 seconds. The plan's explicit --changed invocation supplies neither --lock-timeout 0 nor the later verifier's --required-scope partial.
* Concern: Prose says timeout-zero/scoped verification, but the actionable sequence can wait ten minutes for the lock and reject its valid partial receipt as insufficient full coverage.
* Impact: The user-selected gate cannot reliably run and verify as planned; pressure to mislabel or bypass a rejected partial receipt is avoidable.
* Smallest useful change: Supply a complete command sequence with --changed --lock-timeout 0 --base <reviewed-current-main-sha> --out <new-external-directory>, followed immediately before publication by --verify-receipt <external-receipt.json> --required-scope partial --base <current-origin-main-sha>. Do not wrap the runner in another flock. Require actual selection to remain appropriate for the tracking-only diff; unexpected full-matrix selection stops for scope reconciliation, not a bypass.
* Action owner: Planning parent.
* Exact resolving evidence: Correct commands in P03-T01, original immutable external receipt with partial scope and expected selected checks, and successful explicit partial verification bound to the exact clean candidate/base. A busy lock exits immediately.
* Decision route: Direct planner correction; scoped-gate authority is already explicit and does not require full-tier substitution.

<!-- rpi:critique id=PC-005 -->
### PC-005 [High]: Define the no-rewrite response to a moved main base

* Related IDs: P03-T01; latest-main direction.
* Evidence: The plan fixes base 885ee05fc45122cf7a1ea4f7f003dc88bfda08ee and says a moved base gets a fresh gate without rewriting history. tools/rpi-checks.py:151-166 requires both equality with current origin/main and that base to be an ancestor of candidate HEAD.
* Concern: Merely changing --base and re-running cannot satisfy ancestry if new main commits are not ancestors of this topic. Blind reconciliation can also turn a tracking-only PR into a different deployment/source candidate.
* Impact: Publication can become impossible or proceed against an unassessed source/base under the wrong gate scope.
* Smallest useful change: Fetch immediately before the gate, resolve current main and test ancestry. If it moved incompatibly, stop publication and record the precise source/base delta. Do not silently merge, rebase or force-push. Resume only through a permitted no-rewrite reconciliation with source/deployment identity, changed-path scope and new exact-head evidence re-evaluated. Keep the actual deployed source SHA distinct from the eventual evidence-PR base.
* Action owner: Planning parent.
* Exact resolving evidence: Fetch timestamp, resolved base/head/merge-base, either a passing ancestry check or explicit stopped-publication outcome. Any later authorized reconciliation requires a fresh committed candidate and fresh external receipt against that base.
* Decision route: Direct planner correction to add the stop branch. A future history-changing reconciliation, if needed, follows existing owner authorization boundaries; do not ask for it speculatively.

<!-- rpi:critique id=PC-006 -->
### PC-006 [High]: Distinguish the original Review from the final exact-head publication assessment

* Related IDs: P03-T01; independent review requirement.
* Evidence: The phase details put the one independent Review before commit/gate and then move directly from receipt verification to push. src/README.md, Local RPI gate, separately requires fresh verification immediately before independent exact-head review and push.
* Concern: The original Review cannot certify a later committed receipt-bound head/base or changes introduced while preparing publication. The candidate does not name this final assessment or require unresolved blocking findings to stop publication.
* Impact: An evidence PR can be published without independent assessment of the actual final candidate, despite preserving the original Review.
* Smallest useful change: Preserve the single original RPI Review unchanged; explicitly add the required bounded exact-head publication assessment after the final candidate commit and passing gate, with receipt verification immediately before that assessment and again immediately before push as needed. This is not a second plan critique or a repeated RPI Review loop. Require its assessed head/base to equal the pushed candidate and unresolved publication-blocking findings to stop publication.
* Action owner: Planning parent schedules; independent publication assessor owns the final assessment.
* Exact resolving evidence: Original Review retained, final assessment naming exact candidate SHA/base and verified receipt, recorded disposition of blockers, matching pushed head and no intervening invalidating change. Keep human/hosted approvals separately unresolved until actually supplied.
* Decision route: Direct planner correction; no new owner decision and no serial critique.

<!-- rpi:critique id=PC-007 -->
### PC-007 [High]: Validate the newly built resident image before deployment, outside the tracking-only gate

* Related IDs: P01-T01, P01-T02, P03-T01; research C1/C6.
* Evidence: src/api/Dockerfile.resident-demo performs apt-get update/upgrade during each build. tools/rpi-checks.py:335-342 omits image checks for Markdown/tracking-only changes. The supplied prior release changes distinguish source approval, image scanning and an ungated interim deployment.
* Concern: Merged-source CI and a later tracking-only --changed receipt do not establish the security/runtime properties of this newly built digest. The candidate records build/push success but defines no fresh image validation before replacing the resident revision.
* Impact: A different dependency/base-layer outcome can be deployed without checking the actual artifact; source approval can be incorrectly treated as image approval.
* Smallest useful change: Add existing applicable image validation and pinned Trivy policy checks for the exact built resident artifact before P01-T02, under timeout-zero heavy locking where required. Bind results to the pushed digest/local image identity and stop deployment on missing prerequisites or failures. Use no secret-bearing resident startup configuration or fabricated authenticated acceptance for these checks. Keep this artifact validation separate from the owner-authorized scoped evidence-PR gate.
* Action owner: Planning parent selects existing applicable contracts; deployment implementer executes.
* Exact resolving evidence: Exact-image scan report with scanner/database identity, policy/configuration and actual pass/failure; applicable non-secret image-contract results; registry digest linkage. No source/test additions or full-gate scope expansion is requested.
* Decision route: Direct planner correction using existing validation tools.

<!-- rpi:critique id=PC-008 -->
### PC-008 [Medium]: Define preservation comparison fields without capturing secret-bearing values

* Related IDs: P01-T01, P01-T02, P02-T02.
* Evidence: Phase details request sanitized app metadata, unchanged templates/configurations and resident runtime environment references while forbidding secret reads. Full template/configuration captures can contain inline environment values even without invoking listSecrets.
* Concern: The candidate does not identify a safe projection or the allowed resident deltas. A full capture followed by redaction reads values before redacting them; conversely, comparing entire resident templates literally must fail on the intended image/revision changes.
* Impact: Evidence gathering can violate the no-read boundary or either overclaim preservation or produce unresolvable false differences.
* Smallest useful change: Define management-plane query projections before capture: IDs, identities, image references, resource/replica settings, ingress, job trigger fields, SQL SKU and approved secret-reference names/URIs only; exclude secret values and unapproved inline environment values at retrieval. State allowed resident image/generated revision and temporary ingress deltas and require final expected traffic/revision identity. For employee settings that cannot safely be compared, record that limitation rather than reading or claiming preservation of hidden values.
* Action owner: Planning parent; deployment implementer captures the approved projection.
* Exact resolving evidence: Query/projection specification and sanitized before/after field-level comparisons covering all four apps, all eight Manual jobs, SQL Standard/10 DTU, resident min0/max1, identity/reference metadata and final ingress. State explicitly that these comparisons do not prove an employee interactive login.
* Decision route: Direct planner correction; no secret-access expansion.

## Strengths and Residual Risk

* The plan correctly rejects provision-only model spending, new grants without usable runtime wiring, password replacement, forged positive sessions and historical/local stand-ins for live authenticated acceptance.
* The deterministic merged deployment is an independently authorized, useful subset, not an unauthorized scope substitution. Its partial status must survive implementation, Review, PR wording and final reporting.
* Four existing apps and eight Manual jobs replace the outdated three-app assumption; image-only update and preserved expiry avoid unnecessary infrastructure changes.
* Credential-dependent sign-in, own-case isolation/features, real logout and natural session expiry remain UNMET. The current credential cannot be obtained within this task's no-read boundary.
* Model activation remains UNMET pending separately scoped host/managed-identity/ledger/tariff engineering and its approvals. The new USD20 ceiling is not evidence that the historical USD4 adapter contract has been redesigned.
* Unchanged employee metadata is a preservation observation, not evidence that employee login works. Human/hosted gates remain separate.
* No original adverse critique/Review outcome is to be overwritten. No finding authorizes extra committed source/tests, resource creation, issue closure, protection changes or broader permissions.

## Questions or Blocking Evidence Gaps

* No unresolved user choice prevents the planner from making these corrections or proceeding with an admitted safe subset.
* Missing credentials and missing model wiring block full requested acceptance, not this critique. Keep both as explicit UNMET requirements and owner/follow-up dependencies.
* Operational checks are future execution gates: failed cost admission, unresolved ACR/ingress restoration, image validation failure or an invalid publication identity must stop the affected operation. Do not infer success from the research summaries.

## Limitations

* No cloud operations, external prior-script/credential-file reads, source/test modifications, live browser sessions, image builds, scans, gates, commits or pushes were performed.
* W2-W5 inventory/cost/role assertions are supplied research, not independently refreshed readbacks. Runtime restoration and budget admission must use fresh sanitized execution evidence.
* This artifact assesses planning once. Resolving evidence listed above is a requirement for the parent/executor, not a claim that those future checks have run.

## Recommended Next Action

* Highest-impact finding: PC-001, failure-safe exact ACR restoration.
* Action owner: Planning parent.
* Smallest next action: Revise the ACR restoration procedure and the other seven findings in the existing plan/details, preserve this original Revise verdict, and finalize without another critique.
* User response required: No for these planner-owned corrections. Do not manufacture credential/model acceptance; record the remaining requested outcomes as UNMET.

| [.copilot-tracking/plans/2026-10-27/deploy-resident-474-plan.md](../../../plans/2026-10-27/deploy-resident-474-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-27/deploy-resident-474-phase-details.md](../../../details/2026-10-27/deploy-resident-474-phase-details.md) | Assessed operational phase details |
| [.copilot-tracking/research/2026-10-27/deploy-resident-474-research.md](../../../research/2026-10-27/deploy-resident-474-research.md) | Supplied deployment research and evidence pointers |
| [.copilot-tracking/reviews/plans/2026-10-27/deploy-resident-474-plan-critique.md](deploy-resident-474-plan-critique.md) | Original independent critique and complete PC-001 through PC-008 set |

## Next Steps

The active planning parent revises directly and finalizes; do not launch another critique. Begin P01 only after its applicable safety/admission corrections are incorporated. P03 remains conditional on its corrected exact-head publication sequence. No user action is required to revise or execute the independently authorized subset; full authenticated/model acceptance remains UNMET.
