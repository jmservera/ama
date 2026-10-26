<!-- markdownlint-disable-file -->
---
title: Issue 349 remote-history reconciliation changes
description: Ancestry correction and non-rewriting merge of the owned remote topic
ms.date: 2026-10-25
---

## Correction of an earlier claim

The 2026-10-25 main-integration turn said publication of the merged candidate
would be a fast-forward of remote head 44ba5b77. That was wrong. The candidate
descended from a 2026-10-24 rebase that rewrote the eight remote commits, so
44ba5b77 was not an ancestor (is-ancestor returned 1). The earlier record
(issue349-tenant-readiness-preflight-main-integration-*) is left unchanged and
this record supersedes only that claim. Normal and force pushes were not used.

## Change

Non-rewriting merge commit 155fadad of 44ba5b77 into the candidate line (first
parent ae1e5fa7, the plan commit on top of d78373a5). Its tree is identical to
the first parent's tree (6d99f8fa): conflicts were in
.github/rubric/scores/latest.json (kept main's current score, 73) and
infra/tests/test_tenant_readiness_preflight.py (kept the 13-role
ApplicationAdmin test; the remote's 12-role copy is superseded). The remote
bot score 55 and the remote files remain in history via the second parent.
docs/reference/log.md and the preflight script are identical to the candidate;
no log entry from either side was removed. No source or checker change.

## Provenance proof

* is-ancestor of the new head: 44ba5b77, d78373a5, 229c9199 and ea5577b2 all true.
* All eight remote-only commits (ace512e4 through 44ba5b77) are ancestors.
* Original reviews, critiques, state files and 2026-10-24 adverse evidence are
  unmodified; they were all already present in the candidate.
* Owner-reported login and zero database staff are not independently verified;
  #349 criteria remain unticked.
