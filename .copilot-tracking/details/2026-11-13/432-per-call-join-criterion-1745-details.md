---
title: Issue 432 Criterion 6 per-call join details
ms.date: 2026-11-13
---

## Phase 1 details

Helper `call_join(meter_id)` returns the reserved, completed and output records for one call and asserts:

* reserved: capability, case_type (`retrofit-case`), model (`test-model`), configuration, prompt, retry, root, attempt present.
* completed: tokens prompt 100, completion 20, total 120, cached 10; outcome; held False.
* output: exists for the root, with output id.
* all three records' values carry no canary case text (JSON dump scan) and only opaque hashes.

Worker case: `run_ready("assessment-preparation")`; expect retry matches `task["attempts"] - 1`, outcome `returned`, eligible True.
Chat cases: returned, revoked (outcome `activation-revoked`... verify actual ledger outcome), provider-failure (outcome `provider-unavailable`, tokens None) joined to an ineligible output. Reuse the existing chat adapter setup by extending the existing chat test with helper calls to avoid duplicating setup.
