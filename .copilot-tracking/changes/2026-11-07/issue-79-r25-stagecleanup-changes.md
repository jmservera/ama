---
title: Issue 79 r25 stage-cleanup masking correction changes
description: Changes record for the parent stage-cleanup correction
ms.date: 2026-11-07
---

## Changes

* `src/core/src/zava_forward/core/ranking_publication.py`: the `finally: os.unlink(tmp)` is replaced by a non-throwing `_remove`. A failed removal of this call's own stage file no longer hides `DurabilityUnconfirmedError` or the committed result; the base name (no path) is reported as `stage_retained` on the result or the error. An existing record at the final name returns without a folder sync, as before.
* `src/core/tests/test_ranking_publication.py`: two regressions (typed error kept with a retained stage; confirmed publish reports the retained stage) and the no-delete source guard now pins the single `os.unlink(stage)`.
* `src/api/tests/test_ranking_publication_wiring.py`: stage cleanup failure still gives 409 `committed_unconfirmed`, one unconfirmed audit entry, no path or error text, no false 403.
* `src/core/README.md`: one sentence on `stage_retained`.
* `docs/reference/log.md`: new dated entry; the r24 entry is untouched.

## Evidence

* RED on unfixed `fd57f086`: core 2 errors (`PermissionError`), API `(403, None) != (409, 'committed_unconfirmed')`; logs in `/mnt/ama-gates/g79-stagecleanup-1107/red-*.err`.
* GREEN: core 56 OK, API wiring 18 OK, assistant release OK (1 skip), ruff check and format clean on the five ranking files, mypy 268 files clean (own-source venv, external caches, PYTHONDONTWRITEBYTECODE=1).
* No FULL, SQL, browser, scanner or image gate; no child or main change.

## Divergences

* One existing source guard assertion was updated to follow the intended unlink move; its no-clock and single-unlink intent is kept.
