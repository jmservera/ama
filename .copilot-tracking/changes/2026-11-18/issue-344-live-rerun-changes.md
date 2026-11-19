# Issue 344 live rerun changes (2026-11-18)

Refs #344. Tier FOCUSED (documentation and evidence only; no `src` change; `rpi-checks.py --all` not run).

Files:
* docs/reference/research/public-browser-access-live-rerun-2026-11-18.md (new)
* docs/reference/README.md (index row), docs/reference/log.md (entry)
* .copilot-tracking/evidence/2026-11-18/issue-344-live-rerun/ (curl, Azure read-only JSON, Playwright script, JSON, 3 screenshots)
* rerun research, plan, details, critique, changes, review records and the state file

Azure: read-only; no resource created, nothing to delete. Credentials read at runtime; literal scan of the evidence found no match.

## Per-criterion status

| # | Criterion (short) | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Public landing, sign-in starts Entra, protected pages need auth, anonymous API 401 not redirect | Partly proven | Landing 200, sign-in reaches Entra, test sign-in lands on /app, anonymous curl 401 on /app and APIs. Browser-style API requests get 302 (Easy Auth), so the "not a redirect" part is unproven |
| 2 | Public edge per #143 recorded | Already ticked | External Container Apps environment on the demo |
| 3 | /healthz public; anonymous API 401 | Proven for non-browser clients | /healthz 200; /api/me and /api/cases 401; same browser 302 caveat |
| 4 | SQL private, public access Disabled, no policy bypass | Proven for the demo server | PNA Disabled, 0 firewall rules, private endpoint Approved, 0 policy exemptions at subscription and resource group. SQL audit policies are audit-only and NonCompliant (not a bypass) |
| 5 | Parity with matrix, gaps filed | Partly proven | 11/11 assets and 22/25 read routes 200 (reachability only). 503 on /api/law and /api/account/photo known; /api/time/status 500 reproduced. Write flows, AI, documents not exercised here (#350, #360) |
| 6 | Browser sign-in smoke recorded | Already ticked; refreshed | Passed again with the test account |

Unmet: browser 401 behaviour, full functional parity, /api/time/status 500 cause.
Validation: link and diff review; credential literal scan; no unit tests apply.
