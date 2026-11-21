---
title: Live-demo re-observation of unusable ranking archive paths (#1259), run 4
description: Fresh red-before and green-after output for the unusable archive path regressions on main d2585a4c9, with per-criterion proven/unproven status
ms.date: 2026-11-21
---

Scope: synthetic demo, desktop only, core filesystem logic. No Azure resource, model call or credential was used or read; the owner's Azure authorisation was not exercised because the behaviour is local path classification. Repeats [run 3](2026-11-19-ranking-archive-unusable-1259-live-r3.md) on main `d2585a4c9`.

## Red-before (pre-fix source `cd687abad^`, current test files)

Detached worktree, current `test_ranking_publication_runner.py` and `ranking_blob_fixture.py` copied over, `UnusableArchivePathTests` run, worktree removed:

```text
Ran 6 tests in 0.213s
FAILED (failures=7)
FAIL: test_oserror_without_a_reason_is_reported_without_the_path
FAIL: test_regular_file_archive_exits_nonzero_through_main
FAIL: test_store_status_is_a_problem_for_a_regular_file_archive
FAIL: test_unusable_archive_is_unknown_for_every_operation_and_writes_nothing [regular_file]
FAIL: ... [dangling_link]
FAIL: ... [dangling_ancestor]
FAIL: ... [stat_failure]
```

## Green-after (main `d2585a4c9`)

`cd src/core && PYTHONPATH=src:tests python3 -m unittest test_ranking_publication_runner test_ranking_publication -q`: `Ran 110 tests in 2.151s`, `OK`.

## Per-criterion status

| Criterion | Status |
| --- | --- |
| Distinguish creatable absence from non-directory, dangling link, stat failure | Proven (ticked) |
| Unknown window and unreadable shape, no healthy-empty fallback | Proven (ticked) |
| Preserve absent first run and path-free diagnostics | Proven (ticked) |
| Regular-file and dangling-link regressions plus absent coverage; failure before fix | Proven: seven failures before, all pass after |
| Original RPI, FULL receipt, independent exact-head assessment, hosted checks | Unproven, not provable for the demo: no `src` change, so FULL is not triggered and `rpi-checks.py --all` was not run; nothing is pushed, so no hosted run or independent assessment of a head exists |

Limit: the stat failure is mocked, not a real-filesystem proof.
