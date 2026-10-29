---
title: Both Azure demo sites redeployment changes
description: Owner-authorized image-only refresh from exact current main
ms.date: 2026-10-29
---

## Execution Boundary

* Task ID: 3897222c-2d62-4e25-a059-eecfbdce51d0; slug both-demo-sites-redeploy.
* Declared scope: full plan, research -> plan -> implement -> review.
* Source: fetched main d70ee60ab3d7346a9991cf64382d9985f4d09f2e,
  src tree6684959daaa64df7f8768c4fddb24406f198a308.
* Branch: ops/sites-redeploy-20261029, clean at intake, exactly at main.
* Plan: .copilot-tracking/plans/2026-10-29/both-demo-sites-redeploy-plan.md.
* Details: .copilot-tracking/details/2026-10-29/both-demo-sites-redeploy-phase-details.md.
* Original critique: Complete / Revise, five compatible corrections applied;
  original artifact retained, no second critique.
* Current status: RPI lifecycle and local evidence handoff complete; implementation Partial, original independent Review Complete / Not accepted.

## Authorized Route and Constraints

Use the prior successful local Docker build plus VM-only ACR expose-token push
route, explicitly permitted as the approved-route alternative. No remote ACR
build success is claimed. Preserve exact policies and all app settings except
image/revision suffix. No cost query; billing/headroom unknown.
No gh, push, SQL, roles, other apps, private dataset, .env, secret-value reads,
model calls or registry image/tag deletion. Full private backups stay external;
only sanitized evidence is committed.

## P01-T01: Backup and Clean Builds

Complete. Full management GETs captured for each app, auth configuration and
revision list, plus ACR. Backup root:
/home/azureuser/.copilot/session-state/3897222c-2d62-4e25-a059-eecfbdce51d0/files/redeploy-20261029/
(0700, private files0600). No secret-value/listSecrets request.
Backups contain current reference metadata, not resolved secrets.

Tracked src/ exported using git archive from exact main, no untracked/ignored
working inputs. Both local Docker builds succeeded under nonblocking shared
heavy lock, with exact source-revision labels and correct Dockerfiles/src context.

| App | Built Docker image ID (OCI index, see correction below) | Env entries | Env secretrefs | Secret definitions | Min/max |
| --- | --- | --- | --- | --- | --- |
| Employee | sha256:41db94689ae934e3daa6c7f8fb57d8de5cc58a53995efd50217189231ac1f0c1 | 30 | 0 | 1 | 0/4 |
| Resident | sha256:1c0881a9855ce7ffcaad26da06422a7c7be7d9cf536073ec9c5d955889882354 | 10 | 2 | 2 | 0/1 |

Baseline app projection SHA256 employee4410295198c76a92b1aac5e3a759d8e825f75f064eb33585be3269ad95a254e1;
resident099d344e70738bfeccf310b0faab9bdf9a9d42855ed93f9e7e7a5ceb2f2fc760.
ACR projection6c90667eb84b9a98b3b62997e25aee07c805f4c75bdee586176a25a423fa0fba.
Private build logs retained; no build secrets or private datasets supplied.

## P01-T02: Registry Proof and Exact Restoration

Employee push succeeded, but its post-push proof failed before any app update:
Docker29's containerd store returns an OCI index digest as image inspect Id,
not the config digest assumed by the recipe. This is a tooling/identifier
failure, not startup failure. No rollback or new revision occurred.
Private-first exact ACR restoration passed in21.7s and credential config was
removed; original failed receipt retained.

Immediately relevant correction: inspect local docker-save manifest.json and
hash its exact Config bytes, separately from image Id/index. Verify remote
platform manifest.config.digest against that local config hash, plus source
label. Employee continuation is read-only manifest admission using the same
approved temporary route, not a rebuild or re-push. Resident push remains pending.

Continuation complete: employee read-only admission and resident push both
succeeded. Old manifests verified present before/after. Remote OCI index,
selected linux/amd64 manifest and actual local config are separately bound;
source labels equal main. No tag/image deletion or old-tag overwrite.

| App | New index/deployment digest | Platform manifest | Actual config digest |
| --- | --- | --- | --- |
| Employee | sha256:41db94689ae934e3daa6c7f8fb57d8de5cc58a53995efd50217189231ac1f0c1 | sha256:60b806cec50071591904f6697efa2eb18f6de52f87742685951391af4ece879e | sha256:d02236b5242ce91dd11a4df013277593c4abd87b3c6938eaf3442e4721eac3ef |
| Resident | sha256:1c0881a9855ce7ffcaad26da06422a7c7be7d9cf536073ec9c5d955889882354 | sha256:997fa7342028a1a4d487e4bb1a3eeddde5af7569d6f1819a8e8ea4ef86340003 | sha256:207f7ca16fbe8f87753e7a389e6e2165cdaacaeb4a6c1be77f236199fd61afc8 |

ACR exceptions: employee push07:20:29-07:20:51Z (21.70s, original proof
failure), employee read-only admission07:21:40-07:21:59Z (18.81s), resident
push07:22:06-07:22:25Z (19.80s). Every window restored full frozen ACR
projection exactly, cleanup errors zero, exact owned credential config removed.
Final policies remain public Disabled/default Allow/no IP or VNet rules/
bypass None/exports disabled/admin false, with every other protected field equal.
Both app baseline projections remained unchanged through pushes.

## P02: Per-App Revision, Preservation and Health

| App | Before revision | Before digest | After revision | After digest |
| --- | --- | --- | --- | --- |
| Employee | ca-cutover-test-demo-api--emp-reapply-20261028-110058 | sha256:e6b6e7440c2b64577e96b6322c852bf630f1c5113608267132ebffc07d39fa19 | ca-cutover-test-demo-api--emp-main-20261029-072248 | sha256:41db94689ae934e3daa6c7f8fb57d8de5cc58a53995efd50217189231ac1f0c1 |
| Resident (recovered, NOT latest main) | ca-resident-demo--0000003 | sha256:fab6a85318f65db006bc610f3b3aff8ae799046d1b9a1813662b3b315c1b6fc7 | ca-resident-demo--rollback-20261029-073718 | sha256:fab6a85318f65db006bc610f3b3aff8ae799046d1b9a1813662b3b315c1b6fc7 |

Employee final read-only verification07:26:13Z succeeded: exactly one added
revision (all11 retained,10 historical), no removed revisions, latest=ready,
Succeeded / Healthy / Provisioned / Running / active100%. Full app protected
fields and auth equal baseline, zero unexpected changed paths; revision
representation comparison also zero differences. All30 env entries and other
configuration preserved, min0/max4. Curl /healthz200, /200 byte-equal main public
welcome page, /app,/app.js,/ops.js401. System29 records/11 target, console3
records/one positive startup, zero bounded startup-error matches; one ready
container observed. No rollback or repeated update.

Resident one forward update created ca-resident-demo--res-main-20261029-072628.
At07:33Z it reports Provisioned / health None / ActivationFailed / replicas0;
latestReady remains old0000003. System target events include repeated
ContainerStarted then Warning ContainerTerminated. This is actual runtime
activation failure, not a tooling-only rollback trigger. Public health200
alone is insufficient: it can be served by old ready revision.
No new resident runtime success is claimed.

Offline exact-image startup with no environment/network imports successfully
and refuses missing configuration (expected exit2). Source trace shows #525
now selects17 view columns including documents_json, while prior resident
deployment described16. This is a plausible compatibility dependency, NOT a
verified live SQL diagnosis; no SQL read/change is authorized or performed.
Failure-only old-image recovery will preserve all existing configuration.

Recovery preflight correctly stopped before mutation on two unexpected paths:
the image-only az containerapp update introduced value="" alongside each
resident secretRef (before: value key absent; after: empty value key present).
SecretRef names themselves are equal; no secret values were read or printed.
This violates the literal frozen preservation contract and may affect startup.
No other protected drift was found. It is not being normalized away.

Immediately relevant recovery correction: restore exact original writable
template with old image using a single ARM PATCH, preserving original env/refs
without CLI normalization. Omit only read-only request imageType and derived
ephemeralStorage; final GET must reproduce baseline exactly except recovery
suffix. Known own-update empty-value paths are explicitly matched before
recovery; no unrelated/concurrent drift may be overwritten.
Generated revision probes equal the original revision's defaults exactly;
cross-schema comparison uses that observed baseline, not arbitrary probe removal.

### Resident recovery verified; original failed attempt retained

First raw PATCH was rejected before revision creation. Raw GET at API2025-07-01
proved customMetricsSettings(null) is CLI-only, like imageType. Removing only
that remaining unsupported request field allowed the corrected PATCH at07:41:31Z.
This is one successful recovery mutation/revision, not an ambiguous-write retry.
Original failed request hash/receipt and corrected schema receipt retained.

At07:42:28Z recovery is latest=ready, Healthy/Provisioned/RunningAtMaxScale,
active100%, one ready container. Full app protected fields and auth equal original,
zero unexpected changed paths, including original secretRefs without empty
value fields; min0/max1 preserved. Revision template matches with only documented
service representation differences and exact old default probes. Curl /healthz
and /200; resident public page shows expected synthetic sign-in shell with hash
25f9c35518aa36da8a1f3ebf29d2b5fb449971708c8c5eb8c772a9674d8866d1.
It is explicitly NOT byte-equal current main, as expected for old-image recovery.
System33records/13target include RevisionReady and one positive container-start
match; console3records/no matched startup-error patterns; ready replica observed.
An initial ProbeFailed platform event is retained as a reason, not hidden or
misrepresented as persistent failure after positive readiness/health.

Final07:43:13Z checks: each app has only its final revision active/latest/ready.
Employee retained11 revisions (one forward); resident retained6 (one forward
plus one failure-only recovery); none removed. Complete app/auth comparators
pass; exact ACR policy projection equality passes. Both public health endpoints
return200, but only employee is latest main. A final git fetch confirms main
remains d70ee60ab3d7346a9991cf64382d9985f4d09f2e.

Correct system stream field is Msg rather than Log. Earlier employee system
pattern counts were not a reliable system-error assessment; positive console
startup and replica/health proof were valid. Corrected final log query07:43:51Z
returned system2records/no target records, console3/one positive startup/zero
matched errors. Bounded logs do not prove exhaustive absence of errors.
Resident failed-revision console was unavailable with zero replicas. Source
compatibility and secretRef-empty-field effects remain unisolated hypotheses.
No live SQL query, historical workspace query or secret retrieval occurred.

## Amendments and Divergences

Employee update executed once and created
ca-cutover-test-demo-api--emp-main-20261029-072248. It is Healthy/Provisioned/
Running, active100%, one ready container and positive console startup, no matched
startup errors; full app/config/template/auth equality passed except intended
image/suffix. Initial verification failed because employee / is deliberately
public welcome.html200, not401, and revision GET omits service-populated defaults
present in app GET. Original failed verification receipt is retained.
These are tooling/assertion corrections, not runtime failures: no rollback and
no repeat update. Correct public-shell and explicit cross-schema comparison
contracts are recorded in details; complete app baseline comparator unchanged.

Follow-on read-only checks identified explicit null scale defaults in revision
GET and default active-only revision list behavior. New employee service stayed
healthy with health200 and protected assets401 throughout. Correct list scope
is --all. Employee complete retained-history baseline is explicitly reconstructed
using createdTime before saved update-intent; original active-only backup and
failed verification receipts preserved. Resident full --all baseline is captured
prospectively before its update. No extra revision, deletion or rollback.

No material divergence. Local Docker route chosen because prior remote ACR
task403 would require widening the approved VM-only network boundary.
Fresh gh account resolution is excluded by explicit no-gh instruction;
existing repo-local privacy-safe identity and historical evidence will be used
for the requested local commit without changing global configuration.

## Validation and Review Readiness

Builds, digest binding, complete configuration backups/comparisons, valid-flag
logs, revision list --all/show, ready replicas and bounded anonymous curl checks
executed. Original tooling and runtime failures retained; no failure is silently
converted to success. Sanitized machine evidence:
.copilot-tracking/changes/2026-10-29/both-demo-sites-redeploy-evidence.json.

No new source or canonical tests changed. Complete local publication gate,
independent exact-head publication assessment, hosted checks and human approval
remain coordinator-owned prerequisites, NOT passes claimed here. The old
publication exception is not inherited. No application regression suite needed
for this evidence-only candidate; no full receipt exists for this task.

Pre-Review reconciliation (original handoff): P01/P02-T01/P02-T03 complete; P02-T02 requested
resident-main success remains unchecked and is routed later after actual
failure/recovery. P03 Review/local commit pending. Plan, details, changes and
state agree on Partial execution. Ready for one original independent Review
of this boundary, not accepted/conformant two-site deployment.

## Original Independent Review and Parent Dispositions

One original Review executed Complete, implementation Partial, outcome
Not accepted, at
.copilot-tracking/reviews/logs/2026-10-29/both-demo-sites-redeploy-review.md.
Original2High/1Medium/1Low findings retained verbatim; no second Review.
Reviewer independently reproduced strict full final app/ACR comparisons,
auth equality, source/archive/integrity and current two-app revision metadata.
No ongoing final protected-state mismatch found.

| Finding | Parent disposition and later route |
| --- | --- |
| RV-001 High | Accepted: resident latest-main outcome unmet, cause unisolated. Later rpi-research, no SQL/secret/new rollout authority inferred. |
| RV-002 High | Accepted: installed forward CLI altered exact secretRef representation. Later rpi-implement for synthetic-tested exact-template request handling. Final cloud state is recovered, not future executor acceptance. |
| RV-003 Medium | Accepted: executable cleanup lacks separate restoration-start/readback sub-deadlines and one admission inspect uses a fixed timeout. Observed windows restored exactly within22s, but advertised frozen-contract completion was overstated. Later local rpi-implement; no live failure injection. |
| RV-004 Low | Disputed, retained unchanged: the original Review alleges a task prohibition on a /tmp shared lock, but no such prohibition appears in supplied user/repository requirements. The named nonblocking shared lock is the earlier successful procedure. No lock is moved/deleted or new restriction inferred. Original finding remains historical, not silently closed or regraded. |

Review findings are routed to later work, not corrected or closure-verified
inside this completed task. The task lifecycle can finish despite the explicitly
unmet delivery outcome. Human/authenticated acceptance remains unperformed.

## Local Evidence Commit and Coordinator Handoff

Original dated evidence, including unmodified critique/Review and sanitized
machine receipt, committed locally as
59049aa80de14972c717e1d31a27309b984e7c7c.
Both author and committer use the existing repository-local privacy-safe
noreply identity; exact mandated Co-authored-by trailer verified in the commit.
No fresh gh lookup, gh command, push, PR, merge or history rewrite.

JSON shape/state pointers, evidence secret-field exclusion, explicit Partial
result, existing .gitignore and staged whitespace checks passed. Commit contains
only the eight named task artifacts; raw backups/logs/configuration are external.
Working tree was clean immediately after the original evidence commit.
This final parent-status update is a separate local commit, not an amend.

RPI task status completed means the full ordered loop and handoff finished,
NOT that both apps reached latest main. Automatic session remains running at
Follow-up; no child selected and no further action authorized. Coordinator
owns publication and a Refs-only PR after required gates; no full receipt,
independent exact-head publication approval or hosted/human approval exists.
Original backups remain host-local in the protected session evidence root,
not in an approved remote artifact store; no historical/generated evidence was
deleted. Owned temporary credential config and local image-export tar files
were removed, and no ACR tag/image/revision or shared lock was deleted.

## Follow-Up Items

1. Research actual resident startup failure and installed CLI secretRef
   serialization; highest value because it blocks the requested second site.
2. Correct/test local executor exact-secretRef and restoration deadline behavior
   (RV-002/RV-003). High engineering-quality leverage removes the observed CLI
   failure and makes cleanup bounds reliable without cloud mutation.
3. Plan a separately authorized resident retry using exact raw-template schema,
   compatibility proof and preserved refs; depends on diagnosis/executor work
   and a new forward-revision allowance, not active scope.

Owner authenticated employee feature review remains a distinct immediately
available feedback activity, not evidence that the resident source is accepted.

Coordinator publication remains separate. No deeper discovery or new child
work begins at Follow-up.
