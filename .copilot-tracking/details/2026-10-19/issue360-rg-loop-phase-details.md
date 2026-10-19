---
title: Issue360 bounded RG publisher phase details
description: Original implementation expectations before cloud mutation
ms.date: 2026-10-19
---

Task 360 / issue360-rg-loop. Plan and research are same-date/same-slug siblings.
Active additional recovery P04 is owner-authorized on2026-10-19; no coordinator
implementation. Supplemental research:
.copilot-tracking/research/2026-10-19/issue360-rubric-lifecycle-recovery-research.md.
Same-task original evidence remains immutable, including the adverse Review.

<!-- rpi:task id=P04-T01 -->
## P04-T01: Rubric publication consistency

Starting head7e810dc9c9ac520e4e7717b4604dc08fbbc8e311 was authorized
fast-forward from e879 after clean ancestry/latest.json-only verification.
Current trusted base634a024d contains the exact source/lock/scripts inspected.
Actual record log has successful score push, NEW_SHA populated and all lifecycle
outcomes success; only immediate pulls.get head mismatch explains moved failure.
The exact returned head is unknown. Reproduce old-source visibility separately
from actual concurrent movement; do not invent API telemetry.

Add no more than six test functions to existing test_record_workflow.py, preserving
all existing cases. Exercise source and compiler-generated steps. Simulate
sequential API responses and capture retry delays without real sleeps. Integrate
actual shell step outputs from temporary bare Git repositories into publication,
including real movement/deletion/rejected push. Verify no main changes.
Limit retry to successful self-append plus old scored SHA; five reads,15 seconds
maximum, exact resulting SHA still mandatory. Distinct exhausted diagnostic.
No scoring/gate/prepare/latest.json/model/protection/credential semantic change.
Compile using existing gh-aw v0.89.21; no hand edits to lock. Preserve original
failure evidence and baseline159 passing lifecycle cases externally.

P04-T01 completed: six new parameterized test functions plus integrated
push/publication assertions in the existing race test. Initial reproduction
against unchanged source/lock:24 failed/179 passed. After correction207 lifecycle
cases pass, including real gate.evaluate equality/regression through publication.
Pinned runtime missing on first wider run was restored from official immutable
gh-aw-actions924af5fdc64061cfbf66fb584c8b07e2ac230c60; ten exercised source
blob hashes verified by existing test. Actual stdio/HTTP runtime and generated
schema checks:12 passed (12 unrelated trigger expectations deselected).
Combined focused219 passed. Full rubric331 pass/21 fail/no skips; exact21
failure IDs match untouched7e810dc9 baseline276 pass/21 fail/7 runtime skips.
No failure suppressed or unrelated fixture repaired. Native emitted compilation
with actionlint1.7.12 and actual ShellCheck passes. Earlier no-emit compilation
did not invoke scanners; direct old1.7.7 could not parse existing platform
features. Both failed/partial attempts retained, not treated as passing lint.
Logs: /tmp/issue360-rubric-recovery-20261019/.

<!-- rpi:task id=P04-T02 -->
## P04-T02: Frozen exact-head handoff

Document finite one-score-append lifecycle and required separate final-head
full local gate/independent review. Existing src-ci workflow_dispatch selects
branch; verify actual dispatched run head equals frozen remote head before
trusting retained check names. No dispatch here, no manually set status or
review dismissal. A second rubric rescore is not required just to validate
the appended metadata commit and would move HEAD again.

Update only appropriate rubric guide, KB routing/log and tracking. Resolve
gh api user-derived repository-local noreply for author and committer, Conventional
Commit plus Copilot trailer. Full gate uses /tmp/rpi-413-tools plus existing host
Node PATH, isolated credentials, pip, shared lock and16GB Docker memory limits.
Run explicit focused rubric commands in addition to all17 groups. Commit all
changes before final gate, external fresh output only. Fetch main and verify
receipt; do not postgate commit/push/update PR. Coordinator must independently
assess final exact HEAD/base/receipt/source/RPI/primary evidence first.

Current implementation disposition: candidate source/tests/docs delivered;
both actual provider preflights failed capacity before allocation. P01-T02
and dependent P02 publication/pin remain blocked. The task expectations below
retain their preimplementation design, not a claim those operations ran.
Original233 focused/363 complete infra tests passed, zero skips; original failed
missing-dependency/compile attempts retained externally. The one original
bounded-evidence Review is Complete / Not accepted and immutable.
The coordinator-selected RV-001 continuation adds five focused/364 complete
infra passes, zero skips; no live release acceptance or publication.

## Coordinator-Selected Outbound Continuation (Cycle2)

<!-- rpi:task id=P01-T05 -->
P01-T05 starts from clean9f552eda3efd83443e36384febfda4cf538df023,
base634a024d97d2da7168b8a7d5f343ab26e6108cf3, after prior process exit.
Reviewer84baed3f-578f-4ab8-9a61-3da35b0efc69 closed RV-001 but identified
unrestricted default outbound with public IP. Change only publisher Bicep/tests,
directly related current documentation and RPI artifacts. Preserve original
research/critique/Review bytes and existing guards/resource relationships.

Enforce TCP443 to historical private ACR10.40.4.20/.21 only, platform DNS53
TCP/UDP, WireServer TCP80/32526 and IMDS TCP80, then explicit platform
DNS/IMDS denials and deny-all outbound before default NSG rules. Private IP
identity/DNS/VNet DNS configuration must be independently revalidated before
any future deployment; fixed addresses are not endpoint discovery or attestation.
WireServer is NSG-exempt; DNS tag rules are port/IP policy, not QNAME filtering.
No public package, Storage, AzureCloud, ARM or Entra service-tag allow.
Run Command agent redirection depends on supported guest-agent behavior and
is unverified on the pinned image. Stock Ubuntu Docker/package bootstrap is
blocked until a separately reviewed private/offline route exists. No new
firewall/proxy/image service is introduced or implied to work.

Validation: actual compiled contract, first-match outbound flow cases, bounded
negative mutations compared before/after externally, focused plus full infra.
Then clean commit and fresh actual17group gate with credential isolation, full
host PATH and /tmp/rpi-413-tools first, pip/no uv, shared fixed heavy lock.
No Azure command, what-if, provider attempt, push/PR/merge or repeated Review.

P01-T05 implementation complete: eight focused tests and367 complete infra
tests pass, zero skips. Existing16 relationship/guard mutants stay protected;
18 additional outbound mutants reject. Actual original compiled template
passes original5 tests while both new policy checks reject it (18 assertion
failures including unsafe flow subtests, zero runner errors/skips). The
same remove-all-outbound compiled mutant passes original5 and fails corrected
policy checks. Corrected complete baseline passes8. Evidence and reproduction:
/tmp/issue360-rg-correction2/mutation-evidence.json and mutation-evidence.py;
focused.log and infra-all.log. No live network enforcement is claimed.
Clean commit and fresh17group gate/receipt remain external post-freeze steps.

## Coordinator-Selected RV-001 Continuation (Correction Cycle1)

P01-T04 is the only new active implementation boundary, after original
process exit0 and frozen HEAD 8f996e6ffc0a7e6a4953fff4523d1cbe01190522.
Extend only infra/tests/test_private_proof_publisher.py and associated current
plan/changes/state. Compare original tests and corrected tests on real compiled
ARM mutations: detached NSG, wrong VNet/subnet/NIC/public-IP, absent/unrelated
guard dependencies and weakened refusal expression/minLength.
Assertions protect source regressions, not actual cloud enforcement.
External preview/assignment checks remain operator-owned and unexecuted.
No cloud writes/attempts or new operational/human approval. Both capacity
failures and tenant/live blockers persist. Original critique and Review are
immutable and are not repeated.

<!-- rpi:task id=P01-T04 -->
### P01-T04 Completion Evidence

Existing module now asserts the complete compiled approval/refusal expression,
nonempty nested guard input, exact guard dependency IDs and the connected
NSG -> existing-VNet child subnet -> NIC -> VM path, plus explicit public-IP
reference and prerequisite dependencies. All16 negative fixtures reject.
Actual external before/after runs of the four baseline contracts reproduce
14 escaped mutants before and zero after, with two preexisting guard-condition
rejections retained. Both unmutated baselines pass4/4; zero errors/skips.
Five focused tests and364 complete infra tests pass. Logs and compiled fixture
bytes: /tmp/issue360-rg-correction1/. No template or guard source change.
No cloud command/attempt or claim of operational enforcement.

## Applied Original Critique Corrections

PC-001: acquire exclusive /tmp/ama-issue360-activation.lock for the attended
activation, assert immediately fresh original image/Manual/single container/
identity/registry shape, then compare full normalized properties on readback.
This serializes this host's run; it is not distributed exclusion. Re-read
immediately before write and stop on any drift. On ambiguous update first read;
rollback only this run's image if non-image baseline is intact. Unrelated
drift/failed readback requires handoff, never destructive whole-body recovery.

PC-002/004: Bicep has no IAM resources. After actual VM MI principal exists,
create only one AcrPush assignment using explicit object ID/principal type and
the exact authorized registry ID. Record returned ID privately and independently
read back principal/role/scope. Existing full IAM tests stay unchanged.
Before deployment persist exact RG/subscription/VNet/ACR/owned IDs, deadline,
template/parameter hashes and existing subnet baseline. Preview/apply identical
private files, explicit subscription, Incremental. Only exact owned Creates
including guard-deployment metadata/new subnet allowed; unrelated Ignore records
may be counted as no-operation inventory, never accepted as an authorized change.
Any parent VNet modification, unknown/unresolved actionable delta or wrong
target blocks apply. New tests inspect compiled exact resource/security shape.

PC-003: write planned recovery inventory before first cloud mutation. Responsible
operator is this attended worker, with cleanup finally on exceptions/interruption.
Provisioning timeout15minutes, Run Command timeout bounded with cleanup reserve;
absolute allocation-to-deallocation deadline two hours, persisted as UTC.
Arm and verify guest poweroff timer before build work. If process is hard-killed,
coordinator uses exact inventory IDs and ownership tags to deallocate/delete;
expiry tags and poweroff are not billing guarantees. Confirm separate disk
absence, all exact resource deletions and assignment absence.

PC-005: fetch origin/main before gate and require equality with approved base.
On movement stop for coordinator base decision, never rebase/alter base silently.
Use caller's exact PATH and new external output, then fetch again and run
python3 tools/rpi-checks.py --verify-receipt <fresh-external-dir>/receipt.json
--base <fresh-origin-main-sha>. Any HEAD/base/tool/image/input change requires
new complete gate; no postgate commits or remote publication by this worker.

<!-- rpi:task id=P01-T01 -->
## P01-T01: Canonical template and tests

Use existing Bicep guard pattern to refuse non-ama. Fixed owned name stem and
subnet prefix avoid accidental reuse of existing assets; check absence first.
Existing VNet/ACR remain existing declarations. Explicitly disable password
login and boot diagnostics storage; no extension secret or credential value.
Registry assignment belongs only to temporary VM MI, not initializer/runtime.
Compile offline and inspect actual ARM resources/security properties in tests.

<!-- rpi:task id=P01-T02 -->
## P01-T02: Reviewed preview and allocation

Research-time SKU observation: B2als_v2 unrestricted, 2CPU/4GiB/x64,
Basv2 quota0/100. Actual provider preflight refused capacity, as did separately
researched D2as_v5 (2CPU/8GiB/x64, DASv5 quota0/100). Final undeployed template
fixes D2as_v5; no actual allocation availability is claimed.
Pinned Ubuntu Jammy version 22.04.202610170. Dedicated new 10.40.8.0/28 within
existing 10.40.0.0/16, no existing overlap. Retained public IP does not bypass
explicit deny-all outbound. Apt/package Internet access is forbidden; platform
and private ACR flows alone are allowed. Bootstrap remains blocked, not proven
ready by the pinned stock image. No NSG inbound allow. Preview must not change old subnets/resources,
backing settings or default profile. Reject Deletes/Modifies outside the new
subnet and exact owned resources. Do not deploy if allocation/cost remains unknown.
Write exact created IDs to private inventory immediately; partial apply still
requires exact cleanup. Guest watchdog powers off after 7200 seconds; explicit
operator deallocate/delete controls billing. No subscription Automation changes.

<!-- rpi:task id=P02-T01 -->
## P02-T01: Build and smoke

Archive only Dockerfile, five explicitly named Python files and manifest from
tracked base. Bind each SHA256 and base commit to tag/evidence. Base API digest:
111b26226cad06e229bcf1c3174877510c4c68c5a5fefc885167a2b4c821657d.
Use registry private DNS for login and regional data endpoint, validated TLS.
No public DNS/hosts override, admin password or public bypass.
Use MI ACR OAuth exchange entirely inside VM and stdin Docker login.
Suppress all token/credential output. Build log stays restricted; emit only
exit statuses/hashes/architecture/UID and allowlisted immutable references.
Docker --network none, --read-only, --cap-drop ALL, no-new-privileges smoke
overrides ENTRYPOINT; imports, help and copied-file hashes must succeed.

<!-- rpi:task id=P02-T02 -->
## P02-T02: Pin safety

Retain rollback ef0058f8f380cc610d4b7113509293b3ed624d22afac95e807b4c69a4266dc72.
Fresh pull exact pushed digest and smoke it, not a separately rebuilt image.
Capture job before state only in memory/private operator files. Assert expected
name, one proof container and existing identity/registries; then update only
image with --container-name proof. Compare normalized full properties excluding
image and server-managed timestamps/provisioning state, documenting exclusions.
Do not start job args ["initialize"], change env/secrets/identity or API image.

<!-- rpi:task id=P02-T03 -->
## P02-T03: Acceptance constraints

Existing service-principal Graph token has no roles/scopes; safe application-read
probe failed. No interactive user session supplied. Record concrete tenant-owner
login/registration/consent handoff; do not upload operator credentials or generate
staff. Deny-all ingress stays until real auth readiness; HTTPS403 is restriction
evidence, not welcome/health200. SQL/AI may remain Not run rather than unknown-data
inspection or approval bypass. Existing private proof sentinel alone is not
permission to read staff/application contents.

<!-- rpi:task id=P03-T01 -->
## P03-T01: Cleanup

Delete only registry assignment created for VM, VM, exact OS disk if not
Delete-on-VM, NIC, PIP, NSG and owned dedicated subnet, in dependency order.
Confirm ownership tags/IDs before deletion and absence after; retain deployment
metadata if harmless, inventory it explicitly. Never delete RG, existing VNet,
ACR, initializer, private endpoints, identities or Front Door.

<!-- rpi:task id=P03-T02 -->
## P03-T02: Evidence

Append dated original outcome with sanitized names/config deltas and result
matrix to existing infra README, ADR0002 and cutover pack. KB routes/log update
without historical edits or memory change. Include costs as estimates, timestamps,
created/deleted resource classes, actual failures and evidence limitations.

<!-- rpi:task id=P03-T03 -->
## P03-T03: Review and gate

Exactly one postimplementation independent Review after source/markers/evidence
reconcile. Preserve original adverse findings and route later corrections.
Use gh api user-derived local noreply author/committer, Conventional Commit
and required Copilot trailer. Freeze clean candidate before full local gate:
PATH=/tmp/rpi-413-tools:$PATH PYTHONDONTWRITEBYTECODE=1 python3 tools/rpi-checks.py
--all --base 634a024d97d2da7168b8a7d5f343ab26e6108cf3 --out fresh-external-dir.
All17groups actually run/pass, fixed heavy lock, no real credentials inherited.
Fetch main and verify receipt; no postgate commit, push/PR or remote issue changes.
