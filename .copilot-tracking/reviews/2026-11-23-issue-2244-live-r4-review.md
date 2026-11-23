# Review 2244 live r4 (2026-11-23)

Executed once by the implementing agent. Outcome: conformant with open follow-ups. Independent exact-head review, hosted CI and the complete gate remain required and are not claimed.

* The fast path only reads; the locked path still re-counts, so concurrent first starts stay safe.
* The test fails without the change.
* Residual risk: failures in the full core run are in unrelated Azure SDK tests and were not baselined.

## Open follow-ups

* Read-only currency checks for `_migrate`, `_migrate_recommendations`, `_ensure_queue_membership`.
* Owner deploys, then watches a scale-out (C3, C4); identify the lock holder (C5).
