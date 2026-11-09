---
title: Plan for #184 slice 2, bounded cohort and finite run control
ms.date: 2026-11-08
---

* Goal: a bounded synthetic demo cohort (at most 100 homes), finite expiry and stop, a validated control document, and a bounded receiver host entry; no Azure write, send or model call.
* Phase 1: `api/live_control.py`, a pure validated control document (`enabled`, `expires_at`, `approval_reference`, `owner`, explicit `homes` 1..100), `decide()` returning send, stopped or expired, a window limit of 14 days, and a CLI `template`, `start`, `stop`, `status` that writes atomically.
* Phase 2: wire `live_simulator` so the IoT Hub sink requires the control file, sends only its cohort (intersected with existing homes), re-reads it every slot and stops at expiry or `enabled=false`; capacity is checked against the cohort.
* Phase 3: `api/live_receiver.py`, a bounded host entry that builds `Binding` for the same cohort and runs `HubReceiver` with finite seconds and events; unit tests use injected fakes.
* Phase 4: Bicep job gains the control path variable and a receiver-mode note; README and infra README carry the finite deployment plan, cost headroom and the retained interface freeze for the Quality UI and AI slice.
* Validation (focused): new and existing live simulator, credential hygiene and dependency-rule tests, ruff, mypy `--cache-dir=/tmp/mypy-184`, `az bicep build` and `lint`. No full suite, gate, SQL or browser run (no UI change).
* Critique (one, inline, before implementation): proceed. Risks accepted: an app-level admin control UI is out of this slice because it would touch the server and web surface; admin-only is enforced by Azure RBAC on the file share and job, stated plainly. No secret is read or stored.
* Authority: existing #184 comment 6652226413 (five-minute readings, USD700 cap, scoped identity roles); not re-asked.
