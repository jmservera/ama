# Review: issue #108

* Review execution: executed once, self-review of the diff. Outcome: conformant for the two criteria at the unit level; no independent review or hosted CI yet.
* Findings: (1) `lever_deltas` repeats the same candidate-vs-baseline delta for each lever in a composite, because per-lever attribution needs separate runs; follow-up. (2) Real-model/held-out evidence remains outside this change.
* Classification: focused tier (non-gate-semantics tooling and tests); the gate stays strictest-fail. Independent exact-head review and owner approval remain required. Not pushed.
