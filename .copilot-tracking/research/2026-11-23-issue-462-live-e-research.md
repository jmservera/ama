# Research: issue 462 fifth pass (2026-11-23)

Disposition: executed (targeted, reusing r3 to r9). Planning Readiness: Ready.

Scope: desktop synthetic demo; live Azure authorised in `ama`; no Azure change planned.

Opening findings

* Live app `ca-resident-demo--0000028`, digest prefix `sha256:e6c7e755`, single active revision at 100% traffic (same as r9).
* Main already carries the HSTS header and the empty `sys_version` fix; neither is observed live until a redeploy.
* Unticked criteria 1, 2, 6, 7 rely on r3 to r9; this pass re-runs the live Playwright proof and looks for one further code-satisfiable defect.

Findings (closing)

* The live Playwright script (36 checks) passes on revision 0000028; evidence in `.copilot-tracking/evidence/2026-11-23-resident-showcase-live-e/`. Live headers are unchanged from r9 (no HSTS, `Server` carries the Python version) because main has not been redeployed.
* New defect. `_body()` in `src/api/src/zava_forward/api/resident_demo/app.py` guards with `length.isdigit()` and then `int(length)`. `str.isdigit()` is true for non-ASCII digits such as superscript two, and `int()` raises `ValueError` on them, outside the `try`. A local probe (valid CSRF cookie and header, `Content-Length` of superscript two) got an empty reply: the connection dropped on an unhandled handler exception instead of a generic denial. No data exposure, but an uncontrolled error path on a public login surface (issue: generic login errors, abuse and error controls).
* Fix: also require `length.isascii()`, so the request falls through to the existing generic 401 path.

Planning Readiness: Ready.
