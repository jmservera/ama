---
title: Issue 1231 r26 changes, parent79 fd57f086 directory-sync alignment
description: Implementation record for the local merge of parent79 fd57f086 and reconciliation with the child contract
ms.date: 2026-11-07
---

* Planning commit 8726085f5efcc663c1bd74e1dd349de3a990a215 (research, plan, details, critique) preceded the merge. Backup ref `backup/issue-1231-3696f-pre-r26-merge` preserves 3696ff05.
* One normal `--no-ff` merge of fd57f086d62f1446f8e1dbc3c7f8c89ca41a8c9b: commit 8b538e30dce26bdc901e40127bdc81866e1e4426, tree 946890a6bd2c0c7d786ea7e3555d5c7813fceefb, parents 8726085f and fd57f086. No rebase, push or history rewrite.
* Divergence from research: the research expected a README-only conflict; the real merge stopped on four content conflicts (src/core/README.md, ranking_publication.py, store.py, test_ranking_publication.py). All were resolved by hand. The semantic edits therefore live inside the merge commit, not a separate commit.
* Integration: DurabilityUnconfirmedError(OSError) keeps errno; `_confirmed` wraps a failed directory sync in it for fresh write, race loser and retry; Store handles it before the broad OSError to ArchiveStorageError (503) translation, audits `ranking_snapshot_publication_unconfirmed`, logs/re-raises on audit failure; API returns 409 committed_unconfirmed. Other archive failures keep 503. The parent's documented residual (retry does not confirm) is resolved by the child's retry re-sync; README states the integrated contract, not the parent's retry claim.
* Tests added: API `test_unconfirmed_sync_with_retained_stage_is_409_audited_logged_and_retry_confirms` (combined Store/API retained record, audit, 409, retry) and core `test_retry_stays_unconfirmed_until_the_sync_succeeds`. Existing child and parent assertions kept unweakened.
* Proof: incoming raw/mode/blob delta outside .copilot-tracking (7 paths) matches the parent's delta in paths and modes; log.md blob e92986f9e equals the parent's and has 4 added, 0 deleted lines; no existing .copilot-tracking path modified or deleted; main 23b26a7f, parent fd57f086 and old head 3696ff05 are ancestors.
* Parent scope deviation preserved: fd57f086 appended 4 lines to docs/reference/log.md beyond its narrow scope. Kept append-only and unrewritten; this child makes no other knowledge-base edit.
* Checks (PYTHONDONTWRITEBYTECODE=1, own pip venv, origins verified in this worktree, logs in /mnt/ama-gates/g1231-r26-dirsync-alignment-1107/logs): core 72 OK; API wiring 21 OK; test_assistant_release 48 OK with 1 skipped (opt-in SQL, not SQL acceptance); Ruff check src/core and src/api exit 0; ruff format 331 files formatted; mypy 128 source files exit 0.
* Adverse, preserved: the first run failed with a SyntaxError in store.py (a lost newline in my conflict resolution), kept as first-syntaxerror-* logs; a later Ruff E501 (test name too long) kept as first-ruff-e501.out. Both fixed before the merge commit; the test was renamed.
* Not done: FULL, SQL, browser, images, scanners, lock use, push, PR update, ticks. r25 and all older receipts are invalid for this head.
