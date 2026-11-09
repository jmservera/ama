---
title: Issue 86 integration of local parent ae54963 plan
description: Plan for one normal merge and no-service checks (Refs #86)
ms.date: 2026-11-07
---

Tier: FULL for the eventual integrated head (source, SQL, security surface). No FULL, service, browser, scanner or lock queue is admitted here; #107 is the heavy holder. FULL and independent review are coordinator gates later, and a new parent integration FULL is needed after any child merge.

## Steps

1. Commit research, plan, details and critique first (author-only critique, not independent).
2. Re-verify HEAD, parent identity and `origin/main` `8af3aea6`; stop on drift.
3. One normal `git merge --no-ff ae54963…`. No rebase, force or history rewrite. Stop on any conflict.
4. Verify two parents, the incoming delta (raw name-status and modes) separate from planned records, and that child blobs for the five complaint paths equal the pre-merge blobs.
5. Run selectors in details from a git-archive snapshot of the merged tree, with import origins.
6. Write changes record and one author Review, commit, freeze clean.

## Non-goals

No behaviour change, weakened test, migration, receiver delivery, push, PR update, tick or approval.
