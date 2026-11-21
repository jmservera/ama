# Issue 116 live changes (2026-11-21)

## Changes

* Added `docs/reference/research/issue-116-live-r6-evidence-2026-11-21.md`.
* Index row in `docs/reference/README.md`; entry appended to `docs/reference/log.md`.
* No src change; no Azure resource created or changed.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Allowlists and size limits at every provider boundary | Proven offline for every enumerated boundary, including the previously unrun assistants dispatch test; not observable live | r5 matrix plus 104 api and 24 core tests OK at 08fbe37ef; live payload is not visible from deployed apps |
| Role-by-endpoint, contractor view, redaction decision, reason roles | Ticked before this round; live gate re-probed unauthenticated (401 on four endpoints) | r3 to r5 notes hold the credentialed evidence |

Unproven: live model payload contents; a credentialed second-role live run (not repeated this round); independent review and hosted CI. The owner ticks the box after review.
