<!-- markdownlint-disable-file -->
# Details: #185 keyless Azure IoT Hub Registry backend

Plan: [plan](../plans/2026-11-10-iot-registry-azure-185-1110-plan.md). Research: [research](../research/2026-11-10-iot-registry-azure-185-1110-research.md).

## Module `zava_forward.core.synthetic.device_registry_azure`

Public names: `HUB_HOST`, `MARKER_PREFIX`, `NOT_RUN_OWNED`, `MAX_LIST`, `RegistryError`, `X509Enrollment`, `EnrollmentSpec`, `AzureIotHubRegistry`.

* `RegistryError(RuntimeError)`: `code` (fixed string), `readback` (`None`, `absent`, `owned`, `foreign`, `unreadable`). `str(error)` is the code only. Raised outside handlers with no cause or context.
* `X509Enrollment(device_id, primary_thumbprint, secondary_thumbprint=None)`: `SYN-` plus the `device_identity.SENSOR_ID` shape; thumbprints uppercase hex of 40 (SHA-1) or 64 (SHA-256) characters; secondary optional and different from primary.
* `EnrollmentSpec(run_id, enrollments)`: run ID matches `device_identity.RUN_ID`; 1 to `device_identity.MAX_DEVICES` enrolments; device IDs unique; all thumbprints unique across the spec. Violations raise `RegistryError("INVALID_ENROLLMENT")` at construction before any SDK use. `marker` property is `MARKER_PREFIX + run_id`.
* `AzureIotHubRegistry(hostname, spec, *, credential=None, client=None, timeout=30.0)`:
  * hostname matches `[a-z0-9][a-z0-9-]{1,48}[a-z0-9]\.azure-devices\.net` exactly (no scheme, port, path, uppercase), else `INVALID_HOSTNAME`.
  * exactly one of `credential` (trusted token credential with `get_token`) or `client` (trusted pre-built `IoTHubRegistryManager`); else `INVALID_CONFIGURATION`. `timeout` is a finite float in 1 to 60; else `INVALID_CONFIGURATION`.
  * Construction performs no import of the SDK, no token request, no network, no environment read.
  * First use builds, for a credential, `IoTHubRegistryManager.from_token_credential(hostname, credential)` (owned) and binds `protocol.config.retry_policy.retries = 0` and `protocol.config.connection.timeout = timeout` on either source before the first request. A missing SDK or `six` gives `SDK_MISSING`.
  * `close()` is idempotent; for an owned manager it calls `amqp_svc_client.disconnect_sync()` and `protocol.close()`; an injected client is never closed. Calls after `close()` raise `CLOSED`. Context manager closes.
* `create(device_id, run_id)`: requires `run_id == spec.run_id` and an enrolled ID (`NOT_ENROLLED`, before any SDK call). Sends SDK `Device(device_id, authentication=AuthenticationMechanism("selfSigned", X509Thumbprint(...)), capabilities=DeviceCapabilities(iot_edge=False), status="disabled", status_reason=marker)` via `protocol.devices.create_or_update_identity(id, device, custom_headers={"If-None-Match": "*"})`. Outcome by status: success 200 or 201 returns; 412 or 409 `IDENTITY_CONFLICT` (never adopt); 401 or 403 `ACCESS_DENIED`; other 4xx except 408 `REJECTED`; anything else (408, 5xx, timeout, connection error, non-HTTP exception, malformed) `WRITE_OUTCOME_UNKNOWN` with a safe readback attached and no retry and no adoption.
* `run_of(device_id)`: enrolled ID required. GET. 404 returns None. Success: exact `statusReason == marker-prefix + valid RUN_ID` returns that run ID; otherwise `NOT_RUN_OWNED` (`"(not-run-owned)"`, cannot equal a valid run ID). 401 or 403 `ACCESS_DENIED`; anything else, including a response whose device ID differs, `UNAVAILABLE`.
* `delete(device_id, run_id)`: run and ID checks. GET snapshot; 404 returns (no-op); unreadable raises; owner not exactly `run_id` returns (no-op, non-destructive); require a string ETag matching `[A-Za-z0-9+/=_.:-]{1,64}` and a non-empty `generation_id` else `OWNERSHIP_UNCERTAIN` (no delete). One `delete_identity(id, if_match=<quoted etag>)` (never `*`, never SDK default). 204, 200 or 404 return; 412 `PRECONDITION_FAILED` (snapshot stale; the identity is left untouched and not retried); 401 or 403 `ACCESS_DENIED`; other 4xx except 408 `REJECTED`; otherwise readback: absent returns, otherwise `DELETE_OUTCOME_UNKNOWN` with the readback.
* `list_run(run_id)`: run check. One `get_devices(top=1000)`. `len >= MAX_LIST (1000)` raises `LIST_INCOMPLETE`; a non-list body `UNAVAILABLE`; returns sorted IDs whose `statusReason` is exactly the run marker. Critique amendment: an enrolled ID listed without a string `statusReason` is confirmed by one bounded read (at most `MAX_DEVICES`); a failed confirmation raises `UNAVAILABLE`. 401 or 403 `ACCESS_DENIED`; else `UNAVAILABLE`.
* Readback (`_readback`) is one GET mapped to `absent`, `owned`, `foreign` or `unreadable`; it never raises and never writes.

* Critique amendments (single critique, 2026-11-10T02:38Z, [critique](../plans/critiques/2026-11-10-iot-registry-azure-185-1110-plan-critique.md)): lazy creation and close are guarded by a lock; the conflict code is `IDENTITY_CONFLICT`; the list confirmation read above; a test where the list payload omits `statusReason`; the import-effects subprocess receives `PYTHONPATH` from `sys.path`; README documents one-process-per-run (cross-process same-run contention is not fenced), the injected-client retry limit and the hidden non-enrolled device residual.

## Dependencies

`pyproject.toml`: `iothub = ["azure-iot-hub==2.7.0", "six==1.17.0"]`; `dev` adds the same two pins. The `six` pin is required because the SDK imports it without declaring it. No change to `requirements.in/txt`.

## Tests (`test_device_registry_azure.py`)

Fakes: a token credential class counting `get_token` calls and returning a sentinel `azure.core.credentials.AccessToken`; a `HubSimulator` patched over `requests.adapters.HTTPAdapter.send` that models the documented REST table (If-None-Match and If-Match behaviours, GET, list, DELETE statuses) with injectable faults (timeout before or after applying, forced status, hook between GET and DELETE) and records every prepared request. The real `IoTHubRegistryManager.from_token_credential` and SDK models run unmodified.

Cases (one per theme, subTests only for input tables): import with zero SDK or credential effects (subprocess); Core imports with the SDK blocked and fails with `SDK_MISSING` only at first use; invalid input table refusing with zero requests and zero token calls; no effect on construct or close; create wire payload and headers; create-only conflict leaves the existing identity unchanged; create 201 success; create 403 and 400 mapping; create timeout after write (unknown, readback owned, single PUT, no adoption) and before write (readback absent) and unreadable readback; `run_of` 404, owned, foreign run, unmarked SYN device, near-miss markers, and 401/403/500/timeout raising distinct codes; delete exact owned with quoted ETag header and no wildcard, 200 and 204 success; foreign and missing no DELETE; recreated and modified between GET and DELETE yield `PRECONDITION_FAILED` with the identity preserved; missing or wildcard ETag or missing generation refuses with no DELETE; delete timeout readback absent and owned; `list_run` complete, 999 ok, 1000 incomplete, request `top=1000`, 403 and timeout; sentinel secrets absent from error text, args, traceback and cause; owned manager closed once and injected client never closed; `device_identity.provision` then `teardown` through the real adapter; rollback after store failure.

## Validation commands (from `src/core`, no global install)

* Throwaway venv outside the repository with `pip install -e .[dev]` of this worktree's core only; the primary checkout's editable install is not touched.
* `python -m unittest test_device_registry_azure test_device_identity test_device_provision` with `PYTHONPATH=tests`; `python -m unittest discover -s tests -q` for the dependency rule and broader regression only if time-bounded.
* `mypy` (project configuration), `ruff check .`, `ruff format --check .`.
