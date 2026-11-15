# Critique: C1 plan (single pass)

* Verdict: proceed.
* Risk: exposing reviewer identity or notes. Disposition: applied; only decision and timestamps are exported, tests assert no email or note leaks.
* Risk: inventing a supersession field the store lacks. Disposition: applied; derived only from `status == historical` and worded as such.
* Risk: regex fix may expose real false positives. Disposition: the test runs against all web JS at the rebased head.
