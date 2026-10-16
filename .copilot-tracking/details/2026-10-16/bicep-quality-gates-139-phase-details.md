---
title: Bicep quality gates 139 phase details
description: Task-level implementation boundaries and evidence
ms.date: 2026-10-16
---

Task #139. Research C1-C9 supports ready candidate; no product decision pending.

<!-- P01 -->
## P01: Implement offline gates

<!-- P01-T01 -->
### P01-T01: Exact controls and mutations

Reuse existing unittest class/assertions. Assert module-specific endpoint group,
target, subnet, DNS and actual endpoint resource wiring. Avoid global presence
counts that permit missing service controls. Extend no-key checks to IoT Hub and
Log Analytics. Assert both immutability policies target audit-archive and
ledger-digests with positive constrained parameters, without claiming locking.
Enumerate profile/public/purge combinations and guards; add edge/pilot guard
positive/negative cases. In-memory deep copies must fail the same assertions
when requested controls are removed or disabled. No fixture-only pass.
PC-001: require each network-switch service's public properties and main
forwarding argument, not presence-conditional counts. Assert compiled Container
Apps internal mode and SQL development-firewall condition. Mutations delete a
public property/argument, force public/external mode and remove/force the
firewall condition. Record rejection using the clean-template assertions.

<!-- P01-T02 -->
### P01-T02: Safe Bicep bound and CI

Add audit retention minValue(1), matching existing digest retention. Reuse
existing bicepconfig rules and add regression coverage rather than gratuitous
rewrites. Add infra trigger and offline build/lint/tests to existing source
namespace job. Keep legacy job/step/check names. Check all Bicep files locally
and in the added gate, not only main's reachable tree.
Implementation-time current-state update: all-entry-point build revealed
governance's interpolated subscription-prefixed built-in policy IDs fail
error-level resource-ID lint and target the wrong scope. Use tenantResourceId
and add a compiled assertion; audit mode and Free Defender defaults unchanged.

<!-- P02 -->
## P02: Validate and deliver

<!-- P02-T01 -->
### P02-T01: Local evidence

Baseline compiled main with Bicep 0.48.1. Full infra suite exposed missing
installed source distributions, not Bicep failures. Restore via isolated venv
and pip editable installs. Run full infra suite with REQUIRE_AZ_BICEP=1;
ruff check/format on changed test with explicit isolated repository-like rules.
Verify mutation rejection, all builds/lints and unchanged workflow identities.

<!-- P02-T02 -->
### P02-T02: Documentation and publication

Update infra README with exact gate commands and unlocked immutability/live
ARM/network limits; append log without changing earlier entries. Record one
Review and route outside-scope items; no repeat Review. Verify authenticated
email, commit with trailer, push topic branch and create main-target PR.
No closing keyword in PR body. No deployment or protected private files.
Implementation tasks and documentation are complete. Local full suite passed;
one Review and caller-authorized publication are the delivery handoff.
