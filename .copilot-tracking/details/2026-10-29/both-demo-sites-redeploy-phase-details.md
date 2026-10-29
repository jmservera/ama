---
title: Both demo sites redeployment phase details
description: Exact build, preservation, registry and startup verification boundaries
ms.date: 2026-10-29
---

## Metadata

Task ID3897222c-2d62-4e25-a059-eecfbdce51d0; slug both-demo-sites-redeploy.
Plan .copilot-tracking/plans/2026-10-29/both-demo-sites-redeploy-plan.md.
Research .copilot-tracking/research/2026-10-29/both-demo-sites-redeploy-research.md.
Status: Implementation Partial, original Review Complete / Not accepted. Employee
main deployment and resident old-image recovery verified; resident latest main unmet.
One original critique Complete / Revise preserved, five findings disposed in plan.
Local evidence handoff complete; original evidence commit59049aa80de14972c717e1d31a27309b984e7c7c
verified with privacy-safe author/committer and requested Copilot trailer.
No push or publication gate pass. Final parent handoff status is committed separately.

## Frozen Execution Contracts

* PC-001: Each registry exception starts a monotonic600s deadline at first policy
  mutation. Every operation uses min(per-call bound, remaining time);60s policy,
  token/login/manifest,420s push,20s HTTP. Reserve180s of the600s for private-first
  restoration, so forward operations stop at420s. Restoration has its own180s
  absolute bound, including120s maximum equality readback; public disable is the
  first action even on timeout/interruption. subprocess timeouts terminate only
  the owned child; handled SIGINT/SIGTERM become exceptions and finally runs.
  Remove exact owned Docker credential file/empty config directory in finally.
  Unconfirmed policy restoration blocks all app writes and is explicit recovery
  escalation, not success. Record actual opening/closure/duration and cleanup.
* PC-002: Canonical JSON uses sorted mapping keys and preserves array order and
  null/absent distinctions. Compare the entire app response except top-level
  systemData and properties.{latestRevisionName,latestReadyRevisionName,
  latestRevisionFqdn,provisioningState,runningStatus}. Protect every other field,
  including complete configuration, customDomainVerificationId, identities,
  environment IDs, eventStreamEndpoint, outbound IPs, tags and complete template.
  Forward expected template differs only at revisionSuffix and containers[0].image.
  Pre-write comparison uses the unmodified baseline template. Separate auth
  show must be exactly equal. The excluded revision pointers must explicitly
  equal the requested suffix and expected revision FQDN; provisioning must be
  Succeeded and target revision Healthy/Provisioned/active with100% traffic.
  Top systemData is observational audit metadata, not ignored app configuration.
  For ACR compare the entire show response except top systemData,
  provisioningState and status; every policy field and network setting remains
  protected. No policy timestamp is excluded. Comparator source hash and exact
  exclusions appear in sanitized receipts, with zero unexpected changed paths.
* PC-003: Push output digest = exact remote manifest Docker-Content-Digest =
  local pushed RepoDigest. Separately selected platform manifest.config.digest
  must equal actual local config digest with the pinned-main source label.
  If an OCI index appears, select linux/amd64, verify its manifest digest and
  compare that config to local config, recording both index/platform digests.
  Never equate config and manifest digests. Execution correction: Docker29/containerd image store
  image inspect Id is an OCI index digest. Get actual local config via docker
  save manifest.json Config entry, hash its bytes and verify source label.
  Compare remote platform config.digest to that actual local config digest,
  while preserving image Id/index separately. This corrects tooling semantics,
  not source, registry policy or deployment scope.
* PC-004: Each app must complete preservation, new-revision accounting, positive
  startup/ready replica, health and public-route checks before the next app
  update. Actual unhealthy/provisioning-failed/startup-error evidence permits
  one image-only rollback, not forward retry; recovery has600s convergence and
  the identical comparator, auth, revision accounting, latest/ready/active/
  traffic and health/startup checks, expecting old digest. An ambiguous recovery
  is inspected read-only, not retried. Terminal states: succeeded;
  recovered-but-redeploy-failed; recovery-unverified; or verification-blocked
  for tooling-only failures. A successful other app is never reverted.
* PC-005: curl GET has connect timeout15s, total90s, no cookies/credentials or -L.
  Employee /healthz200; /200 equals main public welcome.html; /app, /app.js and /ops.js must be401 or a30x sign-in
  redirect (no redirect follow). Resident /healthz200 and /200. Resident public
  response must equal the main-built static index.html bytes, contain "Sign in
  to the showcase", "Synthetic showcase" and password input, and contain no
  embedded application/json script or interpolated case payload beyond the
  known static shell. Exact static-byte equality is the bounded no-rendered-
  case-content predicate, not an exhaustive leakage/security assessment.
  Persist only statuses, booleans and public asset SHA256, not response bodies.

## Execution-Time Tooling Corrections (2026-10-29)

Employee forward rollout was Healthy/Provisioned/Running, active100%, with
exact full app/auth preservation and health200. Verification nevertheless
failed two unsupported assumptions, without runtime failure or rollback.
The source server.py:239-246 deliberately serves public welcome.html at /;
correct root assertion is200 and byte equality with main welcome.html plus
sign-in link. /app, /app.js and /ops.js still require401/redirect. This does
not loosen any authentication setting or bypass the protected app.

Revision GET and app GET have different representations: revision template
has null revisionSuffix and omits app-populated imageType, resources.
ephemeralStorage, customMetricsSettings(null), scale.cooldownPeriod and
scale.pollingInterval (the last two returned explicitly null). For cross-resource template comparison only, accept
these explicit absent/null representation differences; all revision container
image/env/secretref/resources/probes and remaining fields must equal app.
The complete app-to-baseline comparator remains unchanged and protects all
these fields exactly. Record these representation paths and zero remaining
differences. Requested suffix is separately proven by exact revision name and
app suffix/latest/ready/FQDN checks. Continue read-only verification of the
existing revision, never issue a second update for these tooling mismatches.

Installed revision list --help confirms default lists active revisions only.
Initial private backups preserved that active list, not all inactive history.
Use --all for all subsequent inventories. Before resident mutation capture its
full history directly. For already-updated employee, retain original backup
and explicitly reconstruct the historical set from retained --all entries with
createdTime before the saved update-intent timestamp; assert exactly the named
new revision was created after that timestamp and the original active revision
remains retained/inactive. This is retrospective history evidence, not a claim
that a complete before inventory was captured prospectively. No revision
deletion or activation is authorized.

For min0 activation, issue an anonymous /healthz curl while waiting for runtime
health rather than waiting indefinitely for metadata first. Resident activation
had Provisioned/Activating/health None until the authorized public health request
returned200. This is a request-driven cold-start wake, not scale/config mutation.

Resident failure recovery discovery: installed image-only CLI added value=""
to both secretRef env records (originally value absent). This is a real
preservation failure, not an accepted null/empty normalization. Recovery may
restore these exact own-update paths in addition to old image; refuse any
other protected drift. Use one ARM PATCH with full original writable template,
old image and new recovery suffix, avoiding CLI env serialization. Remove only
request read-only imageType and derived resources.ephemeralStorage; final
GET must equal complete original app template except suffix. Platform-generated
revision probes must equal original ready revision probes exactly if absent
in configured app template. No new forward retry or scope expansion is approved.

Recovery execution: first raw PATCH was definitively rejected and created no
revision. Raw GET at the same2025-07-01 API proved customMetricsSettings(null)
is another CLI-only field, absent in raw API schema. Removing it from the
request yielded one successful PATCH and one recovery revision, with zero
final protected-field differences. Original rejected request receipt retained.
Owned convergence loops were stopped only after confirming they were read-only
and ARM provisioning was terminal; no ambiguous mutation was retried.

Final07:43Z: employee emp-main-20261029-072248 on new index41db9468...,
resident rollback-20261029-073718 on old fab6a853...; latest=ready and only active
revision each, full auth/config/template preservation, min0/max4 and0/max1.
Resident added exactly one forward and one failure-only rollback, no deletion.
ACR final full protected projection equals original. Implementation is Partial,
not two-site main acceptance. Original resident target startup console could
not be retrieved after replicas disappeared; do not claim a precise SQL or
secret-resolution root cause from the available runtime evidence.

<!-- rpi:phase id=P01 -->
## P01: Preserve and build

<!-- rpi:task id=P01-T01 -->
### P01-T01: Baselines and builds

Capture full az containerapp show, revision list and auth show for both named
apps and full az acr show externally under0700/0600. These management reads
return secret references, not secret values; no listSecrets or vault data read.
Reject secret definitions with values before using backups. Never print raw
backups. Record canonical hashes, env/secretref counts, old revision and image.
Require expected subscription/group/environment and min0, one container each.
Export tracked src/ only from d70ee60ab3d7346a9991cf64382d9985f4d09f2e using git
archive into an owned external build directory. No .env/untracked upload.
Record src tree6684959daaa64df7f8768c4fddb24406f198a308. Acquire shared heavy
lock nonblocking. Build employee and resident sequentially with labels identifying
exact source SHA and unique repository tags. Capture build output privately;
only status/image IDs/hashes become evidence. Failure prevents dependent push.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Approved ACR push

Expected baseline public Disabled/default Allow/no IP or VNet rules/bypass
None/export disabled/admin false. Re-read and compare full stable ACR projection.
Determine current VM egress IPv4, validate; add its /32 while public Disabled,
enable exports, then enable public with default Deny. Capture expose-token in
memory only, use Docker --password-stdin with owned temporary0700 config.
Unique new tags only. No overwrite or deletion. GET exact old manifests with
in-memory pull scope and verify Docker-Content-Digest/body hash; verify new push
digest against remote manifest and local RepoDigest, then separately config.digest.

Private-first finally: disable public, remove only newly added returned IP
(Azure normalizes /32 to bare IPv4), restore default action/exports to exact
baseline. Never change bypass/admin/other policies. Compare all fields using
the exact Frozen Execution Contract exclusions, including all policies,
network settings, registry identity and policy timestamps.
Credential file cleanup removes only exact owned config.json and empty owned
directory, not broad directories or images. If cleanup/equality fails, block all
app updates and report explicit recovery status. ACR route closes between pushes
if needed to keep each exception within600s.

<!-- rpi:phase id=P02 -->
## P02: Refresh and verify both apps

<!-- rpi:task id=P02-T01 -->
### P02-T01: Employee

Baseline expected revision ca-cutover-test-demo-api--emp-reapply-20261028-110058,
digest sha256:e6b6e7440c2b64577e96b6322c852bf630f1c5113608267132ebffc07d39fa19,
container api, min0/max4. Preserve every existing AI and other env value exactly.
Compare current app/auth to backup, invoke exactly one az containerapp update
with --container-name api --image <new-digest> --revision-suffix <unique> -o none.
No env, scale, identity or ingress flags. Wait with read-only revision show/list,
not repeated updates. New revision latest=ready, active, healthy/provisioned.
Curl /healthz200; /, /app, /app.js and /ops.js anonymous statuses only,
no login/cookies/model endpoint.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Resident

Baseline expected ca-resident-demo--0000003,
sha256:fab6a85318f65db006bc610f3b3aff8ae799046d1b9a1813662b3b315c1b6fc7,
container resident-demo, min0/max1, expiry2026-12-31T23:59:00Z.
Preserve current ingress and all MI/SQL/AI/secretref configuration without
printing or interpreting secret values. Same image/suffix-only update and
revision assertions. Curl /healthz and public /; no credential access or
authenticated requests, no assistant POST.

<!-- rpi:task id=P02-T03 -->
### P02-T03: Final proof and recovery disposition

Check CLI help before logs; system app-scoped --type system --tail100 with no
revision/container selectors. Console --type console --revision <new-name>
--container <container> --tail100. Parse logs in memory; persist only counts,
safe reasons and bounded startup/error classifications, never raw case/request
or credential text. Require positive target startup or ready-replica evidence
plus health200; empty errors alone do not prove readiness. Record scope of
system events and any unavailable console stream as explicit limitations.
HTTP requests can wake min0 but never change minimum.

Compare exact configuration and identity; full template except image/suffix;
full stable app fields and separate auth configuration; exactly one new revision;
new revision image/template matches expected and active traffic100 in Single
mode. Final ACR equality and both apps rechecked. If actual runtime failure,
restore only that app's old image; no rollback for command syntax/transport
failure alone. Record unhealthy/error evidence before any rollback.

<!-- rpi:phase id=P03 -->
## P03: Independent Review and local handoff

<!-- rpi:task id=P03-T01 -->
### P03-T01: Review

Activate rpi-review once after implementation reconciliation, with plan/details,
critique and changes pointers and sanitized receipts. Review must distinguish
exact backed-up equality from authenticated user acceptance and local evidence
from publication gates. Preserve original findings and route them later, no
same-task second Review or review-driven redeployment.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Local commit

Use existing verified privacy-safe repo-local identity matching earlier evidence
because explicit owner says no gh. Do not query gh or change global config.
Record exact deviation from normal fresh gh account resolution. Commit only
the task's named tracking evidence with mandated Co-authored-by trailer.
No push, PR or complete publication-gate claim. git diff --check and JSON/pointer
consistency checks apply. Final status and remaining owner/coordinator gates
must agree across plan/details/changes/state.
