<!-- markdownlint-disable-file -->
# Critique: issue 1288 H2 plan (one critique, before any observation)

Readback `date -u` 2026-11-10T00:24Z. Reviewer: rubber-duck, read-only. Verdict: Revise (3 blocking, 2 non-blocking). All applied in the plan amendment of the same date.

* Blocking: snapshots could miss the revoking call (`detail`/`release_reference` can assess and invalidate). Applied: separate before/after snapshots for each step.
* Blocking: later fixtures drop tables and reinstall releases, so they could overwrite H2 evidence. Applied: H2 runs in a first separate process and persists its verdict before the selectors run.
* Blocking: an unmatched baseline could pose as a contrary result. Applied: prerequisite gate; failure is inconclusive.
* Non-blocking: "restart" overstates the test. Applied: described as independent same-process reopen.
* Non-blocking: zero-call and durability endpoints. Applied: per-provider counter deltas, task and control capture after B and C, no unmeasured byte claim.

No further critique is run for this task.
