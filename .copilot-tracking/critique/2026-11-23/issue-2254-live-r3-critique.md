---
title: Issue 2254 live critique, run 3 (2026-11-23)
---

Executed once on the final-candidate plan. Verdict: proceed.

* The fix already exists on the base; the plan correctly avoids a redundant `src/` change and keeps the focused tier.
* Risk: the map assertion could be vacuous if `map_view` clusters. Mitigation: assert `mode == "points"` first.
* Risk: filter argument shape for `map_view`. Mitigation: read `insights.matches` before editing.
* Live probes are observational; the live stale-row cause stays unproven (SQL public access disabled; not changed).

Dispositions: both mitigations applied directly in Phase 2.
