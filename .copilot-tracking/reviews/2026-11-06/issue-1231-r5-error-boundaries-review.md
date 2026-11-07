---
title: Issue 1231 author review r5 (unsupported hard link and committed-cleanup error boundaries)
ms.date: 2026-11-06
---

## Execution

Author-only Review, executed once after the fix commit `2c4f7c3d8` and after the GREEN, Ruff, format and mypy runs recorded in the changes file. It reread `git diff eb42ee276..2c4f7c3d8` (seven source and test files) against the two findings. It is not an independent review and does not replace the pending independent whole-feature review.

## Findings disposition

* Finding 3 (hard link EPERM/ENOTSUP became 403 or an unhandled error): resolved on light evidence. The helper still raises the `OSError` unchanged (existing helper and runner characterizations pass). Only `Store.publish_ranking_snapshot` translates it, around the single `publish` call, to `ArchiveStorageError`; `server.py` maps that class to 503 before the `PermissionError` 403 mapping. Tests assert 503 for both errnos, a path-free actionable message, an empty archive, no audit entry, the partner role still 403 and a later publish still succeeding.
* Finding 4 (cleanup failure after commit lost the outcome): resolved on light evidence. The committer and the concurrent loser both return their truthful metadata with `stage_retained`; the runner reports `published` with a warning; Store audits and returns a path-free warning. The stage is kept, nothing is overwritten, no rollback or silent swallowing. When link and unlink both fail, the link error propagates with a note.
* Earlier critique items (loser, masking, ENOENT truthfulness) are covered by tests.

## Observations and residual risks

* Every `OSError` in the Store publish call becomes a 503 storage failure, including plain write permission and `makedirs` errors. This is intentional (a storage condition, not authorization) but broader than hard-link support alone; the message names the error class and errno.
* The operator log line for a failed write contains the OS error string, which can include the archive path; it is an operator log, not the response.
* The `BaseException` handler re-raises and only adds a note; it does not swallow.
* `store.py` and `server.py` are outside Ruff and mypy gating, so the new lines there were checked only by tests.
* Hard-link EPERM and ENOTSUP are injected, not a real unsupported mount. Light tools are not the project pins and the venv is not isolated.
* The two prospective files carry estimated clock times that exceed the real commit time; the changes file records the correction.

## Outcome

Conformant for the two scoped findings on light evidence only. Not a Pass for the feature: fresh combined FULL on the rebased head, independent whole-feature review, hosted CI and publication remain pending. No acceptance criterion is ticked and no closing keyword is used (`Refs #1231`).
