---
title: SQL feature-recovery wave checkpoint 440 C2 qualification details
ms.date: 2026-11-09
task_id: 440-sql-wave-checkpoint-1109-c2
---

## Phase details

* P1 Stage the five planning files (research, plan, details, critique, state) and commit as `docs(rpi): plan C2 qualification for SQL wave checkpoint (#440)` with the Copilot trailer; author and committer are the repository-local GitHub noreply identity.
* P2 Edit `docs/architecture/cutover-evidence-pack.md` by inserting after the findings and recommendation sections a new heading `### C2 qualification, 2026-11-09` (heading level matching its siblings) with a short table or list for Q1 to Q3. Each statement names its source anchor or label it as coordinator-reported.
* P3 Insert one sentence below the SQL-wave behavior table: "Qualified 2026-11-09 (C2): the last row's `committed or uncertain` wording is narrowed; see C2 qualification Q1." Do not edit the row.
* P4 Index: one concise sentence in the existing SQL-wave paragraph in `docs/reference/README.md`. Log: one appended entry at the end of `docs/reference/log.md`.
* P5 `git merge origin/main` (no fast-forward needed); expected conflict-free. Verify `git diff --stat origin/main..HEAD` after.
* P6 Checks: `git diff --stat`, added-line ASCII and em dash scan, grep of anchors in the pack, `git diff origin/main -- docs/reference/log.md` is append-only, no path outside docs and `.copilot-tracking`.

## Dependencies

* P2 to P4 depend on P1 being committed. P5 depends on P4. P6 depends on P5.
