# Research: issue349 preflight correction 1 (issuer URL validation)

Disposition: reused (independent review finding is the evidence) plus executed code inspection. Planning Readiness: Ready.

* Evidence: coordinator review of head f33c9ff, one Medium functional finding. The issuer check used an unanchored regex, so `https://attacker.invalid/login.microsoftonline.com/<tenant>/v2.0` reported ready.
* Code inspection: `infra/scripts/tenant-readiness-preflight.py` api-issuer-tenant block; the 28 tests only covered a valid issuer and a different tenant.
* Intended contract: `https://login.microsoftonline.com/<uuid>/v2.0` (optional trailing slash), matching the Entra v2 issuer used by the existing auth config.
* Scope: standalone checker and its new test only. Read-only; no tenant or Azure writes.
* The historical gate receipt for f33c9ff was never completed (interrupted by the coordinator); nothing to preserve beyond the head SHA.
