# Issue 2310 live research (2026-11-24)

Disposition: executed (reuses 2026-11-23 findings, re-probes live on revision 0000067).

* Prior runs: code and tests already return 401 for anonymous /api/ requests (GET, HEAD, POST, PUT, PATCH, DELETE); live Easy Auth edge returns 302 (`RedirectToLoginPage`).
* Open question: has revision 0000067 changed the edge behaviour? Probes below decide.
* Planning Readiness: Ready.
