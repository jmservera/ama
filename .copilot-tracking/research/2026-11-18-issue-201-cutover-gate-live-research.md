# Issue 201 live audit research (2026-11-18)

Refs #201. Disposition: executed (refresh of docs/reference/research/cutover-gate-live-2026-11-18.md).
Unticked criteria: (1) repointed + src build deployed healthy, (2) private mvp/data relocated and backed up, (3) owner sign-off.
Planning Readiness: Ready once findings are recorded below.

## Findings
* Repo: 0 tracked mvp/prototype files; workflows and Dockerfile build from src; infra pipeline tests pass.
* Live: revision 0000032 Healthy, /healthz 200 (curl and Playwright), digest unchanged.
* New: az containerapp exec listing shows zava-forward-{agents,api,core} 0.1.0 and no /app/mvp.
* Unprovable: build-run record (ACR public access disabled, 10 ACR task runs Failed, log workspace perimeter-blocked, no src-deploy runs); mvp/data and sign-off are owner-only.
* Adverse: legacy-reference checker 45 violations (was 11).
* Planning Readiness: Ready. Full table: docs/reference/research/cutover-gate-live-r2-2026-11-18.md
