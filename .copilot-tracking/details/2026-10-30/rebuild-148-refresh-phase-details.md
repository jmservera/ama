---
title: Rebuild 148 refresh phase details
description: Task context and completion boundaries
ms.date: 2026-10-30
---

Task: pr-511-refresh-2026-10-30. Planning readiness: ready after PC-001.
Research C1-C4/W1-W2 is adequate; no additional research or plan-authoring
worker is needed for this small, tightly coupled integration.

<!-- rpi:phase id=P01 -->
## P01: Integrate main
<!-- rpi:task id=P01-T01 -->
### P01-T01: Rebase and resolve

Original head d18fc2f998b5ebccf021be8cb0b7bac1d5999c67, main
91e890e07af036263316c153cbc7ceff780cdaa2. Worktree initially clean;
new untracked dated RPI files are this task's own inputs, not owner changes.
Run git rebase origin/main. During rebase, ours is main and theirs is replayed
topic, so do not select conflict sides mechanically. Preserve both prose
entries; restore main rubric/manifest explicitly if necessary. Compare final
topic source/tests against their original blobs and check main ancestry.
Completed: rebase succeeded without conflicts; range-diff shows both patches
equal and main is an ancestor. Main rubric/manifest/index/log and original
orchestrator source/tests/evidence preservation checks all pass.

<!-- rpi:phase id=P02 -->
## P02: Validate and record
<!-- rpi:task id=P02-T01 -->
### P02-T01: Run targeted local checks

Requested venv exists with Python 3.12.3 and Ruff 0.17.1. Use project cwd for
configured mypy/Ruff. Python import path includes each project's src/tests
and sibling core/agents paths. Run orchestrator discovery, core
test_scenario_manifest and dependency rules; API dependency/workbench modules
as applicable. Scenario source hashes changed on main, so validation is
mandatory even if no conflict occurs. Do not regenerate main's manifest.
No full API suite without successful flock -n /tmp/ama-rpi-heavy.lock true;
prefer no full API suite at all for this source-preserving refresh.
Full publication gate is separate and cannot be claimed from focused checks.
Completed: Ruff, format and mypy pass in orchestrator/core/API; 68
orchestrator, 10 core and 5 API targeted tests pass without skips. Both local
CLI modes and 25 migration tests pass. No dependencies or source were changed.

<!-- rpi:phase id=P03 -->
## P03: Review and commit
<!-- rpi:task id=P03-T01 -->
### P03-T01: Independent Review and local handoff

Review exact refresh boundary and full branch diff against main, not original
RV-001 closure. Write one review artifact, route findings forward, preserve
original 2026-10-27 evidence. Use authenticated id/login-derived email for both
author and committer. Commit with Conventional Commit, Refs #148 and required
trailer. Coordinator pushes; do not invoke remote writes.
Post-commit full gate must use external output, and a prerequisite/lock failure
is a publication blocker rather than a passing receipt. No new Azure access.
For PC-001: after commit, fetch origin main, bind the reviewed main SHA and
run `python3 tools/rpi-checks.py --all --base <reviewed-main-sha> --out <new-external-directory>`.
On success fetch main again and run
`python3 tools/rpi-checks.py --verify-receipt <receipt.json> --base <current-origin-main-sha>`.
Record both actual outcomes. If main, candidate or other bound inputs changed,
the receipt is invalid; reconcile within scope and run a fresh gate or report
the blocker. The coordinator owns final prepublication verification and
independent exact-head assessment.
At Review handoff: only Review, local evidence commit and gate attempt remain;
there is no pending source implementation.
Administrative current-main continuation after the one Review: ffd8f35e adds
only unrelated training dependency-lock updates. Rebase is conflict-free,
both original patches remain equal and the same three project validation
commands pass again. Original Review remains Complete / Residual work at its
original boundary; no second Review or exact-final-head approval is inferred.
