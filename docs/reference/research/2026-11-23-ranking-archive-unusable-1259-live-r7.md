---
title: Live-demo re-observation of unusable ranking archive paths (#1259), run 7
description: Fresh red-before and green-after output for the unusable archive path regressions on main 342fad401d, with the live-revision applicability check and per-criterion status
ms.date: 2026-11-23
---

Scope: synthetic demo, desktop only. Local filesystem classification plus a read-only Azure listing. No credential was used, no Azure resource was created or changed. Source is unchanged, so the FULL tier is not triggered and `rpi-checks.py --all` was not run.

## Red-before

Detached worktree at `cd687abadd^` (pre-fix), current `test_ranking_publication_runner.py` and `ranking_blob_fixture.py` copied in, `UnusableArchivePathTests` run, worktree removed:

```text
Ran 6 tests in 0.048s
FAILED (failures=7)
FAIL: test_oserror_without_a_reason_is_reported_without_the_path
FAIL: test_regular_file_archive_exits_nonzero_through_main
FAIL: test_store_status_is_a_problem_for_a_regular_file_archive
FAIL: test_unusable_archive_is_unknown_for_every_operation_and_writes_nothing [regular_file]
FAIL: ... [dangling_link]
FAIL: ... [dangling_ancestor]
FAIL: ... [stat_failure]
```

## Green-after (main 342fad401d)

`cd src/core && PYTHONPATH=src:tests python3 -m unittest test_ranking_publication_runner test_ranking_publication -q`: `Ran 110 tests in 6.115s`, `OK`, including the absent-directory first-run controls.

## Live revisions

`az containerapp revision list` shows `ca-cutover-test-demo-api--0000054` active (image `zava-forward-api`) and `ca-resident-demo--0000026` active (image `zava-resident-demo`). The Container Apps jobs in resource group `ama` are load, audit, orch, live-simulator and live-receiver; no ranking publication job is deployed (`infra/README.md` records the runner as an operator CLI). The live revisions therefore neither exercise nor can disprove the archive classification; the local tests are the applicable proof.

## Per-criterion status

| Criterion | Status |
| --- | --- |
| Distinguish creatable absence from non-directory, dangling link, stat failure | Proven (local tests) |
| Unknown window and unreadable shape, no healthy-empty fallback | Proven (local tests) |
| Preserve absent first run and path-free diagnostics | Proven (local tests) |
| Regular-file and dangling-link regressions plus absent coverage; failure before fix | Proven: seven failures before, 110 pass after |
| Original RPI, FULL receipt, independent exact-head assessment, hosted checks | Unproven and process-gated: no `src` change, nothing pushed, no hosted run or independent assessment for this head |

Limit: the stat failure is mocked, not a real-filesystem proof.
