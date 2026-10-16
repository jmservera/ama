---
title: In-VNet staff initialization final-candidate plan critique
description: One bounded offline assessment of the Refs 360 implementation candidate
ms.date: 2026-10-16
---

## Metadata

* Task ID: 360-run-in-azure
* Critique date: 2026-10-16
* Plan: .copilot-tracking/plans/2026-10-16/run-in-azure-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/run-in-azure-phase-details.md
* Critique execution status: Complete
* Assessment count: One final-candidate critique. No further critique is requested.

## Inputs and Criterion Boundary

* Caller requirements: implement --run-in-azure and automatic continuation when
  local SQL is blocked; cover candidate lookup, check, apply, SQL verification
  and API restart; preserve local Graph authority and deterministic persisted
  roster behavior; use the existing job-<prefix>-init and id-<prefix>-init in
  the selected API VNet, in ama. No public/network changes, live Azure calls,
  image builds, agents, source edits or Git writes during this critique.
* Supplied research: .copilot-tracking/research/2026-10-16/run-in-azure-research.md,
  including C1-C7 and the transport/restart dispositions.
* Candidate: all requirements, acceptance criteria, P01-T01, P01-T02, P02-T01
  and P02-T02 in the supplied plan and phase details.
* Bounded code evidence: infra/scripts/setup-entra.py,
  infra/scripts/initialize-workbench-staff.py, infra/scripts/staff_roster.py,
  infra/scripts/private-cutover-proof.py, infra/cutover-proof.Dockerfile,
  infra/README.md, infra/tests/test_setup_entra.py,
  infra/tests/test_initialize_workbench_staff.py,
  src/core/src/zava_forward/core/mssqlstore.py and src/api/requirements.txt.
  Relevant identity/environment declarations in infra/main.bicep were also
  inspected. Project specification, reference index and owner memory supplied
  context, not evidence of deployed acceptance.
* Boundary: assess implementation credibility and identify exact missing
  contracts, offline evidence and deployment prerequisites. Do not infer
  Azure log reachability, installed image capabilities, tenant authorization,
  SQL connectivity, browser success or human acceptance from local fakes.
* Existing candidate artifacts and other worktree changes were not modified.
  This review is the only authored file.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Explicit --run-in-azure and automatic fallback; C1; P01-T02 | Partial | Both paths are intended, but safe fallback eligibility and uncertain local apply handling are unspecified; PC-004 |
| Candidate/check/apply/verify; P01-T01/P01-T02 | Partial | Canonical SQL is a sound base; execution, post-commit verification and result contracts need definition; PC-005/PC-007 |
| Literal job-owned API restart; research Contrarian; plan Functional Requirements | Conflicting | Candidate explicitly moves restart outside the job; enforce worker-owned restart with narrow API-scoped permission; PC-001 |
| Local Graph authority and seeded roster; C7; P01-T01 | Partial | Separation is correct; manual-roster enrichment and canonical packaging need explicit treatment; PC-008 |
| Existing initializer, identity, private SQL, API VNet and ama only; P01-T02 | Partial | Guard intentions are present, but exact resource/administrator comparisons and refusal fixtures are missing; PC-003 |
| Secret transport, encryption and encrypted logs; C6; P01/P02 | Partial | Private ARM body helper exists; actual retrieval interface and authenticated framing remain unspecified; PC-002/PC-007 |
| Cleanup on success/failure/timeout; P01-T02 | Partial | Finally cleanup is promised without an asynchronous deletion/uncertain-start/interruption contract; PC-006 |
| Concurrency and no uncertain apply retry; Functional Requirements; P01/P02 | Partial | SQL transaction protection exists, but job retry/replica settings and orchestration ownership are not fixed; PC-005 |
| Proof image and dependency readiness; C4/C5; P01-T01 | Partial | Runtime packages exist, but the present image contains only the proof runner and its own entrypoint; PC-008 |
| Offline tests, regression preservation and truthful acceptance; P02-T01/P02-T02 | Partial | Appropriate suites and live limitations are identified; finding-specific negative and recovery cases must become acceptance gates |
| No live Azure/image/network work; scope and P02-T02 | Covered | Candidate preserves this execution boundary; Bicep authoring recommended below does not authorize deployment |

## Verdict

* Verdict: Revise
* Severity summary: 6 High, 2 Medium, 0 Critical, 0 Low.
* Rationale: the core SQL-only transport design is plausible, but the candidate
  is not implementation-ready. It changes an explicit restart requirement,
  assumes an unspecified log-return channel, and leaves security-sensitive
  fallback, identity, execution and cleanup behavior to implementation-time
  decisions. These are planner-owned corrections, not cosmetic objections.
  Revise the plan directly from this complete finding set; do not commission
  another critique. A subsequently unresolved transport feasibility gate must
  be reported as blocked rather than replaced with an unauthorized channel.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Operator restart is not the literal job-owned restart

* Related IDs: caller restart requirement; research Contrarian restart
  disposition; plan Executive Summary, Functional Requirements and Scope;
  P01-T01, P01-T02, P02-T01.
* Evidence: the research and candidate explicitly place restart under operator
  login after job SQL verification. The caller explicitly says the job must
  restart the API. infra/scripts/initialize-workbench-staff.py:230-253 already
  defines the relevant behavior: enumerate traffic-serving revisions, restart
  them, and verify replacement ready replicas, including after a SQL no-op.
* Concern: secure operator orchestration meets the end-to-end business outcome
  but not the stated execution-location requirement. Avoiding broad ARM access
  is not a reason to silently waive that requirement when resource-scoped
  permissions are a candidate solution.
* Impact: implementation can pass its own tests while failing the requested
  acceptance criterion; restart failures may also be incorrectly attributed to
  an already-successful SQL job.
* Smallest useful change: preserve the literal requirement. Plan worker-owned
  restart after successful post-apply SQL verification, using the same existing
  id-<prefix>-init and an offline-authored least-privilege Bicep role/assignment
  scoped to the selected API resource. Enumerate only necessary read,
  traffic/revision/replica discovery and restart actions; exclude Contributor,
  wildcard actions, Graph privileges and unrelated application writes. Acquire
  the worker's own managed-identity ARM token, never forward an operator token.
  Verify exact provider action names before coding the role. Amend the
  candidate's self-imposed no-new-role non-goal only for this narrow assignment.
  Keep all deployment and permission activation Not run.
* Action owner: planning parent, then infra/worker implementer.
* Exact resolving evidence: revised P01 tasks naming the Bicep file, exact
  role actions and API-only role-assignment scope, existing identity principal
  binding and worker ARM client; offline Bicep validation where available;
  worker tests proving SQL verification precedes restart, all serving
  revisions converge to fresh ready replicas, SQL no-op still permits required
  restart, restart failure remains incomplete, and no operator credentials or
  broad role are transferred. Deployment authorization remains a separate
  unmet gate.
* Decision route: direct planner correction to honor current user direction.
  Exact disposition: implement worker restart through least privilege;
  reject the candidate's operator-only split as literal compliance. If the
  parent instead wants to retain operator restart, it must obtain an explicit
  owner-approved requirement change before treating that alternative as
  accepted. This review does not grant that waiver or authorize deployment.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: The encrypted result return channel has no concrete feasibility contract

* Related IDs: research Contrarian and Dispositions; plan Non-Functional
  Requirements; P01-T02, P02-T01.
* Evidence: the supplied research selects encrypted job logs, but names no
  command/API, network endpoint, execution/replica selection or log-retention
  behavior. infra/scripts/setup-entra.py:136-218 currently expects JSON CLI
  output, restricts REST hosts to Graph/ARM, and bounds each subprocess, not
  an entire stream/retrieval operation. infra/README.md:277 onward establishes
  the operator's lack of API-VNet SQL access, not a working log retrieval path.
* Concern: treating "logs" as management-plane transport is unproved. The
  chosen interface may require a distinct streaming/query endpoint or may not
  return completed-job output using the existing JSON helper. A fake accepting
  invented output does not establish interface feasibility.
* Impact: candidate listing and checks can fail even when the worker succeeds.
  Lost apply results leave SQL outcome uncertain, preventing safe restart,
  success reporting or automatic retry.
* Smallest useful change: add a transport feasibility subtask before lifecycle
  implementation. Specify the supported CLI/version or API operation, endpoint
  category, authorization, response format, execution/replica/container
  addressing, completed-execution availability, pagination/tail limits and
  bounded handling of delayed/truncated logs. Supply offline authoritative
  interface evidence when available; otherwise name the missing evidence gate.
  Do not assume public blob access, open networks, add log-workspace access or
  extend the fixed-host client silently. An inaccessible channel fails closed
  with the authorized private-host alternative.
* Action owner: planning parent and transport implementer.
* Exact resolving evidence: a revised P01-T02 interface contract with a
  concrete evidence pointer and realistic recorded/schema fixtures, plus
  tests for plain-text versus JSON framing, completed and running execution
  logs, delayed delivery, inaccessible endpoint, missing tail, wrong execution,
  pagination/truncation and total deadline. Live reachability stays Not run.
* Decision route: direct planner correction; if offline evidence cannot
  substantiate a usable channel within existing access, mark transport
  feasibility blocked and escalate that specific evidence/access gap.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Resource and SQL administrator guards are too imprecise to fail closed

* Related IDs: caller existing-resource/VNet/ama boundary; plan Functional
  Requirements; P01-T02; P02-T01 source mismatch coverage.
* Evidence: phase details require the same ama environment, expected identity
  and private SQL administrator without defining comparison fields.
  infra/scripts/initialize-workbench-staff.py:256-266 checks SQL FQDN,
  database presence and Disabled public access, but does not establish the
  requested initializer administrator binding.
  infra/scripts/setup-entra.py:552-593 demonstrates that demo authorization
  also needs resource-bound deployment/profile evidence, not a name alone.
* Concern: sharing an environment or matching a display name does not prove
  the exact intended job, identity, administrator, tenant or database.
  Client ID and principal ID are different identifiers. Safe template cloning
  also needs explicit rejection of extra containers, init containers,
  identities, secret references, commands and arbitrary SQL connection options.
* Impact: a mistaken source can send private roster data to the wrong
  workload, run with the wrong authority or write to an unintended database.
* Smallest useful change: enumerate a fail-closed guard table before any
  secret-bearing create/start. Bind canonical full resource IDs to the selected
  subscription/tenant, ama, API-derived approved prefix, exact
  job-<prefix>-init and id-<prefix>-init, and the selected environment's actual
  VNet/subnet binding. Resolve and compare the identity's principal ID,
  client ID and tenant to the SQL Entra administrator fields using their
  correct meanings; reject ambiguous/group-based or mismatched administrator
  configurations for this identity-specific path. Require Disabled SQL public
  access and the intended Entra-only configuration. Bind the existing database
  to API settings. Construct an allowlisted one-worker template and SQL MSI
  environment, with TLS verification; do not inherit token/password auth,
  trust-certificate overrides, unrelated registry credentials or arbitrary
  connection-string fragments.
* Action owner: planning parent and transport/infra implementer.
* Exact resolving evidence: a field-by-field guard and template allowlist in
  P01-T02, plus independent refusal fixtures for each ID/tenant/subscription,
  prefix, group, environment/VNet, SQL server/database, admin principal/client
  mix-up, extra identity/container and unsafe environment/registry case.
  Every refusal must precede secret-bearing mutation. Normalization may be
  case-insensitive for ARM IDs but must not accept substring/name-only matches.
* Decision route: direct planner correction; no new network, SQL-admin change
  or live resource discovery is authorized by this finding.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Automatic fallback lacks a safe local failure taxonomy

* Related IDs: explicit/automatic mode requirement; plan no-uncertain-apply
  retry requirement; P01-T02, P02-T01.
* Evidence: infra/scripts/setup-entra.py:596-620 collapses unsuccessful
  candidate processes into a connectivity handoff.
  infra/scripts/setup-entra.py:898-940 distinguishes validation only through
  one stdout marker and otherwise groups connectivity, dependency and
  authority failures. A local apply may already have committed SQL before
  failing restart in infra/scripts/initialize-workbench-staff.py:326-336.
* Concern: "automatic fallback when local SQL blocked" is not a rule for which
  failures permit a new execution. A generic nonzero exit, timeout, malformed
  summary, denied authority, validation rejection or lost apply result cannot
  safely mean "run apply again in Azure."
* Impact: fallback can bypass a meaningful refusal, repeat a committed
  operation or report success after an unknown local state.
* Smallest useful change: define typed/sanitized local outcomes and a state
  machine. Permit fallback only for classified pre-mutation SQL reachability
  failure, and explicitly decide whether missing local SQL packages/driver
  count as eligible preflight failures. Keep validation, tenant, directory and
  guard failures terminal. Explicit Azure mode must bypass local SQL rather
  than require it to fail first. Once any apply may have started, perform only
  explicitly authorized reconciliation/check recovery; do not automatically
  reapply or switch execution hosts.
* Action owner: planning parent and setup/initializer implementer.
* Exact resolving evidence: a P01-T02 outcome/transition table for candidate,
  check, apply and restart; fake-process tests for connectivity, missing
  dependency, validation, 403, timeout before/after possible SQL mutation,
  invalid summary, known committed SQL with restart failure, and explicit
  mode. Tests must assert Graph authority is unchanged and no second apply
  occurs after uncertain completion.
* Decision route: direct planner correction.

<!-- rpi:critique id=PC-005 -->
### PC-005 [High]: Unique job names do not define bounded execution or concurrency safety

* Related IDs: plan independent bounded executions and no uncertain retry;
  P01-T01, P01-T02, P02-T01.
* Evidence: the candidate promises unique jobs and canonical atomic install,
  but fixes no Azure replica/retry settings, cross-phase ownership or post-apply
  verification protocol. infra/scripts/initialize-workbench-staff.py:175-227
  protects an installation transaction.
  src/core/src/zava_forward/core/mssqlstore.py defines the transaction-owned
  zavaforward_write application lock. Existing local and API advisory locks in
  infra/scripts/setup-entra.py:801-824 and :1335-1350 do not automatically
  serialize independent worker jobs or read-only paths.
* Concern: platform retries or multiple replicas can rerun a worker despite
  the client's no-retry promise. Candidate/check/apply are separate executions,
  so stale input and changing API/SQL state need explicit treatment. Returning
  a successful commit summary is not independently verifying persisted state.
* Impact: duplicate work, competing restarts, stale approvals and false
  convergence evidence remain possible.
* Smallest useful change: specify Manual trigger, parallelism 1,
  replicaCompletionCount 1, replicaRetryLimit 0, worker/replica timeouts and a
  total client deadline including retrieval and cleanup. Bind every result to
  its operation and intended target/roster. Preserve SQL transactional
  protection; define coordination ownership from preflight through restart
  and completion reporting without holding the SQL write lock while waiting
  for ARM. Revalidate protected SQL state at apply and perform a post-commit
  read/check that proves zero remaining roster/owner-label drift before
  restart. Never reseed via Store initialization. Define a stale-target/result
  refusal and explicit recovery after known SQL success.
* Action owner: planning parent and worker/setup implementer.
* Exact resolving evidence: concrete execution settings and state transitions
  in phase details; two-session, platform-retry, duplicate-result,
  stale-candidate and changed-target tests; a worker test where commit
  succeeds but the verification read detects drift and prevents restart;
  an adapter-level fixture preserving the MSSQL application-lock behavior,
  alongside existing SQLite atomicity/history regressions. Do not describe
  SQLite-only tests as live SQL concurrency proof.
* Decision route: direct planner correction.

<!-- rpi:critique id=PC-006 -->
### PC-006 [High]: Finally cleanup is not a verified stop-and-delete contract

* Related IDs: research cleanup disposition; plan Non-Functional Requirements;
  P01-T02, P02-T01.
* Evidence: research says delete the ephemeral job in finally; phase details
  mention stop/delete. No ownership check, asynchronous deletion verification,
  uncertain creation/start handling or failure recovery is specified.
  infra/scripts/setup-entra.py:136-193 removes its local request file in
  finally, but that says nothing about remote job lifetime.
* Concern: create/start may succeed before the response is lost. A delete
  request may be asynchronous or fail. Cleanup errors may conceal the primary
  operation failure, leave an SQL-admin worker active, or remove the wrong
  resource if ownership is inferred only from a name.
* Impact: secrets and elevated execution can outlive the command; an operator
  may retry while the previous apply is still running.
* Smallest useful change: reserve a unique owned resource ID before create,
  refuse collisions without adopting/deleting them, and track uncertain
  create/start states. On all normal failures, timeout and handled
  interruption, stop owned executions, establish terminal state as far as
  possible, delete only the owned ephemeral job and poll for confirmed
  absence with a cleanup deadline. Never delete or modify the source job.
  Preserve sanitized primary failure and cleanup status separately; unverified
  cleanup is incomplete, not success. Document that hard termination cannot
  guarantee finally execution, and provide a secret-free operator recovery
  procedure for owned leftovers without automatically reapplying SQL.
* Action owner: planning parent and transport implementer.
* Exact resolving evidence: lifecycle/ownership and cleanup outcome tables;
  tests for lost create/start responses, start failure, worker failure,
  retrieval failure, timeout, interrupt, failed stop, asynchronous delete,
  denied delete, collision and source-job preservation. Assert mode-0600
  body-file deletion and absence of secret payloads in all captured streams,
  including cleanup failures. Runbook recovery must require checking whether
  SQL may already have committed.
* Decision route: direct planner correction.

<!-- rpi:critique id=PC-007 -->
### PC-007 [Medium]: AES-GCM and chunked logs need one precise authenticated protocol

* Related IDs: research encrypted-results decision; plan Non-Functional
  Requirements; P01-T01, P01-T02, P02-T01.
* Evidence: the candidate specifies a random per-run AES-GCM key, bounded
  chunks and strict result validation but not nonce handling, authenticated
  metadata, terminal framing, payload limits or result schema.
* Concern: implementations can differ on whether each chunk is authenticated,
  whether the whole ciphertext is complete, and whether a valid result belongs
  to this operation. Encryption alone neither detects missing complete records
  nor binds success to the intended execution and target.
* Impact: truncated, replayed, mixed-execution or malformed logs can produce
  ambiguous outcomes, excessive memory use or incorrectly trusted success.
* Smallest useful change: define a versioned envelope, key/nonce generation,
  authenticated operation/run/target/input binding, bounded total input/output,
  chunk size/count/order rules and an unambiguous terminal result. Either
  encrypt one bounded result and split its ciphertext, or specify safe unique
  nonces and authenticated indexing for independently encrypted chunks.
  Authenticate and validate the entire result before consuming candidates,
  marking SQL/restart complete or writing a roster. Reject invalid counters,
  including booleans masquerading as integers, unknown operation/schema and
  missing required verification fields. Use encrypted sanitized failure
  results, not raw SQL/SDK errors or tracebacks.
* Action owner: planning parent and transport/worker implementer.
* Exact resolving evidence: one shared wire-contract definition and fixtures;
  tests for wrong key, tampering, truncated ciphertext, missing/duplicate/
  reordered/conflicting chunks, wrong run/operation/target, oversized input
  and logs, malformed schema and exception paths. Tests inspect command
  arguments, body-file permissions, stdout, stderr and captured CLI results
  for absence of roster identities, encryption keys and plaintext candidate
  data. Printed --list-staff output remains an intentional local interface,
  not permission for plaintext worker logs.
* Decision route: direct planner correction.

<!-- rpi:critique id=PC-008 -->
### PC-008 [Medium]: Graph-free reuse and proof-image readiness need an explicit asset contract

* Related IDs: C4, C5, C7; P01-T01, P02-T01; seeded/manual roster preservation.
* Evidence: infra/cutover-proof.Dockerfile currently copies only
  private-cutover-proof.py and sets it as ENTRYPOINT.
  infra/scripts/initialize-workbench-staff.py:142-172 combines SQL preparation
  with Graph lookup and reads infra/entra/app-registration.json by relative
  filesystem layout. It also imports staff_roster.
  infra/scripts/setup-entra.py:1078-1111 fetches name/UPN only when
  verify_people is true, so existing manual-roster resolution does not always
  supply the complete person object needed by the SQL preparer.
* Concern: "a narrow COPY" and "pass resolved people" leave required imports,
  data files, paths and entrypoint overrides undefined. Cloning the currently
  existing image cannot itself add a new worker. A naive reuse may restore
  Graph calls in the worker or fail for manual rosters.
* Impact: the new command can fail after transferring secrets, or diverge from
  canonical eligibility/protected-profile checks and seeded assignment behavior.
* Smallest useful change: enumerate the two-module split and every copied
  helper/manifest, with explicit in-image paths and worker command overriding
  the proof ENTRYPOINT without altering existing proof modes. Separate
  local-person retrieval/validation from a pure SQL preparation interface for
  both generated and manual rosters. Require a compatible initializer image
  containing that asset set; document its later authorized build/publication
  and source-job image update as deployment prerequisites, not tasks silently
  performed here. Fail closed on incompatible images without claiming Azure
  acceptance or forwarding Graph credentials.
* Action owner: planning parent and initializer/image implementer.
* Exact resolving evidence: revised P01-T01 asset/import/interface table;
  offline staged-filesystem import and CLI-dispatch tests, without an image
  build; generated and manual roster tests with local-only Graph requests,
  complete person fields and existing immutable/supplier/history guarantees;
  unchanged seeded assignment and persisted-roster reuse regressions.
  Runbook must identify image capability/version requirements and distinguish
  authored Dockerfile changes from an actually published compatible image.
* Decision route: direct planner correction.

## Strengths and Residual Risk

* Keeping Graph authority and people resolution on the operator host is the
  correct boundary. The worker should not perform directory lookup, assignment
  or use operator credentials.
* The existing private body-file helper, authenticated encryption dependency,
  explicit SQL MSI client ID and canonical atomic installer provide useful
  foundations. Existing SQL history and immutable-profile tests should be
  retained, not replaced by transport mocks.
* Unique ephemeral jobs avoid mutating the source initializer's configuration,
  provided ownership, retry settings and verified cleanup are implemented.
* The candidate appropriately distinguishes dry-run from read-only SQL
  operations that still create transient control-plane resources.
* Live image, authorization, private SQL/network, log delivery and browser/human
  acceptance remain explicitly unverified. This is a valid offline boundary,
  not an accepted substitute for those later gates.
* Adding only narrowly scoped restart permission to the existing identity is
  additional privilege and must be documented and validated. It does not
  justify broad ARM roles, a second identity or public/network changes.

## Questions or Blocking Evidence Gaps

* PC-002 requires a concrete supported log retrieval interface before the
  transport can be considered implementation-ready. Missing live reachability
  is expected; missing interface evidence is not.
* PC-001 has an exact disposition: retain the user's literal worker restart
  requirement and plan the minimal API-scoped Bicep authorization. No user
  response is required to follow that direction. Owner approval is required
  only if the parent wants the divergent operator-only interpretation, or
  later seeks live deployment authorization.

## Limitations

* No external research, Azure calls, image builds, tests, live permission
  discovery or agents were used. Existing tests were read, not executed.
* This is a plan critique, not an implementation security audit or an
  acceptance of Azure runtime behavior.
* Exact Azure log schemas and restart provider action names are not established
  by the supplied evidence; findings require those contracts rather than
  inventing them.
* The review is complete for the supplied candidate boundary. It does not
  require a second critique after corrections and cannot certify code that
  has not yet been implemented.

## Recommended Next Action

* Highest-impact finding: PC-002, the unsubstantiated result return channel.
* Action owner: planning parent.
* Smallest next action: specify and substantiate the exact log retrieval
  interface, then revise P01/P02 directly to resolve PC-001 through PC-008
  with the named acceptance tests and owners.
* User response required: No for these direct corrections. Yes only if the
  parent elects to change the literal restart requirement or needs additional
  live authorization. Neither is implicitly granted here.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-16/run-in-azure-research.md](.copilot-tracking/research/2026-10-16/run-in-azure-research.md) | Supplied offline research |
| [.copilot-tracking/plans/2026-10-16/run-in-azure-plan.md](.copilot-tracking/plans/2026-10-16/run-in-azure-plan.md) | Final candidate assessed without modification |
| [.copilot-tracking/details/2026-10-16/run-in-azure-phase-details.md](.copilot-tracking/details/2026-10-16/run-in-azure-phase-details.md) | Candidate task details assessed without modification |
| [.copilot-tracking/reviews/2026-10-16/run-in-azure-plan-critique.md](.copilot-tracking/reviews/2026-10-16/run-in-azure-plan-critique.md) | This complete single-pass finding set |

## Next Steps

Return Revise to the planning parent. The parent should resolve this finding set
directly and finalize without another critique. No user action is required for
the prescribed worker-owned least-privilege design. Stop this critique here;
source changes, Azure execution, Git operations and deployment remain outside
this invocation.
