---
title: Details for issue 110 live2 plan
ms.date: 2026-11-18
---

* P1 to P3 use `az containerapp job create --trigger-type Manual --replica-timeout 300` in `cae-cutover-test-demo` with the identity `id-cutover-test-api`, env `ZF_SIM_HUB_HOSTNAME`, `ZF_DEMO_EH_NAMESPACE`, `ZF_DEMO_EH_NAME=sensor-readings`, `ZF_DEMO_HOMES`, `ZF_DEMO_SLOTS=2`, `ZF_DEMO_CLEANUP=1`, `ZF_SIM_SEED=110`, plus the SQL variables copied from `ca-cutover-test-demo-api`.
* Output goes to `az containerapp job logs show`, saved under the evidence directory, ids redacted before any quote in the note.
* Cleanup: delete job, delete the two role assignments created here, confirm `az iot hub device-identity` count via `az iot hub show-stats`.
