<!-- markdownlint-disable-file -->
---
title: Issue 349 remote-history reconciliation research
description: Prospective research before merging the owned remote branch into the candidate
ms.date: 2026-10-25
---

## Facts (git and gh, read-only, 2026-10-25)

* Candidate local head d78373a5 (clean). origin/main ea5577b2. Remote topic and
  draft PR #437 head 44ba5b77 (open, draft), unchanged.
* git merge-base --is-ancestor 44ba5b77 HEAD returns 1: the remote head is NOT
  an ancestor of the candidate. The candidate was produced by a rebase onto
  f1e2d830 in the 2026-10-24 continuation, which rewrote the eight remote
  commits (ace512e4 .. 44ba5b77). My earlier claim that publication would be
  a fast-forward was wrong; the coordinator's correction is accepted.
* Merge base of candidate and remote is 140d8f49. The remote side since then
  changes only three non-tracking paths: infra/scripts/tenant-readiness-preflight.py,
  infra/tests/test_tenant_readiness_preflight.py and .github/rubric/scores/latest.json,
  plus original .copilot-tracking evidence. Every remote tracking file already
  exists in the candidate.
* Candidate versus remote: preflight script identical (0 diff lines); the test
  differs only by the planned 13-role ApplicationAdmin alignment (A1).
  latest.json: remote has the bot score 55/100 for commit bd44d149 (2026-10-23);
  main has score 73 for 7b15a6fc (2026-10-25) with eight fingerprints.

## Conflict intent (predicted)

* Test file: keep the candidate (13 roles). Remote 12-role version is superseded.
* Rubric score: keep main's current score, which is the current-main rubric
  intent. The remote bot score stays recorded in history through the merge
  parent; nothing is edited or fabricated.
* docs/reference/log.md: not changed on the remote side since the base, so
  the candidate's (main's) log is unchanged by the merge; both append-only sets
  remain in history. Ambiguous intent: none expected; stop if one appears.

## Planning readiness

Ready: non-rewriting `git merge` of 44ba5b77, no rebase, no force.
