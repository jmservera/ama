<!-- markdownlint-disable-file -->
---
title: Issue 349 integration of main acafc6ee plan
description: Prospective plan for a normal merge of origin/main into the topic
ms.date: 2026-10-26
---

Written before the merge. Inspected delta (git diff HEAD...origin/main): 42 paths,
owner PR 460, docs, tracking, rubric, requirements. Overlap candidates:
.github/rubric/scores/latest.json and docs/reference/log.md; other touched
tools paths (tools/cowork-native-recovery) are disjoint from tools/rpi-checks.py.

* Merge: git merge origin/main (normal, no rebase, no force, no push).
* latest.json conflict: take main's version (rubric baseline, as in the earlier merges).
* log.md: expect auto-merge; verify no removed lines in either side's entries. If
  a conflict arises, keep both append-only entries; stop if intent is ambiguous.
* Any other conflict: stop and report.
* Preserve all original reviews, receipts and byte-preserved historical archives
  (verify git diff of those paths against the first parent is empty).
* Validate: tools.test_rpi_checks (14), infra preflight tests (35), container
  contract tests, git diff --check limited to non-archive paths. No gate, Docker or push.
* Review: one bounded independent integration review only if conflicts needed
  resolution or the diff is not purely additive; record the decision.
* Existing receipts, including the earlier 0fe8c3be failed gate, stay historical.
