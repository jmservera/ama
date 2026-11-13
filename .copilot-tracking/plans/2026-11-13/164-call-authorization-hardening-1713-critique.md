# Critique: 164 call authorization hardening

Executed once by rubber-duck before implementation. Verdict: Revise. Dispositions (all compatible, applied):

* Bounds: wrapper requires finite conservative `tokens_per_call` and `spend_per_call`; unbounded blocks. Provider-enforced output limits are a provider-integration item for the owner-approved actual-model step (not implemented here).
* Reserve before dispatch in a shared `CallLedger`; reservation is kept when the provider raises.
* Shared ledger object passed to every wrapper so limits do not reset per Run.
* Validate `authorised_by` is a non-blank str; request/used counts are non-negative ints and finite non-negative spend.
* Default clock is live UTC; injection kept for tests only.
* Report keeps `actual_model_calls: 0` (no actual provider is run by `run_eval`); gate is exercised by `Run(provider=...)` tests.
