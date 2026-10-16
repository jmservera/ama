---
title: One-command Entra setup final-candidate critique
description: Independent correctness, idempotency, credential and authorization assessment for issue 351
ms.date: 2026-10-16
---

## Metadata

* Task ID: 351
* Critique date: 2026-10-16
* Plan: .copilot-tracking/plans/2026-10-16/one-command-entra-setup-351-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/one-command-entra-setup-351-phase-details.md
* Research: .copilot-tracking/research/2026-10-16/one-command-entra-setup-351-research.md
* Critique execution status: Complete
* Execution count: One independent final-candidate assessment; no nested agents.

## Inputs and Criterion Boundary

* The caller requires one standard-library script with no required arguments,
  ama API/Front Door tag/fallback discovery, additive app/SP/role/callback
  convergence, optional secure secret storage, explicit-role private user/group
  assignments, isolated device-code authentication, tool/network/Graph
  preflight, check/dry-run, offline tests, documentation and a PR.
* Identifiers, email addresses and secrets must not enter logs. No Azure writes,
  private-data reads, or mvp/prototype/.env/.vscode edits are authorized now.
  The pending #344 edge design must remain intact.
* All three supplied artifacts were read completely. Repository case-study,
  index and memory context was consulted for standing boundaries, not as new
  technical evidence. Technical claims below use only the supplied artifacts;
  their source pointers were not independently re-researched.
* Related identifiers are P01-T01, P01-T02, P02-T01 through P02-T03 and research
  C1-C5/W1-W2. Functional requirements lack individual IDs, so findings identify
  their wording and line ranges rather than inventing requirement identifiers.
* Accepted decisions include additive changes, no SQL binding or invitations,
  no automatic directory-wide consent, isolated login, explicit roster roles,
  optional credential creation and separate live operator acceptance.
* The boundary is planning credibility, not implementation verification or live
  tenant readiness. The requested deliverable is this critique only. Existing
  untracked planning inputs on feat/one-command-entra-setup-351 were left intact.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| No-required-arguments standard-library entry point | Partial | Script/runtime are specified; default private-roster discovery and unauthenticated check outcomes are not. PC-007 |
| API tags, fallback, ambiguity; C1; P01-T01/P01-T02 | Covered | Explicit precedence, ambiguity failure and managed-identity sentinel exclusion |
| Tenant, Graph/ARM authority and preflight; W1; P01-T01 | Partial | Fixed hosts and tool checks exist; cross-profile tenant binding, operation authority and network preflight are unspecified. PC-001 |
| App/SP and assignment idempotency; C5; P01-T01 | Partial | Additive roles and stable IDs exist; effective SP role readiness, typed principals and interrupted/concurrent convergence need contracts. PC-003/PC-004 |
| Credential storage and auth-client handoff; W1; P01-T01 | Partial | Explicit creation, private transfer and no rotation exist; one-time-secret failure recovery is absent. PC-002 |
| Origin-linked callbacks and #344; C2/C3; P01-T01/P01-T02 | Partial | Strong origin association; pending proxy/browser-auth patch boundaries and domain eligibility remain underspecified. PC-005 |
| Private explicit-role roster | Partial | Whole-roster validation and legacy rejection exist; principal and conflict semantics need tests. PC-003 |
| No sensitive logs and isolated login | Partial | Raw failure suppression exists; successful subprocess output, login/cache lifecycle and process-launch failures need explicit coverage. PC-006 |
| Check/dry-run, no writes/login; P02-T01 | Partial | Stated clearly; missing authentication, incomplete discovery and local side effects need deterministic outcomes. PC-007 |
| Offline tests, legacy compatibility and docs; P02-T01/P02-T02 | Covered with gaps | Stateful fake az, legacy tests, lints and docs are assigned; resolving evidence below adds concrete negative scenarios |
| Independent review and PR; P02-T03 | Partial | Delivery is assigned, but unconditional follow-up wording can defer release-blocking defects. PC-008 |
| SQL, private network, human consent and live acceptance; C4 | Covered | Explicit separate operator gates; no claim of real browser, tenant or SQL acceptance |

## Verdict

* Verdict: Revise
* Severity summary: 5 High, 3 Medium, 0 Critical, 0 Low.
* The architecture is credible, but the candidate does not yet define enough
  failure-state and trust-boundary behavior to safely implement directory and
  credential mutations. These are direct planner corrections within confirmed
  user direction, not reasons for a new user decision or a live probe.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Bind both authentication contexts and preflight each mutation authority

* Related IDs: P01-T01, P02-T01; isolated login, tool/network/Graph preflight,
  resource scope and human-consent requirements; research W1.
* Evidence: .copilot-tracking/plans/2026-10-16/one-command-entra-setup-351-plan.md:39-55
  specifies client preference, scope validation and extension preflight.
  .copilot-tracking/research/2026-10-16/one-command-entra-setup-351-research.md:53-55,74-76
  distinguishes read access from write authority and describes a read-only
  operator management profile plus an isolated Graph/login profile.
* Concern: There is no executable contract binding the selected subscription,
  resource tenant, isolated Graph tenant, application appId, application object
  and SP object. Nor is it clear which context performs ARM writes, which
  delegated permissions/directory authority each Graph operation requires, or
  how connectivity/consent/authority failures are classified before mutation.
  A UUID-shaped configured client is not evidence of a local writable
  registration. A missing object and a forbidden/incomplete lookup cannot
  trigger the same create fallback.
* Impact: A second device-code account could target the wrong directory, an
  existing foreign-owned registration could be mistaken for a missing local
  app, or setup could partially mutate before discovering missing authority.
* Smallest useful change: Define a tenant/account/context invariant and a
  per-operation preflight matrix for discovery, app/SP updates, role
  assignments, secret storage and auth wiring. Resolve appId versus object IDs
  explicitly; fail closed on tenant mismatch or inaccessible/foreign app.
  Specify bounded tool/extension, ARM/Graph and selected-storage connectivity
  checks without auto-installation, consent grants or test writes. State what
  authority can be checked read-only and what remains unproven until an
  authorized operation. Document human prerequisites and reauthentication/
  resume after consent without changing the operator's normal profile.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P01-T01 context/operation matrix plus
  P02-T01 cases for cross-tenant login, appId/object-ID confusion, existing SP
  without a writable local app, forbidden lookup, unavailable Graph/storage,
  and consent granted without sufficient directory authority. Each must stop
  before unauthorized dependent writes and emit only sanitized status.
* Decision route: Direct planner correction; no user decision required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Define recovery for the one-time secret between creation, storage and activation

* Related IDs: P01-T01, P02-T01; optional secret storage; research W1.
* Evidence: .copilot-tracking/plans/2026-10-16/one-command-entra-setup-351-plan.md:45-46,56-57
  requires explicit creation, no rerun rotation and private file transfer.
  .copilot-tracking/details/2026-10-16/one-command-entra-setup-351-phase-details.md:15
  prohibits activating a new client against an old secret.
  .copilot-tracking/research/2026-10-16/one-command-entra-setup-351-research.md:69
  states addPassword returns the secret once.
* Concern: The contract covers the happy path, but not storage denial, process
  interruption, an indeterminate addPassword response, auth-update failure or
  an existing reference of unknown client provenance. Retrying the whole setup
  can leave orphan credentials, generate another unrecoverable credential or
  treat an unrelated old secret reference as reusable.
* Impact: Broken browser authentication, accumulation of valid credentials and
  violation of the no-rotation-on-rerun promise.
* Smallest useful change: Define a staged credential state machine: verify the
  destination before creation, durably store before activation, verify
  nonsensitive configuration references, then patch/read back auth. Distinguish
  known-created credential keyId from unknown mutation outcome. Specify narrow
  cleanup of only a credential created by this invocation when safe, or a
  sanitized incomplete/manual-recovery state; never delete unrelated
  credentials or create another automatically. Do not silently switch storage
  backends. Fail closed when existing-reference/client compatibility cannot be
  established without exposing secret values.
* Action owner: Planning parent.
* Exact resolving evidence: P01-T01 transition/recovery table and stateful tests
  injecting failure before/after each create/store/activate step, including
  timeout after addPassword, an old-client reference and storage success
  followed by auth failure. Verify no activation before storage, no unintended
  credential removal/rotation and deterministic safe rerun behavior.
* Decision route: Direct planner correction; no user decision required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Specify effective SP roles and typed roster assignment semantics

* Related IDs: P01-T01, P02-T01; explicit-role roster and additive assignments;
  research C5.
* Evidence: .copilot-tracking/plans/2026-10-16/one-command-entra-setup-351-plan.md:39-44
  calls for additive manifest roles and validated userId/groupId rows.
  .copilot-tracking/details/2026-10-16/one-command-entra-setup-351-phase-details.md:13-16
  preserves role identifiers and rejects incompatible roles.
* Concern: It is unspecified how an application manifest update becomes a
  usable enabled role on the resource SP before assignment, how User-capable
  role membership is checked, and how exactly-one userId/groupId, principal
  type/tenant, conflicting duplicate rows and existing assignments are
  validated. The idempotency key for an assignment is also unstated.
* Impact: Group rows could be treated as users, disabled/incompatible roles
  could be assigned, propagation delay could cause partial assignments, or a
  matching principal with a different role could be mistaken for convergence.
* Smallest useful change: Validate the entire roster against a documented
  schema and role mapping before writes; require exactly one typed principal
  identifier and define duplicate/multi-role conflict behavior without
  inferring privileges. Resolve effective enabled SP role IDs after bounded
  propagation and stop dependent assignments if unavailable. Compare existing
  assignments by resource SP, principal and role ID. Preserve unrelated
  assignments, role IDs and existing assignment-required/admission settings;
  do not silently broaden access to make setup pass. Document that assigning
  a group does not prove every member's effective application/SQL access.
* Action owner: Planning parent.
* Exact resolving evidence: P01-T01 role/roster/assignment contract and tests
  for stale SP roles, disabled or incompatible member types, both/neither
  principal fields, wrong-type/nonexistent principals, conflicting duplicates,
  one principal with distinct explicit roles, existing unrelated assignments
  and exact-tuple no-op reruns. Invalid rosters must yield zero mutations.
* Decision route: Direct planner correction; no user decision required.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: No blind POST retry does not establish interrupted or concurrent idempotency

* Related IDs: P01-T01, P02-T01; safe reruns and additive preservation.
* Evidence: .copilot-tracking/plans/2026-10-16/one-command-entra-setup-351-plan.md:26,41,54-55
  promises safe reruns and forbids blind creating-POST retries.
  .copilot-tracking/details/2026-10-16/one-command-entra-setup-351-phase-details.md:23-24
  specifies creation followed by a normal rerun.
* Concern: The plan lacks an outcome-reconciliation rule for a mutation whose
  response is lost, and lacks protection against simultaneous read/merge/write
  updates to array-valued roles or callbacks. Sequential successful reruns
  cannot demonstrate those properties.
* Impact: Duplicate registrations/assignments or loss of unrelated changes
  despite apparently additive intent.
* Smallest useful change: Define serialized local execution and handling of
  indeterminate mutation outcomes. Re-query boundedly by stable identity
  before deciding whether creation is still needed; fail ambiguous/unknown
  results rather than recreate. Use supported conditional updates where
  available, otherwise re-read/merge and verify with an explicit conflict stop
  policy. Do not claim cross-operator concurrency guarantees without evidence.
* Action owner: Planning parent.
* Exact resolving evidence: P01-T01 reconciliation/conflict rules and fake-az
  tests for response loss after app/SP/assignment creation, interruption after
  each completed stage, same-profile overlap and an unrelated role/redirect
  change between read and patch. No duplicates or silent lost updates.
* Decision route: Direct planner correction; no user decision required.

<!-- rpi:critique id=PC-005 -->
### PC-005 [High]: Make the pending #344 auth/proxy and callback eligibility boundary explicit

* Related IDs: P01-T01/P01-T02, P02-T01; research C2/C3; preserve #344.
* Evidence: .copilot-tracking/research/2026-10-16/one-command-entra-setup-351-research.md:43-47,65-66
  describes unpublished pending edge work and Standard forwarded headers.
  .copilot-tracking/details/2026-10-16/one-command-entra-setup-351-phase-details.md:12-19
  specifies origin-linked callbacks and provider/token-store preservation, but
  does not carry forward a concrete proxy/browser-auth compatibility contract.
* Concern: It is not defined whether #351 only patches identity/credential/
  callback fields or also changes bearer/browser behavior and proxy settings.
  Associated custom domains are not necessarily enabled on an eligible route
  or ready for browser use. Absence of an eligible edge needs a safe outcome,
  not an inferred hostname or an implicit auth-mode change.
* Impact: Registration repair could overwrite #344's browser/proxy configuration
  or add redirect destinations that are merely associated, not intended active
  entry points.
* Smallest useful change: Define an auth-field allowlist and preserved-field
  matrix including exclusions, token store, unauthenticated action, proxy/
  forwarded headers and existing provider properties. Specify exact HTTPS
  callback construction from eligible origin-linked routes, enabled endpoint/
  domain associations and safe hostname/path validation. Preserve an
  explicitly pending readiness state for unready/absent edge. Keep #344's
  unpublished modules read-only; do not make #351 depend silently on them or
  claim their live behavior is accepted.
* Action owner: Planning parent, coordinating read-only with the #344 owner.
* Exact resolving evidence: P01-T01/P01-T02 patch/preservation matrix and tests
  for bearer-only and browser-enabled initial states, Standard forwarded
  headers, absent edge, disabled/unassociated domain, multiple linked routes
  and an unrelated origin. Only intended callback/identity fields may change;
  #344 pending behavior and separate browser acceptance remain explicit.
* Decision route: Direct planner correction; existing direction already
  requires preservation, not a new auth-design decision.

<!-- rpi:critique id=PC-006 -->
### PC-006 [High]: Extend privacy controls beyond raw command failures to the full login lifecycle

* Related IDs: P01-T01, P02-T01; no identifiers/emails/secrets in logs and
  isolated device-code login.
* Evidence: .copilot-tracking/plans/2026-10-16/one-command-entra-setup-351-plan.md:19,54-57
  requires private profile/file modes and disabled CLI logs/telemetry.
  .copilot-tracking/details/2026-10-16/one-command-entra-setup-351-phase-details.md:9-10
  suppresses raw failures. Research:82-88 excludes directory payloads and
  identifiers from artifacts and uses generic portal URLs.
* Concern: Successful login and az output, debug/environment inheritance,
  subprocess-launch exceptions, malformed JSON diagnostics and token-cache
  cleanup/reuse are not covered explicitly. An isolated directory is not by
  itself a guarantee that successful account JSON or a traceback stays private.
  Device-code instructions also need a defined transient interaction channel
  without persisting authentication codes in audit logs.
* Impact: Sensitive values can leak on successful paths or exceptional exits
  even when ordinary CLI failures are redacted.
* Smallest useful change: Capture all subprocess streams and emit only
  allowlisted human status. Define minimal interactive device-code presentation
  separately from persistent logs/artifacts. Clear unsafe debug/log settings
  for every invocation; protect against pre-existing unsafe profile paths;
  specify profile/token-cache retention, cleanup on normal/error/interrupted
  exit, and reuse behavior for check mode. Sanitize process errors and
  tracebacks without dumping argv, payloads, account results or filesystem
  paths containing private identity details.
* Action owner: Planning parent.
* Exact resolving evidence: P01-T01 output/profile lifecycle contract and
  capture-based tests seeding synthetic identifiers/emails/secrets in success
  stdout, stderr, malformed responses, launch exceptions and debug settings.
  Assert no marker reaches logs/artifacts; test unsafe profile paths, cleanup
  and unchanged normal CLI profile. Do not use actual private data.
* Decision route: Direct planner correction; no user decision required.

<!-- rpi:critique id=PC-007 -->
### PC-007 [Medium]: Complete the no-arguments and read-only mode state table

* Related IDs: P01-T01, P02-T01/P02-T02; no-required-arguments entry point,
  private roster and check/dry-run.
* Evidence: .copilot-tracking/plans/2026-10-16/one-command-entra-setup-351-plan.md:11,19,42-49
  specifies the entry point and no-login/no-remote-write modes.
  .copilot-tracking/details/2026-10-16/one-command-entra-setup-351-phase-details.md:16,25-27
  reports missing roster as incomplete and promises documented exit codes.
* Concern: No default private-roster location/selection rule is given. The
  behavior of check/dry-run on a fresh isolated profile, expired credentials,
  missing API/SP/edge or absent roster is unspecified. Implementers could add
  a required roster argument, log in from dry-run, manufacture empty desired
  assignments or report incomplete observation as clean convergence.
* Impact: The principal one-command requirement or read-only guarantee can
  fail despite happy-path test success.
* Smallest useful change: Define no-argument defaults and optional overrides,
  including roster path selection without scanning private datasets. Specify
  mode outcomes for converged, known drift, incomplete prerequisite and
  operational failure; distinguish unreadable/unknown state from absent state.
  In check/dry-run do not authenticate, install extensions, mint credentials or
  mutate remote state. State permitted local profile/cache effects explicitly.
* Action owner: Planning parent.
* Exact resolving evidence: CLI/default and mode/exit-code tables in P01/P02
  plus offline no-argument tests for valid/missing/legacy roster, fresh/expired
  isolated login, missing resources and forbidden reads. Fake az must record
  zero login/mutation/extension-install commands in both read-only modes.
* Decision route: Direct planner correction; no user decision required.

<!-- rpi:critique id=PC-008 -->
### PC-008 [Medium]: A single independent review must not automatically defer release blockers

* Related IDs: P02-T03.
* Evidence: .copilot-tracking/details/2026-10-16/one-command-entra-setup-351-phase-details.md:28-30
  says findings not addressed before the review route to follow-up, then
  describes staging, push and PR.
* Concern: Findings first discovered during that review necessarily were not
  addressed before it. The wording has no severity-based disposition gate and
  can route correctness, credential or authorization defects directly to
  follow-up while presenting the task as complete.
* Impact: Delivery can appear ready despite a known blocker. One review is a
  limit on independent review executions, not permission to ignore its result.
* Smallest useful change: Keep exactly one independent review. Require its
  substantive blockers to be corrected and covered by targeted tests, or
  explicitly leave delivery blocked/draft with unresolved findings recorded.
  Only non-blocking residuals may be deferred with owner and rationale. Do not
  require another independent critique or review to enact these corrections.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P02-T03 disposition gate requiring a
  finding/status/fix/test record, with PR readiness and unmet gates matching
  that record and no automatic merge.
* Decision route: Direct planner correction; no user decision required.

## Strengths and Residual Risk

* Discovery ambiguity, managed-identity sentinel handling, additive intent,
  explicit roles, no blind mutation retry and fixed-host pagination are sound
  baseline choices.
* The plan correctly distinguishes directory assignment from private SQL oid
  binding/restart and does not invent staff, roles, invitations or consent.
* Offline fake-az evidence is correctly not live tenant, browser or operational
  acceptance. DNS/certificates, Private Link approval, actual directory
  authority, consent, browser sign-in and private SQL remain separate gates.
* No finding asks for weakened network controls, automatic broad consent,
  secret rotation on rerun, private data inspection or live writes now.

## Questions or Blocking Evidence Gaps

* No significant or divergent user decision is needed for the findings above.
* The supplied research does not establish the exact operation permission
  matrix, effective SP propagation behavior or credential recovery mechanism.
  The planning parent must record bounded resolving evidence or explicitly
  retain the relevant implementation gate; this critique does not claim those
  details have already been verified.
* #344 remains unpublished pending work per supplied research. Its live
  readiness is not a prerequisite for assessing the local preservation
  contract and is not asserted by this verdict.

## Limitations

* No Azure, Graph, network, browser or private-roster access was performed.
* No source implementation or unpublished #344 worktree was independently
  inspected. Potential failures above are planning gaps, not alleged observed
  source defects or claims of proven exploitability.
* Only the caller-specified critique artifact was written. Plan, details,
  research, source, repository context and existing untracked files were not
  changed. No commit, push, PR creation or second critique was attempted.

## Recommended Next Action

* Highest-impact finding: PC-002, unrecoverable one-time credential handoff.
* Action owner: Planning parent.
* Smallest next action: Specify the create/store/activate/recover transitions
  and interruption tests, then incorporate PC-001 and PC-003 through PC-008 in
  the same direct plan revision before implementation.
* User response required: No.

| Artifact | Description |
| --- | --- |
| .copilot-tracking/plans/2026-10-16/one-command-entra-setup-351-plan.md | Supplied final-candidate plan, unchanged |
| .copilot-tracking/details/2026-10-16/one-command-entra-setup-351-phase-details.md | Supplied phase details, unchanged |
| .copilot-tracking/research/2026-10-16/one-command-entra-setup-351-research.md | Supplied research boundary, unchanged |
| .copilot-tracking/plans/2026-10-16/one-command-entra-setup-351-critique.md | This complete independent critique |

## Next Steps

The active planning parent should revise the plan/details directly against all
eight findings and record their disposition without another critique. No user
action or live Azure access is required. This critique execution stops here.
