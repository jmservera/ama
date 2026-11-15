# Details: #440 criteria 7 and 8 closure audit (1848)

Phase 1: Proof table. Per criterion, split into sentence clauses; for each clause give status (Proven / Partial / Unproven), merged evidence (PR, file:line) and the exact missing item.

C7 clauses: dedup/independent scope; severity, reproduction, links, acceptance criteria, dependencies; gating on blocking findings only; owner approval for requirement change, pivot, deferral.
C8 clauses: genuine research/plan/details/changes/independent review in the PR; Major HVE static review; behavior testing; host validation; actual blockers recorded; no unsupported ticks.

Verdict rule: a criterion is closeable only if every clause is Proven by merged, reviewed, surviving evidence. Simulation is not native behavior; attestation without transcript is not independent host evidence.

Phase 2: validation as in the plan. Success: table present, verdicts consistent with the cited lines, diff check clean.
