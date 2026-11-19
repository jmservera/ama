# Changes, issue 344 live

Tier: FOCUSED, documentation-only. No src, infra or workflow file changed. Basis: the only fix for criterion 1 is infrastructure/security (Easy Auth action), which needs FULL tier; stopped per brief.

Changed: docs/reference/research/public-browser-access-live-r4-2026-11-19.md (new), docs/reference/README.md (index row), docs/reference/log.md (entry), plus dated .copilot-tracking artifacts and evidence.

Validation: Markdown link review and git diff; no code tests apply. Hosted CI not read (no push).

| # | Criterion | Status | Basis |
| --- | --- | --- | --- |
| 1 | Landing, Entra sign-in, anon API 401 not redirect | Unproven for browsers | 302 for browser-style API calls; fix is infra, FULL tier |
| 2 | Edge follows #143 | Already ticked | External environment |
| 3 | /healthz public; anon API 401 | Proven for non-browser clients | anon-curl.txt |
| 4 | SQL private, no bypass | Proven for demo server | sql.json, 0 firewall rules; exemptions from pass 2 |
| 5 | Parity matrix | Unproven | Reachability only; /api/time/status 500 unfiled |
| 6 | Browser sign-in smoke | Already ticked | Earlier passes |
