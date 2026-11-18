---
title: Issue 164 / PR 1641 full-gate failure correction research
date: 2026-11-17
---

## Scope

Candidate HEAD 66f38c916 (base 6d7e6da4a). Full gate receipt
`/home/azureuser/.local/share/ama/gates/1641-2027/receipt.json` (retained, not overwritten) failed:

1. browser: `AssertionError: single reset clears every queue override and selection`
   (src/api/checks/workbench_browser_check.py ~699, log 0147-browser.log).
2. project-core: timeout 124 at 1800 s in the Core suite (3288 tests done; second time in
   test_sensor_scenarios after test_sensor_reproducibility_111 the first time).

Research disposition: executed. Findings are appended below.

## Findings

Method: gate venv python (`venvs/api`, `venvs/core`) with `PYTHONPATH` pointing at either a clean detached
worktree of origin/main 6d7e6da4a (`/tmp/ama-main-1117`) or this candidate; raw logs copied to
`/home/azureuser/.local/share/ama/phase-witness/1641-fix-20261117T2112/`. Runs were sequential. Machine load
average was 3 to 5 on 4 CPUs (shared host), which the gate also experienced.

### Browser: single reset assertion

* Clean main: `design_system_browser_check` passed (1 of 1, then 8 of 8 more, 3 of 3 with a forced 0.4 s server delay, 2 of 2 with a 1.5 s delay on the last filter request).
* Candidate: failed once (first run after the gate, same assertion), then passed 4 + 8 + 15 + 10 (under 4 busy CPU loops) + 25 + 6 (cold, no bytecode) runs. A debug print placed before the assertion on a passing run showed every asserted condition true.
* `app.js` diff against main touches only hazard/safeguarding clock rendering and the safety panel (`workSummary`, `caseView` open hazards, `safetyPanel`). The `#reset-queue` handler, `listState`, `defaultListState` and the list `load` path are unchanged. `checks/workbench_browser_check.py` is unchanged.
* Conclusion: not a deterministic regression and no app.js reset defect found. Two failures in about 75 candidate runs (0 in about 17 on main) are consistent with an intermittent timing race in the check (`wait_cases(page, 2)` can be satisfied by the pre-reset DOM while a hash change is pending); the stale-DOM hypothesis is unproven because it could not be reproduced on demand. No source change is justified.

### Core timeout

* `test_installed_cli_success_failure_and_check_failure_exit` alone: 1.3 s on main, 1.6 s on candidate. It is not a hang.
* Whole Core suite, sequential, same command as the gate (`unittest discover -s tests -v`): main 3529 tests in 1085 s; candidate 4059 tests in 1535 s (rc 1 on both, one identical failure `test_discovery_assistant_demo...test_demo_runs_from_this_worktree_without_inputs`, caused by my `PYTHONPATH` harness rather than an installed package; skips 424 vs 428).
* The candidate adds 530 Core tests (+42 % wall time). Gate timeout is 1800 s; the gate run reached 3288 of 4059 tests in 1800 s, about 25 % slower than this run, because of host contention. The candidate runs the suite in 1535 s on a quiet-ish host, leaving 15 % headroom. The two stall points (test_sensor_reproducibility_111, then test_sensor_scenarios) are positions in a uniform slow run, not hangs.
* Conclusion: slowness caused by the added test volume plus host load. Minimal remedy is a gate setting (suite timeout of at least 3600 s, or sharding Core) in `tools/rpi-checks.py`; this changes gate semantics and is reported to the coordinator, not applied.

Planning Readiness: Ready (no source defect found; record-only outcome).
