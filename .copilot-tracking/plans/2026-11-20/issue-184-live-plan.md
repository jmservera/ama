---
title: Issue 184 live demo simulator and consent mix plan
ms.date: 2026-11-20
---

Research: [issue-184-live-research.md](../../research/2026-11-20/issue-184-live-research.md). Details: [issue-184-live-details.md](../../details/2026-11-20/issue-184-live-details.md).
Tier: FULL for the Bicep change (infra); the coordinator runs gates, this run never runs `rpi-checks.py --all`.

## Phases

* [ ] Phase 1: Bicep. Add to `live-simulator-job.bicep` and `live-receiver-job.bicep` a `fileSource` parameter (`AzureFile` default, `Secret` alternative holding files as job secrets mounted read-only at `/certs`), and for the receiver an optional `cronExpression` and `maxEvents`. All scope, digest, approval and hardening guards stay. Compile, lint, run `infra/tests`.
* [ ] Phase 2: Operator tool `tools/demo_cohort.py`: selects a cohort, derives `SensorControl` rows (granted, declined, none) and applies them through `SensorConsumer.configure`, writes `control.json`, and plans device certificates. Focused unit test for the selection and consent split.
* [ ] Phase 3: Live. Generate X.509 certificates locally (private keys never printed, shredded afterwards), register enabled devices through a throwaway job with a temporary Registry Contributor role, apply policy and controls with a throwaway job (repository `configure`), deploy both jobs by `az deployment group create` with the digest of the running API image (no ACR change), start the receiver, and let the simulator cron run every five minutes.
* [ ] Phase 4: Verify: IoT Hub d2c metrics, newest `sensor_reading` age, a granted and a non-granted home in the Home sensors page (Playwright), cleanup readback (no throwaway job, temporary roles removed), `ZF_CONTAINER_HARDENING=off` on the app unchanged, ACR unchanged.
* [ ] Phase 5: Docs: infra README procedure, research note under `docs/reference/research/`, log entry, changes record with per-criterion table.

## Stop conditions

Stop and record a blocker if: the job needs an estate security change, SQL grants beyond existing ones, a Key Vault change, or an ACR push; if cost or message volume would exceed the demo cap; or if a documented guard refuses.
