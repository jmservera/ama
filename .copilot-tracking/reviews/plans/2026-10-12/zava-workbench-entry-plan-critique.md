<!-- markdownlint-disable-file -->
# RPI Plan Critique: zava-workbench-entry-2026-10-12

## Metadata

* Task ID: zava-workbench-entry-2026-10-12.
* Critique date: 2026-10-12.
* Plan: .copilot-tracking/plans/2026-10-12/zava-workbench-entry-plan.md
* Phase details: .copilot-tracking/details/2026-10-12/zava-workbench-entry-phase-details.md
* Critique execution status: Complete.

## Inputs and Criterion Boundary

* Task context and caller requirements: Confirmed-automatic final-candidate critique of the
  public welcome/explicit sign-in/real own-Entra-photo account menu plan. Existing sign-in
  works and must not be replaced. No credential/device-code/token collection, storage or
  output. Tests are parent-owned, no removals, maximum 40 additions. Canonical source is
  mvp and infra. Challenge correctness, SAS bootstrap, secret-scoped RBAC/redeploy safety,
  refresh assumptions, provider prompt and projection; do not recommend broad Graph grants
  or a second sign-in system.
* Research and evidence considered:
  .copilot-tracking/research/2026-10-12/zava-workbench-entry-research.md (C1-C4, W1-W5);
  focused reads of infra/modules/containerapps.bicep, infra/modules/storage.bicep,
  infra/modules/keyvault.bicep, infra/main.bicep, mvp/zavaforward_mvp/auth.py,
  mvp/zavaforward_mvp/server.py, mvp/zavaforward_mvp/projection.py, mvp/web/app.js; and the
  current Microsoft.App/containerApps/authConfigs@2025-07-01 ARM reference fetched live from
  Microsoft Learn to verify `globalValidation.excludedPaths`, `identityProviders.
  azureActiveDirectory.login.loginParameters` and `login.tokenStore.azureBlobStorage.
  sasUrlSettingName` placement against the plan's described design.
* Decisions, dependencies and acceptance criteria considered: all Functional/Non-Functional
  Requirements, Acceptance Criteria, Phase Checklist P01-P03, Test Ownership and Candidate
  Lock, and the plan's own Critique Boundary (no broad Graph grants, no second sign-in
  system).
* Assessment boundary: This critique can confirm or refute technical feasibility against the
  current repository state and the authoritative Container Apps/Graph schemas it fetched. It
  cannot execute a live deployment, so SAS renewal job behavior, actual Container Apps
  `/.auth/refresh` semantics and real-user photo/consent acceptance remain evidenced only to
  the extent the plan itself already scopes them as human/platform acceptance gates.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| FR: root serves welcome only; /sign-in redirects; /app protected | Partial | containerapps.bicep:174-177 excludes only `/healthz`/`/readyz`; no phase task updates `globalValidation.excludedPaths` (PC-001) |
| FR: exact public exemptions, not /api | Partial | App-level exemption is planned, but platform-level EasyAuth gate is not addressed (PC-001) |
| FR: server photo endpoint via Graph /me/photo/$value only | Covered | P01 detail matches W4; auth.py/server.py show no existing photo path to conflict with |
| NFR: keyboard-operable account menu, Escape/outside close | Covered | P01 detail states native details/summary with closure handling |
| NFR: token renewal fails explicitly, never overwrites valid secret | Covered | P02 detail explicit; consistent with keyvault.bicep not declaring secret values today |
| Acceptance: shared keys disabled; private token container | Partial | storage.bicep already disables shared keys account-wide; whether this is a new container or new account is unresolved (PC-003) |
| Acceptance: renewal job least-scope RBAC (Delegator account-scope, Contributor container-scope) | Partial | storage.bicep's `roles` resource only supports account-scope assignments today; no container-scope mechanism exists yet (PC-002) |
| Acceptance: SAS bootstrap before token-store activation | Covered | Phase detail explicitly stages infra provisioning before `tokenStoreReady`; matches existing `deployApplications` staged-bootstrap precedent in main.bicep |
| Acceptance: provider prompt=select_account for fresh sign-in | Covered | Confirmed against live schema: resides at `identityProviders.azureActiveDirectory.login.loginParameters`, matching the plan's placement |
| Acceptance: 40-test cap covers UI, photo proxy and SAS lifecycle | Partial | Budget is plausible in aggregate but no stated priority if exhausted before security-critical paths are covered (PC-004) |
| NFR: refresh through supported same-origin endpoint, no silent fallback | Partial | Plan self-flags verifying platform refresh behavior but does not convert that into an acceptance test item (PC-005) |
| Contractor projection unaffected by account menu | Covered | projection.py/server.py `/api/me` already withholds extra fields for contractors; account menu reads only the existing principal-derived dict |
| Scope: no broad Graph grants, no app recreation | Covered | Plan and research both explicitly reject app-only ProfilePhoto.Read.All and registration recreation |

## Verdict

* Verdict: Revise.
* Rationale: The plan's photo/account-menu and token-store design is technically sound and
  well-evidenced against official Container Apps and Graph documentation, but the P01 welcome
  page will not satisfy its own acceptance criterion ("Anonymous live / returns 200 ... no auth
  redirect") without an explicit Bicep change that the plan currently omits (PC-001). The RBAC
  least-privilege scoping for the maintenance job also assumes a Bicep capability the
  repository does not yet have (PC-002). Both are small, bounded corrections the planning
  parent can make directly; neither requires reopening the overall design.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Critical]: Platform-level EasyAuth gate is not updated for the anonymous welcome path

* Related IDs: FR (root serves welcome only), Acceptance Criteria (anonymous live / returns
  200, no auth redirect), P01-T01.
* Evidence: infra/modules/containerapps.bicep:169-190 (`globalValidation.excludedPaths:
  ['/healthz', '/readyz']`, `unauthenticatedClientAction: 'RedirectToLoginPage'`); Microsoft
  Learn Microsoft.App/containerApps/authConfigs@2025-07-01 reference, `GlobalValidation.
  excludedPaths`: "The paths for which unauthenticated flow would not be redirected to the
  login page"; research Evidence Log C1 itself states "Current root is a workbench page, and
  ingress excludes only probes, so opening it immediately redirects to Entra."
* Concern: `excludedPaths` is enforced by the Container Apps platform before any request
  reaches the application process. The phase details (P01) describe the new public
  exemptions ("root, /welcome.html, /style.css, /zava-logo.png and /sign-in plus probes") as
  being handled "in middleware," i.e., inside the Python app, but no phase task updates
  `infra/modules/containerapps.bicep`'s `globalValidation.excludedPaths`. With
  `unauthenticatedClientAction: RedirectToLoginPage` unchanged, an anonymous browser request
  to `/` will still be intercepted and redirected to Entra by the platform itself, before the
  new welcome page or app-level middleware ever runs.
* Impact: Direct failure of the stated acceptance criterion ("Anonymous live / returns 200
  with name/logo/button and no auth redirect ... Public logo/styles load") on first deploy;
  the public assets (`/welcome.html`, `/style.css`, `/zava-logo.png`) would also 302 for
  anonymous users even though P01 adds them as static exemptions in app code.
* Smallest useful change: Add a P01 (or P02 infrastructure) task line explicitly updating
  `containerapps.bicep`'s `apiAuth.properties.globalValidation.excludedPaths` to include `/`,
  `/welcome.html`, `/style.css`, `/zava-logo.png` and `/sign-in` alongside the existing probe
  paths, keeping `/api/*` and `/app` out of the list.
* Action owner: Planning parent.
* Exact resolving evidence: Updated `excludedPaths` array in
  infra/modules/containerapps.bicep plus a P03 deployed-environment check that anonymous `GET
  /` returns 200 without a redirect `Location` header, matching the existing acceptance
  criterion's wording.
* Decision route: Direct planner correction (no user decision needed; the fix only extends an
  existing, already-approved exemption list to the paths the user already asked to be
  public).

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Container-scoped RBAC for the renewal job has no existing Bicep mechanism

* Related IDs: Acceptance Criteria (shared keys disabled; private token container),
  Non-Functional Requirements, P02-T01.
* Evidence: infra/modules/storage.bicep:81-89 (`roles` resource:
  `scope: account` for every entry in the `roleAssignments` array, i.e., account-wide only);
  phase detail P02: "Give a separate maintenance identity Storage Blob Delegator at account
  scope and Blob Data Contributor only on auth-tokens [container]."
* Concern: The repository's only existing storage role-assignment pattern grants roles at the
  whole-account scope. There is no container-scoped `roleAssignments` resource today. Giving
  "Blob Data Contributor only on auth-tokens" as planned requires a new Bicep resource scoped
  to the specific container child resource (e.g., `scope: blobContainers[<index>]`), which the
  phase details do not call out as a concrete authoring task. Without this explicit
  instruction, the path of least implementation effort is to reuse the existing account-scope
  array, granting the maintenance identity Blob Data Contributor on the whole account
  (including `evidence`, `imports`, `quarantine`, `exports`, `audit-archive`) rather than the
  intended least-privilege "auth-tokens only" scope.
* Impact: Silent privilege-scope regression relative to the plan's own least-privilege
  requirement if implemented via the existing pattern; the maintenance identity would gain
  write access to unrelated evidence/import containers.
* Smallest useful change: Add an explicit P02 phase-detail instruction (or a dedicated task)
  to author a container-scoped `roleAssignments` resource (new symbolic resource with `scope:
  blobContainers[<auth-tokens index>]`), separate from the existing account-scope
  `roleAssignments` array, for the Blob Data Contributor grant; keep Storage Blob Delegator at
  account scope as already planned.
* Action owner: Planning parent.
* Exact resolving evidence: A new container-scoped role assignment resource in
  infra/modules/storage.bicep (or a sibling module) visible in the Bicep diff, plus a Bicep
  `what-if`/build check confirming the maintenance identity's only storage grants are Storage
  Blob Delegator (account) and Blob Data Contributor (auth-tokens container).
* Decision route: Direct planner correction.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: "Token account/container" wording leaves account-vs-container scope unresolved

* Related IDs: Acceptance Criteria (shared keys disabled; private token container), P02-T01.
* Evidence: Phase detail P02: "Create a private, dedicated token account/container with shared
  keys disabled..."; infra/modules/storage.bicep:16-40 (existing storage account already sets
  `allowSharedKeyAccess: false`, private networking and a fixed `containers` list of
  `['evidence', 'imports', 'quarantine', 'exports', 'audit-archive']`).
* Concern: "account/container" reads as an either/or left to the implementer. A new,
  dedicated storage account is materially larger scope than a new container in the existing,
  already-hardened account (it would need its own private endpoint, DNS zone registration,
  diagnostics and zone-redundancy parameters mirroring the existing pattern), which affects
  effort, the 40-test budget and whether existing storage module parameters need new wiring
  in main.bicep. The existing account already satisfies "shared keys disabled" and private
  networking, so a same-account container is the simpler, consistent choice unless there is an
  undocumented isolation reason for a separate account.
* Impact: Ambiguity could cause over-scoped implementation (new account, new private endpoint,
  new DNS zone) that is harder to review and exceeds the intended "small maintenance job"
  footprint the plan otherwise describes.
* Smallest useful change: State explicitly in P02 that the token store is a new `auth-tokens`
  container added to the existing storage account's `containers` list (matching the pattern of
  `evidence`/`imports`/etc.), not a new storage account, unless the user has a specific reason
  to isolate it further.
* Action owner: Planning parent, with a brief user confirmation only if full account isolation
  is actually desired.
* Exact resolving evidence: Phase detail P02 naming the exact container host (existing account
  name) and the new container name, matching the Bicep diff.
* Decision route: Direct planner correction; escalate to a user decision only if the user
  specifically wants token storage isolated in its own account.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: No stated priority order if the 40-test cap is reached before security-critical paths are covered

* Related IDs: Test Ownership and Candidate Lock, Acceptance Criteria (SAS bounds,
  failure/preservation, no credential output; server photo success/failure), P01-T02, P02-T02,
  P03-T01.
* Evidence: Plan's "Test Ownership and Candidate Lock" section: "Maximum 40 additions across
  MVP/API/auth, photo and renewal tests."; P01/P02 phase details enumerate keyboard/menu
  behavior, photo proxy status/error branches (missing token, consent/expiry, network/type
  errors), SAS bound/failure/preservation and no-credential-output as all needing coverage.
* Concern: The combined surface (UI accessibility, server photo proxy branches, SAS lifecycle
  and failure modes, Bicep build) is wide relative to a shared 40-addition budget across three
  phases. The plan does not state which tests are expendable or deferrable if the budget is
  reached first on cosmetic/UI assertions, risking under-coverage of the higher-risk auth and
  credential-handling paths (SAS bound enforcement, failure non-overwrite, redacted job
  output) that the acceptance criteria treat as hard requirements.
* Impact: A technically compliant but thin test suite could pass review while leaving the
  security-sensitive SAS/credential paths under-verified, which is precisely what this
  critique was asked to challenge.
* Smallest useful change: Add one sentence to the Test Ownership section (or P02-T02)
  prioritizing SAS-bound/failure/no-credential-output and photo-proxy error-branch tests ahead
  of cosmetic UI assertions within the 40-addition cap.
* Action owner: Planning parent.
* Exact resolving evidence: Updated plan/phase-detail text naming the priority order; the
  implemented test list showing SAS/credential/photo-proxy error cases present even if the
  40-addition cap is reached.
* Decision route: Direct planner correction.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Low]: Container Apps refresh behavior assumption is not converted into an acceptance test

* Related IDs: Non-Functional Requirements ("Refresh through the supported same-origin
  endpoint at most once; do not fall back silently"), P02.
* Evidence: Research W5 (learn.microsoft.com/.../configure-authentication-oauth-tokens,
  retrieved 2026-10-12) documents the token refresh contract for App Service; phase detail P02
  states "Use versionless Key Vault reference for rotation; check actual platform refresh
  behavior before relying on it," self-flagging the gap.
* Concern: The plan already recognizes that the authoritative source (W5) is an App Service
  document and that Container Apps' actual refresh endpoint behavior needs confirming, but
  this remains a narrative caveat rather than a concrete acceptance-test or verification step
  in P03.
* Impact: Low on its own, since the plan's fallback stance (explicit error, no silent retry)
  is already the safe default regardless of what the platform does; but without a concrete
  check, a wrong assumption about the refresh endpoint could pass unnoticed until a real user
  hits an expired token in production.
* Smallest useful change: Add one P03 verification line: during the real live-environment
  check, exercise an expired/near-expiry delegated token path (or inspect the deployed
  authConfig/platform docs for Container Apps specifically) and confirm the photo endpoint's
  observed behavior matches the "refresh once, explicit error on failure" contract before
  calling P03 complete.
* Action owner: Planning parent (Implement-phase verification step), not a new user decision.
* Exact resolving evidence: P03 verification notes recording the observed refresh behavior
  against the implemented fallback logic.
* Decision route: Direct planner correction.

## Strengths and Residual Risk

* The staged `tokenStoreReady` activation pattern mirrors the repository's existing
  `deployApplications` staged-bootstrap precedent (infra/main.bicep:35-36) and is reinforced
  by the fact that neither `entra-client-secret` nor any other secret value is declared inside
  the Bicep modules today (infra/modules/keyvault.bicep has no `secrets` child resource) — so
  the plan's "never reset a secret on redeployment" goal is already consistent with how this
  repository manages secret values (via out-of-band scripts/jobs, not Bicep).
* The plan's rejection of ID-token picture claims, app-only `ProfilePhoto.Read.All`, shared
  key re-enablement and browser-exposed `/.auth/me` tokens are all independently corroborated
  by the fetched Graph/Container Apps documentation; no broader-than-necessary Graph grant is
  proposed.
* `prompt=select_account` is correctly placed at
  `identityProviders.azureActiveDirectory.login.loginParameters` per the live ARM schema,
  matching the plan's design exactly.
* The existing contractor projection (`projection.py`, `/api/me`) already withholds
  non-contractor fields; the planned account-menu read path does not appear to introduce a new
  leak surface.
* Residual, explicitly accepted risk: real-user photo/consent acceptance is correctly scoped
  as a human acceptance gate outside automated testing, and the plan already states this
  cannot be fabricated.

## Questions or Blocking Evidence Gaps

* None that block planning; PC-001 and PC-002 are concrete, evidence-backed corrections the
  planning parent can apply directly without new user input.

## Limitations

* This critique did not execute a deployment or run the renewal job; SAS-bound enforcement,
  actual Container Apps refresh-endpoint behavior, and real-user Graph photo/consent
  acceptance remain verifiable only at implementation/deployment time, as the plan itself
  already acknowledges.
* Source review was focused on the files the plan/phase-details/research name plus the
  specific Bicep modules needed to verify RBAC and auth-gate claims; it did not re-review
  unrelated pre-existing code paths outside this task's scope.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add an explicit `containerapps.bicep` `globalValidation.excludedPaths`
  update (covering `/`, `/welcome.html`, `/style.css`, `/zava-logo.png`, `/sign-in`) to P01 (or
  a P02 infrastructure task), then re-confirm the P03 anonymous-root acceptance check reflects
  "no redirect" against that updated exclusion list.
* User response required: No. All findings are direct planner corrections; PC-003 only needs a
  brief user confirmation if full storage-account isolation (rather than a new container in
  the existing account) is actually wanted.

## Related Files

| File | Description |
|---|---|
| .copilot-tracking/plans/2026-10-12/zava-workbench-entry-plan.md | Plan under critique |
| .copilot-tracking/details/2026-10-12/zava-workbench-entry-phase-details.md | Phase details under critique |
| .copilot-tracking/research/2026-10-12/zava-workbench-entry-research.md | Supporting research and evidence log |
| infra/modules/containerapps.bicep | Current EasyAuth `globalValidation`/`identityProviders` configuration (PC-001, PC-003 context) |
| infra/modules/storage.bicep | Current account-scope-only role-assignment pattern (PC-002, PC-003) |
| infra/modules/keyvault.bicep | Confirms no Bicep-declared secret values (supports Strengths) |
| mvp/zavaforward_mvp/auth.py | TrustedProxyProvider principal/role/oid handling referenced by P01 account metadata |
| mvp/zavaforward_mvp/projection.py | Contractor field-withholding referenced by P01 account metadata note |

## Next Steps

Return this verdict (Revise) and the two highest-severity findings (PC-001, PC-002) to the
`rpi-plan` planning parent for direct correction; no user decision is required to proceed
except the brief PC-003 confirmation noted above. No further critique pass is requested.
