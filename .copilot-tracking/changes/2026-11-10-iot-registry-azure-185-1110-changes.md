# Changes: keyless IoT Hub Registry adapter (#185, initial increment)

Recorded 2026-11-10T02:42Z. Base `2bfd5e07545db18380f48a9854654c8393d0e9bc`.

## Files

* `src/core/src/zava_forward/core/synthetic/device_registry_azure.py` (new): `AzureIotHubRegistry`, `EnrollmentSpec`, `X509Enrollment`, `RegistryError`. Lazy optional SDK, injected credential or client, create-only (`If-None-Match: *`), exact-marker ownership, exact-ETag delete, complete-or-refuse list, fixed sanitised codes.
* `src/core/tests/test_device_registry_azure.py` (new): 35 tests on the real installed `azure-iot-hub` 2.7.0 request path with a fake token and a `requests` adapter simulator of the documented REST conditional-header table.
* `src/core/pyproject.toml`: `iothub` extra and `dev` extra gain `azure-iot-hub==2.7.0` and `six==1.17.0` so Core CI runs the SDK tests rather than skipping.
* `src/core/README.md`: subsection under the #185 section.

## Plan deviations

* The `_enrolled` helper was split into `_run` and `_device` to avoid a type-ignore. No behavioural change from the plan.

## Validation (focused tier)

Tier basis: optional extra and dev pin only; no permission, secret, image, action, deployment or gate-semantics change. Not the full gate.

Ran in a throwaway venv outside the repo with `pip install -e "src/core[dev]"`:

* `test_device_registry_azure`: 35 passed.
* `test_device_identity test_device_provision test_dependency_rule`: 50 passed.
* `ruff check .`, `ruff format --check .`, `mypy` (286 files): clean.

Not run: full RPI gate, cloud, SQL, browser, scanners, hosted CI (unobserved; not claimed).

## Unobserved

Real Azure behaviour (412 on create, 201 versus 200, delete status, ETag format, list payload and 1000 cap, `statusReason` round trip, RBAC). Whole #185 credential issuance, storage, rotation and teardown remain open. Correction balance is UNKNOWN; no correction cycle is authorised.
