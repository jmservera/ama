---
title: Issue 1231 r26 plan, parent directory-sync audit alignment
description: Prospective plan for one normal merge of local parent79 fd57f086 plus a semantic reconciliation that keeps the child unique-stage and retry-sync contract
ms.date: 2026-11-07
---

Prospective, committed before the merge or any source edit. Research: .copilot-tracking/research/2026-11-07/issue-1231-r26-parent-dirsync-alignment-research.md. Details and critique are sibling r26 files.

## Phases

1. Preflight (done): identities, ignored-inclusive clean, lock free, backup ref backup/issue-1231-3696f-pre-r26-merge created.
2. Commit the four prospective records (noreply author and committer, Conventional Commit, Copilot trailer).
3. One normal `git merge --no-ff fd57f086` of the local parent (parents: planning head first, fd57f086 second). Resolve only src/core/README.md and keep every other hunk. Do not rebase, rewrite or push. Abort only the owned merge on an unexplained conflict.
4. Reconcile semantics in separate follow-up commit(s), source scope only:
   * ranking_publication.py: `DurabilityUnconfirmedError` kept; `_confirmed` raises it for a folder-sync failure (fresh, race loser, retry) with cause errno, actual published_on, path and stage_retained; docstring updated; the parent's post-link one-shot sync removed so one sync path remains.
   * store.py: specific handler before the broad OSError translation, audit, log retained stage, audit failure logged and re-raised.
   * server.py: keep the parent 409 handler; keep ArchiveStorageError 503.
   * README: integrated wording (retry re-attempts the folder sync).
   * One small combined regression (retained record plus unconfirmed audit plus 409 through Store and API) and a helper test that a retry whose sync succeeds returns written False with the winner's date, and one that a failing retry stays unconfirmed. Existing assertions unchanged.
5. Light checks only: core and API targeted suites, test_assistant_release, canonical Ruff and mypy; no SQL server, browser, image, scanner or FULL.
6. Write changes, one author Review and state records; commit and freeze.

## Selectors (from r16 to r21)

* Core, from src/core: tests.test_ranking_publication tests.test_ranking_publication_runner.
* API, from src/api: tests.test_ranking_publication_wiring.
* Release: test_assistant_release (one known opt-in SQL skip is not acceptance).
* Ruff 0.17.1 on src/core and src/api, mypy on src/core with an external cache.

## Environment

External scratch /mnt/ama-gates/g1231-r26-dirsync-alignment-1107, PYTHONDONTWRITEBYTECODE=1, own pip venv with `pip install -e src/core -e src/agents -e src/api[dev]` from this worktree, import origin printed, each command's real exit in its own .exit file.

## Preservation proofs to record

* Merge parents; incoming path list, modes and blobs for the parent delta equal the parent's; log.md has zero deleted lines and both prior prefixes intact; no existing .copilot-tracking path modified or deleted; src paths outside the planned set unchanged from the start.

## Exit and next gate

Stop after a clean frozen source handoff. A new FULL tip gate (parent fd57f086 and the new child as stack members against current main) is a separate coordinator admission once heavy work elsewhere finishes; no passing receipt from old source applies.

## Follow-Up Items

* New FULL, independent exact-head review, hosted checks and human approval remain open and unclaimed.
* Open gaps: cross-UID, real unsupported mount, real filesystem directory-sync fault, unverified future date.
