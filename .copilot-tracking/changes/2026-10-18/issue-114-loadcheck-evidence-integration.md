---
title: Issue 114 exact-main integration receipt
description: Authorized same-session rebase integration, parity and validation, not another original Review
ms.date: 2026-10-18
---

## Authority and Frozen Inputs

Coordinator explicitly authorized integration in session 619ef4ca-dccb-4a9a-b8db-fb4de739c825
on branch fix/loadcheck-evidence-114, PR #403, onto exactly
2975c4fdd7bf7d78e97b703aa2bef8bc97f56c3b only.
Old published head: 84e11721df930cb96c2f031a0430df503ec2f498.
Original base: f91353169756dc41ebbcca944bdd3f44f7c04b89.
GitHub confirms #402 merged at target 2975c4fd and #401 merged at original base f9135316.
Clean worktree, expected branch/local head and remote PR head verified before writes.

This authorizes rebase of this owned branch and only the exact lease publication:

```bash
git push --force-with-lease=refs/heads/fix/loadcheck-evidence-114:84e11721df930cb96c2f031a0430df503ec2f498 origin HEAD:refs/heads/fix/loadcheck-evidence-114
```

Lease failure or ambiguous conflict stops the operation; no weaker force, source-scope expansion,
second original Review, main rewrite, merge or other remote mutation is authorized.

| Frozen bytes | SHA-256 |
| --- | --- |
| loadcheck.py | a6bd8d0c4e3ae31484c6248934647b08251af688bf1f3db93a260a9d81fb9858 |
| test_loadcheck.py | db30c48bbd9151eee3bb72af4e50dbca8ba8fbaeb2d87a7083fa6c52fdd7affd |
| Original Revise critique | 6f40180f9bff6315e3a0296310a61ece41092f943c41b1d755dd16d293cd7012 |
| Original Not accepted Review | 6510bcd1d1055621b7fb37f73f7ef84426ec5160b65ef1e8bef7bd424017befe |

Correction ONE receipt and original adverse reports must remain byte-identical to old published
head. Prior mutation/good-run evidence stays attributed to the unchanged source, not rerun claims.

## Execution

In progress. Persist authorization, commit tracking-only checkpoint, rebase exact base-to-target,
verify all upstream content retained and frozen parity, then focused/coupled core and configured
checks. No production source edits planned.

## Commands and Results

* `git status --short; git branch --show-current; git rev-parse HEAD`: clean, expected branch/head.
* `git fetch origin main; git rev-parse origin/main`: exact authorized 2975c4fd.
* `gh pr view 403 --json headRefOid,baseRefOid,state`: OPEN, expected old head/base.
* `gh pr view 402 --json mergeCommit,state; gh pr view 401 --json mergeCommit,state`: both MERGED,
  target 2975c4fd and f9135316 respectively.
* `git merge-base --is-ancestor f9135316 2975c4fd`: passed.
* `git diff --name-only f9135316..2975c4fd`: upstream #402 tracking, API/web and UX KB only;
  no overlap with issue #114 source/tests/tracking.
* `sha256sum` of the four frozen files: exact expected hashes above.
* `gh api user --jq '{id,login}'`: id 8036360, login jmservera; configure local noreply before commits.

## Boundaries and Handoff

No private inputs, Azure actions, spend, issue/board changes or acceptance-box writes.
Actual Azure load/latency/cost, annual ledger, backup/restore/deletion and all literal issue #114
acceptance remain unmet. Integration is not corrected-head independent acceptance.
Stop after exact-lease publication for coordinator independent complete exact-head review.
