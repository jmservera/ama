# Changes: issue 2118 live walkthrough (2026-11-23)

Tier: focused. No `src/` change; `rpi-checks.py --all` not run. Hosted CI for the exact head not observed. Refs #2118.

## Files

* Added `docs/reference/research/issue-2118-live-iot-map-walkthrough-2026-11-23.md`.
* Updated `docs/reference/README.md` (index) and `docs/reference/log.md`.
* Added evidence under `.copilot-tracking/evidence/2026-11-23/issue-2118-live/`.

## Validation

* `src/api` `tests.test_map_sensors`: 16 tests, OK.
* Live read-only probes (Azure CLI, Playwright) on revisions 0000054 and 0000026; no Azure resource created, nothing to delete.

## Per-criterion table

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Live Azure IoT Hub to SQL to UI map walkthrough recorded separately once live transport is active | Proven for the demo; per message SQL hop inferred (owner decides ticking) | Research note hop table; fresh map reading 79 s old |
| Per message SQL trace | Unproven | Log workspace private-link only; no trace taken |
| Resident live sensor view | Unproven | Test account consent `declined`; stored history only |
| Owner-gated items (DPO/Legal, person-run AT, billing) | Not needed for the demo per owner decision 2026-11-18 | n/a |
