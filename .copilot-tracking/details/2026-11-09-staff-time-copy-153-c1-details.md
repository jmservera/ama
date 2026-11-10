---
title: Issue 153 C1 project mypy details
ms.date: 2026-11-09
task_id: 153-c1-project-mypy-1109
---

## Exact edit set

`src/api/tests/test_timecapture_copy.py`, in red-log order:

* line 192: `TimeCapture(...)` constructor call
* line 194: `self.time.request_enable(SUPPORT)`
* line 195: `self.time.activate(PAM)`
* line 197: `self.time.acknowledge(SAM)`
* line 198: `App(...)`
* line 252: `served.time.mine(SAM)`

Each gets a trailing `# type: ignore[no-untyped-call]`; `ruff format` may reflow. All 12 tests and assertions are preserved.

## Acceptance

* `cd src/api && mypy` exits 0 with no unused-ignore error over the same 204 files.
* 12 tests OK with `ZF_BROWSER_TESTS=1`; 12 run and 5 skipped without it.
* Affected existing suites pass; ruff clean; diff limited to the one test file plus tracking.
