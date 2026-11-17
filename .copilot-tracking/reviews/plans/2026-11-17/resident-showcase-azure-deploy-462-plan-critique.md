<!-- markdownlint-disable-file -->
# Plan critique: resident-showcase-azure-deploy-462

Date: 2026-11-17. One final-candidate critique, performed by the worker before implementation.

| ID | Finding | Disposition |
|---|---|---|
| C-01 | Registry window is the riskiest step: a failed restore leaves public access open. | Applied: trap before first mutation, readback equality, stop on mismatch. |
| C-02 | Cost headroom is RG-only and billing lags; absence of all-in forecast. | Applied: record as limit, incremental plan under USD 1, stop on unknown. Not claimed as complete forecast. |
| C-03 | Image-only update assumes SQL view and Key Vault references are unchanged. | Applied: SQL file diff is empty since the deployed source; startup failure rolls back to the old digest. |
| C-04 | Browser credentials could leak through tool arguments or logs. | Applied: local script reads the file in-process; no printing; screenshots reviewed for absence of the password field value. |
| C-05 | Ingress is already external; leaving it open widens exposure. | Recorded: owner-approved synthetic demo, expiry-gated by `ZF_DEMO_EXPIRES_AT`, fail-closed login; stop plan documented. |
| C-06 | A root 200 is not acceptance. | Applied: acceptance requires real login, correct-case data and negative paths. |

Verdict: proceed. No finding conflicts with a confirmed owner decision.
