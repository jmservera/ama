---
title: Issue 1259 ranking archive path health research
description: Prospective original Research for reporting unusable ranking archive paths as unknown
ms.date: 2026-11-08
---

## Scope and status

* Task: issue 1259 (jmservera/ama), original RPI, FULL tier. Branch fix/ranking-archive-path-health, based on f548b65f4 (current main, tree 32ec) and deliberately stacked on the fix/ranking-archive-ancestor-durability (issue 1258) topic. Planned PR target is the 1258 branch while stacked; body parent 79 is unchanged.
* Research disposition: executed (static reading only). Planning Readiness: Ready for a prospective plan; implementation is gated on the frozen 1258 source (see plan).
* Evidence is static source reading. No test, execution, gate, model, cloud or private-data access was performed. The finding is not an executed reproduction or crash proof.

## Issue data (read with gh issue view 1259; treated as data)

* Medium. Unusable archive paths can appear empty and readable in the ranking runner.
* Acceptance: distinguish an absent creatable directory from an existing non-directory, dangling link or stat failure; unusable inputs use the existing archive-unreadable problem/refusal shape and an unknown window state with no healthy-empty fallback; preserve first-run absent-directory support and path-free diagnostics; regular-file and dangling-link regressions for schedule, verify and publish plus absent-directory coverage that fail before the fix; original RPI, current FULL receipt and verification, independent exact-head assessment, hosted checks.
* Dependencies: parent 79; depends on corrected 79/1231 integration, which reached main through 1239 (code present at f548b65f4). That does not accept 79, 1231, 440 or any human, acceptance-test, model or Azure gap. The checkpoint 1267 CONTINUE disposition stands. The earlier 79 PR is merged; its closed PR and history are not reused.

## Source findings (static, f548b65f4)

* ranking_publication.py `_names()` (line 201): `if not os.path.isdir(archive_dir): return []`. `isdir` is False for a regular file, a dangling symlink, a stat failure (for example EACCES on an ancestor) and a genuinely absent path. All four become an empty list.
* `verify()` (line 208) therefore returns count 0, no problems, latest None for all four.
* ranking_publication_runner.py `_verify()` (line 82) only maps a raised OSError to `{"unreadable": True, "problems": [...]}` using `type(e).__name__` and `e.strerror`, which is path-free for OSError. Nothing raises for the non-directory cases, so:
  * schedule: unknown=False, due=True, exit 0 (source-derived, not executed).
  * verify: overdue True with no unreadable problem and no unknown state.
  * publish: skips the `archive_unreadable` refusal and proceeds toward capacity and `publish()`.
* Existing runner tests (StorageAndDuplicateFindingTests, lines 480 to 506) cover only an `os.listdir` PermissionError with an existing directory. No test covers regular file, dangling link or absent-directory control by name.
* `publish()` creates the directory with `os.makedirs(..., exist_ok=True)`, so absent-directory first-run is a required preserved behavior.
* The runner `os.path.exists(os.path.join(archive_dir, name))` call in publish is only reached after the archive check passes, so it needs no change.

## Candidate fix (smallest behavior-preserving)

Classify in `_names()` instead of `isdir`:

* `os.stat` succeeds and is a directory: list as today.
* `os.stat` succeeds and is not a directory: raise NotADirectoryError (OSError subclass, strerror "Not a directory").
* `os.stat` raises FileNotFoundError: `os.lstat`; if lstat raises FileNotFoundError the path is genuinely absent, return []; if lstat succeeds it is a dangling symlink, raise a path-free OSError (ENOENT with strerror "Dangling symbolic link").
* Any other OSError from stat (EACCES, ELOOP, ENOTDIR from an ancestor file) propagates.

The existing runner `_verify()` mapping then yields the unreadable shape, unknown window (due None, next window None), `archive_unreadable` refusal and no write. `ranking_publication_runner.py` should need no change; it is owned only if a mapping gap appears. Direct callers of `ranking_publication.verify()` and `overdue()` (check with grep at implementation) gain a raised OSError instead of an empty result, which is the intended fail-closed change and must be listed in the changes record.

## Relationship to 1258 and propagation

* Both 1258 and 1259 edit ranking_publication.py; 1258 owns publish/_fsync_dir/_confirmed, 1259 owns `_names`. Hunks are expected to be disjoint, but this is unverified until the 1258 candidate is frozen.
* The 86 and 123 worktree diffs described in the review file are snapshots before current-source reconciliation; they are not followed blindly.
* Review input: ranking-followups-review-1108.md in the coordinator session files (bounded evidence, read-only).

## Open items

* Exact frozen 1258 head and tree are not yet known.
* Whether other `ranking_publication` callers (API wiring, store status) rely on empty-for-missing: to be grepped after propagation.
* Platform note: dangling-link and permission tests use temporary synthetic fixtures; a stat-failure case is simulated with a patched `os.stat`, not a live permission change (mocked, not live-filesystem proof).
