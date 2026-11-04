---
title: Research for #184 live simulator container (slice 1)
ms.date: 2026-11-04
---

* Research disposition: executed (inline). Planning Readiness: Ready.
* Prior delivery checked (merged PRs, `gh pr list --state merged`): #508/#557/#637/#647/#698/#704 (replay, identity, controls, leak tests), #849 (device identity rotation, #185), #852 (child status), #910 (offline fleet identity, #110), #889 (#188 run sheet), #845 (run plan vs B1 and budget, #189). No merged PR sends a periodic per-home stream or provides a container for one.
* Reusable code: `core/synthetic/sensor_identity` (home to sensor key), `device_identity` (SYN- device ids, X.509 per device, 100 device cap), `run_plan` (B1 400,000 per day, 40,000 headroom, USD10 per month), `api/iot_stream.DeviceActivation` (approval and `ama` scope), `factory.open_store` and `SqlStore.query_case_ids` (home enumeration), Container Apps job pattern with `*/5 * * * *` in `infra/modules/containerapps.bicep`, standalone template pattern `infra/resident-demo.bicep`.
* Gaps: no smooth hourly-anchor generator, no all-homes runner, no simulator Dockerfile or job template. Existing consumer schema (`sensor-fault-input-v1`) has no sunlight field.
* Facts for sizing: 288 messages per home per day; B1 budget after headroom allows 1,250 homes. Free tier (8,000 per day) allows 27 homes.
* Decision: add a new project only if needed; instead keep the pure generator in `core` and the runner in `api` (which already holds `azure-iot-device`, `iot_stream` and hashed requirements), so no CI project registry change is needed.
* Unknowns not resolvable offline: real IoT Hub throttle figures, live prices, device registration, certificate delivery, SQL grant.
