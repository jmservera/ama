---
title: Issue 153 C1 project mypy changes
ms.date: 2026-11-09
task_id: 153-c1-project-mypy-1109
---

## Changes (implemented 2026-11-09T23:37Z, after plan and critique)

* `src/api/tests/test_timecapture_copy.py`: added `# type: ignore[no-untyped-call]` to the six calls reported by hosted mypy (`TimeCapture(...)`, `request_enable`, `activate`, `acknowledge`, `App(...)`, `mine`). The `TimeCapture` database path moved to a local `db` so the line stays within the 100-column limit. No assertion, test or behaviour changed; all 12 tests preserved.
* Untouched: mypy configuration, legacy `TimeCapture`/`App`, JS, backend, shared files.

## Validation (raw logs in `/tmp/zf-153-1109/logs/`, prefix `c1-`)

| Check | Result |
| --- | --- |
| Exact `cd src/api && mypy` before (venv Python 3.12.3, mypy 2.4.0) | `c1-mypy-red.log`: 6 errors, 204 files, exit 1; matches hosted run 42719465214 |
| Same command after | `c1-mypy-green.log`: Success, 204 files, exit 0 |
| `ruff format --check .` and `ruff check .` | exit 0 and exit 0 |
| New tests without browser env | 12 run, OK, 5 skipped |
| `test_timecapture` 26, `test_content_standard` 18, `test_workspace_scripts` 5, `test_static_assets` 5, `test_role_screens` 8 | all OK |
| `node --check timecapture.js`, `git diff --check` | exit 0 |
| Five served-browser cases | NOT RUN in C1: `flock -n /tmp/ama-rpi-heavy.lock` refused twice (exit 1) at 23:37:04Z and 23:37:28Z; holder was the 1238 MSSQL run from worktree `issue-1238-manual-verified-1109` (`c1-admission-holder*.txt`). No queue, spin, kill or waiver. The last browser run at cc77ea457 passed 12 of 12 (`new-tests-final.log`); this change is comment-only for runtime. |

## Disclosure

Cause of the miss: the original check was a single-file mypy run, not the project command. No JS changed, so no new web review.
