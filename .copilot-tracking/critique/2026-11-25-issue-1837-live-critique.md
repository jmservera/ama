# Issue 1837 critique, 2026-11-25

Executed once on the final candidate plan. Verdict: proceed.

* Finding 1: a passing new test cannot be failing-first. Disposition: state this plainly; the original failing-first run at 9da3fcd stays the evidence for the first criterion, and no mutation of shared source is made. Applied.
* Finding 2: the test must not overlap the acknowledge negatives. Disposition: cover only `nomination_correct` and `challenge_open`. Applied.
* Finding 3: a defect found would change tier to FULL. Disposition: stop and report rather than run the full gate. Applied.
