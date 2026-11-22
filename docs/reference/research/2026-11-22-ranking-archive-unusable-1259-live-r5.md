---
title: Live-demo re-observation of unusable ranking archive paths (#1259), run 5
description: Fresh red-before and green-after output for the unusable archive path regressions on main 6fd6e3f838, with per-criterion proven/unproven status
ms.date: 2026-11-22
---

Scope: synthetic demo, desktop only, local filesystem classification. No Azure resource, model call or credential was used or read. Source is unchanged (documentation and tracking only), so the FULL tier is not triggered and `rpi-checks.py --all` was not run.

## Red-before

Detached worktree at `cd687abadd^` (pre-fix), current `test_ranking_publication_runner.py` and `ranking_blob_fixture.py` copied in, `UnusableArchivePathTests` run, worktree removed:

```text
Ran 6 tests in 0.072s
FAILED (failures=7)
FAIL: test_oserror_without_a_reason_is_reported_without_the_path
FAIL: test_regular_file_archive_exits_nonzero_through_main
FAIL: test_store_status_is_a_problem_for_a_regular_file_archive
FAIL: test_unusable_archive_is_unknown_for_every_operation_and_writes_nothing [regular_file]
FAIL: ... [dangling_link]
FAIL: ... [dangling_ancestor]
FAIL: ... [stat_failure]
```

## Green-after (main `6fd6e3f838`)

`cd src/core && PYTHONPATH=src:tests python3 -m unittest test_ranking_publication_runner test_ranking_publication -q`: `Ran 110 tests in 9.944s`, `OK`. The absent-directory controls (`test_absent_directory_stays_creatable_for_first_run`, `test_absent_folder_below_a_link_to_a_real_folder_is_creatable`) are in that run.

## Per-criterion status

| Criterion | Status |
| --- | --- |
| Distinguish creatable absence from non-directory, dangling link, stat failure | Proven |
| Unknown window and unreadable shape, no healthy-empty fallback | Proven |
| Preserve absent first run and path-free diagnostics | Proven |
| Regular-file and dangling-link regressions plus absent coverage; failure before fix | Proven: seven failures before, all pass after |
| Original RPI, FULL receipt, independent exact-head assessment, hosted checks | Unproven for the demo: no `src` change, nothing pushed, no hosted run for this head, no independent assessment |

Limit: the stat failure is mocked, not a real-filesystem proof.
