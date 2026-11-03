# Research: Profile journey contract and same-home journey (Refs #134, R1)

Research disposition: executed (repository inspection). Planning Readiness: Ready for slice 1.

## Already delivered (not redone)

* #103: versioned scenario manifest and offline coverage audit (`synthetic/scenario_manifest.py`); all eleven profiles and nine workflows are recorded `unavailable`, by design, until a reviewed evidence contract exists.
* #76 role queues, #75 building context (`buildings.py`), stock conflicts (`stock.py`), quality, finance and technical sign-off audit actions exist in `core`.
* #233 atlas-to-screen trace covers screens, not an event trace. No merged PR delivers a same-home event trace; PR #392 (#88) is unrelated to this issue's criteria.

## Gap against acceptance criteria

1. Eleven perspective walkthroughs over linked records: unmet (manifest still unavailable).
2. AC-034 to AC-043: unmet as a set; no per-AC pass/deferred record.
3. Same-home journey with event order and unknown intervals: no code. Slice 1 target.
4. Sibling and building isolation negative controls: partially (building tests exist); no journey-level control. Slice 1 target.
5. Textual state, keyboard, announcements: unmet (needs screens).
6. Constructed-fixture labelling: slice 1 labels output.

## Evidence for slice 1

Audit entries (`at`, `who`, `action`, `case`, `detail`) carry the actions `stock_comparison`, `stock_query_resolve`, `resident_decision`, `technical_signoff_give`, `quality_accepted`, `quality_handover`, `finance_payment_status`.

## Stacked slices proposed

1. Pure trace function and negative controls (this PR).
2. End-to-end store journey test through handover and finance, then an API read route.
3. Per-AC pass/deferred register for AC-034 to AC-043 and manifest evidence contract.
4. Per-perspective walkthrough screens/checks and accessibility evidence.
