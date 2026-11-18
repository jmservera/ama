---
title: Failing-first evidence for unusable ranking archive paths (#1259)
description: Reproduced red-before/green-after evidence for the unusable archive path classification, with per-criterion proof status
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop, core filesystem logic only. No Azure, model or cloud call was made and no credential was read.

## Method

The fix and its regressions landed together in `cd687abad` (#1328), so the red state is reproduced by overlaying the current regression file onto the parent source.

* Detached worktree at `cd687abad^` (pre-fix `src/core`), current `src/core/tests/test_ranking_publication_runner.py` copied over it, worktree removed afterwards.
* Before: `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_ranking_publication_runner.UnusableArchivePathTests` ran 6 tests, `FAILED (failures=7)`. Failing: oserror-without-reason, regular-file exit through `main`, store status for a regular-file archive, and the all-operations test for four subcases (regular file, dangling link, dangling ancestor, stat failure). Representative assertion: `('problem', None, True) != ('problem', None, None)`, so the window was reported as overdue instead of unknown. The absent-directory tests passed before and after. Observed; raw output not retained.
* After (current main source): the same class ran 6 tests, `OK`; `test_ranking_publication_runner` plus `test_ranking_publication` ran 110 tests, `OK`.

## Per-criterion status

| Criterion | Status | Evidence |
| --- | --- | --- |
| Distinguish creatable absence from non-directory, dangling link, stat failure | Proven (already ticked) | `_names` and `_require_creatable` in `ranking_publication.py`; tests above |
| Unknown window and existing unreadable shape, no healthy-empty fallback | Proven (already ticked) | `check_unknown` asserts `problem`/`refused archive_unreadable`, `due` and `next_window_start` null |
| Preserve absent-directory first run and path-free diagnostics | Proven (already ticked) | absent-directory tests pass; path-free assertions |
| Regular-file and dangling-link regressions plus absent coverage; failure before fix | Proven here (red-before run: Observed; raw output not retained) | Method and Before/After above |
| Original RPI, current FULL receipt, independent exact-head assessment, hosted checks | Not provable for the demo | This lane changes no `src` code, so FULL is not triggered and `rpi-checks.py --all` was not run (brief). An external receipt, independent assessment and hosted CI for a future head are human/CI gates outside this local candidate; the owner's demo decisions do not waive them. The criterion stays unticked |

Limits: the mocked stat failure and the check/use race are not real-filesystem proofs; the coordinator's earlier record of unrepresented items stands.
