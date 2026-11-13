---
title: "#176 provenance publication parent packaging plan"
date: 2026-11-13
---

## Plan

* [x] Verify both snapshot blobs equal their main33 public fixtures; stop if not.
* [x] Select `git diff --name-only 33c261a63 25a7135b1` minus the two duplicate snapshots (34 files) and copy exact blobs with `git checkout 25a7135b1 -- <paths>` into this parent (no merge or cherry-pick, so ancestry does not carry the snapshots).
* [x] Verify every selected index blob equals the child blob; the three source/test blobs equal the child.
* [x] Add own dated research, plan, critique, changes (manifest), review and state records.
* [x] Append one log entry after the child's entry; leave the child's entry byte-intact.
* [x] Commit locally with the noreply identity and Copilot trailer. No push, PR, rebase, gate, test run or remote write.

## Boundaries

* No deletion, move, reset, stash or rewrite of the child worktree, branch, objects or `.venv-176c2`.
* The two public fixtures stay unchanged.
* `docs/reference/log.md` is the only selected file this parent extends beyond the child blob.
* Pending, owned by others: frozen-source validation worker (imported-Core identity, fresh non-SQL consumer proof); root must consume these before publication.
