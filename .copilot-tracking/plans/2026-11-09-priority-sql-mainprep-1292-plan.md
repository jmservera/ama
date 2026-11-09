---
title: Issue 1292 current-main priority SQL candidate main-preparation plan
ms.date: 2026-11-09
task_id: 1292-current-main-sql-mainprep-1109
---

## Objective and boundary

Merge `origin/main` `1a84b3b0054990262a0df0625d95e3f545d2739a` into `test/demo-priority-sql-main-1292-1109` with a normal merge commit so a later PR does not target conflicting append-only knowledge-base pages. Git and Markdown only. No runtime check is required because the `src`, `tools`, `infra` and `.github/workflows` tree ids equal the executed source. No SQL, no campaign, no source or harness change, no push, PR, issue or board write, no rebase, amend, reset or force.

## Phases

* M0 Planning commit. Commit this research, plan, details, critique and state record before the merge. Fetch and require `origin/main` to equal the pinned sha; any SHA mismatch stops the lane and the new delta is reassessed. Compare tree ids; if `src`, `tools`, `infra` or `.github/workflows` differ from the executed source, STOP, report a validation dependency, and do not run the campaign automatically.
* M1 Merge. `git merge --no-ff --no-commit origin/main` is not required; use `git merge origin/main` and resolve only the two append conflicts by keeping both sides: in the evidence pack keep main's two sections first and the candidate's 1292 subsection after them (chronological by merge, no text change to either); in the README index keep main's bullets and the candidate paragraph in the order each block appeared. Merge the exact pinned sha `1a84b3b0054990262a0df0625d95e3f545d2739a`. Accept the order the three-way merge gives the log (candidate entry before main's two entries, verified by dry run) and verify all entries are unchanged; no reorder. Commit the resolved merge on its own before any binding edit. Unclear semantic conflict: abort with `git merge --abort`, record the blocker, no guessed approval.
* M2 Provenance binding (separate commit after the merge commit). Add a dated current-target binding to the candidate's existing evidence-pack subsection and a new append-only log entry: executed at `e208748cf` and source tree `86bc00e19a16`, 148 tests, 67 on SQL Server, 0 skips, one 540 s admission; current main `1a84b3b00` has identical `src`, `tools`, `infra` and `.github/workflows` trees, so no rerun; startup cause UNKNOWN; AC3 old-behaviour-fails half unproven; no full gate, Azure, live, human or whole-81/440 acceptance; no criteria ticked. Controls/photo 13 and 83 observations and the 1314 qualification are identified as historical records on main, not fresh claims. No old record is edited.
* M3 Validation (on the final tree after both commits, comparing preserved blocks against both parents). Markdown link check for the touched KB files, grep that both sides' headings, bullets and log headings survive (no deleted lines versus either parent except conflict markers removed), `git diff` range checks: candidate-only lines preserved, main-only lines preserved, source tree equality, absence of conflict markers. Derive final path counts from the actual Git range, not intermediate file counts.
* M4 Records and freeze. Changes record, Review record (authored by the implementing session, not independent), state update, handoff `handoff-1292-evidence-main-preparation.md` in the session files directory with exact head, tree, current main, original `6c05b1e12..final` delta and own-versus-actual-main comparisons. Commit; the worktree stays clean and local only.

## Acceptance of this lane

* Ordinary merge commit with first parent the planning commit of this lane (whose ancestry contains `6c05b1e12`) and second parent `1a84b3b00`; no conflict markers; both log entries, both index additions and both pack sections present byte-for-byte; `src`, `tools`, `infra` and workflow trees equal to the executed source; original `6c05b1e12` an ancestor of the final head; no push or remote write.
* Not accepted by this lane: independent review, hosted CI, AC mapping, any criterion tick or closure.
