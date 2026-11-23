# Issue 350 r7 details (2026-11-23)

Probe matrix: paths `/api/me`, `/api/cases`, `/api/staff`, `/app`; header sets native (UA curl), browser JSON (Chrome UA, Accept application/json, Sec-Fetch-Mode cors), browser HTML. Redirects not followed. Classify: API paths pass only on 401; page paths pass on 302 or 401 for native; any API 302 is fail; any other status is fail; network error is blocked. Exit 0 on all pass, 1 otherwise, 2 on blocked.
