# Changes, issue 2310

Documentation only; no source change (focused tier). Added `docs/reference/research/issue-2310-live-2026-11-25-r72.md`, index row and log entry. Validation: `tests.test_auth` 45 OK; live read-only probes.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Anonymous API GET with browser User-Agent and Accept json returns 401 | Code proven; live 0000072 unproven (302) | `docs/reference/research/issue-2310-live-2026-11-25-r72.md` |
| Anonymous page request still redirects to Entra | Proven (test and live) | same note |
| Existing auth tests pass; no weakening | Proven locally; hosted CI not observed | 45 tests OK, no source diff |

Open: live 302 is caused by Easy Auth `RedirectToLoginPage`; needs an owner-approved platform change.
