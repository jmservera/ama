<!-- markdownlint-disable-file -->
---
title: Existing-resource Key Vault preservation research
description: Original focused research for issue 358 management-plane acceptance
ms.date: 2026-10-19
---

## Research Brief

Execute the remaining literal existing nonproduction resource preservation
criterion, or establish an exact permission/application-safety blocker.
Audience: owner and independent coordinator. Output mode: convergence.
Resolved evidence root: `.copilot-tracking/research/2026-10-19/`.
Task identity: issue-358-live-preservation, slug live-keyvault-preservation-358.
Base: 7f96d9957b28cb174aa759c842376f24087d71a3.

## Research Parameters and Direction Controls

Focused posture selected from the owner's bounded source/resource task.
Read complete issue/comments and merged #374; do not repeat offline delivery.
Investigate real helper/payload, current demo metadata, ARM authority, revision
and restart effects. Existing RG ama only; never delete RG. No Graph,
credential rotation, user/private data, browser login, image publication,
SQL write, restart/traffic/identity change or private-service weakening.
No secret/token/plaintext output. Private operator files must be external0600.
The owner explicitly requests the entire ordered RPI loop, including original
independent critique before writes and one original independent Review.

## Extension Registry and Participation

Repository instructions, infra/src guides and RPI research protocol selected.
RPI plan/implement/review will be activated only at their corresponding phases.
Architecture/security/web design skills skipped: no architecture redesign,
vulnerability assessment or web edit requested. Research performed inline
because the helper/resource safety investigation is one continuous trace.
No interaction needed: scope and authority supplied explicitly.

## Questions and Candidate Areas

1. Does the production existing-resource secret operation require Graph/images?
2. Is this actual existing app nonproduction, and what reference/binding/revision
   metadata can safely establish a before/after invariant?
3. Can the identical operation run without revision/restart/identity/traffic
   mutation, and does current authority permit it?
4. What smallest reversible operation and readback proves the literal criterion?

Internal candidates: setup-entra.py and tests, existing dated issue evidence,
infra/src guides and cutover evidence. External candidates: Azure Container Apps
ARM schema, secrets/revision documentation and current ama management metadata.

## Research Cycle Log

### Cycle1 Wider (2026-10-19)

Read live issue body and both comments, merged #374 implementation description,
repository instructions, case-study original and relevant addendum context,
KB index/memory and infra/src guides. Traced the real production helper and
its setup caller. Read existing runbook and offline acceptance audit.
Current CLI account reports servicePrincipal, AzureCloud, Enabled.
RG app-list and demo-show projections report all three existing apps with
`configuration.secrets: null` and zero container environment secretRef bindings.
Demo tags establish test/non-production-demonstrator/constructed-non-identifying;
the keyvault store tag alone is NOT an existing Key Vault reference.
Demo auth projection has no clientSecretSettingName and tokenStore disabled.

Reflection: Graph is required for a replacement browser credential in
secret_reference, but not for preserve_app_secrets or an identical ARM
configuration-only PATCH. Conversely, the literal criterion cannot be proven
vacuously on an app without pre-existing references. Prioritize raw versioned
ARM GET to exclude CLI projection/normalization as an explanation before
deciding whether any write is appropriate.

### Cycle1 Deeper (2026-10-19T14:19:11Z)

Imported unchanged setup-entra.py and used its real Azure.rest GET boundary at
its own API_VERSION=2025-07-01 for each of the three exact existing apps.
The first standalone metadata projection failed locally on null initContainers,
before producing any summary; no Azure mutation occurred. Corrected only that
read-only projection and reran through the production Azure class.
All three raw ARM configurations explicitly contain `secrets: null`, not an
omitted field. Each has zero KV pairs, environment/init-container secretRefs,
scale-auth secretRefs and registry passwordSecretRefs. Both APIs have zero
auth client-secret refs and disabled token stores/no SAS binding. The agents
auth GET failed with sanitized AzureError kind=request; no inference that it
has an auth configuration is made.

At each exact app scope, ARM permission metadata allows read, write and
listSecrets/action. This is evidence against assuming an RG-authority blocker,
not proof of PATCH/provider/policy success; neither listSecrets nor PATCH ran.
All apps report provisioning Succeeded, latest==latestReady; no auth advisory
lock/handoff tag or explicit deployment-profile tag is present.
The demo's labels identify nonproduction intent, not a completed require_demo
profile assessment or proof of populated auth storage.

External sanitized session record, directory0700/file0600:
`/tmp/issue-358-live-preservation-20261019-1416/research-management-summary.json`.
No raw app response, ID, token, secret or env value was saved.

Reflection: the exact blocker is missing existing secret/reference/binding
inventory, not established missing Graph/image capability. An empty-array
same-configuration PATCH would exercise ARM but cannot prove preservation of
an actual keyVaultUrl/identity pair alongside unrelated secrets and bindings.
It has no acceptance value and would introduce unnecessary update risk.

### Cycle1 Contrarian (2026-10-19)

Challenged CLI omission: same null inventory confirmed with real production
Azure.rest/raw service API rather than only extension-normalized show/list.
Challenged demo-only absence: both other existing RG apps are also empty.
Challenged presumed permission denial: exact app-scoped permissions metadata
allows all three required operations, subject to unexecuted provider/policy checks.
Challenged harmless-update assumption: official PATCH is JSON Merge Patch and
may return202; no-value-change is not a platform guarantee against update work.
Official secret guidance excludes secret edits from new revisions, but warns
versionless KV refresh can automatically restart active secret-ref revisions.
No versions, secret values, revision restart or traffic mutation were tested.

Rejected: call full setup (unnecessary Graph/password/runtime/SQL/restart);
PATCH an empty inventory (vacuous criterion); add sentinel secrets/references
or bindings (changes configuration and may require a new revision rather than
same-configuration preservation); clone (not literal existing-resource proof).
Do not invent an ARM/Graph permission failure from an unexecuted write.

Parent synthesis: one focused cycle covers all decision-relevant questions.
No further source can conjure absent existing KV pairs. Stop read-only live
research and plan a bounded no-write implementation/evidence disposition.

## Evidence Log

Initial provenance: live issue #358 body and both owner comments retrieved
2026-10-19; merged PR #374 body/files read. The current comment's broad
image/Graph dependency is a claim to test, not assumed prerequisite.

* C1: infra/scripts/setup-entra.py:1396-1418, preserve_app_secrets reconciles
  configured metadata and listSecrets; no Graph/image call.
* C2: infra/scripts/setup-entra.py:1463-1589, secret_reference's mutating rebuild
  unconditionally creates a Graph password before storage/PATCH; its reuse path
  returns before rebuilding. Do not bypass its guards or pretend full setup ran.
* C3: infra/scripts/setup-entra.py:1576-1584, production payload merges the
  existing configuration with preserved and new secrets, not template/identity.
* C4: infra/scripts/setup-entra.py:1690-1925, full setup includes directory
  reconciliation, runtime template update and SQL/restart; it is broader than
  this authorized preservation-only check.
* C5: docs/architecture/cutover-evidence-pack.md:111-154, offline proof and
  literal live existing-resource criterion remain distinct.
* W1: https://learn.microsoft.com/en-us/azure/container-apps/manage-secrets
  retrieved2026-10-19: secrets are application-scoped, edits do not create
  revisions and do not automatically affect existing revisions; versionless
  KV rotation remains a separate behavior requiring scrutiny.
* W2: attempted Learn REST update URL with 2025-07-01 view returned404;
  not treated as schema evidence.
* W3: https://raw.githubusercontent.com/Azure/azure-rest-api-specs/main/specification/app/resource-manager/Microsoft.App/ContainerApps/stable/2025-07-01/ContainerApps.json
  retrieved2026-10-19, ContainerApps_Update: JSON Merge Patch,200/202 and
  long-running-operation semantics.
* W4: W1, Key Vault secret URI and secret rotation: unversioned refs retrieve
  newer versions within30minutes; env-secretRef active revisions auto-restart.
* W5: dated current ARM metadata in external sanitized record above, produced
  by unchanged production Azure.call/rest methods, not a mock/proxy payload.

## Findings, Alternatives and Decisions

Evidence-backed findings: ARM-only management secret rebuild is independently
possible in principle (C1/C3/W3), without images or Graph when no new credential
is being created. The full production secret_reference mutation is not that
operation (C2/C4); it must not be invoked with fabricated registration/password.
No eligible populated existing target currently exists among the RG's apps.
All actual KV-reference, unrelated-secret and secretRef counts are zero (W5).
Owner authority is not the missing condition. Actual literal live criterion
remains UNMET / Not run.

Future minimal approach, conditional on a genuine populated eligible target:
fresh configuration/listSecrets privately -> preserve_app_secrets -> same
configuration-only production Azure.rest PATCH -> exact metadata/value
comparison and stable revision/traffic/identity readback. This is a bounded
component exercise, not secret_reference/full setup. The exact future payload,
rollback and guards require fresh original plan/critique for that actual target.
It is not executed or represented as proven here.

## Planning Readiness

Ready for a no-write evidence disposition only, not for a live preservation
PATCH. Research disposition: executed, complete. Live blocker B1: no existing
KV references, unrelated secrets or app secretRef bindings on available targets.
Resolution: supply an actually populated already-authorized eligible target,
or separately scope/approve creation of representative state; do not create it
merely to convert this same-configuration check into a passing claim.
No source defect demonstrated; #374 source/tests remain unchanged.

### Final profile qualification (2026-10-19T14:20:43Z)

Executed unchanged production require_demo(cli, actual_demo_app) read-only,
without roster generation or setup. It returned SetupError:
"Demo deployment template/parameters are unknown or malformed; verify readable
deployment history before generating a roster."
External sanitized result: same operator directory, `profile-summary.json`
(0600). Thus test/demo tags are not sufficient for positive guarded profile
acceptance. This guard belongs to automatic roster eligibility; it is not
invented as a universal prerequisite for ARM preservation-only PATCH. No guard
was disabled or bypassed. B1 remains independently decisive even if this
separate profile-evidence uncertainty is resolved.

## Owner-Selected Supplemental Research (2026-10-19)

Same task, identity, branch and supplied base; automatic continuation explicitly
selected. The inherited uncommitted delivery is retained, not discarded or
relocated. Original research and no-write outcomes above are historical.
Original critique and original Partial / Residual Review remain immutable;
supplemental work cannot relabel either verdict.

Focused convergence brief: establish provider requirements for a real temporary
nonproduction Container App baseline in an existing ama environment before its
preservation roundtrip. No existing workload/identity/template modification,
ingress, traffic, real secret read, Graph credential creation, public networking,
policy bypass, image publication or RG deletion. Synthetic values must never
appear in logs or committed evidence. Record exact owned inventory externally
0600 with source, owner, expiry and absence checks before allocation.

Questions: can a resource-native private-vault synthetic secret write avoid an
unavailable local data-plane path; what existing authorized private environment
and digest image can support a zero-replica app; what scoped identity/role is
actually needed for validated KV resolution; what proves asynchronous readback,
value/reference/binding preservation and exact cleanup without workload changes?
Unused binding is conditional, never an existing-app change or arbitrary job
payload. A dangling reference is not acceptance.

Extensions: same repository/RPI rules and production helpers selected. Inline
focused investigation is one continuous trace. Independent assessment is reserved
for the new lifecycle/safety plan, as expressly requested, not repeat critique
or repeat original Review. No user interaction is needed; authority and selected
scope were supplied. Publication remains forbidden pending coordinator review.

Cycle2 opening: wider inventory/provider research, deeper exact private path and
production boundary, then contrarian lifecycle/acceptance challenge. Readiness
pending actual evidence; no resource allocation authorized by this opening.

### Cycle2 Wider

S-C1: infra/scripts/credential_arm.py:42-180 already uses secureString incremental
ARM deployment for a new secret in an existing private RBAC vault, rather than
requiring local data-plane connectivity. Its fixed credential naming/Graph
context is not reused or bypassed for this synthetic baseline.
S-W1: https://learn.microsoft.com/en-us/azure/templates/microsoft.keyvault/2024-11-01/vaults/secrets
retrieved 2026-10-19 documents value write and versioned secretUri metadata;
management GET never returns the secret value.
S-W2: https://learn.microsoft.com/en-us/azure/container-apps/manage-secrets
retrieved 2026-10-19 requires an attached MI with actual secret-read authority;
versioned URI avoids background latest-version rotation. Secrets are app-scoped.
S-W3: https://learn.microsoft.com/en-us/azure/container-apps/scale-app and
https://learn.microsoft.com/en-us/azure/container-apps/billing, retrieved
2026-10-19: min0, max1, no ingress/trigger permits scale-zero, not a guarantee
that provisioning never executes a replica. No running replica means no app
consumption charge; existing private-service costs do not disappear.

Reflection: prefer existing internal private Consumption environment, not the
demo environment with publicNetworkAccess Enabled. The selected app itself has
no ingress. Existing private API image is already digest-pinned; no image build
or publication is needed.

### Cycle2 Deeper

Actual production Azure.rest preflight at 2026-10-19T14:41:45Z checked exact
planned app, identity, job and vault-secret IDs absent. Exact deployment GET
returned DeploymentNotFound, which production AzureError categorizes as request;
deployment-list metadata independently confirms absence. No source fix is
justified for that operator diagnostic classification.
External inventory and metadata: /tmp/issue-358-synthetic-20261019-1450,
directory0700/files0600. Before snapshot covers all11 current apps/jobs, their
configuration/template/identity/tags, revision readiness and active revisions.
Existing private environment, Standard RBAC vault (public Disabled, bypass None),
private registry, approved private endpoint and completed DNS link were checked.
Role-assignment write/delete and native-secret-write permission metadata permits
the scoped operations; actual provider acceptance remains untested.

S-W4: https://raw.githubusercontent.com/Azure/azure-rest-api-specs/main/specification/keyvault/resource-manager/Microsoft.KeyVault/KeyVault/stable/2024-11-01/secrets.json
retrieved 2026-10-19: secret management paths expose PUT/PATCH/GET/list, not DELETE.
S-W5: https://learn.microsoft.com/en-us/rest/api/keyvault/secrets/delete-secret/delete-secret?view=rest-keyvault-secrets-2025-07-01
retrieved 2026-10-19: secret deletion is vault data plane and all-version scoped.
Provider operation metadata independently marks secret delete/purge as data
actions. The seven-day soft-delete policy is retained, not weakened.
Authenticated local exact-synthetic-name list-versions failed Forbidden with
network-denial text; local DNS is nonprivate, and direct existing private endpoint
TCP443 timed out. The initial unauthenticated401 was not evidence of access.

Reflection: native creation alone would strand cleanup without a private
data-plane route. Establish that route before creating any vault secret.
Existing initializer/MI HTTP jobs have zero running executions. Reusing their
start override or existing workload exec would risk their identities/spec and
is rejected. A new uniquely owned manual cleanup job, fixed synthetic-only
metadata/delete code, is the smallest isolated route to test.

### Cycle2 Contrarian

S-W6: https://learn.microsoft.com/en-us/azure/container-apps/jobs (2026-10-19)
confirms jobs share the environment's network and start overrides can expose
existing job secrets/identities; do not reuse an existing job. A new owned job
can run only bounded preflight/cleanup at0.25vCPU/0.5GiB, timeout120/retries0.
S-W7: https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide
(2026-10-19) permits individual-secret RBAC scope; a dedicated temporary identity
with Secrets Officer over the single synthetic secret, and AcrPull only over
the existing registry, touches no real secret and modifies no existing identity.
Officer is required for deletion; Secrets User alone cannot clean up.

Challenge: app provisioning success alone need not prove usable KV resolution.
Require actual synthetic resolution evidence (provider success plus synthetic
listSecrets value comparison if returned; otherwise explicitly qualify it).
Require an exact unrelated synthetic value hash before/after, not just counts.
An unused env secretRef binding may exist only on the new app, at creation,
pointing to the unrelated synthetic value; no real-app/template change.
Creation is not preservation: wait for a real successful baseline, then freshly
GET/listSecrets -> unchanged production preserve_app_secrets -> production
Azure.rest configuration-only PATCH -> terminal async readback and exact
configuration/template/identity/tags/revision/binding checks.

Parent synthesis: Research executed, focused three-wave cycle complete.
Ready for a conditional lifecycle plan with an independently assessed gate:
preflight the temporary private cleanup job before any synthetic secret write;
stop and clean only owned allocations if provider/network/RBAC fails. Native
secret creation/validation is a real provider test, not assumed success.
No source defect demonstrated. Synthetic baseline roundtrip is representative
real-resource component evidence, not originally populated deployed-app/full
secret_reference/setup acceptance. Original criterion and issue closure remain
for coordinator judgement; no automatic stronger acceptance is authorized.

Original immutable SHA256 anchors:
Review 5fb39b9ef7b3aac4cbef810019eb1db23d6890b3c74d0baaf98059c75f9df41b;
critique c4e1e226080ba9210ee0b7daac32d34e61bb50533874203b4415ffa805aea121.

## Supplemental Observed Outcome and Readiness

The conditional provider hypotheses were actually tested after new-material
safety assessment, not assumed from documentation. Secret-scoped assignment
before existence succeeded; the new private job resolved the exact empty
versions200/deleted404 metadata route. Native secure ARM deployment produced
a real enabled expiring versioned secret. The real baseline Succeeded before
actual production helper and Azure.rest configuration PATCH. Async InProgress
then Succeeded, exact reference/both synthetic values/binding/config/template/
identity/tags/revision comparisons all passed. Cleanup including active/deleted
secret and all ten historical role IDs is verified. All11 existing workloads
and RG membership/backing hashes match. No source/helper defect demonstrated.

Contrarian qualification confirmed: min0 still yielded one provisioning replica;
actual runtime is not zero cost. The originally populated deployed-app case
was not exercised. Original Partial / Residual Review and exact hashes stay
unchanged. Sanitized primary in-worktree execution summary makes actual
observations readable to the coordinator without exposing private inputs.
Supplemental research disposition executed/complete, readiness satisfied for
this bounded component evidence; original criterion/issue closure and frozen
publication gates remain independently assessed, not inferred.
