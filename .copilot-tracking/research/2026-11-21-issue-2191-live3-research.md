---
title: Issue 2191 live pass 3 research
ms.date: 2026-11-21
---

Disposition: executed. Planning Readiness: Ready.

* The previous pass left one criterion unproven, a live cohort of at least half of all homes (20 of 443), blaming the Container Apps secret limit. That reason is refuted: throwaway jobs `job-2191-secrets-120` and `job-2191-secrets-450` were created with 120 and 450 secrets and read back as 120 and 450; both were deleted. 224 homes need 449 secrets (two files per device plus `control.json`), so the existing secret-volume design works with no source change.
* `MAX_COHORT` is 500 in `live_control.py` and `tools/demo_consent_mix.py` (merged in #2198), so `select`, `plan` and `control` already support the cohort. The job template `infra/live-simulator-job.bicep` takes `secretFiles` and `secretFileNames` without a count limit.
* SQL public access is Disabled, so the home list and the consent mix (`SensorConsumer.configure`) must run in throwaway jobs inside the environment, as in the issue 184 note. Hub registration uses the data plane (`az iot hub device-identity`).
* Capacity: 224 homes x 288 slots = 64,512 messages a day, inside the B1 budget; 224 sends at 10 a second take about 22 s inside the 240 s replica timeout.
* Source of evidence: [live coverage note](../../docs/reference/research/issue-2191-live-coverage-2026-11-21.md), [issue 184 note](../../docs/reference/research/issue-184-live-demo-sim-consent-mix-2026-11-20.md), `infra/README.md` simulator section.
