---
title: Issue 2191 live pass changes
ms.date: 2026-11-21
---

Refs #2191. No source change; focused tier. Added the [live coverage note](../../docs/reference/research/issue-2191-live-coverage-2026-11-21.md), a README row and a log entry. Live Azure: read-only job readbacks plus one dry-run job (`job-2191-probe`) that was deleted; no estate change remains.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Cohort covers at least 50% of homes | Unproven live | 20 of 443 homes (4.5%); target 222. Per-device secrets (two per device) do not scale to about 445; a bundled-certificate change is needed |
| Configurable intermittent-failure rate | Proven in the deployed image | Dry-run probe: homes=443 sent=315 failed=0 skipped=128 at 0.3. Not enabled on the live job |
| Consent mix preserved | Proven locally; live mix 10 granted, 10 declined over the 20 cohort | `plan` test; issue 184 note |
| Unit tests | Proven earlier (229 and 5 tests); not rerun, no source change | issue 2191 first note |
