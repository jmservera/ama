# Issue 1231 r30 root 8010a486 propagation: changes

Plan: .copilot-tracking/plans/2026-11-07/issue-1231-r30-root8010-written-propagation-plan.md (unticked, prospective, committed c6869277 before any merge or source edit).

## Changes

* Backup ref backup/issue-1231-61f3e-pre-r30-merge at 61f3ebe1.
* Normal merge of root 8010a486, merge commit 73fe836c (tree 861b52ee7ac39b112acd01b7d5f6585cd731da6b). Conflicts in README, helper and core test file; resolved to the child's blobs, then adapted. Runner, runner tests, root RPI and log append auto-merged.
* Red evidence first (kept in /mnt/ama-gates/g1231-r30-prep-1107/logs): runner tests 2 errors (no written on the child error), core tests 3 errors. Both failures are AttributeError on written.
* Source: DurabilityUnconfirmedError.written (optional, None unknown); _confirmed passes outcome["written"] (and keeps stage_retained). Runner handler and exit 2 come from root and are now effective. README paragraph adds the written/status wording.
* Tests: written assertions in two existing child tests; one race-loser reconfirmation test adapted to the child's own os.link and .ranking-style stage path (no .publishing- assumption); root's two runner tests merged unchanged.

## Evidence (own venv, imports resolved to this worktree, PYTHONDONTWRITEBYTECODE=1)

* Core ranking helper plus runner: 76 OK. API wiring plus register, register screen, data operator screen: 65 OK. Config class: 2 OK. Ruff clean, format clean (332 files), mypy 128 files clean.
* No conflict markers. Source diff against 61f3ebe1 is exactly 5 ranking files; Store, server, API and UI blobs equal root 8010a486 / unchanged. log.md has 0 deletions; no existing .copilot-tracking path modified.

## Limits

Light/author evidence only. Not FULL, independent, hosted or human approval. Root R28/R29 are also author-only.
