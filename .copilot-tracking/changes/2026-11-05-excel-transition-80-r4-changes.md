---
title: Issue 80 round 4 changes
description: Current-main preparation
ms.date: 2026-11-05
---

Changed: one ordinary no-ff merge commit `96795d87618a89c152c4ee655177914d0a38353f` (parents `ce5ba5728054d92a7fde8a710e089329bb0d45da` and `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`), no conflicts, no rebase, amend or force. No application, web or test edit; the child-owned files are identical to round 3. This round adds only r4 tracking evidence.

## Light validation (not FULL)

Tools: Python 3.12.3, ruff 0.17.3, mypy 2.4.1, node check. `PYTHONDONTWRITEBYTECODE=1`, ruff `--no-cache` with external `RUFF_CACHE_DIR`, mypy caches under `/tmp/r4-80-*` (left in place, not deleted).

* The installed `zava_forward` distributions resolve to `/home/azureuser/source/ama/src/*`, another checkout. I used the worktree `src/*/src` and test directories on `PYTHONPATH` (no `mvp`), and printed `quality.py` and `server.py` paths under this worktree before testing. No package was installed.
* api `test_list_export_api`, `test_role_endpoint_inventory`, `test_loading_feedback`: 37 OK. core `test_list_export`: 4 OK.
* ruff check and format check on api and core: clean. mypy (tests included) api 186 files and core 266 files: clean. `node --check web/ops.js`: OK.
* Ignored-inclusive status after the checks: only the three untracked r4 evidence files, no ignored files.

## Preserved adverse outcomes

* Round 3 `case_journey_browser_check` failure at "320x800 summary within one viewport scroll (1676.40625)", identical with and without the child. Main now carries #1219 for that contract, but it was not re-run (no browser gate allowed), so it is neither confirmed fixed nor closed.
* Round 3 full-gate admission failed ("Global heavy-resource lock timeout"; first attempt blocked by ignored caches). Now the #96 runner holds the lock; no admission was attempted.
* The round 3 review was author-only.

## Not run

FULL receipt, independent exact-head review, hosted CI, browser, Docker, SQL.
