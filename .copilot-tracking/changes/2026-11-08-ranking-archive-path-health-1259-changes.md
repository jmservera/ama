---
title: Issue 1259 ranking archive path health changes
description: Changes record for the LIGHT source and regression preparation on the frozen 1258 parent
ms.date: 2026-11-08
---

## Scope and base

* Child fix/ranking-archive-path-health; planning head abc142fb (tree d088b597); plan-update commit 33b18c26; one normal merge (no rebase, reset or amend) of the frozen parent fix/ranking-archive-ancestor-durability 26b4ea391d6a6000e9be8fc6f78994e52a6d0f6c (tree c9c7c239) into it, merge-tree dry run conflict-free. Main f548b65f4 unchanged. Target stays the 1258 branch.
* LIGHT source/regression preparation only. No FULL, receipt, independent assessment or hosted check.

## Changes

* src/core/src/zava_forward/core/ranking_publication.py: `_names()` replaces `os.path.isdir` with stat. A directory is listed; an existing non-directory raises NotADirectoryError; on FileNotFoundError the new `_require_creatable()` walks lstat to the nearest existing ancestor and treats the path as absent (empty, creatable) only if that ancestor stats as a directory, otherwise raises a path-free OSError (dangling link, non-folder ancestor). Any other stat error (for example PermissionError) propagates. `verify()` docstring states the contract.
* src/core/src/zava_forward/core/ranking_publication_runner.py: `_verify()` fallback text `str(e)` replaced by a fixed phrase so an OSError without strerror cannot expose a path (PC-005). No other runner change was needed: the existing OSError to unreadable mapping gives unknown window, archive_unreadable refusal and no write.
* src/core/tests/test_ranking_publication_runner.py: class UnusableArchivePathTests (6 tests): regular file, dangling link, dangling ancestor and mocked stat failure across verify, schedule, publish and exercise (overdue/due/next window None, archive_unreadable, exercise written False with problems shown, path-free, filesystem unchanged); CLI exit codes 1/1/2; path-free fallback; absent-directory and link-to-real-folder controls; Store.ranking_publication_status regular-file case.

## Red before fix (raw)

External log red.log. Command (installed out-of-tree pre-fix copy): `python -m unittest discover -s tests -p test_ranking_publication_runner.py -k UnusableArchivePathTests`. Result: Ran 6 tests, FAILED (failures=7): oserror-without-reason (path leaked in problem text), CLI exit 0 != 1, Store problems [] is not true, and four subtests regular_file/dangling_link/dangling_ancestor/stat_failure `('problem', None, True) != ('problem', None, None)`. The two absent-directory controls passed pre-fix. An earlier run with wrong control status text ("ok" vs "due") was a test error, corrected before the red record.

## Green and checks (external logs, scratch g1259-parent26b4-source-light-1108)

* Import origin proven: non-editable install from a git-tracked export into an out-of-tree venv; modules resolve under the venv site-packages; synthetic ZF_DATA; external pip cache and TMPDIR; no PYTHONPATH workaround for core.
* ranking_publication tests: Ran 90, OK (includes the 1258 regressions). Full core discover: Ran 2418, OK, skipped=226 (core-green.log; skips not individually analysed). API ranking selectors (policy, wiring, scale): Ran 53, OK. Agents test_cohort_ranking_eval: Ran 20, OK. ruff check and format check on src/core pass; git diff --check clean.
* One invocation mistake: the first API selector run without the tests directories on PYTHONPATH gave 3 import errors; rerun with the documented PYTHONPATH passed.

## Divergences and residuals

* Exercise stays exempt from the refusal (PC-002 decision) but now exposes unreadability and unknown window.
* PC-004 preserved: Store.ranking_publication_status still reports overdue True and its `e.strerror or e` fallback is unchanged (pre-existing, out of scope); only a problem-not-healthy test was added.
* Parent residuals R1 to R6 (writable-parent heuristic, boundary coverage, API-fault) are preserved untouched.
* Stat failure is a mocked case, not live filesystem proof; the check/use race between stat and listdir is not addressed; other stat errors (ELOOP, ENOTDIR) propagate as OSError and map to unreadable.
* Static finding only; no production incident or executed crash proof is claimed.
