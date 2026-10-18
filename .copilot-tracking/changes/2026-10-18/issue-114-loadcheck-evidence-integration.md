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

Local integration and validation complete. Four owned commits replayed without conflicts onto
the exact approved target. No production or test source edits, no correction TWO, no new critique
or original Review. Final receipt reconciliation is artifact-only. Publication uses the exact
old-head lease below; final SHA and observed push outcome are pinned externally in PR #403,
avoiding a self-referential commit hash or an unauthorized second lease.

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
* Preflight tracking checkpoint committed as 94ec9765, with authenticated local noreply author
  and committer and required Copilot trailer.
* `GIT_COMMITTER_EMAIL="$identity" GIT_SEQUENCE_EDITOR=true git rebase --onto 2975c4fdd7bf7d78e97b703aa2bef8bc97f56c3b f91353169756dc41ebbcca944bdd3f44f7c04b89 fix/loadcheck-evidence-114`:
  passed, 4/4 commits replayed, no conflicts; post-rebase head
  6d95a2a5ee3ccfacab797fd58aa75541c08bc425.

## Commit Mapping

| Original identity | Rebased identity |
| --- | --- |
| e63426148b5bac564ffef4195a9ba3b1b873d068 original candidate | e365879b (same source/artifact patch) |
| d55e96c6e1031f4097947f1a0810da1e177a26f1 correction ONE | c100d6b8 |
| 84e11721df930cb96c2f031a0430df503ec2f498 publication receipt | 0b6ab5a3 |
| 94ec9765 integration authorization checkpoint | 6d95a2a5ee3ccfacab797fd58aa75541c08bc425 |

Original reports continue to identify their original candidate. They are not rewritten to pretend
assessment of rebased commits. Current integration base is 2975c4fd; f9135316 remains original base.

## Parity Verification

An inline Python check uses `git show OLD:path` versus `git show HEAD:path` for production
loadcheck, test_loadcheck, original critique, original Review and correction ONE receipt.
All five are byte-identical. Correction ONE receipt SHA-256:
b6ed21c6a096cde854fe23901b8b4ef40e1944954b83c9ee0f6817c5d58e2f8f.
The other four hashes exactly match the frozen table.

`git merge-base --is-ancestor` passes for both #401 merge f9135316 and #402 merge 2975c4fd.
All 28 paths changed by `git diff --name-only f9135316 2975c4fd` have identical
`git ls-tree TARGET -- path` and `git ls-tree HEAD -- path` output (blob and mode).
Thus all upstream #402 content is retained, and all #401 ancestry remains. The only topic diff
against target is the existing two loadcheck source/test files plus task-owned tracking artifacts.

## Post-Integration Validation

`V=/home/azureuser/.copilot/session-state/619ef4ca-dccb-4a9a-b8db-fb4de739c825/files/loadcheck-venv`.
Existing installed editable core[dev] reused; no dependency install required.
`R=/home/azureuser/source/ama-wt/issue-114-loadcheck`.
Commands executed:

```bash
mkdir -p .copilot-tracking/.issue-114-integration-tmp
cd src/core
env -i PATH=/usr/bin:/bin TMPDIR=$R/.copilot-tracking/.issue-114-integration-tmp $V/bin/ruff check .
env -i PATH=/usr/bin:/bin $V/bin/ruff format --check .
env -i PATH=/usr/bin:/bin $V/bin/mypy
cd tests
env -i PATH=/usr/bin:/bin TMPDIR=$R/.copilot-tracking/.issue-114-integration-tmp $V/bin/python -m unittest test_loadcheck test_sqlreads test_sqlstore test_taskqueues test_sqlqueues test_queue_benchmark -q
```

All passed: Ruff clean; 71 files already formatted; mypy no issues in 124 files;
75 tests in 87.495s, no skips. Includes 16 focused loadcheck methods and directly coupled local
SQLite/query/queue tests. Printed benchmark timings are incidental local observations, not Azure
load, performance improvement or operational acceptance.
No validation failures or new dependencies during integration.

Prior 16-mutant and exact healthy-report equality evidence is preserved, not re-executed:
the production and test bytes are unchanged. No need to rerun web/API/#402, Docker/nonroot,
Azure SQL-provider, migration or full repository suites for this no-overlap integration; all upstream
changed files are retained exactly and no store/schema/runtime-image contract changed.
Task scratch is removed with `rmdir .copilot-tracking/.issue-114-integration-tmp`;
`git diff --check` and final parity are required before publication.

## Publication and Actual Handoff

Final artifact-only reconciliation commit follows this validated 6d95a2a5 integration candidate.
PR #403 body/metadata records the exact resulting final head, base 2975c4fd, observed exact-lease
push outcome and final verification. No ordinary push, blanket force, implicit lease or alternate
remote target is permitted. If the specified lease fails, stop without fallback.
All ten task-owned artifacts remain committed. Original publication receipt is historical;
this integration receipt supersedes its old-current-base/head and no-integration handoff text.
Original critique, Review and correction ONE receipt remain entirely unchanged.

## Boundaries and Handoff

No private inputs, Azure actions, spend, issue/board changes or acceptance-box writes.
Actual Azure load/latency/cost, annual ledger, backup/restore/deletion and all literal issue #114
acceptance remain unmet. Integration is not corrected-head independent acceptance.
Stop after exact-lease publication for coordinator independent complete exact-head review.
