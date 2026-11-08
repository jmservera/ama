---
title: Issue 1231 r26 research, parent directory-sync audit alignment
description: Prospective research for one normal merge of local parent79 fd57f086 and reconciliation with the child's unique-stage and retry-sync contract
ms.date: 2026-11-07
---

Disposition: executed (read-only), committed before any source mutation. The r15 chronology deviation, all r16 to r25 records, the old incomplete independent reports and the failed r22 receipt are preserved unchanged.

## Identities (verified before writing)

* Child start 3696ff058342ad3872088fbbc91059254c9f266e / tree 95d11d2f8a1e511d0fe06774a237accb6d16a804, branch fix/ranking-archive-concurrent-writer-metadata, ignored-inclusive clean. PR1242 OPEN, base feat/ranking-publication-runner-79 (unchanged target). Backup ref backup/issue-1231-3696f-pre-r26-merge.
* Local parent79 fd57f086d62f1446f8e1dbc3c7f8c89ca41a8c9b / tree e6e483dbf8a1806e64bc462302cd4fae70810aa1 in the issue-79-publisher worktree, ignored-clean. Merge-base with the child is b8ad4a0e (prior parent). Stale remote parent not used.
* Main 23b26a7f3a4693cd20dcf0447303d97491096cb3 equals origin/main after a fresh fetch and is an ancestor of both.
* Heavy lock free (fuser exit 1). No FULL or heavy gate is admitted for this launch.

## Incoming parent delta b8ad4a0e..fd57f086 (13 paths)

* Six parent r24 RPI records under .copilot-tracking (new files only).
* docs/reference/log.md: one appended entry (4 added lines). The parent's launch scope was narrower than a knowledge-base edit; this is a recorded scope deviation of the parent. The entry is append-only history and is preserved, not rewritten.
* Source: ranking_publication.py adds DurabilityUnconfirmedError (OSError subclass) raised when the folder sync fails after the final link; store.py audits ranking_snapshot_publication_unconfirmed and re-raises (audit failure logged and re-raised); server.py answers 409 outcome committed_unconfirmed with fixed path-free text; core README wording; two core/API tests each side.

## Dry run

`git merge-tree --write-tree` of child and fd57f086 reports one content conflict (src/core/README.md) and auto-merges server.py and the API test. ranking_publication.py, store.py and the core test are listed as touched by both sides; they auto-merge textually but are semantically unsafe, as below. Planning files are added to the child first, so the real tree differs from any pre-planning dry run.

## Semantic overlap analysis

* Child publish(): unique O_EXCL 0600 stage, os.link, stage removal, then _confirmed() syncs the folder for new and already-archived records alike, so a retry re-attempts the folder sync and returns only after it succeeds. Parent publish(): earlier mkstemp-style stage and a one-shot sync after the link; a retry returns the existing record WITHOUT any sync (documented parent residual). The child's _confirmed already resolves that residual; the parent's README claim "a retry still does not confirm durability" must NOT be copied into the integrated contract.
* Child Store catches every OSError and converts it to ArchiveStorageError (503). DurabilityUnconfirmedError is an OSError, so after the merge it would be swallowed into the 503 path with no unconfirmed audit entry. The specific uncertainty must be handled first.
* Child tests assert that a failed directory sync raises OSError with errno EIO and that a retry under a failing sync still raises. Parent exception built with a message only would lose errno; the integrated exception must carry the cause errno so those assertions stay unweakened.
* Child stage_retained diagnostics are set on exceptions or the outcome; a folder-sync failure currently drops the outcome-level stage_retained marker (pre-existing gap, tightly coupled to the new exception, so the integrated exception carries it).
* Other unavailable-archive paths (unsupported hard links, EPERM/ENOTSUP, cleanup failures) keep 503 and path-free text.

## Findings and proposed integrated contract

* Helper: _confirmed wraps a folder-sync OSError in DurabilityUnconfirmedError for the fresh write, the race loser and the retry of an existing record, carrying the cause errno, the actual (winner) published_on and stage_retained when the stage remains. A later retry whose sync succeeds returns the existing record with written False (durability then confirmed).
* Store: catch DurabilityUnconfirmedError before OSError; log a retained stage; audit ranking_snapshot_publication_unconfirmed (actor, policy, signed or unsigned, as of, hash prefix); on audit failure log and re-raise; otherwise re-raise the unconfirmed error. The 409 text stays fixed and path-free.
* API: parent handler for 409 committed_unconfirmed kept; 503 handler for ArchiveStorageError kept.
* README: describe the unconfirmed outcome and that a retry re-attempts the folder sync and reports the existing record once the sync succeeds, otherwise the unconfirmed outcome again.

## Limits and open gaps (not closed here)

* No FULL, independent exact-head review, hosted checks or human approval exist for the merged head. The r25 passing receipt (57e168f3...) applies only to old head 3696ff05 with b8ad4a0e and is not valid for new source.
* Parent three Medium findings and the new dirsync fix are author-corrected only. Cross-UID permissions, a real unsupported mount, post-link directory-sync audit completeness on a real filesystem fault, and unverified future-date handling remain open.
* Retention and Legal approval are not implied. The parent's log scope deviation is recorded, not altered.
