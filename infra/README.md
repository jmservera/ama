---
title: Azure Infrastructure (Bicep)
description: Bicep deployment of the proposed Zava Forward demonstrator Azure architecture
author: AMA programme
ms.date: 2026-10-30
ms.topic: how-to
---

Proposed, non-production infrastructure. The design and its rationale are in
[ADR 0001](../docs/adrs/0001-azure-architecture.md).

The [executive and technical Excalidraw views](../docs/architecture/README.md)
map these sources and the current ADR 0002 exercise realization. They
distinguish working API assistants from placeholder workers, configured
dependencies from observed proof, and development access from the intended
private production profile. They do not authorize deployment.

## Layout

* `main.bicep`: resource group scope entry point wiring all modules.
* `main.bicepparam`, `main.test.bicepparam`, `main.pilot.example.bicepparam`: dev, test and pilot parameter sets (see [Environments](#environments)); replace the marked placeholders.
* `modules/`: identity, network (VNet, NSGs, private DNS), monitoring (Log Analytics, App Insights, AMPLS), Key Vault, storage, registry, SQL, Foundry, IoT Hub, Container Apps and the generic private endpoint.
* `role-assignments.json`: role-assignment matrix; `entra/app-registration.json`: declarative Entra registration and owners. Both are checked by `tests/test_identity_rbac.py`.
* `scripts/create-sql-users.sql`: contained SQL users for the managed identities. `scripts/create-sql-users.py` runs the same grants idempotently from the Azure CLI login.
* `scripts/create-api-app-registration.sh`: Entra app registration, app roles and secret (Key Vault) for API sign-in.
* `scripts/setup-entra.py`: direct-demo or optional edge discovery, additive Entra registration/roles, private-roster assignments and auth wiring.
* `scripts/initialize-api-auth.py`: compatibility CLI forwarding to `setup-entra.py`; its callback-only Python API is retained for existing importers.
* `scripts/initialize-workbench-staff.py`: private tenant-member/app-role/SQL binding reconciliation, with idempotent checks and serving-replica restart.
* `scripts/configure-m365-provisioner-app.sh`: delegated Graph permissions for the app the m365 CLI uses to set up SharePoint and Teams.
* `scripts/grant-sharepoint-access.sh`: optional Graph `Sites.Selected` grant for the SharePoint evidence store.
* `scripts/deploy.py`: image-preserving infrastructure what-if/deploy wrapper; see [Orchestrator image selection](#orchestrator-image-selection-322).
* `scripts/private-cutover-proof.py`, `cutover-proof.Dockerfile`: bounded
  synthetic SQL/private-ingress proof inside the ama VNet and explicit public
  direct-ingress acceptance probes.
* `public-edge-existing.bicep`: additive Front Door Premium/WAF/Private Link
  for an existing internal, authenticated API; preserves data-service settings.

Optional parameters: `teamsWebhookUrl`, `evidenceStore`, `sharePointSiteId`, `monthlyBudget`. See the M365 section of the ADR.

## SQL tier and recovery (Refs #145)

SQL tier, auto-pause, vCores, backup redundancy and retention are `sql*` parameters; the pilot example records the provisioned tier. The restore and ledger verification procedure, undecided objectives and unperformed evidence are in [sql-recovery-runbook.md](sql-recovery-runbook.md).

## Monitoring Authoring Candidate (Refs #146)

The [operator runbooks and issue gap matrix](./monitoring-runbooks.md) catalogue
existing rules/budget notifications and new disabled job/IoT alert candidates.
The [workbook source](./monitoring-workbook.json) provides aggregate
request/error/p95 and availability-test query panels, with configured budget
separate from Unknown actual cost and missing AI usage/reconciliation.
`operationsWorkbookId` is the resource output; no deployment, portal rendering
or operating acceptance is claimed.

Both telemetry queries union the bare table reference with a typed empty
datatable before projecting fields, so an absent table can use the fallback
schema and report Insufficient. `tests/test_monitoring_workbook.py` checks this
source shape for both panels; it does not execute KQL against Azure.

`enableCandidateMonitoringAlerts` defaults false. Even true keeps candidates
disabled when `monitoringApprovalReference` is empty/whitespace; a nonempty string
is not proof of actual named-human approval. Actual primary/backup owners,
thresholds/windows/recipients, privacy exclusion, safe signal producers and
notification/suspension drills remain activation gates. Existing alerts are not
reapproved or disabled by this switch. The budget notifies above 80 percent
actual and 100 percent forecast; it is not a hard cap or AI dispatch control.
This source-only delivery uses Refs #146 and does not close its criteria.

## Deploy

### Bounded Private Publisher Capacity Attempt (2026-10-19, Refs #360)

The owner now authorizes necessary resource operations inside existing `ama`,
except deletion of the group itself. This supersedes the earlier missing
publication-route resource authority, **not** the earlier failures or remaining
technical/human gates. Production defaults and private backing constraints
remain unchanged. The complete current issue/comments and #349/#358 were read;
their earlier deliveries were not repeated.

Fresh management reads found Premium ACR in UK South, public access Disabled,
bypass None, dedicated data endpoint enabled, no agent pool and no existing
publisher VM in `ama`. The initializer still uses old proof digest
`ef0058f8f380cc610d4b7113509293b3ed624d22afac95e807b4c69a4266dc72`;
demo API still uses
`111b26226cad06e229bcf1c3174877510c4c68c5a5fefc885167a2b4c821657d`.
No source-bound fresh worker image or initializer activation was achieved.

| Actual check on 2026-10-19 | Result and limit |
| --- | --- |
| Private ACR task pool support | Official preview region list omits UK South; no pool created or unsupported cross-region subnet assumed |
| B2s current SKU | `NotAvailableForSubscription`; nominal quota/legacy size listing is not deployability |
| B2als_v2 and D2as_v5 SKU/quota | Both unrestricted in SKU GET; respective family usage0/limit100; image Ubuntu Jammy x64 Gen2 `22.04.202610170` available |
| Exact B2als_v2 provider preflight | `InvalidTemplateDeployment / SkuNotAvailable`, capacity restriction |
| Exact D2as_v5 provider preflight | Same capacity restriction; neither yielded a successful what-if change list |
| Resource allocation/assignment | Not attempted after preflight refusals; zero owned resources and no deployment record found |
| Publish/pull/run/pin | Not run; no stale image was republished or pinned |
| Existing Graph credential | Application token has no roles/delegated scopes; application-read probe failed, no directory data returned |
| Direct `/`, `/healthz`, `/api/me`, `/app` | Each403 with TLS validation and no redirect following; deny-all restriction, not health/auth acceptance |

The new [allocation candidate](./private-proof-publisher.bicep) is an
**undeployed, capacity- and bootstrap-blocked template**, not an approved
deployable publisher or one-command
setup. It creates only an exact-group-guarded temporary D2as_v5 VM,32GiB
StandardSSD OS disk, NIC, outbound-use Standard public IP, deny-all-inbound NSG
and dedicated `10.40.8.0/28` child subnet in existing `vnet-cutover-test`.
There is no public inbound allow, backing-service mutation, IAM resource,
runtime/default-profile change or new credential in the template.
`test_private_proof_publisher.py` checks the compiled resource/security boundary;
the precloud focused proof/IAM/setup/staff/auth run passed233tests, zero skips.

#### Explicit outbound restriction (2026-10-19, cycle2)

Independent assessment found that the original template's private-subnet flag
and inbound denial did not restrict outbound Internet access with a public IP.
The later source correction keeps the existing resource/guard relationships
but adds this explicit outbound policy before Azure's default NSG rules:

| Destination | Allowed protocol/port | Purpose and limit |
| --- | --- | --- |
| `10.40.4.20/32`, `10.40.4.21/32` | TCP443 | Recorded UK South ACR data/login private endpoints only; not the whole private-endpoint subnet |
| `AzurePlatformDNS` | TCP/UDP53 | Azure-provided DNS only; no arbitrary public DNS resolver, no DNS QNAME/FQDN content filtering |
| `168.63.129.16/32` | TCP80/32526 | WireServer/guest agent; Azure exempts this agent communication from NSGs, so this rule documents required traffic rather than proving its isolation |
| `AzurePlatformIMDS` | TCP80 | Local instance metadata/managed-identity token acquisition, not general ARM/Entra Internet access |
| Remaining platform DNS/IMDS traffic | Deny all | Explicit service-tag denial after allowed ports, since platform services have special default handling |
| All remaining outbound destinations/protocols/ports | Deny all | Priority200 overrides default VNet/Internet allows; retained public IP does not override the NSG |

No `Internet`, `AzureCloud`, `Storage` or package-host allow is present.
NSG service tags cannot filter Ubuntu/Docker package FQDNs. Stock Ubuntu has
no demonstrated offline Docker/build-tool bootstrap; apt/package downloads are
intentionally blocked. **Do not allocate/apply this template as a working
publisher until a separately reviewed private/offline tool-delivery route
exists**, as well as actual capacity. Do not reopen broad outbound access to
make bootstrap work. No new firewall, proxy, custom image or package mirror was
created or validated in this correction.

An operator must independently revalidate the existing VNet's Azure-provided
DNS configuration and both exact private endpoint IP/resource/DNS relationships
before any later deployment. Address changes require a reviewed source/test
update, not wildcard widening or a hosts override. Supported Azure Linux Agent
versions can redirect extension-package/status traffic through WireServer;
that behavior and Run Command have not been demonstrated on this pinned image.
Direct public blob/extension downloads are not allowed as a fallback.
DNS payloads and permitted registry writes are not content-filtered: these
rules are a restricted network boundary, not prevention of all exfiltration or
misuse of a later `AcrPush` grant. Least-privilege grant, reviewed source,
attended lifetime and independent release approval remain necessary.

Compiled contract and bounded first-match/negative-mutation tests cover the
intended rule precedence and allowed/denied flows; they do not emulate Azure's
platform exceptions or prove live network behavior. Cycle2 executed no Azure
write, deployment, what-if or capacity retry. Both original `SkuNotAvailable`
results and no-allocation status are unchanged.
Official sources checked2026-10-19:
[WireServer and platform DNS exceptions](https://learn.microsoft.com/en-us/azure/virtual-network/what-is-ip-address-168-63-129-16)
and [Linux Agent extension network requirements](https://learn.microsoft.com/en-us/azure/virtual-machines/extensions/features-linux).

Do not apply it unchanged on the strength of SKU GET or quota. An authorized
operator must first re-establish actual capacity with exact provider preflight,
current cost, unique-name absence, exact subscription/group/VNet/registry IDs,
unchanged subnet/policy baselines and a successful owned-only Incremental
what-if. Preserve the exact input hashes and recovery inventory privately
before writes. An unexpected parent VNet modification, unresolved actionable
delta or wrong target must stop apply.

The intended attended lifetime is at most two hours, with reserved cleanup
time, explicit operator deallocation/deletion on every failure and a verified
guest poweroff watchdog before any future approved offline build work. **Neither expiry tags nor
guest poweroff guarantee Azure deallocation or stop billing.** No timer was
armed here because no VM was allocated. Future actual MI creation would require
one separately checked `AcrPush` assignment only at the existing registry;
none was created. Exact owned cleanup must remove that assignment, VM/OS disk,
NIC, IP, NSG and child subnet, never existing VNet/identities/data or `ama`.
Run Command must carry only the reviewed seven-file proof context, not the
repository, operator token or private roster.

Retail estimates retrieved2026-10-19: Linux B2als_v2 USD0.0425/hour, D2as_v5
USD0.10/hour, Standard IPv4 IP USD0.005/hour, E4 LRS32GiB disk USD2.64/month plus
USD0.002/10K operations. Two hours D2as_v5/IP/prorated disk is about USD0.217
before disk operations, transfer and tax. These are retail estimates, not the
account's effective bill, hard cap or observed spend. No new resource allocation
or charge is claimed. Official sources: [agent pools](https://learn.microsoft.com/en-us/azure/container-registry/tasks-agent-pools),
[explicit outbound](https://learn.microsoft.com/en-us/azure/virtual-network/ip-services/default-outbound-access),
[Run Command](https://learn.microsoft.com/en-us/azure/virtual-machines/linux/run-command)
and [Retail Prices API](https://prices.azure.com/api/retail/prices).

Final readback found zero owned resources; original subnet objects and registry
public/bypass/policy settings equal the prewrite baseline. SQL, vault, Storage,
Foundry and IoT public access remain Disabled. No cloud deletion was necessary.
The private image route is still unresolved; actual capacity plus a reviewed
private/offline build-tool route, or an identified existing prepared private
publisher, are technical prerequisites.
#349 still requires an authorized tenant operator's real registration,
permissions/consent, private credential, staff binding and browser session.
#358's live secret-preservation round-trip follows this branch. #360d/e remain
**UNMET**: no real browser/role/SQL/AI acceptance or Front Door retirement.
See the [dated evidence delta](../docs/architecture/cutover-evidence-pack.md#bounded-rg-publication-continuation-2026-10-19).

```bash
python3 infra/scripts/deploy.py --resource-group ama --registry <registry-name> \
  --environment dev --parameters <private-completed-parameters.bicepparam>
# After reviewing the what-if, repeat with --apply to deploy.
```

Then run the SQL script from a host with private network access, push the
application images to the registry and update the image parameters.
Start from the appropriate committed [environment example](#environments),
replace all marked placeholders and record the region/quota checks first.
Compilation alone does not make an example deployable.

For a from-empty rebuild, first set `deployApplications=false`. This creates
the dependencies without temporarily exposing an unauthenticated placeholder
workbench. Build the real image, provision the vault auth secret and seed SQL,
then deploy again with `deployApplications=true`, `entraClientId` and `apiImage`.
The flag does not delete existing apps in incremental deployment mode.

### Orchestrator image selection (#322)

Owner decision, 2026-10-16: `orchestratorImage` defaults to `''` in
`main.bicep`. Both omission and an explicit empty string mean
`mcr.microsoft.com/k8se/quickstart:latest`; an explicit nonempty image tag or
digest is forwarded unchanged. Bicep does not look up existing resources.
The placeholder cannot run the Python auth-renewal and ledger-verify commands.
Do not use a raw Bicep redeploy with an omitted/empty image to preserve jobs.

Use `scripts/deploy.py` for redeployments. It resolves once before invoking
`az deployment group what-if` (default) or `create` (`--apply`):

1. Retain the existing real image from `job-{workload}-{environment}-orchestrator`,
   `-auth-renewal` or `-ledger-verify`. Placeholder jobs do not hide a real image.
   Different real images stop deployment; select an image explicitly to reconcile.
2. Otherwise use the newest updated tag in the specified registry's
   `zava-forward-orchestrator` repository (`show-tags --orderby time_desc --top 1`),
   using that registry's actual login server, not an assumed Azure DNS suffix.
3. Otherwise select the placeholder and print a warning that the maintenance
   jobs cannot run. Registry/repository absence and an empty tag list are valid
   bootstrap states; failed queries, denied access and malformed output stop
   deployment rather than being treated as absence.

Every run prints the full selected image and its source before the deployment
command, including explicit overrides. Job and registry discovery is scoped to
the supplied resource group. `--workload` defaults to `forward` and
`--environment` to `dev`; these options determine both lookup names and the
final Bicep parameters, overriding conflicting values in the parameter file.
Set them explicitly when deploying test or pilot. Workload names must be 3-10
lowercase letters/digits, starting with a letter. The wrapper rejects resource
groups other than `ama` before any Azure call. The registry name is required
even for a from-empty bootstrap; it need not exist yet in the group.

To intentionally roll forward, pass `--orchestrator-image <tag-or-digest>`.
This bypasses discovery, as does explicitly passing the placeholder (still
warned). Leading and trailing whitespace is stripped from the explicit value;
an empty or whitespace-only option uses normal resolution (Refs #339).
The wrapper owns the image
parameter: an image set only in the parameter file is not an explicit override.
Other overrides use repeatable `--parameter NAME=VALUE`; image, workload and
environment must use their named options.

```bash
python3 infra/scripts/deploy.py --resource-group ama --registry <registry-name> \
  --environment test --parameters <private-parameters> \
  --orchestrator-image <registry-server>/zava-forward-orchestrator:<new-tag> \
  --parameter apiImage=<registry-server>/zava-forward-api:<new-tag>
```

Review the printed choice and what-if, then repeat with `--apply`. Discovery
runs again before applying; it is not an atomic lock on changing jobs/tags.
For a reviewed rollout, pin the same explicit digest in both commands.
The helper neither builds images nor creates/deletes resource groups.
Application image builds still use only `src/` as context. Pipeline #138
integration remains separate; these are offline-tested semantics, not evidence
of an Azure rollout.

## Deployment profile

### GitHub deployment pipeline (Refs #138)

[`infra-plan.yml`](../.github/workflows/infra-plan.yml) and
[`src-deploy.yml`](../.github/workflows/src-deploy.yml) add offline-tested
pipeline definitions, **not observed Azure deployment or OIDC acceptance**.
No workflow was dispatched against Azure for this implementation.

The PR workflow runs only after successful `Source projects CI` on an infra
PR from this repository. A default-branch `workflow_run` loads trusted helper
code, checks the candidate paths without executing them, then inspects candidate
Bicep as data. Fork PRs are deliberately excluded: maintainers must review and
adopt their changes onto a trusted branch first. The result is attached as a
seven-day Actions artifact, keyed by environment and exact candidate SHA.
There is no privileged `pull_request_target` checkout or PR comment token.
Only status, change counts, source SHA and a parameter hash are published;
raw what-if output, parameters, resource IDs and Azure errors are withheld.
Failed plans attach a failed-status summary when the helper has started.
The workflow must first merge to the default branch before this trigger exists.

Release is manual, **main-only**, and serialized across all environments in
`ama`. Before dispatching release, manually run `Source projects CI`
(`src-ci.yml`) on `main` and wait for success on the exact commit being released.
Source CI does not run on main pushes. The release's read-only prerequisite
checks the workflow-specific API for a completed, successful manual main run
matching its immutable SHA; missing, failed, malformed or inaccessible evidence
stops before image builds or Azure login. A green PR run or earlier main commit
is not sufficient. No workflow/check name or branch protection is changed.
It builds all four source images from that same immutable workflow SHA.
Every image passes the existing non-root/hardened/plain startup contract and
the same `src/trivy.yaml` fixable HIGH/CRITICAL gate as source CI; full reports
including unfixed findings are retained even on gate failure. Only passing
images leave the unprivileged hosted build job. Each rebuilt release image
also gets an SPDX JSON SBOM, retained for seven days as
`release-sbom-<project>`; generation and upload must succeed before image export.
Source-CI SBOMs do not substitute for this inventory of the rebuilt images.
Private publish jobs load
(never execute) those same-run image artifacts, push tags
`sha-<commit>-r<run>-a<attempt>` to separate `zava-forward-<project>` repositories
and capture registry digests. Importer maps to Bicep `importImage`; agents to
`agentImage`. Deployment validates all four digest records against this run,
attempt, source and registry before applying them. Releases always rebuild
the complete set rather than mixing revisions or trusting mutable cache tags.
Source CI uses dependency-aware per-project image path filters; core/shared
build inputs affect all images, and agents changes also affect API.

#### Required external setup

Create protected GitHub environments `dev`, `test`, `pilot`, plus
`<environment>-plan` and `<environment>-release` for each target. Require
reviewers, prevent self-review, disallow administrator bypass and allow only
protected branches; protect `main` itself. Review the exact PR SHA before
planning and the exact workflow SHA/run, scan reports and four digest artifacts
before deployment approval. The helper verifies reviewer/branch configuration
before Azure login; YAML alone cannot provision or prove that anyone approved.
No particular deployment approver is invented by this implementation.

Use separate OIDC application identities for plan, publish and deploy in every
environment. Configure the GitHub issuer `https://token.actions.githubusercontent.com`,
audience `api://AzureADTokenExchange`, and exact subject
`repo:<owner>/<repo>:environment:<environment-name>`, including the `-plan` and
`-release` suffixes for their respective identities. Never add client secrets,
credential JSON, passwords or long-lived registry credentials. GitHub's
short-lived job token is used only to read environment configuration.

Set these **GitHub environment variables**, never committed values:

| Variable | Where and purpose |
| --- | --- |
| `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID` | Each privileged environment; owner-supplied federation/account configuration |
| `AZURE_PLAN_CLIENT_ID` | `<environment>-plan`; plan identity only |
| `AZURE_PUBLISH_CLIENT_ID` | `<environment>-release`; publisher only |
| `AZURE_DEPLOY_CLIENT_ID` | Target environment; deploy identity only |
| `AZURE_REGISTRY_NAME` | Release and target environments; existing registry in ama |
| `DEPLOY_PARAMETERS` | Plan and target environments; JSON override contract below |

`DEPLOY_PARAMETERS` must contain exactly `location`, `sqlLocation`,
`regionCheckReference`, `quotaCheckReference`, `alertEmail`,
`sqlAdminGroupName`, `sqlAdminGroupObjectId`, `entraClientId` (all nonempty
strings), and `entraBearerOnly` (an explicit JSON boolean). Use approved values
outside the repository; placeholders are refused. The helper compiles the
selected committed dev/test/pilot example with Bicep and overlays only these
keys. Production security defaults, locks and quarantine remain in their
environment set. Public network access is always forced false. The generated
ARM parameter file is private, temporary and removed on success or failure.

Choose `entraBearerOnly=false` to preserve browser mode and its separately
initialized Key Vault application secret. That existing runtime credential is
not a pipeline credential and is never read by the pipeline. Browser sign-in
must return 302 while anonymous `/api/me` must return exactly 401; a platform
302 on the API is a failed check, not a pass. Use `true` only for an explicitly
approved secretless service-test target as described above, not as a silent
workbench UX change. Tenant registration, SQL users/seed and browser callback,
staff/SQL onboarding is orchestrated by setup with one human confirmation;
token-store consent/initialization remains a separate human-controlled task.

Provide isolated, **ephemeral** Linux x64 runners with labels
`ama-private-plan`, `ama-private-release`, `ama-private-deploy`, Python 3.12,
Azure CLI/Bicep, gh and Docker (release/deploy only). They must reach private
ACR and API DNS/network paths without widening any network policy. Restrict
runner groups to the trusted default-branch workflows; do not share runners
with arbitrary PR jobs, ambient managed identities or reusable credentials.
Destroy runner disks, Docker credentials and isolated Azure CLI caches after
each job. Plan needs resource reads plus what-if/validation, no resource
writes; publish needs registry read/AcrPush scoped to the ama registry; deploy
needs an approved ama-scoped deployment/resource custom role, template-required
role-assignment rights and registry **AcrPull only**, without quarantine bypass.
Do not grant subscription Owner or move governance/policy into this pipeline.
Actual RBAC/federation and runner isolation require platform-owner verification.

Quarantine is never disabled or bypassed. Test/pilot registries retain their
quarantine policy: an independently approved scan/release process must make
these digests pullable before target-environment approval. The deploy identity
pulls every exact digest before apply; denied/quarantined images stop the run.
No quarantine-release process is provisioned here, so this remains a live gap.
Registry scan acceptance is not hosted read-only/capability enforcement;
the inherited Container Apps hardening limitation remains Partial.

#### Apply policy, probes and acceptance boundary

The workflow targets existing, initialized infrastructure only. PR planning
requires four existing immutable workload images and consistent maintenance
job images; it does not silently select placeholders or newest tags. The
deployment helper invokes only group-scoped, incremental operations in `ama`.
It creates/deletes no group and rejects Delete, Ignore, unsupported/unknown
what-if changes or resources outside the configured subscription's `ama`.
The exact generated parameters are reused for the fresh what-if and apply.
SQL server discovery must be nonempty, and **every** SQL server in ama must
have public access Disabled before and after deployment. SQL stays private
in the template; there are no firewall or policy-exemption workarounds.

After successful ARM provisioning, the helper uses the deployment's own
`apiInternalFqdn`, HTTPS certificate validation and no redirect following.
It retries health briefly until exact 200, then requires exact 401 for anonymous
API, malformed bearer and forged principal-header requests. Browser mode also
requires sign-in 302. Any unauthenticated 2xx, redirect on the API, wrong status
or network failure fails the run. A failed rollout is not automatically undone:
retain the run and have an owner review a new release; never delete ama.
The sanitized artifact distinguishes successful what-if from successful
deployment/checks. SQL read/write, authorized staff, model access and restart
persistence in rebuild step 7 are **not** proven by these HTTP/SQL-policy
checks; private identity-backed acceptance remains separate.

| Issue criterion | Current evidence and unmet boundary |
| --- | --- |
| Per-environment OIDC | Wired with job-local id-token write, no stored pipeline secrets; actual federation/RBAC unverified |
| Infra PR what-if attached | Trusted trigger and sanitized artifact wired/tested; no live PR what-if executed |
| Approval and environment parameter sets | Same template/examples, environment configuration guard and approval boundaries implemented; pilot region `uksouth` and subscription owner @jmservera selected on 2026-10-15; actual reviewer rules/approval, service choices and approved subscription binding remain unverified |
| Versioned image push and deployment reference | Four image/scan/artifact/digest path implemented/tested; no live build/push/deploy or quarantine release observed |
| Automatic post-deployment checks | Local HTTP negative/positive tests and fake-command orchestration; live ingress/authentication/SQL/model/restart acceptance unmet |
| No secret values in logs/repository | Pinned workflows, no stored-secret inputs, captured command output and canary regression checks; end-to-end live log audit not performed |

All six live issue criteria remain unchecked. Local checks:
`python3 -m pip install PyYAML==6.0.3`, then
`python3 -m unittest discover -s infra/tests -p test_pipeline.py -v`.
`actionlint -config-file infra/tests/actionlint.yaml .github/workflows/infra-plan.yml .github/workflows/src-deploy.yml .github/workflows/src-ci.yml`
checks real workflow syntax when actionlint is installed. Source CI persists
the structure/permission/pinning/no-echo mutation tests and helper Ruff/mypy.

`deploymentProfile` defaults to `production`. Development alone relaxes
nothing: public access, purge protection and registry quarantine each require
an explicit opt-out/opt-in. Production rejects public access, disabled purge
protection or disabled quarantine through named guards. SQL public access is
always Disabled, independent of profile. The single
[environment differences table](#environments) records the committed choices.
These are security profiles for a synthetic demonstrator, not production or
pilot acceptance. No development setting authorizes a policy exception.

### Private cut-over proof (2026-10-16)

For the owner-authorized ama continuation, SQL public access must remain
Disabled by policy. Do not add tags/exemptions, enable public SQL, attempt
firewall changes or peer the operator VM. The VM is not on the ama VNet.
Only management-plane Azure CLI commands run there; SQL, staff initialization
and private HTTP smoke must run inside `vnet-cutover-test`.

Build all images and capture digests before making ACR private. Use ACR Tasks
with `src/acr-cutover.yaml` for the four workloads (BuildKit enabled there), then
build the proof runner from the narrow `infra/` context:

```bash
az acr run -g ama -r <registry> -f acr-cutover.yaml --timeout 1800 src
(cd infra && az acr build -g ama -r <registry> -f cutover-proof.Dockerfile \
  --build-arg API_IMAGE=<registry-server>/zava-forward-api@sha256:<digest> \
  -t zava-forward-cutover-proof:<unique-tag> .)
```

The proof image inherits the installed packages and non-root user of the API
image; it contains no dataset or credential. Do not attempt default ACR Tasks
repair builds after isolation without an approved private task path.
Always supply the captured orchestrator digest to `deploy.py`, avoiding
operator-side tag discovery against a private registry.

Run the wrapper's what-if, inspect scope and apply the same parameters:

```bash
python3 infra/scripts/deploy.py \
  --resource-group ama --registry <registry> --workload cutover --environment test \
  --parameters infra/main.bicepparam \
  --orchestrator-image <registry-server>/zava-forward-orchestrator@sha256:<digest> \
  --parameter allowPublicNetworkAccess=false \
  --parameter deployApplications=false --parameter deployEnvironmentOnly=true \
  --parameter sqlAdminGroupName=id-cutover-test-init \
  --parameter sqlAdminGroupObjectId=<initializer-mi-principal-id> \
  --parameter sqlAdminPrincipalType=Application \
  --parameter entraClientId=<existing-application-client-id> \
  --parameter entraBearerOnly=true \
  --parameter alertEmail=<approved-mailbox> \
  --parameter regionCheckReference=<reviewed-region-record> \
  --parameter quotaCheckReference=<reviewed-quota-record>
# Repeat with --apply only after reviewing the what-if.
```

The historical `modelDeployments=[]` bootstrap override is no longer valid.
The model array must be nonempty: even an environment-only operation includes
the default small model. This changes provisioning and potential inference
cost, not just application startup. For an existing evaluated stack, pass its
explicit reviewed `modelDeployments` array to preserve its model set, names,
versions, SKU and capacity. These full-stack commands are not the bounded
model-only operation described below.

`deployEnvironmentOnly=true` creates the environment and internal DNS without
starting workloads. It is additive to `deployApplications`; neither flag deletes
existing resources in incremental deployments. A dedicated ama initializer
identity is SQL Entra Application administrator, attached to a manual job in
that environment with registry-scoped AcrPull. Pass its client ID as
`ZF_SQL_CLIENT_ID`, SQL FQDN/database as `ZF_SQL_SERVER`/`ZF_SQL_DATABASE`,
and API/import MI client IDs as `PROOF_API_CLIENT_ID`/`PROOF_IMPORT_CLIENT_ID`.
Run the proof image with argument `initialize`. It checks SQL DNS in
`10.40.0.0/16` and system metadata/proof ownership before opening Store.
Unknown databases are refused without case/staff reads or changes.
Known tables include the installed API assistant schema, not arbitrary extra
tables. An owned partial initialization may retry with the synthetic seed;
populated cases are never reseeded by Store.

Initialization grants Graph-free contained users by client UUID little-endian
SID: API reader/writer/ddladmin for existing startup migrations, import
reader/writer only. Administrator binding instead uses the initializer's
principal ID. Do not confuse these identifiers or elevate API to administrator.
The initializer remains the documented administrator of this proof stack.

The runtime-generated seed has one fictional case, no staff or human bindings
and a non-personal proof marker. It is not the continuing 60k/980-case workload.
Deploy applications only after initialization, passing all four captured digests
with `deployApplications=true`. `entraBearerOnly=true` is opt-in secretless
service-test mode: tenant-specific issuer/audience validation, Return401, no
browser client secret or delegated token store. It requires an identified
existing client ID; it does not provision tenant roles or authorize MI as staff.
Browser mode remains the default and requires the registration/vault secret.

Run separate manual proof executions as API MI with argument `verify`; they
reopen application SQL state without a seed and assert marker/case equality
and zero staff. Use `smoke --base-url <private-api-origin>` for exact health 200,
anonymous API 401, malformed bearer 401 and forged principal-header 401.
Restart the serving revision, record before/after replicas and repeat both
probes without initialization or reseeding. Missing probes are not passes.
If an instrument correction is needed after ACR isolation, an explicit
management-plane job-template command may carry the tracked Python runner
source (`command: ['python', '-c', <source>]`, `args: ['verify']`), while retaining
the same immutable ACR image, identity and network. Record the source SHA-256,
the changed command and the new execution separately from image-baked runs.
Do not change network policy just to rebuild the instrument.

Human staff initialization is a distinct in-VNet task requiring an owner-supplied
private roster and authorized Graph access. Never fabricate people, read an old
private dataset or substitute MI. Record missing prerequisites as Blocked.
Owner sign-off remains unchecked in the
[cut-over pack](../docs/architecture/cutover-evidence-pack.md).

Runner unit tests use installed source packages:
`python3 -m unittest discover -s infra/tests -p test_private_cutover_proof.py -v`.
Compiled profile/staging/auth-mode checks run in the existing infra suite.

Example from the repository root: `python3 infra/scripts/deploy.py --resource-group ama --registry <registry-name> --environment dev --parameters <private-completed-parameters.bicepparam>` (what-if; complete the recorded checks below and add `--apply` only after review).

## Direct demo ingress migration proposal (2026-10-16, #360)

Refs #360. The owner selects direct Container Apps HTTPS with Entra browser
sign-in for the synthetic demo, without Front Door. This supersedes the edge
prerequisite in the historical #344 procedure below, not the optional
production/private-origin architecture. This is an **offline implementation and
proposed migration**, not owner migration approval, deployment or permission
to spend. The coordinator owns all live steps after explicit owner approval.
Never delete resource group `ama`, enable SQL public access, bypass policy,
change private endpoints or read a private dataset to perform this migration.

### Configuration and guard boundary

`demoDirectIngress=true` is independent of `allowPublicNetworkAccess`.
Use `deploymentProfile=development`, `allowPublicNetworkAccess=false` and
`enablePublicEdge=false`. The guard rejects production, edge coexistence and
public-backing combinations. Browser authentication is required for serving
demo workloads; bearer-only proof mode is not a browser demo.
Default/production behavior is unchanged. The optional production Front Door
path remains available with its original guards.

The new environment and workload names use a `-demo` suffix on the existing
workload/environment prefix; **do not change `workload` or `environmentName`**
to achieve that suffix. Changing the root prefix provisions different SQL,
storage, identities and other backing services, not a safe replacement.
For the current prefix the replacement environment is
`cae-cutover-test-demo`, API `ca-cutover-test-demo-api` and corresponding
`ca-`/`job-cutover-test-demo-*` workloads. Demo job suffixes are shortened
to `auth`, `orch`, `audit` and `load` for token renewal, orchestration,
ledger verification and imports respectively; this keeps names below 32
characters even at the supported workload/environment input bounds. The
existing non-demo job names are unchanged. Existing identities, registry,
SQL database, Key Vault, storage, Foundry and IoT Hub stay private and retain
their names. The demo environment alone becomes external/public, with HTTPS
ingress; its separate `snet-aca-demo` delegates to Microsoft.App/environments.
The separate demo NSG permits Internet TCP 443, not Internet port 80 or
arbitrary Internet ports. Existing `snet-aca` and its NSG remain unchanged.
Review address-space conflicts before selecting the proposed
`10.40.6.0/23` subnet; a template default is not a measured free allocation.

The external environment uses public default-domain DNS, not the old internal
environment wildcard zone. Keep all service private DNS zones and VNet links.
EasyAuth must use `NoProxy` (`behindPublicEdge=false`); registration callbacks
are `https://<demo-app-fqdn>/.auth/login/aad/callback`. Never reuse an edge
callback as the sole direct callback or trust caller-supplied forwarding hosts.
The API tag `zava-forward-ingress=direct` selects this path in setup without
requiring `az afd`, its `cdn` extension or Front Door discovery permissions.

### Owner-reviewed migration sequence

1. Obtain the owner's review and approval of this exact migration, overlap
   cost, rollback window and future retirement boundary. Reconfirm resource
   scope `ama`, location/capability/quota checks, vacant subnet range, policy
   constraints and external workload-profile support. Record approval outside
   this repository's secret-free evidence; no approval is inferred here.
2. Inventory the old environment, every app/job and trigger, current revisions,
   image digests, identities, environment variables, secret **reference names**,
   auth configuration, SQL persistence baseline and private DNS links. Keep
   IDs, roster, tokens and private config exports outside Git. Never export
   secret values. Confirm workload names are unique within `ama`: apps/jobs
   cannot move to another environment and `internal` is immutable.
3. Review a coordinator-generated incremental what-if using the same existing
   root prefix and all retained private parameters, adding the explicit demo
   flags. Start with `deployApplications=false`,
   `deployEnvironmentOnly=true`, `deployBackgroundWorkloads=false`.
   Expected delta: demo subnet/NSG and external environment/diagnostics only,
   plus reviewed subnet-list reconciliation. Reject deletion, replacement,
   public backing-service changes, identity recreation, unrelated drift or
   unreviewed model/resource creation. Main reconciles the whole stack: these
   flags are not a workload-only deployment or a deletion instruction.
4. Only after approval, let the coordinator create that environment and subnet.
   Keep the original environment/apps/jobs serving. Check public default-domain
   resolution, TLS, VNet integration and private DNS from the new environment.
   Confirm SQL/Key Vault/storage/registry/Foundry/IoT public network access is
   still Disabled. A public browser cannot test those private data paths.
5. Check each reused user-assigned identity, registry AcrPull, vault secret
   access, blob/queue grants, SQL contained-user SID/grants and Foundry roles
   against the existing matrix. Reuse SQL persistence; never reinitialize or
   reseed the database. Managed identity attachment, not just matching labels,
   must agree. Operator RG access is not tenant or vault data-plane authority.
6. Stage the replacement API only: `deployApplications=true`,
   `deployBackgroundWorkloads=false`, explicit retained digests for **all**
   image parameters, browser registration and credential reference. Keep the
   old background generation authoritative. Omission of background resources
   in an incremental template does not stop any already-created resources:
   staging must be a fresh generation or independently verified stopped.
   Configure the direct registration using the setup procedure below from an
   approved private-network path when vault access is needed.
7. Perform the parity checklist and public/identity-backed acceptance below.
   Before any switch of consumers, pause producers and new claims, drain
   running jobs/messages or explicitly disposition them, and verify only one
   generation can consume/publish. Activate the new background generation
   with `deployBackgroundWorkloads=true` only after the old one is stopped
   and its in-flight work accounted for. Do not start an import twice.
8. Update demo links to the new app FQDN after successful human sign-in and
   recorded owner cut-over approval. No custom DNS purchase is necessary.
   If an existing custom domain is retained, separately review its binding,
   certificate, verification records, TTL and rollback; do not move service
   private DNS or overwrite old callback URLs.
9. Retain the old stack and edge through the agreed rollback window. Retirement
   is a **second explicit owner authorization**, after all live criterion d
   checks pass, not a consequence of a successful ARM deployment or unit test.

### Image, configuration and trigger parity checklist

| Surface | Required coordinator comparison |
| --- | --- |
| Images | Exact immutable digests for API, agents, orchestrator, import and maintenance commands; src image context, no placeholders or implicit latest tags |
| API configuration | SQL server/database and MI auth; blob/queue endpoints; document store; tile URL/attribution; trusted-proxy mode; role map; law-store settings; AI endpoint/deployments; release/assistance gates and disabled defaults |
| Authentication | Real registration and tenant-specific issuer/audiences; retained existing callbacks; app-FQDN callback; NoProxy; HTTPS; public exclusions; browser secret/token-store references; assignment-required enterprise app |
| Staff and authorization | Authorized private roster, exactly one effective staff role, scoped SQL bindings, fresh staff cache/restart, unknown/wrong-role denial; no fabricated people or runtime directory-management rights |
| Private dependencies | Same identities, database and grants, private endpoints and VNet DNS links, registry image pulls, vault references, blob/queue/Foundry reachability; all public network access Disabled |
| Operations | Probes/scale, logs/diagnostic destination, alerts for new names, job commands/schedules, retries/timeouts, token SAS rotation and expiry; no omitted secrets reconstructed from redacted readback |

| Consumer/producer | Inactive staging and activation/drain boundary |
| --- | --- |
| Agents queue-scaled app | Omit with `deployBackgroundWorkloads=false`; minReplicas=0 is not disabled KEDA. Pause producers, stop old claims and account for in-flight messages before enabling the new worker |
| Orchestrator scheduled job | Omit during staging; suspend old trigger and wait for/disposition running executions before enabling exactly one new schedule |
| Import event job | Omit during staging; retain queue contents, stop old trigger and finish/disposition each execution; no duplicate import/replay without reviewed idempotency evidence |
| Auth renewal job | Omit during staging; keep the old renewal responsible for the shared token store until ownership switches, with expiry headroom and no two active schedules |
| Ledger verification/publishing job | Omit during staging; retain old verified publication until new job is ready; preserve immutable blobs and checkpoints, then switch one schedule |
| API or other configured producers | Compare runtime gates and pending work; pause discretionary background production for the drain, preserve human/manual safety routes and do not activate new AI authority |

These are migration controls, not evidence that placeholder queue workers
implement their intended contracts. Existing #144 and feature gaps remain.

### Direct Entra setup and acceptance

After owner authorization, explicit selection avoids ambiguity with the retained
old API:

```bash
python3 infra/scripts/setup-entra.py --direct-ingress \
  --run-in-azure --secret-store keyvault \
  --container-app ca-cutover-test-demo-api --dry-run
python3 infra/scripts/setup-entra.py --direct-ingress \
  --run-in-azure --secret-store keyvault \
  --container-app ca-cutover-test-demo-api --check
```

The direct tag also selects direct mode automatically. Use the authorized
isolated login/profile and private roster workflow from
[authentication initialization](#post-deployment-api-authentication-initialization).
Actual initialization is a live mutation, intentionally not run here.
If inherited bearer-only settings are intentional, do not silently replace
them: use `--bearer-only`. The normal direct-demo command now explicitly
targets browser onboarding and creates a missing credential automatically.
Direct mode uses only the app
FQDN; it does not discover or require the retained Front Door.
Setup adds missing registration/enterprise app/manifest roles and roster
assignments, enforces assignment-required sign-in and runtime staff-role
checks, and preserves unrelated callbacks/roles/configuration.
The same command checks SQL staff binding, presents a count-only plan, asks
once, and applies with verified serving-replica restart when private SQL is
reachable. Directory role assignment alone never implies SQL completion.

The default command discovers the Bicep-created vault and API identity; neither
`--vault` nor `--vault-identity` is required. The owner-selected Azure/Key Vault
command uses the ARM handoff and fails on vault failure, with no app fallback.
Its worker image/scoped IAM prerequisites remain explicit; `--dry-run` cannot
create a worker to obtain unavailable private SQL evidence and reports that
limit rather than claiming success. Retain the resulting Key Vault secret
reference on subsequent Bicep redeploys. Use the existing tenant authority/
roster instructions, not Azure RG ownership as a substitute for Entra consent.

Run the strict public probes from an HTTPS-capable client, using installed
src distributions:

```bash
python3 infra/scripts/private-cutover-proof.py smoke --direct-ingress \
  --base-url https://<demo-app-fqdn>
# Optional role-denial evidence; never put a session value on the command line.
python3 infra/scripts/private-cutover-proof.py smoke --direct-ingress \
  --base-url https://<demo-app-fqdn> --auth-hops 1 \
  --wrong-role-session "$HOME/.azure/private/wrong-role.json"
```

The optional session file must be owner-owned mode `0600`, outside the
repository, with exactly one `cookie` or `token` JSON field. It supplies an
already authenticated **Contractor** session; it does not manufacture roles or
authenticate a person. A Contractor signs in only when exactly one enabled roster row binds its
OID to a company. Roster rows match an Entra principal on tenant and OID; a row
without a `tid` matches only when the store records `legacy_roster_tenant`, so
legacy ownership continuity needs that record set through a reviewed guarded step. The probe first
requires `/api/me` 200, then `/api/stats` 403: Contractor may read its own
account but cannot read staff-wide statistics. An administrator is not the
wrong-role fixture for this endpoint. Missing/unknown staff or invalid sessions
are authentication-denial checks, not proof of role authorization.
Default `--auth-hops 0` requires the direct Microsoft login redirect. Where
EasyAuth emits a local login step, `--auth-hops 1` permits one individually
validated same-origin `/.auth/` hop; the bounded maximum is five. No automatic
redirect following or external credential forwarding is allowed.
JSON Lines contain sanitized check/status/outcome fields. Any status/host
mismatch or network/TLS failure exits nonzero. Without a supplied role session,
the role check is explicitly Not run even when transport checks succeed.
Omitting `--direct-ingress` preserves private smoke's private-DNS requirement;
do not use public mode for SQL initialization or private persistence proof.

Probe results must retain only check names/status/outcomes, never credentials,
claims, identity IDs, full login URLs, callback query strings or roster data.
Require health and welcome 200, native and browser JSON API 401, malformed
bearer/forged-header denial, and browser navigation 302 to HTTPS
`login.microsoftonline.com`. A browser API 302 is the known #350 gap, **not**
a 401 pass. Real users must complete callback/session, assigned-role access,
wrong-role/unknown-staff denial and logout/account switching. Validate actual
SQL state before/after an API restart and bounded authorized AI calls with
provider/model/usage evidence. Missing role credentials mean Not run, not Pass;
fixture-based role tests are not real Entra acceptance.

### Rollback and selective retirement

On TLS, authentication, authorization, persistence or private-network failure,
stop the new generation's producers/triggers, drain/disposition executions and
prevent new claims. Restore old triggers only after the new consumers are
inactive; return links/custom DNS to the old entry if it is still verified.
The old edge's historical redirect did not prove usable tenant sign-in:
otherwise mark demo unavailable while correcting it, never grant anonymous
access. Keep both callback sets until the rollback window ends. Do not restore
a stale database snapshot over shared live writes or reseed to hide a failure.
No automatic deletion or network relaxation is a rollback.

After d and the separate retirement approval, the coordinator inventories
dependencies again, disables the old edge route/endpoint, then removes only
the approved `afd-cutover-test` profile/children and dedicated WAF association/
policy, diagnostics and its managed Private Link connection when no longer
referenced. Verify no shared domain/policy/connection is removed. Stop and
remove only old apps/jobs and explicitly approved proof jobs after draining,
then remove `cae-cutover-test` when no workloads or endpoint dependencies
remain. Retire its **environment-specific** private DNS zone/link and old
delegated subnet/NSG only after confirming they are unused and future main
reconciliation will not recreate them. That last IaC retirement delta needs a
separately reviewed change; this implementation intentionally retains them.
Never remove the VNet, service private DNS/PEs, reused identities/RBAC, SQL,
registry, vault, storage or Foundry. Never delete `ama`. Record terminal
resource checks and acceptance without IDs or secrets.

### Cost proposal, not a quote or spending approval

Microsoft's [billing guidance](https://learn.microsoft.com/en-us/azure/container-apps/billing)
and [pricing page](https://azure.microsoft.com/en-us/pricing/details/container-apps/)
were retrieved on 2026-10-16. A Consumption-only environment has no standing
environment management charge **by itself**; running replicas/jobs, requests,
networking and logs still cost money. Private endpoints or planned maintenance
can add the Dedicated Plan Management meter even on Consumption. No new
environment private endpoint or planned-maintenance feature is proposed.
Existing backing private endpoints remain and still incur their own charges;
the retained old edge/environment can retain management/Private Link costs.

The API retains two 0.5-vCPU/1-GiB minimum replicas: 30 continuously running
days allocate 2,592,000 vCPU-seconds and 5,184,000 GiB-seconds per generation.
At **illustrative, unquoted** active rates of USD 0.000024/vCPU-second and
0.000003/GiB-second that is USD 77.76/month before grants; at illustrative
idle CPU USD 0.000003 it is USD 23.33/month. Thus plan roughly USD 23-78
per API generation, USD 47-156 for full-month two-generation overlap, or
USD 0.78-2.59 per additional day of API overlap. These are sensitivity
assumptions, not retrieved UK/account prices; the public page returned no
numeric regional rates. Free subscription grants are shared and not assumed.
Workers/jobs add their allocated active vCPU/GiB-seconds; inference adds actual
model token charges under existing authority. No new model deployment is
authorized.

The coordinator must replace these assumptions with approved region/currency/
agreement rates and estimate new logs (GiB times ingestion/retention rate),
public IP/VNet/data egress, job duration, request volume and overlap duration
before c. Reused SQL/registry/storage/Key Vault/Foundry/PE baseline costs
continue, not zero. Front Door/WAF/Private Link savings begin only after
authorized retirement and invoice verification; no exact savings or total
budget compliance is proved offline.

### Historical MVP comparison

History-only inspection of commit `15e8158` shows external app ingress,
EasyAuth `RedirectToLoginPage`, public welcome exclusions and callbacks built
from the app FQDN. Environment exposure used the broad
`allowPublicNetworkAccess` switch, also affecting backing services. The prior
working sign-in reports are historical, not evidence that the new tenant
registration exists or direct src sign-in works. The new explicit demo mode
reuses the useful FQDN/browser pattern without copying obsolete public-data
configuration, old image names, datasets or tenant identifiers. No code was
restored from `mvp/`.

## Public browser continuation (2026-10-16, #344)

The #360 direct-demo decision above supersedes this edge choice for the demo.
Keep these observations as history and the recipe as an optional private-origin
edge path; they are not observations of the new direct configuration.

Refs #344. Refs #143. Refs #200. The owner authorized public browser access
again, not public SQL or a policy bypass. The proof environment
`cae-cutover-test` is internal in `vnet-cutover-test` (`10.40.0.0/16`,
uksouth); its internal setting cannot be changed in place. We chose Front Door
Premium with Private Link and WAF Prevention over a new external environment:
it reuses the existing API, identities, private data path and immutable src
image without replacing the environment, subnet or jobs. The trade-off is an
additional paid edge/private-endpoint service and connection approval. This
synthetic-development continuation is not production-profile or pilot acceptance.
The owner also allowed an API-only external environment, but not the existing
global `allowPublicNetworkAccess` switch, which also requests public data access.

The additive entry point checks that the existing environment is internal with
public access Disabled and that the sole API origin belongs to it with ingress
authentication enabled. It does not establish a valid tenant registration.
It now also requires a hexadecimal UUID-shaped Entra `clientId`; empty,
malformed and `systemAssignedIdentity` values stop the dependent auth/edge
deployment. The guard points to `python3 infra/scripts/setup-entra.py`, whose
existing `--public-url` discovers and verifies linked edge callbacks. Run setup
before reapplying the edge. A syntactically valid UUID is not proof that the
registration exists, credentials work or a human can sign in.
It leaves main's production-profile guard intact. It carries forward provider
validation, public exclusions, token storage and credential references returned
by the auth-config read, sets
`forwardProxy=Custom` with `X-Forwarded-Host` / `X-Forwarded-Proto`, HTTPS
required, and uses the default
`entraBearerOnly=false` / `RedirectToLoginPage`. No credential is generated.

The auth update is a full-resource PUT formed with `union`, not a PATCH.
Preservation is limited to properties returned by the selected auth-config API
version. Secret **values** belong to the Container App secret store and are not
read or written by this module; their auth-config references are carried forward
only when present in the read response. A write-only, omitted or redacted
provider/token-store reference cannot be reconstructed by `union`. Before a live
reapply, a human operator must verify the non-secret reference names against the
authorized configuration and stop if any required reference is absent/redacted;
repair through setup or the owning secret-management path, never copy secret
values into Bicep or evidence. No preservation of omitted fields or live
credential round-trip has been proved. This continuation makes no live auth write.

```bash
az deployment group what-if -g ama -n public-browser-344 \
  -f infra/public-edge-existing.bicep \
  -p environmentName=cae-cutover-test apiName=ca-cutover-test-api \
  workspaceName=log-cutover-test prefix=cutover-test entraBearerOnly=false \
  --no-pretty-print
# Review the exact delta, then use create --mode Incremental with the same input.
```

Initial what-if: eight edge resources Create, no resource Modify/Delete.
The auth-preserving follow-on also changes only the existing API auth child.
Provider-populated defaults and runtime references can appear as what-if
property deltas; inspect them, never treat them as permission to modify SQL.
Approve only this edge's pending connection on `cae-cutover-test`, matching
`Front Door Premium private origin for cutover-test`. A write can return
Pending while its asynchronous operation runs; verify terminal operation and
connection **Approved**, not just CLI exit 0.

Exact new resource names: `afd-cutover-test`, its `ep-cutover-test` endpoint,
`og-api` group / `api` origin, `route-api`, `sp-waf`,
`to-log-analytics` diagnostics and `wafcutovertest`. The managed connection
belongs to that origin. `job-cutover-test-public-audit` is a manual image-only
asset hash instrument, using the same serving digest and existing pull identity;
it does not open the dataset or any store. A second execution probes only
anonymous private HTTP status/redirect host. No pre-existing resource was
deleted or replaced, including the group, internal environment, SQL, existing
proof jobs and budget. Only the empty, unused `afd-cutover-test/originheaders`
rule set created by a rejected header-removal trial was deleted.

The public endpoint is
<https://ep-cutover-test-esdrcphsarcahhde.b01.azurefd.net/>.
Detailed public checks, resource inventory and feature acceptance are in the
[cut-over pack](../docs/architecture/cutover-evidence-pack.md#public-browser-restoration-2026-10-16)
and its sanitized JSON. Until the tenant gap is resolved, this URL is not a
claim that a person can complete sign-in.

Public curl on 2026-10-16 proved health/welcome/static 200, native anonymous
APIs 401 and browser `/app` redirect to Entra with the public callback host.
Forged principals/malformed bearer were denied; conflicting Host returned 421.
Individual and combined forwarding-header probes retain the HTTPS edge callback.
Standard forwarding initially trusted a client RFC `Forwarded` host; Azure
disallows deleting that reserved header in a rule, so both edge entry points now
use only Front Door-overwritten X-Forwarded headers through Custom configuration.
Native API curl is not the browser API contract: a browser User-Agent still
receives EasyAuth 302 for an anonymous API request, even with
`Accept: application/json`. With `entraBearerOnly=false`, the configured
unauthenticated action is a redirect, not a route-aware browser/API split;
the observed native curl 401 depends on EasyAuth's client/User-Agent handling.
Changing User-Agent can therefore change an anonymous API response from 401
to 302. These observations are not a reliable API-wide 401 guarantee. Refs #350:
the required browser-page redirect plus anonymous API 401 coexistence remains
unchecked, including browser/fetch-style JSON requests. No API exemption was
added without positive authenticated-platform proof.

The existing proof client value `systemAssignedIdentity` is **not an Entra
application registration**. Matching-tenant read-only discovery found no retained
workbench registration; no valid browser credential or staff roster is supplied.
Real-user sign-in is **Blocked**, filed as #349. Supply the intended registration
and private-vault credential through authorized tenant/in-VNet operators; then
run `python3 infra/scripts/setup-entra.py --public-url https://<edge-host>`,
reconcile the private staff
roster and restart replicas. Do not reuse another application's client or
fabricate staff. The full feature/configuration gap audit is filed as #350.

Before auth mutation, baseline was `Return401` / `NoProxy` with the seven
existing public exclusions. If critical health, API denial or routing isolation
fails after propagation, disable only the new endpoint and restore those two
auth fields; do not delete resources or weaken private networking. A tenant
prerequisite blocker alone is not a reason to enable anonymous APIs.

## Environments

Refs #137. The same template/commit supports dev, test and pilot using the
following secret-free examples. Replace every `PLACEHOLDER` in a private,
untracked parameter file kept alongside `main.bicep` so its relative `using`
path resolves; never commit the completed file. Do not store secrets there:
secure inputs use the approved secret-management path.

The [owner's 2026-10-15 comment](https://github.com/jmservera/ama/issues/137#issuecomment-6192754703),
verified live on 2026-10-18 and again on 2026-10-19, selects pilot region `uksouth` and subscription
owner @jmservera. The earlier claim here of a 2026-10-16 superseding decision
was unsupported and is withdrawn. The live issue's 2026-10-16 delivery comment
still calls these decisions open, contradicting the earlier owner selection
without recording a replacement owner decision. That historical comment and
the issue's stale summary/dependencies are not new owner approval or revocation.
This selection is not SQL-region,
zone-redundancy, sizing, cost, deployment or access approval, nor proof that the
signed-in account is bound to the approved pilot subscription. Pilot locations
and check references remain empty in the non-deployable example; its comment
calling all region/ownership choices open is stale, not a later owner decision.
The example is unchanged. Complete a private copy only after the remaining
values and real reviewed records exist. The `ownerTag` default remains an
exercise resource contact, not evidence of subscription authority.

All permitted deployments stay inside the existing resource group `ama`;
never create or delete a group, deploy subscription governance, change a
policy/exemption, or modify resources outside it for this task. Environment
names isolate resource names inside `ama`; they do not create separate security
or subscription boundaries. Separate subscriptions/groups for operational use
remain an owner design decision, not an executable instruction here.

| Setting | dev (`main.bicepparam`) | test (`main.test.bicepparam`) | pilot (`main.pilot.example.bicepparam`) |
| --- | --- | --- | --- |
| `environmentName` | `dev` | `test` | `pilot` |
| `deploymentProfile` | `development` | `production` | `production` (template default) |
| Public access (`allowPublicNetworkAccess`) | `false` | `false` | `false` (private endpoints only) |
| SQL public access | Always Disabled; no firewall | same | same |
| Key Vault (`keyVaultPurgeProtection`) | `false`: 7 day soft delete | `true`: 90 day soft delete, purge protection | `true`: 90 day soft delete, purge protection |
| Registry quarantine (`registryQuarantineEnabled`) | `false`, explicit development opt-out | `true` | `true` |
| `enableLocks` | `false` | `false` | `true` |
| `zoneRedundant` (storage ZRS, SQL zone, registry and Container Apps) | `false` | `false` | `false` PLACEHOLDER pending selected-region support and owner decision |
| `apiMinReplicas` (API minimum, independent of security profile) | `0` | `0` | `0`; explicitly choose `2` for always-on production |
| Service SKUs | IoT Hub `B1`/1 unit; SQL `GP_S_Gen5`/2 max vCores; Log Analytics `PerGB2018`; registry Premium; Foundry `S0`; Container Apps Consumption | same | same; not a pilot sizing approval |
| Model SKU/quota inputs (`modelDeployments`) | `standard`: gpt-4.1-mini; `capable`: gpt-4.1; both version 2025-04-14, `GlobalStandard`, capacity 30 | same defaults, subject to checks | same defaults; catalog checked below, quota and approved subscription binding unknown |
| Retention (fixed unless a documented module input exists) | Log Analytics 90 days; SQL PITR 14 days; blob/container soft delete 30 days; ACR 30 days; audit/digest immutability 365 days unlocked; IoT 1 day | same | same; not a legally approved retention schedule |
| `location` and `sqlLocation` | `uksouth` candidate, recheck | `uksouth` candidate, recheck | empty PLACEHOLDERs retained; pilot `uksouth` selected, separate SQL region unselected |
| `regionCheckReference`, `quotaCheckReference` | empty PLACEHOLDERs | empty PLACEHOLDERs | empty PLACEHOLDERs |
| Deployable as committed | No: complete placeholders/checks privately | No: complete placeholders/checks privately | No: additionally requires pilot decisions |

Rules:

* `apiMinReplicas` defaults to `0` in `main.bicep` and the Container Apps
  module, allowing the API to scale to zero for cost-safe demos. Requests
  after idle periods may incur cold-start latency. The valid range is `0` to
  `4`, matching the unchanged API maximum of `4`; the HTTP concurrency rule
  remains `50`. For always-on production replicas, set
  `param apiMinReplicas = 2` in the private parameter copy. Selecting the
  production security profile alone does not increase the minimum. This
  controls only the API; it does not eliminate other infrastructure costs
  or disable background workloads.
* Production is the template default. Only dev opts out of purge protection
  and quarantine explicitly. Test/pilot retain both. Development with the
  default inputs retains all controls; SQL cannot opt out in any profile.
* `environmentName=pilot` with the development profile or public access is rejected by the parameter guard (`pilotRequiresProductionProfile`).
* Promotion is by the same template version and a different parameter file: validate in dev, deploy the same commit to test with `what-if`, then to pilot after the owner approves the `what-if` output. Images are promoted by digest through the registry, never rebuilt per environment.
* `location`, `sqlLocation`, `modelDeployments` (model/version/SKU/capacity),
  `iotHubSku` and `iotHubUnits` are parameters. Do not infer that fixed service
  SKUs or every retention period are entry-point configurable.
* Empty `regionCheckReference` or `quotaCheckReference` fails a named guard;
  empty locations also fail. These references point to actual dated reviewed
  records, not approval tokens. Any nonempty string satisfies the mechanical
  gate, so a human must verify contents, freshness and exact configuration.
  Do not enter placeholder text to pass it.

Recorded region and quota checks (re-run before each deployment; a check in another subscription or on another date proves nothing):

| Check | Result | Observed |
| --- | --- | --- |
| Container Apps environment in `uksouth` | Deployed in resource group `ama` | 2026-10-08 |
| Container Apps environment in `swedencentral` | `AKSCapacityHeavyUsage` | 2026-10-08 |
| Azure SQL in `northeurope` | Not accepting new servers | 2026-10-08 |
| Model `gpt-4.1-mini` and `gpt-4.1`, `GlobalStandard`, capacity 30 in `uksouth` | Deployed | 2026-10-11 |

Historical rows above remain discovery evidence, not present capacity.

### Read-only pilot capability and quota evidence (2026-10-18, Refs #137)

Requested source: `612cbed78a35a4ab426571aa7d2aeb0ae6d691dd`,
unchanged [main.bicep](./main.bicep) (SHA-256
`daea1e37adc95f704fba7673883e0b4b6c7b65ab00179b59d8473654ab71f42a`),
the [pilot example](./main.pilot.example.bicepparam) and the
[Container Apps](./modules/containerapps.bicep), [SQL](./modules/sql.bicep),
[IoT](./modules/iothub.bicep), [Foundry](./modules/foundry.bicep),
[storage](./modules/storage.bicep) and [registry](./modules/registry.bicep)
modules. These request Consumption/internal VNet; SQL `GP_S_Gen5`, maximum
2 vCores, minimum 0.5, auto-pause 60 minutes; IoT `B1`, one unit; Foundry
`AIServices`/`S0`, OpenAI `gpt-4.1-mini` and `gpt-4.1`, each version
`2025-04-14`, `GlobalStandard`, capacity 30; StorageV2 LRS (ZRS if selected);
registry Premium. These are template requests, not approved pilot sizing.

Initial queries ran on 2026-10-18 with Azure CLI 2.91.0; identical commands
were reproduced on 2026-10-19 at 06:43 UTC. The table below records the
2026-10-18 observations; all selected fields and failure categories matched on
reproduction. No same-day reproduction is claimed. All eight referenced
source files are byte-identical at the original base above and at the later
reviewed base `fa659cfd021100f7c64f8ec73bbff76c03adf234`; this byte comparison
does not redate historical queries or turn them into a new-base deployment.
The current signed-in default subscription matched the initial query binding and its
account state was `Enabled`; this does not establish approved pilot subscription
binding or verify the named owner's permissions. Identifiers and raw results
remain private. Every remote command had a 55-second timeout and
`AZURE_EXTENSION_USE_DYNAMIC_INSTALL=no`; no extensions were installed.
Only management-plane GET/list/show operations ran, without resource enumeration
or data-plane access. Pass below means only the stated catalog fact, never
quota approval, reserved capacity, fresh deployability or operational acceptance.
Unknown is absent/incomplete evidence; Blocked is a failed query.

| Requested region/configuration | Query | Returned support or usage/limit, scope and unit | Result and limitation |
| --- | --- | --- | --- |
| `uksouth` Container Apps managed environment, Consumption | R1, R12 | Provider lists UK South; Consumption profile `cores=4`, `memoryGiB=8` | Pass regional/profile listing only. Profile cores are not environment quota or spare cores |
| Same, zone support | R1, R3 | No UK South zoneMappings returned; location GET `AuthorizationFailed` | Unknown zone support; Blocked detail query, not unsupported/false |
| Same, environment-core quota | R2 | Subscription/uksouth `ManagedEnvironmentCount`: currentValue=2, usage=2, limit=50; no unit field. No managed-environment Consumption-core metric returned | Unknown core quota. Count is not cores. Other returned metrics listed below are not substitutes |
| Candidate `uksouth` SQL `GP_S_Gen5`/2 vCores | R4 | Region Available; server 12.0 / GeneralPurpose / `GP_S_Gen5_2`: Available, Serverless, capacity 2, performanceLevel 2 `VCores`; minCapacity 0.5 Default; auto-pause default 60 `Minutes`; `zoneRedundant=true`, `supportedZones=[]`, `zonePinning=false` | Pass exact catalog SKU/zone flag only, not server admission, named-zone availability or separate SQL-region selection |
| Same, SQL regional quota | R5, R16 | Both subscription/uksouth usage collections `value=[]`; no metric, unit, use or limit | Unknown, not zero quota |
| `uksouth` IoT Hub `B1`, one unit | R6, R13 | IoT SKU collection `value=[]`; IotHubs provider lists UK South, no UK South zoneMappings | Pass resource-type regional listing only; Unknown exact B1/unit/zone support |
| Same, IoT regional quota | R7, R14 | Both API versions failed `Bad Gateway` (exit 1) | Blocked; no quota/use/limit/unit established |
| `uksouth` AIServices S0, both exact models/versions, GlobalStandard/30 each | R8 | Both inference catalog entries present, lifecycle `Legacy`; each SKU capacity default 10, maximum 1000000, minimum/step null; model-level `maxCapacity=3`; rateLimits counts 1 and 1000, each renewalPeriod 60, rules null | Pass catalog match only. Model-level and SKU capacity semantics/units not established; no capacity-30 admission claim or TPM/RPM conversion |
| Same, separate model-family regional quota | R9, R15 | CLI `[]`; REST `value=[]`. Inference usageNames `OpenAI.GlobalStandard.gpt4.1-mini` and `OpenAI.GlobalStandard.gpt4.1` have no returned usage row/unit | Unknown current use/limit. Do not sum families, use fine-tuning entries, or treat deployment capacity as subscription quota |
| `uksouth` StorageV2 `Standard_LRS` / optional `Standard_ZRS` | R10 | Exact kind/SKU entries list uksouth, restrictions `[]` | Pass regional SKU listing; not storage quota, redundancy selection or admission |
| `uksouth` registry Premium | R11, R17 | SKU collection `value=[]`; registries provider lists UK South, no UK South zoneMappings | Pass resource-type listing only; Unknown Premium-specific SKU/zone/quota support |

R2 also returned currentValue/limit (and identical usage):
`SubscriptionDedicatedNCA100Gpus` 0/0, `SessionPools` 0/50,
`ExpressEnvironmentCount` 0/500 and `SandboxCores` 0/20000, all with no unit
field. None establishes the requested managed-environment Consumption-core quota.
R8's same-name GlobalStandard fine-tuning entries were excluded by inference
`usageName`. Existing deployments/current use are not available new capacity;
no existing deployments or per-environment resources were enumerated.

Reproduction command shapes (secret-free; substitute identifiers privately):
`S=https://management.azure.com/subscriptions/<subscription-id>`.
For REST rows run `az rest --method get --url "$S/<path>?api-version=<version>"`;
for all commands use `--only-show-errors -o json` and a 55-second timeout,
with stdout/stderr redirected to private files, not a public terminal/log.
CLI subscription-scoped calls below use `--subscription <subscription-id>`;
provider metadata uses the same current default account.

| Query | Exact command or REST path and version |
| --- | --- |
| R1 | `az provider show -n Microsoft.App` |
| R2 | `az containerapp list-usages --location uksouth --subscription <subscription-id>` |
| R3 | `providers/Microsoft.App/locations/uksouth?api-version=2025-07-01` |
| R4 | `providers/Microsoft.Sql/locations/uksouth/capabilities?api-version=2023-08-01` |
| R5 | `providers/Microsoft.Sql/locations/uksouth/usages?api-version=2023-08-01` |
| R6 | `providers/Microsoft.Devices/skus?api-version=2023-06-30` |
| R7 | `providers/Microsoft.Devices/locations/uksouth/usages?api-version=2023-06-30` |
| R8 | `az cognitiveservices model list --location uksouth --subscription <subscription-id>` |
| R9 | `az cognitiveservices usage list --location uksouth --subscription <subscription-id>` |
| R10 | `az storage sku list --subscription <subscription-id>` |
| R11 | `providers/Microsoft.ContainerRegistry/skus?api-version=2025-04-01` |
| R12 | `providers/Microsoft.App/locations/uksouth/availableManagedEnvironmentsWorkloadProfileTypes?api-version=2025-07-01` |
| R13 | `az provider show -n Microsoft.Devices` |
| R14 | `providers/Microsoft.Devices/locations/uksouth/usages?api-version=2021-07-02` |
| R15 | `providers/Microsoft.CognitiveServices/locations/uksouth/usages?api-version=2025-06-01` |
| R16 | `providers/Microsoft.Sql/locations/uksouth/usages?api-version=2021-11-01` |
| R17 | `az provider show -n Microsoft.ContainerRegistry` |

R3/R7/R14 exited 1; all other listed queries exited 0, including empty
collections. Missing surfaces received at most two distinct approaches; no
permission changes, registration, quota requests or tool installs followed.
Key Vault, monitoring, networking, identity and optional edge capabilities/quota
were not checked by these receipts. This is not an all-services check.

Human review remains required and unperformed. The pilot example stays
non-deployable; no real reviewed reference was created or inserted. SQL region,
redundancy, remaining tier/sizing/network/credential ownership choices and cost/
deployment/access authorization remain open. No billable inference, device
creation, deployment/what-if, resource change or data access was performed.
Issue #137 stays open with its literal remaining criterion unticked; the
coordinator decides acceptance after review. Rerun checks before any separately
authorized deployment; a catalog listing or repeat query is not a reservation.

Supply the record references in the private parameter file or with
`--parameter regionCheckReference=<reviewed-record>` and
`--parameter quotaCheckReference=<reviewed-record>`. Rerun checks when region,
subscription, SKU, capacity, redundancy or template version changes, and
before each deployment; reusing a reference does not certify freshness.

Naming and tagging:

* Keep `{workload}-{environmentName}` as the prefix (`forward-dev`,
  `forward-test`, `forward-pilot`). Workload is 3-10 lowercase letters/digits,
  starting with a letter; the deployment wrapper enforces it. Service prefixes
  include `vnet-`, `ca-`, `job-`, `sql-` and `aif-`; SQL/Foundry and globally
  named Key Vault/storage/registry append a five-character
  `uniqueString(resourceGroup().id, location, 'v2')` hash. Key Vault uses
  `kv-{compact}-{hash}`, storage `st{compact}{hash}`, registry
  `cr{compact}{hash}`, with hyphens removed from `compact`. Existing names,
  version salt and job suffixes stay unchanged. Changing workload, environment
  or hash inputs can create new resources; incremental deployment is not
  cleanup or migration authority.
* `allTags` applies `workload=zava-forward-demonstrator`,
  `environment={environmentName}`, `dataClassification=constructed-non-identifying`,
  `purpose=non-production-demonstrator`, and `owner={ownerTag}` to taggable
  resources through every main module. Extra `tags` cannot override those
  required values. Container workloads refine `workload` to the component;
  token storage/maintenance uses `dataClassification=authentication-secrets`.
  Tags contain no secrets, IDs or resident data. Untaggable child resources
  (RBAC assignments, DNS records, diagnostics, policies/locks) rely on their
  tagged parent; do not claim every child supports tags.
* Resource-group tags are a separate owner-managed prerequisite. Resource-group
  scope templates neither create nor retag `ama`; never add a policy exception.

## Quality gates

Run from the repository root before a pull request. These checks compile locally
and need no Azure login, subscription access or deployment. Install the source
packages first, preferably in a disposable virtual environment (pip only).
Source CI runs the gates within the existing `namespace` / `src-namespace` job
in `.github/workflows/src-ci.yml`, including on `infra/**` changes. The legacy
`.github/workflows/mvp-validation.yml` also runs full infra discovery. Both
infra-test steps install the test-only `PyYAML==6.0.3` pin and the hashed
operator/runtime dependencies from `src/api/requirements.txt` before discovery.
The latter supplies real cryptography for encrypted staff-job transport tests;
do not rely on incidental transitive dependencies. PyYAML is not a production
package dependency. All existing job/check names remain
unchanged, following the #321 cut-over decision. The workflow regression tests
reject missing, unpinned or late installation without skipping pipeline controls.

```bash
python3 -m pip install --no-deps -e src/core -e src/agents -e src/api -e src/orchestrator
python3 -m pip install 'PyYAML==6.0.3'
python3 -m pip install --require-hashes -r src/api/requirements.txt
az bicep version
for file in infra/*.bicep infra/modules/*.bicep; do
  az bicep build --file "$file" --stdout > /dev/null || exit 1
  az bicep lint --file "$file" || exit 1
done
REQUIRE_AZ_BICEP=1 python3 -m unittest discover -s infra/tests -v
python3 -m pip install 'ruff==0.17.1'
ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_bicep_policy.py infra/tests/test_deploy.py infra/scripts/deploy.py
ruff format --isolated --line-length 100 --check infra/tests/test_bicep_policy.py infra/tests/test_deploy.py infra/scripts/deploy.py
```

To reproduce the test dependency boundary in a fresh venv, install only
`pip install --no-deps -e src/core -e src/agents -e src/api -e src/orchestrator`,
then install `PyYAML==6.0.3` and run
`python -m unittest discover -s infra/tests -q`. Without the explicit test
prerequisites, missing PyYAML prevents pipeline test imports and missing
cryptography blocks staff-job tests before lifecycle/cleanup assertions.
Install `python -m pip install --require-hashes -r src/api/requirements.txt`
in that same venv and rerun the identical discovery command. These are
explicit test/operator prerequisites, not a reason to add PyYAML to the
application packages, skip tests or replace real encryption.

Image-selection tests alone need only Python, with no Azure CLI or login:
`python3 -m unittest discover -s infra/tests -p test_deploy.py -v`.
They execute the real wrapper with a temporary fake `az` on `PATH`, checking
selection precedence, query ordering, bootstrap warnings, errors, overrides,
what-if/create arguments and exit codes. Four resolver mutations must fail
the same assertions. The compiled Bicep suite checks default/empty/tag/digest
behaviour and all three job image consumers; three template mutations must
fail. Both suites run in the existing infra discovery step, not a new check.
For local type checking in a pip venv, install `mypy` and run
`mypy --check-untyped-defs infra/scripts/deploy.py infra/tests/test_deploy.py infra/tests/test_bicep_policy.py`.

* `bicepconfig.json` explicitly enables the core analyzer and sets selected high-value rules to `error`: unused declarations, secrets in parameters or outputs, hardcoded environment URLs or locations, and unsafe resource identifiers. A temporary unused-parameter mutation proves both build and lint return nonzero with the named diagnostic. All entry points and standalone modules, including subscription-scoped governance, build and lint.
* `tests/test_bicep_policy.py` checks locally compiled JSON, not a committed snapshot. Public-access properties and module arguments follow the computed switch, including optional token storage and monitoring. SQL is the exception: always Disabled, no public parameter or firewall. Container Apps is internal unless development explicitly opts in. The profile/input matrix rejects unsupported production/public, no-purge and no-quarantine combinations. All three committed parameter files compile and their actual values, placeholders, named missing-check failures, naming and tag propagation are asserted offline.
* Each data service must have its own unconditional endpoint module with the right target, subnet and DNS arguments, an actual private endpoint/connection and DNS-zone-group resources. Existing endpoint tests also check service DNS zones against `network.bicep`. No-shared-key/local-auth assertions cover storage, registry, Foundry, Application Insights, Log Analytics and IoT Hub; forbidden key/credential functions are checked case-insensitively. SQL remains Entra-only without an administrator login/password. Key Vault retains profile-driven purge protection, soft delete and RBAC.
* Both `audit-archive` and `ledger-digests` must have policies on the correct container with positive, constrained retention. Mutated deep copies must fail the same assertions for disconnected endpoints, missing/public network settings, external environment mode, any SQL firewall/public switch, key authentication/functions, SQL authentication, purge/quarantine changes, wrong/missing/zero retention and guard bypass (including recorded-check and location gates). Mutations never alter working Bicep files.
* `modules/guard.bicep` uses descriptive `@minLength(1)` parameter constraints; every main resource waits for the guard directly or transitively. CI sets `REQUIRE_AZ_BICEP=1`, so absence of `az` fails rather than skips the compiled checks. Named rejection cases cover production/public access or disabled purge protection, pilot/development, public edge without production isolation or applications, SharePoint without a site ID, token-store readiness without the store, and a role map without an Entra client ID.

Findings addressed in this offline slice (2026-10-16, Refs #139): audit retention
previously lacked the positive minimum already used for digest retention; it
now has `@minValue(1)`. All-file build exposed governance policy IDs incorrectly
prefixed by the subscription ID; built-in definitions now use
`tenantResourceId('Microsoft.Authorization/policyDefinitions', ...)`, with a
compiled regression. Policy stays audit-only; Defender activation remains opt-in.
Existing lint configuration and guards were reused, not newly invented.

Limits and open items: immutability policies are intentionally created
**unlocked**, not irreversible locked WORM; the 365-day defaults are not an
approved legal retention schedule. Locking and retention approval remain owner
actions, not something these tests perform. Confirm in a subscription that ARM
validation reports the named guard and description and that deployed networking,
DNS and the optional Front Door origin work; none is established by compiled
JSON. No deployment, what-if, Azure Policy compliance check or #138 pipeline
work is part of this offline gate.

## Development access from external networks

`allowPublicNetworkAccess` (default `false`) is a development switch. When `true`, the private endpoints stay in place but the following also accept external connections:

* Storage, Key Vault, Foundry, Container Registry, Log Analytics and Application Insights: public network access enabled (network ACL default action `Allow`).
* Azure SQL is excluded: it remains Disabled with no firewall in all profiles.
  Initialization and data-plane tests require a private-network host/job.
  Historical policy/tag exceptions do not authorize bypassing this boundary.
* Container Apps environment: external (not internal) with public access enabled, so the API gets a public FQDN. The private DNS zone for the environment is not created.

The Container Registry export policy is set to `enabled` in this mode because ACR requires it when public access is on. Identity and RBAC controls are unchanged (no keys, no SQL logins). Never set it to `true` outside a throwaway development stack, and do not use it as evidence for the private-network claims in ADR 0001.

## Governance controls

Governance as code for issue #147 (ADR 0002 decision 6). For this synthetic
exercise Juan Manuel Servera is the Legal, Compliance and DPO owner. The
[verified pilot decision](#environments) selects `uksouth` and subscription
owner @jmservera only; resource contacts and read-only capability checks do not
establish subscription binding, deployment or spending authority.
Agents retrieve, compare, summarize and flag only. Rule activation,
consent, safety, legal interpretation and financial commitments require named
human approval; ADR 0005 is accepted for synthetic development only, with real
owners and sources still a gap before operational reliance.

| Control | Where | Decision | Owner | Cost |
| --- | --- | --- | --- | --- |
| Azure Policy assignments (SQL and storage public access, Key Vault deletion protection, required tags) | [`governance.bicep`](./governance.bicep), subscription scope, deployed separately by the subscription owner | Built-in definitions, audit only (`enforcementMode=DoNotEnforce`): policy reports non-compliance but blocks nothing; a Deny stance is an open owner decision | Juan Manuel Servera | No charge for Azure Policy |
| Defender for Cloud plans (Storage, SQL servers, Key Vaults, Containers) | [`governance.bicep`](./governance.bicep) | No pricing resource is submitted until the owner accepts a cost and sets `enableDefenderPlans=true`; then the four plans request Standard. Existing paid or Free subscription plans are preserved when disabled | Juan Manuel Servera | Per-resource pricing, not yet estimated: open item, confirm in the Azure pricing calculator before enabling |
| Resource locks | `enableLocks` in `main.bicep` (Key Vault, SQL, storage) | [`main.pilot.example.bicepparam`](./main.pilot.example.bicepparam) (a non-deployable example with placeholders; copy it to a private file and fill every value) sets `true`; `pilotRequiresLocks` rejects a pilot override to `false` before dependent resources; dev/test retain their explicit lock choice | Juan Manuel Servera | None |
| Tagging standard | `allTags` in `main.bicep` | Required tags on taggable resources, component refinements and untaggable-child exceptions documented in Environments; group tags remain separate | Juan Manuel Servera (exercise resource contact) | None |
| Known exceptions | [`policy-exceptions.json`](./policy-exceptions.json) | Historical EX-001: `SecurityControl=Ignore` on the development resource group (MCAPS SQL public-access policy); expires 2026-12-31. It does not authorize public SQL in current templates or helpers | Juan Manuel Servera | None |

```bash
az deployment sub what-if -l uksouth -f infra/governance.bicep
az deployment sub create -l uksouth -f infra/governance.bicep
```

The policy and Defender decisions, owner, billable inventory and pending cost approval are recorded in [`defender-decision.json`](./defender-decision.json); unit prices were not retrievable on 2026-11-01 and are not invented.

Open items: Defender cost estimate and the decision to enable; renewal of EX-001 after 2026-12-31 (never on a pilot group); whether to switch any policy from audit to Deny; the group must carry the required tags before Deny is considered. The platform-wide MCAPS policy itself is managed outside this repository.

The synthetic-development decision is to audit the selected public-access,
purge-protection and tag controls without replacing or weakening existing
platform policies. DoNotEnforce applies only to these new assignments, not to
the subscription's existing enforcement. Paid Defender activation is deferred
because an accepted cost and service-coverage appraisal are absent; the Free
tier is not a replacement for image scanning or workload protection. Submitting
Free would downgrade a shared subscription, so disabled opt-in now creates no
pricing resources rather than changing any plan. This is a code decision, not
evidence of deployed policy compliance, protection, or financial approval.
The subscription-scoped governance template is outside a resource-group-only
`ama` execution boundary and was compiled/tested only in this task.

Authoring review, 2026-10-27 (Refs #147/#138): policy/Defender definitions,
pilot locks, tags and the dated exception register are present; no policy
deployment/compliance, Defender cost acceptance or protection is established.
The subscription owner @jmservera must record selected plan/subplan coverage,
current subscription-specific quantities and cost, and an explicit activation
decision before enabling paid plans. Cost remains **not estimated / not approved**,
not zero. No new exception, renewal or public SQL bypass is approved.
Offline pipeline contracts are not observed federation, environment approval,
registry publication, deployment or health acceptance. Both issues remain open
at those owner/live gates; no Azure deployment was performed for this authoring.

## Hardened source image rollout (#118)

Refs #118. All six application containers are defined in
[`modules/containerapps.bicep`](./modules/containerapps.bicep): API, agents,
orchestrator, import, token renewal and ledger verification. Compiled tests
verify each image parameter, API health probes and 2-4 replicas, plus the
default-off Premium Front Door/WAF/Private Link edge. Maintenance jobs retain
their direct Python module commands; no guard-bearing image path is required.
Worker transport remains #144 (see the hosting status table below); a Bicep resource is not worker acceptance.

Hosted hardening acceptance is **Partial**: the
[Container Apps 2025-07-01 schema](https://learn.microsoft.com/azure/templates/microsoft.app/2025-07-01/containerapps)
and 2026-07-01 schema were checked on 2026-10-16 and expose no
`readOnlyRootFilesystem`, capability-drop or `securityContext` settings for
these container definitions. No unsupported property is added and no deployed
kernel enforcement is claimed. Images remain non-root but no longer carry a
fail-closed startup guard that would prevent Container Apps startup. Local/CI
Docker contracts explicitly set `--read-only --cap-drop ALL --security-opt
no-new-privileges` and verify the actual kernel state. They also exercise plain
non-root startup for compatibility; this is not evidence of an Azure rollout.
A future supported hosted configuration and private runtime proof are still
required to meet the full hardening criterion. No hosting architecture change
or deployment approval is inferred.

### Hosting completeness status (issue 144, 2026-11-01)

| Criterion | Status | Evidence |
| --- | --- | --- |
| Worker and job images real, versioned, deployed through the pipeline | Unmet | Images and the `src-deploy.yml` digest pipeline are real. The agents and orchestrator entrypoints still only print a version; queue transport and API post-back are not built |
| Scale rules, probes, limits, rollback | Defined and compile-tested | `test_api_replicas_probes_and_private_edge_contract` asserts the API http rule (50 concurrent, 0 to 4 replicas), Startup, Liveness and Readiness probes, 0.5 vCPU/1 GiB limits, Single revision mode, the agents queue rule and job limits. No live rollout was run |
| Hardening enforced in the deployed app | Partial, platform-blocked | See the hosted hardening note above; CI Docker checks only |
| Load test on the declared fixture | Run locally, not at declared scale | [`scale-load-2026-11-01.json`](../docs/architecture/scale-load-2026-11-01.json) |
| Single-replica restart with audit persistence | Verified on the SQL store | `src/api/tests/test_restart_audit.py` reopens the store; ledger entries, chain and digest persist. No Azure restore proof |

Revision rollback: apps use `activeRevisionsMode: Single`, and a failed Startup
or Readiness probe keeps the previous revision serving. There is no historical
digest redeploy path: `pipeline.py` accepts only digests built, scanned and
pushed by the current run for the current `RELEASE_SHA`, and `src-deploy.yml`
releases only the head of `main` after a successful manual Source projects CI
run for that exact SHA. To roll back an applied release, revert the change
through a reviewed pull request, run Source projects CI manually on the
resulting `main` head, then dispatch `src-deploy.yml` for the target environment
so the rebuilt images pass scanning and admission, the environment approvals
apply and what-if runs first. Confirm `/healthz` and the ledger-verify job
afterwards. No traffic splitting is used, and a guarded redeploy of an earlier
release identity would be a separate, tested change.

Load run, from `src/api` with installed distributions and
`PYTHONPATH=../core/tests:../agents/tests`:
`python3 tests/scale_load.py --duration 120 --out report.json`. The recorded run
used 60,000 fictional homes (53,821 contact and appointment events, not the
declared 600,000), 20 sessions and 5 requests/s for 120 s of the declared 1,800 s,
one in-process API replica on a SQL store (SQLite), no inference. Homes carry an
explicit synthetic marker and a deterministic lifecycle, and the run fails unless
the dashboard covers all 60,000 homes. Latency includes reading the full response
body. Warm p95 was 7,076 ms list, 7,512 ms detail and 7,698 ms dashboard with no
errors, so all three routes exceeded the NFR-002 staff thresholds (1 s, 1 s and 3 s)
in this run; the first cold dashboard request took about 1.5 s. The dashboard
recomputes every lifecycle under the store lock, and the single process, load
client and dashboard share one interpreter, so the figures are local measurements
that need a hosted run before any capacity decision. The stored report timed each
request from dispatch to completion, so it omits scheduling backlog and is a lower
bound for that metric; newer runs time from scheduled arrival, and later runs
report the fixed observation window, in-window throughput (5% tolerance) and drain
time separately. The declared duration and
event volume were not run, and the run makes no production, autoscaling or
availability claim and is not an Azure measurement. Usage and cost drivers per unit
of load (600 requests, 3.99 SQL statements per request, 0 assistant calls,
1 replica, 105 process CPU-seconds, 708 MiB resident after the run, 0.5 vCPU/1 GiB
billable at limit) are in the report; cost is Unknown because no price source is
set (BRD OD-51). The 708 MiB resident figure includes the fixture and the load
client sharing the process, and approaches the 1 GiB limit, so size the memory
limit against a hosted run.

Front Door Premium, WAF and origin Private Link remain infra-only gated
definitions: `enablePublicEdge=false` by default, production/private profile
required, no new edge deployed publicly. No Azure deployment or what-if, policy
bypass, SQL public access change or new deploying CI is part of this work.
See the [criterion audit](../docs/architecture/cutover-evidence-pack.md#deployment-hardening-audit-118-2026-10-16).
ADR 0005 remains accepted only for synthetic development; Juan Manuel Servera
is the exercise Legal, Compliance and DPO owner, not evidence of operational
legal approval. Real owners and sources remain a gap before operational reliance.

## Identity and role assignments (issue 141)

[role-assignments.json](role-assignments.json) lists every identity, scope, role and reason, plus SQL grants. `tests/test_identity_rbac.py` parses every Bicep role assignment (principal, role definition and scope, including the token-maintenance rows) and fails when the set of (identity, role, scope) tuples differs from the matrix, when Owner, Contributor, User Access Administrator or Reader appear, or when a shared key, SQL login or connection string is introduced. The only connection string is the Application Insights ingestion string (not a data credential); `entra-client-secret` and `entra-token-store-sas` are inventoried in [secret-inventory.json](secret-inventory.json).

| Identity | Scope and role | Reason |
| --- | --- | --- |
| api | Key Vault Secrets User; blob Data Contributor; queue Message Sender; AcrPull; OpenAI User and Azure AI User (only when `enableApiAi`); Data Receiver on the dedicated IoT telemetry Event Hub; SQL reader, writer, ddladmin | Serve the workbench, enqueue tasks, read telemetry |
| agents | queue Data Contributor; AcrPull; OpenAI User and Azure AI User; no SQL | Run agents, reach data only through the API |
| orchestrator | queue Message Sender; AcrPull; no SQL | Enqueue only |
| import | blob and queue Data Contributor; AcrPull; SQL reader and writer | Imports |
| token-maintenance | Blob Delegator (account); blob Data Contributor (container); Secrets Officer (one secret); AcrPull | Renew the short-lived SAS |

Chat and memory store (ADR 0004, accepted by the owner 2026-10-15): no Bicep resource exists yet. When added it gets one data-plane role for the api identity, local auth disabled, and a new matrix row.

Entra registration: [entra/app-registration.json](entra/app-registration.json)
records the single-tenant audience, callback path and eight workbench roles.
`setup-entra.py` reads its roles/callback path, preserves existing role IDs and
unrelated grants, and discovers deployed callback hosts. The older creation
shell helper remains for explicit historical procedures; it is not the
recommended repair path. See [API registration management](#api-registration-management-with-the-existing-m365-session).
Juan Manuel Servera is the exercise Legal, Compliance and DPO owner; that does
not establish tenant administrator authority or operational approval.

Open items:

* Owner sign-off of the matrix review (reviewer line is pending).
* Contractor B2B guest model (ADR 0002, #116) is proposed, not confirmed; tenant guest and cross-tenant policy are manual tenant steps. The design is recorded in `entra/app-registration.json` (`contractorIdentity`): guests may hold only the `Contractor` app role, assignment is required, and the staff, roster and application-admin initializers accept enabled `Member` users only. `test_identity_rbac` checks these properties; the tenant owner's confirmation remains open.
* Drop `db_ddladmin` from the api identity after schema migration moves out of app start.
* Live `az role assignment list` comparison against a deployed group was not run here.

## Regulatory assistant capability roles (#217)

The Entra registration manifest keeps auxiliary `capabilityRoles` separate from
the mutually exclusive staff `appRoles`. The registration script declares all
four: `ZavaForward.RuleAuthor`, `ZavaForward.RuleOwner`,
`ZavaForward.RegulatoryChat` and the constructed-only `ZavaForward.AIRestart`
capability (#221). Both setup and the historical shell helper define these
capabilities, but ordinary staff roster/default assignment remains limited to
staff `appRoles`. A capability definition is not an assignment, consent or
actual OD-35 appointment. These supplement, never replace, one staff role.
The API grants them only from a trusted claim bound to a uniquely provisioned
principal; a local staff field or email fallback does not grant authority.
Holding multiple capabilities never permits author self-approval.

Manifest/script/API parity is checked in `test_identity_rbac`. This update
changes local declarations only: no tenant role creation/assignment, identity
administration, Azure deployment or actual revocation test was performed.
Provisioning and human approval remain unmet operational gates. The synthetic
exercise DPO is Juan Manuel Servera; no real-company delegation is inferred.

## Key Vault secret lifecycle

Secrets are listed in [secret-inventory.json](secret-inventory.json) with an owner, rotation interval and expiry alert window. `infra/scripts/secret_lifecycle.py` checks vault metadata against it (never secret values), produces the access review record and prints the rotation steps. Run `python3 -m unittest discover -s infra/tests -q` for its tests.

| Secret | Rotation interval | Expiry alert | Owner |
| --- | --- | --- | --- |
| `entra-client-secret` | 180 days | 30 days | Juan Manuel Servera (repository-recorded owner; confirm or delegate) |
| `entra-token-store-sas` | 1 day (renewal job) | 3 days | Juan Manuel Servera (as above) |
| `resident-demo-password-verifier` | 30 days | 7 days | Juan Manuel Servera (as above) |
| `resident-demo-session-key` | 30 days | 7 days | Juan Manuel Servera (as above) |

A test requires every vault secret declared in `resident-demo.bicep` and `containerapps.bicep` to appear in the inventory with an owner.

Expiry alerting: the vault diagnostic setting sends all logs to Log Analytics, and `modules/keyvault.bicep` adds a scheduled query alert on `SecretNearExpiryEventGridNotification` and `SecretExpiredEventGridNotification` (logged whether or not an Event Grid subscription exists) routed to the operations action group. A second alert fires on repeated 401/403 data-plane results. Every secret must carry an `--expires` date or the alert cannot fire; `check` reports secrets with no expiry.

### Rotate the Entra client secret

Run `secret_lifecycle.py rotation-plan --vault <vault> --app-id <id>`; `secret_lifecycle.py rotation-simulate` runs an offline model of the same order and exits non-zero if sign-in would fail at any step (tests also show that deleting the old credential first, or before the app refreshes, fails). The model proves the ordering only, not a live outage-free exercise. The order gives no downtime: append a new app credential (the old stays valid), write it as a new version of `entra-client-secret` with an expiry, let the versionless Container Apps reference refresh (up to 30 minutes) or restart the active revision, verify sign-in, then delete the old credential. Do not delete first. The repeatable scripted step is `create-api-app-registration.sh -v <vault>`; add an `--end-date` when setting the secret.

### Access review

Quarterly (`reviewIntervalDays` 90), export `az role assignment list --scope <vault id> --include-inherited -o json` and run `secret_lifecycle.py review --assignments roles.json --reviewer <name>`. A named human sets each pending decision to keep or remove and the signed record is kept with the operations evidence. `secret_lifecycle.py review-status --record review.json` exits non-zero while any decision is pending, no reviewer is named or `nextReviewDue` has passed, so a scheduled run can flag a missing or stale review. Owner alone gives no data-plane access.

### Open items

* Owner confirmation (or delegation) for each secret and for the review.
* A live no-downtime rotation exercise in the test environment; only the ordering and checks are tested offline.
* Confirmation after deployment that the alert rules evaluate in Azure Monitor (not verified here; the template builds with `az bicep build`).
* Scheduling the review and `check` runs (for example a calendar task or pipeline) is an owner choice.

## Disposable Key Vault for development

`keyVaultPurgeProtection` (default `true`) keeps 90 day soft delete with purge protection. Set it to `false` for a disposable environment: 7 day soft delete and no purge protection, so a deleted vault can be purged with `az keyvault purge`. Purge protection cannot be switched off on an existing vault, so choose before the first deploy. The vault name also hashes the location, which avoids collisions when a resource group is recreated.

## Tested deployment

Region notes for `northeurope` (observed 2026-10-08): Azure SQL was not accepting new servers, so set `sqlLocation` (for example `uksouth`; the private endpoint stays in the VNet region), and `gpt-4.1*` has no pay-as-you-go SKU, so override `modelDeployments` (for example `gpt-5.4-nano` and `gpt-5.4` with `DataZoneStandard`).

Deployed on 2026-10-08 to resource group `ama` with `location=uksouth environmentName=test`. `swedencentral` returned `AKSCapacityHeavyUsage` for the Container Apps environment, so keep `location` a parameter. The SQL admin can be a user, group or application (`sqlAdminPrincipalType`).

## Deploying the workbench image and sign-in

### Source-image cut-over (#200, 2026-10-16)

Execution evidence is in the
[cut-over pack](../docs/architecture/cutover-evidence-pack.md): four images
built and passed bounded remote runtime checks. The initial bootstrap failed
on Microsoft.Devices registration and SQL public-interface restrictions; the
owner-authorized [private continuation](#private-cut-over-proof-2026-10-16)
has now deployed a healthy source API and passed bounded SQL/HTTP/restart proof.
Tenant staff/authorized HTTP and owner sign-off remain outstanding. Plain `az acr build`
failed on existing BuildKit-only `RUN --mount`; the tested alternative is
`az acr run -r <registry> -f acr-cutover.yaml --timeout 1800 src`, using the
[source task](../src/acr-cutover.yaml). This does not satisfy the unavailable
local Docker checks or authorize subscription/tenant changes.

Where Docker is available, build and run locally before registry publication.
The 2026-10-16 owner direction instead permits ACR Tasks with no local Docker;
its observed contracts are separately labelled in the pack. ADR 0006 uses `src/` as
context so named workload packages can include sibling core; never use `mvp/`
or the repository root as context. The API starts with `python -m zava_forward.api`.
The token-store and ledger jobs use `orchestratorImage` with commands
`python -m zava_forward.orchestrator.token_store` and
`python -m zava_forward.orchestrator.digest_blob --publish`, retaining their
existing identities and grants. No approval authority changes.

```bash
docker build -f src/api/Dockerfile -t zava-forward-api:local src
docker build -f src/orchestrator/Dockerfile -t zava-forward-orchestrator:local src
az acr run -g ama -r <registry> -f acr-cutover.yaml --timeout 1800 src
python3 infra/scripts/deploy.py --resource-group ama --registry <registry> \
  --workload cutover --environment test --parameters <private-parameters> \
  --orchestrator-image <registry-server>/zava-forward-orchestrator@sha256:<digest> \
  --parameter apiImage=<registry-server>/zava-forward-api@sha256:<digest>
```

Publish after the applicable image checks and review the what-if before deployment
to the existing `ama` resources. Use new immutable tags; never overwrite tags
referenced by historical running revisions. The commands above are instructions,
not themselves evidence of deployment. See the dated private continuation for
actual source-image rollout/health results and its synthetic-only boundary.
Private data copy/encrypted backup and #201 owner sign-off remain unmet.

After cut-over (2026-10-27) the workflow display names were renamed in one change
(issue #200 owner decision, 2026-10-15): `MVP CI` is now `Source CI` and
`MVP validation` is now `Source validation`. File names and job IDs are
unchanged. Branch protection on `main` was absent when checked (2026-11-01), so
no required check was dropped; add any future required checks under the new names.
The retired prototype workflow is already absent; do not recreate it.

### Historical deployment recipe

Observed 2026-10-11 in resource group `ama` (`uksouth`, `environmentName=test`, `deploymentProfile=development`):

```bash
az acr build -r <registry> -f src/api/Dockerfile -t zava-forward-mvp:<tag> src
az login --tenant <tenant> --allow-no-subscriptions          # as an Application or Global Administrator
infra/scripts/create-api-app-registration.sh -u https://<api-fqdn> -a <admin-upn>:ProgrammeManager -v <key-vault>
python3 infra/scripts/create-sql-users.py ama <sql-server> retrofit id-forward-test   # as the SQL Entra admin
az deployment group create ... -p entraClientId=<client id> apiImage=<registry>.azurecr.io/zava-forward-mvp:<tag>
```

Notes:

* The registry accepts `az acr build` when public access is on (development profile).
* The image carries no data. Seed the SQL database once from an operator machine (see `src/core/README.md`, Azure SQL store); set `oid` on a staff record to a signed-in user's object id so that user maps to a workbench role.
* With `entraClientId` set, `/` is a public branded welcome and `/sign-in`
  deliberately enters Microsoft sign-in. `/app` and every data API stay
  protected; anonymous APIs return 401. Only the welcome, its stylesheet/logo,
  sign-in route and probes are excluded. The client secret is a Key Vault
  secret named `entra-client-secret` read through the API identity.
* The API listens on 8088 and serves only `/healthz` for probes (there is no `/readyz`). The agents, orchestrator and import workloads still run the placeholder image because no code for them exists yet.
* `ZF_ENV=production` is set when authentication is on, so the map has no background until `tileUrl` is set (for a dev test: `tileUrl=https://tile.openstreetmap.org/{z}/{x}/{y}.png tileAttribution='&copy; OpenStreetMap contributors'`, within the OSM tile usage policy; choose a licensed provider before real use). The CSP follows the tile host.
* Demo basemap (issue 119, 2026-10-25, scoped owner approval to 16:02Z): on the live `ca-cutover-test-demo-api` only `ZF_TILE_URL=https://tile.openstreetmap.org/{z}/{x}/{y}.png` and `ZF_TILE_ATTRIBUTION` (the `OSM_ATTRIBUTION` string in `server.py`) were set with `az containerapp update --set-env-vars`, single-quoting both values because the attribution contains quotes, `&` and angle brackets. Both were empty before; revision `--0000006` took 100 percent of traffic on the same image, and a sanitized before and after diff showed only those two entries changed. Rollback is setting both back to empty strings and confirming both keys. This is the public OpenStreetMap tile service for a synthetic demo only: best effort, no SLA, the browser discloses its IP, the viewed map area and the site origin to OSM, the attribution must stay visible, and there must be no bulk, prefetch, offline or headless use ([tile usage policy](https://operations.osmfoundation.org/policies/tiles/), [privacy policy](https://osmfoundation.org/wiki/Privacy_Policy)). It is not a production provider decision; #119 licence, cost, coverage, processor choice and screen-reader acceptance remain open.
* Active-case removal from the live `retrofit` database (2026-10-25, the obsolete synthetic proof case; schema wording corrected 2026-10-28): `cases` is an updatable ledger table, so the guarded single-row `DELETE` removes the current row but retains its old body in system-managed ledger history. The guard's non-history reference scan does not establish data erasure. The same transaction appends one `case_removed` entry to the append-only `audit` ledger; the audit trigger is an alternative for non-ledger databases, not extra protection on the live ledger. See the [ledger-safe schema research](../.copilot-tracking/research/2026-10-24/ledger-safe-migration-360-research.md#evidence). The API process keeps cases in memory and never evicts them after an external delete, so restart the revision afterwards (`az containerapp revision restart`) before checking the map or lists. Evidence: `.copilot-tracking/*/2026-10-25/remove-synthetic-example-360-*`. This was a one-off owner-authorised active-case removal, not data erasure or a general delete API.
* The previous `allowedPrincipals` restriction on the auth config was removed: it listed managed identity client ids where object ids are expected and would have blocked signed-in users. Access is limited by the app role requirement instead.
* For the existing MVP's direct, human-reviewed model drafts, explicitly set
  `enableApiAi=true`. This grants the API identity model invocation access and
  supplies `AI_ENDPOINT` and both deployment names. The default remains false
  for the separately proposed agent-runner topology. Placeholder worker images
  do not provide real AI to the workbench; verify a result with `source=ai`.
* `entraRoleMap` can explicitly map an existing registration's role values to
  workbench roles during a rename. It does not update tenant roles or callback
  URLs and is not proof of a completed identity rename. An authorised
  registration owner must update those separately; remove the transitional
  mapping when the new default `ZavaForward.*` values are issued.

### Small employee model prerequisite (2026-10-28, Refs #514)

`main.bicep` now defaults to one `standard` deployment using
`gpt-4.1-nano` / `2025-04-14` / `GlobalStandard`, capacity `1`.
`chatModelName`, `chatModelVersion`, `chatModelSku` (`GlobalStandard` or
`Standard`) and positive `chatModelCapacity` parameterize that default.
`modelDeployments` remains the explicit nonempty array override for existing
or separately evaluated model sets. The first entry backs the standard route;
the second backs the capable route, or a single entry backs both. Sharing a
small model does not prove a stronger-task quality threshold. Keep explicit
arrays on existing stacks rather than unintentionally changing evaluated tiers.
`NoAutoUpgrade` and `Microsoft.DefaultV2` filtering are retained.

With `enableApiAi=true`, the API receives the account-advertised Azure OpenAI
endpoint, deployment names and `AI_MODEL_VERSION`/`AI_MODEL_VERSION_STRONG`
derived from the model name plus dated version. The latter must match the
provider response `model`, for example `gpt-4.1-nano-2025-04-14`, not just
`2025-04-14`. The generic Foundry endpoint used by other workloads is retained.
API AI remains disabled in Bicep by default. No keys are needed: preserve
the attached API identity selected by `AZURE_CLIENT_ID`, account-scoped
Cognitive Services OpenAI User access and private networking. See the
[API configuration contract](../src/api/README.md#configuration).

For the existing employee account `aif-cutover-test-rzsrg` in `ama`, the
coordinator's intended settings after #514 merges are:

| Setting | Value |
| --- | --- |
| `AI_ENDPOINT` | `https://aif-cutover-test-rzsrg.openai.azure.com/` |
| `AI_DEPLOYMENT` | `standard` |
| `AI_DEPLOYMENT_STRONG` | `standard` |
| `AI_MODEL_VERSION` | `gpt-4.1-nano-2025-04-14` |
| `AI_MODEL_VERSION_STRONG` | `gpt-4.1-nano-2025-04-14` |
| `AZURE_CLIENT_ID` (retain) | `1b1fe44e-f4cf-4aae-98d0-b30c7927a5e3` |

Azure readback on 2026-10-28 confirms exactly one `standard` deployment,
Succeeded, with the configuration above, `NoAutoUpgrade` and
`Microsoft.DefaultV2`. The missing API account-scoped Cognitive Services
OpenAI User assignment was added for principal
`6ac4c6b9-c516-4e24-81a6-f32663a93aab`; no other role was added.
The live app remains revision `ca-cutover-test-demo-api--0000006`,
with AI_* settings absent and the same selected identity. No app update or
inference occurred.

This task authorizes only the one small model and that missing OpenAI
User assignment, not a live container-app update, full-stack Bicep deployment,
other assignments or inference. Coordinator redeployment must preserve
SQL/Blob/auth/identity settings and separately check registered task releases,
evaluation/model bindings, budget/incident controls, private reachability and
a bounded `source=ai` result. Manual/workflow-only routes and human/resident
approval boundaries remain unchanged. The initial gpt-4o-mini request was
rejected with `ServiceModelDeprecating`; catalogue visibility alone did not
permit new deployment. The accepted gpt-4.1-nano version is listed as Legacy,
with inference retirement on 2027-04-14 in the account model metadata checked
on 2026-10-28; reevaluate availability before a later deployment.

Cost authority is **USD30 additional employee AI through 2026-10-31**,
separate from resident resources/budget. Capacity one is throughput, not a
hard dollar cap or an automatic expiry. No inference is performed by this
change; no exact token price, forecast or actual charge is asserted. Do not
silently continue billable use after that authorization window.

### Current exercise handover (2026-10-13)

The dated deployment notes above are history. The newer five-assistant
handover below supersedes the account-switch serving revision.
At that account-switch handover, after the from-empty rebuild, callback initialization, public welcome/photo
setup and tenant staff reconciliation, the deployed API is
`ca-forward-test-api`, serving image
`crforwardtestrzsrg.azurecr.io/zava-forward-mvp:account-switch-20261013-01`
in ready revision `ca-forward-test-api--0000009`. The tested image digest is
`sha256:8cf327786ac2b891a586e78981b4abf0cc9c86313d721cef74ea7fcda80fa599`.
The account-switch rollout changed the image only; private comparisons
preserved app/auth settings, SQL/AI configuration and secret references.

The owner reports working administrator and Coordinator sign-in. Eleven
tenant members are privately provisioned for ten stable internal positions
plus a supplier-scoped Contractor; no roster is committed. This is not
acceptance of every role, guest onboarding or a changed authenticated session.
The existing registration and `ProperWarm.*` compatibility role map are
retained deliberately, not silently renamed. Next-run recovery starts with
the check modes below; do not replace the registration, reseed the workload
or grant runtime tenant-management rights to fix a sign-in failure.

For observed outcomes and pending product gates, see the
[dated addendum](../docs/case_study_48_addendum.md#observed-deployment-and-identity-learning-2026-10-1213).
Actual account replacement and own-photo acceptance remain separate from
operator checks, unit tests and the source-head CI/rubric results on #65.

### Five-assistant version: current handover

Historical rollout: after explicit owner authorization, image `assistants-20261013-02`
was published and deployed to the existing API as revision `--0000010`, pinned
to ACR digest
`sha256:d3e652cec1bdef8846270a75c124d55743bdb757231ffaeae585cc423e6b8786`.
Private comparisons preserve SQL/AI/auth configuration, workload identity,
scale and the old controlled-domain fingerprints. No model call occurred.

Live Azure SQL exposed a ledger-only DDL incompatibility before assistance
could run. Source `99aeaac` fixes fresh append-only ledger events, preserves
initial generated procurement/as-of, and enriches the
[existing synthetic generator](../docs/reference/research/retrofit-synthetic-data/README.md#mvp-operational-coverage-2026-10-13).
After preserving the concurrent intended-proposal identity fix, combined
backend source `ec7721b` passes all 73 local actual SQL tests. A later
populated-visits rendering correction yields latest source `cd14b3b` and local
image `assistants-20261013-05`, with 389-test discovery (316 passed, 73 conditional
skips), 21 browser regressions and 21 exact-image generated-data UI/API/local
restart checks. It was subsequently published and deployed on 2026-10-14
as described below. Full evidence is in
[ADR 0002](../docs/adrs/0002-pilot-readiness-architecture.md#fresh-ledger-and-synthetic-coverage-learning-2026-10-13).

The owner stopped migration and requested a synthetic database reset. QA
authority was removed; historical revision `--0000011` served image
`d3e652ce`, with proactive off and assistance disabled. Database deletion was
cancelled on 2026-10-13. The owner explicitly reauthorized deletion/recreation
and all offered remaining delivery on 2026-10-14; that cancellation no longer
blocks the exact authorized action.

Only `retrofit` was deleted/recreated, with ledger enabled, serverless Gen5
2 vCore/minimum 0.5, auto-pause 60 minutes, 32 GB, local backups, 14-day
retention/12-hour differential backups and restored diagnostics. Original
contained user SIDs/roles/grants and all 11 privately bound staff were restored
without tenant changes. The generated date/procurement baseline now contains
980 cases, 38 booked visits (11 in the week 2026-10-12 to 2026-10-18), 12
Finance/quality/grant/request records, one package/601 source orders and four
offered handoffs. Previous recommendations/audit were intentionally reset.

Current serving revision is `ca-forward-test-api--0000012`, image05/source
`cd14b3b379026a87ebfa3e9058ac10c0df7888eb`, pinned to ACR manifest
`sha256:e0254cb3a0599c21802f0b6515f975550cf00ddce4849d04fd3fa3d50683af20`.
Existing identity, auth configuration and scale are preserved; an independent
auth-token rotation stamp was retained. Health and restarted replicas pass.
This is
explicit exercise reset authority, not a general reseed or evidence-deletion
permission. Preserve tenant registration/authentication; do not grant runtime
tenant-management permissions. Keep real QA within its effective expiry,
call/token allowance and scoped spend approval; never extend or replenish it
because a reset occurred. Token limits are not a currency guarantee.

Renewed bounded operator QA used the registered service inside this serving
workload, with process-local authority, 10-call/126000-token allowance and
one-hour expiry, proactive off. All five returned distinct citation-validated
`ready` proposals through Azure OpenAI deployment `standard`, model
`gpt-4.1-mini-2025-04-14`: five attempts, 6884 total tokens and 15 ledger events.
Independent SQL controlled-domain hashes stayed unchanged; full assistant
table content hashes, outputs and usage survived a real revision restart.
The normal serving app still has no assistant authority and proactive remains
off; no standing paid worker or fabricated human verification/acceptance.

AC-057 requires a registered assistant through the changed deployed API,
provider/model/usage/outcome and independent actual SQL task/event evidence
before/after an app restart, plus unchanged controlled state and failure/
manual handling. General SQL Server CI or an anonymous HTTP 200 cannot
replace that proof. The operator service/model/SQL/restart portion is now
observed, not blocked on reset authorization. A real staff-authenticated
browser/API acceptance session, semantic calibration, role/accessibility
acceptance and measured benefit remain separate and are not claimed by
operator execution or local Chromium fixtures.

## Post-deployment API authentication initialization

Refs #360. Use one command after a rebuild, or to resume an interrupted setup:

```bash
python3 infra/scripts/setup-entra.py
```

No required resource arguments. Add `--yes` to approve the SQL plan/restart
non-interactively; it does not approve tenant admin consent, migration or spend.
The default resource group is `ama` (other groups are
refused). API selection prefers `zava-forward-role=api`, then the existing
`workload=api` tag, then `ca-*-api`, except that an explicitly tagged direct
API is preferred during migration as described below. New Bicep deployments tag the API and
Front Door profile/endpoint (`zava-forward-role=api-edge`). Existing untagged
resources still work. Ambiguity prints resource-name candidates, never IDs;
an interactive run asks one plain question rather than guessing. A headless
run reports candidates and stops; optional overrides are for unusual ambiguity:

```bash
python3 infra/scripts/setup-entra.py --container-app ca-cutover-test-api
python3 infra/scripts/setup-entra.py --check
python3 infra/scripts/setup-entra.py --dry-run
```

During old/new coexistence, a unique `zava-forward-ingress=direct` API wins
without a name guess. It must also have `zava-forward-role=api`, or the
compatible `workload=api` tag with no modern role tag. On 2026-10-17, read-only
ARM metadata showed precisely that legacy-workload/direct combination on
`ca-cutover-test-demo-api`; the retained `ca-cutover-test-api` has no direct tag.
The former modern-role-only direct filter missed this configuration and fell
back to two workload candidates. The compatibility fix accepts the existing
explicit deployment tag; it neither adds a selector nor changes Azure resources.
More than one eligible direct API, including mixed modern/legacy tags, still
refuses; a conflicting modern role does not qualify. An exact `--container-app`
always overrides preference, including deliberate old-API/Front Door selection.
No API, edge or backing service is removed. Offline regressions are not a live
laptop setup, human sign-in or SQL acceptance result.

`ca-cutover-test-agents` is not the API and is never selected by the fallback.
The script matches enabled Front Door origins to the selected API FQDN and
uses only enabled HTTPS `/*` routes. It includes the API hostname, default
edge domain when linked, and attached custom domains after validation and
deployment succeed. Multiple eligible edges require `--edge-profile`, unless
one linked profile carries the role tag. `--public-url https://<edge-host>`
asserts a discovered eligible origin; it cannot inject an unrelated callback.
This handles both main's edge module and #344's additive existing-app edge.
In particular, setup retains the existing `Custom` forwarding convention and
`X-Forwarded-Host` / `X-Forwarded-Proto` header names used by the pending
`public-edge-existing.bicep` and `edge-existing-auth.bicep` deployment.
It does not replace that configuration with `Standard`. The legacy CLI also
accepts `--public-url` through its delegation to setup.
It does not create an edge, approve Private Link, validate DNS/certificates or
open the private data network.

A UUID auth client selects its existing tenant registration. A managed-identity
value such as `systemAssignedIdentity` is not a registration UUID: find by
exact `zava-forward-api` display name, then by application role tag; create
only when neither exists. Duplicate matches stop. `--registration-name` or
`--client-id` selects an intended registration without printing its identifier.
Missing enterprise app and manifest roles are added; old redirects, unrelated
roles, existing role IDs, credentials and assignments are retained. Disabled
or incompatible existing workbench roles stop rather than being replaced.
Propagation is polled and verified. The script enables assignment-required
sign-in, requires HTTPS, and configures the matching issuer/audiences and
trusted-proxy runtime settings while preserving unrelated container settings.
Existing auth exclusions, token storage and other providers are preserved.
In direct demo mode the normal command enables browser login, including an
inherited `Return401`; use `--bearer-only` to deliberately retain service mode.
The optional edge path retains its previous bearer-mode behavior.

The browser credential is automatic and never printed. Setup reuses a
same-registration, unexpired named credential with matching app storage.
Missing/expired or interrupted unmatched pairs receive a uniquely named
180-day credential; old credentials are not deleted. A stored matched pair is
reused after interruption before auth wiring. Unmatched orphan credentials
are not mistaken for recoverable values; authorized owners should review and
retire unused/expired credentials separately. Metadata matching is not proof
of a successful live token exchange or real browser login.

Credential-preservation follow-up (2026-10-17, Refs #358): before creating a
replacement credential, setup reconciles the app's read-visible secret names
and Key Vault `keyVaultUrl`/`identity` pairs with `listSecrets` values. Full,
metadata-sparse and omitted KV entries retain their known references; a resolved
KV value never replaces a reference. Ordinary app values, including empty
strings, are retained without printing them. Duplicate/malformed inventories,
conflicting or incomplete KV metadata, and missing ordinary values stop before
password creation rather than rebuilding a partial array.

The rebuild atomically records `zava-forward-secret-handoff`, a SHA-256 of the
sorted secret names and KV reference metadata, never secret values. Readback
must match those references before auth switches; ordinary values are write-only
and are not expected in a configuration GET. Setup clears the tag only after
verification. A failed or uncertain readback leaves it pending: reruns cannot
reuse the new credential until the reference inventory matches. A transient
read failure can recover without another credential. For a persistent mismatch,
an authorized operator must reconcile against the original approved reference
inventory using the owning secret-management path, then rerun; do not remove
the tag to bypass the check, delete real secrets, or print/export values.
This tag is a recovery guard, not an Azure-enforced concurrency lock or proof
of a successful secret/token exchange.

The 2026-10-17 #358 evidence below is **offline only**; the later
[real temporary synthetic roundtrip](#real-temporary-synthetic-preservation-2026-10-19)
is separately qualified, not retroactive acceptance. 313 infra tests pass (including 101 setup
tests and seven killed expiry/preservation/recovery mutations). The legacy
delegating CLI remains unchanged. **Actual non-production preservation is
UNMET / Not run**: no existing resources were exercised, no Azure/Graph writes
or secret/private-data reads were permitted, and schema discovery is not live
proof. Even `--check` may create a temporary Azure job, so it was not run live.
The [acceptance audit](../docs/architecture/cutover-evidence-pack.md#credential-preservation-offline-follow-up-2026-10-17)
records the exact remaining criterion and #360 sequencing.

#### Offline acceptance reassessment (2026-10-30, Refs #358)

The current source already includes stored-credential expiry regressions for
generated and legacy names, including expired, equal-to-now, missing and future
expiry. Existing behavioral mutations detect bypasses of both expiry guards.
Mixed-secret regressions assert exact Key Vault URL/identity, ordinary values,
environment secret references and token-store bindings. Fresh offline execution
passed all 124 setup tests (including the seven-mutation test) and all 17 legacy
initializer tests; the setup suite also verifies that the legacy CLI delegates
to `setup-entra.py`. No new source or test change was needed.

This reassessment performed no Azure operation, credential access, deployment
or live sign-in. The earlier real temporary synthetic roundtrip remains the
bounded evidence described below, not proof of the originally populated
deployed-app/token-store/full-setup case. That remaining acceptance criterion
is still **UNMET** and needs a separately authorized operator exercise; local
tests do not satisfy it.

Discovery prefers the API's Key Vault secret references and their attached
identity, then its configured vault URI/attached identities, deployment-tagged
resources in `ama`, and available Bicep outputs. A unique resource is selected
automatically. Multiple/absent candidates are reported by resource name, not
identifier; interactive selection asks once. `--vault` and `--vault-identity`
remain optional overrides only. The API's environment, registry and SQL
settings come from its deployed configuration; no names need to be typed.

For the owner-selected Key Vault path, use `--run-in-azure --secret-store keyvault`.
This mode checks vault metadata through ARM and deploys exactly one new secret
with a secureString parameter, its existing 180-day expiry and no secret output.
The CLI waits for what-if completion; only the selected secret Create (plus
unchanged-scope Ignore rows) is accepted before deployment. Setup verifies
deployment success and write-only secret metadata before wiring the reference.
No vault data-plane connection from the laptop is needed. This is the supported
[ARM template control plane](https://learn.microsoft.com/en-us/azure/key-vault/general/overview-vnet-service-endpoints#usage-scenarios),
not a firewall/trusted-service bypass or an activation of new vault permissions.

Azure mode rejects explicit/recorded app storage, currently referenced
app-backed credentials and the actual eligible app-backed reuse candidate,
even when untagged and unreferenced. A read-only preflight uses the same
expiry/selection rules before directory reconciliation. Unselected unrelated
app secrets remain preserved; no migration, rotation or fallback occurs on
incompatible reuse or vault failure. Existing non-Azure private-host behavior
retains its historical
direct-demo fallback; that is **not authorized for this owner-selected path**.
An explicit `--secret-store keyvault` disables that legacy fallback too.
No path opens vault networking, enables SQL public access, changes policy,
deletes `ama`, or prints a credential or directory identifier. Temporary
secret/request files have mode 0600 outside Git and are removed. Existing app
secrets are retained. The app tags `zava-forward-credential-store` and
`zava-forward-credential-name` record the selected store and reference name.

Full Bicep application deployment is **blocked** for an app-local credential,
rather than trying to export/reimport its value. `entraCredentialStore`
defaults to `keyvault`; its `app` value requires the direct demo and
`deployApplications=false`. `deploy.py` discovers app-local tags and refuses
the unsafe default full deployment; the Key Vault CI pipeline also refuses.
Use the guarded wrapper for dependency-only updates with
`--parameter entraCredentialStore=app --parameter deployApplications=false`.
Migration of existing app-backed credentials to Key Vault needs separately
approved reconciliation and explicit operator review. Do not bypass the
wrapper with raw deployment commands or silently overwrite the store.

Coordination: setup refuses a running group deployment, app/environment
provisioning or revision activation, or another `zava-forward-auth-lock` tag.
It holds a private local lock and app advisory tag through Entra, SQL and
restart, removes only its own tag, and uses conditional If-Match when an ETag
is supplied. The deployment wrappers refuse the same tag. After interruption,
only an authorized operator who verified that the prior process and remote
updates stopped may remove a stale local lock/advisory tag. An advisory tag
is not an Azure-enforced distributed mutex: cross-host simultaneous-start
exclusion and raw-portal deployments still need a serialized operator window.
That stronger concurrency guarantee is not established by offline tests.

An existing edge-path `Return401` configuration stays service-test mode. `--bearer-only`
explicitly selects secretless Return401 service wiring, including when the
previous action was browser redirect, but is not browser acceptance.
For direct mode, browser conversion is now part of the normal command.
The final summary separately reports SQL binding and restart, not just Entra.

Exit codes: `0` means the requested configuration converged, not successful
human sign-in; `2` means drift in read-only mode or incomplete prerequisites;
`1` means blocked/error; `130` means interrupted. `--dry-run`, `--check` and
`--list-staff` make no cloud, Entra or SQL mutations and never restart replicas.
They refuse the Azure SQL job transport before payload creation, including on
automatic fallback, because even a read-only SQL job needs cloud job/secret writes.
Use the same read-only command without `--run-in-azure` on an authorized
private-connected host; unavailable SQL verification stays blocked/incomplete.
Neither check nor dry-run
logs in or creates a missing private profile; both require existing authorized
sessions and cannot be combined with `--login`.
A final fresh Container App read must report provisioning `Succeeded`.
Failed, in-progress, canceled or missing provisioning state blocks mutation
(exit `1`); read-only modes report it as incomplete (exit `2`), even when
runtime values already match.
Successful earlier writes are retained on failure, so rerun discovery after
an unknown write outcome. Mutating POSTs are not blindly retried.
The old `initialize-api-auth.py` CLI forwards to this command with the same
options; its imported callback-only Python function is retained for compatibility.

Historical local regression evidence (before this continuation): 177 infra tests passed with the source
distributions installed in an isolated pip venv, including compiled Bicep
controls. Each RV-001/RV-002/RV-003 safeguard was independently removed in
memory and its behavioral regression failed. This proves mocked command
ordering, preservation and failure handling, not live directory permissions,
vault connectivity/write authority, secret validity, consent, Private Link
readiness, SQL bindings/restart or an authorized person's browser sign-in.

For a Front Door hostname, first configure `forwardProxy.convention=Custom`,
`customHostHeaderName=X-Forwarded-Host` and
`customProtoHeaderName=X-Forwarded-Proto`, then pass the explicit HTTPS origin
to both apply and check:

```bash
python3 infra/scripts/initialize-api-auth.py -g ama -n ca-cutover-test-api \
  --public-url https://<edge-host>
python3 infra/scripts/initialize-api-auth.py -g ama -n ca-cutover-test-api \
  --public-url https://<edge-host> --check
```

This adds only the edge callback, preserving the original callbacks. It rejects
non-HTTPS URLs, credentials, ports, extra paths/queries/fragments and a differing
edge host without that exact Custom proxy configuration. Standard also trusts
client RFC Forwarded input and is rejected for this edge callback. It still requires a real
registration and an authorized tenant profile; it cannot repair the #349
missing-registration prerequisite.

### Existing-resource preservation preflight (2026-10-19)

This is the historical14:19-14:24Z no-write window; the later
[separately authorized synthetic execution](#real-temporary-synthetic-preservation-2026-10-19)
does not rewrite its original Partial / Residual Review.

Refs #358. The later read-only investigation corrects the assumption that this narrow
criterion necessarily waits for image publication or Graph. The unchanged
`preserve_app_secrets` helper and a same-configuration `Azure.rest` PATCH use
only ARM. In contrast, the mutating `secret_reference` rebuild creates a Graph
password before its PATCH; full setup also reconciles directory/runtime/SQL
and restart state. Neither full path was invoked or bypassed for this check.

Actual production `Azure.rest` GET at its `2025-07-01` API version found
explicit `configuration.secrets: null` on `ca-cutover-test-demo-api`,
`ca-cutover-test-api` and `ca-cutover-test-agents`. All three have zero KV
reference pairs and environment/init-container, scale-auth or registry-password
secret bindings. Both APIs also have no auth client-secret setting and disabled
token stores/no SAS binding; the agents auth GET failed with sanitized
request-error classification and is not reported as an empty successful read.
App-scoped permission metadata includes read/write/listSecrets, but no write
or listSecrets was attempted: provider/policy acceptance is unproven.

The demo has test/non-production/constructed-data labels, not proof of a
verified development profile. Its actual read-only `require_demo` guard refused
unknown/malformed deployment template/parameters. This is a separate roster
eligibility uncertainty, not an invented universal ARM-PATCH prerequisite.

**Literal preservation remains Blocked / Not run:** there is no populated
existing KV/reference/secret-binding baseline. An empty PATCH cannot prove
that actual `keyVaultUrl`/`identity`, unrelated secrets and `secretRef` bindings
survive. No sentinel secrets, bindings, clone or credential were created to
manufacture that baseline. No source defect was demonstrated; #374 remains
unchanged and its offline coverage was not repeated.

The [dated evidence delta](../docs/architecture/cutover-evidence-pack.md#existing-resource-preservation-preflight-2026-10-19)
records stable final metadata and zero writes. A later populated-target plan
must re-establish exact payload, concurrency, private value handling and
rollback before any operation. Official [secret management guidance](https://learn.microsoft.com/en-us/azure/container-apps/manage-secrets),
checked2026-10-19, says secret edits do not create revisions, but versionless
KV updates can automatically restart active revisions with env secretRefs.
No-value-change is not a guarantee against all provider update work; do not
change a template, restart or alter traffic merely to complete this check.
The [2025-07-01 PATCH schema](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/app/resource-manager/Microsoft.App/ContainerApps/stable/2025-07-01/ContainerApps.json)
also permits an asynchronous202 response.

### Real temporary synthetic preservation (2026-10-19)

Refs #358. A later explicitly authorized isolated synthetic baseline passed
the actual production reconciliation/configuration-PATCH boundary in the
existing internal/private environment. No existing app/identity/template,
ingress/traffic, private-service policy or real secret was changed.

A new temporary MI received Secrets Officer at only the exact new synthetic
vault-secret scope (including cleanup rights) and AcrPull at the existing
private registry. A new synthetic-only manual job first proved private
metadata access and active/deleted-name absence. No existing job was started,
overridden or used for arbitrary secret-reading payloads. A secureString
incremental deployment then created one expiring tagged synthetic KV secret;
the exact one-Create what-if and actual versioned URI were verified.

The new app contained that real reference, one unrelated random local value
and an unused env secretRef to that value. Its private digest-pinned image
used only a harmless Python sleep override, no API/data work. Fresh actual
GET/listSecrets -> unchanged `preserve_app_secrets` -> unchanged `Azure.rest`
configuration-only PATCH -> InProgress/Succeeded readback preserved exact
reference metadata, both known synthetic values, configuration, template/
binding, identity, tags and latest/ready revision. No Graph password or
`secret_reference` call was made. No helper defect/source fix was demonstrated.

No ingress/rules, min0/max1 and0.25vCPU/0.5GiB bounded allocation, but one
replica was observed during provisioning/readback: zero steady-state target
is not zero execution or a settled zero bill. No new premium service,
environment, vault or network was created. All owned resources and the active/
soft-deleted synthetic secret were removed by15:09:10Z; all ten role IDs across
operator-correction incarnations were separately checked absent. All11 old
workload snapshots, RG membership and existing backing hashes match.

The [actual evidence and cleanup table](../docs/architecture/cutover-evidence-pack.md#real-temporary-synthetic-preservation-roundtrip-2026-10-19)
retains corrections and timestamps. Private IDs/journal/comparison hashes stay
external0600; sanitized primary evidence is included in the frozen candidate
for review access. This proves a real temporary synthetic baseline roundtrip,
not the originally populated deployed-app/token-store/full-setup case.
Original Partial / Residual Review and roster-profile refusal remain unchanged.
Issue closure/acceptance belongs to the coordinator; exact-head full local
gate/receipt and independent assessment are required before any publication.

### Tenant staff and application-role initialization

Entra-authoritative access (owner decision 2026-10-24, Refs #360; see the
[ADR 0002 decision](../docs/adrs/0002-pilot-readiness-architecture.md#entra-authoritative-staff-access-owner-decision-2026-10-24-refs-360)).
A verified tenant, one valid object id and an assigned app role are sufficient
for staff sign-in. No SQL staff row, SQL read or replica reload is a login
prerequisite, and email fallback stays disabled. The roster/binding route below
is historical and optional business-metadata reconciliation only; do not run it
to fix a login. This is selected design for the changed build, not evidence of
the serving revision or of a real-user session.

Provisioning uses the isolated Graph profile. Setup merges `appRoles`
idempotently and its manifest now includes `ZavaForward.ApplicationAdmin`:

```bash
python3 infra/scripts/setup-entra.py --dry-run
python3 infra/scripts/grant-application-admin.py --tenant TENANT_ID \
  --app-id CLIENT_ID --upn VERIFIED_ADMIN_UPN --expected-oid VERIFIED_OID   # dry run
python3 infra/scripts/grant-application-admin.py ... --apply  # one assignment
```

The grant script verifies the tenant, the unique enterprise app, the enabled role
and an enabled member, adds only that assignment and is a no-op on repeat.
`ApplicationAdmin` alone is the non-staff role "Application Administrator": it
lists every option but reads no business data and the server refuses every
state-changing request; combine it with a staff role such
as `ProgrammeManager` to act. It grants no RuleOwner, AIRestart, professional
sign-off, consent or private-thread authority.

Historical route (superseded for sign-in): an enterprise-app role assignment
alone was not enough because an internal staff record bound to the person's
Entra object id was also required. A valid role with no matching staff `oid`
produced `Account not authorised`. SQL staff is cached at startup.

The default setup command now orchestrates `scripts/initialize-workbench-staff.py`
after Entra reconciliation and a fresh Entra check. Its private JSON roster
is an array of `code`/`userId`/`role` objects:
include every existing staff code, with a distinct enabled tenant member for
each. A fixture with ten internal positions and one existing Contractor needs
eleven people; automatic generation covers only positions actually in SQL.
If SQL lacks a Contractor, adding one remains a separate explicit action.
Automatic generation never reuses a person for several staff codes, because the
initializer requires a distinct user per code; with too few eligible users it
stops and reports the shortfall. Members without a mailbox (for example
unlicensed) are skipped, while a permission or login failure stops the run.
New Contractor
entries also require `"role": "Contractor"` and `"contractor"` naming an
existing case supplier. Room, desk and workspace accounts are rejected.

Keep the roster outside the repository with file mode 0600 and parent-directory
mode 0700, for example `~/.azure/zava-forward-staff/roster.json`. The initializer
resolves current names/UPNs from Graph; do not put directory names, UPNs or ids
in committed examples.

Owner decision 2026-10-16, Refs #360: **demo/synthetic-exercise assignment only,
not evidence of professional competence or delegated authority**. A default
run with a missing roster or the exact original placeholder template now:

1. Verifies a development-profile demo/test/dev deployment. The authoritative
   `zava-forward-deployment-profile` tag is propagated to app/environment by
   Bicep. Existing deployments may supply `deploymentProfile` parameters only
   when `outputResources` includes the selected app/environment's exact resource
   ID; nested modules may supply the same profile/environment in their `tags`
   parameter. Setup reads each bound deployment's actual template with
   `az deployment group export` (metadata only, scoped to `ama` and the selected
   subscription). Explicit parameter values take precedence; omitted parameters
   use that template's literal defaults. Thus an omitted `deploymentProfile`
   on the full main template still means production, but a profile-neutral
   app patch/staging template contributes no profile, not invented production.
   Both profile forms and both environment forms are checked independently,
   including defaults: development module tags cannot hide a production
   default. Neutral history alone never proves development.
   Production, unknown, conflicting or unsuccessful bound evidence refuses
   generation, even with direct ingress, purpose tags or a test name. Missing
   development/safe-environment evidence also refuses. Null/malformed relevant
   values, unresolved default expressions, missing required parameters,
   unavailable/denied template export and mismatched environment readback stop
   before roster generation. Setup needs permission to export the existing
   deployment templates; it does not create deployments or follow template-link
   URLs for this check. Merely renaming resources is not an override.
   App/environment IDs are structurally checked as exact subscription/`ama`/
   Microsoft.App resource IDs and compared case-insensitively, including the
   `/providers/` segment; wrong group, provider, type or scope still refuses.
   Exported templates must identify a supported resource-group ARM schema
   (2019-04-01 or 2015-01-01), content version and resource envelope. Omitted or
   `1.0` language uses an array; supported `2.0` uses symbolic-name resource
   objects. Every resource needs a name, type and dated API version.
   Unknown schemas/language versions, malformed resource entries, API-profile/
   import extensions and nested deployment contracts explicitly refuse.
   Nested templates/links and their parameter/default evaluation are not
   interpreted or silently treated as neutral. This bounded check is not a
   complete ARM/provider-schema validator, and schema validity never establishes
   a development profile. A valid nested deployment still needs a separately
   supported evidence path rather than a safety bypass.
2. Reads existing SQL staff codes, approved roles, existing Contractor supplier
   scopes and a binding-present flag through the same `--list-staff` path.
   It never invents an extra code or Contractor. Existing immutable SQL
   bindings stop regeneration: restore the original private roster instead.
3. Enumerates Graph users, excluding guests, disabled accounts, resource/shared/
   service account naming and non-user objects. It additionally requires
   `GET /users/{id}/mailboxSettings/userPurpose` to report `user`, rejecting
   shared, room, equipment and unknown classifications even when names look
   personal. Missing classification/read authority stops before persistence or
   Entra writes, not a naming-only fallback. This requires provisioning access
   to `MailboxSettings.Read` for candidate mailboxes, separately approved by an
   authorized tenant administrator; setup grants no permissions. Unlicensed or
   inaccessible mailboxes are not silently treated as people. See the official
   [GET contract](https://learn.microsoft.com/en-us/graph/api/user-get-mailboxsettings?view=graph-rest-1.0)
   and [purpose values](https://learn.microsoft.com/en-us/graph/api/resources/mailboxsettings?view=graph-rest-1.0),
   retrieved 2026-10-16. Directory/Exchange classification remains the evidence
   boundary, not an attestation of someone's competence or actual identity.
4. Reserves the first code in stable code order with role `ProgrammeManager`
   (Retrofit Programme Manager, the administrative workbench role) for the
   single eligible user whose UPN starts `admin@`, case-insensitively. Zero or
   several matches reports the count and asks one plain UPN question; explicit
   `--admin-upn` resolves it without printing the value. Noninteractive runs
   stop with that flag's instruction. Invalid input or no ProgrammeManager
   position stops, never chooses an invented role or code. No Entra directory
   administrator role is granted.
5. Sorts remaining eligible people before a seeded random shuffle and assigns a
   distinct person to each remaining code, preserving each SQL role and supplier.
   It prints the seed (`--seed N` reproduces the mapping for unchanged inputs),
   counts and administrator role, never personal names, UPNs, object IDs
   or supplier names. Too few people reports the exact deficit and stops without
   writing. This implementation chooses the permitted **stop** alternative:
   there is no reuse override because the initializer requires distinct people.
6. Shows one-screen counts per role and asks once to write the private roster.
   `--yes` accepts; `--check` and `--dry-run` preview without roster/SQL writes or
   confirmation and exit incomplete (2), since no roster/bindings were installed.
   Admin ambiguity in read-only modes requires `--admin-upn`, not a prompt.
   The generated file is atomically saved with mode 0600 in a mode-0700 directory.

Generated JSON is an envelope with `"version": 1`, a nonnegative integer `seed`
and the nonempty `staff` array of code/userId/role objects (plus existing
Contractor scope). Both setup and SQL initializer accept it; legacy array
rosters remain supported. Reruns reuse the persisted mapping even when a new
`--seed` is supplied; they do not reshuffle. Generated-roster reruns revalidate
the demo profile and individual-mailbox eligibility. An existing populated or
partly edited invalid roster is never replaced automatically.

Profile-classification follow-up, 2026-10-17 (Refs #360): the coordinator-reported
API-without-profile, development/test bound environment, neutral app-stage and
module/main deployment-history shape is covered by a failing-before/passing-after
offline regression. The ARM [deployment metadata](https://learn.microsoft.com/en-us/rest/api/resources/deployments/get?view=rest-resources-2025-04-01),
[template export](https://learn.microsoft.com/en-us/rest/api/resources/deployments/export-template?view=rest-resources-2025-04-01)
and [parameter default contract](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/parameters)
were checked on 2026-10-17. This fixes source classification, not live setup:
credential access, initializer publication's 403 and genuine tenant/browser/
SQL/AI acceptance remain unmet; no Azure changes or temporary jobs were run.
Coordinator correction ONE (2026-10-17) retains the original adverse external
assessment: mixed-case ID and malformed-envelope reproductions failed before
correction, and the expanded offline suites pass afterward. The supported
envelope boundary follows the official [template structure](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/syntax)
and [resource-group template schema](https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json),
retrieved 2026-10-17. This is correction evidence, not independent final-head
acceptance or full setup readiness.

Setup still rejects placeholders, non-GUID/zero IDs, duplicates, unknown roles,
group-only entries, symlinks and unsafe modes before directory changes. SQL
additionally validates complete coverage, roles, suppliers and immutable
bindings before its transaction; a connectivity blocker is not validation.

`python3 infra/scripts/setup-entra.py --list-staff` reads only candidate codes
and approved roles from private SQL; no roster or browser configuration is
needed. `--lookup-upn <person-upn> --staff-code <existing-code>
--staff-role <approved-role>` saves one enabled member's mapping to a separate
mode-0600 file beside the roster when Graph directory-read permission allows.
It prints only the private file path, never the object ID. Review and merge
the mapping into the roster privately; the helper does not allocate roles.

The normal command displays only SQL change counts, asks once to apply and
restart, then verifies fresh ready replicas for every traffic-serving revision.
This is a separate confirmation after the roster-write confirmation;
`--yes` accepts both displayed plans. A current roster/revision with recorded restart
evidence needs no further restart. `--check` and `--dry-run` inspect Entra and
SQL without applying or restarting. Unknown/missing restart evidence remains
incomplete. In a mutating setup invocation, a blocked local candidate lookup or
SQL preflight automatically tries the
[in-VNet job path](#in-vnet-sql-staff-step-refs-360). Read-only modes never do:
the transport guard reports the missing evidence and private-host handoff.
Explicit roster/control validation failures do not trigger fallback, and an
uncertain local apply is never retried in another execution. If the Azure path
cannot run, setup prints the exact discovered private-host command and reports
SQL/restart **not confirmed**. Candidate failure instead prints the exact
`setup-entra.py` command, retaining mode/seed but not the administrator UPN.
No missing roster is invented or written on that failure path.

### In-VNet SQL staff step (Refs #360)

After the separately authorized prerequisites below, the single operator command is:

```bash
python3 infra/scripts/setup-entra.py --run-in-azure --secret-store keyvault --yes
```

The command still performs directory registration, app roles and assignments
with the operator's authorized isolated Graph login. Missing-roster generation
remains the same as PR #363: the first ProgrammeManager code gets the eligible
`admin@` person, remaining positions are seeded random, and the private persisted
mapping is reused. No Graph profile/token is uploaded. Only candidate listing,
SQL check, SQL apply/verification and API restart execute in the job.
The internal SQL-check/candidate operations in a mutating invocation use
temporary management-plane jobs/secrets even before SQL apply. User-facing
`--check`, `--list-staff` and `--dry-run` prohibit that transport, including
`--run-in-azure` and automatic fallback. They report missing private SQL evidence
rather than claiming success; use a private-connected authorized host for these
read-only commands. Mutation-mode generated-roster discovery still prints only
counts, not codes or roles, for Azure results.

Prerequisites (not executed or deployed by setup):

* An existing `job-<API-prefix>-init` in the API's actual VNet-injected
  environment in `ama`, using exactly `id-<prefix>-init`, the existing SQL Entra
  Application administrator, and an identity-authenticated registry reference.
  A `-demo` API automatically tries its exact parent initializer if its own
  initializer is absent; `--azure-init-job` remains an explicit override.
  Different environments must both have verified subnets in the same ama VNet.
  The temporary worker runs in the selected API environment, not the parent's.
  No general cross-environment or cross-subscription search occurs.
* An immutable `zava-forward-cutover-proof@sha256:<digest>` initializer image
  built from the source API image. The source API already installs core,
  agents, API, cryptography and mssql-python/ODBC; the former proof image
  contained only its proof runner. The Dockerfile now also copies the staff
  initializer, SQL-only worker, private transport/roster helpers and manifest
  into `/app/scripts/` and `/app/entra/`. Its original proof ENTRYPOINT stays
  unchanged; the transient job overrides it with
  `python /app/scripts/staff-azure-worker.py`. No Azure CLI is needed in the image.
* Operator management permissions to read the API/environment, SQL
  server/database/admin and identity, create/start/read/stop/delete temporary
  jobs, and read the private storage account/container configuration.
  Result reads use operator-profile Entra list/read data-plane permissions
  on the `staff-results` container and a private-connected host that resolves
  and reaches its private endpoint. ARM job control alone is insufficient.
  There is no console streaming, Log Analytics, public Blob, SAS, shared-key
  or tag fallback. Private environment log-endpoint reachability is not
  required. The operator
  also needs existing vault metadata/secret-deployment and group deployment/
  what-if permissions; no role is created by setup. Local cryptography comes from
  `python3 -m pip install -r src/api/requirements.txt`.
* The existing initializer identity needs its existing SQL-admin and AcrPull
  permissions plus the narrowly scoped API restart and private-container write
  roles below. These definitions are **not activated by setup or this delivery**.
  The current template's `includeResultBlob` defaults to `false`; it does not
  accept the removed `includeResultRelay` parameter from historical receipts.
  The Blob role grants only `blobs/write` and `blobs/add/action` on
  `staff-results`, not read, list, delete, jobs/write, listSecrets or
  resource-group access. Its activation needs separate explicit approval.
  No new identity,
  Graph permission or general Contributor role is introduced. SQL remains
  Entra-only with public access Disabled; Blob public network, anonymous
  access and shared keys remain disabled. Private DNS/subnet and the actual
  SQL administrator principal are verified before a roster is transferred.
  Provision the private `staff-results` container and lifecycle policy through
  the reviewed storage module before an authorized Blob writer grant. Set
  `ZF_BLOB_ACCOUNT_URL` on the API and use a rebuilt digest-pinned proof image.

Required later, authorized image build (shown only; not run for this change):

```bash
(cd infra && az acr build -g ama -r <registry> -f cutover-proof.Dockerfile \
  --build-arg API_IMAGE=<registry-server>/zava-forward-api@sha256:<api-digest> \
  -t zava-forward-cutover-proof:<unique-tag> .)
az containerapp job update -g ama -n <existing-init-job> \
  --image <registry-server>/zava-forward-cutover-proof@sha256:<proof-digest> -o none
az deployment group what-if -g ama --template-file infra/staff-initializer-rbac.bicep \
  --parameters apiName=<api-name> initializerIdentityName=<existing-init-identity-name> \
  includeResultBlob=false
# Requires explicit role-creation/assignment authorization, not merely RG Owner:
az deployment group create -g ama --template-file infra/staff-initializer-rbac.bicep \
  --parameters apiName=<api-name> initializerIdentityName=<existing-init-identity-name> \
  includeResultBlob=false -o none
```

Build context is only `infra/`; API image context remains `src/`. The displayed
ACR build command is conditional on an already approved private build path.
At the PR #375 evidence point on 2026-10-17 the existing registry had public
access Disabled, bypass None, no private task pool/task and a denied local
Docker socket. The later [normal-Docker publication follow-up](#normal-docker-private-publication-follow-up-2026-10-17-360)
supersedes the socket blocker, but finds both existing private ACR endpoints
unreachable. Publication remains **Blocked**, not permission to run public ACR
Tasks, add a paid pool, change routing or open the registry. An authorized
existing private publisher must supply the immutable proof digest.
The standalone Bicep template refuses non-ama scope and assigns app/revision/
replica reads/restart only to the selected API. A separately approved opt-in
adds container-scoped Blob write for the initializer identity. It changes
neither SQL admin nor network configuration.
Role activation is an explicit IAM-operator action after authorization and
what-if review, never inferred from the owner asking to continue the demo.

For approval limited to API read/restart, pass `includeResultBlob=false` to
both what-if and create (also the default). This omits the Blob role definition
and assignment; the four API actions and API-only assignment stay unchanged.
After separate explicit approval and container provisioning, preview and
apply the writer grant with the same exact parameters:

```bash
az deployment group what-if -g ama --template-file infra/staff-initializer-rbac.bicep \
  --parameters apiName=<api-name> initializerIdentityName=<existing-init-identity-name> \
  storageAccountName=<private-storage-account> includeResultBlob=true
az deployment group create -g ama --template-file infra/staff-initializer-rbac.bicep \
  --parameters apiName=<api-name> initializerIdentityName=<existing-init-identity-name> \
  storageAccountName=<private-storage-account> includeResultBlob=true -o none
```

These are conditional runbook examples, not current execution authority.
Approval for temporary staff-job lifecycle does not authorize the Blob grant.
Temporary-job operations belong to the operator, not this
template or the initializer MI; do not add a general jobs/Contributor role.
Incremental deployment with Blob disabled does not revoke a pre-existing
Blob assignment, its role definition or a historical tag assignment.
`includeResultBlob=false` selects API-only deployment; it is not a cleanup
command. An authorized IAM operator must separately approve and retire the
exact obsolete assignment/role after checking other consumers. Setup does not
delete result grants or the container; ciphertext follows the configured
lifecycle and soft-delete retention. The dated
[scoped activation receipt](#scoped-initializer-iam-activation-2026-10-17-360)
records historical grants, not approval of the replacement Blob transport;
any grant retirement needs separately authorized IAM review.

Each operation clones only the verified source image/registry/identity into a
unique `job-staff-<random>` manual job, with one replica, no retries and a
600-second execution deadline. The operator uploads the bounded request
(maximum 12 KiB of payload) and a fresh result-encryption key as a Container Apps
secret, via a private mode-0600 ARM body file outside Git. CLI logging and
telemetry are disabled; body files are removed even on failure. No identities
or secret values occur in CLI arguments. Private Blob data-plane access is
required for worker writes and operator reads; no Key Vault data-plane path
is used for result transport. The job never receives an operator access token.

The job reads the existing SQL positions, uses the canonical protected-profile
and atomic installation rules, rereads to verify zero remaining drift, then
uses its own MI to restart every traffic-serving API revision and verify fresh
ready replicas. Historical actor fields are preserved. A SQL no-op still
requires restart unless setup has matching roster/revision restart evidence.
After SQL success but restart failure, the result remains incomplete.

Job logs contain only generic failure messages, never candidates, people,
codes, roster, keys, credentials or SQL exceptions. Results are authenticated
AES-GCM ciphertext bound to this run, operation, input and image digest.
(Superseded 2026-10-22: the ARM tag frames described in earlier revisions are
retired.) The worker writes complete, bounded pages to the private
`staff-results` Blob container with its managed identity, and the client reads
them with Entra credentials from a private-connected host after terminal
Succeeded; see [Private Blob result transport](#private-blob-result-transport-2026-10-22-refs-360).
The key remains in the temporary request secret and operator memory. Missing,
extra, tampered, oversized, expired or mismatched pages, an unreachable Blob,
or a deadline failure cannot be mistaken for success, and there is no tag,
console or local fallback.

Setup stops uncertain/failed executions and deletes only its owned temporary
job, including the roster secret; it polls for confirmed absence. Encrypted
result Blobs are retained for the configured one-day lifecycle deletion,
with 30-day soft-delete retention, not immediately deleted by setup.
It never deletes the source initializer or changes its configuration. A cleanup failure blocks success
and prints only the owned temporary job name. Hard termination/power loss
cannot guarantee cleanup: in a serialized operator window, inspect the
`zava-forward-staff-run` tag and execution of that exact named leftover, then:

```bash
az containerapp job stop -g ama -n <owned-job-staff-name> -o none
az containerapp job delete -g ama -n <owned-job-staff-name> --yes -o none
```

After confirming that the worker has stopped and the exact job is absent,
leave encrypted result Blobs to the configured lifecycle; setup has no
Blob-delete grant and does not mutate source initializer tags. Never infer
ownership from a short prefix or delete the source initializer.
Interrupted hard-kill recovery
requires the serialized operator window; retained ciphertext is not a clear
roster and cannot be decrypted after losing the request key.
Never delete `ama` or an unowned job. SQL may already have committed; first use
`--check` without `--run-in-azure` on an authorized private-connected host with
the same persisted private roster, never regenerate
or blindly retry an uncertain apply. Cross-host simultaneous setup still needs
the serialized operator window described above.

If the image/job/permission/result path is unavailable, setup fails closed.
The following is an optional authorized recovery path, **not** the primary
laptop setup or evidence that the normal command completed. Use the exact command
printed by setup on an authorized private-connected host with the same private
roster and isolated Graph login. Its SQL manual fallback has this form:

```bash
python3 infra/scripts/initialize-workbench-staff.py --resource-group ama \
  --container-app <discovered-api-name> --roster <private-roster-path> \
  --tenant-profile <private-profile-path> --apply --restart
```

For unavailable candidates, the printed fallback is `setup-entra.py` without
`--run-in-azure`; supply any private admin input there if requested. Never
enable SQL public access, add firewall rules, change Key Vault/storage network
settings or bypass policy. Offline fake-az/worker tests exercise the path;
actual image availability, permission activation, VNet/SQL/log access, live
binding/restart and real browser sign-in remain **Not run** in this change.

### Private publication blocker evidence (2026-10-17, PR #375 continuation)

The owner authorized safe image publication in the existing private registry;
the limitation is the available execution route, not a blanket absence of image
approval. Actual `docker version` fails with permission denied at
`unix:///var/run/docker.sock`; no elevation/group change is permitted.
No alternate builder is installed. Anonymous registry `/v2/` returns HTTP403,
which is **not** an authenticated push/AcrPush permission test.

ARM reads succeed: registry public access Disabled/bypass None, task and agent
pool lists empty. Historical default quick runs succeeded on 2026-10-16, but
have no private agent pool. Microsoft's
[private build guidance](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-private-endpoints#use-az-acr-build-with-private-endpoint-and-private-registry)
states default `az acr build` fails with public access disabled; alternatives
need a dedicated pool or public task-IP firewall access.
[Agent pools](https://learn.microsoft.com/en-us/azure/container-registry/tasks-agent-pools)
allocate billable compute, so neither alternative is authorized here.
[ARM image import](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-import-images)
requires trusted-service bypass on restricted registries, incompatible with
current bypass None. Build/import were therefore **not attempted**, not claimed
to have returned a live task/import permission error.

The successful inspected source CI run `39028596880` retains UX/Trivy reports,
not an image archive; current CI neither exports nor pushes the locally built
API images and does not build the infra proof layer. Repository self-hosted
runner inventory is empty. Container-package discovery is **unknown**: the
correct user packages API returned HTTP403 requiring `read:packages`; do not
expand token rights or call that proof of absent packages. No private builder
VM/ACI exists in the permitted ama inventory. Existing proof jobs retain the
old digest; the initializer has AcrPull, not a publisher role.

The smallest publisher action is to identify an **already existing**
private-connected builder/operator with existing push authority on
`crcutovertestrzsrg`, build `infra/cutover-proof.Dockerfile` with the retained
immutable API base, push a new proof tag and supply its immutable digest.
This is not authorization to install a new framework, add infrastructure,
change this host's Docker rights, open ACR or create credentials. If no such
builder exists, a separate infrastructure/spend decision is necessary.

At the PR #375 evidence point, IAM was a separate **unattempted approval boundary**, not an observed Azure
AuthorizationFailed: source-job tags and demo-API restart assignments are absent.
Independent permissions readback reports actions `["*"]` with no exclusions;
there is no demonstrated IAM inability. Missing explicit authorization, not
an attempted permission failure, prevents activation here.
Explicitly authorize only the reviewed `staff-initializer-rbac.bicep` deployment
with `apiName=ca-cutover-test-demo-api` and
`initializerIdentityName=id-cutover-test-init`. An authorized operator then
rechecks the exact four-Create what-if before applying it. No broad role or
Graph grant is needed or authorized.

The later [scoped activation](#scoped-initializer-iam-activation-2026-10-17-360)
supersedes only that API-grant status: API permissions were authorized and
applied. The [later explicit relay approval and activation](#approved-existing-job-relay-delta-2026-10-17-360)
supersedes the remaining tag-grant approval boundary without widening scope.

### Normal-Docker Private Publication Follow-Up (2026-10-17, #360)

This section records the earlier #381 attempt, not the current CLI result.
Its private-publisher-only prerequisite is superseded by the
[renewed hosted CLI attempt](#renewed-initializer-acr-cli-attempt-2026-10-17-360)
below. The private-IP timeout observations remain historical facts; they do
not establish that hosted ACR Tasks cannot be scheduled.

Following merged #375 and #379, the owner authorized publication to the
existing private registry and an image-only pin of the existing initializer,
conditional on validation. Normal Docker now works: Server 29.9.0 and docker
group membership were verified without privilege escalation. This resolves
the historical socket denial, not private registry connectivity.

| Current check | Observed outcome |
| --- | --- |
| Registry | `crcutovertestrzsrg`, public access Disabled, bypass None, admin user false; unchanged on final readback |
| Normal login DNS/HTTPS | `crcutovertestrzsrg.azurecr.io` resolves to public `51.143.208.3`; anonymous `/v2/` returns 403 |
| Existing private DNS/NIC | Both agree: login `10.40.4.21`, UK South data `10.40.4.20` |
| Private login/data HTTPS | Each connection times out after 10 seconds using exact existing IP, normal TLS validation, no proxy and no credentials; no TLS session established |
| Host route | `172.16.0.4` via existing gateway `172.16.0.1`; no working private endpoint path demonstrated |
| Authenticated login/push authority | Not tested; no AcrPush denial claimed |
| Real proof build, image smoke, push/digest and job image pin | Not run: private-route gate failed |

No DNS/hosts/routes, public-access/bypass, permissions or resources were changed.
No ACR Tasks/import, pools, temporary VMs or unrelated source uploads were used.
The concrete remaining prerequisite is an **already existing** authorized
private-connected publisher that can reach both registry endpoints. Do not run
`az acr login`, pull the private base or push through the observed public route.

A strictly local, network-disabled `FROM scratch` / `COPY` context audit
(no `RUN`, no application entrypoint and no container start) found that
`!scripts/` and `!entra/` reintroduced entire directories, including unrelated
scripts and generated bytecode. Removing only those two directory exceptions
preserves every explicit COPY input. The corrected native context contains
exactly the Dockerfile, five Python scripts and `entra/app-registration.json`;
it excludes unrelated scripts, bytecode and private-profile/configuration files.
The existing context test now checks unwanted-file exclusions. Both local audit
containers/images were removed by exact name; no shared images were deleted.
This audit is **not** a built proof image or runtime/no-secrets certification.

The final focused suite passed 83 tests, zero skips. Five source imports with
network connections forbidden and two isolated source `--help` checks passed.
These are source/offline checks, not imports/CLI/nonroot execution inside the
unavailable retained-base image. Test scratch was explicitly isolated and
removed; missing source packages were restored only in a task-owned venv.
The Dockerfile, inherited nonroot contract and retained API base remain:

```text
crcutovertestrzsrg.azurecr.io/zava-forward-api@sha256:111b26226cad06e229bcf1c3174877510c4c68c5a5fefc885167a2b4c821657d
```

On an already approved private-connected publisher, after both endpoints and
normal identity authentication are verified, the local publication commands
have this form. They were **not run** here; use a clean committed source tree
and record the actual pushed immutable digest before considering the pin:

```bash
az acr login -n crcutovertestrzsrg --only-show-errors -o none
TAG="staff-360-$(git rev-parse --short=12 HEAD)-$(date -u +%Y%m%dT%H%M%SZ)"
IMAGE="crcutovertestrzsrg.azurecr.io/zava-forward-cutover-proof:$TAG"
docker build -f infra/cutover-proof.Dockerfile \
  --build-arg API_IMAGE=crcutovertestrzsrg.azurecr.io/zava-forward-api@sha256:111b26226cad06e229bcf1c3174877510c4c68c5a5fefc885167a2b4c821657d \
  -t "$IMAGE" infra
# Perform no-network import/help/nonroot/package checks on this actual image,
# overriding the historical entrypoint; never run its initialize command.
docker push "$IMAGE"
docker image inspect "$IMAGE" --format '{{json .RepoDigests}}'
# Only after validated smoke/digest and reviewed exact settings preservation:
az containerapp job update -g ama -n job-cutover-test-init \
  --container-name proof \
  --image crcutovertestrzsrg.azurecr.io/zava-forward-cutover-proof@sha256:<validated-proof-digest> \
  -o none
```

The existing job was **not updated or started**. Its old immutable image stays:

```text
crcutovertestrzsrg.azurecr.io/zava-forward-cutover-proof@sha256:ef0058f8f380cc610d4b7113509293b3ed624d22afac95e807b4c69a4266dc72
```

It is Manual, one `proof` container, historical args `["initialize"]`, timeout
600 seconds, retry limit 1, parallelism/completion 1, 0.5 CPU/1Gi, existing
`id-cutover-test-init` and MI registry authentication, six existing environment
entries and no declared secrets/volumes. Two in-memory read-visible settings
fingerprints match across the no-write verification window. No environment
values, tag contents, tokens or secret payloads were retained. This proves
unchanged observed configuration, not secret-payload equality or image-pin
idempotency. Preserve the full container/environment/identity/registry shape
on any later image-only update and verify a separate readback; never replace
the container array with an image-only object or start the historical command.

`ca-cutover-test-demo-api` still has `setup-pending-deny-all` for `0.0.0.0/0`;
authentication remains unverified. No SQL/private data, Graph, initialization,
restart, new roles/networking/spend or retirement occurred. #360 d/e remain
**UNMET**; the image blocker does not revoke the already activated #379 grants
or authorize weakening privacy. Full RPI evidence records this blocked outcome,
not successful image delivery.

### Renewed Initializer ACR CLI Attempt (2026-10-17, #360)

Refs #360, retained source `bab4bf3a2ac9ec030d78d27063d1390f800c5c7c`
(merged #381). **An actual hosted build was attempted. Publication remains
blocked at hosted-agent registry login, not source upload.** No new image or
initializer pin was produced.

Read-only `az acr task show-run --run-id dbb` confirms the earlier
2026-10-16T13:53 successful ordinary cpu2 build published
`zava-forward-cutover-proof:proof-20261016` at digest
`sha256:ef0058f8f380cc610d4b7113509293b3ed624d22afac95e807b4c69a4266dc72`.
The five preceding/latest historical runs succeeded and no pools exist.
That retrospective success is distinct from the current failed run below;
neither absent pools nor VM private-endpoint failure alone proves Tasks
unavailable.

| Current command or gate | Actual result on 2026-10-17 |
| --- | --- |
| Local retained-base Docker build, 180-second bound | Exit 1 at retained API manifest HEAD: `403 Forbidden`, client IP not allowed; no image, so actual image smoke unavailable |
| Native CLI archive preflight | Seven unique allowed regular paths, all bytes equal committed source; manifest SHA256 `0ed4d8a56a0c69d85fc7bd8e4d6c52c4fc0d0891cbef8bdcf2821ae78dfe27f4`. CLI appends an identical second Dockerfile entry, not an eighth unique file |
| Corrected `az acr build`, service timeout 600 seconds/client bound 720 | Uploaded 20.157 KiB, queued QuickRun `dbc`, ordinary cpu2 |
| Hosted logs | Source download and Docker configuration succeeded; registry login failed with `login attempt to https://crcutovertestrzsrg.azurecr.io/v2/ failed with status: 403 Forbidden` |
| Run metadata | Failed, 17:57:22.946003 to 17:57:29.852767 UTC; `outputImages: null`; build/base pull/push not reached |
| Actual localhost current-source smoke | One fictional case, no staff, AI off, no SQL; `/` and `/healthz` 200, anonymous `/api/me` and `/api/stats` 401. This is installed-source proof, NOT retained-base/hosted-image or genuine sign-in proof |
| Existing job readback | Full read-visible before/after projection equal; old proof digest, Manual initialize args, identity, environment, resources, settings and registry preserved; no update/start |
| Registry readback | Public access Disabled and bypass None before/after; no networking or IAM change |

The corrected current command, run from the repository root, was:

```bash
timeout 720 az acr build -g ama -r crcutovertestrzsrg \
  -f infra/cutover-proof.Dockerfile \
  --build-arg API_IMAGE=crcutovertestrzsrg.azurecr.io/zava-forward-api@sha256:111b26226cad06e229bcf1c3174877510c4c68c5a5fefc885167a2b4c821657d \
  -t zava-forward-cutover-proof:staff-360-bab4bf3a2ac9-20261017T175718Z \
  --timeout 600 --no-logs infra -o json
az acr task show-run -r crcutovertestrzsrg --run-id dbc
az acr task logs -r crcutovertestrzsrg --run-id dbc
```

The first `-f cutover-proof.Dockerfile infra` invocation failed locally with
`Unable to find 'cutover-proof.Dockerfile'`, before upload. CLI 2.91.0 requires
the root-relative file path in this invocation despite its context-relative
help wording. It was corrected and retried, not counted as a service denial.
Do not retry the recorded unique tag as though it were a successful image.

The failure establishes current hosted-agent registry login403, not its exact
network-policy versus identity cause. It does not establish an RBAC denial,
require a paid pool, or authorize opening the registry. Source upload succeeded;
no secret-bearing build arguments, debug output or SAS URLs were retained.
Only the authorized source upload/failed QuickRun occurred. No workload,
backing-resource, IAM, network, job run, API restart, tenant, SQL, Graph or
retirement operation was performed; existing #379 grants remain unchanged.

Before any future pin, join the submitted seven-file hash manifest, source
commit, retained base, run ID and exact output digest. Pull that digest and
verify local RepoDigest, all six copied payload hashes, UID/import/help and
localhost smoke on that same image. A separate local build or source-only
smoke cannot satisfy this gate. Preserve the entire existing job and prove
non-image settings unchanged; never start its historical initialize command.
Current image gates remain blocked. Genuine operator/browser/roles/SQL/AI
acceptance and #360 d/e remain **UNMET**; old API/edge and group `ama` stay.

### Initializer Registry403 Read-Only Diagnosis (2026-10-17, #360)

Coordinator authorized diagnosis only after the failed `dbc` attempt, not a new
build or configuration change. **Likely cause: `dbb` succeeded before registry
isolation; `dbc` later used default hosted compute without a demonstrated
private/exempt path.** The original
[deployment evidence](../docs/architecture/cutover-evidence-pack.md#private-network-continuation-2026-10-16)
and contemporaneous deployment record explicitly place image capture before
registry isolation. Exact-registry ARM activity metadata shows a successful
registry write at October16 13:56:53 UTC, after `dbb` finished13:53:24, followed
by writes14:07:30,14:14:17 and22:34:36. These timestamps corroborate updates,
not which property changed or the exact network state at `dbb`.

Current read-only findings, retrieved2026-10-17:

| Evidence | Interpretation and limit |
| --- | --- |
| Both runs | QuickRun, Linux/amd64, ordinary cpu2, no named task or selected pool; same basic platform, not proof of equal network state/token |
| Registry | Premium UK South, publicDisabled, bypassNone, approved private endpoint, LegacyRegistryPermissions rather than ABAC |
| Task-specific bypass | Preview2025-06-01 GET omits `networkRuleBypassAllowedForTasks`; absent is not literal false |
| Caller effective permissions | Registry scope actions `["*"]`, no exclusions, empty dataActions; management scheduling/read succeeds, but not an attestation of agent token/pull authorization |
| Existing alternatives | Named tasks and agent pools empty; no VM/pool in inspected ama inventory. No inherited pool/managed-identity task demonstrated; external runners outside that scope are unknown |
| Activity scope | 194 returned exact-registry events, max200, requested October16 11:55 to October17 18:20; only timestamp/operation/status/substatus selected, no actor/claims/request/change payloads |

Microsoft's [private registry quick-build guidance](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-private-endpoints#use-az-acr-build-with-private-endpoint-and-private-registry)
documents default `az acr build` failure with public network disabled and offers
dedicated pools or regional public task-IP access. Its
[Tasks-specific bypass policy](https://learn.microsoft.com/en-us/azure/container-registry/manage-network-bypass-policy-for-tasks)
documents default denial for unset SAMI task bypass from June1,2025, with an
explicit UAMI exception. That is not proof this QuickRun used SAMI or that an
arbitrary UAMI/auth flag gains network access. The
[generic trusted-service setting](https://learn.microsoft.com/en-us/azure/container-registry/allow-access-trusted-services)
is distinct; enabling it alone is not a proven QuickRun fix.

The [pool guide](https://learn.microsoft.com/en-us/azure/container-registry/tasks-agent-pools)
documents VNet access and allocation-based billing; UK South is not in its
published preview region list retrieved October17. No existing pool can simply
be selected here and a new same-region pool is not presumed available.
[Network troubleshooting](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-troubleshoot-access)
also warns authentication and network symptoms can overlap. Without service-side
subreason, the exact agent token/403 cause remains uncertain; no IAM denial or
need for broader grants is established.

| Later option, not an authorized command | Security/cost decision |
| --- | --- |
| Existing authorized private-connected Docker publisher | Preferred no-bypass option if the owner can identify one; no new service allocation, but rights/path/capacity remain unproven |
| New VNet-integrated pool | Private path, but allocated compute billing, region/support/quota/network review and an explicit price ceiling/spend approval required; none provisioned |
| Explicit Tasks/trusted-service bypass appraisal | Potentially avoids new pool allocation, but relaxes network isolation; exact identity/applicability must be proven, not a guaranteed one-flag remedy |
| Public task-IP allowlist | Changes public boundary and conflicts with current requirements; not recommended or authorized |

Smallest later owner choice: identify an existing approved private publisher,
or retain the blocker while separately appraising a costed private-pool design
or explicit task-bypass exception. No blanket access/IAM approval is requested.
No bypass/public change, paid pool, support ticket, new build, workload/initializer
update/start, API restart, SQL/Graph/secret-payload access or teardown occurred
during this read-only continuation. No new live validation, image smoke/pin or
regulatory approval is implied; #360 d/e remain **UNMET**.

### Scoped initializer IAM activation (2026-10-17, #360)

The API-only receipt below is historical. Its unapproved/absent relay status
is superseded only by the [subsequent explicit relay delta](#approved-existing-job-relay-delta-2026-10-17-360).

The owner explicitly approved only reviewed API read/restart and temporary
staff-job lifecycle permissions in `ama` on 2026-10-17 (boolean true).
The existing-job tag relay is not temporary-job lifecycle: its
tag read/write permissions remain **unapproved and unapplied**, and the relay
itself was retired on 2026-10-22 (see the Private Blob result transport). The template does not grant temporary-job
lifecycle to the initializer MI. Those operations belong to the setup
operator; no new operator role or temporary job was created.

After a small conditional-exclusion amendment passed independent standard
source review, both commands used the same source and exact parameters:

```bash
az deployment group what-if -g ama --name staff-iam-360-api-20261017 \
  --template-file infra/staff-initializer-rbac.bicep --mode Incremental \
  --parameters apiName=ca-cutover-test-demo-api \
  initializerIdentityName=id-cutover-test-init includeResultRelay=false
az deployment group create -g ama --name staff-iam-360-api-20261017 \
  --template-file infra/staff-initializer-rbac.bicep --mode Incremental \
  --parameters apiName=ca-cutover-test-demo-api \
  initializerIdentityName=id-cutover-test-init includeResultRelay=false -o none
```

These commands record the performed API-only operation using the 2026-10-17
template, not current deployment instructions or authorization to rerun or
activate relay grants. The current template uses `includeResultBlob=false` by
default and no longer accepts `includeResultRelay`.
The fresh what-if Succeeded with
exactly two Creates (role definition and API child assignment), plus 94
same-group Ignore rows. Deployment `staff-iam-360-api-20261017` **Succeeded**;
correlation ID `2177965b-1d42-4709-962b-3475e2186264`.

| Readback | Exact value |
| --- | --- |
| Role name / GUID | Staff initializer API restart (ama) / `0d8c4586-d46e-514c-9c19-680d9f068755` |
| Sole assignable scope | `/subscriptions/e51ebc89-79d0-4a52-a82b-01a292eefd5b/resourceGroups/ama` |
| Assignment / resource scope | `3a7e0803-3997-5cbe-af9c-c9776b37f3a7` / `Microsoft.App/containerApps/ca-cutover-test-demo-api` in that group |
| Principal / type | `3830883a-f4af-44f8-bff8-8859b78fc2f8` / ServicePrincipal, existing `id-cutover-test-init` |
| Actions | `Microsoft.App/containerApps/read`, `Microsoft.App/containerApps/revisions/read`, `Microsoft.App/containerApps/revisions/replicas/read`, `Microsoft.App/containerApps/revisions/restart/action` |
| Exclusions / data permissions | `notActions`, `dataActions`, `notDataActions` all empty |
| Relay role / assignment | `64ec5d6d-f8ae-51ab-a93a-394f6cc97c6c` / `8e9a497e-3b90-50e2-a783-93e58755165b` absent |

Azure returns the role definition's canonical subscription-level URI despite
the resource-group-addressed preview. This is the same GUID, with only `ama`
in `assignableScopes`, not a subscription-wide assignment or tenant role.
The readback check was corrected for that provider URI normalization and the
expected read-only initializer identity resolution; no redeployment or scope
expansion occurred. Deployment operations show only the two RBAC Creates,
the existing empty-resource scope-guard deployment, identity Read and output
evaluation. No permission denial was observed or fabricated.

Filtered assignment inventory contains the existing registry-scoped AcrPull
and the new demo-API assignment only. No assignment was added to
`ca-cutover-test-api` or `job-cutover-test-init`. Both APIs' observed
environment/revision/ingress metadata are unchanged; the demo remains
`setup-pending-deny-all`. The source initializer's identity/environment
metadata remain unchanged. This verifies permission configuration, not MI
token propagation or exercised restart/job rights.

Private publication remains blocked on an existing authorized private
publisher. Relay approval and genuine tenant/browser/staff/SQL/AI acceptance
are still required; #360 d/e remain **UNMET**. No Graph/SQL/Key Vault secret
read, restart, job execution, image build, network change, new infrastructure,
spend or deletion occurred. Resource group `ama` and old stack are retained.

### Approved existing-job relay delta (2026-10-17, #360)

After the original full RPI and PR #379 publication, the owner supplied a new
explicit boolean true: "allow the initializer identity to read/write encrypted
result tags on the existing initializer job only. No plaintext secrets, job
configuration rights, new resources or broader scope. May I activate that
reviewed grant too?" This resolves the relay approval boundary only.

The reviewed source was unchanged on 2026-10-17. Its parameter name then was
`includeResultRelay`, not `includeResultTagRelay`. The following commands are
historical receipts; the current template no longer accepts either parameter.
Current Blob grants are default-off and need separate approval as described in
the current prerequisites above. Both historical preview and apply used:

```bash
az deployment group what-if -g ama --name staff-iam-360-relay-20261017 \
  --template-file infra/staff-initializer-rbac.bicep --mode Incremental \
  --parameters apiName=ca-cutover-test-demo-api \
  initializerIdentityName=id-cutover-test-init includeResultRelay=true
az deployment group create -g ama --name staff-iam-360-relay-20261017 \
  --template-file infra/staff-initializer-rbac.bicep --mode Incremental \
  --parameters apiName=ca-cutover-test-demo-api \
  initializerIdentityName=id-cutover-test-init includeResultRelay=true -o none
```

These record the authorized performed operation, not renewed execution
approval. Fresh what-if Succeeded with only two new-resource Creates: the
reviewed relay role definition and existing-job assignment, plus 95
same-group Ignore/NoChange rows. Raw what-if also labeled the existing API
assignment Modify. Its entire delta was the known MI reference vs resolved
principal, RG-addressed vs canonical role URI for the same GUID and
principalType NoEffect. Exact before/after equality after resolving only
those two references, plus independent actual API role/assignment reads
matching the original receipt, proved the permitted API-unchanged case.
No arbitrary Modify or extra resource was accepted; raw Modify was retained,
not misreported as NoChange. The scope guard still contains no resources.

Deployment `staff-iam-360-relay-20261017` **Succeeded**; correlation
`53c578e1-bea0-4655-a9ff-ce574b995d6b`. Separate post-apply ARM reads verified:

| Readback | Exact value |
| --- | --- |
| Role name / GUID | Staff initializer result tags (ama) / `64ec5d6d-f8ae-51ab-a93a-394f6cc97c6c` |
| Sole assignable scope | `/subscriptions/e51ebc89-79d0-4a52-a82b-01a292eefd5b/resourceGroups/ama` |
| Assignment GUID | `8e9a497e-3b90-50e2-a783-93e58755165b` |
| Actual assignment scope | `/subscriptions/e51ebc89-79d0-4a52-a82b-01a292eefd5b/resourcegroups/ama/providers/Microsoft.App/jobs/job-cutover-test-init` |
| Principal / type | `3830883a-f4af-44f8-bff8-8859b78fc2f8` / ServicePrincipal, existing `id-cutover-test-init` |
| Actions | `Microsoft.Resources/tags/read`, `Microsoft.Resources/tags/write` only |
| Exclusions / data permissions | `notActions`, `dataActions`, `notDataActions` all empty |

The canonical subscription-addressed role URI does not widen the ama-only
assignable scope or job-only assignment. The sole new initializer assignment
is that relay; existing AcrPull and API role/assignment are unchanged.
ARM deployment operation logs call idempotent PUTs "Create", including the
existing API role/assignment and empty guard metadata. Those are not new
effective grants: exact before/after API readbacks match. No workload resource
was deployed. Existing job identity/environment and both APIs' observed
environment/revision/ingress metadata match the pre-apply inventory; demo
deny-all remains.

No tag value was read or written, including test payloads. RBAC grants actions
at a resource scope, not a ciphertext-content filter: encrypted-only use and
no plaintext remain explicit owner/application constraints. Readback proves
the role configuration, not MI token propagation, worker execution or
end-to-end encryption acceptance. No secret/Graph/SQL operation, temporary
job, job configuration write/run, restart, image build, network change,
new workload/infrastructure/spend or deletion occurred. No permission denial
was observed. Private publisher and genuine tenant/browser/staff/SQL/AI
acceptance remain unproven; #360 d/e are **UNMET**.

### Restricted demo staging receipt (2026-10-17, #360)

The already approved additive migration created only
`ca-cutover-test-demo-api` and `authConfigs/current` in the existing external
`cae-cutover-test-demo`. Deployment `demo-stage-360-20261017` succeeded after
an exact two-Create what-if and a second unchanged-input scope review.
The retained source API digest, template/environment settings, identity,
secret references and auth are preserved; auth forward-proxy convention changes
to NoProxy for direct ingress. Azure materialized the default
`maxInactiveRevisions=100`; no application setting was silently reconstructed.
The old app/auth fingerprints match the pre-apply snapshot.

The direct hostname is
`ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io`.
It intentionally returns **403** for `/`, `/healthz`, `/api/me` and `/app`
under `setup-pending-deny-all` (Deny `0.0.0.0/0`). The replica is Healthy/Running.
This is verified restricted staging, **not** public welcome/health 200,
accepted anonymous-API behavior, real sign-in or replacement acceptance.
The staged configuration still has the invalid managed-identity client sentinel
and no browser credential, so do not remove the restriction yet.

The prerequisite wording below records the original staging point; the API
and separately approved relay grants are now applied as documented above.
The private publisher and human/runtime prerequisites remain outstanding.
After an authorized private publisher supplies the worker digest and an
authorized IAM operator activates the two exact scopes (API restart on
`ca-cutover-test-demo-api`, tag relay on `job-cutover-test-init`), the tenant
operator runs the single command above with `--login` once if needed. This VM
cannot perform that tenant action. The operator needs existing authorized
application/assignment and mailbox-purpose access, and the existing private
roster if SQL bindings already exist; no people or authority are invented.
Then verify real registration/credential/reference/runtime settings, review
the exact restriction-removal what-if and only then permit browser testing.
No restriction removal, SQL mutation/restart, live AI inference, Front Door
retirement or old-stack deletion occurred on 2026-10-17. Resource group `ama`
and all six backing-service privacy settings are preserved.

SQL prerequisites: `python3 -m pip install -e src/core -e src/agents -e src/api
pyodbc` and Microsoft ODBC Driver 18 for SQL Server on an authorized host
with private DNS/routing and SQL write authority. Setup separately diagnoses
Python 3.10+, Azure CLI and the Container Apps extension with exact install
commands, and supplies the isolated device-login link. Direct ingress never
requires Front Door commands or the CDN extension. SQL discovery confirms
the configured server is in `ama` and its public access is `Disabled`.

```bash
python3 infra/scripts/initialize-workbench-staff.py \
  --resource-group ama --container-app ca-cutover-test-api \
  --roster "$HOME/.azure/zava-forward-staff/roster.json" --check
python3 infra/scripts/initialize-workbench-staff.py \
  --resource-group ama --container-app ca-cutover-test-api \
  --roster "$HOME/.azure/zava-forward-staff/roster.json" --apply --restart
```

The initializer imports `ledger` and `mssqlstore` from `zava_forward.core` (moved in M2 of #199), so run `pip install --no-deps -e src/core -e src/agents -e src/api` first (M4 of #199 moved `chat_privacy`, `chat_isolation`, `recovery` to `core` and `ai_eval` to `agents`; no infra script imports them); `zava_forward.api.auth` (moved in M5 of #199) supplies the role map.

Use the existing MVP dependencies and an operator allowed through the SQL
firewall/private endpoint with SQL write authority. Graph management uses the
isolated `~/.azure/zava-entra-init` profile, or `--tenant-profile`. It needs
delegated `AppRoleAssignment.ReadWrite.All`, `Application.Read.All`, directory
user/group read access and an appropriate administrative role. No new grants
are consented automatically. See the official
[application-role assignment API](https://learn.microsoft.com/en-us/graph/api/serviceprincipal-post-approleassignedto?view=graph-rest-1.0).

Check mode is read-only: exit 0 means the directory/SQL configuration matches,
2 means reconciliation is required; it does not claim a user's browser sign-in.
Apply adds missing roles only for this application, preserves Default Access,
rejects conflicting effective roles (including direct group grants), and never changes
directory administrator roles or group membership. Existing bound identities
cannot be replaced. SQL staff/current owner labels are updated atomically,
preserving workload codes, cases, supplier scope, prior approvals,
recommendations and the existing audit prefix; one generic audit event records
the initialization. Historical generated actors remain historical.
Nested group assignments do not cascade to users, so only direct group
membership counts toward an effective role. See Microsoft's
[enterprise-app assignment guidance](https://learn.microsoft.com/entra/identity/enterprise-apps/assign-user-or-group-access-portal).

`--apply --restart` replaces replicas on every traffic-serving revision,
including after a no-op SQL retry. Apply without restart exits 3 to report
incomplete runtime convergence. If SQL commits but restart fails, retry the
same command: no duplicate role grant or audit event is created. Do not reseed
or weaken authentication to repair onboarding. New role assignments may
require the person to sign out and sign in again for fresh role claims.

### Authenticated Roster Result Transport Design (2026-10-20, Refs #360)

> **Superseded for the result path (2026-10-22):** owner decision DN1 rejected
> the ARM-tag relay proposed below. See
> [Private Blob result transport](#private-blob-result-transport-2026-10-22-refs-360).
> The text below is preserved as dated history, including its negative evidence.

**Status: design for review only. Nothing here was executed.** The owner
directed a documented authenticated alternative transport and a
tenant-administrator checklist ([#360 comment](https://github.com/jmservera/ama/issues/360#issuecomment-6290697080),
[#126 comment](https://github.com/jmservera/ama/issues/126#issuecomment-6290697705)).
No cloud allocation, deployment, Graph write, secret access, private dataset
access, billing run, live retry, parser relaxation or decryption occurred.
Whole #360 criteria c, d and e remain **unproved**; a design is not
acceptance.

**Process disclosure (2026-10-20).** The first version of this section was
written without activating the research, plan, implement and review skills.
That version's critique and review were not genuine RPI outcomes. A recovery
cycle re-ran research, planning with one critique, implementation and one
review, re-verified the evidence and corrected two statements below (the shared
decoder and the unverified prefix counting). Independent verification by the
coordinator and human reviewers is still pending; this section is not an
accepted outcome.

#### Preserved evidence (unchanged)

* Three bounded temporary-job recovery attempts (2026-10-19, [#360 comment](https://github.com/jmservera/ama/issues/360#issuecomment-6277108234)) are
  preserved. All temporary recovery resources were confirmed removed. The
  latest attempt passed registry checks, then the console decoder refused the
  provider's framing. No authenticated SQL projection or replacement candidate
  exists. The original private roster is unchanged.
* Public-source research then found an official Azure CLI HTTP recording of
  connection-control messages and application lines, but no exhaustive,
  versioned provider contract for control-message origin, partial versus full
  mapping, completeness or truncation. Sampled output is not authorization to
  discard unknown plaintext. The strict parser stays as is.
* **Unresolved contradiction.** Merged `staff_azure.py` has read results from
  ARM tags since #375 (2026-10-17), while the comment above describes console
  decoding. Repository evidence cannot show which code path the attempts ran.
  Reconcile this from the preserved private run record before any retry
  (decision DN3). No tag value was ever written or read live: the 2026-10-17
  relay grant was verified by role readback only.

#### Requirements and current mechanism

| Required property | Current mechanism | Gap the design must close |
| --- | --- | --- |
| Run binding | Per-run random `run`, per-run key, per-run tag prefix, run in AEAD associated data | None found |
| Query/operation binding | `operation` in associated data (`candidates`, `check`, `apply`) | No projection or schema version |
| Input binding | SHA-256 of payload plus target and relay in associated data | None found |
| Worker, manifest, image binding | Not in associated data; image only validated by the controller before start | Add as controller-held acceptance inputs, see below |
| Authorization | Entra and Azure RBAC on ARM; initializer identity limited to tags read/write on the existing initializer job | RBAC cannot filter tag content; effective-writer inventory needed |
| Confidentiality | AES-GCM ciphertext only in tags | Tags are plain text (official warning below); metadata exposure remains |
| Integrity and completeness | Contiguous index and count, AEAD over the whole value, frame and length bounds, terminal Succeeded required | Single accepted snapshot rule and concurrent-mutation tests |
| Freshness | Fresh per-run key and run, bounded deadline | No explicit not-after value in associated data |
| Fail-closed parsing | Tag values are rebuilt as log-style lines and read by the same console-line decoder; invalid frame, duplicate or tamper refuses, but a non-frame value under the run prefix is skipped | Strict tag-name grammar and extra-key refusal tests (S2) |

#### Options considered

Official sources were read on 2026-10-20; samples are not treated as
exhaustive guarantees.

| Option | Why | Verdict |
| --- | --- | --- |
| T1 ARM tag relay of AEAD frames, plus binding extension | Documented ARM tags API; Entra/RBAC; reachable from the operator without a private route; named records that need a strict grammar (see S2); no new resource; grant already activated on the existing job | **Proposed minimal option** |
| T2 Blob result written by the worker identity | [Blob data access uses Entra RBAC](https://learn.microsoft.com/en-us/azure/storage/blobs/authorize-access-azure-active-directory), but needs a private-endpoint route the operator lacks, the same route that is capacity blocked | Decision-needed fallback if T1 capacity is exceeded |
| T3 Log Analytics query | [Records arrive after several minutes' delay](https://learn.microsoft.com/en-us/azure/container-apps/log-options); query access is Disabled in the private profile; no completeness contract | Not suitable as primary |
| T4 Deployment script outputs | [Creates and bills a storage account and container instance](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deployment-script-bicep); outputs live in deployment history | Rejected |
| T5 Azure support clarification of console framing | Would give a contract for the failed path | Parallel owner action, not a dependency |
| T6 Console stream or exec | Failed three times, no exhaustive contract | Excluded; do not relax the parser |
| T7 Do not return candidates; derive positions from a versioned synthetic manifest | Removes the return payload | Decision-needed (DN4) |
| T8 Approved private-connected controller reading a private data-plane store | Avoids management-plane tag exposure and the frame bound | Out of current scope; needs a working private route and a costed plan; compare later, not rejected as unviable |

#### Proposed minimal design (T1)

The official [tags guidance](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources)
(ms.date 2025-09-15) gives a 50 name-value maximum and a 256-character value
maximum per resource, and warns that tags are plain text that can surface in
cost reports, tag-returning commands, deployment histories, exported templates
and monitoring logs. Therefore only AES-GCM ciphertext may be stored, and the
relay is a bounded, temporary carrier of position metadata, never of names,
UPNs, object IDs or the roster.

Synthetic size evidence (local arithmetic on the existing encoder and
`staff_candidates` shape, no private data): 25 positions need about 12 to 16
of 40 frames; 80 Programme-Manager-shaped or 60 Contractor-shaped positions
need 36 to 37 frames; 100 positions exceed the bound. The real position count
was not read and is unknown (DN2).

Proposed binding extension, subject to review and not implemented here:

* Associated data version 2 covers: version, run, operation, input digest,
  query identifier, result schema version, expected immutable image digest,
  SHA-256 of the worker script and of the manifest, and a not-after time.
* The controller, not the worker, holds the acceptance inputs: the exact
  temporary job resource ID, the returned execution ID, the expected image
  digest read through ARM, and its own file hashes. A result is accepted only
  if the decrypted claims equal those controller-held values.
* **Trust assumption.** The worker holds the per-run key. A valid AEAD result
  therefore proves possession of that key and agreement with the bound
  inputs, not independent proof that a particular image or script ran. Matching
  repository file hashes does not prove image contents. Independent
  image-to-source provenance (for example signed build provenance verified
  against the digest) does not exist yet. Record worker and image binding as
  an unresolved gap until it does (DN5); do not describe it as achieved.

Threat model for tag-capable principals:

| Principal or event | Possible effect | Control |
| --- | --- | --- |
| Holder of tags/write or write on the relay job | Delete, replace, collide with or exhaust frames: denial of service; cannot forge valid ciphertext without the key | Fail closed; effective-writer inventory before and after; stop on an unexpected writer; keep tag and Activity Log evidence; never treat as generic transport failure |
| Reader of tags, cost, history, export or logs | Sees run identifier, frame count and ciphertext length, timing and retained ciphertext | Privacy/security approval gate DN1; delete owned tags after the run and confirm |
| Eventual-consistency delay | Late frame looks like a withheld result | Bounded deadline, then refuse as ambiguous; a longer wait is a new, separately authorized run, never a hidden retry |
| Another tag writer overwrites or deletes an owned frame name | The worker refuses name collisions when it writes, but the [tags API Merge operation](https://learn.microsoft.com/en-us/rest/api/resources/tags/update-at-scope?view=rest-resources-2021-04-01) updates existing names, so a later overwrite is detected only by AEAD and causes refusal, never a repaired result | Fail closed; effective-writer inventory; treat as denial of service |
| Activity Log or other audit surface records the write | [Activity Log keeps management events for 90 days](https://learn.microsoft.com/en-us/azure/azure-monitor/platform/activity-log); whether tag values are recorded was not verified | Assume possible exposure of ciphertext until the DN1 review checks it |
| Stale frames from another run | Misread as current | Run-prefixed names plus per-run key; other prefixes are not read; a check that counts and reports them is proposed for S2 |

Fail-closed acceptance rules (all must hold, evaluated on one snapshot):
exact named execution terminally Succeeded; expected image digest unchanged;
tag names match one strict grammar; contiguous indexes with one consistent
count within the bound; no duplicate, extra or oversized frame; AEAD
authenticates; decrypted claims equal controller-held values; not-after not
passed. Any other state is Refused, Ambiguous or Failed, never a partial
result, and no unknown field is silently dropped. Compression, if later
permitted (DN2), needs a hard decompressed-size bound before decryption output
is parsed.

#### Script-oriented implementation plan (later, separately authorized)

| Step | Work | Offline exit evidence (synthetic only) |
| --- | --- | --- |
| S0 | Reconcile which path ran in the three attempts; capture the private run record outside Git | Written reconciliation, DN3 closed |
| S1 | Add associated data v2 and controller acceptance inputs in `staff_azure.py` and the worker; keep v1 refused after cut-over | Unit tests for each altered binding failing closed |
| S2 | Strict tag grammar and single-snapshot read; ambiguous-outcome states | Tests: replace, add, remove between reads, full capacity, stale same-prefix set, late frame, cleanup failure |
| S3 | Size guard and DN2 decision (compression or paging by role) | Boundary tests at 39, 40 and 41 frames; decompression bound |
| S4 | Image digest and job identity check before and after execution | Fake-ARM tests for digest drift and execution mismatch |
| S5 | Runbook and evidence updates; no private sample | Doc and link review |
| S6 | Operator dry run with fake ARM client only | Full local RPI gate |
| S7 | One live run only after the approvals below | Not planned until approved |

Preconditions before any live use: reviewer decisions DN1 to DN5; an approved
finite cost and execution plan (the #126 plan, which this design deliberately
does not depend on to be complete); fresh read-only inventory of the job,
identity, role assignments and tag count; explicit authorization for one run
of at most one temporary job, one replica, 600 seconds, with owned-only
cleanup. T1 adds no new Azure resource, so its additional cost is the existing
temporary job and ARM calls; no price is asserted here and the current
official pricing must be cited in the approved plan.

**Spending gate (correction 2026-10-20, from independent assessment).** Before
ANY paid start the owner-approved limit is an all-in USD 500 TOTAL for the
October calendar month, not a generic monthly budget. A start requires accrued
AND forecast charges and liabilities across the `ama` resource group and all
other scopes, each recorded with timestamp, scope and source, without double
counting, and a known, bounded headroom. Current headroom is unknown, and the
provisional unchanged RG-only projection of USD 535.41 is above the cap. Unknown
other spend must not be assumed zero, and estimated savings or retirements are
not authorized. A separate finite costed execution-plan approval remains
required (expiry 2026-10-25T16:02Z). No cost query was made for this design.

Decisions needed (not resolved here): DN1 privacy/security approval of
ciphertext and metadata in tags, covering classification, leakage, retention,
export and log surfaces, readers and policy compliance; DN2 real position count
and whether compression or per-role paging is allowed; DN3 attempt path
reconciliation; DN4 whether manifest-derived positions (T7) are acceptable;
DN5 independent attestation or an explicit trusted-endpoint acceptance.

#### Tenant-administrator and operator checklist (for review, nothing run)

Resource management inside `ama` does not imply tenant authority. Read-only
metadata may establish what exists, never permission to change a tenant
object. Do not use another application's client, a random user, an invented
staff binding or an old private dataset. Record evidence as names, counts and
pass/fail only, outside Git where private. Stop at the first failed row and
make no success claim.

| # | Check | Owner and evidence | Stop condition |
| --- | --- | --- | --- |
| 1 | Written authority: tenant administrator names the allowed app registration, enterprise app, roles and assignments; RG authority is not accepted | Tenant administrator, dated record | Missing or RG-only authority |
| 2 | Real application and enterprise app exist for this workbench; roles are in the manifest; assignment required is on | Tenant administrator, read-only Graph/portal record | Wrong app or reused client |
| 3 | Credential created in the tenant; value reaches the private vault path only through the supported handoff; no value printed or committed | Operator, secret reference name and version metadata only | Value seen in logs, args or Git |
| 4 | Private vault path verified: vault public access Disabled, API identity can read only the reference, no new identity | Operator, ARM metadata | Public access on, bypass, new identity |
| 5 | Private roster exists outside Git with owner-only permissions, built from real people with written approval; none invented | Roster owner, file mode check and counts | Fabricated or unapproved person, wrong mode |
| 6 | Relay RBAC evidence: effective read, write and delete paths on the relay job at RG, resource, inherited and privileged levels, exported before and after a run | Tenant administrator and IAM operator | Unexpected writer, unreviewed grant |
| 7 | Relay identifiers recorded privately: exact job resource ID, worker identity, expected immutable image digest with verified provenance, tag count below capacity | Operator | Digest unpinned, provenance missing, capacity short |
| 8 | DN1 privacy/security approval recorded, including Activity Log, diagnostic, cost and export surfaces assessed | Security reviewer | Not approved |
| 9 | Finite cost and execution plan approved separately (resources, runtime, expiry, cleanup) with accrued AND forecast charges and liabilities across `ama` and other scopes recorded (timestamp, scope, source), known bounded headroom under the all-in USD 500 TOTAL October gate, no assumed-zero unknowns, no double counting; expiry 2026-10-25T16:02Z | Owner | No approval, headroom unknown or over cap |
| 10 | SQL: private-only access verified, apply and verified serving-replica restart on every traffic-serving revision, then a fresh `--check` exits 0 | Operator on a private-connected host | Public SQL, no restart evidence, check not 0 |
| 11 | Direct HTTPS: welcome and health 200, anonymous protected API denied, native 401, browser sign-in redirect, production profile and the six private backing-service settings unchanged | Operator, probe JSON lines | Any mismatch, setting changed |
| 12 | Browser role tests with real people: one staff role each, Contractor cannot read staff-wide statistics, unknown or wrong role denied, sign out and in for fresh claims | Real users, screenshots without claims | Role not enforced |
| 13 | Preserve identities and Front Door; never delete `ama`; retire Front Door only after checks 10 to 12 pass and the owner explicitly authorizes | Owner | Any deletion without both |

Non-claims: this design does not show that the relay carries a result, that
the roster can be recovered, that sign-in, Graph authority, deployed SQL or AI
work, or that #360 criteria c, d or e are met. No cloud state was read for this
design; the 2026-10-17 and 2026-10-19 receipts above remain dated evidence and
need a fresh read-only recheck before use.

### Private Blob Result Transport (2026-10-22, Refs #360)

**Status: implemented and tested offline with fake clients only. Nothing was
deployed, no role was granted and no Azure resource or tenant was touched.**
Whole #360 criteria c, d and e remain unproved. This section supersedes the
tag relay of the 2026-10-20 design above and records owner decisions DN1 to DN5
(2026-10-22).

| Decision | Effect in the design |
| --- | --- |
| DN1 | Results travel through a private Blob container with managed identity. No resource tags, public Blob, SAS or shared key. Backing services stay private. |
| DN2 | Complete results, measured size, bounded paging. Over-bound results are refused, never truncated or reduced. |
| DN3 | The three earlier failures stay unknown historical transport failures. Old tag/console result code is retired; the Blob path is validated independently. Root-cause analysis is production follow-up, not claimed solved. This is not permission to delete Front Door or any Azure resource. |
| DN4 | Production roles are assigned manually through the Entra Enterprise App. The demo may match roles from available evidence, else random demo assignment. The admin-prefixed account stays Zava Forward administrator (ProgrammeManager). No directory roles are granted and immutable staff bindings or history are never overwritten. App roles remain the authorization source; a role is not professional competence or real authority. No roster contents are recorded in this repository. Existing role-assignment behaviour (#363) is unchanged by this work. |
| DN5 | A controlled demo worker with expected image, run identity, integrity and completeness checks is accepted. Independent signed source or image attestation is **unverified and deferred**, not established. |

#### Design

1. The worker runs in the private VNet with the existing user-assigned identity. It writes AES-GCM pages to the `staff-results` container (`<run>/page-NNN.json`, no overwrite). The header (run, operation, payload digest, image digest, schema, index, count, item and byte totals, creation and expiry) is the authenticated associated data.
2. The per-run key exists only in the job secret and the controller's memory. Blobs left behind cannot be decrypted later.
3. The controller needs ARM for job control (works from anywhere) and Entra data-plane access to the private Blob endpoint (needs private-connected routing: Bastion/jump host, VPN or an equivalent). There is no operator IP firewall exception.
4. Before any job is created the controller calls `preflight`: the route must work and the run prefix must be empty. If the Blob cannot be reached it refuses and creates nothing.
5. The result is read only after the execution reports `Succeeded` and the job image digest still matches discovery. Anything else is refused: a missing, extra, duplicated, swapped, tampered, oversized, expired, future-dated or mismatched page; a total mismatch; a wrong run, operation, digest or image. There is no console, tag or local fallback and no parser relaxation.
6. If the read fails after the job ran, the outcome is **unverified** (SQL and restart may have happened). Recovery is a new, separately authorized run after reading the live state; never a blind reapply.
7. Discovery verifies through ARM that the storage account named by `ZF_BLOB_ACCOUNT_URL` has public network access Disabled, shared key and anonymous Blob access off, and that the `staff-results` container has no public access. The URL must be an exact public-cloud `*.blob.core.windows.net` account.
8. Bounds: 48 KiB plaintext per page, 128 KiB per blob, 64 pages, 900 s validity with 60 s skew. A result over the bound fails with an explicit error. The real result size has not been measured; that is a live prerequisite.

#### Code and infrastructure

| Area | Change |
| --- | --- |
| `scripts/staff_blob.py` | New codec, `preflight`, write and read validation, shared `StaffJobError` |
| `scripts/staff_azure.py` | Tag and chunk transport removed; Blob discovery checks, preflight, post-success read, image-drift check |
| `scripts/staff-azure-worker.py` | Writes pages with `ManagedIdentityCredential`; never logs detail |
| `modules/storage.bicep` | `staff-results` container appended last (existing index references stay valid) and a lifecycle rule that deletes blobs and versions after one day. Soft delete keeps 30 days |
| `staff-initializer-rbac.bicep` | `includeResultBlob` (default false). Custom role with only `blobs/write` and `blobs/add/action` at the container scope; no read, list or delete |
| Image and checks | `staff_blob.py` added to the Dockerfile, `.dockerignore`, `tools/rpi-checks.py` and CI lint lists |

Residual risk: principals with account-wide data or management rights, such as
subscription Contributors or Owners, can overwrite or delete blobs. The
authenticated encryption turns that into a refusal, not a false success.

#### Review corrections (2026-10-30)

The controller requests at most 128 KiB + 1 byte from offset zero for each
download, rather than buffering an unrestricted replacement before checking
the listed size. The 2026-10-31 hardening also passes that hard byte limit to
the downloader's `read`, never an unbounded `readall`.
Overflow and listing/download length changes are refused
before decoding; the extra byte detects growth beyond the Blob bound.
The existing overall deadline and temporary-job/roster-secret cleanup remain.

Paging measures the complete serialized head and each items wrapper, including
comma/escaping overhead. Exact 48 KiB pages are accepted; oversized heads,
items or intermediate pages and a 65th page are refused before any upload.
The offline regressions include the reviewer's near-boundary counterexample,
exact limits, escaped/Unicode content and replacement between list/download
with confirmed controller cleanup. Fake clients do not establish live SDK,
private-route or managed-identity behavior.

The current setup prerequisites, RBAC examples and cleanup above now describe
the default-off Blob grant and lifecycle-retained ciphertext. Explicitly dated
tag activation receipts below remain historical; their removed parameters are
not current deployment instructions. The older run9 receipt predates current
main integration and is not exact-head validation. Fresh local gate evidence
and hosted scoring must be bound to the final published candidate separately.

#### Correction 1 (2026-10-22): operator context and operation budget

* The controller reads Blob with a credential bound to the selected operator
  profile: `az account get-access-token --resource https://storage.azure.com/`
  runs through the same `Azure` wrapper and `AZURE_CONFIG_DIR` as every ARM
  call, including the isolated tenant-profile fallback. There is no ambient
  `DefaultAzureCredential` chain. The token is primed under a bounded deadline
  before preflight, cached in memory and never printed.
* The Blob client sets explicit socket and retry limits (connect 5 s, read
  15 s, two retries) and every list or download carries a server timeout. An
  overall budget (45 s for preflight, 45 s per read, capped by the job
  deadline) is enforced by abandoning the read-only call on expiry, because a
  per-socket timeout alone is not an overall deadline. Preflight expiry means
  no job was created; read expiry means the outcome is unverified, and the
  job and roster secret are still cleaned up. Offline tests only; live
  behaviour stays NOT RUN.

#### Live prerequisites (all NOT RUN)

These are the dated 2026-10-22 prerequisites, not current execution authority.
The October expiry in item 1 has passed. Main's later dated budget/identity/
handover records are preserved; they do not prove this Blob path was deployed
or tested live. A new finite plan and the relevant approvals are still needed.

1. Coordinator release of a verified affordable finite execution plan within the USD 700 replacement all-in October forecast ceiling (expiry 2026-10-25T16:02Z). No Azure charge, deployment or role write before that.
2. Deploy the storage change so the `staff-results` container and lifecycle rule exist, then deploy the RBAC template with `includeResultBlob=true` and `storageAccountName`, container first, role second. A deployer with `Microsoft.Authorization/roleAssignments/write` and role definition write at the resource group is needed; resource group ownership does not prove Microsoft Graph permissions.
3. Operator identity: `Storage Blob Data Reader` (or an equivalent list/read data role) on the `staff-results` container, ARM read on the job, storage account, containers and the API app, and a private-connected host that resolves and reaches the Blob private endpoint.
4. Microsoft Graph application permissions required by the existing setup are separate and must be named by the tenant administrator; they are not inferred from resource group ownership.
5. `ZF_BLOB_ACCOUNT_URL` set on the API app (already wired in `containerapps.bicep`) and the cutover-proof image rebuilt with `staff_blob.py` and pinned by digest.
6. Measure the real position count and result size on a dry or check run, then confirm it fits the page bound. Over-bound is a design change, not a silent reduction.
7. Prove private routing, the managed-identity write and the Entra read in a controlled run. Record receipts without names, UPNs, object IDs, roster contents or secrets.

#### Not run and not claimed

Live private routing, managed-identity Blob write, operator Entra read, a real
job, deployment of the Bicep, Entra or browser acceptance, role acceptance with
real users, AI behaviour, signed source or image attestation (DN5, deferred),
and demo screen-reader acceptance (documented unverified production follow-up).
Local tests use fake clients and prove only the offline contract.

#### Transport evidence and integration (2026-10-30, Refs #360)

The current-main integration keeps the installed `src/` namespace,
main's IoT sender/receiver scopes and release controls, and the private Blob
transport from this branch. Helpers remain in `infra/scripts`; the worker
imports `zava_forward.core.mssqlstore` from the installed core distribution.
No retired `mvp/` code or old tag permission is restored. The preceding
DN1-DN5 decisions and historical failures remain unchanged.

| Claim | evidence | rationale | change_reason |
| --- | --- | --- | --- |
| Private result channel, DN1 | [Blob codec](./scripts/staff_blob.py), [controller](./scripts/staff_azure.py), [RBAC](./staff-initializer-rbac.bicep), [role matrix tests](./tests/test_identity_rbac.py) | Managed-identity write and operator-profile Entra read avoid tags, SAS, shared keys and public access; fake clients do not prove a live private route | Replaces the historical tag relay; main's unrelated IoT roles are retained |
| Complete bounded results, DN2 | `BlobCodecTests`, `StorageContractTests` and controller cases in [transport tests](./tests/test_staff_azure.py) | Authenticated run/image/input binding, page totals, expiry and fail-closed checks refuse ambiguity rather than truncate | Preserves paging and profile/deadline correction; real position count and size remain unmeasured |
| Historical failures and role authority, DN3/DN4 | Decision table above, [worker](./scripts/staff-azure-worker.py), [staff initializer](./scripts/initialize-workbench-staff.py) | Unknown earlier failures are not retroactively explained; transport changes do not confer tenant roles, professional authority or permission to delete resources | Retains decisions while main's later identity and directory-retirement evidence remains authoritative for its own dated scope |
| Controlled worker, DN5 | `ProfileCredentialTests`, `StorageContractTests`, `BuildContextTests` and image-drift cases in [transport tests](./tests/test_staff_azure.py) | Source tests establish local refusal and packaging contracts, not independent image-to-source provenance | No attestation or live-success claim added; signed provenance remains deferred |

These columns describe engineering provenance, not a scorecard or instructions
to the scorer. For the capstone, this is narrow A1/A3/A5 infrastructure evidence.
It supplies no new AI evaluation, autonomous behavior, measured live latency/
cost, pitch rehearsal or thought-leadership publication. Local tests must be
reported with their actual results; prior counts are dated, not a current pass.

The rejected alternatives remain explicit: tags expose management metadata
and imposed a small result bound; console output was historically ambiguous;
public Blob/SAS/shared keys violate DN1; silently shrinking results violates
DN2. Private Blob instead requires a genuinely private-connected controller,
separate data-plane RBAC, retained ciphertext lifecycle and a newly approved
finite run. Those operational costs and live prerequisites are not removed
by offline success.

### Public welcome and Microsoft account photos

The existing registration is retained. Add only delegated own-user Graph
`User.Read` with the same isolated provisioning profile:

```bash
python3 infra/scripts/setup-entra.py --account-photo
python3 infra/scripts/setup-entra.py --account-photo --check
```

This opt-in flag merges `User.Read` into existing requested permissions,
preserving all previous permissions/redirects. It does not grant administrator
consent, rotate existing credentials or request app-only
`ProfilePhoto.Read.All`. The setup command also reconciles its ordinary
registration/roster/auth scope as described above. Users complete normal Microsoft sign-in/MFA/consent;
an administrator handles consent if tenant policy requires it. Never share
passwords, device codes, access tokens or a CLI profile directory.

Photos use the supported Container Apps Blob token store and a server-only
Graph `/me/photo/$value` proxy, not browser `/.auth/me` token retrieval.
Deployment has two deliberate stages:

1. Keep all existing deployment parameters and the real image. Deploy with
   `enableEntraTokenStore=true entraTokenStoreReady=false`. This creates a
   dedicated token-only storage account, private `auth-tokens` container,
   private endpoint, scoped maintenance identity and daily renewal job.
   Shared account keys and public Blob access remain disabled.
2. Start the maintenance job and require execution status `Succeeded`:

   ```bash
   az containerapp job start -g ama -n job-forward-test-auth-renewal -o none
   az containerapp job execution list -g ama -n job-forward-test-auth-renewal \
     --query '[].{name:name,status:properties.status,start:properties.startTime}' -o table
   ```

3. Only after success, redeploy the same parameters with
   `enableEntraTokenStore=true entraTokenStoreReady=true`. The API references
   the existing `entra-token-store-sas` secret; Bicep never resets its value.
   Auth now requests `openid profile email`, own-user `User.Read` and
   `offline_access`, with the Microsoft account chooser on fresh login.
4. Sign out and sign in again to obtain the new delegated scope. Confirm the
   account name/photo and logout/switch with an actual authorised user.

#### Account selection and safe flow diagnostics

"Use another account" is not Sign out. It goes to the fixed
`/sign-in?switch=1` route, which requests Easy Auth login with
`prompt=select_account` and returns to `/app`. Microsoft presents remembered
accounts or a sign-in form when none are remembered; the user chooses the
account. No global Microsoft logout is requested. Cancelling or choosing the
same account does not guarantee a changed account or a signed-out session.
Normal Sign out still uses platform logout and returns to the public welcome.
See Microsoft's [account-selection parameter](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow#request-an-authorization-code).

The API emits five fixed console markers: `sign-in-started`,
`account-picker-started`, `account-switch-requested`, `sign-out-requested` and
`workbench-entered`, prefixed `auth flow:`. The latter three require successful
app authorization; POST markers also require the existing CSRF header.
New markers contain no identity, URL/query, cookie, principal or token values.
This does not claim all pre-existing platform/denial logs are identity-free.
Generic HTTP access logging remains disabled.

The existing environment `allLogs` diagnostic setting already routes console
output to `log-forward-test`; no new logging resources or role grants are
needed. Live console access:

```bash
az containerapp logs show -g ama -n ca-cutover-test-api \
  --type console --tail 50
```

Use the resource-specific `ContainerAppConsoleLogs` table, not the legacy
`ContainerAppConsoleLogs_CL`. Allow ingestion delay and query fixed events
instead of publishing raw platform logs:

```kusto
ContainerAppConsoleLogs
| where TimeGenerated > ago(1h)
| where ContainerAppName == "ca-cutover-test-api"
| extend Event = extract(@"auth flow: (sign-in-started|account-picker-started|account-switch-requested|sign-out-requested|workbench-entered)", 1, Log)
| where isnotempty(Event)
| summarize Events=count(), Latest=max(TimeGenerated) by Event, RevisionName
```

These events show attempted routes, not which account was chosen. Actual
acceptance starts with an authenticated browser: open Use another account,
select another authorised account and verify its current-account view and
permitted work. A fresh anonymous browser or operator CLI cannot prove session
replacement. Do not share browser cookies, passwords or tokens.

The job uses `ManagedIdentityCredential` and a five-day, HTTPS-only,
read/write/delete user-delegation SAS, renewed daily at 03:00 UTC. Its identity
has Blob Delegator at account scope, Blob Contributor only on `auth-tokens`,
Secrets Officer only on `entra-token-store-sas`, and registry pull. Existing
evidence/import identities get no rights on the separate token account.
Authentication tokens are real secret/personal authentication data, not the
constructed fixture. No token values/photos enter Git, job output or evidence.

Monitor failed/missing renewal executions and act before the last successful
SAS expires; daily renewal leaves about four days of overlap. Job output
reports only status/expiry and fails nonzero without overwriting a secret on
delegation failure. Versionless Key Vault references retrieve updates within
30 minutes; the secret-ref environment setting triggers active revision
refresh. Do not expose its value. See Microsoft's
[Container Apps secret rotation guidance](https://learn.microsoft.com/en-us/azure/container-apps/manage-secrets#reference-secret-from-key-vault)
and [token-store contract](https://learn.microsoft.com/en-us/azure/container-apps/token-store),
checked 2026-10-12.

The UI shows initials and an explicit status when no photo exists or token,
consent or upstream access fails. An expired photo token gets at most one
supported `/.auth/refresh` attempt. This does not weaken workbench/API
authentication or make a mocked photo a live acceptance result.

## Microsoft 365 permissions

For the optional SharePoint evidence store, the runtime identity needs
Microsoft Graph application permission `Sites.Selected` plus a per-site grant
(`scripts/grant-sharepoint-access.sh`, role `write` for the evidence library).
The rebuilt exercise uses Blob; SharePoint grants are not a prerequisite for
that deployment. Teams alerts use a Workflows webhook, which needs no Graph
permission and is created by hand in the channel. Neither an optional template
parameter nor a placeholder worker proves that integration has run.

Setting the optional site and channel up through the m365 CLI needs delegated
Graph permissions on its provisioning app, consented by an administrator:
`Sites.FullControl.All`, `Team.Create`, `Channel.Create`,
`AppRoleAssignment.ReadWrite.All` and `Application.Read.All`.
The existing SharePoint `AllSites.Read` permission is separate from these
Graph scopes and does not grant application-management authority.
`scripts/configure-m365-provisioner-app.sh <app id> --consent` requests and
optionally consents the Graph scopes; it is an operator step, not runtime
startup. Remove unnecessary provisioning consent afterwards, including
`Sites.FullControl.All` once the grants are made. Own-user photos separately
use delegated `User.Read`, not tenant-wide application photo permission.

### API registration management with the existing M365 session

The supported single-line entry point is:

```bash
python3 infra/scripts/setup-entra.py
```

This is Entra application setup, not M365 user creation, licensing, Teams or
SharePoint provisioning. It does not access an existing M365 CLI cache. It
reads the deployment operator's Azure context for the selected subscription
and tenant; device-code sign-in writes only the independent
`~/.azure/zava-entra-init` profile (mode 0700), never the operator's profile.
Use `--login` to renew that isolated session, or `--tenant-profile` for another
private directory outside Git. The directory account must match the deployment
tenant. With no deployment login, setup offers isolated device-code login;
the account must have access to the existing `ama` group. Follow the printed
device-login URL/code in a browser as an authorized human. Other login output,
directory names, IDs and CLI stderr are suppressed. The sign-in has a
five-minute limit; rerun if it expires.

If login waits without displaying a device code, interrupt it with Ctrl+C and
authenticate directly in the same isolated profile, with warnings enabled:

```bash
AZURE_CONFIG_DIR="$HOME/.azure/zava-entra-init" \
AZURE_CORE_ONLY_SHOW_ERRORS=false \
az login --use-device-code --allow-no-subscriptions --output none
python3 infra/scripts/setup-entra.py
```

Choose the deployment's tenant. For `--tenant-profile`, use that directory
instead. Rerun setup without `--login` to reuse this session. Interactive setup
keeps Azure CLI warnings enabled internally because older CLI versions emit
the device code as a warning; only the recognized device-code instructions
are printed. Other setup commands retain warning suppression.

Preflight checks Python >=3.10, az, the isolated `containerapp` extension,
login, Graph token permission hints and authenticated management/Graph reads
(also the network check). Nothing requires a Python framework or package.
Permission hints do not prove app ownership, directory role, policy or write
authority; a denied write is an error, not a missing object or successful setup.
For missing tools the script prints installation commands. Supported examples:

```bash
python3 -m pip install azure-cli
# Or Windows: winget install Microsoft.AzureCLI
# Or macOS: brew install azure-cli
# Python if missing: sudo apt install python3
# Windows: winget install Python.Python.3.12
# macOS: brew install python@3.12
mkdir -p ~/.azure/zava-entra-init
chmod 700 ~/.azure/zava-entra-init
AZURE_CONFIG_DIR=$HOME/.azure/zava-entra-init az extension add --name containerapp --upgrade
AZURE_CONFIG_DIR=$HOME/.azure/zava-entra-init \
AZURE_EXTENSION_DIR=$HOME/.azure/zava-entra-init/cliextensions \
az extension add --name cdn --upgrade
```

The `cdn` extension supplies `az afd` discovery commands on CLI installations
where they are not built in. Install it in the setup extension directory, not
only the operator's default extension directory. Setup reports a missing `afd`
command with these installation instructions rather than a generic request
failure. For `--tenant-profile`, substitute that private directory.

All CLI calls disable file logging, telemetry and automatic extension installs;
use no shell tracing, CLI debug logging or external session recorder when
handling private directory inputs. No real tenant, subscription, object IDs,
secrets or emails should be copied into repository evidence. Generic portal
URLs deliberately contain no identifiers.

The same run reads `~/.azure/zava-forward-staff/roster.json`, or `--roster`
outside Git. Parent directory must be mode 0700 and file mode 0600.
Each entry needs a distinct existing staff code, one `userId` and an explicit
approved role. Group-only rows cannot bind SQL staff. Fictional schema example (replace placeholders
privately; these strings are not usable directory identities):

```json
[
  {"code": "fictional-coordinator", "userId": "<private-user-object-id>", "role": "Coordinator"},
  {"code": "fictional-quality-inspector", "userId": "<different-private-user-object-id>", "role": "QualityInspector"}
]
```

Role keys are `Coordinator`, `LiaisonOfficer`, `SafetyLiaison`, `GrantsOfficer`,
`QualityInspector`, `ProgrammeManager`, `SupportOfficer` and `Contractor`.
Users must be enabled tenant members. Existing direct-group grants are still
checked when computing each person's effective application role.
Existing code/userId-only staff rosters need explicit `role` enrichment for
this setup tool; it never infers a person's authority from their code or name.
Invalid, duplicate or permissively readable input blocks before directory
writes. Missing or exact-template rosters follow the guarded
[automatic demo assignment](#tenant-staff-and-application-role-initialization)
above; no identities, codes, suppliers or approvals are fabricated.
Assignments are additive and app-scoped, preserve Default Access and unrelated
grants, and reject conflicting direct or effective direct-group app roles,
including conflicts from existing group grants.
Nested groups do not confer app assignments. A directory rejection remains a blocker.
No users, groups, group memberships, guests or administrator roles are created.

An authorized provisioning principal needs application-write permission
(`Application.ReadWrite.All`, or application `Application.ReadWrite.OwnedBy`
for owned apps), `AppRoleAssignment.ReadWrite.All` for roster writes and
appropriate user/group read permissions (`User.Read.All`,
`GroupMember.Read.All`), plus the directory role/ownership required by Graph.
Automatic demo assignment also needs readable candidate mailbox user purposes
(`MailboxSettings.Read`); it refuses unverifiable mailbox types rather than
silently selecting personal-looking resource accounts.
Already-consented broader directory scopes are recognized but never requested
or added. Azure RG Owner, an M365 login, and directory authority are different:

* Option A: authorized owner/admin uses
  <https://entra.microsoft.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade>
  > All applications > select the workbench registration > Authentication
  (Web redirect URLs) / App roles. For assignments use
  <https://entra.microsoft.com/#view/Microsoft_AAD_IAM/StartboardApplicationsMenuBlade/~/AppAppsPreview>
  > All applications > select the workbench > Users and groups >
  Add user/group > select principal > Select a role > Assign.
* Option B: authorized tenant admin approves the provisioning client's
  narrowly required management permissions and directory authority, then the
  operator renews the isolated session with `--login` and reruns. A service
  principal without that authority cannot use resource-group ownership to
  grant it to itself. Remove unnecessary provisioning grants afterwards;
  never add directory-management permissions to runtime managed identities.

`--account-photo` only merges delegated own-user Graph `User.Read`, preserving
other requested permissions. User consent may occur naturally at sign-in
where policy permits. If administrator consent is needed, setup prints the
identifier-free portal URL and exact API permissions > Grant admin consent >
Yes steps, then polls the app's Graph grant for up to `--wait-seconds` (default
300, maximum 1800). Use `--wait-seconds 0` or read-only modes to report pending
consent without waiting. It never clicks consent or grants directory-wide
management consent itself. A timeout/denial is not a pass.

App-role assignments alone do not initialize SQL staff. Setup now orchestrates
the
[private-network staff binding and replica restart](#tenant-staff-and-application-role-initialization)
with a complete user roster, not a group row, and installed source packages,
or prints the exact authorized-host command when private connectivity is absent.
SQL stays private; only the explicitly selected workbench staff/current-owner
records and minimal audit/sequence metadata are reconciled, never reseeded.
Juan Manuel Servera's exercise Legal, Compliance and DPO role is not tenant
authority, resident consent, safety approval or operational rule activation.
ADR 0005 remains accepted for synthetic development only; real owners and
sources are still a gap before operational reliance.

Roster reruns preserve enabled user-assignable supplemental capabilities
registered in the manifest, including `ZavaForward.AIRestart`, independently
of the one mutually exclusive staff role. Conflicting staff roles and unknown
or incompatible assignments still block reconciliation. Setup never assigns
these capabilities from the staff roster; retaining an existing permission is
not appointment of an actual restart authority or operational approval.

Offline evidence: `python3 -m unittest discover -s infra/tests -p
test_setup_entra.py -q` covers fake-az discovery, ambiguity, creation/reruns,
drift, private roster, edge matching, secret redaction and failure recovery.
This is not evidence of tenant provisioning or successful human sign-in.

The existing delegated M365 session was checked on 2026-10-12. Its consented
Graph scopes do not include application management. Being logged in does not
make `entra app` write operations authorised. Azure RG Owner and the signed-in
user's directory authority are also distinct from the CLI client's consented
Graph permissions.

For delegated Graph application updates, Microsoft's
[Update application permission table](https://learn.microsoft.com/en-us/graph/api/application-update?view=graph-rest-1.0)
requires `Application.ReadWrite.All`, plus appropriate ownership/directory
authority. `Application.Read.All` is not sufficient to change redirects, app
names or roles. Prefer an authorised owner making this one-off portal update.
If CLI management is needed, an authorised administrator must temporarily
consent the management permission for the provisioning client and obtain a
fresh authenticated session. Remove unnecessary provisioning grants afterwards;
do not add tenant-management permissions to runtime identities.

A separate, legitimate delegated API-token request through the current M365
client returned `AADSTS65001` (consent required). That client is not an
alternative authenticated acceptance path. Graph management consent and
workbench sign-in are separate concerns: updating the registration does not
automatically consent another client to call the API, and an API token cannot
be substituted with a Graph token or forged proxy claims.

## Rebuild authoring and local rehearsal (Refs #148)

The installed `zava_forward.orchestrator.rebuild` module authors the ordered
rebuild/check contracts and runs a **synthetic local SQLite control-plane
simulation only**. The historical observed rebuild below remains unchanged.

### Scripted Azure rebuild and teardown (Refs #148)

`python3 -m zava_forward.orchestrator.rebuild_azure {rebuild|teardown}` drives
the same stages against the `ama` group. It is a **dry run by default** (prints
the plan, makes no `az` or network call); `--apply` executes. Every command is
an argv list with no shell. A guard refuses any argument that looks like a
secret or token; the SQL token goes only in a child process environment, and
the Key Vault credential is checked by name, never read or passed. The seed and
roster files are scanned and rejected if they hold an email-like value outside
`*.test` or `example.com/org/net`.

```bash
python3 -m zava_forward.orchestrator.rebuild_azure rebuild \
  --subscription <id> --registry <acr> --image-tag <tag> \
  --parameters <private.bicepparam> --seed <synthetic-seed.json> \
  --roster <synthetic-roster.json> --container-app <api-app>   # dry run
# add --apply to execute; --from-stage <name> resumes after a stop
```

Rebuild requires empty resource and budget inventories, then runs deploy
(`deployApplications=false`), discovery, image build, credential check, SQL users,
synthetic seed, application deploy, Entra `--check`, staff reconcile and
`--check`, health/401/redirect probes and a revision restart with health recheck,
verifying after each step. `workload-sql`, `model-standard` and `model-capable`
have no scripted probe: the run stops with exit status 2 and records them as
`operator-gated`, never as passed. Teardown reuses the dependency order
(apps/jobs, private endpoints, environment, network, identities), waits for each
delete, rechecks the exact inventory before and after each delete, deletes
budgets last, and verifies both inventories are empty. A resource-group lock, a
`retain=true` tag, an unmodeled type or inventory drift stops it before the next
deletion; the group, locks and soft-deleted services are never touched.
Tests (`src/orchestrator/tests/test_rebuild_azure.py`) use a stateful fake `az`
as the disposable environment. A real disposable Azure rebuild/teardown has not
been run or authorised, so that part of the fourth criterion remains open.

After installing the [source packages](../src/README.md#commands):

```bash
python3 -m zava_forward.orchestrator.rebuild --dry-run
python3 -m zava_forward.orchestrator.rebuild --synthetic-local
```

Dry-run prints the fixed stage, integration and verification contracts without
backend reads, workspace creation, credentials or Azure access. The local mode
creates an exclusively owned temporary SQLite file, generates an invented case,
audit witness and `example.test` staff row, checks them through reopened
connections, removes modeled resources in dependency order and separately checks
budget inventory. It cleans only that owned temporary workspace. It never reads
`ZF_DATA`, a roster, an Azure profile, `.env` or private programme data.
`local-sql-verified` means a SQLite fixture check, not Azure SQL, workload identity
or application-store acceptance; `simulated-not-live` means no corresponding
image, auth, HTTP or model operation was executed. A failing checkpoint exits
nonzero with `REBUILD_FAILED`, never an automatically reported successful rebuild.

The sequencing library rejects foreign subscription/group IDs, unknown types,
duplicate IDs, locks, retained resources and missing boolean safety evidence.
It admits at most 1,000 combined resource/budget records per authoring inventory.
It validates both inventories before the first deletion and compares their
exact remaining records before and after each deletion, stopping on drift,
unconfirmed deletion or unexplained disappearance. Its bounded allowlist/order
covers the modeled resource types, not every possible Azure child or extension;
unsupported inventory must stop, not be skipped. It never removes locks,
purges soft-deleted services or weakens retention to obtain an empty result.
Budgets are separate and last. These checks do not eliminate cloud races.

The remaining #148 acceptance needs authorized preservation of
the continuing synthetic stock/programme lineage, private credential/tenant
operations and a separately authorized disposable Azure rebuild/teardown.
An owner must approve the exact deletion/preservation inventory; Legal/Compliance
must resolve any applicable retained-data/hold disposal decision before a later
live adapter may act. No such decision, authority, deployment or cloud test is
inferred from this rehearsal. The first three criteria are implemented and unit-tested
against a fake `az`; the fourth is partial until a disposable Azure run is authorised.

## From-empty rebuild observed on 2026-10-12

The owner-authorised `ama` reset retained the group, its policy-exception tag,
external deployment identity and tenant/M365 resources. No workload identity
needed preservation: Blob was the active evidence store, and Bicep/SQL recreated
the four workload identities and their grants. Do not generalise that decision
to identities with external site grants or other shared consumers.

Deletion has service-specific dependencies. Remove apps/jobs and private
endpoints before their environment/network, the Foundry project before its
account, and the private-link scope before its linked App Insights component.
Wait for accepted deletions to finish. Enumerate and delete resource-group
budgets separately; `az resource list` does not list them. Verify both the
generic inventory and this budget list are empty before deploying:

```bash
az resource list -g ama --query '[].{name:name,type:type}' -o json
az rest --method get --url \
  "https://management.azure.com/subscriptions/<subscription>/resourceGroups/ama/providers/Microsoft.Consumption/budgets?api-version=2023-05-01" \
  --query 'value[].name' -o json
```

Rebuild sequence:

1. Prepare non-secret deployment parameters: `workload=forward`,
   `environmentName=test`, both locations `uksouth`, `deploymentProfile=development`,
   the actual SQL Entra administrator/principal type, `enableApiAi=true`, Entra
   client ID, and the selected tile URL/attribution. In this subscription the
   tested models were `standard` / `gpt-4.1-mini` and `capable` / `gpt-4.1`, both
   version `2025-04-14`, `skuName=GlobalStandard`, capacity 30. Availability and
   quota must be rechecked, not assumed for another subscription.
2. Deploy with `deployApplications=false`. Use deployment outputs to discover
   the registry, SQL server, model endpoint and vault; do not guess hashed names.
3. Build a versioned `zava-forward-mvp` image with `az acr build` with the `src/` folder as build context (`-f src/api/Dockerfile src`). Provision
   `entra-client-secret` in the new vault through an authorised operator. RG
   Owner alone does not grant Key Vault data-plane access. Transfer a retained
   credential only through a private file or the provisioning script, not a
   command argument or tracked parameter file.
4. Run `create-sql-users.py` as the configured SQL Entra administrator. Seed
   through the [Azure SQL store instructions](../src/core/README.md#azure-sql-store)
   before exposing replicas. Retain the continuing synthetic stock/cases and
   privately restore any signed-in staff object-id mapping. The image contains
   no fixture; a new, empty SQL database is not equivalent to the previous MVP.
5. Deploy with `deployApplications=true` and the real `apiImage`, keeping the
   same non-secret parameters. An explicit transitional `entraRoleMap` can
   preserve existing tenant role values; it cannot update the registration.
6. Run [post-deployment authentication initialization](#post-deployment-api-authentication-initialization)
   against the retained registration, using an authorised isolated tenant
   profile. A new callback does not require a replacement client ID or secret.
   If enabling own-user photos, complete the separate
   [staged token-store setup](#public-welcome-and-microsoft-account-photos).
   Reconcile the private roster with the
   [staff initializer](#tenant-staff-and-application-role-initialization)
   after seeding, including its serving-replica restart and read-only check.
7. Wait for rollout, then check public `/healthz`, API 401 without credentials
   and browser redirection. Check SQL reads/writes and both model deployments
   from the API's own identity. Restart the actual revision and verify the
   audit writes persist. A template fallback or operator-only SQL test is not
   evidence of workload model/SQL access.

Both group deployments succeeded. The restored database has 980 cases, 443
open; the API identity read and appended audit entries; both model deployments
returned `source=ai`. Audit entries survived an actual application revision
restart. The initial health 503 cleared after cold image/auth-sidecar rollout;
subsequent health returned 200, unauthenticated API 401 and browser 302.
Worker jobs/apps still use placeholders and Decision 1 scoring is not thereby
implemented.

The owner subsequently confirmed working workbench sign-in and completed the
isolated provisioning login on 2026-10-12. A real initializer `--check` then
verified the retained callback, and the opt-in `--account-photo` merge and
read-only check succeeded. This separate provisioning profile has authority
for that registration; the deployment identity's directory rights were not
broadened. Later tenant-staff reconciliation and owner-reported sign-in are
recorded in the current handover above. Live user photo/consent, changed-account
acceptance, map acceptance and tenant naming/role transition remain distinct
checks, not established by CLI authentication.

## Validate locally

Use the complete offline commands in [Quality gates](#quality-gates), including
all Bicep entry points, compiled controls, mutation regressions and scoped ruff.

## IoT Hub (issue 140, ADR 0003 decision 6)

### Bounded existing-hub exercise (2026-10-29, Refs #140 #184 #137)

The owner approved paid B1/one unit after the UK South USD10/month cost check,
with at most USD5 additional through 2026-10-31. Inspection found the existing
`iot-cutover-test-rzsrg` already B1/one unit, two partitions and one-day retention.
Reuse it; do not create a second hub. Conservative attribution for three full
October days is USD10 / 31 * 3 = USD0.97. Reserve USD1 for hub attribution,
USD1 for shared metrics/bounded job and USD3 contingency. These are estimates,
not actual billed cost, enforced caps or approval beyond October31. No extra
fixed hub charge was introduced against the inspected baseline.

`iot-hub-live.bicepparam` is a separate, existing-development-hub reconciliation
profile. It is **not** an override for `main.bicep` or the production module.
It references the exact existing hub, verifies actual region/SKU/units, and
writes only its built-in `api-consumer` group and metrics-only
`to-log-analytics` setting. It does not PUT the hub, create a namespace/private
endpoint/budget/role or alter apps/jobs. The initial direct-PUT what-if proposed
deleting service-owned properties, so it was not applied. The narrowed what-if
showed only diagnostic log/metric reconciliation, with group NoChange.
Deployment `iot-live-140-private` succeeded; actual enabled resource logs = 0,
enabled metric categories = 1. Existing private attachment, fallback route,
identityNone, local-auth disabled and public-network Disabled were preserved.

```bash
az bicep build --file infra/modules/iothub.bicep --stdout >/dev/null
az bicep lint --file infra/modules/iothub.bicep
az bicep build --file infra/iot-hub-live.bicep --stdout >/dev/null
az bicep lint --file infra/iot-hub-live.bicep
az deployment group what-if -g ama --parameters infra/iot-hub-live.bicepparam
# Review exact child IDs and log/metric-only differences before any apply.
az deployment group create -g ama --name iot-live-140-private \
  --parameters infra/iot-hub-live.bicepparam --mode Incremental \
  --query properties.provisioningState -o tsv
```

The historical production definition below remains private/keyless and
source-only; this approval does not authorize its paid Event Hubs adapter,
endpoints or roles. The built-in group alone does not unblock Entra receive:
Microsoft's [Entra guidance](https://learn.microsoft.com/en-us/azure/iot-hub/authenticate-authorize-azure-ad),
checked 2026-10-29, still requires a shared service key there. Service SAS
remains disabled; no service key was retrieved.

Live device issue/send is parked, not completed: the authenticated operator has
only inherited Owner on the hub, not registry data permission. No device,
certificate, key file or temporary public-network change was created. Juan
Manuel Servera remains the exercise issue/rotate/revoke owner. The precise
owner decision is whether to authorize a hub-scoped **IoT Hub Registry
Contributor** grant to the selected operator and approve an actual reachable
device path. If approved separately, the owner (not this task) can run:

```bash
az role assignment create --assignee-object-id <approved-operator-object-id> \
  --assignee-principal-type User --role 'IoT Hub Registry Contributor' \
  --scope <existing-iot-cutover-test-rzsrg-resource-id>
```

Do not grant Data Contributor/Owner or a subscription-wide role as a shortcut.
API Event Hubs Data Receiver is already documented for the separate private
entity, but that entity does not exist, so no ineffective hub role was added.
Live-to-SQL and resident gauges remain unproved. Cloud activation needs separately
approved adapter cost/network/roles and an API revision invoking the consumer;
the existing finite callable does not run at startup. The resident SQL view
binds optional sensor tables only at its separately approved view apply, so
creating sensor tables later also needs view reconciliation, not merely a
browser refresh. No real-device or OD-43 approval follows.
Counts-only inspection via the existing in-VNet Manual initializer succeeded
on 2026-10-29: `sensor_reading`, `sensor_delivery` and
`sensor_data_quality_exception` are absent (availability false/count zero),
not existing empty tables. Two initial transient probes failed on driver setup;
the corrected execution completed without changing the job definition or SQL.
The installed driver is `mssql-python`: pass login `timeout=20` as a connect
argument, not the unsupported `Connection Timeout` connection-string property.
Forty-second process limits kept the counts probes finite. Actual disposable
local SQL Server passed 45 ingestion tests; no live Hub-to-SQL claim follows.

`modules/iothub.bicep` defines the device-to-cloud boundary for simulated
monitoring. The 2026-10-27 owner direction approves source authoring and local
validation within Free/B1, `ama` and the overall USD700 cap, **not deployment**.
Never delete resource group `ama`. No resource group, device, key, credential
rotation, live transport or Azure what-if is created/executed by this work.

| Item | Decision |
| --- | --- |
| Region and scope | `uksouth`, existing `ama` only. Named checks in main's parameter guard precede the entire main graph; a separate module guard protects standalone use. Independent SQL and global-resource locations are not changed |
| Tier and units | B1, exactly one unit, two partitions by default. S1 and scale-out are rejected by constraints. Free is not selected: its limited allowance and inability to upgrade are not a drop-in Basic profile. Twins, cloud-to-device and device management remain excluded |
| Retention | One day in the built-in transport endpoint and custom Event Hub, configurable 1-7 days. This is not SQL/DPO record retention; Azure SQL remains the record system |
| Consumer | `api-consumer` on `sensor-readings` in dedicated Standard Event Hubs namespace `eh-<hub-name>`, one TU, no auto-inflate. API identity gets only Azure Event Hubs Data Receiver on that event hub |
| Routing identity | IoT Hub system-assigned identity gets Data Sender on its dedicated namespace. All DeviceMessages route to the custom Event Hub when explicitly activated; built-in fallback is disabled |
| Service credentials | Local service auth disabled on both services; no service key lookup, value or connection string in Bicep/outputs. Disabled shared access does not prove provider-generated policies/keys do not exist |
| Network | Hub: public disabled by default, unconditional private endpoint and both IoT/servicebus DNS zones. Public hub access requires the existing explicit development profile opt-in. Namespace: always public Disabled, default Deny, unconditional private endpoint with servicebus DNS; trusted Microsoft services exception permits system-identity routing, still requiring sender RBAC. This is not IoT egress through its private endpoint |
| Diagnostics | `AllMetrics` to the supplied Log Analytics workspace on hub and namespace; `allLogs` explicitly disabled. Connections and DeviceIdentityOperations also contain device IDs, so excluding DeviceTelemetry alone is insufficient. No raw readings, device IDs or keys are intentionally exported. This does not erase historical logs or cover every external diagnostic setting |
| Device provisioning | Individual device-registry identities, one per simulated sensor/gateway, provisioned later under #185. Per-device symmetric SAS or X.509, never a shared service policy; device SAS remains enabled, module SAS disabled. DPS is deferred; disabling service SAS is not compatible with assuming DPS already works |
| Credential owner | Juan Manuel Servera is the selected exercise issue/rotate/revoke owner. Later #185 work must place credentials in the approved Key Vault, control access, record expiry/rotation and revoke compromised identities without logging values. No real operational appointment, key read/write or credential issuance is established here |

### Keyless consumer and explicit activation

The earlier receiver assignment on IoT Hub was ineffective: Microsoft says
the built-in Event Hubs-compatible endpoint still requires a shared access
key. The custom Event Hub is an Entra consumption adapter; it does not replace
IoT Hub's per-device boundary or implement the #110 consumer. Nonsecret main
outputs `iotHubEventHubNamespaceFqdn`, `iotHubEventHubName`,
`iotHubConsumerGroup` and `iotHubRoutingEnabled` describe its future contract.
The namespace output is a hostname without scheme, port or trailing slash,
including when Azure returns `https://<host>:443/`. The routing endpoint is
constructed separately as `sb://<host>/` from that same normalized hostname.

`iotHubRoutingReady=false` (default; module `routingReady`) is **bootstrap
only**: system identity, namespace, entity, group, roles and endpoints are
defined, but no custom routing endpoint is registered and no route/fallback
is active. Do not enrol devices or send messages in this state. A system
identity exists only after hub creation; registering its routing endpoint
before its sender grant has propagated can fail. The hub therefore does not
depend on its own downstream sender assignment, which would form a cycle.

Only a later separately authorized operator may apply bootstrap, verify actual
sender authorization/propagation, record that evidence, and then apply the same
definition with `iotHubRoutingReady=true`. Preserve true in every subsequent
private parameter set: omitting it reverts to bootstrap and disables routing.
Do not run the generic deployment pipeline for an activated hub without
reviewing its effective parameter set and what-if. No automatic apply/retry,
device provisioning, SDK activation or live propagation check runs here.

### Transport budget entry (2026-10-27)

The public [Azure Retail Prices API](https://prices.azure.com/api/retail/prices),
queried for `armRegionName eq 'uksouth'`, USD, Consumption, returned B1 Unit
USD10/month (product `IoT Hub`), Standard Throughput Unit USD0.03/hour and
Standard Ingress Events USD0.028/million (product `Event Hubs`). These are public
list-price estimates, not the subscription's actual offer, spend or headroom.

| Component | Monthly USD scenario |
| --- | --- |
| B1, one unit | 10.00 |
| Standard Event Hubs, one TU for 730 hours | 21.90 |
| Ingress, illustrative 400,000 events/day for 30 days, each <=64 KiB | 0.336 |
| Two private endpoints | 14.60 planning allowance, assuming USD0.01/endpoint-hour; not verified by the fetched regional price response |
| Shared DNS, metric ingestion, endpoint data processing and contingency | 13.164 planning allowance, not a measured usage/quote |
| Total planned transport allocation | 60.00/month, inside rather than additional to the overall USD700 cap |

The [Private Link pricing page](https://azure.microsoft.com/en-us/pricing/details/private-link/)
retrieved on 2026-10-27 returned currency placeholders, not a usable numeric
quote. Endpoint/variable allowances above are explicit modelling assumptions.
The ingress example is not a traffic forecast; IoT B1 metering uses 4 KiB
blocks, so larger observations reduce its daily observation capacity.
Peak throughput, December funding duration, billing-currency conversion,
current aggregate spend, commitments and remaining USD700 headroom must all be
checked before provisioning. USD60/month is not an approved extra purchase or
a claim the complete programme fits the cap. This authoring task spends zero
on Azure resources.

`iotHubMonthlyCost` / `monthlyCostEstimate` defaults to 60 in the actual
billing currency, constrained to 1-700; do not treat that number as USD unless
the account currency/conversion is reconciled. The dedicated monthly budget
filters hub, namespace and both endpoint resource IDs, with 80% actual and
100% forecast alerts. Shared workspace/DNS charges remain in the overall
budget. Azure budgets send alerts, **not hard spending stops**; this template
cannot enforce the aggregate cap.

### Acceptance and validation boundary

Build/lint are wired through the existing `mvp-validation.yml` check;
`infra/tests/test_iothub_module.py` now examines compiled resources, both
activation states and rejection mutations. The existing
`Infrastructure PR what-if` workflow checks trusted candidate Bicep through
approved plan environments in `ama`; its presence does not mean it ran.
This task uses local tests only, not the full RPI gate.

| #140 criterion | Authored evidence | Remaining evidence |
| --- | --- | --- |
| Tier, region, units, cost, retention | Decision table, constraints and budget scenario above | Actual price/currency/headroom and quota verification before provisioning |
| Hub, consumer/routing and diagnostics | Compiled Bicep and semantic/mutation tests | No actual routed message or Log Analytics arrival |
| API identity / no keys | Event-hub-scoped receiver, separate system sender, role matrix and key-auth guards | Actual #110 SDK/token transport |
| Production network | Both endpoints/DNS, disabled public namespace and trusted-service exception | Actual private resolution and access denial/success |
| Provisioning and owner | Individual identities and named exercise credential owner above | #185 implementation and actual issue/rotate/revoke evidence |
| Gates and cost entry | Local build/lint/infra tests, existing owner-gated what-if wiring, bounded budget definition | Live what-if not run/authorized; not whole-issue closure |

BRD OD-43 remains open for real inventory, lawful basis/DPIA, resident choice,
record retention, calibration, freshness/thresholds and human review ownership.
No operational monitoring or human approval follows from passing local checks.
Incremental deployment would not remove old role assignments/resources absent
from the new source; any live reconciliation needs separate exact-resource
authority, never resource-group deletion.

Official references, retrieved 2026-10-27:

* [IoT Hub Entra authorization and built-in-endpoint limitation](https://learn.microsoft.com/en-us/azure/iot-hub/authenticate-authorize-azure-ad)
* [Managed-identity routing and role propagation](https://learn.microsoft.com/en-us/azure/iot-hub/iot-hub-managed-identity)
* [IoT private networking](https://learn.microsoft.com/en-us/azure/iot-hub/virtual-network-support)
* [Event Hubs private access and trusted-service exception](https://learn.microsoft.com/en-us/azure/event-hubs/private-link-service)
* [Tier capabilities and metering](https://learn.microsoft.com/en-us/azure/iot-hub/iot-hub-scaling)
* [Monitoring log schemas, including device IDs](https://learn.microsoft.com/en-us/azure/iot-hub/monitor-iot-hub-reference)

## Private networking and public edge (issue 143, ADR 0002 decision 6)

Private-endpoint and DNS coverage per service (checked by `infra/tests/test_edge_module.py`, which parses each module's private endpoint calls and resolves their DNS zones against the zone list in `network.bicep`; any module with a public-access switch must have a private endpoint):

| Service | Private endpoint group | Private DNS zone |
|---|---|---|
| Azure SQL | `sqlServer` | `privatelink.database.windows.net` |
| Storage | `blob`, `queue` | `privatelink.blob...`, `privatelink.queue...` |
| Token-only auth storage | `blob` | `privatelink.blob...` |
| Key Vault | `vault` | `privatelink.vaultcore.azure.net` |
| Container Registry | `registry` | `privatelink.azurecr.io` |
| Foundry (Azure OpenAI) | `account` | `cognitiveservices`, `openai`, `services.ai` zones |
| IoT Hub | `iotHub` | `privatelink.azure-devices.net`, `privatelink.servicebus.windows.net` |
| Monitor (AMPLS) | `azuremonitor` | `monitor`, `oms`, `ods`, `agentsvc`, `blob` zones |
| Container Apps environment | Internal environment in the delegated subnet (no endpoint) | Environment DNS zone (`envDns.bicep`) |

Any new store must add a `privateEndpoint.bicep` call, a zone in `network.bicep`, and an entry in the test's coverage map.

Public edge: `enablePublicEdge=true` deploys `modules/edge.bicep` (Front Door Premium, WAF policy with the default and bot rule sets, Private Link origin to the internal environment, diagnostics to Log Analytics). The guard rejects it in the development profile or with `allowPublicNetworkAccess=true`, so development public access cannot be enabled together with the edge or in the production profile. After deployment an owner must approve the pending private endpoint connection on the Container Apps environment (Networking, Private endpoint connections). `edgeCustomDomain` adds a managed-certificate custom domain; the domain is attached to the route in the same deployment, but the managed certificate stays Pending until the owner creates the DNS validation TXT and CNAME records, so the custom host does not serve traffic before that; deploy without a domain first if that matters.

Open items for the edge (no production-profile deployment evidence yet): Private Link to the `managedEnvironments` group of an internal, VNet-injected Container Apps environment is unverified for this configuration, so do not rely on `enablePublicEdge` until a deployment shows the pending connection and a healthy origin; a live `az deployment group what-if` has not been run. The `entraRedirectUri` output is the callback URL to register (`infra/scripts/create-api-app-registration.sh -u https://<edge host>`), and the API sets the forward-proxy convention so sign-in callbacks use the edge host.

Open items (not verified here):

* Evidence for private-network claims must come from a production-profile deployment (uksouth, Azure only). This change was validated by `az bicep build`, lint and static tests only; no deployment ran. Record the deployment evidence before any claim.
* Confirm Front Door Premium Private Link support for Container Apps environments in uksouth and its current pricing at deployment time.
* Custom domain name and DNS ownership, and the pilot edge go/no-go, are owner decisions (ADR 0002 open: pilot network design).

## Resident AI accounting expiry (issue 624)

The resident AI exercise expiry is data: `resident_ai.budget.expires_at` (UTC, `DATETIME2(7)`),
read under the same lock as the cap by `resident_ai.reserve`, which refuses at or after it.
[`sql/resident-assistant.sql`](sql/resident-assistant.sql) adds the column idempotently with
default `2026-11-01T00:00:00`, so an already-deployed ledger keeps its counts and its live expiry.
Read it with `SELECT reserved_cents, expires_at FROM resident_ai.budget;`. Extending it, like
raising the 2000 cent cap, is an owner decision applied as one reviewed data change, for example
`UPDATE resident_ai.budget SET expires_at = '<new UTC instant>' WHERE id = 1;`; re-applying the
script never resets it. No extension is made by the code. The Python `EXPIRES` constant in
`resident_demo/assistant.py` is a second, independent gate and still ends the exercise at
`2026-11-01T00:00:00Z`; extend it in the same reviewed change.

## Synthetic resident showcase SQL boundary (issue 462)

[`sql/resident-showcase.sql`](sql/resident-showcase.sql) is the database side of the synthetic
resident showcase: schema `resident_showcase` (owned by `dbo`), an empty `allowed_case` table whose
window cannot end after the shared 2027-02-01T00:00:00Z cutoff (exclusive
serving end, through January 31 UTC), the view `v_resident_case` and the grants for one dedicated
read-only principal. The principal gets SELECT on the view only, no role membership, and explicit
DENY on `dbo.cases` and on writes, DDL and execute in the schema. SELECT is deliberately not denied at
schema scope because that would override the view grant.
[`scripts/resident_showcase_sql.py PRINCIPAL`](scripts/resident_showcase_sql.py) renders it as a dry
run. `--apply SERVER DATABASE` (and `--create-principal CLIENT_ID`) are for an approved private job
only; nothing here has been applied to Azure, no allowlist row is inserted, and no role, network or
Key Vault grant is made. The approved design names the existing vault `kv-cutovertest-rzsrg`, which
is not a retrieval path: no role or private network route exists for it yet. The cloud deployment
stays blocked on budget headroom proof and the human approvals recorded in the issue 462 tracking
files.

When the optional sensor tables exist but contain no matching readings, the
view returns `[]`, not SQL NULL, for `sensors_json`. Reapplying the view after
sensor-table initialization must verify this evaluated projection as well as
column shape and row counts; `SELECT TOP (0)` does not exercise empty history.
The real-SQL regression is
`test_resident_showcase_sql.SqlBoundaryTests.test_empty_sensor_tables_preserve_valid_empty_history`.

[`scripts/resident_demo_verifier.py`](scripts/resident_demo_verifier.py) is the owner-run offline
tool: it takes no arguments, needs an interactive terminal, reads the demo password twice with hidden
input and prints only the scrypt verifier (sensitive; keep it out of chat and git). It has no
network, Azure or vault access.

[`scripts/resident_demo_secrets.py`](scripts/resident_demo_secrets.py) is the owner-run secret
delivery helper for later use; it has not been run against Azure. It is a dry run by default (local
validation plus vault metadata only, no value sent); a dry run is not what-if proof, because the
what-if runs only under `--apply`. `--apply` writes exactly
`resident-demo-password-verifier` and `resident-demo-session-key` to `kv-cutovertest-rzsrg` in one
secure ARM deployment, only after a what-if proves two new secrets there, with an expiry no later
than the resident policy cap (2027-02-01T00:00:00Z; equality permitted for
configuration, serving ends exclusively then). The verifier comes from a hidden prompt or an owner-only 0600 file outside
the repository; the session key is generated at apply time and never printed. It is not an
authority: it needs a separate exact write approval, cleared budget and a proven private write
path, and Azure roles remain the enforcing control. A part-failed write is not cleaned up
automatically; reconcile it under a separate approval. The employee `credential_arm.store` name
allowlist is unchanged.

The resident demo app has its own template, `infra/resident-demo.bicep`, and command,
`scripts/resident_demo_deploy.py`. They never use `main.bicep` or `scripts/deploy.py`, so they
cannot change the main API's parameterized minimum, cron schedules or the event job. The template
creates only `id-resident-demo`, `ca-resident-demo` (0.25 vCPU, 0.5 GiB, minimum 0, maximum 1,
image by `@sha256:` digest in the fixed registry, Key Vault references without versions) and three
role assignments: Key Vault Secrets User on each of the two resident secrets, and AcrPull on the
registry. It sets the full runtime contract (`ZF_DEMO_*`, `ZF_SQL_*` with managed identity,
`PORT`) and a scope guard that refuses outside `ama` or an expiry after the shared policy cap.
The Owner ARM secret write needs no extra Key Vault writer role; that path is still unproven
against the private vault, and no broader role is proposed.

The command is a dry run by default: it runs a what-if and refuses unless every actionable change
is one of those five resources or the exact nested guard deployment `resident-demo-scope`; no other
deployment is accepted, and an unverified nested what-if shape is refused. `--apply` repeats it, asks for a typed phrase, deploys, and reads
back minimum 0 and maximum 1. It is not an authority; it needs a separate approval and a cleared
cost and headroom check. Stop conditions (all UTC): any minimum replica above 0, a new schedule or
event, an unexpected resource type, daily `ama` cost well above baseline, or time reaching
the configured expiry. Rollback is a rerun with `--no-ingress`; after expiry, confirm no active
revision serves traffic. The template default is public ingress, so the first operational stage must pass `--no-ingress`
until the private-vault and SQL proofs exist. None of this has been validated live: tests use a
fake CLI and the compiled template only. Image builds, logs and egress costs are not estimated here.

## Resident Azure OpenAI (#469)

`resident-assistant.bicep` is standalone and defaults `enabled=false`. It never
deploys the resident app, changes ingress or creates identity/group/storage
resources. Only RG `ama` is active. The explicit `enabled=true` deployment
creates `aoai-resident-469` in Sweden Central, `resident-mini` with
gpt-4.1-mini 2025-04-14 / Standard / capacity 1, and one account-scoped
Cognitive Services OpenAI User assignment for existing `id-resident-demo`.
Local auth and dynamic throttling are disabled; model auto-upgrade is disabled.
No production template imports or enables this resource.

The 2026-10-27 actual deployment `resident-assistant-469` succeeded with these
three resources only. Its role assignment suffix is
`59b49580-bbf9-53d5-80eb-a389ac963e52`; no test resources were created.
The resident revision remained `ca-resident-demo--0000002`; its reachable
`/healthz` returned HTTP200, which does not establish new model activation.

Before enabling the new runtime, an authorised existing Entra SQL administrator
must review and apply `sql/resident-assistant.sql` in the existing database:

```bash
python3 infra/scripts/resident_assistant_sql.py id-resident-demo \
  --client-id <existing-resident-client-id>
# Above is dry-run only. On the existing authorised private SQL host, add:
# --apply sql-cutover-test-rzsrg retrofit
```

The helper verifies the existing identity SID and narrow rights before and after;
it creates no user/role and uses no key/password. It adds only two exact SQL
object EXECUTEs in a separate accounting schema. The original resident-view
SELECT and case-write/DDL denials remain. Reruns preserve spend; never reset
or delete the budget/attempt tables to reopen allowance. Missing ledger rows
fail closed. SQL UTC time and one locked global budget row protect the hard
USD20 ceiling and five-attempt rolling-hour per-resident limit.

Then deploy the reviewed resident image through the existing rollout gate,
preserving all ingress, secret references and min0/max1 settings, and explicitly
set the namespaced assistant settings in the [API guide](../src/api/README.md#resident-advisory-assistant-prototype-469).
No app rollout, SQL migration or authenticated MI inference is implied by
account provisioning. Rollback is `ZF_DEMO_ASSISTANT_ENABLED=false`; retain
the ledger. Never use developer-token inference as a managed-identity smoke
substitute or run an unmetered diagnostic request.

If a consented question returns "AI unavailable: the AI usage check is
unavailable", the ledger may be missing or unreachable, or the identity may lack
permission on its procedures (permission errors map to the same label). Before
applying any schema, run a read-only check of the ledger objects, connectivity,
authentication and procedure permissions. On 2026-10-31 it was found absent (see `.copilot-tracking/research/2026-10-31/resident-ai-activation-563b-research.md`).
The SQL is private, so it was applied by one run of the existing Manual
`job-cutover-test-init` job (its Entra admin identity) with a command override
that restates the SQL environment variables; the job template stays unchanged.
Check `resident_ai.reserve` exists before any activation.

See the [design/cost envelope](../docs/architecture/resident-assistant-prototype.md).
The USD20 ceiling is application-controlled inference admission, not an Azure
budget alert or subscription-wide spending guarantee. Funding through December
does not itself extend resident access or the independent inference cutoff.
The later #521 source renewal below does not renew paid-inference authority.

### Renewed resident feedback window (2026-10-27, Refs #462, #466)

The owner superseded the October-only test window: public feedback access is
authorized through `2026-12-31T23:59:00Z`, within USD30 additional resident spend
inside the renewed USD700 `ama` cap through December31. This supersedes the
historical staging/closure language above, not production identity acceptance.
At that dated baseline the single source of the maximum expiry was
[`resident-demo.json`](../src/core/src/zava_forward/core/resident-demo.json):
`2026-12-31T23:59:59Z` inclusive. Bicep loads it at compilation; the packaged
runtime and secret/deploy helpers use the same value. Configured expiry is still
exclusive for serving: startup and requests fail closed at/after that instant.
The 1000-mapping refusal remains. The optional model provider's separate
authority is not extended; the deterministic assistant remains available.

Deploy only through the resident Bicep helper, with an immutable rebuilt digest:

```bash
python3 infra/scripts/resident_demo_deploy.py \
  --subscription <approved-subscription> \
  --expires 2026-12-31T23:59:00Z \
  --image crcutovertestrzsrg.azurecr.io/zava-resident-demo@sha256:<digest> \
  --sql-server sql-cutover-test-rzsrg.database.windows.net \
  --sql-database retrofit --apply
```

Default `externalIngress=true` is intentional. Leave ingress open and the revision
active for owner testing and the November demonstration; do not install a closure
watchdog or use an imperative app update. Keep min0/max1 and all other app minima0
and eight jobs Manual. Idle replicas scale to zero; the first request can have a
cold-start delay and may need a retry. Scale-to-zero is not a monetary cap:
monitor actual/delayed charges and stop before the USD30 allowance is exhausted.

The owner signs in with an admitted synthetic `@example.com` resident email and
the existing owner-held shared password. Any arbitrary email is not admitted.
No credential is retrieved or printed by this deployment helper.
Authenticated isolation, gauges/history, assistant, top-right logout and genuine
1800-second expiry must be verified by the owner when the password is unavailable
to the operator; anonymous denials and local fixtures are not substitutes.

Important independent expiry boundaries: the existing SQL allowlist constraint
and row windows retain their original November1 limit. Existing vault-secret
validity is not changed by an app deployment. This records the historical
pre-#521 source/live mismatch. December ingress therefore does
not prove December resident-data access. Renewing SQL authorizations or secret
metadata requires a separately approved owner/private operation; this change
does not mutate SQL rows, permissions or secrets. Preserve these limits in any
demonstration-readiness claim. Never delete resource group `ama`.

### January authority source renewal (2026-10-28, Refs #521)

The owner requested resident demo access through January 31, 2027 UTC.
The shared [`resident-demo.json`](../src/core/src/zava_forward/core/resident-demo.json)
now sets `maximum_expiry_utc` to `2027-02-01T00:00:00Z`.
`resident_showcase.AUTHORITY_END`, the secret/deploy helpers and Bicep use
that policy. A configured expiry may equal it; startup, requests, sessions
and row admission refuse at or after the instant. Earlier configured expiries,
revoked rows and shorter row windows still deny access.

The SQL file is a template: render it with `resident_showcase_sql.py`, not
direct SQL-file execution. The renderer substitutes the same UTC policy cap.
Reapply transactionally replaces `ck_allowed_case_window` using `WITH CHECK`,
retaining `valid_to > valid_from` and checking existing data. Failure rolls
back the replacement and rethrows. It does not extend any row window, insert
residents or change the original principal/grant/deny design. The allowlist
remains synthetic, approved, provenance-bearing and capped at 1000 in the app.
The independent model tariff and SQL inference admission cutoff are unchanged.

Local source validation on 2026-10-30 passed the 78 domain/rendering tests
(27 SQL opt-in skips), all 27 separately executed disposable SQL Server tests
(zero skips), the 32 fake-CLI helper tests, and the 1380-test API discovery
(320 opt-in integration skips). API/core Ruff, formatting and mypy passed.
SQL evidence includes migration from the old November constraint, trusted
reapplication, preserved rows/rights and failed-migration rollback. Targeted
infra static checks retain independently reproduced pre-existing lint,
formatting and typing findings; they are not reported as passing.
These local results do not prove live renewal, actual cost headroom,
operational approval or a complete exact-head publication gate.

#### Credential and SQL access rotation plan

Status: source plan only; independent technical review and owner operational
approval remain required. Live credential rotation and SQL renewal are **Pending**.
Juan Manuel Servera remains the exercise credential issue/rotate/revoke owner.
No secret or private dataset was read, generated, printed or stored for #521.

1. Before an owner-approved session, check only app/vault/SQL identity and
   expiry metadata through the existing private path. Record exact resource
   scopes, current SID, view-only SELECT, existing denies, no role membership,
   app image/configuration and approved synthetic row count/window. Verify
   expiry alerts and private access without opening a network path or adding
   RBAC. Unknown or incompatible metadata stops the operation.
2. Obtain separate exact approval for any credential write. Use an owner-held
   password-manager random password, hidden local verifier generation and a
   fresh signing key; never put values in command arguments, chat, logs, git
   or environment dumps. Set both expiries no later than the new cap and
   alert seven days before expiry. Rotate before demonstration, on suspected
   disclosure, and at least every 30 days during the extended window.
   The existing helper deliberately accepts only two new-secret Create
   changes and refuses Modify; it is **not an existing-secret rotation tool**.
   A separately reviewed, explicitly approved exact-version write operation
   is required for existing names. Do not weaken that helper or add writer
   roles to make rotation work.
3. Keep the prior credential versions available only for a bounded, approved
   rollback interval. Refresh the existing versionless references/revision
   using the approved resident rollout path; account for up to 30 minutes
   reference refresh. Signing-key rotation/restart invalidates all sessions.
   Verify owner sign-in, cross-case denial, logout and 1800-second expiry
   without operator password access. Disable superseded secret versions only
   after successful verification, and record metadata/operator/time, not values.
   On failure disable ingress under separate rollback approval and stop;
   never silently restore credentials that were rotated for compromise.
4. SQL managed identity needs no password rotation. Revalidate its existing
   SID and narrow rights before and after the approved private SQL migration.
   Renew **only individually approved existing synthetic allowlist rows**,
   retaining provenance/revocation and `valid_from < valid_to <=` the shared
   cap. Never mass-extend all rows, clear revocations, create users/roles,
   broaden SELECT, or infer works consent from demo admission. Identity
   replacement, if ever necessary, is a separate approval, not this renewal.
5. At or before the configured end, verify requests and sessions deny access,
   approved row windows and secrets expire, and no active revision serves
   resident traffic. Any network/permission change, min replica above zero,
   scope mismatch, unknown cost or failed isolation check stops the operation.

#### Coordinator steps after the 2026-11-01 expiry (Refs #521)

Nothing here is applied by the repository change. The resident app refuses to
start once the live allowlist view admits no row, because rows and the live
`ck_allowed_case_window` still carry the earlier 2026-11-01 end. After the
owner confirms the exact change and the cost check above passes:

1. Re-render and apply the boundary so the check constraint moves to
   `2027-02-01T00:00:00` (never touches row windows or permissions):
   `python3 infra/scripts/resident_showcase_sql.py <principal> --client-id <existing resident managed identity client id> --apply <server> <database>`
   (without `--create-principal`; the script exits with code 2 if neither is given).
2. Renew only individually approved synthetic rows, one reviewed statement each,
   with `valid_to` no later than `2027-02-01T00:00:00`:
   `UPDATE resident_showcase.allowed_case SET valid_to = '2027-02-01T00:00:00' WHERE case_id = '<approved id>' AND revoked = 0;`
3. Redeploy only a validated image digest built after #590, whose packaged
   `resident-demo.json` carries the January 2027 policy (an older image still
   caps authority at November and the app rejects the later expiry). Rebuild
   through the approved image path if necessary and record the digest check.
   Use the extended expiry (what-if first, then
   `--apply`): `python3 infra/scripts/resident_demo_deploy.py --subscription <id>
   --expires 2027-01-31T23:59:59Z --image <repo>@sha256:<digest> --sql-server <fqdn>
   --sql-database <db> [--apply]`. Rotate credentials per step 2 above first.
4. Verify startup, sign-in, cross-case denial and min replicas 0; record
   metadata only, no secret values.

The AI tariff/budget expiry (`assistant.py` `EXPIRES`, `resident_ai.budget`)
is a separate owner approval and is deliberately unchanged here.

#### Added-cost estimate and USD700 cap

Source-only #521 actions add **USD0** Azure spend and zero resources/roles.
That is not a claim that existing idle resources are free: SQL, registry,
private endpoints, retained logs/storage and delayed billing can accrue charges.
No live billing, rates or headroom was queried.

For planning only, use the historical USD30 additional resident envelope for
November-December as a two-month proxy: USD15 per 30-day month, or USD0.50/day.
Relative to the issue's original November 1 cutoff, the extra 92 days
(November 30 + December 31 + January 31) model **USD46**; relative to the
already-renewed December source baseline, January's extra 31 days model
**USD15.50**. These overlap and must not be added together. Add a planning
reserve of USD10: **USD56** versus original October-only access, or **USD25.50**
for January only. This is an assumption-labelled envelope, not a quoted tariff,
measured forecast, new allowance or funding approval. It assumes the same
min0/max1 0.25 vCPU/0.5 GiB synthetic resident workload and no extra resources,
network paths, paid model calls or build/egress/logging increase. Re-estimate
those items explicitly if the approved operation needs them; do not hide them
inside zero-replica assumptions.

The overall **USD700 all-in `ama` cap is unchanged** and the historical USD30
resident allocation is inside it, not additional. Prior funding through
December does not establish January funding or available headroom.
Before **any paid action**, the owner must record actual accrued and delayed/
unbilled charges, outside-group liabilities, existing commitments, remaining
resource costs through the proposed end, new operation/build/egress/logging
cost and reserve in USD. Require their non-overlapping sum <= USD700 and
the proposed increment within an explicitly approved resident allocation.
If January-only incremental cost plus reserve is USD25.50, the other all-in
liabilities must be <= USD674.50; neither amount is known to be available.
Unknown/insufficient headroom, stale estimates or unapproved funding blocks
the operation. Monitor charges during the window and stop before either
the resident allocation or group cap is exhausted.

#### Separate live apply

**Pending owner confirmation; not performed.** Present the exact reviewed
image digest/configuration expiry, SQL constraint/row set, credential-version
operations, bounded refresh/verification/rollback interval and cost evidence
for a separate owner decision. Preserve min0/max1, synthetic resident-only
scope, private SQL/vault paths, narrow identity rights and all existing
approvals. No resource/role/network addition or Azure command is part of this
source-only change. Record the eventual approved apply and live verification
as separate evidence; do not close #521 based on source tests alone.
