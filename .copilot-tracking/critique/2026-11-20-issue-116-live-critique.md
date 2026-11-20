# Issue 116 live critique (2026-11-20)

Execution: one pass on the final candidate plan. Verdict: proceed.

* Finding: do not tick the issue box on the strength of per-site tests alone; require a boundary matrix naming each site and its test. Disposition: applied in the plan (matrix in the research note).
* Finding: a new test must fail without the property it pins. Disposition: the proactive test injects a hidden canary in `dispatch` and asserts byte equality with the requested payload plus `as_of` view; it fails if `build_request` ever serialises dispatch fields.
* Finding: no source change is warranted for resident_demo and heldout sites; they are already bounded and inventoried. Disposition: accepted, recorded as proven offline.
* Conflicts with confirmed decisions: none. Significant or divergent issues: none.
