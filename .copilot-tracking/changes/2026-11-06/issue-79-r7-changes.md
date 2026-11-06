---
title: Issue 79 changes, corrective continuation r7
ms.date: 2026-11-06
---

## Changes

* `src/core/src/zava_forward/core/ranking_publication.py`: private `_valid_date` (str type guard, ASCII `[0-9]{4}-[0-9]{2}-[0-9]{2}` full match, real calendar check with `calendar.monthrange`, year at least 1). `publish` uses it for `published_on` and refuses before writing with the existing `PublicationError`. `verify` records `"{name}: publication date is not a valid calendar date."` and excludes the value from `latest`. `datetime` is not imported because an existing guard test (`test_module_has_no_clock_and_no_delete`) forbids the word; that test is unchanged. The `as_of` check is unchanged.
* Tests added to `tests/test_ranking_publication.py` (verify with `2026-11-31`, `20261011`, empty, null, number, list, trailing newline, Arabic-Indic digits; no trusted latest; publish refusals before writing) and `tests/test_ranking_publication_runner.py` (verify, schedule and publish consistency on `2026-11-31`, malformed types, valid-date scheduling unchanged).
* No runner source change: with a trusted `latest`, the existing schedule, publish (`archive_unverified`) and verify paths report the problem. Valid archive bytes, names, idempotence and policy boundaries are unchanged.
* Manual-edit note: the first source edit was applied with a short Python replace script rather than the edit tool; the final regex change used the edit tool. Content is the same either way.

## Chronology

Research, plan and details were committed as `91f7792dda7f4e4b821a413ded372794cbf27648` (2026-11-06 01:08:22Z) before the first test or source edit. The original r4 failure is not repaired.

## Actual commands (from `src/core`, `/tmp/zf79venv/bin/python`, `PYTHONDONTWRITEBYTECODE=1`; raw logs in `/tmp/i79-r7-logs/`)

| Step | Command | Exit | Result |
| --- | --- | --- | --- |
| Import identity | print `__file__` of the runner and test modules, `zava_forward.core.__path__` | 0 | all under this worktree's `src/core` |
| RED 1 | `python -m unittest discover -s tests -p 'test_ranking_publication*.py'` (`red.log`) | 1 | 36 run, 13 failures, 5 errors |
| GREEN 1 | same (`green.log`) | 1 | one failure: the existing no-clock guard rejected `import datetime`; fixed by using `calendar` |
| Review finding | code-review: `\d` and `$` accept non-ASCII digits and a trailing newline | n/a | RED 2 added |
| RED 2 | same (`red2.log`) | 1 | 36 run, 7 failures |
| GREEN | same (`green2.log`) | 0 | 36 tests OK |
| Ruff | `ruff check --no-cache` on the 3 files, external `RUFF_CACHE_DIR` (`ruff2.log`) | 0 | pass |
| Format | `ruff format --no-cache --check` (`format2.log`) | 0 | 3 files formatted |
| mypy | `python -m mypy --cache-dir <external>` (`mypy2.log`) | 0 | no issues in 268 files |
| api wiring | from `src/api`: `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p 'test_ranking_p*.py' -q` (`api.log`) | 0 | 25 tests OK |

Qualifications preserved: installed Ruff 0.17.3 and mypy 2.4.1 differ from the maintained pins 0.17.1 and 2.4.0, so these are not pinned full results; the runner module's override relaxes only untyped-call checking, so untyped callees stay unchecked and this is not full type safety. The exact coordinator reproduction was covered by the test fixtures, not re-run against a separate scratch archive.

## Missing evidence

* No fresh FULL receipt on the resulting head; #185 owns the sole heavy run (gate a7d4, `/tmp/g185-full-r9-1106`). None was started or prepared.
* No independent exact-head assessment, publication review, hosted CI or human approval.
* Open: named policy-owner sign-off and actual scheduled and retained publication (#79 criteria 3 and 4). A local runner proves neither. Use `Refs #79`.
