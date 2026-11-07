---
title: Issue 79 changes, continuation r15
ms.date: 2026-11-06
---

Task `issue-79-r15-d654-review-corrections`. Planning commit `e88bf6b10fc67a89595d8a90ee763b906ca15bf9` precedes every test and source edit.

## Changed files

* `src/core/src/zava_forward/core/ranking_publication.py`: unique temp file, file fsync, `os.link` first-writer-wins, directory fsync, own temp removed in `finally`; `_existing` validates a record at the final name (parse, snapshot equality, hash, name, date) and raises `PublicationError` instead of returning `written` False for a damaged file.
* `src/core/src/zava_forward/core/store.py`: audit detail and response carry `policy_signed`; status turns a listing `OSError` into a problem entry and derives `overdue` from one result.
* `src/core/tests/test_ranking_publication.py`, `src/api/tests/test_ranking_publication_wiring.py`: regression tests. Two existing assertions changed deliberately: the edited-record test now expects `PublicationError` and unchanged bytes (old behavior was the reviewed defect), and the no-delete guard now permits exactly one `os.unlink(tmp)` of the writer's own temp file.
* `src/core/README.md`: durability, validation, run key and same-window semantics.

## Evidence (external logs under `/tmp/79-r15-1106/`)

| Check | Command (from `src/core/tests` or `src/api`) | Exit | Result |
| --- | --- | --- | --- |
| RED core | `python -m unittest test_ranking_publication` (`red2-core.log`) | 1 | 20 tests, 7 failures, 4 errors |
| RED api | discover `test_ranking_publication_wiring.py` (`red5-api.log`) | 1 | 15 tests, 2 failures, 1 error |
| GREEN core | publication and runner modules (`green3-core.log`, rerun after format) | 0 | 49 tests OK |
| GREEN api | wiring module (`green3-api.log`) | 0 | 15 tests OK |
| Ruff check and format, mypy | pinned ruff 0.17.1, mypy 2.4.0 from `/tmp/79-align-r13-1106/venv` | 0 | clean, 268 files |

Early log files `red1-*.log` and `red3-*.log` record my own invocation mistakes (wrong interpreter, wrong test path) and are kept. The first GREEN run (`green1`) failed on an import line I mangled; `green2` showed one wrong test string; both are preserved.

## Finding map

* HIGH 1: fsync test, race test with real `os.link`, four-process race test.
* HIGH 2: unusable-record test (garbage, truncated, empty, non-mapping, different snapshot, bad date), edited-record test, API corrupt-file test with audit assertion.
* MEDIUM: unsigned audit/response test, status `PermissionError` test, README for run key and window.
* LOW: tests added as listed.

## Limits

* Light, focused checks only; no FULL, SQL, browser or heavy lock (held by #81). The r14 FULL is historical for `d654634f`; the corrected head needs a fresh FULL and independent re-review.
* The helper's temp file is created `0600`, so archived records are owner-only where they were umask-default before; noted for deployment review.
* Not changed: store's own ranking-snapshot cache `.tmp`, `as_of` validation, non-directory archive paths, #1231 manual API.
