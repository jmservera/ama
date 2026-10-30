---
title: Employee redeploy execution evidence
description: Original blocked attempt, owner-admitted rollout failure and exact recovery evidence
ms.date: 2026-10-28
---

## Execution Boundary

* Task ID: employee-redeploy-20261028
* Scope: full plan attempted; only dependency-ready read-only backup permitted.
* Source: merged main `bb6df04cef68cc3694a97238d002c732c3406d81`.
* Branch: ops/employee-redeploy-20261028, initially clean; no existing PR.
* Plan: .copilot-tracking/plans/2026-10-28/employee-redeploy-plan.md
* Details: .copilot-tracking/details/2026-10-28/employee-redeploy-phase-details.md
* Research: .copilot-tracking/research/2026-10-28/employee-redeploy-research.md
* Original critique: .copilot-tracking/reviews/plans/2026-10-28/employee-redeploy-plan-critique.md
* Original status: Blocked before build, push or cloud mutation.
* Current status: one approved re-apply succeeded, Healthy/Provisioned/Running,
  active with100% traffic; evidence published in PR #518. Original failed
  verification, rollback, gate receipt and independent Review retained below.

## One-time re-apply approval (2026-10-28)

Owner explicitly approved "Yes, re-apply once using the image already in ACR".
Scope is P02 re-apply and P03 evidence publication, reusing completed P01 image
proof without rebuild or push. Verify the recorded manifest read-only; only if
necessary use the previously approved temporary ACR route, restoring exact
policy before the app update. Preserve all unrelated app settings, min0.
Roll back only for unhealthy revision or app startup errors, never solely a
verification-tool failure. CLI help checked: system logs are app-scoped with
no revision selector; console logs support revision/container selectors.
Initial read-only app GET returned503; no cloud mutation has occurred.

Owner explicitly directs publication without waiting for the full gate:
commit evidence, push this topic, open Refs-only PR disclosing matrix drift
and #517. Read-only PR check confirms #517 is OPEN, not yet merged; it proposes
the drift fix. No successful full gate, independent exact-head approval, hosted
approval or human acceptance will be claimed. Original Review is not repeated.
This explicit publication exception supersedes the earlier blocked handoff
only for this requested evidence PR, not the failed historical receipt.

### P01 reuse: read-only registry admission

Direct manifest CLI returned network-access denial. Fresh baseline matched the
historical recovery exactly. First approved temporary route was restored with
full policy equality after32.3seconds; manifest CLI still failed, so no employee
mutation occurred. External evidence:
`/tmp/ama-employee-reapply-20261028-43wi5y9g`.
Continue using the previously approved expose-token route with pull-only
manifest HEAD, credentials in process memory only, and the same exact-restoration
finally contract. No rebuild, image push, token printing or other resource change.

Read-only manifest HEAD succeeded HTTP200 via the approved in-memory token
route with pull-only scope. Docker-Content-Digest exactly matches the recorded
e6b6e7440c2b64577e96b6322c852bf630f1c5113608267132ebffc07d39fa19 digest.
Second exception restored exact full policy in17.7seconds; employee baseline
still exactly equals the historical rollback configuration/template/identity.
Fresh protected backup: `/tmp/ama-employee-reapply-20261028-1j8gt8xy`.
No image build/push or credential file was created. P02 now dependency-ready.

### P02 completed: one re-apply, positive startup and exact preservation

Exactly one `az containerapp update` executed, exit0, no retry or rollback.
Final readback at2026-10-28T11:01:59.974987Z:

| Setting | Final value |
|---|---|
| Active revision | `ca-cutover-test-demo-api--emp-reapply-20261028-110058` |
| Image | `crcutovertestrzsrg.azurecr.io/zava-forward-api@sha256:e6b6e7440c2b64577e96b6322c852bf630f1c5113608267132ebffc07d39fa19` |
| AI_ENDPOINT | `https://aif-cutover-test-rzsrg.openai.azure.com/` |
| AI_DEPLOYMENT | `standard` |
| AI_DEPLOYMENT_STRONG | `standard` |
| Health / provisioning / running | Healthy / Provisioned / Running |
| Active / traffic | true /100% |
| Replicas min / max |0 /4 |

Revision list/show and app latest/ready all agree. Full revision-set comparison
found exactly one added revision, the named re-apply. Entire configuration,
identity and normalized template equal fresh baseline except image, suffix and
the three authorized AI entries. All27 original env entries, secret references,
registries, auth, Single mode and scale preserved exactly.

Help checked before log queries. Supported system query omitted revision/
replica/container flags:21 app-scoped records,12 identify the new revision,
zero matched startup errors for that revision. Console query used supported
revision/container flags:3 records, one positive "Zava Forward is running",
zero startup-error matches. Raw logs withheld. Bounded pattern observations
do not establish exhaustive absence of errors or authenticated user acceptance.
Anonymous health200; app/ops.js/app.js401 as expected. No auth bypass or model
call. Prior synthetic HTTP/script-order proof (not bound to the deployed image by config digest, see the correction at the push record) is reused, not rerun
or misrepresented as authenticated live acceptance.

Final complete ACR policy equality passed: public Disabled, default Allow,
IP/VNet arrays empty, bypass None, exports disabled, admin false; all returned
policy fields unchanged. No other workload, roles, networking, costs, private
dataset, `.env`, secret-value or inference operation. No rollback trigger was
observed and no rollback was performed. Protected external evidence remains at
`/tmp/ama-employee-reapply-20261028-1j8gt8xy`, including fresh baselines,
manifest HEAD result, restoration equality, revision/app final readbacks,
preservation, probe/log summaries and result.json.

### P03 publication boundary for this continuation

Owner directs evidence commit/push/Refs-only PR without waiting for full gate.
The historical preflight failure `Workflow matrix drift: src-deploy.yml` and
original failed receipt are unchanged. #517 is OPEN and proposes the fix; no
claim that it has merged or that the current candidate passed the gate.
No new full gate, successful receipt verification, independent exact-head
assessment or hosted/human approval performed. Original independent Review
remains Complete / Not accepted at its original blocked-attempt boundary;
this later successful operational evidence does not rewrite that assessment.

Evidence commit87bd00bd used authenticated account-derived noreply identity
for author/committer and the requested Copilot trailer. Pushed only
`ops/employee-redeploy-20261028`; opened Refs-only PR #518 targeting main:
https://github.com/jmservera/ama/pull/518.
PR discloses actual validation, original failed gate, owner publication exception,
pending #517 and unperformed full-gate/independent/authenticated acceptance.
Local state/pointer/result consistency and evidence-only scope checks passed;
`git diff --check` passed. No runtime source changed; no new application tests
or full gate were run for this evidence-only continuation.

P01 reused, P02 verified successful, P03 evidence publication performed under
the explicit exception. Task implementation is complete; automatic session
remains running at Follow-up with no additional cloud operation authorized.
Original Review remains Not accepted; remaining separately scoped work is
authenticated acceptance and fresh full-gate/exact-head evidence after #517.
No merge or human/hosted approval performed. This final evidence update will be
committed and pushed on the same topic without rewriting existing history.

## Owner-selected continuation (2026-10-28)

The preceding blocked attempt and original independent Review are retained.
Owner explicitly selected implementation now, clearing the prior cost
dependency ("Proceed without cost query"), coordinating heavy-lock release,
and permitting failure-only Single-mode recovery using exact backed-up image
and env. No cost request will be retried. Actual headroom is still unknown.
Full plan is active from P01-T01; write boundary remains only named employee
app, existing ACR temporary exception, external backups and tracking files.
Validate local served script order, exact preservation, revision health,
bounded startup logs and policy equality. Full publication gate remains
mandatory. This is later implementation of routed findings, not a rewrite or
second critique/Review.

### P01-T01 completed: one build and served-image proof

Fresh protected backup:
`/tmp/ama-employee-redeploy-20261028-resumed.kbxpikmg`.
Previous revision/image unchanged from original attempt; safe app projection
hash still3193c65c51640a465e792ea4bc546f7d7f105dff1acaa1292c7934e330c6d8f6.
Fresh ACR hash aa91336c2b8222db6f6f5fa3c86ab5106a947a2bfb3e7a3e8e861d0aa2bf43cf;
full revisions hash c4154bc34aaedac5a6dd47764c2cc53ff948f0ef62055a8e0ccd81a66c40f865.

One `docker build -f src/api/Dockerfile -t <unique-tag> src`, exit0,
with `/tmp/ama-rpi-heavy.lock` acquired nonblocking and held through build.
Value recorded as the built image ID (it equals the pushed manifest digest, so it
is more likely the manifest digest than the Docker config ID; unverified):
`sha256:e6b6e7440c2b64577e96b6322c852bf630f1c5113608267132ebffc07d39fa19`.
Constructed empty cases/staff fixture, loopback-only random port and no
cloud credentials; actual HTTP `/healthz`, `/app`, `/ops.js`, `/app.js` all200.
Parsed served script tags: ops.js index2 before app.js index7.
Asset hashes d28b705ffa88f386cb1b23ca4db9be93dd09d2bcbc6ea2fee3a4f12d0e466cd3
and37aa87d572ffa6aa14cbf9e53dd9819425f38803d5c1318077566fe5f07460ee.
Exact owned proof container removed; backup restored to0700. Fixture remains
external for evidence. No cost query, push or cloud mutation in this step.

### P01-T02 completed: pushed digest and exact ACR restoration

Tag `emp-20261028-102834`, image
`crcutovertestrzsrg.azurecr.io/zava-forward-api@sha256:e6b6e7440c2b64577e96b6322c852bf630f1c5113608267132ebffc07d39fa19`.
Push digest, remote repository digest and local RepoDigest agree. The Docker
image ID identifies the image configuration, not the registry manifest, so the
tested image ID was not shown equal to the manifest digest; binding the
synthetic HTTP proof to the deployed image by config.digest is not recorded
(correction after review). Exact previous digest was independently found still in ACR; no
purge/delete/tag overwrite. Expose-token stayed in process memory/stdin;
temporary Docker config was removed, no token or secret value printed.

Exception began10:29:32Z and exact restoration confirmed10:30:17Z (45.8s).
First equality assertion failed: Azure stored the owned `/32` as bare
`4.225.218.160`, so remove with CIDR did not remove the returned rule.
Public access was already Disabled. Removed only the exact returned bare-IP
rule, then full ACR equality passed. No push/build retry or app mutation.
This immediately relevant CLI normalization correction preserves owner intent.
Restored policy: public Disabled, default Allow, IP/VNet arrays empty, bypass
None, exports disabled, admin false; all other returned policy fields equal.
Employee baseline equality also passed after cleanup. P02 now dependency-ready.

### P02 executed once: verification failure and successful rollback

One forward update created `ca-cutover-test-demo-api--emp-20261028-102834`
using pushed digest e6b6e7440c2b64577e96b6322c852bf630f1c5113608267132ebffc07d39fa19.
Positive platform health Healthy/Provisioned, latest/ready equality, exactly
one added forward revision and exact expected full configuration/template/
identity comparison all passed. Three requested AI entries were present.
Anonymous health200, app/ops.js/app.js401. No protected-asset bypass attempted.

Verification failed because `az containerapp logs show --type system` rejects
`--revision` (and replica/container selectors). Raw logs/credential/config
content were withheld. This is an operator invocation error, not demonstrated
startup failure. Per owner "if anything fails", no forward retry; rollback.

Initial failure-only REST recovery and diagnostic retries were rejected400:
GET template includes read-only `imageType` unsupported in that API request.
Those rejected patches created no revision. The supported CLI update then
restored the exact backed-up image and all original env with
`--replace-env-vars`, same container/min0, preserving other fields.
One recovery revision: `ca-cutover-test-demo-api--rollback-20261028-103137`.
Verified10:32:57Z Healthy/Provisioned/Running, latest=ready; full configuration,
identity and template equal original except required revision suffix.
Exact old digest:
`sha256:0769b52dddc5d6b350c74d6711ae53eda45d3e903ee27fac6b5a6c1d6b8b6e7e`.
Twenty-seven original env entries restored; AI entries absent. Registry,
Key Vault references, identity, min0/max4 and Single mode preserved.

Corrected bounded read-only logs: system command without revision selector,
31entries/no startup-error matches (app-scoped, not falsely revision-scoped);
rollback-specific console3entries, positive "Zava Forward is running",
zero startup-error matches. Rollback health200, protected app/JS401.
Final complete ACR equality passed. No other workload/role/network/resource
change, cost query, secret-value read or paid inference.

Desired AI-enabled outcome NOT achieved. No further rollout is authorized by
this one-redeploy request. Backup/recovery evidence retained externally.
Original independent Review remains Complete / Not accepted, not re-executed
or upgraded; this later implementation reports actual recovery evidence only.

### P03-T02: committed candidate and current-main integration

Evidence committed as a05bae82608572045861b06be9bba27027ce01bd with
authenticated account-derived noreply author/committer and requested trailer.
The required fetch advanced main from bb6df04c to197e5e3c (#513).
Complete-gate invocation with current main was BLOCKED before groups/receipt:
"Candidate does not descend from the reviewed main base". No passing or failed
group receipt exists for that rejected admission.

Read-only comparison proves main added exactly one line to
`.github/workflows/infra-plan.yml`, no app/source change. Both src trees:
`00d32ea390508692cb0fd308e45aac0d8288da94`.
Reconcile this current-main CI-only change by a normal non-rewriting merge
into the requested topic, preserving original evidence/ancestry and exact
built source. No rebase, force-push, main write or additional cloud operation.
Then run the required complete gate in a fresh external directory.

### P03-T02 final: full gate failed; publication blocked

Non-rewriting topic merge323b3adfaac8b6f55c5972397f0b421f97eeec4a integrated
current main197e5e3c6d4f7cfb135c9a985af3f13e0f688ac4; no source/runtime change.
Complete command:
`python3 tools/rpi-checks.py --all --jobs 3 --lock-timeout 0 --base
197e5e3c6d4f7cfb135c9a985af3f13e0f688ac4 --out
/tmp/ama-employee-redeploy-full-gate-20261028-1038`.
Heavy lock acquired immediately; effective jobs2; full matrix selected.
Required preflight failed `Workflow matrix drift: src-deploy.yml`, exit1.
No group passed; original failed receipt retained externally at
`/tmp/ama-employee-redeploy-full-gate-20261028-1038/receipt.json`.
No retry/resume/skip/cloud fallback or unrelated workflow fix. No successful
receipt verification or independent exact-head publication assessment.
No push or PR: repository publication gate is not bypassed by owner authority
for one cloud operation. Final adverse-evidence commit does not validate or
upgrade this historical failed candidate receipt.

Task remains Blocked in Implement, automatic session running, original Review
Complete / Not accepted unchanged. Desired AI outcome rolled back; exact old
configuration healthy and ACR restored. P01/P02 executed, P03-T01 historical
Review retained, P03-T02 commit complete but gate/publication unmet.
Owned proof container/auth config removed and exact constructed fixture file
and empty directories removed; backups/receipts retained. No private-data,
secret-value, .env, resident, role, resource or cost-query operation.

## Original attempt (historical, retained unchanged below)

The following sections retain the earlier blocked attempt. Current results
and owner dispositions are recorded above; do not treat historical no-write
statements as the terminal state of the continuation.

## P01-T01: Safe preservation

Backup complete, directory `/tmp/ama-employee-redeploy-20261028.nbVE6l`
(0700), JSON files0600, not committed. App safe projection retains complete
configuration/template/identity and exact existing image/env/registry/scale;
secret definitions contain only name/keyVaultUrl/identity, never values.
No `.env`, private data, secret values or listSecrets requested. Existing
noncredential configuration is captured externally, never committed.

| File | SHA256 |
|---|---|
| app-before.json | 3193c65c51640a465e792ea4bc546f7d7f105dff1acaa1292c7934e330c6d8f6 |
| revisions-before.json | 3bd9f22fadbf627dca44bbe6dbeba1c9b716680f434a81f1298441c186de61ec |
| acr-before.json | 9e76914c9b68fdbb2ab90bc3f87f171e961568301b53c582b450694090d720d3 |

Fresh independent GETs saved as app-after.json/acr-after.json and semantic
equality assertions passed, exit0; verification.json records sanitized results.
Old revision `ca-cutover-test-demo-api--0000006`; image
`crcutovertestrzsrg.azurecr.io/zava-forward-api@sha256:0769b52dddc5d6b350c74d6711ae53eda45d3e903ee27fac6b5a6c1d6b8b6e7e`.
Twenty-seven original env entries, one Key Vault reference, user-assigned
identity/registry selection, min0/max4 and Single mode all unchanged. Three AI
entries remain absent. No new revision or digest exists.

## P01-T01/P01-T02: Admission and cost failures

* `lslocks --noheadings --output PID,COMMAND,PATH` observed PID3869238,
  `python3`, holding `/tmp/ama-rpi-heavy.lock`; no wait/poll/interruption.
  Build NOT RUN, no image created or pushed.
* Read-only subscription ActualCost MonthToDate query API2025-03-01 failed429
  TooManyRequests, exit1. One alternative API2023-11-01 explicit
  2026-10-01..2026-10-28 query failed Unauthorized/RBACAccessDenied, exit1.
  No roles, logout/login or shared session changes. Required headroom remains
  unknown. No cloud writes or registry exception permitted.
* Original critique PC-001 also requires supported Single-mode rollback while
  preserving mode/traffic without another revision. Official docs consulted
  read-only; no compliant route established and no mode exception inferred.
* PC-002/004/005 corrections define positive readiness evidence, actual
  synthetic HTTP proof and concrete registry timeout/restoration bounds if a
  later separately admitted attempt proceeds. None was run or claimed here.

## P02: No rollout or rollback

No `az containerapp update`, revision activation/restart/mode/traffic mutation,
ACR update/rule/login, token request, Docker login/push or inference occurred.
No new revision/digest exists. Previous revision remains the rollback baseline.
No recovery action is necessary because no cloud mutation was attempted.
ACR final policy equals baseline: public Disabled, default Allow, IP/VNet
arrays empty, bypass None, exports disabled, admin false. It was never opened;
"unchanged" is the correct result, not a claimed restoration operation.

## Validation and Remaining Work

* Exact three AI values verified in runbook, #515 body, Bicep and model GET.
* Existing app/template/identity/registry/secret-reference/scale and ACR policy
  backup and full semantic equality verified, exit0.
* Local image/assets, new-revision health/startup/log checks NOT RUN:
  no new image/revision exists. Do not equate old revision health with redeploy.
* Full local publication gate NOT RUN / Blocked; foreign heavy-lock ownership
  prohibits queueing or polling/re-admission without a later coordination
  event. No passing receipt exists; no inherited exception from #515.
* Human/live/inference acceptance remains unchecked.

## Amendments, Divergences and Handoff

Immediately relevant current-state updates: actual foreign heavy-lock ownership
and denied financial evidence block affected dependent work. Conservative
critique corrections applied; original Revise verdict preserved, no repeat.
Implementation cannot satisfy full plan. Independent Review assessed the full
request against actual read-only/blocked execution, not deployment success.

## Pre-Review Reconciliation

* P01-T01 partial (backup complete, build blocked); P01/P01-T02 and
  P02/P02-T01/P02-T02 unmet, no runtime acceptance.
* P03-T01 complete: original independent Review Complete / Not accepted.
  P03-T02 local evidence commit authorized, full publication remains blocked.
  No completed runtime phase marker invented.
* Plan/details/state/changes agree on actual no-write boundary and blockers.
* Review readiness: ready only for independent assessment of blocked outcome,
  not conformant successful implementation or deployment acceptance.

## Independent Review and Publication Disposition

Original Review:
.copilot-tracking/reviews/logs/2026-10-28/employee-redeploy-review.md.
Execution Complete; outcome Not accepted. Three High, one Medium and one Low:
recovery to planning, financial evidence to research, unexecuted redeploy/
publication to later implementation, authenticated acceptance to distinct owner
follow-up. No findings closed by reimplementation or a repeated Review.
Review did not inspect external backup bytes due its own host boundary; parent
direct equality results above are retained as execution evidence, not upgraded
to independent Azure attestation.

RPI assessment finished, requested deployment still blocked. Automatic session
remains running at Follow-up with ranked evidence-grounded work in state.
Only the expressly requested local evidence commit is permitted now.
Full gate NOT RUN / Blocked, no verified receipt; no push or PR. This is not a
local-gate failure receipt, deployment success or authorized gate exception.
No new revision/digest, hosted checks, authenticated assets or runtime logs
exist for this attempt; original employee and ACR configurations are unchanged.

## Evidence durability note (2026-10-28)

The `/tmp` receipts and backups cited above are host-local and not durable. The
original failed receipt is not retained in an approved artifact store; the
summaries in this record are the only durable account. Preserving the originals
needs an owner-approved access-controlled location and is not done here.
