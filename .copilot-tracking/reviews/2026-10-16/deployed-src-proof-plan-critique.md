---
title: Deployed src proof final-candidate plan critique
description: Bounded independent critique for issues 200 and 201
ms.date: 2026-10-16
---

## Metadata

* Task ID: issues-200-201-deployed-src-proof
* Critique date: 2026-10-16
* Plan: .copilot-tracking/plans/2026-10-16/deployed-src-proof-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/deployed-src-proof-phase-details.md
* Critique execution status: Complete
* Assessment: exactly one bounded final-candidate critique; no further agents.

## Inputs and Criterion Boundary

* Caller direction: deployed proof for #200/#201; changes only within ama;
  preserve private workloads and budget; SQL public access Disabled throughout;
  no firewall writes, policy/tag bypass, peering, tenant mutation, local Docker,
  or legacy-directory changes. SQL and private HTTP data-plane probes run only
  from jobs/apps within the ama VNet; remote ACR Tasks build images.
* Primary evidence: the plan and details above and
  .copilot-tracking/research/2026-10-16/deployed-src-proof-research.md.
* Bounded corroboration: infra/main.bicep, infra/main.bicepparam,
  infra/modules/containerapps.bicep, infra/modules/network.bicep,
  infra/modules/registry.bicep, infra/modules/sql.bicep,
  infra/scripts/deploy.py, relevant infra/README.md guidance,
  src/api/Dockerfile, src/api/src/zava_forward/api/auth.py,
  src/api/src/zava_forward/api/server.py,
  src/core/src/zava_forward/core/sqlstore.py and
  src/core/src/zava_forward/core/mssqlstore.py.
* Context: docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md,
  docs/reference/memory.md, docs/adrs/0006-src-layout-and-cutover.md
  and docs/architecture/cutover-evidence-pack.md.
* Acceptance boundary: infrastructure/image/SQL persistence proof with separately
  reported runtime outcomes, not continuing-stock, staff, browser, inference,
  product acceptance, owner approval or retirement authorization.
* Branch inspected read-only: feat/deployed-from-src-proof-200, tracking
  origin/main. Existing untracked planning inputs were left unchanged.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| AMA-only changes, retained budget, no tenant mutation | Covered | Incremental what-if and scope rejection are explicit; preserve current inputs rather than use placeholder parameter values |
| C1/C2; P01-T01 | Covered | Development AND explicit public switch fixes the defect; checked dev parameter file explicitly sets true, so that file's existing default remains public |
| C3; P01-T03 | Partial | Secretless bearer validation is a credible alternative, not inherently a tenant-change blocker; PC-005 adds its acceptance conditions |
| C4; P01-T02; P02-T02 | Partial | Synthetic proof is properly distinguished from continuing-stock acceptance; PC-002 and PC-004 address preflight and proof integrity |
| C5; staff and authorized HTTP limits | Covered | No roster or Graph access is assumed; no managed identity becomes a human |
| W1/W2; P02-T01/P02-T02 dependency | Partial | No existing environment is reported and bootstrap suppresses its creation; PC-001 |
| P02-T02 SQL identity and grants | Partial | Correct direction but missing executable identity/permission contract; PC-003 |
| P02-T01 registry transition | Partial | Build-before-isolation is correct; private rebuild/recovery and wrapper lookup constraints require PC-006 |
| P02-T03 deployed and restart outcomes | Partial | Honest blockers and skeleton limits are explicit; application persistence must not be inferred from an unrelated SQL marker |
| P03-T01/P03-T02 | Covered | Preserve historical failures, sanitize identifiers, retain owner gates, run existing infra tests and review once |

## Verdict

* Verdict: Revise
* Severity summary: 3 High, 3 Medium, 0 Critical, 0 Low.
* Rationale: the approach respects the owner's boundaries and can be implemented
  without tenant mutation, but its current execution graph cannot create the
  initialization job at the specified point. Data-preservation, SQL grants and
  probe semantics also need concrete gates before deployment. These are direct
  planner corrections, not reasons to request public SQL or broader authority.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Initialization depends on an environment that bootstrap does not create

* Related IDs: W1, P02-T01, P02-T02, P02-T03.
* Evidence: research reports no Container Apps environment. P02-T01 sets
  deployApplications=false. In infra/main.bicep this suppresses the complete
  apps module; infra/modules/containerapps.bicep owns environmentResource and
  its private environment DNS. P02-T02 requires a job in that environment before
  P02-T03 deploys the module.
* Concern: the details do not identify a step that creates the environment and
  DNS before the initializer. Deploying API workloads first instead risks
  starting them against uninitialized SQL.
* Impact: the planned private initialization cannot execute in order; improvised
  fixes could create a conflicting environment or premature application startup.
* Smallest useful change: explicitly stage environment/DNS creation separately
  from workload creation, with a single declarative owner and identical names,
  subnet and configuration across subsequent deployments. Add the initializer
  only after that environment is ready; enable applications after seeding.
  Do not use a placeholder app to work around the dependency.
* Action owner: planning parent, then infrastructure implementer.
* Exact resolving evidence: revised dependency sequence and named template
  inputs/resources; compiled environment-only configuration and scoped what-if;
  runtime environment readiness, delegated ama subnet and private DNS evidence
  preceding initializer execution.
* Decision route: direct planner correction. No user decision required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: The populated-database refusal must precede Store construction and writes

* Related IDs: C4, P01-T02, P02-T02; private-data preservation.
* Evidence: phase details say to refuse an unexpected populated database.
  SqlStore.__init__ in src/core/src/zava_forward/core/sqlstore.py calls schema
  creation, migrations and index creation before _seed, then loads state.
  MssqlStore delegates to that constructor and can create ledger tables.
* Concern: using the installed Store as the inspection mechanism would already
  mutate an unexpected workload and load case/staff data before refusal.
  The plan does not specify a pre-Store guard or recognized-run ownership test.
* Impact: the intended safety check could violate both no-dataset-read and
  no-private-workload-change constraints, even if execution subsequently stops.
* Smallest useful change: define a read-only connection preflight using system
  metadata and a narrowly scoped proof-ownership sentinel. Unknown application
  tables/state must cause refusal without constructing Store or selecting
  case/staff bodies. Permit only a new empty target or an explicitly recognized
  proof target. Do not delete, reseed or repurpose an unexpected target.
* Action owner: planning parent and proof-runner implementer.
* Exact resolving evidence: unit tests assert zero DDL, DML, Store construction
  or dataset queries before rejection; explicit empty/recognized/unknown
  branches; sanitized in-VNet preflight outcome recorded before initialization.
* Decision route: direct planner correction. An unexpected retained workload
  blocks that execution path; selecting a materially different target would
  require separate authority, not an automatic workaround.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: SQL identity selection and runtime grants are underspecified

* Related IDs: P01-T02, P02-T02, P02-T03.
* Evidence: infra/modules/sql.bicep accepts an Application administrator SID.
  Phase details propose a dedicated initializer MI and known-client-SID
  contained users. MssqlStore uses ZF_SQL_CLIENT_ID for MSI selection, while
  its startup executes schema/index/migration operations and sp_getapplock.
* Concern: naming contained users alone does not grant sufficient runtime
  permissions. Conversely, making API/import server administrators to get a
  green probe would defeat identity separation. Administrator object identity,
  contained application SID and MSI client selection are different inputs;
  their binding and the identity used for each probe are not defined.
* Impact: initialization can succeed under the powerful identity while the API
  fails on startup, or a probe can accidentally prove only administrator access.
* Smallest useful change: specify administrator Application principal/object
  binding, explicit user-assigned MSI selection and Graph-free contained-user
  SID conversion/type. Define idempotent grants compatible with actual startup,
  including schema/index/migration and locking needs where required. State
  intended steady-state administrator disposition without silently replacing
  another administrator on later redeployment. Run app SQL probes under the
  app's identity, attached to the in-VNet job if necessary, not the initializer.
* Action owner: planning parent and SQL/infrastructure implementer.
* Exact resolving evidence: documented identity-to-operation/grant matrix;
  idempotence and SID conversion tests; sanitized in-VNet results for
  initializer connection, contained-user/grant checks, and API identity
  MssqlStore startup and post-restart read. Import capabilities remain bounded
  to what its actual CLI can demonstrate.
* Decision route: direct planner correction within the requested dedicated-MI
  design. Permission failure is a blocker, not authority to add tenant roles.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: A generic SQL marker does not establish application persistence

* Related IDs: C4, P01-T02, P02-T03; restart-persistence acceptance.
* Evidence: src/api/Dockerfile contains no dataset and points ZF_DATA to an
  unpopulated /data path. SqlStore._seed opens that file whenever cases is
  empty; otherwise it skips file loading. Phase details promise a tiny fixture
  and a marker, then SQL-marker and health checks after restart.
* Concern: an empty fixture or marker in an unrelated table can survive while
  API startup still needs a missing seed. Reading a marker as the initializer
  plus receiving /healthz is not evidence that the runtime identity reloaded
  retained application state.
* Impact: a persistence pass could overstate what was demonstrated.
* Smallest useful change: use a valid, nonempty, explicitly labelled fictional
  case fixture with no human binding or privileges; define its contract and a
  unique application-state marker. After initialization, start/restart without
  the seed available and without another seed operation. Verify the same
  recognized synthetic state through MssqlStore under API MI in the VNet.
  Keep authorized HTTP/staff acceptance separately Blocked or Not run.
* Action owner: planning parent and proof-runner implementer.
* Exact resolving evidence: fixture-contract and empty-fixture tests; pre/post
  marker equality and source/image digests; old/new serving instance or restart
  evidence; post-restart app-identity Store read with no seed and no reseeding.
* Decision route: direct planner correction; synthetic infrastructure proof
  does not require permission to inspect continuing private data.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Bearer-only mode needs explicit fail-closed and regression probes

* Related IDs: C3, P01-T03, P02-T03.
* Evidence: existing authConfigs sets RedirectToLoginPage and always references
  entra-client-secret; trusted-proxy authorization separately requires one
  mapped role and a matching staff oid. The candidate proposes opt-in
  bearer-only mode with issuer/audience validation and 401 denial.
* Concern: absence of a client secret does not inherently block inbound bearer
  validation; the secret supports interactive login/token acquisition. However,
  absence of Graph enumeration cannot justify guessing a registration or
  audience. A no-token 401 alone does not prove bad tokens or forged proxy
  headers are rejected.
* Impact: either a safe deployment route is needlessly blocked, or the new mode
  is treated as secure without testing its important differences.
* Smallest useful change: retain the alternative, explicitly omit the secret
  reference and browser/token-store dependencies in bearer mode, require a
  nonempty audience from an identified existing configuration, and configure
  Return401 with tenant-specific issuer/audience validation. Preserve browser
  mode unchanged. Add tests for missing audience, secret omission, malformed
  token, wrong issuer/audience configuration, forged principal headers and
  unchanged browser behavior. Perform feasible live negative ingress probes
  without logging tokens; token-validation acceptance beyond those probes
  remains unverified if no suitable token is available.
* Action owner: planning parent and authentication implementer.
* Exact resolving evidence: compiled auth-mode matrix; provenance category for
  existing audience without publishing identifiers; actual no-token,
  malformed-token and forged-header denial over private ingress, plus health
  200. Record other token probes as Blocked/Not run when prerequisites are
  absent. A denied MI token is not a human or authorized HTTP pass.
* Decision route: direct planner correction. No tenant mutation or new owner
  decision is necessary to try this route; missing audience blocks only the
  affected authenticated application path.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Registry isolation must be an explicit build-completion gate

* Related IDs: P01-T02, P02-T01, P02-T02.
* Evidence: the runner is a new image derived from the remotely built API.
  Bootstrap disables ACR public access through the shared publicAccess switch.
  infra/modules/registry.bicep uses networkRuleBypassOptions=None.
  infra/scripts/deploy.py queries repositories/tags unless an explicit
  --orchestrator-image is supplied or an existing real job image is resolved.
* Concern: the plan correctly builds before isolation but does not explicitly
  close over the new runner image, digest capture, remote validation and any
  repair build before the registry transition. Default remote ACR Tasks are
  not demonstrated to reach this registry once isolated, and the wrapper's
  fallback registry lookup is then not an available operator-side data path.
* Impact: a late runner fix or digest lookup can halt private execution and
  tempt registry re-exposure or a prohibited external data-plane workaround.
* Smallest useful change: make all four workload images plus the derived
  runner, their digests and bounded remote runtime checks prerequisites to
  isolation. Pass --orchestrator-image explicitly for every wrapper call.
  Verify private endpoint approval, login/data-endpoint DNS and MI AcrPull
  before relying on pulls. Define the post-isolation repair outcome as Blocked
  unless an already-authorized private ACR task network path is evidenced.
  Do not invent a build agent, peering or network bypass.
* Action owner: planning parent and build/infrastructure implementer.
* Exact resolving evidence: pre-isolation image/run/digest manifest including
  runner; explicit wrapper invocation; scoped what-if retaining development
  quarantine behavior; successful post-isolation initializer image pull and
  revision/job pull evidence. Registry digest capture must not require later
  operator data-plane access.
* Decision route: direct planner correction. No user response required unless
  the implementation later seeks a new network/build topology.

## Strengths and Residual Risk

* Explicit-false networking, no-firewall enforcement, incremental what-if,
  fixed resource-group scope and retained budget are well aligned.
* Dedicated initialization identity and Graph-free contained users are credible
  approaches; neither requires pretending that an MI is a staff member.
* Bearer-only EasyAuth is not rejected for lacking a client secret. Its Azure
  behavior remains runtime evidence to obtain, not a guaranteed success.
* ACR-before-isolation ordering is directionally correct. Production quarantine
  is not itself a proven blocker for the retained development profile, where
  quarantine is disabled.
* Skeleton agents and importer CLI limitations, unexecuted probes, missing staff
  and owner gates remain explicit. These are honest residual limits, not
  grounds to fabricate a pass or expand scope.

## Questions or Blocking Evidence Gaps

* No decision-critical owner question is required to revise this plan.
* Azure permission propagation, actual secretless auth acceptance, private DNS,
  image pulls and SQL driver MSI behavior remain bounded execution gates.
  Stop affected probes on failure and retain independent evidence.

## Limitations

* Static critique only; no Azure, production or tenant writes, remote builds,
  deployments, token acquisition or dataset reads were performed.
* Research's Azure observations are supplied evidence, not independently
  revalidated live state. No legal/regulatory currentness claims are made.
* No .env, .vscode, github-issues tracking, private datasets, mvp or prototype
  contents were inspected. Only this critique artifact was written.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: add the environment-only dependency stage, then integrate
  PC-002 through PC-006 into the same plan/details revision and finalize without
  commissioning another critique.
* User response required: no. Existing direction resolves the authority boundary.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-16/deployed-src-proof-plan.md](.copilot-tracking/plans/2026-10-16/deployed-src-proof-plan.md) | Final-candidate plan assessed |
| [.copilot-tracking/details/2026-10-16/deployed-src-proof-phase-details.md](.copilot-tracking/details/2026-10-16/deployed-src-proof-phase-details.md) | Execution details assessed |
| [.copilot-tracking/research/2026-10-16/deployed-src-proof-research.md](.copilot-tracking/research/2026-10-16/deployed-src-proof-research.md) | Supplied research |
| [.copilot-tracking/reviews/2026-10-16/deployed-src-proof-plan-critique.md](.copilot-tracking/reviews/2026-10-16/deployed-src-proof-plan-critique.md) | Complete single-pass critique |

## Next Steps

The active planning parent should apply the six direct corrections, record their
disposition and finalize the plan without a second critique. No user action is
required, and no deployment or broader authority is granted by this assessment.
