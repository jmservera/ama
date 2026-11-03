# Research: issue 810 Easy Auth intermittent 500s (2026-11-03)

Disposition: executed. Planning Readiness: Ready (documentation slice only).

## Prior delivery checked

* PR 764 (probes, cold-start retry), PR 786 (listen backlog), PR 796 (500 with logging), PR 780 (live evidence for #691) are merged. None addresses Easy Auth; `infra/modules/containerapps.bicep` already excludes `/healthz` and `/readyz`.

## Evidence

Full findings: [docs/reference/research/easy-auth-intermittent-500-2026-11-03.md](../../docs/reference/research/easy-auth-intermittent-500-2026-11-03.md).

* Read-only: auth config, scale, probes, replica, app console log; Log Analytics query denied by network perimeter; environment diagnostic setting lists no categories.
* Burst 4 x 30: `/healthz` and `/welcome.html` (excluded) 0 to 3 x 500 per round; `/workspace-shell.js` unauthenticated 120 x 401, no 500; no-auth `ca-resident-demo` 120 x 200.
* 500s have `content-length: 0`, `x-ms-middleware-request-id`, no app headers.

## Gates

* Slice does not touch security config, infrastructure files, SQL or deployment: focused tier. Azure changes need owner approval and were not made.
* Unmet: criteria 2 and 3; criterion 1 partly met.
