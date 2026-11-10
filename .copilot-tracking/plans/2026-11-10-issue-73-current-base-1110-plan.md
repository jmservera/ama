---
title: Issue 73 current-base refresh - plan
ms.date: 2026-11-10
---

## Objective

Merge exact origin/main 736561ba into the branch (no rebase, rewrite or force push) to resolve the published CONFLICTING state, keeping source byte-identical to 27dab9b5.

## Steps

1. Record plan-done, open the changes record, record implement-start.
2. `git merge --no-ff 736561ba` with the repository-local privacy-safe identity. On a log.md conflict keep both append-only histories (main's entries and this branch's entries, in order, no rewriting). Stop with a diagnostic on any conflict outside docs or any change to src, infra, tools, .github.
3. Assert `git diff --quiet 27dab9b5 HEAD -- src infra tools .github` exits 0 and that both parents are 27dab9b5 and 736561ba.
4. Add only this loop's RPI records and one append-only log entry; check links and diff.
5. Review once, record implement-done and review-done, commit, record commit-complete with the actual head, verify the witness, write the handoff.

## Out of scope

Source repair, #1360, runtime or gate reruns, push, PR or board changes, workflow or protection changes.
