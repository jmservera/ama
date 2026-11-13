---
title: Issue 74 retained focused validation of frozen candidate f50c5c7fd
description: Retained execution results for the read-only building scope display delta; synthetic unit checks only
ms.date: 2026-11-13
---

Scope: frozen candidate `f50c5c7fdd179e4d3c187130afbdf1e369983992`, tree `65e39a2821c95f13a9a5375ab5bea633688273ef`, base `15bfee2d7`. Worktree `issue-74-retained-validation-0518`, branch `test/demo-home-scope-74-0518`. Candidate source is unchanged: this commit adds only this file. Raw outputs are external in `/tmp/ama-74-retained-0518/` (`*.cmd`, `*.out`, `*.err`, `*.exit`, `identity.txt`, `provenance.out`, `browser-blocked-memory.txt`).

Environment: system `python3` 3.12 with `PYTHONPATH=src:../core/src:../agents/src:tests:../core/tests:../agents/tests`, cwd `src/api`. Module provenance: `checks.home_case_browser_check` and `building_fixture` resolve under this worktree. The namespace packages `zava_forward.api` and `zava_forward.core` list this worktree first and the stale primary editable install (`/home/azureuser/source/ama`) second. Nothing was installed.

| Check | Exit | Result |
| --- | --- | --- |
| `node --check src/zava_forward/api/web/app.js` | 0 | no output |
| `ruff check checks/home_case_browser_check.py` | 0 | All checks passed |
| `ruff format --check checks/home_case_browser_check.py` | 0 | 1 file already formatted |
| `mypy checks/home_case_browser_check.py` | 0 | no issues, 1 source file |
| `python3 -m unittest tests.test_home_case_api -v` | 0 | 6 run, 0 failures, 0 errors, 0 skips |
| `python3 -m checks.home_case_browser_check` | not run | blocked, see below |

Browser blocked: `/tmp/ama-rpi-heavy.lock` had no holder (`fuser`), but `MemAvailable` was about 4.52 GiB with no swap, below the documented worker budget in `src/README.md` (four GiB per worker plus one GiB headroom, five GiB). The largest consumer is a foreign long-running Copilot process (PID 4648, about 8.8 GiB RSS), which was not touched. No lock was taken, nothing was queued or polled, and no condition was lowered. Resume condition: a later explicit coordination event with at least 5 GiB available, then nonqueued ownership of the heavy lock for the whole run and one synthetic run with `ZF_AXE_JS` set only if the pinned axe asset already exists.

Not established: browser behavior, axe, base-red behavior, human, assistive-technology or WCAG acceptance. Earlier six-test, browser and lint claims remain author-reported except as re-observed above. Publication is blocked on the browser run.
