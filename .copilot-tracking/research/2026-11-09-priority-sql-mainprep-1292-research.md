---
title: Issue 1292 current-main priority SQL candidate main-preparation research
ms.date: 2026-11-09
task_id: 1292-current-main-sql-mainprep-1109
---

## Scope

Git and Markdown integration only. Bring the local evidence-only candidate (`6c05b1e12922205286400a17c73957c9c23bb35e`, planning commit `e208748cf`) up to current `origin/main` with one ordinary merge before any later publication decision. No SQL execution, no source, test or harness change, no new campaign, no Source E5, no push, PR, issue or board write. Research disposition: executed (Git read-only inspection).

## Actual identities (fetched 2026-11-09)

* Candidate head: `6c05b1e12922205286400a17c73957c9c23bb35e`, tree `9752a876ccadff51edba16f61c461762f4ee6a06`, base `ba71894bb1a94d6a24aabf9828312668f88f3ff5`. Diff versus base: 10 paths, +319, 0 deletions.
* `origin/main`: `1a84b3b0054990262a0df0625d95e3f545d2739a` (merged PR 1322, parent #1322 / child #1324 controls and photo checkpoint, on top of rubric commit `5c3b8b4be`). Merge base with the candidate: `ba71894bb`.
* Main delta versus the executed base (`ba71894bb..origin/main`): 18 paths, +623 / -10: 14 `.copilot-tracking` records (controls checkpoint 440 and count qualification 1314), `docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md`, `docs/reference/log.md`, and `.github/rubric/scores/latest.json` (rubric score data from `5c3b8b4be`, not a workflow).

## Executed-source equality (decisive)

Tree ids are identical between the executed candidate and current main for `src` (`86bc00e19a167e517ae2955ad88d6e2f7b4eac26`), `tools` (`74ad3cb586dbff7f08ed3ba78301b9596a31ca86`), `infra` (`b0969f8b7b8c3b21763c5f332123ef5ea2aac94d`) and `.github/workflows` (`29eb03ea759ea6717e334d8f0949915d5ba37a90`). The only non-docs, non-tracking path that moved is the rubric score JSON. The stop condition (src, tools, infra or workflow changed versus the executed source) does not hold, so the validation stays bound to unchanged source and no campaign is repeated.

## Conflict surface (read-only `git merge-tree`, no merge performed)

* `docs/architecture/cutover-evidence-pack.md`: append conflict at the end of file. Main appended the 1314 count qualification subsection and the 440 controls checkpoint section; the candidate appended the 1292 current-main priority SQL subsection at the same place.
* `docs/reference/README.md`: append conflict. Main added index bullets for the 440 and 1314 records; the candidate added the 1292 current-main paragraph.
* `docs/reference/log.md`: auto-merges (both appended entries; verify order and preservation after the merge).
* `.copilot-tracking` records: disjoint names, no conflict.

## Decisions to preserve

* Both append-only log entries, both index additions and both pack sections are kept in full. No row is deleted and no historical count is rewritten to resolve a conflict.
* Main's controls checkpoint and its initial controls/photo observations (13 and 83 browser observations) and the 1314 count qualification stay historical and dated as main recorded them. The candidate neither restates nor refreshes them.
* The candidate's own records, the Revise C1 to C7 critique, the authored Review and the raw 30-member sanitized evidence stay immutable.
* Where a main-side statement and the candidate disagree semantically (not merely order), stop and report rather than guess.

## Boundaries that remain true

* The historical startup cause stays UNKNOWN; the old-behaviour-fails half of AC3 stays unproven; no full gate, Azure, live, human or whole-#81 or #440 acceptance; no criteria ticked or closed.
* Executed evidence is bound to commit `e208748cf` (planning) / source tree `86bc00e19a16`: 148 tests, 67 on SQL Server, 0 skips, one 540 s admission. Because the source tree is unchanged on the new head, no ceremonial SQL rerun is justified.

## Planning Readiness

Ready. Merge in an ordinary non-rebasing way on the candidate branch after the planning commit of this preparation.
