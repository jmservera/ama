---
title: Issue 2191 live pass 3 details
ms.date: 2026-11-21
---

* Phase 1: job `job-2191-homes` (manual, simulator image digest, identity `id-cutover-test-internal`, simulator SQL env) running `python -c` that prints `store_home_ids`; delete afterwards.
* Phase 2: `openssl ecparam` self-signed certificates with CN equal to the device id, thumbprint registered with `az iot hub device-identity create --am x509_thumbprint`.
* Phase 3: `az deployment group create` with `infra/live-simulator-job.bicep` and a secure parameter file; consent mix via `tools/demo_consent_mix.py` logic in a job using the receiver identity.
* Phase 4: evidence gathered without secrets; screenshots under `docs/reference/research/`.
* Stop conditions: any step needing a credential printout, an estate change outside the simulator job and hub device registry, or a cost above the cap.
