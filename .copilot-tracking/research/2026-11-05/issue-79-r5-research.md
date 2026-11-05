---
title: Issue 79 research, continuation r5 (clean frozen candidate)
ms.date: 2026-11-05
---

## Identity and pins

* Task: `issue-79-r5-clean-candidate`, parent `issue-79-r4-publication-runner` (earlier research, plan, implementation and Review outcomes preserved unchanged).
* Branch `feat/ranking-publication-runner-79`, head `f4e62db42ca502aed2441cd5c6738d94e2bea6ac`. `origin/main` (fetched 2026-11-05) is `ead177ef90d24666557708ea344848a1be43bdf8` and an ancestor of the head. Target parent topic: `feat/case-workbench-integration-73`.
* Research disposition: `executed`. Planning Readiness: `Ready`.

## Findings

* The earlier "clean" summary was inaccurate: `git status --short --ignored` listed 13 ignored generated directories (`__pycache__` x8, `*.egg-info` x3, `src/core/.mypy_cache`, `src/core/.ruff_cache`). No untracked or modified tracked file existed. No full receipt exists.
* The [tracking retention policy](../../../docs/reference/method/tracking-retention-policy.md) requires a finite per-run manifest, no glob or age rules, and archive/restore backing; it grants no deletion authority beyond the selection. Its archive contract is written for tracking snapshots; these paths are regenerable, git-ignored build output, so the same discipline was applied at file level and a hash archive was kept as backing.
* Pip editable installs for `zava-forward-core/agents/api` resolve to the main checkout `/home/azureuser/source/ama/src/*`, not this worktree. The worktree `egg-info` directories were created at 07:55 on 2026-11-05 by a worktree-local metadata build and are not the installed record.
* Worktree creation time (mtime of `.git` file) is 07:53:44; every candidate file is newer, owned by the current user, a regular file, untracked and git-ignored.
* Heavy lock `/tmp/ama-rpi-heavy.lock`: holder #96, pid 1232396, `python3 tools/rpi-checks.py --all --base ead177ef... --out /tmp/ama-96-gate-r7 --lock-timeout 0` (observed with `ps`, 27 minutes elapsed at the time). The Chromium prerequisite sequencing that failed the #188 gate is being fixed by #1208 (reported by the owner, not verified here).

## Typing question (mypy override)

* The override added in `f4e62db42` puts `zava_forward.core.ranking_publication_runner`, `test_ranking_publication_runner` and `tests.test_ranking_publication_runner` into an existing block that sets only `disallow_untyped_calls = false`. It does not set `ignore_errors` and does not exclude the module; `strict = true` still applies otherwise. The separate `ignore_errors = true` block lists neither the new module nor its test.
* Evidence (mypy 2.4.1, external cache): full `python -m mypy` from `src/core` reports `Success: no issues found in 268 source files`, with both new files listed as found sources. With a scratch copy of the config (outside the repo) that omits the three override entries, mypy reports 15 errors in the two files, all `no-untyped-call`, because the callees (`ranking_publication`, `Store`, helpers in the test harness) are not yet typed. No other error code appears. So the override relaxes exactly one strict check at the untyped migrated boundary, as the other entries in that block already do; the new module is otherwise strictly checked.
* Limits: this shows strict coverage apart from untyped-call checking, not full type safety; calls into untyped siblings are unchecked. The installed mypy (2.4.1) differs from the pin `mypy==2.4.0`; the gate venv result governs.
