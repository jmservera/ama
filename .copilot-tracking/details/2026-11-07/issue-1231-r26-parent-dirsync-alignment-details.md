---
title: Issue 1231 r26 details, parent directory-sync audit alignment
description: Phase details for the r26 merge of parent79 fd57f086 and the dirsync reconciliation
ms.date: 2026-11-07
---

## Phase 2 to 3: records, then one normal merge

* Stage only the four r26 files; commit; backup ref already exists (refuse any unexpected existing ref).
* `git merge-tree --write-tree HEAD fd57f086` dry run; expect only src/core/README.md to conflict; then `git merge --no-ff fd57f086 -m ...`.
* README resolution: keep the child's Durability paragraph and add the parent's unconfirmed sentence rewritten to the integrated contract (below); drop the false "retry does not confirm" claim.

## Phase 4: reconciliation (exact edits)

1. ranking_publication.py
   * `DurabilityUnconfirmedError.__init__(path, published_on, cause)` calls `super().__init__(cause.errno, message)` so errno is kept.
   * `_confirmed(outcome, archive_dir)`: try `_fsync_dir`; on OSError raise DurabilityUnconfirmedError(outcome["path"], outcome["published_on"], e); if outcome has stage_retained set it on the error. Used for new, loser and existing paths. Remove the parent's try around the post-link sync (child publish does not have it after the merge resolution; confirm no double sync).
   * Update docstring text about the failed sync.
2. store.py: `except DurabilityUnconfirmedError` placed before `except OSError`; log retained stage; audit unconfirmed with actor, policy, signed, as of and hash prefix, no path; audit OSError logged and re-raised.
3. server.py: keep the parent's 409 handler for the publish route; keep the ArchiveStorageError 503 handler unchanged.
4. core README: integrated wording.
5. Tests: keep both sides' tests. Add (a) API/Store: record retained plus audit unconfirmed plus 409 plus retained stage logged; (b) helper: retry after a failed sync with sync restored returns written False and winner date, retry under failing sync raises DurabilityUnconfirmedError again. Parent test expecting retry not to confirm does not exist (README only).

## Commands

Per-command .out/.err/.exit under /mnt/ama-gates/g1231-r26-dirsync-alignment-1107. Prove import origin from this worktree. Run the same suite before the semantic edit (post-merge, expected to show the swallowed 409) and after, and preserve the first failure.
