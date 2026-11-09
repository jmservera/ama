---
title: SQL wave checkpoint 440 current-main preparation plan
ms.date: 2026-11-09
task_id: 440-sql-wave-checkpoint-1109-mainprep
---

## Task metadata

* Task `440-sql-wave-checkpoint-1109-mainprep`, parent `440-sql-wave-checkpoint-1109-c2`. Research: `.copilot-tracking/research/2026-11-09-sql-wave-checkpoint-440-mainprep-research.md` (executed, Ready). Details: `.copilot-tracking/details/2026-11-09-sql-wave-checkpoint-440-mainprep-details.md`.
* Branch `docs/demo-sql-checkpoint-440-1109`, base head `f2e07999386399694abe91562555b35c0105ab9b`, target `origin/main` `3a9767d5cf728c5e3be76813ce0bfdac4c06841e`.

## Executive summary

Bring merged main into the branch with an ordinary `--no-ff` merge, preserving both main's lifecycle pack records and the existing SQL-wave and C2 sections, then add one small dated provenance note. No source edit, no new correction cycle.

## User decisions and requirements

* Source-preserving preparation; C1 and C2 spent, 3 remain unused. No amend, rebase, force, stash or reset.
* Do not fix the Low 15 versus 17 scope finding (follow-up #1314, D5 after C1 and C2) and do not rewrite earlier author or reviewer outcomes. Preserve the earlier partial assessments and the new complete Readiness at `f2e07999` as external evidence.
* Pure documentation: no tests, gates, services, browser or model. Owner demo tier: no gate for pure documentation. Hosted checks and independent exact-head review stay mandatory and separate.
* Reuse the already read prefix coverage via exact byte proof; read only new main append and context.
* Stop and report specific conflicts if intent is ambiguous. No push, PR, issue, board or merge to main.

## Implementation phases

1. P1 Commit this research, plan, details, critique and state BEFORE the merge or any documentation edit.
2. P2 Fetch, confirm `origin/main` is still `3a9767d5c`, run `git merge --no-ff origin/main`. Expected clean (merge-tree exit 0). On conflict, resolve by preserving both entries; stop if intent is ambiguous.
3. P3 Prove source equality: `git diff origin/main HEAD -- src infra tools .github` is empty, and the changed path inventory outside `docs/` and tracking is empty.
4. P4 Append, after the C2 qualification, a dated "Current-main preparation (2026-11-09)" subsection: identities, observed source `8d6f029ca` versus current base `3a9767d5c`, lifecycle not retested or accepted by this record, whole #81 and #440 open, the next lifecycle-wave checkpoint trigger, affected closure hold, resume point, independent #189, #954, #159 work permitted, no legal, resident or production approval. Add one index sentence and one log entry, append-only.
5. P5 Validate: relative Markdown links, append-only prefix equality of pack and log against the merge parents, original RPI bytes unchanged, clean tracked tree, ignored inputs listed.
6. P6 Changes record, one Review, state, commit, handoff.

## Acceptance criteria

* AC1 Merge commit has the P1 planning commit (a child of `f2e07999`) and `3a9767d5c` as parents, so `f2e07999` is on first-parent ancestry; no conflict markers. Final-state checks (source equality, path inventory, clean tree, preservation) run after the last commit (P6), not before.
* AC6 Preservation: `git diff --numstat` of the final pack, log and index versus each of `f2e07999` and `origin/main` shows 0 deleted lines (all lines of both parents are kept in order, only additions).
* AC2 Final tree differs from `origin/main` only in pack, index, log and own tracking records.
* AC3 Both main's new pack sections and the SQL-wave and C2 sections are present, in order.
* AC4 The note distinguishes observed source `8d6f029ca` from current base `3a9767d5c` and does not claim a completed lifecycle checkpoint, acceptance or closure.
* AC5 Original RPI files byte-equal to `f2e07999`.

## Risks

* R1 Concurrent main advance: refetch before merging and report any new SHA.
* R2 Pack line 5062 and 5263 insertions of main shift anchors; verify anchors after merge.
