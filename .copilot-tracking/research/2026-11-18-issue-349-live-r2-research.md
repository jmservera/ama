# Research: issue 349 tenant prerequisites, live demo (2026-11-18)

* Task: issue-349-live. Research disposition: executed (opening; findings appended below).
* Prior note reused as baseline: docs/reference/research/entra-signin-live-demo-2026-11-18.md
* Gaps to close: retained 401/forged-header curl evidence, readable auth/KV/secret/roster facts, Entra-side wrong-account denial, positive API request in browser mode.
* Planning Readiness: pending

## Completion

* Findings: docs/reference/research/issue-349-tenant-prerequisites-live-2026-11-18.md; evidence under evidence/2026-11-18/issue-349-live2/.
* Disposition: executed (read-only Azure, Playwright). Planning Readiness: Ready.
* Adverse evidence kept: Graph reads refused (insufficient privileges); direct vault list refused (private link only); Accept: application/json gives 302 not 401.
