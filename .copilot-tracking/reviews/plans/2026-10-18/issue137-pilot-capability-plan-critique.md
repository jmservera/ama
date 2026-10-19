<!-- markdownlint-disable-file -->
# RPI Plan Critique: issue137-pilot-capability

## Metadata

* Task ID: 137.
* Critique date: 2026-10-18.
* Plan: .copilot-tracking/plans/2026-10-18/issue137-pilot-capability-plan.md
* Phase details: .copilot-tracking/details/2026-10-18/issue137-pilot-capability-phase-details.md
* Research: .copilot-tracking/research/2026-10-18/issue137-pilot-capability-research.md
* Critique execution status: Complete.
* Execution: one independent final-candidate plan critique; rpi-plan-critique activated. No agents, live queries, implementation or original Review.

## Inputs and Criterion Boundary

* Assessed the three supplied artifacts in full, including Q1-Q3, W1-W2,
  C1-C4, R1-R17, P01-P03 and their tasks, dependencies and acceptance criteria.
* Caller direction establishes that the owner comment at
  https://github.com/jmservera/ama/issues/137#issuecomment-6192754703
  selects only pilot uksouth and subscription owner @jmservera. It does not
  approve SQL region, subscription binding, sizing, zone redundancy, cost,
  deployment or access. No independent GitHub verification was performed here.
* Source consulted: infra/main.bicep; infra/modules/containerapps.bicep;
  infra/modules/sql.bicep; infra/modules/iothub.bicep;
  infra/modules/foundry.bicep; infra/modules/storage.bicep;
  infra/modules/registry.bicep; infra/README.md, Environments;
  docs/adrs/0002-pilot-readiness-architecture.md, Implementation status.
  Repository-required case-study and reference entry-point/context reads did
  not supply new operational approval.
* Existing topic branch is docs/pilot-region-quota-evidence-137. Initial
  status showed the supplied research, plan, details and session-state files
  as untracked. They were neither changed nor staged by this critique.
* Boundary: credibility of a documentation-only implementation and delivery
  plan for dated 2026-10-18 management GET evidence. This does not certify
  Azure results, private account identity, subscription authorization,
  deployment viability, reviewed-reference contents or issue acceptance.
* Constraints assessed: all parameter examples and templates unchanged;
  no false reviewed tokens; issue remains open with its remaining criterion
  unticked; at most two distinct missing-surface approaches; adverse receipts
  and all RPI artifacts retained and committed; privacy-safe commit and draft
  PR with Refs #137; zero test additions/deletions and unrelated suites N/A.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Q1, W1-W2, C1-C4: authority and source reconciliation | Partial | Plan correctly limits the owner decision and forbids example edits; ADR task must distinguish historical snapshot from current delta, PC-002. |
| Q2, R1-R17: dated support and unavailable surfaces | Covered | All receipt IDs retained; empty collections, AuthorizationFailed and Bad Gateway remain adverse or unknown, not zero quota or support. |
| Q3: approval and deployment boundary | Covered | No subscription authorization, service admission, quota reservation, human review, sizing or deployment acceptance is inferred. |
| P01-T01: exact configuration | Covered | Main and service modules establish internal VNet Consumption environment, SQL GP_S_Gen5 at 2 max vCores with serverless properties, IoT B1/one unit, AIServices S0 and both exact OpenAI model/version/GlobalStandard/capacity-30 requests, StorageV2 LRS/ZRS branch and Premium registry. Requested settings remain distinct from owner decisions. |
| P01-T01: scope, metrics and units | Covered | R2 counts and profile resources are not environment-core quota; model families are separate; inference usageNames distinguish fine-tuning entries; returned capacity fields/rate counts do not authorize unit conversion. |
| P01-T01: SQL and zone claims | Covered | SQL uksouth is a candidate catalog check, not selected SQL location; zoneRedundant support does not resolve empty supportedZones, pinning or admission. No optional zone setting is approved. |
| P01-T01: unchanged examples and reviewed references | Covered | Explain stale example comments in prose only; leave placeholders and gates intact. A nonempty string is not a human-reviewed record. |
| P02-T01: reproducibility and configuration binding | Covered | R1-R17 command shapes, API versions where REST is used, date, scoped observations, unchanged-base hashes and identical bounded reruns are planned; private same-account comparison must not be presented as approved-pilot binding. |
| P02-T01: preservation and query budget | Covered | Preserve initial adverse receipts separately from reruns. Repeating an identical command does not add a distinct approach; no new endpoint, API-version fallback or permission change is authorized. Unknowns are valid final outcomes. |
| P02-T01, P03-T01: sanitization and full delivery scope | Partial | Pre-Review staged-content inspection does not cover artifacts generated or staged later, PC-001. |
| P02-T01: change and test budget | Covered | Documentation/source-hash/link/diff checks are appropriate; test additions 0, deletions 0; application/SQL/Docker suites N/A. No new tooling or tests required. |
| P03-T01: one original Review and delivery | Covered with PC-001 correction | Preserve original verdict, route findings forward without correction or second Review; include all RPI artifacts/state, use privacy-safe email/trailer, push only topic branch and create draft PR to main with Refs #137. |
| Dependencies and residual blockers | Covered | GET/branch access can fail without authorizing access changes. Missing capability, quota, account approval and named review block readiness claims, not honest documentation delivery. |

## Verdict

* Verdict: Revise.
* Severity summary: Critical 0; High 0; Medium 2; Low 0.
* The evidence and authority boundaries are credible. Two bounded planning
  corrections are needed to preserve historical provenance and ensure the
  privacy check covers the actual final commit contents. Neither finding
  requests further research, infrastructure work or a changed test budget.
* This is the complete actionable finding set for the supplied boundary.
  The planning parent should resolve it directly and finalize without another
  critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Final delivery artifacts fall after the explicit sanitization gate

* Related IDs: P02-T01, P03-T01; acceptance criteria for sanitized delivery and
  inclusion of every RPI artifact; non-functional allowlist requirement.
* Evidence: .copilot-tracking/details/2026-10-18/issue137-pilot-capability-phase-details.md,
  P02-T01 instructs inspection of staged content for identifiers and secret
  fields. P03-T01 subsequently generates the original Review, resolves commit
  identity and explicitly stages documentation plus all RPI categories/state.
  The plan assigns sanitization to P02, before those later artifacts exist in
  their final staged form.
* Concern: The explicit check can inspect an incomplete or empty index and
  cannot establish that the later original Review, state, changes record and
  other staged artifacts satisfy the publication allowlist. "No private
  scratch" is necessary but does not cover an accidental sensitive value in
  an otherwise authorized artifact.
* Impact: The committed/pushed evidence set could contain private identifiers
  or raw response material despite a recorded successful P02 privacy check.
* Smallest useful change: Retain P02 content checks, but add an explicit
  P03 pre-commit gate after original Review generation and final explicit
  staging: inventory every staged path, inspect the complete staged additions
  and full contents of newly added artifacts, check the allowlist and
  identifier/secret exclusions, and inspect the outgoing PR text. Permit
  documented public handles, commit/source digests and required privacy-safe
  attribution rather than treating every email-like string as a leak.
  A failure stops commit/push and routes to the coordinator; it does not
  authorize changing the original Review or starting another Review.
* Action owner: Planning parent; implementation parent executes the gate.
* Exact resolving evidence: Revised P03-T01 in both plan and details places
  this gate after generation/staging and before commit/push; its completion
  evidence records the final staged-path inventory and sanitization result
  for that same staged tree, including original Review and session state.
  Any later staged-content change invalidates the gate. Delivery records a
  sanitized draft PR body without exposing rejected content.
* Decision route: Direct planner correction. Existing privacy and immutable
  Review requirements already resolve the policy; no significant or divergent
  user decision and no additional Review are required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: ADR reconciliation needs an explicit dated-delta instruction

* Related IDs: C4, P01-T01; historical-receipt preservation requirement.
* Evidence: docs/adrs/0002-pilot-readiness-architecture.md:878-880 explicitly
  labels its implementation table a historical 2026-10-08 snapshot with
  2026-10-09 updates. Its row at line 898 records pilot region as undecided
  at that time. A separate Current Exercise Delivery Delta begins at line
  900. Research C4 calls the implementation status outdated; the plan calls
  for "ADR 0002 current implementation status" and "ADR current-status
  correction"; phase details say W1 contradicts ADR implementation status,
  while also requiring historical material to remain intact.
* Concern: The later 2026-10-15 owner comment does not contradict a correctly
  dated 2026-10-08/09 historical snapshot. The task does not explicitly say
  where the new status belongs, leaving a plausible implementation that
  replaces a historically accurate undecided statement or presents the later
  decision as true at the earlier date.
* Impact: A current-status correction could destroy decision chronology or
  overstate what the historical deployment evidence established.
* Smallest useful change: Specify a 2026-10-18 current-status delta adjacent
  to the existing later-evidence material, leaving the historical snapshot
  and its rows unchanged. State the 2026-10-15 decision date separately from
  the 2026-10-18 evidence retrieval date; limit selection to pilot uksouth and
  @jmservera ownership, with SQL region and operational approval still open.
  Correct genuinely current unsupported supersession prose in infra/README.md
  without projecting that correction backward into historical ADR rows.
* Action owner: Planning parent; implementation parent authors the delta.
* Exact resolving evidence: P01-T01 in plan and details explicitly requires
  the dated delta and unchanged historical table; implementation diff later
  shows no edits to the 2026-10-08/09 snapshot or historical receipts, and
  the new delta separates decision/retrieval dates and unresolved approvals.
* Decision route: Direct planner correction. The supplied decision and
  history-preservation instruction already determine the outcome; no
  significant or divergent user decision is needed.

## Strengths and Residual Risk

* R1-R17 deliberately preserve unsuccessful and empty results. Authorization
  failure is not a reason to grant access, and empty usage is not zero quota.
* SQL zoneRedundant=true in a catalog is not SQL-region selection, named-zone
  availability or server admission. Storage support must remain filtered by
  StorageV2 kind and exact redundancy SKU.
* Container Apps ManagedEnvironmentCount and Consumption profile cores/memory
  do not prove available managed-environment Consumption cores. No environment
  enumeration is needed to turn that intended unknown into a guessed result.
* AIServices S0, OpenAI format, exact versions and inference usageNames matter.
  Model maxCapacity=3, SKU maximum=1000000, requested capacity=30 and returned
  rate-limit counts have no established common unit here. Do not sum model
  families, infer TPM/RPM or declare capacity Pass.
* Same-account private comparison can support rerun consistency only. It
  cannot establish that the queried subscription is the authorized pilot
  subscription. Public evidence should continue to say this binding is
  unproven, even when all query invocations use the same private identifier.
* Source hashes bind observations to checked source, not to a completed pilot
  parameter set. All examples remain byte-identical and unapproved choices
  remain unselected.
* Provider regional listings do not establish exact IoT B1/one-unit or Premium
  registry support. Key Vault, networking, identity, monitoring and optional
  edge are not newly verified by these receipts.
* Full region/quota readiness and named human review remain incomplete. This
  delivery must neither populate reviewed-reference tokens nor close the
  issue or tick its remaining criterion.

## Questions or Blocking Evidence Gaps

* No user question is required for these two findings.
* Missing quotas, zone evidence, exact IoT/registry support and approved
  subscription binding are already explicit outcomes. Do not spend additional
  approaches or treat their absence as a blocker to accurate documentation.
* Private first-run receipts and account-comparison evidence were not supplied
  for inspection. Their preservation and local reproducibility remain
  implementation obligations, not independently verified facts of this
  critique.

## Limitations

* No Azure, gh or other remote queries were made. The supplied sanitized
  research is the sole basis for live-service outcomes and comment contents.
* No private data or account material was inspected; no raw-response
  authenticity or future quota stability is certified.
* No source, example, research, plan, details, state or original Review was
  changed. The only write is this caller-specified critique artifact.
* No tests were added, deleted or run. This read-only planning assessment
  does not change the locked documentation-only validation budget.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Clarify the final staged-tree privacy gate and dated
  ADR delta in the existing plan/details, record disposition of both findings,
  then finalize and continue the parent-owned implementation.
* User response required: No. Neither correction changes approved scope.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-18/issue137-pilot-capability-research.md](.copilot-tracking/research/2026-10-18/issue137-pilot-capability-research.md) | Supplied source and sanitized management evidence |
| [.copilot-tracking/plans/2026-10-18/issue137-pilot-capability-plan.md](.copilot-tracking/plans/2026-10-18/issue137-pilot-capability-plan.md) | Final-candidate plan assessed |
| [.copilot-tracking/details/2026-10-18/issue137-pilot-capability-phase-details.md](.copilot-tracking/details/2026-10-18/issue137-pilot-capability-phase-details.md) | Phase and validation sequence assessed |
| [.copilot-tracking/reviews/plans/2026-10-18/issue137-pilot-capability-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-18/issue137-pilot-capability-plan-critique.md) | Complete independent critique and finding set |

## Next Steps

The active planning parent resolves PC-001 and PC-002 directly, records their
disposition and finalizes without a second critique. Parent owns implementation,
the one original Review and delivery. No user action is required.
