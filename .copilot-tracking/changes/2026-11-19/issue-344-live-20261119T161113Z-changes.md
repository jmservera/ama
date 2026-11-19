# Changes, issue 344 seventh pass

Docs only; no `src` change; tier FOCUSED. No Azure resource created.

Files: docs/reference/research/public-browser-access-live-r7-2026-11-19.md (new), docs/reference/README.md (index row), docs/reference/log.md (entry), these tracking artifacts and the state file.

| # | Criterion | Status |
| --- | --- | --- |
| 1 | Landing, Entra sign-in, anonymous API 401 not redirect | Unproven for browsers (needs Return401 infra change, owner decision, FULL tier); proven for curl |
| 2 | Edge follows #143 | Already ticked |
| 3 | /healthz public; anonymous API 401 | Proven live (200; 401) |
| 4 | SQL private, public Disabled, no bypass | Proven live (Disabled, 0 firewall rules, private endpoint, 0 policy assignments) |
| 5 | MVP parity, gaps filed | Unproven (time/status SQL-path 500; FULL tier) |
| 6 | Browser sign-in smoke | Already ticked |

Validation: documentation link and diff review only; no tests apply.
