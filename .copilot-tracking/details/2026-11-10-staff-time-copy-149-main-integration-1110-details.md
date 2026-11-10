---
title: Parent 149 component-only main integration details
ms.date: 2026-11-10
task_id: 149-copy-main-integration-1110
---

## Commands (venv `/tmp/zf-149-1110/venv`, raw logs `/tmp/zf-149-1110/logs/`)

Environment for every Python command: `cd src/api`, `PYTHONPATH=tests:../core/tests:../agents/tests`, `PATH=/tmp/zf-149-1110/venv/bin:$PATH`. No `ZF_DATA`, credentials, provider or Azure variable set; `ZF_BROWSER_SCRATCH` unset.

| Step | Command | Pass condition |
| --- | --- | --- |
| V1 | `python -c "import zava_forward.api, zava_forward.core, zava_forward.agents"` and `pip list` | all three resolve under this worktree; Ruff 0.17.1, mypy 2.4.0, Playwright 1.64.0 |
| V2 | `python -m unittest test_timecapture_copy -v` without browser flag | 12 run, 5 skipped (shows the skips are opt-in only; not accepted as evidence) |
| V3 | `flock -n /tmp/ama-rpi-heavy.lock env ZF_BROWSER_TESTS=1 python -m unittest test_timecapture_copy -v` | exit 0, 12 run, 0 skipped, all 5 browser cases ran. Lock busy: exit 1, no queue, spin or kill; record exact pending step |
| V4 | `python -m unittest test_timecapture test_content_standard test_workspace_scripts test_role_screens test_static_assets -v` | all OK, 0 skipped in required scope (skips, if any, listed by id and reason) |
| V5 | `ruff check .` and `ruff format --check .` from `src/api` | exit 0 |
| V6 | `mypy` from `src/api` (project config, not single-file) | exit 0 |
| V7 | `node --check src/zava_forward/api/web/timecapture.js` and `git diff --check` | exit 0 |
| V8 | blob identity: `git rev-parse HEAD:<path>` for the two product files | equal to parent blobs `14e0b5ad...` and `f7cac3ac...` |

Tests in V4 that opt into browsers run in V3 only when the lock is held once; V4 does not set `ZF_BROWSER_TESTS`, so any browser-gated skip inside it is listed and judged against the selected scope (the five component cases are in V3).

Not run, by design: full API suite, full local gate, SQL, mssql store tests needing SQL, Azure, provider, private data, axe, assistive technology.

## Stop rules

* Merge conflict, unexpected unrelated parent source, or a shared-hook path (server, app, roles, store, procurement, sqlstore, Core hooks) changed by the parent: STOP, record exact evidence, do not resolve by invention.
* Lock busy: record holder read and exit code, no retry loop; resume needs an actual resource change.
* Any skipped selected test blocks a ready claim.
