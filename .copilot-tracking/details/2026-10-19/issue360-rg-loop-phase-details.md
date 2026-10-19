---
title: Issue360 bounded RG publisher phase details
description: Original implementation expectations before cloud mutation
ms.date: 2026-10-19
---

Task 360 / issue360-rg-loop. Plan and research are same-date/same-slug siblings.
Current implementation disposition: candidate source/tests/docs delivered;
both actual provider preflights failed capacity before allocation. P01-T02
and dependent P02 publication/pin remain blocked. The task expectations below
retain their preimplementation design, not a claim those operations ran.
233 focused and363 complete infra tests pass, zero skips; original failed
missing-dependency/compile attempts retained externally. Ready for one original
bounded-evidence Review, not live release acceptance or publication.

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
existing 10.40.0.0/16, no existing overlap. Public IP enables outbound apt/agent
only, no NSG inbound allow. Preview must not change old subnets/resources,
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
