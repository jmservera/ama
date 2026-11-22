# Issue 146 critique (2026-11-22), one pass

Verdict: proceed with narrowed scope.

* Adding entries to the src coverage register would force the FULL tier; skip it and document the new alerts in the runbook only. Accepted.
* DTU alert must exist only when `sqlTier == 'dtu'`, since `dtu_consumption_percent` is absent on vCore tiers. Accepted.
* Use Average over 15 minutes at 80 percent, not Maximum, because observed hourly maxima already reach 92 percent. Accepted.
* Receiver job alert in a separate template must be optional (empty action group means no rule) so the existing deployment contract does not change. Accepted.
* Do not claim any criterion proven by source authoring; deployment and notification drills are out of scope (no live change). Accepted.
