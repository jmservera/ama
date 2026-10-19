---
title: Issue360 bounded RG publisher plan
description: Original preimplementation candidate and critique dispositions
ms.date: 2026-10-19
---

Task: 360 / issue360-rg-loop. Base: 634a024d97d2da7168b8a7d5f343ab26e6108cf3.

## Executive Summary

2026-10-19 additional owner-authorized recovery: P04 repairs only the rubric
publication lifecycle on existing PR416. Source scoring and original issue360
acceptance stay separate. Supplemental research shows the gate actually passed
48/100 against48, but publication denied an immediate post-push API head mismatch.
The response SHA was not logged; stale visibility must be reproduced, not
asserted as observed fact. Add bounded old-source-head visibility retries only
after a successful score push; never accept a mismatched final head.
No repeat original critique/Review or publication before coordinator assessment.

Publish the reviewed proof layer through one ephemeral same-VNet x64 VM, then
pin only the existing initializer image after actual digest pull/run verification.
Research rules out an existing standalone publisher, unsupported UK South ACR
pool and restricted B2s; available B2als_v2 has quota and retail pricing.
Use a dedicated subnet/deny-inbound NSG with explicit private-registry and
platform outbound rules followed by deny-all outbound. No package Internet
egress is permitted; the retained public IP does not authorize Internet access.
No public backing-service changes, tenant writes or historical SQL initialize.
Real tenant/role/browser/AI acceptance may remain blocked and edge must remain.
Status: implementation executed with provider-capacity blocker after direct
critique dispositions (original verdict Revise retained, not overwritten).
The actual B2als_v2 and D2as_v5 preflights both failed capacity restriction.
No resources allocated; dependent image publication and pin remain unexecuted.
Coordinator-selected cycle2 now restricts outbound source policy and adds
compiled egress regressions with actual offline mutation evidence. Package
bootstrap remains blocked, not a deployable/working publisher. Original critique/Review
remain unchanged; this is not acceptance of the blocked live objective.

## Sources

.copilot-tracking/research/2026-10-19/issue360-rg-loop-research.md (C1-C4, W1-W6).
Live #360/#349/#358 body/comments retrieved 2026-10-19.

## User Decisions and Requirements

* Owner explicitly authorizes additional bounded rubric lifecycle recovery on
  the same branch, preserving original artifacts and prior adverse evidence.
* No push/PR update, paid hosted scoring, cloud/model/tenant writes or coordinator
  implementation. Frozen candidate/full17group receipt goes to coordinator first.
* Run Research, Plan with one original critique, Implement, one Review in order.
* Preserve existing ama, private backing, production defaults and historical evidence.
* Necessary RG-contained resource/network/publication operations are authorized.
* Prefer existing publisher; new temporary infrastructure needs availability,
  pricing, bounded lifetime, minimal grants and exact owned cleanup.
* No push/PR: coordinator independently assesses frozen HEAD/base/full receipt.
* Cycle2 explicitly rejects unrestricted outbound; no Azure writes, what-if or
  capacity attempts. Prefer blocked package bootstrap over broad service-tag
  Internet access or unjustified new filtering infrastructure.
* #349 tenant/human gates persist; #358 follows this branch without shared edits.

## Goals

Restore reliable exact-result-head rubric publication without weakening the
nondecreasing comparison or authorizing arbitrary score-file trust.

Prove fresh source-bound publication and safe image-only initializer activation,
or record exact technical blockers without success substitution. Execute available
HTTPS/SQL/AI checks only within the supplied credential/data/approval boundaries.

## Scope and Non-Goals

P04 adds only rubric workflow publication retry logic, its existing source/lock
regression harness, compiler-generated lock, related rubric guide/KB routing
and same-task tracking. No gate/prepare scoring semantics or scores edits.

Add narrowly bounded infrastructure template and its safety tests if needed.
Use existing proof Dockerfile/context and scripts unchanged. Update existing
infra README, ADR 0002, evidence pack, KB index/log; no memory changes.
No new app feature, web edit, public backing/bypass, tenant change, private data,
Front Door retirement, subscription scheduling resource or broad IAM.

## Functional Requirements

For P04, retry only a verified old scored SHA when NEW_SHA exists after a
successful recording step, no push failure or pre-record movement occurred,
and the deterministic gate succeeded. At most five API reads and15 seconds
of delays (1/2/4/8). A new unrelated SHA, closed PR, malformed response or API
error terminates the wait. Success still requires the exact NEW_SHA.
Exhaustion fails with a distinct visibility diagnostic; no green fallback.
Log only public commit IDs/attempts, not response bodies or credentials.

New resources: uniquely named owned VM (system MI), OS disk, NIC, NSG, public IP,
dedicated subnet and one registry-scoped AcrPush assignment. No other assignment.
NSG denies all inbound (including SSH); Run Command is management transport.
Outbound permits TCP443 only to recorded ACR private endpoints10.40.4.20/.21,
Azure platform DNS TCP/UDP53, WireServer TCP80/32526 and IMDS TCP80. Explicit
platform DNS/IMDS deny rules and final deny-all override ordinary defaults.
NSGs cannot filter package FQDNs or WireServer guest-agent traffic; platform
exceptions and DNS/registry misuse remain explicit limitations. No apt,
Docker/package download or general ARM/Entra/Storage/AzureCloud allow exists.
The pinned stock image has no proven offline build-tool bootstrap: P01-T02 and
P02-T01 remain blocked pending a separately reviewed private/offline tool route.
Use pinned Ubuntu image, researched fallback D2as_v5, 32GiB StandardSSD,
existing VNet/registry. Both actual preflights are now capacity-blocked.
Provision a two-hour guest poweroff watchdog before package/network operations;
operator deallocates/deletes exact owned resources on every completion/failure.
Poweroff is not deallocation: cleanup remains required to stop Azure compute billing.
Expiry tags are inventory, never claimed as automatic billing termination.

Proof files come from exact tracked base source with a SHA256 manifest; no whole
repository upload. Build and smoke the actual image without initializing SQL,
verify linux/amd64, nonroot, required imports/help and all copied file hashes.
Push a unique source-SHA tag, capture digest, remove the local tag/reference,
pull the exact digest and repeat smoke. Retain old initializer digest for rollback.
Pin through existing image-only CLI, compare full read-visible configuration
minus intended image before/after, preserving env, identity, registries and secrets.
Never claim write-only secret equality from GET.

## Non-Functional Requirements

Existing guarded non-force push, immutable event checkout, trusted main tools,
status names, model, baseline, review policy and main write prohibition remain
unchanged. Preserve original research/critique/Review hashes. Additional rubric
commands must run explicitly because the complete matrix omits this workflow.

External private files mode0600, directories0700; no credentials/raw response
payload in source/evidence. MI tokens obtained only inside the temporary VM,
never in arguments/logs. Fresh readback confirms all backing public access stays
Disabled and bypass/policies unchanged. Two-hour lifetime target with operator
cleanup, estimated D2as_v5 VM/IP/disk USD ~0.217 excluding IO/transfer/tax,
not an invoice. No allocation or new resource charge was observed.
No concurrent heavy commands outside /tmp/ama-rpi-heavy.lock on shared host.

## Acceptance Criteria

9. Source and compiled tests reproduce immediate old-head publication denial,
   recover only when the exact pushed SHA becomes visible, reject persistent
   old-head/unrelated movement/push failure and retain closed/error protections.
10. Integrate real temporary-Git push outputs with publication regression:
    unchanged ref self-append succeeds after visibility settles; concurrent
    move/deletion and remote push rejection cannot pass or write main.
11. Generate lock with installed gh-aw v0.89.21; run focused existing rubric
    regressions, available pinned runtime, compiler and native workflow lint.
12. Document one score append followed by final-remote-head full local gate,
    independent assessment and retained hosted checks on that head without
    another source push/rescore. Persistent publication failure is a blocker.

1. Focused template/proof/setup tests pass before cloud writes; exact preview
   is limited to owned Creates and one dedicated new subnet.
2. Private publisher proves both ACR endpoints private/reachable before login.
3. Source manifest, immutable base/digest/architecture and pull/run evidence exist.
4. Initializer image-only readback preserves other observed settings.
5. Owned resource/assignment deletion and ama/old stack preservation verified.
6. Honest #360 criterion table separates source, owner authority and live outcomes.
7. One original Review retained; clean commit and all17group gate external receipt.
8. Explicit compiled outbound allowlist/deny precedence and behavioral negative
   cases reject Internet/general-VNet/public-Storage/package destinations.
   This is source-contract evidence, not live NSG, DNS-content or package proof.

## Test Ownership and Locked Targets

Canonical template infra/private-proof-publisher.bicep and new
infra/tests/test_private_proof_publisher.py; maximum one new test module.
Existing proof/setup/staff/auth tests remain authoritative, no removals.
Generated ARM/parameters/context/scripts/logs stay external, never canonical.
Tests cover compiled semantic security/resource boundaries and negative input
guards; focused existing regressions cover proof context and setup behavior.
Full gate adds all existing SQL/browser/images/scans without claiming live approval.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01: Validate publisher and allocate bounded resources

* [x] P01-T01: Implement template/safety tests and run focused tests/Bicep.
<!-- rpi:task id=P01-T04 -->
* [x] P01-T04: Implement RV-001 compiled boundary regressions and before/after
  mutation evidence. Five focused/364 complete infra tests pass, zero skips;
  original tests accept14/16 mutants, corrected tests reject16/16.
  Fresh final commit/full local gate evidence remains external and pending.
<!-- rpi:task id=P01-T05 -->
* [x] P01-T05: Cycle2 restrict outbound, document blocked package bootstrap,
  preserve existing guards/relationships, capture compiled mutation evidence
  and focused infra results externally. Eight focused/367 infra pass, no skips;
  all18 outbound mutants reject, unsafe original passes old5 tests but fails
  new policy checks. Final clean commit/fresh full gate remain external.
* [ ] P01-T02: BLOCKED: private plan/inventory generated, both exact provider
  preflights refused capacity; allocation/assignment/watchdog not executed.

<!-- rpi:phase id=P02 -->
### P02: Publish, verify and activate

* [ ] P02-T01: BLOCKED by P01-T02; no build/smoke/publication.
* [ ] P02-T02: BLOCKED by P02-T01; no digest/pin/rollback.
* [x] P02-T03: Probe available direct HTTPS/credential prerequisites; stop tenant
  portion with concrete human handoff. Do not read unknown SQL application data.

<!-- rpi:phase id=P03 -->
### P03: Cleanup and durable handoff

* [x] P03-T01: Verified zero owned resources/assignment created; no cloud deletion
  needed. Existing subnet/policy baseline and private backing preserved.
* [x] P03-T02: Updated runbook/ADR/evidence/index/append-only log and changes record;
  363 complete infra tests pass, zero skips, after pinned missing YAML restore.
* [ ] P03-T03: Original Review executed Complete / Not accepted, RV-001/002/003
  routed below. Remaining commit/full gate/receipt verification occurs after
  this artifact is frozen; authoritative completion evidence stays external.

<!-- rpi:phase id=P04 -->
### P04: Owner-selected rubric lifecycle recovery

<!-- rpi:task id=P04-T01 -->
* [x] P04-T01: Reproduced post-push visibility mismatch, implemented bounded
  exact-head retry with real push/publication cases, compiled lock and ran
  focused lifecycle/runtime/compiler/lint evidence. 219 focused cases pass;
  full rubric331 pass/21 unchanged pre-existing failures, zero skips.
<!-- rpi:task id=P04-T02 -->
* [ ] P04-T02: Finite publication guide, KB routing/log and tracking reconciled;
  clean frozen commit/full actual17group gate and external receipt verification
  remain post-freeze steps for coordinator. No push or PR update.

P04 test ownership: existing test_record_workflow.py only; no test removal or
new module. Six new test functions, parameterized. Generated
target rubric-score.lock.yml only via compiler; canonical rubric-score.md.
Behavioral coverage, real temporary Git races and pinned MCP runtime
remain distinct from hosted API acceptance.

## Critique Disposition

P04 reuses the one historical critique and does not rerun or overwrite it,
as explicitly required by the owner. Supplemental focused plan is ready for
implementation from research C1-C5/W1-W2; original five dispositions remain.

Original executed once: .copilot-tracking/reviews/2026-10-19/issue360-rg-loop-plan-critique.md.
Verdict Revise. All five corrections are compatible with owner direction:

| Finding | Disposition and resolving contract |
| --- | --- |
| PC-001 | Applied: serialized local operator lock, immediate fresh baseline/expected old digest assertions; independent readback on update error; image-only rollback only if current image is this run's and non-image baseline still matches; otherwise stop for unrelated drift, never blind restore or full-body replay |
| PC-002 | Applied: prewrite private exact subscription/RG/VNet/ACR IDs, exact owned-resource allowlist, Incremental mode, input hashes; reject unexpected/unresolved actionable results. Separate MI role assignment until actual VM principal is known; assignment scope/principal/role and readback exact |
| PC-003 | Applied: planned IDs/ownership/deadline/cleanup manifest before first write; 15-minute provisioning and per-command limits with two-hour absolute deadline; finally cleanup on all paths, inventory hard-interruption recovery; VM deallocation/deletion and separate disk absence checks mandatory |
| PC-004 | Resolved by simplifying: no role assignment in new Bicep, instead staged explicit registry-only CLI assignment after actual MI readback; assert template has no IAM resource and run full existing IAM suite before writes. Existing exhaustive parser/matrix remains unchanged and no assignment is hidden from its scope |
| PC-005 | Applied current-main equality before gate and fresh-main exact receipt verify before handoff; no silent rebase. Reject advice to omit /tmp/rpi-413-tools or /tmp outputs: explicit caller requires that PATH and fresh external output, no host prohibition applies. Verify actual prerequisites; missing failure blocks/permits pinned restore, never reuse another receipt |

Assignment validation is an implementation operator gate, not claimed as
coverage by the static all-Bicep parser. No test removal/parser exclusion.

## Follow-Up Items

Cycle2 supersedes cycle1's test-only write boundary for P01-T05 only.
Authorized targets: publisher Bicep, its existing test module, directly related
runbook/ADR/evidence/KB routing and current plan/details/changes/state.
Independent exacthead reviewer84baed3f-578f-4ab8-9a61-3da35b0efc69 verified
RV-001 closed and the prior full receipt, but found a new Medium blocking
unrestricted outbound source policy. No repeated Research, critique or Review.
The previous receipt is invalidated by this correction. Existing P01-T04
completion evidence and original adverse artifacts remain historical.
No live package route is approved: keep bootstrap blocked rather than allow
Internet, AzureCloud, Storage service tags or pretend NSGs filter FQDNs.

Review RV-001 is now explicitly selected by the coordinator for bounded
rpi-implement continuation of this same task (correction cycle1).
Only the existing test module and current RPI planning/state/changes artifacts
may change. Assert compiled guard/refusal semantics, exact guard dependencies,
existing-VNet child subnet, NSG attachment, NIC subnet/public-IP and VM NIC
connections. Run actual bounded compiled mutations against original and
corrected tests and retain concrete before/after results externally.
Do not change the correctly wired Bicep, guards, IAM parser or matrix.
Original critique and Not accepted Review remain byte-identical; no repeated
Research, critique or Review. No Azure attempt, size/region escalation,
publication/pin/browser/tenant success or new approval is authorized.

P01-T04 implementation is complete with 16 concrete compiled mutations:
14 escaped the original four tests, none escape the corrected four checks;
both original and corrected baselines pass. Two original guard-condition
checks already rejected the missing-name/ID mutants and remain protected.
The added fifth test persistently exercises all16 negative fixtures.
Evidence: /tmp/issue360-rg-correction1/mutation-evidence.json and per-case logs.
No actual cloud-security proof, preview validator or role-assignment validation
is claimed. Original Review remains Not accepted; coordinator assessment pending.

Review RV-002/003 preserve publication/live-acceptance blockers below.
Actual UK South publisher capacity remains the primary technical blocker;
fresh provider-preflight success or an existing verified private publisher is
required. Quota/SKU GETs are insufficient. No speculative larger allocation.
#349 authorized tenant provisioning/credential/staff/browser acceptance remains
blocked by existing application credential with no Graph permission hints and
failed application-read probe. #358 real KV preservation round-trip follows.
#350 parity and model/human approvals are outside this bounded loop.

## Handoff

Current P04 supplemental recovery implementation is complete; focused cases
and generated/native lint pass. Final frozen commit/full gate are still pending,
not inferred from earlier receipts. Exact-head independent coordinator review
follows externally, without another original Review or any push here. Persistent
visibility failure and unsupported exact-head hosted checks remain blockers,
not permission for repeated paid scoring. Full rubric has21 independently
reproduced pre-existing failures, not a claimed complete rubric-suite pass.

The one original Review is complete / Not accepted and unchanged.
Cycle2 P01-T05 outbound source correction is implemented; no repeated
Review. P01-T02/P02-T01/P02-T02 remain blocked by actual capacity and unproven
private/offline build-tool bootstrap, not complete. No approved deployable
publisher or live security acceptance is claimed.
Final cycle2 commit/full17gate remain to run; authoritative receipt and
post-freeze state stay external. Coordinator independently assesses exact
HEAD/base/receipt and primary evidence before publication. Changes path:
.copilot-tracking/changes/2026-10-19/issue360-rg-loop-changes.md.
