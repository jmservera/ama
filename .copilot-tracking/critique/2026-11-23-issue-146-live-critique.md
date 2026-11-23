# Critique (2026-11-23), executed once

Verdict: proceed with amendments applied directly.

* Risk: a classifier reporting "covered" on disabled rules would overstate coverage. Amendment: status values are `enabled`, `disabled` and `missing`; overall criterion result is `partial` unless all four classes have an enabled rule, and never `proven` (firing is not observed).
* Risk: name-pattern matching drifts from Bicep. Amendment: test cross-checks that every class pattern matches a rule name declared in the Bicep sources.
* Risk: secrets or tenant ids in output. Amendment: output only rule name, class and enabled flag.
* Risk: scope creep into enabling rules. Rejected; no Azure change.
