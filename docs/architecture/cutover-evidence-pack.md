---
title: Source cut-over evidence pack
description: Dated parity, private SQL and public edge proof with remaining owner gates
ms.date: 2026-10-16
ms.topic: reference
---

## Decision and Scope

Refs #200. Refs #201. Evidence prepared on 2026-10-16 against base
`aedd616ffff8abfcf0379a538b895e4427147c8f`, then refreshed after integrating
`79b153b` (including #337 and #338), plus the source changes in this PR.
**Cut-over is not ready for owner sign-off.** The original failed bootstrap
below is preserved as historical evidence. The owner-authorized private-network
continuation on 2026-10-16 has since passed bootstrap, private health/denial,
API-MI SQL and restart persistence for one synthetic case. Authorized HTTP and
human staff initialization remain Blocked. The results below supersede the
original platform blockers, not the remaining owner gates. No owner sign-off
is recorded or inferred. The public-edge continuation below additionally proves
public health, native API denial and browser redirect, not a real-user session.

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
| Owner task direction, 2026-10-16 | Providers registered, ama costs acceptable, RG ownership available; SQL public access stays Disabled, no policy/tag/firewall bypass or peering; all private data-plane probes run inside the ama VNet |

## Direct Demo Ingress Offline Scope (2026-10-16)

Refs #360. Owner decision: the demo entry point is direct Container Apps HTTPS
with Entra browser sign-in; Front Door is optional for production, not required
for this synthetic demo. This supersedes the historical edge selection below,
not its observations or unmet sign-in/feature gates. **No Azure resources,
tenant objects, DNS, data or network settings were changed for this task.**
The live facts below are supplied coordinator findings, not fresh Azure reads.

The current `cae-cutover-test` is internal, Consumption, on `snet-aca`.
Its internal setting is immutable; apps/jobs cannot move environments and
their names must remain unique in `ama`. The replacement therefore needs a
new external environment, dedicated delegated subnet/HTTPS NSG and distinctly
named apps/jobs. Existing identities, images, private SQL/vault/storage/
registry/Foundry/IoT and private endpoints are reused, not recreated.
`demoDirectIngress` is independent of the forbidden broad public-data switch.
Default/production behavior is retained, direct auth uses NoProxy and the app
FQDN, and the demo tag/flag bypasses all Front Door discovery.

### Single-command Authentication Continuation (2026-10-16)

Refs #360. The earlier owner follow-up replaced manual credential flags, roster creation,
separate Entra check, and SQL check/apply/restart instructions with
`python3 infra/scripts/setup-entra.py` (`--yes` for the single SQL confirmation).
This continuation is offline implementation only, not a tenant/deployment
receipt. The [runbook](../../infra/README.md#post-deployment-api-authentication-initialization)
is the current operator contract; earlier step-by-step observations below
remain historical.

| Owner requirement | Offline evidence and limit |
| --- | --- |
| Automatic browser credential and private-vault preference | Named unexpired credential/storage matching, unique interrupted-handoff recovery, automatic direct-demo fallback on vault probe/write failure, and private temporary body files are mocked. Actual vault access, MI permission and token exchange are Not run |
| No typed vault or identity | API secret references/attached identities, configured vault URI, deployment tags/resource lookup, and available Bicep outputs are used; optional overrides remain. Interactive ambiguity asks once; headless ambiguity stops with names, never invented choices |
| Private roster onboarding/validation | Historical at this continuation: missing roster created a 0700 directory/0600 placeholder template and stopped. Superseded only for missing/exact-template demo rosters by the automatic roster follow-up below. Placeholders in other populated files, duplicates, invalid IDs/roles, groups, symlinks and unsafe modes remain rejected |
| Reconcile then check Entra | Default run rereads registration/auth/credential/runtime state and checks assignments before SQL. Mocked ordering is evidence, not real tenant/browser acceptance |
| SQL binding and restart | Default checks, shows counts, asks once, applies and verifies serving replicas. Matching roster/revision evidence avoids redundant restart. Missing private connectivity/driver/authority produces an exact authorized-host command and explicitly unconfirmed SQL/restart |
| Approved private execution route | Existing in-VNet proof initialization has no staff-roster or delegated Graph-profile transport. No new upload/job/permission mechanism is invented; authorized-host handoff is implemented. Live SQL binding/restart remains Not run |
| Credential-store deployment protection | Store/name tags and default-Key-Vault Bicep parameter/guards exist. Guarded CLI and CI refuse full application deployment over app-local credentials. Explicit app mode permits dependency-only updates; no secret value is exported into ARM templates |
| Coordination | Existing advisory tag, app/environment/revision update and running group-deployment refusals are mocked. Local exclusive lock and owned app-tag release are tested; conditional If-Match is used when available. A tag alone does not establish an Azure-enforced simultaneous-start mutex; that stronger cross-host guarantee remains unmet/unverified and raw portal changes require operator serialization |
| Read-only and privacy boundaries | Check/dry-run do not mutate cloud resources or create a roster/profile, apply SQL or restart. Real identifiers/credentials/private datasets are absent from committed evidence. `ama` deletion, network opening and direct-mode Front Door discovery have no new path |
| Original issue acceptance | Offline infrastructure/auth/documentation work does not satisfy migration/cost approval (c), live HTTPS/browser/roles/SQL/AI (d), or authorized edge retirement (e). No issue checkboxes changed |

The SQL helper additionally discovers the configured server within `ama` and
refuses anything except public access `Disabled`; role keys/full labels must
match existing workbench positions before SQL writes. Juan Manuel Servera
remains the synthetic exercise Legal, Compliance and DPO owner. This technical
onboarding adds no legal interpretation, control activation, consent, safety
or financial approval and makes no operational-readiness claim.

Offline continuation receipt: 260 infra tests passed without skips, including
local compiled Bicep guards; four production scripts passed scoped mypy;
focused Ruff passed with no introduced baseline findings; 32 local loopback
API authentication tests and Markdown/diff checks passed. No deployed probe
was run, and no strict distributed-mutex or full live acceptance is claimed.

### Automatic Demo Roster Follow-up (2026-10-16)

Refs #360. Owner instruction removes manual template filling for the synthetic
demo only. **No setup command was run live and no Azure, Entra, SQL, network or
private dataset was changed.** Results below are offline engineering evidence,
not a deployment receipt. The current contract is the
[tenant initialization runbook](../../infra/README.md#tenant-staff-and-application-role-initialization).

| Owner follow-up criterion | Observed offline evidence | Unmet or bounded evidence |
| --- | --- | --- |
| 1. Authoritative SQL candidate codes/roles, approved private route or exact command | Pass: existing candidate subprocess adds supplier scope and binding-present metadata without personal fields. Invalid/unknown/duplicate/placeholder candidates stop. Connectivity failure prints one exact setup command, preserving safe mode/seed/profile/app without private administrator input | Actual SQL connectivity Not run. Existing VNet proof job still has no approved roster/Graph-profile transport; no invented codes or new transport |
| 2. Case-insensitive admin, none/one/many and administrative role | Pass: mocked zero/one/multiple matches, explicit selection and one invalid interactive answer; first stable ProgrammeManager code reserved and described in plain words. Missing role or ineligible admin stops | UPN prefix is an owner-selected exercise convention, not proof of actual tenant admin authority. No directory administrator role is granted |
| 3. Distinct enabled people, seeded random assignment, role/supplier preservation and shortage | Pass: guests, disabled, rooms/desks/workspaces/shared/service naming, non-user objects and non-user/unknown mailbox purposes excluded. Personal-looking shared account rejected by Graph purpose. Sorted input/reversed-response seed equality, differing seed variation and persisted no-reshuffle tested. Exact one-user deficit stops; existing bound SQL rows stop before writes | Uses Graph/Exchange classifications, not independent verification of real humans or competence. `MailboxSettings.Read` access to all candidates is a real prerequisite, Not run. Deliberately chooses the permitted stop alternative, not an `--allow-reuse` override incompatible with distinct SQL bindings |
| 4. Private write, redacted counts/role summary, confirmation and read-only | Pass: private 0700/0600 envelope shared by both readers, seed persistence, exact-template replacement only, symlink/changed-input refusal, no object IDs/UPNs/names/supplier names in generated output, one roster confirmation and decline, `--yes`, no-write check/dry-run previews | Offline filesystem and mocked directory evidence only. Existing populated legacy arrays remain supported and are not automatically replaced |
| 5. Synthetic-only disclaimer and production refusal | Pass: disclaimer in docs/output; Bicep profile tag cannot be overridden by caller tags. App/environment production, omitted/default profile, unknown/conflicting evidence and unrelated deployment outputs refuse generation without candidate SQL or auth writes. Bound development outputs and nested module tags accepted; persisted generated rosters rechecked | No deployment/tag mutation performed. Old untagged resources need verified resource-bound development evidence; a demo name/direct ingress cannot authorize generation |
| 6. Continue Entra check, SQL check/confirmation/apply/restart and final status | Pass: default mocked generation reaches existing reconciliation/final Entra verification, then SQL check and one separate SQL confirmation, apply with restart, and final explicit binding/restart summary. Current persisted roster reuses mapping; mailbox eligibility rechecked before remote mutation | Actual Entra grants, SQL binding, serving-replica restart and browser sign-in Not run. Existing advisory lock is not independently proven cross-host exclusion |
| 7. Existing safeguards, tests, README/evidence/log | Pass within offline scope: legacy array and envelope readers, existing placeholder/duplicate/mode/role/group/lock tests retained; full infra suite 282 passed, including compiled Bicep and SQL initializer tests. Scoped script mypy and 32 local responsive loopback auth tests pass | Lint baseline uses existing script exclusions; new-line lint is checked separately. No issue-body boxes changed; coordinator owns merge-time evidence decisions |

ProgrammeManager is selected for existing administrative capabilities, including
the memory administration role (`src/core/src/zava_forward/core/chat_privacy.py`)
and document controls (`src/core/src/zava_forward/core/doc_controls.py`), not
because random assignment creates authority. Juan Manuel Servera remains the
exercise Legal, Compliance and DPO owner. Legal interpretation, activation,
consent, safety and financial commitments remain named-human decisions.
ADR 0005 acceptance is synthetic-development only, with real owners/sources
still a gap before operational reliance.

Mailbox-purpose API and classification values were checked against official
Microsoft Graph documentation on 2026-10-16; links and permission prerequisites
are in the runbook. Permission denial/unknown classification fails closed;
setup never grants new mailbox or directory permissions.

Original issue #360 criteria a/b/f have additional bounded offline coverage only;
c (migration/cost approval), d (live HTTPS/browser/roles/SQL/AI) and e (separately
authorized retirement) remain unmet by this follow-up. Historical observations
elsewhere in this pack are not fresh acceptance evidence.

### Proposed Migration and Approval Gates

The canonical step-by-step
[migration proposal](../../infra/README.md#direct-demo-ingress-migration-proposal-2026-10-16-360)
covers environment-only then API-only staging, DNS, reused identity/RBAC and
image/config checks, all queue/scheduled/import consumer drain/activation,
rollback, cost sensitivity and selective retirement. It is written, **not
reviewed or approved by the owner**. The coordinator must obtain approval
before any replacement, deletion or spend; this task authorizes none.

Keep old and new background consumers from acting concurrently against shared
queues/token storage/ledger. Zero minimum replicas does not disable KEDA.
Stage with background workloads omitted, drain or disposition old running
executions and messages, then activate only one generation. Reverse the same
boundary during rollback; do not restore stale shared SQL or reseed.
Keep old callbacks and the old environment/edge through the approved rollback
window. After verified d and a separate owner authorization, remove only the
approved old workloads, environment-specific DNS/subnet/NSG and dedicated
`afd-cutover-test` edge dependencies. Retain all shared services, private
endpoints, identities/RBAC, VNet and resource group `ama`.

Consumption has no standing environment charge by itself; replicas/jobs,
logs/network, existing private endpoints and retained edge overlap still cost.
Private-endpoint/planned-maintenance features can add management fees even
on Consumption. The runbook records dated official billing sources and
unquoted USD 23-78/API-month illustrative sensitivity, not a current account
quote or approved budget. Exact rates/overlap remain owner approval inputs.

### Historical MVP Difference

History-only commit `15e8158` shows direct external ingress, browser EasyAuth,
public welcome exclusions and app-FQDN callback generation. Its environment
exposure depended on `allowPublicNetworkAccess`, which also opened backing
services; that obsolete configuration is not copied. Historical owner sign-in
reports and old names/datasets are not direct-src acceptance. No working-tree
`mvp/` or `prototype/` code was restored or changed.

### Issue 360 Acceptance Audit

| Criterion | Offline status | Unmet acceptance boundary |
| --- | --- | --- |
| a. Explicit demo Bicep external environment, own subnet/NSG, independent private services and unchanged defaults/production | Implemented; offline validation recorded below | No deployed network/private-service readback or new environment observed |
| b. Direct setup without Front Door command/permission/extension; optional edge retained | Implemented; fake CLI/auth regressions recorded below | No real directory/credential/roster changes, human sign-in or live tool completion |
| c. Owner-reviewed and approved migration before replacement/deletion/spend | Proposal written; **Unmet** | Owner review and approval not performed or inferred |
| d. Live HTTPS/welcome/health, API denial, browser sign-in, roles, SQL persistence and AI | **Not run / Unmet** | All replacement live checks await coordinator and owner authorization; browser JSON API 302 gap remains Refs #350 |
| e. Retire demo Front Door after d and explicit owner authorization | **Not run / Unmet** | No deletion authorized/performed; `afd-cutover-test`, old environment and `ama` untouched |
| f. Runbook, infra guide, ADR/architecture/evidence updated with historical separation | Updated offline | New deployment observations must be appended by the coordinator, not substituted for history |

No issue body checkboxes are changed. The coordinator alone ticks those whose
merge-time evidence proves acceptance. Offline tests do not prove criterion d
or clear #349/#350. Probe credentials/claims, subscription/tenant/Entra IDs,
roster, full login URLs and secret values must never enter the evidence.
Juan Manuel Servera remains exercise Legal/Compliance/DPO owner; ADR 0005 is
accepted for synthetic development only. Real owners and sources, legal
interpretation, rule activation, consent, safety and financial commitments
remain human boundaries; nothing here approves operational reliance.

### Offline Validation Receipt

All 234 infra unit tests passed with `REQUIRE_AZ_BICEP=1`, including compiled
demo/default/guard/private-service controls, 54 setup tests and 18 probe tests.
All root/module Bicep templates built and linted locally with `az bicep`;
no deployment, what-if or Azure data/management request was run.
CI-aligned Bicep-test Ruff/format, probe Ruff and setup production mypy passed.
Broader setup Ruff and probe mypy still report pre-existing diagnostics, with
none introduced; full lint/type cleanliness is not claimed.
All 563 API tests passed with 110 conditional skips from the documented
`src/api` working directory and absolute project test paths; the authentication
subset runs a responsive local HTTP app against temporary synthetic fixtures.
An initial root-directory discovery failed six project-relative imports and
was rerun correctly without changing source. Documentation links/anchors and
diff whitespace checks passed. None of these local checks prove real Entra,
Azure SQL persistence, AI calls, owner approval or replacement deployment.

The single post-implementation Review found two defects in that initial
candidate and returned **Not accepted**: overlong demo job names and an
ineffective role-denial probe against universally available `/api/me`.
Routed implementation shortens only demo job suffixes (unchanged defaults)
and tests supported name bounds/ledger-alert matching; role probes now require
authenticated Contractor `/api/me` 200 followed by `/api/stats` 403.
A real local trusted-provider/router regression covers that distinction.
The original Review verdict is retained; corrections are subsequent
implementation, not a second Review or retroactive conformance claim.
After these corrections all 237 infra tests passed without skips; corrected
template builds/lints, scoped Ruff/CI formatting and diff checks passed.
Current main was then merged, including the device-code prompt and missing-tool
diagnostics fixes. Final integrated infra discovery passed **238 tests** without
skips, and integrated setup production mypy passed. PR #362 contains the offline
implementation/corrections; its human review and CI are separate from local
evidence. No live acceptance or issue checkbox is implied.

## Public Browser Restoration (2026-10-16)

Historical #344 configuration and observations follow. The direct-demo decision
above supersedes their edge prerequisite, not their limited observed results.

Refs #344. Refs #143. Refs #200. The owner requires public browser entry again,
with SQL private and no policy bypass. This supersedes the private-only entry
point as the intended exercise access path, not the private SQL proof or the
unchecked cut-over/sign-off gates.

Historically selected edge: **Front Door Premium, WAF Prevention, Private Link to the
existing internal environment**. An API-only external environment was permitted
but would require a new environment/subnet and parallel API or explicit
replacement because `internal` cannot change in place. The chosen additive
edge reuses the serving src digest and private dependencies. It costs an
additional edge/private-endpoint service, requires connection approval, and
does not establish the complete production-profile controls in #143/#118.
Official Microsoft guidance checked on 2026-10-16:
[networking](https://learn.microsoft.com/en-us/azure/container-apps/networking),
[Front Door integration](https://learn.microsoft.com/en-us/azure/container-apps/how-to-integrate-with-azure-front-door)
and [existing environment Private Link](https://learn.microsoft.com/en-us/azure/container-apps/private-endpoints-with-dns).

Public HTTPS origin:
<https://ep-cutover-test-esdrcphsarcahhde.b01.azurefd.net/>.
The [infra continuation recipe](../../infra/README.md#public-browser-continuation-2026-10-16-344)
and [sanitized JSON](./cutover-azure-evidence.json) separate configuration,
transport, denial and actual-user acceptance.

### Bounded Resources and Configuration

`infra/public-edge-existing.bicep` was deployed incrementally inside `ama`,
without running main's broad development public-access switch. Initial
what-if: eight Create, zero Modify/Delete resources. The auth-preserving
follow-on uses `entraBearerOnly=false`, the same default as main, and changes
only the auth child in addition to the edge. It carries forward read-visible
provider validation, exclusions, token store and credential references; sets HTTPS required,
`RedirectToLoginPage` and `forwardProxy=Custom` using only
`X-Forwarded-Host` / `X-Forwarded-Proto`. A separate client secret
was not invented to conceal the missing tenant prerequisite.

New resources retained: `afd-cutover-test`, its `ep-cutover-test`, `og-api/api`,
`route-api`, `sp-waf`, `to-log-analytics`, and `wafcutovertest`; one managed
Private Link connection to `cae-cutover-test`; manual
`job-cutover-test-public-audit` using the exact serving API image. ARM nested
deployment records are execution metadata, not replaced workloads.
No pre-existing resources were deleted or replaced. Only the empty, unused
`afd-cutover-test/originheaders` rule set created by a failed header-removal
trial was deleted; Azure rejected deletion of reserved `Forwarded` request
headers before creating the rule. In particular, `ama`, all data services,
the internal environment, existing apps/jobs/identities, private DNS and budgets
remain. No tenant object, private dataset, firewall, policy/tag exemption or
network peering was changed.

The sole origin and origin Host/TLS name are the API's internal FQDN. The
endpoint has one HTTPS `/*` route, no alternate origin, rewrite rule or cache
configuration. Health probes use GET `/healthz` (the API does not implement
HEAD). WAF associates all paths with the endpoint. The connection was read
back **Approved** after native async approval completed. Earlier approval
writes returned Pending; an exit-zero write was not counted as approval.
SQL metadata still reports Ready, publicNetworkAccess **Disabled**, one
Approved private connection. The environment remains internal/Disabled.
No other app currently has ingress enabled.

At 17:01 UTC, public curl from the operator VM proved `/healthz`, `/`,
`/welcome.html`, `/style.css` and `/zava-logo.png` **200**; all probed native
anonymous `/api/` families **401**; `/sign-in` **302** to the platform login;
and browser `/app` **302** to `login.microsoftonline.com` with the HTTPS edge
callback. Native curl `/app` is 401, not a browser redirect. Initial Front Door
404s during propagation are retained separately, not counted as passes.

Forged principal and malformed bearer returned 401; conflicting Host returned
421. Individual and combined RFC Forwarded / X-Forwarded-Host/Proto requests
kept the canonical HTTPS edge callback after Custom auth propagation. Standard
initially accepted an attacker-supplied RFC host; changing both entry points to
explicit Custom headers fixed that observed failure. Final repeated probes
passed. No route rewrite, header-removal rule or API auth exemption remains.

An anonymous API request with a browser User-Agent still receives EasyAuth
302 even with `Accept: application/json`. Native curl 401 does **not** prove
the browser API-expiry contract; this additional parity gap is filed in #350.
Authenticated platform-principal handling must be proved before introducing
any API path exemption. The current result is bounded, not full acceptance.

### Browser and Feature Acceptance Boundary

The proof client is the literal `systemAssignedIdentity`, not a valid Entra
application identifier. Matching-tenant read-only discovery found no retained
workbench registration. Its browser credential is absent, delegated token store
is off, and the prior synthetic proof has zero staff. This invalidates any
interpretation of the earlier configured issuer/audience as proof of a usable
tenant registration. No real user signed in during this task.
**Real-user smoke is Blocked**, filed as #349. A redirect reaching an Entra host
is only a redirect observation, not successful client validation, callback,
role, staff binding or authenticated session. The edge-aware initializer
preserves old callbacks but still requires an authorized tenant operator and a
real registration; it cannot resolve this prerequisite itself.

The [complete dated feature audit](./mvp-to-src-parity-matrix.md#public-deployment-feature-audit-2026-10-16)
covers every historical user-visible capability and all 16 historical web
assets. The image-only job succeeded on execution
`job-cutover-test-public-audit-ud03kna`; all 17 present assets, including the
newer chat script, hash-match current src. It reads package files only, never
Store/SQL/staff/data. This proves image presence, **not functional acceptance**.

Full deployed feature parity is **Blocked**, filed as #350: one fictional case
instead of the continuing workload, no model deployment/API model settings,
empty production map tile configuration, disabled delegated-photo token store,
missing law-store settings and unexecuted positive-role workflows. Time capture
remains intentionally gated by actual DPIA/consultation/notice approvals.
Existing specialist issues are linked from each audit row, not silently treated
as delivered. Legal/source interpretation, rule activation, resident consent,
safety and financial commitments remain named human decisions. Juan Manuel
Servera is the exercise Legal/Compliance/DPO owner; ADR 0005 acceptance covers
synthetic development only, not real sources/owners or operational reliance.

### Issue 344 Acceptance Audit

| Criterion | Status | Evidence boundary |
| --- | --- | --- |
| Public workbench with Entra browser sign-in | Blocked | Public edge configured; a valid tenant application/credential/staff session is not available (#349) |
| Edge choice and trade-off | Passed | Deployed Premium/WAF/Private Link; no environment replacement; additional service/cost/approval boundary recorded |
| Public health 200 and anonymous API 401 | Native curl Passed; browser API contract Blocked | Health 200, all native API probes 401; browser User-Agent API 302 is filed in #350 |
| SQL private, Disabled, no policy bypass | Passed for this continuation | SQL/environment management metadata read back; no public-data, firewall, policy or exemption mutation |
| Every MVP feature reachable, gaps filed | Audit complete; acceptance Blocked | All capability/asset rows reconciled; image presence verified; gaps #349/#350 |
| Honest real-user browser smoke | Blocked, recorded | No real-user callback/session, staff authorization or consent performed |

No #344 body checkboxes were ticked. Owner/coordinator acceptance remains
separate. Local evidence: 123 infra tests passed, 549 API tests with 110 opt-in
skips, including 31 real-loopback auth HTTP contracts; API Ruff/format/mypy and
changed initializer mypy passed. These are not live authentication or actual
SQL feature tests. Initial missing-package checks failed before pip installation;
one new compiled assertion was corrected for runtime ARM parameter shape.
An optional mypy run over the older initializer test fixture still reports its
pre-existing heterogeneous-dict typing errors; production initializer checks
pass. No unrelated test typing cleanup was performed.

Recovery baseline: Return401 / NoProxy and seven exact existing public
exclusions. Critical network/denial/isolation failure disables only the new
endpoint and restores those auth fields; no deletion or private-network
relaxation. Tenant-prerequisite failure does not authorize anonymous access.

### PR 352 Review Continuation (2026-10-16)

Merged `origin/main`, including the #351 setup command and #118 hardening
evidence, retaining both additive evidence sections and log entries. The old
`initialize-api-auth.py` CLI remains a thin delegate to `setup-entra.py`; the
existing setup tests cover linked-edge `--public-url`, Custom forwarding and
idempotent callback updates. No second CLI implementation was added.

The additive edge now rejects missing, empty, malformed and
`systemAssignedIdentity` client values before its dependent auth/edge writes.
It requires hexadecimal UUID syntax with exact separator positions and points
to `python3 infra/scripts/setup-entra.py`. This is a local compiled-template
guard, not verification that the registration exists or a live redeployment:
the currently deployed placeholder remains an unresolved #349 prerequisite.
Full #344 acceptance stays **Blocked** until authorized setup creates or
reconciles the real registration/credential/staff bindings and a human completes
sign-in. No issue checkbox was ticked.

Fresh public curl at approximately 18:30 UTC: `/healthz` 200; native `/api/me`
401; browser User-Agent `/api/me` with `Accept: application/json` 302 to
`login.microsoftonline.com`; browser `/app` 302 to the same host. Redirect
headers/queries were discarded, retaining only status and hostname. In default
`entraBearerOnly=false` mode, EasyAuth is configured to redirect anonymous
requests; native curl's observed 401 depends on client/User-Agent handling.
This is not a route-aware browser/API split or API-wide 401 guarantee. The
browser/fetch JSON API criterion remains unmet and explicitly tracked in #350.
Read-only management probes at approximately 18:32 UTC confirmed SQL Ready/
public access Disabled and environment internal/public access Disabled.
No Azure or tenant configuration was changed.

Auth preservation has a specific limit: `edge-existing-auth.bicep` uses a
full-resource PUT with `union` of the read response. Returned references are
carried forward, but omitted/write-only/redacted credential or token-store
references cannot be recovered this way. Container App secret values are not
read or written by the module. A human must verify non-secret required
references before a live reapply and stop/repair through the authorized setup
or secret-management path if any are absent/redacted. No omitted-field
preservation or live credential round-trip is claimed.

Continuation validation: 186 infra tests passed in an isolated pip venv with
editable core/agents/API distributions and absolute fixture PYTHONPATH; this
includes compiled guard behavior and rejected mutations. Focused API auth:
32 tests passed. Scoped compiled-test Ruff/format, compiled-test/initializer
mypy and Bicep build passed. The installed local app served health/welcome 200
and anonymous API 401 on an isolated synthetic fixture; this is not live Entra
acceptance. Historical broader suite results above remain dated, not rerun.
The serving image was not rebuilt or redeployed in this continuation. Asset
hashes above describe the earlier recorded serving image, not parity with the
new branch head after integrating main's later source/UX changes.

## Deployment Hardening Audit #118 (2026-10-16)

Refs #118. This audit is separate from the historical cut-over results below.
No Azure resources, tenant configuration, existing policy or public access
were changed. The original issue checkboxes are left for the coordinator at
merge, and only evidence-proven criteria are eligible.

| Original criterion | Evidence from this change | Honest disposition |
| --- | --- | --- |
| Non-root, read-only root filesystem and dropped capabilities enforced in the Dockerfile | Four Dockerfiles set UID/GID 10001:10001. Local/CI Docker launches enforce read-only root, zero capability sets and NoNewPrivs via flags; probes prove EROFS and writable state. Shipped images have no startup guard and pass plain non-root startup as well | **Partial**. Dockerfiles cannot enforce host flags; Container Apps exposes no required read-only-root/capability controls. Local proof is not hosted enforcement |
| Image scan and tests in CI | Existing workflows run tests, lint/types and image contracts. Trivy 0.76.0 gates fixable HIGH/CRITICAL findings using ignore-unfixed true, with separate non-gating full/unfixed-inclusive JSON artifacts. No ignore lists or baselines | **Met for the owner-directed CI boundary**: all 11 integrated source checks pass at 8142553, zero fixable findings. 61 HIGH/two CRITICAL unfixed package findings per image remain unresolved. A green fixable gate does not mean clean images or hosted acceptance |
| Application defined in Bicep | Compiled tests prove six workload image consumers, API health probes and 2-4 replicas. Maintenance jobs retain direct Python module commands without the guard | **Partial** overall acceptance. Definitions passed offline; queue-worker behavior (#144), manual Entra initialization and complete rebuild/live acceptance are not proved by resource existence |
| Front Door Premium, WAF and Private Link before any public edge | Existing default-off production/private guards plus compiled Premium SKU, WAF association, HTTPS-only route and Private Link origin checks | **Partial** overall acceptance. Gated definitions proved, no public edge deployed; live Private Link approval and healthy origin remain unmet (#143). Public-edge changes are owned by the separate #344 loop |
| Azure Policy and Defender plans decided | Audit/non-enforcing assignments and opt-in Standard Defender plans are code. Disabled Defender submits no pricing resources, preserving existing plans; README gives rationale | **Partial**. Code decisions proved; owner cost acceptance, deployed policy compliance and active paid protection are not proved (#147) |

PR 347 review returned CHANGES. Per the owner's 2026-10-16 direction, the
fail-closed image ENTRYPOINT and guard-only maintenance command changes were
removed rather than shipping images that cannot start on Container Apps.
Four fresh local builds used `--pull --no-cache` with `src/` context. The
external harness enforces `--read-only --cap-drop ALL --security-opt
no-new-privileges`; five incomplete-control probes per image fail the contract.
Both hardened and plain non-root default startup pass, including API HTTP
health/PNG and writable state. Agents dependency isolation passes.
Non-API default commands remain version-only CLIs, not worker acceptance.
No new hosted runtime controls or actual Azure rollout are proved.
See [hosting limits](../../infra/README.md#hardened-source-image-rollout-118).

| Local validation for this change | Result |
| --- | --- |
| Core / API / agents / orchestrator / importer complete suites | 517 / 553 / 77 / 22 / 39 tests after concurrent main integration; all suites OK, 111 opt-in skips total (one core, 110 API). Before integration: 504 / 549 / 70 / 22 / 39 |
| All five projects' Ruff check, format check and mypy | Passed with existing project exemptions; API/orchestrator test-fixture PYTHONPATH used absolute paths |
| Infrastructure suite / all Bicep build and lint | 130 tests passed after merging main; all templates passed with Bicep 0.48.1 |
| Container tooling | Strict mypy and isolated Ruff/format passed; seven external-contract regression methods plus actual Docker harness |
| Changed GitHub workflows | actionlint 1.7.12 passed with shellcheck integration disabled; names preserved. Fixed absolute fixture paths at step runtime: github.workspace inside the matrix previously expanded to an empty prefix, breaking API/orchestrator tests |

Trivy 0.76.0 was downloaded from its official release and archive SHA-256
verified against published checksums. A fresh 2026-10-16 database was used for
both pre-review image rescans and rebuilt images, with DB updates disabled
only between comparison scans. Each still has 16 unique CVEs across 63 package
findings, with no FixedVersion. CRITICAL: CVE-2025-7458 (`libsqlite3-0`) and
CVE-2023-45853 (`zlib1g`). These are scanner results, not exploitability findings.

First attempted remediation: re-resolved `python:3.12-slim-bookworm` at Docker
Hub. Its latest index digest is still
`sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258`;
there is no newer same-tag digest to adopt. All four no-cache builds reran
`apt-get update && apt-get upgrade`; apt reported zero available upgrades.
No CVE reduction is claimed. The owner-approved gate now selects fixable
findings with the scanner option `ignore-unfixed: true`. Full reports use
`ignore-unfixed: false`, retain every HIGH/CRITICAL finding and upload alongside
gate results, even when the gate fails. No ignore lists, baselines,
package metadata removal or vulnerability-specific suppressions are used.

| Pre-review local image | Image ID (SHA-256) | Historical runtime | Fresh full scan before rebuild |
| --- | --- | --- | --- |
| api | `68ec10d0e0c12a3f5e3e5cad1e976fd8747067e4913e053e7f8670b0db0de4d9` | Passed, including real HTTP health and PNG | 61 HIGH, 2 CRITICAL |
| agents | `5344bb07abe20cac2487fa6d5744cb622b9cc6acaf76189a06e05b58668aaf3d` | Passed, including no SQL/blob clients | 61 HIGH, 2 CRITICAL |
| orchestrator | `6fd32ed1ee18672885b41d79a5a54bed6025dfc69dda18d5efcb78dd53af727d` | Passed | 61 HIGH, 2 CRITICAL |
| importer | `272b0877b6332b4f363d067fc3503b892fea0c0b4e76078a9b47bdaf8367bde0` | Passed | 61 HIGH, 2 CRITICAL |

| Rebuilt local image | Image ID (SHA-256) | Before -> after HIGH/CRITICAL package counts | Fixable-only gate |
| --- | --- | --- | --- |
| api | `50a1accf9b47bb2e1906d40da443c27fc656ecf2fdc4f67113dde860e3985371` | 61/2 -> 61/2, all unfixed | Passed, zero findings |
| agents | `1db52043163081da1ad84bae903b8491e713fa16bd2ee5b1432454ae07c65329` | 61/2 -> 61/2, all unfixed | Passed, zero findings |
| orchestrator | `23c2aec69b57321c208c6936e951844ffe5dd7915ce291833d0b6d5aa414af03` | 61/2 -> 61/2, all unfixed | Passed, zero findings |
| importer | `77f0c4127f9e154be232518273d98a996c5ef502828ca67c7d0d3c5828ce1d49` | 61/2 -> 61/2, all unfixed | Passed, zero findings |

While PR CI ran, main advanced with #348. Merged it without rewriting history
(8142553), again preserving both log sides. Its new agents tests require core
fixtures; retained that dependency in the step-time absolute PYTHONPATH.
Repeated all five local suites/Ruff/mypy and infra tests, rebuilt all four
images using the already-refreshed OS layers, reran hardened/plain application
contracts and rescanned with the same DB. Counts remain 61 HIGH/two CRITICAL
unfixed per image and zero fixable findings.

| Integrated local image | Image ID (SHA-256) |
| --- | --- |
| api | `ee757c29fdca27a82e42caf68d94b06c0926a8177f1550e61d925b74a83de45d` |
| agents | `9ec0f2f278483598f6bb27a77b244e6ae176f9139d093b4224f0247c7f161733` |
| orchestrator | `8971d9338fdd95cf67a179962dc5143669512904004d5ec1556bb62b47801e4a` |
| importer | `6ccd4998e64c721fa4f3ade66363e28b12b64b0b7a355285b93e242105b02ad0` |

At ab1c5c0 all 11 checks passed, including Source projects CI
[38934285993](https://github.com/jmservera/ama/actions/runs/38934285993) on
attempt 2, MVP CI
[38934285490](https://github.com/jmservera/ama/actions/runs/38934285490) and
MVP validation
[38934285398](https://github.com/jmservera/ama/actions/runs/38934285398).
The initial source attempt timed out at an existing browser marker navigation.
The entire browser harness passed locally unchanged, then the failed job
passed on rerun; no test bypass, reduced assertion or runtime source change.
Downloaded all four source image scan artifacts plus the existing API image
job report: each full report retains 61 HIGH/two CRITICAL, each gate is empty.
CI must still be green for the latest integrated PR head before marking ready;
historical success alone is not current-head acceptance.

Integrated source candidate 8142553 passed all 11 checks on its first attempt:
[Source projects CI 38936437239](https://github.com/jmservera/ama/actions/runs/38936437239),
[MVP CI 38936437236](https://github.com/jmservera/ama/actions/runs/38936437236)
and [MVP validation 38936437380](https://github.com/jmservera/ama/actions/runs/38936437380).
Final evidence-only publication retains the same source, infrastructure and
workflow trees. Latest-head checks must also pass before ready; status is
visible on [PR 347](https://github.com/jmservera/ama/pull/347). No merge or
full hosted acceptance is implied.

Reproduce with [source image commands](../../src/README.md#images) and
[infra quality gates](../../infra/README.md#quality-gates):

```bash
for project in api agents orchestrator importer; do
  docker build --pull --no-cache -f "src/$project/Dockerfile" -t "zava-forward-$project:local" src
  python src/check-container.py "$project" "zava-forward-$project:local"
  trivy image --config src/trivy.yaml --ignore-unfixed --exit-code 1 \
    --format json --output "trivy-$project.json" "zava-forward-$project:local"
  trivy image --config src/trivy.yaml --ignore-unfixed=false --exit-code 0 \
    --format json --output "trivy-$project-all.json" "zava-forward-$project:local"
done
```

For failure evidence, run the full report even if the fixable gate fails, as CI
does. Local before/after/fixable JSON reports remain in session evidence; CI
uploads gate and full/unfixed-inclusive reports per image.
No new deploying CI was added. SQL public access stays disabled in the actual
`ama` environment; no Azure run was needed. ADR 0005 is accepted for synthetic
development only: Juan Manuel Servera is the exercise Legal, Compliance and
DPO owner; real owners and sources remain a gap before operational reliance.
No consent, safety, legal or financial approval is inferred from this work.

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

### Historical Infrastructure Result: Failed Before Private Continuation

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

At that earlier checkpoint, do not advance to `deployApplications=true`: successful dependency provisioning,
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

### Historical Deployed Smoke: Blocked, Not Passed

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

### Private-Network Continuation (2026-10-16)

The owner confirmed that resource providers are registered, ama resource costs
are acceptable and RG Owner rights are available. SQL public access Disabled
is intentional. The operator VM is on SwedenCentral `172.16.0.0/24`, not
`vnet-cutover-test` in uksouth `10.40.0.0/16`; no peering was wanted or created.
No policy/tag exemption, public SQL enablement or firewall request was attempted.
All SQL and private HTTP probes below execute inside Container Apps jobs.

The original failures above remain historical, not current diagnoses.
`Microsoft.Devices` now reports `Registered`. A private bootstrap through
`infra/scripts/deploy.py` and `infra/main.bicep` succeeded at
**2026-10-16 14:03:51 UTC**. The explicit false public-access switch is now
honored in development; dev/test parameter-file defaults remain unchanged.
The private development stack is not a production-profile acceptance claim.

The bootstrap used `deployApplications=false`,
`deployEnvironmentOnly=true`, `allowPublicNetworkAccess=false`,
`sqlAdminGroupName=id-cutover-test-init`,
`sqlAdminGroupObjectId=<initializer-mi-principal-id>`,
`sqlAdminPrincipalType=Application`, `entraBearerOnly=true`,
`entraClientId=<existing-application-client-id>` and `modelDeployments=[]`.
The Entra audience is the application identified by the existing CLI
service-principal session, not an invented workbench registration. No Entra
app, role assignment or secret was created. RG ownership does not grant Graph
rights: the read-only application lookup returned `Insufficient privileges`.

```bash
# Workload build context is src/, never a legacy directory.
az acr run -g ama -r crcutovertestrzsrg -f acr-cutover.yaml --timeout 1800 src
az acr build -g ama -r crcutovertestrzsrg -f infra/cutover-proof.Dockerfile \
  --build-arg API_IMAGE=crcutovertestrzsrg.azurecr.io/zava-forward-api@sha256:111b26226cad06e229bcf1c3174877510c4c68c5a5fefc885167a2b4c821657d \
  -t zava-forward-cutover-proof:proof-20261016 infra

# Use the private recipe's remaining parameters, unchanged for what-if/apply.
python3 infra/scripts/deploy.py \
  --resource-group ama --registry crcutovertestrzsrg \
  --workload cutover --environment test --parameters infra/main.bicepparam \
  --orchestrator-image crcutovertestrzsrg.azurecr.io/zava-forward-orchestrator@sha256:e3b290bfa2af70918ae667feab4212f2d4d4ff8c6f4bd4b01fc629ced4a099d7 \
  --parameter allowPublicNetworkAccess=false \
  --parameter deployApplications=false --parameter deployEnvironmentOnly=true \
  --parameter sqlAdminGroupName=id-cutover-test-init \
  --parameter sqlAdminGroupObjectId=<initializer-mi-principal-id> \
  --parameter sqlAdminPrincipalType=Application \
  --parameter entraClientId=<existing-application-client-id> \
  --parameter entraBearerOnly=true \
  --parameter alertEmail=8036360+jmservera@users.noreply.github.com \
  --parameter 'modelDeployments=[]'
# Repeat with --apply after scope review. For workload rollout, use
# deployApplications=true and all four digest image parameters below.
```

Bootstrap what-if: 9 Create, 43 Modify, 47 NoChange, 18 Unsupported,
11 Ignore, zero Delete. First workload what-if: 10 Create, 47 Modify,
52 NoChange, 18 Unsupported, 16 Ignore, zero Delete. These touched only ama
cutover resources; the pre-existing `budget-forward-test` was preserved.
The first workload rollout failed on two ledger alerts using the obsolete
`ContainerAppConsoleLogs_CL` schema. ARM log-table metadata identifies
`ContainerAppConsoleLogs` with `JobName` and `Log`; both queries were corrected,
without disabling validation. Corrected what-if: 2 Create, 53 Modify,
54 NoChange, 18 Unsupported, 17 Ignore, zero Delete.

ACR task `dba` succeeded at 13:52:27 UTC with all four existing remote image
contracts passing; proof build `dbb` succeeded at 13:53:24 UTC. Source base is
`3c2d9e9`; src contents were unchanged, built from the local src context,
not a Git-context build. Both builds preceded ACR isolation. No local Docker
was used. The proof image predates final source formatting, diagnostic-message
cleanup and an offline-tested partial-initialization retry correction. The
observed clean initialization/seedless verification paths are unchanged; no
deployed partial-initialization retry pass is claimed. Its immutable digest
remains the one below; no post-isolation rebuild was attempted.

| Image repository | Deployed digest |
| --- | --- |
| `zava-forward-api` | `sha256:111b26226cad06e229bcf1c3174877510c4c68c5a5fefc885167a2b4c821657d` |
| `zava-forward-agents` | `sha256:79ec0c252c22e271fb5e833437dab1e217cca7f46cc683a48e4216c9c917fcf0` |
| `zava-forward-orchestrator` | `sha256:e3b290bfa2af70918ae667feab4212f2d4d4ff8c6f4bd4b01fc629ced4a099d7` |
| `zava-forward-importer` | `sha256:51b6a480bd7e89506341cb8d2fa667c0c24d86a4793f22358fa930a86f093f6f` |
| `zava-forward-cutover-proof` | `sha256:ef0058f8f380cc610d4b7113509293b3ed624d22afac95e807b4c69a4266dc72` |

All are under `crcutovertestrzsrg.azurecr.io`. ACR is now private with
quarantine disabled for this development exercise. Successful private job pulls
demonstrate registry MI access; default post-isolation ACR Tasks repair access
is not claimed.

SQL initializer execution `job-cutover-test-init-siaykij` succeeded at
14:03:13 UTC. Its non-root proof container used the dedicated initializer MI,
the configured SQL Entra Application administrator. It first inspected only
system-table metadata, confirmed an empty target and then created the schema
through the installed MssqlStore. API/import contained users were granted by
known client SID without Directory Readers. API has reader/writer/ddladmin for
existing startup migrations; import has reader/writer only. The initializer
remains administrator of this isolated proof stack, not the API runtime.

This is a **one-case synthetic infrastructure fixture, with zero staff**,
not a restored private dataset or the continuing 60,000-home/980-case lineage.
The runner refuses unrecognized tables/state before constructing Store.
No private dataset, answer key, roster or backup was opened.

```json
{"check":"sql_private_dns","addresses":["10.40.4.25"],"status":"Passed"}
{"check":"database_preflight","recognized_proof":false,"status":"Passed"}
{"check":"contained_users","count":2,"status":"Passed"}
{"check":"application_sql_state","status":"Passed","cases":1,"staff":0,"marker":"ama-src-private-proof-2026-10-16","seed_available":true,"identity":"initializer"}
```

Separate execution `job-cutover-test-verify-oerk856` succeeded at 14:04:39 UTC
using **API MI**, not the administrator. It reopened MssqlStore with no seed
file, reading the same case/marker and zero staff:

```json
{"check":"application_sql_state","status":"Passed","cases":1,"staff":0,"marker":"ama-src-private-proof-2026-10-16","seed_available":false,"identity":"api"}
```

The source API revision `ca-cutover-test-api--bl42b7u` became Healthy/Running,
with two serving replicas, pinned to the API digest above. Its private origin is
`https://ca-cutover-test-api.jollytree-20e6e99e.uksouth.azurecontainerapps.io`.
Environment DNS resolves inside the VNet to `10.40.0.184`; environment ingress
is internal and public network access Disabled. The source agents app is
provisioned with its digest but remains a scale-to-zero skeleton, not a proven
queue worker. Orchestrator/import job image bindings are separate from actual
functional worker acceptance.

Private smoke execution `job-cutover-test-smoke-pdil7sg` succeeded at
14:11:51 UTC. The app's EasyAuth configuration is enabled, tenant-specific,
bearer-only and Return401; no browser secret/delegated token store was used.

```json
{"check":"api_private_dns","addresses":["10.40.0.184"],"status":"Passed"}
{"check":"health","http_status":200,"expected":200,"status":"Passed"}
{"check":"anonymous_api_denial","http_status":401,"expected":401,"status":"Passed"}
{"check":"malformed_bearer_denial","http_status":401,"expected":401,"status":"Passed"}
{"check":"forged_principal_denial","http_status":401,"expected":401,"status":"Passed"}
```

#### Deployed Smoke: Bounded Infrastructure Passed, Staff/HTTP Blocked

The corrected full workload deployment succeeded at **14:17:06 UTC**.
The final JSON therefore reports the aggregate as **Partially passed**, not
unqualified acceptance. Both ledger alerts are now enabled with corrected
queries; alert delivery and scheduled digest publication were not exercised.

Continuation validation passed **117 offline infra tests**, including ten
runner tests, all Bicep builds/lints and scoped Ruff check/format. The runner
tests include unknown-table refusal before application queries, known assistant
tables, SID validation/idempotence, partial-initialization retry, private
DNS/URL rejection, exact HTTP outcomes and redacted errors. These are separate
from the actual Azure executions, not substitutes for them.

The serving revision was explicitly restarted. Both original replicas
(`...-c9c685d79-9pptb`, `...-c9c685d79-dsdq9`) were replaced by running
replicas (`...-7698b9d7ff-xvgrk`, `...-7698b9d7ff-zzk8d`).
Post-restart HTTP execution `job-cutover-test-smoke-elvbjnq` repeated health
200 and all three 401 checks successfully.

The first post-restart SQL probe `job-cutover-test-verify-qlkf04p` failed
closed in the proof instrument, before reading case/staff bodies: API startup
had added its five expected `assistant_*` tables, absent from the initial
instrument allowlist. Metadata-only execution `job-cutover-test-verify-pwkpi12`
confirmed 16 recognized tables including the sentinel. The runner now derives
assistant table names from installed MSSQL DDL, still rejecting arbitrary
tables; an offline regression covers both branches.

No private registry rebuild or network reopening was used. The corrected
tracked runner was deployed explicitly as the verify job's Python command,
retaining the immutable proof image and API identity. Its source SHA-256 is
`0560f367cf36fa7dd0e850040c55463b712b781a465d1ebd5f4e8de6406cd7e4`.
Execution `job-cutover-test-verify-8ycguks` succeeded at **14:22:48 UTC**:
same synthetic case and marker, zero staff, `seed_available=false`, identity
`api`. No initialization or reseeding ran after restart.

```bash
az containerapp job create -g ama -n job-cutover-test-init \
  --yaml <private-initializer-job-specification> -o none
az containerapp job start -g ama -n job-cutover-test-init
az containerapp job start -g ama -n job-cutover-test-verify
az containerapp job start -g ama -n job-cutover-test-smoke
az containerapp revision restart -g ama -n ca-cutover-test-api \
  --revision ca-cutover-test-api--bl42b7u
az containerapp job update -g ama -n job-cutover-test-verify \
  --yaml <private-job-specification-with-tracked-runner-command> -o none
az containerapp job start -g ama -n job-cutover-test-verify
az containerapp job logs show -g ama -n job-cutover-test-verify \
  --execution job-cutover-test-verify-8ycguks --container proof \
  --tail 100 --format text
```

The private job specifications contain ama resource IDs and MI client selection,
not credentials or datasets; they are not published. The
[infra recipe](../../infra/README.md#private-cut-over-proof-2026-10-16) documents
their inputs and source-command delivery. An initial smoke CLI submission
rejected `--base-url` as a CLI argument; using a generated JSON/YAML job
specification preserved the intended container argument array. No resource
was created by the rejected submission.

Orchestrator execution `job-cutover-test-orchestrator-fquuldv` and importer
execution `job-cutover-test-import-tm1jmkt` succeeded with their source images.
These are CLI-only results: the importer ran `python -m
zava_forward.importer --help`, not an import; orchestration remains a version
entry point, not an accepted scheduler/worker. Agents remain a provisioned
scale-to-zero skeleton. No assertion of four functional workers, real inference,
continuing-stock acceptance or deployed read-only-root enforcement follows.

An additional in-VNet API-MI HTTP attempt
`job-cutover-test-mi-http-4d5qn9m` reached the managed-identity endpoint, but
token acquisition for the identified existing application resource returned
HTTP **400**. No token was printed or exported; no tenant permissions were
added. This is **Blocked**, not authorized HTTP success. Staff initialization
is also **Blocked**: no owner-supplied private roster or approved workbench
registration/Graph permissions are available, and the proof intentionally has
no staff. RG Owner cannot supply these tenant prerequisites. A managed identity
was not bound as a human or granted a fictional staff role. Browser sign-in,
valid-token issuer/audience acceptance and actual staff-authorized API behavior
remain unproved.

Resource IDs are group ID plus `/providers/` and these suffixes:

* `Microsoft.App/managedEnvironments/cae-cutover-test`
* `Microsoft.App/containerApps/ca-cutover-test-api`
* `Microsoft.App/containerApps/ca-cutover-test-agents`
* `Microsoft.App/jobs/job-cutover-test-init`
* `Microsoft.App/jobs/job-cutover-test-verify`
* `Microsoft.App/jobs/job-cutover-test-smoke`
* `Microsoft.App/jobs/job-cutover-test-mi-http`
* `Microsoft.ManagedIdentity/userAssignedIdentities/id-cutover-test-init`
* `Microsoft.Sql/servers/sql-cutover-test-rzsrg/databases/retrofit`

Execution IDs append `/executions/<execution-name>` to their job ID.
The sanitized JSON contains observed image/revision/job bindings and final
resource inventory. Subscription, tenant and Entra identifiers remain
placeholders; command arguments carrying them stay outside Git.

### Retained Resources and Cleanup

The historical captured inventory contained **65 generic resources** inside ama, listed
by ID in the JSON, plus the run-created `budget-cutover-test`. Billable partial
services include ACR Premium, SQL/database, monitoring, storage/private
endpoints and a Foundry account without model deployments. No cost estimate
or successful alert delivery is asserted. The continuation's final inventory
is separately recorded in JSON. The owner explicitly accepts ama costs for
this run; that is not permission for unbounded future spending.
It contains **87 generic resources**, plus the retained budgets
`budget-forward-test`, `budget-cutover-test` and `budget-iot-cutover-test-rzsrg`.
No resource was deleted in this continuation.

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
* [ ] Review the resolved provider registration and private SQL network route,
  including Disabled public access and no policy/tag/firewall bypass or peering.
* [ ] Review the explicit source-image rollout, private health/denial, API-MI
  SQL and restart proof. Separately resolve tenant registration/Graph/private
  roster prerequisites and authorized HTTP/staff acceptance. Confirm each
  workload/job's functional versus skeleton boundary; no public health is claimed.
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
