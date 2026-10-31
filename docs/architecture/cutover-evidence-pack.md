---
title: Source cut-over evidence pack
description: Dated parity, private SQL and public edge proof with remaining owner gates
ms.date: 2026-10-31
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
