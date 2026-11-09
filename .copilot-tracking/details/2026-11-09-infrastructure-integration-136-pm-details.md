---
title: Infrastructure integration 136 post-merge refresh details
description: Phase details for the post-merge refresh plan
ms.date: 2026-11-09
---

## Phase 1 Prospective records

* Files: research, plan, details (this file), all under `.copilot-tracking/`, committed before the merge.
* Done when: critique result is appended and committed.

## Phase 2 Merge

* Command: `git merge --no-ff origin/main -m "<message>"` after `git fetch origin`; target `d4d6827fe60be651cd922ab9656688c18c978e1d` unless main moved (then re-record).
* Done when: merge commit exists with two parents and a clean worktree.

## Phase 3 Evidence verification

* Non-tracking content: compare `git ls-tree -r <ref>` (with modes) filtered to exclude `.copilot-tracking/` for the merge result against `origin/main`, and for `24d1cfb16` against merge base `0f05e9aae`.
* Tracking preservation: for every path under `.copilot-tracking/` at `24d1cfb16`, `git rev-parse <ref>:<path>` equals the merge result's blob id.
* `git diff origin/main HEAD -- docs/reference/log.md` is empty.
* Before the merge, re-fetch and confirm main is still `d4d6827fe60be651cd922ab9656688c18c978e1d`; otherwise stop and reassess.

## Phase 4 Records

* Changes, review and state JSON for `infrastructure-integration-136-pm`; handoff to the coordinator files directory.
* Review is author-only; the independent exact-delta closure and hosted checks remain coordinator actions.
