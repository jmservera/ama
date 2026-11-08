---
title: Issue 79 r29 changes, written field of the unconfirmed runner outcome
ms.date: 2026-11-07
---

## Changes

* `ranking_publication.py`: `DurabilityUnconfirmedError(path, published_on, cause, written=None)` stores `written` (True: this call created the record; False: existing record or lost race; None: unknown, never defaulted to False). `_confirmed` passes the outcome's `written`. Store and API callers use only the type, path and date and are unaffected.
* `ranking_publication_runner.py`: the `committed_unconfirmed` handler outputs `written` from the error instead of a hardcoded False.
* Tests: the r28 runner test expectation for a newly created record is corrected to True (the r28 expectation was the introduced bug); core tests assert `written` for first link (True), existing record and race loser (False) and unspecified (None); a runner test covers an existing-record retry (False). README clause and new log entry; the r28 log entry and Review stay as history.

## Evidence

* RED on `4a88793f`: 3 core errors (no `written`) and 1 runner failure `(False, ...) != (True, ...)` (`/mnt/ama-gates/g79-writtenfield-1107/red.err`).
* GREEN: core 60 OK, API wiring 18 OK, ruff, format (one of my own test lines reformatted) and mypy 268 files clean, `git diff --check` clean. Own-source venv, external caches, `PYTHONDONTWRITEBYTECODE=1`. No FULL, SQL, browser, image or child change.

## Child propagation requirement

* Child 61f3ebe1 `_confirmed` must also pass `written` into the typed error, preserving its private-stage and `_remove` behaviour.
