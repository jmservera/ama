---
title: Issue 1231 details r5 (unsupported hard link and committed-cleanup error boundaries)
ms.date: 2026-11-06
---

## Chronology statement (prospective)

Written about 13:59Z, before any rebase, test run or edit.

## Planned changes

* `src/core/src/zava_forward/core/ranking_publication.py`
  * New `class ArchiveStorageError(Exception)`: archive storage cannot be written; raised only by callers that translate `OSError` (the helper itself still propagates `OSError`).
  * In `publish`, compute the outcome (committed record, or the winner's record when `FileExistsError` made this caller the loser) inside a `try`. On any exception the owned stage is removed best effort and the primary exception propagates; a cleanup failure is attached with `add_note` (Python 3.12 floor) rather than replacing or silently losing it. On success, remove the stage with a small helper: `FileNotFoundError` means nothing is retained; any other `OSError` returns the outcome (written True for the committer, written False for the loser) plus `stage_retained` set to the stage base name. Amended after the critique below.
* `src/core/src/zava_forward/core/ranking_publication_runner.py`: after publish, when `stage_retained` is present append warning `stage_not_removed` and set `stage_retained`; status stays `published`.
* `src/core/src/zava_forward/core/store.py` `publish_ranking_snapshot`: wrap only the `publish` call with `except OSError as e` and raise `ArchiveStorageError` from it with a message such as "The ranking archive cannot be written (PermissionError, EPERM). It must be a local folder that supports hard links. Owner: your operator. Next action: ask them to check the archive location. Nothing was published." with no path. On `stage_retained`, audit as usual, `logging.warning` with the file name, and add `warning` to the response.
* `src/api/src/zava_forward/api/server.py`: add `except ranking_publication.ArchiveStorageError as e: return 503 {"error": str(e)}` ahead of the `PermissionError` mapping (import `ranking_publication` from core).
* `src/core/README.md`: one sentence on the committed-cleanup warning and the 503 manager response.

* Runner warning text states that the retained hidden file is a hard-link alias of the committed record and must not be modified; it is removed by an operator.

## Tests first

* Added after the critique: concurrent loser with a failing stage unlink returns the winner's metadata with `written` False and `stage_retained`; simultaneous `os.link` and unlink failure propagates the link error with a note; unlink `FileNotFoundError` reports no retained stage.

* `src/core/tests/test_ranking_publication.py`: real `os.link` with only `os.unlink` of the stage name failing (patched wrapper delegating to the real function otherwise); assert final bytes, written True, winner date, `stage_retained` file exists, no other file touched.
* `src/core/tests/test_ranking_publication_runner.py`: same fault through `run`; assert `published`, written, warning code, no refusal.
* `src/api/tests/test_ranking_publication_wiring.py`: manager POST with EPERM and ENOTSUP at real helper `os.link` returns 503 and not 403, no record, no audit entry, message has no archive path; partner role still 403; stage-unlink-failure POST returns 200 with `warning` and one `ranking_snapshot_published` audit entry.

## Checks (light)

`PYTHONDONTWRITEBYTECODE=1`, external caches under `/mnt/ama-gates/e1231-r5-r65-1106/`, read-only `/tmp/zf79venv/bin/python` with explicit `PYTHONPATH` to this worktree and printed `__file__`/SHA-256 proof. Core focused: `unittest` for the two ranking publication modules. API focused: wiring module with `PYTHONPATH=core/src:core/tests:api/src:api/tests:agents/tests` from `src`. Ruff check and format, mypy on edited core sources as the component pyproject configures. Record actual versions and counts.
