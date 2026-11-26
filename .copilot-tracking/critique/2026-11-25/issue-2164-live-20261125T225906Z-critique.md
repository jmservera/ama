# Critique (one pass), issue 2164, round 14

Verdict: proceed with one test-only change.

* The test must assert denial for `case_ids` as a string, an over-length list, a non-string entry, and `areas` with an empty string, all on a bound row. Applied.
* Do not touch src: the guard already exists. Applied.
* The live restricted-row proof stays unproven; no roster edit is allowed. Applied.
