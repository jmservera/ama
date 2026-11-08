---
title: Issue 1231 r21 plan, merge parent79 b8ad4a0e
description: Prospective plan for one normal local merge of parent79 b8ad4a0e into the child
ms.date: 2026-11-07
---

Details: `.copilot-tracking/details/2026-11-07/issue-1231-r21-parentb8ad-details.md`. Critique: `.copilot-tracking/challenges/2026-11-07/issue-1231-r21-parentb8ad-critique.md`.

* [ ] Phase 1: re-verify identities; create `backup/issue-1231-8d235-pre-r21-merge`.
* [ ] Phase 2: one `git merge --no-ff` of b8ad4a0e; abort only it on conflict.
* [ ] Phase 3: prove parents, main 23b26a7f ancestry, incoming raw/mode/blob delta, all non-record blobs outside the two incoming paths unchanged, original RPI bytes and log prefix preserved.
* [ ] Phase 4: no suite reruns when proof holds; JSON validity of latest.json; git diff --check.
* [ ] Phase 5: records, commit, freeze.

Exclusions: FULL, lock, SQL, browser, images, scanners, cloud, push, PR update, ticks, parent/main mutation, cleanup.
Follow-up: sole FULL with --lock-timeout 0, independent review, hosted checks, new parent integration FULL.
