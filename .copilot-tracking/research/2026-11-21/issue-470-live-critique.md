# Critique: issue 470 gate scan count

Executed once on the final candidate. Verdict: compatible, proceed.

* A literal bump keeps exact-count strictness; deriving the count from the receipt would weaken the gate. Accepted.
* Risk: the count drifts again when scans are added. Accepted as a deliberate tripwire; recorded as a follow-up to export a declared count.
* Boundary negative tests must move with the literal (90, 92). Applied.
