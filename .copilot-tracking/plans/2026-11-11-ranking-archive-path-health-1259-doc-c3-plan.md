---
title: Issue 1259 documentary C3 plan
description: Prospective plan for additive qualification of four evidence-documentation errors
ms.date: 2026-11-11
---

## Objective

Correct only four documentation errors by additive, dated qualification. No source, test, runner, workflow, script or manifest change. No run of any command beyond Git and Markdown hygiene. No critique round beyond what the owner already received from the independent report (recorded as the critique input; no further critique, one author review).

## Steps

1. Commit research, plan and details first (this commit) before any qualification edit.
2. Create `changes/2026-11-11-ranking-archive-path-health-1259-doc-c3-changes.md` as the canonical current description: corrected old-red reach, corrected counts, run.sh and exit qualification, process disclosure.
3. Append one short "Superseded in part" pointer section to each of the original failing-first changes, review and details records; no original text is rewritten. Raw logs and `run.sh` stay byte-identical.
4. Create one new author review and state file. Leave the original review and state untouched.
5. Hygiene: `git diff --check`, relative-link check, plain-ASCII/no em dash check, file list limited to exact explicit paths, `git add` by explicit path only.
6. Commit with the noreply identity for author and committer and the Copilot trailer. Write `handoff-1259-doc-c3-2133.txt` outside the repository.

## Boundaries and stops

* AC4 stays Partial and unticked; AC5 unmet; no whole-issue acceptance. No push, PR, issue, board or merge.
* Stop if any step would need an observation, a source edit or an unrelated file; record the blocker instead.

## Checkpoints

* [ ] Research, plan, details committed.
* [ ] Qualification, pointers, review and state written.
* [ ] Hygiene and final commit.
