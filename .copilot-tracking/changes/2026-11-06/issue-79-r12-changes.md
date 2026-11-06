---
title: Issue 79 changes, continuation r12
ms.date: 2026-11-06
---

Prospective Research, Plan and details were committed first at `79d86e272bc980b8452c4914c5636888cde8b65b`, before any test or source edit. Earlier r4 to r11 records, logs, receipts and the independent assessment files are unchanged. No earlier FULL receipt (r9 `fe414bb7`, whole-feature `b7f6186d`) covers the corrected head.

## Changes

* `src/core/src/zava_forward/core/ranking_publication_runner.py`:
  * new `_verify` wrapper turns an `OSError` from archive enumeration into a result with `count` 0, `latest` None, `unreadable` True and one problem line naming the exception; used by `verify`, `schedule` and `publish`.
  * `verify` returns status `problem` with `overdue` None when unreadable; `schedule` returns `problem` with `due` and `next_window_start` None; `publish` refuses with `archive_unreadable` and permissions guidance.
  * the `free_bytes` call is wrapped; an `OSError` becomes a `capacity_missing` refusal naming the error. The capacity comparison and the existing-record skip are unchanged.
  * before `ranking.snapshot`, a repeated case `id` is refused as `source_invalid` with a next action. The ranking algorithm, `load_cases` and the helper are untouched.
* `src/core/tests/test_ranking_publication_runner.py`: four tests in new `StorageAndDuplicateFindingTests`, using the existing fixtures and CLI helpers.
* `src/core/README.md`: runner paragraph names `archive_unreadable`, repeated case ids and an unreadable free-space probe.
* Edit method: native edit tool.

## Findings to evidence

| Finding | Regression test | RED before fix | GREEN after |
| --- | --- | --- | --- |
| 1 listdir PermissionError | `test_unreadable_archive_is_a_problem_never_empty_or_healthy` (run), `test_unreadable_archive_exits_nonzero_through_main` (CLI) | `PermissionError` escapes | pass |
| 1 capacity OSError | `test_capacity_probe_failure_is_a_refusal_not_a_traceback` (run and CLI via `shutil.disk_usage`) | `OSError` escapes | pass |
| 2 duplicate ids | `test_duplicate_case_identity_is_source_invalid_before_ranking` (run and CLI) | `StopIteration` from `ranking.py:160` | pass |

## Commands and exits (all under `/tmp/79-functional-r12-1106/`, from `src/core`, `PYTHONDONTWRITEBYTECODE=1`, `/tmp/zf79venv/bin/python`)

* `red1`: `-m unittest discover -s tests -p test_ranking_publication_runner.py -k StorageAndDuplicate`, exit 1, 4 tests, 4 errors, each for the stated reason.
* `green1`: `-m unittest discover -s tests -p "test_ranking_publication*.py"`, exit 0, 45 tests. `ruff1` exit 1 (E501, test line 411) and `format1` exit 1 (same line), preserved. `mypy1` exit 0.
* After wrapping that one test line with the edit tool: `green2` exit 0 (45 tests, 0 skips), `ruff2` exit 0 (`ruff check --no-cache`), `format2` exit 0 (`ruff format --no-cache --check`), `mypy2` exit 0 (268 files, `--cache-dir` under `/tmp`). Installed Ruff 0.17.3 and mypy 2.4.1 differ from the pins, so these are not pinned-tool results.
* The README sentence was added after `green2` and affects no code. Not run: gate, SQL, browser, Docker, install, scan, lock, cloud, push, cleanup or deletion.

## Limits

* Light, author-run checks only. The corrected head needs a fresh FULL gate and a fresh independent whole-feature assessment. Named policy-owner signoff, Legal retention and scheduled retained operation remain unproven. #1231 findings 3 and 4 are untouched and sequenced after this parent.
