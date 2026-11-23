# Critique (one pass)

Verdict: approve with dispositions.

* A source-ordering test is weaker than a behavioural race test: accepted, stated as such; the race is browser timing.
* Do not edit the check script (would force recipe/manifest hash churn and FULL tier): applied, test lives in tools.
* No check relaxed: the test only adds an assertion.
