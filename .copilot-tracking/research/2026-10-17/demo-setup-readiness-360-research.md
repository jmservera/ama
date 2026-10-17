<!-- markdownlint-disable-file -->
# Research: demo setup readiness (#360)

## Research Brief

* Date: 2026-10-17. Task identity: issue-360 / demo-setup-readiness-360.
* Purpose: converge on the simplest laptop-operated, private-network setup
  transport, then hand off a bounded implementation and actual readiness audit.
* Audience: owner, tenant operator and backlog coordinator.
* Scope: #360, #349, #350, #358 and merged #370; existing ama assets only.
* Non-goals: Graph mutation with this service principal, private datasets,
  credential fallback, new paid services, broad RBAC, public backing access,
  deleting ama or retiring anything before verified replacement.
* Criteria: one operator command; private SQL and Key Vault operations executed
  in VNet; authenticated results retrievable without private console access;
  no credentials/roster in arguments, logs or artifacts; honest human gates.
* Output mode: convergence. Research posture: focused, selected from the
  caller's named targets and supplied failure evidence.

## Research Parameters

* Evidence root: `.copilot-tracking/research/2026-10-17/`.
* Internal candidates: existing staff job/client, setup credential adapter,
  proof Dockerfile, Bicep migration/RBAC, runbook, existing tests and RPI evidence.
* External candidates: official ARM Container Apps, Key Vault and ACR APIs.
* Prior-knowledge gate: #370 is merged source, not live acceptance. Verify its
  transport and deployed prerequisites rather than treating comments as proof.
* Initial questions: Can existing jobs return bounded encrypted results through
  ARM? Can the same worker write a credential into the existing private vault
  without new services or unjustified permissions? What live actions are safe?

## Direction Controls

The caller explicitly requests the full automatic RPI loop, dated committed
artifacts and persistent completion logs. Stop after pushed PR, not a new child
loop. Existing migration/image approval is retained; role creation/assignments,
unapproved billable build paths and unclear destructive operations stay blocked.
Preserve expiry/preservation code owned by #358. No live Graph mutation by SP.

## Extension Registry and Provenance

Repository instructions and caller safety boundaries selected. RPI research,
plan, implement and review skills selected for their respective phases.
Research specialist skipped: this is one coupled transport trace, performed
inline. No web changes planned, so frontend skills do not apply.

## User Participation and Research Decisions

No interaction required: explicit full-loop direction and scope are sufficient.
Do not wait indefinitely for tenant login; record an exact human action.

## Research Cycle Log

Cycle 1, inline (no delegated worker):

1. Wider: traced #370 client/worker, setup credential writer, deployed job,
   identities, environment, ACR and monitoring. ARM job status is reachable,
   but stdout is not an ARM result API. Existing source job and AES-GCM envelope
   are reusable; adding another service is unnecessary.
2. Deeper: verified the generic ARM tags GET on the existing initializer
   (two tags); official selective Merge/Delete contract permits a bounded
   ciphertext-only relay without changing job configuration. Existing init MI
   has AcrPull/SQL administration, not tags or API restart rights. Official
   Key Vault guidance explicitly includes deployment of secrets through ARM
   templates among control-plane operations unaffected by vault firewalls.
   ARM metadata list reaches the private vault (zero secrets); use a minimal
   secureString deployment, not an undocumented direct data-plane proxy.
3. Contrarian: tried the supported ARM Log Analytics proxy with constant
   `print readiness=1`, not a dataset query. It returns
   NspValidationFailedError because workspace query public access is Disabled.
   Reject log-query fallback and do not weaken it. Reject termination-message
   extraction: no supported arbitrary result contract. Tags have a 50-tag /
   256-character value bound, so reserve bounded frames, reject oversized
   candidate results and never put keys, credentials or plaintext in tags.
   Reject source-job configuration/secret mutation and delegated operator
   tokens. Explicit source-job-only tag rights are a human activation blocker,
   not grounds to assign roles automatically.

Reflection: a laptop command is source-feasible without private endpoint access,
but not currently deployable from this host. ACR is Premium/private with bypass
None, no agent pools or tasks, and local Docker is permission-denied by caller
evidence. The formerly used public ACR task path is no longer approved/reachable.
The replacement external environment already exists and is Succeeded; no demo
API exists. Additive API migration using its retained immutable image is a
separate safe action to evaluate by exact one-resource what-if, not a reason
to redeploy the full stack/RBAC.

## Evidence Log

* C1: `infra/scripts/staff_azure.py:31` encrypts results with per-run AES-GCM;
  its current log retrieval is a private environment data-plane dependency.
* C2: `infra/scripts/staff-azure-worker.py:153` waits for live console capture.
* C3: clean topic worktree, no existing PR for this branch; main ancestor includes
  merge #370. GitHub account resolved and repository-local noreply configured.
* C4: `infra/scripts/setup-entra.py:1272` requires vault metadata data-plane
  access before credential creation; `:1321` uses `keyvault secret set`.
  Expiry selection and app secret preservation belong to #358 and stay untouched.
* C5: `infra/staff-initializer-rbac.bicep:23` defines but has not activated an
  API-scoped read/restart role; deployed role inventory confirms no such grant.
* C6: `infra/README.md:1586` requires initializer and API environments to match.
  Deployed source initializer remains in the internal environment while the
  replacement environment is external, so cross-environment transport needs
  same-VNet verification, not an unexplained guard removal.
* C7: 2026-10-17 read-only Azure inventory: backing public access Disabled;
  source proof image digest ef0058f8..., API image digest 111b2622...;
  external demo environment ready, no demo app; private ACR has no agent
  pools/tasks. No secrets/private data read, no Graph mutation.
* C8: initial local test fails importing zava_forward; install source packages
  with pip in an isolated venv before focused tests.
* W1: https://learn.microsoft.com/en-us/azure/key-vault/general/overview-vnet-service-endpoints
  (retrieved 2026-10-17), Usage scenarios note: ARM secret template deployment
  is not affected by vault firewalls. This is supported control-plane behavior,
  not enabling a trusted-service/firewall bypass.
* W2: https://learn.microsoft.com/en-us/azure/templates/microsoft.keyvault/2023-07-01/vaults/secrets
  (retrieved 2026-10-17): value write-only; attributes.exp; ARM templates are
  supported. Secure parameter values must never be outputs.
* W3: https://learn.microsoft.com/en-us/rest/api/resources/tags/update-at-scope?view=rest-resources-2021-04-01
  (retrieved 2026-10-17): selective Merge/Delete, 50 tags maximum.
* W4: https://raw.githubusercontent.com/Azure/azure-rest-api-specs/main/specification/app/resource-manager/Microsoft.App/ContainerApps/stable/2025-07-01/Jobs.json
  (retrieved 2026-10-17): supported job ARM contract, not arbitrary stdout.
* W5: https://learn.microsoft.com/en-us/azure/azure-monitor/logs/api/azure-resource-queries
  (retrieved 2026-10-17): query API permissions/partial-result limitations.
  Several guessed REST documentation URLs returned 404; replaced by official
  template reference/schema above, not represented as retrieved evidence.

## Findings Mapped to Questions and Evidence

Laptop SQL results: use existing source initializer as ciphertext-only ARM tag
relay, keep per-run authenticated envelope and terminal-status/cleanup gates.
Laptop credential write: minimal ARM secureString secret deployment and metadata
verification in the existing vault. No private-host runbook is the primary path.
Directory work stays local to the operator. Live readiness remains bounded by
image publication, scoped permission activation and real tenant login.

## Alternatives and Decision State

Selected: ARM tags relay plus secure ARM Key Vault template deployment.
Rejected: Log Analytics (live network denial), public endpoints/firewall changes
(excluded), new service/agent pool (unapproved spend), token delegation (unneeded
privilege exposure), secret/configuration result relay (needlessly broad writes).
Deferred: live publication and role activation until explicitly authorized path
exists. Preserve source initializer and every non-owned tag. Allow a parent
initializer only after proving both environments share the same ama VNet.

## Open Questions, Risks, and Residual Uncertainty

Image publication, worker permissions, migration preservation and tenant login
remain unverified. No simulated success or redirect acceptance.

## Planning Readiness

Ready for bounded implementation, not live acceptance. Research disposition:
executed, Complete. All three waves complete; no further cycle would resolve
missing authorization. Self-check: questions mapped, code/external evidence IDs,
counter-evidence and explicit boundaries recorded. Persistent Research completion
logged here on 2026-10-17; no implementation or Azure write occurred in Research.
