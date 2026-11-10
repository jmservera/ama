<!-- markdownlint-disable-file -->
# Plan: #185 keyless Azure IoT Hub Registry backend (initial source increment)

Written 2026-11-10 (readback `date -u` 02:37Z onward). Task `185-iot-registry-azure-initial`, branch `feat/demo-iot-registry-185-1110`, base `2bfd5e07545db18380f48a9854654c8393d0e9bc`. Research: [research](../research/2026-11-10-iot-registry-azure-185-1110-research.md). Details: [details](../details/2026-11-10-iot-registry-azure-185-1110-details.md). Local frozen candidate only: no push, PR, issue or board write. Correction balance UNKNOWN; no post-independent-review correction is authorised.

## Objective

Add a default-off, source-only, keyless Azure IoT Hub identity-registry adapter that satisfies the existing injected `device_identity.Registry` protocol, with real installed-SDK transport tests. It is not wired into the CLI, creates no credential, and makes no live call.

## Phases

* [x] Phase 0: Research (SDK and REST contract, repository facts, scope). Done 2026-11-10.
* [ ] Phase 1: Dependency declaration. `src/core/pyproject.toml`: new `iothub` extra (`azure-iot-hub==2.7.0`, `six==1.17.0`); `dev` extra gains the same two pins so Core CI and the local gate run the SDK tests. No other manifest.
* [ ] Phase 2: Adapter `device_registry_azure.py` per the details (spec, hostname, lazy SDK, create-only, ownership read, ETag-fenced delete, complete list, sanitised errors, owned-client close).
* [ ] Phase 3: Tests `test_device_registry_azure.py` using the real SDK and a documented-REST transport simulator at `requests.adapters.HTTPAdapter.send`, plus integration through `device_identity.provision/teardown`.
* [ ] Phase 4: README section in `src/core/README.md` (#185): purpose, inputs, limits, unobserved items, what stays open.
* [ ] Phase 5: Validation (targeted tests, existing DeviceIdentity/provision tests, Core mypy, ruff check and format) and changes record.
* [ ] Phase 6: One post-implementation review, state update, local commit (privacy-safe identity, Copilot trailer), handoff.

## Constraints carried from the brief

* Create-only with `If-None-Match: *`, exact marker ownership, exact non-wildcard ETag delete, complete-or-refuse list, 404 distinct from 401/403/unreadable/timeout, fixed sanitised codes, close only owned clients, no import-time or default effects, no ambient credential, no connection-string fallback, no enable path.
* No change to `device_identity.py`, `device_provision.py` or any file outside the owned set. If the contract needs more, stop and report.
* Heavy gates (full RPI gate, cloud, SQL, browser, scanners) are not run; tier: focused (source-only, default-off, component-local; not infrastructure, deployment, SQL or a live security control). The change adds dependency pins to `pyproject.toml`; its impact is a new optional extra plus a dev pin, no permission, secret, image, action or gate-semantics change, so the focused tier holds, recorded with that basis. Hosted CI for the exact head is not observed locally and is not claimed.

## Acceptance

* The adapter passes the Registry contract through `device_identity.provision` and `teardown` against the SDK transport simulator.
* Wire-level assertions: exact URL host, token header, create body and `If-None-Match: *`, delete `If-Match` exact quoted ETag, bounded timeout and zero transport retries.
* Races and uncertainty: same-ID conflict, recreated or modified identity at delete, timeout after write, readback outcomes, list saturation.
* Core without Azure extras still imports; no `azure`, `uamqp` or `six` import at import time.
* Unchanged CLI refusal and dry-run (existing `test_device_provision` passes).
* Core mypy, ruff check and ruff format clean. No out-of-scope file in the diff.
