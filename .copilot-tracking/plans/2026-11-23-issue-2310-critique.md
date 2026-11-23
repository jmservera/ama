# Issue 2310 plan critique (single pass, 2026-11-23)

Verdict: accept. Execution: once.

* Adding a duplicate test would restate #1005 coverage; rejected (compatible with the no-duplicate-tests rule).
* Changing the edge auth to Return401 or excluding `/api/*` changes the production boundary; the owner decision forbids production changes. Recorded as a follow-up, not done.
* No src change, so focused tier; never run rpi-checks --all.
