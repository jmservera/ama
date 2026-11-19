# Changes, issue 344 live (20261119T152819Z)

Refs #344. Files: docs/reference/research/public-browser-access-live-r5-2026-11-19.md (new), docs/reference/README.md (index), docs/reference/log.md (entry), tracking artifacts. No src change; FOCUSED tier. Validation: link and diff review; no tests applicable. The state file for this slug was overwritten from an earlier tracked version.

| # | Criterion | Status |
| --- | --- | --- |
| 1 | Landing, Entra, anonymous API 401 not redirect | Unproven for browser clients (infra change) |
| 2 | Public edge | Ticked already |
| 3 | /healthz public, API 401 | Proven non-browser clients only |
| 4 | SQL private | Proven earlier, not re-run |
| 5 | Parity | Unproven; time/status 500 cause unknown (SQL scope) |
| 6 | Sign-in smoke | Ticked already |

Witness note: plan-done, implement-start and implement-done were first refused (state lacked artifact paths) and re-recorded after the state was fixed, so implement-start follows the content commit.
