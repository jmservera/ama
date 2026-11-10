---
title: Issue 79 changes, r24 directory-sync audit correction
ms.date: 2026-11-07
---

## Changes

* Planning commit `8d5772eaa4208416c03f7647f6de3938cbc3618e` (ref `preserve/issue-79-r24-planning`); preserve ref `preserve/issue-79-pre-dirsync-audit` = `b8ad4a0e607fca85cef198f6428cd41c758b04b0`.
* `ranking_publication.py`: `DurabilityUnconfirmedError(OSError)` (path, published_on) raised only when the post-link folder sync fails; the stage is still removed and the record kept.
* `store.py`: `publish_ranking_snapshot` audits `ranking_snapshot_publication_unconfirmed` under the actor with policy, signed state, as-of and hash, then re-raises. An `OSError` from the audit write is logged (`logging.exception`) and surfaced.
* `server.py`: `/api/ranking/publish` returns 409 `outcome: committed_unconfirmed` with a fixed path-free message.
* Tests (3 new): core directory-sync failure after link; API audit-as-unconfirmed with no path or error text; audit failure logged and surfaced. README paragraph updated.

## Evidence

* RED before source (kept in `/mnt/ama-gates/g79-dirsync-audit-1107/red-core.err`, `red-api.err`): core `AttributeError` no `DurabilityUnconfirmedError`; API `(500, None) != (409, 'committed_unconfirmed')` and no ERROR log for audit failure.
* GREEN: core 54 OK; API wiring 17 OK; `test_assistant_release.py` 48 OK, 1 skip (SQL); Ruff check and format on the five ranking files 0; `mypy src tests` 268 files 0. One E501 in my new test was fixed by `ruff format`. Own-worktree packages (`/tmp/zf79venv`), `PYTHONDONTWRITEBYTECODE=1`, scratch `/mnt/ama-gates/g79-dirsync-audit-1107`.
* Not run: FULL, SQL, browser, scanner, images. Child 1231 untouched.
