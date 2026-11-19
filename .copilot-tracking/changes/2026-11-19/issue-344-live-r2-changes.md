---
title: Issue 344 live r2 changes
ms.date: 2026-11-19
---

Refs #344. Tier: FOCUSED (documentation only; no src, infra, workflow or dependency change). Azure use was read-only, nothing created, nothing to delete. No credentials used.

Changes: docs/reference/research/public-browser-access-live-r5-2026-11-19.md (new), index entry in docs/reference/README.md, log entry in docs/reference/log.md, evidence under .copilot-tracking/evidence/2026-11-19/issue-344-live-r2/.

## Per-criterion table

| # | Criterion | Status | Basis |
| --- | --- | --- | --- |
| 1 | Public landing, Entra sign-in, anonymous API 401 not redirect | Unproven for browser clients | Fresh 302 for browser-style /api/me; fix is FULL tier (Easy Auth control, Bicep, redeploy) |
| 2 | Public edge follows #143 | Already ticked | Not re-run |
| 3 | /healthz public; anonymous API 401 | Proven for non-browser clients | curl 200/401 |
| 4 | SQL private, public access Disabled | Proven for the demo server | Disabled, 0 firewall rules, TLS 1.2 |
| 5 | Parity matrix, gaps filed | Unproven | Reachability only; /api/time/status 500 unfiled |
| 6 | Browser sign-in smoke | Already ticked | Not re-run |

Validation: relative-link check and git diff only; no tests apply. No checkbox changed.
