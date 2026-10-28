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
