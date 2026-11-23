# Issue 350 r8 research (2026-11-23)

Disposition: executed. Planning Readiness: Ready.

Criterion 1 is the first unticked box. r7 showed the edge returns 302 for browser-style anonymous API requests; the app returns 401. Excluding `/api` from Easy Auth would let unauthenticated traffic (and spoofable X-MS-CLIENT-PRINCIPAL headers) reach the app without platform proof, and the SPA needs the platform principal on API calls. So the safe code-level step is a regression guard: neither Easy Auth module may exempt `/api` paths, until trusted-principal proof exists. Live re-probe by the r7 tool follows.
