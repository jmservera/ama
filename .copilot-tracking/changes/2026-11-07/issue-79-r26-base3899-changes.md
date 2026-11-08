---
title: Issue 79 r26 changes, base reconciliation to main 38990b19
ms.date: 2026-11-07
---

## Changes

* Plain `git rebase origin/main` of the run-owned local root (planning commit `53155e27` included) onto `38990b19122bfa59a292d3bbaedecfec43580db5`; no conflict. 37 commits replayed, five old main-merge commits dropped (their content is in main). Old chain preserved at `preserve/issue-79-pre-base3899` (`bb7e044c`) and `preserve/issue-79-r26-planning` (`53155e27`).
* Replay duplicated 11 main #108 lines in `docs/reference/log.md`; the log blob was restored to the pre-rebase `53155e27` blob (zero deletions against main, all topic entries kept). No old log entry rewritten.
* No source change. Production ranking publication bytes equal `bb7e044c`.

## Proofs

* Topic-owned path set versus main equals the set versus `23b26a7f` of the old head; all those blobs and modes equal the old head except `log.md`, fixed above.
* The four incoming src/docs paths equal main; 18 incoming RPI files present.
* `origin/main` is an ancestor of HEAD; 0 merges ahead.

## Checks (own-source venv `/tmp/zf79venv`, `ranking_publication` from this worktree, `PYTHONDONTWRITEBYTECODE=1`, scratch `/mnt/ama-gates/g79-base3899-1107`)

* Core ranking publication and runner: 56 OK. API ranking wiring 18 OK. Exception register screen 15 OK, exception register 19 OK, data operator screen 9 OK, assistant release 48 OK (1 skip).
* Ruff check and format clean on six files, mypy 268 files clean, `git diff --check` clean.
* Config: no unit test named for Config exists; the production config a11y check is a browser-oriented check and was not run (source-only admission).
* No FULL, `--changed`, browser, SQL, Docker or scanner.
