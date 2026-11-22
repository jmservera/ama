# Critique: issue 2245 chat ask timeout plan (executed once)

Date 2026-11-22. Verdict: proceed with the narrowed scope.

* Risk: claiming the 120 s cause as proven. Disposition: accepted; research states the lock explanation as supported by code and a 19.4 s ProgrammingError, not by telemetry, and lists the 120 s case as not reproduced.
* Risk: memoising `ensure` could skip a needed reseed (new day, changed settings, new ledger, patched budgets in tests). Disposition: key on label (date), configuration, CALLS, TOKENS, AMOUNT and store it on the ledger instance; failures are never cached.
* Risk: stale cache if the ledger rows are deleted out of band. Disposition: acceptable for the synthetic demo; a restart reseeds.
* Risk: changing the lock timeout or hold ordering widens scope into security controls. Disposition: rejected; suspension and lock semantics are untouched.
* Tier: src change, so FULL tier applies; the coordinator runs the gate. Local checks here are the targeted tests and mypy/ruff only.
