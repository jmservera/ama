---
title: IoT Hub test strength phase details
description: Evidence-based task details and completion expectations for PR 557
ms.date: 2026-10-29
---

Task: pr-557-test-strength / iothub-test-strength-557.
Readiness: research Ready (C1-C6), one final-candidate critique executed with
original Revise preserved and PC-001/PC-002 disposed in the plan. P01-T01,
P01-T02, P02-T01, P02-T02 and P02-T03 complete.
Plan: .copilot-tracking/plans/2026-10-29/iothub-test-strength-557-plan.md.

<!-- phase: P01 -->
## P01: Strengthen live contract assertions

<!-- task: P01-T01 -->
### P01-T01: Bind both reference fixtures

Extract the body of test_live_profile_never_puts_existing_hub_and_guards_actual_sku
to assert_live_sku_guards(template), replacing self.live only inside that helper
with its argument. Preserve the existing test entry point, no-hub-PUT check,
parameter constraints, matrix and consumer-group assertion. In each matrix
iteration define reference(identifier, *args) that asserts the exact fixture ID
before returning synthetic sku/capacity or location. Default-bound loop values
may follow local fixture conventions. Do not modify the ARM evaluator.

Completion: valid templates pass and both fixture functions reject unrelated IDs.
Evidence: final 23-test IoT selector passes; independent SKU/unit/location
wrong-hub subtests check both IDs in the failure message.

<!-- task: P01-T02 -->
### P01-T02: Add isolated identity mutations

Add one test method iterating the SKU, units and location guard keys and
corresponding helper. Deep-copy self.live for each case. Replace
`resourceId('Microsoft.Devices/IotHubs', parameters('name'))` with
`resourceId('Microsoft.Devices/IotHubs', 'wrong-hub')` only in the selected
guard value. Assert before/after differ, then assert failure identifies both
fixture and wrong-hub IDs. This preserves valid returned properties so only
reference identity changes.

In assert_live_diagnostics assert name equals to-log-analytics. Extend the
existing scope/workspace mutation test with a name case, mutating no other
field; rename its test method descriptively if needed, without removing coverage.

Completion: all three wrong-reference subtests and the renamed diagnostic
setting are rejected by the same helpers used by positive tests.
Evidence: helper assertions and all four identity mutation cases pass. Removing
only the three identity assertions from the parsed source in memory causes
exactly the expected four mutation failures, without errors or skips.

<!-- phase: P02 -->
## P02: Validate and review

<!-- task: P02-T01 -->
### P02-T01: Requested validation

From infra:
`python3 -m unittest discover -s tests -p 'test_iothub*'`.
Use restored Ruff 0.17.1 at /tmp/ama-iothub-557-ruff-20261029/bin/ruff.
Run root-relative:
`ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_iothub_module.py`
and
`ruff format --isolated --line-length 100 --check infra/tests/test_iothub_module.py`.
Record exact commands, counts and skips. If tools are absent, restore only
missing tooling outside the repository. Review diff for test-only scope and
unchanged score file. No Azure service operation is allowed.
Evidence: 23 tests OK, no skips; Ruff 0.17.1 lint/format checks pass after its
formatter corrected an initial one-character line-length issue. Full command
results are recorded in the changes artifact.

<!-- task: P02-T02 -->
### P02-T02: Independent Review

Activate rpi-review once after implementation and validation. Supply the
canonical research, plan, details, critique and changes paths, affected test
file and output path. Record execution separately from outcome. Route any
remaining findings as later work, never repeat Review in this task.
Material in-scope findings block successful acceptance/closeout; report the
unmet criterion and route correction to later work under the one-pass RPI
contract. Do not silently defer a failed criterion while claiming success.
Preserve the original independent outcome. Out-of-scope findings remain
separate follow-ups and do not widen this task.
Evidence: one independent Review execution Complete, outcome Conformant, zero
findings or blockers. Reviewer independently reran 23 tests/no skips, Ruff,
method-preservation and four mutation-sensitivity checks. No correction needed.

<!-- task: P02-T03 -->
### P02-T03: Local commit

Resolve the authenticated GitHub account (done: id 8036360, login jmservera),
configure repository-local privacy-safe author/committer identity, stage only
the test file and this task's dated artifacts, and create a Conventional Commit
with the required Copilot coauthor trailer. No push, full publication gate,
merge, or score-file edit. Confirm clean worktree and commit paths afterward.
Only claim successful delivery when all requested criteria and validation are
proven and no material Review finding remains. A blocked candidate may be
preserved locally only with its incomplete outcome explicitly recorded.
Evidence: ce55aa80856756ce8fba11a91c37a2bcebbaf7f8 committed the test file and
seven dated original RPI artifacts. Verified privacy-safe author/committer,
required coauthor trailer, clean worktree, one unpushed commit and unchanged
score file. All AC1-AC5 are met for this local-only task. Evidence-only closeout
is a separate local commit, without changing reviewed Python.
