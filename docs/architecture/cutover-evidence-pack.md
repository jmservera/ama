---
title: Source cut-over evidence pack
description: Dated parity, local validation, Azure build and failed deployment evidence for owner review of issues 200 and 201
ms.date: 2026-10-16
ms.topic: reference
---

## Decision and Scope

Refs #200. Refs #201. Evidence prepared on 2026-10-16 against base
`aedd616ffff8abfcf0379a538b895e4427147c8f`, then refreshed after integrating
`79b153b` (including #337 and #338), plus the source changes in this PR.
**Cut-over is not ready for owner sign-off.** Four source images built and
passed bounded remote image checks, but the infrastructure bootstrap failed.
There is no deployed application, healthy revision or deployed smoke pass.
No owner sign-off is recorded or inferred.

This pack does not delete `mvp/` or `prototype/`, rename workflows, migrate
private data, change tenant configuration or authorize product operation.
`mvp/README.md` remains tracked. `prototype/` was already removed by
commit `a7e3004` / #295 before this work; it is not recreated or deleted here.
The canonical policy is [ADR 0006](../adrs/0006-src-layout-and-cutover.md).

| Owner evidence, read before execution | Current direction |
| --- | --- |
| [#200 comments](https://github.com/jmservera/ama/issues/200), 2026-10-15 | Keep old workflow/check names through cut-over, then rename together in one PR |
| [#201 comments](https://github.com/jmservera/ama/issues/201), 2026-10-15 | Juan Manuel Servera (@jmservera) signs off; no minimum soak; healthy src deployment and owner sign-off precede deletion |
| [#322 comment](https://github.com/jmservera/ama/issues/322), 2026-10-16 | Deploy-script resolution: existing job image, else newest registry tag, else visibly reported placeholder. Implemented by #337 and integrated here; explicit digest used for this evidence run |
| [#323 comment](https://github.com/jmservera/ama/issues/323), 2026-10-16 | Rulesets warn, not enforce; owner says no protection change needed; src-ci already validates source |

## Current Parity Audit

The [historical matrix](./mvp-to-src-parity-matrix.md) remains the migration
record, not a claim that every feature is accepted. The generated
[row reconciliation](./cutover-parity-audit.tsv) checks **130 rows/patterns**:
116 migrate, one partial rebuild, 12 retire and one archive. The two sandbox
patterns represent 450 files. Comparing names only with
`git ls-tree -r --name-only 736b387 -- mvp prototype` accounts for all **578**
historical tracked paths, with zero unmapped names. No historical dataset or
sandbox content was opened.

Every migrate row has a tracked destination. Destination existence is not a
behavioural or deployment proof; local suites below provide separate evidence.
The 13 retire/archive rows, including the two sandbox patterns, were absent
before this pack. They were not deleted by this work.

| Feature or artifact | Current disposition and actual location | Evidence and remaining boundary |
| --- | --- | --- |
| Domain, JSON/SQLite/SQL Server stores, ledger, finance, grants, workflows, resident decisions, controls, ranking and projection | Migrated to `src/core/src/zava_forward/core/`; package data under `policies/` and `law/` | Core/API suites pass locally; SQL Server integration is opt-in and skipped locally. No deployed SQL proof |
| Rule cards, law register, chat privacy/isolation/recovery, synthetic tools | Migrated to core; later rule-engine/source-monitor/taskqueue features are new source work, not proof of historical deployment | Core suite covers synthetic/local behaviour; human legal approval, hosted monitoring and owner policy remain separate |
| HTTP server, auth, time capture and all 16 historical web assets | Migrated to `src/api/src/zava_forward/api/`; web is package data | API suite, JS syntax and synthetic Chromium harness pass; no live sign-in, consent or user acceptance |
| AI evaluation and fixtures | `src/agents/src/zava_forward/agents/ai_eval.py`; evals stay in `src/agents/evals/` | Agents suite passes; scripted evaluation is not actual-model quality/benefit. API explicitly uses `ai_priority_golden.json` at runtime |
| Assistant proposal logic / registry / release gate | `core/assistants.py`, `core/ai_registry.py`, `core/assistant_release.py`, not the proposed agents paths | Explicit A1/A2 divergence retained; core cannot import a workload |
| Assistant dispatch rebuild | `src/agents/src/zava_forward/agents/dispatch.py` plus core proposal/SQL half and API composition | Partial rebuild under #107/#144. Worker/provider ports exist; agents `__main__` only prints a version. No deployed queue transport or autonomous worker acceptance |
| Token maintenance and digest publication | Migrated to orchestrator modules; Bicep commands use `zava_forward.orchestrator.token_store` and `zava_forward.orchestrator.digest_blob --publish`, using `orchestratorImage` | 22 orchestrator tests pass; no scheduled execution or vault SAS publication performed |
| Import workload | Historical form fixtures migrated. New #80 `xlsx`, `mapping`, `quarantine`, `export` implement synthetic Excel preview/approval/export contracts | 39 importer tests pass. CLI preview exists; HTTP integration, queue transport, limited-role deployment and owner thresholds remain open |
| Shared fixtures / browser harnesses | `release_support.py` is in `src/core/tests/`, not matrix's proposed API tests. Browser checks are `src/api/checks/`, outside the package | Explicit actual-target correction; API/orchestrator use only external-test fixture PYTHONPATH, never PYTHONPATH=mvp |
| Build files / requirements / README | Dockerfiles in each workload, context `src/`; actual ignore file `src/.dockerignore`, not proposed `src/api/.dockerignore`; dependencies in API/core pyprojects, hashed locks per image; README split across projects | Narrow golden-only context exception fixes a reproduced ACR build failure; pinned dependencies and privilege settings unchanged |
| Prototype and sandbox debris | Intentionally not carried forward; concepts/contracts retained in ADRs and source tests; namespace package replaces old empty package marker | Historical retire/archive decisions, not new deletion. The matrix's explicit service-role denial gap remains unresolved; staff-role coverage is not that proof |

The audit's five explicit target exceptions cover registry, assistants,
shared release fixture, context ignore file and requirements declarations.
Historical proposed targets remain visible beside actual targets in the TSV.
The remaining proposed law CLI-to-importer move is future work, not a missing
migration destination. No claim is made that A1-A5 owner ratification is complete.

Reproduce from the repository root after installing source packages:

```bash
python -m zava_forward.core.synthetic.cutover_audit --write
python -m zava_forward.core.synthetic.cutover_audit
git ls-files mvp prototype
git ls-tree -r --name-only 736b387 -- mvp prototype
```

The no-argument audit compares regenerated TSV content and fails on drift or
missing targets. Stage newly added evidence/source files before regeneration,
because enumeration deliberately uses `git ls-files`, not an unbounded scan.

## Local Validation Ledger

Python 3.12.3, pip venv outside the checkout, Ruff 0.17.1, mypy 2.4.0.
All five editable distributions and their declared dev extras were installed
with pip. No uv, Docker or private working data was used.

```bash
python3 -m venv <session>/venv
<session>/venv/bin/python -m pip install \
  -e 'src/core[dev]' -e 'src/agents[dev]' -e 'src/api[dev]' \
  -e 'src/orchestrator[dev]' -e 'src/importer[dev]'
# In each project, with the venv active:
python -m unittest discover -s tests -q
ruff check . && ruff format --check . && mypy
# API only:
PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -q
# Orchestrator only:
PYTHONPATH=../core/tests python -m unittest discover -s tests -q
```

| Check run locally | Actual result |
| --- | --- |
| Core complete suite after upstream integration and all nine audit tests | 491 tests, 314.870s, OK, one opt-in SQL skip; replaces the earlier 482-test run |
| Audit tests before upstream integration | Nine passed, 0.457s; sandbox regression is also included in the latest complete core run |
| Agents complete suite | 70 passed, 6.186s |
| API complete suite | 542 tests, 205.126s, OK, 103 skipped, principally disposable SQL Server contracts |
| Orchestrator complete suite | 22 passed, 3.181s |
| Importer complete suite | 39 passed, 0.148s |
| Ruff check, Ruff format check and mypy | Passed for all five projects; final core mypy checked 91 source files. Existing migration exemptions remain; this is not full typing/formatting cleanup |
| Every `infra/*.bicep` and `infra/modules/*.bicep`, build and lint | Passed using Azure CLI 2.91.0 / Bicep 0.48.1 |
| `REQUIRE_AZ_BICEP=1 python -m unittest discover -s infra/tests -q` | 103 passed after integrating #337; earlier 86-test run passed in 24.912s |
| New deployment-wrapper static checks | CI's scoped Ruff/format selector passed; `mypy --follow-imports=silent infra/scripts/deploy.py infra/tests/test_deploy.py` passed. Additional non-CI `--strict` probe failed with 23 missing-annotation/type-argument errors in upstream test code; no unrelated typing cleanup performed |
| `python tools/rename-zava-tests.py` | 25 passed after pip installation of `tools/rename-zava-requirements.txt` |
| Installed namespace and tracked-data checks | Five namespace locations, no namespace init; no tracked `src/**/data/**` |
| `node --check` on every `src/api/src/zava_forward/api/web/*.js` | Passed |
| `cd src/api && python -m checks.design_system_browser_check` | Passed, Chromium 156.0.8078.4; manifest 152-ia-v1; partial AC-034/043, not complete accessibility or human acceptance |
| Local image runtime checks / vulnerability scan | Not run: Docker unavailable. Remote runtime checks below are separately labelled; no new vulnerability scan claimed |

Initial failures are retained as execution evidence: applying shared-fixture
PYTHONPATH to agents caused a duplicate `test_dependency_rule` import and
discovery exited 1. Rerunning agents with PYTHONPATH unset passed all 70 tests.
The first rename run failed seven tests because pptx/PIL were missing;
installing the existing requirements resolved all seven, without changing pins.
Initial audit tests exposed stale targets and an omitted sandbox table shape;
the final audit explicitly handles both.

Historical matrix baseline: 719 tests with 92 skips on `736b387`, then 747
tests with 92 skips before M6. The five latest complete runs above total 1,164
tests with 104 skips, including all nine audit tests in the complete core run.
Growth reflects later source features and these audit tests,
not a measured increase in line/branch coverage. Prototype's 15 retired tests
were outside the historical baseline. Current SQL-dependent tests grew as
features landed; opt-in SQL execution remains a separate gate. Equal-or-greater
test count is supported; equal-or-greater measured coverage is **not established**.

Mutation evidence uses the same real audit and external test module:

* With actual-target corrections disabled in memory (retaining only the
  requirements-cell parser mapping), two assertions fail: current matrix
  destination completeness and actual shared-fixture placement. Zero
  import/discovery errors. Restoring the corrections passes.
* Substituting the actual `aedd616:src/.dockerignore` text makes the named
  golden-context regression fail. The old context also failed a real ACR
  BuildKit build (`db6`); corrected context built successfully (`db7`-`db9`).
* Missing-target, added-reference/drift, duplicate/unknown/empty matrix and
  excluded-before-read controls are exercised by the nine-test suite.
  No tracked source was mutated or reverted to run these negative controls.

Baseline CI is separate evidence, not this branch's CI:
[src-ci run 38884766231](https://github.com/jmservera/ama/actions/runs/38884766231)
at `aedd616` succeeded for all seven jobs, and
[MVP CI run 38884766269](https://github.com/jmservera/ama/actions/runs/38884766269)
succeeded. PR checks must establish the new commit's status.

## Azure Execution and Deployed-Proof Result

Only resource group `ama` in subscription
`<subscription-id>` was targeted. Group ID:
`/subscriptions/<subscription-id>/resourceGroups/ama`.
The group already existed in `uksouth`. Initial generic inventory was `[]`,
but the Consumption budgets endpoint contained `budget-forward-test`.
That pre-existing budget was preserved.

The active Azure principal is an application
(`<entra-sql-admin-group-object-id>`), not the owner's interactive account.
No token, credential, cookie, dataset, secret value or signed storage URL is
published. The [sanitized Azure evidence](./cutover-azure-evidence.json)
contains the actual run metadata, terminal deployment errors, resource IDs,
inventory and source-input hashes.

### Commands and Effective Parameters

The initial bootstrap used the repo's
[two-stage recipe](../../infra/README.md#from-empty-rebuild-observed-on-2026-10-12),
`az deployment group` with `infra/main.bicep`. The subsequently merged
[deploy wrapper](../../infra/scripts/deploy.py) from #337 is now the canonical
entry point and was also executed below. Tenant/staff initializer scripts were
inspected but not run: tenant mutation, private roster restoration and existing
app credentials are not supplied by RG ownership.

```bash
az account show --query '{subscription:id,tenant:tenantId}' -o json
az group show -n ama --query '{id:id,location:location}' -o json
az resource list -g ama --query '[].{id:id,type:type,name:name}' -o json
az rest --method get --url \
  'https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/ama/providers/Microsoft.Consumption/budgets?api-version=2023-05-01' \
  --query 'value[].name'
```

Both what-if and create used the following parameter set:

```bash
az deployment group what-if \
  --subscription <subscription-id> -g ama \
  -n cutover-201-bootstrap -f infra/main.bicep -p infra/main.bicepparam \
  -p workload=cutover environmentName=test deployApplications=false \
  sqlAdminGroupName=cutover-evidence-principal \
  sqlAdminGroupObjectId=<entra-sql-admin-group-object-id> \
  sqlAdminPrincipalType=Application \
  alertEmail=8036360+jmservera@users.noreply.github.com modelDeployments='[]' \
  --no-pretty-print
# Same arguments, replacing "what-if" with "create --mode Incremental".
```

Development profile, public access requested, purge protection false, locks
false, Entra client ID empty, no applications and no model deployments.
The noreply address is a non-secret test notification target, not a verified
operational alert mailbox. `modelDeployments=[]` deliberately avoids unneeded
inference capacity; no model availability/quality proof follows.

The first what-if using `workload=forward` proposed modifying the existing
budget; it was not deployed. Isolated `workload=cutover` what-if succeeded:
98 Create, 14 Unsupported expressions, zero Modify/Delete. Unsupported
identity-dependent role expressions were inspected for ama-scoped targets;
what-if is not full validation. An initial literal-ID-only assertion rejected
those expressions; manual source/target review preceded the actual deployment.

### Infrastructure Result: Failed

The group deployment exited **1**, terminal state `Failed`, correlation ID
`4758806b-a539-494a-a02e-4433215b7c27`.

| Failed nested deployment | Actual error | Boundary and disposition |
| --- | --- | --- |
| `iothub` | `MissingSubscriptionRegistration`: subscription not registered for `Microsoft.Devices` | `az provider show --namespace Microsoft.Devices` returned `NotRegistered`. Subscription registration is outside authorized scope; not attempted |
| `sql` | `DenyPublicEndpointEnabled`: firewall rules cannot be modified while public network interface is disabled | Actual SQL server state Ready, `publicNetworkAccess=Disabled`, despite development parameters requesting public access. Existing infra guide documents policy interference; no new policy-compliance diagnosis or policy/tag bypass is claimed |

Resource ID of the deployment is group ID plus
`/providers/Microsoft.Resources/deployments/cutover-201-bootstrap`.
SQL server ID is group ID plus
`/providers/Microsoft.Sql/servers/sql-cutover-test-rzsrg`.

After integrating #337, the canonical wrapper was run from the repository root
with the same safe bootstrap parameters and the final orchestrator digest:

```bash
test "$(az account show --query id -o tsv)" = \
  <subscription-id>
python infra/scripts/deploy.py \
  --resource-group ama --registry crcutovertestrzsrg \
  --workload cutover --environment test --parameters infra/main.bicepparam \
  --orchestrator-image crcutovertestrzsrg.azurecr.io/zava-forward-orchestrator@sha256:509d18af6288eb59d6f90eff1655a53dab9830d928140ff9798f7facc2cdaa01 \
  --parameter deployApplications=false \
  --parameter sqlAdminGroupName=cutover-evidence-principal \
  --parameter sqlAdminGroupObjectId=<entra-sql-admin-group-object-id> \
  --parameter sqlAdminPrincipalType=Application \
  --parameter alertEmail=8036360+jmservera@users.noreply.github.com \
  --parameter 'modelDeployments=[]'
# Repeat the same wrapper invocation with --apply after inspecting what-if.
```

The wrapper printed the exact digest with source `explicit
--orchestrator-image`. Default what-if exited 0: eight Create, 43 Modify,
47 NoChange, 14 Unsupported and nine Ignore, with no Delete. Modifications
targeted the run-created cutover stack, not the pre-existing forward budget.
The unsupported identity-dependent role assignments remain ama-scoped.
The `--apply` attempt exited **1** at 2026-10-16 12:30 UTC, again failing
on `MissingSubscriptionRegistration` and `DenyPublicEndpointEnabled`.
Deployment ID is group ID plus `/providers/Microsoft.Resources/deployments/main`;
correlation ID `d32ef897-d489-4fb9-a259-c614322cbc8e`. The sanitized JSON
retains both attempts. Retrying through the wrapper does not resolve the
platform prerequisites or constitute deployed-image proof.

Do not advance to `deployApplications=true`: successful dependency provisioning,
reachable/initialized SQL with managed-identity users, existing Entra client ID,
vault auth-secret availability and safe synthetic initialization have not all
been established. No unauthenticated public substitute was deployed. The
repository SQL-user initializer was not run against the inaccessible server;
no private dataset was read or restored.

### Source Images: Remote Build and Bounded Runtime Checks Passed

Four direct calls of the documented form
`az acr build -r crcutovertestrzsrg -f src/<project>/Dockerfile -t <tag> src`
failed with exit 1: API `db3`, agents `db2`, orchestrator `db1`, importer `db4`.
Each failed because existing `RUN --mount` requires BuildKit.

The documented [ACR Tasks YAML environment support](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-tasks-reference-yaml#task-properties)
(checked 2026-10-16) enables a Docker-free alternative:

```bash
az acr run --subscription <subscription-id> \
  -r crcutovertestrzsrg -f acr-cutover.yaml --timeout 1800 src
```

[src/acr-cutover.yaml](../../src/acr-cutover.yaml) sets
`DOCKER_BUILDKIT=1`, builds only named packages from `src/`, runs contracts and
publishes unique `cutover-<run ID>` tags. A first stdin-template attempt (`db5`)
failed because the service looked for `/workspace/-`; the checked-in task file
avoids that CLI path problem. BuildKit then exposed the excluded runtime
golden (`db6`); this PR adds only that file as an eval-context exception.
`db7` built/pushed four images. `db8` rebuilt the source audit and passed all
four runtime checks before push. Final `db9` repeated all four builds,
contracts and pushes after integrating #337/#338, finishing
2026-10-16 12:25 UTC.

Registry: `crcutovertestrzsrg.azurecr.io`. Final tag: `cutover-db9`.

| Repository | Final digest |
| --- | --- |
| `zava-forward-api` | `sha256:248c70fe3653fb9f7e11ff7bf50b54eb243c61e911c2bb30e19cb8370064064e` |
| `zava-forward-agents` | `sha256:587a43f4110ed22e0c02cbdee9c3cf5dcd8df39ad214fcfcdea374fe799a9eed` |
| `zava-forward-orchestrator` | `sha256:509d18af6288eb59d6f90eff1655a53dab9830d928140ff9798f7facc2cdaa01` |
| `zava-forward-importer` | `sha256:53a00d7f34a0895798642c096dbb7dd9db13096fc1b9747017a3798e5f8537d5` |

Run resource ID: group ID plus
`/providers/Microsoft.ContainerRegistry/registries/crcutovertestrzsrg/runs/db9`.
The upload was a local working tree, not a Git-context build: original base,
integrated upstream `79b153b`, and this PR's audit/context/task additions,
identified by hashes in the JSON.
Do not relabel it as an image built from a future merge commit.

All four remote contracts ran as UID 10001, checked read-only root, zero
effective capabilities and absence of `/app/data` and `/data/zavaforward.json`.
Agents also checked that neither SQL nor Azure client packages were installed.
These are bounded remote image checks, not full filesystem absence proofs,
vulnerability scans or Container Apps workload health.

### Deployed Smoke: Blocked, Not Passed

```bash
az containerapp list -g ama \
  --query '[].{name:name,fqdn:properties.configuration.ingress.fqdn}' -o json
# []
az containerapp show -g ama -n ca-cutover-test-api \
  --query '{id:id,revision:properties.latestReadyRevisionName,fqdn:properties.configuration.ingress.fqdn}'
# exit 1: ResourceNotFound
```

No FQDN exists, so there is no valid target for curl. `/healthz`, protected
API anonymous denial, authenticated SQL read/write, revision restart/persistence
and scheduled jobs are **Not run / blocked**. No health 200, auth 401 or
revision/image binding is invented. When prerequisites are cleared, deploy
all four explicit digest references, verify actual revision image/readiness,
then probe `/healthz` and protected `/api/cases` (anonymous denial). Bound
polling to 12 attempts, ten seconds apart, each request timeout ten seconds.
Authenticated synthetic SQL and restart checks require an authorized identity,
without publishing tokens or private response bodies.

### Retained Resources and Cleanup

The final captured inventory contains **65 generic resources** inside ama, listed
by ID in the JSON, plus the run-created `budget-cutover-test`. Billable partial
services include ACR Premium, SQL/database, monitoring, storage/private
endpoints and a Foundry account without model deployments. No cost estimate
or successful alert delivery is asserted.

No current owner instruction requires automatic post-evidence teardown; the
historical from-empty rebuild describes a pre-rebuild reset, not teardown of
this run. Therefore no resource cleanup was performed. The group, pre-existing
`budget-forward-test`, partial stack and versioned images are retained for
inspection/remediation. They can continue accruing charges. Any later cleanup
must use the exact run-created ID inventory, handle dependent child resources
and hidden run-created budget, and **never delete the resource group** or the
pre-existing budget. No subscription registration, tenant provisioning or
resource outside ama was created/deleted.

## Remaining References and Post-Cut-Over Rename Plan

The [reference inventory](./cutover-reference-inventory.tsv) lists every
matched tracked-text path, line, token and review class in the audited scope.
Tokens: `mvp/`, `prototype/`, `zavaforward_mvp`, `mvp-ci.yml`,
`mvp-validation.yml`. It intentionally reports locations/tokens, not raw
lines that might include configuration values. Classification is routing,
not automatic approval to rewrite a line.

Scope includes tracked source, docs, configuration and dated tracking text.
It excludes binary assets, generated TSVs, all working `data/` paths,
`properwarm.json`, `.env*`, `.vscode`, `.copilot-tracking/github-issues`, and
private support material except generator Python source. Exclusions happen
before opening files and are tested. Text mentions of prohibited names are
not reads of those files. Untracked/private contents are not inventoried.

| Reference group | Disposition proposed after owner cut-over |
| --- | --- |
| `.github/workflows/mvp-ci.yml`: `MVP CI`, concurrency `mvp-ci-*`, jobs `test`, `image`, `mssql`, legacy image/SBOM labels | Keep now. Proposed rename: `application-ci.yml`, `Application CI`, `application-ci-*`; coordinate any chosen job/check and artifact-label changes in the same PR, without dropping SQL/image coverage |
| `.github/workflows/mvp-validation.yml`: `MVP validation`, concurrency `mvp-validation-*`, job `validate` | Keep now. Proposed rename: `application-validation.yml`, `Application validation`, `application-validation-*`; retain equivalent tests and infra gates |
| `src-ci.yml` and its `src-*` checks | Keep; it already validates source. Do not create a replacement `prototype-validation.yml` |
| `.gitignore`, committed-data refusal in validation, rubric excludes and `mvp/README.md` | Remove obsolete live legacy guards/pointer only in authorized #202/#203 cut-over follow-up. Retain external data and `src/**/data/**` protections; do not remove protections before private backup attestation |
| Migration tools/tests and generator filenames such as `build_mvp_dataset.py`, `zf_mvp_coverage.py`, `test_mvp.py` | Review as compatibility or regression identifiers, not necessarily old path dependencies. If renamed, update imports, tests, docs and commands together; no need to rewrite historical brand/path fixtures |
| ADRs, historical matrix/PR records, dated deployment recipes, rubric score evidence and tracking | Preserve historical identifiers and dates. Update adjacent live guidance, not the historical evidence |

The old workflows already point to src; names are not evidence of old-path
execution. Before the single rename PR, export actual workflow/job/check
contexts and any status integrations, reconfirm #323's warning-only ruleset
position, and search this inventory for references to update. After the rename,
run all replacement paths and verify PR check output before retiring old
contexts or dashboard links. The ruleset API returned **403** ("Upgrade to
GitHub Pro or make this repository public"); no independent live enforcement
verification is claimed and no protection mutation was attempted.

## Other Cut-Over Gates

At initial inspection before publishing #341,
`gh pr list --state open --limit 100` returned `[]`; thus no
open PR on old paths was visible for dependent epics #113, #136, #165, #157,
#149. All five epics remain open. This is a timestamped PR observation, not
proof that their feature/acceptance criteria are complete; refresh before
sign-off.

The rubric registry includes `src/**/*` and excludes source vendor/data.
Both historical and currently committed score snapshots point to
`fa730d63190c200e36b9a09c890445f17e8cb164`, scored 2026-10-15, total 47
(A29/B13/C5/D0), floors false. That unchanged snapshot is stale relative to
the migration: **no valid post-migration numeric comparison is available**.
The owner accepts a temporary dip, but a fresh score, its cause and recovery
expectation still need recording before sign-off. Recover by rerunning scoring
on the actual candidate and resolving content/evidence gaps, not by inventing
a score or rewriting dated score evidence.

BRD version at preparation is `0.18.0`; the prospective archive tag is
`v0.18.0` only if that remains current at cut-over. No tag/release was created.

## Owner Sign-Off Checklist

All boxes are deliberately unchecked. Technical evidence is not owner approval.

* [ ] Confirm Juan Manuel Servera (@jmservera) as cut-over approver in #201.
* [ ] Accept the ADR 0006 implementation boundary and explicitly disposition
  A1-A5 actual placements, partial assistant rebuild and prototype service-role
  denial gap using the matrix and this pack.
* [ ] Refresh all historical-row/destination checks and attach green
  candidate-commit CI, SQL Server and image evidence; resolve coverage
  equivalence uncertainty rather than equating counts with coverage.
* [ ] Resolve Microsoft.Devices registration through an authorized
  subscription operator and the SQL public-access/network restriction through
  the approved network/policy route. Do not weaken controls silently.
* [ ] Complete safe SQL/Entra/secret prerequisites, deploy explicit source
  image digests through repo infra, and capture healthy revision binding,
  public health, protected API denial, authorized SQL and restart persistence.
  Record each workload/job's actual functional versus skeleton status.
* [ ] Review retained ama resources and ongoing charges; explicitly choose
  remediation/retention or ID-scoped cleanup without deleting ama.
* [ ] Personally confirm private data copied to `ZF_DATA`, opened successfully
  by the app, and encrypted backup exists outside git. Provide a non-sensitive
  attestation only; agents must not read the dataset or backup.
* [ ] Refresh dependent-epic open-PR/old-path review for #113/#136/#165/#157/#149.
* [ ] Obtain a real before/after rubric comparison, record any accepted dip,
  cause and recovery expectation.
* [ ] Confirm current BRD version and `v<BRD version>` archive tag plus GitHub
  release at cut-over, without creating either prematurely.
* [ ] Review updated README/index/log and scoped reference inventory; approve
  the separate single-PR post-cut-over workflow/check rename plan.
* [ ] Explicitly record go/no-go and sign-off in #201. Only a later authorized
  #202/#203 change may remove legacy paths; this PR never performs deletion.
