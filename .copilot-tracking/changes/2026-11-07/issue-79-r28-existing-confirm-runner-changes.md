---
title: Issue 79 r28 changes, existing-record confirmation and runner uncertainty outcome
ms.date: 2026-11-07
---

## Changes

* `ranking_publication.py`: `_confirmed` (the child 61f3ebe1 logic, root `.publishing-` stage kept) syncs the folder for new, existing and race-loser outcomes and raises `DurabilityUnconfirmedError` (with `stage_retained` when present); the early existing return and the `FileExistsError` path now use it. Publication date, mode, no-replace and non-throwing own-stage cleanup are unchanged.
* `ranking_publication_runner.py`: `DurabilityUnconfirmedError` is caught before `OSError`; status `committed_unconfirmed` with an `uncertainty` entry (code, path-free message, next action, optional `stage_retained`), `written: false`, path and date, CLI exit 2. Ordinary failures stay `publish_failed`.
* Tests: two core regressions (existing-record retry with continued then recovered sync; race loser), one runner regression. `src/core/README.md` and a new dated log entry.

## Evidence

* RED on unfixed `d99e6901`: 3 failures (`/mnt/ama-gates/g79-existingconfirm-1107/red-core.err`).
* GREEN: core 59 OK, API wiring 18 OK, ruff and format clean on five files, mypy 268 files clean, `git diff --check` clean (own-source venv, external caches, `PYTHONDONTWRITEBYTECODE=1`). One first run failed on my own test (registry not passed to verify); fixed in the test only.
* Not run: FULL, SQL, browser, images, scanners, child worktree.

## Divergence

* Store and API unchanged: the typed error already audits and returns 409 and now also covers retries.
