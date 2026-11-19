# Changes r5 (no source change)

Refs #344. One-line result: every remaining unticked criterion is production-only (infra change and redeploy) or lacks a diagnosable cause, so no code was built. Tier: FOCUSED, documentation-only; no src or infra file edited. Validation: git diff review only.

| # | Criterion | Demo status | Basis |
| --- | --- | --- | --- |
| 1 | Public landing, Entra sign-in, anonymous API 401 not redirect | Unproven for browser clients | Easy Auth `RedirectToLoginPage`; fix is Bicep line 302 plus redeploy (FULL tier) |
| 2 | Edge follows #143 | Already ticked | External Container Apps environment |
| 3 | /healthz public; anonymous API 401 | Proven for non-browser clients | Same redirect caveat |
| 4 | SQL private, public Disabled | Proven (earlier passes, r4 re-read) | Disabled, 0 firewall rules |
| 5 | Parity, gaps filed | Unproven | Reachability only; `/api/time/status` 500 cause unknown, logs show no exception |
| 6 | Browser sign-in smoke | Already ticked | Earlier passes |

No Azure resource created; nothing to delete. No checkbox changed.
