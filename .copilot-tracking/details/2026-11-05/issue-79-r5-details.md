---
title: Issue 79 details, continuation r5
ms.date: 2026-11-05
---

## Cleanup manifest

* Tool and evidence, outside the checkout: `/home/azureuser/.local/share/ama/cleanup-2026-11-05-issue79/` (`clean.py`, `manifest.json`, `generated-inputs.tar.gz`, `removal-journal.jsonl`). Owner-only local scratch, not a public artifact or an approved store.
* Selection: 13 exact directories, 333 files, 15 directories to `rmdir` (two cache subdirectories counted), 0 refused. Per-file checks: regular file, not a symlink, not tracked, `git check-ignore`, current owner, mtime after worktree creation, `.pyc` with sibling `.py`, `egg-info` members limited to the five standard names, caches limited to files under the two known cache roots.
* Archive: the 333 files were archived with `tarfile`, read back and compared by SHA-256 before removal (archive SHA-256 `7089e642fb4c298e057783a55edeacd328901c27ee9ce9473b64941946b44d32`). Each file was re-hashed immediately before `unlink`; 348 journal lines (333 removals, 15 `rmdir`).
* Not touched: tracked files, `.copilot-tracking` evidence, `support/` private data and everything outside this worktree. The scratch mypy cache and config used for the typing proof were in a `/tmp` directory created for this task and removed afterward.
* Restore: extract the archive to a new empty directory and compare to `manifest.json`; copying back is not needed because all files regenerate.

## Unknowns kept visible

* Whether the owner approves the `clean.py` selection formally is not recorded; it was run on the owner's instruction to clean own generated inputs.
* The archive is not in an approved artifact store.
