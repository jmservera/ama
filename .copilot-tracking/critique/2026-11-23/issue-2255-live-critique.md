# Critique: issue 2255 live re-check (2026-11-23)

Executed once on the final candidate plan. Verdict: proceed.

* The only open criterion (re-seed survival) cannot be proven read-only; a re-seed would change the demo store and the generator is outside the repo. Plan states it as owner-gated, not proven. Applied.
* A src change would be speculative (merge_seed is insert-only by design). Rejected; no src change, focused tier.
* Probe must wait for the last ranked row to avoid an undercount. Already in the reused probe.
