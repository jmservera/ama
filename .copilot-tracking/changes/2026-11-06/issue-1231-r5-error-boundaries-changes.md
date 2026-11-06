---
title: Issue 1231 changes r5 (unsupported hard link and committed-cleanup error boundaries)
ms.date: 2026-11-06
---

## Chronology (actual, from git)

* Prospective research, plan, details, critique and state were committed as `17b4e19d0` (author and committer time 13:57:22Z) before any rebase, test run or source edit. Correction: the approximate clock times written inside those prospective files (about 13:56Z to 14:01Z) were my estimates; the later ones exceed the real commit time. The commit timestamp, not those estimates, is authoritative. The files are unchanged.
* Backup ref `refs/heads/backup/issue-1231-b7f6186-pre-r65-rebase` created at `b7f6186dc1c7357f255c7d54da30b501ea5ba111` (it did not exist before).
* Rebase `--onto 43080ab42a96fada36b9d0bc523dfa16fe0c3cd5 397419724e68b24bce879512a24c7df430177f87` of the seven child commits plus the r5 planning commit completed without conflicts. Replayed hashes: planning `eb42ee276`, R2 records `1b6640434`, R2 tests `f7718d1da`, `ccf398d51`, R1 records `c6d5534bd`, R1 fix `df0f2ede7`, R1 research `1e0872d0d`. Committer on replayed commits is the repository-local noreply identity. Original bytes and lineage remain in the backup ref. Rebase touched no other branch or worktree.
* Tests first, RED, correction, GREEN (below), then the fix commit `2c4f7c3d8` (13:59:41Z), then this record, the separate review and state.

## RED (new tests, unchanged source, rebased head `eb42ee276`)

* Core `test_ranking_publication` plus `test_ranking_publication_runner`: exit 1, 59 tests, 2 failures and 3 errors (`/mnt/ama-gates/e1231-r5-r65-1106/red-core.log`).
* API `test_ranking_publication_wiring`: exit 1, 14 tests, 2 failures (EPERM and ENOTSUP subtests) and 1 error (`red-api.log`).

## Changes

* `ranking_publication.py`: new `ArchiveStorageError`; `publish` computes the outcome, removes only its own stage with `_remove`, returns `stage_retained` (base name) when the stage could not be removed after a committed or loser outcome, keeps the primary exception and attaches a note when cleanup also fails. `FileNotFoundError` on cleanup means nothing is retained.
* `ranking_publication_runner.py`: `stage_retained` field and `stage_not_removed` warning; status stays `published` or `already_published`.
* `store.py` `publish_ranking_snapshot`: only around `publish`, `OSError` is logged and raised as `ArchiveStorageError` with a path-free actionable message; success audit and a path-free `warning` when a stage is retained.
* `server.py`: `ArchiveStorageError` returns 503 ahead of the `PermissionError` 403 mapping. Role checks and global handling unchanged.
* `README.md`: documents the 503 and the retained-stage warning.
* Tests: five core tests (committed cleanup failure, loser cleanup failure, no masking, stage already gone, runner warning) and two API tests (EPERM and ENOTSUP 503 with no record and no audit, plus manager success still works and `sam` still 403; committed cleanup failure is audited and reported).

## GREEN and checks

Interpreter `/tmp/zf79venv/bin/python` 3.12.3, read-only, with `PYTHONPATH` set to this worktree's `src/core/src`, `src/core/tests`, `src/api/src`, `src/api/tests`, `src/agents/tests`. Import proof (`import-proof-green.log`): `ranking_publication.py`, `store.py` and `server.py` import from this worktree, SHA-256 of ranking_publication.py after correction `f056386f3fcf0d4fcf690c864fef3915250a7b5a1ef835ae79d2d6ed401b349b`. The venv's editable install points at another worktree, so the `PYTHONPATH` override is deliberate; this is not an isolated or pinned environment.

* Core focused: 59 tests OK, exit 0 (`green-core.log`, rerun `green-core2.log` after formatting).
* API: wiring, role endpoint inventory and ranking policy, 49 tests OK (`green-api.log`); wiring alone 14 OK (`green-api2.log`).
* Ruff 0.17.3 (project pin 0.17.1) and mypy 2.4.1 (pin 2.4.0), not the pinned versions. First Ruff run: check exit 1 (E501 in a new test) and format exit 1 (`ruff-check.log`, `ruff-format.log` kept); after the fix, check 0, format 0, mypy 0 on four ranking files (`ruff-check2.log`, `ruff-format2.log`, `mypy.log`).
* `store.py` and `server.py` are not Ruff or mypy gated in this project and were not linted.

## Limits

* EPERM and ENOTSUP are injected at `os.link`; no real unsupported mount was tested. The cleanup failure injection wraps the real `os.unlink` and fails only for the owned stage name; link, files and bytes are real.
* FULL, independent whole-feature review and publication are pending. The R4 FULL receipt applies to `b7f6186` only and is invalid for this head.
* A crash-orphaned or retained stage still needs manual removal. Parent findings 1 and 2 are fixed by the corrected parent and not re-tested here beyond the inherited runner tests in the core run.
