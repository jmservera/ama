---
title: Source cut-over evidence pack
description: Dated parity, private SQL and public edge proof with remaining owner gates
ms.date: 2026-11-13
ms.topic: reference
---

## Live app verification (2026-10-31, Refs #523 #524 #570 #432)

Observed UTC window: 15:42:51.045838 to 15:45:41.433264 on 2026-10-31.
Owner authorized live checks using the supplied test accounts, at most two
sign-in attempts per account, with no Azure configuration, replica, job or
deployment changes. No such Azure changes occurred. Health warming allowed
idle-start delay; replica state was not inspected or changed, so this is not
a controlled scale-from-zero test.

| Target | Exact deployed origin |
| --- | --- |
| Employee | https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io |
| Resident | https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io |

The [sanitized live result](../../.copilot-tracking/changes/2026-10-31/live-azure-verification-results.json)
preserves each original checkpoint and later employee-only continuations;
the [sole driver](../../.copilot-tracking/changes/2026-10-31/live-azure-verification.py)
contains the exact controls and assertions. Source comparison pin:
`4512193276f18c474af42e37a3cc27357eeef017`. Actual loaded asset hashes below
prove those resident assets match that pin, not that every deployment component
matches it. No credentials, identity claims, cookies, case text, screenshots,
HAR, video or persisted browser sessions were recorded.

| Observation | Result | Exact evidence and limit |
| --- | --- | --- |
| Employee health | Observed pass | Initial `/healthz` HTTP200 in 24.016s; later 200 in 0.153s and 0.157s |
| Resident health | Observed pass | `/healthz` HTTP200 in 38.623s |
| Employee independent identity (#570) | Observed blocked | Captured `az account show --query tenantId -o json` exit0; `az ad user list --filter "startswith(displayName,'Aadi')" --query "[].{oid:id,upn:userPrincipalName}" -o json` exit1 with directory-access-denied predicate true. No raw directory output retained |
| Employee chat, map filters, case (#570) | Blocked, not run | Independent tenant/object expectation unavailable; maintained `verify_employee` not invoked live. Zero employee sign-in attempts; no weakened admission or expectation derived from `/api/me` |
| Employee first-time tabbed case layout/assets (#524) | Blocked, not run | Fresh unauthenticated `/app` navigation did not load workspace assets. No authenticated case/tab navigation, Leaflet delivery or stale-cache recovery proved; no manual reload |
| Capacity and other manager pages (#523) | Blocked, not run | Identity admission prevented authenticated `/api/packages`, `/api/workorders` and manager page checks. Historical local SQL/browser results remain historical |
| AI metering (#432) | Blocked, not run | Manager-only `/api/ai/report` not read without employee admission. No live call joins, limits, prices, billing reconciliation, quality denominator or held-out batch observed |
| Resident sign-in | Observed pass | One submission to `/demo/login`, HTTP200; account and own-content regions visible. Shared synthetic showcase, not real resident identity/enrolment |
| Resident chat open/close | Observed pass | Existing `checks.resident_assistant_browser_check.open_chat` executed: title focused; close hides panel and launcher reopens it |
| Resident chat resize | Observed pass | At 1280x900: panel changed from 448x630 at (816,182) to 1248x630 at (16,182), then 1248x448 at (16,364) using offered width/height range controls |
| Resident dock/undock | Observed pass | Dock pressed=true; 1254x900 panel at (26,0), right edge=1280, height control disabled. Undock pressed=false and height enabled |
| Resident narrow/wide containment | Observed pass | 390x844: 358x448 at (16,308); 1280x900: 1248x448 at (16,364). All measured states contained, no document horizontal overflow |
| Resident first-navigation assets | Observed pass | All five actual first-navigation JS/CSS responses HTTP200 and source-matching; zero script/stylesheet request failures and zero page errors |
| Resident chat answers/AI | Not run | Geometry did not require own-case AI consent or a question. No answer generation, callback booking, consent change or model call was performed |

Resident first-navigation responses, observed at 15:43:55Z on 2026-10-31:

| Asset | Bytes | SHA-256 |
| --- | --- | --- |
| `/demo.css` | 8775 | `7a1e73a926f230cc61ec3398ee135bf8370a875b44cb54783faa6c8ec2891b09` |
| `/chat-widget.css` | 5300 | `e9be468cb6119a5997cceee8630887973150b5e0f4c755f9491e73de82e20dfd` |
| `/assistant.js` | 15297 | `9493a357fe93ba29da27c6dcbedf65fe02e01901e25b3188c50223dfd7ff8477` |
| `/chat-widget.js` | 9866 | `6c37bd91b51134ebb1aebbe1e9fe1c7c688bba09601e44dacb9cd683275d1960` |
| `/demo.js` | 17305 | `9801816f1609d39d73e4ddd5640433d42fdbfa108a9584ae6d50235cf47eb429` |

Reproduction uses an external Python 3.12 venv, pip-installed `src/core`,
`src/agents`, `src/api[dev]` and installed Chromium. Credential files are read
only inside automation. From the repository root, with that venv on PATH:

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=src/api:src/api/tests:src/core/tests:src/agents/tests \
timeout 1200 python .copilot-tracking/changes/2026-10-31/live-azure-verification.py --run
```

The committed result prevents replay/reset: do not delete or overwrite it to
get new sign-in slots. Two employee-only continuations repaired the local
credential parser (the employee file contained only a password) and established
the directory denial without consuming an employee attempt; resident's one
attempt and original observations were preserved. The initial writer used
append-mode checkpoint output; the corrected driver uses locked read/write
output with fsync and retains the original checkpoint stream as nested
evidence. These were automation defects, not deployed product bugs.
Credential-free self-tests check persisted count==2 refusal and overwrite
validity; they do not constitute live acceptance.

Issues #523 and #524 explicitly allow their final live-record criterion to be
marked pending the owner. Only that record criterion is ticked, with
authenticated verification still pending independently verified expected
tenant/object IDs. Both remain open; a tick is not a claim their live page
works. #570 and #432 receive blocked live-evidence comments and no new criterion
ticks. No new deployed product failure was observed, so no fabricated or
duplicate bug issue is filed. The identity dependency is retained on #570.
Resident geometry evidence is also recorded on related #550 without claiming
its bundled employee/chat criteria.

Fresh-context resident success does not prove all historical caches,
employee assets, whole WCAG conformance, real-resident acceptance, production
capacity, AI activation, economics, legal compliance or human release approval.
Full local gate and hosted/human publication checks are separate from this
live observation and are not implied by it.

### Later local publication-gate failure (2026-10-31, Refs #608)

The full local gate at candidate
`37cc1fed15a95f1bc84e82135b0c496862867e85`, base
`7136be9778b17e495b1941e6eb93f50d32de8a2b`, failed separately from the
live app observations. Project/static/infra/migration and image groups passed;
browser failed and SQL was blocked by its prerequisite. This is not a full
passing receipt or a deployed Azure application defect.

At 16:26:24.224183 to 16:27:48.426292Z, the persistent Chromium launch in
`checks.case_journey_browser_check` aborted with
`chrome/browser/process_singleton_posix.cc:315: Socket path too long`,
SIGABRT. The accepted long external output root made the Chromium
`TMPDIR/.../SingletonSocket` pathname too long. Exact external evidence:
`rpi-live-full-main-integrated/receipt.json`, log `0157-browser.log`,
SHA256 `24620a9b6a4c69b8e8c6bc68ece24d7d6fa876a3f35095a4ebb17fbbef9e5a2e`
under this task's session files.

The deduplicated [local tooling bug #608](https://github.com/jmservera/ama/issues/608)
records reproduction and open criteria. A short external output retry is
required; no source patch, browser/SQL skip, partial-gate substitution or
successful retry is inferred here. Main advanced twice during publication;
integration uses additive topic merges, not rebases, force pushes or main
mutation. A changed base/candidate invalidates resume eligibility and requires
a fresh full run. The original Review and failed receipt remain preserved.

## Live employee acceptance (2026-11-02, Refs #570)

Observed UTC time of the run: about 09:32-09:34 on 2026-11-02. The owner
authorized live Azure checks with the supplied employee test account. One
sign-in was made against the exact employee origin in the table above; no
Azure configuration, replica, job or deployment change occurred. `/healthz`
returned 200 on the first warm-up attempt. Deployed code is the main build
recorded for #749 (`1a644d317`), not a controlled scale-from-zero test.

| Observation | Result | Exact evidence and limit |
| --- | --- | --- |
| Independent identity | Observed pass | Directory lookup was still denied (`az ad user show`, insufficient privileges). The expected object ID came instead from an `id_token` issued by the Entra token endpoint for the test account, in tenant `bccd6ad2-b77b-461c-bbc5-5b032e7930ba` (the Azure CLI tenant), before the application was contacted. It was held only in process memory and never copied from `/api/me`. |
| Strict admission | Observed pass | `authenticated`, `expectedIdentity`, `employeeRole`, `notViewOnly`, `providerMatches`, `schemaValid` all true. `displayEmailMatches` and `rosterBound` false, as designed: Entra identity and role bind the account, not the roster |
| Chat | Observed pass | Skill selection, send and reply passed. The reply label was workflow-only (`workflowOnly` true, `actualAiLabel` false), so no live AI generation is claimed |
| Map filters | Observed pass | Strict stage covering the six flags: payload, list, marker and status agreement |
| Case view | Observed pass | Strict case stage passed |
| Today's briefing | Observed pass | Read-only; no review action taken |

Method: Chromium started headless with a loopback debugging port and a fresh
temporary profile; sign-in through the Entra form; then
`python3 -m checks.employee_live_acceptance --origin <employee origin>` from
`src/api`, exit 0, `passed` true. The profile and driver were deleted. No
credentials, tokens, identity claims, cookies, case text, screenshots, HAR,
video or raw bundles were retained. Only fixed booleans are recorded here.

Limits: one account and one session; desktop viewport only; no Azure-side
telemetry cross-check; no real-resident data. This is the evidence for #570
criterion 3. It does not change #523, #524 or #432, which remain open.

## Transport integration qualification (2026-10-30, Refs #360)

Current main and the private Blob transport branch are integrated without
rewriting their original evidence. The
[transport evidence map](../../infra/README.md#transport-evidence-and-integration-2026-10-30-refs-360)
preserves DN1-DN5, private/no-key/no-tag controls, bounded complete results
and offline-only proof. Main's later `src/` cut-over, identity, IoT and release
records remain authoritative for their dated scopes; the historical proposal
does not undo directory retirement or prove this transport live.

The [rubric incident diagnosis](../../.github/rubric/README.md#pr-423-invalid-d1-details-2026-10-30-refs-360)
records an invalid extra D1 `evidence2` key, not a measured score regression.
Removing that field only in a diagnostic replay yields 77 versus 77; no
scorecard is repaired or published here. Actual hosted scoring, current-head
publication gates and live/human acceptance remain separate.

## Decision and Scope

This section records the original 2026-10-16 decision boundary. For the later
owner sign-off and directory retirement, see the
[2026-10-27 record](#owner-authorized-directory-retirement-2026-10-27).
Original failures, outcomes and unchecked historical gates below are preserved.

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

## Bounded RG Publication Continuation (2026-10-19)

Refs #360, #349 and sequenced #358. Original base:
`634a024d97d2da7168b8a7d5f343ab26e6108cf3`. This is a new bounded RPI loop,
not a rewritten verdict for #375/#379/#381/#385/#391. Research, one original
plan critique, implementation and one later original Review are separate dated
tracking evidence. The new RG resource authority removes the former missing
publication-route authorization only. It does not supply technical acceptance,
tenant/Graph rights, resident data permission or human release approvals.

| #360 criterion | New evidence | Disposition |
| --- | --- | --- |
| a/b | Prior merged private-backing/direct-ingress source retained;233 focused publisher/proof/IAM/setup/staff/auth tests pass, zero skips | Source evidence only; no new setup completion |
| c | Owner explicitly permits necessary operations within ama, excluding RG deletion; minimum publisher/cost/rollback researched | Resource authority resolved; technical route not verified |
| d | Direct four-route probes each403; existing Graph application-read failed; both exact VM provider preflights failed capacity | **UNMET**; no health200, real session/roles, SQL persistence or real task-bound AI acceptance |
| e | Existing Front Door and old stack retained; no deletion | **UNMET**, verification-before-retirement still applies |
| f | Dated runbook/ADR/evidence/KB update preserves historical failures and new contradictions | Bounded documentation delivered, not whole issue closure |

Current ACR is Premium/UK South, Disabled public access/bypass None, no agent
pool/VM publisher. Initializer remains on old proof digest `ef0058f8...`,
demo API on `111b2622...`; neither was updated or started. The
[tested allocation candidate](../../infra/private-proof-publisher.bicep) isolates
the temporary VM in a dedicated subnet, denies all inbound and adds no IAM or
backing-service resources. Actual B2als_v2 and then D2as_v5 exact preflights
returned `InvalidTemplateDeployment / SkuNotAvailable` for capacity. Unrestricted
SKU metadata/quota were therefore insufficient. No successful what-if, create,
temporary resource, AcrPush assignment, source upload, build, push, digest
pull/run or image pin occurred.

No unchanged historical host endpoint or default-pool publication attempt was
repeated. The [runbook](../../infra/README.md#bounded-private-publisher-capacity-attempt-2026-10-19-refs-360)
records researched pricing, conditional recovery and explicit fresh-capacity
requirements; no guest watchdog or billing-bound claim is made without an
allocation. Exact private operator inventory and failed responses remain
external/mode0600, without committed IDs, tokens, roster or raw app payload.
Unused task-owned SSH keys were removed. Final management readback found zero
owned resources/no deployment record, unchanged subnet objects and registry
public/bypass/policies, all six backing services private, Front Door and `ama`
retained. No cloud cleanup deletion was needed.

The authorized tenant operator must still establish real single-tenant app,
provisioning permissions/consent, private vault credential and staff bindings,
then execute real browser/role/SQL/AI checks. Existing token acquisition without
Graph roles/scopes does not satisfy them. #358's live Key Vault-reference
preservation round-trip remains separately sequenced. Local SQL/browser/image
engineering checks and later complete local gate are not live acceptance, full
WCAG conformance, vulnerability-free certification or human approval.

### Later outbound source restriction (2026-10-19, cycle2)

The independent exacthead assessment closed the earlier resource-relationship
test gap but found unrestricted outbound defaults in the unused VM template.
The later source correction permits TCP443 only to recorded private ACR
`10.40.4.20/.21`, Azure DNS TCP/UDP53, WireServer TCP80/32526 and IMDS TCP80;
explicit remaining platform-service denials and deny-all outbound precede NSG
defaults. No backing service, inbound allowance, exact-RG guard, resource
relationship or IAM resource changed. The retained public IP is not permission
for Internet/package traffic. See the
[enforced policy and limitations](../../infra/README.md#explicit-outbound-restriction-2026-10-19-cycle2).

Package bootstrap is intentionally blocked: no verified offline Docker/tool
route exists for the stock pinned Ubuntu image. This is not an approved
deployable publisher. NSGs do not provide package FQDN, DNS-payload or registry
content filtering; WireServer guest-agent traffic is NSG-exempt. Supported
agent redirection of extensions is documented, not observed here. Exact
private endpoint identities/IPs and VNet DNS need future independent
revalidation before allocation. Broad Internet/Storage/AzureCloud access is
not an accepted workaround.

No Azure write/deploy/what-if/new capacity attempt ran in cycle2. Both original
UK South `SkuNotAvailable` results, zero allocations, old image digests,
Graph403/direct403 and all tenant/privacy/human gates remain unchanged.
Original Research, critique and Not accepted Review remain immutable; later
source/mutation evidence does not retroactively accept that original outcome.

## Existing-Resource Preservation Preflight (2026-10-19)

This section records the14:19-14:24Z no-write window. The later separately
authorized [synthetic roundtrip](#real-temporary-synthetic-preservation-roundtrip-2026-10-19)
adds real-provider component evidence without rewriting this result or its
original Partial / Residual Review.

Refs #358, base `7f96d9957b28cb174aa759c842376f24087d71a3`.
This is a new actual read-only investigation, not a rerun or replacement of
the original offline delivery or adverse reviews. The owner authorizes
operations within existing ama except RG deletion; this supplies no Graph
authority and does not justify changing credentials, bindings or runtime just
to obtain a preservation result.

| Actual observation | Result and limit |
| --- | --- |
| Production source path | `preserve_app_secrets` plus existing configuration/`Azure.rest` ARM PATCH has no intrinsic image/Graph dependency; full `secret_reference` mutation creates a Graph password and full setup has broader effects |
| Exact-version existing app GET | At14:19:11Z, actual production `Azure.rest`, API2025-07-01: demo API, old API and agents all explicitly `secrets: null`; zero KV URL/identity pairs, env/init, scale-auth and registry-password secret bindings |
| API auth metadata | Both APIs: zero client-secret refs; token store disabled, no SAS binding. Agents auth GET returned sanitized request error, not a successful empty inventory |
| Exact app-scoped permissions metadata | Read/write/listSecrets actions allowed in metadata; no actual listSecrets/PATCH, policy/deny/provider success not proven |
| Nonproduction qualification | All three have test/non-production-demonstrator/constructed-non-identifying labels; actual demo `require_demo` refuses unknown/malformed deployment template/parameters. No guard bypass or positive guarded profile claim |
| Final management read | At14:24:58Z all compared null/count/latest/ready/lock/handoff fields equal initial observations; all apps Succeeded and latest==latestReady |
| Literal live criterion | **Blocked / Not run**: no actual pre-existing KV pairs, unrelated secrets or app secretRef bindings to preserve. Empty rebuild/clone/new sentinel state is not substituted |

The current primary blocker is **absent populated existing target state**, not
an established image/Graph prerequisite or tested ARM permission denial.
The profile-guard refusal is independently retained as roster-setup evidence,
not a universal preservation prerequisite. Full setup, its guards and #374
source/tests are unchanged. No source defect was demonstrated.

All reads captured CLI output privately and emitted only reference/count/state
summaries. Qualified external session records are retained in directory0700,
files0600: initial management summary, profile-guard summary and final
management summary. No raw app payload, IDs, token, plaintext secret, private
roster/dataset or `.env` was saved or published. A first local projection
failed on null initContainers before summary generation; the corrected
production-boundary read supplied the actual evidence.

No listSecrets, preserve-helper live round-trip, Graph/password, SQL write,
deployment/PATCH, image publication, restart/traffic/identity mutation,
network/policy/bypass change, resource creation or deletion occurred. Thus no
cloud rollback/cleanup was needed; ama and Front Door were untouched.
Four run-generated local bytecode files were removed individually; no secret
request/backup files or cloud locks were created.

See the [runbook safety boundary](../../infra/README.md#existing-resource-preservation-preflight-2026-10-19):
ordinary secret edits do not create revisions, but versionless KV refresh may
restart env-secretRef revisions and PATCH may be asynchronous. No such update
was tested here. A later actually populated eligible target requires fresh
exact-target plan/critique and comparison, or separately scoped approval for
representative-state preparation; do not fabricate literal existing-state proof.

This blocked no-source/no-cloud-change result has no review-ready publication
candidate or full-gate receipt. The owner's no-heavy-gate exception applies
only to this local blocked disposition; later publication retains all normal
frozen-candidate/gate/coordinator requirements. #358 remains unmet; no whole
#360/demo, browser/role/SQL/AI, retirement or human acceptance is claimed.

## Authenticated Roster Transport Design (2026-10-20)

Refs #360. Design for review only, per the owner planning direction of
2026-10-20. The [runbook design](../../infra/README.md#authenticated-roster-result-transport-design-2026-10-20-refs-360)
records the preserved three failed recovery attempts (2026-10-19), the
unchanged original roster, the unresolved question of which code path those
attempts ran, an options comparison, the proposed ARM tag relay with a binding
extension, five decisions needed (DN1 to DN5), a script-oriented plan and the
tenant-administrator checklist.

| Item | Status |
| --- | --- |
| Transport executed or retried | No |
| Parser relaxed, ciphertext decrypted, cloud state changed, secret or private data read | No |
| Relay carried a result live | Never observed; 2026-10-17 grant readback only |
| Worker/image binding | Unresolved gap: self-asserted by the worker until independent provenance exists |
| Cost and execution plan | Separate later approval; not a dependency. Spending gate: all-in USD 500 TOTAL October, accrued plus forecast across all scopes, headroom unknown, RG-only projection USD 535.41 above cap |
| #360 c, d, e | Unproved and unchanged |

Process disclosure (2026-10-20): the first draft of this entry and the runbook
design was written without activating the RPI skills; its critique and review
were not genuine RPI outcomes. A recovery cycle re-verified the evidence and
corrected two statements. Independent verification is pending.

## Private Blob Result Transport (2026-10-22)

Refs #360. Owner decisions DN1 to DN5 (2026-10-22) superseded the ARM tag
relay above. The [runbook design](../../infra/README.md#private-blob-result-transport-2026-10-22-refs-360)
records the private-Blob design, the offline implementation and the live
prerequisites. The 2026-10-20 entry and the three failed attempts stay as
dated history.

| Item | Status |
| --- | --- |
| Offline code, Bicep and fake-client tests | Implemented |
| Live private routing, managed-identity write, operator read, real job | NOT RUN |
| Deployment, role grants, Azure spend | NOT RUN, awaiting coordinator release of a finite plan |
| Historical failures | Unknown transport failures; root cause is production follow-up |
| Correction 1: Blob read bound to the selected operator profile, explicit timeouts and overall budget with cleanup | Implemented offline (fake clients); live NOT RUN |
| Signed source or image attestation | Unverified, deferred (DN5) |
| Demo screen-reader acceptance | Unverified production follow-up |
| #360 c, d, e | Unproved and unchanged |

## Real Temporary Synthetic Preservation Roundtrip (2026-10-19)

Refs #358. Later owner direction selected an isolated temporary synthetic
baseline in the existing internal/private Consumption environment, not changes
to any running app. Supplemental research, amended lifecycle plan and one
independent new-material safety assessment preceded resource writes. Original
critique and original **Partial / Residual** Review remain byte-identical.

| Actual primary observation | Result and boundary |
| --- | --- |
| Private lifecycle prerequisite | Local authenticated vault metadata was network-denied and existing private-endpoint TCP timed out. A new synthetic-only private manual job successfully read exact absent-name metadata (versions200/empty, deleted404) before any vault secret allocation; no existing job/exec was reused |
| Minimal authority | Dedicated temporary MI; Secrets Officer only over the single new synthetic secret, AcrPull only over the existing private registry. No existing identity or subscription/tenant grant changed |
| Baseline established | SecureString incremental ARM deployment what-if proved exactly one owned-secret Create; deployment Succeeded and supplied an actual versioned URI. New no-ingress app Succeeded at15:06:41Z with one KV reference pair, one unrelated random local secret and one unused env secretRef to that local secret |
| Production boundary exercised | Fresh actual GET/listSecrets, unchanged `preserve_app_secrets`, then unchanged `Azure.rest` PATCH of `properties.configuration` only at15:06:42Z; no `secret_reference`, addPassword or full setup |
| Async completion and exact comparison | Actual GET observed InProgress through15:07:04Z, then Succeeded at15:07:07Z. Fresh GET/listSecrets matched exact KV URL/identity, known random resolved KV value, unrelated random value, configuration, template/unused binding, identity, tags and latest/ready revision; all eight comparisons passed |
| Runtime/cost qualification | Existing private image reused by digest, benign Python sleep command,0.25vCPU/0.5GiB, no ingress/rules, min0/max1. One replica was actually present at readback; min0 was not zero execution. Four total preflight/cleanup executions across operator corrections used timeout120/retries0; no premium service, new environment/vault/network or settled zero-cost claim |
| Exact cleanup | App, synthetic secret (active AND soft-deleted states), secure deployment history, private job/executions, MI and both final role assignments removed by15:09:10Z. All ten exact role UUIDs across earlier cleaned incarnations independently re-read RoleAssignmentNotFound |
| Existing-resource preservation | All11 existing app/job configuration/template/identity/tag/readiness/active-revision snapshots match; full RG resource-ID membership and top-level existing environment/vault/registry hashes match. No existing workload, real secret, private dataset, Graph, network/public-access/policy or RG deletion |

The temporary names were `ca-issue358-synth-20261019-1450`,
`job-issue358-synth-20261019-1450`, `id-issue358-synth-20261019-1450` and
`issue358-synth-20261019-1450` for the vault secret/deployment. Exact resource
and role IDs, ownership/absence/lifetime journal and comparison hashes remain
external0700/0600; synthetic values/tokens were never logged or committed.
Sanitized primary observations are also included in the candidate's dated
execution evidence for reviewer access, rather than requiring external-only
summary reads or claiming a replacement independent Review.

Operator-only corrections are retained: exact not-found classification, an
HTTP400 unsupported job-start `volumes` field, log framing and the metadata
API's valid200-empty absence shape. The exact-owned-execution Log Analytics
query was denied `InsufficientAccessError`; direct owned console capture
provided the actual subsequent evidence. These were not production helper
defects. Every failed allocation attempt was cleaned before continuing.

**Passed: real temporary synthetic baseline component roundtrip.** It was a
real resource populated before preservation, not a mocked PATCH, but it was
created for this exercise. It is not the originally described populated
deployed-app/token-store case, full credential rebuild, runtime token usability,
roster-profile repair, browser/SQL/AI/human or whole-demo acceptance. #358 stays
open pending coordinator judgement of this bounded evidence and any remaining
original criterion. Frozen exact-HEAD full local gate/receipt and coordinator
assessment remain separate publication gates; no push/PR/merge/status change
is authorized here. See the [runbook qualification](../../infra/README.md#real-temporary-synthetic-preservation-2026-10-19).

## Credential Preservation Offline Follow-Up (2026-10-17)

Refs #358. This is a focused continuation of merged #356/#352, based on
`abaca7881e2a4a77eacf865fe235d4af9196643f`, preserving merged #370 staff-job/CI
behavior. **Partial issue delivery: actual non-production preservation remains
UNMET.** No live Azure/Graph/SQL command, secret/private dataset read, role or
network change, build, new spend or resource mutation was performed.

| Requested criterion | Evidence and status | Unmet boundary |
| --- | --- | --- |
| Stored-but-expired guard | Offline fixed-clock generated and legacy selected-name cases cover past, exact expiry, absent expiry and strictly future credentials across check/dry-run/apply; old credentials retained. Both expiry bypass mutations fail assertions | No real credential/token exchange tested |
| Preserve KV references during rebuild | Actual source reconciles known app KV URL/identity with full, sparse name/value and omitted-KV list responses; captured PATCH and backing store retain exact pairs, ordinary values (including empty), env secretRef and auth token-store refs | Actual service round-trip Not run; public schema only describes allowed fields, not deployed preservation |
| Fail safely | Malformed/duplicate/incomplete/conflicting inventories stop before addPassword. List denial and PATCH failure retain old configuration/auth. Missing/altered readback refs prevent auth switch, including reruns; one-shot read failure can recover without another password | Cloud failure/propagation behavior and operator recovery Not run |
| Verify without reading write-only values | Positive fake GET projection omits all ordinary values; exact name/KV verification succeeds and clears the reference-only handoff digest | Not proof of app-local secret value usability |
| Preserve legacy CLI/conflict resolution | Existing delegation/options/return-code regression plus 17 callback-helper tests pass; initialize-api-auth.py unchanged | Merged #352 already resolved the historic conflict; no duplicate CLI implemented |
| Required local gates | 15 assertion failures before the source fix, zero runner errors; 101 setup and 313 total infra tests pass with Bicep required; seven safeguard mutations killed by behavioral assertions; scoped lint/types/CLI and existing Bicep build/lint pass | Offline evidence only, not browser/tenant/SQL acceptance or human sign-off |

The public [2025-07-01 Container Apps schema](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/app/resource-manager/Microsoft.App/ContainerApps/stable/2025-07-01/ContainerApps.json)
(retrieved 2026-10-17) defines `SecretsCollection.value` and optional per-entry
`name`, `value`, `keyVaultUrl` and `identity`. No Azure management endpoint or
`listSecrets` was called live, and no values were output. Earlier failed Learn
URLs were not treated as evidence.

Exact remaining criterion: on an **already authorized existing non-production
target**, demonstrate that a real rebuild preserves every prior KV
`keyVaultUrl`/`identity` pair and app secret reference/value usability, retaining
only sanitized reference-level before/after evidence. The safe scope and
permission to perform such a round-trip were not available under this task's
explicit no-Azure-write/no-secret-read limits. Do not alter/delete real secrets,
open private services, provision a test resource or infer approval from an
offline pass. Owner/coordinator must arrange a separately permitted safe scope;
a read-only schema/configuration inspection cannot meet this criterion.

Coordinator sequencing: #360 owns broader setup/job readiness and its live
acceptance. This change touches only setup's credential preservation/recovery
helpers and their existing suite, not job transport, crypto, roster, identity or
network policy. Reconcile the narrow shared setup/test changes before advancing
that broader loop; this audit grants no deployment or merge approval.

## Laptop Setup and Restricted Migration Readiness (2026-10-17)

This is the original #375 readiness receipt. For the later API-only IAM
activation, see [Scoped Initializer IAM Activation](#scoped-initializer-iam-activation-2026-10-17).
Its API-grant status supersedes the historical absent/unattempted statements
below. The [subsequent relay delta](#approved-existing-job-relay-delta-2026-10-17)
supersedes only the relay authorization/grant status; all live d/e gates remain unmet.

Refs #360; coordinated with #349/#350 and #358. This section supersedes only
the console/credential transport limitations and migration status in the dated
sections below. It does not replace their observations or assert owner sign-off.
The full RPI task delivers a management-plane-only laptop path: the existing
initializer relays bounded authenticated ciphertext in per-run ARM tags;
Key Vault receives a minimal secureString ARM deployment with reviewed
single-secret Create scope and verified metadata. Neither requires laptop
access to private console, Log Analytics or vault data-plane endpoints.
No clear roster/key/credential is placed in tags, arguments, logs or artifacts.
The [current runbook](../../infra/README.md#in-vnet-sql-staff-step-refs-360)
documents the normal command, prerequisites and bounded cleanup.

Live read-only discovery confirmed the ARM Log Analytics proxy is still
network-restricted, even for a constant query; this avenue was rejected.
A real selected-vault what-if through the new adapter passed; the subsequent
PUT was intercepted before sending. No secret was created and no credential
exchange was claimed. The new transport is locally tested, **not live proven**:
the retained proof image predates its worker and the narrow grants are absent.
The fresh role what-if for `ca-cutover-test-demo-api` and `job-cutover-test-init`
has exactly two custom role definitions and two resource-scoped assignments.
It was **not applied**; explicit role activation authorization is still needed.

The authorized additive API migration passed an exact two-Create what-if and
created only `ca-cutover-test-demo-api` and its auth child in the existing
external environment. Deployment `demo-stage-360-20261017` is Succeeded;
the replica is Healthy/Running. Readback preserved the old app/auth pre-apply
fingerprint and copied API image/template/runtime configuration/identity/auth,
apart from reviewed direct-ingress/environment/tag changes and Azure's
`maxInactiveRevisions=100` default. The staged ingress rule
`setup-pending-deny-all` denies `0.0.0.0/0`. Without following redirects,
`/`, `/healthz`, `/api/me` and `/app` all returned **403** at
`ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io`.
That is restriction evidence, not welcome/health 200 or real authentication.
The app still has a managed-identity client sentinel and no browser credential;
the rule must remain until real operator setup and reviewed exposure.

SQL, Key Vault, storage, ACR, Foundry and IoT each still report public network
access Disabled. No SQL/private dataset query, live worker run, Graph write,
secret write, image build/push, role assignment, exposure transition or resource
retirement occurred. The old API, environment and Front Door remain; `ama`
must never be deleted.

| #360 criterion | Current evidence | Status and remaining boundary |
| --- | --- | --- |
| a: direct-demo infrastructure and private backing services | Existing Bicep guards retained; all six live public-access flags Disabled; external environment already existed | Source/local delivery complete; no full-stack redeployment or broader privacy certification |
| b: direct/edge setup and one-command initialization | Existing setup paths retained; ARM ciphertext/secure credential transport, verified same-VNet parent discovery, no app fallback, cleanup and failure regressions | Local delivery complete; live tenant/worker/credential/restart execution Not run |
| c: owner-approved migration plan | Explicit owner continuation/migration approval; exact narrow what-if followed by verified deny-all staging | Approved additive step done; image publication path, IAM activation and later exposure remain gated |
| d: welcome/health, login, roles, SQL and AI acceptance | Restricted routes 403; no 302 or fixture accepted as sign-in | **UNMET**. Real operator registration/login, private staff/SQL/restart, runtime/model and browser/per-role evidence required |
| e: old stack/Front Door retirement after d | Nothing retired; source resources preserved | **UNMET**, correctly blocked by d and exact destructive-scope review |
| f: runbook, ADR and evidence | Current runbook/ADR, this audit and reference routing updated; historical observations retained | Documentation delivered; no claim all live criteria pass |

At the PR #375 evidence point, image publication was blocked: private ACR had bypass None and no private task
pool/task, while local Docker is permission-denied. An authorized existing
private publisher must supply/pin the proof digest without a new paid service
or public-access workaround. An IAM owner must separately authorize/apply the
reviewed source-job-only tags and selected-demo-API restart grants. Then a human
tenant operator uses the single runbook command, isolated login and existing
private roster/authorized mailbox-purpose decisions. No SP Graph mutation or
human approval is simulated. Only after auth/runtime verification and fresh
exact exposure review can real browser/SQL/AI acceptance and retirement proceed.
Issue closure remains with the coordinator; this delivery uses Refs #360.

The [later normal-Docker follow-up](#normal-docker-private-publication-follow-up-2026-10-17)
supersedes the socket-denial observation, not the unmet publication outcome.
The #379 receipts below supersede the historical IAM approval blockers.

PR #375 same-session integration continuation (2026-10-17): rebased onto
`51db4fa80a29528f5a3d19420b1c7e1597d27213`, preserving merged #373 sensor
changes and #374 expiry/inventory/digest/readback/legacy contracts and all their
evidence. Added combined ARM/preservation regressions, not changed upstream
tests. The original Review is historical, not an independent assessment of the
new head; reviewer `4536f9cc` remains independent and prior findings are not
discarded by rebase.

The [concrete publisher/IAM evidence](../../infra/README.md#private-publication-blocker-evidence-2026-10-17-pr-375-continuation)
distinguishes actual Docker socket permission denial, anonymous registry403
and GitHub package-read403 from **unattempted** default Tasks/import (unsupported
under unchanged private networking) and IAM activation (explicit approval
boundary). Existing CI retains reports, not publishable proof images; no private
pool/task/self-hosted runner or ama builder VM/ACI was discovered. No claim that
a build/import/IAM mutation failed when it was not sent. Current continuation
made no Azure resource/credential/role/data changes; d/e remain UNMET.

## Scoped Initializer IAM Activation (2026-10-17)

This API-only receipt predates the [subsequent explicit relay approval](#approved-existing-job-relay-delta-2026-10-17).
Its absent/unapproved relay statements remain historical, not current blockers.

Refs #360. Starting main: `e065ecd2c5b09b0f4bc22bfbfdb343e41910189b`,
including merged #375. This follow-up follows ordered Research, Plan,
Implement and independent Review; the source review before live apply is
a separate gate, not a substitute for final Review. It does not duplicate
the merged staff transport or credential implementation.

The owner answered boolean true to deploying only reviewed API read/restart
and temporary staff-job lifecycle permissions in `ama`, with no broader
roles/networking/spend/deletion. Research found that the merged template
also granted tags/read and tags/write on the **existing** initializer job.
That separate grant was treated as unapproved, not silently included.
Temporary-job lifecycle belongs to the operator and is not a worker MI
grant in this template; no additional lifecycle role or job was created.

One boolean opt-out, default true for compatibility, conditions both relay
resources. Independent standard source review passed before live deployment;
the API-only invocation explicitly set `includeResultRelay=false`. The
[exact runbook receipt](../../infra/README.md#scoped-initializer-iam-activation-2026-10-17-360)
records the command, IDs, actions and boundaries.

| Live proof | Outcome |
| --- | --- |
| Exact reviewed API-only preview | Succeeded; two Creates (role definition and demo-API assignment), 94 same-group Ignore rows; no workload/network/tag changes |
| Apply | `staff-iam-360-api-20261017` Succeeded, correlation `2177965b-1d42-4709-962b-3475e2186264` |
| Principal | Existing `id-cutover-test-init`, `3830883a-f4af-44f8-bff8-8859b78fc2f8`, ServicePrincipal |
| Role / scope | `0d8c4586-d46e-514c-9c19-680d9f068755`; sole assignable scope `ama`, actual assignment only on `ca-cutover-test-demo-api` |
| Assignment | `3a7e0803-3997-5cbe-af9c-c9776b37f3a7`; exact principal, role and API scope read back |
| Actions | Container App read, revision read, replica read, revision restart/action only; no dataActions/exclusions |
| Relay | Role `64ec5d6d-f8ae-51ab-a93a-394f6cc97c6c` and job assignment `8e9a497e-3b90-50e2-a783-93e58755165b` absent |
| Preservation | Existing AcrPull retained; no old-API/job assignment; both APIs' observed environment/revision/ingress metadata unchanged, demo deny-all retained |
| Resource writes | Two RBAC Creates plus pre-existing empty-resource guard deployment metadata only; existing initializer MI resolved by Read |

The provider returned the role's canonical subscription-level definition URI,
with unchanged GUID and **only ama in assignableScopes**. The initial
RG-URI-only verification assertion failed after successful create; read-only
canonical-ID and operation-kind checks then completed. This was a verification
normalization, not an Azure denial or authorization expansion. No second
deployment, wildcard role, tenant role or broad fallback was used.

Local source gates passed: 11 identity matrix tests, 48 compiled Bicep/guard
tests including two new semantic/mutation regressions, Bicep build/lint and
scoped Ruff/format. Missing source packages and Ruff were restored only after
observed dependency failures, in a session-only venv. This is offline/source
evidence plus actual role readback, not runtime staff acceptance.

The permission configuration slice succeeded. Existing-job relay activation
still requires exact owner approval; private worker publication still requires
an existing authorized private publisher. No new builder was started. No
Graph/SQL/Key Vault secret reads, restart, temporary job execution, browser
acceptance, image build, network change, spend or deletion occurred.
MI propagation/exercised rights remain untested by design. #360 d/e are
**UNMET**; resource group `ama`, old stack and all human approval boundaries
remain intact.

### Approved Existing-Job Relay Delta (2026-10-17)

Refs #360, continuing PR #379 after publication completed at
`38e6abf5246a231b871d00d5e7bb1a3402094be8`. Original full RPI and independent
Review are preserved; this is an approved P04 scope delta with targeted
final-state review, not a fabricated first or repeated full Review.

New owner boolean true explicitly permits only the existing initializer MI
to read/write encrypted result tags on the existing initializer job, with no
plaintext secrets, job configuration rights, new workload resources or broader
scope. No Bicep source change was needed; the actual reviewed parameter
`includeResultRelay=true` enables the previously omitted grant.
The [exact relay runbook](../../infra/README.md#approved-existing-job-relay-delta-2026-10-17-360)
records commands and full principal/resource scope.

| Scope delta proof | Observed outcome |
| --- | --- |
| New grants | Role `64ec5d6d-f8ae-51ab-a93a-394f6cc97c6c`, job assignment `8e9a497e-3b90-50e2-a783-93e58755165b` |
| Exact actions / principal | Microsoft.Resources/tags/read and tags/write only; existing initializer principal `3830883a-f4af-44f8-bff8-8859b78fc2f8`, ServicePrincipal |
| Scope | Sole assignable scope ama; assignment only at existing job-cutover-test-init |
| Fresh preview | Two exact relay Creates, 95 same-group Ignore/NoChange, one proven API assignment no-op reported raw as Modify |
| API no-op proof | Whole before/after equality after resolving exact MI reference/canonical role URI; principalType NoEffect; independent actual API role/assignment match against original receipt |
| Apply | staff-iam-360-relay-20261017 Succeeded, correlation `53c578e1-bea0-4655-a9ff-ce574b995d6b` |
| Independent readback | Separate ARM reads verify role/action/scope/principal; only new MI assignment is relay; previous API grant/AcrPull exact |
| Preservation | Existing job identity/environment and observed old/demo API environment/revision/ingress metadata unchanged; demo deny-all retained |
| Source | Reviewed Bicep/guard source hashes unchanged; no new standard source review needed |

Deployment logs label idempotent existing API/empty guard PUTs Create too;
this is not a new API grant. Raw what-if Modify and actual before/after
proofs are retained, not converted into a claimed two-row raw preview.
Only two effective grants were new; no arbitrary Modify or unrelated resource
creation was accepted. The guard contains no workload resources.

No tag payload read/write or secret-bearing test, MI token/propagation test,
temporary job, job configuration write/run, secret/Graph/SQL access, restart,
image build, network/new infrastructure/spend/deletion or human browser
acceptance occurred. The action-based RBAC role cannot enforce ciphertext
content; encrypted-only use remains an owner/application boundary, not a
claim of content-filtered permission enforcement. Actual encryption/runtime
acceptance remains untested.

Prior RV-001 is resolved only for exact permission authorization/configuration.
Private image publisher RV-002 and genuine tenant/runtime acceptance RV-003
remain unproven; #360 d/e remain **UNMET**. Old stack and ama retained.

## Normal-Docker Private Publication Follow-Up (2026-10-17)

Historical #381 evidence. The private-route-only conclusion below is superseded
by the [current actual hosted CLI attempt](#renewed-initializer-acr-cli-attempt-2026-10-17);
the prior endpoint measurements and unperformed-command status are preserved.

Refs #360, source baseline `b15f2f00e48300c4cf74815d7586ba84f61ee1d4`
after merged #375/#379. Owner authorization covers normal private publication
and conditional image-only pin, not route repair or workload execution.
The [exact runbook and conditional commands](../../infra/README.md#normal-docker-private-publication-follow-up-2026-10-17-360)
record the safe boundary and actual immutable references.

| Evidence | Actual outcome |
| --- | --- |
| Normal Docker | Server 29.9.0; docker group verified, no privilege escalation; old socket blocker resolved |
| Private ACR restrictions | Public Disabled, bypass None, admin false before/after |
| Existing DNS/NIC | Login `10.40.4.21`, UK South data `10.40.4.20`; ordinary host DNS resolves publicly |
| Reachability | Public login HTTPS403; both exact private-IP HTTPS connections time out at 10 seconds, no TLS established |
| Authorization | Normal authenticated ACR login/push not attempted; no IAM denial claimed |
| Packaging correction | Remove two directory-wide ignore exceptions; native local scratch/COPY audit now includes exactly seven intended files, no unrelated scripts/pyc |
| Source checks | 83 focused tests pass, zero skips; five no-network source imports and two isolated source-help checks pass |
| Real image delivery | Retained-base proof build/import/help/nonroot smoke, push, new tag/digest and pin Not run |
| Preservation | Two read-visible job fingerprints match; old image, Manual initialize args, identity, complete template/configuration/environment preserved within no-write window |
| Demo API | Existing `setup-pending-deny-all`, Deny `0.0.0.0/0` retained; auth unverified |

The only Docker builds were local, network-disabled `FROM scratch` / COPY
context audits, with no RUN/entrypoint execution, cloud upload or container
start. Both exact named audit containers/images and test scratch were removed.
These audits and source checks do not establish behavior of the unavailable
real proof image, secret-payload equality, image-pin idempotency or staff setup.
No SQL/private dataset, secret payload, Graph, job start, API restart, role,
resource/network change, new spend or deletion of the old stack occurred.

Ordered Research, Plan, Implement and one post-implementation Review retain
the concrete private-route blocker. An already existing authorized private
publisher must supply working private connectivity, a source-SHA-tagged
validated image and immutable digest before the existing Manual job can be
considered for image-only pin. The job's historical `initialize` args must
never run implicitly. #360 d/e and genuine browser/role/SQL/AI acceptance remain
**UNMET**; nothing here authorizes exposure or retirement.

## Renewed Initializer ACR CLI Attempt (2026-10-17)

Refs #360. Current source baseline `bab4bf3a2ac9ec030d78d27063d1390f800c5c7c`
preserves merged #375/#379/#381, retained immutable API base, upstream Python
pin/security-upgrade source and seven-file proof context without source changes.
The [current commands and exact error](../../infra/README.md#renewed-initializer-acr-cli-attempt-2026-10-17-360)
supersede the assumption that VM private TCP443 failure establishes hosted Tasks
unavailability. Independent ARM readback confirms historical `dbb` Succeeded,
ordinary cpu2, 2026-10-16T13:53 and old proof digest; that is not current proof.

| Current evidence | Result and boundary |
| --- | --- |
| Local retained-base build | Actual Docker attempt failed at base manifest HEAD with firewall403; no real proof image or actual image smoke |
| Exact CLI upload preflight | Seven unique regular paths/SHA256, committed-source bytes equal; duplicate identical Dockerfile archive member disclosed |
| Current hosted command | Actual source upload 20.157 KiB succeeded, ordinary cpu2 QuickRun `dbc` queued |
| Current agent logs | Source download and Docker setup succeeded; registry login `/v2/` returned 403, run Failed after six seconds; no build/push/output digest |
| Localhost source smoke | Current installed source, one fictional case/zero staff, AI off/no SQL: welcome/health200, anonymous protected endpoints401; not real-image/browser/SQL/AI evidence |
| Existing initializer preservation | Full read-visible projection SHA256 before/after `fbc548ae52b49563b3e6c3c8d0c0cd2ecec8b1d04f8f4c109d9fff77b1c5908e`; unchanged old digest/Manual initialize args/settings/identity/environment/configuration, no update/start |
| Restrictions | Registry public Disabled/bypass None before/after; activated #379 permissions retained, no IAM change |
| Regression | 83 focused infra tests pass, zero skips after missing-package recovery in worktree-local pip venv |

No new published tag/digest, pin or image-validation acceptance exists.
Registry login403 does not by itself distinguish network policy from identity.
No new pool, public access, bypass, IAM, infrastructure or workload modification
was attempted. The authorized source upload and failed existing-service build
are the only Azure write operations. No secret payload, private dataset, SQL,
Graph, API restart, job execution, exposure or retirement.

Future pin requires a single source/run/digest identity record and actual
payload-hash/UID/import/help/localhost smoke on that exact hosted digest; source
smoke and a separately built image cannot substitute. **#360 d/e UNMET**.
Owner/operator tenant context and separately authorized retirement remain
human gates. Old API/edge and resource group ama are untouched.

### Read-Only Registry403 Root Diagnosis and PR385 Integration

Coordinator-authorized continuation2026-10-17, no repeated full RPI or Review.
Clean topic60134c5 integrated onto verified origin/main
`bbbc9243505b606550327c64bf5429243f457f2e`; intermediate rebase head6311b51
is an integration head, **not** tested/built source. Historical dbc receipt
still records `bab4bf3a2ac9ec030d78d27063d1390f800c5c7c`, original base/payload
hashes and results, byte-identical to prior PR385. Original single Review
Complete/Residual work remains historical and unchanged; coordinator's external
final-head review is pending, not Pass.

Likely explanation is now narrower: the original deployment record says dba/
dbb images were captured before registry isolation. Current ARM metadata shows
registry writes after dbb (first completed October16 13:56:53, after13:53:24
success). This supports later isolation as the cause of current default-agent
login403; metadata alone does not identify the changed property or daemon token.
Current registry is publicDisabled/bypassNone/LegacyRegistryPermissions. Both
runs are QuickRun Linux/amd64/cpu2 with no named task/pool, current task/pool
lists and ama VM inventory empty. Caller actions["*"] supports management
operations, not proof of hosted data-plane auth; no RBAC denial is established.

[Exact read-only diagnosis and options](../../infra/README.md#initializer-registry403-read-only-diagnosis-2026-10-17-360)
cite Microsoft private-build, Tasks-specific bypass and VNet-pool guidance.
Task bypass property is absent in preview GET, not literal false; the documented
unset-SAMI deny rule is a candidate condition, not a proven identity or
guaranteed trusted-services toggle fix. UK South is not in the published pool
preview region list; no existing private publisher or same-region new pool is
assumed available. Existing externally owned runners are outside inspected
inventory, not proven nonexistent.

No new Azure writes/build/log payload/secret/identity claim/private-data/
initializer/API/network/IAM activity in this continuation. Preferred next
decision is identify an existing authorized private-connected publisher; otherwise
retain blocker while separately appraising explicit pool cost/region/network
or task-bypass security exception. No option is authorized here. Actual image
smoke/digest/pin and #360 d/e remain **UNMET**, old API/edge/ama untouched.

## In-VNet Staff Initialization Offline Follow-Up (2026-10-16)

Refs #360. This offline change supersedes only the earlier absence of private
staff-job transport. No live Azure command, image build, tenant change, SQL
binding, restart or permission activation was performed. The
[runbook](../../infra/README.md#in-vnet-sql-staff-step-refs-360) documents the
single command and exact prerequisites/fallback.

| Requested criterion | Offline evidence | Unmet or unverified boundary |
| --- | --- | --- |
| Explicit mode and automatic blocked-local continuation | `--run-in-azure` bypasses local SQL; failed read-only local candidate/check attempts may switch to a job. Validation failures stop; uncertain local apply never switches/retries | Actual laptop/private-job execution Not run |
| Reuse API environment, init job/image and SQL-admin identity in ama | Fake az verifies exact resource IDs, matching VNet/subnet, one expected init MI, SQL administrator principal/tenant, Entra-only SQL, Disabled public access, database and pinned proof image | Actual deployed asset/version/admin/image availability Not run; cross-environment reuse refused |
| Candidate listing, existing seeded roster and operator-only Entra work | Candidates returned privately; Azure listing prints count only. Existing admin/seed/persisted-roster regressions retained. Operator resolves people and reconciles all directory grants; worker has no Graph client/profile/token | Actual mailbox classifications, directory authority and real users Not run |
| Private roster transfer without identity CLI/log disclosure | Mode-0600 body files, Container Apps secretRef input, fresh AES-GCM key, authenticated/chunked encrypted results and codes-free output tested with canaries | Console logs use an authenticated environment endpoint, not ARM alone. Actual operator reachability and completed-run log/retention behavior Not run |
| Bind, independently verify and restart API in job | Worker tests use canonical protected SQL preparation/atomic install, post-commit reread, no-op restart and failure-before-success. Existing restart tests verify serving replicas. API-only MI restart role compiles offline and is recorded in the role matrix | Real Azure SQL transactions, provider action authorization and fresh live replicas Not run. Required role/image deployment is not performed |
| Failure, timeout and roster cleanup | Fake az exercises job failure, lost create/start response, log failure, timeout, handled interruption, collision, stop failure and delete denial. Success requires confirmed deletion of owned job/secret; source job untouched | Hard kill/power loss cannot guarantee cleanup; serialized manual stop/delete and check-first recovery documented. Live deletion/retention Not run |
| No SQL/Key Vault networking changes | All transport writes in fake az target only owned temporary jobs; Bicep adds only narrow role definition/API assignment and scope guard | No live configuration inspection; existing network assertions are not a fresh deployed compliance check |
| Required local quality gates | Targeted and full infra suites, responsive loopback auth tests, scoped Ruff/mypy and standalone offline Bicep build/lint are recorded with the delivered changes | Passing fakes are not deployment, real browser acceptance, security certification or human sign-off |

`--check` remains read-only for Entra/SQL/API replicas, but its Azure path
necessarily creates/removes temporary jobs/secrets. `--dry-run` never creates
jobs and cannot claim private SQL evidence it could not obtain. Historical
claims below that both modes make no cloud mutations predate this distinction.

The initial proof image inherits installed zava_forward packages and the SQL
driver, but did not contain the staff scripts/manifest. The Dockerfile now
adds those assets while preserving its proof entrypoint. No live image build,
registry opening or source-job image update was attempted. The existing SQL
administrator receives no Graph permission or broad Contributor grant; the
optional standalone Bicep assigns only reads/restart on the selected API.
Deployment remains an authorized operator prerequisite, not an inferred approval.

All live and owner-sign-off criteria stay unchecked. This change activates
no legal rule, resident consent, safety decision or financial commitment.
ADR 0005 remains accepted for synthetic development only; Juan Manuel Servera
is the exercise Legal, Compliance and DPO owner, with real owners/sources still
a gap before operational reliance.

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

## Soak and Cut-Over Evidence Preparation (2026-10-21)

Refs #201. Preparation only, at base
`993a7b88c03f5240f1e7a4c7c7afa7c064281622`, following the owner direction of
2026-10-20 in [#126](https://github.com/jmservera/ama/issues/126#issuecomment-6290697705)
to propose a soak duration and cut-over evidence checklist for review. This is
not a soak, not acceptance and not sign-off. No Azure, paid, tenant, private
data, backup, tag, release or deletion action occurred, and no budget headroom
is inferred: the USD500 total cap (expiring 2026-10-25T16:02Z) is already
forecast to be exceeded, so any soak needing running resources requires a
separate, affordable, finite plan approval. Evidence for this section is read
only: repository files and read-only GitHub queries on 2026-10-21. Method and
sources are in the dated RPI research record for this task.

### Original 11 Acceptance Criteria Map

Closed status vocabulary: every criterion is `UNMET` overall. The evidenced
component records only what the cited source proves; the unmet component keeps
every missing, stale or unverified part visible. No box in #201 is ticked here.

| # | Criterion | Source, date, revision | Evidenced component | Unmet component | Status | Human owner |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Layout ADR accepted | [ADR 0006](../adrs/0006-src-layout-and-cutover.md), 2026-10-15; #201 comment 6196711316 | Acceptance recorded | A1-A5 placement exceptions and the partial assistant rebuild are not ratified | UNMET | @jmservera |
| 2 | `prototype/` retired | Commit `a7e30046` (#295), 2026-10-15; `mvp/` tracks only `README.md` | Directory absent; content mapped in the matrix | Agreement on each retire row and the service-role denial gap are not recorded | UNMET | @jmservera |
| 3 | Parity matrix complete | [Current Parity Audit](#current-parity-audit), [audit TSV](./cutover-parity-audit.tsv), pack revision of 2026-10-16 | 130 rows each migrated, mapped or retired; 578 historical paths mapped; no missing destination | Matrix is a migration record, not acceptance; owner agreement on retire rows not recorded; audit not rerun at this base | UNMET | @jmservera |
| 4 | Tests migrated and passing in CI, coverage equal or greater | [Local Validation Ledger](#local-validation-ledger); `src-ci.yml` | Test count 1,164 (104 skips) on named runs against baseline 719 (92 skips) | Measured coverage equivalence not established; no CI result on a candidate commit; CI runs on pull requests only | UNMET | Coordinator, @jmservera |
| 5 | CI, Docker, Bicep, scripts repointed; src build deployed and healthy | [Public Browser Restoration](#public-browser-restoration-2026-10-16), [Bounded RG Publication Continuation](#bounded-rg-publication-continuation-2026-10-19) | Repointing evidenced; private health 200 and native API 401 on 2026-10-16 for one fictional case | Health proof is historical; later publication failed; initializer and API on old proof digests; no real staff sign-in (#349); feature acceptance blocked (#350) | UNMET | Tenant operator, @jmservera |
| 6 | Rubric tracks `src/`; before and after comparison recorded; dip cause and recovery recorded | `.github/rubric/artifacts.json` registry; `.github/rubric/scores/latest.json`; history in git | Registry includes `src/**/*`; snapshot 47 at `fa730d63` (2026-10-15), 48 from `b1fd9042` (2026-10-16) to `332101ed` (2026-10-20), rubric_version 2; no dip observed | No score on a candidate commit; baseline comparability unverified; floors not met ("Incomplete (thought leadership artifact not submitted)"); cause and recovery statement not recorded for sign-off | UNMET | @jmservera |
| 7 | Dependent epics #113, #136, #165, #157, #149 have no open work on old paths | Read-only GitHub, 2026-10-21 | Open PRs 420 to 426: none changes `mvp/` or `prototype/` paths; all five epics are open | Epic open state is not completion evidence; refresh at sign-off | UNMET | @jmservera |
| 8 | Docs, ADRs, index, log and live instructions updated; links checked | [Reference inventory](./cutover-reference-inventory.tsv); this section, ADR note, index row and log entry | Inventory exists; reconciliation added with a focused local link check | Live workflow names retained until the single rename PR; full link and gate checks are external | UNMET | Coordinator |
| 9 | Archive tag `v<BRD version>` confirmed | BRD `0.18.0` (2026-10-15); no `v*` tag locally or on origin on 2026-10-21 | Prospective name `v0.18.0` only | Not confirmed at cut-over; tag and release not created | UNMET | @jmservera |
| 10 | Private `mvp/data/` relocated and backed up outside git | Owner checklist below | Nothing an agent may verify | Owner-only non-sensitive attestation; no agent read the dataset or backup | UNMET | @jmservera |
| 11 | Owner signs off in the issue | #201 comments (four, last 2026-10-16) | None | No sign-off exists or is inferred | UNMET | @jmservera |

### Dated Corrections and Contradictions

* Soak: the owner decided on 2026-10-15 that there is no minimum soak
  ([comment](https://github.com/jmservera/ama/issues/201#issuecomment-6196800819),
  ADR 0006, matrix), but the #201 body still lists "Minimum soak period" as an
  open decision and the owner asked on 2026-10-20 for a proposal. This is an
  unresolved contradiction, not resolved here. Minimum duration stays OPEN.
* Rubric: the statement below that no post-migration numeric comparison is
  available predates later snapshots. A snapshot pair now exists (47 then 48)
  but no candidate-commit score does, so the comparison remains unmet.
* Open pull requests: the initial inspection below is superseded for 2026-10-21
  by the read-only check above; epics remain open.
* CI: `src-ci.yml` triggers on pull requests and manual dispatch only; the last
  `main` push run was 2026-10-18 at `612cbed7`. Candidate CI evidence must come
  from pull request checks and the external gate receipt for the exact commit.
* Health: private health 200 (2026-10-16) is historical and is not staff
  sign-in, feature acceptance or current health.

### Proposed Soak Evidence Specification (for owner review, not started)

Every row is a proposal, not an owner rule. `OPEN (owner)` means no value is
proposed and none may be assumed.

| Element | Proposed content |
| --- | --- |
| Candidate revision | Full 40-character git SHA on `main`, the four workload image digests, the infra commit and the BRD version, all frozen for the window |
| Environment | Named non-production synthetic environment inside `ama`; identifiers in an external mode 0600 receipt with a sanitized summary committed beside [cutover-azure-evidence.json](./cutover-azure-evidence.json); no private, resident or staff data |
| Entry and start | Start only when AC 4 and 5 are evidenced for the exact SHA (pull request checks, external gate receipt, deployment of those digests), an authorized tenant operator has completed real staff sign-in (#349) and a finite costed plan is separately approved; the collector records the UTC start |
| Window | Kind (none, event count, calendar), length, consecutive or cumulative: OPEN (owner) |
| Health signal | Deployed `/healthz` on each path under test plus the protected API 401 canary; cadence and miss tolerance OPEN (owner) |
| Parity signal | `python -m zava_forward.core.synthetic.cutover_audit` without drift; authenticated positive-role smoke; one SQL restart-persistence check on the fictional case |
| CI signal | Proposed set: `src-ci.yml`, `mvp-ci.yml`, `mvp-validation.yml`, `infra-plan.yml` green for the SHA; required set OPEN (owner), as rulesets are warn-only per #323 |
| Rubric signal | Scorer run on the SHA compared with the committed snapshot 48 (A30 B13 C5 D0, `332101ed`, 2026-10-20); comparator basis and dip cause and recovery expectation OPEN (owner) |
| Old-path signal | Refresh of the open pull request and file scan for #113, #136, #165, #157 and #149 at start and end |
| Failure and reset | Proposed reset-class: any `src/`, infra or image change to the candidate, auth bypass, SQL public access enabled, data loss, or health failure beyond the OPEN tolerance. A new SHA restarts the window. A single transient miss within tolerance is logged only. Thresholds OPEN (owner) |
| Rollback | Keep `ama`, delete nothing, follow the recovery baseline in the [Issue 344 Acceptance Audit](#issue-344-acceptance-audit) (`Return401 / NoProxy` and the seven exact public exclusions) |
| Escalation | Coordinator notifies the owner in #201 immediately on a reset-class failure; a cost overrun stops collection under the approved plan |
| Collector and reviewer | Collector: OPEN (owner). Reviewer: independent of the collector, OPEN (owner). Approver: @jmservera, confirmation pending (checklist item 1) |
| Retention | Sanitized JSON committed; raw receipts external and uncommitted |

### Pending Owner Decisions

All are Pending. None is decided or inferred. The evidence needed is an owner
comment in #201 (or the named human action). They supplement, and do not
replace, the sign-off checklist below.

| ID | Decision | Owner |
| --- | --- | --- |
| D1 | Whether any soak is required, reconciling the 2026-10-15 "no minimum" with the open item and the 2026-10-20 proposal request: A none, B event-count window, C calendar window | @jmservera |
| D2 | Window length and unit if B or C | @jmservera |
| D3 | Consecutive or cumulative, and whether the reset follows any `src/` change or only a deployed-artifact change | @jmservera |
| D4 | Probe cadence, miss tolerance and path scope (private, public edge, both) | @jmservera |
| D5 | Entry conditions and who authorizes the start | @jmservera |
| D6 | Collector and independent reviewer assignment | @jmservera |
| D7 | Finite costed plan and funding beyond the USD500 cap and its 2026-10-25T16:02Z expiry; tenant operator for staff sign-in | @jmservera, tenant operator |
| D8 | Rubric comparison basis, and recorded dip cause and recovery expectation | @jmservera |
| D9 | Service-role denial gap disposition | @jmservera |
| D10 | Confirm the cut-over approver in #201 | @jmservera |
| D11 | Archive tag and release at the BRD version current at cut-over | @jmservera |
| D12 | Private data relocation and encrypted backup: owner-only non-sensitive attestation | @jmservera |
| D13 | Agreement on each `prototype/` retire row and the A1-A5 placements | @jmservera |
| D14 | Retained `ama` resources and charges: remediation, retention or ID-scoped cleanup, never deleting `ama` | @jmservera |
| D15 | Approve the separate single-pull-request post-cut-over workflow and check rename plan | @jmservera |
| D16 | Tenant registration, real staff sign-in and feature acceptance (#349, #350), then the final go/no-go in #201 | @jmservera, tenant operator |

## Other Cut-Over Gates

> Superseded in part by
> [Soak and Cut-Over Evidence Preparation (2026-10-21)](#soak-and-cut-over-evidence-preparation-2026-10-21)
> for the open pull request check and the rubric comparison status. The
> historical text below is unchanged.

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
* [ ] Review the [proposed soak evidence specification](#proposed-soak-evidence-specification-for-owner-review-not-started)
  and decide D1 to D16 in [Pending Owner Decisions](#pending-owner-decisions);
  no soak has started and no duration is chosen.
* [ ] Explicitly record go/no-go and sign-off in #201. Only a later authorized
  #202/#203 change may remove legacy paths; this PR never performs deletion.

## Owner-authorized directory retirement (2026-10-27)

Refs #199. Refs #200. Refs #201. Refs #202. Refs #203.
The owner explicitly **SIGNED OFF cut-over (#201) on 2026-10-27** in the
retirement task direction. This later authority permits directory retirement;
it supersedes the earlier unsigned deletion status, not the original technical
results, unresolved human/operational gates or historical unchecked checklist.
No new soak, deployment, private-data inspection or backup verification ran.

Fetched `origin/main` at `65a514ed20e97816dbf47e9fb981ab4cfe40597d`
already contained all executable migration: the five installed source projects,
source-context Dockerfiles, source CI and new Bicep job module paths.
Only `mvp/README.md` remained tracked; `prototype/` was already retired by
`a7e3004` / #295. This retirement removes that pointer, not application code.
Working data remains external through `ZF_DATA`; no agent read a private dataset.

The current BRD frontmatter is `0.21.0`. Local annotated tag `v0.21.0`
was absent and was created at the main SHA above, the last pre-deletion commit
containing the pointer. It archives the pointer-era tree; earlier code remains
in its Git history. Neither tag publication nor a GitHub release was performed.
The owner publishes the tag with exactly:

```bash
git push origin refs/tags/v0.21.0:refs/tags/v0.21.0
```

### Remaining-reference policy

Current build/test/deploy commands use `src/` and installed `zava_forward`
packages. Workflow/check names remain unchanged, including dispatch-only legacy
workflow files. Do not remove required contexts or rename them during cleanup.
The rubric registry already includes source projects, not legacy directories;
deleting the unscored pointer adds no loss of scored source coverage. A measured
post-merge score comparison is still required; no score or recovery is invented.

Intentional old-path occurrences remain in dated ADRs, parity/audit TSVs,
reports, pinned GitHub URLs and original RPI evidence. The append-only log
retains old links with an additive repair map in its 2026-10-27 entry.
Historical `zavaforward_mvp`/`properwarm_mvp` strings in migration fixtures and
the cut-over audit parser test historical inputs, not live imports. Defensive
`mvp/data` ignores/refusal checks and obsolete registry excludes remain to
prevent accidental private-data reintroduction. Archive `v0.21.0` supplies the
cut-over boundary for these intentional exceptions; earlier pinned commits
remain the authoritative source for their original executable content.

### Acceptance boundary

This maintenance change supplies source-reference reconciliation, local
archive creation, pointer deletion and current navigation. Existing API,
rename and narrow parity/registry tests are the scoped validation; no full
gate is authorized for this task. Hosted CI and owner merge remain required.
It does not prove all-suite baseline parity, fresh deployed health, release
publication, every dependent-epic disposition or post-merge rubric comparison.
Accordingly all five issues are referenced, not closed. The literal zero-token
repository-wide criterion in #203 is not claimed complete: preserved history
and defensive fixtures are explicit exceptions.
## First Bounded Local Stabilization Checkpoint (2026-10-23, #440)

**Executed, partial; not a product or release pass.** This checkpoint assesses
merged-main runtime inputs, separately from the proposed coordinator policy.
No issue/epic criterion was ticked, no cloud action or paid inference ran, and
no resident, professional or release approval is inferred.

### Source, coverage and requirement baseline

Fresh `origin/main` before testing and after the run:
`140d8f494482c78e84d15f3d46b9223d3c487af0`, tree
`e4910768767a071827a771d9c0c919451cccae57`. Focused tests used an external
exact-main export, installed distributions and constructed fixtures. The native
runner requires a clean commit: preliminary policy/evidence head
`d8a6506100c56c9454a85bcc31bac11d56b4a3bc`, tree
`681da68894aa36082d84bfe4f4b15f45502e5992`, was frozen for its entire run.
Its diff from main contained only the existing coordinator, `src/README.md`
and this issue's tracking evidence. All application, test, dependency, tool,
workflow and executable build inputs were identical to main. The external
allowlist proof is `/tmp/ama-440-preliminary-identity-20261023.json`.
The receipt binds that preliminary head, **not literally main HEAD and not a
final publication candidate**. Subsequent checkpoint-documentation commits
invalidate any publication eligibility independently of its failed status.

Bounded recent merged coverage is #419 / #221 (incident/restart source,
`993a7b88c03f5240f1e7a4c7c7afa7c064281622`), #418 / #220 (resident
challenge/correction, `7e95f0224bfb7a8a62990a1de162fbcfa68db539`), #427 /
#151 (contrast correction, `9e55a392b95c90730c6410b9a4db4ad3a5ae70ce`)
and #414 / #413 (native gate,
`fa659cfd021100f7c64f8ec73bbff76c03adf234`). Requirements amendments #433 /
#432 are at the source pin; #431 / #122
(`3deb179d57b6520e114a27862f79ca95399f833e`) remains a custody proposal,
not observed recovery-service delivery. Older merged runtime code supports
the tested welcome, session, proposal, import and persistence boundaries;
this is not exhaustive feature, PR or acceptance coverage. Unmerged #437 and
all sibling-branch functionality are excluded. #349, #350 and #360 remain
open live-acceptance gaps, not new duplicate bugs.

| Baseline document | Version/status at source pin | Git blob |
| --- | --- | --- |
| [BRD](../brds/agentic-retrofit-programme-brd.md) | Draft 0.19.0, 2026-10-22 | `e96c4b16010f47a8ce01b29a9c208e4b3bb34319` |
| [Demonstrator PRD](../prds/zava-forward-retrofit-programme-demonstrator.md) | Candidate 0.18.0, 2026-10-22; historical exercise acceptance of 0.12.0 does not accept this delta | `a1fa17ab39924bb4bed7cd92c7bf2c8c79772410` |
| [ADR 0001](../adrs/0001-azure-architecture.md) | Proposed, dated amendments | `9f53b5b6ee36ff0a21854c3058e10c55e3bd7835` |
| [ADR 0002](../adrs/0002-pilot-readiness-architecture.md) | Proposed, dated shared-API realization | `e6c8ce004e04dd0aeda3beafc01719ebe81c927a` |
| [ADR 0003](../adrs/0003-journey-derived-capabilities-runtime-fit.md) | Accepted with Basic IoT Hub amendment | `6044e1061f45964393e649aefa80b2293644d58f` |
| [ADR 0004](../adrs/0004-per-user-agent-chat-and-memory.md) | Accepted staged | `259358e53e37ddeade73f9ee3aafd8dcacea20f9` |
| [ADR 0005](../adrs/0005-regulatory-compliance-assistant.md) | Accepted synthetic-development scope only | `4d610335a5a18bb282e29c6cb3053404beda995d` |
| [ADR 0006](../adrs/0006-src-layout-and-cutover.md) | Accepted layout/dependency boundary | `a5063f8f31c79044137b529145fbef7667841305` |

Document-qualified IDs below are traceability, not new document approval,
legal-currentness confirmation or activation of operational controls.

### Actual local commands and outcomes

Focused environment: `/tmp/ama-440-focused-20261023`, Python 3.12.3, installed
all five `src/` distributions with pip after the chosen import probe actually
failed `ModuleNotFoundError: zava_forward`. No `PYTHONPATH=mvp`, default/private
dataset, private roster or `.env` was used. From each exported component,
the installed interpreter ran `-m unittest -v` with these exact selector sets:

| Component | Selectors | Actual result |
| --- | --- | --- |
| API | `test_auth.ProxyHttpTests`, `test_auth.PasswordProviderTests`, `test_auth.TrustedProxyTests`, `test_assistants.ContractTests.test_every_capability_failure_disabled_and_malformed`, `test_assistants.DurabilityTests.test_schema_failure_disables_assistance_not_manual_reads`, `test_assistants.ApiTests.test_invalid_payload_and_store_failure_leave_manual_api_available`, `test_assistants.ReviewTests.test_independent_qa_reviewer_and_separate_human_verification`, `test_resident_api.ResidentApi.test_live_local_http_decision_pause_redress_and_restart`, `test_workflows.SqlFlows.test_safety_flow_blocks_booking_until_released_by_someone_else`, `test_ai_tasks` | 60 passed, 16.309s, exit0 |
| Core | `test_sqlstore test_recovery test_dependency_rule` | 32 passed, 9.258s, exit0 |
| Importer | `test_excel_transition test_dependency_rule` | 32 passed, 0.118s, exit0 |
| Orchestrator | `test_digest_blob test_token_store test_document_rescan_job test_source_monitor test_dependency_rule` | 44 passed, 4.744s, exit0 |
| Agents | `test_ai_identity test_dependency_rule` | 6 passed, 0.069s, exit0 |

API used fixture-only `PYTHONPATH=tests:../core/tests:../agents/tests`.
The five existing component discoveries used the installed interpreter,
`-m unittest discover -s tests -q` and documented shared fixture paths.
Final standalone outcomes: core1243/307.123s, skipped167; agents105/18.226s;
API959/386.227s, skipped301; orchestrator46/4.863s; importer39/0.147s.
All exited0: 2392 discovered, 468 skipped, 1924 executed successfully.
Skipped checks are not passes.

The original archive-only core run failed three tests and errored once:
Git audit/provenance and repository-output guards require Git metadata.
Restoring metadata from the exact local pin, preserving erroneous generated
outputs externally, then running all four focused failures and the full core
suite resolved them without source edits. Intermediate mistyped-SHA/import-path
and stale-fixture retries are retained, not hidden. Logs are
`*-focused.log`, `*-suite.log`, `core-harness-reproduction*.log`,
`core-suite-git-aware.log` and `archive-harness-artifacts/` under the focused
directory. These harness failures are not confirmed application bugs.

The existing native gate then ran once, 13:10:49-13:41:44Z:

```bash
python3 tools/rpi-checks.py --all --base 140d8f494482c78e84d15f3d46b9223d3c487af0 --out /tmp/ama-440-preliminary-20261023-d8a65061 --lock-timeout 0
```

**Exit1, failed receipt preserved.** Sixteen groups passed; `project-core`
failed one benchmark. The runner continued its other groups rather than
converting the overall result to success.

| Native result | Exact evidence in native output directory | Classification and limitation |
| --- | --- | --- |
| Core1243/361.428s, one failure, skipped167 | `0012-project-core.log`: `test_sqlreads.Scale.test_sql_reads_at_60000`, filtered page17383.017630ms, required strictly below1500ms | Local observed failure; core Ruff/format/mypy were not reached in this group |
| Agents105, API959 skipped301, orchestrator46, importer39; all exit0 | `0018`, `0027`, `0036`, `0045` component logs; their Ruff/format/mypy commands passed | Local observed; integration skips remain qualified |
| Namespace, static, infra and migration groups passed | Receipt command ledger; static runner12 tests, infra368 tests; offline Bicep build/lint and workflow inventory | Local observed, not Azure deployment/what-if |
| Actual Chromium design-system and regulatory UX harnesses exit0 | `0139-browser.log`, `0140-browser.log`, `regulatory-ux-results.json`; Chromium156.0.8078.4, pinned axe4.10.3 | Local observed, synthetic changed surfaces only; 19 scans, zero reported violations, ten color-contrast incomplete observations needing manual review |
| Actual disposable SQL Server244/378.736s, exit0, skipped1 | `0155-mssql.log`; owned loopback SQL container and random credentials, seven existing SQL selector groups | Local observed persistence/proposal/review/ledger parity; one JSON-only separate-file audit test deliberately skipped, not SQL proof |
| Four Docker/non-root contracts and separate API logo-mode0600 contract passed | `image-api`, `image-agents`, `image-orchestrator`, `image-importer`, `logo-0600` receipt groups | Local observed startup/negative-probe controls, not deployed workload equivalence |
| Four configured scanner gates and SPDX reports produced | Each component `*-gate.json`, `*-all.json`, `*.spdx.json` | Local observed: zero fixable HIGH/CRITICAL under configured gate; full reports retain residuals, not vulnerability-free certification |

Native output and retained environments:
`/tmp/ama-440-preliminary-20261023-d8a65061`.
Failed receipt SHA256:
`ce6ff80079f2086b49159dd33a9d208fb1f328998de1d4cc85dd14de8b2990a9`.
The official `--verify-receipt` with that `receipt.json` and the same current
base exited1: `Receipt does not establish a complete passing run`.
Verification output is `/tmp/ama-440-preliminary-verification-20261023.log`.
There is **no eligible final receipt**.

After the gate released its lock, a nonqueued focused invocation repeated
`test_sqlreads.Scale.test_sql_reads_at_60000` three times in the exact-main
focused environment. All three passed in55.045s; filtered measurements were
108/106/108ms, with the original1500ms assertion unchanged. Full standalone
core had also passed earlier. These retests do not repair the failed receipt
or prove the cause of the17.383s observation. Contention and suite-order effects
remain unproven possibilities; bounded host-tool image restores overlapped
the native run, so environmental interference cannot be excluded.

### Requirement, architecture and journey reconciliation

| Qualified requirement / decision | Planned boundary and actual local observation | Remaining gap / classification |
| --- | --- | --- |
| PRD FR-003, AC-004/005, NFR-003; ADR0002 | Public feedback-first welcome, protected workbench/API, missing-principal401, dev-cookie expiry and trusted-proxy role/case denial exercised by focused `test_auth` and browser harness | Local observed only. Real Entra callback/session/role provisioning blocked under #349; historical #350 redirect is not JSON/API acceptance |
| PRD FR-028/044/047, AC-030/052/058-061; BRD RULE-018, FR-044 | Disabled/malformed/schema/storage/provider failures preserve manual reads and explicit AI status; independent proposal QA/human-verification separation, unchanged controlled state and durable proposal evidence tested locally and in SQL | Local observed scripted/model-off behavior. Real task-bound AI, task quality/value and deployed AC-057 blocked/unverified under #360, not accepted from mocks |
| PRD FR-045/046; BRD CON-006/RULE-006 | Local HTTP supplied measure decision/pause/redress/restart and scoped safety/booking hold; unrelated choices and manual paths remain separate | Local observed constructed decisions, not actual resident consent, appointed professional review or witnessed restart |
| BRD RULE-020/024; #221 | Incident/restart guards and distinct-authority fixture checks included in package suites; emergency/manual routes independent | Actual OD-35 named acceptance/thresholds and controlled restart remain blocked/unknown; synthetic reviewer cannot release work |
| PRD FR-001/005, NFR-010; ADR0002/0006 | SQLite reopen/recovery plus actual SQL Server store, ledger, assistant durability/review/API tests | Local observed parity, not production Azure SQL identity, backup/restore or deployed restart acceptance; #350/#360 remain |
| PRD FR-030; ADR0006 supporting importer boundary | Import quarantine/preparer-reviewer refusal, retained source/history and namespace contracts exercised; portable exports are a separate PRD obligation | Local observed library/API support, not complete import UI/worker/approval-channel delivery |
| ADR0006 | Five installed distributions and namespace/dependency tests; workloads depend on core, temporary API-to-agents edge allowed; no workload-to-API | Local observed accepted layout. Cohesive core is an accepted trade-off, not evidence demanding speculative decomposition |
| ADR0001 versus ADR0002 | Shared API proposal realization tested; orchestrator digest/token/rescan/source and importer interfaces exercised with local/mocked providers | Separate autonomous worker/identity estate remains proposed/deferred, not delivered by skeletons or unit tests |
| ADR0003/0004/0005 | Existing synthetic sensor, staged chat/memory and compliance-assistant guards fall within component/regulatory harness scope | Live Hub transport, privacy/human gates and qualified legal/RAI acceptance remain implemented-unverified, blocked or deferred as applicable; no operational-law approval |
| BRD FR-052/NFR-012, PRD Tokenomics amendments from #433 | Pinned requirement delta reconciled against existing proposal usage controls | Full all-in cost/value reporting deferred to existing #432, not a newly discovered regression or inferred acceptance |

No new `Azure observed` row exists. Complete all-in headroom is Unknown despite
the USD700 replacement ceiling and unchanged 2026-10-25T16:02Z expiry. Cloud,
Graph, tenant, paid inference and private-data operations were not authorized
or executed. Staff comprehension, resident wording review, screen-reader/
universal WCAG conformance and actual human approvals remain unmet.

### Findings, scoped recommendation and resume

| Priority / severity | Finding and reproduction | Smallest next action, owner and dependency |
| --- | --- | --- |
| 1 / High delivery blocker; source-defect severity unknown | PRD NFR-002/PR-005 and ADR0002 paging boundary: native core benchmark17383ms exceeds its existing1500ms assertion; standalone suite and three focused repeats pass. Original failure and recipe above retained | Issue440/coordinator validation owner: diagnose performance repeatability/environment attribution in separately scoped work if needed; retain unchanged threshold and regression. No speculative query refactor or code fix here. A later complete stable-candidate run, not a focused pass, is required for publication |
| 2 / High validation blocker, not a product defect | Policy static Pass and seven-scenario simulation Complete/Pass; independent host metadata/references pass, but actual contained native chooser did not discover the candidate | P04-T01 host-validation owner: establish safe supported exact-candidate native discovery without selecting/launching coordinator, model submissions, private credentials or cloud effects. HVE remains Deferred, original RPI Review and final publication gate not yet eligible |
| Existing acceptance gates | #349 tenant/session, #350 deployed parity, #360 real deployed/AI workflow; #432 requirements delta; named safety/resident/quality authority | Existing owners, no duplicate issues, no ticks/closure. Local fixture success cannot substitute for these gates |

Current open-issue inventory was refreshed; exact benchmark-name body search
found no open match, and existing #76 remains the queue-functionality owner.
No stable application defect or necessary refactor was confirmed, so no new
bug issue or code change was manufactured. The transient measured gate failure
is an explicit regression/reliability risk, not dismissed as a pass.

Recommendation: **fix the affected validation evidence before publication or
affected closure/dependent expansion; continue independent local lanes**.
No product pivot, requirement relaxation or deliberate acceptance deferral is
approved or proposed. Epics cannot close merely because their children merged.
The original critique, failed runs and unchecked human sign-off above remain.
The shared heavy lock was free after the owned gate and focused repeats; no
#349 process/output or receipt environment was interrupted, read or reused.

### Reconciliation with later main (2026-10-25, #440)

The checkpoint above describes main `140d8f49` and BRD 0.19.0 / PRD 0.18.0 only.
Main has since advanced to `ea5577b2` (BRD 0.21.0, PRD 0.20.0, ADR0001/0002
changes, and #360 Entra-authoritative access, ledger-safe migration and seed
merge runtime changes). That later runtime was not assessed by the checkpoint,
which stays historical evidence; a further checkpoint is a separate
coordinator-scheduled item. The branch now includes main through a
non-rewriting merge, with the append-only knowledge-base index and log
conflicts resolved by keeping both sides.

Evidence classes stay separate. The one-time owner-approved native `/agent`
discovery succeeded only as reported in the coordinator comment on #440
(6385349053); the retained local transcript does not show the entry, so it is
attested and not independently reproducible, is not behavioral acceptance, and
will not be repeated. The seven HVE scenarios remain simulated proxy evidence
with the human checkbox unchecked. The external failed-receipt directories were
found absent on 2026-10-24 and are not recreated; the failed 17383 ms against
1500 ms measurement, its receipt SHA256 and its unknown root cause remain
repository records only. The threshold is unwaived. The original Review
(Partial, Residual work) is unchanged. No Conformant outcome, live AI, Entra,
Azure or resident-UX acceptance is claimed; Azure authority has expired. The
final full gate on the merged exact head is recorded after it runs.

## Second Bounded Local Stabilization Checkpoint (2026-11-01, #440)

**Executed, focused tier; not a product or release pass.** Trigger: main
advanced 172 commits since the first checkpoint (140d8f49), including requirement
changes (BRD/PRD 0.21.0) and runtime changes, and the 2026-10-31 closure audit
left #440 criteria 7 and 8 unmet. No Azure, paid model, private data or
heavy-gate group ran. No issue criterion was ticked.

### Source and baseline

`origin/main` fetched 2026-11-01 before testing; later advances are not covered: `36a1d0da25cf73ca41f613a5c7a7df071d5b0771`,
tree `5a8a1fac0bd3ce40426ecaa4d1cdc7424bbe3827`; the worktree was fast-forwarded
to it and tests ran on that tree plus this issue's tracking files only.

| Baseline document | Version/status | Git blob |
| --- | --- | --- |
| [BRD](../brds/agentic-retrofit-programme-brd.md) | Draft 0.21.0, 2026-10-24 | `34d88395de861e9799eb9e24121a21c92c7a5adc` |
| [Demonstrator PRD](../prds/zava-forward-retrofit-programme-demonstrator.md) | In review 0.21.0, 2026-10-25 | `c788b917bafaede215f326f0efc71e071a687f1c` |
| [ADR 0001](../adrs/0001-azure-architecture.md) | Status per document | `d42fa5c4615f4107cee83e07555dba6985c1f53e` |
| [ADR 0002](../adrs/0002-pilot-readiness-architecture.md) | Status per document | `cbe21530043ff15432cc6dce1086d080f5eb15b4` |
| [ADR 0003](../adrs/0003-journey-derived-capabilities-runtime-fit.md) | Status per document | `d60645397b20fb70ac3d1dc47c7a6c8671201306` |
| [ADR 0004](../adrs/0004-per-user-agent-chat-and-memory.md) | Status per document | `9406c2e747ced91e5ba7be4072f9482293c0c38f` |
| [ADR 0005](../adrs/0005-regulatory-compliance-assistant.md) | Status per document | `4d610335a5a18bb282e29c6cb3053404beda995d` |
| [ADR 0006](../adrs/0006-src-layout-and-cutover.md) | Status per document | `956da1a3b804c803041fe2e8a312bd9f400273ae` |

Draft, in-review and proposed documents are not approved by this record. Covered
scope is the affected package boundaries and the feedback-first journey surfaces
(auth, assistant failure paths, resident API, store, import, orchestration);
merged-PR coverage is bounded to the main range above, not an exhaustive PR list.
Open acceptance gaps stay with #349, #350, #360, #432 and #570.

### Actual local commands and outcomes

Environment: `/tmp/ama-440-ckpt2`, Python 3.12.3, pip only, the five `src/`
distributions installed editable (`pip install -e`), plus `ruff`, `mypy` and
the `playwright` package (no browsers). The first attempt installed non-editable
and 16 agents tests errored because the golden-file path resolves relative to the
source tree; that was a harness mistake, the runs were discarded and repeated
editable, and no source defect is claimed.

| Check | Command (from the project directory) | Actual result |
| --- | --- | --- |
| Core suite | `PYTHONPATH=tests python -m unittest discover -s tests -q` | 1727 tests, 502.7s, OK, 206 skipped, exit 0 |
| Agents suite | `PYTHONPATH=tests:../core/tests ...` | 138 tests, 38.8s, OK, exit 0 |
| API suite | `PYTHONPATH=../core/tests:../agents/tests ...` | 1500 tests, 746.2s, OK, 323 skipped, exit 0 |
| Orchestrator suite | `PYTHONPATH=tests:../core/tests ...` | 69 tests, 17.4s, OK, exit 0 |
| Importer suite | `PYTHONPATH=tests:../core/tests ...` | 39 tests, 0.5s, OK, exit 0 |
| Ruff check and format check | `ruff check .`, `ruff format --check .` per project | All five passed |
| mypy | `mypy` per project | Core, agents, orchestrator, importer clean; API first reported 34 `import-not-found` errors for `playwright.sync_api` only, clean (131 files) after installing the package |
| PERF-440 selector | `python -m unittest test_sqlreads.Scale.test_sql_reads_at_60000` x3 | OK x3; filtered page 107/128/107 ms against the unchanged 1500 ms; the full core run measured 123 ms |

All five suites ran concurrently while another session's complete gate held the
shared heavy lock (observed running at the start; absent at 07:59Z), so the
timings are under contention. Skipped tests (529) are not passes. Logs are in
`/tmp/ama-440-ckpt2/*.log` and are not retained in the repository.

Not run, with reason: disposable SQL Server parity, Docker/non-root contracts,
Chromium harnesses and the complete native gate are blocked for this slice by the
foreign heavy-lock holder and by the owner's focused-tier direction. They remain
`implemented-unverified` for this head, and the first checkpoint's observations
(2026-10-23, older main) are historical only. No `Azure observed` row exists.

### Reconciliation delta

The first checkpoint's requirement table is unchanged in classification:
local-observed for scripted/model-off failure paths, auth boundaries, store and
import behavior; blocked or unknown for real Entra sessions (#349), deployed
parity (#350), real AI (#360), actual resident consent, named professional or
authority approval and OD-35 thresholds. BRD/PRD 0.21.0 changes were not
re-traced row by row in this focused slice; that remains `unknown` until a
checkpoint with an owner-approved scope covers them. No new behavior bug was
reproduced, so no regression test was required. No refactoring need was
confirmed; ADR 0006 boundaries held (dependency-rule tests passed in each project).

### Findings, triage and recommendation

| Priority / severity | Finding | Owner |
| --- | --- | --- |
| 1 / High delivery risk, defect severity unknown | PERF-440: one-off 17,383 ms against 1500 ms on 2026-10-23, not reproduced on 36a1d0da under contention (107-128 ms) | New scoped issue #687, independent lane, threshold unchanged |
| Validation | Native `/agent` discovery remains coordinator-attested and the seven HVE scenarios simulated; no coordinator edit in this slice | #440 criterion 8 stays unmet; owner-supplied host evidence needed |
| Existing gates | #349, #350, #360, #432, #570 | Existing owners; no duplicates filed |

Recommendation: **continue**. Independent local lanes proceed; #687 gates only
claims that cite a complete passing benchmark receipt, not feature expansion. The
next full gate for this head is CI and the owner's release cadence. A pivot,
requirement relaxation or deliberate deferral is neither approved nor proposed.

## Third local stabilization checkpoint (2026-11-01)

Refs #440. Bounded engineering checkpoint after a 40-commit wave, not broad
product acceptance. Focused tier, documentation and evidence only; no source,
coordinator, threshold, Azure or private-data change.

### Source and document identities

| Item | Value |
| --- | --- |
| Pinned `origin/main` (freshly fetched) | `b18f7f98e4c890b99187bda9eebd2c7b810e3b91`, tree `e78c8e9885cf8e17b1d80af943351f16e7b07263` |
| Range since second checkpoint | `36a1d0da..b18f7f98` (40 commits: role-screen web slices, core exception queues, regulatory/RAI gates, scale harness and infra scripts, PERF-440 diagnostics #689) |
| [BRD](../brds/agentic-retrofit-programme-brd.md) | 0.21.0, draft, blob `34d88395de861e9799eb9e24121a21c92c7a5adc` |
| [PRD](../prds/zava-forward-retrofit-programme-demonstrator.md) | 0.21.0, in-review, blob `c788b917bafaede215f326f0efc71e071a687f1c` |
| ADR 0001 to 0006 | Unchanged since the second checkpoint |
| Coordinator agent | Unchanged, blob `0c66ef19b329d7a5b0364b78dd8fc7caf6dfede1` |

Draft and in-review documents are not approved by this record. Merged-PR
coverage is bounded to the range above.

### Actual local commands and outcomes

Environment: `/tmp/ama-440-ckpt3`, pip only, five `src/` distributions
installed editable, plus `ruff`, `mypy` and the `playwright` package (no
browsers). Suites ran concurrently on a 4-CPU host while a foreign complete gate
(issue 233) held the heavy lock, so timings are under contention.

| Check | Actual result |
| --- | --- |
| Core suite | 1791 tests, 999.4s, OK, 206 skipped, exit 0 |
| Agents suite | 142 tests, 77.9s, OK, exit 0 |
| API suite | 1547 tests, 1220.3s, OK, 323 skipped, exit 0 |
| Orchestrator suite | 100 tests, 39.9s, OK, exit 0 |
| Importer suite | 39 tests, 0.4s, OK, exit 0 |
| Ruff check, ruff format --check | All five projects passed |
| mypy | Clean: core 190, agents 26, API 139, orchestrator 16, importer 10 source files |
| PERF-440 selector x3 | OK x3; first page 115-194 ms and keyset page 70-153 ms at load1 4.7-6.0 against the unchanged 1500 ms. The original per-repeat filtered-page timings were not captured; the retained full core run logged filtered page 157 ms (8577 matches, load1 8.21). A same-head re-measure (not the original repeats; load1 9.5-10.0, 4 CPUs) gave filtered page 113/282/123 ms, first page 96/92/68 ms, keyset 72/109/76 ms, all OK against 1500 ms |

Command record (no raw logs committed). Working directories are relative to the
repository root; no benchmark-specific environment variables were set, only the
venv `/tmp/ama-440-ckpt3` (Python, pip only, editable installs):

* Suites per project: `cd src/<project> && python -m unittest discover -s tests -q`, with `PYTHONPATH=tests:../core/tests` for agents, orchestrator and importer and `PYTHONPATH=../core/tests:../agents/tests` for API (core needs no extra path).
* Static checks per project: `ruff check .`, `ruff format --check .`, `mypy`.
* PERF-440 selector: `cd src/core/tests && python -m unittest -v test_sqlreads.Scale.test_sql_reads_at_60000`, three sequential runs.
* Load context: host of 4 CPUs, load1 reported by the test's own timing line.

Skipped tests (529) are not passes. Raw logs stay in `/tmp/ama-440-ckpt3` and
are not retained.

Not run: disposable SQL Server parity, Docker/non-root contracts, Chromium
harnesses and the complete native gate (foreign heavy lock; focused tier). They
remain `implemented-unverified` for this head. No `Azure observed` row exists.

### Reconciliation delta

Classification is unchanged from the second checkpoint: `local observed` for
scripted failure paths, auth boundaries, store, import and orchestration
behavior at package level; `blocked` or `unknown` for real Entra sessions
(#349), deployed parity (#350), real AI (#360), actual resident consent, named
professional approval and OD-35 thresholds. The 40-commit wave was not re-traced
requirement by requirement; that stays `unknown`. The new role-screen web slices
are covered only by their merged per-PR tests and are `implemented-unverified`
here. No behavior bug was reproduced and no refactoring need confirmed; ADR 0006
dependency-rule tests passed in each project, so no regression test was required.

### Findings, triage and recommendation

| Priority / severity | Finding | Owner |
| --- | --- | --- |
| 1 / High delivery risk | PERF-440 one-off 17,383 ms (2026-10-23) still not reproduced; #689 added diagnostics, #720 (reproduction under IO contention) is open | #687, independent lane, threshold unchanged |
| Validation | Native discovery coordinator-attested, seven HVE scenarios simulated; no coordinator edit here | #440 criterion 8 unmet; owner-supplied host evidence needed |
| Existing gates | #349, #350, #360, #432, #570 | Existing owners; no duplicates filed |

Recommendation: **continue**. Independent local lanes proceed; #687 gates only
claims citing a complete passing benchmark receipt. Criteria 7 (until #687 is
resolved) and 8 stay unmet. A pivot, requirement relaxation or deliberate
deferral is neither approved nor proposed.

## Epic #89 scoped stabilization checkpoint (2026-11-03)

Refs #89, applying the #440 checkpoint to the provider capacity, work order and
quality acceptance surface only. Focused tier, documentation and evidence only;
no source, Azure, private-data or threshold change. This is a bounded
engineering checkpoint, not product acceptance and not epic closure.

### Source and scope

| Item | Value |
| --- | --- |
| Pinned `origin/main` | `b855aec86b47939ed4cafd38bc17b9318f2284c7`, tree `4109880ddc5bdde26b6ff405ab742e60bb8b6daf` |
| [BRD](../brds/agentic-retrofit-programme-brd.md) | 0.21.0, blob `34d88395de861e9799eb9e24121a21c92c7a5adc`, unchanged since the third checkpoint |
| [PRD](../prds/zava-forward-retrofit-programme-demonstrator.md) | 0.21.0, blob `c788b917bafaede215f326f0efc71e071a687f1c`, unchanged |
| Covered issues | Children #90 and #91 (closed), #92, #132, #133 (open); parent #89 |
| Merged PRs on the surface | #389 (consultation evidence and scoped holds, Refs #92); earlier #90 and #91 delivery in `core/procurement.py` and `core/quality.py` after the M2 move (#199) |
| Open, unmerged, not counted | #900 (#92 read-only letting and renewal gate), #873 (#132 job pack), #869 (#133 aftercare register) |

Draft and in-review documents are not approved by this record.

### Actual local commands and outcomes

Environment: `/tmp/venv-89` (pip only; `src/core`, `src/agents` and `src/api`
editable, plus `ruff`, `mypy` and the `playwright` package without browsers).
`PYTHONDONTWRITEBYTECODE=1`; mypy used `--cache-dir=/tmp/mypy-89`.

| Check | Actual result |
| --- | --- |
| `cd src/core/tests && python -m unittest test_quality_procurement test_consultation_controls -q` | 146 tests, 84.0s, OK, 13 skipped (SQL Server variants), exit 0 |
| `cd src/api && PYTHONPATH=../core/tests:../agents/tests python -m unittest tests.test_procurement_api tests.test_procurement_screens tests.test_technical_quality_screens -q` | 59 tests, 36.6s, OK, exit 0 |
| `ruff check` and `ruff format --check` in `src/core` | Passed (153 files formatted) |
| `ruff check` in `src/api` | Passed |
| `mypy` in `src/core` and `src/api` | Clean (206 and 156 source files); the first API run failed only for the missing `playwright` stub package, fixed by installing it |

Skipped tests are not passes. Not run: full package suites, disposable SQL
Server parity, Docker, Chromium harnesses, benchmarks and the complete gate
(coordinator-owned). Those paths stay `implemented-unverified` for this head.
No `Azure observed` row exists.

### Reconciliation of requirements with code and tests

| Requirement | Local evidence on this head | Class |
| --- | --- | --- |
| RULE-007 (no scheduling or confirmation beyond committed capacity), AC-026 | `test_committed_capacity_needs_evidence_and_limits_work_orders`, `test_imported_numeric_capacity_is_not_evidenced`, `test_capacity_dates_scope_source_and_deficit_invalidate_progression`, `test_advance_without_evidenced_booked_order_is_refused` | local observed (scripted fixtures); real contracts unknown |
| RULE-008 (only a named authorised contract manager instructs; drafts are not instructions), AC-030 | `test_named_authority_is_not_a_role_or_caller_claim`, `test_drafts_and_draft_review_never_issue_instructions`, `test_every_order_change_has_a_version`, `test_contractor_sees_only_own_work_orders_without_reason` | local observed; real contract-manager identities blocked (#349, #350) |
| RULE-004 (contractors submit evidence, never approve quality) and RULE-013 (independent re-verification before defect closure), AC-013, AC-044 | `test_never_auto_accepts_and_accepter_must_be_independent`, `test_installer_name_blocks_acceptance`, `test_quality_remediation_and_reinspection`, `test_quality_replacement_dependencies` | local observed |
| RULE-023 (Legal records consultation status before let or renewal), AC-073 | `test_consultation_controls` (four-state supplied record, authority stays Unverified, effective status unknown, dependent actions held). No contract let or renewal transition exists; #900 is open | partly implemented; criteria of #92 unmet |
| FR-016 and FR-017 as numbered in the PRD (versioned provider-package record; quality acceptance) | Covered by the tests above; BRD FR-016/FR-017 are handoff requirements (AC-022, AC-023), a numbering difference between the two documents | contradiction flagged, not resolved here |
| BG-002 and BG-006 outcomes (accepted handovers, right-first-time) | No measured outcome; thresholds are planning assumptions | unknown |

Child ledger: #90 and #91 are closed with their ticked criteria supported by
the tests above. #92 is open: both criteria unmet (verified Legal status and a
real let or renew transition do not exist). #132 and #133 are open and
not-started on main; their PRs are unmerged. Child scope that is neither
delivered nor deferred by an owner decision remains open.

### Findings, triage and recommendation

| Priority / severity | Finding | Owner |
| --- | --- | --- |
| 1 / Medium | PRD and BRD both define FR-016 and FR-017 with different meanings; the epic cites both | Requirements owner; to be reconciled in a document PR, not silently |
| 2 / Medium delivery | Three children (#92, #132, #133) have open unmerged PRs; criterion 2 of #89 needs each closed or owner-deferred | Existing PRs |
| 3 / Low | Procurement is held as one document rather than per-row tables (#90 note) | Backlog, no bug reproduced |

No behavior bug was reproduced and no refactoring need confirmed, so no
regression test was added. Recommendation: **continue**. Epic #89 criterion 1
is not met: this checkpoint is partial evidence only, because children are open
and no pivot or deferral decision has been recorded. Rerun the checkpoint after
the child PRs resolve and before epic closure.

## Epic #123 scoped stabilization checkpoint (2026-11-03)

Refs #123, applying the #440 checkpoint to the discovery, evaluation and
release governance surface only. Focused tier, documentation and evidence
only; no source, Azure, private-data or threshold change. This is a bounded
engineering checkpoint, not product acceptance and not epic closure.

### Source and scope

| Item | Value |
| --- | --- |
| Pinned `origin/main` | `61a4ac54329b5362109ec63fd85490d03b98f486`, tree `accfed0a94abf6e1ac5f9485aea6dab2b65fa5f4` |
| [BRD](../brds/agentic-retrofit-programme-brd.md) | 0.21.0, blob `34d88395de861e9799eb9e24121a21c92c7a5adc`, unchanged |
| [PRD](../prds/zava-forward-retrofit-programme-demonstrator.md) | 0.21.0, blob `c788b917bafaede215f326f0efc71e071a687f1c`, unchanged |
| Covered issues | Children #124, #125, #126, #128, #129 (open); #127 and #166 (closed); parent #123; checkpoint rule #440 |
| Merged PRs on the surface | #899 (journey learning-test bundles protocol, Refs #129); #651 (`is_synthetic` on scale fixtures, Refs #167); earlier #126, #127 and #166 delivery in `core/governance.py`, `core/rulecards.py` and the synthetic-data modules |
| Open, unmerged, not counted | #895 (#124 register rules), #894 (#125 readiness gate), #905 (#126 AI running-cost line), #901 (#128 journey ownership register) |

Draft and in-review documents are not approved by this record.

### Actual local commands and outcomes

Environment: `/tmp/venv-123` (pip only; `src/core`, `src/agents` and `src/api`
editable, plus `ruff`, `mypy` and the `playwright` package without browsers).
`PYTHONDONTWRITEBYTECODE=1`; mypy used `--cache-dir=/tmp/mypy-123`.

| Check | Actual result |
| --- | --- |
| `cd src/core/tests && python -m unittest test_governance test_rulecards test_change_provenance -q` | 95 tests, 23.3s, OK, 16 skipped (SQL Server variants), exit 0 |
| `cd src/api && PYTHONPATH=../core/tests:../agents/tests python -m unittest tests.test_governance_evidence_api -q` | 10 tests, 8.2s, OK, exit 0 |
| `ruff check` and `ruff format --check` in `src/core` | Passed (153 files formatted) |
| `ruff check` in `src/api` | Passed |
| `mypy` in `src/core` and `src/api` | Clean (206 and 156 source files) |

Skipped tests are not passes. Not run: full package suites, disposable SQL
Server parity, Docker, Chromium harnesses, benchmarks and the complete gate
(coordinator-owned). Those paths stay `implemented-unverified` for this head.
No `Azure observed` row exists.

### Reconciliation of requirements with code and tests

| Requirement | Local evidence on this head | Class |
| --- | --- | --- |
| RULE-019 (frozen protocol, DPIA and register before capture; BG-011 never pass or fail when the MDE exceeds the target), AC-062, AC-077 | `test_capture_closed_until_protocol_dpia_and_register_approved`, `test_changed_protocol_needs_reason_and_new_approval`, `test_bg011_never_pass_or_fail_when_mde_exceeds_target`, `test_shadow_and_live_need_phase_0_released`, `test_pilot_case_events_need_open_capture_gate` | local observed (synthetic fixtures); real protocol, DPIA and register approvals unknown (company owners) |
| RULE-020 (evidence-based release decision per phase and tranche), AC-063 | `test_phase_release_decisions_are_recorded_and_gated`, `test_view_is_manager_only` | local observed; no real release decision exists |
| RULE-024 (guardrail breach pauses scope until authorised restart), AC-078 | `test_breach_record_needs_an_authorised_role`, `test_breach_pauses_scope_until_authorised_restart`, `test_paused_scope_blocks_case_workflows_but_not_hazards`; SQL restart variant skipped | local observed (JSON store); SQL variant implemented-unverified |
| RULE-021 (regulatory change enters a human-owned workflow before activation), AC-068 | `test_review_item_lists_affected_requirements_rules_tests_and_versions`, `test_assessment_needs_named_owner_and_complete_record`, `test_assessment_never_activates_a_rule` | local observed; no live source monitoring or named Legal owner |
| RULE-017 (professional ownership and evidence versions), AC-054 | `test_change_provenance` upload and handoff metadata tests; evidence register tests in `test_governance` | local observed |
| RULE-016 (appraisal of options before solution), AC-053 | No code path; readiness decision record is a company document | unknown (owner evidence needed) |
| NFR-008, NFR-009 (equity and accessibility testing; journey ownership and manual alternatives), AC-064, AC-071 | #899 protocol only; #901 (journey ownership register) is open and unmerged; no equity test has been run | partly specified; unmet |
| BG-011 and BG-012 outcomes | Targets are proposals; no measured baseline, no AI economics line merged (#905 open) | unknown |

Child ledger: #127 and #166 are closed with ticked criteria supported by the
tests above. #124, #125, #126, #128 and #129 are open: each has criteria that
need company owners or data (discovery owner, DPIA, budget-owner booked
destinations, direct user research, atlas-owner mapping) and four have
unmerged PRs. Child scope that is neither delivered nor deferred by an owner
decision remains open.

### Findings, triage and recommendation

| Priority / severity | Finding | Owner |
| --- | --- | --- |
| 1 / Medium delivery | Four children have open unmerged PRs (#895, #894, #905, #901); criterion 2 needs each closed or owner-deferred | Existing PRs |
| 2 / Medium | RULE-016 and the BG-011 baseline depend on company data and approvals that no code can supply | Company owners, programme board |
| 3 / Low | SQL Server variants of the governance tests were skipped here; parity is unverified for this head | Coordinator gate |

No behavior bug was reproduced and no refactoring need confirmed, so no
regression test was added. Recommendation: **continue**. Epic #123 criterion 1
is not met: this checkpoint is partial evidence only, because children are open
and no pivot or deferral decision has been recorded. Criterion 2 is unmet.
Rerun the checkpoint after the child PRs resolve and before epic closure.

## Rubric src counting reconciliation (2026-10-27)

Refs #198. This additive reconciliation preserves the original UNMET rubric
row, historical retirement boundary and earlier failed/unchecked evidence.
It supplies subsequently retrieved evidence, not retrospective sign-off or
whole-issue closure. Inspected base: `09099ecd1a66ee9d37ad993707d1f2eda07cdfd4`.
No model scoring was dispatched, no private dataset read and no score edited.

### Main integration qualification (2026-10-29)

Refs #198, PR #507. Rebased onto main
`5653547507f3056f09a726a18516237728da5e5b`, preserving both additive
documentation histories. At the owner's direction, the entire rubric tree
and scenario manifest now use that main revision's bytes, including its
recorded score and tests. The 2026-10-27 repairs, guide changes and test counts
below describe the original candidate, not the rebased executable delta:
those rubric edits are not retained. Original critique, Review and historical
acceptance gaps remain unchanged. No new rubric score, hosted CI success,
publication receipt, merge or issue acceptance is inferred.

The later same-day conflict rebase uses main
`356a3cfbaa2cd63a6fbf80e87e11a29cacaaf4c7` and retains that revision's
complete rubric tree and scenario manifest, superseding only the integration
base above. Both independent index entries and append-only log histories
survive. Core/API lint, format, typing and twelve focused tests pass; the
scenario validator confirms the existing pins without re-pinning. The
authoritative-main rubric suite still reports 18 failed, 355 passed and seven
missing-runtime skips. Those failures are not repaired here; no fresh hosted
CI or remote mergeability is claimed before the coordinator's push.

### Current-main synchronization (2026-10-30)

Refs #198, PR #507. The new conflict rebase first used main
`91e890e07af036263316c153cbc7ceff780cdaa2`, then integrated the concurrently
updated `ffd8f35e63b24905b9aeb937dbf2a7fe9968747f` before Review.
The intervening changes affect only a training-material development lockfile.
Main's complete rubric and scenario
manifest are retained, together with all independent index entries, both
append-only log histories and the original dated RPI outcomes. The earlier
integration bases and test counts above remain historical observations, not
results for this candidate. No application, workflow, infrastructure or legacy
code is changed. Local synchronization does not establish a fresh hosted CI
result, remote mergeability, publication approval or whole-issue acceptance;
the coordinator owns the later push and hosted checks.

For this candidate, core/API Ruff lint, format and mypy passed, as did twelve
focused manifest/dependency tests and twenty-five migration regressions.
Scenario source pins validated without re-pinning. Main's unchanged rubric
suite still reports 18 failed, 355 passed and seven missing-runtime skips;
this is not a green full-suite result. The actual prepare decision is
`should_score=false`, baseline 77/100, because no scored artifact changed.
No full API suite or full publication gate was run.

### PR #507 review correction (2026-10-30)

Refs #198. The integrated PR is documentation-only. The original 2026-10-27
candidate's synthetic fixtures, workflow-test repairs and rubric-guide edits
were discarded during integration; they are not current deliverables.
Its **374 passed / one failed / seven skipped** result and 31 targeted passes
are historical only. The integrated inputs instead report **355 passed /
18 failed / seven skipped**, with no scored artifact changed and
`should_score=false`. No new model score or B6 recovery is delivered.

The original Review froze the non-tracking diff against
`09099ecd1a66ee9d37ad993707d1f2eda07cdfd4` with SHA-256
`de87d9e063b59ca93f178241776d82c2ac447d68efc02ba9780373fb17a75962`.
The later integrated Review assessed `86ce8f660d846a57da03ddd973ab513dd482465f`
plus its documentation edits against
`ffd8f35e63b24905b9aeb937dbf2a7fe9968747f`. Its three-document diff
(`docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md`,
`docs/reference/log.md`) has SHA-256
`8059b4aa91f469ff735c33c620bd23cc1b529d108a5737a08d862b53f0061883`,
preserved in the
[pre-correction integrated snapshot](https://github.com/jmservera/ama/compare/ffd8f35e63b24905b9aeb937dbf2a7fe9968747f...254d2274693c8190f827067c3732e03d102a563d).
These identify different historical assessed boundaries, not this corrected
candidate's diff or a fresh exact-head publication assessment. This correction
changes the documentation delta; it does not restore the discarded changes,
repeat those Reviews or change their original outcomes.

### Baseline and score provenance

The pre-migration snapshot at `9261c5cb1dcca013d9bc93c79d3fafebc70b8f71`
records 47/100, rubric_version 2, scored commit
`80660e95014c5abf5327d5e5e235c0612b991aa1`, 2026-10-14 15:47:56 UTC,
[run 38590975162](https://github.com/jmservera/ama/actions/runs/38590975162).
Its solution-code criteria are A1=4, A3=5, A4=5, A5=3, A6=3, A7=4, B6=4;
the score file preserves original rationale and evidence, including then-live
`mvp/` paths. Those are historical citations, not current live links.

| Boundary / PR | Repository snapshot | Recorded total vs 47 | Evidence qualification |
| --- | --- | --- | --- |
| Registry exclusions #292 | `ef4656a1` | 47, delta 0 | Existing assessment of `fa730d63`, not a fresh score of this merge |
| Prototype retirement #295 | `a7e30046` | 47, delta 0 | Same carried assessment |
| M1 #296 | `5c717d9e` | 47, delta 0 | Same carried assessment |
| M2 #297 | `14b776c0` | 47, delta 0 | Same carried assessment |
| M3 #298 | `55462829` | 47, delta 0 | Same carried assessment |
| M4 #299 | `74a84dcf` | 47, delta 0 | Same carried assessment |
| M5 #300 | `e0192934` | 47, delta 0 | Same carried assessment |
| R1 #301 | `a99e38e9` | 47, delta 0 | Same carried assessment |
| M6 #302 | `a381532d` | 47, delta 0 | Same carried assessment |
| Last pre-pointer-deletion main | `65a514ed` | 77, delta +30 | Score of `89c52cba`, not of this snapshot |
| Pointer deletion #499 | `4a02baf6` | 77, delta +30 | Hosted PR score 77 vs then-baseline 77; scored `1ed59d75`, not merge SHA |
| Main inspected on 2026-10-27 | `09099ecd` | 77, delta +30 | Score of `f1be9b1d`, not a new #198 assessment |

All migration snapshots above contain the same assessment of
`fa730d63190c200e36b9a09c890445f17e8cb164`, dated 2026-10-15 15:58:33 UTC,
[run 38763347056](https://github.com/jmservera/ama/actions/runs/38763347056),
with the same seven criterion values as the pre-migration baseline.
No sticky rubric scorecards were available on #292/#295/#296-#302 when queried
on 2026-10-27. The snapshots prove carried state only; they do not prove
each PR was freshly scored or recorded its comparison during the dual window.

The pre-deletion assessment is
[run 40548249080](https://github.com/jmservera/ama/actions/runs/40548249080),
2026-10-27 17:18:42 UTC. The actual #499
[sticky comparison](https://github.com/jmservera/ama/pull/499#issuecomment-6450533583)
and [run 40560161654](https://github.com/jmservera/ama/actions/runs/40560161654),
2026-10-27 18:38:28 UTC, record **77/100 against 77/100**, delta 0.
The assessment inspected on 2026-10-27 is
[run 40569657958](https://github.com/jmservera/ama/actions/runs/40569657958),
2026-10-27 19:50:57 UTC. Each has A1=5, A3=5, A4=5, A5=5, A6=5, A7=4,
B6=5 and rubric_version 2. Intervening features, deck and other portfolio
changes prevent attributing the +30 from the old baseline to migration.

### Registry sequence and recovery expectation

PR #292 added src vendor/data/egg-info/build exclusions before the first
module move. `src/**/*` already covers package code, external project tests,
`pyproject.toml`, Dockerfiles, READMEs and web assets. No extra include is
needed. Actual legacy removals were distributed across merged PRs:
#295 removed `prototype/deploy/**/*.bicep`; #300 removed executable/web/test/
Dockerfile mvp globs in the same PR as the moves; #302 removed `mvp/README.md`
when its content moved to source guides. #499 later removed the unscored pointer.
They were not one dedicated final registry PR. Production prepare reads the
base registry. The original candidate's temporary-Git regressions demonstrated
old-registry deletion detection and merged-registry exclusion, not that every
historic run succeeded; those added fixtures were discarded during integration.

No dip is visible in the available snapshots or actual #499 comparison.
There is therefore no evidenced moved-out-of-glob/deleted-evidence loss to
assign as its cause. The owner accepts a temporary dip if one is observed:
record the removed path and affected criterion, distinguish deleted evidence
from an out-of-glob move, and recover by relevant changed src evidence, never
by inflating grades, changing version or treating an unchanged file as new.

| Criterion | Re-evidence route and delivery PR | Recovery expectation / limit |
| --- | --- | --- |
| A1 | `src/core/src/zava_forward/core/`, #296/#297; project manifests and Dockerfiles, #290/#300 | Assess actual modularity/dependency boundaries, not rename volume |
| A3 | `src/core/src/zava_forward/core/ai.py`, #296; `assistants.py`, #297; API auth, #300 | Re-evidence scope/consent/approval controls; no live approval inferred |
| A4 | Core modules, #297; `src/api/src/zava_forward/api/server.py`, #300; worker `src/agents/src/zava_forward/agents/dispatch.py`, #301 | Completeness requires actual composed evidence, not file presence |
| A5 | `src/core/src/zava_forward/core/ledger.py`, #297; orchestrator jobs and image, #300 | Measured operational evidence remains separate from moved implementation |
| A6 | Core AI client, #296; `src/agents/evals/` and AI eval, #298/#299 | Evaluation artifacts and results, not a model-quality claim from tests alone |
| A7 | Proposal service, #297; database-free worker dispatch, #301 | Worker slice does not establish deployed queue orchestration |
| B6 | Five project READMEs delivered by #302; registered `src/README.md` is the proposed recovery target in a later PR titled `docs(src): strengthen B6 navigation and evidence` | That PR is proposed, not created or delivered here. Only when it actually changes this scored README can it reopen B6 and supply a changed-file citation; no score increase or deck/live-session acceptance is inferred |

The historical delivery PRs above are not fresh scores or a promise of grade
recovery. `.github/rubric/README.md` is outside every artifact in
`artifacts.json`; changing it cannot open B6 or supply a changed-file citation
for an increase. It is also unchanged by this integrated branch. In contrast,
`src/README.md` is included in the registered `solution-code` artifact, which
informs B6. If a new dip needs changed evidence, the later scoped PR must name
that criterion and the actual changed evidence; an unchanged historical file
cannot justify an incremental increase. This #198 branch now changes
documentation only, not tests or scored artifacts, and makes no claim to
recover application grades.

### Local test reassessment and acceptance

PR #292 reported 124 passed / 19 failed / seven skipped. PR #295 removed eight
stale prototype cases, leaving 11 pre-existing failures then. Original candidate
baseline `09099ecd`: 355 passed / 18 failed / seven skipped. Re-assessed causes: seven
mutable-score assertions; ten obsolete workflow event/path assumptions; one
unrelated deck-selection mismatch. After the original candidate's scoped
repairs, its complete rubric suite reported **374 passed / one failed /
seven skipped**. Its remaining failure was the executive-deck exclusion
expectation versus the
`docs/capstone/deck/*.pptx` wildcard. Seven real MCP runtime tests skip because
the pinned runtime is unavailable; generated-schema tests do not replace them.
Original migration-targeted fixtures: 31 passed. Those repairs and added
fixtures are not retained by the integrated PR. Its unchanged-main suite
reports **355 passed / 18 failed / seven skipped**, not 374/1/7.
No full/heavy gate or cloud checks ran; workflow Markdown/lock, production
registry, rubric and scores are unchanged by this documentation-only delta.

| #198 acceptance | Evidence and remaining boundary |
| --- | --- |
| Pre-migration baseline and seven criteria | Historical 47 snapshot and original evidence retained above |
| src tests/Dockerfile counting and exclusions | #292 and existing upstream prepare coverage remain; original candidate's added fixtures were discarded, not current deliverables. No extra layout glob needed |
| Each dual-window PR records fresh comparison/cause/recovery | Not proven; merge snapshots are carried scores, not contemporaneous per-PR assessments |
| Dedicated cut-over registry PR / preceding old-registry deletion | Actual #295/#300/#302 sequencing recorded; cannot retroactively meet original ordering |
| README update and 19 failures re-assessed | Original candidate's guide/test repairs discarded; no rubric README update delivered now. Historical 374/1/7 and integrated 355/18/7 results distinguished; this original acceptance criterion is not met by the documentation-only correction |
| Workflow Markdown change requires compiled lock | Not applicable: neither file changes |
| Comparison and recovery in sign-off | Later additive 47/77/77 evidence and criterion routes supplied; not a pre-sign-off fresh migration assessment or post-merge assessment of this branch |

Keep Refs #198. Recovering any missing historic scorecards or accepting a
historical sequencing/scoring deviation belongs to the owner; no such
decision is guessed here. This does not block the bounded documentation correction
or authorize issue closure, merge, release or live use.

## Rubric before-and-after score record (2026-11-03, Refs #198 #203)

Refs #198, Refs #203. Owner decision 2026-11-03: record the pre-cut-over
total against the after-cleanup total, with the dip cause and recovery
expectation. Source: the Git history of `.github/rubric/scores/latest.json`
read on 2026-11-03 at main `9a9f9dada`. No model scoring was dispatched, no
score edited and no workflow or registry changed. Earlier sections of this pack
are preserved; this record adds to them.

| Point | Date (UTC) | Scored commit | Total | A / B / C / D | Source |
| --- | --- | --- | --- | --- | --- |
| Pre-migration baseline | 2026-10-14 | `80660e95` | 47 | not restated | [run 38590975162](https://github.com/jmservera/ama/actions/runs/38590975162) |
| Pre-cut-over (pre-deletion of the pointer, #499) | 2026-10-27 17:18 | `89c52cba` | 77 | 34 / 23 / 11 / 9 | [run 40548249080](https://github.com/jmservera/ama/actions/runs/40548249080) |
| After cleanup, current main | 2026-11-03 13:58 | `949f9346` | 77 | 34 / 23 / 11 / 9 | [run 41647768785](https://github.com/jmservera/ama/actions/runs/41647768785) |

Result: pre-cut-over 77, after cleanup 77, delta 0, floors met, outcome Pass,
`rubric_version` 2 throughout. All 118 distinct scoring points recorded between
2026-10-27 17:18 and 2026-11-03 are 77. The solution-code criteria are
unchanged between the two points: A1=5, A3=5, A4=5, A5=5, A6=5, A7=4, B6=5.
The 47 baseline to 77 delta (+30) is not attributable to the migration: the
intervening scores also include feature, deck and portfolio changes (see the
2026-10-27 reconciliation above).

Dip cause: no dip occurred across the cut-over window. The totals rose from 64
(2026-10-24) to 75 and then 77 (2026-10-27), before the pointer deletion, and
stayed at 77 after it. There is therefore no moved-out-of-glob or
deleted-evidence loss to assign. Totals below 47 in the history (for example
22 on 2026-10-07 and 45 to 54 on 2026-10-13 and 2026-10-14) precede the first
migration PR and are not cut-over effects. They are kept as scorer variance
and earlier portfolio changes, not explained further here.

Recovery expectation: none needed, because nothing was lost. If a later
registry or deletion PR does cause a dip, the owner-accepted rule of
2026-10-14 applies: record the removed path and criterion, then recover through
changed `src/` evidence using the route table above, never by changing the
version or treating an unchanged file as new.

Registry state: `.github/rubric/artifacts.json` contains no `mvp/` or
`prototype/` glob; `src/**/*` covers package code, tests, `pyproject.toml`,
Dockerfiles and READMEs.

### Acceptance effect

| Criterion | Effect of this record and repository evidence |
| --- | --- |
| #198 before-and-after comparison with recovery expectation in the sign-off record | Evidenced here (47 baseline, 77 pre-cut-over, 77 after cleanup, recovery stated). The owner confirms this pack section is the sign-off record |
| #198 baseline, src coverage, README, lock file | Already ticked or not applicable (#292, #705, #851); unchanged |
| #198 per-PR dual-window records | Still unmet: merge snapshots are carried scores, not contemporaneous per-PR records. Not provable retroactively |
| #198 dedicated cut-over registry PR and ordering | Still unmet as written: removal was spread across #295, #300, #302 and #851. The glob removal is proven; the owner decides whether to accept the sequence |
| #203 rubric run on main after cleanup compared with pre-cut-over, dip explained | Proven for the local record: 77 against 77, no dip. Based on workflow scores recorded in Git, not a new run |
| #203 literal `mvp/` and `prototype/` search | Still unmet: 51 tracked files still match the literal pattern, many outside dated historical records |
| #203 relative links in changed docs | Not re-evidenced here; see the earlier link audits and the test of #850 |
| #203 deployed app and CI green from `src/` | Still unmet: needs live deployed-app and hosted CI evidence, not produced here |

No issue is closed by this record. Ticking is for the owner after merge, using
this PR as evidence.

## Fourth local stabilization checkpoint (2026-11-04)

Refs #440. Bounded engineering checkpoint on current `origin/main` per the
owner decision of 2026-11-04, not broad product acceptance. Focused tier,
documentation and evidence only; no source, coordinator, threshold, Azure or
private-data change. The coordinator owns any full gate; none was run.

### Source and document identities

| Item | Value |
| --- | --- |
| Pinned `origin/main` (freshly fetched) | `fab02307eb14e4c01af25092a7192b771dc1f491`, tree `19d7956b4b883db680863eeefa07fc70d474ee4a` |
| Range since third checkpoint | `b18f7f98..fab02307` (323 commits; `src/` 258 files: core 123, api 106, agents 25, orchestrator 3; includes the #810 HTTP/1.1 keep-alive fix) |
| [BRD](../brds/agentic-retrofit-programme-brd.md) | 0.21.0, draft, blob `34d88395de861e9799eb9e24121a21c92c7a5adc`, unchanged |
| [PRD](../prds/zava-forward-retrofit-programme-demonstrator.md) | 0.21.0, in-review, blob `c788b917bafaede215f326f0efc71e071a687f1c`, unchanged |
| ADR 0001 to 0006 | Unchanged since the third checkpoint |
| Coordinator agent | Blob `7f8bf9ce842177c59992f3f38a2701bb999f6716`; changed since the third checkpoint by other merged PRs (D5 review-thread rule, CI economy and PR cap, gate shard text), not by this record |

Draft and in-review documents are not approved by this record. Merged-PR
coverage is bounded to the range above and was not re-traced requirement by
requirement. Previously delivered and not repeated: PRs #461, #688, #729,
#689, #720 and #733.

### Actual local commands and outcomes

Environment `/tmp/venv-440` (pip only, five `src/` distributions editable,
`ruff`, `mypy`, `playwright` package without browsers), `PYTHONDONTWRITEBYTECODE=1`,
mypy `--cache-dir=/tmp/mypy-440`.

| Check | Actual result |
| --- | --- |
| `ruff check .` per project | Passed in core, agents, api, orchestrator and importer |
| `ruff format --check . --no-cache` per project | Passed (core 194, agents 36, api 102, orchestrator 13, importer 11 files) |
| `mypy` per project | Clean: core 247, agents 40, api 171, orchestrator 16, importer 10 source files |
| ADR 0006 `tests.test_dependency_rule` | core 2, agents 4, orchestrator 2, importer 2 tests, OK |
| API focused: `tests.test_dependency_rule tests.test_keepalive tests.test_auth tests.test_entra_authoritative tests.test_ai_boundary tests.test_design_system` with `PYTHONPATH=tests:../core/tests:../agents/tests` | 96 tests, 36.3s, OK, exit 0 |

An earlier API invocation without `tests` on `PYTHONPATH` failed with
`ModuleNotFoundError` for sibling test modules; that was an invocation error,
not a product failure, and the corrected command above passed.

Not run: full package suites, the PERF-440 benchmark selector, disposable SQL
Server parity, Docker and non-root contracts, Chromium harnesses and the
complete gate. Those paths stay `implemented-unverified` for this head. Raw
logs stay in `/tmp` and are not retained.

### Reconciliation delta

Classification is unchanged. `local observed`: scripted AI failure and manual
paths (`test_ai_boundary`), auth and Entra-authoritative role boundaries,
HTTP/1.1 keep-alive handler behavior and ADR 0006 dependency direction, all at
package level. `blocked` or `unknown`: real Entra sessions (#349), deployed
parity (#350), real AI (#360), actual resident consent, named professional
approval and OD-35 thresholds. #810 live Easy Auth empty-body 500s were
reported 0 in 2,140 requests after deploy of main 4d56cf609 (infra README
evidence, owner-approved); that is Azure evidence recorded elsewhere and is not
re-observed here. Feedback-first issues #344, #349, #350 and #360 remain open.
The resident and employee demo web slices merged in the range are covered only
by their per-PR tests and by `test_design_system` here; accessibility
acceptance, assistive-technology testing and resident consent are not
established. No behavior bug was reproduced and no refactoring need was
confirmed, so no regression test was added.

### Findings, triage and recommendation

| Priority / severity | Finding | Owner |
| --- | --- | --- |
| 1 / Medium validation | Coordinator text changed after the first checkpoint through other PRs; no Major HVE static, behavior or host validation for those edits is recorded under #440 | Owner-supplied host evidence; criterion 8 |
| 2 / Low | PERF-440 (#687) is closed after #689, #720 and #733: diagnostics and a contention reproduction (59,647 ms under 16 fsync writers) attribute the outlier to the environment; threshold unchanged. Not re-run here | None open |
| Existing gates | #349, #350, #360, #432 | Existing owners; no duplicates filed |

Recommendation: **continue**. No blocking finding gates epic closure or
dependent expansion. No pivot, requirement change or deliberate deferral is
proposed or approved.

### Criteria after this checkpoint

Unmet, stated plainly: criterion 8 (Major HVE behavior and host validation of
the coordinator is not established; native discovery was a one-time
coordinator-attested owner check and the seven scenarios are simulated).
Criterion 7 has supporting evidence (the only confirmed finding was triaged to
#687 and delivered by #689, #720 and #733, with no further confirmed finding),
but this PR uses `Refs`, so the owner decides the ticks. Criteria 1 to 6 are
supported by PR #461 and checkpoints 2 to 4. No issue is closed by this record.

## Fifth stabilization checkpoint: current-main sensor contract, retention and handover (2026-11-05, Refs #440 #184 #110)

Refs #440, #184 and #110. Bounded, documentation-only, local-only record on
current `origin/main` for the already-due #184/#110 sensor contract,
retention and handover gaps. It adds no source, schema, threshold,
coordinator, workflow, infrastructure or requirement change and no
acceptance. Original RPI evidence is under
`.copilot-tracking/*/2026-11-05-sensor-checkpoint-recovery-440-*`.

### Trigger, identities and coverage

The trigger is the due sensor checkpoint named on #184 after the merged live
simulator generator and container slice (2026-11-04) and the merged delivery
tooling PRs #1209 and #1210. The existing owner is #440 (open, parent #123);
no duplicate checkpoint issue was created.

| Item | Value |
| --- | --- |
| Current `origin/main` (fetched 2026-11-05) | `c6d5a8f3c3a35892322300be27b9747f7b11362d`, tree `876679c32ff8f8a3d35822d9e46d8b377ce15428` |
| Working base (parent topic pin) | `3d7ad2feaa9c4cba5fe917edd2fbc40e40a5c246`, tree `b35f4e4808a4eb74bfee55f098bb101369358d98` |
| Base to main delta | One commit (#1210). `git diff --stat` over `src`, `docs` and `infra` is empty; only `tools/rpi-checks.py`, `tools/test_rpi_checks.py` and tracking records differ |
| Covered merged PRs | #1209 (`3d7ad2fea`, 2026-11-05T09:31:21Z, backlog-sync active-delivery state) and #1210 (`c6d5a8f3`, 2026-11-05T10:01:58Z, isolated Chromium before API discovery). Both are delivery tooling; neither changes sensor behaviour and neither is sensor acceptance |
| Excluded, unmerged | #1203 (open; public head `c9a14573d76a128c028ca2371ed9612b41461b8a`; a user-reported unpublished local head `834e2bec` was neither read nor validated), #1205 (open; public head `dbacb32f8713c5c1acf088f8d8b536193f3269be`) and the unmerged sibling code128 work. Their source is not main and is not accepted here |
| This record's evidence pack blob at main | `2566e8efd7084346421fffb101d5b171100dfd63` (before this section) |

Document identities at `c6d5a8f3`. Draft, in-review and proposed documents
are not approvals by this record.

| Document | Status, version, date | Blob |
| --- | --- | --- |
| [BRD](../brds/agentic-retrofit-programme-brd.md) BRD-2026-AMA48-001 | draft, 0.21.0, 2026-10-24 | `34d88395de861e9799eb9e24121a21c92c7a5adc` |
| [PRD](../prds/zava-forward-retrofit-programme-demonstrator.md) PRD-2026-AMA48-001 | in-review, 0.21.0, 2026-10-25 | `c788b917bafaede215f326f0efc71e071a687f1c` |
| [ADR 0002](../adrs/0002-pilot-readiness-architecture.md) | Proposed, no version field, 2026-10-24; its "no IoT Hub" sensor position is amended by ADR 0003 decision 6 | `cbe21530043ff15432cc6dce1086d080f5eb15b4` |
| [ADR 0003](../adrs/0003-journey-derived-capabilities-runtime-fit.md) | Accepted with amendment by the owner (2026-10-15, reconciled 2026-10-18), no version field, 2026-10-29; Basic hub exercise only, live gates separate | `d60645397b20fb70ac3d1dc47c7a6c8671201306` |

Requirement IDs are used only document-qualified because numbers collide:
BRD FR-048 (in-use monitoring capture), AC-090, RULE-014 and OD-43 (real
inventory, blocks operational use with real data, not the simulator
exercise); PRD FR-050 (simulated monitoring through IoT Hub), AC-066,
AC-067 and AC-068. BRD FR-050 is opt-in working memory and PRD FR-048 is
appointment commitment; neither is sensor work. The #184, #110 and #188
bodies cite BRD FR-048/OD-43 and PRD FR-050/AC-066 and are read that way.

### Planned feature to code, tests, journeys and backlog

Source inspection only; no code or test was executed for this record.

| Approved planned feature | Main code and tests (blob at `c6d5a8f3`) | Observed journey or execution | Remaining backlog |
| --- | --- | --- | --- |
| PRD FR-050 / AC-066 idempotent append, DQ, no public endpoint (ADR 0003 decision 6) | `src/core/src/zava_forward/core/sensor_consumer.py` (`8125b88b`), `src/api/src/zava_forward/api/sensor_ingestion.py`, `test_sensor_consumer.py`, `test_sensor_ingestion.py` | Local observed only as dated historical constructed SQLite/SQL Server runs (45 ingestion tests 2026-10-29); not re-executed here | #110: distinct Hub identities (criterion 1 unmet), Azure SQL, restart |
| PRD FR-050 live generation every home every five minutes (owner requirement 2026-11-04) | `src/core/src/zava_forward/core/synthetic/live_readings.py` (`289051ee`), `src/api/src/zava_forward/api/live_simulator.py`, `test_live_readings.py`, `test_live_simulator.py` | Implemented-unverified; stdout dry run and fakes documented, no live send | #184 parent criteria; #185 identity; #189 run controls; #140 hub |
| PRD FR-050 / AC-066 per-device Hub identity | `src/api/src/zava_forward/api/iot_stream.py` (`8eeaccbb`), `test_iot_stream.py`, `test_iot_credential_hygiene.py` | Fake-SDK only; no device issued, no stream sent (2026-10-29 B1 exercise was metrics only) | #185 (PR #1205 excluded), #110 |
| Handover consistency, ADR 0003 and PRD FR-050 | `synthetic/sensor_consistency.py`, `sensor_handover_verify.py`, `test_sensor_handover.py`, `test_sensor_consistency.py` | Local observed, historical (2026-10-30 and 2026-11-01 constructed witnesses, zero default tolerance) | #188: live and backfill queryable together, statistical handover, window rerun (all unmet) |
| BRD FR-048 / AC-090 retained raw observations, owned DQ | `sensor_consumer.py` retained witnesses, `sensor_reading` columns | Implemented-unverified; real data blocked by BRD OD-43 | OD-43 owners |
| PRD AC-067 / AC-068 review-signal authority and method evidence | `sensor_analysis.py`, `sensor_analysis_store.py`, research plan | Out of this record's refreshed scope; unchanged | Existing research gates |

### Raw weather and wire versus indoor observed series

* The live generator emits a wire message `live-sim-reading-v1` at 300-second UTC slots: `temperature_c` (`degC`), `humidity_pct` (`percent`) and `sunlight_wm2` (`W/m2`, global horizontal irradiance), `source_type=SYNTHETIC`, `scenario`, `seed`, `injected_fault=none` and a `label`. Its daily averages are an illustrative UK-like monthly table, a synthetic assumption, not retrieved weather and not an observed indoor series.
* The consumer admits only `sensor-fault-input-v1` rows with exactly the 13 closed fields of `READING_FIELDS` (including `calibrated` and unit fields, all strings). `sensor_reading` stores 11 columns: temperature and humidity only, no sunlight and no unit columns. Units and calibration claims come from trusted per-sensor controls.
* Therefore live-sim wire messages are not admissible by the main consumer and the main API README already says so. The sunlight value has no stored indoor representation: retained raw weather or wire provenance, an indoor projection and a continuous sunlight series are three different things, and nothing here promotes an outdoor or sunlight input to indoor risk evidence or claims indoor and weather equivalence. Classification: implemented-unverified (source and README), with the gap owned by #188 and its open, excluded PR #1203.
* Identifiers and timestamps: backfill `reading-v1` and composed rows use reading IDs of the form `<sensor>-<epoch seconds>` at three observations per day by default; live rows use `LIVE-<sensor>-<YYYYMMDDTHHMM>Z` at 288 per day. Idempotency is on `(sensor_id, reading_id)` within a producer. Cross-producer continuity at the handover instant is not observed on main. `sensor_key` is `S` plus ten base32 characters of the SHA-256 of the UTF-8 stock home ID; `home_key` accepts non-empty, untrimmed, control-free IDs up to 128 UTF-16 units. Export accepts 128 units but consumer availability and `observed_series` are bounded to 64 UTF-16 units and return `HOME_UNAVAILABLE` beyond it; that is a documented, deliberate boundary, not a new defect.
* Calibration: no physical calibration evidence exists. Legacy fixture calibration claims and managed envelope identity are not physical sensor calibration. Indoor-risk thresholds, lawful basis, retention basis and real resident consent are unknown and unapproved (BRD OD-43); exercise values stay exercise values.

### Retention, restart and handover limits

Historical, source-documented behaviour, not re-observed here: fresh receivers
replay the retained beginning (`starting_position="-1"`, non-inclusive) and
use SQL outcomes as durable state with no checkpoint store; retention expiry
is a recovery limit; concurrent receivers are not coordinated; database
commit uncertainty is explicit and cancellation does not prove rollback; a
poisoned envelope stops for investigation. A device ID must equal
`SYN-<sensor key>` and map to one stock home. An unsupported or missing
window is blocked or unknown and never a pass by omission. Legacy indoor
model continuity (constructed SQLite and SQL Server witnesses with zero
default tolerance, negative controls and reopened-window replay) is separate
from a versioned weather-to-weather continuity, which is proposed research
only and not an approved pivot.

### Evidence classification

| Finding | Classification | Source, date, limit |
| --- | --- | --- |
| Constructed backfill and suffix handover and 45 ingestion tests | local observed (historical) | Research plan entries 2026-10-29 to 2026-11-01 at their original heads; not re-run against `c6d5a8f3` |
| Bounded B1 hub exercise, metrics-only diagnostics | Azure observed (historical) | 2026-10-29 infra README; no device issued, no stream sent, no identity, SQL or retention acceptance |
| Generator schema and consumer admission mismatch | implemented-unverified | `c6d5a8f3` blobs above and API README; no execution |
| Sunlight wire field with no stored indoor column | implemented-unverified | Source inspection; no equivalence claimed |
| Retention, restart and commit-uncertainty behaviour | implemented-unverified | Source and README; Azure behaviour not observed |
| Joint Azure SQL query, restart and live handover | deferred | #188; not an owner-approved deferral of acceptance |
| Distinct Hub identities, credential issue and teardown | blocked | #110, #185; need approved credential owner action, not agent supply |
| Candidate FULL validation of #1203 and #1205 | blocked | Heavy lock owned by native rpi96 FULL gate (PID 1361642 observed alive at 2026-11-05, running `tools/rpi-checks.py --all --jobs 1 --lock-timeout 0 --base c6d5a8f3`); observation only, no authority to stop it |
| Physical calibration, thresholds, lawful retention, real consent | unknown | BRD OD-43; no fixture or agent can supply them |

No native gate receipt, IoT send, indoor and weather equivalence, threshold,
calibrated acceptance or approved pivot is recorded or invented.

### Actual commands, exits and limitations

Recorded in the changes artifact after the final validation run. Not run:
`tools/rpi-checks.py` (acquires the shared heavy lock), package suites, SQL
Server, Docker and images, Chromium, FULL gate, cloud, provider and model
calls, billing and private datasets. Those paths are unperformed, not
passed. The change is documentation only; no source, schema, coordinator
or workflow file was edited.

### Existing authorizations

The owner comments on #184 (2026-11-04 live every-home five-minute and
smoothed-climate requirement; 2026-11-05 authorization within the existing
USD700 cap, scoped simulator job permissions and admin-only controls; 2026-11-05
retained scoped approvals) are existing direction, are not requested again and
do not waive exact-head validation, capacity or secret controls. No physical
calibration or indoor-risk approval exists.

### Findings, triage and recommendation

No new confirmed defect or refactor need was found. The findings above are
owned by existing open issues, so none was filed: contract and seam
continuity #188 (PR #1203 excluded), ingestion and Hub identity #110 and
#185 (PR #1205 excluded), run controls #189, hub #140 and the checkpoint #440.
The 64 versus 128 unit boundary is documented by the core README.

Recommendation: **continue** this bounded record, **fix** the admission,
sensor-schema and handover gaps in the existing #188 and #185 lanes after
their candidates pass their own independent FULL receipts, and treat versioned
weather-to-weather continuity as a **proposed pivot** that awaits owner
approval; none is approved here and no new permission is requested.

| Gate | Condition to close or expand |
| --- | --- |
| #184 (keep open) | #185, #188 and #189 closed or owner-deferred; actual credential, log and telemetry evidence on a Hub |
| #110 (keep open) | Actual distinct Hub identity with schema version and stable reading ID; Azure SQL and restart evidence |
| #188 (keep open) | Live and backfill series queryable per home, statistical handover within declared tolerance and idempotent window rerun on a validated head |
| #440 (keep open) | Criterion 7 triage and criterion 8 Major HVE Builder host evidence for the coordinator remain open; this record does not satisfy either |
| Dependent expansion | Gate only work that relies on unvalidated sensor ingestion, live handover, indoor interpretation or scale; independent documentation and unrelated engineering continue |

Resume conditions: the native FULL gate releases `/tmp/ama-rpi-heavy.lock`;
#1203 and #1205 obtain current exact-head FULL receipts and independent
assessment by the coordinator; the validated integration candidate is
requalified against its actual main base; an authorized credential owner
completes any live issuance. Independent lanes: coordinator (gates,
integration), #188 owner lane (handover), #185 and #140 owners (identity and
hub), #189 (run controls), named human owners for OD-43 decisions.
Final independent exact-head assessment remains coordinator-owned. A
pivot or deliberate deferral needs explicit owner approval. This record uses
`Refs` only; no issue is closed or ticked.

### Parent-base refresh qualification (2026-11-05, local, Refs #440 #184 #110)

The record above is preserved unchanged at its original observation: base
`3d7ad2feaa9c4cba5fe917edd2fbc40e40a5c246`, main `c6d5a8f3c3a35892322300be27b9747f7b11362d`,
original published head `3082206618ca484aab6d35531e89248773fc3295` (PR #1212).
This qualification only records a documentation branch refresh.

| Item | Value |
| --- | --- |
| Refreshed declared parent (`feat/discovery-assurance-integration-123`) | `e546bf23e491c49de56eaa08d4e68eab48517660`, tree `adcdf2db7a29cbb5664d522e1741401c95c021f3`, after the guarded child #1211 merge |
| Parent-only delta from original base | One commit (#1211, constructed paired-cohort comparability): `src/core/.../paired_equity.py`, its test, `src/core/README.md` and #128 tracking records. No sensor, IoT, `docs/` or `infra/` path changed |
| Current main | Unchanged at `c6d5a8f3`. The parent-only #1211 and cohort #128 source are not main and are not sensor or acceptance evidence |
| Sensor source identity | Blobs for `live_readings.py` (`289051ee`), `sensor_consumer.py` (`8125b88b`), `sensor_faults.py`, `sensor_identity.py`, `sensor_backfill.py`, `iot_stream.py`, the API README, BRD, PRD and ADR 0003 are identical at `c6d5a8f3` and at the refreshed branch base (observed with `git rev-parse` on both) |

Every classification, exclusion and gate above stays as recorded. The
original partial review is a documentation-scope review of the original head
and is not promoted to current-main acceptance. #440 criteria 7 and 8 and the
#184, #110 and #188 gates stay open; no approval, pivot or deferral is
inferred. Source inspection does not establish SQL, browser, IoT or human
acceptance.

Process disclosure: the earlier run removed its own scratch directory
`/tmp/s440` with `rm -rf` without a retained finite selection, archive,
readback or restore proof. The committed RPI records and session log survived;
no backup or restoration of that scratch exists or is claimed. Checks in this
refresh are new observations, not recovery.

## Sixth stabilization checkpoint: parent-topic paired comparability integration (2026-11-05, Refs #440 #128 #123)

Refs #440, #128 and #123. Bounded, documentation-only, local-only record of
the affected surface after the completed parent-topic child wave #1211
(constructed paired-cohort comparability) and #1212 (qualified sensor
documentation). It is separate from, and does not restate, the
[fifth checkpoint](#fifth-stabilization-checkpoint-current-main-sensor-contract-retention-and-handover-2026-11-05-refs-440-184-110):
that earlier record was sensor-only and did not cover the comparability
integration. It adds no source, schema, threshold, coordinator, workflow or
requirement change, no approval and no pivot, and it is independent of sensor
acceptance and of any actual AI or human approval. Original RPI evidence is
under `.copilot-tracking/*/2026-11-05/parent-comparability-checkpoint-440-*`.

### Trigger, identities and observation scope

The existing owner is #440 (open, parent #123); no duplicate checkpoint issue
was created. Parent #123 closure and dependent cohort expansion wait for this
scoped record, which is a precondition and not an acceptance.

| Item | Value |
| --- | --- |
| Declared parent topic `feat/discovery-assurance-integration-123` (remote head read with `git ls-remote`, 2026-11-05) | `ad1ee0264a381fb76de100417c535a4e194e2460`, tree `8052fa5d3248c9dc3a4f9cb8558ccfbfa65e360e`; the local ref of that name was stale at `3d7ad2fe` and was not used |
| Observed documentation head (branch `docs/parent123-checkpoint-wave2`) | Started at the same `ad1ee026`; this section is added on top |
| Current `origin/main` (fetched 2026-11-05) | `c6d5a8f3c3a35892322300be27b9747f7b11362d`, tree `876679c32ff8f8a3d35822d9e46d8b377ce15428` |
| Merge base of parent and main | `3d7ad2feaa9c4cba5fe917edd2fbc40e40a5c246`. Parent is two commits ahead (#1211 `e546bf23e`, #1212 `ad1ee0264`); main is one commit ahead (#1210, delivery tooling only) |
| Merge state | #1211 and #1212 are merged into the parent topic only. They are not on main. Parent-only source is not merged-main acceptance |
| Excluded, unmerged | #1203, #1205, #1141 and #1206 (all open when checked, 2026-11-05). Their source was neither read nor adopted; no private dataset was read |
| This evidence pack blob before this section (parent head) | `9e7ffed7a571f4381d5ddb743f3ac84688818efa` (main: `2566e8efd7084346421fffb101d5b171100dfd63`) |

Actual observation scope: parent-topic source at `ad1ee026` only. Nothing was
run against main, so main behaviour is known by blob identity alone. Main
still holds the unfixed `paired_equity.py` blob `d29768d5`, the blob on which
the original #128 reproduction (a confounded pair returning `pass`) was
recorded; the fix is `5aedcd7b` on the parent topic only.

Document identities, identical at parent and main. Draft, in-review and
proposed documents are not approvals by this record.

| Document | Status, version, date | Blob |
| --- | --- | --- |
| [BRD](../brds/agentic-retrofit-programme-brd.md) BRD-2026-AMA48-001 | draft, 0.21.0, 2026-10-24 | `34d88395de861e9799eb9e24121a21c92c7a5adc` |
| [PRD](../prds/zava-forward-retrofit-programme-demonstrator.md) PRD-2026-AMA48-001 | in-review, 0.21.0, 2026-10-25 | `c788b917bafaede215f326f0efc71e071a687f1c` |
| [ADR 0002](../adrs/0002-pilot-readiness-architecture.md) | Proposed, no version field, 2026-10-24 (decision 4 is cited by `ranking_publication.py`) | `cbe21530043ff15432cc6dce1086d080f5eb15b4` |
| [ADR 0003](../adrs/0003-journey-derived-capabilities-runtime-fit.md) | Accepted with amendment by the owner, no version field, 2026-10-29 | `d60645397b20fb70ac3d1dc47c7a6c8671201306` |

Requirement IDs are document-qualified because numbers collide: PRD FR-054
(versioned cohort and missing-data evaluation record), PRD AC-073 (paired
constructed cohorts, seeded defects detected, thresholds block activation
pending human disposition; its status cell reads "Not run"), PRD FR-012,
PRD PR-006 (deterministic ranking, versioned policy), PRD OQ-018 (which
cohorts, lawful fields, thresholds and windows apply; open), BRD NFR-008
(accessibility and unfair-exclusion testing with human review of missing
data), BRD NFR-009 (journey ownership, service times, tested manual
alternatives) and BRD AC-064 and AC-071. The #128 body also cites BRD
RULE-005 and PRD SA-009, SA-010 and AC-055; those were not re-reconciled here.

### Paired diagnostic to boundaries

Source inspection of blobs at `ad1ee026`, plus the one observation below.
`paired_equity.evaluate` is a pure, constructed-fixture check. It imports
only `journey_register`, `ranking` and `rai_release.digest`.

| Boundary | Source and tests (blob at parent, unchanged from main unless stated) | Relationship to the paired diagnostic | Limit |
| --- | --- | --- | --- |
| Paired diagnostic | `paired_equity.py` (`5aedcd7b`, changed from main), `test_paired_equity.py` (`f9b07cb6`, changed), `src/core/README.md` (`bb709453`, changed) | Predeclared fixture-local contrasts reject confounded, no-contrast and mislabeled pairs as `invalid_comparison` blockers and `invalid_pairs`; an invalid pair counts as neither tested nor failed; `activation_allowed` and `fairness_evidence` stay false | The contrast table is not a production field mapping or an approved policy; seeded-defect accounting on a rejected pair is not separately tested |
| `journey_register` | `journey_register.py` (`92f75403`), `test_journey_register.py` (`12c114aa`) | `human_review_route` supplies the rank-effect-none check used per pair; the register evaluation of owners, measures and tested manual alternatives (BRD NFR-009) is not called by the diagnostic | A supplied register is checked, never invented; no owner, threshold or manual-alternative test result is approved |
| `ranking` and `ranking_publication` | `ranking.py` (`052bc6b9`), `ranking_publication.py` (`934ef16d`), `test_ranking_publication.py` (`6b66f232`) | `ranking.rank` is the default ranker for position comparison; an injected ranker is allowed. Publication (immutable dated snapshots, `verify`, `overdue`) is a separate retained-archive boundary the diagnostic does not call | Retention period is a Legal decision and the schedule belongs to the deployment; ADR 0002 is Proposed. Store and API wiring (`store.py`, `api/server.py`) was inspected by reference only |
| `rai_release` and invalidation | `rai_release.py` (`970678ca`), `test_rai_release.py` (`d8a346cb`), `test_rai_release_invalidation.py` (`1ca9d5e7`) | Only `digest` is shared. The diagnostic does not select, admit or invalidate any release record, so a comparability result cannot revoke or activate anything | Exercise release records and invalidation tests are constructed; no actual release authorization exists |
| `cohort_eval` | `cohort_eval.py` (`60907194`), `test_cohort_eval.py` (`47e0c7f3`), `cohort_eval_fixture.py` (`f5bb1cfc`); agent consumers in `src/agents` were not run | Not imported by the diagnostic. `cohort_eval` holds the approved expected-outcome manifest, approval binding and thresholds (PRD AC-073); the paired diagnostic predeclares only fixture contrasts | Mocked or fixture approvals and thresholds are not actual approvals. Threshold approval stays open (PRD OQ-018) |

No integration seam between `paired_equity` and `cohort_eval` or the release
invalidation path exists in source, and none is required by this record; the
absence is stated, not raised as a defect, because the owning criteria (#128
cohort and release acceptance) are open and unclaimed.

### Evidence classification

| Finding | Classification | Source, date and limit |
| --- | --- | --- |
| 74 coupled core tests pass on the parent-topic candidate | local observed (parent-topic only) | Observation below, 2026-11-05; no run on main, no full core, API or agents suite |
| Comparability fix and the four historical confound fixes present in `paired_equity.py` | local observed (parent-topic only, tests) and implemented-unverified beyond constructed fixtures | Source blob `5aedcd7b`; constructed pairs only |
| Original NOT CLEAN review of #1211 work (two Medium) | historical adverse outcome, preserved | `.copilot-tracking/reviews/2026-11-05/issue-128-paired-cohort-comparability-review.md`; two pre-freeze fixes were verified by tests and never independently re-reviewed in that record |
| Correction-2 adverse findings (nested sequence type masking, dotted-key shadowing) | historical adverse outcome, preserved | Same review and changes records; self-check by tests only, no review approval claimed |
| Published exact-head functional assessment of #1211 (verdict approve, no findings) | separate later outcome, helper-only | `issue-128-published-functional-assessment.json`; reading only, constructed diagnostic scope; it does not supersede, approve or regrade the original review |
| Independent published readiness approval of the #1212 sensor documentation (0 findings) | separate outcome for sensor documentation only | Reported in the #440 comment of 2026-11-05 (read only); not a comparability review |
| Azure observation of the comparability, cohort or release surface | none (no Azure observation exists for this surface) | Historical Azure records elsewhere in this pack concern other surfaces |
| Paired diagnostic with `cohort_eval` manifest, release invalidation and ranking publication integration | implemented-unverified (components) and unknown (integration) | No seam exercised; not run end to end |
| Actual-model or AI task evaluation of paired cohorts | deferred | Needs an approved task, manifest and thresholds |
| Independent expected-pair manifest, thresholds, representative cohorts, lawful fields (PRD OQ-018) | blocked | Named human approval; no agent or fixture can supply it |
| Keyboard and screen-reader testing, user research, assistive-technology acceptance | blocked | #128 criteria; no results exist |
| Population fairness, lawful protected-characteristic fields, activation of any task | unknown | Constructed pairs are not population evidence; nothing is approved or activated |
| Hosted CI on the parent topic | unknown | No hosted green run is claimed for these documents |

An accepted helper implementation is not actual AI, cohort, population
fairness, threshold, lawful-field, user-research, assistive-technology or
human acceptance, and none of those exists. Fixtures, mocked approvals, false
activation flags and fairness flags are not approvals.

### Actual commands, exits and limitations

All commands ran from `src/core` of the documentation worktree, Python 3.12.3,
with `PYTHONDONTWRITEBYTECODE=1` and an explicit
`PYTHONPATH=<worktree>/src/core/src:<worktree>/src/core/tests`. The existing
external environment `/tmp/rpi128-venv` was used read-only. Its editable
installs resolve through other trees first (a sibling worktree and the primary
checkout), so the explicit path was required and the loaded paths were
asserted; no installation or shared-environment change was made.

| Command | Exit | Result |
| --- | --- | --- |
| Import `paired_equity` and assert `__file__` is under this worktree's `src/core/src/` | 0 | Candidate path confirmed |
| `python -m unittest tests.test_paired_equity tests.test_journey_register tests.test_rai_release tests.test_rai_release_invalidation tests.test_ranking_publication tests.test_cohort_eval` | 0 | 74 tests OK in 0.062 s |
| Assert `__file__` under this worktree for the six modules and six test modules | 0 | All twelve confirmed |
| `git status --short --ignored` after the runs | 0 | Empty (no bytecode written) |

The log is outside the repository at
`/tmp/parent123-comparability-440/core74.log`; it is a command summary, not a
gate receipt. Not run: `tools/rpi-checks.py`, SQL Server, Docker and images,
browser, cloud, provider and model calls, billing, private datasets, the full
core, API or agents suites, Ruff or mypy. Those paths are unperformed, not
passed. The native FULL gate lock, its receipt and images were not touched.

### Findings, triage and recommendation

No defect was confirmed. No finding was compared against a new owner, no
issue was filed and no refactor is proposed. Unreproduced observations, left
with existing owners (#128 and its coordinator lane) and not raised as
defects: the optional seeded-defect-on-rejected-pair regression named by the
published assessment, strict type equality separating mapping subclasses, and
the absence of an integration seam with `cohort_eval`.

Recommendation: **continue** the parent-topic integration under #123 with
this record as the affected-surface stabilization precondition. **Fix**: none
required; no defect is confirmed. **Proposed pivot**: none new. The earlier
versioned weather-to-weather continuity proposal remains proposed research
only; the #188 weather interpretation remains unanswered by the owner and is
not assumed. No requirement is relaxed and no pivot is approved.

| Gate | Condition to close or expand |
| --- | --- |
| Parent #123 closure | The parent-topic work is integrated into main through an independent exact-head local gate and a requalification against the actual main base; #128 is closed or owner-deferred; the sensor lane (#184, #110, #188) is closed or owner-deferred; #440 criteria 7 and 8 are met; human approvals recorded by named owners |
| #128 closure (keep open) | Keyboard and screen-reader testing, human review of missing data and incomplete appointments, agreed user-research protocol, independent expected-pair and threshold approval (PRD OQ-018), lawful-field decision, actual-model run where relevant and named human acceptance |
| Dependent cohort expansion | Gate only work that relies on the comparability fix being on main, on approved cohort thresholds or manifests, or on a fairness or population claim. Independent documentation and unrelated engineering continue |
| #440 (keep open) | Criterion 7 triage and criterion 8 Major HVE Builder host evidence for the coordinator remain open; this record satisfies neither |
| Sensor gates | #184, #110 and #188 stay open as recorded in the fifth checkpoint; nothing here changes them |

Resume conditions: the parent topic is refreshed against current main and
requalified with its own exact-head gate by the coordinator; the native FULL
gate releases the shared heavy lock before any heavy validation; named human
owners decide the open OQ-018 items. Independent lanes: coordinator (gates and
integration), #128 owner lane (accessibility, user research, approvals),
#188 and #185 owners (sensor lanes), named human owners for approvals. A pivot
or deliberate deferral needs explicit owner approval. This record uses `Refs`
only; no issue is closed or ticked.

### Process disclosure

The earlier #440 run removed its own scratch directory `/tmp/s440` with
`rm -rf` without a retained finite selection, archive, readback or restore
proof. That disclosure survives. This task deleted nothing, including its own
scratch and logs, created no backup or archive, and its new observations are
not a restoration. No human approval, gate receipt or review approval is
invented; the one independent review of this documentation diff is recorded
in the tracking review artifact with its original outcome.

## Seventh stabilization checkpoint: current-main UI and cache recovery (2026-11-05, Refs #440 #96)

Refs #440 and #96. Bounded, documentation-only, local-only record of the
recovery after the two merged main fixes for #1215 (API discovery bytecode) and
#1214 (320px case-summary header spacing). It is separate from the
[sixth checkpoint](#sixth-stabilization-checkpoint-parent-topic-paired-comparability-integration-2026-11-05-refs-440-128-123),
whose parent-topic observation, original NOT CLEAN review and #1213 records
stay parent-only, immutable and are not regraded. It adds no runtime,
coordinator, workflow, threshold, requirement or ADR change and no approval.
Its original RPI evidence is under
`.copilot-tracking/*/2026-11-05-ui-cache-checkpoint-wave3-440-*`.

**The planned focused observation of current main was NOT performed.** The
exclusive heavy lock was held by another session, and this task did not queue,
wait or retry. Both focused checks are blocked and unrun, not passed.

### Source and document identities

| Item | Value |
| --- | --- |
| Current main, pinned after scorer run 42036086584 completed `success` and two fetches agreed (2026-11-05, about 13:36Z) | `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`, tree `5c2988b71aec609b007b41f408685d54e2c28e0d`. It is the bot commit `chore(rubric): record score 77/100` (13:34:38Z); its only change from `2edba50b7` (#1219) is `.github/rubric/scores/latest.json`, 4 lines |
| Merged fixes under checkpoint | #1217 `180dcf3e2` (#1215, `Runner.install_bytecode_policy()` called from `Runner._install("api")`); #1219 `2edba50b7739b83b88ba491648717a9750777a0c` (#1214, merged 13:28:35Z). #1214 and #1215 are closed |
| Parent topic `feat/discovery-assurance-integration-123` (child base, unchanged) | `23cdae38b1fe47a47ba5f3f356ed18253aad9c46`, tree `263475b0e4d01203186b42b5311f4c85c0d4f5dd`. It is 3 ahead of and 4 behind the pre-rubric main, is not current main and lacks the #1215 and #1219 fixes |
| Documentation child | Branch `docs/parent123-ui-cache-checkpoint-wave3` based on the parent `23cdae38`; no merge, rebase, reset, retarget or flattening to main |
| This evidence pack blob at the parent before this section | `3aec3dd44b24d4bf039faadced830ae25b9deba5` (main: `2566e8efd7084346421fffb101d5b171100dfd63`; they differ because the parent carries the sixth checkpoint) |

| Document | Status, version | Blob (main and parent equal, verified with `git rev-parse`) |
| --- | --- | --- |
| BRD-2026-AMA48-001 | draft, 0.21.0 | `34d88395de861e9799eb9e24121a21c92c7a5adc` |
| PRD-2026-AMA48-001 | in-review, 0.21.0 | `c788b917bafaede215f326f0efc71e071a687f1c` |
| ADR 0003 | Accepted with amendment by the owner (2026-10-15, reconciled 2026-10-18) | `d60645397b20fb70ac3d1dc47c7a6c8671201306` |
| ADR 0006 | Accepted (owner, 2026-10-15) | `956da1a3b804c803041fe2e8a312bd9f400273ae` |

Draft and in-review documents are not approvals. Excluded, unmerged: the #96
feature, schema and Finance acceptance (#96 is open) and every other parent
or sibling branch change not on main. Parent-only source was never run or
labelled as main.

### Traceability to source and tests

Requirement IDs are document-qualified; reads are of main blobs.

| Requirement or decision | Implementing source and tests on main | Limit |
| --- | --- | --- |
| BRD NFR-008 and AC-064 (accessibility, unfair-exclusion testing, digital and non-digital journeys) | `src/api/checks/case_journey_browser_check.py`: reflow over 320, 390 and 1280 CSS px at height 800 asserting `scrollWidth <= innerWidth`; 320x800 `.case-summary` bottom `<= 1600`; reduced-motion and forced-colour states; stacked fallback when the enhancement script is missing | Synthetic fixture and engineering checks, not live-contact or user-research acceptance |
| BRD NFR-009 and AC-071 (owned journeys, tested manual alternative) | Same check: manual-route fixture, keyboard Enter, Home, End, Space and Escape paths | Owner-set thresholds (OD-09, OD-25) are not approved here |
| PRD NFR-001, NFR-018, AC-093 and AC-134 (keyboard, focus, reflow at 320, 390, 1280) | Same check | PRD acceptance status cells read "Not run"; six-script, zoom and screen-reader results are not provided here |
| ADR 0003 decision 2 (authority enforced in the API, not a view) | The check drives the real server and moves no authority into a view | ADR 0003 has no reflow or keyboard text; the trace is indirect |
| ADR 0006 (src layout and cut-over gate) | `tools/rpi-checks.py` `Runner._install("api")` then `install_bytecode_policy()`; scrubbed harness server launch; `tools.test_rpi_checks.GateTests.test_api_install_prevents_scrubbed_server_child_writing_source_bytecode` | ADR 0006 has no bytecode clause; the trace is through its gate and layout rules |
| #96 full gate versus #96 feature | Full-gate dependency is the fixed Runner install and the 320px contract | A focused main pass would not be a #96 full receipt; the earlier #96 full receipt failed, is non-resumable and is preserved |

### Evidence classification

| Finding | Classification | Source, date and limit |
| --- | --- | --- |
| Main, parent and document identities above | local observed (git only) | `git fetch`, `rev-parse`, `diff --stat`, 2026-11-05 |
| Auxiliary main environment: detached clean worktree at `bb3a3b03`, own venv, editable installs of `src/core`, `src/agents`, `src/api[dev]`, `pip check` clean, `zava_forward.*` and `playwright 1.64.0` resolve inside the worktree | local observed (environment only) | Not a check result; ignored `*.egg-info` directories exist in that worktree |
| Pinned axe 4.10.3 copy | local observed | SHA-256 `880970c0...a68bb` equals `AXE_SHA256` in `tools/rpi-checks.py`; copied from existing evidence, none modified |
| Bytecode isolation regression on main | blocked (not run) | Lock held, below |
| Case-journey browser check on main (320x800 bound 1600, wider and keyboard states, reduced motion, manual controls) | blocked (not run) | Lock held, below |
| #1219 reported 19 checks pass, independent published functional and readiness Pass, premerge partial receipt verified; #1215 merged with the real-producer test | implemented, reported by the merged issue and PR records; not re-observed by this record | Premerge partial receipt is not a main or full receipt |
| Azure observation of this surface | none | Local synthetic checks only |
| Actual AI, user research, assistive-technology and human acceptance | deferred or blocked | Named owners and approved plans |
| Hosted CI on this documentation child | unknown | Nothing published |

### Actual commands, exits and the lock

| Step | Result |
| --- | --- |
| `git worktree add --detach /tmp/ama-main-440-ui-cache-wave3 bb3a3b03...` (path absent first) | Exit 0, clean |
| New venv `/tmp/ama-main-440-ui-cache-wave3-venv`, editable installs, bytecode policy `.pth` written, `pip check` | Exit 0 |
| `flock -n -x /tmp/ama-rpi-heavy.lock -c <both focused checks>` at about 13:37:15Z | Exit 1 immediately; neither check ran; no check output exists |
| Passive `lsof` of the lock at 13:37:29Z | Held by `python3 tools/rpi-checks.py --changed --base bb3a3b03... --out /tmp/r233f --lock-timeout 0` (pid 1560051) from `/tmp/ama-wt-233-gate-final`, an issue #233 session |

No queue, wait, retry, interruption, or change to the holder's worktree,
images or environment occurred. The browser, SQL, Docker, cloud and model
paths were not exercised.

Resume point, for a later session that can take the lock without queueing:
`flock -n -x /tmp/ama-rpi-heavy.lock` around (1) from the auxiliary worktree
root `python3 -m unittest tools.test_rpi_checks.GateTests.test_api_install_prevents_scrubbed_server_child_writing_source_bytecode`
and (2) from `src/api`, the auxiliary venv's
`checks.case_journey_browser_check --axe /tmp/ama-main-440-wave3-out/axe-4.10.3.min.js --out /tmp/ama-main-440-wave3-out/journey`
with a scrubbed environment, `TMPDIR` external and module identities asserted.
Re-fetch and re-pin `origin/main` first; a different pin needs its own worktree.
The prepared external paths `/tmp/ama-main-440-ui-cache-wave3`,
`/tmp/ama-main-440-ui-cache-wave3-venv` and `/tmp/ama-main-440-wave3-out` are
retained, not deleted.

### Findings, triage and recommendation

No new defect was reproduced or confirmed, because the observation did not run.
Nothing differs from #1214 or #1215, so no new issue is proposed and no
refactor or package-card correction is proposed.

Recommendation: **continue**. **Fix**: none confirmed. **Pivot**: none.
The #1214 and #1215 recoveries rest on the merged owners' evidence until the
focused main observation above is taken. A blocked observation is not a pass.

| Gate | Effect |
| --- | --- |
| Publication of this child | Needs coordinator independent exact-head assessment, hosted checks and human approval; none is claimed |
| Parent #123 closure | Still needs the parent refreshed against main with its own exact-head gate, plus the conditions in the sixth checkpoint |
| #96 full-gate receipt | A new native full receipt by its own session; this record supplies none |
| #440 (stays open) | Criterion 7 whole triage and criterion 8 Major HVE Builder behaviour-testing and host validation are not covered; no coordinator behaviour changed |

Independent lanes continue. This record uses `Refs` only; no issue is
closed or ticked.

### Process disclosure

No existing record, cache, snapshot, image or evidence was deleted, moved or
modified. New external paths were created, not overwritten, and retained
without archive or backup. The one axe file was copied from existing
evidence. No human approval, receipt or review approval is invented.

### Required-observations continuation: actual results (2026-11-05, Refs #440 #96)

This continuation is separate and dated after the record above. The unrun
statements above stay as the historical record at that time; they are not
rewritten. Both required focused checks have now run on current main, in a
documentation child that stays based on parent `23cdae38`. This is focused
stabilization evidence only: not a full or `--changed` gate, not a #96 full
receipt, and not #440 C7 whole triage, C8 HVE Builder host validation, legal
or human approval, Azure or #96 feature acceptance. Original RPI evidence is
under `.copilot-tracking/*/2026-11-05-ui-cache-required-observations-followup-440-*`.

| Item | Value |
| --- | --- |
| Child head and tree at start | `66c81b2893f00442813220d322d254927e68f9eb`, tree `650251ad26ca0af27c3c5bb5ef633341e5f337ad`, clean |
| Main re-resolved at admission (2026-11-05, 15:02Z) | `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`, tree `5c2988b71aec609b007b41f408685d54e2c28e0d`, unchanged from the earlier pin; latest scorer run 42036086584 `completed` `success`; no newer commit |
| Parent (unchanged, not moved) | `23cdae38b1fe47a47ba5f3f356ed18253aad9c46`, tree `263475b0e4d01203186b42b5311f4c85c0d4f5dd` |
| Document blobs and status | Unchanged and re-read equal at main: BRD `34d88395...` draft 0.21.0, PRD `c788b917...` in-review 0.21.0, ADR 0003 `d6064539...` accepted with owner amendment, ADR 0006 `956da1a3...` accepted. Draft and in-review are not approvals |
| Clean observed source | New detached exact-main auxiliary `/tmp/m440b` at `bb3a3b03`, 0 tracked, untracked or ignored entries before and after the observations; no `__pycache__` or `*.pyc` under it |
| Environment | The existing #440-owned venv `/tmp/ama-main-440-ui-cache-wave3-venv` was reused without any install (Python 3.12.3, playwright 1.64.0, `src/api/pyproject.toml` identical in both auxiliaries). Explicit `PYTHONPATH` placed `/tmp/m440b/src/{core,agents,api}/src` and the tests ahead of the editable installs; `zava_forward.core.store` and `zava_forward.api.server` resolved to `/tmp/m440b/...`, and the checker `__file__` is `/tmp/m440b/src/api/checks/case_journey_browser_check.py`. Scrubbed environment (`env` cleared), `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR` external, stdin from `/dev/null` |
| Lock | One non-blocking exclusive `fcntl` hold of `/tmp/ama-rpi-heavy.lock` across both checks, acquired 15:03:36Z, released 15:05:14Z. It was free on probe (no holder, no runner process), so no queue, retry or wait occurred |
| Axe | The copied pin `/tmp/o440c/axe-4.10.3.min.js`, SHA-256 `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb`, equal to `AXE_SHA256` in main `tools/rpi-checks.py`; copied from the #440 wave3 output copy, nothing downloaded |
| Browser | Chromium `156.0.8078.4` (Playwright cache `chromium-1248`), axe 4.10.3 as reported in `results.json` |

| Check | Command (from) | Exit | Result |
| --- | --- | --- | --- |
| 1. Real-producer bytecode isolation | `python -m unittest -v tools.test_rpi_checks.GateTests.test_api_install_prevents_scrubbed_server_child_writing_source_bytecode` (`/tmp/m440b`) | 0 | `Ran 1 test in 0.722s`, OK, no skips. The test itself asserts the owned loopback server responded and no `__pycache__` or `*.pyc` appeared under its scratch source roots |
| 2. Case-journey browser check | Runner `BROWSER_ENTRY` equivalent around `checks.case_journey_browser_check --axe /tmp/o440c/axe-4.10.3.min.js --out /tmp/o440c/journey` (`/tmp/m440b/src/api`) | 0 | 407 `PASS` lines and no `FAIL` line (the 17 other lines are printed page text); `results.json`: 87 axe scans, 0 page errors, zoom `chrome.tabs.setZoom=2; innerWidth<=640`. `320x800 summary within one viewport scroll (1592.40625)` against the unchanged bound 1600; 320, 390 and 1280 reflow, reduced-motion and forced-colour, missing-enhancement fallback, keyboard focus and 200% zoom all pass. Screenshots `mobile-320.png`, `desktop-1280.png`, `forced-colours.png`, `browser-zoom-200.png` retained |

The 320px margin is 7.6 CSS px under the 1600 bound; it passes and is stated
as a thin margin, not a defect. No skip, threshold, test or harness change was
made. Preserved outputs: `/tmp/o440c` (accepted observation) and `/tmp/o440b`
(a first attempt whose check 1 also passed, exit 0; its check 2 exited 1
because the runner script had pre-created the `journey` output directory
and pre-imported the module, a harness mistake before any browser step, so
it is not a product result). Nothing was deleted.

| Finding | Classification |
| --- | --- |
| Bytecode isolation regression passes on exact current main source | local observed (main, focused) |
| Case-journey browser check passes on exact current main source at the unchanged 320x800 bound and wider, keyboard, reduced-motion and manual-fallback states | local observed (main, focused, synthetic fixture) |
| Together with the merged #1215 and #1219 records, the two recoveries are reproduced on main | local observed; they are not a full or `--changed` gate, not a #96 full receipt and not a sealed receipt |
| Resident, assistive-technology, screen-reader and user-research acceptance, six-script PRD AC-134 | blocked or deferred, as before |
| Azure observation, actual AI | none |
| #96 feature, schema and Finance acceptance | excluded, unmerged |
| Hosted CI and independent exact-head assessment of this documentation child | unknown (coordinator work) |

No new defect was reproduced, so there is nothing to compare with #1214 or
#1215 and no new issue, fix or refactor is proposed.

Recommendation: **continue**. **Fix**: none confirmed. **Pivot**: none.
Gates: publication of this child still needs the coordinator independent
exact-head assessment, hosted checks and human approval; parent #123 closure
still needs the parent refreshed against main and requalified (the parent
lacks the #1215 and #1219 fixes); a #96 full receipt must come from its own
native full run; #440 stays open for criteria 7 and 8. Issues are not closed or
ticked.

Process disclosure: the old auxiliary `/tmp/ama-main-440-ui-cache-wave3`
(known ignored `*.egg-info`) and the venv were reused read-only or left
unchanged and are not the observed clean source. The runner scripts
`/tmp/o440b-run.py` and `/tmp/o440c-run.py` are retained outside the
repository. Nothing was deleted, moved, archived or cleaned.

## Eighth stabilization checkpoint: integrated parent topic preparation (2026-11-05, Refs #123 #440 #128)

Refs #123, #440 and #128. Local, light-only preparation of the parent topic
`feat/discovery-assurance-integration-123` for an eventual main integration.
It is not documentation only: the integrated surface carries the constructed
#128 diagnostic `paired_equity.py` and its tests. It adds no runtime behaviour,
threshold, approval or requirement change. Epic #123 acceptance criteria 1 and
2 stay unchecked and unproven; #440 criteria 7 and 8, the whole-#440 HVE
residuals, company-owner and data prerequisites, actual-model, threshold and
lawful-field approvals, resident and accessibility research and authorized
Azure-only residuals stay outstanding. Holds on weather and indoor series
(#82, #188) and the #1204 HVE item stay scoped as before. Original RPI
evidence is under `.copilot-tracking/*/2026-11-05/parent-integration-preparation-123-*`.

### Source, intake and merge identities

| Item | Value |
| --- | --- |
| Old local placeholder (strict ancestor, kept) | `3d7ad2feaa9c4cba5fe917edd2fbc40e40a5c246` |
| Remote parent intake (fetched 2026-11-05) | `63dd5798ee474ea3137018749b604c1f78774801`, tree `73c8eda8f49891aea173623f79e1fd8f95c7ec1b` |
| Fresh main baseline (fetched 2026-11-05) | `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`, tree `5c2988b71aec609b007b41f408685d54e2c28e0d` |
| Remote-parent merge (ordinary, fast-forward eligible) | local head became `63dd5798`, tree `73c8eda8` |
| Main merge commit (ordinary, no reset, rebase or force) | `6703b0b1a9e44844fc64446c8a311d28f36dec81`, tree `e23d35e72b480ba0c650e57f754871a23353a14f`; parents `63dd5798` and `bb3a3b03` |
| Final frozen local head | the commit that adds this section; reported in the task hand-off, not self-referenced here |

Both tips are ancestors of the merge commit (`git merge-base --is-ancestor`
exit 0 for each). `docs/reference/log.md` auto-merged with no conflict;
afterwards no line of either side's log was removed (zero deleted lines
against each parent). The prior compound command that reported exit 1 after
the merge ended in `grep -v` over an empty tracked-change list, which exits 1
by design; the merge itself succeeded and was rechecked separately. No parent
pull request existed (open: #1216, #1205, #1203, #1141). Nothing was pushed.

### Covered children and surface

Covered #128 and #440 children already on the remote parent: #1211
`e546bf23e` (constructed paired-cohort comparability), #1212 `ad1ee0264`
(qualified sensor documentation), #1213 `23cdae38b` (parent comparability
checkpoint, sixth) and #1221 `63dd5798e` (UI and cache checkpoint, seventh).
Their original NOT CLEAN reviews, failed receipts, first harness mistakes and
later qualified successes are unchanged.

Final fresh-main-relative scope (`git diff bb3a3b03 HEAD` before this
checkpoint): 39 files, 1710 additions, 2 deletions. Source and tests:
`src/core/src/zava_forward/core/paired_equity.py` (`5aedcd7b`),
`src/core/tests/test_paired_equity.py` (`f9b07cb6`) and `src/core/README.md`
(`bb709453`). Documentation: this pack, the KB index and the log. The remaining
33 files are dated `.copilot-tracking` RPI records. Main-only gate tooling
(`tools/rpi-checks.py`, `src/README.md`, API `style.css`) is identical to main
and not part of the diff. Tier: FOCUSED is recommended only while this stays
bounded metric tooling, tests and documentation; it is a recommendation for
coordinator admission, not an admission. Any mixed infrastructure, security,
SQL, finance, deployment or large-feature change needs reclassification to
FULL.

### Document identities and traceability

Identical on main and the parent. Statuses are not approvals by this record.

| Document | Status, version, date | Blob |
| --- | --- | --- |
| BRD-2026-AMA48-001 | draft, 0.21.0, 2026-10-24 | `34d88395` |
| PRD-2026-AMA48-001 | in-review, 0.21.0, 2026-10-25 | `c788b917` |
| ADR 0002 | Proposed | `cbe21530` |
| ADR 0003 | Accepted with amendment | `d6064539` |

Traceability stays document-qualified: PRD FR-054 and AC-073 (constructed
paired cohorts; status cell "Not run"), PRD OQ-018 (open), BRD NFR-008 and
NFR-009. `paired_equity.py` keeps `fairness_evidence=False` and
`activation_allowed=False`; its fixture contrasts are not a production mapping
or an approved threshold. Main still holds the unfixed blobs `d29768d5` and
`432aef3e` for the diagnostic and its tests; the parent holds the fix.

### Evidence classification

| Finding | Classification | Limit |
| --- | --- | --- |
| Six coupled core test modules pass on the integrated working tree | local observed (parent topic, integrated head `6703b0b1` content) | 74 tests; light only; not a gate, not a main observation |
| Ruff check and format check of the two changed Python files pass | local observed (parent topic) | Two files only; mypy not run |
| `git diff --check bb3a3b03 HEAD` clean | local observed (parent topic) | Whitespace only |
| Main observations of this surface | none | Main holds the unfixed diagnostic |
| Complete parent validation (relevant core tests as a gate, core Ruff and mypy including tests, offline requirement and design traces, link and anchor checks, final identity record) | pending coordinator admission | Not run here; historical child receipts and the earlier 74-test observation are context, not parent results |
| Independent exact-head review, hosted checks, guarded merge | deferred to coordinator | None exist for this head |
| Actual-model evaluation, thresholds, lawful fields, population fairness, human approval | blocked or unknown | Nothing inferred |

### Actual commands, exits and skips

Python 3.12.3 from the existing external `/tmp/ama-96-venv`, with
`PYTHONDONTWRITEBYTECODE=1`, external `XDG_CACHE_HOME`, `RUFF_CACHE_DIR` and
`MYPY_CACHE_DIR` under `/tmp`, and an explicit
`PYTHONPATH=<worktree>/src/core/src:<worktree>/src/core/tests`.

| Command | Exit | Result |
| --- | --- | --- |
| Import `paired_equity`, `journey_register`, `ranking`, `rai_release`; assert `__file__` under this worktree | 0 | Current-source paths confirmed |
| `python -m unittest` over `test_paired_equity`, `test_journey_register`, `test_rai_release`, `test_rai_release_invalidation`, `test_ranking_publication`, `test_cohort_eval` | 0 | 74 tests OK in 0.062 s |
| `ruff check --no-cache` and `ruff format --check --no-cache` on `paired_equity.py` and `test_paired_equity.py` | 0, 0 | Passed |
| `git diff --check bb3a3b03 HEAD` | 0 | Clean |
| Ignored-inclusive status | 0 | No ignored files |

Not run: `tools/rpi-checks.py` in any mode, mypy, browser, SQL, Docker,
scanners, cloud, provider or model calls, private datasets, broad suites and
offline traces. The heavy lock and the #144 runner were not touched.

### Findings, triage and recommendation

No new defect was confirmed and no correction beyond the merge was needed.
Earlier unreproduced observations stay observations. Recommendation: the
coordinator admits the selected-tier parent validation, independent exact-head
review and hosted checks; the recorded gaps remain open. No issue, board or
criterion was changed and no closing keyword is used. Nothing was deleted,
moved, archived, reset or cleaned.

<a id="eighth-stabilization-checkpoint-finance-parent-held-export-manifest-contract-2026-11-05-refs-440-96"></a>

## Ninth stabilization checkpoint: finance parent held-export manifest contract (2026-11-05, Refs #440 #96)

Refs #440 and #96. This is the ninth checkpoint. The previous record of the
same name that labelled it eighth is superseded by this label; the baseline
eighth checkpoint is the integrated parent topic preparation. Local DRAFT,
not consumed by the coordinator and not approved for publication.

Process qualification: the original local commit `d26791065f21f45ab42cae34e4efbcfddc8f419f`
created its Research, Plan, details and Review files after the pack, index and
log edits, so its phase artifacts were post-implementation and its process is
not claimed compliant or repaired. The coordinator held publication and
consumption. A separate corrective loop (r2) started prospectively from that
commit; its research, plan, details and critique were written before any
corrective edit, and the original records are preserved unchanged.

Refs #440 and #96. Bounded, documentation-only, local-only record of the
finance parent integration and of one proposed material contract change: adding
required per-field review history to the Held draft export integrity manifest.
It is separate from main and from the governance parent, adds no source, test,
tool, workflow, coordinator, ADR, requirement or policy change, and approves
nothing. It does not complete whole #440 (criteria 7 and 8), HVE behaviour
testing, parent #123 acceptance, #96 schemas, reviewed packs or dependency
graph, Finance or Legal approval, or any main, Azure or human acceptance.
Original RPI evidence is under
`.copilot-tracking/*/2026-11-05-finance-export-checkpoint-440-*` (original,
post-implementation phase files) and the prospective correction under
`.copilot-tracking/*/2026-11-05-finance-export-checkpoint-440-r2-*`.

### Identities and exclusions

| Item | Value |
| --- | --- |
| Documentation child | Branch `docs/finance-export-checkpoint-440`, started clean at the governance-parent head `dec700c7af46778140bf5c46d4df932832a31f11` (declared target `feat/discovery-assurance-integration-123`); parent not moved |
| Finance parent (source observed) | `feat/finance-integration-93` at `0472fd5d5625bb610b5ac65ad177026953802830`, tree `268ead3a098f2320c0fba1a16aed14dd68a7fbe2`; it is main plus exactly one commit |
| Main (re-fetched 2026-11-05) | `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`, tree `5c2988b71aec609b007b41f408685d54e2c28e0d`; fetched commit and tree identity only. Hosted run status, scorer completion and acceptance were not verified by this record |
| Covered PR | #1223 (`c738fde9b27b5c88af6453c0ababfd84eeca5850` squash-merged into the finance parent only, 2026-11-05T21:53:46Z, merge commit `0472fd5d`); main does not contain it. #96 is open |
| Excluded | Governance-parent runtime and its differently scoped inherited implementation; unmerged siblings; the paused #96 successor with only prospective research, plan and details; any code not on `0472fd5d` |

| Document | Status, version | Blob (equal at main and finance parent) |
| --- | --- | --- |
| BRD-2026-AMA48-001 | draft, 0.21.0 | `34d88395de861e9799eb9e24121a21c92c7a5adc` |
| PRD-2026-AMA48-001 | in-review, 0.21.0 | `c788b917bafaede215f326f0efc71e071a687f1c` |
| ADR 0003 | Accepted with owner amendment | `d60645397b20fb70ac3d1dc47c7a6c8671201306` |
| ADR 0006 | Accepted | `956da1a3b804c803041fe2e8a312bd9f400273ae` |

Draft and in-review documents are not approvals. Actual AI registry
prerequisite #105 is closed and in main; it supplies no personal, Legal or
Finance authority.

### Traceability (document-qualified)

BRD FR-038 to FR-041 (regulatory source register, monitoring, decision
traceability, role-appropriate evidence views) are different requirements from
PRD FR-038 to FR-043 (assisted forms). This record concerns the PRD forms
group, with BRD FR-040 and FR-041 as related context only.

| Requirement | Finance-parent source and tests (`0472fd5d`) | Limit |
| --- | --- | --- |
| PRD FR-040, AC-048 (accept, correct, reject; prior value, reviewer, evidence or reason, state) | `form_review._review` appends a history event with `field_id`, `input_version`, `prior`, `new`, `decision`, `reviewer` (actor email), `reason` (at most 500 characters) and `at`; authority-bearing categories are refused (`forms.HUMAN_ONLY`) | Working draft only; no source record changes |
| PRD FR-042 (reviewable pack with template and input versions and Finance review history), AC-050, AC-054 | `form_export.draft_export` is read-only, status `Held`, `reviewed` false, `Not submitted`, eligibility `Not assessed`; it hashes `BODY_KEYS` (11 keys, no history) with SHA-256 over canonical JSON. `form_review._report` already returns `history` | Review history is not in the export body today. A reviewed pack, AC-050 and AC-054 stay "Not run" in the PRD |
| PRD FR-043, AC-051 (exact dependent stale sets) | `form_export.export_freshness` and `test_form_dependencies.py` | Constructed fixtures; reviewed re-export blocking is not implemented |
| Access, persistence, manual and AI-unavailable paths | `forms._actor` requires a verified or registered Finance-view actor with reason visibility; `form_review._visible` already checks that cited evidence in history is readable and unreadable evidence returns `Unavailable`; the working review is the manual path; no AI dispatch; JSON and SQLite stores hold the working review, and the export persists nothing | Callers hold saved copies; the store stores none |
| PRD FR-038, FR-039, FR-041 | Schema binding, staged candidates and diagnostics in `form_review` and `forms` | #96 C1, C5 and C6 stay unchecked; approved schema, rule and authority are not supplied |

### Compatibility disposition of the proposed required history key

Source-visible fact: `export_freshness` rebuilds `body` from `BODY_KEYS` and
treats a missing key as `Invalid` with the action "Create a new held export from
the working review." Adding `history` to `BODY_KEYS` therefore makes every
existing history-less saved copy `Invalid`, with no backfill or rewrite and the
established regenerate-Held recovery. A git search of the finance parent found
no consumer of `form_export` outside its own tests and `src/core/README.md`
(no API, web or store caller), so no in-repository consumer is broken. Actual
saved copies held by users were not read and are unknown.

Disposition, as a scoped engineering recommendation and not an approval:

* Compatible with PRD FR-042 intent, which names review history in the pack, and it keeps the integrity manifest covering provenance. An optional history key is rejected because incomplete manifests would read as `Current`.
* Material contract change: the meaning of "valid saved export" changes. The README must state that copies without history are `Invalid` and must be regenerated.
* Privacy: history carries reviewer email and free-text reason, and superseded prior values. Access stays limited by the existing Finance-view actor gate and visibility check. Reviewer identity and reason in a held copy that callers store is a data-protection point for the named DPO or data owner, not decided here.
* Integrity is a SHA-256 over content, not a signature or delegation, and proves neither author nor approval.
* No expansion into reviewed-pack, eligibility, submission, award or payment authority; the export stays `Held`, unreviewed and `Not submitted`.

### Evidence classification

| Finding | Classification | Source and limit |
| --- | --- | --- |
| Identities, blobs, covered PR state | local observed (git and `gh`) | 2026-11-05 |
| Source and consumer inspection above | local observed (source read at `0472fd5d`) | Static reading, not execution |
| 40 form tests pass on the pinned finance source | local observed (light, finance parent); historical to the r2 correction, not rerun | Below; log `/tmp/f440fin/run.log` dated 22:05:10Z |
| #1223 hosted checks, published functional approval, default-FULL receipt `07ae` | coordinator-supplied, unverified by this child | Supplied at `c738`; not re-checked here. A receipt is not a test at `0472fd5d` or main; tree equality is an identity fact, not a new run |
| Behaviour at `0472fd5d` beyond the 40 tests | implemented-unverified | No full gate was run |
| Required-history export | proposed, not implemented | Waits for this record's consumption |
| SQL Server, browser, Docker, Azure, actual AI, user research | none or blocked | Not run; heavy resources were not admitted |
| Finance, Legal, DPO and human acceptance; whole #96 | blocked or deferred | Named humans; nothing approved |

### Actual commands and limits

| Command | Exit | Result |
| --- | --- | --- |
| `git archive origin/feat/finance-integration-93 src/core src/agents` into the new external path `/tmp/f440fin/src` | 0 | Pinned source extracted, not a checkout |
| `python -m unittest tests.test_form_export tests.test_form_review tests.test_form_dependencies` from `/tmp/f440fin/src/src/core` with the #440-owned venv `/tmp/ama-main-440-ui-cache-wave3-venv`, scrubbed environment, `PYTHONDONTWRITEBYTECODE=1`, external `TMPDIR`, explicit `PYTHONPATH` to the pinned export | 0 | `Ran 40 tests`, OK in 21.4 s; `form_export.__file__` resolved to `/tmp/f440fin/src/src/core/src/...`; no `__pycache__`; JSON and SQLite fixtures only, no SQL Server |

The c738 checkout `/tmp/g96-r14-review1-1105/checkout` no longer exists, so it
was not used. The first attempt failed on the shell `cd` into
`/tmp/f440fin/src/core` (the pinned source is nested at
`/tmp/f440fin/src/src/...`) with exit 1, before any Python import or test
command, so no test ran in that attempt. No dedicated per-test output file was
created for it, but its wrapper error (`cd: /tmp/f440fin/src/core: No such file
or directory`) and exit 1 are preserved in the native session log
`/tmp/rpi-440-finance-export-checkpoint-20261105.log`. The repaired run's exit 0
and 40 tests OK remain historical, not rerun or upgraded. No heavy lock was taken, and no gate runner, SQL Server, browser,
Docker, cloud or private data was used. Nothing was installed.

### Findings, triage and recommendation

No defect was confirmed and no new issue or refactor is proposed. Engineering
recommendation (not an approval, and not yet consumed by the coordinator):
**continue**. If the coordinator accepts a valid checkpoint, this record
supports resuming the paused #96 export-history slice under its own FULL tier,
with these conditions. #96 stays PAUSED and is not released by this draft. Conditions: the manifest change and the legacy `Invalid` and regenerate
behaviour are documented, a regression test covers a history-less copy being
`Invalid` and a tampered history failing the hash, and the slice adds no
authority, endpoint or reviewed-pack state. **Fix**: none. **Pivot**: none.
The required-history compatibility decision is proposed, not approved by a named human.
Requirement relaxation, deliberate deferral, the reviewer-history privacy
position and any Finance or Legal approval need named human owners.

| Gate | Effect |
| --- | --- |
| #96 resume | Coordinator consumes this record, then runs the retained slice through its own FULL tier, independent review and hosted checks |
| #96 closure | C1, C5 and C6 stay unchecked; approved schemas, reviewed packs, dependency graph and human acceptance remain |
| Parent #123 and whole #440 | Unchanged; criteria 7 and 8 untouched |
| Publication of this child | Coordinator independent exact-head assessment, hosted checks and human approval |

Process disclosure: nothing was deleted, moved or cleaned; `/tmp/f440fin`
is retained.

<a id="tenth-stabilization-checkpoint-lifecycle-parent-quality-evidence-gate-2026-11-05-refs-440-82-81"></a>

## Tenth stabilization checkpoint: lifecycle parent quality evidence gate (2026-11-05, Refs #440 #82 #81)

Refs #440, #82 and #81. This is the tenth checkpoint: the baseline eighth is
the integrated parent topic preparation and the ninth is the finance parent
record. It is a new bounded lifecycle integration checkpoint, not a correction
of either. Local DRAFT, not consumed by the coordinator and not approved for
publication. It assesses one merged increment, PR 1226, and accepts nothing.

Process: Research, Plan, details and one critique were written before any pack,
index or log edit (verified with `git status`). A read-only light observation
on an immutable export was made during research, before the plan, and is
recorded as research-phase evidence.

### Three separate pins

| Pin | Identity | Role |
| --- | --- | --- |
| Governance documentation target | `feat/discovery-assurance-integration-123` `1faadaa3e75d3b4003319fde0491473fa1a87dee`, tree `678085a22e982a438fd275701f1e686bb212f258` | Base of this docs child; contains the reviewed finance record, unchanged |
| Lifecycle implementation SOURCE | `feat/controlled-lifecycle-integration-81` `cd271cfa54216fbc2ae7d59a63ac8068f372d697`, tree `6bc669420643d524402b3b26ef325aae3a65b53a` | Contains PR 1226 merged 2026-11-05T23:01:10Z; tree equals reviewed child `10161ecbcf879e44f64d6e3ad97e481ae8e2d81d` |
| Main | `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` | Unchanged at the last fetch; hosted status of main is not asserted |

Identities were fetched on 2026-11-05. Source is one commit over main (28
files, +682/-10): `gates.py`, `quality.py`, `store.py`, three test files and
issue 82 tracking. Governance runtime and the unmerged #144, #79, #80, #96,
#185, #188 and #1204 work are excluded from lifecycle and main acceptance.
Fetched identity is not hosted completion, approval or runtime acceptance.

### Document identities (verified at the lifecycle parent, equal to main)

| Document | Version and status | Blob |
| --- | --- | --- |
| BRD `agentic-retrofit-programme-brd.md` | 0.21.0 draft | `34d88395de861e9799eb9e24121a21c92c7a5adc` |
| PRD `zava-forward-retrofit-programme-demonstrator.md` | 0.21.0 in-review | `c788b917bafaede215f326f0efc71e071a687f1c` |
| ADR 0003 | accepted with owner amendment | `d60645397b20fb70ac3d1dc47c7a6c8671201306` |
| ADR 0006 | accepted | `956da1a3b804c803041fe2e8a312bd9f400273ae` |

Draft and in-review documents are not approval, and the quality rule below has
no named professional reviewer.

### Traceability of the quality transition

* PRD FR-008 requires deterministic evidence, eligibility, authority, safety,
  resident, funding, capacity, quality and finance gates before a controlled
  state transition (mapped criteria AC-010, AC-011, AC-067 and AC-144). BRD
  FR-008 is a different requirement (a material change invalidates downstream
  approvals) and is not the governing source of the gate; `QUALITY_RULE`
  nevertheless cites BRD FR-008 in its source field (see Findings). PRD FR-007 forbids bulk quality
  acceptance. The acceptance rows are not run; passing light tests do not
  tick them.
* `gates.quality_gate` passes only with no gaps, returns Unknown for an
  unreadable record and Fails with the reason "Checks without evidence".
  `quality.evidence_gaps` returns `None` for malformed stored items, checklist
  name or measure, so malformed labels, checklist or measure inference return
  Unknown and never pass. `store.require_quality_evidence` refuses accept and
  handover with the reason, owner and next action.
* Corrupted in-progress evidence: a replacement is the owner's approved narrow
  recovery (decision of 2026-11-05) and is limited to a quality role
  (Quality Inspector or a manager); originals are kept. It does not reassign
  identity and does not accept anything.
* Independence: `_independent` still bars anyone who submitted, recorded or
  fixed the work from accepting it; an unresolved contributor identity blocks
  acceptance. Resident clear and safety clear are retained. Bulk acceptance
  stays forbidden.
* Store boundary: the JSON store and the SQLite-backed `SqlStore` path share the
  gate; SQL Server is a different boundary and was not run at the parent.
* Evidence visibility: a refusal surfaces the gate reason, owner and next
  action to the user rather than a silent pass; manual paths are unchanged.
* Rule provenance: `QUALITY_RULE` cites BRD FR-008 and the quality checklist as
  an exercise fixture (effective 2026-11-05, version 1) with the reviewer set
  to the unreviewed marker. This is unreviewed exercise-rule provenance, not
  named professional approval.

### Evidence classification

| Finding | Classification | Source and limit |
| --- | --- | --- |
| Pins, blobs, PR 1226 merge, issue states (82, 81, 440, 144, 80 open) | local observed (git and `gh`) | 2026-11-05 |
| Source read of the gate, quality and store changes | local observed | Static reading at `cd271cfa` |
| 183 core tests pass on the export of `cd271cfa` | local observed (light, lifecycle parent) | Below; includes SQLite-backed `SqlStore` variants, not SQL Server |
| Child `10161` full receipt (17 groups, 205 commands, 192 exit 0, 13 probe exit 1 individually inspected) | coordinator-supplied, historical for source `10161` | Receipt sha256 `ba37e035fe06e0dddb63d2ed5971fe0989387a917c10ed850e2b049bca987f57` matched the file at `/tmp/g82-measure1-1105/receipt.json`; contents not re-adjudicated |
| SQL Server log (291 total, 290 executed, 1 JSON-only ordering skip; three new measure fallback and three earlier metadata cases ok) | coordinator-supplied, historical for source `10161` | `/tmp/g82-measure1-1105/0176-mssql.log`; not read or rerun here |
| Root default-FULL before merge, local and published functional approval (0 findings, 28 sections), 10 hosted checks success | coordinator-supplied | Not re-checked here; published diff sha256 `408ce2bf...`, local raw diff differs, no byte identity claim |
| Behaviour at `cd271cfa` under SQL Server, browser, full or partial gate | implemented-unverified | Tree equality with `10161` is an identity fact, never a new run at the parent or main |
| Other capacity, authority, finance and eligibility gate families | deferred | #82 owns them |
| Named review of `QUALITY_RULE` and the other exercise rules | unknown | No named reviewer recorded |
| Heavy gate, SQL Server, browser, Docker, scanner, Azure, AI | blocked (not admitted) | #144 owns exclusive heavy resources; nothing was queued |

### Actual commands and limits

* Export: `git archive` of `origin/feat/controlled-lifecycle-integration-81`
  (`cd271cfa`) paths `src/core` and `src/agents` into the new external path
  `/tmp/l440cd271/src` (refused an existing path; nothing was overwritten).
* Environment: the existing 440-owned venv
  `/tmp/ama-main-440-ui-cache-wave3-venv`, `env -i`, bytecode off, external
  `TMPDIR`. No installation. Import proof: `store`, `quality` and `gates`
  resolve under `/tmp/l440cd271/src/src/core/src/zava_forward/core/` and
  `evidence_gaps` exists.
* Command: `python -m unittest tests.test_gates tests.test_quality_procurement
  tests.test_hazard_referral` from `/tmp/l440cd271/src/src/core`. Exit 0
  captured directly from the subprocess; Ran 183 tests in 80.2 s, OK with 1
  skip. The skip is attributed by source reading, not by the non-verbose log,
  to the single `skipTest` ("JSON-only separate-file audit ordering") in
  `test_hazard_referral.py`. The logged traceback is an injected-fault test's
  expected error output. No `__pycache__` was created. Output
  `/tmp/l440cd271/out/run.log`, sha256
  `3b43f8b16bb79baf1e4298ee649e666a67ba8c2587bb69c13f8c1706342b88e0`
  (identified by hash only; `/tmp` is outside the repository).
* No failed attempt occurred. No lock, service, SQL Server, browser, Docker,
  scanner or cloud use. This is a focused light run, not a full or partial
  gate and not a receipt.

### Findings, triage and recommendation

* No confirmed runtime defect, so no issue is proposed and no refactoring is
  suggested. One provenance ambiguity is recorded for #82 ownership (not fixed
  here): `QUALITY_RULE.source` at `cd271cfa` cites BRD FR-008, while the
  governing requirement for controlled-transition gates is PRD FR-008. Whether
  the citation is corrected is for #82's owner under its rule source
  criterion. The open owners were compared: #82 (gates and named rule review),
  #81 (epic), #80 (unmerged Excel work), #144 (heavy owner) and #440 (this
  series).
* #82 stays OPEN with three criteria incomplete (each gate with a pass, fail
  or unknown result and reason; unknown never passes across all families; each
  controlled rule with source, effective date, version and reviewer). The
  quality gate is one family with an unreviewed rule; no tick is made.
* Recommendation: continue. No fix or pivot is indicated by this evidence.
  Pivots, requirement relaxation, deferral and named approvals belong to the
  owner and named humans, not to this record.

| Gate | Effect |
| --- | --- |
| This record | Draft until coordinator independent assessment, publication, published-head and hosted gates, and explicit consumption |
| Remaining #82 family implementation and affected expansion | Wait for this checkpoint's consumption; independent lanes may continue; a heavy or SQL gate waits for coordinator admission after #144 releases heavy resources |
| #81, #82 and whole #440 | Unchanged; no closure or criterion tick; #440 criteria 7 and 8 untouched |
| #80 | Unmerged Excel work is excluded and unaffected |

Process disclosure: nothing was deleted, moved or cleaned; `/tmp/l440cd271`
is retained as read-only test setup and is not authority to delete it.

<a id="eleventh-stabilization-checkpoint-lifecycle-parent-capacity-booking-gate-2026-11-06-refs-440-82-81"></a>

## Eleventh stabilization checkpoint: lifecycle parent capacity booking gate (2026-11-06, Refs #440 #82 #81)

Refs #440, #82 and #81. This is the eleventh checkpoint (baseline eighth,
finance ninth and lifecycle quality tenth are distinct and unchanged). It is a
new bounded checkpoint, not a rewrite or correction of any of them. Local
candidate, not consumed by the coordinator and not approved for publication.
Trigger: PR 1229, a completed capacity booking increment under #82 that
changes controlled transition outcomes, merged 2026-11-06T03:10:17Z.

Process: Research, then Plan, details and one critique, were each committed
before any pack, index or log edit. A read-only light observation on an
immutable export was made during research and is recorded as such.

### Three separate pins

| Pin | Identity | Role |
| --- | --- | --- |
| Governance documentation target | `feat/discovery-assurance-integration-123` `a97bea15318307aacf60ed1690d054d32417c23e`, tree `7995337ffe41a01d250c2c4856e48b5f08d45b82` | Base of this docs child; contains the tenth record unchanged |
| Lifecycle implementation SOURCE | `feat/controlled-lifecycle-integration-81` `af891a5cccf730ccf61e670f312b7674218dbe4b`, tree `cb8a3d463b0f1d31d1a5de0d1e1a2e68de7ebc8e` | Holds #1226, #1228 and #1229; its tree equals reviewed child `272146f4eb5e810b03290004942d37b22edda968` |
| Main | `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` | Unchanged at the fetch of 2026-11-06; hosted status of main is not asserted |

All three equal the supplied pins; nothing changed. The parent is 3 commits
over main (48 files, +1200/-25); #1228 and #1229 together are 23 files,
+519/-16 over `cd271cfa5` (5 source files, +152/-16). Governance runtime and
the unmerged #144, #79, #80, #96, #188 and #1204 work are excluded from
lifecycle and main acceptance. Fetched identity is not hosted completion,
approval or runtime acceptance.

### Document identities (verified; equal to main)

| Document and path | Version and status | Blob |
| --- | --- | --- |
| BRD `docs/brds/agentic-retrofit-programme-brd.md` | 0.21.0 draft | `34d88395de861e9799eb9e24121a21c92c7a5adc` |
| PRD `docs/prds/zava-forward-retrofit-programme-demonstrator.md` | 0.21.0 in-review | `c788b917bafaede215f326f0efc71e071a687f1c` |
| ADR 0003 `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md` | accepted with owner amendment | `d60645397b20fb70ac3d1dc47c7a6c8671201306` |
| ADR 0006 `docs/adrs/0006-src-layout-and-cutover.md` | accepted | `956da1a3b804c803041fe2e8a312bd9f400273ae` |

Draft, in-review and exercise-fixture rules are not approved professional
rules.

### Traceability of the capacity booking transition

* Requirements: PRD FR-008 governs gates (mapped AC-010, AC-011, AC-067 and
  AC-144; acceptance not run). PRD FR-016 is the provider-package and
  committed-capacity record. PRD FR-017 is the quality disposition record.
  BRD FR-008 is a different requirement (material change invalidates
  downstream approvals). `CAPACITY_RULE` cites PRD FR-008 and FR-016 and
  `QUALITY_RULE` cites PRD FR-008 and FR-017 (#1228), which resolves the
  citation ambiguity disclosed in the tenth checkpoint.
* `gates.capacity_gate`: True is Pass, a known violation is Fail, missing or
  unreadable evidence is Unknown. `CapacityGateError` subclasses `ValueError`,
  so the existing API 400 text contract is kept, and carries the state and
  result internally.
* Procurement mapping: a known deficit or a work date outside the evidenced
  period is Fail. An absent single appointed order, absent, legacy or
  unverified capacity, changed source, scope or contract, a lost authorised
  acceptor and a changed authority are Unknown. Fail and Unknown refuse before
  a successful mutation. Pass is returned only after the resident clear, is
  server-internal and is not newly persisted or API-exposed.
* `appointments._appointment_assessment`: only a sole capacity failure rethrows
  structurally; mixed failures stay a plain `ValueError`. Capacity remains the
  last check. The inherited Low RV-C1 future-ordering caveat is not a current
  defect.
* Quality interaction: quality still needs explicit Pass evidence (unknown
  never passes), independent human acceptance by someone who did not submit,
  record or fix the work, and the resident and safety clears; capacity does not
  bypass them and does not accept quality.
* Boundaries: the JSON store and the SQLite-backed store were exercised;
  SQL Server was not. Actor and authority are checked against the named
  manager and contract authority; no identity is reassigned. Manual paths
  (contract manager records current evidence, then re-books) are unchanged.
  Unavailable evidence stops the transition with owner and next action.

### Evidence classification

| Finding | Classification | Source and limit |
| --- | --- | --- |
| Pins, blobs, PR 1229 merge, issues 82, 81, 440, 144, 80 and 79 open | local observed (git and `gh`) | 2026-11-06 |
| Source read of the gate, procurement and appointment changes | local observed | Static reading at `af891a5cc` |
| 193 core tests total, 192 executed, 1 declared JSON-only skip; suite exit 0 (PASS), on the export of `af891a5cc` | local observed (light, lifecycle parent) | Below; JSON and SQLite paths, not SQL Server |
| Candidate `272146f4e` FULL receipt: 17 groups, 205 commands, no group skip | coordinator-supplied, historical for the candidate | Receipt sha256 `eb1cd5ed8546bd5f128324d4c1799fc3248fcb481cdc471b3138d2d0e765a0bc` matched `/tmp/g82-cap-r3-1106/receipt.json`; contents not re-adjudicated |
| Thirteen nonzero probe commands | coordinator-supplied, attributed to the #82 comment | Expected pre-installation, import or SQL-startup probes individually read by others, not here; the earlier zero-nonzero assertion was false and is not relied on |
| Candidate SQL Server log: 296 total, 295 executed, 1 declared JSON-only audit-ordering skip, 5 new capacity cases passed | coordinator-supplied, historical for the candidate | Log sha256 `51953f94e8674ec36038098421b2064e6c919a47fa251212da3fbc1b8edec5e1` matched; log not read or rerun here |
| Root default-FULL before merge, 10 hosted checks success, local and published functional code-review result with 0 findings, human boxes unchecked | coordinator-supplied | Not re-checked here; a code-review result is not an approval |
| Behaviour at `af891a5cc` under SQL Server, browser or a full or partial gate | implemented-unverified | Tree equality with `272146f4e` is an identity fact, never a new run at the parent or main |
| Other gate families, named rule review, integrated parent FULL, live acceptance | deferred or unknown | #82 and the coordinator own them; no named reviewer is recorded for either exercise rule |
| Heavy gate, SQL Server, browser, image, scanner, Azure, AI | blocked (not admitted) | Heavy holder is original 79 r9 (PID 2560481, `/tmp/g79-pub-r9-1106`); nothing queued |

### Actual commands and limits

* Export: `git archive` of `origin/feat/controlled-lifecycle-integration-81`
  (`af891a5cc`) paths `src/core` and `src/agents` into the new external path
  `/tmp/l440af891/src`; the path was refused if it existed.
* Environment: the existing 440-owned venv
  `/tmp/ama-main-440-ui-cache-wave3-venv` (the #82 venv was not used or
  changed), `env -i`, bytecode off, external `TMPDIR`, no installation, no
  network use. Import proof: `gates`, `procurement`, `appointments`, `quality`
  and the fixture module `test_gates` resolve under
  `/tmp/l440af891/src/src/core/`, and `CapacityGateError` exists.
* Command: `python -m unittest tests.test_gates tests.test_quality_procurement
  tests.test_hazard_referral` from `/tmp/l440af891/src/src/core`. Exit 0
  captured directly from the subprocess; 193 tests in 65.9 s, OK, 1 skip. The
  skip is attributed by source reading, not by the non-verbose log, to the
  single `skipTest` ("JSON-only separate-file audit ordering"). The logged
  traceback is an injected-fault test's expected output. No `__pycache__` was
  created. Log sha256
  `3fd61476e1c5ceb642590380499abe252872fe825855adce3734bb568edab9e6`.
  `/tmp` evidence is session-only; the hash is the durable pointer.
* No failed attempt occurred. This is a focused light run, not a full or
  partial gate and not a receipt.

### Findings, triage and recommendation

* No new defect and no necessary behaviour-preserving refactor was confirmed,
  so no issue is proposed. Owners compared: #82 (remaining families and rule
  review), #81, #80, #144, #79 and #440.
* #82 stays OPEN with three criteria unchecked. Capacity and quality are two
  gate families with unreviewed exercise rules; the other families and named
  rule review remain unproven.
* Recommendation: continue; no fix or pivot. Pivots, requirement relaxation,
  deferral and named approvals belong to the owner and named humans.

| Gate | Effect |
| --- | --- |
| This record | Candidate until coordinator independent assessment, publication, published-head and hosted gates, and explicit consumption |
| #81 and #82 closure | Unchanged; no tick; remaining gate families, named rule review and integrated parent FULL must be proven first |
| #80 dependent expansion | Waits for coordinator consumption and its own admission; independent lanes (79, 80, 96, 144, 188, 1204) may continue; a heavy or SQL gate resumes only on coordinator admission after the holder releases |
| Whole #440 | Unchanged; criteria 7 and 8 untouched; native HVE Deferred or not available is not a Pass |

Process disclosure: nothing was deleted, moved or cleaned; `/tmp/l440af891`
is retained as read-only test setup and is not authority to delete it.

<a id="twelfth-stabilization-checkpoint-archive-helper-filesystem-contract-2026-11-06-refs-440-79-1231"></a>

## Twelfth stabilization checkpoint: archive helper filesystem contract (2026-11-06, Refs #440 #79 #1231)

Refs #440, #79 and #1231. This is the twelfth checkpoint (baseline eighth,
finance ninth, lifecycle quality tenth and capacity eleventh are distinct and
unchanged). It is a new bounded checkpoint, not a rewrite or regrade of any of
them. Local candidate, not consumed by the coordinator and not approved for
publication. Trigger: bug #1231 changes the ranking archive helper inherited by
#79 so that it requires a filesystem with hard links and removes its own
staging file. That is a contract change for any deployment archive mount.

Process: Research, then Plan and details, were committed before any pack,
index or log edit. No test, SQL, browser, install or cleanup was run here; the
child's retained logs were read, not rerun. Disk was 98% used and nothing was
deleted.

### Pins

| Pin | Identity | Role |
| --- | --- | --- |
| Governance documentation target | `feat/discovery-assurance-integration-123` `dce6498cf850de9bdc79ecb1706f8491d75b2ea8`, tree `c7440e42226178d6967966b8003794c795a2c314` | Base of this docs child; eventual target |
| Main | `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` | Unchanged at the fetch of 2026-11-06 |
| #79 candidate (local, unpublished) | `feat/ranking-publication-runner-79` `397419724e68b24bce879512a24c7df430177f87`, tree `c728049e33a3a0e20d9a7bf16b3738fabfbc14d7` | Not an ancestor of the governance parent; not main acceptance |
| Child #1231 (local, unpublished) | `fix/ranking-archive-concurrent-writer-metadata` `57b3b6a09f6ac5b77b37881e21447751a56be5ff`, tree `fea8273a05c2a42da3e127d77a2c4ad9377f365b` | Based on the #79 candidate; eventual target #79, which targets #73 |

These are separate pins. Nothing from the #79 candidate or #1231 is on the
governance parent or main, and tree identity is not a test execution.

### Document identities

| Document | Version and status | Blob |
| --- | --- | --- |
| BRD `docs/brds/agentic-retrofit-programme-brd.md` | 0.21.0 draft | `34d88395de861e9799eb9e24121a21c92c7a5adc` |
| PRD `docs/prds/zava-forward-retrofit-programme-demonstrator.md` | 0.21.0 in-review | `c788b917bafaede215f326f0efc71e071a687f1c` |
| ADR 0003 `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md` | accepted with owner amendment | `d60645397b20fb70ac3d1dc47c7a6c8671201306` |
| ADR 0006 `docs/adrs/0006-src-layout-and-cutover.md` | accepted | `956da1a3b804c803041fe2e8a312bd9f400273ae` |

Blobs are equal on the governance parent and main. Draft and in-review
documents are not approval.

### What changed in the candidate

Read from the child diff (`748526484~1` to `24cab4b60`: 8 files, +412/-15,
including the helper, `src/core/README.md`, two test files and the child's
own research, plan, details and issue note). In `publish`, the existing
pre-check and canonical text remain. A unique same-directory staging file is
created exclusively, written, then linked to the final name with
`os.link`, which cannot overwrite. On `FileExistsError` the existing record is
read back and returned with `written` false. A `finally` then unlinks the
caller-owned staging file only. Any other `OSError`, including no hard-link
support, propagates and the runner reports `publish_failed`. There is no
fallback and no overwrite. The old shared `.tmp` and `os.replace` are gone.

Original diagnosis (issue #1231, from the #79 R11 session): one deterministic
two-thread, one-process, local-filesystem interleaving gave `published` for
2026-11-05 while the retained bytes said 2026-11-06, and the other caller got a
structured `publish_failed` from a shared-temporary `FileNotFoundError`;
verification still passed. No lost publication, overwrite of a finished
record or production incident was demonstrated. #1231 is open, linked to #79
and is the only owner; no new issue is proposed.

### Traceability

* PRD PR-006 (deterministic published policy version) is the demonstrator
  behaviour the archive records; PRD DH-002, DH-003 and PR-003 keep retention
  periods as defaults pending DPO and Legal approval. The helper sets neither
  the legal period nor the schedule.
* ADR 0006 mounts runtime data at `/data` and state at `/state` but defines no
  hard-link or archive mount contract. A deployment filesystem is therefore an
  unowned and unknown decision.
* Authentication, identity, resident, AI and manual boundaries are unchanged
  and out of this bounded contract: dates are inputs, no clock is read and no
  ranking changes. No new journey was run.

Document-qualified joins (correction 1, read 2026-11-06). The same identifier
AC-015 means different things in the two documents: BRD AC-015 belongs to BRD
FR-011 (consent is not inferred), while PRD AC-015 belongs to PRD FR-012
(prioritisation inputs missing or conflicting). Paths are in the unmerged #1231
child (`57b3b6a09`); no join is an owner-confirmed trace.

| Requirement (document-qualified) | Contract or decision | Code and tests | Observation versus unverified | Owner and resume |
| --- | --- | --- | --- | --- |
| BRD NFR-006, AC-060 (exportable versioned evidence, Must) | Partial, indirect fit only; no export test, approval history or exit contract was observed for the archive | `src/core/src/zava_forward/core/ranking_publication.py` (`publish`, `verify`) | unknown; nothing observed exercises export or exit | Digital and data owners; no resume point set here |
| BRD NFR-002, AC-049 (immutable versions, supersede not overwrite, Must) | A finished record is kept unchanged | `src/core/tests/test_ranking_publication.py` `ConcurrentWriterTests`: `test_delayed_contender_leaves_a_finished_record_unchanged`, `test_sequential_bytes_and_name_are_unchanged` | local observed in the child (read, not rerun); FULL and independent assessment unverified | #1231 owner; isolated validation and independent assessment |
| PRD PR-006, PRD AC-015 (deterministic published policy version; AC-015 status Not run) | One truthful record per snapshot and retained date | `ConcurrentWriterTests.test_same_snapshot_different_dates_keep_one_truthful_record`, `test_separate_processes_publish_one_truthful_record`; `src/core/tests/test_ranking_publication_runner.py` `test_same_snapshot_on_two_dates_publishes_once_and_reports_the_retained_date` | local observed in the child; PRD journey not run; the spawned-process case also passed the old helper | #79 archive delivery; #1231 resume |
| PRD DH-002, DH-003, PR-003 (retention pending DPO and Legal) | The helper sets no retention period or schedule | Not applicable | unknown; legal period unowned | DPO and Legal; not decided here |
| ADR 0006 (accepted source layout) | No hard-link or archive mount contract | Hard link in `publish`; refusal path only tested by an injected `PermissionError` | implemented-unverified; no real unsupported mount tested | Deployment owner; hard-link disposition blocked, owner unavailable on 2026-11-06 |

Gate effect is unchanged: HOLD #79 archive delivery and #73 dependent expansion.
Independent #96, #188 and #80 lanes may continue and are not necessarily
publication-ready.

### Classification

| Finding | Classification | Source and limit |
| --- | --- | --- |
| Pins, blobs, candidate and child heads, #1231 open and linked | local observed (git and `gh`) | 2026-11-06 |
| Source and README change read in the child diff | local observed | Static reading; child is unpublished |
| Child RED: 48 tests, 4 failures and 2 errors, exit 1 | local observed (child retained log, read not rerun) | `/tmp/1231-ranking-archive-r1-1106/red1.log`; retained as the adverse first result |
| Child GREEN: 48 tests, 0 skips, OK in 0.628s, exit 0; API wiring 12 tests OK in 12.635s, exit 0 | local observed (child retained logs, read not rerun) | Deliberate child source and test imports with a parent read-only environment; not an isolated installed-package or FULL run |
| Ruff check, Ruff format and mypy three-file checks passed | local observed (child, read) | Used Ruff 0.17.3 and mypy 2.4.1, newer than the maintained 0.17.1 and 2.4.0 |
| Spawned-process smoke | local observed (child, read) | Also passed the old helper, so not independent RED proof |
| Unsupported-filesystem refusal | implemented-unverified | Only an injected `PermissionError` was tested, not a real unsupported mount |
| Fix of the concurrent-writer divergence | implemented-unverified | Child local; no FULL, no independent publication Pass |
| Hard-link compatibility disposition | blocked | Needs the #79 or deployment owner; not decided here |
| Windows, SMB, network or production mount support | unknown | Linux development evidence only; no approved deployment mount |
| Coordinator consumption of the 702-line native log and 11-file diff | unknown (not independently re-executed by this author) | Attribution: coordinator-supplied. Not an independent publication Pass and not re-adjudicated here |

### Limits and qualifications

* The child's original details forecast a completed-record overwrite and a
  tolerated missing stage at cleanup. Later actual results demonstrate neither;
  the final code unlinks unconditionally. The originals stay unchanged.
* `import-proof-final.txt` was overwritten during successive green runs. The
  final proof matches the candidate (helper sha256
  `4d222878a5031fbe04b69f7d2c063d2486daac6505483167eeefa94160544c2b`); earlier
  printed metadata is kept only in the native event output and the original raw
  proof files are not restored. First RED and static failures remain retained.
* Native child session `b353a2c9-455a-4ca9-8ab2-8ee2ca09d516`, exit 0; its
  research, plan and details were committed before the first test edit and its
  author Review followed its checks. Read-only evidence: the native log
  `/tmp/rpi-1231-ranking-archive-r1-1106.log` and
  `/tmp/1231-ranking-archive-r1-1106/`. These `/tmp` paths are session-only,
  so the hashes and numbers above are the durable pointers.

### Finding owners and recommendation

* Owner of the divergence fix and its validation: #1231, then #79.
* Owner of any deployment mount, hard-link compatibility disposition and legal
  retention period: owner, deployment and Legal decisions not made here.
* Recommendation: HOLD #79 archive delivery and #73 dependent expansion until
  the hard-link compatibility disposition, relevant final validation and an
  independent assessment hold. Continue the #1231 fix lane under its own RPI.
  This checkpoint does not release the archive lane or approve a deployment
  filesystem. No new defect is raised beyond #1231.

### Gate effects

| Gate | Effect |
| --- | --- |
| #79 archive delivery | Held until compatibility disposition, final validation and independent assessment |
| #73 dependent expansion | Held on the same conditions |
| #96, #188 and #80 lanes | Independent; may continue |
| #1231 closure | Unchanged; no tick |
| Whole #440 | Unchanged; criteria 7 and 8 untouched; native HVE Deferred or not available is not a Pass |

Resume conditions: a named disposition on hard-link support for the intended
mount (supported, refused or replaced), the child's relevant validation in an
isolated installed-package run, an independent assessment, and coordinator
consumption of this record.

Process disclosure: nothing was deleted, moved or cleaned; the child worktree
and `/tmp` evidence were read only.

### Correction 1 qualifications (2026-11-06)

* The classification of the coordinator consumption row was corrected from an
  attribution label to an allowed class, and a small document-qualified
  traceability table was added. The earlier text is otherwise unchanged.
* The original Research file says "Written before any plan". Per the
  coordinator's reading of native events, the research, plan and details create
  calls were dispatched together at 05:03:07.973 to .974Z, completed at
  05:03:08.006, .017 and .028Z, and were committed at 05:03:14Z before any
  target edit. The Research observations preceded that batch. The original
  files are preserved; the before-implementation chronology stands.
* The coordinator asked the owner once whether the archive may require atomic
  hard links and refuse unsupported filesystems; the result was owner
  unavailable. No selection, default or approval is inferred, and the
  compatibility disposition stays blocked. The earlier #144 financial choice
  is separate and out of scope.

## Thirteenth stabilization checkpoint: finance parent history export (2026-11-06, Refs #440 #96 #93)

Refs #440, #96 and #93. This is the thirteenth checkpoint, a new bounded
post-integration checkpoint. The ninth (finance) and the earlier #1225 scoped
checkpoint are historical, unchanged and do not prove this one. Local
candidate, not consumed by the coordinator and not approved for publication.
Trigger: PR #1233 was squash-merged on 2026-11-06 at 06:32:47 UTC into the
finance source parent and adds the recorded working-review history to the Held
export (routed in the #440 comment 6678812333).

### Pins (two topic heads and main)

| Pin | Identity |
| --- | --- |
| Governance documentation target `feat/discovery-assurance-integration-123` | `7ed4a33f543bf7e1eed4aa351712734c743867b7`, tree `04d2e99a85ce26a59395d1ccfa60cae5a842308c`; does not contain #1233 |
| Finance source parent `feat/finance-integration-93` | `4642b55fdbafec564b67803420439b91d7ea8ce1`, tree `e2628422d13ae87df3a6b7ecfdd12f24a4fc1052`, direct parent `0472fd5d5625bb610b5ac65ad177026953802830`; not an ancestor of governance |
| Main | `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`; has no #1233 |

The source tree equals the reviewed child `abeb022ba26fce149664f62d674c47dc6c0ef4e2`
per the coordinator; that is an equality observation, not a fresh receipt for
the squash head. Documents (blobs equal on governance and main, read
2026-11-06): BRD 0.21.0 draft `34d88395de861e9799eb9e24121a21c92c7a5adc`; PRD
0.21.0 in-review `c788b917bafaede215f326f0efc71e071a687f1c`; ADR 0003 accepted
with owner amendment `d60645397b20fb70ac3d1dc47c7a6c8671201306`; ADR 0006
accepted `956da1a3b804c803041fe2e8a312bd9f400273ae`. Draft and in-review are
not approval.

### What changed in #1233 (static reading of git objects)

The merge diff is 10 files, +280/-1: seven original RPI artifacts,
`src/core/README.md`, `form_export.py` (two lines) and `test_form_export.py`.

* `BODY_KEYS` gains `history` and `draft_export` copies
  `report["history"]`, so the ordered, detached per-field history (reviewer
  email, prior and new value and evidence, decision, reason, time, input
  version) is inside the content hash.
* `export_freshness` rebuilds the body from `BODY_KEYS`. A saved copy without
  `history`, with reordered or truncated history, is `Invalid` with the action
  to create a new Held export. Nothing is backfilled and a saved copy is never
  edited. The owner chose, for synthetic data only, full history and
  regeneration of old copies; that authority is not broadened.
* Preflight visibility (actor, case, current and historical evidence) is
  `form_review._visible`, already present in parent `0472fd5d5` and not changed
  by #1233; it checks prior and new evidence of every history event and the
  attachments, and unreadable evidence is `Unavailable`. Parent #1223 changes
  are not attributed to #1233.
* Unchanged boundaries: status `Held`, `reviewed` false, `Not submitted`,
  eligibility `Not assessed`, manual path is the working review itself. The
  hash is not a signature and history is field review, not Finance pack
  approval.

### Traceability (document-qualified)

| Requirement | Source and tests (finance parent `4642b55fd`) | Limit |
| --- | --- | --- |
| PRD FR-040, AC-048 (accept, correct, reject; prior value, reviewer, evidence or reason) | `form_export.draft_export` history; `test_export_carries_ordered_detached_review_history` (empty, accept, correct, reject, accept; stored equality; detached; deterministic digest) on JSON and SQLite stores | Constructed synthetic fixtures; read, not run here |
| PRD FR-042, AC-050, AC-054 (reviewable pack, no submission or eligibility) | Status `Held`, `reviewed` false; `test_history_is_integrity_covered_and_legacy_copy_is_invalid` | A reviewed export is not implemented; PRD AC-050 and AC-054 not satisfied here |
| PRD FR-043, AC-051 (only dependent fields stale) | `export_freshness` with history key | History change makes a copy Stale; exact dependent sets stay in earlier tests |
| BRD NFR-002, AC-049 (retained prior versions; context only) | Saved copy is never edited; regeneration creates a new Held export | Interpretive join, not owner-confirmed |
| ADR 0006 (accepted source layout) | `src/core` module and tests | No history or export contract; no approval implied |

Remaining criteria: #96 still has unchecked the approved versioned schema, the
reviewed export that never submits or implies eligibility, and dependent-only
stale marking; #93 still has the stabilization checkpoint, child closure or
deferral, and the no automated submission or approval criteria. Checked boxes
are the owner's records and are not re-adjudicated.

### Classification

| Finding | Classification | Source and limit |
| --- | --- | --- |
| Pins, blobs, issue states (#440, #96, #93 open) | local observed | `git` and `gh`, 2026-11-06 |
| Source and test reading of #1233 | local observed | Static; no test was run in this checkpoint |
| History in Held export, Invalid legacy copy, regeneration | implemented-unverified | Child FULL is source-qualified to `abeb022ba`; no exact-head receipt for `4642b55fd` or governance |
| Child FULL, 205-row ledger, SQL 285 tests with one JSON-only skip, hosted checks, independent and published functional and readiness approvals | unknown | Attribution: coordinator and PR #1233 comment 6678688323; not inspected by this author in the original cycle. In correction 1 only the identity block of `/mnt/ama-gates/g96-r18-1106/receipt.json` was read (head `abeb022ba`, tree `e2628422`, 205 commands, no failure); the ledger `96-r18-execution-consumption-r44.json` was not read. Child-source evidence, not a receipt for `4642b55fd`, governance or main |
| History tests on SQL Server | unknown | SQL covers 285 tests per the coordinator; the new history tests exercised JSON and SQLite only |
| Local constructed browser observations | unknown | Attribution: coordinator; not re-executed by this author. Not Azure, AT or WCAG acceptance |
| Vulnerability gates (four fixable-vulnerability gates found zero; 39 unfixed per image, 37 High and 2 Critical) | unknown | Attribution: coordinator; not re-executed by this author. No security-clean or risk-acceptance claim |
| Real or private data, named schema, DPO, Legal, resident, professional, Azure, assistive technology | blocked | Not supplied; synthetic data only |
| Disk space at intake | local observed | `df` on 2026-11-06: 99% used, 3.8G free; nothing deleted |
| Heavy-resource release and #188 handoff admission | unknown | Attribution: coordinator-supplied; not verified by this author. No heavy work was run |

### Findings, recommendation and gates

No new defect and no necessary refactor was confirmed by static reading. A
search of open issues for form export history found only the existing owners
#96 and #80. Recommendation: CONTINUE the independent #188, #80 and #1204
lanes under their own prerequisites; HOLD #93 and #96 closure and dependent
expansion until this record passes current independent and published
assessment and explicit coordinator consumption, and an exact-head FULL for
the integrated source is supplied if it is relied on. No pivot or deferral is
proposed or approved.

| Gate | Effect |
| --- | --- |
| #96 closure and #93 closure | Held; no tick |
| Dependent expansion on the finance parent | Held on the same conditions |
| #188, #80, #1204 | Independent |
| Whole #440 | Unchanged; criteria 7 and 8 and native HVE Deferred or not available are not a Pass |

Resume conditions: independent assessment of this record, publication gates,
coordinator consumption, and a named exact-head receipt where relied on.

Process disclosure: research, plan and details were committed as `5764cb570`
before this edit. No test, SQL, browser, install, lock, cleanup, push or PR.

### Correction 1 qualifications (2026-11-06)

The original records above and in the first cycle's artifacts are preserved.
Actual chronology: Research, Details and Plan were created in that order
(not Research, Plan, Details as the original Changes says) before the planning
commit `5764cb570` and any canonical edit. The first README edit failed on a
mistyped path and was redone. Changes and state were created before the final
checks, not after as planned, and the Review followed in a later call. The
final check read cached refs; only the intake step fetched, so the Review's
"re-fetched" overstates it. The commits used the privacy-safe address without
a shown `gh api user` resolution. Correction 1 corrects the disk and admission
classification, replaces "paths not accessible" with "not inspected by this
author", and fixes the pins heading. It re-fetched all three pins and found
them unchanged. No defect, requirement or approval changed.

## Fourteenth stabilization checkpoint: queue dispatch permit protocol (2026-11-06, Refs #440 #144 #107 #118 #122)

Refs #440 (open), #144 (open), #107, #118 and #122. This is the fourteenth
checkpoint, a new bounded documentation-only preimplementation checkpoint for
the proposed #144 background-dispatch safeguards. It is not a runtime change,
not a feature or acceptance claim and not a live enablement. Earlier
checkpoints are historical and unchanged. Local candidate, not consumed by the
coordinator and not approved for publication. The #144 code PR would belong
under `feat/infra-hosting-integration-136`; this documentation child is based
on the governance parent `feat/discovery-assurance-integration-123`.

### Pins

| Pin | Identity |
| --- | --- |
| Governance documentation target `feat/discovery-assurance-integration-123` | `119828353ccc1d678c1a4e9c1c67b621b0d263a0` (fetched 2026-11-06) |
| Main | `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` |
| Code parent `feat/infra-hosting-integration-136` | Not observed: `git ls-remote` and `gh api` returned no branch (HTTP 404) on 2026-11-06. The brief says it points to main; that is supplied, not observed |
| Candidate (read-only) `issue-144-queue-recovery` | HEAD `4c878d664853074e9dec49e57d5c89c4cc9bf3a2`, tree `978986c9374f6b1019136d121a4ee1f21be7941c`; merge base with main is main |

Documents read at governance `119828353` (draft and in-review status is not
approval): BRD 0.21.0 draft `34d88395de861e9799eb9e24121a21c92c7a5adc`;
PRD 0.21.0 in-review `c788b917bafaede215f326f0efc71e071a687f1c`; ADR 0001
Proposed `d42fa5c4615f4107cee83e07555dba6985c1f53e`; ADR 0002 Proposed
`cbe21530043ff15432cc6dce1086d080f5eb15b4`; ADR 0003 accepted with owner
amendment `d60645397b20fb70ac3d1dc47c7a6c8671201306`; ADR 0006 accepted
`956da1a3b804c803041fe2e8a312bd9f400273ae`.

### Main versus candidate

A static `git grep` for symbols under `src` on each commit shows that the
queue slice is candidate-only. The candidate differs from main by 12 `src`
files, +1241/-18.

| Symbol | Main `bb3a3b03` | Candidate `4c878d664` |
| --- | --- | --- |
| `WORKER_ROLE`, `_worker_complete`, `build_serve`, `publish_pending`, `ZF_ASSIST_QUEUE` | absent | present |
| Ledger `Consumption.reserve`, `dispatch_check`, `complete`, `liability-unknown` | present | present |
| `financial-meter-unavailable` hold in `Ai._request` | present | present |

So the worker, its role and its single completion route are unmerged candidate
code, not main behavior. Candidate-policy evidence is not merged-main
acceptance, operational acceptance or approved requirements.

### Trigger and owner decisions (supplied by the coordinator)

The owner retained duplicate-dispatch and revocation safeguards for the demo
and chose "include background processing and recovery; design and implement its
safeguards first". This is code and design authority only. It is not a live
grant, deployment, provider call, financial-policy waiver, price approval,
production budget, operational enablement or final ADR acceptance, and the
end state is not replaced by in-process only.

The candidate's r8 record proposes an API-owned per-attempt dispatch permit,
authoritative financial reservation and settlement, durable unknown-outcome
reconciliation and no automatic re-inference of possibly dispatched work, with a
second exact route for the Application-only AgentsWorker role. It is a draft,
not an approved interface or implemented behavior. Existing High findings 1
(composed worker reaches `financial-meter-unavailable`) and 2 (redelivery
re-infers) stay open. No live unsafe call or new production bug is claimed.
Coordinator-supplied r8 qualifications kept: its skill body was not loaded,
its creation order was Research, Details, Plan, state, log, commit, three
originals have no frontmatter, and "no network" is not literal because issue
metadata was retrieved. The r8 raw log was not inspected by this author.

### Traceability (document-qualified)

| Requirement or decision | Source (candidate unless noted) | Status and limit |
| --- | --- | --- |
| PRD FR-061 (AI consumption economics; joins BRD FR-052, AC-102, AC-103, OD-51), verified by PRD AC-107, AC-108 | `ai_consumption.Consumption` ledger (main and candidate) | Draft documents; economics reporting not delivered here |
| PRD NFR-017 (finite limits, hard termination, unknown liability degrades to workflow-only, human approval of live budgets; joins BRD NFR-012, AC-100, AC-101, OD-51), verified by PRD AC-109, AC-110 | `Consumption.reserve`, `dispatch_check`, `complete`; 40 s stale-liability window; `Ai._request` hold | AC-109 is the closest criterion and is "Not run" in the PRD; the permit protocol is a proposal that would serve it, not evidence of it |
| BRD OD-51 and PRD OQ-027 (budgets, owners, price source) | None | Open; no budget, price or owner is invented; production budget deferred |
| ADR 0001 (Proposed): `agents` app on the `agent-tasks` queue, agents identity without database | Candidate queue slice | Only Proposed support for a queue estate; no approval implied |
| ADR 0002 (Proposed) Five-Assistant section: queue/agent estate "remains proposed" | In-process `Assistants.execute` | The candidate's cited "ADR 0002 decision 6" is the Dockerfile and CI item, not a dispatch decision, and is not repeated here |
| ADR 0003 (accepted with amendment) decision 1: "No new service, queue, store or network path is added" for the journey capabilities | None | Tension with a background queue, recorded and not resolved; the owner decision above is not an ADR acceptance |
| ADR 0006 (accepted) source layout | `src/core`, `src/api`, `src/agents` | Package boundary only; no dispatch contract |

### Safeguard trace

| Safeguard | Where | Status |
| --- | --- | --- |
| Service identity and role | `auth.service_caller` (Application-only, proxy flag, exact tenant, audience, oid, appid), one completion route `_worker_complete` | Candidate-only, implemented-unverified; the permit route is a draft |
| Authoritative ledger and persistence | `Consumption` over the `Assistants` port (shared database and clock); `assistant_attempts` row `{task}:{fence}` | Ledger on main; queue attempts candidate |
| Lease, fence, epoch, release, source checks | `claim` and `complete` re-validate; `execute` re-checks suspension, admission, epoch and release just before the provider thread | Present for in-process; the queue path has no equivalent pre-dispatch check (High finding 2) |
| Unknown outcomes | `complete` returns timeout or provider-unavailable tasks to `pending`; `claim` re-claims an expired lease with a new fence | Current behavior can repeat a possibly dispatched call on the queue path; the draft reconciliation is not implemented |
| Duplicate handling | `reserve` holds `duplicate-attempt`; draft compare-and-set `reserved -> permitted` | Ledger present; permit draft only |
| Approval and manual paths | Manual and in-process execution unchanged; background work is proposal generation only | Preserved; no funding, consent, works or release authority |
| Default-off activation | `ZF_ASSIST_QUEUE` unset means off (candidate, server lines 79-88) | Candidate-only; the worker stays held by `financial-meter-unavailable` |

### Revocation windows (draft protocol)

| Window | Physical call | Handling and limit |
| --- | --- | --- |
| Before a permit is issued | None | The same checks as in-process can deny with no spend |
| Between permit and provider dispatch | Possible | Only a worker-side deadline can stop a late start; an issued permit cannot be recalled |
| After dispatch | In flight | A late result can be rejected and settled; the call is not undone |
| Lost permit response, lost ack, visibility expiry, restart | Unknown | Must be surfaced as unknown and not re-inferred; no exactly-once or perfect-revocation claim |

### Design gaps (not code defects; no test exists)

1. Transaction composition: `Assistants.transaction()` opens a new connection
   with `BEGIN IMMEDIATE` per call, and `Consumption.reserve` and `complete`
   each open their own. The draft names an optional `db` for `reserve` only;
   `complete` needs the same, and atomic issue and settlement are unproven on
   SQLite and SQL Server. The fallback order leaves an orphan-reservation
   window that the 40 s stale-liability rule would turn into a budget-wide stop.
2. Clocks: lease (default 60 s, range 10 to 120), provider timeout (default 20
   s, range 1 to 40), the ledger's 40 s window and the permit deadline are not
   bound to values. A 40 s timeout equals the window, so a legitimate late
   settlement could be held as `liability-unknown`.
3. Attempt state: the attempt `outcome` column is overwritten with the
   envelope outcome at completion, and the line-1025 pending-retry for timeout
   and provider-unavailable is not reconciled with the draft `permitted`,
   `dispatching` and `unknown` states.
4. Lost permit response: classed unknown although no call occurred, which
   holds the budget with no clearing authority.
5. Late or wrong-fence result: the draft settles by the stored meter id and
   rejects the result; its interaction with the 40 s hold and with a settlement
   of a real earlier call is not specified.
6. Unknown liability: `complete` with no usage always records
   `liability-unknown`, and `src/core` has no ledger clearing route (a `git
   grep` for clear, reconcile and resolve functions found only unrelated
   modules).
7. Authority price and expiry: the draft reserves at permit time; treatment of
   authority or price expiry between permit and call relies on `dispatch_check`
   inside the worker path, which the draft meter makes local.

### Open decisions (not approved here)

* Role-code authority for a second exact AgentsWorker permit route; no live
  grant is implied. The coordinator asks the owner separately.
* The operator path that clears a budget-wide `liability-unknown` stop. No
  Finance approver is named, no liability is forgiven, no usage is invented,
  no budget is reset and no retry is silently enabled.
* Alternative B (API-proxied inference) remains the smallest safer option if
  the strictest revocation bound is needed; it changes hosting and identity
  (#118).

### Classification

| Finding | Classification | Source and limit |
| --- | --- | --- |
| Pins, blobs, issue states (#440 and #144 open) | local observed | `git` and `gh`, 2026-11-06 |
| Main lacks the queue slice; candidate has it | local observed | Static `git grep` on both commits; no code was run |
| Static reading of ledger, `claim`, `complete`, server and auth anchors | local observed | Read-only; design gaps above are readings, not reproductions |
| Parent 136 branch | unknown | 404 on the remote; brief statement supplied |
| Queue slice behavior, worker route, default-off flag | implemented-unverified | Candidate only; no exact-head receipt for it in this checkpoint |
| Permit, settlement, reconciliation protocol | deferred | Draft only; not implemented |
| Candidate gate, tests and r8 raw log | unknown | Attribution: coordinator; the log was not inspected by this author |
| Second route authority, operator clearing authority | blocked | Unassigned decisions; nothing approved |
| Live, Azure, provider, SQL race, price and budget | blocked | Not run or supplied; synthetic and design only |

### Findings, recommendation and gates

No new defect is confirmed and none is reproduced. The seven design gaps and
two open decisions are preimplementation items for #144, not duplicate issues.

Recommendation: FIX, with #144 implementation held for the unresolved
contract decisions. This is not an unconditional continue, not a feature or
operational acceptance and not a pivot; the owner-approved background goal
stays in force. Code readiness is separate from demo and operational
acceptance. Bounded implementation could proceed independently of a later
operational clearing workflow only under this invariant: no worker path calls
the provider without an API-issued permit, no unknown outcome is
automatically retried, and the ledger stays fail-closed on
`liability-unknown`. That is a condition for the coordinator and owner, not an
approval of a new authority.

Resume conditions:

* A corrected implementation-ready prospective #144 design that resolves the
  gaps above.
* A role-code authority decision on the second exact route.
* A safe unknown-liability and operator disposition.
* Coordinator consumption of this checkpoint after independent exact-head
  assessment.
* Original #144 tests-first implementation, then a new FULL gate and current
  independent review before any publication or enablement.

| Gate | Effect |
| --- | --- |
| #144 implementation and worker enablement | Held (FIX) |
| #118 hosting and #122 continuity dependents | Dependent on the #144 contract; no change here |
| #188, #79 and #1231, #80, #1204 | Independent; continue on their own prerequisites |
| Whole #440 | Unchanged; criteria 7 and 8 and native HVE are not a Pass; no tick or closure |

Process disclosure: research, plan and details were committed as `5233db299`
before this edit. No test, SQL, browser, install, lock, cleanup, push or PR.

### Correction 1 qualifications (2026-11-06)

The original text above, including the sentence that the r8 creation order was
"Research, Details, Plan, state, log, commit" and the parent 136 row, is
preserved. This subsection supersedes them for two points only. The
coordinator supplied the r8 order from the outer CLI log display and has since
corrected that inference; the original text repeated it.

* r8 Plan and Details were parallel, not serial. Native event metadata (only
  call IDs, event types, timestamps and success flags) shows: first Research
  create started 08:17:18.098Z and failed (retained; the coordinator attributes
  it to a missing directory); successful Research create 08:17:36.958Z to
  08:17:36.985Z; Plan create and Details create both started at exactly
  08:18:22.940Z, with Details completing at .970Z and Plan at .981Z. Neither the
  log display order nor the shared start time shows a serial chain, and
  completion order is not creation order. No serial r8 phase chain is claimed.
  The state, log and commit order is as supplied and was not re-derived. The
  other r8 qualifications stand: unread research skill body, no source edit,
  three original Markdown files without frontmatter, issue metadata retrieved
  (so "no network" is not literal), and no Azure, Graph, provider, SQL or
  browser run.
* Parent 136: on 2026-11-06 a local `git rev-parse
  refs/heads/feat/infra-hosting-integration-136` returned
  `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` (equal to main), and
  `git ls-remote origin 'refs/heads/feat/infra*'` returned nothing. So the ref
  is a local, unpublished integration branch: local observed `bb3a3b03`,
  remote absent as observed, intended code target. The earlier remote 404
  stays true and historical. No remote branch is created and no owner
  branch-choice question is raised by this.

Unchanged: the second AgentsWorker route authority is unresolved (the owner's
reply was a question about URL versus container, not an approval, and
clarification or the general background scope is not role-code approval); the
liability-unknown operator disposition and all seven design gaps stay open; the
recommendation stays FIX with #144 implementation held. Correction research,
plan and details were committed as `6d9a8818d` before this edit; no test, SQL,
browser, lock, push or PR.

### Correction 2 qualifications (2026-11-06)

Correction 1 above and its records are preserved. This subsection qualifies
them for three points, after an independent readiness report on head
`f7d6057d9` (verdict approve_with_comments, one Medium and one Low, no tests or
gates run) and a later owner decision.

* Correction 1 order. The correction 1 details record says its Details was
  created after its Plan. Native event metadata (call IDs, types, timestamps
  and success flags only) shows the Research create started 08:55:04.608Z, and
  the Plan and Details creates both started at exactly 08:55:24.371Z, with
  Details completing at .416Z and Plan at .432Z. They overlapped; no serial
  Plan-then-Details chain is shown, and completion order is not creation
  order. The supported fact is unchanged: Research, Plan and Details were
  committed together as `6d9a8818d` before any canonical edit. The correction 1
  Changes and Review describe separate calls, which is true, but do not
  disclose the overlap, so their chronology and conformance accounts are
  qualified by this paragraph. The correction 2 records were created in
  individual tool turns and were committed as `737a16abc` before this edit.
* Correction 1 heading check. Its Changes record reports the heading count as
  a uniqueness pass. The exact heading `### Correction 1 qualifications
  (2026-11-06)` occurs three times in this pack (earlier checkpoints'
  correction subsections and the fourteenth's); within the fourteenth
  checkpoint it occurs once. The fourteenth checkpoint's own top-level anchor
  is a distinct heading, was not shown broken, and appears once in the README
  and twice in the log at that check. Only the scoped count supports
  uniqueness, not a pack-wide one.
* Second-route role-code decision. After the clarification that the second
  endpoint is another HTTP route on the proposed API integration, not another
  ACA environment or worker container, the owner approved it (issue 144
  comment `6681120797`, 2026-11-06T08:57:53Z, later than the correction 1
  launch; the saved text and readback are supplied coordinator session files).
  The demo code may extend the Application-only `ZavaForward.AgentsWorker`
  allowance to request an API-authorized, metered dispatch permit in addition
  to submitting results. This resolves the role-code decision only. It is not a
  second environment or container, live grant, infrastructure, deployment,
  provider call or spend, approval of the whole protocol or ADR, waiver of
  financial or revocation controls, or appointment of a financial
  reconciliation operator. The earlier statements above that the route
  authority was unresolved were true when dated and remain as history.

Unchanged: the liability-unknown operator and safe-resume authority and all
seven design gaps stay open; the recommendation stays FIX with #144
implementation held; no runtime defect is confirmed; original 144 tests-first
RPI, checkpoint consumption, full validation and exact-head independent review
remain required. Local 136 is `bb3a3b03` (equal to main) and remote absence is
unchanged. No test, SQL, browser, lock, push or PR.

### Current status qualifications (2026-11-06, post-correction 2)

Additive status record at 13:50Z against governance `119828353`, main
`bb3a3b03`. Nothing above is rewritten. The correction 2 Research cited the
Correction 1 heading interval as 4285 to 4526; the Fourteenth checkpoint begins
at line 4300, so the interval is 4300 to 4526. The count of three matching
Correction 1 headings pack-wide stands (one inside this checkpoint before
correction 2). The independent readiness report (approve_with_comments, one Low)
found both original defects resolved.

| Item | Class | Status at 2026-11-06 |
| --- | --- | --- |
| Second exact permit route for the Application-only `ZavaForward.AgentsWorker` (issue 144 comment `6681120797`, 08:57:53Z) | Approved demo code authority | Resolved, unchanged |
| Demo Finance-role audited reconciliation of unknown AI usage from provider evidence (issue 144 comment `6685915140`, 13:26:36Z, read-only confirmed by `gh api`) | Approved demo code authority | Resolved by this status |
| R9 dispatch permit, settlement and reconciliation design (144 candidate commit `323abba2e6f392e54c4ac27b427e00d05a3e6782`, tree `13c61bfe37b20eb42d75fc604b3c1d7fcd7f779d`, read from pinned objects) | Proposed, DRAFT | Not approved, not consumed here, no code |
| Root assessment of R9 | Observed (coordinator, supplied) | Revise, design only |
| Original two High runtime findings | Observed, open | Open |
| Implementation of 144 | Held | FIX, tests first, full validation and independent exact-head review required |

* Finance-role decision. The existing Finance role may handle audited
  reconciliation of unknown AI charges using provider evidence. Unknown amounts
  stay reserved. Resumption needs the existing budget, consent and revocation
  checks. No invented usage, budget reset, safeguard bypass or automatic
  repeat dispatch is authorized, and manual non-AI work stays available. It is
  not a live grant, deployment, provider spend, real financial waiver,
  production approval, or acceptance of the whole protocol or ADR. The earlier
  09:40-era statements that an operator decision was pending were true when
  dated and remain history. No further owner question on these two code
  choices.
* R9 items the root assessment leaves open: pre-dispatch binding of the final
  serialized request, model and token bounds inside the worker adapter; a strict
  reconciliation event schema; a durable no-repeat representation including
  in-process compatibility; code-discoverable role and transaction facts (the
  Finance role names are discoverable in code, not an owner question); and
  numeric timing margins, backoff and poison handling. A bounded R10 design
  correction is independent work and is not approved by this snapshot.
* R9 process qualifications from native events (not CLI display order): the r9
  Markdown files carry no frontmatter; Changes, Review and state creates start
  in parallel at 13:37:53.482 to .483 and Review precedes its light checks;
  Research 13:33:20, Plan 13:34:50, Details 13:35:14 and the planning commit
  13:36:49 precede the design create at 13:37:35.
* Unchanged: unknown-liability operator and safe-resume authority beyond the
  code role, the seven design gaps and FIX recommendation remain open; no
  runtime defect is confirmed; local 136 `bb3a3b03` is unpublished (remote
  absent). No test, SQL, browser, lock, push or PR.

## Fifteenth stabilization checkpoint: finance parent integration (2026-11-06, Refs #440 #96 #93)

Focused, documentation-only status. It builds on the
[thirteenth checkpoint](#thirteenth-stabilization-checkpoint-finance-parent-history-export-2026-11-06-refs-440-96-93) and does not repeat its static reading.

### Source and document identities

| Item | Value |
| --- | --- |
| Parent `origin/feat/finance-integration-93` (fetched 13:45Z) | `4642b55fdbafec564b67803420439b91d7ea8ce1`, tree `e2628422d13ae87df3a6b7ecfdd12f24a4fc1052`; 2 ahead and 0 behind main; not in governance |
| Child #1233 head | `abeb022ba26fce149664f62d674c47dc6c0ef4e2`, same tree; merged 2026-11-06T06:32:47Z |
| Prior parent | `0472fd5d5` (#1223 dependency, covered) |
| Governance and main | `119828353ccc1d678c1a4e9c1c67b621b0d263a0` and `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` |
| Stale local ref (not used) | local `feat/finance-integration-93` is `0472fd5d5`; the remote tracking ref is the pin |
| BRD 0.21.0 draft | `34d88395de861e9799eb9e24121a21c92c7a5adc` |
| PRD 0.21.0 in-review | `c788b917bafaede215f326f0efc71e071a687f1c` |
| ADR 0003 accepted with owner amendment | `d60645397b20fb70ac3d1dc47c7a6c8671201306` |
| ADR 0006 accepted | `956da1a3b804c803041fe2e8a312bd9f400273ae` |

Blobs are identical at main, governance and the parent. Draft and in-review are not approval.

### Evidence and classification

| Observation | Class |
| --- | --- |
| Receipt `/mnt/ama-gates/g96-r18-1106/receipt.json` read by this author: 297806 bytes, SHA-256 `070403bd4f64bf12d46e369b1bf84e051fa4ace1d592099c126fe7bdd897dfd1`, top-level `failure` null, `image_cache` fresh; matches the supplied value | Local observed (file identity only) |
| Supplied child FULL for source `abeb022ba` and main `bb3a3b03`: 205 commands, 17 groups; dedicated SQL 285 tests with one JSON-only skip; four images with zero fixable findings and 39 unfixed per image (37 High, 2 Critical); independent bounded functional pass | Supplied, historical child observation, not re-executed |
| New history tests used synthetic JSON and SQLite; the MSSQL run did not specifically exercise them | Implemented-unverified on SQL Server |
| Static: `form_export.py` lists `history` among body keys (line 30) and passes `history=report["history"]` (line 87) | Local observed (source reading) |
| Receipt for the squashed parent `4642b55f`, main acceptance, live Azure SQL | Unknown or not performed |

The child receipt is not a receipt for the squashed parent, governance or main.

### Trace

* PRD FR-040 with AC-048, PRD FR-042 with AC-050 and AC-054 (not met), PRD FR-043 with AC-051; BRD NFR-002 with AC-049 as an interpretive join; ADR 0006 layout. Backlog: #96 (open C1, C5, C6 and the named schemas) and #93.
* Authority: the full-history contract and regeneration of old Invalid copies are owner-approved for synthetic data only. Originals are not rewritten or backfilled. No actual or private data authority. Real Finance, DPO, Legal, Reviewed, submission and eligibility approvals are unproven.

### Gaps, owners, recommendation

* Exact gaps: #96 C1, C5, C6; named schemas; per-approver evidence; MSSQL exercise of the history tests; a receipt and independent review at the parent head; main integration.
* No new defect is established; every finding maps to an existing owner. No speculative issue or refactor. Financial policy is not activated.
* Recommendation: CONTINUE the independent #96 lanes. HOLD closure of #96 and any dependent expansion. Resume when the owners supply the missing approvals and a gate is run at the intended head.
* Publication and closure gates: coordinator reassessment, hosted CI on the parent, human approvals; no tick.

## Sixteenth stabilization checkpoint: sensor parent integration (2026-11-06, Refs #440 #184 #185 #188 #110)

Focused, documentation-only status. It builds on the fifth checkpoint, whose main-source reading and requirement IDs are reused.

### Source and document identities

| Item | Value |
| --- | --- |
| Parent `origin/feat/live-simulator-integration-184` (fetched 13:45Z) | `9476dc9610368a9a1bd46c88314586885638580d`, tree `30167885b00d308d7b29e9a78a064f4af834ce98`; 2 ahead and 0 behind main; not in governance |
| Child #1205 (merged 02:13:34Z) | head `a7d4e956db3b2c194c7601b888be5a558869a6de`, merge `2dc125f9` |
| Child #1203 (merged 09:37:52Z) | head `6887377845648502f2a5509801ee5d9807869703`, same tree as the parent |
| Durable trigger | #440 comment `6681870292`, 2026-11-06T09:40:32Z |
| Stale local ref (not used) | local `feat/live-simulator-integration-184` is `ead177ef9` |
| Documents | BRD, PRD, ADR 0003, ADR 0006 identical to the finance table above |

### Evidence and classification

| Observation | Class |
| --- | --- |
| Receipt `/mnt/ama-gates/g188-r20-1106/receipt.json` read by this author: 297806 bytes, SHA-256 `e575146936c97ffb4e397dd78a75951a079000c18c979d3374f863e6c1c95014`, `failure` null; matches the supplied value | Local observed (file identity only) |
| Supplied child #188 FULL for `6887377`: 205 commands, 17 groups; dedicated SQL 285 with one JSON-only skip; a separate sensor SQL supplement of 68 tests with zero skips; four images with 42 unfixed (40 High, 2 Critical), fixable 0; older figure 39 is history and the cause of the increase is unverified; two independent assessments approved with zero findings | Supplied, historical child observation |
| Parent static diff against main: 19 files, +1169 and -81 (live envelope admission with retained envelopes at `sensor_consumer.py` lines 430 and 749, versioned synthetic weather reference `synthetic-weather-continuity-v1` in `sensor_consistency.py` line 36, dry-run device provisioning reporting "none created or stored" in `device_provision.py` line 23) | Local observed (source reading) |
| #1205 apply path needs injected Registry and CredentialStore adapters that the CLI does not supply; its criteria 1, 3 and 4 are unmet | Implemented-unverified, deferred |
| Receipt at the squashed parent `9476dc96`, main integration, real credential issuance, secure storage and teardown, resident consent, indoor calibration, statistical validity, live authenticated Azure SQL, activation | Unknown, not performed or blocked |

The #188 receipt belongs to `6887377`, not to `9476dc96`. Weather reference data is not indoor measurement.

### Trace

* BRD FR-048, AC-090, RULE-014, OD-43 (real inventory; blocks operational use with real data); PRD FR-050, AC-066, AC-067, AC-068; ADR 0003 decision 6 (no public endpoint). BRD FR-050 and PRD FR-048 are different subjects and are not sensor work. Backlog: #184, #185, #188 (three criteria unchecked), #110, #186.

### Gaps, owners, recommendation

* Exact gaps: named credential owner and secure store, teardown evidence, resident consent, calibration and validity, authenticated Azure SQL, receipt at the squashed parent, main integration.
* No new defect is established; no speculative issue or refactor. Independent lanes can continue (#110 and #186 analysis, #185 adapter design) without activating sensors.
* Recommendation: CONTINUE independent lanes; HOLD closure of #184, #185 and #188 and dependent expansion. Resume when the credential owner, consent and a gate at the intended head exist.
* Publication and closure gates: coordinator reassessment, hosted CI on the parent, human approvals; no tick.

### Provenance qualifications (2026-11-06, post-integration correction 1)

Additive qualification of the Fourteenth checkpoint current-status subsection
and of the batch that added the Fifteenth and Sixteenth sections. It is
appended here because the pack is append-only; it is not part of the Sixteenth
checkpoint. Nothing above is rewritten and no new checkpoint number is used.
The times below are tool call boundaries read from the uncommitted native
session event log (tool start and completion, UTC); this qualification makes
no time claim of its own beyond those boundaries.

* Time labels. The status subsection says "status record at 13:50Z" and the
  original batch Changes record says "observed 13:55Z". Neither was an
  observation at that time. The focused checks and status ran as one bash call
  from 13:49:06.882 to 13:49:07.721, after the canonical edits ended
  (13:49:00.243) and before the Changes create (13:49:17.183). The pack status
  text was written before the checks started, and 13:55Z is later than the
  batch final commit (13:49:45.676). The checks did run after the edits and
  before the Changes record and Review; the call was not timed per check. The
  state create and parse ran in parallel at 13:49:25.8, and the Review create
  and two state edits started in parallel at 13:49:40.806, after the checks
  and the Changes record. Original records are preserved unchanged.
* Defect wording. The statement "no runtime defect is confirmed" in the
  current-status subsection means that no NEW runtime defect was identified
  by this documentation checkpoint, which did not run or assess runtime
  behaviour. It does not remove or disprove the original two High runtime
  findings, which stay open in the status table. R9 root outcome Revise, the
  independent and unapproved R10 design correction, and FIX with #144
  implementation held are unchanged. Both owner code decisions (comments
  `6681120797` and `6685915140`) stay resolved and are not reopened.

## Seventeenth stabilization checkpoint: queue dispatch R10 design (2026-11-06, Refs #440 #144 #107 #118 #122)

Refs #440 (open), #144 (open), #107, #118 and #122. This is a new bounded
documentation-only checkpoint that records the finished #144 R10 dispatch
protocol design as an unapproved DRAFT proposal and gives this author's own read
assessment of it. It is design and source observation only: no test, SQL,
browser, container, scanner or provider call, no source change and no
enablement. Earlier checkpoints and RPI records are historical and unchanged.
The draft design, this checkpoint and its recommendation are not approved by
any owner, role or ADR. Local candidate, pending coordinator consumption.

Evidence labels used below: Proposed (a draft design contract, not behavior);
Approved, code-role only (an owner code decision, not a live grant, spend,
deployment, financial waiver or ADR acceptance); Observed (a git or read-only
check recorded in the Changes record); Implemented-unverified (candidate code
read but not run); Unobserved (needs a real SQL, Azure or provider run);
Deferred. Times in this section are per the coordinator's assessment, not
independently observed, unless the Changes record captures them.

### R10 pins and topology

| Pin | Identity |
| --- | --- |
| Governance documentation target `feat/discovery-assurance-integration-123` | `119828353ccc1d678c1a4e9c1c67b621b0d263a0` (fetched; this checkpoint does not move it) |
| Main | `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` |
| R10 design commit (`issue-144-queue-recovery`, read from pinned objects) | `1e19209985d93e053dd449e873e792f214dd110c`, tree `7c6126374cbd6e5f5c2e62479cbee1dea98d75e3` |
| R10 design file | `.copilot-tracking/design/2026-11-06/issue-144-r10-dispatch-protocol-design.md`, blob `de776799aafc925c372c6c1c85e0c72ecc75b389`, 15360 bytes (re-resolved by `git rev-parse` and `git cat-file -s`) |
| Design source pin (R10 planning commit) | `3b1f51849d4108581fcbe7fc5059ce61fb448c80`, parent `323abba2e6f392e54c4ac27b427e00d05a3e6782` (the R9 design); merge base with main is main `bb3a3b03`; `src` differs from main by 12 files, +1241/-18 (the unmerged queue slice) |
| `feat/infra-hosting-integration-136` | Local ref `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` whose reflog reads "branch: Created from origin/main"; `git ls-remote --heads origin` returned no branch, `git fetch` of it failed ("couldn't find remote ref") and `gh pr list --state all --head` returned `[]` |

Topology reading. The earlier claim that a parent 136 points to main is
historical (fourteenth checkpoint). As observed when checked, a local label at
main exists and no published branch or PR exists. That is neither a published
parent, ancestry, authorization nor approval; no branch is created, retargeted,
rebased or published here. The eventual code parent is UNKNOWN until deliberately
resolved before any publication, and main `bb3a3b03` is the only verified pin.
This differs from the supplied brief (no local or remote ref) for the local ref
only; the remote and PR absence match it.

Documents at governance, main and this child (identical blobs; draft or
in-review status is not approval): BRD 0.21.0 draft
`34d88395de861e9799eb9e24121a21c92c7a5adc`; PRD 0.21.0 in-review
`c788b917bafaede215f326f0efc71e071a687f1c`; ADR 0001 Proposed
`d42fa5c4615f4107cee83e07555dba6985c1f53e`; ADR 0002 Proposed
`cbe21530043ff15432cc6dce1086d080f5eb15b4`; ADR 0003 accepted with owner
amendment `d60645397b20fb70ac3d1dc47c7a6c8671201306`; ADR 0006 accepted
`956da1a3b804c803041fe2e8a312bd9f400273ae`.

### R10 source facts, merged versus candidate-only

| Fact cited by the design | On main `bb3a3b03` | In the 144 candidate source | Class |
| --- | --- | --- | --- |
| Strict ledger `EVENT_FIELDS` and `meter-evidence-invalid` reader | Present | Present | Observed by static read; not run |
| `FINANCE_ROLES` tuple and `require_role` | Present | Present | Observed by static read |
| `Assistants.transaction()` SERIALIZABLE on SQL Server and BEGIN IMMEDIATE on SQLite | Present | Present | Observed by static read; real SQL races unobserved |
| Queue adapter (`MAX_DELIVERIES` 5, `visibilitytimeout`, `release` at 0), worker, `_worker_complete` route, service-caller wiring | Absent | Present | Implemented-unverified, unmerged |

The design's "established code facts" therefore mix merged code with unmerged
candidate code. Candidate-only code is not main behavior and not acceptance.

### R10 contracts (all Proposed, DRAFT)

The final design supersedes the preliminary R10 Research, Plan and Details where
they differ (for example the optional digest method and the strict `reconciled`
field set). Each of the 14 critique findings (PC-001 to PC-014) has a stated
proposed contract; that is design coverage, not behavioral closure.

| Part | Proposed contract | Owner |
| --- | --- | --- |
| A | API recomputes the exact request with a shared `request_plan` before any reservation; optional final-bytes `dispatch_check_request` leaves one-argument meters unchanged | #144, #107 |
| B | Durable `queued` provenance and a never-overwritten `permitted` marker; derived states unused, permitted, unknown, settled; marker blocks reclaim, republish and retry | #144 |
| C | One `issue_permit` transaction, task row first, DB time re-read, explicit rollback or committed denial per branch, `closed-without-permit` ordering | #144, #118 |
| D | Marker-bound settlement first; `conflict_key` dedupe; held null amounts counted as reserved | #107 |
| E | Strict `reconciled` ledger kind, one `_settled` helper with report cutoff, Finance reconcile route using the unchanged role tuple, `ZF_AI_RECONCILE` default off, ledger event as the audit of record | #107, #144 |
| F | Monotonic worker timing, 35 s nominal inside the 40 s window, lease at least 45 s and visibility equal to the lease, backoff, poison and authentication hold | #118, #144 |
| G | Race and failure matrix | #144 |
| H | Owner map and surface change: worker permit route and Finance reconcile route; no Bicep, role, manifest or table change | #107, #144, #118, #122 |

Owner code decisions (Approved, code-role only, resolved, not reopened): the
second exact permit route for the Application-only worker (issue 144 comment
`6681120797`) and audited Finance-role reconciliation of unknown AI usage from
provider evidence (comment `6685915140`). Unknown amounts stay reserved;
budget, consent, revocation, manual-path and default-off controls are
preserved. No invented usage, reset, bypass or automatic repeat, no live grant,
spend, deployment, financial waiver or ADR acceptance, and no new role grant.

### R10 trace (document-qualified)

| Requirement or decision | Design part | Status and limit |
| --- | --- | --- |
| PRD FR-061 (joins BRD FR-052, AC-102, AC-103, OD-51), PRD AC-107, AC-108 | A, D, E (ledger, price, reporting) | Draft documents; economics reporting not delivered here |
| PRD NFR-017 (joins BRD NFR-012, AC-100, AC-101, OD-51), PRD AC-109, AC-110 | A to F (finite limits, hard termination, unknown liability reserved, human approval of live budgets) | AC-109 is the closest criterion and is "Not run" in the PRD; the proposal would serve it and is not evidence of it |
| BRD OD-51, PRD OQ-027 (budgets, owners, price) | None | Open; nothing invented |
| ADR 0001 and ADR 0002 (Proposed) | Queue and agent estate | Only Proposed support; no approval implied |
| ADR 0003 (accepted with owner amendment) decision 1: no new service, queue, store or network path for the journey capabilities | Queue path | Tension recorded in the fourteenth checkpoint, still unresolved; the owner code decisions are not an ADR change |
| ADR 0006 (accepted) | `src/core`, `src/api`, `src/agents` boundary | Package boundary only |

The design's own closing citation of "ADR 0002 decision 6, PRD PR-005 and
NFR-002" is not carried forward. In the documents at these pins ADR 0002
"decision 6" is the Dockerfile and CI item and PRD PR-005 is the whole-stock
(about 60,000 homes) paging requirement; neither concerns dispatch or AI
consumption. The fourteenth checkpoint already flagged the ADR 0002 item.

### R10 findings, recommendation and gates

Independent assessment (read of the whole design, its critique and Review, plus
static greps; no run). It agrees with the coordinator's conclusion that no new
blocking design flaw is established, with two additions above: the document
trace mis-citation (documentation only, non-blocking) and the local 136 ref
observation. No new runtime defect is established by this documentation
checkpoint. That does not remove or disprove the original two High runtime
findings, which stay OPEN, nor the R9 Revise history; the issue 144 acceptance
criteria stay unproven.

Residual risks, owners and classes:

* Provider evidence for `unused` reconciliation is free text that code cannot
  verify; conclusive Finance-owned evidence is Unobserved (U4, Finance, #107).
* Real SQL Server races and deadlocks for `issue_permit` are Unobserved (U6, #144).
* Azure delayed visibility, `DequeueCount` poison behavior and the 5 s timing
  margin are Unobserved (U3, #118).
* Equality of API and worker Foundry settings when hosted is Unobserved (U7, #118).
* The marker binds only workers that use the permit route.
* The lease, visibility and startup validation contract is Proposed and absent
  from the candidate source.

Classification: local read and git topology observations (Observed);
candidate queue and worker code (Implemented-unverified); R10 contracts
(Proposed); U3, U4, U6, U7 (Unobserved); production budget and real
provider evidence (Deferred). Nothing is Azure observed or blocked for this
slice.

Recommendation: CONTINUE, a bounded tests-first runtime correction, only after the
coordinator consumes this checkpoint, run as an independent genuine full RPI.
HOLD worker enablement, spend, live acceptance, main integration and whole
issue closure; FIX stays the status for 144 implementation until then.

Gates before any publication of that code: FULL local gate, real SQL
Server evidence, independent exact-head review and hosted CI. Resume
conditions: coordinator consumption, a deliberate decision on the code parent
(topology above), and the owners above for the Unobserved items. Independent
lanes (79, 80, 1231, HVE work) continue. No push, pull request, issue or board
write, tick or closure is made by this checkpoint, and no approval is implied.

## Retained-evidence verification of the Sixteenth checkpoint (2026-11-06, Refs #440 #184 #185 #188)

Focused, documentation-only, additive. It qualifies the Sixteenth sensor
checkpoint, which labelled the child receipt figures as supplied. It adds no
checkpoint number, no runtime run and no approval. Files were read by the
author in this session; nothing was re-executed.

### Pins and documents

| Item | Value |
| --- | --- |
| Main | `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` |
| Parent `origin/feat/live-simulator-integration-184` | `9476dc9610368a9a1bd46c88314586885638580d`, tree `30167885b00d308d7b29e9a78a064f4af834ce98` (fetched this session) |
| Reviewed child head | `6887377845648502f2a5509801ee5d9807869703`, same tree as the parent |
| BRD 0.21.0 draft | blob `34d88395de861e9799eb9e24121a21c92c7a5adc` |
| PRD 0.21.0 in review | blob `c788b917bafaede215f326f0efc71e071a687f1c` |
| Diff size, parent against main | 99 files, +1967 and -81 including tracking records; the Sixteenth's 19 files, +1169 and -81 counted source and tests only |

Draft and in-review documents are not approvals.

### Retained evidence read

| Observation | Class |
| --- | --- |
| `/mnt/ama-gates/g188-r20-1106/receipt.json`: sha256 `e575146936c97ffb4e397dd78a75951a079000c18c979d3374f863e6c1c95014` equal to `receipt.sha256`; status passed, scope full, jobs 1, failure null, 17 executed groups, none skipped, fresh image cache | Local observed (file) |
| Receipt identity: head `6887377`, tree `30167885...`, base and merge base main `bb3a3b03`. The receipt belongs to the child head, not to the parent commit `9476dc96`; the trees are equal | Local observed (file); not a gate at the parent commit |
| 205 commands: 192 with exit 0 and 13 with exit 1 (counted from `exit_code`). The child's native handoff attributes the 13 to expected probes (six namespace, one yaml, one pptx, five SQL readiness attempts); that attribution was not re-derived here | Local observed (count); child account (cause) |
| Hosted-only items in the receipt: GitHub approvals and checks, OIDC and Azure what-if, manual release, real AI acceptance | Not run, blocked or unknown |
| Maintained real SQL (`0176-mssql.log`): 285 tests OK, one skip `MssqlHazardReferral.test_json_postsave_audit_failure_reports_persisted_uncertainty` ("JSON-only separate-file audit ordering") | Historical child observation, read from retained log |
| Package suites: core 2363 tests with 226 skips, API 1941 with 338 skips; these skips are not real SQL runs | Historical child observation, read from logs |
| Owned SQL supplement (`/mnt/ama-gates/e188-r20-1106/sql-sensor.log`): 68 tests OK; `cleanup.json` status removed-and-absent-confirmed. It is a separate run outside the receipt command list. Zero skips is the child's account; the log tail shows OK | Historical child observation |
| Image scans (all-vulnerability reports for api, agents, orchestrator, importer): each 42 instances (40 High, 2 Critical), 17 unique vulnerability IDs, fixable 0. The older figure 39 (37 High) is history; the cause of the increase is not verified | Local observed (computed from JSON) |

Zero fixable findings is not a security-clean result. Browser and accessibility
results in the receipt directory were only partly read and are not cited.

### Boundaries and trace

* Document-qualified trace is unchanged from the Sixteenth: BRD FR-048, AC-090, RULE-014, OD-43; PRD FR-050, AC-066 to AC-068; ADR 0003 decision 6.
* Device mapping remains dry-run and synthetic. Weather data is the versioned synthetic reference `synthetic-weather-continuity-v1`, whose source says it is not witnessed Azure continuity, physical accuracy, indoor evidence or calibration. Replay is a flag on consumer receipts and indoor rows use a separate reading-v2 path. These are static source readings, not runtime evidence.
* Unproven: live Hub and authenticated Azure SQL, credential issuance, secure storage and teardown, resident consent, calibration, statistical validity, generator provenance, named human approvals, a receipt at the parent commit, main integration.

### Classification, recommendation and gates

* Local observed: file identities, counts and image scan figures above. Historical child observation: SQL runs and suite results. Implemented-unverified and deferred: the #1205 apply path and its unmet criteria. Blocked or unknown: the items under Unproven.
* No new defect is established; no new issue or refactor is proposed. Open criteria stay with #184, #185 and #188. Verifying the 42 versus 39 image difference belongs to the #188 lane.
* Recommendation: CONTINUE independent lanes (#110 and #186 analysis, #185 adapter design, scanner-difference verification). HOLD closure of #184, #185 and #188 and dependent expansion until the credential owner, consent, calibration evidence, a gate at the intended parent head, hosted CI and named approvals exist.
* Gates: coordinator reassessment, hosted CI on the parent, human approvals. No tick, closure, push or pull request is made here.

## Parent #73 topic checkpoint: employee exception screen integration (2026-11-07, Refs #73 #135)

Parent-topic observed and candidate evidence on `feat/workbench-integration-73-demo`. It is not merged-`main`, Azure, live, human or assistive-technology acceptance. Focused tier, one test file and this record; no server, store, auth, schema, model, infrastructure, dependency or web source change in this slice.

### Source identities

| Item | Value |
| --- | --- |
| `origin/main` (fetched) | `23b26a7f3a4693cd20dcf0447303d97491096cb3`, unchanged |
| Parent topic after child merge | `d17aee537ec267162af106e14056440274ae589d`, tree `38ebb2da6b0499ffadcf29fd8ddfe675afdc564c` |
| Child PR | #1257 (`feat/operator-exception-api-screen-135` into the parent topic, not `main`), squash merged 2026-11-07T17:59:43Z, original head `819022f858b3fdc4dfe20357304a5754221d5ed8`; hosted and review results are coordinator-reported, not re-observed here |
| `role-screens.js` | blob `55f503d5952942d0fbed84deac38f9273cc06b23` |
| BRD | 0.21.0, draft, blob `34d88395de861e9799eb9e24121a21c92c7a5adc`, unchanged |
| PRD | 0.21.0, in-review, blob `c788b917bafaede215f326f0efc71e071a687f1c`, unchanged |

Draft and in-review documents are not approved by this record.

### What the integration observes in source

* The existing role-screen host (`roleScreensView`) forwards the page rows and selected case to the data-operator `overview`, which asks the existing `GET /api/exceptions` only after an explicit link (`exceptions=1`). Each view is audited by the existing endpoint (`src/core/README.md`, exception register), so the default screen load makes no request.
* The screen is installed for the existing programme manager and support officer roles only. Other roles reach neither the screen nor the endpoint.
* Returned values render as text with both conflict values, source, date and version, eligibility Unknown and no winner. Denied, unavailable, malformed and aborted responses show no rows. Failed or quarantined AI requests are labelled as not delivering a model result; deliberate workflow-only processing is neither a failure nor a model result and is never listed.
* Traceability: [BRD](../brds/agentic-retrofit-programme-brd.md) `BRD::FR-034` and [PRD](../prds/zava-forward-retrofit-programme-demonstrator.md) `PRD::FR-034` and `PRD::SA-003` (shared ownership, reason and explicit unknowns), within epic #73; #135 cites `PRD::FR-029` and `PRD::AC-040`. These are mapping observations, not proven acceptance.

### Actual local commands and outcomes

Run from `src/api` in a dedicated virtual environment with editable installs of `src/core`, `src/agents` and `src/api` (import path confirmed inside this worktree), `PYTHONPATH=../core/tests:../agents/tests:tests`.

| Command | Exit and result |
| --- | --- |
| `python -m unittest tests.test_exception_register.Config tests.test_exception_register_screen tests.test_data_operator_screen tests.test_role_screens tests.test_role_screens_conformance` | 0; 45 tests OK, including 5 new `HostIntegration` host-level tests |
| Three one-line mutants of `role-screens.js` (host stops forwarding rows and case; explicit-request rule removed; screen role list widened), each restored afterwards | `HostIntegration` failed each time (1 failure per mutant); source diff empty after restore |
| `ruff check`, `ruff format --check`, `mypy` on the test file; `node --check role-screens.js` | all pass |

### Not run, open gates

* Selected-tier native `python3 tools/rpi-checks.py --changed` and the integrated real-browser observation (keyboard, narrow reflow, real DOM abort): not run, because another run holds the shared heavy resource; they await a new coordinator admission. The existing `Register` and `Endpoint` authority classes (SQL store and local server fixtures) were not re-run on the parent head.
* Independent current assessment, hosted checks on the final head and human approvals.
* The child browser story ended 74 steps with exit 0, but an intentional held-request abort printed a `CancelledError` and the original helper expectation failures are retained; page errors were 0, which is not an all-console or pristine-harness proof.

### Limitations and remaining owners

* #135 stays open: no failed-import, integration or stranded-task producers wired to intake, no durable controlled recovery, no named stewards or approved runbooks, and no role, human, resident, professional, assistive-technology or live acceptance. The owner is the existing #135 issue owner.
* Manager-only host (a named non-manager steward cannot open it), re-audit on refresh, raw provenance strings without `translate="no"`, placeholder guidance, and unbounded rendering above 50 rows are recorded follow-ups.
* No actual model result was observed. Fallback, quarantine and workflow-only are never successful AI.
* #73 criteria (stabilization #440, all children closed or deferred, every requirement with a passing check or deferral), #74, #76, #79 and #80 remain open. Nothing is closed or ticked by this record.

## Ranking publication current-main stabilization checkpoint (2026-11-08, Refs #440 #79 #1231)

Scoped recurrence of the open #440 checkpoint on current `main` after the ranking publication integration (PR #1239) merged. Focused tier: documentation and tracking only, no production, deployment, infrastructure, SQL or security-policy change. It is local engineering observation, not whole #79, #1231 or #440 acceptance, and it does not alter the earlier sensor or discovery checkpoints, which stay on their own protected branch and PR.

### Source and document identities

| Item | Value |
| --- | --- |
| Source observed (merged PR #1239 squash) | `a80acadaa1b7d96a10e71b246e297bc2825d3de5`, tree `5d2df9af254883ec75dedb93ac29bab50482fbe1`, merged 2026-11-08T02:11:31Z; coordinator reports tree equality with candidate `ac0f29f92afcc39e0700f67239a4b202f29b7573`, and the retained receipt identity tree is the same value |
| `origin/main` when observed | advanced once to `77fa5d35e` (generated rubric score commit, one file `.github/rubric/scores/latest.json`); no ranking source, test or document change, so the observed ranking source is unchanged |
| Docs child | branch `docs/ranking-main-stabilization-440`, declared PR target `main`, started on `a80acada`; planning commit `32db7bd6e430fa99292b495ebe9dd9e01f0aee98` precedes this edit |
| BRD | 0.21.0, status draft, blob `34d88395de861e9799eb9e24121a21c92c7a5adc` |
| PRD | 0.21.0, status in-review, blob `c788b917bafaede215f326f0efc71e071a687f1c` |
| ADR 0002 | Status Proposed, ms.date 2026-10-24, blob `cbe21530043ff15432cc6dce1086d080f5eb15b4` (decision 4: ranking policy and retained publication) |
| ADR 0003 | accepted with owner amendment, blob `d60645397b20fb70ac3d1dc47c7a6c8671201306` |
| ADR 0006 | accepted, blob `956da1a3b804c803041fe2e8a312bd9f400273ae` |

Draft, in-review and Proposed documents are not approved by this record.

### Retained historical evidence (source-qualified, not fresh at the squash commit)

* Receipt `/home/azureuser/.local/share/ama/gates/g79-p-dd92-r1-1108/receipt.json`, sha256 `5627d5758cb14745164054c0c1803544ed0c90f5d064b2fc1b4297ed75a0744c` (matches the supplied value): schema 4, scope full, status passed, failure null, jobs 1 (a higher count was requested), image cache fresh, sealed 2026-11-08T01:34:20Z, head `ac0f29f9`, base `b284d0d3e8ebed24d40bf9eb1e23de1ae9101d01`. It was verified full immediately before merge against that base; main then advanced, so it is historical premerge evidence and not a current full-base receipt or a gate at `a80acada`.
* 205 commands, 192 exit 0 and 13 exit 1; the 13 are `python -c import ...` probes (read from the receipt argv). No group is recorded as skipped. This session read the retained logs and the sha256 of every log read equals the receipt value. Counts from those logs: core 2404 tests with 226 skips, agents 273, API 1982 with 339 skips, orchestrator 104, importer 39, static 86, infra 533, migration 25, MSSQL 286 with 1 skip (the declared JSON-only audit-ordering skip), browser logs 3 and 1. The maintained Chromium and axe states and the four image reports are coordinator-reported and were not re-read here.
* Hosted-only items the receipt lists as not run: GitHub approvals and protection, OIDC and Azure what-if, manual release or deployment, real AI acceptance.
* The serialized `gh pr diff` failed at the 300-file cap and is recorded as failed; it is not claimed successful. The complete 308-path equivalence (four paginated API pages, 308 blob matches, byte-equal remote Git diff) is a coordinator report in session files and was not re-run here, so it is not observed in this session. The earlier full-log read's missing contemporaneous-hash caveat remains.
* Retained history, unedited: the original socket-path preflight refusal and the earlier R35, R31 and 7990 adverse records are kept by the coordinator and named in `.copilot-tracking/reviews/2026-11-08/issue-79-r33-parent-dd92-review.md` (RV-001, RV-002). No tracked file in this checkout holds the socket-path refusal log, so no path is invented and it is not read or reported as a pass.

### Actual local commands and outcomes (this session, installed packages)

Environment: Python 3.12.3 virtual environment `/mnt/ama-gates/ranking-main-440-1108/venv`, built from `git archive HEAD src` exported to scratch so no build output touched the checkout; `src/core`, `src/agents` and `src/api` installed non-editable (`pip install` exit 0, `pip check` exit 0, versions 0.1.0). `PYTHONDONTWRITEBYTECODE=1`, scratch `TMPDIR`, `HOME` and `ZF_DATA=/mnt/ama-gates/ranking-main-440-1108/data/zavaforward.json` (empty; no private dataset read). Import identity run from the scratch directory: every probed module (`zava_forward.core`, `ranking_publication`, `ranking_publication_runner`, `zava_forward.api.server`, `cohort_ranking_eval`) resolves under the venv `site-packages`; the installed `ranking_publication.py`, `ranking_publication_runner.py`, `ranking.py`, `store.py` and `server.py` have the same sha256 prefix as the worktree files. Native time 2026-11-08T02:20:08Z to 02:21:26Z; no heavy lock holder or competing gate was present; `/mnt` stayed at 5.4 GB free; the checkout stayed ignored-inclusive clean after the install and after the runs.

| Command | Exit and result |
| --- | --- |
| `cd src/core && PYTHONPATH=tests python -m unittest discover -s tests -p "test_ranking_publication*.py" -q` | 0; 76 tests OK, 0 skips |
| `cd src/api && PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p "test_ranking_*.py" -v` | 0; 53 tests OK, 0 skips; includes the 60,000-case timing in `test_ranking_scale.py` (filtered paged list 63 ms, map clusters 325 ms) |
| `cd src/agents && PYTHONPATH=../core/tests python -m unittest discover -s tests -p "test_cohort_ranking_eval.py" -q` | 0; 20 tests OK; the runner output keeps the blockers `insufficient_sample` and `unapproved_thresholds` (OQ-018) |

The API `SqlStore` classes in `test_ranking_policy.py` use a SQLite-backed store, not SQL Server; this observation is not real MSSQL evidence. Logs are in `/mnt/ama-gates/ranking-main-440-1108` (`core.log`, `api.log`, `agents.log`, `identity.log`, `bytes-equal.log`, `pip-install.log`).

### Traceability and boundary findings

| Requirement or decision | Source and observation | Class |
| --- | --- | --- |
| PRD `PR-006`: deterministic order, versioned policy, named owner | `ranking.py` pure function with no clock, seed or model; `ranking_publication.py` immutable record named by policy version, as_of and snapshot hash; core selectors passed | local observed (this session) plus historical receipt |
| PRD `PR-006` truthful concurrent outcome | exclusive 0600 stage, synced, hard link so the first writer wins; the loser reports the existing record; stage removal failure reported as `stage_retained`; damaged existing record refused; `ConcurrentWriterTests` including separate processes passed | local observed |
| Durability | a failed folder sync after the link raises `DurabilityUnconfirmedError`, record kept, audited as `ranking_snapshot_publication_unconfirmed`, HTTP 409 `committed_unconfirmed`; retry confirms; wiring tests passed. Crash and supported-filesystem behaviour is not observed; first publication into missing nested ancestors is owned by #1258 | local observed for the mocked paths; filesystem crash unknown |
| Hard links and storage | no hard-link support or unwritable folder is a path-free storage failure, not an authorization failure; nothing is overwritten; wiring test passed | local observed |
| API, auth and roles | snapshot, publication status and publish are manager-only; GET does not publish; non-manager gets 403; wiring and policy tests passed | local observed |
| Human authority | the runner refuses to publish an unsigned policy outside exercise (`approval_missing`); sign-off is a recorded human act bound to the rule-order hash and cannot be proved by code; `ranking-v1.json` has owner `to be named`, no sign-off and status draft; the API reports `policy_signed` and unsigned publication is audited | local observed; sign-off, first rule order and policy owner unapproved |
| PRD `PR-007`, `PR-008` AI never changes ranking | ranking has no AI input; the offline cohort evaluation uses constructed pairs through the real `rank` and says its results are never fairness evidence | deterministic computation observed; actual model work not observed |
| PRD `FR-012` with `AC-015`, `AC-040`; `FR-054` with `AC-073` | missing or ineligible inputs give reason codes or review, not silent exclusion; evaluation stays blocked on unapproved thresholds (OQ-018); manifest is a developer fixture | implemented, unverified for acceptance; blocked on owner approval |
| ADR 0002 decision 4 (Proposed) | its implementation-status row (a dated 2026-10-08 snapshot that says it is not the current status) still says no scheduled publish step; the current contract is in `src/core/README.md` | dated history, not a contradiction; no ADR edit |
| ADR 0003, ADR 0006 | local-first ladder and layout boundaries respected; nothing in this slice changes them | no change |
| BRD 0.21.0 draft | states ranking only generally (arithmetic once weights are agreed; fair prioritisation needs an approved cohort policy); no numbered BRD NFR for ranking is claimed | draft |

Boundary observations: the viewer snapshot file `ranking-snapshot-<version>.json` beside the data is rewritten with `os.replace` and is not the immutable archive, so it carries no no-overwrite contract; this is a design distinction, not a PR-006 defect. No new runtime defect is established by this checkpoint: static reading and the three selectors found none.

### Existing owners compared

* #1258 (Medium, archive ancestor durability) and #1259 (Medium, unusable archive path read as a healthy empty archive) stay open and non-blocking for the previously scoped publication. They were compared against every observation; this record adds no duplicate and no new issue.
* #1231 (concurrent-writer metadata, parent topic merged), #79 (epic), #81, #86 and #107 stay open. No other open issue matched `ranking in:title`.
* This record cannot regrade or close any of them.

### Not run, exclusions and open gates

* Not run: fresh FULL at the squash commit, real SQL Server, browser or axe, container or image build and scan, Azure, any model or provider call, private `ZF_DATA`, and the native focused gate result, which is kept in the external handoff for the final head and not embedded here.
* Not established: live model effectiveness (there is none in this checkpoint), controlled benchmark, policy owner and first rule order, thresholds, retention (a separate Legal or DPO decision), deployed scheduling, supported deployment, filesystem, cross-UID and crash behaviour, assistive-technology and human acceptance.
* Remaining gates: independent exact-head assessment, hosted CI, human and policy-owner approvals, a later full gate at the then-current `main` before any whole-issue claim, whole #79, #1231 and #440 closure, and expansion approvals for #81, #86, #107 and ranking follow-up work.

### Classification, recommendation and gates

* Local observed (this session): installed-package ranking publication, runner, API boundary and cohort evaluation selectors above. Local observed, historical and source-qualified: the full receipt at `ac0f29f9` against `b284d0d3`. Azure observed: none. Implemented, unverified: scheduler, retention, crash behaviour, sign-off. Deferred: #1258, #1259 fixes. Blocked: threshold approval and policy sign-off. Unknown: live model, Azure and acceptance behaviour.
* Recommendation: CONTINUE. The merged ranking surface holds its deterministic, no-overwrite, truthful-outcome and manager-only boundaries at this source; no fix or pivot is proposed, and no pivot, threshold, rule order or retention is approved here. Work on #1258 and #1259 proceeds as separate FULL-tier RPI, and independent lanes continue.
* Gated by this record: closure of #79, #1231 and #440, and approval of #81, #86 and #107 expansion, stay gated on the remaining gates above. Nothing is ticked and nothing is closed by this record.

### Current-main currency note (2026-11-08, appended later)

* After the section above was frozen at `aa8f0d11baefab38e4d5e4dc4d9c6f55ed03d77b`, `origin/main` was `77fa5d35e915e524af9a5d536e3ae093b69c5807` (`chore(rubric): record score 77/100`, 2026-11-08T02:19:23Z). Against `a80acada` it changes only `.github/rubric/scores/latest.json` (blob `6741ddd61aba2ff80cd8b7cb2f59e63cb1af7db3`, mode 100644, valid JSON). It is a generated score commit, not new ranking, model, deployment or acceptance evidence. The observations above stay as recorded, and the `ac0f29f9` full receipt remains historical premerge evidence against `b284d0d3`, not a current-base full run.
* This branch took `77fa5d35` by a normal merge; no rebase, amend or reset was used, so the earlier planning, author Review and refusal evidence stay in ancestry.
* Distinct refusals: the original socket-path preflight refusal and the earlier R35 adverse records are unchanged and coordinator-held; the native focused gate attempt for `aa8f0d11` was refused before execution (exit 1, candidate does not descend from the reviewed main base) with no receipt, logs in `/mnt/ama-gates/ranking-main-440-1108`.
* Selectors refreshed on the merged tree with a fresh out-of-tree install in `/mnt/ama-gates/c440-currency-r2-1108-checks` (installed modules byte-equal to the worktree sources, synthetic empty `ZF_DATA`, no bytecode): core ranking publication 76 OK, API ranking 53 OK on a SQLite-backed store (not SQL Server), cohort evaluation 20 OK, retention pytest 37 passed, no skips reported, all exit 0. The native focused gate result for the final head is kept in the external handoff and is not stated here.
* The failed serialized `gh pr diff` and the coordinator-reported 308-path equivalence qualification are unchanged. Recommendation stays CONTINUE and gates ranking expansion, #81, #86, #107, #1258, #1259 and discovery #123 shared-document reconciliation; it accepts no whole #79, #1231 or #440 and no policy.


## AI and employee chat current-main stabilization checkpoint (2026-11-08, Refs #440 #157 #159 #104 #107)

Scoped recurrence of the open #440 checkpoint on current `main`, reconciling the AI and employee chat integration surface after three bounded engineering increments merged and after backlog status drift was found. Focused tier: documentation and tracking only; no production, tool, workflow, agent, test, BRD, PRD or ADR change. It is local engineering observation. It is not whole #157, #159, #104, #107 or #440 acceptance, not real-provider evidence, and not an approval, pivot, deferral or relaxation.

## Issue 81 parent alignment checkpoint (2026-11-06)

Refs #81 #440. Bounded alignment-only checkpoint for the controlled-lifecycle
parent topic branch `feat/controlled-lifecycle-integration-81`. It records a
local rebase onto current `origin/main` and no-service observations. It is not
FULL validation, publication or acceptance, and it adds no product behavior.
Original records:
[research](../../.copilot-tracking/research/2026-11-06/issue-81-alignment-research.md),
[plan](../../.copilot-tracking/plans/2026-11-06/issue-81-alignment-plan.md),
[critique](../../.copilot-tracking/plans/2026-11-06/issue-81-alignment-critique.md),
[changes](../../.copilot-tracking/changes/2026-11-06/issue-81-alignment-changes.md) and
[review](../../.copilot-tracking/reviews/2026-11-06/issue-81-alignment-review.md).

### Source and document identities

| Item | Value |
| --- | --- |
| Source observed | `main` `608c98e639c874b127b3a4e8f9fdb335673c22c6`, tree `b518fcbc0fbd5f96d834c405a8b853f39d07cc7c`; `origin/main` was equal when fetched (newest change is the generated rubric score file, blob `7e10826b967a9d530dc45f75fb1df8ec9524cb09`) |
| Covered merged PRs | #1275 `4bc1e3f3361a762cc9f0c187d394fdab9a11b033` (tree `85ef5852bcdd17ce73d1684e76f96b70f8d2274f`, merged 2026-11-08T10:51:51Z, Refs #1274 #118 #138); #1271 `457a0c824972f318e41cafae635563d252f8b0ef` (tree `31d67a841b5f0884eef85115222fe56a72717117`, 2026-11-08T11:09:27Z, Refs #107 #104); #1273 `a5295c45209ecc25206c79566a07191921700cfe` (tree `a6f392d4201bc75d6dfcd235805050803b0be740`, 2026-11-08T11:17:13Z, Refs #530) |
| Excluded (scoped to the 608c pin; see Correction 1 for current identities) | At launch and at 608c, PR 1278 (sensor analysis, candidate `6d7b52fd`), PR 1243 (complaints, `eddc7d71`) and parent PR 1240 (`c5edb320`) were OPEN and not in that main; their added functionality and acceptance are excluded from the 608c observation, and candidate-policy observations stay separate. This is not a statement about current main: #1278 later merged to main and #1243 to its parent branch (Correction 1) |
| BRD | 0.21.0, status draft, ms.date 2026-10-24, blob `34d88395de861e9799eb9e24121a21c92c7a5adc` |
| PRD | 0.21.0, status in-review, ms.date 2026-10-25, blob `c788b917bafaede215f326f0efc71e071a687f1c` |
| ADR 0004 | Accepted by the owner 2026-10-15 (decision issue #158, closed 2026-10-15T14:19:00Z), option C staged, blob `9406c2e747ced91e5ba7be4072f9482293c0c38f` |
| ADR 0002, 0003, 0006 | 0002 Proposed `cbe21530043ff15432cc6dce1086d080f5eb15b4`; 0003 `d60645397b20fb70ac3d1dc47c7a6c8671201306`; 0006 accepted `956da1a3b804c803041fe2e8a312bd9f400273ae` |
| Pack and case study at start | pack `81c183ed555a244c1072cff72b6a27a1e168a62b`; case study original `0aec2d8070117a647574b1fadc8cfbdd2af68598`, addendum `888d9ff7d0190799308618dc7f153c00adabd6f6` |
| Docs child | branch `docs/ai-main-stabilization-440`, declared target `main`, started on `608c98e6` |

Owner adoption of ADR 0004 option C staged on 2026-10-15 adopts the architectural direction. It is not DPO, Legal, HR, control-owner or live personal-data acceptance. Draft, in-review and Proposed documents are not approved by this record.

### Status-drift correction (recorded, no new adoption)

The coordinator found that #157 said ADR 0004 was not adopted and #159 said no follow-up panel existed, although ADR 0004 is Accepted (#158 closed 2026-10-15) and child delivery is recorded in `src/`. Only those status paragraphs and the proven #157 criterion "Decision issue below is accepted or the epic is closed as out of scope" were corrected; both updated issue bodies were read in this session and still leave the checkpoint criterion, child acceptance, the #159 screen-reader criterion and the tokenomics criteria unticked. The correction adds no adoption, approval or closure; the earlier "not adopted" wording described the retired MVP.

### Retained historical evidence (source-qualified, not fresh at the pinned main)

* #1273 (coordinator summary `review-530-c162`, reviewed head `c1628cb5`, executed candidate `b02f4492`): 21 actual SQL Server cases (privacy 13, projection 4, demo meter 4), zero skips; three controlled employee Chromium states each with 20 axe passes and zero violations. The coordinator reports that the merged executable inputs equal the tested projection and only the rubric JSON race differed. The responses are controlled or model-unavailable, so this is not real-provider evidence; native egress confinement was unavailable, so no network isolation is certified. Three Low execution-record qualifications are retained by the coordinator, including an expired throwaway SQL credential in generated container metadata that was restricted and not copied. The earlier failed r1 receipt remains unchanged and the manual run is not a verified partial or FULL receipt.
* #1271 (`review-107-0639`, head `0639b6e3`, executed source `8fac72f8`): three `MssqlUnleasedRevocation` methods pass with zero skips; the sole executable delta is 27 added test lines. It proves a restarted worker keeps a partially used allowance. It is not real-AI, budget, attestation or release acceptance; #107 and #104 stay open and use Refs only.
* #1275 (`review-1274-4db`, head `4db31928`, tree equal to the merged tree): actionlint release retrieval is bounded and verified (12 installer, 19 selection and 86 runner tests, plus seven-file lint and four-file strict typing). Original c96a wording, superseded by Correction 1 and kept as history: "The AWF checksum retrieval still fails with 504 and has no supported override; #1274 stays a partial blocker, and no whole-#1274 acceptance is claimed." Corrected reading: the 504 on the AWF checksum retrieval is a dated earlier observation, not a current failure; the rootless checksums-and-bundle installer recovered in #1275 (Correction 1). Permanent AWF resilience stays unimplemented under #1274, and no whole-#1274 acceptance is claimed.
* Each is an actual execution on a historical candidate, plus source equivalence to main as reported by the coordinator. Only the section "Actual local commands and outcomes" below was freshly observed, on the pinned 608c main (not on the later current main in Correction 1). Human review boxes in those summaries are unchecked.

### Where AI is invoked and the authority ceiling (source observation)

Provider boundary for the five assistants and employee chat: `Ai._request` in `src/core/src/zava_forward/core/ai.py` (the resident demo has separate inventoried call sites in `src/api/tests/test_ai_call_site_inventory.py`). It refuses under a data-protection hold, requires a financial meter, and reserves, dispatch-checks and completes the consumption ledger. `Ai.evidence` returns a bounded envelope with no fallback text or raw error.

| Surface | Where the model is called | What deterministic services do | Authority ceiling |
| --- | --- | --- | --- |
| Five registered assistants: `stock-prioritisation`, `assessment-preparation`, `funding-evidence`, `works-resident-coordination`, `quality-evidence` (`REGISTRY`, `src/core/src/zava_forward/core/assistants.py`) | `Assistants.execute`: one provider call per attempt, one agent, no tools, at most 3 attempts, via `AgentWorker.provider_call` | SQL owns role and scope check (`authorize`), rule eligibility, snapshot and source signature, claim and lease, continuity suspension, release admission, validation of output shape and citations, ledger and review state | Proposal only. `Assistants.review` (`assistants.py` 1106-1173): verify, accept and edit-accept need current role and case scope, explicit human source verification, and accept or edit-accept only by the same verifier at the current source signature; reject needs current role and scope only; `quality-evidence` adds an independence check against evidence submitters, recorders and fixers. The proposal requester is not generally barred from reviewing (no general requester separation is enforced). It writes task state and events, never a controlled record. Manual owner route stays available |
| Employee chat, stored thread (`/api/chat/threads/{id}/ask`, `ChatPanel._ask`, `src/core/src/zava_forward/core/chat_panel.py`) | One call per turn through `ChatModel` only when permitted case sources exist; denied by default unless `chat_admission` (`src/api/src/zava_forward/api/server.py`) returns none before and after the call | Refusal of approve, decide, certify, record consent, diagnose and contact-resident asks before any call; per-turn role and case re-check; citation and unsupported-claim, action-claim and withheld-value checks; consumption receipt and audit | Text with citations and the label "AI suggestion, not approved"; no tools, no write path. On any model failure the reply is workflow-only and then a rules-only grounded answer |
| Employee chat, unstored (`/api/chat/unstored-ask`, `ask_unstored`) | None (`model_calls` 0) | Rules-only `chat_case_answers.answer` over the caller's own case projection; audit `chat.turn.unstored` | Used while chat storage is unapproved; stores nothing |
| Proposal from chat (`/api/chat/threads/{id}/proposals`) | Indirect, through `Assistants.invoke` | Same queue and review as the assistants row | HTTP 202 request only; no change before human review under the assistants row (verification and quality independence as qualified there; no general requester separation) |
| Regulatory chat (`src/agents/src/zava_forward/agents/regulatory_chat.py`) | None; offline extractive, `model="offline-extractive"` | Separate synthetic-demo route and role rule | Source excerpts, not legal advice or approval |
| Retained legacy tasks (`ai_tasks.py`, `store.py` `priority`) | `Ai.run` and `look_at` | Template fallback | Not part of the five assistants; unchanged by this record |

Controls observed in source: staff roles only, no contractor chat (`projection.py`); owner-filtered SQL thread, message and memory storage (`chatthreads.py`, Azure SQL or SQLite); storage refused until DPIA, lawful basis and staff notice references exist (`chat_privacy.py`, `ChatNotApproved`) and retention Unknown until a reference and day count exist; owner demo-only activation (`ai_registry.DEMO_ACTIVATION`, owner decision 2026-11-03) honoured only with the exact switch and the demo deployment profile and recorded as superseding DPO and Legal review for the demonstrator only, with DPO, Legal and RAI approval outstanding. Memory items can be stored, listed, edited and deleted, but the live panel prompt does not include them (`memory_used: False` in `/api/chat/status`). No resident contact, consent or approval is possible from any of these paths.

### Actual local commands and outcomes (this session, installed packages)

Environment: Python 3.12.3 virtual environment `/tmp/ai-main-440-1108/venv` built from `git archive HEAD src` exported to scratch; `src/core`, `src/agents` and `src/api` installed non-editable (`pip install` exit 0, `pip check` exit 0, versions 0.1.0). `PYTHONDONTWRITEBYTECODE=1`, scratch `TMPDIR`, `HOME` and empty `ZF_DATA`; no `.env`, no provider or demo-switch variable, no private dataset, no Docker. Import identity: the probed `zava_forward` modules resolve under the venv `site-packages` and the installed `chat_panel.py`, `chat_isolation.py` and `assistants.py` have the same sha256 prefix as the worktree files. Native time 2026-11-08T11:38Z to 11:40Z, sequential, `timeout` and `nice` bounded. Logs stayed in the scratch directory.

| Command (from the project directory) | Exit and result |
| --- | --- |
| core `python -m unittest discover -s tests -p "test_<name>.py" -q` for `chat_panel`, `chat_privacy`, `chatthreads`, `chat_memory`, `chat_case_answers` | all 0; 43, 29, 27, 21 and 4 tests OK, 0 skips |
| agents (`PYTHONPATH=../core/tests`, `ZF_CHAT_GOLDEN` set to the archived `evals/chat_golden.json`) for `chat_model`, `chat_eval` | both 0; 7 and 39 tests OK, 0 skips |
| api (`PYTHONPATH=../core/tests:../agents/tests`) for `chat_panel`, `chat_isolation`, `ai_boundary`, `ai_call_site_inventory` | all 0; 53 (1 skip, "opt-in local Chromium"), 32, 6 and 6 tests OK |
| api `test_assistants.py` | 0; 120 tests OK, 58 skips, each "needs disposable SQL Server (ZF_TEST_MSSQL=1)" |

The skips are reported, not passes: no Chromium and no SQL Server ran in this session. The chat selectors use SQLite-backed stores and a fixture model, so they are not Azure SQL, real-provider or live-processing evidence. Reproduction for finding F1: from the checkout, `grep -rn "\bturn(" src tools --include=*.py` shows only the definition in `src/core/src/zava_forward/core/chat_isolation.py` (non-JavaScript lines).

### Traceability (document-qualified)

| Requirement or decision | Source and tests observed | Class |
| --- | --- | --- |
| PRD FR-047, FR-036; ADR 0002 five-assistant runtime; ADR 0003 decision 3 | five-entry `REGISTRY` and the execute and review path above; `test_assistants.py`, `test_ai_boundary.py`, `test_ai_call_site_inventory.py` | local observed (SQLite and fixture); MSSQL cases skipped here and historical for #1271 |
| PRD FR-055 (panel, registered assistants, sources shown), BRD FR-049 | `ChatPanel`, `permitted_sources`, `skill_sources`; `test_chat_panel.py` (core and API) | local observed; screen-reader acceptance not established (#159, #619) |
| PRD FR-056, AC-095 (owner thread, delete, ledger metadata only), PRD NFR-016, BRD FR-049, NFR-011, RULE-026 | `chatthreads.py`, `chat_privacy.py`; `test_chatthreads.py`, `test_chat_privacy.py` | local observed; retention per class Unknown until BRD OD-46; DPIA, lawful basis and notice references are not recorded; the RULE-026 performance-use prohibition appears as a decision field in `ChatPrivacy.decision()` and its enforcement was not separately observed |
| PRD FR-057, BRD FR-050 (opt-in memory) | `chat_privacy` memory lifecycle; `test_chat_memory.py` | local observed for the lifecycle; memory is not used in the live prompt; BRD OD-48 scope decision open |
| PRD FR-058, PR-007, PR-008, SA-004; BRD RULE-025 (refuse approve and decide, untrusted input, context not evidence, no AI approval) | `out_of_scope`, `ACTION_CLAIM`, `TOOLISH`, withheld paths; `test_chat_panel.py`, `test_chat_model.py` | local observed (lexical checks, not semantic safety guarantees) |
| PRD NFR-015, BRD NFR-010 (per-user isolation and break-glass) | `ChatIsolation.current_user`, `case_context`; `test_chat_isolation.py`; SQL projection cases in #1273 | local observed; SQL cases historical and source-qualified |
| PRD FR-059 (registered task, thresholds, multi-turn evaluation) | `chat_eval.py` over the real `ChatPanel`; `test_chat_eval.py`, golden file | implemented, unverified for acceptance; thresholds and reviewer approvals not recorded |
| BRD NFR-012, FR-052, PRD NFR-017, FR-061, AC-103; BRD OD-51 (tokenomics) | consumption ledger, `chat_demo_meter`, caps in `/api/chat/status` ("engineering caps, not spend authorization") | local observed for caps; price, budget and cost per accepted outcome Unknown |
| ADR 0004 decisions 5 and 6 (isolation, break-glass) | `chat_isolation.py` break-glass default-deny with audit | local observed; owner demo-only policy, unreviewed by DPO or Legal |
| Real model operation, Azure deployment, attestation | none observed | unknown or blocked; no actual-provider response was observed |

### Findings and existing owners

* F1, confirmed, Low, refactor need, no new behaviour defect: `ChatIsolation.turn` and its `_ask` (`src/core/src/zava_forward/core/chat_isolation.py`, lines 133 and 147) have no static callers in `src` or `tools`. If wired, `_ask` calls `Ai._chat` without `chat_admission`, release or continuity checks (the data-protection hold and financial meter in `_request` would still apply). It is unreachable from the API today. Status: unowned, unfiled, pending triage as a proposed refactor (not an owner-approved deferral). Candidate owner families for triage are #162 (isolation) or #164; a search of open and closed issues for the wording found no existing owner. No issue was filed and no source was changed here.
* F2, traceability gap, not a defect: the evaluation `isolation_contains` and `isolation_forbid` probes use `ChatIsolation.build_prompt`, which can add memory, while the live `ChatPanel._ask` builds a different prompt without memory. Memory-in-prompt behaviour is therefore not evaluated on the live path. It is consistent with `memory_used: False` and stays in the scope of #164 and #163; no separate issue is proposed.
* No new bug in the ordinary employee chat, assistant, isolation or consumption paths was reproduced by the selectors above. This does not prove absence of defects.
* Existing owners compared and left open: #157, #159, #104, #107, #116, #121, #162, #163, #164, #432, #530, #619 (assistive technology, consent and Fluent acceptance for the widget) and #1274 (AWF resilience). #158, #160 and #161 are closed. This record cannot regrade, tick or close any of them.

### Not run, exclusions and open gates

* Not run: Azure SQL or any SQL Server, Chromium and axe, container build or scan, any real provider, Azure or production mutation, private `ZF_DATA`, the full local gate, and fresh hosted CI. No new Docker resources or receipt.
* Not established: real-model operation and quality, screen-reader and other human acceptance, DPO, Legal, HR and control-owner decisions (BRD OD-45, OD-46, OD-48), retention, RAI and Assurance release approvals, tokenomics approval (BRD OD-51), live personal-data use, and whole-epic acceptance.
* Excluded from the pinned 608c main (not from current main; see Correction 1): PR 1278, PR 1243 and PR 1240 functionality.

### Classification, recommendation and gates

* Local observed (this session): the focused chat, assistant boundary, isolation and evaluation selectors above on SQLite or fixture stores. Local observed, historical and source-qualified: #1273 SQL and controlled browser runs, #1271 restart regression, #1275 installer. Azure observed: none. Implemented, unverified: memory in prompts, retention, real-provider behaviour. Proposed, pending triage (unowned, unfiled, not deferred): F1 refactor. Blocked: named DPO, Legal, RAI and owner approvals. Open, not implemented: permanent AWF resilience (#1274); the historical installer 504 was recovered (Correction 1). Original c96a wording, superseded: "Deferred: F1 clean-up" and "Blocked: ... AWF checksum retrieval (#1274)". Unknown: real-provider answers, cost and screen-reader behaviour.
* Recommendation (proposal only): CONTINUE. The merged surface holds its proposal-only, human-review, role-scoped and workflow-only fallback boundaries at this source; no pivot, deferral or relaxation is proposed and none can be approved here. Resume conditions: independent exact-head assessment of this record, hosted CI, then the existing child lanes (#162, #163, #164, #619, #432, #107) proceed as separate RPI; F1 needs triage first (candidate owner #162 or #164) before any clean-up lane exists.
* Gated by this record: closure of #157, #159, #104, #107 and #440, and any dependent expansion (#208 and further assistant or memory features), stay gated on the open items above. Independent lanes that do not touch chat or assistant admission (ranking, discovery, resident work) are not blocked by this checkpoint. Nothing is ticked and nothing is closed by this record.

### Correction 1 and currency (observed 2026-11-08T11:55Z, after independent assessment `review-440-c96a`)

Scope: documentation qualifications only. The independent assessment of candidate `c96a32310466d4f39d31eed986489f44e0ab7c26` (tree `e824079515af425437f03b387e7a2a08b0f6de2e`) requested changes (4 Medium, 1 Low). This subsection corrects those qualifications, adds no adoption, approval, deferral or acceptance, changes no application, tool, test, workflow, agent, requirement or decision file, and reruns no suite. Original c96a research, critique, Review, plan, details, changes and state records are unchanged; the new records are the `correction1` files named below.

| Original c96a statement | Status | Correction |
| --- | --- | --- |
| AWF checksum retrieval "still fails with 504 ... Blocked" (installer bullet and classification line) | Superseded as a current-state claim; kept above as history | The 504 is a dated earlier observation. Safe coordinator log `pr1275-awf-agent-recovery.log` (Capstone Rubric Scorer run `42472167065`, #1275 head `4db319288b837d7269f0e6cc19a309cd52b81b17`, 2026-11-08T10:38Z) shows `install_awf_binary.sh v0.28.23 --rootless` downloading `checksums.txt` and `awf-bundle.js`, "Checksum verification passed", bundle installed and version 0.28.23 reported. The coordinator reports later exact-head scorer retries and the #1278 scorer also passed (not re-run here). That is recovery. Remediation is #1274 (permanent resilience), open and not implemented. Neither is a currently observed installer outage |
| PR 1278, PR 1243 and PR 1240 "excluded from main" | Valid only for the 608c pin | See the current identities below |
| "independent role review before anything changes" (proposal row) and a general independence implication | Overstated | `Assistants.review` (`assistants.py` 1106-1173, read 2026-11-08): verify, accept and edit-accept need current role and scope, explicit human source verification and the same verifier for accept; reject needs current role and scope only; `quality-evidence` adds independence from evidence submitters, recorders and fixers. No general requester separation exists. No new authority rule is proposed or implemented here |
| F1 "Deferred: F1 clean-up" | Overstated | F1 is unowned, unfiled and pending triage as a proposed refactor. It is not an owner-approved deferral. No removal, wiring, refactor or issue action is taken here |
| Original research claim that the case study, addendum, reference index, memory and component guides were read before planning | Unsupported by the original transcript | Amended in new evidence only: `.copilot-tracking/research/2026-11-08-ai-main-stabilization-440-correction1-research.md` records what was genuinely read in this iteration and its exact ranges. The original file is preserved unchanged and its original claims and outcomes were not re-derived from this reading |

#### Current identities (read-only fetch, 2026-11-08T11:55Z)

| Item | Observed |
| --- | --- |
| Pinned observation | `main` `608c98e639c874b127b3a4e8f9fdb335673c22c6`, tree `b518fcbc0fbd5f96d834c405a8b853f39d07cc7c`, unchanged as the source of the original local results |
| Current `origin/main` | `3c57a02d4d2ef61f6922436025b245c8a97e2694`, tree `3ed3dec05adbb7673515fbd90bd51791fd3b58a1` (generated rubric score commit) |
| #1278 | merged to `main` as `e73d421046d00565f610fb671a80e683d2981874`, tree `feff48a485f0d1919698c08e3abd7d70af6a45d4`, 2026-11-08T11:37:10Z, head `6d7b52fdd9e55cd3a1f3a16d976d595bdc63dc88`. Its sensor analysis functionality is now in main; this checkpoint still makes no observation of it and its acceptance is not claimed |
| #1243 | merged into the declared parent branch `feat/controlled-lifecycle-integration-81`, not `main`, as `6ef6dc368ae3f8739095f740aa1e68634bd52922`, tree `0006f193b0fc459920f1fa3cf319d96c2a050c4a`, 2026-11-08T11:38:59Z, head `eddc7d715757a1cf2b50027471adcd9146dd08dd`. Not in main |
| Parent PR 1240 | OPEN against `main`, head now `6ef6dc368ae3f8739095f740aa1e68634bd52922` (was `c5edb320`). Not accepted or published. The coordinator reports native integration in progress locally; that is a coordinator statement, not observed or accepted here |
| #1274 | OPEN: permanent AWF resilience not implemented |

#### Source-equivalence proof for the original local results

`git diff --name-only 608c98e6 origin/main` lists 11 files, all from #1278 (sensor analysis tests, `sensor_sql_check.py`, `src/api/README.md`, its tracking records) and the rubric score file. None is under the audited chat, assistant, isolation, privacy, thread, AI or registry modules, the agents `chat.py`, `server.py`, or any selected test file. The first 16 hex digits of the sha256 of each installed module used by the original selectors equal the content at both `608c98e6` and `origin/main`: `chat_panel` `bf6991cc547cbe94`, `chat_isolation` `7b8c009766ff6d9d`, `assistants` `80fb9a5fdb406158`, `chat_privacy` `ab30c5d022769534`, `chatthreads` `53d25ca09e82d20c`, `ai` `3593be1ea5cdb4e0`, `ai_registry` `cdac92bb3128ab1e`. The original results (core 124, agents 46, API 217 discovered; 59 explicit skips, 58 SQL Server and 1 Chromium; 328 non-skipped cases; every selected runner exit 0; SQLite and fixture stores) therefore stand as source-equivalent observations at the audited modules on current main. They were observed at 608c, no selector was rerun for this correction, and the skipped SQL Server and Chromium checks remain unverified. Expected unavailable-model and law-store fixture messages in those logs are not new failures. No new real-provider, Azure or human approval evidence exists.

#### Remaining gates and exact resume conditions

Unchanged: independent exact-head assessment of this corrected record, hosted CI, and named DPO, Legal, HR and control-owner decisions (BRD OD-45, OD-46, OD-48). Continue is still proposal only. F1 needs triage before any lane; F2 stays within #164 and #163. Pivot, deferral, relaxation and approval cannot be granted here. Nothing is ticked or closed.

## Visible-demo integration checkpoint (2026-11-08, Refs #440 #149 #229 #891)

Scoped recurrence of the open #440 checkpoint after the #149/#229 UX wave (PR 1286) and the owner-authorized employee model observation (PR 1290, #891). Documentation only; no production, tool, workflow, agent, test, BRD, PRD or ADR change, and no test, SQL, browser or model run. It builds on the earlier AI and employee chat section above and does not repeat its architecture or traceability. It is not whole #149, #229, #891 or #440 acceptance, and no approval, pivot, deferral or relaxation follows. Records: `.copilot-tracking/*/2026-11-08-visible-demo-checkpoint-440-*`.

### Identities and covered changes

| Item | Value |
| --- | --- |
| Base and `origin/main` | `6354b13f7abf1441a815e92f2b01dc184ce0b0ac`, tree `0fddb514670c2e1e112f0eb284fdee9f9846c952`, fetched 2026-11-08T19:55Z. Actual `git diff --name-only 656cafb1 6354b13f7` lists only `.github/rubric/scores/latest.json` |
| PR 1286 | merged `28c6ec11cbfc0185a756eb15cd9b324ab0856b94` 2026-11-08T19:38:09Z, exact head `0362e2626587153f367d1dab49c7d0f52611bcba`. AI-state and exception-register checks, atlas and source identity checks, content-standard evidence and document-control refusal wording (Refs #149 #229 #153 #233) |
| PR 1290 | merged `656cafb1eca2813469cf0e8e60af3bfb31b619a6` 2026-11-08T19:44:02Z, head `5b6b965715d5192b323145574156bddedcb3e7ae`. Ten `.copilot-tracking` record paths only (#891 live and C1 records); no application, test or infrastructure file |
| Also on main since the previous checkpoint | #1281 (that checkpoint), #1284 (memory-evaluation scope qualification), #1285 (VM demo release record) |
| Documents | BRD 0.21.0 draft `34d88395de861e9799eb9e24121a21c92c7a5adc`; PRD 0.21.0 in-review `c788b917bafaede215f326f0efc71e071a687f1c`; ADR 0004 accepted by the owner 2026-10-15, option C staged, `9406c2e747ced91e5ba7be4072f9482293c0c38f`; original case study `0aec2d8070117a647574b1fadc8cfbdd2af68598`; addendum `28c1924285eed255e53c1e359e0ad98eedab1d22`. Draft and in-review documents are not approved, and ADR 0004 adoption is not DPO, Legal, HR, control-owner or live-personal-data acceptance |
| Excluded | Unmerged #184 (live streaming into Azure IoT Hub) and #1288 (sensor values and sensor-grounded Quality AI flags) candidate work, and parent PR 1240 (#81, open, head `6ef6dc36`). Their native corrections proceed in their own sessions and their source and activation state is not asserted here. No live IoT sender or receiver activation and no sensor-grounded Quality model activation was observed or verified within this checkpoint |

Source movement since the previous checkpoint pin (`608c98e6`, actual Git): two production modules changed, `src/agents/src/zava_forward/agents/chat_eval.py` (#1284: isolation memory assertions disclosed as component-only, serving memory only as receipt-declared, integrated memory poisoning "not covered") and `src/core/src/zava_forward/core/doc_controls.py` (#1286: refusal wording only, stating nothing was deleted and that retention values are demonstration values). Tests, checks and READMEs under `src/` also changed. The chat, assistant, isolation, privacy, thread, AI and registry modules, `chat_admission` and `Assistants.review` are unchanged, so the earlier source observations on them hold as source reading, not as a new execution.

### Where AI is invoked in the visible demo and the authority ceiling

| Original agent and autonomy | Registered assistant (`REGISTRY`, `assistants.py`) | Where the model is called | Deterministic services | Authority ceiling today |
| --- | --- | --- | --- | --- |
| Stock Prioritisation, L2 recommend | `stock-prioritisation` | `Assistants.execute`, at most 3 attempts, no tools | Ranking, eligibility, scope check, citation validation, ledger | Proposal; human verification and review before any use |
| Assessment, L3 drafts | `assessment-preparation` | same | Stage gates, sign-off separation, safety-hold check | Evidence preparation; no draft submission or sign-off |
| Grant and Funding, L3 drafts | `funding-evidence` | same | Four-state ledger, claim holds | Evidence preparation; Finance submits |
| Contractor and Resident Coordination, L3 acts | `works-resident-coordination` | same | Consent and preference rules | Proposal; no resident contact or booking |
| Quality Verification, L4 autonomous flags | `quality-evidence` | same | Evidence checklist, independence check | Proposal; no autonomous flag, acceptance or sensor-grounded input |

Employee chat is separate from the five assistants. The stored-thread route can call `ChatModel` through `ChatPanel._ask`, at most once per turn and only after `chat_admission` (`src/api/src/zava_forward/api/server.py` lines 48-58) passes. Admission needs a registered activation and, in the demo, the owner-approved demo-only switch (`ai_registry.demo_activation_honoured`: exact `ZF_CHAT_DEMO_ACTIVATION` value and `ZF_DEPLOYMENT_PROFILE=demo`), a finance meter and no continuity suspension. Otherwise the reply is workflow-only or the rules-only grounded answer, and the unstored route never calls a model. The UI label in `src/api/src/zava_forward/api/web/chat.js` line 131 is chosen from the response: "Summary by rules, no record changed", "Model-generated, not approved. Demo only." or "Workflow-only help, no record changed". The employee browser check asserts that label against a controlled provider only, so it shows rendering, not model inference. The ceiling is unchanged: cited text, no tool and no write path; AI cannot approve, decide, certify, record consent, diagnose or contact a resident. A model-generated answer needs the model, called at most once per stored turn. Where no model answer is available (unstored route, model failure, or no model admitted), a rules-only grounded answer from permitted case facts or workflow-only guidance is returned where applicable (`chat_panel.py` 455-505 and 681-688), and the ordinary case controls remain the manual path.

### Evidence by classification

| Class | Item | Source and date | Not shown |
| --- | --- | --- | --- |
| Local observed (this session) | Git identities, diffs and PR and issue states above; direct source reads | 2026-11-08T19:55Z | Any test result. No suite was run |
| Local observed, historical | PR 1286 candidate `fd48`: selected API 76 and Core 19 tests OK; raw mypy API 195 and Core 269 success; Ruff API 121 and Core 216 pass; 212 matching installed production files; Chromium Atlas 194 and Data 100 passed, with two bounded axe scans on Data and zero violations (Atlas has none). Initial API-only import failure in the Core selection retained | Coordinator-reported 2026-11-08, `review-149-fd48-20261108-functional`, executed before the ordinary merge and later main moves | New-tree results, assistive-technology or human usability, real model, SQL Server, scanner or full gate. The Core test selection was source-qualified, not a universal installed-file comparison |
| Local observed, exact head (coordinator assessment) | `0362e262` independent bounded Functional assessment Pass with no blocking findings; merged tree matched the prepared projection | PR 1286 body, 2026-11-08 | Whole-issue acceptance |
| Hosted exact-head checks | All 19 hosted checks passed on `0362e262` (`gh pr checks 1286`, 2026-11-08). Hosted, not local, evidence | GitHub Actions | Results do not transfer to later heads or to this candidate |
| Azure observed, historical | One generic synthetic employee question on the deployed demo app (source `e2ecee2565e86889c6beb43cb32e7c5b54270e01`, revision 0000027): HTTP 200, provider `azure-openai`, `workflow_only` false, `model_calls` 1, outcome answer; UI disclaimer and model-generated label visible; displayed token count 375. First-party identity attested; identity, token and account values are not copied | PR 1290 body and coordinator assessment `891-5b6b`, Pass with zero blocking findings; C1 made zero new calls | Five agents, case-grounded or Quality inference, current-main deployment, complete token, cost, privacy, retention and refusal acceptance (#891 criterion 2 stays unticked), named approval. #891 criteria 3 and 6 are ticked by the coordinator and criterion 2 is not |
| Implemented, unverified | Employee chat over real case sources with a real model; five-assistant answers; the full map, case and briefing journey | Source and controlled tests only. A real generic model answer was observed once (Azure row above) | A real case-grounded answer or human acceptance |
| Deferred or blocked | Sensor-grounded Quality AI (#1288), live IoT streaming (#184), parent #81 integration (PR 1240), assistive-technology and human usability, DPO, Legal, HR, RAI and control-owner decisions | Existing open issues | Any activation or approval |
| Unknown | Whether the deployed demo matches current main; effect of later main moves on the demo | None observed | Current-main deployment |

Adverse qualifications retained. The earlier fd48 evidence ran before the merge into later mains. The PR 1286 native record named `fd48` as the immediate first parent of the merge; the actual immediate parents are `86ed569` and `ecb28815`, so the PR body annotates it additively and the original is preserved. The two early navigation failures and the retrospective chronology of the #891 original report are preserved; its C1 records qualify them, and no timestamp witness is claimed. Existing guarded test-demo direction and the finite demo meter are references, not Legal, DPO, Finance or RAI approval, a new budget or a release waiver. Synthetic fixtures establish no resident or human approval.

### Traceability for this checkpoint

| Requirement or decision | Source and tests | Journey and status | Remaining owner |
| --- | --- | --- | --- |
| Original brief, five agents with L2 to L4 autonomy (original case study; addendum lines 15-26 and 1481-1560) | `REGISTRY` in `assistants.py`; `Assistants.review` | Five proposal-only assistants; fuller L3 and L4 behaviour is a scope or authority gap, not delivered | #157, #104, #107 |
| ADR 0004 option C staged (accepted 2026-10-15) | `chat_panel.py`, `chat_isolation.py`, `server.py` admission | Employee chat, demo-only activation observed once (Azure, historical); stored chat storage remains unapproved | #157, #159 |
| BRD and PRD AI authority rules (FR-044, AC-084, RULE-018, 022, 025, 028 as traced in the earlier section; BRD draft, PRD in-review) | `chat_panel`, `chat_privacy`, `test_chat_panel.py`, `employee_chat_browser_check.py` | Label, refusal and manual path implemented; one real generic model answer was observed (see the Azure observed row), but real case-grounded provider behavior and human acceptance are not shown | #159, #891 |
| UX wave (#149, #229): AI-state, exception register, document-control refusals, content standard | `data_operator_ai_state.py`, `atlas_tensions_browser_check.py`, `doc_controls.py`, `test_document_controls.py` | Local observed at `fd48`, hosted 19 passed at `0362e262`; assistive-technology and usability not shown | #149, #229 |
| Sensor exclusions (addendum sensor-supported condition review row) | None on main for #184 and #1288 | Not delivered. At this pin the `Assistants.capture` Quality allowlist (`assistants.py` 156-160) takes quality records, checklists and documents, not sensor readings; this is not an exhaustive claim about every path or about the deployed demo | #184, #1288, #81 |

### Findings, owners and gates

* No additional defect was confirmed by this checkpoint, and none was reproduced. No new issue is proposed.
* The unused `ChatIsolation.turn` clean-up (F1 of the previous section) is still unowned and unfiled, pending triage. The evaluation probe prompt still differs from the serving prompt (F2); #1284 now discloses it as component-only, and it stays within #164 and #163.
* A recommendation-ordering defect said to have been diagnosed in #81 could not be verified in the #81 body or comments, so it is not linked here and no duplicate is created.
* Open gates: independent exact-head assessment of this record, hosted checks, named professional approvals, assistive-technology and human usability, tokenomics and cost, privacy, retention and refusal acceptance for model calls, fresh deployment evidence on a later head.

### C2 provenance note

The C1 research record states "Written 2026-11-08T20:10Z", but Git records its commit `844884247` at 2026-11-08T20:08:47Z and the correction commit `d8cda455` at 20:09:18Z. Commit ancestry shows the committed plan preceded the correction commit; the stated wall-clock time conflicts with the commit times and the cause is unknown. No timestamp witness exists, and the C1 record is preserved unchanged (C2 research, 2026-11-08).

### Recommendation and resume conditions

Proposed bounded CONTINUE of the existing employee demo and of the independent source corrections for #184 (cohort, receiver and stop contract) and #1288 (sensor provenance, latest capture, honest autonomous flags, withdrawal-safe projections). Only sensor-grounded Quality acceptance needs its own corrected source, integration, separately admitted activation and observed journey. Other gates are each issue's own and are not tied to IoT: #229 its accessibility (WCAG) criterion; #159 screen-reader and turn-accounting criteria; #891 its per-call token, cost, privacy, retention and refusal conjunction (criterion 2); #149, #157 and #81 their epic checkpoints and named-human gates; #440 its triage and independent-review criteria. Named Legal, DPO, Finance, RAI and control-owner decisions stay with their owners. Independent lanes continue, and no criterion is ticked. Pivot, deferral, relaxation and named approval cannot be granted here. Nothing is ticked or closed.
| Pinned `origin/main` (freshly fetched twice, unchanged) | `56eec736906774ef56d8c9a66ed7f3f9c1e520c6` (#1236), tree `e0b82395edda97b2be84f9cc1b44432fbe77727b`; it changes only the coordinator agent file and tracking records, no `src/`, `docs/` or `tools/` |
| Parent starting HEAD (retained as local ref `refs/ama/issue81-start`) | `af891a5cccf730ccf61e670f312b7674218dbe4b`, old base `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` (not used as a workaround) |
| Aligned child commits | `9055abce3` (#1226), `e6434dd1d` (#1228), `81c106998` (#1229); `git range-diff` reports all three `=` (identical patches) |
| [BRD](../brds/agentic-retrofit-programme-brd.md) | 0.21.0, draft, blob `34d88395de861e9799eb9e24121a21c92c7a5adc`, unchanged |
| [PRD](../prds/zava-forward-retrofit-programme-demonstrator.md) | 0.21.0, in-review, unsigned, blob `c788b917bafaede215f326f0efc71e071a687f1c`, unchanged |
| ADR 0001 to 0007 | Unchanged; only ADR 0002 states an owner acceptance line (2026-10-24, staff identity); other statuses not re-assessed |

Draft and in-review documents are not approved by this record. The three
child PRs are parent-topic observations merged into this parent, not
merged-main acceptance. The capacity checkpoint consumed at #440 comment
6676325240 did not satisfy integrated-parent FULL or epic acceptance.

### Covered contributions and requirement traceability

| PR | Behavior | Requirement trace |
| --- | --- | --- |
| #1226 | Fail-closed quality evidence gate; malformed metadata and corrupted replacement handling | PRD FR-008 (governing) with FR-017; PRD AC-011, AC-020 |
| #1228 | Quality gate rule provenance qualified to the PRD | PRD FR-008 and FR-017 |
| #1229 | Explicit capacity booking Pass, Fail and Unknown outcomes | PRD FR-008 (governing) with FR-016; PRD AC-011 |

Numbering differs between documents. PRD FR-008 is the deterministic
controlled-transition gate requirement. BRD FR-008 is a different requirement
(material change invalidates downstream approvals) and is related traceability
only. PRD FR-017 is per-measure quality disposition; BRD FR-017 is handoff
content and is not a quality source. Gate rule records for quality and capacity
cite the PRD; booking rules cite BRD RULE-001 and RULE-002. Rule records stay
exercise fixtures with an unreviewed reviewer; no legal, operational, resident
or professional approval is inferred.

### Preservation proof (local observed)

* `git merge-base --is-ancestor origin/main HEAD` returned 0.
* The pre-alignment dry run `git merge-tree --write-tree` was clean and the real rebase completed with no conflict, so no conflict resolution changed any child content.
* All 48 paths touched by the three children between `bb3a3b03` and `af891a5cc` (8 source and test files, 40 original evidence files) have identical mode and blob at the new head (48 same, 0 different); `git diff refs/ama/issue81-start HEAD -- src` is empty.
* The only difference outside new records is main's own coordinator agent file change. Prior blobs: `gates.py` `0d8d3d15`, `quality.py` `4a1e2991`, `store.py` `86948572`, `appointments.py` `9dc02c5a`, `procurement.py` `f0178666`, `test_gates.py` `91330fb9`, `test_hazard_referral.py` `c89f89f2`, `test_quality_procurement.py` `73813789`.

### Actual local commands and outcomes

No service, no private or default dataset and no sending. Scratch
`/mnt/ama-gates/restart-1106-81-integration`; `env -i` with an explicit
allowlist, `PYTHONDONTWRITEBYTECODE=1`, scratch `TMPDIR`, `ZF_DATA` and caches.
Source origin proven: `zava_forward.core.__path__` is this worktree's
`src/core/src/zava_forward/core`; nothing was installed except `mypy` in a
scratch venv after a real `ModuleNotFoundError`.

| Check (from `src/core`, `PYTHONPATH=src:tests`) | Actual result |
| --- | --- |
| `python3 -m unittest test_gates test_quality_procurement test_hazard_referral -q` | 193 tests, OK, 1 skipped, exit 0 (an injected-failure traceback is logged by an expected test) |
| `python3 -m unittest test_resident_decisions test_resident_documents test_resident_choice_queue -q` | 265 tests, OK, 93 skipped, exit 0 |
| `python3 -m unittest test_bulk_edits test_aftercare test_consultation_controls test_change_provenance -q` | 118 tests, OK, 16 skipped, exit 0 |
| `ruff check --no-cache .` | All checks passed, exit 0 |
| `ruff format --check --no-cache .` | 213 files already formatted |
| `mypy --cache-dir=<scratch>` (scratch venv) | Success, no issues in 266 source files, exit 0 |

Skips, not hidden: 91 `opt-in owned loopback SQL Server`, one `explicit
isolated synthetic Azure SQL database`, one `JSON file rollback only`; these
were not enabled. The SQLite-file `SqlFlows` and `SqlResidentDecisions` tests
ran as isolated local no-service tests and are not SQL Server parity.

### Classification

* `local observed` (core package level only): quality fail-closed, malformed-metadata and rule-provenance behavior; capacity Pass, Fail and Unknown; existing resident and authority refusals covered by the selected tests; ruff and mypy cleanliness.
* `implemented-unverified`: SQL Server and Azure SQL paths, API, agents and orchestrator suites, browser and accessibility harnesses, Docker, scanner and the FULL gate.
* `blocked`: the integrated-parent FULL gate is not admitted here; a later stack-tip full receipt counts only if canonical runner semantics and independent verification support the parent member.
* `unknown`: independent exact-head assessment, hosted checks, resident consent, named professional or legal approval, owner acceptance of draft and in-review documents.

### Exclusions

Unmerged child #86 behavior, any new feature or refactor, and any change to
other worktrees. No push, pull request, issue or project write or merge.

### Gaps, owners and resume conditions

| Gap | Owner | Resume condition |
| --- | --- | --- |
| Integrated FULL gate and receipt | Coordinator | Admission slot, clean frozen head, canonical runner and independent receipt verification |
| Child #86 retarget | Coordinator | Resume #86 in its original native session onto this exact parent branch; no silent retarget to main |
| Replacement route for in-progress quality records with missing evidence (original #1226 follow-up rank 1) | Quality owner and product owner | Owner decision on a manual route; not resolved here |
| Reviewer for exercise rule records stays unreviewed | Named human control owners | Approval is outside agent authority |
| Independent, hosted and human review | Owner and reviewers | After publication request |

### Recommendation and criteria

Recommendation: **continue**. The alignment lost no child content and the
no-service observations are consistent with the three PRs. No fix or pivot is
indicated by this checkpoint. The four issue #81 criteria and issue #440
acceptance are unchanged and remain unticked; this record establishes no
acceptance.

### Re-alignment addendum after #1245 (2026-11-07)

Refs #81 #440. Local re-alignment of the parent topic branch onto later
`origin/main`; this addendum does not change the section above, which stays
valid for its own base only. Original records:
[research](../../.copilot-tracking/research/2026-11-07/issue-81-realign-r2-research.md),
[plan](../../.copilot-tracking/plans/2026-11-07/issue-81-realign-r2-plan.md),
[critique](../../.copilot-tracking/plans/2026-11-07/issue-81-realign-r2-critique.md),
[changes](../../.copilot-tracking/changes/2026-11-07/issue-81-realign-r2-changes.md) and
[review](../../.copilot-tracking/reviews/2026-11-07/issue-81-realign-r2-review.md).

| Item | Value |
| --- | --- |
| Pinned `origin/main` (fetched again after Capstone Rubric Scorer run 42361331168 completed with success) | `0f420dc9514db22081cb48fa733267d9d33a0d24`; above the previous base it adds `0209b46bf` (#1241 checklist export), `add72cc90` (score), `312fa3dcc` (#1245 chat demo disclaimer) and `0f420dc95` (score-only) |
| Prior frozen head (local ref `refs/ama/issue81-r2-pre-realign`) | `c5edb320ad10d3d73bb985bfb82b2d0bee94381a`, tree `4f2a712c483112e1c6c5faf231591c1b24fac234` |
| Conflicts | None; `git merge-tree` dry run and the rebase were clean |
| Child commits after rebase | `cf9bf329e` (#1226), `eca6e1bbf` (#1228), `5f1bf0a42` (#1229); range-diff `=` for #1228 and #1229, and `!` for #1226 only by the context line of main's `from typing import Any` |

Preservation (local observed): 47 of 48 original child paths are identical in
mode and blob. The one difference is `quality.py`, and the full diff against
the prior head is exactly main's additive `typing.Any` import and
`checklist_rows()` helper (#1241), which reads only `CHECKLISTS` and does not
touch the fail-closed gate paths. Main's #1245 disclaimer, browser-check, UI
and log changes are present unmodified.

The 2026-11-06 FULL receipt (`g81-r15-1106`, head `c5edb320a`, base `56eec7369`,
status passed) is invalid for this base and is not reused. No FULL gate was run
for this head.

Actual local commands (scratch venv, `env -i`, no service switches, core and
agents installed non-editable with `--no-deps`; imports resolve first to the
worktree sources):

| Check | Result |
| --- | --- |
| core `test_gates test_quality_procurement test_hazard_referral` | 193 tests OK, 1 skipped |
| core `test_list_export` | 4 tests OK |
| core resident, bulk edit, aftercare, consultation and change-provenance suites | 383 tests OK, 109 skipped: 91 loopback SQL Server, 15 task-owned SQL Server, 1 Azure SQL, 1 JSON-only, 1 SQL writer dependency |
| core `ruff check`, `ruff format --check`, `mypy` (ruff 0.17.1, mypy 2.4.0) | passed; 213 files formatted; no issues in 266 files |
| api `test_chat_panel test_loading_feedback test_role_endpoint_inventory test_list_export_api test_form_staging_api test_finance_grants_screens` | 123 tests OK, 1 skipped (opt-in local Chromium) |

An earlier API run without `node` on the restricted `PATH` failed with 21
errors (`FileNotFoundError: node`); that was an invocation error and the
corrected run passed.

Classification: the above is `local observed` at package level. FULL gate,
browser harnesses, SQL Server and Azure paths, Docker, scanner, independent
exact-head review, hosted CI and resident, legal or human approval remain
`implemented-unverified`, `blocked` or `unknown`. Child #86 (PR #1243) is
excluded and untouched. Recommendation: **continue** to the coordinator's
combined-tip FULL gate. The four issue #81 criteria and issue #440 acceptance
remain unticked.

## Demo stabilization current-main checkpoint (2026-11-09, Refs #440 #123 #184 #136)

DRAFT, not approved. This documentation-only record pins current `main`, qualifies the governing documents, reads the demo path hop by hop from source, classifies the evidence and records three tiny current observations. It follows PR 1222 (merged 2026-11-09) and PR 1304 (merged 2026-11-09) and the #440 comment `6740015794` (2026-11-09T12:25:55Z). It changes no source, test, coordinator, workflow, infrastructure or approved document, and it writes to no issue, board, pull request or remote. The earlier sections above, every historical adverse record or grade and every previous acceptance tick are unchanged.

### Identities and triggers

| Item | Pinned value (read 2026-11-09) |
| --- | --- |
| `main` commit | `df8e858b2150198e5e22c73d224a0d3592c73daa`, tree `af1e9ea329f7ff5116c1279ab780ef649b1593cd` (rubric-bot commit; its only difference from the PR 1304 squash `23e944c1fccf0c4578e7beb0740ddd55c3f935b2` is `.github/rubric/scores/latest.json`) |
| PR 1222 | merged `d4d6827fe60be651cd922ab9656688c18c978e1d` at 09:12:23Z, head `5ecc1fe9dd214b8f2b8080f680f3f9d6d03842e5`; constructed-cohort paired-equity diagnostic only, `fairness_evidence=False`, `activation_allowed=False` per its body |
| PR 1304 | merged `23e944c1fccf0c4578e7beb0740ddd55c3f935b2` at 12:19:47Z, head `68fc3e61b187175e87bedd412a2b8d8c261be435`, tree `39e2a3f4b7599844e45fe7c441910ea6ff0d08f6`; 19 hosted check entries returned, counted from the status rollup and not individually re-read |
| Business requirements document | version 0.21.0, status draft, blob `34d88395de861e9799eb9e24121a21c92c7a5adc` |
| Product requirements document | version 0.21.0, status in-review, blob `c788b917bafaede215f326f0efc71e071a687f1c` |
| Case study and addendum | original `0aec2d8070117a647574b1fadc8cfbdd2af68598` (unchanged); addendum `28c1924285eed255e53c1e359e0ad98eedab1d22` (`ms.date` 2026-11-08) |
| Decision records | 0001 Proposed (`d42fa5c4`); 0002 Proposed with the owner-accepted staff identity decision of 2026-10-24 (`cbe21530`); 0003 Accepted with amendment 2026-10-15, Basic IoT Hub (`d6064537`); 0004 Accepted 2026-10-15 (`9406c2e7`); 0005 accepted for synthetic development only (`4d610335`); 0006 Accepted 2026-10-15 (`956da1a3`); 0007 Proposed, not accepted (`abb21088`) |

The local read-only ref `origin/pr1304` (`refs/pull/1304/head`) was fetched only to compare heads. The dirty primary checkout was not used.

### Requirement trace (document-qualified)

BRD and PRD functional requirement numbers collide, so each trace names its document. BRD FR-050 is opt-in staff memory and PRD FR-048 is offered against confirmed appointments; neither is sensor work.

| Concern | BRD (draft) | PRD (in-review) | Decision record |
| --- | --- | --- | --- |
| Consented in-use monitoring retained with source, mapping, calibration and time | FR-048, AC-090 | FR-050 with AC-066 to AC-068 | ADR 0003 decision 6 (IoT Hub is the ingestion product) |
| Sensor data or an absent flag is not acceptance evidence | RULE-014 | AC-067 (deterministic review signal only creates a human review task) | ADR 0005 synthetic development only |
| Real AI per record, proposed against reviewed, case access independent of model | FR-044, AC-084 | FR-044 | ADR 0004 option C staged (employee chat, not sensor Quality review) |

### Demo path read from source on `main`

| Hop | What main implements (source) | Not on main |
| --- | --- | --- |
| Simulator | One synthetic reading per home per 5-minute UTC slot, `live-sim-reading-v1`, `source_type=SYNTHETIC`, no AI. Control file `live-sim-control-v1` with owner, approval reference, `enabled`, hard `expires_at` (at most 14 days from start) and cohort 1 to 100; the Hub sink refuses without it and fails closed on stop, expiry or an unreadable file (`src/api/README.md:2025-2135`, `src/api/src/zava_forward/api/live_control.py:28-100`) | Deployed jobs, certificates, route, grants and quota are not verified; the authored Bicep jobs state they are not deployed (`infra/live-simulator-job.bicep`, `infra/live-receiver-job.bicep:34-36`: immutable `@sha256` image, scope guard, `routingReady` false by default) |
| Persistence | Receiver admission of `live-sim-reading-v1` in a 16-field closed shape (`src/core/src/zava_forward/core/sensor_consumer.py:431`), mapping interval, consent and window checks (`:603-611`), `observed_series` keeping the indoor `reading-v2` contract and excluding live rows (`:734`), and a sensor-only SQL connector with no DDL, seed or case write (`sensor_sql.py`) | A live end-to-end ingestion observation; live rows are not calibrated indoor evidence |
| Employee UI | No employee retained-value UI was identified in the inspected paths. A textual search of `src/api` finds sensor code only in control, ingestion, simulator, receiver, handover and the resident demo script, and no employee route, template or script reading retained live readings was identified | The retained-value employee view (owner #1288, unmerged). The textual search cannot exclude a differently named path, which remains unverified |
| Actual Quality model | The registered `quality-evidence` snapshot contains permitted document metadata, Quality records and checklists and no dedicated retained-sensor fields (`src/core/src/zava_forward/core/assistants.py:97-180`, caller `:504-509`); the assistant is proposal-only (`:47-56`); `src/core/README.md:1136-1178` states no new sensor AI task is authorised | Any sensor input to the real model (#1288) |
| Attributed flag | No sensor-attributed model flag was identified in the inspected paths; a differently named path remains unverified. The only sensor-derived human task identified is the deterministic review signal of PRD AC-067, which is not model output | A visible unapproved flag naming model, version and time (#1288) |
| Auth, tenant, admin | Staff access derives from an Entra principal in the configured tenant with assigned application roles (PRD FR-003; ADR 0002 owner decision). Authentication trusts the ingress-provided `X-MS-CLIENT-PRINCIPAL` header and validates no token signature (`src/api/src/zava_forward/api/auth.py:7-14`), so it is safe only when the service is reachable solely through the platform ingress; that deployment prerequisite is not observed here. Simulator administration is Azure RBAC on the share and job; the receiver and simulator use separate identities (`infra/live-receiver-job.bicep:9-10`) | The in-app simulator admin screen (`src/api/README.md:2107-2110`, owner #189) |
| Manual, failure, consent, approval | Stdout dry-run sink; fixed-code errors with no traceback or driver text; a missing certificate is non-retryable; stale, missing and unavailable states are explicit; resident consent is checked at admission; Quality acceptance stays a named human decision (#91 closed 2026-10-17) | Named human approvals for production, legal, security and cost remain with their owners |
| Package identity | The receiver image digest requirement and the case and measure identity on Quality records | Work-package identity is unknown: an image digest is not work-package identity and that path was not examined here |

### Evidence by class

| Class | Items |
| --- | --- |
| Local observed (this checkpoint) | Git identities and source equivalence; document blobs and statuses; the source reading above; the three test runs below |
| Local observed, historical | The retained 184 results below (source-equivalent, environment not re-proved) |
| Azure observed | None for sensors. The single generic employee chat model answer of 2026-11-08 (PR 1290) is not sensor or Quality evidence |
| Implemented, unverified | Simulator, control, receiver jobs, admission against a real Hub, sensor-only SQL grants, deployed jobs, resident own-home view freshness |
| Deferred | Production compliance, legal, security hardening, named approvals, live finite-cohort admission and model use |
| Blocked | Employee retained-value UI and Quality model input (#1288, unmerged), admin screen (#189), live transport prerequisites (#185, #140, #110) |
| Unknown | Deployment parity with main; certificates, route, quota and cost headroom; calibration and statistical validity; authentication of generator provenance; work-package identity |

### Retained 184 evidence and Git equivalence

`git diff --stat 68fc3e61b df8e858b2 -- src infra tools .github/workflows pyproject.toml` is empty, so the source tested in the 2026-11-09 #184 validation (head `68fc3e61`) is byte-identical to `main` for those paths. That proves which source ran; it does not make the logs, image or environment current. The following are therefore reused only as historical observed and are not rerun or relabelled here: owned disposable SQL default 70 and analysis 10 with zero skips; Core `sensor*` 192 OK with 11 offline opt-in skips; API `live*` 66 with 2 SQL-need skips, `iot*` 49 and `sensor*` 103; paired-equity 23; API mypy 0 errors in 199 files; Ruff exit 0; tools checks 102. Limits carried forward: the SQL image tag is mutable and only a contemporaneous digest and package hashes were recorded (not a hermetic attestation); some earlier piped producer exits were not individually captured; there is no executed-selector import trace; the original failing logs were overwritten by reruns; one send-rate timing assertion failed once then passed with the cause unproven; the original mypy 53 errors in 48 files came from a missing playwright 1.64.0; the carried Low items (exact-grant receiver main, rejected data quality, replay SQL coverage) remain open. Mock, skip and merge counts are not live acceptance.

### Current observations (this checkpoint)

Commands ran at `df8e858b2` on Python 3.12.3 in an isolated virtual environment with editable installs of this worktree's `src/core`, `src/agents` and `src/api`, because the existing editable installs pointed at another checkout. Logs are outside the repository in `/home/azureuser/source/ama-demo-wt/logs-440-1109/` and are not committed. Two first attempts failed on harness imports only (producer exit 1: `core-sensor-consumer-live.log` sha256 prefix `d008abcd`, missing `sensor_consumer_fixture`; `api-assistants.log` prefix `f64dd5cf`, missing `test_mvp`) because the tests directory was not on `PYTHONPATH`. They are retained unchanged and are not product failures.

| Command (working directory) | Producer exit | Result |
| --- | --- | --- |
| `python -m unittest -v tests.test_live_control tests.test_live_simulator` (`src/api`, `PYTHONPATH=../core/tests:../agents/tests`), log prefix `07930eca` | 0 | 64 tests OK, 0 skips |
| `PYTHONPATH=tests python -m unittest -v tests.test_sensor_consumer_live` (`src/core`), log prefix `c8afc350` | 0 | 10 tests OK, 0 skips |
| `PYTHONPATH=../core/tests:../agents/tests:tests python -m unittest -v tests.test_assistants` (`src/api`), log prefix `43a33be0` | 0 | 120 tests, 58 skipped ("needs disposable SQL Server"), 62 ran OK |

These runs show control fail-closed logic, simulator mechanics, live-envelope admission on fixtures and assistant contract mechanics at this exact tree. They do not show SQL behavior (not run, to avoid the resource owned by #1292), a live Hub send, the employee UI, a real model call or any acceptance. The 58 skipped assistant tests are not SQL evidence. The selected tests did not exercise the full sensor-to-Quality-model journey; no sensor Quality test was identified in the inspected paths. No full gate, browser, Azure, model or job run was made.

### Exclusions

Unmerged and excluded functionality, reported by the coordinator from the 2026-11-09 briefs and not observed here: #1288 E3 (from `89a7a45b`), #1292 E1 (from `384d149a`), #144 new head (from `d2d95606`), #189, #1295 (published head `0bcf55da`) and #1296 (frozen `52e44a70`). The #1296 High-profile validation outcome REVISE, eleven of 27 matches, is an adverse result for an unmerged candidate policy. It is not a current-main pass, not native validation and not a reason to change the coordinator in this task. MainIoT PR 1304 source is implemented; it is not an accepted, fully actual-model-grounded demo.

### Findings, owners and gates

No new defect was reproduced, so no issue is proposed and no code fix is made. If one were confirmed, this record would need its reproduction, severity, minimum fix, test and requirement dependencies. The #184 body text reported stale by the audit ("not started", "no Hub module") was not re-verified here. Gaps are assigned to existing owners and not duplicated: persistence to employee UI to Quality model to attributed flag (#1288); admin surface (#189); provisioning and credentials (#185, #140); live receiver ingestion (#110, #188); persistence ordering (#1292, #81 via PR 1240); worker and queue (#144 via PR 1141); skip contract (#1297); per-call chat activation (#891); architecture deck (#1295). Closure of #184, #185, #188, #110, #189 and #136, the parent #123, and the #440 triage and HVE Builder behavior-change independent-review criteria stay unproven. Nothing is ticked or closed, and the previous #440 first-checkpoint tick is preserved.

### Recommendation and resume conditions

Proposed bounded CONTINUE through the existing owners and HOLD on every closure claim. No pivot, deferral or relaxation is inferred or granted. The lanes #189 source, #1292, #144, #1295 and #1296 continue independently. Dependent expansion of the Quality sensor path resumes only when all of these hold: (1) #1288 is merged on `main` and independently assessed at its exact head; (2) the dedicated synthetic source is authenticated without inferring from `SYN-` ids or labels; (3) finite admission names the owner, cohort of at most 100, duration, call and token ceilings and cost headroom; (4) certificates, route and grants are verified by an authorised operator; (5) one retained observation shows identical reading ids and values in the employee view and snapshot, a privacy-compatible traceable link to the provider request (no raw values in logs, per PRD AC-067), and a visible unapproved flag with model, version and time.

Limits: this is a single-session, authored record with no independent exact-head review, no hosted CI observation for the commit that carries it and no live check. Coordinator-reported items are labelled as such.

### Qualification C1 (2026-11-09, Refs #440)

An independent readiness review of the candidate head `df4252e7` (verdict approve with comments, no High, two Medium) found that the Employee UI, attributed flag and no-test statements above had been stated more categorically than the bounded inspected paths support. They are qualified in place to the inspected scope, and the superseded wording is retained in the git history of `df4252e7` and in the original tracking records. No contrary runtime implementation or bug is established.

* Superseded scope: "None" for the employee UI, "None for sensors" for the attributed flag, "Quality records and checklists only" for the model snapshot and "no such path exists" for tests. The wording now reads: no employee retained-value UI or sensor-attributed model flag was identified in the inspected paths and a differently named path remains unverified; the registered quality-evidence snapshot contains permitted document metadata, Quality records and checklists but no dedicated retained-sensor fields; the selected tests did not exercise the full sensor-to-Quality-model journey.
* The dated observation remains an observation of `df8e858b2` and is not rewritten. Later `main` additions (for example `4fcd1934f`, `ad679b96b` and `daf45a46c`) are not freshly observed by this historical record.
* No approval, tick, closure, live, model, SQL or hosted evidence is added. BRD, PRD and decision record statuses are unchanged. This is correction cycle 1 of 5 for this candidate; no earlier review-correction cycle is recorded in the original records.

## SQL feature-recovery wave current-main checkpoint (2026-11-09, Refs #440)

DRAFT, not approved. This documentation-only record follows the merge of PR 1308, the completed SQL feature-recovery wave for #1292 (traceability references #81 and #440). It pins `main`, proves which source the retained real-SQL results ran, classifies current, historical and hosted evidence separately, records fresh targeted local observations of the current tree, compares findings with existing owners and bounds the recommendation. It changes no source, test, coordinator, workflow, infrastructure, tool or approved document and writes to no issue, board, pull request or remote. Every earlier section, the earlier checkpoints, the old merged #440 branch, `b270` and DF8 records and every historical adverse record are unchanged. A source SQL merge is not full demo acceptance.

### Identities and trigger

| Item | Pinned value (read 2026-11-09) |
| --- | --- |
| Working base | `main` `8d6f029cac004506953f36606862168bbe9d9412`, tree `4f3a11a1a42615de66d2e5fe1799a08867ad31c1`, the PR 1308 squash |
| Later `origin/main` | `ef28d4da42d83b111d48f14df9b70e3c4932a477` at 15:47Z, a rubric-bot commit whose only change from the working base is `.github/rubric/scores/latest.json`; the candidate stays on the working base |
| PR 1308 | `fix(core): preserve priority ordering and serialize SQL index bootstrap`, merged 2026-11-09T15:30:40Z, head `6ded235e2a7b8ca36edc4414bcd903be8690d4e3`, head tree `02c1a813cd73a3d29b62f0ce1a1143637d2bc5f1`, squash parent `ba5cc74b8b717957b046fd1d28804a989a7f3dd7` (rubric bot, previous checkpoint PR 1309 at `9f9aacc8b`), 311 changed paths, 12 source paths |
| Hosted checks on the PR head | 19 rollup entries: 18 check runs COMPLETED SUCCESS (15:14:19Z to 15:26:06Z, including `src-core`, `src-api`, `src-agents`, `src-orchestrator`, `src-importer`, `src-namespace`, `mssql`) and the commit status `rubric/score` success (15:21:15Z). Workflow runs `42642580079` (Source projects CI) and `42642580067` (Capstone Rubric Scorer) |
| Hosted checks on the squash | Source projects CI runs on `pull_request` and `workflow_dispatch` only (`.github/workflows/src-ci.yml:3-6`), so a push to `main` has no Source run. The squash has run `42645390735` (rubric scorer, push, success at the later read) and `42645402788` (graph update, success). That is not source CI for the squash |
| Previous pin | `df8e858b2` (see the earlier checkpoint); main since then also gained `4fcd1934f` (#1141 queue adapter, Refs #144), `ad679b96b` (#1295), `06e3f2f45`, `daf45a46c` (paper), `9f9aacc8b` (PR 1309, the previous checkpoint). Those are present on main and are not examined here |
| Documents | BRD 0.21.0 `draft` blob `34d88395de861e9799eb9e24121a21c92c7a5adc`; PRD 0.21.0 `in-review` blob `c788b917bafaede215f326f0efc71e071a687f1c`; ADR 0001 Proposed (`d42fa5c4`), 0002 (`cbe21530`, owner-accepted staff identity decision 2026-10-24), 0003 (`d6064539`), 0004 (`9406c2e7`), 0005 (`4d610335`), 0006 (`956da1a3`), 0007 Proposed (`abb21088`); case study original `0aec2d80`, addendum `28c19242`. All blobs equal the previous pin; no approval is added |

The trigger is the coordinator brief of 2026-11-09 after the merge. The latest #440 comment read is `6740015794` (2026-11-09T12:25:55Z); no newer comment exists. The coordinator's "all 19 hosted checks green" is confirmed here as 18 successful check runs plus one successful status.

### Source equivalence (Git, read-only)

| Command | Result |
| --- | --- |
| `git diff --stat 6ded235e2 8d6f029ca -- src infra tools .github/workflows pyproject.toml` | empty: the hosted PR head source equals main for those paths |
| `git diff --stat 31464e65c 8d6f029ca -- src/core/src src/api/src` | empty: the production source at the E2 real-SQL frozen head equals main |
| `git diff 31464e65c 6ded235e2 -- src/core/tests/test_priority_order.py` | 3 insertions and 1 deletion: the fake MSSQL driver in the `MssqlBeginRecovery` fixture became a `types.ModuleType`, a non-SQL fixture |
| `sha256sum` of `sqlstore.py` and `mssqlstore.py` at `8d6f029ca` | `0b0caf62802d...` and `1825dc5f2c6d...`, equal to the import provenance recorded by the final real-SQL run |

This proves which production source the retained SQL runs imported; it does not make their environment, logs or image current, and the changed test line and the tests, README and test guard are not claimed identical to the SQL-run tree beyond the commands above.

### Requirement trace (document-qualified)

| Concern | Source |
| --- | --- |
| Stock Prioritisation recommendation is advice for human review, no consequential ranking change | original case study Stock Prioritisation L2 and draft PRD `PR-007`, as cited by the #1292 issue body (attributed to the issue, not re-searched in the PRD here) |
| An unconfirmed-order recommendation needs a named data owner before action; accept stays a named human decision | `src/core/src/zava_forward/core/store.py:939-947` (`ORDER_NOTE`, `_order_unresolved`), accept or edit raises `PermissionError(ORDER_NOTE)` at `store.py:1060`, reject and ordinary case controls stay available |
| Real AI per record is proposed against reviewed, with a labelled rule fallback | BRD FR-044 and PRD FR-044 (as traced in the previous checkpoint); the priority panel labels "Written by AI" or "Written by rules" with the fallback reason (`src/api/src/zava_forward/api/web/app.js:694`) |

BRD and PRD functional requirement numbers collide in this repository, so each trace names its document. The PRD `PR-007` identifier is attributed to the #1292 issue body.

### SQL wave behavior read from source (at `8d6f029ca`)

| Behavior | Where (source) | Not shown here |
| --- | --- | --- |
| Immutable creation ordinal, zero ordinals repaired under the write section and never cached; legacy heuristic ordinals assessed once, the newest record of an employee not provably latest flagged `order_confirmed=False`, not actionable | `sqlstore.py:350-393`, `595-`; `store.py:939-947`, `1035` | Behavior on a deployed or private database; deployment parity |
| SQL Server: `created_ord BIGINT NOT NULL DEFAULT 0`, ordinal indexes, `_abandon_partial_begin` rolls back or discards the connection when BEGIN fails mid-way | `mssqlstore.py:46`, `181`, `199`, `314` | Lock duration at scale and Azure SQL behavior |
| Index bootstrap serialized under the write transaction (fix for the reproduced `ix_recs_seq` race) | `mssqlstore.py:323` (check-then-create index statements under the write lock) | Production concurrency |
| Committed or uncertain creation maps to HTTP 409 `outcome=committed`; the UI latches `pending` and `checkHistory`, hides the repeat control and shows a status note | `server.py:1242-1268`; `app.js:677-681`, `689`, `695-707` | A rendered browser observation in this checkpoint |

Mocks, rules and fixtures are not actual AI: the SQL-wave tests use a database and fakes, and no provider answer is observed or claimed. The UI states whether the order was written by AI or by rules at runtime; which applies on a deployed service is unknown here.

Qualified 2026-11-09 (C2): the last row's "Committed or uncertain" wording is narrowed; see Q1 in the C2 qualification below. The row is kept as originally written.

### Evidence by class

| Class | Items |
| --- | --- |
| Local observed (this checkpoint, current tree `8d6f029ca`) | Git identities and equivalence; three Core and API unit selections below with import origins |
| Local observed, historical (source-equivalent, environment not re-proved) | Real SQL Server 2022 (16.0.4305.5 RTM-CU27-GDR, image `sha256:cf8f0ab2ebe6...`, one nonqueued `flock -n` on the shared heavy lock): `test_priority_order` 142 OK with no skip in 536.659s (`e2-sql-admission2-140248-2867281`, head `a20472734`, stderr sha256 prefix `8093a31f`); `MssqlResidentControls` 91 OK with 1 pre-existing skip (`e2-sql-admission-134433-2845787`, head `fa74e8ed4`, `848b671c`; the same suite at `e1-sql-admission2-132322-2818937` also 91 OK, `e9321001`). The tested `mssqlstore.py` is byte-identical |
| Retained adverse (kept, external raw files) | E1 unskipped out-of-tree rerun FAIL, `ix_recs_seq` already exists (`r2repro`, exit 1, `910cee9a`); first E2 priority run exit 1, 142 tests FAILED errors=1, `_Cursor` not iterable (`f576b906`) |
| Hosted observed (PR head `6ded235e2`, source-equivalent to main) | `src-core` 2594 tests OK, 301 skips; `mssql` job `Ran 306 tests in 339.301s`, `OK (skipped=1)`; the other named checks success. The `mssql` job selects `test_mssqlstore`, `test_lawstore.MssqlStoreTests`, the five `test_assistants.Mssql*` classes and `test_resident_aoai_sql.AccountingSqlTests` (`.github/workflows/src-ci.yml:326-`) |
| Author-reported, not reproduced here | E4 priority suite 142 with 65 opt-in skips, Core mypy 275 files, lint and the DOM history harness; independent Functional approve with zero findings on the 13 E4 incremental paths (earlier assessments requested changes, see below) |
| Implemented, unverified | SQL index bootstrap, ordinal repair and BEGIN recovery on a deployed or Azure SQL database; lock duration at scale; the committed-creation UI in a rendered browser at this tree |
| Deferred | Production compliance, legal and security hardening, WORM and migration approvals, live model use, named approvals |
| Blocked | Unmerged #1288, #189, #1258, #1259, #136 and #1298 functionality (excluded) |
| Unknown | Deployed service parity with main, real-provider behavior of the priority suggestion, and the named data owner process for unresolved-order records |

Hosted limit found in the log and workflow: no test named for priority appears in the hosted `mssql` job selection or output, and the priority real-SQL tests need a task-owned manifest (`ZF_SQL_TASK_MANIFEST`, `src/core/tests/sqlguard.py`). No hosted check executing `test_priority_order` on SQL Server was identified in the inspected workflow selection and job log. The real-SQL evidence for the new suite is therefore the retained local record only. The hosted log also prints `Stock/technical SQL recovery failed` tracebacks that are injected-fault test output inside a run that reported OK, not a failed check. Whether `src-core` discovery includes the priority file was not read from the per-test list and remains unverified.

### Current observations (this checkpoint)

Commands ran at `8d6f029ca` on Python 3.12.3 in an owned virtual environment created with `mktemp -d` and editable installs of this worktree's `src/core`, `src/agents` and `src/api`, with `ZF_TEST_MSSQL` and `ZF_SQL_TASK_MANIFEST` unset and no Azure, model, credential or private input. Import origins (log prefix `e15167d5`): the three `zava_forward` packages are namespace packages (`__file__` is `None`); their `__path__` entries and `sqlstore`, `mssqlstore`, `server` and `queue_azure` module files are under this worktree; the SQL driver `mssql_python` resolves to the owned venv. Logs are outside the repository in `/home/azureuser/source/ama-demo-wt/logs-440-sqlwave/` and are not committed.

| Command (working directory) | Producer exit | Result |
| --- | --- | --- |
| `PYTHONPATH=tests python -m unittest -v tests.test_priority_order tests.test_resident_decisions tests.test_sqlstore tests.test_journey_store` (`src/core`), first run, log prefix `f3b54e83` | 1 | 421 tests, 1 failure, 158 skipped: `SqliteLegacyEdges.test_large_legacy_backfill_is_linear_and_survives_concurrent_openers`, `AssertionError: [OperationalError('database is locked')] != []` (`test_priority_order.py:734`). Retained unchanged. It ran at the same time as the API selection on a host at load average 5.4 |
| Same test alone, three runs (`core-sqlite-concurrent-r1..r3`, prefixes `7c26c5be`, `67834eb7`, `e70288eb`) | 0, 0, 0 | 1 test OK each |
| Same four-module command, serial rerun, log prefix `3413ad0c` | 0 | 421 tests OK, 158 skipped (156 "opt-in owned loopback SQL Server", 1 "JSON file rollback only", 1 "Explicit isolated synthetic Azure SQL database required"); `test_priority_order` 77 OK and 65 skipped, matching the 142 reported in the PR 1308 body |
| `PYTHONPATH=../core/tests:../agents/tests:tests python -m unittest -v tests.test_case_journey tests.test_auth tests.test_entra_authoritative tests.test_role_endpoint_inventory tests.test_role_matrix tests.test_assistants` (`src/api`), log prefix `8f630cfb` | 0 | 263 tests OK, 58 skipped ("needs disposable SQL Server (ZF_TEST_MSSQL=1)"); `test_case_journey` 31 OK |

These runs show, at this exact tree, priority-order, resident-decision, store and journey mechanics on SQLite and fakes, the ingress-principal auth and role-matrix contracts, and the case-journey and assistant contract mechanics. They do not show SQL Server behavior: all 156 SQL-class skips and the 58 API skips are not SQL evidence, and no SQL admission was made because the production SQL source is byte-equal to the retained real-SQL runs and a missing or busy admission would only block a SQL row. They do not show a browser rendering, a live or model call, or any acceptance. No full gate, browser, Azure, provider, job or private-data run was made.

### Findings, owners and gates

| Finding | Severity and status | Existing owner and handling |
| --- | --- | --- |
| F1 Hosted CI does not execute the new priority real-SQL suite; its evidence is local and historical | Medium, gap, not a defect in behavior | #1292 criterion 3 (task-owned SQL, zero skips) and the open #1297 (skip and dispatch contract, sensor scope, adjacent not identical). No new issue; the owners decide whether a hosted or admitted rerun is required |
| F2 One SQLite concurrent-opener test failed once ("database is locked") under parallel local load and passed four times in isolation or serial | Low, unproven cause: the store sets `PRAGMA busy_timeout=5000` (`sqlstore.py:224`, `258`) and the test also asserts under 20s | Existing #1292 test. A load-sensitive timing assertion is suspected, not shown. No fix or issue here; recorded so a recurrence on hosted or local runs is recognised |
| F3 #1292 stays OPEN with its criteria unticked (read 2026-11-09, last updated 10:33Z); PR 1308 used `Refs` | Status | Merge is not closure. The independent history is retained: C2 requested changes (5 High, 4 Medium, 2026-11-08T21:57Z), C4 Revise (1 High, 11 Medium, 2026-11-08T23:29Z), `384d149ab` requested changes (1 High, 1 Medium, 2026-11-09T10:33Z) |
| F4 No new defect reproduced, no source change proposed | n/a | If one were confirmed this record would need its reproduction, severity, minimum fix, test and requirement dependencies |

The negative statements above are limited to the inspected paths: the workflow selection, the `mssql` job log, the Core and API test selections named here and the source files cited. A differently named path remains unverified.

### Exclusions

Unmerged and excluded: #1288, #189, #1258, #1259, #136 and #1298 functionality; any actual provider, dataset or private captured-readings path; WORM, migration and legal approval. Their heads and outcomes were not observed here. #1141 and #1295 are merged and present on main but are not examined.

### Recommendation and resume conditions

Proposed bounded CONTINUE through the existing owners with a HOLD on every closure claim. No fix, pivot, deferral or policy relaxation is inferred or granted; a bounded fix is proposed only if an owner confirms F1 or recurrence of F2 as a defect. Affected closure that stays unproven: #1292, the #81 epic and its #1240 integration, the #440 triage and HVE Builder behavior-change criteria, and the parent epic #123. Nothing is ticked or closed.

Dependent expansion that relies on the SQL ordering wave (for example the #1240 lifecycle integration evidence) resumes when all hold: (1) an independent exact-head assessment of this record exists; (2) the owners decide whether hosted or one nonqueued owned SQL admission must execute `test_priority_order` for the current main, and any such run records exits, counts, skips and the source identity; (3) F2 is diagnosed or its recurrence is accepted by the owner; (4) the named data-owner confirmation of unresolved-order records is shown to exist as a process; (5) deployed parity and a rendered browser observation of the committed-creation notice are obtained under the existing cost and release controls.

Limits: single-session authored record with no independent exact-head review and no hosted CI for the commit that carries it; the hosted state for the squash was read at 15:47Z; author-reported items are labelled; the check count came from the status rollup and the commit status API.

### C2 qualification, 2026-11-09

Dated qualification of the section above after an independent PARTIAL Readiness assessment (one Medium, one Low finding; not a full publication clearance). The original table row, the original authored Review and the F2 finding text are kept unchanged; this subsection narrows them. No source, test or policy changed, no test was repeated, and the statements below are source reads or coordinator-reported facts, not browser, SQL or hosted observations.

| Id | Qualification | Evidence |
| --- | --- | --- |
| Q1 | The creation row in the SQL wave behavior table said "Committed or uncertain creation maps to HTTP 409 `outcome=committed`". Only a `CommittedReloadError`, a write that committed whose reload afterwards did not settle, is mapped to HTTP 409 with `outcome=committed`; a successful creation returns 200. An uncertain outcome or a transport failure is a different path: the UI treats `outcome` committed, `outcome` uncertain or an error without a `status` as needing history reconciliation, latches that state in the current panel instance and hides the repeat control. That state does not prove that a write committed or that any HTTP status was returned. | `server.py:1242-1246` (also `1265-1268` for resolve); `sqlstore.py:156-159`; `app.js:38-40`, `724-730` |
| Q2 | The original Review R3 says "one occurrence in four runs". The retained records show five executions of the affected SQLite concurrent-opener test: the first Core selection failed (exit 1, 421 tests, one "database is locked" failure), then three isolated runs and the serial Core selection (exit 0, 421 tests) passed. That is one failure in five executions followed by four passes. The failed assertion was the errors-list assertion at `test_priority_order.py:734`, not the elapsed-time assertion at 735. Cause UNKNOWN; not classified as a flake or a defect; no waiver of the failure. | Retained external logs named in the Current observations section; test file lines 734 and 735 |
| Q3 | A later, separate #1292 diagnosis at frozen head `59accfa1ca9be77f2e98faf5ef862deba76cf941` (base `ef28d4da4`, documentation records only) ran the same test six times (three plain, three observer-instrumented, about 15 to 16 s each) with 0 of 6 reproductions. Its observational timing hypothesis, a write-lock hold of about 3.05 to 3.25 s against a 5.0 s wait, is consistent with a load-sensitive failure but is NOT confirmed or reproduced. It neither explains nor relabels the earlier failure, implies no fix, and gives no basis to close F2, #1292 or any criterion. | Coordinator-reported from the diagnosis handoff (raw logs outside this repository, not re-read here) |

The F2 owner handling, F1 and the resume conditions above are unchanged. Hold on closure for #1292, #81, #1240, #440 and #123 remains. Not claimed: approval, closure, independent exact-head review or hosted CI for this commit, whole #440, #1292 or #81 acceptance, live SQL, Azure or AI evidence.

### Current-main preparation, 2026-11-09 (Refs #440 #81)

Source-preserving preparation, not a new correction cycle and not a new checkpoint. Prospective records:
[research](../../.copilot-tracking/research/2026-11-09-sql-wave-checkpoint-440-mainprep-research.md),
[plan](../../.copilot-tracking/plans/2026-11-09-sql-wave-checkpoint-440-mainprep-plan.md) and
[critique](../../.copilot-tracking/plans/2026-11-09-sql-wave-checkpoint-440-mainprep-critique.md).

| Item | Value (read 2026-11-09) |
| --- | --- |
| Observed SQL-wave source (unchanged) | `8d6f029cac004506953f36606862168bbe9d9412`, the PR 1308 squash; every observation above still refers to it |
| Current base merged locally | `main` `3a9767d5cf728c5e3be76813ce0bfdac4c06841e`, tree `d5b8e46c4931e729bdd04ef5701be5da32e46c2e`, the PR 1240 squash (merged 2026-11-09T16:50:00Z, head `ccc7358dad0628a660b76b1feb4e3a3556cc952c`, 19 of 19 status entries SUCCESS read with `gh`) |
| Main delta since the observed source | 225 paths: 12 in `src/core` (source, tests, README), `tools/rpi-checks.py` with its test (#1312 at `1464b4d85`), the rubric score, the pack and tracking records |

Main `3a9767d5c` includes controlled lifecycle source (gates, quality, procurement, appointments, store, resident decisions, complaints route) that this SQL-wave record did not observe. This record does not retest or accept it, and its hosted result for #1240 is not evidence for the SQL-wave observations. Whole #81 and #440 stay open. The merge kept both main's new pack sections and every earlier SQL-wave and C2 line; no source file was edited.

Next lifecycle-wave checkpoint trigger: an owner-selected, bounded integrated checkpoint of main at or after `3a9767d5c` with new evidence (targeted local results, hosted state of the exact head and the resident-decision and gate behavior on SQL where the owner requires it). Until it exists, the resume condition above that depends on the #1240 lifecycle integration evidence is not met, and closure of #81, #1240, #1292, #440 and #123 stays on hold. This note is the hold and resume point, not a completed checkpoint. Independent #189, #954 and #159 source work may proceed. No legal, resident or production approval is implied.

### Original-load #1292 diagnostic and record qualification, 2026-11-09 (Refs #1292)

Bounded additive note. A second unchanged-source diagnosis (frozen head `f1f73d23f269415f74427350ec7018c234ee799b`, historical diagnosis source `8d6f029ca`, documentation records only) ran two original paired selections (API six modules with Core four modules, concurrently): P1 plain and P2 with an observer on Core only. 0 of 2 pairs reproduced `database is locked`, so the cause stays UNKNOWN. It supports no flake, waiver, load-necessity, load-sufficiency, source-fix or acceptance claim. Records: [changes](../../.copilot-tracking/changes/2026-11-09-issue1292-original-load-diagnostic-changes.md), [review](../../.copilot-tracking/reviews/2026-11-09-issue1292-original-load-diagnostic-review.md) and the dated [record qualification](../../.copilot-tracking/changes/2026-11-09-issue1292-record-qualification-changes.md) with its [plan](../../.copilot-tracking/plans/2026-11-09-issue1292-record-qualification-plan.md) and [review](../../.copilot-tracking/reviews/2026-11-09-issue1292-record-qualification-review.md).

| Id | Qualification | Evidence |
| --- | --- | --- |
| N1 | The observer run supports only no reported harness error and no observed new error. Its recorder has unguarded enter and exit appends and suppressed trace-callback and reporting failures, so universal harmlessness and exhaustive reporting are unproven. The primary guarded `open_store` capture is distinct. This does not explain the original plain failure. | `observer_core.py` lines 34-132, outside this repository |
| N2 | The earlier 120.4, 174.9, 115.9 and 145.6 s figures are unittest durations. Process wallclock from the `.meta` epochs is 121.756, 177.081, 117.147 and 147.510 s; API nearly fully overlapped Core. All are far below the 420 s cap. | `.meta` files, outside this repository |
| N3 | The external log manifest lists 26 members plus itself (27 entries); its digest `634ceca206c1a077e57cb8d421e2d5e9f63d30ad495cd2af8c7918e0f91566de` is valid and no evidence was removed. | `SHA256SUMS`, outside this repository |
| N4 | The design allowed the observer pair after a plain PASS or REPRODUCED (disclosed partial disposition); the actual P1 was PASS and the REPRODUCED branch was not exercised. | plan P4, `driver.sh` |

Counts are not aggregated: the original series of one failure among five total executions, with the initial failure followed by four passes, the 0 of 6 earlier attempts (Q3 above) and this 0 of 2 pairs are separate denominators. The qualification addresses current claims only; it does not state the older records were accurate, authorizes no past amendment and does not authorize E5. The merged source equals main `2b6d80a25` (lifecycle source `3a9767d5c`); nothing was retested or accepted. All whole-issue #1292 criteria remain unticked and open. Not claimed: independent exact-head review of this commit, hosted CI, SQL, browser or cloud evidence, a full gate or approval.

### Current-main priority SQL regression validation, 2026-11-09 (Refs #1292)

Bounded, validation-only record on pinned `main` `ba71894bb1a94d6a24aabf9828312668f88f3ff5` (tree `83ab51163dd0d24f6a48ea1a329b1693881e8f38`; `src` tree `86bc00e19a167e517ae2955ad88d6e2f7b4eac26`, identical at the executed tracking-only commit `e208748cf`). It is the due earlier lifecycle and priority current-source SQL checkpoint; the controls and photo records (#1322) do not satisfy it. PR #1308 (`8d6f029ca`, merged 2026-11-09) is an ancestor and current main orders reloads by `created_ord`. Planning records were committed before execution; one independent critique (Revise) was applied before any SQL ran.

One non-queued shared-heavy admission, one disposable SQL Server 2022 container (16.0.4305.5, image `sha256:cf8f0ab2ebe6...1718`, loopback only, removed afterwards, no leftover database), `mssql-python` 1.15.0, Python 3.12.3, own environment with imports verified under this worktree's `src` (blobs `sqlstore.py` `89f409ee0`, `mssqlstore.py` `c712ad4a8`).

| Id | Process | Selection | Result |
| --- | --- | --- | --- |
| V1 | A | `test_priority_order`: JSON, SQLite and guard classes plus `MssqlPriorityOrder`, `MssqlLegacyMetadata`, `MssqlLegacyEdges`, `MssqlLockTimeoutBegin`, `MssqlBeginRecovery` | 108 ran, 108 ok, 0 skips, exit 0, 309.4 s, 31 on SQL Server |
| V2 | B | `MssqlC3Corrections`, `MssqlC4Corrections` | 34 ran, 34 ok, 0 skips, exit 0, 201.2 s, 34 on SQL Server |
| V3 | C | the two original `MssqlResidentControls` methods (`test_challenge_source_exact_dependency_manifest_and_original_reviews`, `test_failed_priority_accept_edit_remove_disposition_and_audit`) with SQLite and in-memory parity | 6 ran, 6 ok, 0 skips, exit 0, 10.4 s, 2 on SQL Server |

Totals: 3 processes, 148 tests, 0 skips, 0 failures, 67 on SQL Server, 540 s campaign. A plus B equal the full 142-test module once (split by class only to stay under the 600 s per-process bound; earlier full runs took 536.7 s and 558.0 s). Raw outputs are external with a 30-member `SHA256SUMS` (digest `b6cec06e5c4075e5271747f188078a30e49e169255a7810a350475fc57798bc0`).

Separate statements: source fulfillment, current observed behavior and root cause are not merged. At the pinned source, the selected existing tests passed once on SQL Server. This does not show the original unordered defect is absent from pre-fix source (the fails-against-old-behavior half of the third criterion is not re-proved here), and it does not explain, fix or retire the unknown historical startup failure, which remains UNKNOWN with the earlier 0 of 6, 0 of 2 and one-in-five denominators unaggregated. No whole-SQL acceptance, full-gate waiver, hosted CI, independent review, scale or lock-duration, Azure or live evidence, resident or professional approval, source correction or E5 is claimed or consumed. All whole-issue #1292, #81 and #440 criteria remain unticked and open. Records: `.copilot-tracking/{research,plans,details,changes,reviews}/2026-11-09-priority-sql-main-1292-*` and the state file.

Current-target binding, 2026-11-09 (Git, read-only, no SQL run). The campaign above executed at planning commit `e208748cf` on source tree `86bc00e19a167e517ae2955ad88d6e2f7b4eac26` (pinned base `ba71894bb`). Current `main` `1a84b3b0054990262a0df0625d95e3f545d2739a` (merged PR 1322 plus a rubric score commit) has the same `src` tree and the same `tools` (`74ad3cb586db...`), `infra` (`b0969f8b7b8c...`) and `.github/workflows` (`29eb03ea759e...`) trees; the only non-documentation path that moved is `.github/rubric/scores/latest.json`. The 148 tests, 67 on SQL Server, 0 skips and one 540 s admission therefore remain the evidence for the unchanged source, and no ceremonial SQL rerun is made or implied. The main-side controls checkpoint (its 13 and 83 browser observations) and the #1314 count qualification stay the historical dated records main published, not fresh claims here. This candidate was brought to main by an ordinary merge, keeping both sides' sections, index paragraphs and log entries; one block order was moved in a separate commit to keep this subsection under its original parent heading. Unchanged limits: the historical startup cause stays unknown, the old-behavior-fails half of AC3 stays unproven, and there is no full-gate, Azure, live, human, whole-#81 or whole-#440 acceptance; no criterion is ticked or closed and E5 stays unspent.

Qualification Q1, 2026-11-09 (documentation only, no SQL rerun, from the same-reviewer assessment of `6c05b1e12`: approve with comments, one Medium; [research](../../.copilot-tracking/research/2026-11-09-priority-sql-q1-1292-research.md), [critique](../../.copilot-tracking/plans/2026-11-09-priority-sql-q1-1292-critique.md)). The original claim above and in the earlier critique and plan that the external verifier covers cleanup and leftovers is kept as originally authored and is not retrospectively blessed. Correct attribution: `verify-1292-cm.py` gates test outcomes only (exits, totals, `OK`, skips, SQL counts); it prints cleanup and leftovers but does not fail on missing or failed cleanup. Cleanup was observed separately in the successful run: `container-id.txt` and `container-cleanup.txt` hold the same container id, `leftover-databases.txt` is empty (captured output only, because the script did not keep the query exit status), and the executing session reported an empty `docker ps -a` afterwards (stated in the changes record, not a retained receipt). The seven critique dispositions C1 to C7 marked Applied describe changes made before the run, not proof of universal guarantees. Limit on C4 (deadlines): the per-process intervals were 311, 201 and 11 s (unittest 309.366, 201.206 and 10.367 s) and the campaign 540 s, all inside the 600 and 1200 s bounds, but no timeout-path receipt exists and the post-timeout output-thread joins can add up to 5 s each, so a universal hard bound is not shown. Limit on C5 (local-only admission): the precheck tested `DOCKER_HOST`, the context name and the local tag image id `sha256:cf8f0ab2ebe6...1718`, and the run used the tag with `--pull=never` rather than the immutable id; no daemon endpoint inspection was retained, so neither an immutable runtime image nor endpoint authentication is claimed. The observed versions, tag, image id and the 67 passing SQL Server tests stay as recorded. No new defect or fix is asserted; the startup cause stays unknown and no criterion is ticked.

### Comparison count qualification, 2026-11-09 (Refs #1314 #440)

Dated wording qualification, a first pass of the separately scoped #1314 follow-up and not a new #440 correction cycle. It supersedes only the explanatory counts and ranges named below. The original C2 and current-main preparation records, their reviews and adverse findings are kept byte for byte, and no source, fixture, policy, SQL behavior or acceptance changed. Every number was reproduced with `git diff --name-only` and `git diff --numstat` between the pinned commits, never against a later `origin/main`. Records:
[research](../../.copilot-tracking/research/2026-11-09-count-qualification-1314-research.md),
[plan](../../.copilot-tracking/plans/2026-11-09-count-qualification-1314-plan.md),
[details](../../.copilot-tracking/details/2026-11-09-count-qualification-1314-details.md) and
[critique](../../.copilot-tracking/plans/2026-11-09-count-qualification-1314-critique.md).

| Id | Qualification | Evidence |
| --- | --- | --- |
| Q1 | The C2 changes record (`2026-11-09-sql-wave-checkpoint-440-c2-changes.md`, line 17) says the comparison against `ef28d4da4` is 15 paths with "one re-wrapped index line". The final comparison of C2 `f2e07999386399694abe91562555b35c0105ab9b` against `ef28d4da4` is 17 paths, 700 additions and 0 deletions, with no index replacement. The 15-path figure (604 additions, 0 deletions) matches the intermediate tree at the C2 merge `ec597d023`, before the C2 changes and review records were added and the C2 state record was rewritten. The index re-wrap (`docs/reference/README.md`, 4 additions and 1 deletion) belongs to the separate comparison of `06f408dd7` against `f2e07999` (11 paths, 258 additions, 5 deletions; the other 4 deletions are in `.github/rubric/scores/latest.json`, which arrived with the C2 merge of `ef28d4da4`). Neither comparison is a range against later `origin/main`. | `git diff --name-only` and `--numstat` for `ef28d4da4..f2e07999`, `ef28d4da4..ec597d023`, `ec597d023..f2e07999` and `06f408dd7..f2e07999` |
| Q2 | The current-main preparation details (`2026-11-09-sql-wave-checkpoint-440-mainprep-details.md`, line 12) describe main's pack insertions as the only additions versus `f2e07999`, and the note, index sentence and log entry as the only additions versus `origin/main`. The reproduced figures in the preparation changes record (pack 171 and 133, log 5 and 15, index 4 and 17) are correct but mix sources. Versus `f2e07999` for `45e8744f`: pack +171, index +4, log +5 are incoming main pack content (+154 pack, 0 index, 0 log, to the merge `53cef9040`) plus the new preparation note (+17, +4, +5). Versus main `3a9767d5c`: pack +133, index +17, log +15 are inherited SQL-wave and C2 content (+116, +13, +10) plus the same new note (+17, +4, +5). Zero deletions holds for those three files in every one of these ranges only; the whole tree from `f2e07999` to `45e8744f` is 234 files with 7141 insertions and 34 deletions because it contains incoming main, and the 7 deletions between `53cef9040` and `45e8744f` are in the preparation state record, not in the pack, index or log. | `git diff --numstat` for `f2e07999..53cef9040`, `53cef9040..45e8744f`, `f2e07999..45e8744f`, `3a9767d5c..53cef9040` and `3a9767d5c..45e8744f` limited to the pack, index and log, plus the whole-tree `--shortstat` |
| Q3 | The preparation plan (line 30, P5) and details (line 12) speak of append-only prefix equality. The index and log of `45e8744f` are byte-prefix extensions of `f2e07999` (checked with `cmp`); the pack is not, because incoming main inserted its sections before the SQL-wave sections. For the pack the valid proof is ordered line preservation with 0 deletions, not a byte prefix. | `cmp` of the `f2e07999` blobs against the leading bytes of the `45e8744f` blobs |

The original records, reviews and adverse outcomes stay as authored, and their other statements are not re-assessed here. Not claimed: a SQL fix, new live, SQL, browser or model evidence, whole #440, #81 or #1314 closure or acceptance, a third #440 correction cycle or budget renewal, independent exact-head review, hosted CI or any approval.

### Priority ordering before-fix paired validation, 2026-11-11 (Refs #1292)

Evidence-only; not Source E5 and not a new correction grant. One paired campaign run once, with no retry, at `main` `cea1cee5b20f63d7bb134fb7cb87a1bbc7d8618f`, on one task-owned disposable SQL Server (image id `sha256:cf8f0ab2ebe61feec2eed2629061a07d247f791c2a8ddda74a4ac9f06a291718`, SQL Server 2022 16.0.4305.5, Python 3.12.3, `mssql-python` 1.15.0, local default Docker engine, run by image id with `--pull=never`). Both arms ran the unchanged maintained `test_priority_order.py` (blob `c140d4a8249ba38042d86755a94445925ac5f7be`) from `src/core/tests`, with a sanitized empty environment and no `PYTHONPATH`, against non-editable `pip` installs of Git snapshots: the original source `e2ecee2565e86889c6beb43cb32e7c5b54270e01` (`store.py` `a99948569d64`, `sqlstore.py` `d790455892b6`, `mssqlstore.py` `842d790484eb`) and this head (`store.py` `70d71de39a79`, `sqlstore.py` `01a3a44c9269`, `mssqlstore.py` `c712ad4a8a15`). Each process printed its own `sys.path` and module files; every installed file came from that arm's site-packages and its Git blob hash equalled the arm's blob. Whole-source identity between the arms is not claimed; the blobs differ.

| Arm | Selection | Result |
| --- | --- | --- |
| Original source | 5 inherited methods on `MssqlPriorityOrder` (batch, older-edit, per-user and `ai_task` exclusion, decision boundary, older-edit after incremental reload) | Ran 5, FAILED (failures=4), exit 1, 22 s. Four methods failed with the wrong recommendation (`zzz000000001`, the oldest-created proposal with the highest identifier, instead of the newest-created `aaa000000003` or `mmm000000003`); the decision-boundary method passed, as predicted for a method that never reloads. No import, DDL or bootstrap error |
| Current source | The same 5 on SQL Server, the same 5 on `SqlitePriorityOrder` and 4 on `JsonPriorityOrder` | Ran 14, OK, exit 0, 0 skips, 5 on SQL Server, 23 s |

Qualifications of the red: the older-edit-after-incremental-reload method failed at its first, cold-load assertion (test line 194), before the incremental step; the other three failed at assertions on a freshly opened store (lines 78, 88 and 98). The red therefore evidences the unordered cold-reload recommendation, not an incremental-reload defect specifically. The earlier original native SQL log (`.copilot-tracking/changes/logs/1292-2026-11-08-sql/base-priority.stderr.txt`) is a separate, historical observation of the same four methods and is not aggregated with this run. The 13 failures pinned in the issue are of two other resident-control methods and are not re-derived here. The unknown historical startup failure stays UNKNOWN: this run neither reproduces nor explains it.

Cleanup and receipts (verifier gates these this time): container id equals removal id (`fc9993abf50c...`), the leftover-database query exited 0 with an empty list, a post-removal `docker ps -a` for the task label was empty with status 0, and the container's `.Image` equalled the pinned id. Whole admission 75 s (processes 22 s and 24 s) under the 600 s and 1200 s bounds. Raw sanitized receipts are session-held with `SHA256SUMS.txt` digest prefix `b247dbd1a5c9`, original-arm stderr `41c46d7f27e3`, current-arm stderr `63cd1512f29e` and verifier output `fdcbe9c7758b`. The runtime image is identified by the id from `docker image inspect` and the container `.Image` field, and the daemon is the local default context (`unix:///var/run/docker.sock`); no authentication of the endpoint beyond that is claimed.

Literal acceptance mapping (no box is ticked; the closure decision stays with the owner and coordinator):

| Criterion | Surviving and fresh evidence | Status |
| --- | --- | --- |
| AC1 ordering across cold and incremental reloads, in-memory parity, requesting user and `ai_task` exclusion | Original implementation and tests (`656bacb56`, merged 1308 `8d6f029ca`), the original independent review, the 148-test real-SQL pass at `ba71894bb` (2026-11-09) and this fresh 14-test pass at the pinned head | Evidenced by merged source, tests and runs; criterion owner decides |
| AC2 same-timestamp batches, older edits, multiple users, truthful legacy transition | Batch, older-edit and per-user methods re-run here; legacy transition covered by the 148-test run and the documented heuristic, which still needs a named data-owner decision | Partly re-executed here; legacy decision open |
| AC3 fails against old behavior, passes on SQL Server with zero skips, SQLite and in-memory parity, with commands, counts and outcomes | Fail half: 4 of 5 ordering failures on original source on real SQL Server (this run). Pass half: 14 passed, 5 on SQL Server, 0 skips, with SQLite and in-memory parity | Both halves now have native SQL evidence for the selected methods; not the whole 142-test module against the old source |
| AC4 review and approval boundary and ranking policy preserved | The decision-boundary method passes on both arms; no review, approval, consent or ranking rule changed | Evidenced for the tested boundary; no human or live approval inferred |
| AC5 RPI evidence through the issue's own branch and PR | Original records and merged 1308 and 1326 survive; this lane adds its own ordered RPI records (research, plan, details, critique, state, changes, review) on a separate branch | The issue's own PR exists; independent exact-head review of this candidate is not done |

Not claimed: Source E5 or any fix, the startup cause, whole #1292, #81 or #440 acceptance, a full local gate, hosted CI, Azure or live behavior, independent review of this record, or any approval. Original records and adverse outcomes stay as authored. Prospective records: [research](../../.copilot-tracking/research/2026-11-11-priority-before-fix-1292-research.md), [plan](../../.copilot-tracking/plans/2026-11-11-priority-before-fix-1292-plan.md), [details](../../.copilot-tracking/details/2026-11-11-priority-before-fix-1292-details.md), [critique](../../.copilot-tracking/plans/2026-11-11-priority-before-fix-1292-critique.md), [changes](../../.copilot-tracking/changes/2026-11-11-priority-before-fix-1292-changes.md) and [review](../../.copilot-tracking/reviews/2026-11-11-priority-before-fix-1292-review.md).

## Lifecycle and simulator controls current-main checkpoint (2026-11-09, Refs #440 #81 #189 #954 #1292)

DRAFT, not approved. A new recurring #440 checkpoint, not a corrective cycle or a renewal, and documentation only: no feature, code or policy changed. It gives the merged lifecycle (#1240) and simulator controls (#1313) integration an explicit current-main disposition after the photo regression (#1315) and the #1292 diagnostic record (#1318). It appends to the sections above; the earlier SQL-wave section, its C2, its independent Low findings and the open #1314 wording follow-up are not changed. Records:
[research](../../.copilot-tracking/research/2026-11-09-controls-checkpoint-440-research.md),
[plan](../../.copilot-tracking/plans/2026-11-09-controls-checkpoint-440-plan.md),
[details](../../.copilot-tracking/details/2026-11-09-controls-checkpoint-440-details.md) and
[critique](../../.copilot-tracking/plans/2026-11-09-controls-checkpoint-440-critique.md).

### Identities, merged changes and exclusions

| Item | Pinned value (read 2026-11-09) |
| --- | --- |
| Source `main` | `48350983be156d33afb5803570e1bc0bdb5455bb`, tree `1f6f8021cfbab17ee4975ada308771ba1cbd952b`, `src` tree `99c5354df6d5ebe886d1ad1b98e6a60146543c03` (PR 1315 squash) |
| PR 1240 (#81 lifecycle) | `3a9767d5c`, merged 16:50:00Z, head `ccc7358dad0628a660b76b1feb4e3a3556cc952c` |
| PR 1317 (previous #440 checkpoint) | `2b6d80a25`, merged 17:11:39Z |
| PR 1313 (#189 simulator controls) | `0dc4dd35ce9ea6bddd1d4ca34d5f8ec6e234adfe`, merged 17:35:18Z, reviewed head `e192bc74732e824a3488c49a4875df9bd4463cd8` |
| PR 1318 (#1292 diagnostic record) | `9557d9da429ec732f4f24dbd94cb28acaf0a7545`, merged 17:44:15Z, documentation only |
| PR 1315 (#954 photo regression) | `48350983b`, merged 17:47:10Z, head `c46a7a025a20666527b65783410f12967379ee0a` |
| Rubric commits | `700bf11e1`, `b4a343a16`: only `.github/rubric/scores/latest.json` |
| Issue states (read live) | #81 OPEN, #189 OPEN, #954 CLOSED (both literal acceptance criteria ticked), #1292 OPEN, #440 OPEN, #1314 OPEN, #159, #1288, #1258, #144 and #123 OPEN |
| Excluded | PR 1320 (`ff06a15f`, chat refusal receipts) is OPEN and not on main; its approved source and any candidate compatibility run are candidate evidence only and are not main acceptance. #159 stays separate |

Hosted checks: PR 1313 and PR 1315 are reported by the coordinator as all 19 status entries SUCCESS; PR 1240 was read as 19 of 19 SUCCESS in the earlier preparation note. Source CI does not run on a push to `main`, so none of these is a hosted run of `48350983b` itself.

### Source delta and equivalence (Git, read-only)

Main changed 16 files since the previous checkpoint base `3a9767d5c` (1889 insertions, 43 deletions), all under `src/api` plus the rubric file. Nothing under `src/core`, `src/agents`, `infra`, `tools` or `.github/workflows` changed.

| Command | Result |
| --- | --- |
| `git diff e192bc747 0dc4dd35c -- src tools infra` | empty: the 1313 squash source equals the reviewed 189 head |
| `git diff e192bc747 48350983b -- src tools infra` | one file: new `src/api/checks/photo_flag_stale_browser_check.py` (448 lines, sha256 `620301300f3f3dc541e2d1bb577e5331a89e2e440c6a56466a62bd19f324a6db`); no production source changed |
| `git rev-parse` of the `src` tree of the tested 954 projection `7c72dbd58588094956c7467e0b7b4afbe1c7fc2e` versus `48350983b:src` | both `99c5354d`, identical |
| `sha256sum -c MANIFEST-projection-src.sha256` over `git archive 48350983b src` | 642 of 642 OK |

Equivalence therefore shows that the runtime source on main is the source that the 189 and 954 browser runs exercised. It does not extend to `src/core` behavior, which was last exercised by the PR 1240 hosted checks and the SQL-wave observations, and it adds nothing about SQL Server.

### Byte witnesses consumed (coordinator-held, outside this repository)

| Evidence | Witness | Result |
| --- | --- | --- |
| 189 composed browser, head `e192bc747` | `capture-189-composed-browser/hashes.sha256`, sha256 `2f0275c1743b7af5062b08bb60057e710209d461c569b3aa6a998e6142b03e01` | 78 of 78 members OK; exit 0; 13 states, 13 axe scans, 0 violations; delayed-Stop probe old exit 1 (negative control), new exit 0; synthetic, intended 503 write-error state in stderr |
| 189 independent Functional | `independent-189-c4-final/functional-findings.json`, sha256 `0230cf4aecafb0aeabee56fd5779ff5811659263e7a18e8eb33d2922c871bb77` | approve, 0 findings; reused unchanged coverage, not a fresh full web or assistive-technology audit |
| 954 current-main compatibility | `evidence-954-current-main/MANIFEST.sha256`, sha256 `2647335942707f46d134b1fe9a5f9442db044962fed4d42f40bc0c084d64fe49` | 16 of 16 OK; exit 0; 83 PASS and one FAIL that is the expected negative control; one nonqueued `flock -n` admission 17:41:21Z to 17:41:27Z after a holder check; both 503 and 403 receipts quiet |
| 954 independent | `independent-954-current-main/functional-findings.json`, sha256 `480ed8441b7e1c10e49b3f595f024a115fd36589724b9781fd91cc6e7cf318a5` | approve, 0 findings |
| 1292 record (#1318) | coordinator ledger and the original-load diagnostic section above | 0 of 2 historical paired campaigns reproduced, cause UNKNOWN; the original series stays one failure then four passes in five total executions; manifest 26 members plus itself |

The 954 result is native diagnostics with `literal_no_console_event` false and informational (two native failed-resource diagnostics per receipt). It is not a literal console-zero, assistive-technology, live or general UI conformance claim. The 1292 record supports no current-source SQL fix or acceptance.

### Document identities (draft is not approved)

BRD 0.21.0 `draft` blob `34d88395de861e9799eb9e24121a21c92c7a5adc`; PRD 0.21.0 `in-review`, unsigned, blob `c788b917bafaede215f326f0efc71e071a687f1c`; case study original `0aec2d80` and addendum `28c19242`; ADR 0001 `d42fa5c4`, 0002 `cbe21530` (only its staff identity decision is owner-accepted, 2026-10-24), 0003 `d6064539`, 0004 `9406c2e7`, 0005 `4d610335`, 0006 `956da1a3`, 0007 `abb21088`. All identical to the previous checkpoint; no new legal or regulatory claim is made.

### Requirement trace (document-qualified) and boundaries

BRD and PRD functional requirement numbers collide, so each trace names its document.

| Requirement | Package, API or UI boundary read from source at `48350983b` |
| --- | --- |
| PRD FR-050 and AC-066 (simulated monitoring through IoT Hub), ADR 0003 decision 6 as cited by the #189 issue body | `src/api/src/zava_forward/api/simulator_admin.py` edits only the existing `live-sim-control-v1` document through `live_control` guards and `live_simulator.check_capacity`; it starts no job, calls no Azure API and changes no role or resource |
| Auth and roles | administrator only (`ADMIN_REQUIRED` 403); a view-only administrator sees every option and changes nothing (`VIEW_ONLY` 403); the destination is listed in `workbench.py` with access "needs a role with this authority" for view-only users |
| Finite cost and run controls | expiry must be in the future and at most 14 days (`CONTROL_WINDOW_INVALID`); cohort capacity checks (`B1_QUOTA_HEADROOM`, `RATE_TOO_LOW_FOR_HOMES`); confirmation tick; stale-control check; `live_control.locked` advisory lock refuses interleaved writers with `CONTROL_BUSY` |
| Failure and manual routes | unconfigured control returns 503 with a named manual route (`MANUAL_ROUTE`); write failures 503; a missing or invalid control already blocks sending; the IoT SDK import is lazy and reports `IOT_SDK_MISSING` |
| Budget alert (live gate) | reported `not_recorded`, `live_verified` false (`simulator_admin.py:131`); the approval reference is not evidence of an alert; #146 stays the owner |
| PRD FR-008 controlled transition gate with FR-016 and FR-017 (issue 81 alignment section above) | lifecycle source merged by PR 1240 in `src/core` (gates, quality, procurement, appointments, store, resident decisions, complaints route); human approval, resident consent and legal review stay with named humans, and the rule records stay exercise fixtures |
| BRD OD-43 | the actual monitoring inventory and ownership stay an open decision; simulated values are not site facts |

Resident-facing consent and human quality decisions are unchanged by this record. Backlog owners: #189 (live run owner, time limit and budget alert criterion unticked), #1292 (SQL priority ordering), #1258, #1288, #144, #159 (with unmerged PR 1320) and #146 (budget alert).

### Findings, owners and gates

No new defect and no new refactoring is confirmed by this checkpoint, within this bounded scope: source and evidence identity, the boundaries above and the open issue states. The candidate items are existing and owned: current-source SQL recurrence and acceptance (#1292, wording in #1314), ranking archive durability (#1258), quality sensor grounding (#1288), hosting and load (#144) and chat receipts (#159, PR 1320). No speculative issue is opened.

Not run, so unverified: any new unit, static or browser check (none needed after the equivalence proof above, and neither browser campaign is repeated), SQL Server and Azure paths (the 189 handoff records 19 Source and 110 Core SQL or Azure skips), live run and budget alert, real IoT or model calls, assistive technology, literal console zero, hosted CI for this branch, and the whole Major HVE behavior validation obligation of #440. None of these is relaxed. This documentation checkpoint does not supply that behavior evidence and does not approve any deferral.

### Recommendation and resume conditions

Continue the existing owners, with a HOLD on every closure claim. No fix, pivot or deferral is proposed or granted.

* This checkpoint does NOT satisfy the lifecycle-wave trigger recorded in the SQL-wave section above. That trigger still needs new integrated evidence: targeted local results, hosted state of the exact head, and resident-decision and gate behavior on SQL where the owner requires it. Those resume conditions are retained unchanged.
* Closure holds stay on #81 and its #1240 integration, #1292, #123, #440, and the #189 live criterion (owner, time limit and budget alert verified live).
* Dependent expansion that relies on lifecycle or SQL ordering evidence waits for the trigger above. Expansion that relies on the simulator controls waits for a live-verified budget alert and a named run owner.
* #159 compatibility with main, PR 1320 and any candidate work are evaluated on their own evidence.
* Independent #189, #954, #159, #1288, #1258 and #144 source work may proceed. #954 is already closed on its literal criteria.

Limits: single-session authored record with no independent exact-head review and no hosted CI for the commit that carries it; the witnesses are coordinator-held files read in this session, with their digests recorded here; PR check counts for 1313 and 1315 are coordinator-reported. Not claimed: approval, closure, acceptance of any criterion, whole #440, #81, #189 or #1292 acceptance, live, SQL, Azure, model, assistive-technology or production readiness, or any legal, resident or production approval.

## Integrated current-main journey checkpoint (2026-11-09, Refs #440 #81 #123 #184 #136)

DRAFT, not approved. A new recurring #440 checkpoint for the earlier lifecycle and shared-SQL integration trigger that stayed due after the controls and count records (#1322) and the current-source SQL observations (#1326). It is evidence only: no source, test, policy, coordinator or workflow change, no issue, board or pull request write, and no corrective cycle or budget renewal. Earlier sections, their reviews and adverse outcomes are unchanged. Records:
[research](../../.copilot-tracking/research/2026-11-09-current-main-1924-440-research.md),
[plan](../../.copilot-tracking/plans/2026-11-09-current-main-1924-440-plan.md),
[details](../../.copilot-tracking/details/2026-11-09-current-main-1924-440-details.md),
[critique](../../.copilot-tracking/plans/2026-11-09-current-main-1924-440-critique.md),
[changes](../../.copilot-tracking/changes/2026-11-09-current-main-1924-440-changes.md) and
[review](../../.copilot-tracking/reviews/2026-11-09-current-main-1924-440-review.md).

### Identities, covered changes and exclusions

| Item | Value (read 2026-11-09) |
| --- | --- |
| Pinned `main` and latest `origin/main` | `2be660e9d290f95ff05fc5a56d6539768576732b` (PR 1326), tree `d09e22c71df705ad13127a490b0d742269d2f2a2`; `git fetch origin main` resolved the same commit |
| Executed source | planning commit `eb8301c50feeebf2b40892c3878f682181dbe668` (tree `339f2bd93c236fe776933a6b129a506506089c3c`), whose only difference from main is `.copilot-tracking`; `src` tree `86bc00e19a167e517ae2955ad88d6e2f7b4eac26` equals main and the #1326 campaign input; `tools`, `infra` and `.github/workflows` trees equal main |
| Documents | BRD 0.21.0 `draft` blob `34d88395de861e9799eb9e24121a21c92c7a5adc`; PRD 0.21.0 `in-review` blob `c788b917bafaede215f326f0efc71e071a687f1c`; case study original `0aec2d80`, addendum `28c19242`; ADR 0001 `d42fa5c4` Proposed, 0002 `cbe21530` (only the staff identity decision accepted 2026-10-24), 0003 `d6064539`, 0004 `9406c2e7`, 0005 `4d610335`, 0006 `956da1a3`, 0007 `abb21088` Proposed. All unchanged since the previous checkpoint; none becomes approved here |
| Covered merged changes | PR 1141 Azure Queue adapter (`4fcd1934f`), 1295 capstone documentation (`ad679b96b`), 1308 priority ordering (`8d6f029ca`), 1312 chat-schema SQL selector, 1240 lifecycle (`3a9767d5c`), 1313 simulator controls (`0dc4dd35c`), 1315 photo regression (`48350983b`), 1320 metadata-only validation refusal receipts (`ba71894bb`, merged 18:00Z, so no longer excluded), 1322 and 1326. Issues #81, #123, #144 (queue slice), #184, #189, #954, #1292, #159 |
| Excluded, not on main | #1288 retained-value UI and Quality AI (issue open, no published pull request); #1258 and #1259 ranking archive durability (open issues); open PR 1327 (Blob ranking archive Bicep, #136); #136 epic; #1296 candidate policy; any unpublished work. No functionality of these is observed or accepted |
| Issue states (read live) | #440, #123, #81, #136, #144, #146, #159, #184, #185, #189, #891, #1258, #1259, #1288, #1292, #1296 and #1297 open; #91, #954 and #1314 closed |

### Requirement trace (document-qualified)

BRD and PRD functional requirement numbers collide, so each row names its document.

| Requirement | Source boundary on `main` | Observed local this checkpoint | Class |
| --- | --- | --- | --- |
| PRD FR-050 with AC-066 to AC-068 and BRD FR-048, AC-090, RULE-014 (simulated monitoring, sensor data is not acceptance evidence); ADR 0003 decision 6 | `live_control.py`, `live_simulator.py`, `simulator_admin.py`, `iot_stream.py`, `sensor_ingestion.py`; core `sensor_consumer.py`, `sensor_stream.py`, resident sensors | API `live_control` 34, `live_simulator` 31, `simulator_admin` 27, `iot_stream` 37, `iot_credential_hygiene` 12, `sensor_ingestion` 47, `sensor_handover_demo` 4; core `sensor_consumer` 37, `sensor_consumer_live` 10, `sensor_stream` 15, `resident_sensors` 10, `sensor_privacy` 17 | Local observed on fixtures; live Hub, deployed jobs, grants, route unverified |
| PRD FR-044 and BRD FR-044 with AC-084 (real AI per record, proposal against reviewed, case access independent of the model); ADR 0004 option C staged; ADR 0005 synthetic only | `chat_panel.py`, `assistants.py`, AI boundary and ledger paths | API `ai_boundary` 6, `ai_call_site_inventory` 6, `chat_panel` 55, `resident_assistant_api` 10, `assistants` 120 (58 SQL skips); core `chat_panel` 45, `ai_consumption_safety` 2. Named AI-unavailable cases passed: demo switch off or wrong key keeps rules-only status and makes no call, provider failure falls back to workflow-only, a call fails closed without a ledger | Local observed with stub providers; no actual model call, so no actual-AI evidence |
| PRD FR-008 controlled transition gate (resident decisions and complaints route: no requirement ID asserted here, because BRD and PRD numbers collide); human approval and resident consent stay with named humans | core `gates.py`, `resident_decisions.py`, `complaints_route.py`, `store.py`, `sqlstore.py` | Core `gates` 20, `handoff_lifecycle` 20, `resident_decisions` (SQLite and JSON legs), `resident_choice_queue` 4, `quality_procurement` 136, `journey_acceptance` 4; plus SQL Server run S1 below | Local observed, including one SQL Server run of the resident-decision class |
| PRD FR-003 and ADR 0002 staff identity (Entra principal, roles) | `auth.py`, role matrix, administrator-only simulator control (403 for view-only) | API `role_matrix` 13, `simulator_admin` 27, `workbench` 5, `photo_availability` 1 (Node-driven fixture) | Local observed; ingress trust and tenant not observed |
| PR 1320 chat refusal receipts (issue #159 thread; this record asserts no requirement ID for it) | `chat_panel.record_validation_refused`, `server.py` | four new tests passed in both packages; the "JSON and SQL audit" case uses the SQLite-backed `SqlStore`, not SQL Server | Local observed; not live |
| ADR 0006 package boundaries | core, agents and api dependency-rule tests | merged queue adapter `test_queue_azure` 24 and `test_worker` 6 | Local observed |

### Actual local commands and outcomes

Python 3.12.3 in a task-owned virtual environment with editable installs of this worktree's `src/core`, `src/agents` and `src/api`, because the pre-existing editable installs point at another checkout. Every A-series check ran under `env -i` with only `PATH`, `HOME`, `TMPDIR`, `ZF_DATA` (inside the owned scratch directory), `LANG` and `PYTHONPATH`, so every `ZF_*` SQL, Azure, browser and benchmark switch and every credential was unset (the ambient shell held none). S1 alone ran under the nonqueued SQL harness, which exported the disposable-SQL switches and a generated throwaway container password for its own container only; no other secret was present. Source status was empty before and after, and a preflight proved package and test-module import origins inside this worktree. Raw logs are outside the repository in the owned scratch directory, are not committed and are summarized by the digests below.

| Id | Selection (working directory) | Producer exit | Result |
| --- | --- | --- | --- |
| A1 | 13 core modules (`src/core`, `PYTHONPATH=tests`): `test_sensor_consumer`, `_consumer_live`, `_stream`, `test_resident_sensors`, `test_sensor_privacy`, `test_chat_panel`, `test_gates`, `test_handoff_lifecycle`, `test_resident_decisions`, `test_resident_choice_queue`, `test_quality_procurement`, `test_ai_consumption_safety`, `test_journey_acceptance` | 0 | 628 ran, OK, 111 skipped: 108 `MssqlResidentControls` needing an owned loopback SQL Server (observed separately in S1), 1 own local SQL, 1 JSON-only rollback, 1 explicit isolated Azure SQL |
| A2 | 16 API modules (`src/api`, `PYTHONPATH=../core/tests:../agents/tests:tests`) | 1 | 439 ran, 36 errors, 59 skipped. Cause: my sanitized `PATH` omitted `node`, so 35 `test_case_journey` and 1 `test_photo_availability` tests raised `FileNotFoundError: 'node'`. Environment fault of this run, not a product failure. The log is retained unchanged |
| A2b | the same 16 modules with the Node directory added to `PATH` (node v24.21.0) | 0 | 439 ran, OK, 59 skipped: 58 `test_assistants` needing a disposable SQL Server, 1 opt-in local Chromium chat browser test. 37 handled fail-closed log tracebacks "Rule evaluation unavailable ... law store is not loaded" appear in the passing output (fixtures without a law store); no defect is asserted |
| A3 | `test_queue_azure` and `test_worker` (`src/agents`, `PYTHONPATH=tests`) | 0 | 30 ran, OK, 0 skips |
| S1 | `test_resident_decisions.MssqlResidentControls` (108 tests) on a disposable SQL Server 2022 container (16.0.4305.5 RTM-CU27-GDR, image `sha256:cf8f0ab2ebe6...1718`, loopback only, `mssql-python` 1.15.0, `--pull=never`), one nonqueued `timeout -k 10 700 flock -n /tmp/ama-rpi-heavy.lock` admission at 19:43Z (lock observed free), one 600 s process bound | 0 | 108 ran, OK, 1 skipped (`JSON file rollback only`), 528.1 s unittest time, 547 s campaign. Cleanup: removal exit 0, leftover-database query exit 0 with an empty result, no container with the owned name afterwards, container id `79c48f89fcb7`. Imports verified under this worktree (`sqlstore.py` sha256 `0b0caf62...`, `mssqlstore.py` `1825dc5f...`) |

Totals of the four final processes A1, A2b, A3 and S1: 1205 tests ran, 0 failures or errors, 171 skips (108 of A1's skips are the class S1 ran). The superseded A2 run (439 ran, 36 errors) is retained, not counted. Digests of the retained raw output manifests: `SHA256SUMS` of the A-series logs `60aff6461f6aaa3824b9fc5e51b5a26705a9ed993ab8477c8decdf3eb05097ba` (9 members), of the S1 outputs `8d607b0eab4d7bc56a97690dfbdd81bcec2fdeaf39636fa0e679f7ca2dd4942f` (14 members). Log sha256 prefixes: A1 `bad8e841a806`, A2 `f8181f8dece4`, A2b `565e72b22425`, A3 `352eaf6524d7`.

S1 limits, stated as the earlier SQL records state theirs: only the resident-decision class on SQL Server (the lifecycle gates, quality, procurement and appointment tests ran on SQLite and JSON stores only); the mutable image tag was used with `--pull=never` and the immutable image id was checked before start; no daemon endpoint authentication was inspected; the test outcome gate is the unittest exit and `OK` line read by hand, and cleanup was gated by the script exit statuses recorded in files, not by an external verifier; a timeout path was not exercised.

### Reused evidence (not rerun)

* #1326 priority SQL campaign: 3 processes, 148 tests, 67 on SQL Server, 0 skips, source `src` tree `86bc00e19a167e517ae2955ad88d6e2f7b4eac26`, identical to this checkpoint's tree (`git rev-parse HEAD:src`). Its limits stand: the verifier gated outcomes and not cleanup (cleanup was observed separately), the leftover query exit status was not retained, no timeout-path receipt, mutable tag with `--pull=never`, and no endpoint authentication. It does not show the original unordered defect is absent from pre-fix source and does not explain the UNKNOWN historical startup failure. Not rerun to refresh a date.
* #1313 and #1315 browser observations and the #1322 witnesses: their inputs predate #1320 (the 189 input `e192bc747` predates the photo-check script too), so each keeps its own source identity and the production runtime differs from the current by the four-file #1320 chat receipt delta. Not rerun here: Playwright is not installed in the task environment and the #1320 change is server-side. No browser, axe or assistive-technology result is claimed for this tree, and scripted axe observations never equal assistive-technology or actual-model acceptance.

### Journey read from source and what is not observed

The merged chain is: finite simulator control (administrator only, 14 day maximum, cohort 1 to 100, advisory lock, fail closed) to the Hub sink to receiver admission with consent, mapping and window checks to the observed-series store to the resident own-home view. The employee retained-value view and the sensor input to the real Quality model are not on main (#1288, no published pull request). The chain is exercised in pieces by fixture-level tests, not by one end-to-end automated journey, and no live Hub send, deployed job, certificate, route or grant was observed. Quality acceptance, resident consent, legal review and professional approval stay named human decisions; deterministic rules and stubs are never presented as actual AI.

### Findings, owners and gates

No defect or refactoring need is confirmed. The A2 failure was this run's `PATH` and is corrected by A2b; it is not filed. Gaps map to existing owners and are not duplicated:

| Gap | Owner | Gate effect |
| --- | --- | --- |
| Employee retained-value UI, sensor input to the Quality model, attributed unapproved flag | #1288 | holds Quality sensor expansion; no merged candidate |
| Live Hub, provisioning, certificates, run owner, time limit, budget alert | #184, #185, #189, #146 | holds those closures and live-dependent expansion |
| Resident-decision SQL Server leg (S1) now observed once; remaining lifecycle gates, quality and appointment SQL legs, assistants SQL (58 skipped) and sensor SQL (opt-in) not run | #81 (#1240), #1297 for the sensor skip contract | #81 closure still waits for hosted state of the exact head and any owner-required SQL scope |
| Priority ordering recurrence and startup cause UNKNOWN | #1292 | unchanged |
| Ranking archive durability and Blob wiring | #1258, #1259, #136 (PR 1327 open) | excluded; unproven |
| Container hosting beyond the merged queue adapter | #144 | unproven |
| Chat per-call activation and receipts beyond #1320 | #891, #159 | unchanged |

### Recommendation and resume conditions

CONTINUE through the existing owners, HOLD every closure claim, and gate only the affected closures and dependent expansion: #81 and #123 closure, #184, #185, #188, #189 live criteria, #136 and #1288-dependent Quality sensor expansion. Independent repairs continue. No fix, pivot, requirement relaxation or deferral is proposed or granted, and none is inferred.

Resume conditions: (1) hosted checks for the exact head of any #81 or #123 closure candidate; (2) the remaining lifecycle SQL legs only if the owner requires them, via one nonqueued shared-lock admission with finite cleanup and no live or private fallback; (3) #1288 merged and independently assessed before any Quality sensor claim; (4) authorised operators verify certificates, route, grants and budget alert before any live claim; (5) assistive-technology and actual-model evidence under named human approval.

Limits: single-session authored record; the commit carrying it has no independent exact-head review (see the review record for the one review executed), no hosted CI and no push; per-process logs are retained outside the repository. Not claimed: approval of any document, closure or tick of any criterion, whole #440, #81, #123, #184, #136 or Major HVE acceptance, live, Azure, actual-model, assistive-technology, browser or production evidence, legal, resident or professional approval, or a full gate.

### Qualification Q1 (2026-11-09, appended after the frozen checkpoint `3965fa489d8f07d0180b94d3fdfd7db16441790d`; originals above unchanged)

These statements qualify the section above and take precedence over it where they differ. They follow an independent documentation assessment; no runtime, SQL or browser work was repeated.

* S1 chronology. The prospective plan and details selected only the sanitized, SQL-off processes A1 to A3. S1 was selected afterwards, without a recorded prospective amendment, so it is not an ordered or planned phase. The earlier brief permitted a distinct necessary heavy check under nonqueued shared-lock admission; no other authority is inferred. S1 (the resident-decision class, 108 discovered) is broader than the #1326 two MSSQL resident methods plus four parity tests, so it is a useful broader observation and not a whole duplicate. The coordinator withdrew its earlier overbroad no-coverage claim in issue 440 comment 6750088725, preserving comment 6749815210.
* Raw retention. The producer removed the scratch directory `/tmp/i440-1924-opq5ok` at the end of the original loop, so the statement above that raw logs remain in the owned scratch directory is superseded. The A-series originals, including the adverse A2 log, survive at the coordinator-saved `observed-440-1945-logs` with a `SHA256SUMS` readback that was OK. Raw retention of S1 is unverified: no surviving copy was located, and nothing was reconstructed or rerun. The S1 exit 0, 108 discovered, one skip and cleanup observation rests on the historical producer transcript, not on a retained 14-member bundle or a fresh independent cleanup verification. The digests above are historical summaries and do not show that any bytes survive.
* Absence bound. No employee retained-value path was identified in the inspected paths; differently named paths are unverified. The inspected registered Quality snapshot carried permitted document metadata, Quality records and checklists, and no dedicated retained-sensor fields. The exclusion of the unpublished #1288 candidate is not a whole-main absence proof.
* Requirement IDs. PRD FR-008 governs controlled gates. PRD FR-016 and FR-017 are provider-package and quality-disposition records, not resident-decision or complaints IDs; no resident or complaints requirement ID is asserted by this checkpoint, and none is invented. The original native Review corrected this pack only, not every tracking record.
* Process count. The four final processes are A1, A2b, A3 and S1, including one nonqueued disposable SQL run: 1205 discovered, 171 skipped. The first failed A2 is separate and not a fifth final process. The 108 S1 discoveries are not all actual SQL executions (one by-design skip).
* Unchanged: the document approval statuses, the #440 closure and Major HVE holds, pin `2be660e9`, and the exclusions of unmerged Quality and Blob work, which remain a historical current-main observation and not later acceptance. Refs #440 #81 #123 #184 #136 only.

## Parent-topic Blob and Quality checkpoint (2026-11-09, Refs #440 #1288 #1258 #1259 #136)

Draft, local-only, not approved. It qualifies the 2026-11-09 current-main checkpoint above, which observed `main` `2be660e9` and excluded Blob and Quality; that record is unchanged and remains a historical observation. This section records two separately labelled source scopes and is neither final merged-main acceptance nor Quality merged-main functionality. Records: [research](../../.copilot-tracking/research/2026-11-09-blob-quality-2055-440-research.md), [plan](../../.copilot-tracking/plans/2026-11-09-blob-quality-2055-440-plan.md), [details](../../.copilot-tracking/details/2026-11-09-blob-quality-2055-440-details.md), [changes](../../.copilot-tracking/changes/2026-11-09-blob-quality-2055-440-changes.md) and [review](../../.copilot-tracking/reviews/2026-11-09-blob-quality-2055-440-review.md).

### Source identities

| Item | Identity |
| --- | --- |
| Merged main (fetched) | `a04668ae94b5c2f38e6c55ed789db245e8c71d16`: Blob and Bicep #1328, historical checkpoint #1329, bot score metadata #1330 |
| Quality parent topic | `feat/demo-recovery-quality-1288-1109`, PR 1331 OPEN against `main`; published head `581207e18fedd66d9e24704a663dbb5f7b870d50` (hosted `src-agents` FAILURE on E501, `src-api` in progress at read time) |
| Checkpoint source | local `3483815492f331b1254d46bee7be783584977ef2`, tree `3aebb1da13c452da48f49da1b8d063a3df1fbdd0`: the parent head plus two unpublished commits (E8 plan and the E8 line wrap, AST-equal); contains main `a04668ae` and is 0 commits behind it; E8 is under independent assessment and no hosted success is assumed |
| Documents (unchanged, statuses not promoted) | BRD 0.21.0 draft `34d88395`; PRD (Zava Forward) 0.21.0 in-review `c788b917`; PRD (proper-warm) `f7f9b767`; addendum `28c19242`; original `0aec2d80`; ADRs 0001 `d42fa5c4`, 0002 `cbe21530`, 0003 `d6064539`, 0004 `9406c2e7`, 0005 `4d610335`, 0006 `956da1a3`, 0007 `abb21088` (identical at HEAD and `origin/main`) |

### Merged-main Blob observations (source-qualified, historical reuse)

* The Blob archive wave adds the ranking archive Blob adapter, publication and runner, store wiring, the `/api/ranking/publish` uncertain-write handling and Bicep policy tests. Main's own unit tests exercise it with fakes; no live or emulated Blob service, immutability policy, remote atomicity or from-empty deployment was observed here (owners #1258, #1259, #136).
* Retained raw logs from the Quality parent's main-integration run at the tree of `2aa038043` (session files `logs-1288-main-integration/`): Core `ranking_archive_blob` 26, `ranking_publication` 57, `ranking_publication_runner` 53; API `ranking_publication_wiring` 36; infra `test_bicep_policy` 59; all OK, no skips. These are historical, not fresh at this head: `git diff 2aa038043 HEAD -- src infra tools .github '*.toml'` changes only `dispatch.py` (E8) and bot score data.

### Parent-topic Quality observations (not main)

* The Quality delta against main is 144 files and touches no ranking, Blob, infra or Bicep file. The only shared file is `server.py`, where both intents were preserved by the recorded ordinary merge.
* Historical reuse from the same retained logs: assistants 120 OK (58 skipped, disposable SQL Server needed), assistant release 54 (4 skipped), sensor c7 45 (7 skipped), sensor e2 62 (31 skipped), simulation lane 30, transport deadline 7, inventories 29, consumption 17 and 42, input bounds 6, sensor consumer 47. Summed from the retained logs: 761 discovered, 100 skipped. A figure of 861 discovered appeared in a task statement; it is not reproducible from the retained logs (difference exactly 100) and is not used here. Agents 303 OK at the E8 wrap (`logs-1288-e8/unittest-after.log`) is a local result for that one line wrap, not a hosted result.
* SQL Server legs remain historical (605 with one skip at `5827ebede`); no SQL was rerun here. The real-provider simulation route is code-disabled; the ordinary-assistant post-fence suspension risk, local-only socket cancellation and final SQL refusal-audit persistence remain unproven.

### Observation O1 (one local run, adverse)

Selected before running (plan committed `1b1c3f73`): `python -m checks.quality_sensors_browser_check --out results.json` from an owned `mktemp` directory under one nonqueued `flock -n /tmp/ama-rpi-heavy.lock` (the lock was free; the holder was this run), in an `env -i` sanitized environment, with an owned `mktemp` venv (editable `src/core`, `src/agents`, `src/api`; Playwright 1.64.1 installed in that venv only after a real `ModuleNotFoundError`; Chromium from the existing user cache; Python 3.12.3). Constructed synthetic fixture, mock provider, SQLite store, loopback only; no model, Azure, credential, private data or default `ZF_DATA`. Axe was not run (bytes not supplied). Window 2026-11-09T20:56:52Z to 20:57:05Z.

* Exit 1. Twelve checks passed before the failure: the authorised Quality request reaches the mock provider; the captured snapshot holds retained readings; displayed reading ids and values equal the captured snapshot; the attributed unapproved flag cites readings the model was given and offers no approval control; withheld consent shows no readings table and is not reported as missing; stale readings are labelled stale, not live; unavailable readings and unavailable capture are explicit; the simulation panel is labelled synthetic and its readings equal the stored simulation readings.
* The step "Request Simulation Proposal" failed: the check expects `Proposal stored as unapproved`, but the panel shows `Not sent (real-provider-route-unavailable) ... nothing was sent to a model`. This is the intended guarded-off behavior of commit `cf3f84692` (E7, newer than the check's last change `c8afa77bb`), which updated the lane unit tests but not this browser check. Cause confirmed by the source, the panel text and the unit-test expectation; it is a stale check, not a product defect. The later checks (stored-proposal counts, rotation, role denials, manual path) did not run, so they are unobserved at this head.
* Raw stdout, stderr, exit, window, versions and install logs are retained in the coordinator session files `observed-440-bq-2055/` with `SHA256SUMS`, and the owned scratch directory is preserved, not deleted. No owned process remained afterwards. The run is local synthetic engineering evidence only: no assistive-technology, actual-model, human, Fluent or merged-main claim.

### Document-qualified trace

| Statement | Document-qualified link | Status |
| --- | --- | --- |
| Controlled gates before transitions; human approval, consent and quality decision stay with named humans | PRD (Zava Forward) FR-008 | Fixture and unit observed on the parent topic; no actual-model or human acceptance |
| Independent per-measure quality-disposition record linking checklist evidence, provider submission and reviewer acceptance | PRD (Zava Forward) FR-017 (quality-disposition record); FR-016 is the provider-package record | The retained-sensor journey is advisory display of synthetic readings against a mock model snapshot; it does not establish FR-017 |
| Resident or complaints requirement IDs | none asserted | Earlier join mistakes are preserved and not copied |
| Src layout and distributions | ADR-0006 | Editable installs resolve to this worktree |

### Unmet matrix and owners

| Gap | State | Owner |
| --- | --- | --- |
| Quality browser journey after the simulation step; browser check stale versus code-off route | Observed adverse, minimal fix is to update the check expectation to the unavailable and manual-route outcome and keep a stored-proposal seed path, with a regression run of the same command | #1288 (existing parent, within its recorded finite correction grant; owner authorization to use it is not inferred); no new issue proposed |
| Quality merged-main status | Not merged; PR 1331 hosted checks incomplete; E8 unpublished | #1288 |
| Live Blob, immutability, remote atomicity, from-empty deployment | Unknown, deferred | #1258, #1259, #136 |
| Actual-model AI, real-provider route, ordinary post-fence risk, final SQL audit | Code-off, unproven | #1288 |
| Priority-order recurrence, startup cause | Unknown | #1292 |
| Axe, assistive technology, human acceptance | Not run | #440 later criteria |

Recommendation: CONTINUE; hold Quality merged-main claims, #1288 closure and dependent expansion, and the whole #440 and Major HVE criteria; no pivot, deferral or requirement relaxation is inferred. Independent repairs may continue.

Final merged-main resume requirement: after PR 1331 actually merges, fetch `main`, prove the merged source tree and its hosted checks, rerun the O1 command once (or its corrected successor) at that tree through one nonqueued admission, and then re-evaluate this checkpoint as a separate merged-main qualification. Until then every Quality statement here is parent-topic only.

## Merged-main Blob and Quality qualification (2026-11-09, Refs #440 #1288 #1258 #1259 #136)

Separate dated continuation of the parent-topic checkpoint above, which is preserved unchanged, including its original exit 1 observation O1. It qualifies only what is implemented on merged `main` after PR 1331 and records one new observation M1. Records: [research](../../.copilot-tracking/research/2026-11-09-blob-quality-main-440-research.md), [plan](../../.copilot-tracking/plans/2026-11-09-blob-quality-main-440-plan.md), [details](../../.copilot-tracking/details/2026-11-09-blob-quality-main-440-details.md), [critique](../../.copilot-tracking/plans/critiques/2026-11-09-blob-quality-main-440-critique.md), [changes](../../.copilot-tracking/changes/2026-11-09-blob-quality-main-440-changes.md), [review](../../.copilot-tracking/reviews/2026-11-09-blob-quality-main-440-review.md). LOCAL ONLY, documentation only, no source, check or test change by this lane.

### Source identities and provenance

| Item | Identity |
| --- | --- |
| Merged `main` (fetched 2026-11-09T22:52:08Z) | `1b7a1719bee088ce2823bff45242e319bc928295`, tree `dd2bedcb8f4e73266e143be09bf72474c62db9fd`; squash merge of PR 1331 at 2026-11-09T22:47:40Z |
| PR 1331 final head | `f995774ca2415f6ae8903b6f45683dd55432eff1`; its tree equals the main tree (empty diff) |
| Former parent-topic head (E8 wrap) | `348381549`; not an ancestor of main (squash provenance) |
| Prior local checkpoint head | `6c2173dc3f5c6e35c7b30512f637f329fc883ddc`, preserved as an ancestor; the merge's first parent is `dbce15bc2a626e25c9e9aa869500ea9ba8c950aa` (the timestamp-correction commit above it) |
| Prospective records commit | `0a6f5a605f41a90d2aa67e36e52ed5b7b8473f03` (plus timestamp correction), recorded before the merge and M1 |
| Merge commit | `d0f806c9467fe0fe2f7d8b737567dd9e59315d01` (parents: the local checkpoint and main) |

The declared target of this local child is now `main` (the Quality parent topic has merged as a squash). The ordinary merge of `origin/main` conflicted in two source files because the local branch carried the parent's unsquashed commits and main the squashed result; the conflict intent was unambiguous (main is the reviewed final tree), both were resolved to main, and `git diff origin/main HEAD -- src infra tools .github` is empty. No rebase, force or remote write. The candidate therefore differs from main by documentation and tracking files only. Hosted checks at PR 1331 head, read with `gh`: all listed checks SUCCESS (src-api, src-agents, mssql, src-core, src-orchestrator, src-importer, rubric and the framework jobs). Durations, the independent APPROVE and the c160 MSSQL job (319 tests, 1 skip) are coordinator-reported or historical figures, not re-read by this lane.

### Source change since the original O1

Between the parent-topic head `348381549` and main the src delta is five files, +117/-10: `quality_sensors_browser_check.py` (E9: expect the guarded-off refusal and its manual-route text, assert that a refused request stores no proposal, then seed a proposal for the later steps), one line of `assistants.js`, and three API tests (journey pin, web copy audit, resident demo shed). No Blob, ranking, infra or Bicep file changed. The Blob wave (#1328) was already on main at `a04668ae`; Blob observations from the parent-topic section remain valid historical reuse. Original O1 stays exit 1 at `348381549` (12 checks, then the stale expectation; later assertions and axe not reached) and is not relabelled green.

### Observation M1 (new, source-qualified, local synthetic)

Selected before running (plan and details committed first). Environment: the owned venv of the parent-topic checkpoint (editable `src/core`, `src/agents`, `src/api` resolve to this worktree, whose `src` equals main; Python 3.12.3, Playwright 1.64.1, azure-storage-blob 12.31.0; `pip freeze` retained), Chromium from the existing user cache, `env -i` with `PYTHONPATH` to `src/api`, `src/api/tests`, `src/core/tests` and `src/agents/tests`, constructed synthetic fixture with a mock provider, SQLite in an owned `mktemp` directory and a loopback server, and the pinned axe 4.10.3 bytes (sha256 `880970c0...a68bb`, verified by the check). No private data, `ZF_DATA`, model, Azure, SQL campaign or credential.

Command (nonqueued, one heavy-resource admission each): `flock -n /tmp/ama-rpi-heavy.lock python -m checks.quality_sensors_browser_check --axe axe-4.10.3.min.js --out results.json`.

| Attempt | Time (UTC) | Outcome |
| --- | --- | --- |
| 1 | 22:53:43 | Harness error, exit 1: `ModuleNotFoundError: checks` (no `PYTHONPATH`); the check did not start |
| 2 | 22:53:53 | Harness error, exit 1: `ModuleNotFoundError: release_support` (test helper path missing); the check did not start |
| 3 | 22:54:02 | Admission refused, exit 1, no output: lock held by another lane (holder named from a live `fuser` and `ps` read at 22:54:04Z, `flock` PID 3349620 running `unittest ... test_timecapture_copy.py` in the issue 153 worktree; that read was not saved to a file, only the empty log and exit 1 are retained); not queued, not killed |
| 4 | 22:54:17 to 22:54:31 | Lock free; this run was the holder. Exit 0, 30 checks passed |

Attempts 1 to 3 are harness or admission failures of the invocation, not observations of the product, and their logs are retained. No owned process remained after attempt 4.

Observed behavior labels (attempt 4): the authorised Quality request reaches the mock provider; the captured snapshot holds retained readings and the displayed reading ids and values equal it; the attributed flag is unapproved with no approval control; withheld consent shows no readings table and is not reported as missing; stale readings are labelled stale not live; unavailable readings and capture are explicit; the simulation panel is labelled synthetic; the guarded-off real-provider route refuses and points to the manual route, and a refused request stores no proposal; with a seeded (synthetic, fixture) proposal the panel says how many readings it was given and cited, including one of twelve and zero cited, keeps them after rotation; the denied role sees no readings and the sensor API denies it too; no page errors. The seeded proposal is a fixture rendering, not model output, and is labelled separately from the refusal path.

Axe, separate from the labels (WCAG rule set of axe 4.10.3, scripted states): 0 violations in all seven scans. Incomplete results remain: `color-contrast` (impact serious) needs manual review in five of the seven scans (unapproved flag 3 nodes, withheld 3, unavailable 3, simulation panel 2, and simulation panel with supplied and cited readings 2). Zero violations with serious contrast incompletes is not WCAG conformance, not an assistive-technology result and not Fluent 2 or human acceptance.

Raw evidence (coordinator session files `observed-440-bq-main/`, `SHA256SUMS` verified; scratch preserved, path in `scratch-path.txt`): stdout, stderr, exit and start and end times per attempt, `m1-results.json`, `pip-freeze.txt`, `axe.sha256`. The `http-error ... client-disconnect` stderr lines are server-side teardown notices from the loopback fixture, not check failures.

### Reuse of historical evidence

| Evidence | Basis for reuse |
| --- | --- |
| Hosted Core, API, Agents, orchestrator, importer, MSSQL, rubric at `f995774` | Main tree equals the `f995774` tree, so hosted results at that exact head cover identical executable inputs; read via `gh`, not rerun here |
| c160 MSSQL 319 tests, 1 skip | Historical, qualified: it does not by itself prove a specific unexamined refusal-event transaction or second-connection contract, or Azure SQL |
| Parent-topic local logs (761 discovered, 100 skipped) and Blob suites | Historical for their trees; the 861 figure remains unreproducible; no local broad rerun |

### Document-qualified trace (statuses not promoted)

| Statement | Document-qualified link | Status after M1 |
| --- | --- | --- |
| Controlled gates; human approval, consent and quality decision stay with named humans | PRD (Zava Forward) 0.21.0 in review, FR-008 | Fixture and local browser observed on main source: no approval control on flags or simulation, consent withheld and role denial. No actual-model, human or live acceptance |
| Per-measure quality-disposition record; provider package | PRD (Zava Forward) FR-017 and FR-016 | Not established by the advisory retained-sensor display |
| No resident or complaints requirement ID asserted | BRD 0.21.0 draft and PRD (documents' numbers collide, so always document-qualified) | Earlier join mistakes preserved, not copied |
| src distributions and layout | ADR-0006 | Editable installs resolve to this worktree |
| Blob configuration and ranking publication | ADR set as listed in the parent-topic trace | Merged-main source and historical suites only; live Blob not observed |

### Gaps, owners and recommendation

| Gap | State | Owner |
| --- | --- | --- |
| Actual-model demo, ordinary post-fence suspension risk, local-only or remote cancellation, final SQL refusal-audit persistence, Azure SQL | Unproven, unchanged | #1288 (no closure claimed) |
| Live Blob, immutability, remote atomicity, from-empty deployment | Unknown, deferred | #1258, #1259, #136 |
| Serious `color-contrast` incompletes; assistive technology, consent, human acceptance, Major HVE, whole #440 | Open | #440 later criteria and existing accessibility owners; no new issue |
| Priority-order recurrence, startup cause | Unknown | #1292 |

No new defect was confirmed: the original O1 red was a stale check, corrected on main by E9, and M1 observed the corrected successor green. Recommendation: CONTINUE. Affected closure of #1288, #136 and #440, dependent expansion, and the Major HVE criterion stay on hold for the unmet criteria above; independent lanes may continue. No pivot, deferral, requirement relaxation or document approval is inferred. Source corrections need their own scoped route; this lane consumed no cycle of any other issue.

## Quality M2 current-main qualification (2026-11-10, Refs #440 #1288 #891 #184)

Separate dated continuation of the merged-main Blob and Quality qualification above, which is preserved unchanged. It is a documentation-only record: it qualifies merged Quality persistence (PR 1331) and the merged #891 transport-accounting correction (PR 1339) at current `main`, and classifies the already executed H0, H1 and H2 SQL observations. It runs nothing, repeats no finance #1234 checkpoint, ticks no criterion and approves no document. Records: [research](../../.copilot-tracking/research/2026-11-10-quality-m2-record-440-research.md), [plan](../../.copilot-tracking/plans/2026-11-10-quality-m2-record-440-plan.md), [details](../../.copilot-tracking/details/2026-11-10-quality-m2-record-440-details.md), [critique](../../.copilot-tracking/plans/critiques/2026-11-10-quality-m2-record-440-plan-critique.md), [changes](../../.copilot-tracking/changes/2026-11-10-quality-m2-record-440-changes.md), [review](../../.copilot-tracking/reviews/2026-11-10-quality-m2-record-440-review.md) and [state](../../.copilot-tracking/rpi-sessions/2026-11-10/quality-m2-record-440-state.json). The observations it relies on are in the merged records for [H0 and H1](../../.copilot-tracking/changes/2026-11-09-issue-1288-merged-sql-proof-changes.md) ([review](../../.copilot-tracking/reviews/2026-11-09-issue-1288-merged-sql-proof-review.md)) and [H2](../../.copilot-tracking/changes/2026-11-10-issue-1288-h2-matching-context-changes.md) ([review](../../.copilot-tracking/reviews/2026-11-10-issue-1288-h2-matching-context-review.md)).

### Identities and covered changes

| Item | Identity |
| --- | --- |
| Current `main` (fetched) and start of this record | `32221a8459ff5c42d45be1dd86adccb5fcb4c1d6`, tree `74107550f69ce77108f15961d16e1e80f363338d`; squash of PR 1342 at 2026-11-10T01:01:55Z |
| PR 1331 Quality retained-sensor evidence and guarded AI request (merged, trigger) | `1b7a1719bee088ce2823bff45242e319bc928295`, 2026-11-09T22:47:40Z; head `f995774ca2415f6ae8903b6f45683dd55432eff1` |
| PR 1339 #891 witnessed transport-attempt accounting (merged) | `ddeebd01694ddb46b456451d9ac6390347e51aaa`, 2026-11-10T00:17:56Z; head `1692b2315b59b6275a35a467af366c47ae72dfaa`; tree `b917297ef34bc3e7e7948f9e46ffe6b7e66e6c88` |
| PR 1341 importer refusal CLI (merged, unrelated) | `5318f738f6bc58a10a9d4df1ca18ae51c1547a79`, 2026-11-10T00:54:31Z; changes `src/importer` and tracking records (the rubric score file moves via separate later bot commits); excluded from this qualification (surface identified, not assessed) |
| PR 1342 tracking-only H0, H1 and H2 evidence (merged) | `32221a8459ff5c42d45be1dd86adccb5fcb4c1d6`; head `d41195a274b921e320f94b65e8483b6022103c85`; records only, no hosted checks because of path filters |
| Excluded, not merged | PR 1338 (aftercare, open, stacked base `feat/demo-quality-workflows-89-1109`) and parent epic #149 (open); no functionality of either is accepted here. Shared hooks of #132 and resident-decision modules of #1238 untouched |

Hosted CI was read with `gh` and not rerun. PR 1339 head `1692b2315` passed src-core, src-api, src-agents, src-importer and mssql; PR 1341 head `80cc8363c` passed too. Neither head tree equals the merged tree (the 1339 head predates the independently merged #1332 `resident_decisions` change; the 1341 head predates the #1339 files), and merges to `main` ran only the rubric scorer, so no exact-head hosted `src-ci` success exists for current `main` and none is claimed. The hosted `mssql` job selects `test_mssqlstore`, `test_lawstore`, `test_assistants.Mssql*` and `test_resident_aoai_sql`; it selects no `test_quality_sensors*` class, so the Quality SQL contracts are local-only evidence.

### Source equivalence and classification of H2

H2 ran at a head that was `ddeebd01` plus tracking-only records: merge `5d0460dd6c05312d0a905e69774d561c7ab8fc59`, tree `230c976d5ceaedea7515683f1746f685cc71d096`, two tracking timestamp corrections uncommitted (dirty 2). Read-only Git comparison on 2026-11-10:

* `src/core` is `7a83bae4adfa`, `src/api` is `ea090b15e073` and `src/agents` is `db7717006298` at `ddeebd01`, at `5d0460dd6` and at current `main`: identical subtrees.
* `git diff ddeebd01 HEAD` and `git diff 5d0460dd6 HEAD` over `src`, `infra`, `tools` and `.github` show only the importer files of PR 1341 and `.github/rubric/scores/latest.json`. No Core, API, Agents, orchestrator, infrastructure, tool or workflow byte changed.
* No Core, API or Agents file imports `zava_forward.importer`; core imports neither agents nor api; agents import neither api, orchestrator nor importer (package boundary of ADR-0006 holds).

Classification: H2 is a dated local observation that applies to the identical Core, API and Agents surface at current `main`. It is not a new runtime, Azure or hosted observation, and it gives no freshness to anything outside that surface. No relevant code drift was found, so no acceptance stops for drift and no heavy check was rerun.

### Errata (original records unchanged)

* The merged H2 research, H2 review and the coordinator handoff say "unmerged 891 excluded". For source `ddeebd01` that is wrong: #891 (PR 1339) is included. It was true for the older H0 and H1 base `a8593a7a8`.
* H2 had no stub peer. The earlier research mention of a peer and 0 bytes was superseded by the applied plan amendment. There is no H2 measured byte or bytes-saved claim.
* The existing Quality selectors ran 30 tests with 29 passes and one SQLite-only skip; they are not 30 SQL passes. The earlier review phrase "30 existing tests ok" overstates this.
* Label correction (2026-11-10, correction C2): the first version of this section and the original research record called `b4791e0c22b1f1be` the task body digest. In raw `h2.json` it is `binding_sha`; the task body fingerprint is the distinct `task_body_sha` `cfc0f0a9922fd69f`. The raw file is VM-local and was read, not re-executed. No source, persistence or runtime defect follows.
* The H2 SQL admission was 2026-11-10T00:23:08Z, not 23:23 on 2026-11-09. The first two readbacks were wrong and the correction commits are additive history.

### Observed commands

Raw runtime artifacts are VM-local in the coordinator session files, are not committed and are not required to read the findings below. Hashes are recorded so the bundle can be matched if it is kept.

| Run | Source | Command identity | Result |
| --- | --- | --- | --- |
| H0 | `a8593a7a8`, tree `5113adcb2` | merged-SQL-proof selectors (33 selected) | 31 ok, 1 skip, 1 failure (`after == before`, flag status `not-current`): failed, inconclusive, preserved |
| H1 | `a8593a7a8` | one restart-context test, default-provider variant A then B | FAILED: A gave `release-denied`; the synthetic `fx-quality-evidence` row went from active revision 1 to revoked revision 2 and variant B then ran after the revoke. Which call revoked is unestablished; it is not classified as a bug or as intended; the A-then-B ordering is a harness confound |
| H2 test | merge `5d0460dd6` (equivalent surface) | `test_h2_matching_context`, harness `harness_h2_matching_context.py` sha256 `698c13ec5188f24e18d0d607331e1441beaf60e5b269fa83242bef4418f96ac4`, wrapper `sql-run-h2.sh` sha256 `68851d83f02127446b1d7c8c3d88ad5fee0b74fedff1dc832686df0f3a2940fe` | exit 0, Ran 1, OK, no skips, 3.7 s; one `flock -n /tmp/ama-rpi-heavy.lock` admission, exit 0 |
| H2 companion | same | 30 existing Quality MSSQL selectors | exit 0, Ran 30, OK, skipped=1, 29 passes plus one SQLite-only skip, 70.9 s |

Environment: SQL Server 2022 RTM-CU27-GDR 16.0.4305.5 container, image `sha256:cf8f0ab2ebe61feec2eed2629061a07d247f791c2a8ddda74a4ac9f06a291718`, Python 3.12.3, localhost only, container removed. `h2.json` sha256 `1285e610f60ea9595b4de48a3af8de55eb4d4d872692352ef8bb328bebbc44e6` (recomputed on 2026-11-10).

H2 values: the first service and independently constructed B and C (own matching-context providers, fresh stores, services and connections, same process reopen) all read flag `review-suggested`, actionable, no release denial, the same cited IDs (`sensor:SENS-SYN-1:LIVE-SENS-SYN-1-20261109T2350Z`, `sensor:SENS-SYN-1:R-ZF-1-000`), the same five reading pairs for Quality Inspector and Retrofit Programme Manager (other role labels refused), the same task state. Two distinct fingerprints are equal across them: the binding fingerprint `b4791e0c22b1f1be` (`binding_sha` of the first, B and C reads) and the stored task body fingerprint `cfc0f0a9922fd69f` (`task_body_sha` of the three raw reads). Eleven synthetic release rows stayed unchanged across 47 snapshots. B and C made zero provider calls and zero prompts. Both are truncated 16-hex fingerprints, not cryptographic byte identity; the equality result is unchanged by the label correction below.

Limits: same-process reopen, not an OS or VM restart; synthetic capturing provider, not a model; no Azure SQL, IoT Hub or hosted run. H0 and H1 stay adverse observations: H2 did not reproduce them under a matching context, but that does not disprove a defect or explain them (cross-base inference only). E11 succeeded; E12 and E13 are unused; no extra code correction, model grant or counter reset is made here.

### Document identities and trace

Draft and in-review are not approval. BRD 0.21.0 draft (`34d88395`), PRD for Zava Forward 0.21.0 in-review (`c788b917`), PRD proper-warm 0.13.0 in-review (`f7f9b767`), addendum `28c19242`, original case study `0aec2d80`, parity matrix `91b5d33d` (proposal for owner review). ADR-0001 and ADR-0002 Proposed (only the staff identity and role decision of 0002 is owner-accepted, 2026-10-24); ADR-0003 accepted with amendment, ADR-0004 and ADR-0006 accepted (2026-10-15); ADR-0005 accepted for synthetic development only (2026-10-16); ADR-0007 Proposed (2026-11-04), not accepted. Requirement numbers of the BRD and PRDs collide, so every ID is document-qualified.

| Requirement or decision | Architecture and contract | Tested code and journey | Class |
| --- | --- | --- | --- |
| PRD FR-050 simulated sensor monitoring creating only a human review task; BRD FR-048 consented in-use monitoring with provenance | `core/sensor_view.py`, `core/assistants.py`, `core/sensor_consumer.py`, API `GET /api/cases/{id}/sensors`, `web/assistants.js`, `web/ops.js` | `test_quality_sensors*` unit, SQLite, SQL and the browser check, plus H2 | Local observed (synthetic data); PRD AC-066 live IoT Hub, Azure SQL and real AI task is not run |
| Persistence and replay: retained readings, flag, task, withdrawal | SQL control index, guard triggers, dispatch hold, per-attempt gate before the first byte | H2 matching-context test and 29 companion passes; the one SQLite-only withdrawal test is skipped on SQL | Local observed on SQL Server 2022 container; Azure SQL and OS restart unknown |
| Auth and roles (PRD FR-003, FR-072, AC-144; ADR-0002 identity decision) | Role projection refuses all but Quality Inspector and Retrofit Programme Manager | H2 projection per role label; fixtures are synthetic | Local observed; synthetic release and role rows establish no real person, resident or model authority; real role enforcement in a deployment is implemented-unverified |
| Sensor consent and withdrawal (BRD FR-048, RULE-025) | Control index; withdrawal withholds values, citations, derived output and flags; absent index fails closed | Quality sensor suites | Local observed (unit, SQLite, SQL); no real consent evidence |
| Human approval (PRD FR-008, AC-010, AC-011) | A returned finding is a `review-suggested` flag that requests human review and approves nothing | Quality sensor suites, H2 | Local observed; the per-measure quality-disposition record (PRD FR-017, AC-020, AC-042) is not established by the advisory display |
| AI use and unavailable-AI paths (PRD FR-044, CON-009) | Real-provider simulation route code-off; private readings are never given to a real AI by the Agents worker or API composition; manual route remains when AI, store or release is unavailable | E2 tests and unavailable-AI tests | Local observed with synthetic provider; actual UI-to-model Quality proof is blocked |
| AI metering (PRD NFR-017, AC-109, AC-110; BRD NFR-012) | PR 1339 `DispatchWitness` and `count_dispatches()`: calls counted from the witnessed transport attempt; unwitnessed providers are an unverified assumption of one | `test_ai_dispatch_marker`, `test_chat_model` | Local observed accounting only; #891 criterion 2 (per-call gate, token and cost, privacy, retention and refusal conjunction) remains unticked |
| RAI release, suspension and restart authority (PRD FR-051, FR-053, AC-069 to AC-072, OQ-017) | Synthetic release rows only | H1 and H2 synthetic rows | Blocked: owner release, budget and role decisions are unassigned; the $700 transport authority of #184 is not a paid-model grant |
| Package layout (ADR-0006) | Import boundaries listed above | Git comparison | Local observed |

Evidence classes: local observed is the SQL Server container and unit rows above; Azure observed is none new; implemented-unverified is deployed role enforcement and the 1339 provenance fallback; not run (admission pending, no owner-approved deferral) are the actual-model walkthrough, IoT Hub, Azure SQL and OS restart; blocked is release authority and budget; unknown is the cause of the H1 revoke and exact-head hosted `src-ci`. Relevant blobs at current `main`: `core/ai.py` `7699f8509d4f`, `ai_consumption.py` `abd24acd4887`, `ai_transport.py` `4508686c6957`, `assistant_release.py` `c8ae720aed94`, `assistants.py` `4cb575163a49`, `sensor_consumer.py` `134d5d516c5a`, `sensor_view.py` `9937817472b9`, `simulation_lane.py` `5c26cfb06838`; `api/server.py` `187c3648fb13`, `web/assistants.js` `4312f85723cc`, `web/ops.js` `e3e56191bbe3`; `agents/chat.py` `ae03ad5f25e5`, `dispatch.py` `2e2306c62790`.

### Gaps, owners and recommendation

| Gap | State | Owner |
| --- | --- | --- |
| H0 default-provider denial and H1 revoke side effect, classification unestablished | Adverse, unreproduced under a matching context | #1288 with release machinery under #107; needs an owner-authorised read-only diagnostic first |
| Actual UI-to-model autonomous Quality walkthrough (IoT Hub, SQL, UI, model, flag) | Not run; blocked on admission and owner decisions (no requirement deferral approved) | #1288 criterion 8, #891 criterion 2, #184 |
| Release owner, budget and role decisions (OQ-017) | Blocked, not invented | owner |
| Quality SQL classes outside hosted CI; no exact-head hosted `src-ci` | Local-only evidence | #440 later criteria and #1288 |
| #891 receipt provenance for the unwitnessed fallback and test hygiene from the PR 1339 review | Routed later work | #891 |
| Azure SQL, OS restart, assistive technology, human acceptance, Major HVE, whole #440 | Open | #440 and existing owners; no new issue filed, no issue or board written |

No new defect is confirmed and none is asserted. Recommendation: CONTINUE. The affected closures of #1288, #891, #184 and #440 stay on hold, and so do expansions that depend on the actual-model proof; independent lanes (importer, finance, aftercare once merged) may continue. Resume conditions: the owner assigns release authority, budget and role decisions; a separately admitted finite live walkthrough is approved under #1288; a read-only diagnostic of the H1 revoke is authorised before any source fix; any later source change after current `main` requires comparing the Core, API and Agents subtree ids above and restarts the classification. Proposed fix route, not decided: only after that diagnostic, scoped under #1288 or #107. No pivot, deferral, requirement relaxation, approval or production acceptance is inferred.

## Merged-wave checkpoint (2026-11-10, Refs #440 #149 #153 #1238 #93 #96 #148)

Draft, local-only, not approved. This is the required completed-feature-wave checkpoint for four merged features, an actual local observation of one pinned merged source with a small targeted matrix. It is not a blanket full gate, not a repeat of the historical Quality M2 record above (inherited, not new runtime validation), and not a SQL, Azure, model, live or browser-accessibility acceptance. Earlier sections, their adverse outcomes and their original source-qualified limits are unchanged. Records: [research](../../.copilot-tracking/research/2026-11-10-merged-wave-440-1110-research.md), [plan](../../.copilot-tracking/plans/2026-11-10-merged-wave-440-1110-plan.md), [details](../../.copilot-tracking/details/2026-11-10-merged-wave-440-1110-details.md), [critique](../../.copilot-tracking/plans/critiques/2026-11-10-merged-wave-440-1110-plan-critique.md), [changes and execution](../../.copilot-tracking/changes/2026-11-10-merged-wave-440-1110-changes.md), [review](../../.copilot-tracking/reviews/2026-11-10-merged-wave-440-1110-review.md) and [state](../../.copilot-tracking/rpi-sessions/2026-11-10/merged-wave-440-1110-state.json).

### Identities, covered changes and exclusions

| Item | Identity (read 2026-11-10) |
| --- | --- |
| Pinned source | `da4f52abb5bfdc50acc9b9b8aa84cc42babc77fe` (PR 1348, squash 02:00:25Z), tree `823c9cba2e219c5810f4e289145cb4ebe5c7c6cf`; subtrees `src` `f8cf2443b124c0e8e089ea4f49ed6ef1eeebd6f3`, `tools` `74ad3cb586db`, `infra` `d94040329d54`, `.github/workflows` `29eb03ea759e`. Branch `docs/demo-merged-wave-440-1110`, clean at start; `src` tree unchanged after the runs |
| Fresh `main` at start | `git ls-remote origin refs/heads/main` at 02:04:16Z: `da4f52abb` (same as the pin) |
| Fresh `main` at end of runs | 02:10:18Z: `6f24e554aa22da67756006c5185a329c14101ec3`, a rubric bot commit (02:06:46Z) that changes only `.github/rubric/scores/latest.json`. `src`, `tools`, `infra`, `.github/workflows`, this pack and the reference index are identical to the pin. The bot commit is not merged here; nothing below applies to a later main or implies approval |
| Covered feature PRs (merged) | PR 1343 staff-time copy `a740072d1` (01:23:03Z); 1346 resident default-deny approval binding `0385ad6a5` (01:41:47Z); 1345 finance retained history and dependency integration `96afce427` (01:45:21Z); 1348 four-image rebuild adapter `da4f52abb` (02:00:25Z) |
| Inherited, not re-run | Quality M2 record PR 1347 `e9c98eb20` (documentation); scorer bot commits PR 1349 `933416991` and 1350 `5861d6d3e` (rubric score file only; applicable metadata, not feature delivery) |
| Hosted CI | The owner brief reports independent bounded review and 19 passing actual checks across the four source PRs. They were not re-read or re-run here; no exact-head hosted `src-ci` for the merged tree is claimed |
| Excluded, not in the observed source | PR 1351 (open; empty-queue helper and recipe change, #152), parent #89 aftercare component, blocked #132 intake hooks, the old a482 and R15 worker. The queue producer and CLI components already on main are not extended; the real queue-worker `serve` still fails closed and is not operational. No function of an unmerged sibling is observed or accepted |
| Issue states (read live) | #440, #149, #153, #1238, #93, #96 and #148 OPEN; no criterion is ticked and no issue is closed by this record |
| Documents (blob at pin) | BRD 0.21.0 `draft` `34d88395de861e9799eb9e24121a21c92c7a5adc`; PRD Zava Forward 0.21.0 `in-review` `c788b917bafaede215f326f0efc71e071a687f1c`; PRD proper-warm 0.13.0 `in-review` `f7f9b7675e60e49006127a374e1106ff18aae282`; addendum `28c1924285eed255e53c1e359e0ad98eedab1d22`; original case study `0aec2d8070117a647574b1fadc8cfbdd2af68598`; ADR-0006 package layout accepted 2026-10-15. Draft and in-review are not approval and none changes here |

### Actual local observation

Python 3.12.3 and node v24.21.0 in an owned virtual environment with editable installs of this worktree's `src/core`, `src/agents`, `src/api`, `src/orchestrator` and `src/importer` plus the declared `playwright==1.64.0` pin; import origins were printed under each run's path and lie inside this worktree (API runs list `tests` first so API and Core modules with the same name are not confused). Each run used `env -i` with only `PATH`, `HOME`, `TMPDIR`, `LANG`, `ZF_DATA` (owned scratch) and `PYTHONPATH` (plus `ZF_BROWSER_TESTS=1` for R6), so no SQL, Azure, model, provider or credential switch existed; no private data, real user, image build or push. Raw logs stay outside the repository and are not committed (`SHA256SUMS` of the 13 logs `bf60e679516048770d27feac96f02d3f7deb8424b7b72c15cdfe7acdb4ebe599`). Times are tool `date -u` readings, 02:06:02Z to 02:07:53Z.

| Id | Selection | Exit | RUN | PASS | SKIP |
| --- | --- | --- | --- | --- | --- |
| R1 | Core finance: `test_form_dependencies` 10, `test_form_review` 23, `test_form_review_pack` 8, `test_form_export` 9, `test_form_staging` 17 | 0 | 67 | 67 | 0 |
| R2 | API `test_form_staging_api` (14 tests in the module at this source: staging, held review and seven schema-CSV cases) | 0 | 14 | 14 | 0 |
| R3 | Core `test_resident_decisions` (JSON 110, SQLite-backed 129, SQL Server class 129, fake Azure 1, complaints route 1, priority query 1) | 0 | 371 | 239 | 132 |
| R4 | Orchestrator first invocation (`-v` before `discover`, my argument-order fault, usage error) | 2 | 0 | 0 | 0 |
| R4b | Orchestrator `discover -v -s tests`: `test_rebuild_azure` 39, `test_rebuild` 23 and five other modules | 0 | 112 | 112 | 0 |
| R5 | API `test_timecapture` 26 and `test_timecapture_copy` 7 plus 5 browser skips (no opt-in) | 0 | 38 | 33 | 5 |
| R6 | API `StaffTimeGuidanceBrowser` with opt-in, loopback Chromium, external requests aborted | 0 | 5 | 5 | 0 |
| R7 | API synthetic served staff journey: `test_case_journey` 31, `test_role_matrix` 13, `test_workbench` 5 | 0 | 49 | 49 | 0 |
| R8 | Core `test_scenario_manifest` 8, `test_needs_inventory` 11, `test_version` 3, `test_dependency_rule` 2 | 0 | 24 | 24 | 0 |
| R9 | `test_version` and `test_dependency_rule` in API (5), agents (6), orchestrator (4) and importer (4), one process each | 0 | 19 | 19 | 0 |

Totals of the final processes: RUN 699, PASS 562, SKIP 137, failures and errors 0. These are execution counts of the final processes, not a unique-test total (corrected in C3, 2026-11-10; an earlier wording here claimed 694 distinct tests and 562 distinct passes and is withdrawn). Known repeated executions: the five R5 browser skips are the tests R6 executed, and R4b and R9c both ran the same four orchestrator version and dependency-rule cases. No project-qualified deduplication of every log was done, so no aggregate unique total is asserted. Of the 137 skipped executions, 5 are those browser skips and 132 are in R3: 129 "opt-in owned loopback SQL Server", 1 "Explicit isolated synthetic Azure SQL database required", 1 "JSON file rollback only" (a backend exclusion on the SQLite-backed class) and 1 "SQL replay only" (a backend exclusion on the JSON class, executed and passed by the SQLite-backed class). Only 130 are opt-in skips of external SQL services, and none is a SQL Server or Azure SQL pass: SQLite ran, and no external SQL Server or Azure SQL service ran. Nothing here is all-backend acceptance. R4 is retained as an adverse invocation fault of this run (zero tests, no product failure) and is not counted; R4b is the same selection with the order corrected. R7 prints 24 handled fail-closed tracebacks "Rule evaluation unavailable ... law store is not loaded" from fixtures without a law store, the same pattern recorded on 2026-11-09 (37 then); no defect is asserted and its absence is not proven.

### Requirement trace (document-qualified)

BRD and PRD requirement numbers collide (for example FR-045 means different things), so each row names its document. Draft and in-review documents stay unapproved.

| Feature and contract | Requirement reference (document) | Tests and observed journey | Class |
| --- | --- | --- | --- |
| Finance held form report, dependency evidence, retained history, legacy copy Invalid-and-regenerate, schema CSV (PR 1345) | PRD 0.21.0 FR-038 to FR-041 (assisted form schema, staged candidates, individual accept/correct/reject, deterministic validation); no BRD row asserted | R1 67 and R2 14; named cases `test_history_is_integrity_covered_and_legacy_copy_is_invalid`, `test_edited_or_incomplete_saved_export_is_invalid_not_trusted`, `test_export_carries_ordered_detached_review_history`, `test_missing_bytes_block_stale_rejected_and_replaced_retained_history`, API `test_schema_csv_*` (denials, formula neutralisation, empty list, revocation) | Local observed (JSON and SQLite temp stores, constructed data). The earlier 67 Core and 14 API counts are historical context only; they match the actual current counts here. Finance sign-off, funder acceptance and a live funder return are not observed |
| Resident forwarding default-unconfigured DENY, supersession approval bound to evidence, binding mutation rejection (PR 1346) | PRD 0.21.0 FR-045 (resident-owned decision, task-limited authority) and BRD 0.21.0 FR-045 (representative authority) are different requirements; neither is asserted to be satisfied. No named activation requirement ID is asserted | R3 named cases (list in the changes record) ok on JSON and on the SQLite-backed store; SQL Server class skipped by design | Local observed (JSON, SQLite) for default-unconfigured denial, forged, substituted, restamped and legacy generic audit evidence not counted, changed binding withdrawn and immutable binding. Not observed: SQL Server, named human activation or approval, trusted resident binding, a real send (the receiver is synthetic) |
| Four-image rebuild adapter: build, tag, verification, explicit mapping, failure and resume, no-I/O dry run (PR 1348) | PRD 0.21.0 CON-009 (actual Azure hosting for accepted exercise builds); #58 owner cap override applies to that rebuild only | R4b 112 with `FakeAzure`: all four workloads from their source contexts, every tag mapped and passed explicitly, build failure stops before later builds and deployment, resume never treats the API tag as four-image readiness, unpublished image fails before deployment, default is a dry run with no Azure call, dry run lists four images without I/O | Local observed against a fake only. Implemented-unverified for a real build, registry, deployment and health. Blocked: no live rebuild admission (owner authority, all-in cost headroom, finite plan) |
| Staff time capture default off, DPIA and notice gates, manager-only audited activation, copy states (PR 1343) | PRD 0.21.0 PR-004 (staff time capture only with staff knowledge and a completed DPIA; off until the DPIA exists; not a performance rating); BRD 0.21.0 RULE-019 (OD-36 DPIA before event capture) | R5 33 pass and R6 5 browser pass; named `test_off_by_default_and_nothing_is_written`, `test_dpia_alone_does_not_switch_it_on`, `test_notice_must_be_acknowledged_before_recording_or_listing`, `test_enabling_is_manager_only_and_audited_through_the_api`, `test_report_suppresses_small_groups_and_lists_no_person` | Local observed on constructed staff and temporary stores. A real DPIA, DPO approval, staff notice acknowledgement and any live capture are not observed; accessible-copy review by people is not claimed |
| Synthetic served staff journey: boot, role projection, denials, error and manual paths | PRD 0.21.0 FR-003 and FR-072 (staff identity and roles), ADR-0002 staff identity decision | R7 49 (`test_case_journey` 31, `test_role_matrix` 13, `test_workbench` 5); R6 browser copy journey | Local observed with constructed users and the fixture login; ingress trust, tenant, assistive technology and real identities are not observed |
| Public scenario manifest, needs inventory, package and version boundary | ADR-0006 package layout | R8 24 and R9 19 in separate project processes | Local observed |

Evidence classes. Local observed: every row above on the fixtures named. Historical: the 2026-11-09 and 2026-11-10 SQL, browser and Quality records (H0, H1, H2, S1, #1326 campaign), the prior 67 and 14 finance counts, the earlier SQL38 C3 observation, and the 19 hosted checks reported in the brief; none was re-run. Implemented-unverified: the resident SQL Server leg of PR 1346, the real image build, registry and deployment path of PR 1348, deployed role enforcement. Blocked or not run: live rebuild, SQL Server and Azure SQL legs, IoT Hub, any model or provider call, hosted CI for the exact head, assistive technology, human approvals. Unknown: the H1 revoke cause and later-main behaviour.

### Preserved adverse results and limits

* The Quality M2 H0 failure and H1 revoke observations stay adverse and unclassified; H2 did not reproduce them under a matching context and does not disprove a defect. This checkpoint adds no Quality observation and takes no part in them.
* The earlier source-qualified limits stand: SQL runs observe only the classes they selected; fake builders, fake providers, constructed users and SQLite do not prove deployed workloads, auth, model behaviour, financial acceptance, resident consent or human approval.
* Model, release and budget gates are unproven: actual-model Quality proof (#1288, #891 criterion 2) still needs owner release, budget and role decisions (OQ-017) and an admitted live walkthrough; the USD 700 transport authority is not a paid-model grant.
* Trusted resident binding is unproven: the default is deny and the unconfigured route sends nothing, but no named activation, trusted binding source or human approval was shown. A passing denial test is not an approval.
* Live rebuild gates are unproven: the four-image adapter is only exercised against a fake; no image was built, pushed or deployed.
* No new defect was reproduced. The only adverse item is R4, a wrong argument order in this run's own command, corrected as R4b with its log kept.

### Gaps, owners and recommendation

| Gap | State | Owner and dependent gate |
| --- | --- | --- |
| Resident forwarding activation, trusted binding, human approval; SQL Server legs of PR 1346 | Not observed | #1238 and the resident-decision epic; holds any resident-facing live claim and closure of #1238 |
| Real four-image build, registry, deployment, health | Not run, blocked on owner authority and cost headroom | #148 and #440 rung 4; holds live rebuild and Azure-dependent acceptance |
| Staff time capture DPIA, DPO approval, notice, live capture | Not observed | #149 and #153; holds time-capture activation and closure |
| Finance live funder return, sign-off, SQL Server finance legs | Not observed | #93 and #96; holds closure only |
| Actual-model Quality walkthrough, release authority, budget | Blocked | #1288, #891, #184 and OQ-017 |
| Exact-head hosted CI for the merged tree, assistive technology, human acceptance, Major HVE, whole #440 | Open | #440 and existing owners |
| Queue-worker `serve` fail-closed and not operational; PR 1351, #89 and #132 | Excluded | their own owners |

Recommendation: CONTINUE. The affected epics stay open and only the dependent gates above stay on hold: #1238 resident live claims, #148 live rebuild, #149 and #153 activation, #1288 and #184 actual-model and live-dependent expansion, and #440 closure. Independent lanes (importer, finance without live funder acceptance, documentation, tooling, the excluded PR 1351, #89 and #132 once merged and assessed) may proceed. No fix, pivot, deferral, requirement relaxation or approval is proposed or granted. Resume conditions: the owner assigns release, budget and role decisions and approves a finite live admission; named humans activate and approve resident controls; a DPIA and DPO approval exist for time capture; a later source change after this pin restarts the classification by comparing the subtree ids above. This observation does not reset the #440 correction ledger (C2 of 5 spent, three remain) and grants no source correction.

Limits: single-session authored record; the producer reviewed it once natively and an independent exact-head assessment, hosted CI, human review and push are not part of it. Not claimed: approval of any document, closure or tick of any criterion, whole #440, #149, #1238, #93, #96, #148 or Major HVE acceptance, SQL Server, Azure, IoT Hub, actual-model, real-build, assistive-technology, production, legal, resident or professional approval, or a full gate.

### C3 addendum: corrections and PR 1351 empty-queue observation (2026-11-10, Refs #440 #152)

Draft, local-only, not approved. Correction C3 of five on the #440 ledger (two remain, no reset). The da4f52abb rows above stay historical local observations at their pin and are not retconned to the newer source. The original wave observation ended 2026-11-10T02:12:36Z, before PR 1351 merged at 02:15:38Z, so 1351 was correctly excluded then.

Corrections (append-only, original records unchanged): (1) the "694 distinct, 562 distinct passes" claim in the original table note and in the original changes record line 27 is withdrawn: 699 RUN, 562 PASS, 137 SKIP remain execution totals, at least nine executions are known repeats (five R5/R6 browser, four R4b/R9c orchestrator version and dependency-rule cases) and no unique total is asserted. (2) The log and index wording that called all 132 resident skips SQL opt-in is corrected to 129 SQL Server opt-in, 1 Azure SQL opt-in, 1 SQL-replay-only JSON exclusion and 1 JSON-rollback-only SQLite exclusion, plus the 5 browser skips later executed in R6. SQLite ran; no external SQL Server or Azure SQL service ran. The original raw logs and manifest `SHA256SUMS` (`bf60e679...e599`) were re-verified unchanged (all entries OK).

| Item | Value |
| --- | --- |
| Integrated source | merge commit `da842ed19` (parents `807c5ea67` the C2 candidate and `bcc99405c` main after PR 1351), tree `7d287ebd`; `src/` tree `e6d4e656`, identical to `origin/main` at `bcc99405c` |
| Main at start and end | `bcc99405c` at 2026-11-10T02:20Z; at 02:21:48Z `origin/main` is `2bfd5e075`, a rubric-bot commit touching only `.github/rubric/scores/latest.json`; not merged, source after the pin is not observed |
| Blobs | `workbench_browser_check.py` `b9241811`, `app.js` `6cb8ee4d`, `test_queue_empty_state.py` `e1f6c429`, `scenario-manifest.json` `27a1d3e6`, `needs-inventory.json` `cf20a635` |
| Environment | owned venv `/tmp/i440-1110-PIVEGs/venv` (Python 3.12.3, Node v24.21.0, Chromium 156.0.8078.4) with module origins proven under this worktree `src/` for core, agents, api, orchestrator and importer; `env -i`, synthetic loopback only; logs and manifest in `/tmp/i440-c3-1110-obs` (`SHA256SUMS` `63e6cb50...a1e9`), separate from the original logs |

| Run | Command | Start to end (UTC, tool output) | Result |
| --- | --- | --- | --- |
| C1 | `src/api` `python -m unittest -v test_queue_empty_state` | 02:21:12 to 02:21:12 | exit 0; 7 RUN, 7 PASS, 0 SKIP |
| C2 | `src/core` `python -m unittest -v test_scenario_manifest test_needs_inventory` | 02:21:12 to 02:21:13 | exit 0; 19 RUN, 19 PASS, 0 SKIP (Core classes only) |
| C3 | `src/api` `ZF_BROWSER_TESTS=1 python -m checks.workbench_browser_check` | 02:21:13 to 02:21:25 | exit 0; 108 PASS lines, 0 FAIL; seven non-Contractor roles each pass the "empty explanation only when the own queue is empty, unknown coverage never declared unrepresented" check; no-match search passes "not a statement about scenario coverage"; reflow lines at 320, 390 and 1280 CSS pixels pass; no uncaught JavaScript errors |
| C4 | SHA-256 of `workbench_browser_check.py` | at 02:21 | `56409ec2...ac7df9` equals the `recipe` digest in `scenario-manifest.json` |

These counts are this addendum's own and are not added to the 699. The C3 browser check is a larger served journey than the empty-text assertions, which this record attributes to the issue 152 change; which viewports each assertion uses was taken from that record and the log, not separately instrumented.

Trace join (document-qualified; the BRD 0.21.0 draft `34d88395`, PRD Zava Forward 0.21.0 in-review `c788b917` and PRD proper-warm 0.13.0 in-review `f7f9b767` are unchanged and unapproved): PRD Zava Forward AC-034 and AC-043 stay PARTIAL. Local observed: an empty own queue explains that coverage for the perspective is Unknown, a search or filter with no result is a search result, a populated queue has no explanation, an unverified coverage payload is ignored and the all-cases scope keeps its own wording, on constructed synthetic cases. Implemented-unverified or absent: no runtime coverage producer or trusted current-fixture provenance exists, so declared-gap statements are deferred to an owner-approved producer outside this change. Unknown stays Unknown; it is not zero programme work.

Adverse and limits: no failure and no new defect was reproduced. The tests do not prove real assistive technology, representative-user research, a WCAG audit or accepted role mapping. Still unproven and not claimed: actual-model release and budget, trusted resident binding, a DPIA, a live four-image rebuild, SQL Server or Azure SQL, hosted CI for the merge head and any named professional approval. Still excluded: #89 aftercare, blocked #132 and #133 hooks, and the old a482/R15 worker; real queue-worker `serve` stays fail-closed. Recommendation unchanged: CONTINUE, with the same dependent gates on hold. No closure, deferral, pivot or requirement relaxation. Records: `.copilot-tracking/*/2026-11-10-merged-wave-440-c3-1110-*` and the C3 state.

## Discovery CLI feature-increment checkpoint (2026-11-10, Refs #440 #125)

Draft, local-only, not approved. This is the recurring checkpoint after one completed feature increment: the read-only synthetic `discovery-demo` command (#125, PR 1355 `a0f7cf182`). It is a new periodic observation, not a correction: the #440 ledger stays at C3 of five (two left, no reset, none spent here). It is not a repeat of the earlier broad merged-wave record above and not a blanket gate. Earlier sections and their adverse results are unchanged. Records: [research](../../.copilot-tracking/research/2026-11-10-discovery-checkpoint-440-1110-research.md), [plan](../../.copilot-tracking/plans/2026-11-10-discovery-checkpoint-440-1110-plan.md), [details](../../.copilot-tracking/details/2026-11-10-discovery-checkpoint-440-1110-details.md), [critique](../../.copilot-tracking/plans/critiques/2026-11-10-discovery-checkpoint-440-1110-plan-critique.md), [changes and execution](../../.copilot-tracking/changes/2026-11-10-discovery-checkpoint-440-1110-changes.md), [review](../../.copilot-tracking/reviews/2026-11-10-discovery-checkpoint-440-1110-review.md) and [state](../../.copilot-tracking/rpi-sessions/2026-11-10/discovery-checkpoint-440-1110-state.json).

### Identities, scope and exclusions

| Item | Identity (read 2026-11-10) |
| --- | --- |
| Pinned source | `origin/main` `0d262beee2dfa6feca27680aa1d596111154c8d9` (confirmed by `git fetch` and `git ls-remote` at 04:27:31Z), tree `9679e7a97cfd`; subtrees `src` `b4349401011b`, `src/core` `148b928864ba`, `tools` `74ad3cb586db`, `infra` `d94040329d54`, `.github/workflows` `29eb03ea759e`. Branch `docs/demo-discovery-checkpoint-440-1110`, clean at start |
| Delivered change | PR 1355 squash `a0f7cf182` (merged 03:42:37Z), 12 paths: three Core source and test files, a README section and the 125 RPI records. `0d262beee` above it is a rubric bot commit that changes only `.github/rubric/scores/latest.json`; it is not product source and is not observed as a feature |
| Source blobs | `discovery_assistant_demo.py` `ff27c7a4ca6e`, `__main__.py` `a258a2abf15f`, `test_discovery_assistant_demo.py` `acc532c32c8c`, Core `README.md` `1cc9a1c7a09f`; helpers `discovery_assistant_boundary.py` `b2d036f03150`, `_drafting.py` `0ef21b8a7198`, `_evaluation.py` `a5e2b0476516` |
| Documents (blob at pin) | Discovery brief (ms.date 2026-11-04, no version field) `fee5a6e4895d`; BRD 0.21.0 `draft` `34d88395de86`; PRD Zava Forward 0.21.0 `in-review` `c788b917bafa`; addendum `28c1924285ee`; original case study `0aec2d807011`; ADR-0006 source layout, accepted 2026-10-15, `956da1a3b804`. Draft and in-review are not approval and none changes here |
| Hosted CI | PR 1355 metadata read, not re-run: independent exact-head review APPROVED by `github-actions`, `src-core`, `src-api`, `src-agents`, `src-orchestrator`, `src-importer`, `mssql` and the guard checks SUCCESS on the PR head. No hosted `src-ci` for the exact `0d262beee` is claimed |
| Issue states (read live) | #440 and #125 OPEN; #125's three criteria unticked, #440 criteria 7 and 8 open; this record ticks and closes nothing |
| Excluded | Unmerged 135 C4 and 1300 C2, retained 185 and 132, the current-live R10 and 4 November image (not current-main acceptance), the broad merged-wave surface, and any model, Azure, SQL or UI check |

### Actual local observation

Python 3.12.3 in a new owned virtual environment `/tmp/i440-disc-1110/venv` with an editable install of this worktree `src/core` only; `zava_forward.core.version` and `discovery_assistant_demo` import from this worktree `src/core/src`. Every run used `env -i` with `PATH`, `HOME` (an empty scratch home), `TMPDIR` and `LANG`, from `src/core` (unit runs) or an empty scratch directory (CLI runs); no `ZF_DATA`, SQL, Azure, model or credential setting, no private data, no network use by the product. Tool `date -u` readings 04:28:51Z to 04:29:23Z. Raw logs stay outside the repository (26 files; manifest `SHA256SUMS` `c81aa583a2f706601c97cb2ba639236938842f3fc80abd21c591ea2625ba3675`).

| Id | Selection | Exit | Result |
| --- | --- | --- | --- |
| D1 | Core `discover -s tests -p test_discovery_assistant_demo.py -v` (README command; includes the real-subprocess `InstalledCommandTests`) | 0 | 14 RUN, 14 pass, 0 skip |
| D2 | Core affected helper suites: boundary, drafting, evaluation, `test_discovery_register`, `test_discovery_flow` | 0 | 46 RUN, 46 pass, 0 skip |
| D3 | Core `test_version`, `test_dependency_rule` | 0 | 5 RUN, 5 pass, 0 skip |
| D4 | `python -m zava_forward.core discovery-demo` twice, JSON read back by a constructed assertion over the captured stdout only | 0, 0 | byte-identical (7995 bytes, sha256 `dd47e232...0a8e`), empty stderr. `NOT_READY`, 10 missing, 0 satisfied; `company_connection` `DENY`; connection not permitted; `query_approved_analytical_store` allowed as read-only policy; `write_source_system`, `contact_resident` and `rank_properties` `DENIED_BY_AUTHORITY_BOUNDARY`; `read_company_dataset` `NOT_ON_READ_ONLY_ALLOWLIST`; all five `dispatched` and `attempted` false; `model_used` false, `NO_DRAFTER` fallback, draft status `DRAFT_FOR_HUMAN_REVIEW`, no validated finding; `criterion_met` false with no human result pointer; `approved_solution` false, `UNAPPROVED_DESIGN_HYPOTHESIS`; hours design 60, install 12, survey 36.5 and the one unusable-timestamp gap match the constructed expectation (0 mismatches); three identical repeat digests; `overall_passed` true; `manual_path` present |
| D5 | No argument; `discovery-demo extra`; `discovery-demo --path x`; unknown subcommand `other` | 0; 2; 2; 0 | version line `zava-forward-core 0.1.0` for no argument and `other`; the two extra-argument runs print the explicit usage message to stderr and nothing to stdout |
| D6 | Same command under constructed marker environment (`ZF_DATA` to a nonexistent path, marker connection and key values, an unreachable proxy), plus a scratch listing before and after, plus `strace -f` of the clean run | 0; 0 | stdout byte-identical to D4 in both; scratch unchanged; the trace holds 118 lines with no `connect` or `socket` call and no write-mode open; the opens outside the interpreter, standard library, venv and worktree source are the dynamic-linker cache, a FIPS flag probe (not found), locale files, `/etc/localtime` and the scratch directory read for module search (C4 qualification, 2026-11-10: the retained trace also records `/usr/lib/ssl/openssl.cnf` opened read-only, so the list above is not exhaustive; no connect call or write-mode open is contradicted, the trace covers only the selected syscalls `openat`, `connect`, `socket`, `execve`, `unlink`, `rename`, `mkdir` and `write`, so it is not universal confinement evidence, and no new run was made) |
| D7 | `ruff check`, `ruff format --check`, `mypy` on the three delivered Python files | 0; 0; 0 | clean. Tool versions are ruff 0.17.3 and mypy 2.4.1, not the Core pins 0.17.1 and 2.4.0. The first mypy attempt under `env -i` failed to import (user-site not visible, `D7c-first-fault.log`, kept) and was rerun with the real `HOME`; no product failure |

Totals of the unit processes: 65 RUN, 65 pass, 0 skip, 0 failure or error. The 14 demo cases and the 46 helper cases are distinct modules; D3 is the project version and dependency-rule boundary only. There is no skipped case in this selection, and no SQL, Azure, browser, API, agents, orchestrator or importer suite was selected, so no result here extends to them. The D6 poisoning shows no dependence on those markers only; it does not prove the absence of every possible read.

### Requirement trace (document-qualified)

The PRD and BRD carry no requirement ID for the discovery assistant, so none is asserted; the BRD only links the discovery brief. The trace names the brief sections.

| Contract | Source (document) | Observation | Class |
| --- | --- | --- | --- |
| Deterministic code calculates, a model only drafts; calculation repeatable and traceable | Discovery brief, Proposed Assistant Concept and Evaluation Criteria (calculation repeatability, traceability) | D1, D4: constructed hours, references and one gap match; three identical digests; model absent | Local observed on one fictional fixture. Constructed expectation, not an analyst result; the conventional table reuses the same calculation, so no independent comparator |
| Read-only, no write authority | Discovery brief, Authority and Safety Boundary | D4, D6: write, contact and ranking decisions refused, nothing registered, dispatched or attempted, no write-mode open | Local observed policy decisions. Not observed: any real operational system, because none is connected; "no write access to operational systems" is unmet as a whole-#125 criterion |
| Readiness before any company-data connection | Discovery brief, Readiness Before Writing the Agent (ten items) | D4: `NOT_READY`, ten missing, `DENY` | Local observed that the gate refuses. Readiness is not satisfied; no accountable owner, approved access or reviewer exists |
| Compare with manual and conventional reporting; manual path remains | Discovery brief, Evaluation Criteria and Readiness (manual analysis and export remain possible) | D4: empty comparison, `criterion_met` false; `manual_path` present; works with no model or service | Local observed that the comparison is empty by design. The actual comparison is not performed |
| Entry point, version and package boundary | ADR-0006 package layout; Core README slice 4 | D3, D5: no-argument version line unchanged, extra arguments exit 2, no dependency-rule failure | Local observed |

Evidence classes. Local observed: every row above on the stated fixture. Historical, not re-run: PR 1355 hosted checks and its independent review, the earlier 60 discovery suite count recorded in the 125 review, all earlier checkpoint results. Implemented-unverified: any use of the helpers against company data. Blocked: Phase 0 sponsor nomination, owner validation and an approved extract, privacy and access approval. Unknown: later-main behaviour after this pin.

### Adverse results, limits and findings

* No product failure, no defect reproduced and no new issue filed. The one adverse item is a fault in this run's own command (D7c under `env -i`), kept as `D7c-first-fault.log` and rerun.
* Reading note, not a defect: the demo prints `allowed: true` for `query_approved_analytical_store` while the company connection is `DENY`. The field is a read-only allowlist policy decision with no tool registered, as the README states; a reader may still misread it, which is a wording risk for the human reviewer and not a reproduced fault.
* Deduplicated prerequisite: the subprocess cases need the package installed (the 125 review R2). This run installed `src/core` as the repository requires, and Core CI installs it; no `PYTHONPATH` workaround was used. No issue filed.
* Constructed-only evidence: the fixture is fictional, the expected constants are authored from it, and the fallback text is deterministic code, not AI. The CLI does not read an environment, path or store, so these runs say nothing about any approved company dataset.
* Not observed, still unmet: whole #125 (readiness list satisfied, no write access to a real operational system, actual manual and conventional comparison), Phase 0 and every named human approval, a current Azure model or UI acceptance, hosted CI for the exact main head, independent exact-head assessment, whole #440. Source artifact unchanged here, so no new Major coordinator HVE mutation.

### Recommendation

CONTINUE. The delivered CLI conforms to its documented boundaries on the pinned source for this focused matrix, and no fix or pivot is indicated. #125 and #440 stay open with no criterion ticked; dependent expansion that needs company data, an actual model or a human comparison stays on hold until the accountable owner, access approvals and a real comparison exist. Independent lanes may proceed. No approval, requirement relaxation, deferral or issue closure is proposed or inferred. Resume conditions: sponsor and data-owner decisions under #124, approved extract and access, then an owner-approved comparison under #125; any later source change after this pin restarts the classification by comparing the subtree ids above.

## Served import-refusal and exception-register post-integration checkpoint (2026-11-10, Refs #440 #73 #135 #1360)

Draft, local-only, not approved. This is a new bounded checkpoint after PR 1361 reached `main`. It is not a repair or reset of the Discovery checkpoint above: the #440 correction ledger stays at C4 of five spent with one remaining, none is spent here, no new corrective budget exists and no source fix is made. It is a focused documentation and evidence tier record, not the full or `--changed` gate and not a repeat of the earlier broad matrices. Earlier sections and their adverse results are unchanged. Records: [research](../../.copilot-tracking/research/2026-11-10-served-checkpoint-440-1110-research.md), [plan](../../.copilot-tracking/plans/2026-11-10-served-checkpoint-440-1110-plan.md), [details](../../.copilot-tracking/details/2026-11-10-served-checkpoint-440-1110-details.md), [critique](../../.copilot-tracking/plans/critiques/2026-11-10-served-checkpoint-440-1110-plan-critique.md), [changes and execution](../../.copilot-tracking/changes/2026-11-10-served-checkpoint-440-1110-changes.md), [review](../../.copilot-tracking/reviews/2026-11-10-served-checkpoint-440-1110-review.md) and [state](../../.copilot-tracking/rpi-sessions/2026-11-10/issue-440-served-checkpoint-1110-state.json).

### Identities, scope and exclusions

| Item | Identity (read 2026-11-10) |
| --- | --- |
| Pinned source | `origin/main` `1ee56da3a27ad39eb53eaede0b66dc4905f0d820` (confirmed by `git fetch` at the start of this task and equal to the worktree head; a fetch before commit showed `origin/main` `fe59ef56a0`, 2026-11-10T06:59:58Z, which adds only the rubric score file `.github/rubric/scores/latest.json`, with `src`, `infra`, `tools` and `.github/workflows` subtree ids unchanged, so the observations stay valid for that source and this branch is not rebased), tree `b56e2bc2165149f23a2ec31e31d4d648e04da4de`; subtrees `src` `4d7dc17fad54`, `src/core` `973b78bacab3`, `src/api` `1dc8eb03b13f`, `src/importer` `c6e324d1c3a0`, `tools` `432a4e8f7d74`, `infra` `d94040329d54`, `.github/workflows` `29eb03ea759e`. Branch `docs/demo-served-checkpoint-440-1110`, clean at start |
| Main acceptance | PR 1361 (`feat/demo-served-exceptions-73-1110` to `main`) merged 06:51:12Z as squash `1ee56da3a`; its tree equals the tree of the PR head `1fab5d04` and `git diff` of `src`, `infra`, `tools` and `.github` against the independently reviewed product head `af7b20a3` is empty |
| Contributing declared parent | PR 1357 (`feat/demo-served-import-refusal-135-1110` to the declared parent branch above) merged 05:17:41Z as `b0af68a3` into that parent branch, not into `main`. It is contributing history only; its hosted Importer run failed on mypy (`mssql_python` import-not-found, log kept in the Root folder) and the optional-driver override that cleared it travelled in the 1361 history. `main` acceptance is the 1361 merge and nothing earlier |
| Changed by 1361 (13 source paths against `736561ba`) | Core `exception_register.py`, `import_refusals.py` (new), `sqlstore.py`, `store.py`; Importer `__main__.py`, `exceptions.py`, `pyproject.toml`, README; API `role-screens.js` (empty-state wording) and `test_exception_register*.py`; Core `test_import_refusals.py` and Importer `test_import_exceptions.py`. Documentation and original RPI records of 73 and 135 also arrived and are not re-read as product evidence |
| Documents (blob at pin) | BRD 0.21.0 `draft` `34d88395de86`; PRD Zava Forward 0.21.0 `in-review` `c788b917bafa` (FR-066, AC-120 marked "Not run", NFR-019, AC-135); addendum `28c1924285ee`; original case study `0aec2d807011`; ADR-0006 source layout; this pack before this entry `abdecf2ee74f`. No ADR changes the exception contract. Draft and in-review are not approval and none changes here |
| Hosted CI | The guard `1361-final-merge-guard-1110.json` read 19 reported checks SUCCESS on the PR head `1fab5d04` (base `736561ba`), no closing references. That is PR-head metadata, not a run of the merge commit: commit-scoped runs read for `1ee56da3a` showed only a Dependabot graph run and a queued Capstone Rubric Scorer push run, so no Source projects CI is claimed for the exact main commit |
| Issue states (read live) | #440, #73, #135 and #1360 OPEN; #440 criteria 7 and 8 open; nothing is ticked or closed by this record |
| Excluded | Unmerged siblings 130, 111, the 149 children and 132, #144 container hosting, #185 IoT identity, the Discovery CLI observations (pinned at `0d262beee`, later Core subtree change, not re-run here), the earlier merged-wave surface, any live, Azure, model, resident or professional step, and whole-demo, whole-73, whole-135 or whole-440 acceptance |

### Actual local observation

Python 3.12.3 in a new owned virtual environment `/tmp/i440-served-1110/venv` created only after the first Importer test run failed (`E0`, kept; the missing-package cause is author-attributed, see the C5 qualification below). It holds editable installs of this worktree `core[dev]`, `agents`, `api[dev]` and `importer[dev]` (ruff 0.17.1, mypy 2.4.0, `mssql_python` present as a package dependency but no SQL Server running). `zava_forward.core`, `zava_forward.importer` and `zava_forward.api` resolve to `src/*/src` of this worktree; the shared checkout's installs were not used. Every run used `env -i` with `PATH`, `HOME` (an empty scratch home), `TMPDIR`, `LANG` and the explicit owned `ZF_DATA=/tmp/i440-served-1110/zfdata/zavaforward.json` (plus `ZF_STORE=sqlite` and an owned `ZF_SQLITE` in S1 only). Readings from `date -u` 07:01:15Z to 07:02:09Z. No real dataset, credential, cloud, provider, model or network use by the product. Raw logs stay outside the repository (15 files; manifest `SHA256SUMS` `4d7822b2730da2cbe8e0a0657b46228e5fe57a402a33cfad18de0b7225154430`; the two scratch scripts have sha256 `71aaa41a...ffb6` and `9b36c247...9149`).

| Id | Selection | Exit | Result |
| --- | --- | --- | --- |
| T1 | Core `discover -s tests -p test_import_refusals.py -v` | 0 | 21 RUN, 14 pass, 7 skip (the `MssqlProjection` class, reason `opt-in task-owned loopback SQL`); JSON and SQLite projection, rollback, retry, audit and repeat cases pass |
| T2 | Core `test_dependency_rule.py` | 0 | 2 RUN, 2 pass, 0 skip |
| T3 | Importer full `discover -s tests -v` (includes `test_import_exceptions.py` stage, view, transfer and `TransferFailureTests`) | 0 | 79 RUN, 79 pass, 0 skip |
| T4 | API `test_exception_register*.py` with `PYTHONPATH=../core/tests:../agents/tests` as the project README documents (register, operator, steward, unnamed manager, import-refusal register on SQLite and JSON, HTTP endpoint on the matrix server) | 0 | 51 RUN, 51 pass, 0 skip |
| T5 | API `test_role_screens*.py` | 0 | 19 RUN, 19 pass, 0 skip |
| T6 | `node --check` of `role-screens.js`, the one API source file 1361 changed | 0 | Syntax only; no browser rendering |
| T7, T8 | Importer `ruff check src` and `ruff format --check src tests` | 0, 0 | clean, 12 files formatted |
| T9, T10 | Importer `mypy src` (7 files) and plain `mypy`, the Source CI selector (12 files) | 0, 0 | no issues |
| S1 | Constructed served story: a synthetic non-workbook file staged with `python -m zava_forward.importer stage`, then `transfer` twice into a SQLite served store, the store reopened, then the register read for a named steward, a named operator and an unnamed manager | 1, 0, 0 | `stage` refused (exit 1, durable ledger entry); first `transfer` `added=1 already_present=0 stored=1 of ledger=1`, repeat `added=0 already_present=1`; source file and ledger hashes unchanged; steward sees one `failed_import` with the owner as configured, `Unknown` eligibility and the source hash matching; operator sees the source text "1 refused import file(s) are stored here ... and 0 are shown in this view" and no item; the unnamed manager is refused with `PermissionError`; the register states that rejected batches and other failures are not connected |
| S2 | `transfer` with `ZF_STORE=nonsense` | 2 | `Cannot transfer: the served store could not be opened ... Nothing was recorded.`, stdout empty, no traceback |

Totals of the unit processes: 172 RUN, 165 pass, 7 skip, 0 failure or error. The skips are the opt-in SQL Server class only. Tool versions are as pinned by the Importer `dev` extra. T1 to T5 overlap in subject with the historical Root selections (21 with 7 skips, 79 and an 80-test API group); T1 and T3 repeat the historical counts, but T4 and T5 are a different selection from the 80-test API group, so no equality is claimed.

### Historical observations (retain date and source; not re-run)

* `af7b20a3` (2026-11-10, parent 73): affected full-project suites (Core 2864 RUN with 347 skips, API 2584 with 542 skips), disposable MSSQL `ZF_IMPORT135_MSSQL=1 test_import_refusals` 21 OK and 0 skipped (first attempt refused by the sql guard with 7 setup errors, kept), JSON and SQLite restart and idempotency stories and ad hoc Chromium register screenshots (first run failed on a wrong URL, kept). Root did not repeat the MSSQL or browser runs.
* `27dab9b5` and `1fab5d04`: record-only and base-refresh commits whose source is byte-identical to `af7b20a3`; the independent Functional review (approve with comments, 0 Critical or High, one non-blocking Medium, now #1360) was of `af7b20a3`. Byte-identical code does not make those runs fresh evidence for the pin; only T1 to S2 above are.
* PR 1361 hosted checks (19 SUCCESS on the PR head, including `mssql`, `src-api`, `src-importer`, `src-core`) are read metadata, not repeated and not a result for `1ee56da3a`.

### Requirement trace (document-qualified)

| Contract | Source (document, blob at pin) | Observation | Class |
| --- | --- | --- | --- |
| Owned staff exception queue shows reason, case or reference, owner and next step; a handoff is not closed by delivery alone | PRD FR-066 and AC-120 (`c788b917bafa`, in-review, AC-120 "Not run"); BRD exception and staff-queue text (`34d88395de86`, draft) | S1 and T4: one refused import appears for the configured steward with reason, time, source hash, owner and manual next step; the operator sees a stored-versus-shown count; no approval or retry is performed | Local observed on a synthetic ledger and SQLite or JSON store. Document status unchanged; AC-120 is not satisfied as a whole (failed contact, overdue work and unaccepted handoffs are other sources) |
| No silent loss; absence is not an all clear | PRD AC-120, PRD exception wording and the register source text | S1, T1, T4: unconnected sources and not-yet-transferred refusals are stated; repeat transfer adds nothing twice | Local observed |
| Role scope and denial of unnamed staff, no cross-role disclosure | PRD NFR-019 and AC-135 (denial and privacy), role text at the pin | S1 and T4: unnamed manager refused and the refusal audited, other staff emails not exposed to the operator, unauthenticated refused | Local observed for the seeded fictional roles; real roles are not nominated (open decision on #135), so no real staff, resident or case access is observed |
| Manual path and no automation of approvals | Exception wording in the PRD and the register's placeholder runbook | S1: `transfer` prints "Nothing was retried or approved"; the register guidance is labelled a placeholder, not an approved runbook | Local observed text and behaviour; no human or professional approval observed |
| Unavailable and error paths | PRD AC-120 and Importer README | S2, T3: unopenable store exits 2 with "Nothing was recorded"; competing writer rolled back; committed-but-unconfirmed, partial and driver outcomes use distinct messages | Local observed for those injected cases. The generic `(OSError, ValueError)` branch is not exercised after a commit (see findings) |
| Source layout and dependency boundary | ADR-0006 | T2, T3, T4: no dependency-rule failure; Importer typing passed (T9, T10); Core typing not run in this checkpoint | Local observed |

Evidence classes. Local observed: every row above on the stated synthetic fixtures. Historical, not re-run: the af7b, 27dab and 1fab observations, the MSSQL 21-test run, the ad hoc Chromium stories and the PR 1361 hosted checks. Implemented-unverified: SQL Server persistence at the pin (T1 skipped its class), the register rendering in a served browser at the pin, the served HTTP path beyond the unit matrix server, and any real source ledger. Deferred: those same MSSQL and browser runs; the shared heavy lock `/tmp/ama-rpi-heavy.lock` was probed with a non-blocking `flock -n` and read free, but no exact maintained scoped served-browser harness for the register exists (the earlier browser story was an ad hoc script) and no SQL Server service is required merely for this documentation, so neither was started. Resume only on an explicit later coordination event with a maintained harness and nonqueued admission. Blocked: any step that needs a named steward or operator, a real ledger, an approved runbook, resident consent or a professional approval. Unknown: hosted CI of the exact `1ee56da3a` merge commit and later-main behaviour after this pin.

### Findings, owners and gates

* No product failure, no defect reproduced and no new issue proposed. Two first-attempt faults are this run's own and are kept: the importer suite reported `FAILED (errors=1)` before the editable install (`E0`, qualified below: only the tailed summary is retained), and `mypy src` checks 7 files while the Source CI selector checks 12 (`T9` then `T10`), so the CI-selector result is the one used.
* #1360 (OPEN, Medium, non-blocking, static, unreproduced, unfixed) is the existing owner of the generic transfer message: at the pin `src/importer/src/zava_forward/importer/__main__.py:160-161` reports "the served store refused it (...). Nothing was recorded." for any `OSError` or `ValueError`, while `SqlStore.save` commits before its final refresh. The selected tests exercise a pre-commit `ValueError` and the explicit committed-reload, partial and driver outcomes, but none injects an `OSError` or `ValueError` after the commit, so this run neither reproduces nor refutes it. It is not duplicated, waived or reset here, and creates no budget: the #135 correction C5 stays spent at zero left and any repair needs its own finite grant.
* Compared and unrelated to this path: #144 (container hosting), #185 (IoT identity), #111 (sensor analysis, unmerged) and #132 (contractor pack, unmerged). No finding of this run belongs to them.
* Reading notes, not defects: the refusal reason for a non-workbook file reads "did not pass the content scan (mismatch)", which is the importer's own scan-gate wording; the operator view shows only a count, by design, and a reader may misread it as an empty queue, which the source text explicitly counters.
* Limits: fictional bytes, SQLite and JSON only, in-process register reads for S1 (the HTTP endpoint is covered only by the unit matrix server), no resident, professional, legal, human or live approval observed, no assistive-technology or browser result, the model label of the witness is asserted and the witness is a writable local record, not attestation. Not observed and still unmet: whole #73, #135 and #440, SQL Server at this pin, hosted CI for the exact main commit, independent exact-head assessment of this documentation candidate, actual role nominations.

### Recommendation

CONTINUE for this integration scope. The served import-refusal path and its operator and steward presentation behave as documented on the pinned source for this focused matrix, and no fix or pivot is indicated. The only open product item is the non-blocking #1360, which blocks no dependent work. Gates: closing #73, #135 or #440 needs the remaining criteria with their own evidence (named role nominations, an actual served-browser and SQL Server observation at the then-current main, hosted CI and independent exact-head review, human and resident approvals), none of which this record supplies; a repair of #1360 needs a dated finite correction grant. Independent lanes #230, #231 and #153 may proceed. No requirement change, deferral, waiver, approval or issue closure is proposed or inferred, and required epic and human criteria stay unticked. Resume conditions: an owner decision on the roles and on any #1360 repair grant, and a maintained served-browser harness with nonqueued heavy-lock admission; any source change after this pin restarts the classification by comparing the subtree ids above.

### Independent review and C5 qualification (2026-11-10)

Draft, local-only, additive. Earlier text, the original review and all adverse records stay as written.

* Independent assessment: reviewer 19f0152 read the complete supplied diff and all ten changed records of `c4ed9f64b7f2c14d4c5d1a34e0a3b4d0111d3616` against `1ee56da3a27ad39eb53eaede0b66dc4905f0d820` and returned approve_with_comments: zero Critical, zero High, two nonblocking Medium documentation findings. It is a bounded documentation assessment, not publication, merge, hosted CI, whole #440 or product acceptance. The earlier self-executed review is not withdrawn or replaced.
* Finding 1 corrected: the dependency row said Core and Importer were typed clean. Only Importer was type checked (T9, T10). The Core observation is the dependency-rule test T2, which is not a type check. Core typing was not run in this checkpoint and is not claimed. No check was run to justify the old wording.
* Finding 2 qualified: `E0` retains only the tailed five-line unittest summary (`Ran 1 test`, `FAILED (errors=1)`) followed by `exit=0`. The command was piped through `tail -5`, so the printed `exit=0` is the `tail` pipeline status, not a producer pass. The producer exit, the exception text and the missing package name were not retained; the missing-package cause is author-attributed only. The `E0` file is preserved byte for byte, was not reconstructed or rerun, and is not reclassified. The later T1 to T5 direct exits and counts stand.
* Ledger: the earlier Discovery state C4 of five spent with one remaining was historical and is not changed by this record. This current #440 documentation correction uses the one remaining allowance under the standing owner five total, so C5 is consumed and zero remain. It is not five extra, a new pool or a reset, and nothing is transferred from #132 or #135 (the #135 C5 stays zero). No further source or correction cycle is authorized.
* Unchanged: 172 cases run, 165 pass, 7 opt-in SQL Server skips, 0 failures; the S1 and S2 observations are CLI and SQLite only, not browser; af7b, 27dab and 1fab stay historical and byte-identical code is not fresh execution; #1360 stays static, unreproduced and unfixed; no human, model or live acceptance; #73, #135 and #440 stay open.
* Conclusion: CONTINUE applies only to this bounded integration observation and the independent lanes #230, #231 and #153. It relaxes no requirement or permission and is not universal current-main proof. The independent reviewer must assess the complete C5 delta before publication; if a blocking finding remains after C5, stop and do not retry.

## Parent 149 coverage integration checkpoint (2026-11-10, Refs #149 #440 #153 #156 #230 #231 #233 #96)

Draft, local-only, not approved. This is parent 149's own integration candidate and a #440 checkpoint input: a normal merge of current `main` into the reviewed parent topic, then a focused DEMO-tier qualification of the combined source. It is not a feature redesign, not epic closure and not acceptance of any child. No correction allowance is minted or spent and none is reset. Records: [research](../../.copilot-tracking/research/2026-11-10/issue-149-coverage-integration-1110-research.md), [plan](../../.copilot-tracking/plans/2026-11-10/issue-149-coverage-integration-1110-plan.md), [details](../../.copilot-tracking/details/2026-11-10/issue-149-coverage-integration-1110-details.md), [critique](../../.copilot-tracking/reviews/2026-11-10/issue-149-coverage-integration-1110-critique.md), [changes](../../.copilot-tracking/changes/2026-11-10/issue-149-coverage-integration-1110-changes.md), [review](../../.copilot-tracking/reviews/2026-11-10/issue-149-coverage-integration-1110-review.md) and [state](../../.copilot-tracking/rpi-sessions/2026-11-10/issue-149-coverage-integration-1110-state.json).

### Identities, scope and exclusions

| Item | Identity (read 2026-11-10, 09:13Z to 09:25Z) |
| --- | --- |
| Input parent | `ae4b20007ec9bc1d4bd5dd3eef91445f29f5e50f`, tree `c3e755d07edf`, reached by a normal fast-forward from the clean local head `736561ba0cccb9beb69eea3ae0d3a997bd0dd9bd` (an ancestor); the same branch carries #1363 (#233), #1365 (#231), #1366 (#230), #1367 (#153) and #1372 (#156) |
| Input main | `d52f20a5198de7269f39daf794911545aee01ced`, tree `a817c8480a08`, confirmed by `git fetch` and `git ls-remote` at 09:18Z; no difference from the reviewed input of the brief. Merge base `736561ba0` |
| Merge | `git merge --no-ff origin/main`, commit `0e5758da2531564dbcceef889f1ee479c3c220f2`, tree `a9b51381c57e`, equal to the tree predicted before integration by `git merge-tree --write-tree`. No conflict, no hand resolution. Parents `ae4b20007` and `d52f20a51` |
| Main-only content (24 non-tracking paths) | #1361 served import refusals with the exception register (Core `import_refusals.py`, `exception_register.py`, `sqlstore.py`, `store.py`, importer), #1369 Held draft download (#96, default-OFF, synthetic local/password only; trusted-proxy refuses it; no Azure or Entra Held download or wiring claim), their API tests and checker, the pack, index, log and `src/api/README.md` additions |
| Parent-only content (12 non-tracking paths) | `app.js` (#153 handoff read failure guidance), the atlas, programme paging and role-screens checkers (#233, #231, #230), their unit tests, the #156 programme design Markdown, the atlas trace and profile review notes |
| Overlap | Only `docs/reference/README.md`, `docs/reference/log.md` and `src/api/README.md`; merged automatically. The parent-to-merge diff has no deleted line in those three; the merge-to-main diff changes only the parent's own lines. No source file overlaps. `role-screens.js` changed on the main side only, `app.js` on the parent side only |
| Source blobs after the merge | `role-screens.js` sha256 `64cabb328366` (previous `e6bc1a351cac`, now includes #96), `app.js` from #153. Scenario-manifest sources (`workbench-manifest.json`, `workbench_browser_check.py`, `dataset.py`, `test_workbench.py`) are unchanged on both sides, so no manifest or needs-manifest test is required |
| Documents (blob at the input parent) | BRD 0.21.0 `draft` `34d88395de86`; PRD Zava Forward `in-review` `c788b917bafa`; addendum `28c1924285ee`; `src/README.md` `b6e13012a836`; atlas trace `40ad47a4991d`; programme journey (#156, PROPOSED, PARTIAL, NOT APPROVED, NOT IMPLEMENTATION-READY) `bb6417d2a201`; this pack before the section `abdecf2ee74f` and after the merge. Draft and in-review are not approval and none changes here |
| Excluded | Pending #80 Closed CSV and #216 constructed report (not in main or in the input); PR 1371 Core `test_resident_showcase` collision (separately diagnosed, test not selected, neither hit nor waived nor fixed here); #1362 correction; Azure, SQL Server, scanners, images, model calls; the complete local gate and any receipt |

Classification: focused tier. The merge changes no workflow, gate tool, Dockerfile, permission, secret, deployment, schema or security control by this candidate, and no dependency manifest by hand (the importer `pyproject.toml` hunk arrived through main). Basis: the owner DEMO targeted-tier direction and the actual merge delta. A partial or `--changed` receipt is not produced.

### Actual local observation

Python 3.12.3; owned virtual environment `/tmp/i149-1110/venv` with editable installs of this worktree's `src/core`, `src/agents`, `src/api[dev]` and `src/importer`; ruff 0.17.1, mypy 2.4.0, Playwright 1.64.0 (the repository pins, not the global 0.17.3, 2.4.1 and 1.64.1, and not the editable installs that point to another checkout); Chromium 156.0.8078.4; axe-core 4.10.3 file `/tmp/axe-4.10.3.min.js` verified by the repository checks against the pinned digest. Browser work ran under `flock -n /tmp/ama-rpi-heavy.lock` (the lock was free at both admissions; each admitted run was a single nonqueued acquisition). Raw logs (34 files, manifest `SHA256SUMS` `f76081274fa1`) stay outside the repository in the Root evidence directory.

| Id | Selection (from the stated project directory) | Exit | Result |
| --- | --- | --- | --- |
| B1 to B5 | Baseline on the unmerged input `ae4b20007`: the focused API unit set, ruff, file-less mypy, handoff browser, and the role-screens, atlas and paging Chromium checks | all 0 | 102 unit run (4 opt-in browser skips), 9 browser cases pass, atlas 362 PASS, paging 89 PASS, five role-screen stories pass with axe |
| M2 | API `unittest` of atlas checker, handoff read guidance and API, role screens and conformance, programme screen, workspace paging, role endpoint inventory, workbench, exception register and screen, finance grants screens, Held download API, form staging API | 0 | 194 run, 190 pass, 4 skip (opt-in handoff browser cases) |
| M3 | `ZF_BROWSER_TESTS=1 unittest test_handoff_read_guidance` | 0 | 9 run, 0 skip: constructed rejection shows guidance and not an empty state, no automatic retry, session-ended keeps the sign-in path, abort and navigation paint nothing, success and empty unchanged |
| M4a | Core `unittest test_import_refusals test_atlas_screen_trace` first attempt without `PYTHONPATH=tests` | 1 | 2 import errors from this run's own command (kept as `M4a-core-unit.log`), not a product failure |
| M4a2 | Same selection with `PYTHONPATH=tests` (rerun after the command fault, not a retry of a product failure) | 0 | 38 run, 31 pass, 7 skip (the opt-in task-owned loopback SQL cases of `MssqlProjection`). `Atlas trace: complete` against the merged `role-screens.js` |
| M4b | Importer `unittest discover -s tests` | 0 | 79 run, 0 skip |
| M5 | API, Core and importer `ruff check .`, `ruff format --check .` and configured file-less `mypy` | 0, 0, 0 | API 138 files formatted, 217 sources typed; Core 235 and 288; importer 13 and 12; no issue |
| M1 | `role_screens_browser_check` default, `230`, `231`, `231q`, `231p`, `231qp`; `atlas_tensions_browser_check`; `programme_paging_browser_check`; main-owned `held_form_download_browser_check`, one admission, `ZF_AXE_JS` set | all 0 | PASS counts 47, 70, 36, 36, 47, 46; atlas 362 COMPLETE; paging 89; Held download 31 COMPLETE; zero FAIL. The six role-screen and atlas pass sets equal the baseline; the paging set differs only by the ephemeral port and the new `role-screens.js` blob |

Axe: axe-core 4.10.3 ran only in five role-screen selectors, 230, 231, 231q, 231p and 231qp (the programme stories at 1280 px on `main` only, no violations, `incomplete` empty where reported). It did not run in the default role-screens selector, the atlas, paging or Held download checks, which state so. Automation is engineering evidence only; it is not human, assistive-technology or WCAG acceptance.

### Requirement trace (document-qualified)

| Contract | Source (document) | Actual change and test | Class |
| --- | --- | --- | --- |
| Visible blocker owner and next action, reason and unknown not hidden | PRD SA-003, SA-007, AC-036 (in-review) | #153 `app.js` handoff read-failure text (reason, owner, next action; manual refresh, no automatic retry) with `test_handoff_read_guidance`, M2 and M3 | Local observed on constructed rejection. Whole AC-036 and human review unmet |
| Scope, reset and paging semantics on the programme queue | PRD AC-034 (in-review) | #230 `programme_paging_browser_check` (89 PASS) and role-screens story 230 (70 PASS) | Local observed for the constructed 60-case fixture and one intercepted failure per width. #156 design is PROPOSED/PARTIAL; M1 (empty page versus empty set) is unresolved and not decided here; implementation-unverified |
| Technical and Quality per-home withheld and positive states, case rationale | PRD AC-040 (in-review), SA-001 | #233 atlas checker (362 PASS), #231 stories 231, 231q, 231p, 231qp | Local observed on the synthetic home; the Quality Inspector omission of the technical change note stays unasserted (a #233 qualification) |
| Atlas themes traced to registered screens | atlas trace (hypotheses until #155) | Core `test_atlas_screen_trace` complete against the merged `role-screens.js` | Local observed (static) |
| Held draft download, native download and role boundaries | PRD SA-006 export principle (in-review), #96 | Main `held_form_download_browser_check` (31 PASS), `test_form_held_download_api` in M2 | Local observed on the default-OFF synthetic local/password path; Azure or Entra Held download not claimed |
| Plain-language and non-colour status, Fluent semantics, reduced motion | BRD NFR-008 and NFR-009 (draft), `design-system.md`, `content-standard.md` | No web file was edited. Static read against the fetched Web Interface Guidelines found no new anti-pattern in the two hunks; `app.js` keeps `role="alert"` for the failure text (not `aria-live="polite"`, an existing semantic retained) | Static observation only; whole NFR-008 and NFR-009 unmet |
| SA-009, SA-010, AC-035, AC-037 to AC-039, AC-041 to AC-043, NFR-001 usability evidence | PRD (in-review) | Not exercised by this candidate | Unknown or deferred; no claim |

Evidence classes. Local observed: every M row on synthetic loopback data. Parent-only integration: the #153, #156, #230, #231 and #233 contents before the merge (baseline B rows) and their history, which stay reviewed-parent records and not main evidence until published. Current merged-main evidence: the #96 and #1361 contents in the combined tree, observed here only by the selected tests and checks (their own CI and reviews are historical and not re-run). Implemented-unverified: any programme paging behaviour on real data, Held download under Azure or Entra. Blocked: #156 owner decisions and named reviews, assistive-technology and usability evidence. Deferred: SQL Server persistence (7 skips), full gates, hosted CI for this head. Unknown: later-main behaviour, #1362 correction balance.

### Findings, owners and gates

* No new product defect reproduced and no refactoring change made. No new issue is filed. No real defect or unrelated correction was needed, so the stop-and-route path was not used.
* Existing owners: #1362 (checker false positive: a `1` inside the recorded-at timestamp can mask the Current design version `dd`, and `10` or a duplicate label are missed; constructed, not a proven product defect; correction balance Unknown; the retained diagnostic ran Chromium 156 and Playwright 1.64.1; not resolved here and no checker was bypassed or weakened); #156 M1 and owner decisions O1 to O6; PR 1371 Core `test_resident_showcase` token collision (not selected, not waived); #153 original hosted type failure and PR-body Medium, preserved; #1360 stays as recorded.
* Adverse items kept: M4a command fault; the four unit skips (opt-in browser, covered by M3); the seven SQL skips; the witness implement-start qualification that reviewed parent content was committed before the boundary (the fast-forward).
* Gates not met by this record: independent exact-head assessment of the final local head, hosted CI for it, whole UX, WCAG, assistive-technology, human, content and design acceptance, #440 whole-checkpoint, epic #149 criteria (none ticked), no closing keyword. Refs only.

### Recommendation

CONTINUE. The merged tree integrates both histories without conflict and the focused local set passes with the parent baseline reproduced unchanged. No fix or pivot is indicated by this evidence. Publication stays blocked behind independent exact-head assessment of the final head and applicable hosted checks. Any change after this record (including a later main or rubric commit) restarts the comparison of the subtree identities above. No approval, deferral, requirement relaxation or issue closure is proposed or inferred.

## Nomination and UX integration wave checkpoint (2026-11-10, Refs #440 #130 #149 #153 #156 #1360 #1362)

Draft, local-only, not approved. This is a new recurring observation and documentation checkpoint after PR 1381 and PR 1376 reached `main`. It is not the old #440 C6 and spends no source repair budget; it makes no source fix and opens no issue. It is the focused documentation tier: no full or `--changed` gate, no heavy, SQL, image, model, cloud or private-data run, and no command was run by this task. It neither includes nor republishes the separate #440 CSV-learning record, whose frozen independent review is unchanged; this section, its index paragraph and its log entry are owned only by this record. Records: [research](../../.copilot-tracking/research/2026-11-10-nom-ux-retry-440-1110-research.md), [plan](../../.copilot-tracking/plans/2026-11-10-nom-ux-retry-440-1110-plan.md), [details](../../.copilot-tracking/details/2026-11-10-nom-ux-retry-440-1110-details.md), [critique](../../.copilot-tracking/plans/critiques/2026-11-10-nom-ux-retry-440-1110-plan-critique.md), [changes](../../.copilot-tracking/changes/2026-11-10-nom-ux-retry-440-1110-changes.md), [review](../../.copilot-tracking/reviews/2026-11-10-nom-ux-retry-440-1110-review.md) and [state](../../.copilot-tracking/rpi-sessions/2026-11-10/issue-440-nom-ux-retry-1110-state.json).

### Identities, scope and exclusions

| Item | Identity (read 2026-11-10) |
| --- | --- |
| Pinned source | `origin/main` `65c2ab9d947d1498dafd37e24a377d1ff503e86f`, tree `520d12561000e9dc596ed0b03f9f862a9240b32f`, equal to the worktree head at launch. Subtrees `src` `70d956b06f31`, `infra` `d94040329d54`, `tools` `432a4e8f7d74`. Branch `docs/demo-nomination-ux-checkpoint-440-1110` |
| Later main | A fetch during the task shows `83503b74e0e5f555382436c0ae27f64cd200971f` (tree `696c4acbe2ee`), a `github-actions[bot]` rubric commit whose only changed path against the pin is `.github/rubric/scores/latest.json`; `src`, `infra` and `tools` subtree ids are the same as at the pin. It is not merged here and no full-tree equality with the pin is claimed |
| Nomination wave | PR 1381 (`Refs #130 #81`, published head `210161bdc1779953c349049565312d6983e160fb`) merged 12:58:55Z as `0376606dc97a14ebd0cbc81bb8fe136e836a3d1b`, tree `0368d5e6689cb58be2606d255b7d20bd9e5d6011` |
| UX wave | PR 1376 (`Refs #149 #440 #233 #231 #230 #153 #156 #152`, head `621f29d29b363dfd25729079180bb33f94ba0b20`) merged 13:02:24Z as the pin `65c2ab9d9`. Child PR 1382 merged earlier (12:20:13Z) into the parent branch as `621f29d29`, not into `main` |
| Hosted checks | Each PR head showed 19 reported checks all SUCCESS (18 check runs and the `rubric/score` status), no closing reference. That is PR-head metadata. Commit-scoped runs read for `65c2ab9d9` were only 7 (one still in progress, the rest skipped or the agent activation set), so no Source projects CI result is claimed for the exact main commit |
| Product blobs at the pin | `app.js` `c735acad6350`, `panels.js` `5f37f2a71b4a`, `style.css` `32234917f66e`, `test_nomination_screen.py` `4d0481a27961`, `nomination_browser_check.py` `81cafcb4d434`, `workbench_browser_check.py` `0fbe0be3b0c3`, `src/api/README.md` `b117333c3e1d`, `scenario-manifest.json` `e6624d6d0c71` |
| Documents (blob at pin) | BRD 0.21.0 `draft` `34d88395de86` (FR-037, AC-065, RULE-005); PRD Zava Forward 0.21.0 `in-review` `c788b917bafa`; PRD Proper Warm 0.13.0 `in-review` `f7f9b7675e60`; ADR-0006 source layout `956da1a3b804`; ADR-0007 Proposed `abb21088a9bb`; this pack before the section `5f223b53b7ed`, index `28b3ec408855`, log `058338f4903c`. Draft, in-review and proposed are not approval and none changes here |
| Issue states (read live) | #130, #149, #156, #440, #1360, #1362, #1383 and #1384 OPEN; nothing is ticked or closed by this record |
| Excluded | Unmerged 136 and 175 Bicep; the #89 aftercare parent and its child #133 (merged into the parent, not `main`); held #132 and contractor identities; the #1384 checker fix; the old C6 and the CSV-learning record; any live, Azure, model, resident or professional step; whole-demo, whole-130, whole-149 or whole-440 acceptance |

### Consumed evidence (Root local runs, not re-run here)

Both Root runs used source-qualified local predictions, made before the merges, and an owned environment. The raw logs, versions and `SHA256SUMS` are in the Root session folder, not in the repository. Neither is a GitHub merge preview, an observation on `65c2ab9d9` or an Azure run.

| Record | Tested composition | Result as retained |
| --- | --- | --- |
| Nomination only (`handoff-130-current-main-caaf-1240`) | local merge of the published head `210161bd` into the then-main `caaf98914`, tree `36b16ae74700e3745e180106aed1931a2cf7352e`, equal to the `git merge-tree` prediction | API 11 selectors 120 OK with 1 skip, simulator admin 30, Core learning 21, Agents paired-command 21, API ruff, format (137 files) and mypy (217 files), `node --check` of the web scripts; the nomination and challenge browser checks passed with 3 nomination axe scans, zero violations, zero incomplete, and no non-GET request while viewing (six GET paths listed) |
| UX combined (`handoff-149-combined-verification-1230`) | parent `621f29d29` plus nomination `210161bd` plus `caaf98914`, tree `bb90e4d3ef9123696117523d7c47261f17968365`, `src` `70d956b06f31cabfd8321b4ee9c203ae8b21d89c` | API unit 379 run with 16 skips, nomination and resident API 25 with 1 skip, Core 88 with 7 opt-in SQL skips, Core integrity 35, six static runs exit 0, one non-queued heavy-lock acquisition; browser: handoff 9, role variants 47, 70, 36, 36, 47 and 46, atlas 362, paging 89, Held 31, workbench 124, progress 58, nomination three scans |

* Tree equivalence (Root proofs, read and not recomputed here): the actual main tree `520d1256...` differs from the tested UX tree `bb90e4d3...` only at `.github/rubric/scores/latest.json`, with equal `src` ids `70d956b0...`; the actual nomination-main tree `0368d5e6...` differs from the tested `36b16ae7...` only at the same file, with equal `src` `e1b868d2...` and `infra` `d9404032...`. This is current-metadata and tree equivalence for the source, not a rerun on the pin.
* Axe ran only in the named selectors: role variants 230, 231, 231q, 231p and 231qp, the progress states, and the nomination scans. Default roles, atlas, paging, Held and workbench ran no axe. Screen reader and human acceptance are "Not run" in the nomination output.
* The split of the 21 role-width observations into 15 empty-queue (five roles) and 6 populated-queue (two roles) observations was not independently re-derived by Root or by this task. The passing nomination browser output still contains law-store-unavailable tracebacks, assistants 503 and client-disconnect lines, so no zero-server-error claim is made.
* Independent records (Root): the UX combined review is approve_with_comments with zero new findings, the inherited Mediums #1362 and #1360 and the #156 M1 proposal still unapproved, with a fresh-guideline addendum; the nomination-only review is approve with zero new findings and the known Low heading hierarchy (h2 to h4 in `panels.js`, lines 326, 353, 369 and 385) OPEN. The fresh rules retrieval `web-interface-guidelines-fresh-1257.md` has SHA-256 `d246b026f4f29b5823a9cc857f9edf3d2507002e055e32040cadeaf3b38e0234`, re-hashed here and equal. No complete conformance, assistive-technology, WCAG or human content acceptance is claimed.

### Requirement trace (document-qualified)

| Contract | Source (document, blob at pin) | Observation | Class |
| --- | --- | --- | --- |
| Nomination and self-referral keep the original account with correctable identity, each with a named human owner; unknown is never "none"; a correction does not change priority automatically (FR-037, AC-065, RULE-005) | BRD `34d88395de86` (draft); PRD `c788b917bafa` (in-review); #130 body | The read-only `nominationPanel` in `panels.js` shows original and corrected accounts separately, "Not recorded" or "Unknown" for missing values, the named owner and review state by version, and states it does not contact a resident, decide eligibility, change priority or assign an owner | Static read of source at the pin plus Root local observation on a constructed synthetic fixture. Document status unchanged; #130 criteria 2 to 4 and 5 stay open |
| Read-only, no non-GET | #130 scope | The Root nomination browser run recorded zero non-GET requests while viewing; monitoring starts after the initial navigation and ends before the current-review navigation | Local observed on the predicted tree; scoped, not whole-system |
| Manual and non-AI route | PRD and BRD staffed-route text | The "Staffed non-digital route" and acknowledgement fields come from server record fields only; acknowledgement reads "Delivery unverified" and no assistant call renders them. The record states a recorded review is a staff record, not an approval or eligibility decision | Static read plus local observed; no staffed delivery or human approval observed |
| Roles and denial | PRD role text | `nominationPanel` returns nothing for a role without the fields and shows "No nomination or self-referral is recorded for this home." for an authorised empty list; unit test `test_authorised_empty_and_role_denied_differ` | Local observed on constructed fixtures; real role nominations are not observed |
| Resident and handoff read paths | #153 and PR 1376 scope | The disjoint `app.js` hunks (handoff read guidance and the Resident tab) compose; handoff browser 9 OK | Local observed on the predicted tree |
| Paging, empty and negative cases | #230, #231, #233, #152 scope | Paging 89, Held 31, workbench 124 (hidden-explanation and vertical-clipping constructed negatives) and progress 58 passed | Local observed; #156 M1 empty-page versus empty-set ambiguity stays an unapproved proposal |
| Source layout | ADR-0006 | No dependency-rule failure in the Core selections | Local observed |

### Evidence classes

* Local observed: only the Root runs above on the two predicted trees.
* Historic source-qualified: those runs, because the tested trees are not the pin; the source subtree equality is current-metadata equivalence read from Root proofs.
* Azure observed: NONE.
* Implemented, unverified: the nomination view and UX coverage on the exact merge commit, SQL Server persistence for nomination records, a served browser run on `65c2ab9d9`, trusted role binding, staffed acknowledgement delivery.
* Deferred or blocked: hosted CI for the exact main commit, device, screen reader and human acceptance, whole #130 criteria, the #156 M1 decision, the heading Low fix and any source correction. Their owners are named below.
* Unknown: the exact count of source corrections left on the nomination work and the actual GitHub merge-preview trees.

### Findings, owners and gates

* No new defect, no new issue and no source fix. Existing owners checked before any new issue: #1362 (atlas version assertion false positive) and #1360 (served transfer message) remain open and unwaived; #156 M1 remains an unapproved proposal; the heading hierarchy Low has no separate issue (an open-issue search found none) and is recorded in the #130 independent record, not duplicated.
* #1384 (workspace exhaustion checker alignment) stays with its owner. Root's ongoing diagnostic states current exhaustion proven for 4 and the missing-global case for 2, with the whole workspace browser check not green (delayed companion); this task did not reproduce it, and no whole-workspace acceptance follows. Its fix is excluded from this record.
* #1383 (rubric scorer failed on `901fea60e`) is OPEN with no comments. A later overall SUCCESS alone does not prove incident recovery, and no closure is invented. Rubric-only commits on `main` do not change the product source.
* Gates: the affected #89 UI-dependent publication and the whole epic gates remain awaiting Root consumption of this record. Whole #440 criteria 7 and 8, human and HVE approval stay unmet; no #132 or #133 budget is added; no requirement is relaxed.

### Recommendation

CONTINUE for this integration scope. The read-only nomination view and the UX coverage behave as retained on source-equal predicted trees, and no fix or pivot is indicated. Independent Bicep, backend and checker lanes may continue. Publication of this record needs independent exact-head assessment and applicable hosted checks; any later change restarts the subtree comparison. No approval, requirement relaxation or issue closure is proposed or inferred.

### Process record and limits

* First attempt (same task, slug `nomination-ux-main-440-1110`): the witness refused `plan-done` because of a missing comma in the worker's own state edit; `verify` exited 1; log sha256 `17a6744678fd59bc6a5bf98fb16bb3f393364e70b47d927a371966a6446b5466`. Its research, plan, details and critique are unchanged. The invalid state was archived byte-exact (sha256 `ee52a75c7c4ccc82a2e997807caeae9b910ac4291a5f74a009be1910ae81379e`) at `.copilot-tracking/evidence/2026-11-10-440-nom-ux-first-refusal/original-state.json.invalid`. The retry is the one Root-authorized operational retry of the same observation and is not healing of the first record.
* The witness is a locally writable record, not host or model attestation; the model label is asserted. The critique and review of this retry are author-executed, not independent. No push, pull request or GitHub write was made.

## Bicep public-simulation current-main checkpoint (2026-11-10, Refs #440 #136 #1288)

Draft, local-only, not approved. This is a new recurring observation and documentation checkpoint after PR 1380 reached `main`. It is not a retry of the nomination and UX record above (which stays unchanged and historical at `65c2ab9d9`), not the old #440 C6, and spends no source repair budget; it makes no source fix and opens no issue. It is the focused documentation tier: no gate, `--changed`, test, image, SQL, browser, cloud, model, live or private-data run was made by this task. It neither includes nor republishes the separate #440 CSV-learning record, whose frozen independent review is unchanged. Records: [research](../../.copilot-tracking/research/2026-11-10-bicep-observation-440-1110-research.md), [plan](../../.copilot-tracking/plans/2026-11-10-bicep-observation-440-1110-plan.md), [details](../../.copilot-tracking/details/2026-11-10-bicep-observation-440-1110-details.md), [critique](../../.copilot-tracking/plans/critiques/2026-11-10-bicep-observation-440-1110-plan-critique.md), [changes](../../.copilot-tracking/changes/2026-11-10-bicep-observation-440-1110-changes.md), [review](../../.copilot-tracking/reviews/2026-11-10-bicep-observation-440-1110-review.md) and [state](../../.copilot-tracking/rpi-sessions/2026-11-10/issue-440-bicep-observation-1110-state.json).

### Identities, scope and exclusions

| Item | Identity (read 2026-11-10) |
| --- | --- |
| Pinned source | `origin/main` `0a6dc0b3f0b3ecf098536369a8308b02226b98b8`, tree `55e6b6a36b9e53378f2c0cc8d7172d307fd2b8e4`, read through read-only git. Subtrees `src` `70d956b06f31cabfd8321b4ee9c203ae8b21d89c`, `infra` `f7f31c0934cfe0bafb4505408706e55aa8ab61e7`, `tools` `432a4e8f7d74f26e88a55dd937c9c6f193016da9`. This topic branch stays on base `65c2ab9d9` by explicit choice, so the pin is observed, not merged here |
| Trigger | PR 1380 (`Refs #136`, published head `1752260338f519a79cb427448bd7c45c34ae80ff`) merged 13:29:38Z as the pin; parent `83503b74e0e5f555382436c0ae27f64cd200971f` is a rubric bot commit. The diff from the parent is 54 files (1882 insertions, 8 deletions), `src` unchanged and no `docs/` change |
| Hosted checks | 19 reported checks all SUCCESS and MERGEABLE on the published head before merge, as reported by Root and in the durable PR comment 6768612559. That is PR-head metadata, not a result for the merge commit |
| Source blobs at the pin | `infra/main.bicep` `7074af59dbc8`, `infra/modules/guard.bicep` `f08d8b235078`, `infra/modules/containerapps.bicep` `da71bef970a9`, `infra/README.md` `b4a2a2c49a3d`, `infra/tests/test_bicep_policy.py` `751afd16a69c`, `infra/tests/test_public_simulation_startup.py` `c68c04cfcc8f`, `infra/tests/test_resident_demo_deploy.py` `77237ef15d76` |
| Documents (blob at pin) | BRD 0.21.0 `draft` `34d88395de86`; PRD Zava Forward 0.21.0 `in-review` `c788b917bafa`; PRD Proper Warm 0.13.0 `in-review` `f7f9b7675e60`; ADR-0006 `956da1a3b804`; ADR-0007 Proposed `abb21088a9bb`; unchanged by PR 1380. Draft, in-review and proposed are not approval and none changes here |
| Issue states (read live) | #136, #1288, #440, #89, #133, #132, #1384 and #1388 OPEN; nothing is ticked or closed. Number 1400 does not resolve to an issue or pull request |
| Local aftercare candidate | The #89 aftercare candidate `c6c0e4d2590eab632238e45cfec0c009d15691e1` (`src` subtree `3ad519b53426`) is a local branch, not an ancestor of `origin/main` and not main. It awaits Root consumption of the nomination and UX gate and is only named here |
| Excluded | The #89 aftercare parent and #133 as main content, held #132 and contractor identities, the #1384 and #1388 checker work, the old C6, the CSV-learning record, any deployment, Azure, live, model, resident or professional step, and whole #136, #1288 or #440 acceptance |

### Consumed evidence (Root local runs, not re-run here)

Both Root runs used a detached auxiliary composition and an owned environment. Their raw `.cmd`, `.out`, `.err` and `.exit` files are in the Root session folder, not in the repository. Neither is a GitHub merge preview, an observation on `0a6dc0b3f` or an Azure run.

| Record | Tested composition | Result as retained |
| --- | --- | --- |
| Current-main verification (`handoff-136-current-main-verification-1314`) | local merge `b9bae9f2b51c67e2edc0fbe0d4ccdc7aaa856e63`, tree `fd357610b99e9c14461e6de9a50150fc9a9d9770`, the published head merged with then-main `65c2ab9d9` (equal to the `git merge-tree` prediction) | policy 60, container contract 7, resident demo 17, resident secrets 16, IoT Hub 23, API simulation 30, live control 34 and Core resident 41, all OK with exit 0; ruff check and format and resident-module mypy exit 0; six offline Bicep build and lint commands (main, guard, containerapps) exit 0 with upgrade warnings only |
| Later image admission (`handoff-136-image-later-admission-1324`) | the same auxiliary head | one non-queued API image build exit 0, image id `sha256:38361713e1856ab6ae0b749b542ee0f99717e60fd55985b8445e7aa8eccd1d98` (the manifest-list identity, not the config digest); the four startup tests (fresh start and reuse, partial or corrupt pair untouched, slot crossing, unimportable lane module) `Ran 4`, OK, exit 0 |

* Tree equivalence (Root proof `136-current-main-prediction-1332.json`, read here and checked against the actual tree id): main `83503b74e` plus the published head predicts tree `55e6b6a3...`, which differs from the tested auxiliary tree only at `.github/rubric/scores/latest.json`, with `src`, `infra` and `tools` subtree ids equal. The actual merged main tree equals that prediction. The API runtime `src` tree `70d956b0...` is unchanged by this infrastructure merge. This is current-metadata and tree equivalence for the source, not a rerun on the pin.
* Adverse history retained: two earlier image attempts exited 1 because the shared heavy lock was busy (held by another worker's job) and are not relabeled; the old `d6d6` image is not current-composition proof. The supplemental mypy run over the policy and startup tests exits 1 with three known baseline errors in `test_bicep_policy.py` (lines 2023, 2024, 2047) and is unwaived, so there is no all-infrastructure typing or all-process pass claim. The published-head review chronology (C1 to C5 adverse and chronology qualifications) is unchanged and not healed.
* Independent records (Root): Functional and Readiness reviews of the full 54-file, 2423-line composition packet are approve with 0 findings each, supplement and do not replace the original published reviews, and grant no merge authorization or unqualified process acceptance. The local-store startup tests use the default JSON working store; they are not MSSQL, browser-authentication or Azure evidence.

### Requirement trace (Bicep contract)

| Contract | Source (blob at pin) | Observation | Class |
| --- | --- | --- | --- |
| Default off, ordinary commands unchanged | `main.bicep` `7074af59dbc8`, `containerapps.bicep` `da71bef970a9` | `enablePublicSimulationLane` defaults to false; the API `command` is null, the two `ZF_SIM_*` variables are absent and `maxReplicas` stays 4 when off | Static read plus Root offline render and policy tests; not deployed |
| Opt-in guards | `main.bicep`, `guard.bicep` `f08d8b235078` | Five guards refuse the lane outside the development direct-ingress demo, without browser authentication (client id set, not bearer-only), without deployed applications, with the placeholder API image and with `apiMinReplicas` above 1 | Static read plus Root policy tests (60) and mutation rejection; not deployed |
| Maximum one replica when on | `containerapps.bicep` | `maxReplicas` is 1 when enabled | Static read plus Root compiled-render tests |
| Fixed startup recipe | `containerapps.bicep` | A fixed `python -c` recipe provisions only when neither the store nor the key exists, validates with `Lane.open`, then runs the ordinary API module | Static read plus the four Root image startup tests (local image, local JSON store) |
| Absent, partial and corrupt fixtures | recipe, `infra/README.md` `b4a2a2c49a3d` | Only an absent pair is provisioned; a partial or corrupt pair is left untouched, an error code goes to stderr and the API starts with the lane unavailable, so the manual API fallback remains; an older image lacking the lane module also starts the ordinary API | Local observed in the Root startup tests, source qualified; not on Azure |
| Replica-local, volatile, non-durable | README | State under `/state/public-simulation` is lost on replica replacement and scale to zero; it is not durable history | Static read; durability not observed |
| Accounting boundary | README, `containerapps.bicep` | `ZF_STORE=mssql` is unchanged, so allowance, attempts and holds stay in Azure SQL and a lost simulation store cannot mint or reset them; budgets, chat and model settings are not changed | Static read; SQL not observed |
| Seal lifetime | README | A restart that retains the valid key and store pair does not itself revoke seals; losing or replacing the pair invalidates prior seals; expiry and single-use checks still apply | Static read only; no cross-restart seal runtime test is claimed |
| Image guard scope | `guard.bicep` | The guard rejects only the quickstart placeholder; it does not validate that an arbitrary image is compatible | Static read; limit stated |

### Evidence classes

* Local observed, source qualified: only the Root runs above on the auxiliary composition `b9bae9f2`.
* Current-metadata equivalence: the pin tree equals the prediction and differs from the tested tree only in the rubric score file; `src`, `infra` and `tools` ids equal.
* Azure observed: NONE.
* Implemented, unverified: the enabled path on a real deployment, MSSQL accounting with the lane on, browser authentication, a real selected-home reading path, live IoT Hub ingestion, replica replacement and scale-to-zero behaviour, and cross-restart seal behaviour.
* Deferred or blocked: an actual Azure rollout and what-if, whole #136 closure, deployment-dependent expansion, and any live SQL, authentication, resident or model acceptance. They await separately authorized live inputs and evidence.
* Unknown: behaviour of an arbitrary non-placeholder API image, and the actual GitHub merge-preview trees.

### Findings, owners and gates

* No new defect, no new issue and no source fix. The three baseline policy typing errors are known and tracked under the existing owner and are not newly fixed here; no duplicate issue is opened.
* Whole #136, #1288 and #440 criteria 7 and 8 stay unmet, and human and HVE approval stay unmet and are not invented. No #132 or #133 budget is added and no requirement is relaxed.
* The Bicep wave gate (awaiting any later live evidence and independent exact-head assessment) is distinct from the nomination and UX gate that affects #89 UI-dependent publication. The local #89 candidate stays awaiting Root consumption of the nomination and UX record and is not main. #1384 and #1388 are separate checker work and grant no source waiver.

### Recommendation

CONTINUE bounded offline source qualification of the infrastructure lane; it can proceed independently of the nomination and UX gate. No fix or pivot is indicated by this evidence. An actual Azure rollout, whole #136 closure and any deployment-dependent expansion should wait for separately authorized live inputs and evidence. Publication of this record needs independent exact-head assessment and applicable hosted checks; Root qualifies the actual publication composition later. No approval, requirement relaxation or issue closure is proposed or inferred.

### Process record and limits

* The nomination and UX section above and this section ship in one documentation batch so hosted CI runs once; each has its own heading, index paragraph and log entry, and neither edits the other.
* The witness is a locally writable record, not host or model attestation; the model label is asserted. The critique and review are author-executed, not independent. No push, pull request or GitHub write was made.

## Registry wave current-main checkpoint (2026-11-10, Refs #440 #185 #110 #109 #184 #111 #1288)

Draft, local-only, not approved. This is a new recurring observation and documentation checkpoint after the Registry wave (PR 1393, `Refs #185`) reached `main`. It is distinct from the nomination and UX record and the Bicep record above (both unchanged), not the old #440 C6, not a retry, and spends no source repair budget; it makes no product, test or configuration fix and opens no issue. It is the focused documentation tier: no gate, `--changed`, test, install, image, SQL, browser, cloud, model, live or private-data run was made by this task. It neither includes nor republishes the separate #440 CSV-learning record, whose frozen independent review is unchanged. This branch was a declared child of `docs/demo-nomination-ux-checkpoint-440-1110` at `6119b7aa3858c35fd4964d4f54dc7f8ef27ca2fa`. That parent was published as PR 1396 and squash-merged into `main` as `eff05737e8eaed584f3c269754d45bc5e44d0168` (tree `d486dc8837a7d765438500813feab227d5b574f3`) at 15:09:16Z; at Root's explicit direction this topic then took main by an ordinary merge, keeping its earlier commit, and is now an independent main-target candidate (no PR open, nothing pushed). The pin below stays the historical `6cc59776`; between `6cc59776` and `eff05737` only documentation and tracking files changed, and the `src` (`af889a4f05a2`), `infra` (`f7f31c0934cf`), `tools` (`432a4e8f7d74`) and `.github` (`220ca5404c8a`) subtree ids are identical, so the Registry source read at the pin is unchanged on `eff05737`. That is source identity only: the consumed tests ran on the reviewed candidate, not on either main commit. Records: [research](../../.copilot-tracking/research/2026-11-10-registry-source-observation-440-1110-research.md), [plan](../../.copilot-tracking/plans/2026-11-10-registry-source-observation-440-1110-plan.md), [details](../../.copilot-tracking/details/2026-11-10-registry-source-observation-440-1110-details.md), [critique](../../.copilot-tracking/plans/critiques/2026-11-10-registry-source-observation-440-1110-plan-critique.md), [changes](../../.copilot-tracking/changes/2026-11-10-registry-source-observation-440-1110-changes.md), [review](../../.copilot-tracking/reviews/2026-11-10-registry-source-observation-440-1110-review.md) and [state](../../.copilot-tracking/rpi-sessions/2026-11-10/issue-440-registry-source-observation-1110-state.json).

### Identities, scope and exclusions

| Item | Identity (read 2026-11-10) |
| --- | --- |
| Pinned source | `origin/main` `6cc59776666620309fb6b67ad2fdafb343d40998`, tree `eaf44bcdec8bdf5e9dfab2e73b1ded5459d8ff3c` (equals the Root prediction), fetched and resolved fresh, read through read-only `git show` only. The local branch source (base `65c2ab9d9`) is older, has no Registry adapter and is not current-main source; nothing here is merged into it |
| Trigger | PR 1393 merged 2026-11-10T14:54:22Z as `6cc59776`, after #1392 (`57d32c0d0`, workspace oracle repair) and #1394 (`15516ff3d`, documentation). The merge changes 25 files (2012 insertions, 1 deletion) against `57d32c0d0`: the adapter and its tests, the Core README, `pyproject.toml` and the PR's own tracking records |
| Source blobs at the pin | `src/core/src/zava_forward/core/synthetic/device_registry_azure.py` `5add5e34d4d4` (418 lines), `src/core/tests/test_device_registry_azure.py` `954c8a206c9d` (844 lines), `src/core/README.md` `e4619c34a8f8`, `src/core/pyproject.toml` `1c2d73533df4`; the four equal the independently reviewed candidate `7085213b969c` blobs |
| Documents (blob at pin) | BRD Agentic Retrofit Programme 0.21.0 `draft` `34d88395de86`; PRD Zava Forward 0.21.0 `in-review` `c788b917bafa`; ADR 0003 `d60645397b20` (owner-accepted with amendment 2026-10-15, `ms.date` 2026-10-29). The wave changes none of them; draft and in-review are not approval and none changes here |
| Hosted checks | The reviewed head `7085213b9` reported all 19 contexts SUCCESS (PR 1393 text, Root guard text). For main `6cc59776` the run list read here shows Capstone Rubric Scorer (push) success, Graph Update pip in `/src/core` success and Infrastructure PR what-if skipped, and no other push run; that is reported, not inferred green for the source, and the 19 are PR-head metadata |
| Issue and PR states (read live) | #185, #110, #109, #184, #111, #1288 and #440 OPEN; nothing is ticked or closed here. PR 1395 (the #109 sensor-review draft child, base `feat/demo-sensor-review-109-1110`, head `2b050647bff5`) is OPEN and not merged into main |
| Excluded | PR 1395 and the local #109 integration preparation (research and plan only, `a3d5e615f`, not implemented integration), the #89 aftercare candidate, #132 and #133, the #1384 and #1388 checker work, the old C6, the CSV-learning record, Bicep and nomination and UX content except by name, any deployment, Azure, live, model, resident or professional step, and whole #185, #110, #109, #440 acceptance |

### Consumed evidence (Root local runs, not re-run here)

The Root handoff `handoff-185-main-integration-1110`, its raw `.log` and `.exit` files (`checks-185-main-integration-1110`), the independent Functional verdict (`independent-185-main-integration-1433`), the PR text and the Root equivalence proof are in the Root session folder, not in the repository. They were run on the reviewed candidate `7085213b9` (tree `2cd50a62147c`, an ordinary adoption of main `06374dfca` into the approved E1 `105d479ae`) in an owned environment with the pinned SDK. None is an observation on `6cc59776` and none is an Azure run.

| Record | Result as retained |
| --- | --- |
| Targeted selectors (adapter, identity, provisioning, dependency rule) | 89 tests OK, no skips, exit 0 |
| Root reproductions of the original findings | 2 OK, exit 0; four regressions fail on the frozen old source and pass fixed (PR text) |
| Configured Core static checks | Ruff check passed, format 237 files, mypy 290 files with no issues, `tomllib` parse of `pyproject.toml`, all exit 0 |
| SDK identity | `azure-iot-hub` 2.7.0 and `six` 1.17.0 in an own environment; adapter imported from the candidate worktree (provenance log) |
| Independent Functional review | approve, 0 findings (functional-findings.json), no E2, no waiver, limits restated |
| Witness for the source run | seven records, verify exit 0, log hash `c1c091859a51f3250dd4f1e177268031c55c185bc0d3b1963e86cf8622b30d35`; local writable record, not attestation |

* Current-main equivalence scope: the prospective and actual main tree `eaf44bcd` has Core, Agents, Orchestrator, Importer and API product-source subtrees and the API dependency manifest exactly equal to the reviewed and tested candidate, per the Root proof; remaining differences are rubric documentation and the independently reviewed workspace checker helper, two checkers and their tests. This is component-source equivalence, not full-tree equality, and I did not recompute the candidate subtree ids here. The four Registry blobs above were read directly at the pin.
* Adverse and qualified items retained: an earlier extra full Core discovery timed out and is NOT a pass and was not re-run; no API selector was identified or claimed; `__context__` stays programmatically reachable (suppression is for formatted tracebacks only); in the source run `research-open` and `plan-done` were recorded in one call after one preflight and the review file was drafted just before `implement-done`. The original adverse reports (incomplete-inventory High and formatted-traceback Medium, closed on the candidate, not erased) are unchanged and not healed.

### Requirement trace (Registry contract)

| Contract | Source (blob at pin) | Observation | Class |
| --- | --- | --- | --- |
| BRD FR-048, AC-090, OD-43 (in-use monitoring inventory and ownership) | BRD 0.21.0 `draft` | Documents the monitoring need and the open ownership decision; the adapter does not satisfy or approve OD-43 | Document-qualified, draft; not approved |
| PRD FR-050, AC-066 to AC-068 | PRD 0.21.0 `in-review` | AC-066 (simulator identities through Azure IoT Hub) and AC-067 and AC-068 are all "Not run"; the adapter supplies a bounded part of identity enrolment only | Document-qualified; whole AC-066 unmet |
| ADR 0003 decision 6 | ADR 0003 `d60645397b20` | Per-device X.509 or symmetric keys, managed identity for services, named credential owner; its implementation status says no live Hub identity, provisioning, SDK use or deployment follows from an accepted ADR | Owner-accepted with amendment; no live approval |
| Keyless and default off | `device_registry_azure.py` `5add5e34d4d4` | Import, construction, dry run and `close()` do not import the SDK, acquire a token or connect; one injected Entra token credential or pre-built client; no connection string, key or ambient discovery | Static read plus consumed tests; not run on main |
| Bounded inputs | same | Hub host must match `*.azure-devices.net`; a finite `EnrollmentSpec` of 1 to 100 `SYN-` device ids with public X.509 thumbprints; timeout 1 to 60 seconds; invalid input refused before any SDK call | Static read plus consumed tests |
| Create-only and conditional writes | same, README `e4619c34a8f8` | Create sends `If-None-Match: *`, disabled, with the exact run marker; delete uses the exact snapshot ETag, never a wildcard, and refuses drift; uncertain writes return a readback and are not retried | Local observed against an SDK-level simulator of the documented REST conditions; Azure behaviour unobserved |
| Complete or refused enumeration | same | A full 1000-device page is `LIST_INCOMPLETE`; entries without a string marker are confirmed by bounded individual reads (at most 100 per call); an unreadable confirmation or exhausted budget refuses, so whole-run teardown refuses before any delete; more than 100 unmarked devices in one listing refuses | Static read plus consumed tests |
| Safe errors | same | Fixed codes without SDK response text; `__suppress_context__` set; context object remains reachable | Static read plus consumed regression tests; reachability qualified |
| Packaging | `pyproject.toml` `1c2d73533df4` | `iothub` extra and `dev` extra pin `azure-iot-hub==2.7.0` and `six==1.17.0`; runtime `dependencies` stay empty; Core imports without the SDK | Static read, TOML parse in consumed run |
| Out of source scope | README | No certificate or key issuance, storage, rotation, activation, Device Provisioning Service, Registry-before-credential ordering or authentication update; the command line does not use the adapter and `--apply` still refuses | Static read; deferred or open |

### Evidence classes

* Local observed, source-qualified carry-forward: only the Root runs above on the reviewed candidate `7085213b9`, tied to the pin by component-subtree equivalence.
* Current-metadata equivalence: main tree `eaf44bcd` equals the Root prediction; the four Registry blobs equal the reviewed candidate blobs.
* Azure observed: NONE.
* Implemented, unverified: the adapter against a real IoT Hub (status codes, 412 behaviour, ETag format, list limits, RBAC), Entra token acquisition, any live enrolment or teardown, and hosted CI on main for the source.
* Deferred or blocked: actual device identity issuance, credential owner choice and secure credential storage, whole-run teardown criteria, Registry-before-credential ordering, authentication update, live Hub, SQL, UI and model acceptance, and the Registry choice and credentials decision. These stay human or live gates and are neither approved nor silently deferred by this record.
* Unknown: how the adapter behaves with more than 100 unmarked devices on a real hub beyond its refusal, the behaviour of a real SDK response shape not covered by the simulator, and the unrun full Core discovery result.

### Findings, owners and gates

* No new confirmed defect, no confirmed refactoring and no source fix. The stale "not implemented" wording in older issue text is not copied as current source truth; the pin shows the bounded adapter, and the issue criteria stay open.
* Remaining gaps by owner: #185 (credential owner, issuance and storage without leaking, teardown of all simulated identities, Registry-before-credential, authentication update); #110 and #184 (live Hub identities, live ingestion and streaming acceptance); #109 and #111 (integration of the sensor-review child, analysis and review task, reproducibility and acceptance, local preparation only); #1288 (retained sensor values and Quality AI review-flag UI). No duplicate issue is opened.
* Whole #185, #110, #109 and #440 criteria 7 and 8 stay unmet, and human and HVE approval stay unmet and are not invented. The affected gates (live identity, credential, secure storage, teardown, Hub, SQL, UI and model acceptance) await Root consumption after independent review of this record.

### Recommendation

CONTINUE bounded local #109 integration and testing against current main, using the existing owners; PR 1395 and the local preparation remain unmerged and are not integration until Root records an actual merged head. Do not expand dependent features, close an epic, start live provisioning or treat this as approval of the Registry choice, credentials or any live decision; those remain named human gates. No fix or pivot is indicated by this evidence. Publication of this record needs independent exact-head assessment and applicable hosted checks.

### Process record and limits

* Added as a distinct section; the nomination and UX and Bicep sections above are unchanged. The old CSV-learning record is independent and unchanged.
* The witness is a locally writable record, not host or model attestation; the model label is asserted. The critique and review are author-executed, not independent. No push, pull request or GitHub write was made, and no command in this task ran on `6cc59776` beyond read-only git and read-only GitHub queries.

## Sensor-review wave actual-main checkpoint (2026-11-10, Refs #440 #109 #111 #184 #1288)

Draft, local-only, not approved. This is the due recurring observation and documentation checkpoint after the sensor-review wave (PR 1404, `Refs #109` and `Refs #111`) reached `main`. It is distinct from every section above, which are unchanged, is not another implementation, spends no source repair budget, and makes no product, test, oracle, tool, workflow or gate change and opens no issue. It is the focused documentation tier: this task ran no gate, `--changed`, test, install, image, SQL, browser, cloud, model, live or private-data command, only read-only git and read-only GitHub queries. It is separate from the aftercare checkpoint in PR 1405, which was OPEN and not on `main` when this record was read (head `5450b07a89a6`) and owns its own section; nothing from it is copied, adopted or described as merged here. Records: [research](../../.copilot-tracking/research/2026-11-10-sensor-actual-main-440-1110-research.md), [plan](../../.copilot-tracking/plans/2026-11-10-sensor-actual-main-440-1110-plan.md), [details](../../.copilot-tracking/details/2026-11-10-sensor-actual-main-440-1110-details.md), [critique](../../.copilot-tracking/plans/critiques/2026-11-10-sensor-actual-main-440-1110-plan-critique.md), [changes](../../.copilot-tracking/changes/2026-11-10-sensor-actual-main-440-1110-changes.md), [review](../../.copilot-tracking/reviews/2026-11-10-sensor-actual-main-440-1110-review.md) and [state](../../.copilot-tracking/rpi-sessions/2026-11-10/issue-440-sensor-actual-main-1110-state.json).

### Dated qualification (2026-11-10, after the original checkpoint commit `80643f6b9cafa4e33ccd7afab77cbc7c282ab496`)

The statements below that PR 1405 was OPEN and not on `main` describe the `4c1b4099` snapshot read at 16:41Z and are retained as historical. PR 1405 has since been merged (2026-11-10T16:44:27Z) as `main` `ac962fe6ce0faf89539e13606d2a0f1498a59f7a` (tree `a1ac49c7`), and its aftercare section follows this one, unchanged. This topic then took the later `main` `d79180309edc7eabb2a13e7f8f0d3b4579c5fb34` (tree `e494695af7b1`, after PR 1407 and PR 1408) by an ordinary merge, with no rebase. On that `main` the `src` (`49c7b0b06f97`), `infra` (`f7f31c0934cf`) and `tools` (`432a4e8f7d74`) subtree ids still equal `4c1b4099`; the only path outside tracking records and the three documentation files that differs from `4c1b4099` is `.github/rubric/README.md` (documentation), so the sensor runtime source remains the `4c1b4099` source. That is source identity only: the candidate-stage runs still executed on the staged tree `d45426bd` (equal `src`, `infra`, `tools` and `.github` to reviewed `6fe2218c`), the `.github/rubric/scores/latest.json` exception above is unchanged, and no fresh runtime run on any `main` is claimed. The original witness `verify` for the first checkpoint exited 1 (QUALIFIED: the review artifact changed after `review-done` because two review lines were edited after that marker); that result is preserved and the correction is recorded in a separate chain. Records: [research](../../.copilot-tracking/research/2026-11-10-sensor-qualification-440-1110-research.md), [plan](../../.copilot-tracking/plans/2026-11-10-sensor-qualification-440-1110-plan.md), [details](../../.copilot-tracking/details/2026-11-10-sensor-qualification-440-1110-details.md), [critique](../../.copilot-tracking/plans/critiques/2026-11-10-sensor-qualification-440-1110-plan-critique.md), [changes](../../.copilot-tracking/changes/2026-11-10-sensor-qualification-440-1110-changes.md), [review](../../.copilot-tracking/reviews/2026-11-10-sensor-qualification-440-1110-review.md) and [state](../../.copilot-tracking/rpi-sessions/2026-11-10/issue-440-sensor-qualification-1110-state.json).

### Dated publication qualification (2026-11-10, correction C2 on `c21849e05efe2f88d50ab4b56a0fea03b0967a8a`)

Both witness chains behind this section are QUALIFIED and publication stays on HOLD. Neither is green, and independent approval or the 19 historical PR 1404 checks do not clear it.

* Original chain (commit `80643f6b9cafa4e33ccd7afab77cbc7c282ab496`): 7 records, `verify` exit 1, because the review artifact was edited after `review-done`. Locators in the Root session folder `38e61c82-3c44-4b97-af59-9eed5c151ac7/files`: handoff `handoff-440-sensor-actual-main-1110.md`, valid verify output `phase440-sensor-actual-main-evidence-1110/verify.out`, native log `phase440-sensor-actual-main-evidence-1110/issue-440/events.jsonl`.
* Qualification chain (commit `c21849e05efe2f88d50ab4b56a0fea03b0967a8a`): 8 records, `verify` exit 1, because `research-open` seq 2 was refused (the state lacked the research artifact path) before the accepted seq 3. Locators: handoff `handoff-440-sensor-qualification-1110.md`, valid verify output `phase440-sensor-qualification-evidence-1110/verify.out`, native log `phase440-sensor-qualification-evidence-1110/issue-440/events.jsonl`. An earlier verify command for this chain used the unsupported `--state` and `--brief` flags and exited 64 (usage error); that output file was overwritten by the valid run, so only the command history survives.
* The external handoffs of both chains describe strict state validation before each marker. That check only parsed JSON and rejected duplicate keys; it did not validate artifact paths or event prerequisites, and the logs do not show full validation, so the claim is unsupported beyond parsing. The refused seq 2 is the consequence.
* Correction C2 (this commit) is a later separate chain, not a retroactive repair of either. Its prospective external evidence is `phase440-sensor-c2-evidence-1110` with `phase440-sensor-c2-preflight-1110.log` in the same Root folder. Its final verify outcome is recorded in the external handoff `handoff-440-sensor-c2-1110.md` and pull request metadata, not here, so no committed text claims a result after the marker.
* C2 adds no source, runtime, gate, cloud or model change and no fresh runtime run on any main. Against `origin/main` `54eae28f8bc2b3c5e3786ab5169b0ed375f826ef` the `src`, `infra` and `tools` tree ids (`49c7b0b06f97`, `f7f31c0934cf`, `432a4e8f7d74`) are equal; the other differences are other topics' appended documentation and the workflow-recorded `.github/rubric/scores/latest.json`. Records: [research](../../.copilot-tracking/research/2026-11-10-sensor-c2-440-1110-research.md), [plan](../../.copilot-tracking/plans/2026-11-10-sensor-c2-440-1110-plan.md), [details](../../.copilot-tracking/details/2026-11-10-sensor-c2-440-1110-details.md), [critique](../../.copilot-tracking/plans/critiques/2026-11-10-sensor-c2-440-1110-plan-critique.md), [changes](../../.copilot-tracking/changes/2026-11-10-sensor-c2-440-1110-changes.md), [review](../../.copilot-tracking/reviews/2026-11-10-sensor-c2-440-1110-review.md) and [state](../../.copilot-tracking/rpi-sessions/2026-11-10/issue-440-sensor-c2-1110-state.json).

### Identities, lineage, scope and exclusions

| Item | Identity (read 2026-11-10) |
| --- | --- |
| Pinned source | `origin/main` `4c1b4099869d132e06291a29ee476e98286c2245`, tree `7515820333a23e76d1d200ea558ad01127024aab` (equals the independently assessed prospective merge tree), fetched fresh and unmoved, read through read-only `git show` only. One squash parent `d240cc589f483c03e9c728bd3615a966775c90dc` (rubric score record), before it `64c3f9191a2f` (PR 1400 aftercare) |
| Lineage | Child PR 1395 (head `6b0ba7b14f99`) merged 15:51:03Z into the declared parent branch `feat/demo-sensor-review-109-1110` as `bd2a6494464b451572fc3dc7c8d53c549e0f9dad`, not into `main`. Parent PR 1404 (base `main`, no closing reference) merged 16:38:22Z as `4c1b4099`. Reviewed head `6fe2218c7960a60a9d18c9680230b37fad7e972c` (tree `00c7abf4209d`) was an ordinary merge of that parent squash and `main` `64c3f9191`; the squash changes 56 paths against `d240cc589` (3216 insertions, 2 deletions): 8 source and test paths and 48 tracking records |
| Source equivalence | `src` `49c7b0b06f97`, `infra` `f7f31c0934cf` and `tools` `432a4e8f7d74` are identical on `4c1b4099`, reviewed head `6fe2218c` and the tested staged tree `d45426bd28850d893622b48df1a2649a13135992`. The only path outside `.copilot-tracking` that differs between `6fe2218c` and `main` is `.github/rubric/scores/latest.json` (blob `b0bc2db354d0` on `6fe2218c`, `b9c8b5d9e978` on `d240cc589` and `main`); `main`'s trusted rubric baseline advanced by `d240cc589`. `.github` is `e2ecbb8ea5b2` on `6fe2218c` and `d45426bd` and `ce96a8f4c2c5` on `main`; no workflow, action or gate file differs. The prior pin tooling and runtime inputs are therefore preserved, and no fresh execution on `main` is claimed |
| Selected source blobs at the pin | `src/core/src/zava_forward/core/sensor_review_draft.py` `15055cd59a0a` (388 lines), `sensor_analysis.py` `dd6a363db74b` (255), `projection.py` `14892308364e` (204), `src/api/src/zava_forward/api/server.py` `ab381d0718ba`, `web/ops.js` `2178e06f299c`, Core `pyproject.toml` `caeac749acca`; tests `src/core/tests/test_sensor_review_draft.py` `1fe0a7469455` (619 lines), `src/api/tests/test_sensor_review_draft_api.py` `7aef271edf4e` (168), `src/api/checks/quality_sensors_browser_check.py` `80a1bf730adf` (509) |
| Documents (blob at pin) | BRD Agentic Retrofit Programme 0.21.0 `draft` `34d88395de86`; PRD Zava Forward 0.21.0 `in-review` `c788b917bafa`; ADR 0003 `d60645397b20`. The wave changes none of them; draft and in-review are not approval and none changes here |
| Hosted checks | PR 1404 head `6fe2218c` reported 19 contexts, all SUCCESS, MERGEABLE, in Root's final merge gate read before the merge. That is PR-head metadata, distinct from the local staged validation below; the push runs for `main` `4c1b4099` were not read here and are not inferred green |
| Issue and PR states (read live) | #109, #111, #110, #184, #185, #1288, #81 and #440 OPEN; nothing is ticked or closed here. #132 and #144 OPEN and excluded. Inherited aftercare #1401 and #1402 OPEN and unrepaired. #1297 and #1298 (sensor MSSQL skip binding) OPEN. PR 1395 and PR 1404 MERGED; PR 1405 OPEN |
| Excluded | #132, #144, PR 1405 and the aftercare checkpoint, the inherited #1401 and #1402 source holds, any deployment, live Hub, provider, Quality-model, resident, professional or accessibility acceptance step, and whole #109, #111 and #440 acceptance |

### Consumed evidence (Root local runs, read raw, not re-run here)

Root's final merge gate, the PR text, the 109 handoff, the independent Functional report and its metadata supplement, the Root witness verification, the raw `.txt` outputs and the witness log are in the Root session folder, not in the repository. They ran on the staged integration tree `d45426bd28850d893622b48df1a2649a13135992` while the worktree metadata still named `20addb9ae` with 83 dirty entries, in an owned environment with the declared pins. This is NOT a literal post-commit execution and not an execution on `main`. The raw outputs were read, not summaries.

| Record | Result as retained |
| --- | --- |
| Core selectors | draft 65 run with 22 opt-in skips OK; analysis 11, analysis store 9, scenario manifest 8, Registry 39, aftercare intake 39 OK; aftercare store 36 run with 13 skips OK |
| API selectors | sensor draft API 6 with no skips; aftercare served 8; aftercare screen 13; accessibility baseline 12; workbench 5 OK |
| Role inventory | first run FAILED with `ModuleNotFoundError: test_role_matrix` (the command omitted the tests directory from `PYTHONPATH`); one corrected-path rerun passed 24 tests. The failure is retained and is not a pass; no test or check was patched |
| Static | configured Core mypy 296 files and API mypy 224 files, Ruff check and format check (Core 243, API 142) pass. Configured with disclosed scoped exemptions, not unchanged strict checking. `node --check` of three scripts is recorded only in the handoff and transcript, with no separate raw file |
| Sensor browser | maintained check, 33 passed, exit 0, no page errors, short owned cwd, one non-queued lock |
| Local MSSQL | `MssqlDraftCases` 22 run, zero skips, exit 0 on SQL Server 2022 CU27-GDR 16.0.4305.5 in a disposable container that was removed. Local synthetic SQL, not Azure SQL |
| Independent Functional review | approve, zero findings, on the cumulative 56-path diff; the metadata supplement approves the PR text and records Root's tree comparisons as supplied, not reviewer-executed |
| Witness | seven records, `verify` records 7, log sha256 `4fe3212a1ff10ba42af278e94325d9662e02d55f6b5bebf90bf3603b6ed6a3d8`, with six "artifact changed after observation" notes; a local writable record, not tamperproof and not host or model attestation |

* Adverse and qualified items retained: the role-inventory first failure above; the earlier browser socket-length and environment failures preserved in the PR text, not reclassified; opt-in skips (22 Core draft, 13 aftercare store) are not SQL passes; the earlier preparation chain (three events, partial) and the prospective chain stay unchanged.
* The PR text states that these fixture checks do not prove an actual provider consumed readings.

### Requirement trace (sensor-review contract)

| Contract | Source (blob at pin) | Observation | Class |
| --- | --- | --- | --- |
| BRD FR-048 and RULE-014 (consented in-use monitoring; absence of an alert is not evidence) | BRD 0.21.0 `draft` | Drafts do not treat missing or normal sensor data as acceptance, closure or payment evidence; the BRD is not approved | Document-qualified, draft; not approved |
| PRD FR-050, AC-066 to AC-068 | PRD 0.21.0 `in-review` | AC-066 (Hub ingestion), AC-067 (versioned reproducible analysis; only an approved rule creates a human task) and AC-068 (research R1 to R3) are all "Not run" in the acceptance table; the wave supplies a bounded local part of the review-task path only | Document-qualified; whole ACs unmet |
| Default off and proposed only | `sensor_review_draft.py` `15055cd59a0a` | Flag `ZF_SENSOR_REVIEW_DRAFTS`; state `PROPOSED_UNAPPROVED`; the label says not an approved task and the rule is an exercise rule, not a sourced standard; no task, owner, queue, model call, ranking, hold, hazard clock or consent change | Static read plus consumed tests |
| Served write refusal | same | No approved policy source exists, so a served write refuses; constructed approvals belong only to tests through a private synthetic seam | Static read plus consumed tests |
| Role, consent and bounds | same | Quality Inspector and Retrofit Programme Manager only; at most 20 drafts per case; withheld note when monitoring consent is not granted now; manual route `manual-sensor-review` | Static read plus consumed tests and browser |
| Routing and redaction | `server.py` `ab381d0718ba`, `projection.py` `14892308364e` | Dedicated `/api/cases/{id}/sensor-drafts` read and request dispatch before generic case access, apart from the `/api/aftercare` prefix; 503 points to the manual route; generic detail projection strips `sensor_review_drafts` | Static read plus consumed tests |
| Employee display | `ops.js` `2178e06f299c` | Read-only section, absent while the flag is unset, no write control, markup rendered as text, semantic list and time elements | Consumed browser run on the staged tree; no WCAG or assistive-technology acceptance |
| Packaging | Core `pyproject.toml` `caeac749acca` | SDK pins `azure-iot-hub==2.7.0` and `six==1.17.0` preserved with the scoped test exemptions; no broader typing policy change established | Static read plus Functional review |
| Out of scope | the wave | Live Hub, simulator-to-Hub-to-SQL-to-model, a real provider, Quality-model review, resident, professional and human approval, accessibility acceptance | Open, owned elsewhere |

### Evidence classes

* Local observed, source-qualified carry-forward: only the Root runs above, on the staged tree `d45426bd`, tied to `main` by equal `src`, `infra` and `tools` subtree ids and the single rubric exception.
* Hosted: PR-head `6fe2218c` all 19 contexts SUCCESS before the merge; `main` `4c1b4099` push runs not read.
* Azure, provider, model and resident observed: NONE.
* Implemented, unverified: unforced `ConflictError` and `CommittedReloadError` branches (the conflict-named green test does not force the exception, and 22 SQL passes do not prove them); behaviour against an actual Hub, SQL Azure and model.
* Deferred or blocked: approval of any rule or policy source, resident and professional decisions, accessibility acceptance, and live ingestion. These stay human or live gates and are neither approved nor silently deferred by this record.
* Unknown: how the drafts behave on `main` under a fresh run (not executed), and the result of the `main` push workflows.

### Findings, owners and gates

* No new confirmed defect, no confirmed refactoring and no source fix. Nothing read contradicts the independent approve, and no current open issue needs a duplicate.
* Remaining gaps by owner: #111 (reproducible outputs from retained readings, R1 to R3 research, approved rule or policy source); #109 (epic closure); #110 and #184 (live ingestion and streaming); #1288 (retained sensor values and Quality AI review flags); #1297 and #1298 (bind sensor MSSQL skips to required SQL execution); #1401 and #1402 (inherited aftercare, not repaired here).
* Whole #109 and #111 stay OPEN and unmet, #132 and #144 are excluded, and human and HVE approval stay unmet and are not invented. The affected live, resident, model and accessibility gates await Root consumption after independent review of this record.

### Recommendation

CONTINUE: keep the default-off, proposed-only drafts as the local baseline and take the remaining owned gaps through their existing issues (skip binding, reproducibility and research, live ingestion). This evidence supports neither closing #109 or #111 nor expanding dependent features (live Hub, provider, Quality-model or resident use) and indicates no fix or pivot. Publication of this record needs independent exact-head assessment and applicable hosted checks for the exact head.

### Process record and limits

* Original snapshot (`80643f6b` on `4c1b4099`): added as a distinct section; all earlier sections are unchanged and the PR 1405 aftercare section is not present on this branch. If both sections later need integration, keep both append-only.
* Dated clarification (2026-11-10, C2): that sentence is history. The `c21849e0` ordinary merge of `d79180309` preserves both the sensor section and the aftercare section, append-only. No runtime was executed on the merged head.
* The witness is a locally writable record, not host or model attestation; the model label is asserted. The critique and review are author-executed, not independent. No push, pull request or GitHub write was made, and no command in this task ran on `4c1b4099` beyond read-only git and read-only GitHub queries.

## Aftercare integration current-main checkpoint (2026-11-10, Refs #440 #89 #133 #134 #1401 #1402)

Draft, local-only, not approved. This is a new recurring observation and documentation checkpoint after the delivery-quality and aftercare persistence integration (PR 1400) reached `main`. It is distinct from every earlier section above (all unchanged, including the Registry wave section of PR 1399), not the old #440 C6, not a retry, and spends no source repair budget; it makes no product, test, configuration or dependency fix and opens no issue. It is the focused documentation tier and pure documentation: no gate, `--changed`, test, install, image, SQL, browser, cloud, model, live or private-data run was made by this task, and no reviewed result below is a new execution on `main`. It observes proven source composition and retained evidence, not new runtime acceptance. Records: [research](../../.copilot-tracking/research/2026-11-10-aftercare-main-440-1110-research.md), [plan](../../.copilot-tracking/plans/2026-11-10-aftercare-main-440-1110-plan.md), [details](../../.copilot-tracking/details/2026-11-10-aftercare-main-440-1110-details.md), [critique](../../.copilot-tracking/plans/critiques/2026-11-10-aftercare-main-440-1110-plan-critique.md), [changes](../../.copilot-tracking/changes/2026-11-10-aftercare-main-440-1110-changes.md), [review](../../.copilot-tracking/reviews/2026-11-10-aftercare-main-440-1110-review.md) and [state](../../.copilot-tracking/rpi-sessions/2026-11-10/issue-440-aftercare-main-1110-state.json).

### Identities, scope and exclusions

| Item | Identity (read 2026-11-10) |
| --- | --- |
| Trigger | PR 1400 `feat(demo): integrate delivery-quality aftercare persistence`, MERGED 2026-11-10T15:56:55Z as `main` `64c3f9191a2ffa97ef2dc07245422333ad4d6585`, tree `8fbdaec7d138e360e9e460ad714742cb78b4d621` (parent `1290aa557`, the PR 1399 Registry checkpoint). The actual tree equals the guarded Root prediction. Head `b7e46b3be3d34734f49f0397c8c8022e920c1781`, tree `06ab5118310b662b57414772f7ba157e7bdec559`, branch `feat/demo-quality-workflows-89-1109`. No closing references; `Refs #89`, `Refs #133`, `Refs #134` only |
| Authored paths | The actual PR diff is 77 paths (21 under `src`, 53 tracking records, 3 documentation files), exactly the local diff from merge-base `6cc59776`. The reviewer's cumulative two-dot packet of 98 paths and 6,586 lines is a SUPERSET: 21 further paths are main-only documents that appear removed only because `b7e46b3be` predates later main. They are qualified as not authored deletions; main-only documents, including the 1396 and 1399 checkpoint sections and log entries, are retained in the merged tree |
| Hosted checks | All 19 PR contexts read SUCCESS (PR-head observations, a separate observation from the local runs). For main `64c3f9191` the run list read here shows Graph Update pip in `/src/api, /src/core` completed with success and Capstone Rubric Scorer (push) still in progress; nothing more is claimed green for main |
| Documents (blob at `64c3f9191`) | BRD Agentic Retrofit Programme 0.21.0 `draft` `34d88395de86`; PRD Zava Forward Retrofit Programme Workbench `in-review`, `exercise_status` author-complete-unsigned-pending-review-and-owner-acceptance, `c788b917bafa`. Neither is changed by PR 1400; draft and in-review are not approval and no requirement or decision is approved here |
| Issue states (read live) | #89, #133, #134, #132, #440, #1401 and #1402 OPEN; #89 carries `status:partially-delivered`, #132 `status:not-started`. Nothing is ticked or closed here |
| Excluded | The unmerged #109 and #111 sensor-draft parent (child PR 1395 merged only into its parent branch `bd2a649`; local #109 integration still running), the #144 legacy worker, #132 contractor job pack and fieldwork evidence capture (not delivered by PR 1400 and separately blocked; whole #89 acceptance does not depend on it), real-provider activation, any actual Azure dispatch, and any actual resident or professional acceptance |

### Source identity proof (direct tree comparison)

Compared with `git rev-parse <commit>:<path>` for the tested commit `b7e46b3be` and actual main `64c3f9191`. Commit ancestry and green CI were not used as proof.

| Tree | Tested `b7e46b3be` | Actual `64c3f9191` | Equal |
| --- | --- | --- | --- |
| `src` | `c322b0f7a710c7f121fcd75b6685683ff57fa893` | `c322b0f7a710c7f121fcd75b6685683ff57fa893` | Yes |
| `src/core`, `src/api`, `src/agents`, `src/orchestrator`, `src/importer` | `bc095465f75d`, `5bc36cda619b`, `a35f7e1d7fa9`, `d06c99144364`, `c6e324d1c3a0` | identical ids | Yes |
| `infra` | `f7f31c0934cfe0bafb4505408706e55aa8ab61e7` | `f7f31c0934cfe0bafb4505408706e55aa8ab61e7` | Yes |
| `.github` | `220ca5404c8a` | `e2ecbb8ea5b2` | No: `64c3f9191` equals its parent `1290aa557`, so current main workflow and rubric state is preserved, not replaced by the candidate |

The dependency manifests are inside `src` (`src/core/pyproject.toml` `663adeb012ba`, `src/api/pyproject.toml` `1ae6604c812f`, identical in both). Outside `docs/`, `git diff --name-only b7e46b3be 64c3f9191` lists only main's tracking records and `.github/rubric/scores/latest.json`. The runtime, test and dependency inputs of `64c3f9191` are therefore exactly the tested inputs. This is source identity only: the tests below ran on the author's candidate, not on `64c3f9191`. Aftercare blobs equal in both commits: `aftercare_intake.py` `96674907da90`, `aftercare_store.py` `e5bd737c6d9b`, `aftercare.py` `115f639bc782`, `web/aftercare.js` `682457e40fd6`.

### Consumed evidence (original commands on `b7e46b3be`, not re-run here)

Root session sources, outside the repository: `handoff-89-current-main-adoption-1110`, raw `checks-89-current-main-adoption-1110/` (exit files, outputs, `SHA256SUMS`), the bounded handoff and qualified PR text, and the independent Functional report (`independent-89-main-final-1913`, reviewer `f73048c6`). Each result was observed by the author's original commands on the adopted merge composition (`a664e316`, tree `7af3d7fc`) and the tracking-only head `b7e46b3be`, which has identical runtime and dependency inputs.

| Original result (author commands on `b7e46b3be`) | Retained outcome and limit |
| --- | --- |
| Core nine targeted modules, API 16 targeted modules | Exit 0 per module; aftercare_intake 39, aftercare_store 36 with 13 SQL-gated skips, resident_decisions 371 with 132 skips, handoff read guidance 9 with 4 skips. Skips are not passes |
| Registry SDK dependent module | First run exit 1 (39 tests, 34 failures and 16 errors) because the author's owned environment lacked the newly pinned SDK; after installing `azure-iot-hub` 2.7.0 and `six` 1.17.0 into that environment only, the single rerun passed 39 tests. Original red and install log retained; not a product defect |
| Fresh affected persistence SQL | 36 tests OK, zero skips, disposable MSSQL, worktree imports and source hashes recorded, container removed, no leftover databases; a fresh run because Core pins changed, not a carry-forward. Not a high-volume or long-lived proof |
| Static checks | Ruff check and format clean; configured Core mypy 294 files and API mypy 223 files clean; `node --check` 15 files clean. Infrastructure is not covered |
| Browser checks | aftercare, workbench, workspace_scripts, employee_workspace, nomination and progress: 207 PASS, 0 FAIL. Progress first failed with `FileExistsError` on the author's own existing output directory; one justified rerun with a fresh output directory passed. Both outputs retained. Pinned axe execution is not WCAG, assistive-technology or human acceptance |
| Independent Functional report | `approve_with_comments` on the complete 164-file adoption packet and then the 98-path two-dot packet: 0 Critical, 0 High, 2 inherited Medium OPEN, no new functional blocker; bounded synthetic-demo scope only; no infrastructure or `.github` candidate delta |
| Witness for the source run | Seven records, verify exit 0, log hash `1a43156483ef5f21dc252244496818ff3f8b71a0eba82fd304f434ca80bbee9f`; a locally writable record, not host or model attestation |

* Not run and therefore Unknown: any test on `64c3f9191` itself, infrastructure tests of main's delta, full Core or API discovery, the full gate, `--changed`, all-image build, live, model, accessibility-tool beyond the pinned axe checks, assistive-technology, WCAG and release proof. The SDK-missing and progress output-directory first failures are preserved and not healed.
* Where a selected input identity could not be proven equal (for example the `.github` tree above), the limitation is stated rather than assumed.

### Requirement trace (document-qualified)

| Requirement (document, status) | Source at `64c3f9191` | Observation | Class |
| --- | --- | --- | --- |
| PRD FR-049, AC-063 (in-review; AC-063 Not run): complaint, remedy, package, handover and financial closure stay distinct | `aftercare.py` `record_closure`, `aftercare_intake.py` manager-only closure | Handover and financial closure never change a concern or remedy; unresolved concerns stay visible. Age bands owned by Housing/Complaints, lease evidence and leasehold text are not implemented on this surface | Local observed for constructed data, document-qualified; whole AC-063 unmet |
| BRD FR-047, AC-089 (draft): closure cannot close a remedy, defect or dispute | same | Remedy status is separate and completion needs evidence | Implemented for the constructed register; document-qualified |
| BRD FR-029, FR-030, RULE-013 (draft): reopened defects, severity, independent closure | Earlier defect and quality delivery, not changed by PR 1400 | Not re-observed in this wave; the aftercare route is a concern route, not defect closure | Not observed here |
| BRD RULE-014 (draft): a missing sensor alert is not acceptance or closure evidence | register and store restore refusals | A sensor reading is context only, never a human basis and never dismisses a report; a restore marking a concern sensor-dismissed is refused | Local observed for constructed data |
| PRD FR-014, AC-017 (in-review; Not run): type, desired outcome, owner, accessible or representative route, contact is not consent | `aftercare.py` `intake_form`, `aftercare_intake.py` `record_concern` | Digital and staff-recorded routes (phone, in person, paper, assisted visit); a missing owner is Unknown; a synthetic scenario owner is labelled | Local observed for constructed data; whole AC-017 unmet |
| PRD FR-036 (in-review): AI tasks registered, unapproved tasks use manual handling | `ai_registry` task `aftercare-concern-pack` | Registered unapproved and disabled, manual route, no model binding | Static read; no model route delivered |
| #133 acceptance criteria (OPEN, all unticked) | whole feature | Staff-assisted intake, owner, outcome, remedy, closure and denominators exist for synthetic data. A household or representative self-service route, evaluator role access, the DPO position on outcome data and an AI concern pack are not delivered | Partially delivered; criteria unmet |
| #134 acceptance criteria (OPEN) | whole feature | PR 1400 adds one staff screen route and a browser check; no eleven-perspective walkthrough, AC-034 to AC-043, keyboard or status-announcement acceptance is claimed | Not delivered by this PR |

### Boundaries observed (static read of `64c3f9191`)

* Contract and package boundary: `AftercareService.handle(method, path, user, body, query)` is the route contract. Core owns the register, service and `DocumentStateStore`; API owns `/api/aftercare` (GET and POST through `server.py` `_aftercare`), the `#/aftercare` screen `web/aftercare.js`, the workbench manifest entry and the endpoint inventory. `aftercare` is the only document added to `SqlStore.DOCS` and `projection.STAFF_GET`. Agents, Orchestrator and Importer are unchanged.
* Roles, consent and human decisions: existing staff role tuples only; the Residents Liaison Officer and Retrofit Coordinator record and the other listed roles read; contractors and the Quality Inspector receive 403. The actor comes from the session, never the request body. Owner actions are limited to the named synthetic owner, closure is manager-only, no consent is read or written, and no evaluator or resident account, portal or approval is added.
* Persistence: one validated JSON document per update and one atomic save; the mutator runs once under the store lock; a failed save is classified by re-reading under that lock; an unconfirmed write is never reported as not saved; the same `request_id` replays the committed receipt and a changed payload under it is a conflict. The JSON `Store` is single-process; cross-instance protection is SQL only.
* Refusal, manual path and recovery: field errors link to inputs and move focus to the summary; the draft, request id and unconfirmed state survive validation failures and route changes and clear on sign-out; a late reply after sign-out or a route change does not render or take focus; a `beforeunload` guard protects the in-memory draft; the paper and phone routes are the manual path; AI stays off. These are source reads and the retained constructed checks, not human or assistive-technology acceptance.

### Inherited open findings (read from the actual issues; not waived, not fixed)

| Issue | Severity and status | Reproduction evidence as recorded | Bounded demo limitation |
| --- | --- | --- | --- |
| #1401 `fix(aftercare): restore numerically ordered concern identifiers at 1000` | Medium, OPEN | `aftercare_intake.py:378-379` sorts JSON keys so `AC-1000` precedes `AC-101`; restoration in `aftercare.py:195-198` relies on insertion order, so self-produced state becomes invalid at 1,000 concerns (StateInvalid, 503); the adapter also sorts (`aftercare_store.py:40-41`). Static read plus the reviewer report; not run here | Valid only for registers below 1,000 concerns; no high-volume or long-lived persistence is approved |
| #1402 `fix(aftercare): refuse existing blank FileStateStore documents` | Medium, OPEN | `aftercare_intake.py:267-269` treats an existing blank or whitespace `FileStateStore` document as fresh, so a later write can restart identifiers. Scope is the standalone `FileStateStore`, which the runtime does not use; the connected adapter is not shown to behave the same. Static read plus the reviewer report; not run here | Do not rely on `FileStateStore` for damaged-state refusal; the runtime uses `DocumentStateStore` |

Both issues state that source-repair authority is BLOCKED pending a finite owner correction grant (minimum remaining UNKNOWN, 0, no fresh five, nothing inferred from issue creation). This record claims no new fix, grant or waiver.

### Evidence classes

* Local observed, source-qualified carry-forward: only the author's original runs listed above on `b7e46b3be`, tied to `64c3f9191` by the direct `src` and `infra` tree equality. Constructed synthetic data only.
* Current-metadata observation: PR 1400 merge identity, 19 hosted PR checks, live issue states and the two issue bodies, read 2026-11-10.
* Azure observed: NONE. No resident, professional, human, live, model or release observation.
* Implemented, unverified: the aftercare route on `64c3f9191` itself (no run on that commit), behaviour above 999 concerns, and hosted CI of main beyond the single completed run read.
* Deferred or blocked: #1401 and #1402 source repair (finite owner grant), household or representative self-service and resident accounts, evaluator access and the DPO position, an AI concern pack route, the #132 contractor pack, whole #89, #133, #134 and #440 criteria, and every human, HVE and legal approval.
* Unknown: backlog behaviour at scale, accessibility with assistive technology, and which age bands Housing/Complaints will set.

### Findings, owners and gates

* No new confirmed defect, no confirmed refactoring and no source fix. The two inherited Mediums are already deduplicated as #1401 and #1402; no further issue is opened.
* Remaining backlog by owner: #133 (self-service route, evaluator role, DPO position, AI pack); #134 (perspective walkthroughs and AC-034 to AC-043); #89 (whole delivery-quality epic); #1401 and #1402 (blocked corrections); #132 (separate, blocked); #109 and #111 (sensor-draft parent, excluded).
* Whole #89, #133, #134 and #440 criteria stay unmet. Independent exact-head review and applicable hosted checks of this record remain required.

### Recommendation

CONTINUE, bounded. The evidence permits #134 current-main local screen walkthroughs of the implemented staff-assisted aftercare surface only (constructed synthetic data, existing staff roles, the `#/aftercare` screen on source equal to the tested tree), preserving the two inherited Mediums as stated limitations (keep scenarios below 1,000 concerns and the runtime adapter, not `FileStateStore`) and every exclusion above. This is a recommendation for Root to consume, not permission, not an approval of any requirement, and not a tick of #440, #89, #133 or #134. No fix or pivot is indicated: a confirmed correction is available only through a separately authorized #1401 or #1402 RPI, and any new confirmed defect needs deduplication and its own issue.

### Process record and limits

* Added as a distinct section; no earlier section, log entry or original adverse result was altered. The witness is a locally writable record, not host or model attestation; the model label is asserted. The critique and review are author-executed, not independent. No push, pull request or GitHub write was made, and the only commands run were read-only git, read-only GitHub queries and reads of the Root session files.

## Specialist keyboard probe current-main checkpoint (2026-11-10, Refs #440 #134 #73 #108 #184)

Draft, local-only, not approved. This is a new scoped observation and documentation checkpoint after the specialist keyboard and evidence probe (PR 1414, a child of #134) reached `main`. It is distinct from every earlier section above (all unchanged), is not a source repair cycle or reset, spends none of the #134 correction allowance (C4 of five spent, one left, untouched), and adds no QA campaign, cloud, transport or model budget. A merged child is not whole journey acceptance. It records scoped current-main integration before any closure of whole #134, #73 or #440 or any dependent expansion. It is the focused owner-demo tier: only the existing selectors and one existing synthetic browser walk named below ran; no gate, `--changed`, image, SQL, scanner, model, live, Azure or private-data run was made. Records: [research](../../.copilot-tracking/research/2026-11-10-profile-main-440-1110-research.md), [plan](../../.copilot-tracking/plans/2026-11-10-profile-main-440-1110-plan.md), [details](../../.copilot-tracking/details/2026-11-10-profile-main-440-1110-details.md), [critique](../../.copilot-tracking/plans/critiques/2026-11-10-profile-main-440-1110-plan-critique.md), [changes](../../.copilot-tracking/changes/2026-11-10-profile-main-440-1110-changes.md), [review](../../.copilot-tracking/reviews/2026-11-10-profile-main-440-1110-review.md) and [state](../../.copilot-tracking/rpi-sessions/2026-11-10/profile-main-440-1110-state.json).

### Identities, scope and exclusions

| Item | Identity (read 2026-11-10) |
| --- | --- |
| Trigger | PR 1414 `test: add bounded specialist keyboard and evidence probe`, MERGED 2026-11-10T17:58:44Z as `main` `b23c08e33e4ebdb0aaa1dfd8fa586999448d8ca6`, tree `0bdc704b78b9a3ed95926b5915ae93ae9148032d` (parent `4d8443d44`). PR head `124af0b63b727d3d8889d6900a0bca7d6b70578c`. No closing references |
| Pinned source of this observation | Worktree HEAD and merge base `b23c08e33`, branch `docs/profile-main-checkpoint-440-1110`, clean source at every observation (only own `.copilot-tracking` files untracked) |
| Current origin/main | After a fetch at 2026-11-10T18:07:12Z, `88a17f8b6d3da6dcfcb8b0db19f481f9e257f61e`, one commit past `b23c08e33` that changes only `.github/rubric/scores/latest.json`. No `src`, `docs` or `infra` path differs, so the observed source equals current main source. This is currency as of that fetch, not a later one |
| Hosted checks | All 19 reported PR-head contexts read SUCCESS, including Source projects CI run 42867523237 and Capstone Rubric Scorer run 42867523337 on `124af0b63`. The scorer on `b23c08e33` (run 42870426563, completed success) recorded 78/100 with B6 at 4 in `latest.json`. The earlier 77/78 B6 failure on the same PR (run 42864188813) is preserved as an adverse record. No Source projects CI run for the main head was among the latest four main runs read, so none is claimed |
| Documents (blob at `b23c08e33`) | BRD Agentic Retrofit Programme 0.21.0 `draft` `34d88395de861e9799eb9e24121a21c92c7a5adc`; PRD Zava Forward Retrofit Programme Workbench 0.21.0 `in-review`, `exercise_status` author-complete-unsigned-pending-review-and-owner-acceptance, `c788b917bafaede215f326f0efc71e071a687f1c`; ADR 0003 accepted with amendment 2026-10-15 `d60645397b20fb70ac3d1dc47c7a6c8671201306`; ADR 0006 accepted 2026-10-15 `956da1a3b804c803041fe2e8a312bd9f400273ae`. Draft and in-review are not approval. The BRD AC-034 is a Finance grant criterion and is not the PRD AC-034 used below |
| Issue states (read live) | #134 OPEN `status:not-started`; #73, #440, #108 and #184 OPEN `status:partially-delivered`. Nothing is ticked or closed here |
| Covered | The bounded specialist keyboard and evidence probe, its API helper test, and the Core journey acceptance, perspective walkthrough and scenario manifest registers, on the constructed synthetic fixture |
| Excluded | Whole #134 and #73 acceptance, assistive-technology, voice, user, professional and resident acceptance, the Sensor C2 chain (PR 1412, current chain recorded elsewhere) and the Quality checkpoints (PR 1331 and the 2026-11-09 Quality-main record), which are not duplicated here and need no new live call; any live, Azure, IoT, SQL, model, provider, private-data or deployment observation. The independent #108 (AI) and #184 (IoT) lanes may do read-only metadata work and have no functional dependency on this record |

### Source identity proof (direct comparison)

Compared with `git rev-parse <commit>:<path>`. The four source blobs equal those validated in correction C2 at `cb01c33c42ceef31ee699649ecceedadc487945d`. Commit ancestry and green CI were not used as proof.

| Path | Blob at `b23c08e33` (equal to `cb01c33c`) |
| --- | --- |
| `src/api/checks/specialist_keyboard_browser_check.py` | `e8b7d9f16200896373c86d6b31d728c0d773c28a` |
| `src/api/tests/test_specialist_keyboard_check.py` | `228a5390221b64d9ffb0bd3ecb286308a5e50c7d` |
| `src/core/src/zava_forward/core/journey_acceptance.py` | `e3466b6eafc07d319ce3f2ee835d832b58f34032` |
| `src/core/src/zava_forward/core/perspective_walkthroughs.py` | `f1828b2eb805078421731170c91a3218cc56a411` |

Trees at `b23c08e33`: `src` `901a74c62a8b980b3cbe0b925db2e69f00003a91`, `src/api` `ed94d555101aa9b1be04be32787576a3bbb46960`, `src/core` `0d3caa315d9194e2551de5a95b0d76a75958dd5d`, `infra` `f7f31c0934cfe0bafb4505408706e55aa8ab61e7`. Outside `.copilot-tracking`, the path difference between `cb01c33c42` and `b23c08e33` is the rubric score file, this pack, the knowledge base index and log, and `src/api/README.md`; the only `src` change is the README rewrite of C4. C3 and C4 changed README and RPI records only.

### Observed this checkpoint (local, raw outputs outside the repository)

Raw directory: `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/profile-main-440-observation-1110/` (files `01-identity.txt` to `08-post-run.txt`). Host: Linux, Python 3.12.3, 4 CPUs, 15.6 GiB memory with about 2.8 GiB available at the browser run, no swap. Chromium 1248 from the existing Playwright cache; no browser was installed.

| Step and command (from the worktree root) | Exit and result | Class and limit |
| --- | --- | --- |
| A1 `cd src/api && python3 -m unittest tests.test_specialist_keyboard_check`, system Python | Exit 0, 6 tests OK. The imported `zava_forward.core` resolved to the separate primary checkout `/home/azureuser/source/ama/src/core` (an editable install of that checkout, `03-provenance-A.txt`) | Not current-main proof: the Core source was outside this worktree. Preserved, not discarded |
| A2 `cd src/core && python3 -m unittest tests.test_perspective_walkthroughs tests.test_journey_acceptance tests.test_scenario_manifest`, system Python | Exit 0, 16 tests OK, same out-of-worktree Core path | Not current-main proof, same reason |
| Restore `python3 -m venv /tmp/ama-440-profile-venv-1110`; `/tmp/ama-440-profile-venv-1110/bin/python -m pip install -e src/core -e src/agents -e src/api playwright==1.64.0` | Both exit 0 (`04-restore-venv.txt`). Private environment only; the three `zava-forward-*` packages resolve to this worktree's `src`, Playwright 1.64.0 as pinned by `src/api/pyproject.toml`. The system Playwright was 1.64.1 | Environment restore after the wrong-source finding above, not a product defect. No global install and no network use by the checks |
| B1 `cd src/api && /tmp/ama-440-profile-venv-1110/bin/python -m unittest tests.test_specialist_keyboard_check -q` | Exit 0, 6 tests OK. Core modules and `checks` resolve inside this worktree (`05-attemptB-api.txt`) | Local observed on current-main source, helper level only |
| B2 `cd src/core && /tmp/ama-440-profile-venv-1110/bin/python -m unittest tests.test_perspective_walkthroughs tests.test_journey_acceptance tests.test_scenario_manifest -q` | Exit 0, 16 tests OK, modules inside this worktree (`05-attemptB-core.txt`) | Local observed. The registers are recorded as partial or deferred with none passed, so this shows register integrity, not acceptance |
| Admission before the browser walk | No holder of `/tmp/ama-rpi-heavy.lock` (`fuser` exit 1), `MemAvailable` 2,884,556 kB, the cached `chrome` present (`06-admission.txt`). The 1.5 GiB memory floor was an engineering threshold chosen for this record, not a repository rule | Admission met; no queueing |
| C1 `cd src/api && ZF_BROWSER_SCRATCH=/tmp/z440p PYTHONDONTWRITEBYTECODE=1 flock -n /tmp/ama-rpi-heavy.lock timeout 900 /tmp/ama-440-profile-venv-1110/bin/python -m checks.specialist_keyboard_browser_check` | Exit 0 in about 29 seconds (2026-11-10T18:08:11Z to 18:08:40Z). 714 printed `PASS` lines, 0 `FAIL`, 38 role-screen walks (Resident Liaison Officer 3, Retrofit Coordinator 5, Retrofit Programme Manager 11, Programme Support Officer 11, Building Safety Liaison 2, Quality Inspector 3, Grants and Evidence Officer 2, Contractor 1), 15 deliberate negatives rejected, 15 declared no-table walks, case `ZF-4` only (`07-browser-run.txt`) | Local observed on a loopback owned server with constructed synthetic data. The 714 is a count of printed checks, not of acceptance criteria |

Cleanup: after the run no process of the check remained (`08-post-run.txt`); the empty scratch directory `/tmp/z440p` was removed; the private environment `/tmp/ama-440-profile-venv-1110` and its ignored editable-install metadata were left in place for inspection. No foreign process, lock or data was touched. No tool or admission was missing, so no blocked row arose in this run.

### Historical retained observations (not re-run as new proof)

* C2 on `cb01c33c` (Root `134-keyboard-c2-evidence-1110/`): API helper 6 and Core 16 OK, one walk with 714 PASS, 15 negatives and 15 no-table walks. This checkpoint's counts match it, which is consistent but is a separate observation on a later head, not a new proof of the C2 result. Class: historical.
* C4 (Root `phase134-keyboard-c4-evidence-1110/`): seven canonical witness records, verify exit 0 with disclosed timing notes; README-only change. Original, C1 and C2 witness chains keep their refused or qualified outcomes. Class: historical, preserved, not waived.
* The hosted B6 failure at 77 of 78 and its repair by README only are preserved above. Class: historical adverse record.

### Requirement trace (document-qualified; bounded probe to partial journey requirements)

| Requirement (document, status) | Probe evidence | Class |
| --- | --- | --- |
| PRD AC-034 (in-review): scope, reset and selection-focus announcement | `journey_acceptance` registers it `partial`: keyboard reach, focus visibility and DOM status text for the first listed home plus the workbench check. The 714 PASS lines, 38 role-screen walks and 15 negatives are partial coverage for the first listed home only | Local observed, partial; the full criterion and no-match behaviour are not shown |
| PRD AC-036 (in-review) | Registered `deferred`; the walk observes only that owner or next-action text exists, not that owner, destination, receiver and chase-owner labels agree | Not shown |
| PRD AC-035, AC-038, AC-041 | Registered `deferred`; no probe evidence | Not shown |
| PRD AC-037, AC-039, AC-040, AC-042 | Registered `partial` from existing Core evidence (resident decisions, procurement, exception queue, quality and invoices); the probe adds no evidence for these | Implemented, unverified by this probe |
| PRD AC-043 (in-review) | Perspective register: eleven perspectives, five elements each, zero met; Asset, Procurement and Auditor have no fixture login role | Partial; whole AC-043 unmet |
| BRD (draft), ADR 0003 and ADR 0006 (accepted) | No BRD requirement is approved or met by this probe. ADR 0003 and ADR 0006 constrain journey-derived scope and source layout; nothing here amends or satisfies them | Context only |

### Gaps (exact)

* Roles: Asset, Procurement and Auditor have no fixture login role, so those perspectives stay proxy or deferred; the 38 walks cover eight role names.
* Homes: only the first listed home (`ZF-4`) stands in for all homes.
* Screens: 15 walks reach screens with no evidence table on this fixture, so table-level checks are declared gaps, not passes.
* Endpoint and handoff wording is checked as text presence only, so end-to-end handoff behaviour is not shown.
* Fixture role selection is not Entra authentication or any identity-provider proof. DOM status text and attributes are not screen-reader or other assistive-technology output. No voice, user, professional or resident acceptance exists.
* Not run and therefore Unknown: the workbench baseline and other browser checks, the fourteen-command checklist, images, scanners, SQL, the complete gate, `--changed`, live, Azure, IoT, model and private-data checks, and any run on a later main head. Source projects CI for the main head was not observed.

### Findings, owners and gates

* No new defect, refactor or source repair is claimed or reproduced. The focused observations all passed on current-main source. Existing owners were compared first: #134 owns the walkthrough and AC-034 to AC-043 coverage, #73 the case workbench epic, #440 the stabilization cadence; the independent #108 and #184 lanes are metadata-only. No new issue is opened.
* Whole #134, #73 and #440 closure, genuine end-to-end journey proof and assistive-technology or human acceptance remain open and gated on the remaining evidence and approvals above. Independent exact-head review and applicable hosted checks of this record remain required.

### Recommendation

CONTINUE, bounded. Continue only independent bounded engineering that needs none of the gated surfaces (for example the #108 and #184 read-only metadata lanes). Keep the affected whole #134, #73 and #440 closure and any genuine end-to-end or assistive-technology expansion waiting on the remaining evidence and approvals. This is a recommendation for Root to consume, not permission, not an approval of any requirement, and not a tick of #134, #73 or #440.

### Process record and limits

* Added as a distinct section; no earlier section, log entry or original adverse result was altered. No shared knowledge base file was edited: the pack is already indexed and the index and log are owned by the #108 and then #184 lanes. The witness is a locally writable record, not host or model attestation; the model label is asserted. The plan critique was one read-only subagent pass at plan time and is not an independent assessment of the final pack. The review is author-executed and not independent, and independent exact-head review remains required. No push, pull request, issue or board write was made. Commands were read-only git and GitHub queries, the checks above and one dependency restore into the private environment.

## Household inventory and staff intake current-main checkpoint (2026-11-11, Refs #440 #131 #132 #1362)

Draft, local-only, not approved. This is a new scoped observation and documentation checkpoint after three merges reached `main`: PR 1421 (checker issue 1362), PR 1422 (household inventory, issue 131) and PR 1425 (staff-mediated intake, issue 132), plus an independently identified need to check that household holds still guard ordinary independent QA after the new staff intake. It is distinct from every earlier section (all unchanged), is not a source repair, feature correction or new issue discovery, and adds no QA campaign, cloud, model or spend. A merged increment is not whole issue acceptance. It is the focused owner-demo tier: only existing selectors named below ran; no complete local gate, `--changed` run, image, SQL Server, scanner, live, Azure or private-data run was made. Records: [research](../../.copilot-tracking/research/2026-11-11-inventory-intake-main-440-1111-research.md), [plan](../../.copilot-tracking/plans/2026-11-11-inventory-intake-main-440-1111-plan.md), [details](../../.copilot-tracking/details/2026-11-11-inventory-intake-main-440-1111-details.md), [critique](../../.copilot-tracking/plans/critiques/2026-11-11-inventory-intake-main-440-1111-plan-critique.md), [changes](../../.copilot-tracking/changes/2026-11-11-inventory-intake-main-440-1111-changes.md), [review](../../.copilot-tracking/reviews/2026-11-11-inventory-intake-main-440-1111-review.md) and [state](../../.copilot-tracking/rpi-sessions/2026-11-11/inventory-intake-main-440-1111-state.json).

### Identities, scope and exclusions

| Item | Identity (read 2026-11-11) |
| --- | --- |
| Pinned source of this observation | Worktree HEAD and merge base `0509ddcef14d9c2046791b283fad65229f536202`, tree `69a4812252456e6b854f09ab0560468c89f22e9c`, branch `docs/demo-inventory-intake-checkpoint-440`, clean source at every observation |
| Current origin/main | A fresh fetch at 2026-11-11T00:20:21Z read `7e2744cf7774825b21c73fffbc075b95755239cc`, tree `d77ac24dae1ebd84a9260161d2d1f610acf3f785`, one commit past the pin that changes only `.github/rubric/scores/latest.json` (`chore(rubric): record score 78/100`). No `src` or `infra` path differs, so the observed source equals current main source as of that fetch. Nothing was merged or rebased to refresh. This is currency at that fetch, not a later one |
| PR 1421 | MERGED 2026-11-10T23:50:46Z as `6f5e5007a84ab719013b94d592d5416c7949b453`, head `355cbb0558d9f22824ad9f1c57c8116439033ce0`; closes 1362 (now CLOSED) |
| PR 1422 | MERGED 2026-11-10T23:52:41Z as `83c28132ceb7c8609569c4c4fe9f1f9bca1ded58`, head `500a868ecda23e84bcf1d326817fb1626b7d3ac0`; Refs 131 only |
| PR 1425 | MERGED 2026-11-11T00:09:22Z as `0509ddcef14d9c2046791b283fad65229f536202`, head `204bc6adb2a1b5d429c634e8ed1b9a49f820553a`; Refs 132 only |
| Trees at the pin | `src` `f47636fa76bcf295276c419f178d8d7855f862b9`, `src/core` `06418f54614c1fa2063d3b28c51498bc2eb9ceca`, `src/api` `ccb6944509692f43f80065128321e9d386bb944d`, `infra` `f7f31c0934cfe0bafb4505408706e55aa8ab61e7` |
| Source blobs at the pin | `atlas_tensions_browser_check.py` `b1facccfa2c8396a3c798654a4e0544168659a40`; `test_atlas_tensions_checker.py` `63fd2327751bddce263b3973309975dc720ca882`; `resident_decisions.py` `ba5d1c13e5a368013cc5fb4b6466d9d1a11e76b4`; `test_resident_decisions.py` `21fb8384be3299ecce0c865ea8446176cd1f22ec`; `test_resident_api.py` `425a13720574332aede2624911e8f24500613c31`; `staff_intake.py` `3de31ca27b08ec4de0aa37affd54a2cd9a39ee53`; `test_staff_intake_api.py` `358e34b303277c74383b9e7c1fabf75d32271370`; `test_staff_intake_browser.py` `16f7d4edc5c5df298124ae395ac7121d9ae1750d`; `quality.py` `23f97a33b98f5ede4a8d8c51a7131514e7b834c4` |
| Documents (blob at the pin) | BRD Agentic Retrofit Programme 0.21.0 `draft` (2026-10-24) `34d88395de861e9799eb9e24121a21c92c7a5adc`; PRD Zava Forward Retrofit Programme Workbench 0.21.0 `in-review`, author-complete-unsigned-pending-review-and-owner-acceptance (2026-10-25) `c788b917bafaede215f326f0efc71e071a687f1c`; ADR 0007 Contractor Job Pack and Evidence Intake Delivery Proposed 2026-11-04, not accepted, `abb21088a9bb9771234a305b8052c3bcdd181b33`; ADR 0003 and ADR 0006 accepted, `d60645397b20fb70ac3d1dc47c7a6c8671201306` and `956da1a3b804c803041fe2e8a312bd9f400273ae`. Draft, in-review and proposed are not approval |
| Hosted checks | When read, the pin's Capstone Rubric Scorer run was `in_progress` and the commit's check runs read 3 success and 1 incomplete. No Source projects CI result for the main head is claimed |
| Issue states (read live) | #440, #131 and #132 OPEN (`status:partially-delivered`, #131 also `status:not-started`, #132 `status:not-started`); #1362 CLOSED. Nothing is ticked or closed here |
| Covered | The three merged increments as seen on pinned main, and the QA guard trace after staff intake, on constructed synthetic fixtures |
| Excluded | Unmerged PR 1423 (Capacity CSV and handoff parent, OPEN), PR 1426 (served-transfer report, OPEN) and worker issue 144 (OPEN). The branch 1360 regression is not main acceptance and is not reported as a main defect. Whole #131, #132 and #440 acceptance; the #1420 expansion; any live, Azure, SQL Server, model, provider, private-data or deployment observation |

### Requirement qualification (document-qualified, not interchangeable)

* BRD FR-015 (BR-061, AC-021, `draft`) is the tenure and lease-interest decision route: unverified homes cannot be offered measures, communal works are held until Legal confirms consultation (RULE-023), agreement from one household is never applied to another, and no automated capability interprets a lease. It is the requirement behind `TENURE_HOLD` and the household inventory.
* PRD FR-015 (AC-018, AC-038, `in-review`) is hazard source, referral and retrofit-hold evidence. It is a different requirement; nothing observed here satisfies it, and household tenure holds are not hazard releases.
* BRD FR-016 and FR-017 (AC-022, AC-023) are exception stops and handoff contents. PRD FR-016 (AC-019, AC-039) is the versioned provider-package record and PRD FR-017 (AC-020, AC-042) is the independent per-measure quality-disposition record. Issue 132 cites PRD FR-016 and FR-017; the staff-mediated intake touches them only partly (worker-confirmed evidence as a quality submission, a distinct acknowledgement, and independent QA accept), not provider submission authority, readiness, returns or chronology. ADR 0007 is proposed and does not close issue 132 criterion 6.

### Observed this checkpoint (local, raw outputs outside the repository)

Raw directory: `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/inventory-intake-main-440-observation-1111/`. Host: Linux, Python 3.12.3. Fresh private venv `/tmp/ama-440-inventory-venv-1111` with editable installs of this worktree's `src/core`, `src/agents` and `src/api` (module origins proven under this worktree); no `ZF_DATA`, `.env`, credential or provider variable; `~/.zava-forward` absent before and after; `PYTHONPATH` held only the existing test-helper directories.

| Id and command (existing tests only) | Exit and result | Class and limit |
| --- | --- | --- |
| O1 `cd src/core && PYTHONPATH=tests python -m unittest tests.test_resident_decisions -k inventory -v` | 0; ran 48, 31 ok, 17 skipped (all the `MssqlResidentControls` opt-in cases). Covers inventory integrity, Unknown valid and held, stale link, missing `households` key malformed versus explicit null Unknown, corrupt history never extended, refreshed data never releasing scope or work, count-only identity and route reasons, private projection, deletion keeping the hold, failure races and truthful committed acknowledgement, on the JSON class and the SQLite subclass | Local observed on SQLite and JSON stores. SQLite is a store double and is not MSSQL; the 17 MSSQL cases were not run |
| O2 same dir, `test_resident_acceptance_never_clears_technical_or_hazard_gates` and `test_quality_dependencies_are_scoped_and_unknown_evidence_cannot_release` | 0; ran 2, ok | Local observed: shared resident and quality gates on non-inventory cases |
| O3 `cd src/api && PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest tests.test_resident_api -k inventory -v` | 0; ran 1, ok (`test_http_household_inventory_is_opt_in_refusal_only_and_hidden`). A logged, swallowed "Rule evaluation unavailable ... law store is not loaded" traceback is preserved raw | Local observed over a loopback HTTP fixture; the fixture has no law store, so the rule engine is not exercised |
| O4 same, `tests.test_staff_intake_api -v` | 0; ran 90, 56 ok, 34 skipped (30 `MssqlStaffIntakeApi` cases needing `ZF_STAFF_INTAKE_MSSQL=1`, and 4 JSON cases that need an SQL store contract). Covers capture, restart readback, distinct acknowledgement, append-only correction, self-review and worker-identity denial, contractor and unknown route denial, not-ready pack refusal, unbound or changed resident scope refusal (409, no receipt), stale pack, replay after retry, injected failure leaving no partial receipt, offline capture, privacy allow-list, escalation unknown and the independent QA positive control `test_recorder_is_denied_and_independent_qa_accepts` | Local observed on SQLite (`StaffIntakeApi` base, owned SQLite `SqlStore`) and JSON (`JsonStaffIntakeApi`) stores; corrected 2026-11-11, the original wording said JSON only. Not MSSQL, not a worker or provider portal, not QA, legal or resident approval |
| O5 same, `tests.test_role_endpoint_inventory tests.test_content_standard -v` | 0; ran 42, ok | Local observed: every role against the endpoint inventory including the four new field routes, contractor canaries and plain-language audit including `staff-intake.js` |
| O6a `tests.test_atlas_tensions_checker` before Playwright was present | Exit 1, `ModuleNotFoundError: No module named 'playwright'`, 1 import error, 0 tests run | Actual dependency gap of the private venv, preserved; not a product defect |
| O6 restore `pip install playwright==1.64.0` (the declared dev pin) into the private venv | Exit 0 | Environment restore after the actual failure; no global or shared install |
| O6b `ZF_BROWSER_TESTS=1 ... flock -n /tmp/ama-rpi-heavy.lock timeout 900 python -m unittest tests.test_atlas_tensions_checker -v` (lock free by `fuser` exit 1, 8.2 GiB available, cached Chromium 1248) | 0; ran 20, OK, 0 skipped (the same selector without the opt-in ran 20 with 3 skipped, exit 0, and is not browser evidence) | Local observed: checker 1362 real-DOM negatives on a loopback owned server with constructed data. Checker-only; says nothing about product behaviour |
| O7 `tests.test_staff_intake_browser` | Not run, blocked: needs `ZF_STAFF_INTAKE_BROWSER=1` and the pinned `ZF_AXE_PATH`, both absent; the prerequisite was not installed or fetched | The screen's four axe states are not observed on this head; the 1425 browser result is historical only |

### Combined-journey gap (exact)

* No existing selector exercises the combined journey of an inventory-managed case, staff-mediated capture or correction or acknowledgement, and then independent QA. A scan of every `src/*/tests/test_*.py` function found no body that sets up an inventory together with `accept_quality`, `submit_quality`, field capture or `staff_intake`, and none that calls QA accept or handover with tenure or inventory setup.
* The QA positive control (`test_recorder_is_denied_and_independent_qa_accepts` on the non-inventory case ZF-3) passed in O4. The inventory-managed refusal control exists only as the shared function: O1 asserts `resident_gate` returns the unchanged `TENURE_HOLD` with and without a scope binding even for fully verified linked households, and a fully linked, current inventory releases nothing.
* Static trace (read, not run in combination): `_inventory_managed` opts a case in when `tenure_household_inventories` is present, `tenure_review_required` is truthy, `tenure_reports` is non-empty, or `tenure_reports` is present and not a list; then `resident_gate` returns the inventory reasons plus `TENURE_HOLD` whatever the bindings. `accept_quality` and `hand_over_quality` call `require_resident_clear`, so QA acceptance and handover refuse; `return_quality` is not guarded. `staff_intake.py` never references the inventory or the hold, and acknowledgement leaves the quality state `Submitted`, so acknowledgement and scope binding cannot clear `TENURE_HOLD`. `_res_scope_record` refuses a new scope on an inventory-managed case; a scope bound before the inventory was recorded stays bound but the gate still holds. Class: implemented but unverified at the combined-journey level. This is a verification gap, not a reproduced defect.

### Requirement trace (document-qualified)

| Requirement (document, status) | Decision and code | Test and observation | Class | Remaining owner |
| --- | --- | --- | --- | --- |
| BRD FR-015, AC-021 (draft), tenure route and unverified-home hold | Caller-declared household inventory and unchanged `TENURE_HOLD` in `resident_decisions.py` (PR 1422); Legal interpretation stays human | O1 and O3 pass on JSON and SQLite: Unknown valid and held, stale or malformed links refuse, no action releases the hold | Local observed (partial); caller-declared, not a verified roster; MSSQL not run | #131 open: universal home and household coverage, pre-offer integration, responsibility appointments, Legal and data-owner acceptance |
| BRD AC-021 "agreement from one household is never applied to another" | Per-household report link and digest in the inventory | O1 one-of-two households missing link refuses the gate and scope | Local observed (partial); constructed two-household fixture | #131 |
| PRD FR-015, AC-018, AC-038 (in-review), hazard and retrofit hold | `require_safety_clear` in the QA path, separate from tenure | Not observed here; O2 exercises shared gates on non-inventory cases only | Not shown by this checkpoint | Existing hazard owners; not #131 |
| PRD FR-016, FR-017, AC-019, AC-020, AC-039, AC-042 (in-review), partial via issue 132 | `staff_intake.py` orchestrates `job_pack.py` and `submit_quality`; ADR 0007 proposed | O4 and O5 pass on the SQLite and JSON stores (not MSSQL): separate acknowledgement, independent accept, denials, scope-binding refusal | Local observed (partial); MSSQL, browser axe and independent identity not observed | #132 open: named-owner escalation, provider identity (#116), human and operational acceptance |
| Household holds guard ordinary independent QA after staff intake | `require_resident_clear` in `accept_quality` and `hand_over_quality` | Positive control observed (O4); refusal control only via the shared gate (O1, O2) | Implemented, unverified at the combined level | #440 owns this stabilization cadence; whether a regression test is added awaits the owner under #131, #132 or #440 |
| Checker 1362 (checker-only) | Exact Current design version matching | O6b 20 tests OK in a real browser, no skip | Local observed | Closed; whole #149 and #233 remain open elsewhere |

### Findings, owners and gates

* No new defect, necessary refactor or source repair is confirmed or reproduced. All observed selectors passed on current-main source; the only failure was the O6a dependency gap of the private venv, restored from the declared pin. Existing owners were compared first: #131 owns the household coverage and hold, #132 the staff intake, #440 the stabilization checkpoint and its criteria on requirement reconciliation. No new issue is opened and no issue criterion is ticked.
* The combined-journey verification gap above is the one thing this checkpoint cannot show; it is not a failure.
* Named human, consent and legal boundaries remain: Legal interpretation of tenure and lease, Home Ownership data owner, the actual household roster, resident consent, QA approval, the owner-selected identity and delivery decision (ADR 0007 proposed) and production identity. Synthetic fixtures, SQLite and the loopback HTTP server are not MSSQL, live, an actual worker, QA or resident approval.
* Original authoring and marker qualifications of the merged PRs remain historical: PR 1421 disclosed a withheld and restored Review artifact at implement-done, PR 1422 an already-present final Review at implement-done and PR 1425 an implement-done validator KeyError without a preceding successful validation. A local witness exit 0 here is not strict chronology attestation.

### Recommendation

CONTINUE, bounded. Continue independent engineering that does not depend on the gaps. Keep whole #131 and #132 closure, the #440 closure and any dependent expansion (including #1420) waiting on the remaining evidence and approvals above. Proposed for the owner, not decided: whether to authorize one existing-test addition for the combined QA guard under an existing owner (#131, #132 or #440). Pivot or requirement relaxation awaits the owner. This is a recommendation for Root to consume, not permission, not approval of any requirement and not a tick of #131, #132 or #440.

### Process record and limits

* Added as a distinct section; no earlier section or adverse record was altered. The witness is a locally writable record, not host or model attestation; the model label is asserted. Strict state parse, `load_artifacts` and a passing preflight ran before each recorded marker. The plan critique was one subagent pass at plan time and is not an independent assessment of the final record. The review is author-executed and not independent; independent exact-head review and applicable hosted checks remain required. No push, pull request, issue or board write was made. Commands were read-only git and GitHub queries, the existing tests above and one dependency restore into the private environment.

### Follow-up observation and readiness correction (2026-11-11, additive)

* O7 above stays as recorded (blocked). Follow-up O7b ran the existing `tests.test_staff_intake_browser` selector from `src/api` on head `d174ab85347a49386c92a42aefe0513f6a3a9f58` with the private venv, the existing owned asset `/tmp/axepk/package/axe.min.js` (reads axe 4.10.3, sha256 `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb`, equal to the digest the test pins) and `ZF_STAFF_INTAKE_BROWSER=1`, under a free nonqueued `flock -n /tmp/ama-rpi-heavy.lock` (00:36:53Z to 00:37:01Z). Exit 0, 2 run, OK, 0 skipped, five axe states with no violations. Class: local observed on constructed synthetic data, JSON store and a loopback server. It is not accessibility acceptance, not MSSQL and not an inventory-managed or QA journey.
* A committed-range `git diff --check` found a trailing blank line in the changes record, which the original clean claim had not covered; it was corrected in a follow-up commit and recorded in the changes and review records.
* The recommendation above stays historical. Root has routed one test-only E2 under existing #132 on `7e2744cf7774825b21c73fffbc075b95755239cc`; it is not yet run or read here, so the combined inventory-managed staff intake to independent QA acceptance gap stays unverified. Whole #131, #132 and #440 stay open; no #1420 expansion and no approval is claimed.

### Store classification correction (2026-11-11, additive)

* Root's independent review found that O4 was classified too narrowly as "JSON store only" in the O4 row, the requirement trace row for PRD FR-016 and FR-017, and the earlier research, changes and review wording; those older records are kept as history. Raw check of `o4-api-staff-intake.err`: the 90 tests split as 30 `StaffIntakeApi`, 30 `JsonStaffIntakeApi` and 30 `MssqlStaffIntakeApi`. `StaffIntakeApi` inherits `ProcurementApiFixture`, whose `sql = True` makes `make_store` build an owned SQLite `SqlStore`; `JsonStaffIntakeApi` sets `sql = False`; the MSSQL class is opt-in. So O4 covered SQLite and JSON, not MSSQL. The counts 90 run, 56 ok and 34 skipped (30 MSSQL, 4 JSON) are unchanged. SQLite is a store double, not MSSQL, live, an actual worker or QA, legal or resident approval. The O7b statement "JSON store" refers to the browser fixture as recorded and is unchanged. No test was rerun and no source changed.

## Closure-wave integrated-main checkpoint (2026-11-11, Refs #440 #80 #144 #1360 #1419)

Draft, local-only, not approved. One bounded observation of existing focused selectors after the feature wave PR 1428 (permit timing and attribution, issue 144), PR 1426 (committed transfer reload errors, issue 1360), PR 1423 (Capacity and handoff CSV downloads including child PR 1424, issues 80 and 1419) and documentary PR 1430 reached `main`. It is not a Quality campaign, not a full gate and not acceptance.

### Identities, scope and exclusions

| Item | Identity (read 2026-11-11) |
| --- | --- |
| Pin of the planned work | `8aedb56b5909903abd6c6f84777b49f237c1cbb0`, tree `9e0e8efda1145ea4c990d0208e8cf6d07f0f8af4` |
| Observed main | `e0dec207dab2cce2e2bf9d0084e1cdea9d10ec1d`, tree `4fcaac76dca4c6dd5cb252fe676a0dad20d2d7d4`. Fetch verified the only movement from the pin is `.github/rubric/scores/latest.json` (one rubric commit). Merged into the topic with an ordinary no-ff commit `04973ebf2ffc5a63954bfbaeb727d555662e3710` before any test; no conflict, rebase or reset |
| Observed candidate | Merge commit `04973ebf2`, tree `552970ba51936533bf7401d74ec2120b46e09006`. `src` `84f7b054e66db107edf5753151dce23912da4bac`, `docs` `f3d6a06c66566ea572d64db16f988da4d2f93fcb`, `infra` `f7f31c0934cfe0bafb4505408706e55aa8ab61e7`, `tools` `432a4e8f7d74f26e88a55dd937c9c6f193016da9` and `.github` `ae8da14e60c30758b90462553f51f6ba08d974c0` equal main's; the only differences from main are `.copilot-tracking/` files. Clean source at every observation |
| Merged increments | PR 1428 `05f11ebe9`, PR 1426 `01f461dd7`, PR 1423 `3dbb79e90`, PR 1430 `8aedb56b5` (documentary) |
| Source blobs | `server.py` `9227eb9842c81aead8f8f14587f6a5ac118b3f0e`, `app.js` `734aab48bbf32292fb5d6668cbecfe7fff8b757a`, `ops.js` `4ef77471a07949858901dc00254c63eeccf23ef0`, `capacity_browser_check.py` `6a4487eb9e31898c8931dede4e0bc568b8f8dba8`, `sqlstore.py` `01a3a44c926981fbf02ba26e91fc23b9fc710225`, `assistants.py` `7057beaefd4c60ef36942c21996e701ba2247baa`, `ai.py` `580838fe73ea18533291ebead4db0db7273097f2`, `ai_consumption.py` `4ff3848d4d3025c79aebc0a986da319155f37d48` |
| Documents and status | BRD 0.21.0 `draft` `34d88395de861e9799eb9e24121a21c92c7a5adc`; PRD 0.21.0 `in-review`, author-complete-unsigned-pending-review-and-owner-acceptance, `c788b917bafaede215f326f0efc71e071a687f1c`; ADR 0001 Proposed `d42fa5c4615f4107cee83e07555dba6985c1f53e`; ADR 0006 Accepted 2026-10-15 `956da1a3b804c803041fe2e8a312bd9f400273ae`; ADR 0007 Proposed, not accepted, `abb21088a9bb9771234a305b8052c3bcdd181b33`. Only ADR 0006 is approved |
| Issue states (read live) | #1360 and #1419 CLOSED with 4 of 4 and 7 of 7 criteria ticked (earlier closures, unchanged); PR 1424 MERGED; #80, #73, #144, #131, #132, #440 and #1420 OPEN. Nothing is ticked, closed or opened here |
| Hosted checks | Not read or claimed for this exact head |
| Excluded | PR 1425 (staff intake) and PR 1422 (household inventory) are on the tree but have no selector here; this result says nothing about them. Whole importer suite (82 tests, N4) omitted by Root: `TransferFailureTests` covers the modified error-contract surface; this is a scope omission, not a skipped or passed full suite. SQL Server, Docker, the full gate and Core 3057 were not used. The #132 candidate `fdf0d3beb` is unpublished, under separate independent review and excluded, see below |

### Observed this checkpoint (local, raw outputs outside the repository)

Raw directory: `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/closure-wave-main-440-observation-1111/` (one `.out` and `.err` per id). Host Linux, Python 3.12.3. Private venv `/tmp/ama-440-closure-venv-1111`, new owned private HOME (never the real HOME), `ZF_DATA` unset, `~/.zava-forward` absent before and after, no `.env` or private data read. All commands ran under `env -i`, existing tests only, once each, none retried.

Dependency path (preserved): the import preflight `import zava_forward.core ... playwright` in the fresh venv failed with `ModuleNotFoundError: No module named 'zava_forward'` (exit 1). Only then were the local `src/core`, `src/agents`, `src/api`, `src/importer` and declared `playwright==1.64.0` installed (exit 0); every module and the `dataset` helper origin was proven under this worktree. Prerequisites read: cached Chromium 1248 reached through a new symlink in the private `HOME/.cache` to the existing cache (not modified), `node` v24.21.0, the lock free (`fuser` exit 1), about 9 GiB available, axe asset sha256 `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb` (equal to the pin, reused, not refetched).

| Id and selector | Exit and result | Class and limit |
| --- | --- | --- |
| N1 `src/core` `tests.test_priority_order.SqliteC4Corrections` | 0; ran 21, OK, 0 skipped | Local observed on an owned SQLite store double (PR 1426 reload contract). Not MSSQL; the `Mssql*` subclasses were not selected |
| N2 `src/core` `tests.test_ai_consumption.ConsumptionTests` | 0; ran 34, OK | Local observed on the in-memory port (`mssql = False`) |
| N3 `src/importer` `tests.test_import_exceptions.TransferFailureTests` | 0; ran 8, OK | Local observed, owned SQLite and JSON fixtures |
| N5 `src/api` `tests.test_ai_consumption_api.ConsumptionApi` | 0; ran 32, OK (59 s) | Local observed permit timing and attribution on owned fixtures; no model or cloud call |
| N6 `tests.test_unaccepted_handoff_csv_api.UnacceptedHandoffCsv` | 0; ran 13, OK | Local observed CSV bytes, read-only and role boundaries on a loopback fixture |
| N7 `tests.test_handoff_api.HandoffApi` and `tests.test_list_export_api.ListExportApi` | 0; ran 18 (7 and 11), OK | Local observed |
| N8 `tests.test_role_endpoint_inventory.RoleEndpointInventory` | 0; ran 24 (14 own and 10 inherited from `Matrix`), OK | Local observed: every role against the endpoint inventory |
| N9 `tests.test_case_journey` | 0; ran 31, OK | Local observed, Node subprocess DOM double, no browser |
| N10 `tests.test_content_standard`, `tests.test_static_assets`, `tests.test_capacity_browser_check` | 0; ran 28 (18, 5 and 5), OK | Local observed copy audit of changed `app.js` and `ops.js`, static assets, scanner unit checks |
| B2 `tests.test_handoff_read_guidance`, `ZF_BROWSER_TESTS=1`, one external `flock -n -E 99` | 0 (not 99, lock acquired); ran 9, OK, 0 skipped | Local observed in real Chromium, constructed data, loopback server |
| B1 `tests.test_unaccepted_handoff_download_ui`, `ZF_BROWSER_TESTS=1`, self-locking, no outer lock | 0; ran 6, OK, 0 skipped | Local observed real download, read-only and role boundaries in Chromium; the class took the lock itself |
| B3 `python -m checks.capacity_browser_check --axe /tmp/axepk/package/axe.min.js` (no `--mssql`), self-locking, ONE run | 0; seeded, empty, failure and retry, transport, 403, abort and 401 scenarios PASS; four axe states (seeded capacity, packages unavailable, workorders unavailable, empty capacity), each `violations: []`, none "NOT RUN" | Local observed on a generated synthetic seed in an owned store and a loopback server. One server-side `BrokenPipeError` client-disconnect line during the injected abort scenario is preserved in `B3.err` and was the harness's own scenario, not a failure |

Expected counts equalled actual counts for every selector; no skip appeared in any selector. No failure, blocked resource or busy lock occurred.

### Requirement trace (document-qualified)

| Requirement (document, status) | Code and test | Class | Remaining owner |
| --- | --- | --- | --- |
| PRD FR-066 and AC-120 (`in-review`, AC-120 previously "Not run"); BRD FR-057 and AC-112 (`draft`): owned staff exception queue including unaccepted handoffs | Read-only CSV copy and download of unaccepted handoffs (`server.py`, `app.js`, `ops.js`); N6, N7, N8, N9, B1, B2 | Local observed (partial): the read-only copy and its role and download boundaries on synthetic data. The queue's ownership, escalation and handling are not shown | #1419 (closed, criteria unchanged), #73 and #440 |
| PRD FR-008 and AC-010, AC-011 (capacity gate, `in-review`) | Capacity page and downloads; B3 | Local observed (partial) for the page, downloads, failure states and four axe states. The deterministic capacity gate itself is not exercised by these selectors; the CSV control is not the gate | #80 and #73 (open) |
| BRD NFR-012 (`draft`) and PRD NFR-017 with AC-109 and AC-110 (`in-review`): metering, attribution and bounds. PRD AC-100 and AC-101 are a conversation requirement and are not these | Permit timing and server-bound attribution (`ai.py`, `ai_consumption.py`, `assistants.py`); N2, N5 | Local observed on in-memory and owned-SQLite fixtures; no model call, no MSSQL, no cost run | #144 (open) |
| Issue 1360 criteria only (no BRD or PRD requirement cited): truthful committed-reload outcome | `sqlstore.py`; N1, N3 | Local observed on SQLite and owned fixtures; MSSQL cases not run | #1360 (closed), #80 for the importer, #440 |
| ADR 0001 (Proposed) for the Excel transition and hosting | Not exercised beyond the above | Not shown | #80 and #144 |

Local observed here means constructed synthetic fixtures, owned temporary SQLite or JSON stores and loopback servers on one host. Azure observed: none. Implemented but unverified: MSSQL variants of N1, N2 and N3, deployed hosting, the actual queue handling. Blocked: none. Unknown: assistive-technology behaviour.

### Separately owned gap and resume point (issue 132)

The combined inventory-managed staff intake to independent QA journey stays implemented but unverified on main. Its test-only forward adoption candidate is the local, unpublished branch `test/demo-inventory-intake-qa-132-1111`, head `fdf0d3beb`, not an ancestor of main, under independent exact-final review owned by #132. Its tests are excluded and not duplicated here. Resume condition: Root's #132 disposition of that candidate, then a refresh against the then-current main.

### Findings, gates and recommendation

* No defect, necessary refactor or source repair is observed or reproduced. No new issue, no correction budget drawn: #80 C5 stays spent with no C6; #1360 and #144 E1 and E2 stay spent with three remaining each. No criterion is ticked.
* Human and legal boundaries remain: no consent, Legal, identity, QA, resident, production, live or deployed acceptance, and no accessibility acceptance or WCAG conformance is inferred from axe, fixtures, SQLite or loopback runs. No fresh web-interface-guidelines review was performed.
* Affected gates: whole #80, #73, #144, #131, #132 and #440 stay open. Independent lanes that need none of the gated surfaces may continue.

Recommendation (proposed for the owner, not a decision or approval): CONTINUE, bounded. The merged increments show no regression on the selected local selectors. The #1420 resident-choice CSV expansion is no longer waiting on this checkpoint: its disposition here is that the selected selectors passed with no blocking finding, so planning may proceed under its own independent scope, while the #132 combined gap, whole-issue closure and every human or accessibility acceptance remain open and independent of it.

### Process record and limits

* Added as a distinct section; no earlier section or adverse record was altered. Root's admission amendment was committed before the merge and any observation. The witness and model label are locally asserted, not attested. The plan critique was one subagent pass at plan time. The review is author-executed and not independent; independent exact-head review, human approval and applicable hosted checks remain required. No push, pull request, issue or board write was made. Commands were read-only git and GitHub queries, the existing tests above and one dependency restore into the private venv after an actual import failure.

## Resident-choice CSV feature-wave integrated-main checkpoint (2026-11-11, Refs #440 #1420 #1432 #80 #73)

Draft, local-only, not approved. One bounded observation of existing focused selectors on main after PR 1435 (resident-choice page CSV, issue 1420) was squash-merged, together with the four inventory and QA cases merged by PR 1432. It is not a Quality campaign, not a full gate and not acceptance.

### Identities, scope and exclusions

| Item | Identity (read 2026-11-11) |
| --- | --- |
| Planning pin | `1b169fe7d4f9b5a005123c8eb1825028ea431612` (before PR 1435) |
| Observed main | `e09b21f1d7effb6f5a4bfff8315db99bf59c2372`, tree `9a52f75ea5bc4ac39f0e7f468c45ed2301e931a6`, PR 1435 squash-merged 2026-11-11T02:40:30Z. Fresh `origin/main` equalled it. Merged into the topic with an ordinary no-ff commit `1b3d178d37449b6ce1940ff17d4042cdbea048dd` before any test; no conflict, rebase or reset |
| Observed candidate | `src` `87ea0ed8db9f180aec258eed42ca6232a7c97b6a` (equal to the reviewed PR candidate head `1febb4b0` and tested `07041ce0`), `docs` `9a33d247`, `infra` `f7f31c09`, `tools` `432a4e8f`, `.github` `8ee22819`, all equal to main; only own `.copilot-tracking/` files differ. Clean at every run |
| Source blobs | `server.py` `749d3d3ac8492a081610d3082cdfd1bd9bf818bf`, `resident_choice_export.py` `86b6c75a6a0d8f40355391d8758fdb5606a1dbe6`, `role-screens.js` `77f15dc72f1bf26233214122086e87e05570c728`, `role_screens_browser_check.py` `b5bf1ceaadb4dc46b04aae66676e22c01bc9b62c` |
| Documents and status | BRD `BRD-2026-AMA48-001` `docs/brds/agentic-retrofit-programme-brd.md` v0.21.0 `draft`, blob `34d88395`; PRD `PRD-2026-AMA48-001` `docs/prds/zava-forward-retrofit-programme-demonstrator.md` v0.21.0 `in-review` (`author-complete-unsigned-pending-review-and-owner-acceptance`), blob `c788b917`. A second PRD file, `docs/prds/proper-warm-retrofit-programme-demonstrator.md` (same `prd_id`, v0.13.0), reuses numbers and is not cited. ADR 0001 and 0007 Proposed; only ADR 0006 is Accepted |
| Issue and hosted states | #1420 CLOSED by Root's read (six criteria ticked); #80, #73 and #440 OPEN. PR 1435's 19 hosted checks were reported SUCCESS by Root before merge. Main's own scorer run 42947632230 was in progress and no main Source CI run was seen at Root's observation: pending or unobserved is not claimed as passed |
| Excluded | Whole Capacity, importer suite, SQL Server, Docker, `test_case_journey`, story 232s, the full gate, model, cloud and private data. This is a scope choice, not a skipped or passed suite. The earlier PR 1433 checkpoint was observed on `e0dec207`, before the CSV integration, and is historical |

### Observed this checkpoint (local, raw outputs outside the repository)

Raw directory: `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/choice-wave-main-440-observation-1111/`. Linux, Python 3.12.3, task-private venv `/tmp/ama-440-choice-venv-1111`, owned private HOME with the existing Chromium cache linked, `ZF_DATA` unset, `~/.zava-forward` absent, no `.env` or private data. Commands ran under `env -i`.

Adverse and dependency record (preserved): the import preflight in the fresh venv failed with `ModuleNotFoundError: No module named 'zava_forward'` (exit 1); only then were `src/core`, `src/agents`, `src/api` (editable) and `playwright==1.64.0` installed (exit 0). The importer was not installed. Module origins for core and api resolve under this worktree (agents is a namespace package with no `__file__`; its tests path is the worktree's). First C2 attempt failed 9 of 9 with `FileNotFoundError: 'node'` because my `env -i` PATH omitted it. The error arose inside test execution: the nine tests errored before their Node child programs could run. It is kept as `C2-attempt1-node-missing.*` and C2 was rerun once with `node` on PATH (see the process qualification at the end of this section). Other selectors had already passed and were not rerun.

| Id and selector | Exit and result | Class and limit |
| --- | --- | --- |
| C7 `src/core` `tests.test_resident_choice_queue` | 0; ran 4, OK | Local observed; the unchanged JSON queue projection the CSV copies |
| C1 `src/api` `tests.test_resident_choice_export` | 0; ran 30, OK | Local observed: serializer and HTTP route on owned fixtures, including the three review-status regressions |
| C2 `tests.test_resident_choice_screen` | 0 on rerun; ran 9, OK (first attempt environment error above) | Local observed, Node vm double |
| C3 `tests.test_role_endpoint_inventory.RoleEndpointInventory` | 0; ran 24, OK | Local observed, roles against the inventory |
| C4 `tests.test_list_export_api.ListExportApi` | 0; ran 11, OK | Local observed |
| C5 `tests.test_role_screens_conformance.RoleScreenConformance` | 0; ran 11, OK | Local observed |
| C6 `tests.test_content_standard.CopyAudit` | 0; ran 18, OK | Local observed copy audit |
| I1 four named `test_inventory_hold_*` cases on `StaffIntakeApi` and `JsonStaffIntakeApi` | 0; ran 4, OK | Local observed on SQLite or JSON stores; MSSQL class not selected. Co-observation only: no new combined journey and not whole #132 |
| B1 `python -m checks.role_screens_browser_check 232`, `ZF_AXE_JS` pinned (sha256 `880970c0...` verified), one `flock -n -E 99`, `timeout 900` | 0; 42 PASS lines including the download link and CSV attachment checks, axe 4.10.3 no violations, incomplete empty, Chromium 156.0.8078.4 | Local observed on a synthetic loopback server, one role |

Static expectation 107 plus 4 equalled actual counts for every selector (4, 30, 9, 24, 11, 11, 18 and 4); no skip appeared. The B1 PASS count equals the candidate's earlier 42, which remains candidate history, not main evidence.

### Requirement trace (document-qualified, proposed)

| Requirement (document, status) | Code and test | Class |
| --- | --- | --- |
| PRD FR-046, AC-037, AC-056 (`in-review`): pause or withdrawal per measure; no consent or sanction inferred | `resident_choice_export.py`, `server.py`, `role-screens.js`; C1, C2, B1 | Local observed (partial): read-only copy of recorded state on constructed fixtures |
| BRD FR-013 and FR-014 (`draft`) | same | Local observed (partial): display only; no consent, readiness or approval inferred |
| PRD FR-048, AC-065 | same | Weak, partial link for human confirmation: the CSV carries only a bounded update status, no named owner |
| ADR 0006 (Accepted) | route and tests in `src/api` | Layout only |

Azure observed: none. Implemented but unverified: MSSQL variants, deployed hosting, actual-record export, retention, privacy review. Unknown: assistive-technology behaviour. The trace links are proposals of this checkpoint; issue 1420 cites none.

### Findings, gates and recommendation

* No defect or source repair observed; no new issue, no correction budget drawn, no criterion ticked here.
* Remaining boundaries: whole #80, #73 and #440 stay open; no production, real-data, privacy, retention, resident consent, human or assistive-technology acceptance is inferred. Axe, fixtures and loopback runs do not show WCAG conformance. No fresh web-interface review was done; no web file changed.
* Affected gates: acceptance of the merged feature waits on main's own CI outcome, not read here. Independent lanes that do not need the CSV surface may continue.

Recommendation (proposed for the owner, not a decision): CONTINUE, bounded. Resume conditions: main CI and scorer outcome for `e09b21f1d` read and green; a combined inventory to QA journey claim needs its own owner review under #132.

### Process record and limits

* Added as a distinct section; no earlier section or adverse record was altered. The admission amendment was committed before the merge and any test. The single plan critique is the original one (conformant after CW-01 to CW-06); no second critique ran. The review is author-executed, not independent; independent exact-head review, human approval and hosted CI remain required. Model label locally asserted. No push, PR, issue or board write was made.

### Dated process qualification (2026-11-11)

* The plan required Root direction before any rerun of a failed selector. C2 was rerun after the omitted-`node` PATH error without that direction. This is a process exception, not retrospectively authorized and not fully conformant execution.
* The successful C2 (9 OK) is an environment-corrected observation, not a pristine once-only campaign. The first attempt is retained raw: it errored 9 of 9 with `FileNotFoundError: 'node'` inside test execution, before the Node child programs could run. It is not evidence that no test logic ran.
* The original plan and author Review are unchanged. No source correction cycle is spent.
* Later Root observation (not an original runtime read): `origin/main` was `22a30cd92b9a3e1b436dc94cf747a3fc147fb51a`, differing from observed `e09b21f1d` only in `.github/rubric/scores/latest.json`. Main Capstone Rubric Scorer 42947632230 completed SUCCESS on `e09b21f1d`. No separate main Source CI run was observed and none is claimed green. The tested pin and source are unchanged; no integration or rerun was done. No broad acceptance or closure is inferred.

## Keyboard probe compatibility integrated-main checkpoint (2026-11-11, Refs #440 #132 #134)

Draft, documentary only, not approved. This is a small checkpoint after merged PR 1438 reached `main`. It runs no test, browser, SQL, Docker, model, provider or cloud check, changes no source, configuration, test, workflow or requirement, and opens no issue. Every earlier section is unchanged.

### Identities, scope and exclusions

| Item | Value (read 2026-11-11 by read-only Git and `gh`) |
| --- | --- |
| Pinned and fresh `origin/main` | `74e63363bdcb6f9d420ff9c71b8332a9baf0044b`, tree `e89381c5fa93d093ca8ab90f95812a023c1d3e7a`; a fetch before edits showed no movement from the pin |
| PR 1438 | Merged 2026-11-11T04:43:41Z by squash into `74e63363`, zero closing references; assessed head `f62d4b66ed96d54ace8b42343c30cdea2140a614` with the same tree as the merged tree |
| Covered | PR 1438 (bounded repair of the existing keyboard probe for the staff intake screen), under existing issue 132 and the 440 cadence |
| Excluded | The unpublished #134 connected-home candidate `468bdd3` (a High checker false pass, no correction authority; see the existing [#134 blocker comment](https://github.com/jmservera/ama/issues/134#issuecomment-6786645682)); `main` is not claimed to contain it. Also issues 149, 233, 80 and 73 |
| Documents (blob at the pin) | BRD 0.21.0 `draft` `34d88395de861e9799eb9e24121a21c92c7a5adc`; PRD 0.21.0 `in-review`, author-complete-unsigned-pending-review-and-owner-acceptance, `c788b917bafaede215f326f0efc71e071a687f1c`; ADR 0003 Accepted with amendment (2026-10-15) `d60645397b20fb70ac3d1dc47c7a6c8671201306`; ADR 0006 Accepted (2026-10-15) `956da1a3b804c803041fe2e8a312bd9f400273ae`; ADR 0007 Proposed 2026-11-04, not accepted, `abb21088a9bb9771234a305b8052c3bcdd181b33` |

Product delta is zero in behaviour: one `NO_REGION_GAPS` entry for `staff-job-pack-intake` in the existing probe, a seventh unit test and a README count change from five to six. The unknown-screen and unexpected-table fail-closed predicate is unchanged. The fixture has no work orders, so the screen renders no table for the seven staff intake roles; the entry declares that gap and is not a pass. Root and the independent reviewer read the supplied change diff; the PR touched 24 paths including tracking evidence.

### Evidence, origins and classes

| Evidence | Origin and date | Class |
| --- | --- | --- |
| Original RPI categories (research, plan, critique, changes, review) and the independent assessment, in the merged tree under `.copilot-tracking/` (2026-11-11 issue-132-keyboard-compat-1111) | Committed, preserved with the original adverse records | Committed record |
| Independent published review `3e182ded-9135-47cc-a341-58186013ee67`: approve, zero findings; [durable PR comment](https://github.com/jmservera/ama/pull/1438#issuecomment-6786933451) | Root-read 2026-11-11 | Independent review of the PR 1438 scope only; not whole-issue acceptance |
| Retained original browser log (`/tmp/zf132-e4/browser.log`, 863 lines, not copied here): one non-queued run on source candidate `f8939a5a438b3fac62c548d2a42c50f36f8a2778`, 805 printed assertions, 15 negatives, 46 OBS lines, 22 declared gap walks, seven staff intake roles with no regions | Local, before merge; `git diff f8939a5a 74e63363 -- src` is empty (verified 2026-11-11) | Dated, source-equivalent local observed output. Not a fresh main run, not acceptance testing, not Azure. Axe not run; the order-read HTTP status and the cause of the empty order state were not observed |
| Merged compact validation: seven helper tests, full API `mypy` over 232 files, Ruff check and Ruff format over 149 files, each exit 0 after a CI-style private install | Merged tree validation record | Local observed. The original missing tool, the 24, 4 and 2 error configurations, the additional classification run, the limited pipeline exit and the critic runtime and scripted-edit exceptions remain explicit adverse history; this is not pristine conformance |
| Hosted Source projects CI run 42958485921 on head `f62d4b66`: success for the api, core, importer, orchestrator, agents, namespace, image-paths, changes, no-working-data and MSSQL jobs; Root read all 19 PR checks as success, including the rubric score (78 of 78) | `gh api` and Root read 2026-11-11 | Hosted CI only. Four jobs show 12 skipped steps each (causes not examined); test-level skips are not known and no zero-skip claim is made |

Hosted success is not a deployed Azure result, a real SQL lock crossing, a provider or identity check, resident or professional consent, human acceptance or production acceptance.

### Requirement trace (document-qualified, proposed)

| Requirement (document, status) | Evidence | Class |
| --- | --- | --- |
| PRD AC-043 (`in-review`): perspective and workflow coverage declared or explicitly unrepresented | The probe walks the screens its fixture roles are served and now declares the intake screen's empty table state | Local observed (partial); the Asset, Procurement and Auditor perspectives still lack a fixture login role |
| PRD AC-034 (`in-review`): scope, reset and selection focus | Existing partial keyboard coverage is unchanged | Not advanced by this change |
| PRD FR-016, FR-017, AC-039, AC-042 (`in-review`), partial via issue 132 | Intake screen reachability only; no recovery, receipt or acceptance behaviour is exercised by the probe | Not shown here; separately owned by issue 132 |
| BRD (`draft`) | No BRD requirement is approved or met | Context only |
| ADR 0003 and ADR 0006 (Accepted); ADR 0007 (Proposed, not accepted) | ADR 0003 and 0006 constrain journey scope and layout and are not amended. ADR 0007 does not close criterion 6 of issue 132 | Context only; no approval inferred |

### Affected boundaries and gaps

* Fixture roles only: the seven staff intake roles are a synthetic fixture, not Entra or any identity-provider proof. No device, resident or professional consent, screen-reader or other assistive-technology output exists.
* Whole #132 stays 4 checked and 2 unmet: the variation named owner and the delivery channel and identity decision. #134 all-perspective, assistive-technology and whole-journey criteria are untouched. #149, #233, #80, #73 and #440 stay open; no live, human or approval gate is closed.
* The populated intake states stay covered only by the existing opt-in staff intake browser test, which was not run here.

### Findings, owners and recommendation

* No new confirmed product defect and no required refactor is inferred. No new issue, source change, correction budget or criterion tick.
* Existing owners remain: #132 (variation owner and channel decision), #134 (the walkthrough and its unpublished candidate), #440 (cadence). The pending #132 channel-decision lane is planning-only, independent of this record, with no source implementation.
* Pending, not decided here: whether the owner of #134 grants a finite allowance for its unpublished candidate or leaves it unpublished; any named human, device, identity or variation owner decision is requested only where actually required. No new proposal or waiver is made.

Recommendation (proposed for Root, not a decision): CONTINUE, bounded, only for unrelated authorized work and for the existing bounded probe compatibility. No epic closure and no dependent claim beyond this evidence.

### Process record and limits

* One original plan critique (conformant after one non-blocking fix, applied) and one author Review, recorded under `.copilot-tracking/` (2026-11-11 keyboard-checkpoint-440-1111). The review is author-executed, not independent; independent exact-head review and hosted checks of this record remain required.
* Documentary checkpoint only: Git and `gh` read-only, Markdown and diff review. No push, PR, issue or board write was made.

## Handoff waiting screen integrated-main checkpoint (2026-11-11, Refs #440 #83)

Draft, not approved. This is a narrow local observation on constructed synthetic fixtures after merged PR 1444 reached `main`. It runs only existing tests and light checks listed below, changes no source, configuration, test, workflow, requirement or ADR, and opens no issue. Every earlier section is unchanged. It is not user acceptance, not an OD-09 result and not an Azure result.

### Trigger and pin provenance

* Trigger: the recurring checkpoint criterion of issue #440 after the feature wave PR 1444 (issue #83, the staff handoff waiting screen at `#/handoff-waiting`). The previous checkpoint is the [keyboard probe compatibility section](#keyboard-probe-compatibility-integrated-main-checkpoint-2026-11-11-refs-440-132-134) (PR 1440, `main` `b7d66e42`; the PR 1441 ADR 0007 decision record stays Proposed). No earlier Quality campaign is rerun and no correction authority is created; unknown historical product-correction balances stay unknown.
* Pin: PR 1444 squash-merged 2026-11-11T09:02:15Z as `ef3e00ad05a78c3a0fd3b342b860fb3d43796223`, root tree `513c3f9d8f7ae7c0c78672aa9f1650e23f7451cd`. A fetch before the first test showed `origin/main` unchanged from the pin. Trees: `src` `f82975dfc345f1a3705d62e08819383f6dd7bfd5`, `docs` `8a9d7693f8b3e880e84614fb40a8a88dcccc9c78`, `infra` `f7f31c0934cfe0bafb4505408706e55aa8ab61e7`, `tools` `432a4e8f7d74f26e88a55dd937c9c6f193016da9`, `.github` `0fc8e7647628658093899f132499e08e8ec4df7d`.
* The root tree equals the independently assessed and PR-gated candidate `441fd7edf8597972f79c8100caafc39d9afcd844`; the squash has a new commit identity, so this record does not claim the reviewer assessed the new SHA. The planning branch merged the pin with an ordinary merge; `src` at HEAD equals the pin's `src` tree and only `.copilot-tracking/` files differ from the pin.
* Hosted state read at the pin: main scorer run `42991793134` was `in_progress` and no Source CI run on the pin was observed, so neither is called passing. Root admitted this local-only observation while scoring is pending, from the PR gates passed on the identical tree. It permits no publication or downstream source admission. The earlier failed PR run `42984858029` (table inventory 13 versus 12, fixed by metadata-only change D1) stays historical adverse evidence.
* Issues #83 and #440 were open at read time, with no closing reference. The #153 planning head `99f01d7` and the #521 fixture candidate `1587f4baa` are excluded.

### Requirement-qualified traceability

| Requirement or contract (document, status) | Evidence in the pinned tree | Class |
| --- | --- | --- |
| PRD FR-011, AC-014, AC-036 (`in-review`): staff view of unaccepted handoffs and its scope | W1 text and browser cases show the explicit scope text, the read-only table, elapsed time and the server supplied as-of and owner, distinct from the personal pending card | Local observed, synthetic |
| PRD FR-066, AC-120 (`in-review`) | The screen has no urgency, next-update or accountable-reviewer column | Implemented but unverified; partial gap recorded for #83, not a defect finding |
| PRD FR-004 | Existing role guard and `RoleEndpointInventory` (W6) pass with the new route | Local observed, synthetic |
| BRD FR-018, AC-024, BG-010, NFR-009, AC-071 (`draft`) | Read-only view, manual case links, WCAG baseline table inventory (W7) | Local observed only for the listed tests; no BRD item is approved or met |
| BRD OD-09 | No approved global threshold times; the screen has no threshold and no automatic escalation | Blocked; #83 criterion 3 stays open |
| ADR 0003 and 0006 (Accepted); ADR 0007 (Proposed) | Not amended. ADR 0007 stays Proposed and is not exercised | Context only |
| Staff `#/handoff-waiting` versus personal pending card | W1, W2 | Local observed, synthetic |
| Guarded route and projection | One unscoped read; `approved_limit_hours` must be null; W5, W6 | Local observed, synthetic |
| Valid zero versus unavailable, malformed, 403 and abort | A valid empty list states the scope without a table; abort and 401 render nothing; 403 shows a fixed denied alert; other errors and malformed payloads show a fixed read-error alert with no table (W1, text and browser) | Local observed, synthetic |
| Manual case links and recheck | Case links and the Check again button re-run the read (W1) | Local observed, synthetic |
| Existing CSV and JSON | W3, W4 and W5 pass unchanged | Local observed, synthetic |

Source-reference drift: issue #83 cites BRD FR-009 to FR-011, while BRD 0.21.0 has the handoff rows at FR-016 to FR-018 (AC-022 to AC-024). It is recorded for #83 and not corrected here. Azure observed is empty.

### Commands, environment and results

Environment: Python 3.12.3, Node v24.21.0, Ruff 0.17.3, existing user-site Playwright and the existing Chromium cache, an owned temporary HOME, `ZF_DATA` unset, worktree source imports, the shared non-queued lock free at start, 8.5 GB memory available. No install, pull, service, Docker, SQL or cloud. Run from `src/api` with `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests`.

| Id | Selector | Exit | Ran | Skips | Failures |
| --- | --- | --- | --- | --- | --- |
| W4 | `tests.test_unaccepted_handoff_csv_api` | 0 | 13 | 0 | 0 |
| W5 | `tests.test_handoff_api` | 0 | 7 | 0 | 0 |
| W6 | `tests.test_role_endpoint_inventory.RoleEndpointInventory` | 0 | 24 | 0 | 0 |
| W7 | `tests.test_accessibility_baseline` | 0 | 12 | 0 | 0 |
| W8 | `tests.test_workbench.WorkbenchNavigation` | 0 | 5 | 0 | 0 |
| W2 | `tests.test_handoff_read_guidance` (browser, `ZF_BROWSER_TESTS=1`, shared lock held around this module only) | 0 | 9 | 0 | 0 |
| W3 | `tests.test_unaccepted_handoff_download_ui` (browser) | 0 | 6 | 0 | 0 |
| W1 | `tests.test_handoff_waiting_view` (4 browser, 6 text) | 0 | 10 | 0 | 0 |
| S1 | `node --check` of `app.js` (blob `7eb700fe`); Ruff check and format check of `test_handoff_waiting_view.py` | 0 | n/a | n/a | n/a |

Total 86 tests, zero skips, zero failures; each selector ran once on the final run. The count differs from the coordinator's 81-test combined command (which runs all of `test_role_screens` and not the CSV API module); no reconciliation is forced. W9 and the whole-suite gate were not run, and no mypy run was made here.

First raw failure, preserved: the first attempt of W2, W3 and W1 ran with an isolated HOME that hid the user-site Playwright, so each browser class errored in `setUpClass` with `ModuleNotFoundError: No module named 'playwright'` (W1 text cases passed; zero product assertions ran). That is an environment error, not a product failure. After pointing the existing user-site directory back in, with no install, each was run once more and passed. The first logs are kept locally.

### Exclusions and residuals

* Unproved: actual OD-09 times and operational acceptance, manual assistive-technology testing, reflow and zoom, large-queue performance (no open issue owns it), the urgency, next-update and accountable-reviewer columns of AC-120, Azure, identity, human and resident acceptance.
* Whole #83 (criterion 3), root #81 and whole #440 are not closed by this record or by merged children.
* The unmerged #153 plan `99f01d7` is excluded. No fresh web-interface review was performed; no web file changed.

### Recommendation (proposed for Root, not a decision)

CONTINUE, bounded. No new product defect is found and no fix, refactor or new issue is proposed. Affected gates: main scorer run `42991793134` and any Source CI on the pin must be read before downstream admission; the independent exact-head review of this record is required. #153 source work may continue as an independent lane only after Root's own admission, not by this record. Exact resume: the OD-09 owner decision for #83 criterion 3, then the next #440 wave checkpoint.

### Process record and limits

* One plan critique (conformant after fixes WC-01 to WC-05) and one original Review under `.copilot-tracking/` (2026-11-11 waiting-checkpoint-440-1111), plus Root's admission amendment. The review is author-executed, not independent.
* Raw logs stay local outside the repository. No push, PR, issue or board write, no criterion tick.

## Personal handoff HTTP guidance integrated-main checkpoint (2026-11-11, Refs #440 #153)

Draft, not approved. This is a narrow local observation on constructed synthetic fixtures after merged PR 1449 reached `main`. It runs only existing tests and light checks listed below, changes no source, configuration, test, workflow, requirement or ADR, and opens no issue. Every earlier section is unchanged. It is not user acceptance, not an OD-09 result and not an Azure result.

### Trigger and pin provenance

* Trigger: the recurring checkpoint criterion of issue #440 after the feature wave PR 1449 (issue #153, refusal and load-failure guidance on the personal pending-handoff card). The previous checkpoint is the [handoff waiting screen section](#handoff-waiting-screen-integrated-main-checkpoint-2026-11-11-refs-440-83) (PR 1448, observation pin `ef3e00ad`, 86 tests). No earlier Quality campaign is rerun and no correction authority is created; unknown historical product-correction balances stay unknown.
* Pin: PR 1449 squash-merged 2026-11-11T10:39:52Z as `f0eb928f8abe17c512fba2e564837e97c0c5e655`, root tree `a0a4aea03f400f2f1c0a3cd347bebd76c8f9350c`, admitted by Root's amendment. Trees: `src` `bb7a461f0acc9ccff0cde8ddb16df3717c552c50`, `docs` `435e0b50828a6928fc0f78cf6ce2a08ac248c5a2`, `infra` `a022907662e2a98374f36d8f641eefd29d0dc798`, `tools` `432a4e8f7d74f26e88a55dd937c9c6f193016da9`, `.github` `48577d6868c72b11eb872133064883dc10c63cee`. Only that exact main was merged into the planning topic by an ordinary merge; after it all five directory trees equal the pin and the only topic-only paths are `.copilot-tracking/` files.
* Tree equality, stated separately from execution: the pin's `src` tree equals the frozen candidate `2db08d8e2141d60a52d688b731f192972ca8293b` `src` tree. That equality is not integrated-main execution evidence. The candidate root tree `e328d3eb18d69cc58293e2200eb9a0b51f377322` differs because of earlier documentation integration. Base main `ab44d42fa` had `src` tree `f6d487b51ce3314d732cab87a91844fe221a6e38`; between it and the pin only PR 1449 changed source (`app.js` and `test_handoff_read_guidance.py`).
* Hosted state: at admission the main scorer run `43005506332` was queued (in progress when re-read) and no main Source CI run was listed, so neither is called passing. Root permitted this local observation while scoring is pending; it is not publication or downstream acceptance. The PR 1449 contexts (19) were reported passing by Root before merge; this record did not re-read them as main evidence.
* Included and excluded: PR 1449 is the only source merge since the previous base. The #521 fixture candidate and any unmerged branch are excluded. Issues #153 and #440 were open at read time, with no closing reference.
* Candidate history, not main evidence: Root's raw candidate observations (149 tests with 13 opt-in skips, then 15 with zero skips and 16 with zero skips) and the independent bounded approvals with zero findings (comment `pull/1449#issuecomment-6793048206`) belong to the unmerged candidate. They are not relabelled as main execution.

### Requirement-qualified traceability

| Requirement or contract (document, version, status, blob) | Evidence in the pinned tree | Class |
| --- | --- | --- |
| PRD FR-011, AC-014, AC-036 (`docs/prds/zava-forward-retrofit-programme-demonstrator.md`, 0.21.0, `in-review`, `c788b917`) | H1 cases show that a refused, failed or malformed read of the personal card is stated as unknown, not as an empty list; the scope is the personal card only | Local observed, synthetic |
| PRD FR-004 and the role guard | H4 and H6 pass for the guarded `/api/handoffs` route and the role inventory | Local observed, synthetic |
| PRD FR-066, AC-120 | Not touched by this wave; urgency, next-update and accountable-reviewer columns stay a gap owned by #83 | Implemented but unverified; partial gap carried forward |
| BRD FR-018, AC-024, BG-010, NFR-009, AC-071 (`docs/brds/agentic-retrofit-programme-brd.md`, 0.21.0, `draft`, `34d88395`) | The refusal copy keeps manual paths (ask the sender or open a known case) | Local observed only for the listed tests; no BRD item is approved or met |
| BRD OD-09 | No approved global threshold; the card sets none | Blocked; unchanged |
| ADR 0003 (`d6064539`) and 0006 (`956da1a3`) Accepted; ADR 0007 (`541e0f72`) Proposed | Not amended and not exercised | Context only |
| Personal card versus staff `#/handoff-waiting` and existing CSV links | H3 (10) and H2 (6) pass unchanged beside the new card behaviour | Local observed, synthetic |
| Guarded route, projection and CSV | H4 (7), H5 (13), H6 (24) | Local observed, synthetic |
| Card 403, 500 and malformed states | H1 browser cases use constructed `page.route` responses; they are not backend permission statuses and not live acceptance | Local observed, synthetic, constructed |

Additive correction dated 2026-11-11: the historical research row for issue #153 called this slice C1. The assessed increment is the personal-handoff C3 refusal and load-failure guidance slice, not proof of C1 and not proof of universal C2, C3 or C5. The 403 owner-role wording is an internal interpretation; named-human wording review and owner-role validation are unproved. Source-reference drift for #83 (BRD FR-009 to FR-011 versus FR-016 to FR-018) is carried forward unchanged. Azure observed is empty.

### Commands, environment and results

Environment: Python 3.12.3, Node v24.21.0, Ruff 0.17.3, Playwright 1.64.1 (read with `importlib.metadata`), the existing user-site and the existing Chromium cache (`chromium-1248`) exposed explicitly, an owned temporary `HOME` under `env -i`, `ZF_DATA` unset, 8.4 GB memory available, the shared lock free at start. No install, pull, service, Docker, SQL or cloud. Run from `src/api` with `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests` plus the user-site path. Preflight proved the `zava_forward.api.server`, `core.store`, `agents.chat` and test module origins lie under this worktree. The first preflight printed `None` for the `zava_forward.agents` namespace package; a read-only probe resolved its search location and `chat` module to this worktree (log `preflight2-agents-origin.log`).

| Id | Selector | Exit | Ran | Skips | Failures |
| --- | --- | --- | --- | --- | --- |
| H4 | `tests.test_handoff_api` | 0 | 7 | 0 | 0 |
| H5 | `tests.test_unaccepted_handoff_csv_api` | 0 | 13 | 0 | 0 |
| H6 | `tests.test_role_endpoint_inventory.RoleEndpointInventory` | 0 | 24 | 0 | 0 |
| H1 | `tests.test_handoff_read_guidance` (browser, `ZF_BROWSER_TESTS=1`, under outer non-queued `flock -n`) | 0 | 15 | 0 | 0 |
| H2 | `tests.test_unaccepted_handoff_download_ui` (browser, internal lock, no outer lock) | 0 | 6 | 0 | 0 |
| H3 | `tests.test_handoff_waiting_view` (browser, internal lock, no outer lock) | 0 | 10 | 0 | 0 |
| S1 | `node --check` of `app.js` (blob `7971ac3a`); Ruff check and format check of `test_handoff_read_guidance.py` | 0 | n/a | n/a | n/a |

Total 75 tests, zero skips, zero failures, one run each, no rerun. H1 lock holder was recorded inside the held wrapper before and after the test (the same `/proc/locks` entry, holder `flock` pid 304261 with the wrapper child 304262 running the test). Raw logs, one file per command and never overwritten, are local at `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/http-handoff-checkpoint-440-observation-1111/` (`preflight.log`, `H4.log` to `H3.log`, `S1.log`, `run.sh`). Other blobs at the pin: `test_handoff_read_guidance.py` `0ac5639b`, `test_handoff_waiting_view.py` `db0e3c64`, `test_unaccepted_handoff_download_ui.py` `d43d82a2`, `test_handoff_api.py` `08e0ed90`, `test_unaccepted_handoff_csv_api.py` `49f982f2`, `test_role_endpoint_inventory.py` `b563c91c`. The optional copy audit, mypy, the 149-module set and the whole-suite gate were not run.

### Exclusions and residuals

* Unproved: named-human wording and owner-role validation, actual OD-09 times and operational acceptance, manual assistive-technology testing, reflow and zoom, large-queue performance, the urgency, next-update and accountable-reviewer columns of AC-120, Azure, identity, human and resident acceptance, and #153 slices C2, universal C3 and C5.
* Whole #83, #81, #153 and #440 are not closed by this record or by merged children. A real non-staff 500 from an uncaught `PermissionError` in `pending_handoffs` is existing server behaviour, unchanged by scope.
* No fresh web-interface review was performed; no web file changed.

### Recommendation (proposed for Root, not a decision)

CONTINUE, bounded. No new product defect is found and no fix, refactor or new issue is proposed. Affected gates: main scorer run `43005506332` and any Source CI on the pin must be read before downstream admission, and an independent exact-head review of this record is required. Exact resume: named-human wording review for #153 and its remaining slices, the OD-09 owner decision for #83 criterion 3, then the next #440 wave checkpoint.

### Process record and limits

* Historical qualifications, not rewritten: the native #153 session corrected its test after five assertion failures and reran its lock, format and `PYTHONPATH` steps without a Root pause; the earlier #440 waiting checkpoint made an unauthorized native browser-environment retry, and Root's publication sequencing and end-of-file check error stands as a qualified outcome. Root's fresh candidate verification (149 with 13 skips, 15 and 16 with zero skips) was separately authorized and is not retroactive permission.
* Pause-rule qualification (correction D1, 2026-11-11): all 75 selector tests succeeded, with no skips, no busy lock and no reruns. However, the diagnostic `grep -c` for skips that followed H1 matched nothing, printed 0 and returned 1; the native shell tool reported exit 1, and the author continued to H2 and H3 without a Root pause. That is a command-level deviation from the plan's pause rule, not an H1 failure: H1's recorded selector exit 0 and 15 tests OK stand. `run.sh` ends with `tail` and does not propagate selector status as its own exit, so the result rests on the individually recorded selector exits, the actual Ran and OK lines and S1's individual exit records, not on outer harness success. There was no rerun and no retroactive permission.
* Editing-rule deviation (correction D1): the author first appended its own new log entry with a shell heredoc, contrary to the file-change rule, reverted that own uncommitted append with `git checkout`, and reapplied it with the edit tool before commit; the final content is unchanged. The recovery does not erase the deviation and does not authorize `git checkout` generally. The original author Review and changes record are preserved as history.
* Data-isolation evidence limit (correction D1): the retained raw preflight proves the original-user `~/.zava-forward` directory was absent and `ZF_DATA` unset before the run. `env -i`, an owned temporary `HOME` and `TMPDIR`, and synthetic fixture sources support isolation. The execution log records an after-run probe of the original-user directory but its output was not retained, and no before or after absence output for the owned `HOME` is retained. No private or default data access is inferred, and no fresh probe is offered as historical proof.
* One plan critique (conformant after fixes HC-01 to HC-03) and one original Review under `.copilot-tracking/` (2026-11-11 http-handoff-checkpoint-440-1111), plus Root's admission amendment. The review is author-executed, not independent.
* No push, PR, issue or board write, no criterion tick.

## Aftercare numeric-order integrated-main checkpoint (2026-11-11, Refs #440 #1401 #1402 #134)

Draft, local-only, not approved. This is a new, narrow recurring-checkpoint record after merged PR 1456 (issue #1401, numeric restore order for aftercare concerns) reached `main`. It is distinct from the earlier [aftercare integration checkpoint of PR 1400](#aftercare-integration-current-main-checkpoint-2026-11-10-refs-440-89-133-134-1401-1402), whose text is unchanged and whose "#1401 OPEN" rows are history now superseded for #1401 only. It is not the old #440 C6, not a retry and not the personal-handoff campaign; it changes no source, test, tool, workflow, configuration, requirement or ADR, makes no fix, opens no issue and resets no finite correction allowance of #1401, #1402, #134 or #440. It runs only the focused checks listed below, not the complete local gate, `--changed`, SQL, browser, Azure, model or private-data runs. Records: [research](../../.copilot-tracking/research/2026-11-11/aftercare-wave-checkpoint-440-2119-research.md), [plan](../../.copilot-tracking/plans/2026-11-11/aftercare-wave-checkpoint-440-2119-plan.md), [details](../../.copilot-tracking/details/2026-11-11/aftercare-wave-checkpoint-440-2119-details.md), [critique](../../.copilot-tracking/plans/2026-11-11/aftercare-wave-checkpoint-440-2119-critique.md), [changes](../../.copilot-tracking/changes/2026-11-11/aftercare-wave-checkpoint-440-2119-changes.md), [review](../../.copilot-tracking/reviews/2026-11-11/aftercare-wave-checkpoint-440-2119-review.md) and [state](../../.copilot-tracking/rpi-sessions/2026-11-11/aftercare-wave-checkpoint-440-2119-state.json).

### Identities, scope and exclusions

| Item | Identity (read 2026-11-11) |
| --- | --- |
| Start pin and fresh main | `origin/main` fetched 2026-11-11T21:21Z is `077ad5ad20293a1d79932ea14e9f639dd11e5a22`, equal to the start pin and to the worktree HEAD (branch `docs/aftercare-wave-checkpoint-2119`). Root tree `d1dde25bc3476772bd9d97711558ed87d1f7a035`; `src` `51feb8eaaed8d83d578164cebd06bb89861924e3`, `infra` `a022907662e2a98374f36d8f641eefd29d0dc798`, `tools` `432a4e8f7d74f26e88a55dd937c9c6f193016da9`, `.github` `56e251c7cd6762cd4f344fa393150649ae020875` |
| Trigger | PR 1456 `fix(core): restore aftercare concerns in numeric identifier order`, MERGED 2026-11-11T20:04:04Z as `a3862eed4a324b13715eeebf0c98053d9079dec1`, an ancestor of the pin; `Closes #1401` (now CLOSED) and `Refs #133`, `Refs #89`. Since that merge only `.github/rubric/scores/latest.json` changed, so the pin `src` equals the merged source |
| Source blobs at the pin | `aftercare.py` `59b66dd1eed0` (changed by PR 1456), `aftercare_intake.py` `96674907da90` and `aftercare_store.py` `e5bd737c6d9b` (both unchanged since PR 1400), `test_aftercare.py` `9ef75fe6abce`, `test_aftercare_store.py` `eebba62b0f19`, `test_aftercare_intake.py` `b3f220bb1e11` |
| Documents (blob at the pin) | BRD 0.21.0 `draft` `34d88395de86`; PRD 0.21.0 `in-review` `c788b917bafa`; ADR 0003 `d60645397b20` and ADR 0006 `956da1a3b804` Accepted. None is changed by PR 1456; draft and in-review are not approval |
| Hosted state of main | `Capstone Rubric Scorer` for `a3862eed4` completed success; for the pin only `Infrastructure PR what-if` is listed and it was skipped. A skipped or absent workflow is not a successful check, and no Source CI result for the pin is claimed |
| Issue states (read live) | #440, #133, #134, #89, #132 and #1402 OPEN; #1401 CLOSED by the merge. Nothing is ticked, closed or opened by this record |
| Pending, unmerged, not counted as main | PR 1458 `fix(aftercare): refuse existing blank intake state` (closes #1402), OPEN at head `ff6c181ea7921ace9d1704c6890b3beda1d5cd3b`, base `main`; PR 1455 `test(api): verify connected-home specialist screens` (#134), OPEN. Neither is on `main` and no result of either is relabelled as main evidence |
| Excluded | The personal-handoff and other earlier campaigns, #132 job pack, #109 and #111, deployment, Azure, real providers and models, resident or professional acceptance, private data |

### Observed on current main (local, constructed synthetic data)

Environment: Python 3.12.3, Ruff 0.17.3, mypy 2.4.1, Node v24.21.0, `env -i` with an owned temporary `HOME`, `ZF_DATA` and `ZF_RESIDENT_MSSQL` unset. The installed `zava-forward-*` distributions are editable installs of the owner's primary checkout, so an explicit `PYTHONPATH` of this worktree's `src/*/src` and test folders (not `mvp`) was set and a preflight proved that the `aftercare`, `aftercare_intake`, `aftercare_store` and `zava_forward.api.server` modules import from this worktree. HEAD equalled the pin, `git status --porcelain -- src` was empty before and after, and the disk hash of each tested file equalled its pin blob. No install, service, Docker, SQL or cloud use. Each selector ran once; raw logs and exit codes are local outside the repository at `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/aftercare-checkpoint-440-2119/`.

| Id | Selector | Exit | Ran | Skipped | Notes |
| --- | --- | --- | --- | --- | --- |
| A1 | `src/core` `test_aftercare` | 0 | 23 | 0 | Includes `test_restore_is_numeric_whatever_the_json_key_order` (999, 1000, 1001; text-sorted and reversed key order) and `test_restore_still_refuses_gaps_and_non_canonical_identifiers_past_999` |
| A2 | `src/core` `test_aftercare_store` | 0 | 42 | 15 | The 15 skips are the SQL Server variants (`opt-in owned loopback SQL Server`). The 27 executed tests include the 1000-record restart read and the 999/1000/1001 write, restart and replay tests on the JSON `Store` and SQLite adapters |
| A3 | `src/core` `test_aftercare_intake` | 0 | 39 | 0 | Intake roles, persistence, replay and routes; it has no blank or whitespace document case |
| A4 | `src/api` `test_aftercare_served`, `test_aftercare_screen` | 0 | 21 | 0 | Route contract and staff screen; the screen module runs in a node vm and is not a served-browser or keyboard check |
| S1 | Ruff check and `ruff format --check` on `aftercare.py`, `test_aftercare.py`, `test_aftercare_store.py` | 0, 0 | n/a | n/a | All checks passed, 3 files already formatted |
| S1 | mypy on the same three files | 1, then 0 | n/a | n/a | The first invocation failed with `ModuleNotFoundError: No module named 'mypy'` because the `env -i` command hid the user site where mypy is installed; it is an invocation error, not a product finding and not a pass. One rerun with the user site exposed read `Success: no issues found in 3 source files`, exit 0 |

Totals: 125 tests discovered, 110 executed and passing, 15 skipped (SQL Server), 0 failures. Skips are not passes: SQL Server persistence at 999/1000/1001 is NOT observed on main here. PR 1456's own text reports an independent disposable SQL Server inspection of 15 tests on its candidate; that is candidate evidence on the pre-merge head, was not re-run here and is not carried into this observation. Not run, therefore Unknown: full Core or API discovery, browser suites, an HTTP journey above 999 concerns, concurrency or volume behaviour, hosted Source CI of the pin, the full gate.

### Requirement trace (document-qualified, proposed)

BRD and PRD both use the FR-049 label for different topics, so each row names its document. Classes follow the repository separation of local observed, implemented but unverified, blocked and unknown.

| Requirement (document, status) | Evidence at the pin | Class |
| --- | --- | --- |
| PRD FR-014, AC-017 (in-review; AC-017 Not run): intake records type, owner and route; contact is not consent | A3 intake persistence, replay and role tests pass on constructed data; A2 shows records survive a store reopen at 999, 1000 and 1001 on the JSON and SQLite adapters | Local observed, constructed synthetic; whole AC-017 unmet |
| PRD FR-049, AC-063 (in-review; AC-063 Not run): complaint, remedy, package, handover and financial closure stay distinct | A1 and A3 closure and refusal tests pass; the ordering fix keeps every concern visible after restore past 999 | Local observed, constructed synthetic; age bands, lease evidence and leasehold text remain a gap, so whole AC-063 is unmet |
| BRD FR-047, AC-089 (draft): closure cannot close an outstanding remedy, defect or dispute | A1 `ClosureTests` pass; restore still refuses a snapshot that would weaken a recorded concern (gap, unpadded and foreign identifiers refused) | Local observed, constructed synthetic; document-qualified |
| BRD RULE-014 (draft): a sensor signal is context, never closure evidence | A1 `SensorContextTests` and the restore refusals pass; unchanged by PR 1456 | Local observed, constructed synthetic |
| PRD FR-036 (in-review): AI tasks registered, unapproved tasks use the manual route | Not touched; `aftercare-concern-pack` stays unapproved and disabled | Static, unchanged |
| ADR 0006 (Accepted) `src` layout; ADR 0003 (Accepted) runtime fit | The change is inside `src/core` and its tests; no amendment | Context only |
| Persistence integrity of the stored register (supporting the above, not a separate requirement) | Canonical JSON sorts `AC-1000` before `AC-101` (`json.dumps(..., sort_keys=True)` in `aftercare_intake.py` `_txn` and `_canon` in `aftercare_store.py`); `from_state` now restores in numeric order. Observed by A1 and A2 on the JSON and SQLite adapters | Local observed for the listed adapters; SQL Server not observed here; an HTTP journey above 999 not run |
| #133, #134, #89 and #440 acceptance criteria | Unchanged, all OPEN | Partially delivered; criteria unmet |

### Boundaries observed

* Ordering: restore order is numeric (`AC-\d{3,}` identifiers), independent of JSON key order, and the existing gap, uniqueness and key checks are kept; the next identifier after 999 and 1000 continues the sequence (A1, A2).
* Intake persistence and manual path: one validated JSON document per update, replay by the same request id and a changed payload as a conflict remain as read in the earlier section; the paper and phone routes remain the manual path, the draft and request reference survive failures. These are tested on constructed data only and are not human or assistive-technology acceptance.
* Human, consent and resident boundaries: no consent is read or written; actors come from the session; closure remains manager-only; a missing owner stays Unknown; no resident account, portal, approval or AI route is added. PR 1456 does not widen any of these and no requirement is relaxed or deferred by this record.

### Pending gap owned by #1402 (not repaired on main)

* Static read of `aftercare_intake.py` `_parse` at the pin: `if text is None or not text.strip(): return _blank()`. A present but blank or whitespace-only `FileStateStore` document is therefore still treated as fresh, so a later write can restart identifiers. This is NOT corrected on `main`, and PR 1456 does not claim it is. The gap is stated from source only: no probe or reproduction was run here, and A3 passing is not blank-state verification because it has no such case.
* The runtime adapter `DocumentStateStore` returns `None` or serialized JSON, so a raw blank string does not reach `_parse` through it (a source reading, not proof for every deployment). The existing limitation therefore stands at any register size and independently of numeric ordering: do not rely on the standalone `FileStateStore` for damaged-state refusal.
* PR 1458 (OPEN, unmerged, head `ff6c181ea7921ace9d1704c6890b3beda1d5cd3b`) proposes the repair. Its text (a one-predicate parser change, 67 intake and register tests, 13 API screen tests, an independent exact-head approval) is candidate policy and evidence, not observed on `main`. #1402 stays OPEN until that PR is merged under its own guarded gates; this record neither depends on nor assesses it.

### Findings, owners and recommendation (proposed for Root, not a decision)

* No new product defect is found and none is asserted. #1401's recorded finding is delivered on `main` for the JSON and SQLite adapters and constructed data; #1402 is the only remaining inherited aftercare finding and its owner is #1402 and PR 1458. No fix, refactor or new issue is proposed.
* Affected gates: closure of whole #133, #134, #89 and #440 stays held; #1402 closure, and any aftercare expansion that would rely on `FileStateStore` damaged-state refusal, stay held until PR 1458 is merged and observed on main; SQL Server persistence at 999/1000/1001 and any 1000-concern HTTP, browser or volume claim stay unverified until separately run; independent exact-head review of this record and applicable hosted checks of its exact head remain required.
* Recommendation: CONTINUE, bounded. The #134 local walkthrough of the staff-assisted aftercare surface, on constructed data and the runtime adapter, may proceed with the #1402 limitation stated. This is not a tick of any criterion, an approval of any requirement or ADR, or a deferral decision.

### Process record and limits

* One plan critique by an independent read-only subagent (five findings; two rejected with reasons, three applied) and one original author Review are under `.copilot-tracking/`; the Review is author-executed, not independent. The critique's original text is preserved.
* The mypy first-run failure above is retained as adverse evidence. No other command failed, no test was rerun and no dependency was installed.
* Counts are those printed by each selector in this run. The model label is asserted and no witness or host attestation exists. Raw logs stay local outside the repository. No push, PR, issue or board write was made.

### Dated follow-up after PR 1458 merged (2026-11-11, post-1458 current-main observation)

Everything above this subsection is the original observation at pin `077ad5ad2`, unchanged and still correct for that date: at that pin PR 1458 was OPEN and the blank-document gap was a static read. It was independently approved for the frozen head `4d7be2015672d62eba5d325d9da025af07f1c036` only; that approval does not extend to this subsection. This is a new bounded completed-wave follow-up, not a source correction, not a reset of any finite correction allowance and not a retry. Records: [research](../../.copilot-tracking/research/2026-11-11/aftercare-bc-followup-440-2140-research.md), [plan](../../.copilot-tracking/plans/2026-11-11/aftercare-bc-followup-440-2140-plan.md), [details](../../.copilot-tracking/details/2026-11-11/aftercare-bc-followup-440-2140-details.md), [critique](../../.copilot-tracking/plans/2026-11-11/aftercare-bc-followup-440-2140-critique.md), [changes](../../.copilot-tracking/changes/2026-11-11/aftercare-bc-followup-440-2140-changes.md), [review](../../.copilot-tracking/reviews/2026-11-11/aftercare-bc-followup-440-2140-review.md) and [state](../../.copilot-tracking/rpi-sessions/2026-11-11/aftercare-bc-followup-440-2140-state.json).

| Item | Identity (read 2026-11-11) |
| --- | --- |
| Trigger | PR 1458 `fix(aftercare): refuse existing blank intake state`, MERGED 2026-11-11T21:34:00Z as `bc123235af30b63de9808c97a430860f1e00dcc8` (root tree `ee35ec2e34c70111005cb173597698af9e72359e`, PR head `ff6c181ea7921ace9d1704c6890b3beda1d5cd3b`). #1402 and #1401 CLOSED; #133, #134, #89 and #440 OPEN |
| Current main at read | A fetch at about 21:45Z showed `origin/main` `97ec3f3c82a4aeeace7709f2f5a8766f4c638dfa` (root tree `49fc10d9ef7118b060cd04d02ec33ef2f0784ee0`), one rubric-only commit past `bc123235`; the only differing path is `.github/rubric/scores/latest.json`. `src` tree `297e248aef8140e34ecaa059acd68ee067951d23` is equal at both, as are `docs`, `infra` and `tools`. No speculative merge claim: the observed source is the exported `src` of `97ec3f3c8`, identical to that of `bc123235` |
| Source delta of PR 1458 (pin to main) | Exactly two paths: `aftercare_intake.py` (`96674907da90` to `fb25f9f5de5b`, `_parse` now blank-initialises only for `None`; a present blank or whitespace document goes to `json.loads` and raises `StateInvalid`) and `test_aftercare_intake.py` (`b3f220bb1e11` to `ed815f6bd3b5`, new `BlankStateTests`, 5 tests). `aftercare.py` and `aftercare_store.py` are unchanged from the original observation |
| Not the observed source | The frozen branch head `4d7be201` is a documentation-only child of `077ad5ad2`; its `src` does not include PR 1458 and was not used |

Method: a `git archive` export of `src` from `origin/main` into a new folder outside the repository, not the primary checkout. Each of six aftercare source and test files hashed equal to its blob on `origin/main`, and a preflight proved that `aftercare`, `aftercare_intake` and `aftercare_store` import from the export. `env -i`, an owned temporary `HOME`, `ZF_DATA` and `ZF_RESIDENT_MSSQL` unset, Python 3.12.3, constructed synthetic data, no install, no SQL Server, browser, cloud or model. Each selector ran once; Ran and skip counts are read from stderr, not inferred from exit status.

| Id | Selector (from `src/core` of the export) | Exit | Ran | Skipped | Covers |
| --- | --- | --- | --- | --- | --- |
| B1 | `test_aftercare_intake` | 0 | 44 | 0 | Includes the 5 `BlankStateTests`: absent state initialises and replays; blank read refused with bytes preserved for `""`, `"   "` and `"\n\t \n"`; blank write refused with bytes preserved; the service `handle` contract returns 503 twice and survives a service restart; an existing non-empty document is not reset (second receipt `RC-AC-002`). The 39 earlier tests, including the damaged and non-blank refusal cases of `PersistenceTests`, also pass |
| B2 | `test_aftercare.SnapshotTests` | 0 | 5 | 0 | Numeric restore at 999, 1000 and 1001 for text-sorted and reversed key order, and gap, unpadded and foreign-identifier refusals |
| B3 | `test_aftercare_store` | 0 | 42 | 15 | The 15 skips are the opt-in SQL Server variants and are not passes. The 27 executed tests include the 1000-record restart read and the 999/1000/1001 write, restart and replay tests on the JSON `Store` and SQLite adapters |

Totals as printed: 91 tests ran across three selectors, 15 skipped, 0 failures. B1 is 5 more than the 39 of the original observation, exactly the new `BlankStateTests`. The "HTTP" case is the in-process `AftercareService.handle` contract, not a live server or browser. Raw stdout, stderr, exit files, `env.log` and `origins.log` are local outside the repository at `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/aftercare-bc-followup-440-2140/`.

Requirement and issue-boundary trace (document-qualified; statuses unchanged: BRD 0.21.0 `draft` `34d88395de86`, PRD 0.21.0 `in-review` `c788b917bafa`, ADR 0003 and ADR 0006 Accepted):

| Boundary | Observation on main source | Class |
| --- | --- | --- |
| #1402 criteria (issue-ticked; see the issue) | Scoped regression for a blank existing `FileStateStore` document: refused, bytes preserved, 503 on the handler contract, absent and valid state still initialise and replay | Local observed, constructed synthetic, JSON file store; SQL Server not run. The static limit of the 077 observation is superseded for this boundary only |
| #1401 numeric restore | B2 and B3 pass on the current register source | Local observed for JSON and SQLite; SQL Server not observed |
| PRD FR-014, AC-017 (in-review, Not run) intake persistence and replay | B1 persistence, replay and refusal tests pass | Local observed, constructed; whole AC-017 unmet |
| PRD FR-049, AC-063 and BRD FR-047, AC-089 closure stays distinct and cannot close a remedy | Logic untouched by 1456 or 1458; restore refusals protect it | Unchanged; whole AC-063 unmet |
| BRD RULE-014, PRD FR-036 | Untouched; sensor context is not closure evidence; the AI concern pack stays unapproved | Static, unchanged |
| Human, resident, consent boundaries | A refused damaged or blank state tells the user to use the manual route and ask a person to check it; no consent, resident account or approval is added | Not relaxed; human, resident, legal and assistive-technology acceptance not observed |
| Whole #133, #134, #89, #440 | Unchanged, OPEN; no criterion is ticked by this record | Unmet |

Remaining unproved: SQL Server numeric restore and blank behaviour (the blank branch is unreachable through `DocumentStateStore` by source reading, not run), an HTTP or browser journey above 999 concerns, volume and concurrency, hosted Source CI of `bc123235` and `97ec3f3c8` (not read as passing), the full gate, and the earlier adverse mypy invocation failure, which remains retained and is not re-run here.

Recommendation (proposed for Root, not a decision): CONTINUE, bounded. No new defect is found and no fix, refactor or issue is proposed. Affected gates: the aftercare ordering and blank-state holds of the original observation are lifted for constructed JSON and SQLite data only; closure of whole #133, #134, #89 and #440, expansion that relies on SQL Server persistence at 1000 concerns, and any live, resident or professional claim stay held; independent exact-head review of this delta and applicable hosted checks remain required.

Process limits: the plan critique found two blocking items (stdout versus stderr capture, a premature claim) and one stale-main item, all applied. The author wrote the first three tracking files with a shell heredoc, contrary to the file-change rule, before switching to the edit tools; the content is unchanged. The Review is author-executed, not independent.

## Demo wave integrated-main checkpoint (2026-11-12, Refs #440 #99 #116 #80 #432 #184)

Draft, local-only, not approved. This is a bounded recurring checkpoint after the merged source wave of PRs 1465, 1466, 1467, 1468, 1469 and 1473 reached `main`. It is not a new issue, feature, approval or correction pool; it changes no source, test, tool, workflow, configuration, requirement or ADR, makes no fix, opens no issue, writes no issue, board or acceptance-criterion state and resets no correction allowance. It does not complete the last two open acceptance criteria of #440 (triage into independent issues, and the Major HVE behavior-tested coordinator change) and does not retroactively complete original HVE behavior testing.

### Identities, scope and exclusions

| Item | Identity (read 2026-11-12) |
| --- | --- |
| Start pin and fresh main | Worktree HEAD (branch `docs/demo-wave-checkpoint-440-1112`) `bbb1d20cc984d7c4107459485712d4b618a17afe`, the expected pin and the merge of PR 1473. `origin/main` fetched 2026-11-12 is `5ee8ac14c70f457925f3333321094e46b93373b9`, one rubric-only commit later (only `.github/rubric/scores/latest.json` differs). Root trees `f0cc063601781108c1554a73e40165f7f595dd80` and `f5348aa9b4a2062c6f7982ab776f8d1abadd5798`; `src` `60d841010c4ad5551e530c2b4e67b717fc063648` equal at both, `infra` `a022907662e2`, `tools` `432a4e8f7d74`, `docs` `629b84683280` at the pin. The tested source therefore equals the source of fresh main; nothing was rebased or merged to refresh |
| Documents (blob at the pin) | BRD 0.21.0 `draft` `34d88395de86`; PRD 0.21.0 `in-review` `c788b917bafa`; ADR 0003 `d60645397b20` and ADR 0006 `956da1a3b804` Accepted; ADR 0007 `541e0f72dd2c` Proposed. None of the six PRs changes any of them; draft, in-review and Proposed are not approval |
| Hosted state | The only workflow run listed for the pin is `Capstone Rubric Scorer` (push, completed, success); none is listed for `5ee8ac14`. No Source CI result is claimed for either; an absent workflow is not a successful check |
| Issue states (read live) | #440, #99, #116, #80, #432, #184 and #134 OPEN. Nothing is ticked, closed or opened here |
| Excluded | Unmerged PR 1470 (proposal cards) and PR 1475 (five-home script), the local #184 minute and cohort commit `6819456`, all other siblings, SQL Server, Docker, the browser harness, scanners, hosted CI, deployment, Azure, real providers and models, resident or professional acceptance, private data |

### Wave identity: the task labels do not match the merged PRs

Merged commits and diffs were read, not the task labels. The mismatches are recorded as an adverse qualification.

| PR (merge commit) | Actual content | Task label | Match |
| --- | --- | --- | --- |
| 1465 (`5df20e639821`) | Documentation only: PROPOSED narrow #184 engineering design for bounded run and cost controls in `iot-sensor-analytics-research-plan.md`; no source | "#116 weather and provider spy" | No |
| 1466 (`04e2620556b0`) | Tests only: `test_ai_provider_payload_spy.py`, offline AI provider payload boundaries (#116) | not named under its number | Label shifted |
| 1467 (`e3339de62b19`) | Core fix: `exposure_limits.py` treats a NaN or infinite committed or tolerance observation as an Unknown finding for that limit (existing pause behaviour), not Within limits; finite values, including arbitrarily large integers, are compared normally when the currency matches, with no `isfinite` overflow (#99); no CSV, no HTTP route, no UI | "finite household finance CSV" and "target-mode proposal" | No: no CSV and no target-mode proposal exists in the wave |
| 1468 (`f0896869d437`) | `ai.py` settles the ledger before the receipt reports usage; API tests; tokenomics text corrected (#432) | "legacy usage settlement" | Yes |
| 1469 (`71fabf00957a`) | `role-screens.js` browser-built four-column exception summary CSV with formula neutralisation and fail-closed export (#80) | "exception CSV" | Yes |
| 1473 (`bbb1d20cc984`) | `live_simulator.py`, `live_control.py`: run control re-read before every send attempt including retries, `RUN_CONTROL_FENCED`, single instance only; B2 cross-process fence deferred (#184) | "simulator stop and retry B1" | Yes |

Consequences: the only candidate policy in the wave is the 1465 PROPOSED design; it stays Draft and proposed and is not executable acceptance. The task's "target-mode proposal" and "finance CSV" are not in any merged diff and are recorded as not applicable, not as passed. No weather path and no `src/orchestrator` or `src/importer` file is changed by any merged PR, so no such test is run.

### Commands, environment and results (local, constructed synthetic data)

Environment: Python 3.12.3, Node v24.21.0, `env -i` with an owned empty `HOME`, `ZF_DATA` and `ZF_RESIDENT_MSSQL` unset, `PYTHONDONTWRITEBYTECODE=1`, run from an owned external working directory with `python -m unittest discover -s <worktree tests dir> -p <file> -q`; API selectors used `PYTHONPATH=<worktree>/src/core/tests:<worktree>/src/agents/tests:<worktree>/src/api` (not `mvp`). The pre-installed `zava-forward-*` distributions are editable installs of the owner's primary checkout and a preflight import resolved `zava_forward.core.ai` there, so they were not used. An owned venv outside the repository (`--system-site-packages`) took `pip install --no-deps -e src/core -e src/agents -e src/api` from this worktree (no uv). Preflight imports resolved `ai`, `exposure_limits`, `finance`, `live_simulator`, `live_control` and `server` from this worktree, and `git hash-object` equalled `git rev-parse HEAD:<path>` for 14 changed or tested files; `git status --porcelain --ignored -- src` was identical before and after (6 ignored build and cache folders). HEAD equalled the pin. No Docker, SQL Server, browser, scanner, external service, Azure, model or telemetry was used; T3 and T5 start ephemeral loopback HTTP fixtures and T6 uses Node, neither is an external service. The shared heavy-resource lock `/tmp/ama-rpi-heavy.lock` exists and was not taken because no heavy resource was needed.

| Id | Selector | Exit | Ran | Skipped | Covers |
| --- | --- | --- | --- | --- | --- |
| T1 | core `test_ai_provider_payload_spy` | 0 | 14 | 0 | PR 1466: exact provider wire bodies and closed field sets, no provider call when not permitted, unreadable inputs stop before a request (manual path) |
| T2 | core `test_exposure_limits` | 0 | 16 | 0 | PR 1467: non-finite observation is Unknown and pauses, huge integer still breaches, finite behaviour unchanged |
| T3 | api `test_finance_exposure_api` | 0 | 4 | 0 | Consumer regression of `finance.py` only; it has no non-finite case, so non-finite behaviour is attributed to T2 alone |
| T4 | core `test_ai_consumption` | 0 | 34 | 0 | Neighbour of the `ai.py` change (ledger) |
| T5 | api `test_ai_consumption_api` | 0 | 37 | 0 | PR 1468: legacy draft joins returned usage, missing or malformed usage is Unknown, provider failure stays manual with no usage, settlement failure never reports unsettled usage, workflow-only reserves nothing |
| T6 | api `test_exception_register`, `test_exception_register_screen`, `test_role_screens_conformance`, `test_data_operator_ai_state` | 0, 0, 0, 0 | 37, 22, 11, 7 | 0 | PR 1469: four-column contract, exact bytes, excluded fields absent, no second request, allowlists to Unknown, no file for unsafe or incomplete views, failure releases resources, escaping equal to the repository helper; node vm, not a served browser |
| T7 | api `test_live_control`, `test_live_simulator` | 0, 0 | 42, 37 | 0 | PR 1473: permit needs a sending control and a cohort home, unreadable or corrupt control is not a permit, stop, expiry or cohort removal mid-slot, stop before a retry or after backoff or a pacing delay, a raising gate fails closed, an open gate changes nothing, run ends after a fenced slot |
| T8 | core `test_live_readings` | 0 | 20 | 0 | Provider-independent simulator reading generator that the permit gate feeds |

Totals as printed by each final run: 281 tests ran, 281 passed, 0 skipped, 0 failures. Raw stdout, stderr, exit files, the preflight and pip logs and the failed attempts are local and outside the repository at `/home/azureuser/.copilot/session-state/676885f4-85ba-42d8-929c-40f438e5190f/files/checkpoint-440-1112/`.

Adverse and intermediate results, retained: `test_data_operator_ai_state` first failed at import (`No module named 'checks'`, an invocation error: `src/api` was missing from `PYTHONPATH`) and passed with 7 tests after the path was added. `test_live_control` and `test_live_simulator` failed at import four times, three of them after dependency installs, with `No module named 'azure'`, then `azure.identity`, then `azure.iot` (declared dependencies `azure-eventhub==5.15.1`, `azure-identity==1.26.0` and `azure-iot-device==2.14.0` of `src/api/pyproject.toml` were absent from the owned environment; an earlier pip run reported eventhub as already satisfied from the hidden user site, so it did not help the isolated run). Each was installed with pip into the owned venv only and both modules then passed. A preflight one-liner had a syntax error and was rerun. These are environment and invocation failures, not product findings and not passes.

### Requirement trace (document-qualified, proposed)

BRD and PRD both use the FR-049 label for different topics, so each row names its document. Classes: local observed (constructed synthetic), Azure observed (none here), implemented but unverified, deferred, blocked, unknown.

| Boundary or requirement | Contract, code and test | Class |
| --- | --- | --- |
| PRD FR-036 (in-review): AI tasks registered, unapproved or unavailable tasks use the manual route | `ai.py` (1468) and T1, T5: provider failure, malformed usage and workflow-only paths keep a manual or Unknown outcome and report no unsettled usage | Local observed on a loopback provider spy; no real model or cost claim; whole requirement unmet |
| BRD BG-012 (draft): whole-life cost, Total Cost of AI and AI cost per accepted outcome | T4 and T5 ledger behaviour; usage is attribution, not billing | Local observed; price, billing and cap enforcement not claimed; Azure usage unknown. Nearest requirement by inspection, not an authoritative mapping |
| PRD FR-018 (in-review): budgets, commitments and Finance disposition; #99 | `exposure_limits.py` (1467) with T2; `finance.py` consumer T3. Nearest requirement by inspection, not an authoritative mapping | Local observed for the finite guard; no Finance-screen false all-clear journey demonstrated; no Board or Finance input change; whole #99 unmet |
| PRD FR-012 (in-review): review exceptions expose both values; #80 | `role-screens.js` (1469) with T6: demonstrator-only CSV of the already-rendered `/api/exceptions` view, role-scoped, formula-neutralised, no complete-list or all-clear claim. Nearest requirement by inspection, not an authoritative mapping | Local observed in a node vm; browser download behaviour and assistive-technology use are not observed (browser harness not run); whole #80 unmet |
| #184 run-control stop and retry (stage B1); ADR 0003 IoT ingestion (Accepted) | `live_simulator.py`, `live_control.py` (1473) with T7 and T8: fail-closed permit before every attempt | Local observed on an in-process fake sink; a send already handed to the sink is not recalled (documented); cross-process fence B2, receiver start position, real Event Hub or device, and any cost or live run are deferred or unknown; Azure not observed |
| ADR 0006 `src` layout (Accepted); ADR 0003 runtime fit | All changes are inside `src/api` and `src/core` and their tests; no amendment | Context only |
| 1465 PROPOSED #184 design | Documentation proposal | Draft and proposed, candidate policy, not accepted and not executable acceptance |
| #440, #99, #116, #80, #432, #184 acceptance criteria | Unchanged, all OPEN | Partially delivered; criteria unmet |

### Boundaries observed

* Persistence: no persistence code changed in the wave; the ledger settlement order (1468) changes only what the receipt reports after settlement. SQL Server persistence is not observed here.
* Auth and roles: the exception CSV is built from the role-scoped view the API already returned and adds no route or request (T6); the run control remains admin-written, and no auth, role or access rule is widened. Role gating of the live control file (Azure RBAC on the share) is not observed locally.
* Resident, human, manual and AI-unavailable: no consent is read or written and no resident account, approval or AI route is added. A provider failure or Unknown usage leaves the human or manual outcome (T1, T5). The simulator stop is a fail-closed demonstrator control, not a human approval, and `live_control` approval references are not evaluated or granted by this record.
* Confidence limits: tests use synthetic loopback and in-process fakes; no deployed case, live telemetry, tenant or private generator was read.

### Findings, gates and recommendation (proposed for Root, not a decision)

* No defect is confirmed and none is asserted; no fix, refactor or new issue is proposed. The only failures were environment and invocation failures of this checkpoint, listed above. The task labels that do not match the merged PRs are a documentation qualification, not a product defect.
* Static observation, not a defect: a fenced slot ends the whole simulator run (`run` returns after a slot with `RUN_CONTROL_FENCED`), including when only one home left the cohort; this is the documented B1 behaviour and is covered by `test_run_ends_after_a_fenced_slot_without_waiting_for_the_next_one`.
* Affected gates: closure of whole #440, #99, #116, #80, #432 and #184 stays held. Any expansion that relies on cross-process run control (B2), a live or Azure simulator run, a real-model provider payload, billing or cost claims, the browser download of the exception CSV, or the 1465 proposal being treated as accepted stays held until separately evidenced and approved by the named human owners. Independent exact-head review of this record and applicable hosted checks remain required, and its publication waits for the #134 log and pack append and conflict resolution so both append-only entries are preserved.
* Independent lanes: (1) browser-served exception CSV download and keyboard or assistive-technology check under the existing admitted browser harness; (2) #184 B2 or Azure-only residuals after the owner admits spend and cleanup boundaries; (3) #99 Finance-screen journey with non-finite input. Resume condition for any lane: a named owner scope and, for Azure or browser, the existing admission and lock.
* Recommendation: CONTINUE, bounded. This is not a tick of any criterion, an approval of any requirement or ADR, or a deferral decision. Human decisions still open: acceptance of the 1465 proposal, owner admission for Azure or live runs, and legal, professional and resident acceptance of any resident-facing use.

### Process limits

* Original dated RPI evidence is under `.copilot-tracking/` (`demo-wave-checkpoint-440-1112`): research, plan, details, one independent read-only critique (two blocking, three significant, one minor finding, all applied), changes and one author Review (author-executed, not independent). Model label asserted; no witness or host attestation exists.
* The case study addendum (158 KB) was read by section, not end to end. Counts are as printed in this run. No push, PR, issue or board write was made.

### Accuracy follow-up (2026-11-12, documentation only, after frozen head `26cb3968`)

This is a bounded accuracy correction of this record, not a source, HVE or coordinator-code correction, not a reopening of the old #440 campaign and not a new correction pool. The text above is otherwise unchanged and the original is preserved at commit `26cb3968`; original research and Review files are not rewritten and carry additive follow-up files instead.

* 1467 wording: the wave-table row first said "non-finite or huge-integer-unsafe ... observation as Unknown". That wrongly implied huge integers become Unknown. `_finite_observation` accepts every `int` and only a finite `float`; NaN and infinite observations give an Unknown finding for that limit, and huge integers still breach (`test_huge_integer_observation_still_breaches`). No product defect is implied or asserted.
* Preflight qualification: the original `02b` preflight printed `None` for the namespace `zava_forward.agents`, which proves no concrete origin and is preserved unchanged. Later, after the freeze and with no repository change, the author ran one import trace in the same owned environment, working directory and `PYTHONPATH` and compared each loaded module `__file__` hash with `git hash-object` against `HEAD:<path>`: 14 of 14 matched and no loaded module came from the primary checkout. Concrete agents modules `chat` `ae03ad5f25e5`, `dispatch` `2e2306c62790` and `regulatory_chat` `d8937e62df1a`; helpers `release_support`, `test_assistants`, `test_mvp` and `checks.data_operator_ai_state` are all under this worktree. Limitation: this is a fresh trace of the same selectors, not instrumentation of the original 281 tests; only T5 imports `zava_forward.agents` directly and transitive imports of the other modules were not traced; the environment and procedure are as reported by the author and not independently attested. Raw output: `/home/azureuser/.copilot/session-state/676885f4-85ba-42d8-929c-40f438e5190f/files/checkpoint-440-1112/diag/agents-origin.out` and `.err`.
* Scope: the tested source pin remains `bbb1d20cc984` and the source-equal fresh main `5ee8ac14c70f`. Later main `088e8c3` (it includes PR 1470) is outside the tested wave; no current-main acceptance is claimed for it. Nothing was rerun or installed.

## Post-153 integration checkpoint (2026-11-12, Refs #440 #153 #134 #184)

Draft, local-only, not approved. This is a bounded recurring checkpoint under existing issue #440 after the previous checkpoint (PR 1478, merge `4074b44f3704b860dd4b890473cca620115d3dca`) whose 281 historical tests, run at the earlier pin `bbb1d20cc`, explicitly excluded PR 1470 (proposal-card plain-language source) and PR 1475 (five-home runbook). Both merged after that tested pin but before the PR 1478 publication (see the accuracy note below), not after it. It supplies current evidence for those two inputs only. It is not a new issue, feature, approval or correction pool, grants no new correction allowance, does not rerun the 281-test campaign, changes no source, test, tool, workflow, configuration, requirement or ADR, opens no issue and ticks no criterion. The last two acceptance criteria of #440 (triage into independent issues and the Major HVE behavior-tested coordinator change) are not completed here.

### Identities and exclusions

| Item | Identity (read 2026-11-12) |
| --- | --- |
| Pin | Worktree HEAD (branch `docs/post153-integration-checkpoint-440-1112`) equals freshly fetched `origin/main` `4074b44f3704b860dd4b890473cca620115d3dca`. Root tree `88a7ffbd1c88ecdaee5a3f538579fbcabfab5dd2`; `src` `b03b4c9d8ca1dbabc04a9032686a471bf300100c`; `docs` `99601f87116262eb1add72b7aeb3cf0271b9b461`; `infra` `a022907662e2`; `tools` `432a4e8f7d74` |
| PR 1470 | Merge `088e8c3c031be45b22422b91b3195b0988583ebd`, tree `68f0db875dfab4ad5b1f9fa4410a8b47c359148d`. Non-evidence paths: `assistants.js`, `assistants_browser_check.py`, `test_content_standard.py`, `test_case_journey.py`, `content-standard.md`, `log.md` |
| PR 1475 | Merge `38d3ed18703ee05c6795f715b6e62600d36225ec`, tree `cc219a7fc19c31b876144aa9ac783fd9863d6c5f`. Documentation only: `runbook.md`, `docs/reference/README.md`, `log.md` |
| Source delta from the previous tested pin `bbb1d20cc` | `src` tree `60d841010c4a` to `b03b4c9d8ca1`: 4 files, 554 insertions, 179 deletions, all from PR 1470 |
| Blobs at the pin | `assistants.js` `40cfc532cab0`; `test_content_standard.py` `029516bee815`; `test_case_journey.py` `f05d5eee41b7`; `runbook.md` `e15eef73925b`; `content-standard.md` `aa1cf210269f` |
| Status documents | BRD 0.21.0 `draft` `34d88395de86`; PRD 0.21.0 `in-review` `c788b917bafa`; ADR 0003 `d60645397b20` and ADR 0006 `956da1a3b804` Accepted; ADR 0007 `541e0f72dd2c` Proposed. None is changed by either PR; draft, in-review and Proposed are not approval |
| Issue and PR states (live `gh`) | #440, #153, #132, #134 and #184 OPEN; PRs 1470 and 1475 MERGED |
| Excluded | The 281 historical tests (not rerun); execution of `assistants_browser_check.py` and `loading_briefing_browser_check.py` (browser harness not installed or run); `test_workspace_scripts.py` (it lists `assistants.js` only in a route and script allowlist, not the card); local commit `6819456` (not an ancestor of HEAD, on a sibling branch); SQL Server, Docker, hosted CI, scanners, Azure, models, the live endpoint, sensors, private data and `support/` |

### Environment, commands and results (local, constructed synthetic data)

Python 3.12.3 in an owned venv outside the repository, `/home/azureuser/.venvs/post153-440-1112` (`--system-site-packages`), with `pip install --no-deps -e src/core -e src/agents -e src/api` from this worktree (exit 0; no uv). Every run used `env -i`, an owned empty `HOME`, `PYTHONDONTWRITEBYTECODE=1`, an owned external working directory and `PYTHONPATH=<worktree>/src/core/tests:<worktree>/src/agents/tests:<worktree>/src/api`. The pre-installed `zava-forward-*` distributions in the user site were not used. Origin proof is the loaded module `__file__` with `git hash-object` equal to `git rev-parse HEAD:<path>`: 7 of 7 equal (`test_content_standard`, `test_case_journey`, `test_quality_sensors`, `ai`, `exposure_limits`, `server`, `agents.chat`). The namespace package `zava_forward.core` prints `__file__` `None`, which is not origin proof; its `__path__` is in this worktree. `git status --porcelain --ignored -- src` was identical before and after (3 ignored egg-info folders). No Docker, SQL Server, browser, scanner, external service, Azure, model or telemetry was used, and the shared heavy-resource lock was not needed.

| Id | Selector (`python -m unittest discover -s <worktree>/src/api/tests -p <file> -q`) | Exit | Ran | Skipped | Covers |
| --- | --- | --- | --- | --- | --- |
| T1 | `test_content_standard.py` | 0 | 19 | 0 | PR 1470: copy audit of web files, the new check that technical evidence sits in one labelled disclosure, banned-term guard |
| T2 | `test_case_journey.py` (node `v24.21.0` on PATH) | 0 | 31 | 0 | PR 1470: assistant proposal-card fixtures including the renamed edit label (`test_case_journey.py:1299`); node fixtures, not a served browser |
| T3 | `test_quality_sensors.py` | 0 | 187 | 92 | Quality tab and `assistants.js` token tests that the five links target; 95 executed, 92 skipped |
| T4 | `node --check` on `assistants.js` and `app.js` | 0, 0 | not applicable | not applicable | Syntax only |
| T5 | Static runbook check (`five-home-static-check.py`, standard library, outside the repository) | 0 | 5 rows | not applicable | PR 1475 link contract, string level |

Executed and passing: 145 tests (19, 31, 95), 0 failures in the final runs. The 92 skips are not passes. Their reason is the `MSSQL` gate at `test_quality_sensors.py:1802` ("needs disposable SQL Server (ZF_TEST_MSSQL=1)"); per-test reasons were not captured with `-q`, so attributing all 92 to that gate is inferred from source. Raw stdout, stderr, exit files, `preflight.out`, `origin-trace.out`, `five-home-static-check.out`, `dedupe-search.out`, `command-manifest.txt` and `sha256-manifest.txt` are outside the repository at `/home/azureuser/.copilot/session-state/d351ddc0-f4e6-4e5f-ae56-db0937d3ad2b/files/checkpoint-440-post153-1112/`.

Adverse and intermediate results, retained: the first `test_case_journey.py` run failed with 35 errors (`FileNotFoundError: 'node'`, because `env -i` removed node from PATH; an invocation error, preserved as `test_case_journey-attempt1-nonode.err`) and passed with 31 tests once node was on PATH. The first origin trace failed (`No module named 'test_content_standard'`, tests path missing; preserved) and was rerun. The first preflight guessed the module `zava_forward.core.sensors`, which does not exist (the modules are `sensor_*.py`); this was an author error, not a product finding. These are environment and invocation failures, not passes and not defects.

### Five-home link contract (PR 1475, static, public source only)

The check parsed the five table rows of `runbook.md` and confirmed: five unique ids matching `ZF-<4 digits>-<4 digits>` (`ZF-2025-0355`, `ZF-2025-0382`, `ZF-2025-0286`, `ZF-2026-0829`, `ZF-2026-0892`); each link text and path id equal the table id; each link is `<origin>/app#/case/<id>?tab=quality`; the route `#/case/<encoded id>`, the `tab` query and the `quality` tab ("Quality and handover") exist in `app.js` (lines 382-387 and 1146); the single origin host equals the host this pack documents from the 2026-10-31 observation (one mention); the README anchor equals the computed heading slug; the two relative documentation links resolve. Search boundary: the script read only `runbook.md` and the web source. A later `git grep` over tracked files at `8bfd52729` (`five-id-tracked-search.out`; not searched: untracked and ignored files, `support/`) finds the ids in this pack, `runbook.md` and one tracked historical record, `.copilot-tracking/research/2026-11-12/five-home-script-134-1112-research.md`. That record and the generator replay it cites were not reproduced or read here, and the original sentence that no other tracked file mentioned the ids was wrong (see the accuracy note below). Limits: the id shape check tests the runbook against itself, because no public source defines the id shape (`chat_case_answers.py:16` uses `ZF-\d+`); the ids, their open state, any sensor and the effective AI scope are not verified in any build; the generator replay behind them sits under `support/` and was not read; availability of the origin, sign-in behaviour, redirect retention of the hash and the `Funding check` stage of home 5 are unknown. The runbook labels all of this a target.

### Requirement trace (document-qualified, proposed)

Classes: local observed (constructed synthetic), implemented but unverified, blocked, unknown. Requirement rows are nearest by inspection, not an authoritative mapping.

| Boundary or requirement | Source and test | Class |
| --- | --- | --- |
| #153 plain-language content standard (content-standard.md, owner-approved 2026-11-12) | `assistants.js:130-135`, `content-standard.md` row, T1, T2 | Local observed in static and node fixtures: technical evidence in one native details disclosure; warnings, reasons, unknowns and review controls remain outside it; edit label renamed. No human resident-wording review and no assistive-technology acceptance; whole #153 and its criteria unmet. PRD FR-036 (versioned AI task registry with manual route for unregistered tasks, in-review) is not exercised by these checks: the card change touches presentation only, and no registry or denied-task path was run |
| Keyboard reachability and disclosure behaviour of the card | `assistants.js:103,133` (`tabindex="0"`), `assistants_browser_check.py` | Implemented but unverified: the browser check changed by PR 1470 was not run |
| Human and resident boundaries on the card | `assistants.js` review fieldset unchanged | Local observed only as unchanged structure; no consent, approval or send is read or written |
| #134 and #184 five-home demo target; ADR 0003 (Accepted) | `runbook.md:48-119`, T5 | Documentation observed; target, not implemented or deployed; live ids, cohort, sensor store and AI scope are unknown; no model call or spend authority |
| ADR 0006 `src` layout (Accepted); BRD `draft` and PRD `in-review` | no change | Context only |
| #440, #153, #132, #134, #184 acceptance criteria | unchanged | All OPEN, partially delivered, unmet |

### Findings, owners and omissions (reported, no issue created)

* F1, static and unverified: the two new `pre` elements at `assistants.js:103` and `assistants.js:133` carry `aria-label` and `tabindex="0"` without an explicit role. Whether an accessible name is exposed for a `pre` with its implicit generic role is not established: no standard was fetched, no web review was done and no assistive-technology observation exists, so this is not a conformance claim or a confirmed defect (an earlier blanket statement that ARIA prohibits naming a role-less element was overbroad and is withdrawn). The repository's own focusable scroll areas use `role="region"` (for example `app.js:853`; `design-system.md:94-95,109` describes that pattern for tables only). No repository rule is shown to be breached. Owner candidates by inspection: #153, or #132 and #134 accessibility work; three open-issue searches found no duplicate (`dedupe-search.out`), which is not proof of absence. Not filed, not fixed.
* F2, omission: the browser check changed by PR 1470 and the keyboard behaviour of the card were not run; this stays unverified until the admitted browser harness runs.
* F3, coverage gap: no repository test covers the five-home runbook contract; the string-level check used here lives outside the repository and was not added as a test.
* No product defect is confirmed and none is asserted.

### Gates and recommendation (proposed, not a decision)

* Closure of whole #440 and #153, and any expansion that relies on the card, the five homes or the live demo target, stay held. Held items: browser and assistive-technology evidence of the card, human resident-wording review, a live preflight of the five ids and cohort, owner admission for any Azure, model or spend action. Independent exact-head review of this record and the applicable hosted checks remain required. No hosted workflow result is claimed for this head.
* Recommendation: CONTINUE, bounded. It is not a tick of any criterion, an approval of any requirement or ADR, or an acceptance of PR 1470 or PR 1475. Human decisions still open: owner approval of any change for F1, owner admission for live or browser lanes, and resident and professional acceptance of any resident-facing use.

### Process limits

* Original dated RPI evidence is under `.copilot-tracking/` (`post153-integration-440-1112`): research, plan and details, one independent read-only critique (verdict Revise, nine findings; the original plan recorded all as applied, but PC-007 was not fully applied, see the accuracy note), changes, state and one Review. The model label is asserted; no witness or host attestation exists.
* The case study addendum was not read end to end. Counts are as printed in this run. No push, PR, issue or board write was made.

### Accuracy note (2026-11-12, documentation only)

Added after the coordinator's independent read of the frozen candidate `8bfd52729`. It corrects four statements; the original research, plan, critique, review and raw evidence of this checkpoint are unchanged and still contain the errors named here. Counts (145 executed, 92 skipped), the `4074b44f3` pin and the partial requirement-qualified coverage are unchanged, and nothing was rerun.

* Five-id search boundary: the earlier sentence that no other public tracked file mentions the ids was wrong; see the five-home section for the actual boundary. A tracked historical record exists and was not reproduced here. Nothing is claimed about deployed membership or absence.
* Tracking-file counts: `git show --format= --name-only` lists 20 paths under `.copilot-tracking` for PR 1470 and 7 for PR 1475. The original research said 16 for PR 1470 and the original critique said 19; both were wrong, and PC-007 was not fully applied although the original plan recorded all nine critique findings as applied. The count is context only.
* Merge ordering: PR 1470 merged 2026-11-12T17:38:13Z, PR 1475 at 17:46:55Z and PR 1478 at 18:00:25Z (GitHub merge metadata). Both inputs followed the tested pin `bbb1d20cc` and preceded the PR 1478 publication; the original research wording "merged after the previous #440 checkpoint (PR #1478)" was wrong. They were still outside the 281-test evidence and outside the PR 1478 record.
* Accessibility wording: the original statement that ARIA 1.2 prohibits naming a role-less element was overbroad and is withdrawn (finding F1 above states the narrowed, unverified concern). No source was changed.
* Any proposed acceptance gate in this section is a proposal; it does not bar independent source work and is not an owner decision. No criterion, approval or closure follows from this note.
* Evidence under `.copilot-tracking/` (`post153-integration-440-1112-accuracy`).

## AC-034 to AC-043 disposition reconciliation (2026-11-12, Refs #134)

Draft, documentation only, not approved. This section reconciles the ten document-qualified PRD requirements named by the literal second acceptance criterion of #134 ("AC-034 to AC-043 pass or are recorded as deferred with reason") against the register, the sections of this pack that already trace some of them and exact source at the pin. It adds only what was missing: the work owner, a concrete resume check, candidate source evidence not yet in the register and the reading of `partial`. It changes no source, test, tool, workflow, requirement or ADR, opens no issue, ticks no criterion, accepts no epic and approves no pivot or deferral. The pack's other sections are linked, not restated.

### Identities and what ran

| Item | Identity (read 2026-11-12) |
| --- | --- |
| Pin | Worktree `HEAD` and the local `feat/demo-ux-integration-1112` equal `43b2187b918206666c63cb25d8b338be09791118`, tree `67cbe8ede92d4f9f02ac3a3f71d0de06872f6b55`; `origin/main` also equalled it at read time and has since advanced, so it is historical and not the current main. The branch `feat/demo-ux-integration-1112` was not present on the remote at read time |
| Requirement source | PRD Zava Forward Retrofit Programme Workbench 0.21.0 `in-review`, blob `c788b917bafa` (AC-034 to AC-043, lines 2130 to 2139). In-review is not approval |
| Register | `src/core/src/zava_forward/core/journey_acceptance.py` blob `e3466b6eafc0`, unchanged; indexed in [the Core guide](../../src/core/README.md#acceptance-register-for-ac-034-to-ac-043-134-slice-2) and the 2026-11-04 log entry |
| Executed here (register integrity only, not evidence for any row) | `journey_acceptance.check` printed status `recorded`, no blockers, `passed` empty, `partial` AC-034, 037, 039, 040, 042, 043, `deferred` AC-035, 036, 038, 041. `python -m unittest tests.test_journey_acceptance tests.test_journey_store tests.test_journey_building -q` from `src/core` with `PYTHONPATH=src:tests` ran 15 tests, OK. No browser, SQL Server, axe, model, cloud or private data |
| Not rerun | Every other figure below is quoted from the cited pack section or record at its own date and source version. None is promoted to a current execution |

### Reading of the register statuses

The register status is authoritative for the code check and is not changed here. No row passes. `deferred` means no existing evidence is mapped to the criterion. `partial` means named constructed-fixture evidence covers part of the Given, When or Then; the column "Not shown" names the unproven remainder, which this record reports as unproven and not as accepted. Candidate evidence marked implemented but unverified is source that exists and was not mapped or run against the criterion. The work owner column names issues that own or last owned the behaviour; closed issues #85 and #90 are historical evidence and not live owners. #83 and #134 are open owners; no named person is assigned. No human acceptance owner is recorded for any row (unassigned). The resume check is the smallest executed check that would let the row be re-read; human or assistive-technology observation is separate and not recorded for any row.

### Disposition table (document-qualified, none passes)

| Requirement (PRD 0.21.0 in-review) | Register | Qualified observed evidence | Not shown | Work owner and resume check |
| --- | --- | --- | --- | --- |
| AC-034 scope, reset, selection and focus (FR-032) | partial | Workbench browser check, 108 PASS lines and no-match versus unknown coverage text, local synthetic ([merged-wave section](#merged-wave-checkpoint-2026-11-10-refs-440-149-153-1238-93-96-148), row C3, line 6186). Keyboard and evidence probe at `b23c08e33`, 714 PASS lines, 38 role-screen walks, 15 negatives, first listed home only (line 6828; limit restated at line 6842). Programme paging 89 PASS and role-screens story 230, 70 PASS, observed on the parent integration before PR 1376 reached main (line 6373) | Focus return to the originating row (the [profile review](../reference/research/ux/zava-forward-prototype-profile-review.md#shared-workbench-ia-engineering-slice-2026-10-15), lines 1020 to 1028, records that returning to a list focuses main, not the originating row); reset ID, count and order compared with the manifest for all eleven profiles; announcement by assistive technology; a producer that separates unrepresented from zero-match | #152 and #134. Resume: a served browser check that, per profile, resets and compares IDs, count, order and focus, then named human and assistive-technology observation |
| AC-035 update commitment and rejected handoff (FR-033) | deferred | Candidate only, implemented but unverified for this criterion: `resident_decisions.py` `_res_update_record` (line 1861) with `test_incomplete_commitments_dates_and_identity_fail_without_mutation` (line 3278) and `test_handoff_cannot_create_partial_commitment_or_clear_existing_one` (line 3544). They relate to the clause that a handoff does not clear or create a commitment, not to the rejected-handoff Given or to display of purpose, owner, due basis and safe route | The full Given, When and Then; any screen showing the commitment beside a rejected handoff | #134 with the resident-workflow owner. Resume: map the two tests to the criterion and add a served view check |
| AC-036 owner, destination, receiver and chase-owner labels (FR-011, FR-034) | deferred | Staff waiting screen, PR 1444 ([section](#handoff-waiting-screen-integrated-main-checkpoint-2026-11-11-refs-440-83), trace row line 7164) and personal handoff refusal guidance, PR 1449 ([section](#personal-handoff-http-guidance-integrated-main-checkpoint-2026-11-11-refs-440-153), trace row line 7230), local synthetic: unknown is stated, scope is explicit, manual paths kept | Agreement of the four labels across queue, detail, source and history; the keyboard walk saw only that owner or next-action text exists (line 6843) | #83 (open) and #134. Resume: a served check that asserts the four labels agree on one fixture with an unassigned receiver and a missing return reason |
| AC-037 per-measure pause or withdrawal (FR-014, FR-045, FR-046) | partial | Per-measure decision records and `src/core/tests/test_resident_decisions.py` (Core); read-only copy of recorded state on constructed fixtures ([line 7065](#resident-choice-csv-feature-wave-integrated-main-checkpoint-2026-11-11-refs-440-1420-1432-80-73)) | Pause isolation across measures mapped to the criterion, contact is not consent, service and redress owner display | #134 and the resident-workflow owner. Resume: map or add the isolation test and a served check; resident or professional acceptance is separate and absent |
| AC-038 referral with unconfirmed receipt and retrofit hold (FR-015) | deferred | Candidate only, implemented but unverified for this criterion: the hazard referral and home-hold contract with `src/core/tests/test_hazard_referral.py`; the [2026-10-17 #85 record](../reference/research/ux/zava-forward-prototype-profile-review.md#hazard-referral-evidence-engineering-continuation-2026-10-17-85) reports 33 run on SQLite and 16 on task-owned SQL Server, with one JSON-only skip in each run, with its original adverse review retained; the closing comment on #85 (closed 2026-10-17) records independent final-head review and merged PR 388, which supersedes the profile review's "closure pending" wording | A workbench display of awareness, sent reference, chase owner and a read-only release reference for the constructed referral; hazard-service human acceptance. The workbench does not judge release sufficiency | #134 (#85 closed, historical evidence). Resume: a served view check of the constructed referral; the hazard service keeps its own authority |
| AC-039 draft package readiness (FR-016) | partial | Capacity and package records, `src/core/tests/test_quality_procurement.py` (Core); provider capacity [continuation #90](../reference/research/ux/zava-forward-prototype-profile-review.md#provider-capacity-engineering-continuation-2026-10-17-90) | Readiness display with period, scope, offered versus committed state and next reviewer; not an instruction or booking | #134 (#90 closed, historical evidence). Resume: a served check of the draft-package panel |
| AC-040 conflict comparison and case rationale (FR-012, FR-034) | partial | Source-conflict queue and `src/core/tests/test_exception_queue.py` (Core); atlas checker 362 PASS and the story selectors 231, 231q, 231p and 231qp, as named in the source, observed on the parent integration (line 6374; selector names, not a count of stories) | Per-case rationale that agrees with its own evidence across the fixtures on switching; the Quality Inspector omission of the technical change note stays unasserted | #134 and #233. Resume: an executed check over the fixtures on current main |
| AC-041 portfolio figures and filter impact (FR-024) | deferred | None mapped | Population, as-of basis, denominator, filter impact and handover versus accepted handover for the fixed illustrative figures | #134. Resume: a constructed reconciliation or an illustrative-cohort label with a served check |
| AC-042 quality review and invoice comparison (FR-017, FR-018) | partial | Quality and finance records, `src/core/tests/test_quality_procurement.py` and `src/core/tests/test_finance_match_controls.py` (Core) | The incomplete-pack and quantity-mismatch invoice views with independent disposition; payment stays unavailable | #134 (#90 closed, historical evidence). Resume: a served check of the incomplete pack and mismatch lines |
| AC-043 manifest coverage (FR-001, FR-002, FR-022, FR-035) | partial | Manifest with eleven profiles and nine workflows and `src/core/tests/test_scenario_manifest.py`; the actual AC-043 probe (pack line 7123: walks the screens its fixture roles are served and declares the intake empty state, local observed, partial); related isolation only, not manifest coverage: the #1029 JSON-store trace and #1152 sibling and building negative controls (eleven constructed current-source tests per the [2026-11-05 closure-audit comment on #134](https://github.com/jmservera/ama/issues/134#issuecomment-6655269090), an issue comment and not a repository record), which support same-home trace and isolation; perspective register eleven by five with zero met (line 6846) | Slice B connected exception view; all eleven endpoints; fixture login roles for Asset, Procurement and Auditor | #134. Resume: eleven declared entries each with a served endpoint check |

### What this does not establish

* Criterion 2 is not claimed met. Six rows are partial and four deferred; the reasons and owners above are an engineering record, not an owner-approved deferral. The owner decides whether it suffices.
* No keyboard, assistive-technology, human, resident, professional or live acceptance is recorded for any row. No requirement, ADR or BRD item is approved; BRD 0.21.0 is `draft`.
* The register still says "not mapped yet" for AC-035 and AC-038 and has no owner or resume fields. Updating it is a source change and is a separately owner-admitted slice, not done here.
* Legal and regulatory: no claim is made. AC-038 involves hazard handling; the workbench neither classifies hazards nor runs a statutory clock.
* The remaining literal #134 criteria stay open: all eleven perspectives with entry, evidence, safe endpoint, recovery and handoff (1), this criterion (2) and keyboard, text and status announcements (5). Criteria 3, 4 and 6 are already ticked and unchanged. Whole #134, the original A4 and E1 to E4 corrections (spent) and the unadmitted E5 and E6 are untouched.
* Correction 1 (2026-11-12, independent review R-1 to R-5) amended this section after publication review, and correction 2 restored #83 as an open owner (it had been wrongly called closed); the original adverse critique and review stay preserved in their artifacts.
* Original RPI evidence is under `.copilot-tracking/` (`ac-dispositions-134-1112`): research, plan, details, one independent critique (Revise, eight findings, all applied), changes, state and one Review. The model label `claude-sonnet-5.5` is asserted by the launcher; no witness or host attestation exists.

## Post-fix-wave checkpoint (2026-11-12, Refs #440 #128 #98 #115)

Draft, local-only, not approved. This is the recurring checkpoint under existing issue #440 that is due because one specific fix wave completed: PR 1481 (#128), PR 1483 (#115) and PR 1482 (#98). It is not a whole-product audit, epic closure, new issue, new feature or approval, and it resets no earlier correction budget. The preceding checkpoint (post-153 section above, PR 1480, merge `cd81888e4a81cf4c712d50b357ca900fd5c8c06b`) is the baseline and is not a fresh result. The unmerged candidates 107, 134, 153, 157, 435 and 82 and their sibling functionality are excluded. No source, test, tool, workflow, configuration, requirement or ADR is changed, no issue is opened and no criterion is ticked. The last two acceptance criteria of #440 (triage into independent issues; Major HVE behavior-tested coordinator change) are not completed here.

### Identities and exclusions

| Item | Identity (read 2026-11-12) |
| --- | --- |
| Pin | Worktree HEAD (branch `docs/demo-fix-wave-checkpoint-440-1112`) equaled `origin/main` `e155c88ed6357259a11520e7150b7ad9d349b9f8` when freshly fetched at the time of the checks (2026-11-12). A later fetch shows `origin/main` at `eac1206c6ca08bd551e3d0d2384bb87a1f05c24f` (tree `ff26901294f2`), which differs from the checked base only by the rubric score record `.github/rubric/scores/latest.json` (a `chore(rubric)` commit); the checked base is its ancestor and nothing here was rerun at the later commit. Checked-base identities: root tree `82eea54a212bbb442e7c2257e1349480faa18505`; `src` `7b61d44bc705`, `docs` `8fe82ba5b637`, `infra` `be7fa0b2502e`, `tools` `432a4e8f7d74` (unchanged from the baseline). Delta from `cd81888e4`: 11 files, 216 insertions, 28 deletions outside `.copilot-tracking` and the rubric score record `.github/rubric/scores/latest.json` (a `chore(rubric)` commit, 5 insertions and 5 deletions) |
| PR 1481 (#128) | Merged 2026-11-12T21:38:04Z as `59eac895112ebb97cfa6c27413b3d398e6f056e4`, tree `8fcebb38afee`. The PR title says `fix` and the squash commit subject says `feat`; the content is the one change below |
| PR 1483 (#115) | Merged 21:50:20Z as `43b2187b918206666c63cb25d8b338be09791118`, tree `67cbe8ede92d` |
| PR 1482 (#98) | Merged 22:00:46Z as `e155c88ed6357259a11520e7150b7ad9d349b9f8` (two squashed commits: the fix and a hosted-typing correction) |
| Blobs at the pin | `paired_equity.py` `23e553ab982a`; `test_paired_equity.py` `15dce2f3dfa5`; `form_export.py` `51b9a4af9d68`; `test_form_export.py` `18e582573670`; `digest_blob.py` `03544499a722`; `test_digest_blob.py` `9f55c0a65a18`; `infra/tests/test_bicep_policy.py` `0d482ae35238`; `test_form_held_download_api.py` `1c9b900f33df` |
| Documents | PRD `zava-forward-retrofit-programme-demonstrator.md` 0.21.0 `in-review` `c788b917bafa`; BRD `agentic-retrofit-programme-brd.md` 0.21.0 `draft` `34d88395de86`; ADR 0002 `cbe21530043f` Status Proposed; ADR 0003 `d60645397b20` and ADR 0006 `956da1a3b804` Accepted. None is changed by the wave; draft, in-review and Proposed are not approval |
| Issue states (live `gh`) | #440, #128, #98, #115 OPEN; the three merges use `Refs` and no closing keyword |

What changed, read at the pin: #128 adds `source_completeness` (constructed `source_record` complete versus missing) as a fourth required `paired_equity` dimension and reports a ranker that leaves the subject out as `excluded` instead of raising (`fairness_evidence` and `activation_allowed` stay false). #115 makes the scheduled ledger job print `LEDGER_DIGEST_ALERT ledger verification could not run: <exception type>` and exit 1 for any unexpected store, container, publish or verify failure, with a static test binding both alert queries in Bicep to the marker constants. #98 makes `export_freshness` compare each saved field's digest-covered open validation issues, so a held pack is no longer `Current` after an issue changes, and treats a malformed issue list as `Invalid`.

### Environment, commands and results (local, constructed synthetic data)

Python 3.12.3 in an owned venv outside the repository, `/home/azureuser/.venvs/postwave-440-1112` (`--system-site-packages`), with `pip install --no-deps -e src/core -e src/agents -e src/api -e src/orchestrator` from this worktree (exit 0; no uv). Origin proof: the loaded `__file__` of `paired_equity`, `form_export`, `digest_blob` and `api.server` equals this worktree and its `git hash-object` equals `HEAD:<path>` (4 of 4). Tracked tree clean before and after the runs; untracked paths were limited to this task's artifacts. Installed tools differ from the pinned ones (ruff 0.17.3 versus 0.17.1, mypy 2.4.1 versus 2.4.0), so no hosted-parity claim is made. In-process SQLite test stores (for example `test_form_review.py:31`) ran as local synthetic coverage; SQL Server (`ZF_TEST_MSSQL`), Docker, the browser harness, scanners, hosted CI, Azure, models, the live endpoint, private data and `support/` were not run or used.

| Id | Command (from the named directory) | Exit | Ran | Skipped | Covers |
| --- | --- | --- | --- | --- | --- |
| T1 | `src/core`: `unittest discover -s tests -p test_paired_equity.py -q` | 0 | 26 | 0 | #128: four dimensions, seeded defects, exclusion without crash |
| T2 | `src/core`: `-p test_journey_register.py` | 0 | 7 | 0 | Dependency of the paired check |
| T3 | `src/core`: `-p test_form_export.py` | 0 | 11 | 0 | #98: changed, removed and malformed open issues |
| T4 | `src/core`: `-p test_form_dependencies.py` | 0 | 10 | 0 | Stale propagation consumer |
| T5 | `src/orchestrator`, `PYTHONPATH=../core/tests`: `-p test_digest_blob.py` | 0 | 30 | 0 | #115: unexpected-failure marker, exit codes, no secret leak |
| T6 | `src/api`, `PYTHONPATH=../core/tests:../agents/tests`: `-p test_form_held_download_api.py` | 0 | 6 | 0 | Local HTTP held-download regression, synthetic fixture |
| T7 | `infra`, `REQUIRE_AZ_BICEP=1`: `unittest tests.test_bicep_policy.BicepPolicyTests.test_ledger_alert_queries_match_the_verifier_markers -v` | 0 | 1 | 0 | Alert queries contain `ALERT_MARKER` and `OK_MARKER` (local `az bicep` compile, no cloud call) |
| T8 | `infra`, `REQUIRE_AZ_BICEP=1`: `unittest tests.test_bicep_policy -q` | 0 | 61 | 0 | Whole Bicep policy module |
| T9 | `src/core` and `src/orchestrator`: `python -m ruff check` and `ruff format --check` on `src tests` | 0, 0, 0, 0 | not applicable | not applicable | Lint and format |
| T10 | `src/core`: `python -m mypy` (configured scope, 298 files); `src/orchestrator`: `python -m mypy src tests` (16 files) | 0, 0 | not applicable | not applicable | Types; the #98 hosted failure was in this core scope |

Executed and passing: 90 unit and HTTP tests in T1 to T6 plus the 61-test infra module (T8, which includes T7), 151 in total, with 0 failures and 0 skips in the final runs. Raw stdout, stderr, `preflight.out`, `origin-trace.out` and `sha256-manifest.txt` are outside the repository at `/home/azureuser/.copilot/session-state/f9385f39-ed8d-41ab-b9b0-67f1574db2fe/files/checkpoint-440-postwave-1112/`.

Adverse and intermediate results, retained: the first static run called `ruff` and `mypy` by bare entry-point name from the venv `bin` directory and exited 127 for all six commands (the tools are in the system site, not in the venv); it was an invocation error, preserved under `attempt1-exit127/`, and the checks were rerun with `python -m`. The T1 to T6 runs were not repeated at the baseline, so failing-first proof of the new tests is the feature artifacts' claim and was not reproduced here.

### Original feature-wave qualifications (preserved, not re-observed)

* #128 (PR 1481): the independent critique ran after the draft plan and implementation draft existed; its High finding (exclusion crash) was added to scope and fixed failing-first. Review CLEAN with one non-defect note: a ranker that excludes only the reference while ranking the subject passes under the stated rule.
* #98 (PR 1482): the first focused mypy covered `form_export.py` only, not the configured scope; hosted SourceCI run 43308748514 then failed configured `mypy` with two `attr-defined` errors at `test_form_export.py:170,172`, corrected in the same PR by importing helpers from their defining modules. T10 now passes the configured scope locally.
* #115 (PR 1483): initial wrong-tool and configuration checks occurred (recorded in its changes file); the review agent could not run the orchestrator tests in its own environment and the author's runs are the execution evidence; one Low note stayed open and routed (a `DocumentStoreError` raised while opening the store would print its message; no store module raises it).
* 1483 merge process, as reported by the coordinator: an immediate GraphQL `UNKNOWN` merge-state response preceded a normal guarded accepted merge. It was not re-observed here; live `gh` shows the PR `MERGED`.

### Cross-package contracts

* Orchestrator to infra: the marker constants in `digest_blob.py` equal the strings in the two ledger alert queries (T7, static compile). The alert rules are candidates with a proposed owner and an actual appointment pending (`operationalMonitoring.bicep` description text); no hosted alert, scheduler run or notification delivery was observed.
* Core to API: the API server calls `draft_export` for the held download (`server.py:1204`) and does not call `export_freshness`. T6 is therefore regression evidence for the held download only; no HTTP freshness surface exists or is demonstrated, and the #98 fix is evidenced by core tests T3 and T4 alone.
* Paired check: `paired_equity` has no production consumer; it is a test-only diagnostic over constructed fixtures, so the new dimension affects no ranking, queue or resident outcome.

### Requirement trace (document-qualified, proposed)

Classes: local observed (constructed synthetic), implemented but unverified, deferred, blocked, unknown. Requirement rows are nearest by inspection, not an authoritative mapping.

| Boundary or requirement | Source and test | Class |
| --- | --- | --- |
| PRD 0.21.0 FR-054 (versioned evaluation record with cohort definitions and subgroup results) and AC-073 (paired constructed cohorts differing in sensor/source completeness, contact need or appointment history; AC-073 is `Not run` in the PRD); the 'missing data never lowers priority' rule is the repository check's own pair rule and #128 criterion; #128 | `paired_equity.py` `DIMENSIONS`, T1, T2 | Local observed for the constructed source pair and exclusion path only. Population fairness, approved expected-outcome manifest, AI-task evaluation, small-sample handling and human disparity disposition are not evidenced; `fairness_evidence` and `activation_allowed` stay false. BRD 0.21.0 NFR-008, NFR-009 and RULE-005 (cited by #128) unverified. #128 criteria unmet |
| PRD 0.21.0 FR-043 and AC-051 (exact stale propagation; AC-051 is `Not run` in the PRD); FR-042 (export is not submission); #98 | `form_export.py` `export_freshness`, `_issues_by_field`, T3, T4 | Local observed for open-issue changes on a saved held pack in SQLite fixtures. The fixture-owned exact-affected manifest of AC-051 is not claimed. Held status, no submission, Finance human review and the manual route are unchanged by the diff. #98 criteria 2 and 3 stay unproven |
| ADR 0002 (Proposed) Audit row of its decision table (append-only SQL ledger, digests to an immutable Blob container with a time-based retention lock, scheduled verification; the row states it meets PRD DH-007, which concerns retaining audit entries in full for the legal period); not a numbered decision; #115 | `digest_blob.py` `main`, `_publish_and_verify`, T5, T7 | Local observed for marker emission, exit codes and the static alert binding with fake stores. Retention lock, immutable container, real scheduler run, hosted alert delivery and second-person reconciliation are implemented-unverified or unknown; #115 criteria unmet |
| Human, consent and AI-unavailable boundaries | Unchanged by the diff | The diff adds no permission, consent, approval, send or AI call path. Fixture providers, approvals and users are synthetic. A failed ledger check alerts and exits non-zero; it never degrades silently to success |
| ADR 0003 and ADR 0006 (Accepted) | No change | Context only |
| #440, #128, #98, #115 acceptance criteria | Unchanged | All OPEN and unmet or partially delivered |

### Findings, owners and risks (reported, no issue created)

No refactoring is confirmed necessary and no new defect was found by the checks run. Remaining risks, each routed to an existing owner:

* R1 (#115, residual from the feature review, not re-tested): `SystemExit` from SQL configuration bypasses the marker, and tracebacks are no longer printed for unexpected errors, which can reduce operator diagnosis. Whether the candidate absence alert (`OK_MARKER` missing) covers a `SystemExit` was not run and is unknown.
* R2 (#115, Low, theoretical): a `DocumentStoreError` raised while opening the store would print its message. No store module raises it today.
* R3 (#128): a ranker that excludes only the reference passes the paired rule; confirmed by the original reviewer as a stated-rule note, owner #128.
* R4 (#98): the freshness fix has no HTTP or browser surface; a user-visible stale indicator for held packs, if required, belongs to the existing #98 and #134 work and is unverified.
* R5 (omission): no hosted CI result for this head, no SQL Server run (the #98 and form tests ran on SQLite), no browser, scanner or Docker run, and the independent exact-head review of this record is outstanding.

### Gates and recommendation (proposed, not a decision)

* Recommendation: CONTINUE, bounded. The wave is locally consistent at `e155c88ed`; no fix or pivot is indicated by this evidence. It is not a tick of any criterion, an approval of any requirement, BRD, PRD or ADR, or an acceptance of PRs 1481, 1482 or 1483.
* Affected gates: closure of #128, #98 and #115 and whole #440 stay held (retention lock and hosted scheduler evidence for #115; AC-051 manifest and SQL Server evidence for #98; population or AI-task cohort evidence and human disparity disposition for #128). Dependent lanes: any use of the paired result as fairness evidence, any claim of an alerting ledger in a deployed environment, and any resident-facing stale-export behaviour. Independent lanes that this record does not block: unmerged source work on 107, 134, 153, 157, 435 and 82, and documentation work.
* Human decisions still open: owner appointment for the ledger alert, owner admission for any Azure, hosted or SQL lane, legal and professional acceptance of any resident-facing use.

### Process limits

* Original dated RPI evidence is under `.copilot-tracking/` (`post-fix-wave-440-1112`): research, plan and details, one independent read-only critique (verdict Revise, four findings, all applied; the critique worker could not write its file, so the coordinator persisted its findings), changes, state and one Review. The model label (Claude Sonnet 5.5) is asserted; no host attestation exists.
* The case study addendum was read by headings and relevant sections only, not end to end. No push, PR, issue, criterion or board write was made.
* Correction batch (2026-11-12, documentation only, after independent review RV2-1 to RV2-4 of frozen head `5244265c8`): qualified the pin identity at observation time, added the test-helper `PYTHONPATH` to T5 and T6, named the ADR 0002 Audit row accurately and stated that both AC-051 and AC-073 are `Not run` in the PRD. Original results, counts and adverse outcomes are unchanged and nothing was rerun.
* Evidence under `.copilot-tracking/` (`post-fix-wave-440-1112`, `post-fix-wave-440-1112-correction`).


## AI parent integration checkpoint (2026-11-12, Refs #104 #107 #157 #216)

Draft, local-only, not approved. A candidate integration of the AI parent (merged PR 1488 for #157 and PR 1489 for #107) with fresh main and one reviewed unmerged candidate (#216). It is not whole-issue acceptance, epic closure, a closing reference, a new issue, an approval or a hosted result. The prospective broad matrix and baseline inventory belong to the existing `parent-base-preflight-2300` task and are not repeated here.

### Identities (candidate and parent kept separate from merged main)

| Item | Identity (read 2026-11-12) |
| --- | --- |
| Merged main | `origin/main` `8e6e554570f4075ff41ea130e29511455f57df2d` (`src` tree `7b61d44bc705`). Merged, post-merge-of-PRs state; its delta over the parent base touches `src/core` `form_export.py`, its test and `src/core/README.md` only, outside the AI assistant, release, memory and citation code |
| Actual AI parent | `4459dadb4c751fcb4e1cc93d369ff844f2cbc9b7` (`src` tree `0b5ec0b6c344`), containing merged PR 1488 (#157) and PR 1489 (#107). Its `src` tree equals the merged tree validated in the 107 actual-parent run |
| Candidate 216 | `e4aac8b72802f583f19eabf88e14742f68f4f653` (`src` tree `ed460bbb673c`): one own commit after `eac1206c6` (already in main), test-only change to `src/api/tests/test_regulatory_chat_api.py` plus its dated original RPI files. Unmerged candidate, not main |
| Integrated local candidate | Source-validated commit `e056064136855b5ee9335c72d4e6a57b41ed80f2` (tree `9e206e8b5fc7`, `src` tree `4cf9398b44db`): the parent plus the plan and critique commit `0e03a176a`, a normal local merge of main, then a normal local merge of candidate 216. Source delta over main is exactly four test files (214 insertions, 1 deletion): `assistant_process_worker.py`, `test_assistant_release.py`, `test_assistants.py`, `test_regulatory_chat_api.py`. No production code changed. Later commits on the branch add only this record and its tracking files |

### Environment, commands and results (local, constructed synthetic data)

Python 3.12.3 venv outside the repository (`/tmp/v2333`), pip only, no uv. Tests and non-editable installs both came from one `git archive` of the validated commit: `pip install --require-hashes -r src/api/requirements.txt`, then `pip install --no-deps ./core ./agents ./api`. The three packages loaded from the venv `site-packages`, not the source trees. `PYTHONPATH` held only the canonical test-helper directories (`tests:../core/tests:../agents/tests`). `ZF_TEST_MSSQL` was explicitly unset for every run.

| Id | Command (from `src/api`) | Exit | Ran | Skipped | Covers |
| --- | --- | --- | --- | --- | --- |
| T1 | `unittest test_assistant_release.SqliteUnleasedRevocation -k changed -v` | 0 | 3 | 0 | #107 changed policy, prompt and permission process revoke, then a fresh process stays denied |
| T2 | `unittest test_assistants.ApiTests.test_active_chat_memory_is_never_evidence_for_a_chat_proposal -v` | 0 | 1 | 0 | #157 active chat memory cannot become proposal evidence |
| T3 | `unittest test_regulatory_chat_api -v` | 0 | 12 | 0 | #216 emitted citation and card links resolve to the cited content; forgery controls fail |
| T4 | `unittest test_assistant_release -v` | 0 | 60 | 7 | Whole canonical release module, including the 3 changed tests; the 7 skips are the `MssqlUnleasedRevocation` tests that need a disposable SQL Server |
| T5 | `ruff check` on the four touched files (ruff 0.17.1, the project pin) | 0 | not applicable | not applicable | Lint |
| T6 | `ruff format --check` on the project scope `tests` | 0 | not applicable | not applicable | 126 files already formatted. `test_assistant_release.py` and `test_assistants.py` are listed in the project `[tool.ruff.format] exclude`, so they were not format-checked; passing them explicitly would ignore that configuration and report a diff unrelated to this change |

All runs exited 0 with no failures. T1 is a subset of T4, so the distinct tests run were 73 (60 release including 7 skipped, 1 memory, 12 citation). Raw logs are outside the repository at `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/rpi-104-parent-integration-2333-evidence/`.

Adverse and intermediate results, retained: the first import-origin probe used a wrong module name (`api.server`) and failed with `ModuleNotFoundError`, then a second probe printed `None` for `__file__` because the packages are namespace packages; the origin was proved from `__path__` instead. The first ruff run from the `tests` directory explicitly named the format-excluded files and reported two files would be reformatted; that is a configuration artefact, resolved as the T6 note. Earlier results are preserved unchanged: the 107 actual-parent proof `rpi-107-current-parent-validation-2320-result.json` (60 release tests, 3 changed tests, 1 memory test, 7 MSSQL skips) and the original 107 independent assessment, which ran against the older parent `43b2187b9` with `PYTHONPATH` set to worktree source in a throwaway venv. That source-`PYTHONPATH` caveat applies to that earlier run; this checkpoint used installed distributions.

### Limits

* Not run: MSSQL or any SQL Server lane, old-image exclusion, broad or full gate, browser, mypy, scanners, hosted CI, provider or model calls, cloud, private data, spend.
* #107, #157 and #216 acceptance criteria stay unmet or human and live owned (for #216: owner thresholds, independent grader, staff paired trial, cost). No criterion is ticked and no approval is implied.
* No push, PR or merge was made. A later pull request would use `Refs` only. Hosted CI and human review for the exact head remain required.
* Original dated RPI evidence is under `.copilot-tracking/` (`ai-parent-integration-2333`): research, plan, details, one independent read-only critique (verdict Revise, five findings, all applied; the worker could not write its file so the coordinator persisted its findings), changes, state and one Review. The model label (Claude Sonnet 5.5) is asserted; no host attestation exists.

## Partial independent UX release affected-integration checkpoint (2026-11-13, Refs #149 #96 #216 #440)

Provisional, local-only, not approved. This is the affected-surface checkpoint of the bounded partial independent UX release of parent 149, prepared as a metadata record on the coherent integration topic `feat/demo-ux-partial-release-0117` (not a sibling pull request). It is not a final Review, not a Pass, not a finished RPI, not an independent exact-head assessment, not publication readiness and not a hosted result. The scope is established by the existing prospective partial plan `3862d97b3` and its executed critiques (the original plan critique and the amendment 0055 critique A55C-01 to A55C-04, all dispositions applied and not repeated). No new plan and no retrospective RPI is created here. Candidate policy stays candidate.

### Trigger, scope and pinned identities

Trigger: all eight actual final validation results for the integrated source at `288b6a376` exist, the original final parent Review has produced an actual result (consumed and adopted later, see the final evidence assembly below), and the C3 and main integration changed an affected surface beyond the earlier checkpoints.

| Item | Identity (read 2026-11-13) |
| --- | --- |
| Source head | `288b6a37665602718122ed0ab35b9bbdcca963ed`, `src` tree `6915b96c8ededf363b76c8fb4700153eb18ff588`. The source-frozen merge `b705b61f1` (M0 `d4f0c92fc` C3, M1 `b705b61f1` main) precedes the record commit `288b6a376`; this checkpoint adds only the pack section and `.copilot-tracking` records, so the `src` tree is unchanged |
| Main | `origin/main` `c401e5d56446b5752e8d91af6a45f3f06269c4bd`, fetched read-only at 01:19Z; equals the expected value, so no movement, no merge and no rebase. The only commit after the known `c5bfac6ee` (merged PR 1498) is the rubric score record |
| Module trees | `src/api` `0786923447a54a5bb2ac4e9ac7dd261f61522dca`, `src/core` `93de8839f422d3d502f7f6197bedaf68e45f12a7`, `src/agents` `ce54d120cc1c22177d7fd9f464cc89d39f92c2cb`, `src/orchestrator` `f29cc12760a42a3be2c3d0f854d42b2ce3ada666`, `src/importer` `887e665146ca1720dbb1074e79065bcd48c89810` |
| Covered children | UX parent `318465aae` including #82 and the funding correction (1490), 74, 176 (five-home replay), 215, 96 combined (backend `94760af7d` plus UI), C3 role-contract tests (`ec25487e2`, Refs #96), 156 docs, 134 documentation correction (`ca14b1523`), and the 216 law-link regression (test-only content and artifacts already on actual main via merge `e05606413` and squash `e44de171e`, PR 1495; not a child introduced by this branch, and the original child `e4aac8b72` is not an ancestor because of the squash; its test blob `65e4e683f800` equals the head blob; the integrated run proves coexistence only). Main-borne 1498 AI harness (`c5bfac6ee`, Refs #108) is covered as coexistence only |
| Exclusions | The entire 233 feature (`aebd381d9` and `837da4fde` are not ancestors; its symbols are absent) is excluded and held, neither admitted nor deferred. Original d790 and its adverse Review 0031 are not regraded. 108 and 203 adoption and the complete A2 cut line are not claimed |

### Documents at this head (blob and status as read)

| Document | Blob | Status as written |
| --- | --- | --- |
| `docs/brds/agentic-retrofit-programme-brd.md` | `34d88395de86` | version 0.21.0, `draft` |
| `docs/prds/zava-forward-retrofit-programme-demonstrator.md` | `c788b917bafa` | version 0.21.0, `in-review`; AC-001, 003, 011, 034, 037, 043, 050, 051, 054 and 066 read Not run |
| `docs/prds/proper-warm-retrofit-programme-demonstrator.md` | `f7f9b7675e60` | version 0.13.0, `in-review`; no input maps to it |
| `docs/adrs/0001-azure-architecture.md` | `d42fa5c4615f` | Proposed |
| `docs/adrs/0002-pilot-readiness-architecture.md` | `cbe21530043f` | Proposed as a whole; owner accepted only the bounded Entra-authoritative staff identity decision on 2026-10-24 |
| `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md` | `d60645397b20` | Accepted with amendment by the owner on 2026-10-15 (records an existing owner decision, not deployment, DPO or legal acceptance) |
| `docs/adrs/0004-per-user-agent-chat-and-memory.md` | `9406c2e747ce` | Accepted as written on 2026-10-15 (option C, staged); live personal data not activated |
| `docs/adrs/0005-regulatory-compliance-assistant.md` | `4d610335a5a1` | Accepted for synthetic development only on 2026-10-16; operational use unapproved |
| `docs/adrs/0006-src-layout-and-cutover.md` | `956da1a3b804` | Accepted 2026-10-15 |
| `docs/adrs/0007-contractor-intake-staff-mediated-proposal.md` | `541e0f72dd2c` | Proposed as a whole; synthetic-demonstrator owner direction reported, not formal acceptance |

All blobs equal `origin/main`. No requirement, ADR or BRD item is approved by this record. BRD identifiers below are nearest-by-inspection unless the BRD row itself names the work; none is owner-confirmed.

### Document-qualified traceability

| Input | Documents | Code | Tests, checks and journeys | Class |
| --- | --- | --- | --- | --- |
| UX parent incl. #82 funding gate and 1487 stale ordering | PRD FR-008 with AC-011, FR-001 with AC-001; BRD FR-008 (nearest) | core `store.py` `gate_reasons` explicit-True; `taskqueues.py` `MEMBERSHIP_REVISION` 3; strict readers in `home_case.py` and `chat_case_answers.py` | core 72 (REUSED); api `test_mvp.ApiTests` stale-advance and missing-funding cases and `test_home_case_api` (home 28, local-observed) | core REUSED and SQLite only; api local-observed |
| 74 home case isolation | PRD FR-002 with AC-001, AC-003; NFR-003 (nearest) | none (tests and browser check) | `test_home_case_api` over HTTP, core `HomeCaseTests` (REUSED), `home_case_browser_check` 24 PASS | local-observed, engineering only |
| 176 five-home cohort replay | no requirement asserted (owner-selected demo cohort); NFR-021 and AC-139 sizing context only | none (tests, runbook, synthetic-data README) | core `test_generated_dataset` five-home table parser and cohort reproduction inside synthetic 51 | local-observed; requirement anchor unknown, route through the #176 owner |
| 215 Refresh alerts keyboard focus | PRD FR-060 with AC-104 and AC-105 (nearest); ADR 0005 | `web/chat.js` focus restore | `regulatory_ux_check` `check_refresh_focus`, 21 browser states with pinned axe 4.10.3 | local-observed, engineering only; keyboard, AT and staff comprehension unobserved |
| 216 law-link regression | ADR 0005; no new requirement asserted | none (test-only) | `test_regulatory_chat_api` 12 tests including three link-resolution tests with forgery controls | local-observed on the integrated head, synthetic fixtures |
| 96 combined Held copy saved-check | PRD FR-042 with AC-050, AC-054; FR-043 with AC-051; BRD NFR-002 and AC-049 (interpretive join) | `server.py` freshness POST; `role-screens.js` saved-copy check | forms 74, role 21, `held_form_download_browser_check` 88 PASS | local-observed; numeric fidelity human decision and Finance review blocked |
| C3 role-contract tests (Refs #96) | same 96 rows | none (product source unchanged) | `test_role_screens` and `test_role_screens_conformance` 21, `role_screens_browser_check` 47 PASS | local-observed on the C3 head (coordinator assessment) and on this head |
| 156 IoT-to-UI source trace | PRD FR-050 with AC-066; BRD FR-048; ADR 0003 | none | none (documentation) | implemented-unverified (documentation) |
| 134 AC-034 to AC-043 correction | PRD AC-034 to AC-043 | none; `journey_acceptance.py` blob `e3466b6eafc0` equals main | register status only: 6 partial, 4 deferred, 0 passed | documentation register; criteria 1, 2 and 5 open |
| Main 1498 AI harness and core coexistence | none asserted | `ai_eval.py` (+277), `test_ai_eval.py` (+68), README | agents AI lane 28 tests and 11 scripted scenarios | local-observed, scripted offline only |

### Observed commands, environments and results

All lanes ran on a `git archive` export of exact `288b6a376` in a scratch directory outside the worktree (Python 3.12.3, pip only, editable installs of the project packages, no `PYTHONPATH` for source packages, helper test directories only where documented, isolated `HOME` and `ZF_DATA`, no Azure, provider or SQL credentials, no private data, no model or provider calls). The input worktree was clean before and after each lane. Raw results are outside the repository in the coordinator root as `rpi-149-final-{types,forms,home,roles,browser,synthetic,ai,trace}-0104-result.json` and `rpi-216-integrated-validation-0117-result.json`.

| Lane | Command (from the stated project) | Exit | Ran | Skipped | Notes |
| --- | --- | --- | --- | --- | --- |
| types | core and api `ruff check .`, `ruff format --check .`, `mypy` (ruff 0.17.1, mypy 2.4.0, configured exclusions and overrides unchanged) | 0 | mypy core 298 and api 236 source files; format 245 and 152 files | 0 | The three role-named api test files are inside the whole-tree scope |
| forms | `unittest -v test_form_held_download_api.HeldDownload test_form_staging_api.FormApi test_finance_grants_screens.FinanceGrantsScreens test_role_endpoint_inventory.RoleEndpointInventory` (`src/api`) | initial 1, rerun 0 | 74 (initial 53 ok, 21 errors) | 0 | Initial run failed only because the sanitized `PATH` omitted Node (21 `FinanceGrantsScreens` errors); one environment-only rerun with Node 24.21.0 on `PATH` passed 74 of 74 in 41.2 s. Both logs retained. The 35 logged law-store tracebacks are expected fault-path logs, not failures |
| home | `unittest -v test_home_case_api.HomeCaseApiTests test_programme_screen.ProgrammeScreen test_mvp.ApiTests` (`src/api`) | initial 1, rerun 0 | 28 (6, 16 and 6; initial 16 errors) | 0 | Same Node `PATH` cause, same single environment-only correction, 28 of 28 in 16.2 s. `ApiTests` is the six-method class, not the whole api suite. Stale-advance 400 and missing-funding 409 cases ran once each. Programme baseline only; no 233 feature |
| roles | `unittest -v tests.test_role_screens.RoleScreens tests.test_role_screens_conformance.RoleScreenConformance` (`src/api`) | 0 | 21 | 0 | Two strict negative-variant tests and three retained positives passed; discrimination inferred from them, no mutation run |
| browser | five existing checks: held 88 PASS, programme paging 89 PASS (baseline, not the excluded 233 count), home case 24 PASS, regulatory UX 21 states with 21 axe scans and no violations, role screens 47 PASS | 0 each | not applicable | 0 | Programme paging first failed on a runner invocation artefact (`__main__` has no `__file__`); original preserved, one rerun with the documented module invocation passed. Chromium 156 via Playwright 1.64.0, axe 4.10.3 verified by checksum. Engineering evidence, not AT or WCAG acceptance |
| synthetic | `unittest -v test_generated_dataset.GeneratedDatasetTests test_needs_inventory.NeedsInventoryTests test_scenario_manifest.ScenarioManifestTests test_determinism_audit.DeterminismAuditTests` (`src/core`) | 0 | 51 | 0 | Includes the 176 five-home replay. A negative case shows `all_available_pass` false because the private stock register is unavailable; constructed fictional stock only |
| ai | `unittest tests.test_ai_eval tests.test_eval_registry` and `python -m zava_forward.agents.ai_eval --json` (`src/agents`); scoped ruff, format check and mypy | 0 | 28 tests; 11 scripted scenarios, 0 critical misses | 0 | Registry 6 exercised scripted, 7 not evaluated of 13; provider scripted, actual model and human not evaluated. Format check 42 files and mypy 48 files with configured exclusions. Whole agents suite and the 28 main-only tests not run |
| 216 integrated | `unittest -v test_regulatory_chat_api` (`src/api`) | 0 | 12 | 0 | Distinct integrated validator, single pass, no correction, 16.8 s; the same 12-test count as the original 216 record; coexistence on the integrated head, not child introduction |
| core 72 | not run | not applicable | 72 (historical) | 0 | REUSED, see below |

Seven executed validation lanes (types, forms, home, roles, browser, synthetic, ai) plus the 216 integrated module all passed. Three diagnostics are environment-only and preserved: the forms and home Node `PATH` omissions and the programme paging invocation. None is a source defect and none consumed a correction allowance. A separate operational credential-handling note is held in private coordinator records; no value or detail is recorded here and it is not a source or test result.

### Core 72: reused observation, not freshly run

The 72 core tests (`test_gates`, `test_home_case`, `test_chat_case_answers`, `test_sqlqueues`, `test_taskqueues`) are labelled REUSED from the d790 observation (`rpi-149-core-validation-0025`: Python 3.12.3, editable core only, exit 0, 72 ok, 0 failures, 0 skips, 54.0 s). Reuse is supported because all three archived inputs of that run are identical at this head: `src/core` tree `93de8839f422`, `src/README.md` blob `b6e13012a836` and `README.md` blob `f47c6be00a06` (`git diff d790b6b45 HEAD` over those paths is empty, while the whole `src` tree differs and is not claimed identical). A static selector proof found all 72 test ids at this head, ten classes holding exactly 72 methods and no skip decorator. The actual SQLite membership regression (`test_non_boolean_funding_refreshes_stale_revision_two_memberships`) is in the 72. Mocked and static SQL Server portability tests are not an actual SQL Server run, which is not observed. No literal `MEMBERSHIP_REVISION == 3` assertion exists (indirect coverage only); that is recorded as an observation, not a claimed test gap.

### Archived-input equivalence per lane

Every lane exported exact `288b6a376`. This checkpoint changes only `docs/architecture/cutover-evidence-pack.md` and `.copilot-tracking`; no lane test or check reads those paths. Non-`src` files actually read by the lane tests are pinned and unchanged:

| Lane | Non-`src` inputs read | Blob or tree at head |
| --- | --- | --- |
| roles, browser (role screens) | `docs/reference/research/ux/design-system.md` | `e8b0caa87538` |
| synthetic | `docs/capstone/demo/runbook.md`; `docs/reference/research/retrofit-synthetic-data/`; the PRD above | `c131e41bd6e2`; tree `302891d728f1`; `c788b917bafa` |
| forms, home, ai, types, 216 | none found by search of the selected modules; the AI golden file resolves from the exported `src/agents/evals` | `src/agents/evals` tree `cfa3792a2aa5` |
| core 72 (reused) | `src/README.md`, `README.md` | `b6e13012a836`, `f47c6be00a06` |

The core test `test_live_doc_links` checks relative links in all live Markdown including this pack; it is not in any lane above and was not run. The new section uses no relative Markdown links, and a focused local link and diff review is the only check applied to this change.

### Original and adverse outcomes preserved

* d790 candidate and its original Review 0031: execution Partial, outcome not accepted for publication of affected UX (RV-001 open, mypy api, originating in 233 test code absent from this head). Immutable; not claimed resolved or inherited.
* Early static trace 0045: Partial, superseded for the final-source subset by trace 0104 (its stale browser set, head and ADR statuses are not copied). The 0104 trace's own stale pending-results statements are reconciled here against the actual completed results. The 134 section pin `43b2187b9` elsewhere in this pack is historical, not current main.
* C3 original three Low textual-guard limitations (L1 to L3) are retained; the earlier role failures at `9085e85c6` are history. C3 budget is 3 of 5 cycles spent with two left, not renewed by this record; older whole-96 history is unknown, not zero.
* 233: five correction cycles spent, the extension for a typing-only correction is unavailable and is NO approval. Whole 149, A2, the epic, manual acceptance testing, Finance, legal, live and actual SQL Server remain open and unproven.
* Original final parent Review `rpi-149-original-review-0104` (adopted as an immutable Partial original result in the final evidence assembly below): executed once, execution Partial, outcome conformant within the bounded partial source, test and check scope; no Critical, High or Medium finding; five Low observations (RV-L1 to RV-L5: duplicate status and field-error message, no focus move on the no-file error, 403 copy always names the Retrofit Programme Manager, retained textual-guard limits, bare `assert` in the five-home helper). It states it is not publication approval and accepts no criterion. When this checkpoint was first written it cited the Review only; the final evidence assembly below records its adoption as an original result, not an acceptance. The Review predates the 216 integrated result and records `main` as not freshly fetched; both are covered here.

### Boundaries, gaps, owners and resume conditions

* Consent, approval and AI boundaries: all data is constructed or synthetic. No resident consent, named human approval, owner acceptance or legal sign-off is recorded or implied. The AI evidence is a scripted offline harness; actual model behaviour, semantic accuracy and human review are not evaluated, and unavailable-AI paths stay manual.
* Open and unproven: whole 149, A2, epic closure, manual acceptance testing, Finance review and the numeric-fidelity decision, legal review, live checks, actual SQL Server, assistive technology and WCAG acceptance, and the complete local gate. Owners are the issue and criterion owners; nothing is delegated or ticked here.
* Unavailable or not run: a fresh core 72 run, whole api, core and agents suites, `test_live_doc_links`, the 233 programme feature checks, hosted CI (an absent, skipped or path-filtered workflow is not success) and the complete local gate.
* Hazard: historical commit `8307d2580` begins "Closed #83/#85/#90 are historical evidence"; publication needs a `Refs`-only pull request body and merge title and body with no closing keyword (even negated), empty closing references before and after any body edit, and #83 verified open afterwards. No pull request exists.
* Classification: focused-tier test, source-subset and documentation scope, with no workflow, manifest, Dockerfile, infrastructure, SQL, permission or gate-tool change against main; the Review and independent assessment must reassess it, and doubt takes the full tier.
* Proposal (not a decision): CONTINUE, bounded, only under the original Review adoption, the remaining validation above, metadata equivalence at the final head, an independent exact-head assessment and actual hosted gates. Affected closures stay held. No new issue, criterion tick, board edit, pivot or requirement relaxation is made.
* Not done: no push, pull request, merge, rebase, amend or issue action. Hosted CI and human review for the exact head remain required.
* Original dated RPI evidence is under `.copilot-tracking/` (`issue-149-independent-ux-0042` changes and state, the prospective plan `3862d97b3` and its critiques). The model label (Claude Sonnet 5.5) is asserted; no host attestation exists.

### Final evidence assembly (2026-11-13, metadata only)

Added after the checkpoint candidate `37e2715b5` and applied to the same `src` tree `6915b96c8ededf363b76c8fb4700153eb18ff588`. It assembles existing actual results and changes no source, test, tool, workflow, infrastructure, manifest or README file. It is not a new Review, not a Pass, not a fresh validation of the final head, not an independent exact-head assessment and not publication readiness. Main was fetched read-only and equals `c401e5d56446b5752e8d91af6a45f3f06269c4bd`; nothing moved.

| Item | Record (tracked under `.copilot-tracking/reviews/2026-11-13/`) |
| --- | --- |
| Original Review `rpi-149-original-review-0104` | Adopted as an immutable original result. Execution stays Partial and the outcome stays conformant within the bounded partial scope with five open Low observations. Tracked as a labelled PUBLIC TECHNICAL COPY, `issue-149-original-review-0104-public-technical-copy.md` and the matching result JSON. It is a derivative, not verbatim and not a newly executed Review. Only private operational handling text is omitted, each omission marked; no technical, adverse or validation text is removed. SHA256 of the privately retained original report is `ad5a288ac821f434833926eed5d09df131106e4ea19ba5d52bcb20e501e72128` |
| Provenance complements 0122 | `issue-149-provenance-core-0122-result.json` (74, 82, 176, 216 and parent lineage) and `issue-149-provenance-ux-0122-result.json` with its review (96, C3, 215, 134, 156 and public documentation). Each read its relevant child RPI bodies or public cells in full and is Partial by its own status, excluding the other's scope, raw pass logs read line by line and irrelevant history. No Critical, High or Medium finding. They do not make the original Review complete |
| Metadata input proof 0125 | `issue-149-metadata-inputs-0125-result.json`: binds `37e2715b5`; for every observed lane no actually-read source, configuration, helper, fixture or documentation input differs from `288b6a376`; three metadata files differ and no lane reads them. Not whole-archive equality. Core 72 is exactly three historic inputs, REUSED not fresh. Dynamic and transitive-read caveats remain |
| 216 integrated result | `issue-149-216-integrated-validation-0117-result.json`: 12 of 12, coexistence only (see the corrected 216 wording above) |
| Issue 153 input | The nine tracked 153 paths were read in full as input. Blobs equal at `c358dd675`, squash `8f8be74e1` (PR 1487, an ancestor of this head, not of main) and this head; `c358dd675` is not an ancestor. The independent Pass (`issue-149-153-independent-closure-1112.json`, with `issue-149-153-independent-final-1112.json` and `issue-149-153157-provenance-2228.json`) is per input and bound to `c358dd675` and target `43b2187b9`; it does not assess this head |
| Adoption record | `issue-149-partial-release-evidence-adoption-0131.md` |

Open and disclosed, none repaired here: the five Low observations of the original Review; the provenance Lows (commit history cannot prove prospective critique order for 74, 176, 216 and original 82, although the actual native phase logs show independent critic and reviewer launches, which is not tamper-proof attestation; byte-order-mark handling in `role-screens.js`; the unverified 176 as-of mutation; stale plan markers and a stale 0048 state marker; author-only original 96 backend records; the 134 ordering and amend-after-Review observations). The 74 adverse and mutation outputs M1 to M8 and A1 to A4 failed the intended assertions, A2 rejected a missing restriction key and is not a pure amount-only control, the first M8 run used invalid JavaScript and timed out at login (not a valid result) and the later M8 run failed the intended assertion; the final 74 browser check passed 24. Historical blockers in the 0048 and 0042 state files are superseded by the current 0042 state; the original critique and child state history are not rewritten.

Remaining gates, unchanged and not claimed: a final independent exact-head assessment that rechecks the new metadata paths against the input manifest, a clean final head and current main; current-main applicability; publication authority with `Refs`-only closing hygiene; and actual hosted checks for the exact head (an absent, skipped or path-filtered workflow is not success). Human, assistive-technology, Finance, legal, live, actual SQL Server, whole 149, A2 and epic evidence stay unproven, and no acceptance box is ticked. The entire 233 feature stays excluded and held, neither admitted nor deferred; its five spent cycles and the unavailable extension are no approval, and no deferral, requirement relaxation or pivot is approved. Original Review execution remains Partial; source conformance and documentation coverage are separate.
