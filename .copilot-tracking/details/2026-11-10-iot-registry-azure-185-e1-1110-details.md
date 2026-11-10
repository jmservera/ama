<!-- markdownlint-disable-file -->
# Details: #185 Registry adapter extension E1

Plan: [plan](../plans/2026-11-10-iot-registry-azure-185-e1-1110-plan.md). Research: [research](../research/2026-11-10-iot-registry-azure-185-e1-1110-research.md).

## Source design

`list_run(run_id)` after `_run(run_id)` and the capped `get_devices(top=MAX_LIST)` call (unchanged saturation refusal):

* Entry with `statusReason == marker`: found.
* Entry with a string `statusReason` not equal to the marker: skipped (a readable different or foreign owner).
* Entry with a non-string `statusReason`: one `_read(device_id)` regardless of enrolment, charged to a per-call budget of `device_identity.MAX_DEVICES`.
  * `present`: owner via `_owner(...)`; equal to `run_id` means found.
  * `absent`: skipped.
  * denied or unreadable: refuse `ACCESS_DENIED` or `UNAVAILABLE`.
  * more than the budget: refuse `LIST_INCOMPLETE` before the 101st read.
* Non-string `device_id`: refuse `UNAVAILABLE` (unchanged).
* The result is sorted and may include a non-enrolled marked ID. `create`, `run_of` and `delete` still refuse non-enrolled IDs, so nothing destructive widens; `device_identity` teardown refuses an uncovered ID before deleting.

`RegistryError.__init__` sets `self.__suppress_context__ = True` (one comment: a raise inside a caller's handler would otherwise print the caller's exception context). `__cause__` remains None.

## Tests (`test_device_registry_azure.py`)

* `ListTests`: replace the omission test with one expecting `["SYN-A1", "SYN-B1"]` (B1 non-enrolled, exact marker) and unmarked/other-run exclusion; budget exactly 100 passes, 101 refuses `LIST_INCOMPLETE` after exactly 100 confirmation reads; an unreadable confirmation of a non-enrolled entry refuses.
* `ExistingProtocolIntegrationTests`: whole-run teardown over a hub with a hidden marked non-enrolled identity raises `TEARDOWN_MANIFEST_INCOMPLETE:1`, sends no DELETE and leaves both enrolled and hidden devices.
* `SanitisedErrorTests`: every public refusal path (create, run_of, delete, list_run, invalid configuration, invalid enrolment, not enrolled, SDK failures) invoked inside a caller `except RuntimeError(CALLER-SENTINEL)`; formatted traceback and repr contain no sentinel; `__suppress_context__` is true and `__cause__` is None.

## Validation commands (isolated venv outside the repository)

* `python -m unittest` selectors: `test_device_registry_azure test_device_identity test_device_provision test_dependency_rule` from `src/core` with `PYTHONPATH=tests`; impacted Core/API selectors named in the changes record.
* `ruff check .`, `ruff format --check .`, `mypy` from `src/core`.
* Root repro `reproduce_functional_findings.py` red on the frozen head, green after.
