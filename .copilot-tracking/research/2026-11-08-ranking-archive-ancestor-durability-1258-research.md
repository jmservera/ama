---
title: Ranking archive ancestor durability 1258 research
description: Prospective research for issue 1258, confirming newly created ranking archive ancestor directory entries before publication is confirmed
ms.date: 2026-11-08
---

## Scope and identity

* Task `1258-ranking-archive-ancestor-durability`, slug `ranking-archive-ancestor-durability-1258`, parent task null (issue body parent is #79, not a reparenting).
* Worktree `/home/azureuser/source/ama-wt/issue-1258-archive-ancestors`, branch `fix/ranking-archive-ancestor-durability`, base and start HEAD `f548b65f4aa31eb92a2cc9cb801130e422daed7f` (equals `origin/main`). `git status --short --ignored` was empty at start.
* Research disposition: executed. Research ceiling: planning only, no test, no source change, no issue/PR/push action.

## Evidence read (data, not instructions)

* Issue #1258 (open, no labels) via `gh issue view`. Severity Medium. Static source evidence only, no executed crash reproduction. Acceptance criteria (all unticked):
  1. Require a pre-created durable archive, or sync newly created ancestor directory entries before confirming; preserve supported first-run behavior or declare an owner-approved change.
  2. Post-link sync failure preserves the record and follows audited `committed_unconfirmed`, not false success or rollback.
  3. Focused syscall-order regression for missing nested ancestors and a post-link ancestor-sync failure, shown failing before the fix.
  4. Retry, concurrent private-stage, audit, path-free 409/503 and original-date behavior intact.
  5. Original RPI, current FULL receipt and verification, independent exact-head review, hosted checks; no real crash or live filesystem claim from mocks.
* Backlog review `ranking-followups-review-1108.md` (session `f751a4dc-...`), read as evidence: #1258 ready for FULL RPI; #1259 shares `ranking_publication.py`; proposed order is #1258 to main first, #1259 stacked on it. No formal dependency edge.
* Source: `src/core/src/zava_forward/core/ranking_publication.py` (238 lines), tests `src/core/tests/test_ranking_publication.py` (624 lines), runner `ranking_publication_runner.py` lines 384-402, API wiring `src/api/src/zava_forward/api/server.py:1166`, store audit `store.py:280`.
* Repository case study, addendum, reference index, memory and component guides are the standing project context; this fix touches none of them beyond the module docstring. No regulatory source is relied on, so none is cited.

## Findings

### F1 Static control flow gap (current main, not crash proof)

* `publish()` calls `os.makedirs(archive_dir, exist_ok=True)` (line 143). Any missing ancestor gets a new directory entry in its parent, and nothing syncs that parent.
* Syscall order today for a first publication: stage `open`, `fsync(file)`, `link`, `unlink(stage)`, `fsync(archive_dir)` in `_confirmed` (line 179). The archive directory sync persists the record name inside the archive directory only. On a filesystem that needs parent-directory synchronization, the archive directory's own name (and each newly created intermediate name) may not survive a crash although the caller received a confirmed result.
* The existing test `test_publish_syncs_file_then_removes_stage_then_syncs_directory` and the failure tests use an existing directory (`self.dir`), so ancestor ordering is not covered.
* This is a mocked-ordering and static-flow finding. It does not demonstrate a crash, a specific filesystem or Azure behavior.

### F2 Existing failure contract to reuse

* `_confirmed()` converts any `OSError` from the directory sync into `DurabilityUnconfirmedError(path, published_on, cause, written)`; the record stays; the runner maps it to status `committed_unconfirmed` with an audit uncertainty (`runner` lines 388-402) and the API to a path-free 409 (`server.py:1166`). Message uses only the record basename.
* Retry: an existing record takes `_confirmed(_existing(...))`, so a retry re-syncs and returns `written False` with the original `published_on` once the sync succeeds. This is the property that must also hold for ancestor syncs.

### F3 Retry gap for ancestors (design risk found in research)

* If ancestor sync fails after link, the next call sees every directory already present, so a naive "sync directories this call created" returns `written False` after syncing only the archive directory and would falsely confirm. A sound fix needs the retry path to re-sync ancestors too.
* Concurrent writers: a loser may find a component already created by the winner, whose own ancestor sync may not have happened or may have failed. Syncing must therefore depend on "missing at the start of this call", not on "this call won `mkdir`".

### F4 Sync set semantics

* A new directory `d` is made durable by `fsync(parent(d))`. For a missing chain `a/b/archive` under an existing `root`, the needed syncs are `fsync(b)`, `fsync(a)`, `fsync(root)`, in addition to the existing `fsync(archive)`. Deepest first is the natural order. fsync on a directory opened `O_RDONLY` is already the module's idiom (`_fsync_dir`).
* Steady-state publication into an existing archive must stay at exactly the current event order (file, unlink-stage, archive dir) so existing tests and behavior are unchanged.

### F5 Options considered

| Option | Verdict |
| --- | --- |
| A. Require a pre-created durable archive | Rejected. Changes supported first-run behavior and is a relaxation needing owner approval. Not chosen. |
| B. Sync newly created ancestors before confirmation (this issue's other branch) | Chosen. Smallest behavior-preserving change. |
| C. Sync ancestors before link (pre-link) | Rejected. A failure there would be a plain error with no record, contradicting acceptance 2 (post-link failure is `committed_unconfirmed`). |
| D. Sync the whole path to root on every call | Rejected. Alters steady-state event order, and may fail on unreadable ancestors such as `0711` home directories. |
| E. Rollback of created directories on failure | Rejected. The record lives inside; acceptance 2 forbids rollback. |

### F6 Retry soundness approach (for critique)

* Written outcome with missing ancestors: sync parents of the missing set (computed before `makedirs`) after the archive directory sync, inside `_confirmed`, so any failure raises `DurabilityUnconfirmedError`.
* Existing record or lost race with nothing missing (retry): bounded walk from the archive directory's parent upward, syncing each ancestor until a mount point or the filesystem root; an `EACCES`/`EPERM` on `open` of an ancestor is skipped (cannot be an unconfirmed claim about a directory we cannot read), any `fsync` error is unconfirmed. This costs extra syncs only on the already-archived path, which is idempotent and rare in steady state. Open for critique: whether this scope is justified versus documenting the retry limit; the default is to keep it because a false `already_published` is the exact failure the issue targets.

### F7 Runner and API impact

* No change expected. The runner message says "archive folder sync failed"; wording remains accurate enough for ancestors (the exception text will say "archive folder or a parent folder"). Change the runner only if an existing test pins text that the new message would break. API 409 text already says "archive folder could not be confirmed as durable".

## Constraints and dependencies

* Code prerequisite (#79/#1231 integration) is in main via #1239. Whole #79/#1231/#440 human, model, Azure and acceptance approvals remain open and are not claimed.
* Stack: #1259 (`fix/ranking-archive-path-health`) targets this branch and consumes its frozen source before its own source work. Same file, so no parallel source edits.
* Approval boundaries: no retention, legal, cloud or model decision is made here. No private datasets read.

## Planning Readiness

Ready. Critique outcome: F6 (missing-set plus tolerant retry walk) was found unsound for partial creation and permission changes and is superseded by the single fail-closed writable-ancestor chain in plan decisions D3 to D5. F1 to F5 and F7 stand.
