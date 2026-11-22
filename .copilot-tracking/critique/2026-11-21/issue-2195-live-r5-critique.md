# Issue 2195 r5 critique

One critique of the final candidate plan. Verdict: proceed with applied findings.

* C-1: r4 rejected the SQL fix because the 500s did not recur; they recurred (log evidence). Applied: carry the fix from 193c9aaa90 with its test.
* C-2: Root cause is unlogged. Applied: record the fix as unproven live until deploy; do not claim the 500s are cured.
* C-3: Explicit transactions can still interleave across threads. Applied: record as a limit, no wider redesign.
* C-4: Deploying an image changes the Azure estate. Applied: deploy is out of this task; local commit only.
