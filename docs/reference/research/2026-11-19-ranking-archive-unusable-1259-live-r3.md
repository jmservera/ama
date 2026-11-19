---
title: Live-demo re-observation of unusable ranking archive paths (#1259), run 3
description: Fresh red-before and green-after output for the unusable archive path regressions, with per-criterion proven/unproven status
ms.date: 2026-11-19
---

Scope: synthetic demo, desktop only, core filesystem logic. No Azure resource, model call or credential was used or read; the owner's Azure authorisation was not exercised because the behaviour is local path classification. Repeats [run 2](2026-11-18-ranking-archive-unusable-1259-live-r2.md) on main `1dddac2e0`.

## Red-before (pre-fix source `cd687abad^`, current test file)

Detached worktree, current `test_ranking_publication_runner.py` and `ranking_blob_fixture.py` copied over, `UnusableArchivePathTests` run, worktree removed. Output excerpt, temporary path elided:

```text
Ran 6 tests in 0.068s
FAILED (failures=7)
FAIL: test_oserror_without_a_reason_is_reported_without_the_path   (path appears in the problem text)
FAIL: test_regular_file_archive_exits_nonzero_through_main         AssertionError: 0 != 1
FAIL: test_store_status_is_a_problem_for_a_regular_file_archive    AssertionError: [] is not true
FAIL: test_unusable_archive_is_unknown_for_every_operation_and_writes_nothing
      [regular_file] [dangling_link] [dangling_ancestor] [stat_failure]
      Tuples differ: ('problem', None, True) != ('problem', None, None)
```

## Green-after (main `1dddac2e0`)

`cd src/core && PYTHONPATH=src:tests python3 -m unittest test_ranking_publication_runner test_ranking_publication -q`: `Ran 110 tests ... OK`.

## Per-criterion status

| Criterion | Status |
| --- | --- |
| Distinguish creatable absence from non-directory, dangling link, stat failure | Proven (ticked) |
| Unknown window and unreadable shape, no healthy-empty fallback | Proven (ticked) |
| Preserve absent first run and path-free diagnostics | Proven (ticked) |
| Regular-file and dangling-link regressions plus absent coverage; failure before fix | Proven: seven failures before, all pass after |
| Original RPI, FULL receipt, independent exact-head assessment, hosted checks | Not provable for the demo: no `src` change, `rpi-checks.py --all` not run, no push, so no hosted run or independent assessment of a head exists. Stays unticked |

Limit: the stat failure is mocked, not a real-filesystem proof.
