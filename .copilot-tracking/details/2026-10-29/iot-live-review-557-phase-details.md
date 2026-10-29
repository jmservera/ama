---
title: PR 557 live IoT review correction phase details
description: Task-level boundaries and completion evidence
ms.date: 2026-10-29
---

Task ID: pr-557-review-corrections. Source of decisions:
.copilot-tracking/plans/2026-10-29/iot-live-review-557-plan.md.
Research C1-C5 is complete and adequate. No unresolved source blocker.

<!-- rpi:phase id=P01 -->
### [x] P01: Correct test coverage and exercise guidance

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Compiled diagnostics

Use the compiled self.live fixture, resource/resources helpers and deepcopy.
The helper should verify exactly one setting with scope
`[resourceId('Microsoft.Devices/IotHubs', parameters('name'))]` and workspaceId
`[resourceId('Microsoft.OperationalInsights/workspaces', 'log-cutover-test')]`.
The existing allowedValues assertion already pins the hub name. Preserve
metrics-only/no-resource-log checks in the shared live diagnostic helper.
One positive method calls it. One mutation method changes only scope or
workspaceId per subtest to another otherwise plausible resource expression
and requires AssertionError from the helper. No removals or fixture changes;
maximum one helper and two test methods. Existing production tests stay intact.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Bounded documentation

State one call total for this approval, no concurrent/repeated invocation even
via a new instance/process. Explain per-call pacing is not cumulative allowance.
Retain explicit budget/cutoff and owner/cost/alert references. Replace "Before
each run" and uncertain-frame rerun advice: stop, preserve truth and require
separate owner approval with reconciled attempted/uncertain deliveries and quota
before any further send. Keep receiver replay/SQL idempotency wording distinct.
Runtime changes are unnecessary and not approved by this plan.

<!-- rpi:phase id=P02 -->
### [ ] P02: Validate, independently review and commit locally

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Validation

Run the owner-specified infra unittest pattern without skips; baseline is 18
passing tests. Added positive/mutation methods should produce 20 tests.
Ruff check and format --check apply only to infra/tests/test_iothub_module.py.
Install missing tooling in an external task-owned venv after the confirmed
missing-module error; do not override the externally managed Python policy.
Completion evidence: final discovery passed 20 tests, zero skips; scoped
repository-standard Ruff check and format --check passed; diff --check passed.
Full command/result history is in the changes record.

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Review and local lifecycle

A fresh independent worker reads the final source diff and artifacts, writes
only the original Review artifact and reports actual findings/outcome. Preserve
it, route residuals to later work, and do not run a second Review.
Commit implementation and dated original evidence with authenticated account's
id+login noreply identity, repository-local configuration and Copilot trailer.
Attempt the full local gate after committing, with --lock-timeout 0 and a new
external output directory. Any missing prerequisite, dirty/ignored-input
refusal or inherited failure remains blocked. Never hand-edit scores, push,
make Azure calls, delete unknown inputs or alter protection/skip policy.
