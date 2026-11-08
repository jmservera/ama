---
title: Issue 79 plan, r25 stage-cleanup masking correction
ms.date: 2026-11-07
---

Planning readiness: ready. Critique: one author-only prospective critique (not independent), before any test or source edit.

## Plan

* Commit research, plan, details. RED: one core regression (file fsync and link succeed, folder fsync EIO, `os.unlink` of the stage raises PermissionError) and one API regression (409, one unconfirmed audit, no 403). Run on `fd57f086` source and keep failures.
* Fix in `ranking_publication.py`: `_remove(stage)` that never raises; `finally` uses it; attach `stage_retained` (base name only) to `DurabilityUnconfirmedError` and to a successful result.
* GREEN, Ruff, mypy, README sentence, Changes, Review, log entry, commit.

## Critique

* Catching `OSError` in `_remove` is narrow (cleanup of one owned file) and not a success-shaped fallback: the committed outcome or the original error is still raised. FileNotFoundError is treated as removed.
* `stage_retained` carries only the base name, not a path or error text, and the API message stays fixed. The audit detail may name the retained stage base name.
* Generic errors (a failed link or write) keep their original exception, with a note when the stage remains.
