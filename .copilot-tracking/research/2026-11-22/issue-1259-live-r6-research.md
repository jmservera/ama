# Research: issue 1259 live run 6 (Refs #1259)

Disposition: executed. Planning Readiness: Ready.

* Main check: `origin/main` is 10cad2e413 and equals HEAD. The fix (`ranking_publication.py` lines about 387-430) and `UnusableArchivePathTests` already exist on main (fix from cd687abadd).
* Unticked criteria: regression coverage with failure before the fix (evidence reproducible), and RPI/FULL receipt/exact-head assessment/hosted checks (not provable for the demo).
* Red-before: pre-fix worktree at cd687abadd^ with current tests: 6 run, 7 failures. Green-after: 110 tests OK.
* Scope: synthetic, local only; no Azure, no credentials. No src change planned, so FULL tier is not triggered.
