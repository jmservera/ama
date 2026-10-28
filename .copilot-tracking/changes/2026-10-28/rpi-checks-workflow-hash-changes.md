---
title: Local gate workflow pin correction changes
description: Implementation and validation evidence for the stale deployment pin
ms.date: 2026-10-28
---

Task: rpi-checks-workflow-hash. Declared implementation scope: P01.
Plan and phase details use the same slug under their 2026-10-28 directories.
Single critique: Complete / Pass, no findings. Original artifacts preserved.

## P01: Correction and focused validation

P01-T01 complete: extended only the existing pin test with all real pin/key
assertions and a positive fixture preflight followed by exact per-name drift
checks. Baseline runner suite: 30 tests passed.

The first red run exposed both the stale deployment pin and missing command
ledger rows in the new positive fixture branch. Corrected the test's mocked
command to record its group, preserving the runner's no-empty-evidence rule.
The second red run failed only for actual src-deploy.yml pin inequality;
all five intentional fixture-drift checks ran successfully.

P01-T02 complete: changed only the src-deploy.yml hash literal to the
raw-byte digest established in Research. Four other pins unchanged.
No workflow edits or .env access.

## Focused validation

* python3 -B -m unittest tools.test_rpi_checks -q: all 30 passed after
  correction, most recent 10.361s. Intentional fixture failures are expected
  test output, not suite failures.
* Real Runner.preflight(), no mocked probes, candidate snapshot and external
  output: passed Python 3.12.3, Node 24.21.0, Docker client/server, Bicep
  0.48.1, actionlint 1.7.12, ShellCheck 0.11.0, Trivy 0.76.0 and all five pins.
  Logs: /home/azureuser/.copilot/session-state/8062dee7-4253-4b34-9a7e-d09331b44436/files/workflow-pin-preflight-q48t336b.
  No CLI preflight-only option exists; this is not a full/partial receipt.
* Host Ruff was missing. Installed existing pinned Ruff 0.17.1 and mypy
  2.4.0 in an external session venv only. Initial Ruff invocation omitted
  the runner's --select E,F,I,B,UP --target-version py312 and reported nine
  unrelated baseline diagnostics; no source changes made for them.
  Canonical lint passed. Formatter corrected one added assertion's layout;
  final format check passed both files. Strict mypy passed both files.
* git diff --check passed; workflow diff against origin/main is empty.

## Remaining work and review readiness

P01 source implementation and P02-T01 original independent Review complete.
Review execution Complete / outcome Conformant, no findings; original record:
.copilot-tracking/reviews/logs/2026-10-28/rpi-checks-workflow-hash-review.md.
Reviewed source diff SHA256:
b3c34aa7c47053246becfbd72c70268c821f9104f361cd00ece81999677dc5e1.
Original Review is not repeated or promoted to hosted/human approval.

Main moved from 98b0bb98 to b6755bb5 during Review (merged unrelated
documentation PR #459). Read-only diff confirmed neither tooling source
nor any workflow changed; fast-forwarded this unpublished topic with
git merge --ff-only origin/main, preserving all work without history rewrite.

P02-T02 clean-commit gate/publication remains pending at this committed
snapshot. The complete --all gate will use external directory
/home/azureuser/.copilot/session-state/8062dee7-4253-4b34-9a7e-d09331b44436/files/workflow-pin-final-gate.
Keep that receipt authoritative and external; no later source commit merely
to copy a receipt. The PR will report final outcome and exact-head assessment.
No blockers or out-of-scope follow-up work currently known. No deployment,
workflow dispatch, .env access, private-data access or main push authorized.

## P02 publication: original full-gate base movement

The first --all run executed and passed all 17 required groups, including
real SQL, browser/axe, all four images/scans/SPDX and logo stress. Its final
identity check failed: main advanced to 5abc6c6b32c536ad933cd926850eb8a3d8220a77
(merged #515) during execution. This is a FAILED receipt, not publication
evidence, and cannot be resumed after a base/commit change.

Original receipt remains immutable at the external directory above,
receipt.json, for head 74fd1f48917c5f3ed32b694c990e522c33401036 and base b6755bb5.
Original independent exact-head assessment also remains external and conditional.
No push or PR occurred on that failed gate.

The new main changes infrastructure and documentation, not runner/test source
or workflows. Integrated it through an ordinary merge, preserving topic
history and original Review; the reviewed source diff is unchanged.
Fresh complete gate destination:
/home/azureuser/.copilot/session-state/8062dee7-4253-4b34-9a7e-d09331b44436/files/workflow-pin-final-gate-2.
This committed snapshot precedes that new gate; its outcome belongs to the
external receipt and publication record.

## P02 publication: blocked after the second full gate

The fresh --all run at head 1c65a7a5 again passed all 17 required groups
(192 command records). Final verification again rejected the receipt solely
because main advanced during execution, now to
bb6df04cef68cc3694a97238d002c732c3406d81 (merged #516).
The second FAILED receipt remains immutable in workflow-pin-final-gate-2.
Neither failed receipt establishes publication permission.

The latest main delta changes application code and documentation, not the
runner, its test or any workflow; all five workflow findings remain valid.
No pin/source correction is needed. A second independent committed-head
assessment found no findings at 1c65a7a5, conditional on a passing receipt;
it remains external at workflow-pin-exact-head-assessment-2.json.

Stop publication rather than bypass the exact-current-base contract or
repeat unbounded full gates while other PRs are merging. This is an external
coordination blocker, not a local test failure. No push or PR has occurred.
P02-T02 remains unchecked. Next action: reconcile current main in a stable
validation window, commit the candidate, rerun the complete gate, obtain
exact-head assessment, fetch/verify immediately before topic push and the
Refs #500 PR. Any later candidate invalidates previous assessments/receipts.
This final documentation-only commit records the blocked handoff, not a
passing final-head gate. Original Review remains Complete / Conformant at
its original bounded source assessment.

## Addendum 2026-10-28: second pin refresh (infra-plan.yml)

Merged #513 (commit after the original review) added the `INFRA_PLAN_ENABLED`
condition to `.github/workflows/infra-plan.yml`, so its pin drifted after the
original single-pin boundary (`src-deploy.yml` only). The pin was refreshed to the
raw-byte SHA256 `4240d803e33e68e63e03d201f241fa21101e2e260848c276b32817624cca6056`,
computed with `sha256sum` on the merged file. Validation: `python3 -m unittest
tools.test_rpi_checks` (30 tests) passes, including the per-workflow drift assertion.
The original review remains bounded to the `src-deploy.yml` pin; this addendum is
not a new full-gate pass.
