---
title: Issue 1259 ranking archive path health details
description: Phase details for the prospective archive path health fix
ms.date: 2026-11-08
---

## Phase 2.1 Propagation

* `git fetch` origin; confirm the coordinator-supplied frozen 1258 head. Merge it normally into fix/ranking-archive-path-health. Record head, tree and merge result. Re-read `_names`, `verify`, `overdue` in the merged file.
* grep callers: `ranking_publication.verify`, `overdue`, `_names` across src/ (runner, API wiring, store status, tests) and list any reliance on empty-for-missing.

## Phase 2.2 Tests (synthetic temporary fixtures only)

In ScheduleAndVerifyTests/StorageAndDuplicateFindingTests style, reusing RunnerBase, `signed_registry()` and `open_cases()`:

* Regular file at the archive path: `self.archive.write_text("x")`.
* Dangling symlink: `os.symlink(self.root / "missing", self.archive)`.
* Stat failure: `patch("os.stat", side_effect=PermissionError(13, "Permission denied"))` scoped to the archive path (wrap to delegate other paths), labelled as a mocked case.
* For each: `verify` gives status problem, latest None, one problem containing the OSError name, overdue None; `schedule` gives status problem, due None, next_window_start None; `publish` gives refused with `archive_unreadable`; archive path unchanged (file content intact, symlink still dangling, nothing created); assert no str(self.root) in problems or refusal text.
* Dangling ancestor (PC-001): archive at `link/archive` where `link` is a dangling symlink; and the control where `link` is a symlink to an existing directory (creatable, first run).
* Exercise (PC-002): `publish` with `exercise=True` keeps the existing convention (exempt from the refusal, never writes). Test asserts written False, nothing created, problems list the unreadable archive and due/next window None.
* Store caller (PC-004): add one `Store.ranking_publication_status` case for a regular-file archive asserting a problem (not healthy). Its `overdue=True` for unreadable is pre-existing for PermissionError and is recorded as a residual follow-up, not widened here.
* Path-free (PC-005): a runner case where `_names` raises `OSError` without strerror asserts the problem text carries no temporary path.
* Control: absent directory: schedule due True with next window today; publish creates the record (existing first-run tests may already cover publish; add a named explicit absent control for schedule/verify).
* One CLI case through `main`: verify and schedule exit 1, publish exit 2 for the regular file.
* Red: run the new tests before the fix and record the failures.

## Phase 2.3 Source

In `_names(archive_dir)`: stat; on FileNotFoundError lstat the path; if that is also FileNotFoundError, walk to the nearest ancestor that lstat finds and require `os.stat` on it to succeed and be a directory (a dangling or non-directory ancestor raises; a real directory or a symlink to one means absent and creatable, return []) (PC-001). If lstat succeeds the path is a dangling symlink (raise `OSError(errno.ENOENT, "Dangling symbolic link")` without the path argument); non-directory raises `NotADirectoryError(errno.ENOTDIR, "Not a directory")` without the path; other OSError propagates. Keep the sort/filter unchanged. Add `import errno` only if needed. Update the `verify()` docstring to say it raises OSError for an unusable archive path.

In ranking_publication_runner.py `_verify()` replace the `e.strerror or str(e)` fallback with a fixed path-free phrase (PC-005); this is the only runner change planned.

## Phase 2.4 Selectors

From src/core with the installed distributions: `PYTHONPATH=tests python3 -m unittest test_ranking_publication_runner test_ranking_publication -q` (PC-003; tests has no package initializer and imports dataset top-level; use the same command for red and green), plus the API ranking wiring selectors if the caller grep finds a dependency. Do not run until phase 2.1 is done.

## Gate commands (later)

Fetch main, commit implementation and original RPI evidence, then `python3 tools/rpi-checks.py --all --base <origin/main sha> --out <new external dir>` (add `--stack` heads of the 1258 and 1259 candidates so the receipt identifies stack members, PC-007) and `--verify-receipt <receipt.json> --base <current origin/main sha>`. Any later commit invalidates the receipt.
