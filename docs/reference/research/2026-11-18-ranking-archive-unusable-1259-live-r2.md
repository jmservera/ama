---
title: Live-demo audit of unusable ranking archive paths (#1259), run 2
description: Real-filesystem and red-before evidence with retained output, plus per-criterion proven/unproven status for issue 1259
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only, core filesystem logic. No Azure resource, model call or credential was used or read; the owner's Azure authorisation was not exercised because the behaviour under test is local path classification. Builds on [run 1](2026-11-18-ranking-archive-unusable-1259-failing-first.md), whose gaps were that raw output was not retained and that the stat failure was mocked.

## Method

* Red-before: a detached worktree at `cd687abad^` (pre-fix `src/core`) received the current `test_ranking_publication_runner.py`; the `UnusableArchivePathTests` class was run; the worktree was then removed.
* Real-filesystem repro: a synthetic signed registry (a copy of the shipped policy with a placeholder owner, signed in memory only) and three archive inputs in a temp folder: an existing regular file, a dangling symlink and an absent creatable folder. Each of `schedule`, `verify` and `publish` was run through `runner.run` on the pre-fix and the current source with `--today` 2026-11-05. The script was a throwaway and is not committed.

## Red-before output (pre-fix source, current tests)

Abridged excerpt of the run; the full console log was not saved.

```text
Ran 6 tests in 0.151s
FAILED (failures=7)
FAIL: test_oserror_without_a_reason_is_reported_without_the_path
FAIL: test_regular_file_archive_exits_nonzero_through_main          AssertionError: 0 != 1
FAIL: test_store_status_is_a_problem_for_a_regular_file_archive     AssertionError: [] is not true
FAIL: test_unusable_archive_is_unknown_for_every_operation_and_writes_nothing [regular_file]
FAIL: ... [dangling_link]     Tuples differ: ('problem', None, True) != ('problem', None, None)
FAIL: ... [dangling_ancestor] (same tuple)
FAIL: ... [stat_failure]      (same tuple)
```

The tuple shows the window reported overdue (`True`) instead of unknown (`None`).

## Green-after output (current main, `19dc0ef87`)

`UnusableArchivePathTests`, `test_ranking_publication_runner` and `test_ranking_publication` together: `Ran 116 tests ... OK`.

## Real-filesystem repro output

Observed; raw output not retained. The table below is a summary, and the throwaway script was not kept.

| Input | Operation | Pre-fix | Current |
| --- | --- | --- | --- |
| regular file | schedule | status `due`, 0 problems | status `problem`, 1 problem, window unknown |
| regular file | verify | `problem`, overdue `True`, 0 problems | `problem`, overdue null, 1 problem |
| regular file | publish | refused `publish_failed`, 0 problems | refused `archive_unreadable`, 1 problem |
| dangling link | schedule | `due`, 0 problems | `problem`, 1 problem, window unknown |
| dangling link | verify | `problem`, overdue `True`, 0 problems | `problem`, overdue null, 1 problem |
| dangling link | publish | refused `publish_failed`, 0 problems | refused `archive_unreadable`, 1 problem |
| absent folder | schedule | `due` | `due` (unchanged) |
| absent folder | verify | overdue `True`, 0 problems | overdue `True`, 0 problems (unchanged) |
| absent folder | publish | `published`, folder created | `published`, folder created (unchanged) |

After every run the regular file and the dangling link were left untouched (not replaced by a folder); the absent folder was created only by `publish`. Pre-fix, the two unusable inputs were classified as a healthy empty archive that was due, which is the defect in the issue.

## Per-criterion status

| Criterion | Status | Evidence |
| --- | --- | --- |
| Distinguish creatable absence from non-directory, dangling link, stat failure | Proven (ticked) | Repro table; `_names` and `_require_creatable` in `ranking_publication.py`; stat failure covered by mocked test only |
| Unusable inputs report the unreadable shape and unknown window; no healthy-empty fallback | Proven (ticked) | Repro table: 1 problem, `archive_unreadable` on publish, overdue/due null |
| Preserve absent-directory first run and path-free diagnostics | Proven (ticked) | Absent-folder rows unchanged; path-free assertions in the tests; the pre-fix path-leak failure is in the red output |
| Regular-file and dangling-link regressions for schedule/verify/publish, absent coverage, failure before fix | Proven by the tests and the abridged red-before excerpt above; the real-filesystem table is observed, raw output not retained | Red-before and green-after runs; real-filesystem table |
| Original RPI, FULL receipt, independent exact-head assessment, hosted checks | Unproven; not provable for the demo | No `src` change in this lane, so FULL is not triggered and `rpi-checks.py --all` was not run. The receipt, an independent assessment and hosted CI for a publishing head are CI and human gates; commit check-runs on `cd687abad` show only an unrelated agentic workflow, so no source CI result is observed for that SHA from here. Not waived by the demo decisions |

Production-only items: none. The Blob archive variant (`--blob`) was not exercised; it uses a different adapter and needs a configured account, which is outside this issue's path-classification scope.

Limits: the stat-failure case is mocked, not a real permission fault; the check-then-use race on a path changing between classification and use is not tested.
