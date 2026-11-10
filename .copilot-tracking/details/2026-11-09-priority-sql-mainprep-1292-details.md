---
title: Issue 1292 current-main priority SQL candidate main-preparation details
ms.date: 2026-11-09
task_id: 1292-current-main-sql-mainprep-1109
---

## Exact steps

1. `git fetch origin main`; require `git rev-parse origin/main` to equal `1a84b3b0054990262a0df0625d95e3f545d2739a` (mismatch stops the lane) and record the four tree ids (`src`, `tools`, `infra`, `.github/workflows`) on both sides. Any difference from the executed source stops the lane.
2. `git merge origin/main` (default merge, no fast-forward possible; no `-X` strategy options). Expected conflicts: `docs/architecture/cutover-evidence-pack.md` and `docs/reference/README.md` only.
3. Resolve by keeping both sides in full. Manual edit of conflict hunks only; remove only the marker lines and place blocks in this order: main's block, then the candidate's block. Do not alter wording or counts of either side.
4. After the merge commit, add the current-target binding under the candidate's 1292 subsection and a new log entry after the existing entries. Use ASCII punctuation, `*` lists, no em dashes.
5. Verify: `git grep -n '^<<<<<<<\|^=======$\|^>>>>>>>'` finds nothing in tracked docs; compare added-line sets of each parent against the merged files with `git diff <parent> HEAD` and confirm only the intended additions (binding, new log entry, tracking records) differ; relative links resolve (script over touched Markdown); trees equal; `git merge-base --is-ancestor 6c05b1e12922205286400a17c73957c9c23bb35e HEAD`, run on the final head after both commits.
6. Commit the resolved merge (before step 4) with the repository-local noreply identity and the Copilot co-author trailer; later commit the binding and records separately so the merge commit stays a pure integration.

## Stop conditions

Source/tools/infra/workflow tree difference; a semantic conflict that cannot be resolved by keeping both sides; link or marker failure that cannot be fixed within Markdown; dirty tracked inputs. Record the real evidence and stop, no automatic campaign.
