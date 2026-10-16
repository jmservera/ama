---
title: Azure Infrastructure (Bicep)
description: Bicep deployment of the proposed Zava Forward demonstrator Azure architecture
author: AMA programme
ms.date: 2026-10-16
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
* `scripts/initialize-api-auth.py`: post-deployment callback synchronization for an existing API registration, without replacing roles, assignments or credentials.
* `scripts/initialize-workbench-staff.py`: private tenant-member/app-role/SQL binding reconciliation, with idempotent checks and serving-replica restart.
* `scripts/configure-m365-provisioner-app.sh`: delegated Graph permissions for the app the m365 CLI uses to set up SharePoint and Teams.
* `scripts/grant-sharepoint-access.sh`: optional Graph `Sites.Selected` grant for the SharePoint evidence store.
* `scripts/deploy.py`: image-preserving infrastructure what-if/deploy wrapper; see [Orchestrator image selection](#orchestrator-image-selection-322).
* `scripts/private-cutover-proof.py`, `cutover-proof.Dockerfile`: bounded
  synthetic SQL/private-ingress proof executed inside the ama VNet.

Optional parameters: `teamsWebhookUrl`, `evidenceStore`, `sharePointSiteId`, `monthlyBudget`. See the M365 section of the ADR.

## Deploy

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
warned). An empty option uses normal resolution. The wrapper owns the image
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
`ama`. It builds all four source images from the same immutable workflow SHA.
Every image passes the existing non-root/hardened/plain startup contract and
the same `src/trivy.yaml` fixable HIGH/CRITICAL gate as source CI; full reports
including unfixed findings are retained even on gate failure. Only passing
images leave the unprivileged hosted build job. Private publish jobs load
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
staff and token-store initialization remain separate human-controlled tasks.

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
| Approval and environment parameter sets | Same template/examples, environment configuration guard and approval boundaries implemented; actual reviewer rules/approval and pilot ownership/region unverified |
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
az acr build -g ama -r <registry> -f infra/cutover-proof.Dockerfile \
  --build-arg API_IMAGE=<registry-server>/zava-forward-api@sha256:<digest> \
  -t zava-forward-cutover-proof:<unique-tag> infra
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
  --parameter alertEmail=<approved-mailbox> --parameter 'modelDeployments=[]' \
  --parameter regionCheckReference=<reviewed-region-record> \
  --parameter quotaCheckReference=<reviewed-quota-record>
# Repeat with --apply only after reviewing the what-if.
```

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

## Environments

Refs #137. The same template/commit supports dev, test and pilot using the
following secret-free examples. Replace every `PLACEHOLDER` in a private,
untracked parameter file kept alongside `main.bicep` so its relative `using`
path resolves; never commit the completed file. Do not store secrets there:
secure inputs use the approved secret-management path.

Current owner direction (2026-10-16) leaves pilot region and subscription
ownership **open**. It supersedes the 2026-10-15 issue comment for this task;
no previous region or ownership claim is deployment authority. Pilot locations
are empty placeholders, not `uksouth` defaults. The `ownerTag` default identifies
the synthetic exercise resource contact, not the pilot subscription owner.

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
| Service SKUs | IoT Hub `B1`/1 unit; SQL `GP_S_Gen5`/2 max vCores; Log Analytics `PerGB2018`; registry Premium; Foundry `S0`; Container Apps Consumption | same | same; not a pilot sizing approval |
| Model SKU/quota inputs (`modelDeployments`) | `standard`: gpt-4.1-mini; `capable`: gpt-4.1; both version 2025-04-14, `GlobalStandard`, capacity 30 | same defaults, subject to checks | same defaults, unverified until region/subscription selected |
| Retention (fixed unless a documented module input exists) | Log Analytics 90 days; SQL PITR 14 days; blob/container soft delete 30 days; ACR 30 days; audit/digest immutability 365 days unlocked; IoT 1 day | same | same; not a legally approved retention schedule |
| `location` and `sqlLocation` | `uksouth` candidate, recheck | `uksouth` candidate, recheck | empty PLACEHOLDERs, owner decisions |
| `regionCheckReference`, `quotaCheckReference` | empty PLACEHOLDERs | empty PLACEHOLDERs | empty PLACEHOLDERs |
| Deployable as committed | No: complete placeholders/checks privately | No: complete placeholders/checks privately | No: additionally requires pilot decisions |

Rules:

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
| Zone redundancy support and quota in the owner-selected pilot regions/subscription | Not yet checked: open decisions | none |
| Pilot subscription quota for Container Apps cores and model capacity | Not yet checked: open item | none |

Historical rows above are discovery evidence, not current checks for another
subscription or configuration. No fresh Azure check was run for this offline
change. Before what-if/apply, the owner records a dated result/reference for:
Container Apps regional/zone availability and managed-environment core quota
(`az containerapp list-usages --location <region>`); SQL regional provisioning,
the selected SKU and zone support; IoT SKU/units; and each model/version,
deployment SKU and capacity (`az cognitiveservices model list --location
<region>` and `az cognitiveservices usage list --location <region>`).
Use the relevant provider's capability/quota surfaces, not VM SKU results as
proof for these services. Record requested/available quantities, zone support,
reviewer, date and pass/blocked outcome with the exact configuration. Keep
actual identifiers and raw account output private. Cost authorization and
pilot subscription ownership remain human decisions, not agent approvals.

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
infra-test steps install the test-only `PyYAML==6.0.3` pin before discovery;
it is not a production package dependency. All existing job/check names remain
unchanged, following the #321 cut-over decision. The workflow regression tests
reject missing, unpinned or late installation without skipping pipeline controls.

```bash
python3 -m pip install --no-deps -e src/core -e src/agents -e src/api -e src/orchestrator
python3 -m pip install 'PyYAML==6.0.3'
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
`pip install -e src/core -e src/agents -e src/api`, then run
`python -m unittest discover -s infra/tests -q`. Without the explicit test
prerequisite, discovery fails with `ModuleNotFoundError: No module named 'yaml'`.
Install `python -m pip install 'PyYAML==6.0.3'` in that same venv and rerun
the identical discovery command. This is intentional test setup, not a reason
to add PyYAML to the application packages.

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
exercise Juan Manuel Servera is the Legal, Compliance and DPO owner. Current
direction (2026-10-16) leaves pilot region and subscription ownership open,
superseding the older selection; resource contacts below do not settle those
decisions. Agents retrieve, compare, summarize and flag only. Rule activation,
consent, safety, legal interpretation and financial commitments require named
human approval; ADR 0005 is accepted for synthetic development only, with real
owners and sources still a gap before operational reliance.

| Control | Where | Decision | Owner | Cost |
| --- | --- | --- | --- | --- |
| Azure Policy assignments (SQL and storage public access, Key Vault deletion protection, required tags) | [`governance.bicep`](./governance.bicep), subscription scope, deployed separately by the subscription owner | Built-in definitions, audit only (`enforcementMode=DoNotEnforce`): policy reports non-compliance but blocks nothing; a Deny stance is an open owner decision | Juan Manuel Servera | No charge for Azure Policy |
| Defender for Cloud plans (Storage, SQL servers, Key Vaults, Containers) | [`governance.bicep`](./governance.bicep) | No pricing resource is submitted until the owner accepts a cost and sets `enableDefenderPlans=true`; then the four plans request Standard. Existing paid or Free subscription plans are preserved when disabled | Juan Manuel Servera | Per-resource pricing, not yet estimated: open item, confirm in the Azure pricing calculator before enabling |
| Resource locks | `enableLocks` in `main.bicep` (Key Vault, SQL, storage) | [`main.pilot.example.bicepparam`](./main.pilot.example.bicepparam) (a non-deployable example with placeholders; copy it to a private file and fill every value) sets `true`; the development file keeps `false` so the stack can be reset | Juan Manuel Servera | None |
| Tagging standard | `allTags` in `main.bicep` | Required tags on taggable resources, component refinements and untaggable-child exceptions documented in Environments; group tags remain separate | Juan Manuel Servera (exercise resource contact) | None |
| Known exceptions | [`policy-exceptions.json`](./policy-exceptions.json) | EX-001: `SecurityControl=Ignore` on the development resource group (MCAPS SQL public-access policy); expires 2026-12-31 | Juan Manuel Servera | None |

```bash
az deployment sub what-if -l uksouth -f infra/governance.bicep
az deployment sub create -l uksouth -f infra/governance.bicep
```

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

## Hardened source image rollout (#118)

Refs #118. All six application containers are defined in
[`modules/containerapps.bicep`](./modules/containerapps.bicep): API, agents,
orchestrator, import, token renewal and ledger verification. Compiled tests
verify each image parameter, API health probes and 2-4 replicas, plus the
default-off Premium Front Door/WAF/Private Link edge. Maintenance jobs retain
their direct Python module commands; no guard-bearing image path is required.
Worker transport remains #144; a Bicep resource is not worker acceptance.

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
| api | Key Vault Secrets User; blob Data Contributor; queue Message Sender; AcrPull; OpenAI User and Azure AI User (only when `enableApiAi`); IoT Hub Event Hubs Data Receiver; SQL reader, writer, ddladmin | Serve the workbench, enqueue tasks, read telemetry |
| agents | queue Data Contributor; AcrPull; OpenAI User and Azure AI User; no SQL | Run agents, reach data only through the API |
| orchestrator | queue Message Sender; AcrPull; no SQL | Enqueue only |
| import | blob and queue Data Contributor; AcrPull; SQL reader and writer | Imports |
| token-maintenance | Blob Delegator (account); blob Data Contributor (container); Secrets Officer (one secret); AcrPull | Renew the short-lived SAS |

Chat and memory store (ADR 0004, accepted by the owner 2026-10-15): no Bicep resource exists yet. When added it gets one data-plane role for the api identity, local auth disabled, and a new matrix row.

Entra registration: [entra/app-registration.json](entra/app-registration.json) is the declarative record (audience, callback, eight app roles mapped to the MVP personas, assignment required). `create-api-app-registration.sh` applies the registration idempotently but does not read the manifest: a test only keeps manifest, script app roles and `DEFAULT_ROLE_MAP` identical, and callback hostnames are supplied with `-u` at run time. Reproducibility (criterion 4) is therefore met by explicit manual steps and a named owner, not declaratively. Existing sign-in, picture and user switching are unchanged. Owner of the manual steps: Juan Manuel Servera (subscription owner; tenant ownership unconfirmed).

Open items:

* Owner sign-off of the matrix review (reviewer line is pending).
* Contractor B2B guest model (ADR 0002, #116) is proposed, not confirmed; tenant guest and cross-tenant policy are manual tenant steps.
* Drop `db_ddladmin` from the api identity after schema migration moves out of app start.
* Live `az role assignment list` comparison against a deployed group was not run here.

## Regulatory assistant capability roles (#217)

The Entra registration manifest keeps auxiliary `capabilityRoles` separate from
the mutually exclusive staff `appRoles`. The registration script declares all
three: `ZavaForward.RuleAuthor`, `ZavaForward.RuleOwner` and
`ZavaForward.RegulatoryChat`. These supplement, never replace, one staff role.
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
| `entra-client-secret` | 180 days | 30 days | Platform operator, named person open |
| `entra-token-store-sas` | 1 day (renewal job) | 3 days | Platform operator, named person open |

Expiry alerting: the vault diagnostic setting sends all logs to Log Analytics, and `modules/keyvault.bicep` adds a scheduled query alert on `SecretNearExpiryEventGridNotification` and `SecretExpiredEventGridNotification` (logged whether or not an Event Grid subscription exists) routed to the operations action group. A second alert fires on repeated 401/403 data-plane results. Every secret must carry an `--expires` date or the alert cannot fire; `check` reports secrets with no expiry.

### Rotate the Entra client secret

Run `secret_lifecycle.py rotation-plan --vault <vault> --app-id <id>`. The order gives no downtime: append a new app credential (the old stays valid), write it as a new version of `entra-client-secret` with an expiry, let the versionless Container Apps reference refresh (up to 30 minutes) or restart the active revision, verify sign-in, then delete the old credential. Do not delete first. The repeatable scripted step is `create-api-app-registration.sh -v <vault>`; add an `--end-date` when setting the secret.

### Access review

Quarterly (`reviewIntervalDays` 90), export `az role assignment list --scope <vault id> --include-inherited -o json` and run `secret_lifecycle.py review --assignments roles.json --reviewer <name>`. A named human sets each pending decision to keep or remove and the signed record is kept with the operations evidence. Owner alone gives no data-plane access.

### Open items

* Named owners for each secret and for the review.
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

Existing `MVP CI` / `MVP validation` names and job/check IDs remain unchanged.
The issue #200 owner decision (2026-10-15) retains them through cut-over; later
naming and branch-protection changes remain one deliberate owner-directed PR.
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

An environment rebuild changes the ingress FQDN even when the API registration
is retained. After the protected API has been deployed, initialize its callback:

```bash
python3 infra/scripts/initialize-api-auth.py \
  -g ama -n ca-forward-test-api --login
```

The deployment operator discovers the tenant, current FQDN and configured client
ID. Explicit `--login` starts tenant-scoped device-code authentication in a
separate private Azure CLI profile, by default
`$AZURE_CONFIG_DIR/zava-entra-init` (or `~/.azure/zava-entra-init` when unset).
Complete it as an authorised registration owner or administrator. This does
not overwrite the deployment identity or grant tenant permissions to it.
Keep the profile outside the repository: it contains authentication material.

Subsequent initialization runs omit `--login`. Use `--tenant-profile <directory>`
to select an existing Graph-authorised provisioning profile. Verify without
changing the registration:

```bash
python3 infra/scripts/initialize-api-auth.py \
  -g ama -n ca-forward-test-api --check
```

The command validates tenant/client identity and enabled ingress authentication,
then reads the existing registration by client ID. It adds the current callback
to `web.redirectUris` only if missing, preserves prior redirects, and verifies
the update. Reruns do not patch an already initialized registration. Missing
callbacks in check-only mode, permission denial and unverifiable updates exit
nonzero. The command does not change display names, roles, assignments or
secrets. The existing creation helper is for first-time registration and role
provisioning, not a callback-only repair.

### Tenant staff and application-role initialization

An enterprise-app role assignment alone is not enough. The workbench also
requires an internal staff record bound to the person's Entra object id. A
valid role with no matching staff `oid` produces `Account not authorised`;
email fallback remains disabled. SQL staff is cached at startup, so completing
the binding also requires reloading the API replicas.

Use `scripts/initialize-workbench-staff.py` after callback initialization and
SQL seeding. Its private JSON roster is an array of `code`/`userId` objects:
include every existing staff code, with a distinct enabled tenant member for
each. The current fixture needs ten internal positions; one additional
Contractor makes eleven people covering all eight role kinds. New Contractor
entries also require `"role": "Contractor"` and `"contractor"` naming an
existing case supplier. Room, desk and workspace accounts are rejected.

Keep the roster outside the repository with file mode 0600 and parent-directory
mode 0700, for example `~/.azure/zava-forward-staff/roster.json`. The initializer
resolves current names/UPNs from Graph; do not put directory names, UPNs or ids
in committed examples. Title/group-based allocation is illustrative exercise
coherence, not evidence of professional competence or delegated authority.

```bash
python3 infra/scripts/initialize-workbench-staff.py \
  --resource-group ama --container-app ca-forward-test-api \
  --roster "$HOME/.azure/zava-forward-staff/roster.json" --check
python3 infra/scripts/initialize-workbench-staff.py \
  --resource-group ama --container-app ca-forward-test-api \
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

### Public welcome and Microsoft account photos

The existing registration is retained. Add only delegated own-user Graph
`User.Read` with the same isolated provisioning profile:

```bash
python3 infra/scripts/initialize-api-auth.py \
  -g ama -n ca-forward-test-api --account-photo
python3 infra/scripts/initialize-api-auth.py \
  -g ama -n ca-forward-test-api --account-photo --check
```

This opt-in flag merges `User.Read` into existing requested permissions,
preserving all previous permissions/redirects. It does not grant administrator
consent, change roles, rotate credentials or request app-only
`ProfilePhoto.Read.All`. Users complete normal Microsoft sign-in/MFA/consent;
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
az containerapp logs show -g ama -n ca-forward-test-api \
  --type console --tail 50
```

Use the resource-specific `ContainerAppConsoleLogs` table, not the legacy
`ContainerAppConsoleLogs_CL`. Allow ingestion delay and query fixed events
instead of publishing raw platform logs:

```kusto
ContainerAppConsoleLogs
| where TimeGenerated > ago(1h)
| where ContainerAppName == "ca-forward-test-api"
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

`modules/iothub.bicep` provisions the device-to-cloud ingestion boundary for simulated in-use monitoring. Decisions recorded here are proposals pending owner approval of ADR 0003.

| Item | Decision |
| --- | --- |
| Region | uksouth (owner decision) |
| Tier and units | B1, 1 unit: device-to-cloud and message routing only, enough for the simulator. Move to S1 (parameter `iotHubSku`) only if twins, cloud-to-device or IoT Edge are needed |
| Cost | Estimate of 25 per month in the billing currency, set as a hub-scoped budget (`iotHubMonthlyCost`) with 80 percent actual and 100 percent forecast alerts. An estimate: confirm against the Azure pricing page before provisioning |
| Retention | Built-in endpoint keeps messages 1 day (`iotHubRetentionDays`, maximum 7). Azure SQL is the system of record |
| Consumer | Consumer group `api-consumer` on the built-in endpoint; the API managed identity has only Azure Event Hubs Data Receiver on the hub |
| Service credentials | `disableLocalAuth` is true: no shared access policy or connection string exists, so none can be stored in source or logs |
| Network | Production profile: public access disabled, private endpoint with `privatelink.azure-devices.net` and `privatelink.servicebus.windows.net`. Development profile: public access allowed for a throwaway stack |
| Diagnostics | Connections, DeviceIdentityOperations, Routes, Configurations and metrics to Log Analytics. DeviceTelemetry is not logged, keeping readings and device ids out of logs |
| Device identity | Individual device identities with per-device keys or X.509 certificates, issued by the simulator provisioning step (#185). Device Provisioning Service is deferred until real sensors are in scope |
| Credential owner | Juan Manuel Servera issues and rotates device credentials (owner decision); device keys are held in Key Vault, never in source |

Gates: `az bicep build` and `az bicep lint` run in `mvp-validation.yml`; `infra/tests/test_iothub_module.py` guards the module. Open: a live `az deployment group what-if` against the target resource group needs subscription access and has not been run; real pricing confirmation; B1 private endpoint behaviour verified in a deployment.

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
