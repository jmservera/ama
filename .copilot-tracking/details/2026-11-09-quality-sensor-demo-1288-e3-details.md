---
title: Details - issue 1288 E3
---

# Phase details: issue 1288 E3

Plan: [plan](../plans/2026-11-09-quality-sensor-demo-1288-e3-plan.md).

## P3 freeze decision (design, not activation)

Options considered against the brief's invariants:

| Option | Outcome |
| --- | --- |
| Env flag or boolean opens the real route | Rejected: caller or operator label, not provenance |
| Trust `SYN-` device or `LIVE-` reading IDs, or `source_type` SYNTHETIC | Rejected: naming and row contract, writable by the same receiver that serves real stores |
| Trust values matching a fixture | Rejected: coincidence |
| Trust dataset path or `ZF_DATA` | Rejected: arbitrary path |
| Payload allowlist at `Ai` | Rejected as sole control: `Ai` sees a string; quality checklist evidence is free text; case facts come from the working store |
| Dedicated simulation store plus bundled public fixture case plus token over exact payload bytes verified at `Ai` | Sound, but a new provenance architecture across store, composer and egress; not surgical |
| Lease-enforcing egress proxy | Sound, infrastructure and owner decision |

Decision: freeze. Owner decision needed: choose (a) the proxy or (b) the dedicated simulation store and token architecture, then a separate finite admission for one live call. The exact future step is in research.

## P4 test

Add `Boundary.test_no_spoofed_simulation_claim_releases_captured_readings_to_a_real_ai` to `src/api/tests/test_quality_sensors_e2.py`:

* Seed a persisted live reading (`SYN-` device, `LIVE-` ID), a ready quality record and the real TLS peer through `tls_ai()`.
* Patch the environment with the demo profile, the chat demo switch, an arbitrary `ZF_DATA` path and a made-up simulation variable.
* Assert the built request does carry the persisted `LIVE-` reading, the dispatch still holds with the manual route reason, and peer accepts and bytes, meter reserved and checked, and token counts are all zero.

Mocked transport shows payload wiring only. Exact same-ID and value correlation through the non-transmitting mock is already covered by the E1 suite and the browser check (`quality_sensors_browser_check.py`) and is re-run.

## P5 commands (all from `src/api` or `src/core`, pinned `.venv-1288`)

* `PYTHONPATH=../core/tests:../agents/tests:tests python -m unittest test_quality_sensors test_assistants test_quality_sensors_e1 test_quality_sensors_c7 test_quality_sensors_e2`
* Core: `test_sensor_consumer test_sensor_consumer_live test_sensor_analysis_store test_live_readings`
* SQL: owned SQL Server 2022 container on localhost under `flock -n /tmp/ama-rpi-heavy.lock`, `ZF_TEST_MSSQL=1`, removed afterwards.
* Browser: `PYTHONPATH=tests:../core/tests:../agents/tests python -m checks.quality_sensors_browser_check --axe <pinned axe>`.
* `ruff check`, `ruff format --check`, `mypy` normalized comparison against `c772364`.
