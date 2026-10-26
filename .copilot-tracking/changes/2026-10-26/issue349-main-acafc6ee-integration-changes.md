<!-- markdownlint-disable-file -->
---
title: Issue 349 integration of main acafc6ee changes
description: Record of the normal merge of origin/main into the topic
ms.date: 2026-10-26
---

Plan committed before the merge (issue349-main-acafc6ee-integration-plan.md).
Merge commit 147980af (parents 26a9f2e1 topic, acafc6ee main), normal merge, no
rebase, no force, no push. Merge message amended once before any publication to
add the required trailer.

* Result: automatic merge, no conflicts. latest.json equals main's version;
  docs/reference/log.md has zero removed lines relative to either parent, so both
  append-only intents are kept. No .patch archive, review, runner or infra path
  differs from the first parent.
* Remote e95c0f51 and main acafc6ee are both ancestors of the merge.
* Validation: tools.test_rpi_checks 14 OK; infra preflight and container contract
  tests 42 OK; git diff --check (excluding byte-preserved patch archives) clean.
* Review decision: no conflict resolution was needed and the main delta was
  additive and disjoint from the topic's tools and infra paths, so no separate
  integration review was run; this is a decision, not a review outcome.
* Not done: full gate (the 0fe8c3be failed receipt and earlier receipts stay
  historical), push, PR or issue edits. Not whole-issue or live acceptance.
