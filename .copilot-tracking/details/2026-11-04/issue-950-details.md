---
title: Issue 950 phase details
ms.date: 2026-11-04
---

* `SEED_PROPOSER = "Phase 0 discovery seed list"`, passed as `proposed_by` for all five seeds.
* Test asserts every seed has a non-empty proposer, that the proposer cannot decide its own seed, and that a named owner can.
