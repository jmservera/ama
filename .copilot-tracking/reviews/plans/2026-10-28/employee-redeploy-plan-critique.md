---
title: Employee redeploy independent plan critique
description: Original one-pass final-candidate assessment for employee-redeploy-20261028
ms.date: 2026-10-28
---

## Metadata

* Task ID: employee-redeploy-20261028
* Critique date: 2026-10-28
* Plan: .copilot-tracking/plans/2026-10-28/employee-redeploy-plan.md
* Phase details: .copilot-tracking/details/2026-10-28/employee-redeploy-phase-details.md
* Research: .copilot-tracking/research/2026-10-28/employee-redeploy-research.md
* Critique execution status: Complete
* Assessment: exactly one independent final-candidate critique; original verdict retained here.
* Observed branch: ops/employee-redeploy-20261028
* Observed source HEAD: bb6df04cef68cc3694a97238d002c732c3406d81

## Inputs and Criterion Boundary

* Caller authority: one redeploy of ca-cutover-test-demo-api in ama after merged
  #514/#515/#516; existing model and role only. Set exactly AI_ENDPOINT to
  https://aif-cutover-test-rzsrg.openai.azure.com/ and both AI_DEPLOYMENT and
  AI_DEPLOYMENT_STRONG to standard. Preserve min zero and all unrelated state.
* Operational boundary: local source-image build, existing ACR with authorized
  temporary VM /32/export/public exception, exact original policy restoration,
  one new revision, verification or previous-revision rollback without another
  revision. No other workloads, roles, new Azure resources, inference, private
  data, secret values or .env access.
* Evidence boundary: supplied plan/details/research, directly referenced
  src/README.md, infra/README.md, tools/rpi-checks.py,
  src/api/Dockerfile, src/.dockerignore,
  src/api/src/zava_forward/api/server.py,
  src/api/src/zava_forward/api/__main__.py,
  src/api/src/zava_forward/api/web/index.html and the API container guidance.
  Repository-required project context was read in docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md and
  docs/reference/memory.md; memory is not evidence.
* Publication boundary: tracking-only commits, requested PR, original critique
  and independent Review retained, mandatory full clean exact-head local gate,
  current-main receipt verification and independent exact-head assessment.
  No test removals or additions; maximum additions zero.
* Assessment establishes planning credibility, not current Azure state,
  execution success, authenticated UX, model quality or human acceptance.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| Caller scope; C2/W1; P02-T01 | Covered | Exact three-variable additive update, explicit app/container, digest and min zero; no version-variable, model or role changes. |
| Preservation; W3/W4; P01-T01/P02-T01 | Covered | External reference-only baseline and full semantic comparison; current-state drift stops the write. |
| Image provenance and local regression; C3/C4; P01-T01 | Partial | Correct build context and actual HTTP requirement; executable synthetic startup/proof contract incomplete, PC-004. |
| Registry exception; W3/W4; P01-T02 | Partial | Correct original Disabled/Allow/export-disabled/None/empty-rule restoration and private-first cleanup; finite exception deadline missing, PC-005. |
| One revision and runtime verification; C4/W3; P02-T01 | Partial | GET-only convergence retries and honest protected assets; expected 401 plus no logs can leave actual startup unobserved, PC-002. |
| Recovery and unrelated configuration; Q3; P02-T02 | Partial | Old revision/digest identified; unproven Single-mode recovery and unresolved mode/traffic divergence, PC-001. |
| Azure readiness; P01-T02/P02-T01 | Missing | Current all-in headroom and finite costed execution precondition absent, PC-003. |
| Publication; C1; P03-T01/P03-T02 | Covered | Original Review, committed candidate, full gate, nonqueued admission, receipt verification, independent exact-head assessment; failure blocks publication. |
| Test ownership and protected acceptance | Covered | Zero additions/removals, semantic equality and existing image/probe/log evidence; no invented session, inference or acceptance. |

## Verdict

* Verdict: Revise
* Severity summary: 3 High, 2 Medium, 0 Critical, 0 Low.
* Rationale: scope and publication controls are credible, but the candidate
  permits an unresolved rollback configuration change and can overstate runtime
  verification without observed startup. Required cost readiness and finite
  operational/proof details also need explicit preconditions. These are planning
  corrections, not authority to expand the redeploy.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Recovery can leave an unauthorized revision-mode and traffic divergence

* Related IDs: preservation requirement; Q3; P02-T02.
* Evidence: .copilot-tracking/details/2026-10-28/employee-redeploy-phase-details.md,
  P02-T02, permits switching Single to multiple, routing old traffic and
  deactivating the new revision, then merely reporting mode divergence.
  .copilot-tracking/research/2026-10-28/employee-redeploy-research.md, W3/Q3,
  reports Single mode but provides no demonstrated recovery sequence preserving
  that mode. Caller requires unrelated configuration preservation and no second
  revision.
* Concern: disclosing a persistent mode/traffic change does not authorize it.
  The plan neither establishes that previous-revision activation works in the
  observed mode nor provides a supported sequence restoring original mode and
  traffic while keeping the old revision serving without another revision.
* Impact: a failed rollout can strand the app outside its authorized
  configuration or leave recovery unproven precisely when it is needed.
* Smallest useful change: make a supported, bounded, no-new-revision recovery
  sequence a pre-rollout prerequisite. Remove automatic permission to leave
  multiple mode behind. Specify baseline-mode/traffic readbacks and recovery
  stop conditions. If no compliant route can be established, block the app
  mutation rather than improvise.
* Action owner: planning parent; operator supplies bounded read-only recovery
  evidence before mutation.
* Exact resolving evidence: revised P02-T02 names the supported sequence and
  its authority/evidence, shows how original mode and effective traffic are
  restored to the old revision/digest, and requires revision-set comparison
  proving no additional revision. Alternatively it explicitly blocks rollout
  pending the unresolved recovery prerequisite.
* Decision route: direct planner correction to fail closed. Only if the
  selected recovery necessarily retains changed mode/traffic is that a
  significant/divergent user decision; current authority does not grant that
  exception.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Expected authentication challenges can mask an unobserved startup

* Related IDs: runtime acceptance criteria; C4/W3; P02-T01.
* Evidence: plan accepts Healthy, expected HTTP 401 and no startup error in
  bounded logs. Research reports the old revision as Healthy/ScaledToZero.
  src/api/src/zava_forward/api/server.py:220-223 makes application health
  contingent on store readiness, while protected routing is separately handled
  at src/api/src/zava_forward/api/server.py:239-243.
* Concern: an authentication-layer challenge need not demonstrate that the
  target revision started or that its application health ran. With min zero,
  no new-revision console entries may mean no observed startup, not zero
  startup errors. The candidate does not require positive, revision-specific
  startup/readiness evidence before declaring a healthy rollout.
* Impact: an image or store initialization defect can escape verification
  while the evidence is summarized as successful runtime health.
* Smallest useful change: define positive, timestamped new-revision platform
  readiness/startup evidence and a bounded observation rule, including replica
  or probe evidence when available without extra mutation or private-data
  access. Keep 401/302 expected and keep protected assets explicitly residual.
  If startup cannot be observed within authority, record runtime verification
  as unverified/blocked, not passed, with an explicit disposition. Absence of
  logs alone must not satisfy startup acceptance.
* Action owner: planning parent.
* Exact resolving evidence: revised P02-T01 distinguishes auth, platform and
  application observations, identifies required revision/time-bound positive
  fields, and defines timeout/failure/unobserved outcomes. Implementation
  evidence later records those readbacks or the honest unmet criterion.
* Decision route: direct planner correction; no new session, auth weakening,
  inference, private-data inspection or scale change is authorized.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Azure execution lacks the required current cost-readiness precondition

* Related IDs: P01-T02; P02-T01; operational dependencies.
* Evidence: src/README.md:179-192 requires complete all-in cost headroom and
  finite commands, budget, time window and stop conditions before Azure-only
  work; unknown/partial evidence blocks Azure-dependent work.
  docs/case_study_48_addendum.md:591-611 records all-in headroom as
  Unknown/Blocked and names the missing sanitized cost evidence.
  infra/README.md, Small employee model prerequisite, records USD30 additional
  employee AI authority through 2026-10-31, not complete all-in headroom.
  Supplied plan/research contains no refreshed cost prerequisite.
* Concern: explicit fresh redeploy authority resolves permission for this
  operation; it does not itself establish the separate documented all-in
  headroom condition. No inference and min zero reduce exposure but do not
  prove zero incremental registry, revision or hosting liability.
* Impact: the planner can begin cloud writes while a standing financial
  readiness condition remains unsupported.
* Smallest useful change: add a pre-cloud-write gate for current sanitized
  headroom evidence, a bounded incremental redeploy estimate, execution window
  and financial stop condition. Continue independent local preparation while
  missing evidence blocks cloud actions; do not broaden cost-read roles or
  infer missing amounts as zero.
* Action owner: planning parent records the gate; owner/coordinator supplies
  existing authorized sanitized financial evidence.
* Exact resolving evidence: a dated evidence pointer covering accrued and
  remaining attributable liabilities, scope/currency/lag/exclusions, approved
  reserve and the bounded redeploy exposure, or an explicit blocked
  P01-T02/P02-T01 dependency until that evidence is supplied.
* Decision route: direct planner correction to enforce the existing condition.
  A new budget exception would require a significant user decision, but the
  plan need not request one to record the blocker.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: The built-image HTTP proof lacks a runnable synthetic startup contract

* Related IDs: C3/C4; P01-T01; local asset acceptance; locked test ownership.
* Evidence: phase details require the built image with synthetic empty data,
  but name no fixture schema, mount, state setup, loopback binding or startup
  checks. src/api/Dockerfile supplies no seed data, runs as UID10001 and expects
  /data/zavaforward.json and writable /state.
  src/api/src/zava_forward/api/server.py:1067-1083 opens the store before serving
  and exits when the dataset is missing. The required script order is visible
  in src/api/src/zava_forward/api/web/index.html:35-41.
* Concern: an unspecified empty dataset is not a demonstrated valid startup
  fixture. The plan also does not bind the locally served HTTP result to the
  exact image subsequently pushed or state the concrete order assertion.
  A source-file check or extracted layer alone would not meet caller acceptance.
* Impact: the mandatory local regression proof can fail for fixture reasons or
  be replaced inadvertently by a weaker static assertion.
* Smallest useful change: specify an existing valid constructed-fixture recipe,
  explicit isolated data/state mounts and UID permissions, loopback-only
  ephemeral container, readiness timeout, HTTP requests to /app, /ops.js and
  /app.js, ordered script-element assertion, and exact owned-container cleanup.
  Bind the run to the built image ID and subsequently pushed manifest digest.
  Use runtime evidence only, not a new tracked test.
* Action owner: planning parent.
* Exact resolving evidence: executable bounded commands in P01-T01 using only
  constructed local data, plus a required evidence record containing image
  identity, successful HTTP statuses, response hashes and the asserted
  ops.js-before-app.js positions. No credential or response body is committed.
* Decision route: direct planner correction; test additions remain zero and
  live protected UX remains a disclosed residual.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: The temporary registry exception has no concrete maximum duration

* Related IDs: bounded-command requirement; P01-T02.
* Evidence: the plan promises bounded command timeouts, but phase details
  provide only the ten-minute revision convergence limit in P02-T01.
  P01-T02 specifies finally restoration without concrete login, push,
  digest-readback or overall public/export-exception deadlines.
* Concern: a hung token/login/push/readback can indefinitely postpone the
  finally block while the otherwise correctly restricted exception remains
  active.
* Impact: temporary access can outlive the intended finite operational window
  and prevent timely exact policy restoration.
* Smallest useful change: specify per-operation and total exception time
  bounds, guaranteed cleanup on handled timeout/error/interruption, bounded
  restoration readback, and the precise blocked/escalation outcome if cleanup
  cannot be confirmed. Preserve the existing private-first cleanup and
  original Disabled/Allow/export-disabled/None/empty-rule policy.
* Action owner: planning parent.
* Exact resolving evidence: revised P01-T02 lists concrete deadlines and cleanup
  control flow; operation evidence later records exception start/end,
  restoration equality and any unconfirmed recovery, without token output.
* Decision route: direct planner correction; no broader route, extra IP,
  resource, role or policy normalization is needed.

## Strengths and Residual Risk

* Additive explicit-container update preserves the caller's exact three
  settings; model-version variables and existing model/role changes are
  correctly excluded despite broader historical handover advice.
* Baseline comparisons, digest pinning, one update with no blind retry and
  exact ACR policy restoration are strong safeguards.
* Full exact-head gate and publication failure handling are correctly retained;
  no historical exception, changed-path shortcut or hosted-check substitute is
  proposed. Gate failure is correctly separate from runtime rollback.
* Authenticated live assets, employee UX, task-release/model bindings and
  inference remain explicitly unaccepted. These disclosed boundaries are not
  findings demanding expanded authorization.
* Zero test additions/removals is compatible with existing gate execution and
  operational semantic/image/probe/log evidence.

## Questions or Blocking Evidence Gaps

* Establish a compliant Single-mode recovery route before rollout, or block the
  mutation. Do not resolve the gap by unapproved persistent mode divergence.
* Current cost readiness is not established by supplied evidence; record its
  prerequisite rather than performing additional Azure research in this
  critique.
* No immediate user choice is required to correct the plan conservatively.
  A material exception would need separate explicit authority.

## Limitations

* No Azure calls, Docker build, runtime probe, full gate, secret/.env access,
  private-data access, implementation or delegated review was performed.
* W1-W4 are supplied research assertions, not independently refreshed live
  readbacks; no claim is made about present infrastructure or remote PR state.
* Git inspection confirmed the named branch/HEAD and existing untracked
  planning/state inputs. They were not changed, moved, staged or committed.
* This is the complete actionable finding set for this supplied boundary, not
  a general infrastructure, UI, security or source audit.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: revise P02-T02 to establish compliant recovery or make
  rollout blocked, then disposition PC-002 through PC-005 in the plan/details.
* User response required: no for planner-owned corrections; only a newly
  proposed significant exception would require a user decision.
* Preserve this original Revise verdict and findings; do not repeat critique.

## Artifacts

| Artifact | Description |
|---|---|
| [.copilot-tracking/plans/2026-10-28/employee-redeploy-plan.md](../../../plans/2026-10-28/employee-redeploy-plan.md) | Assessed final-candidate plan; unchanged. |
| [.copilot-tracking/details/2026-10-28/employee-redeploy-phase-details.md](../../../details/2026-10-28/employee-redeploy-phase-details.md) | Assessed task details; unchanged. |
| [.copilot-tracking/research/2026-10-28/employee-redeploy-research.md](../../../research/2026-10-28/employee-redeploy-research.md) | Supplied evidence and decisions; unchanged. |
| [.copilot-tracking/reviews/plans/2026-10-28/employee-redeploy-plan-critique.md](employee-redeploy-plan-critique.md) | Original Complete / Revise critique. |

## Next Steps

Planning parent: directly correct and disposition PC-001 through PC-005,
retaining this original assessment. Do not dispatch another critique. Keep
cloud execution blocked wherever recovery or cost prerequisites remain unmet;
keep publication blocked until the complete exact-head gate and independent
assessment pass. No user action is required for conservative plan correction.
