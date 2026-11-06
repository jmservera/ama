---
title: Issue 79 details, continuation r12
ms.date: 2026-11-06
---

## P01 commit planning records

* Commit only the r12 research, plan and details before any test or source edit.

## P02 regression tests (RED first)

* Allowed diff: `src/core/src/zava_forward/core/ranking_publication_runner.py`, `src/core/tests/test_ranking_publication_runner.py`, README runner paragraph only if necessary, and new dated r12 records (changes, review, state).
* Tests in a new `StorageAndDuplicateFindingTests` class, reusing `RunnerBase`, `cli`, `registry_patched`, `cases_file`, `open_cases` and `signed_registry`:
  * archive enumeration failure: patch `os.listdir` with `unittest.mock.patch` to raise `PermissionError`, for `verify`, `schedule` and `publish` through `run`, and `verify` and `schedule` through `main`; assert status, exit code, problem line or refusal code, `due` None for schedule, and no archive file written.
  * capacity probe failure: `free_bytes` callback raising `OSError` through `run`; and through `main` by patching `ranking_publication_runner._free_bytes` is not possible once bound as a default, so patch `shutil.disk_usage` to raise `OSError`; assert refusal `capacity_missing`, exit 2, no archive file.
  * duplicate cases: the same open case twice, through direct `run` and through the CLI cases file; assert `source_invalid`, JSON on stdout, exit 2, no archive file.
* RED run: one command, one fresh log, direct exit code recorded. Failures must be for the stated reasons (traceback or wrong status), not test mistakes; a test that fails for a test mistake is corrected and the first failure preserved.

## P03 minimal corrections

* Add a runner helper wrapping `ranking_publication.verify` that converts `OSError` into a result with `count` 0, `latest` None, one problem line (exception type and strerror) and `unreadable` True. Use it at the verify operation and at the schedule/publish call site.
* `verify` operation: `overdue` None when unreadable; status `problem`.
* Schedule and publish: `due` and `next_window_start` None when unreadable; `publish` adds refusal `archive_unreadable` with permissions and location guidance; the existing `archive_unverified` refusal is not duplicated.
* Wrap the `free_bytes` call in an `OSError` handler returning `capacity_missing` with the error type and guidance.
* In the existing source-invalid `try`, before `ranking.snapshot`, refuse a repeated `id` with `source_invalid`.
* No change to `load_cases`, the helper, `ranking.py`, policy, scheduling or README unless the runner paragraph becomes false.
* Edits use the native edit tool.

## P04 checks, Changes, Review

* Light commands only, from `src/core`, with `PYTHONDONTWRITEBYTECODE=1` and `/tmp/zf79venv/bin/python`: `-m unittest` for `test_ranking_publication` and `test_ranking_publication_runner`; Ruff `--no-cache` check and format check; mypy with `--cache-dir` under `/tmp`. Each writes to a fresh log under `/tmp/79-functional-r12-1106/`; exit codes are recorded directly; a retry gets a new path.
* Not run: gate, SQL, browser, Docker, install, scan, lock, cloud, push, cleanup or deletion.
* Changes and state are written and validated (JSON, links, diff) before the Review; the Review is author-only, created after the checks, with no human-review box checked, and any later validation gets a supplement.
* Wording: no closing keyword, `Refs #79`, no acceptance claim; the r9 receipt and the b7f receipt do not cover the corrected head.
