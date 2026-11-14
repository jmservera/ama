# C1 review

* Execution: one self-review after implementation. Outcome: conformant for the two findings.
* Finding 1 resolved by fixing the stale-DOM race. Finding 2 resolved by the targeted ignore.
* Open (routed, not blocking): the genuine list heading-order gap (`#/`, `#/all`) stays a recorded shrink-only gap for a later template fix; test crawl is slower (about 90s) because of full page loads.
* Human review and hosted CI remain required.
