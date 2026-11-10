---
title: Issue 156 process D1 details (2026-11-10)
ms.date: 2026-11-10
---

Provenance qualification content (short, no copying of old evidence):

* Original verify: exit 1, 8 records, log sha256 `9ed0edc8baf4d430900bbd6ce442aead489029203a2c28b083d32d5f7bf8d8ce`, QUALIFIED at seq 6 (review artifact changed after observation, `9e512ae1` to `dbfd26e6`).
* Correct the old handoff claim: it called the result passing with notes; the actual result is exit 1. State this as an additive correction; the old handoff is not edited.
* Launch provenance: seq 1 Root, seq 2 producer. Producer actions were not Root or independent actions.
* Retain: earlier BLOCKED review; later independent approve_with_comments with M1 unresolved and M2 expected local-only; limited coverage; the same reviewer's PROPOSED, PARTIAL, NOT APPROVED, NOT IMPLEMENTATION-READY publication condition.
* No acceptance claims, no source fix, no new corrective grant. Old balance stays UNKNOWN. One D1 debit.

Verification at implement-done and commit: `git diff --name-status d8d103ffc HEAD` shows only new `issue-156-process-d1-1110-*` files; the old witness log hash is unchanged; the new witness `verify` exit is captured directly, not through a pipe, and reported as is.

The old chain is not repaired or re-recorded, and the old state is not cloned.
