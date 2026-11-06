---
title: Issue 79 changes, continuation r10
ms.date: 2026-11-06
---

Prospective Research, Plan and details were committed first at `16d939be7ab19035d01f4d8dc863e4c697fd5736`, before any test or source edit. Earlier r4 to r9 records, logs, receipts and the independent assessment files are unchanged. The r9 FULL receipt (SHA-256 `2ac8174cc73644d847c7f9e6c93ff37f46d633d1997e27e514f1efb3a5db1a4a`) covers head `fe414bb71e24` only and is historical for the new head.

## Changes

* `src/core/src/zava_forward/core/ranking_publication_runner.py`: `load_cases` requires each case to be a mapping with a boolean `closed` and raises `TypeError` otherwise (F1); `schedule` returns status `problem` when archive problems exist, with due, latest and any approval refusal kept (F2); the capacity check is skipped only when the exact target file already exists (F3); `today` of `9999-12-31` is refused as `bad_date` before arithmetic, and an archived latest of `9999-12-31` gives `next_window_start` of `None` plus one problem line, so schedule is `problem` and publish refuses with `archive_unverified` (F4).
* `src/core/tests/test_ranking_publication_runner.py`: five new tests in `AssessmentFindingTests`, one per behaviour above plus the unchanged valid paths. The CLI helpers moved from `CliAndStoreTests` to the shared `RunnerBase` so the new class can use them; the existing tests are unchanged.
* `src/core/README.md`: runner paragraph states the new behaviour.
* Edit method: the source and helper-move edits were applied with a small Python script (found strings replaced once each), not the edit tool; the diff is the evidence.

## Findings to evidence

| Finding | Regression test | RED before fix | GREEN after |
| --- | --- | --- | --- |
| F1 closed flags | `test_malformed_closed_flags_refuse_the_whole_source` | `TypeError not raised` for each of six values | pass |
| F2 schedule health | `test_schedule_is_a_problem_when_the_archive_does_not_verify` | `current` instead of `problem` | pass |
| F3 identical retry | `test_verified_identical_retry_needs_no_new_capacity` | `capacity_missing`, no `written` key | pass |
| F4 today max | `test_latest_representable_date_is_refused_without_a_traceback` | `OverflowError` for all three operations | pass |
| F4 archived latest max | `test_archived_latest_without_a_next_day_is_a_problem_not_a_crash` | `OverflowError` | pass |

## Commands (all under `/tmp/79-functional-r10-1106/`, each a new path, stdin from /dev/null where relevant)

All run from `src/core` with `PYTHONDONTWRITEBYTECODE=1` and `/tmp/zf79venv/bin/python`. Installed Ruff 0.17.3 and mypy 2.4.1 differ from the maintained pins 0.17.1 and 2.4.0, so these are not pinned full results. The mypy override on the runner module still relaxes only untyped-call checks.

| Log | Command | Exit | Result |
| --- | --- | --- | --- |
| `red1.log` | `-m unittest discover -s tests -p test_ranking_publication_runner.py -k AssessmentFindingTests` | 1 | RED: 5 tests, 7 failures and 6 errors, before the fix |
| `green1.log` | `-m unittest discover -s tests -p 'test_ranking_publication*.py' -v` | 0 | 41 tests OK |
| `ruff1.log` | `-m ruff check --no-cache` on the two runner files | 1 | adverse: E501 at runner line 198; preserved |
| `format1.log` | `-m ruff format --check --no-cache` on the two runner files | 1 | adverse: one file to reformat; preserved |
| `green2.log` | same selector | 0 | 41 tests OK |
| `ruff2.log`, `format2.log` | Ruff check and format check on `.` | 0, 0 | pass |
| `mypy2.log` | `-m mypy --cache-dir` under the log dir | 1 | adverse: 7 errors (helper reuse via class attributes, and `next_start` typing); preserved |
| `green3.log`, `ruff3.log`, `format3.log` | after moving helpers to the base and typing `next_start` | 0, 0, 0 | pass |
| `mypy3.log` | mypy | 1 | adverse: one missing annotation in the new test; preserved |
| `green4.log`, `ruff4.log`, `format4.log`, `mypy4.log` | final run after annotating the loop variable | 0, 0, 0, 0 | 41 tests OK; Ruff and format pass; mypy success over 268 files |

The final source state was checked by the `*4` logs. The `*1` to `*3` failures are first failures and were not overwritten.

## Not run

Gate (any tier), SQL, browser, Docker, install, scan, lock acquisition, cloud, API tests, cleanup or deletion. The corrected head needs a fresh FULL gate and a fresh independent reassessment. Named policy-owner signoff, Legal retention, scheduler activation and retained scheduled operation remain unproven. #79 stays open; the eventual child publication targets #73 with `Refs #79`.
