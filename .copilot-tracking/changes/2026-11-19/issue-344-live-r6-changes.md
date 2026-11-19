# Changes r6 (no source change)

Refs #344. Result: every remaining unticked criterion needs an infra change/redeploy or SQL-scope work (FULL tier), so no code was built. Tier: FOCUSED, documentation only; no src or infra file edited, no rpi-checks run. New: research note `docs/reference/research/public-browser-access-live-r6-2026-11-19.md` and evidence dir.

| # | Criterion | Demo status | Basis |
| --- | --- | --- | --- |
| 1 | Landing, Entra sign-in, anonymous API 401 not redirect | Unproven (browser clients) | Easy Auth RedirectToLoginPage; Bicep plus redeploy needed |
| 2 | Edge follows #143 | Already ticked | n/a |
| 3 | /healthz public; anonymous API 401 | Proven (non-browser clients) | Same caveat |
| 4 | SQL private, public Disabled | Proven earlier, not re-read | rerun note |
| 5 | Parity, gaps filed | Unproven | time/status 500 = SQL-path ProgrammingError; fix is SQL scope |
| 6 | Browser sign-in smoke | Already ticked; passed again | probe |

No Azure resource created; nothing to delete.
