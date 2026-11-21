---
title: Issue 2191 live check of simulator coverage and skip rate
description: Live readbacks on the synthetic demo showing the deployed image supports the skip rate, the store holds 443 homes and the live cohort is still 20, with the reason the 50 percent target is not met
author: AMA RPI agent
ms.date: 2026-11-21
ms.topic: reference
keywords:
  - issue 2191
  - simulator
  - live demo
estimated_reading_time: 4
---

Refs #2191, #184, #165. Synthetic desktop demo in resource group `ama`; owner decisions of 2026-11-18 apply. This note extends the [code and local test note](./issue-2191-demo-sim-coverage-2026-11-21.md). No credential was read or printed, and no source file changed.

## Live readbacks

* `job-live-simulator` (cron `*/5 * * * *`, image digest `sha256:79f2b7d7...`, the same digest as `ca-cutover-test-demo-api`) shows `Succeeded` for the five newest executions, 21:05 to 21:25 UTC. Its definition has 41 Container Apps secrets (20 devices at two files each, plus the control file), no `ZF_SIM_FAILURE_RATE` variable and the argument list `--sink iothub --once --max-per-second 10`.
* Throwaway job `job-2191-probe` (manual, same image, identity and SQL settings, `--sink stdout --once --failure-rate 0.3`, no hub traffic) ran and `Succeeded`. Its summary line read `slot=2026-11-21T21:30Z homes=443 sent=315 failed=0 skipped=128`. So the live store holds 443 homes, the deployed image already contains the seeded skip decision, and 128 of 443 (29%) skipped at a requested 0.3 without counting as failures. The probe was deleted; the job list now shows the original six jobs only.
* Cohort ceiling for the criterion: at least half of 443 homes is 222. The live cohort is 20 homes, 4.5%.

## Acceptance criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| Cohort covers at least 50% of homes | Unproven live (20 of 443, 4.5%) | The count above; code selection proven earlier by `select_cohort` tests |
| Configurable intermittent-failure rate | Proven in the deployed image; not enabled on the live job | Probe summary with 128 skipped and 0 failed; the live job has no `ZF_SIM_FAILURE_RATE` |
| Consent mix preserved | Proven locally; live mix is the earlier 10 granted and 10 declined over 20 homes | `plan` alternation test; [issue 184 note](./issue-184-live-demo-sim-consent-mix-2026-11-20.md) |
| Unit tests | Proven | Earlier note (229 and 5 tests); not rerun, no source change |

## Why coverage is not reached

Each added home needs its own hub X.509 identity and, in the current jobs, two Container Apps secrets. Going from 20 to 222 homes needs about 445 secrets, far above the 41 in use and above the per-app secret limit I could not confirm from the documentation I found. Azure Files is unusable (shared-key access disabled). A feasible route is to bundle many certificate pairs into a few secrets and unpack them into the job's private scratch at start, which is a simulator code change, an image push through the documented registry window, 202 hub device registrations needing a temporary registry role, and a new consent mix. I did not start it: it is a multi-hour, security-sensitive change that needs its own reviewed plan.

Enabling the skip rate on the live job also needs an environment update (`ZF_SIM_FAILURE_RATE`); I left the running demo unchanged so readings keep flowing.
