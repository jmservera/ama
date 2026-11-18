# Issue 344 live changes (2026-11-18)

Refs #344. Tier: FOCUSED (documentation and evidence only; no src change; rpi-checks.py --all not run).

Files:
* docs/reference/research/public-browser-access-live-demo-2026-11-18.md (new)
* docs/reference/README.md (index row), docs/reference/log.md (entry)
* .copilot-tracking/evidence/2026-11-18/issue-344-live/ (curl, Azure read-only JSON, Playwright script, JSON, 3 screenshots)

Azure: read-only only; no resource created, nothing to delete. Credentials read at runtime; literal scan of evidence found no match.

## Per-criterion status

| # | Criterion (short) | Proven for the demo? | Basis or reason |
| --- | --- | --- | --- |
| 1 | Public landing, sign-in to Entra, protected pages need auth, anonymous API 401 not redirect | Partly | Landing 200, sign-in click reaches Entra, sign-in lands on /app, /app and APIs 401 by curl. Browser-originated anonymous API calls are redirected (#350) |
| 2 | Public edge per #143 recorded | Already ticked | External Container Apps environment on the demo |
| 3 | /healthz public; protected API 401 anonymous | Proven for non-browser clients | /healthz 200; /api/me and /api/cases 401 by curl; browser redirect caveat |
| 4 | SQL private, public access Disabled | Proven for demo server | PNA Disabled, 0 firewall rules, private endpoint approved; policy assignments not inspected |
| 5 | Parity with matrix, gaps filed | Partly | Assets and 22 of 25 read routes 200 (reachability only). New gap: /api/time/status 500 (not yet filed); /api/law, /api/account/photo 503 known. Write flows, AI, documents, chat not exercised (#350) |
| 6 | Browser sign-in smoke recorded | Already ticked; refreshed | Passed with the test account, plus #349 |

Unmet: browser 401 behaviour, full functional parity, time-status 500 cause, policy-assignment inspection.
Validation: link and diff review; credential literal scan; no unit tests apply (no code change).
