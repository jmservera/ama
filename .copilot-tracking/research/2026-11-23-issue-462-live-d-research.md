# Research: issue 462 fourth pass (2026-11-23)

Disposition: executed (targeted, reusing r3 to r8). Planning Readiness: Ready.

Scope: desktop synthetic demo; live Azure authorised in `ama`; no Azure change made.

Findings

* Live app `ca-resident-demo--0000028` (digest prefix `sha256:e6c7e755`) still returns no `Strict-Transport-Security`; source already carries it (commit 02e63b0690). Redeploy is outside this pass (brief: no estate change).
* Live responses send `server: ZavaResidentDemo Python/3.12.15`. `BaseHTTPRequestHandler.version_string()` appends `sys_version`, disclosing the interpreter version on a public login surface. `resident_demo/app.py` Handler sets only `server_version`. This supports criterion 3/4 (abuse and error controls, no information leakage) and is code-satisfiable.
* Criteria 1, 2, 6, 7 have no further code work; evidence stays in r3, r7, r8.

Unproven for the demo: owner ticking of 1, 2, 6, 7; live HSTS; full gate.
