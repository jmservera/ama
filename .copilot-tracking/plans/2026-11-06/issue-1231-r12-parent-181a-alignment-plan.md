---
title: Issue 1231 r12 plan and details (merge parent 181a1c1bb, align the child)
ms.date: 2026-11-06
---

## Chronology statement (prospective)

Written after the r12 research and before any merge commit or source edit. No new critique is claimed yet; see Critique below.

## Start identity

Branch `fix/ranking-archive-concurrent-writer-metadata`, head `ae23c0d7274d1314ff632de268ad77e103d09ca6`, tree `ee9410dc0bf5dda11555f01121cb2e48d971c207`. Preserved ref `backup/issue-1231-ae23-pre-r12-align`. Parent `181a1c1bb5e83c2ce08a7663d0a2b9145e6fc85e`. Main `56eec736906774ef56d8c9a66ed7f3f9c1e520c6`.

## Phases

1. Commit these prospective records. Resolve and set the repository-local privacy-safe identity first.
2. `git merge --no-ff --no-commit 181a1c1bb5e83c2ce08a7663d0a2b9145e6fc85e`. Resolve the three conflicts per the research design. `README.md` and the wiring test auto-merge and are reviewed, not rewritten.
3. Helper: add file and directory `fsync`, adopt `_existing(path, snap)` and `lexists`; keep the unique exclusive stage, `_remove`, `stage_retained` and `ArchiveStorageError`; drop the now-unused `tempfile` import if the merge brings one in.
4. Store: combine both sides (`OSError` translation, retained-stage warning, `policy_signed`, audit wording, status listing error).
5. Tests: keep child tests; replace the parent source-text `unlink` test with a behavioural no-staging-left assertion plus the no-clock check; keep the parent behavioural tests; no new tests unless a child path loses coverage (for example `stage_retained` with the validated `_existing`).
6. Checks: unit tests `test_ranking_publication`, `test_ranking_publication_runner` (core) and `test_ranking_publication_wiring` (API) with `PYTHONDONTWRITEBYTECODE=1` and `PYTHONPATH` to this worktree; Ruff check and format on the changed files with the pinned 0.17.1 from the r7 venv, mypy from `src/core` with an external cache; import origin proof; `git diff --check`; JSON validity. Tool output, caches and temp under `/mnt/ama-gates/restart-1106-1231-r12/`. Leave no ignored file and remove none by glob.
7. Changes, one author Review, final state, one commit.

## Critique

One independent critique ran before the merge. Verdict Pass with changes; all four findings accepted as plan changes (see the critique file). They add to phases 3 to 5:

* Helper order after a successful link: remove the owned stage first, then sync the directory; `stage_retained` still reports a failed removal. A validated existing record (retry or race loser) is returned only after the directory is synced.
* A directory sync `OSError` stays an `OSError` (the runner already catches it; the Store translates it to `ArchiveStorageError`), and the Store message is reworded from "Nothing was published" to "Publication could not be confirmed; ... a retry reports an already-archived record as already published", with the wiring assertion updated to match. No new return state.
* The child test that expects an edited record to be accepted now expects `PublicationError` and unchanged bytes (the parent already changed it; the merge keeps the parent version).
* Tests added for: order (stage removed before the directory sync), directory sync on the existing-record path, and an injected directory sync failure.

## Out of scope

No push, PR, retarget, FULL, SQL, browser, image, scanner, ref move, deletion or edit of memory, original case study, knowledge index or log or older records.

## Follow-up items

Fresh FULL on the new head (stack 1231 to 79 to 73), independent exact-head assessment, human approvals, the directory-`fsync` message residual, and the pre-existing `store.py` `ruff format` finding from r10 RV-002.
