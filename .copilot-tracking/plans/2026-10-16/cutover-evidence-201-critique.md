---
title: Cut-over Evidence 201 Final-candidate Plan Critique
description: One bounded credibility assessment of the supplied evidence-pack plan
ms.date: 2026-10-16
ms.topic: reference
---

## Metadata

* Task ID: issue-201 / cutover-evidence-201
* Critique date: 2026-10-16
* Plan: .copilot-tracking/plans/2026-10-16/cutover-evidence-201-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/cutover-evidence-201-phase-details.md
* Critique execution status: Complete
* Execution count: one final-candidate critique; no subsequent critique requested.

## Inputs and Criterion Boundary

* The supplied plan, phase details and research are the primary inputs.
  Research reports owner comments on #200/#201 and an empty ama resource
  inventory; those observations were not independently refreshed here.
* Caller requirements: actual local tests and a bounded Azure deployment
  through repository templates/scripts, writes only within existing ama,
  pip rather than uv, no Docker, no group or mvp/prototype deletion, no
  acceptance/sign-off claim, and no access to properwarm.json, .env,
  .vscode or .copilot-tracking/github-issues.
* The change budget permits at most one src/core audit module and one
  external test module. This critique changes neither source nor that budget.
* Read the required repository context documents and the supplied evidence
  pointers: infra/README.md, infra/main.bicep,
  infra/modules/containerapps.bicep,
  docs/architecture/mvp-to-src-parity-matrix.md and
  .github/workflows/src-ci.yml. Inspection was limited to the candidate's
  stated deployment, parity and validation boundary; no open-ended research,
  live Azure operation, application test execution or issue retrieval occurred.
* Assessment covers requirements, research assumptions, all phases/tasks,
  acceptance criteria, dependencies, safety boundaries, mutation evidence
  and reporting claims. It assesses planning credibility, not implementation
  acceptance or exploitable vulnerabilities.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| #200/#201 owner authority, no deletion, retained check names | Covered | Explicitly preserved; private backup and sign-off remain owner gates. |
| P01-T01 actual local suites, pip, lint/types, infra | Partial | Commands, auxiliary checks and parity comparison acceptance are not fully specified; PC-005/006. |
| Research W3, C3/C4; P01-T02 ama-only bootstrap | Partial | Valid two-stage direction but missing executable preflight and second-stage gates; PC-001/002. |
| P01-T02 bounded deployed smoke | Partial | No concrete image/revision/authentication/SQL proof contract; PC-003. |
| P02-T01 audit, exclusions, mutation contract | Partial | Correct intent and module budget; meaningful regression oracle and baseline experiment undefined; PC-004. |
| P02-T02 current destinations, reference inventory, owner checklist | Partial | Honest categories present; row reconciliation and comparisons need defined evidence; PC-004/005. |
| P03-T01 acceptance review and defect disposition | Partial | Blanket routing of implementation defects to future work can bypass this task's acceptance; PC-007. |
| P03-T02 identity, trailer, Refs-only PR and no merge | Covered | Appropriate publication boundary; gate results must constrain readiness wording. |
| Phase dependencies | Partial | Order is implied, but explicit prerequisites for Azure stage two and final readiness are missing; PC-002/007. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 3 High, 4 Medium.
* The evidence-pack scope is credible and appropriately distinct from
  cut-over approval. Direct planner corrections are required before execution:
  the cloud boundary is not yet executable, and the negative validation
  contract can currently be met by detecting absence rather than a regression.
  The supplied evidence supports these findings without another research or
  critique cycle. Existing caller direction resolves the scope decisions.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Make the ama-only deployment boundary an executable preflight

* Related IDs: P01-T02; research C3/C4 and W3; ama-only and no-tenant-write requirements.
* Evidence: Phase details specify an existing Azure session and first-stage
  deployApplications=false, but not pinned subscription/group IDs, parameter
  resolution, profile selection or what-if review. infra/main.bicep defaults
  deployApplications=true and production isolation; development changes public
  connectivity and purge protection. infra/README.md documents placeholders,
  required SQL administrator values and what-if before publication/deployment.
* Concern: A generic authenticated session and historical empty inventory do
  not establish the current target or safe effective parameters. Simply
  following the README can also encounter group creation, subscription
  governance or tenant-registration instructions outside this authorization.
* Impact: Wrong-target writes, uncontrolled profile changes or unintended
  application creation can occur before an honest failure report is possible.
* Smallest useful change: Add a read-only preflight that pins subscription and
  existing ama resource ID, refreshes inventory, validates non-placeholder
  non-secret parameters and explicit deployment flags, then inspects a
  group-scoped what-if. Restrict execution to named group-scoped steps in
  incremental mode. Explicitly exclude group creation/deletion, subscription
  governance, tenant writes and policy-exception/tag workarounds. Stop and
  report rather than widen scope when prerequisites cannot be resolved safely.
* Action owner: Planning parent; implementation operator executes the guard.
* Exact resolving evidence: Revised P01-T02 contains the preflight commands,
  effective profile/flags, permitted target ID and abort criteria; later pack
  records sanitized current inventory, what-if outcome and deployment target
  IDs consistent with that same subscription and ama scope.
* Decision route: Direct planner correction. No user decision is required to
  enforce the already supplied boundary.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Specify stage-two prerequisites without bypassing tenant or private-data limits

* Related IDs: P01-T02; research C4; P02-T02 dependency disclosure.
* Evidence: Phase details name only the first-stage flag and registry builds.
  infra/README.md requires the real image, vault authentication secret and SQL
  preparation before enabling applications. infra/modules/containerapps.bicep
  enables authentication only with entraClientId, reads the secret through
  the API identity and configures the deployed API for MSSQL. Research rejects
  tenant changes and an unauthenticated public substitute.
* Concern: There is no planned path from bootstrap to authenticated serving,
  or precise stop condition if existing registration, secret, SQL admin/grants
  or reachable SQL are unavailable. A historical registration-creation recipe
  is not authorized by this task. A seed requirement cannot justify reading
  private working data or resetting existing SQL.
* Impact: Infrastructure/ACR success can be mistaken for a deployment attempt
  completed through the application stage, or the operator can improvise
  unauthorized initialization to make the app start.
* Smallest useful change: Add an ordered stage-two gate covering existing
  registration/client ID, required secret availability without value capture,
  managed-identity SQL access using the relevant repository script, and
  explicitly authorized synthetic initialization only if needed and safe.
  For each repository script, state its allowed side effects and skip it if
  they include tenant writes or private configuration access. Require explicit
  real image parameters for enabled workloads, never placeholder substitution.
  If any prerequisite is unavailable, record the blocked stage, retain
  deployApplications=false and report the bounded deployment attempt honestly.
* Action owner: Planning parent; implementation operator records prerequisites.
* Exact resolving evidence: Revised details show the dependency chain,
  allowed script invocations and stage-two command or deterministic stop
  branch; the pack later shows actual prerequisite statuses and executed
  stage outcomes, with unexecuted stages marked Blocked/Not run.
* Decision route: Direct planner correction. Obtaining new tenant authority or
  private-data access would be a separate owner decision, not a prerequisite
  to delivering this evidence pack.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Define what deployed proof and bounded smoke must establish

* Related IDs: P01-T02; P02-T02; deployed-proof acceptance criterion.
* Evidence: The plan requests smoke outputs and IDs but defines no checks.
  infra/README.md distinguishes the public welcome and /healthz from protected
  /app and data APIs; its recipe requires new immutable image tags.
  .github/workflows/src-ci.yml separately tests image properties.
* Concern: A successful build, an ARM success or a 200 from a public probe
  could satisfy the current wording without proving the src image is serving
  or the workbench remains protected.
* Impact: The report can overclaim deployment or security acceptance while
  the application is unhealthy, unauthorized or still running another image.
* Smallest useful change: Define per-workload build/tag/digest evidence,
  deployed revision/image/readiness observation, bounded /healthz checks and
  anonymous protected-API denial checks. Define an authenticated synthetic
  SQL-backed read if existing access permits, otherwise mark it Blocked.
  Record timeouts/retry limits and separate build, rollout, health, auth and
  data-path statuses. Do not log credentials, tokens, cookies or private
  response bodies; do not trigger real AI calls or worker actions merely to
  manufacture smoke proof.
* Action owner: Planning parent; implementation operator captures evidence.
* Exact resolving evidence: Details contain concrete endpoints, expected
  status/results, bounds and sanitization rules; the pack later binds each
  observation to commit, digest/revision, timestamp and actual exit/status.
  Build success alone cannot produce deployed-proof Pass.
* Decision route: Direct planner correction; unavailable authenticated access
  is a reported residual gate, not a demand for new owner authorization.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Replace absence-only baseline proof with a substantive regression experiment

* Related IDs: P02-T01; semantic/regression coverage; mutation acceptance criterion.
* Evidence: The plan says to prove the old revision lacks the required
  pack/test contract and lists mutations, but does not define the shared
  oracle, baseline invocation or meaningful expected failures. The audit is
  to scan tracked allowlisted text and classify references.
* Concern: Showing that a new test/module/pack is absent on the old revision
  does not prove the new audit detects a reference, destination or gate-claim
  regression. A fixture test can also pass while never exercising the real
  inventory regeneration or document guard.
* Impact: The requested "must fail without the new change" condition can be
  satisfied tautologically, and prohibited content can be opened before
  filtering if exclusions are tested only against final output.
* Smallest useful change: Define one repeatable contract exercised against
  the baseline and candidate, with named expected assertion failures rather
  than import/discovery errors. Separately mutate representative current
  destinations, reference additions/removals/classes, missing pack/checklist,
  and forbidden completion/sign-off claims; require the same real validator
  to reject each mutation. Instrument fixture reads to prove excluded paths
  are rejected before opening. Specify deterministic tracked-file enumeration,
  allowlist/classes, regeneration comparison and a permitted checkout-relative
  fixture location or in-memory fixtures, never system temporary directories.
* Action owner: Planning parent; audit/test implementer.
* Exact resolving evidence: Revised details specify baseline commit,
  callable/CLI contract, fixture inputs and expected diagnostics/exits;
  implementation evidence records clean candidate Pass, each mutant Fail
  with the named reason, the meaningful old-revision failure and a clean
  post-experiment diff. Actual prohibited files are never opened.
* Decision route: Direct planner correction within the one-audit-module and
  one-external-test-module budget.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Give current parity a row-level and test-baseline reconciliation oracle

* Related IDs: P01-T01; P02-T01/T02; historical matrix acceptance criterion.
* Evidence: The matrix retains proposed targets, A1-A5 divergences, rebuilds,
  sandbox pattern rows and historical totals/skips. The plan says to check
  exceptions and run five suites, but defines neither a complete row
  reconciliation nor a baseline comparison beyond reporting counts.
* Concern: Destination existence alone cannot prove all historical outcomes
  were accounted for, that an intentional drop was authorized, or that tests
  with different current placements preserve the historical gate.
* Impact: Missing rows, stale proposed paths, partial rebuilds or changed
  skips can be hidden behind a green file-existence audit or aggregate count.
* Smallest useful change: Define a dated reconciliation keyed by every
  historical row/pattern: historical outcome/target, current actual
  destination or evidenced exception, current status and remaining owner
  gate. Preserve the historical record. Compare current suite totals and
  skip reasons with the documented baseline, explaining additions/removals,
  moved tests and prototype exclusions without equating count with coverage.
  Unknown or unresolved rows remain visibly unresolved.
* Action owner: Planning parent; report/audit implementer.
* Exact resolving evidence: The plan names the row-universe and mismatch
  checks; the pack later contains exhaustive row accounting, explicit
  exceptions and a baseline/current test-and-skip comparison linked to actual
  run outputs, with no undocumented omissions or parity claims.
* Decision route: Direct planner correction; unresolved owner acceptance is
  recorded, not silently converted into a new implementation requirement.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Account for relevant non-suite gates and unavailable image checks

* Related IDs: P01-T01; research C2/C5; #200 validation and current-parity scope.
* Evidence: The matrix identifies web-script syntax and image properties as
  additional migration gates. .github/workflows/src-ci.yml includes installed
  namespace checks, browser checks, no-working-data checks and image
  assertions/scanning. P01-T01 enumerates suites, ruff/mypy, infra and rename
  regressions only. The source-image recipe asks for local image checks before
  publication, but Docker is explicitly unavailable in this task.
* Concern: "Existing relevant suites run" leaves auxiliary migration gates
  unaccounted for and does not resolve the recipe's unavailable local-image
  prerequisite. ACR build is not equivalent to non-root/read-only/no-data,
  isolation or vulnerability results.
* Impact: The pack may imply full #200 validation based on local unit tests
  and remote compilation, or overlook feasible existing offline checks.
* Smallest useful change: Add a validation ledger mapping each relevant
  existing gate to its exact command and execution location. Run feasible
  installed-package/namespace, no-data and web checks; explicitly disposition
  browser checks. Mark Docker/image assertions Not run locally, and attach
  matching-commit CI results when available without changing check names.
  State that the caller-authorized remote attempt does not satisfy the
  README's local-image validation claim.
* Action owner: Planning parent; validation operator.
* Exact resolving evidence: Revised P01-T01 lists commands or justified
  blocked/deferred statuses for auxiliary gates; the pack later records
  actual outputs and any exact-commit CI URLs, separating local, remote
  build and CI evidence. No unavailable image check is labeled Pass.
* Decision route: Direct planner correction; no Docker installation or new
  tooling/workflow expansion is requested.

<!-- rpi:critique id=PC-007 -->
### PC-007 [Medium]: Prevent the final review from deferring defects in this deliverable

* Related IDs: P03-T01/T02; evidence-pack acceptance criteria.
* Evidence: P03-T01 routes "remaining acceptance or implementation defects
  to future work" and forbids a second review, without distinguishing this
  pack's defects from existing cut-over/product gaps.
* Concern: That wording permits a broken audit, wrong inventory, unsafe
  deployment change or inaccurate result to survive publication as future
  work even when caused by this task.
* Impact: The single-review limit can become a readiness waiver and the
  owner receives an apparently completed pack that fails its own contract.
* Smallest useful change: Require current-task safety, evidence-integrity and
  audit/test defects to be corrected directly and targeted checks rerun before
  readiness claims. Only existing product, tenant and owner-acceptance gates
  may be deferred with explicit status/owner/evidence. Preserve one review
  and one critique; correction verification is not a new critique cycle.
  Permit an explicitly incomplete/blocked evidence PR rather than a false
  completion claim when a current-task defect cannot be resolved.
* Action owner: Planning parent and implementation/review parent.
* Exact resolving evidence: Revised P03-T01 states the separation and
  publication gate; review/change records later show each current-task
  finding resolved with targeted validation or prominently blocking
  completion, while owner checklist items stay unchecked.
* Decision route: Direct planner correction; no user response is required.

## Strengths and Residual Risk

* The candidate preserves user authority, the existing group and legacy
  folders, historical identifiers, unchanged workflow names and Refs-only PRs.
* It correctly treats an honest deployment failure as evidence, not as
  permission for an unauthenticated substitute or a cut-over approval.
* Pip installation, src-only build context, external tests and bounded module
  changes match the supplied constraints.
* SQL integrations, private copy/encrypted backup, tenant dependencies,
  worker transport and owner approval remain separate gates. They must not
  be inferred from offline success or this critique.
* No new owner choice is needed to make the plan safe and executable.
  Additional authority, if later desired, belongs to a separately scoped
  owner decision rather than an implicit workaround.

## Questions or Blocking Evidence Gaps

* None prevents this planning verdict. Current Azure permissions, registration,
  secret availability, SQL reachability and capacity remain execution-time
  unknowns with required stop/report branches, not assumed facts.

## Limitations

* No application tests, deployment, account changes, issue refresh or artifact
  regeneration were performed. The critique verifies neither historical Azure
  observations nor future success.
* Only this critique file was written. The supplied dirty-worktree artifacts
  were retained in place; no branch switch, commit, stash or source edit occurred.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Revise P01-T02 with explicit target/parameter/what-if
  guards, then incorporate the remaining direct corrections in the same
  finalization. Do not dispatch another critique.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-16/cutover-evidence-201-plan.md](.copilot-tracking/plans/2026-10-16/cutover-evidence-201-plan.md) | Assessed final candidate |
| [.copilot-tracking/details/2026-10-16/cutover-evidence-201-phase-details.md](.copilot-tracking/details/2026-10-16/cutover-evidence-201-phase-details.md) | Assessed execution details |
| [.copilot-tracking/research/2026-10-16/cutover-evidence-201-research.md](.copilot-tracking/research/2026-10-16/cutover-evidence-201-research.md) | Supplied evidence and decisions |
| [.copilot-tracking/plans/2026-10-16/cutover-evidence-201-critique.md](.copilot-tracking/plans/2026-10-16/cutover-evidence-201-critique.md) | Complete single-pass findings |

## Next Steps

The active planning parent should make the seven direct corrections and
finalize without another critique. No user action is required. Continue only
within the caller's existing authority and report unavailable deployment
prerequisites as explicit blocked stages.
