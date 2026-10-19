---
title: Issue360 bounded RG publisher plan
description: Original preimplementation candidate and critique dispositions
ms.date: 2026-10-19
---

Task: 360 / issue360-rg-loop. Base: 634a024d97d2da7168b8a7d5f343ab26e6108cf3.

## Executive Summary

Publish the reviewed proof layer through one ephemeral same-VNet x64 VM, then
pin only the existing initializer image after actual digest pull/run verification.
Research rules out an existing standalone publisher, unsupported UK South ACR
pool and restricted B2s; available B2als_v2 has quota and retail pricing.
Use a dedicated subnet/deny-inbound NSG and public IP for outbound only.
No public backing-service changes, tenant writes or historical SQL initialize.
Real tenant/role/browser/AI acceptance may remain blocked and edge must remain.
Status: implementation executed with provider-capacity blocker after direct
critique dispositions (original verdict Revise retained, not overwritten).
The actual B2als_v2 and D2as_v5 preflights both failed capacity restriction.
No resources allocated; dependent image publication and pin remain unexecuted.

## Sources

.copilot-tracking/research/2026-10-19/issue360-rg-loop-research.md (C1-C4, W1-W6).
Live #360/#349/#358 body/comments retrieved 2026-10-19.

## User Decisions and Requirements

* Run Research, Plan with one original critique, Implement, one Review in order.
* Preserve existing ama, private backing, production defaults and historical evidence.
* Necessary RG-contained resource/network/publication operations are authorized.
* Prefer existing publisher; new temporary infrastructure needs availability,
  pricing, bounded lifetime, minimal grants and exact owned cleanup.
* No push/PR: coordinator independently assesses frozen HEAD/base/full receipt.
* #349 tenant/human gates persist; #358 follows this branch without shared edits.

## Goals

Prove fresh source-bound publication and safe image-only initializer activation,
or record exact technical blockers without success substitution. Execute available
HTTPS/SQL/AI checks only within the supplied credential/data/approval boundaries.

## Scope and Non-Goals

Add narrowly bounded infrastructure template and its safety tests if needed.
Use existing proof Dockerfile/context and scripts unchanged. Update existing
infra README, ADR 0002, evidence pack, KB index/log; no memory changes.
No new app feature, web edit, public backing/bypass, tenant change, private data,
Front Door retirement, subscription scheduling resource or broad IAM.

## Functional Requirements

New resources: uniquely named owned VM (system MI), OS disk, NIC, NSG, public IP,
dedicated subnet and one registry-scoped AcrPush assignment. No other assignment.
NSG denies all inbound (including SSH); Run Command is management transport.
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

External private files mode0600, directories0700; no credentials/raw response
payload in source/evidence. MI tokens obtained only inside the temporary VM,
never in arguments/logs. Fresh readback confirms all backing public access stays
Disabled and bypass/policies unchanged. Two-hour lifetime target with operator
cleanup, estimated D2as_v5 VM/IP/disk USD ~0.217 excluding IO/transfer/tax,
not an invoice. No allocation or new resource charge was observed.
No concurrent heavy commands outside /tmp/ama-rpi-heavy.lock on shared host.

## Acceptance Criteria

1. Focused template/proof/setup tests pass before cloud writes; exact preview
   is limited to owned Creates and one dedicated new subnet.
2. Private publisher proves both ACR endpoints private/reachable before login.
3. Source manifest, immutable base/digest/architecture and pull/run evidence exist.
4. Initializer image-only readback preserves other observed settings.
5. Owned resource/assignment deletion and ama/old stack preservation verified.
6. Honest #360 criterion table separates source, owner authority and live outcomes.
7. One original Review retained; clean commit and all17group gate external receipt.

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

## Critique Disposition

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

Review RV-001: strengthen exact compiled resource-relationship and negative
guard tests in a later rpi-implement invocation. Current template was inspected
as correctly wired, but test coverage is incomplete. Original Review is not
overwritten or rerun; this task makes no post-Review source correction.
Review RV-002/003 preserve publication/live-acceptance blockers below.
Actual UK South publisher capacity remains the primary technical blocker;
fresh provider-preflight success or an existing verified private publisher is
required. Quota/SKU GETs are insufficient. No speculative larger allocation.
#349 authorized tenant provisioning/credential/staff/browser acceptance remains
blocked by existing application credential with no Graph permission hints and
failed application-read probe. #358 real KV preservation round-trip follows.
#350 parity and model/human approvals are outside this bounded loop.

## Handoff

Bounded implementation evidence is ready for its one original Review.
P01-T02/P02-T01/P02-T02 remain blocked, not complete. Review must assess source
and actual failed-preflight evidence without inventing live completion.
Final commit/full17gate remain after Review. Changes path:
.copilot-tracking/changes/2026-10-19/issue360-rg-loop-changes.md.
