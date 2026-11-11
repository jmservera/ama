<!-- markdownlint-disable-file -->
# Plan critique: aftercare blank stored state (issue 1402, C1)

Executed once on the final-candidate plan by the rubber-duck agent (observed, read-only, no tests run). Verdict: needs changes; both findings applied directly.

* CK-01 Blocking: the plan ran SQL-backed suites (`test_aftercare_store.py`, `test_aftercare_served.py`). Applied: removed; recorded N/A because SQL is not admitted and the adapter cannot reach the changed branch.
* CK-02 Non-blocking: one test could mask later assertions with an early failure. Applied: independent test methods per path with bytes checked after each attempt.
* Confirmed: one-line fix sufficient for the file-store boundary; both `_parse` callers refuse blank state; `handle()` maps to 503; a failed update may create a `.lock` file but not alter the state file; unreachability claim holds for `DocumentStateStore` canonical output only (its `None` also covers a stored JSON null), not as a universal adapter claim.
