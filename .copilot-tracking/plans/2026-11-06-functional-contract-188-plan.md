---
title: Plan for #188 functional findings F1 and F2
ms.date: 2026-11-06
---

* Step 1 RED: small reproduction script in new /tmp/188-functional-contract-r16-1106 (raw outputs preserved, unique names), with explicit i188 PYTHONPATH, bytecode off, module `__file__` identities printed: direct core `report(weather, weather)` KeyError; `weather_report` and `verify` accept a relabelled copy. If either does not reproduce, preserve that and stop without speculative edits.
* Step 2 F1: in `_index`, require the exact indoor `READING_FIELDS` key set (and keep the existing `_shape` and unit checks) so any non-indoor schema is ValueError INVALID_HANDOVER_OBSERVATION. No calibration invented; `weather_report` and consumer weather acceptance untouched.
* Step 3 F2: in `weather_report`, after the coverage check and before numeric comparison, compare `int(seed)` of each matched pair and raise ValueError for equal declared seeds (new reason HANDOVER_REFERENCE_NOT_DISTINCT). Different-seed cases and invalid-seed validation unchanged. Docstring states distinct seeds do not authenticate provenance.
* Step 4 tests in existing files: core report with weather rows raises INVALID_HANDOVER_OBSERVATION (api `test_sensor_consistency.py`), relabelled copy refused by `weather_report` and by `verify` with `replay_check=True` leaving retained envelopes unchanged, `-0` vs `0` equivalence refused; existing different-seed tests stay.
* Step 5 light checks only: new tests, the sensor consistency, live consumer, ingestion and analysis modules, Ruff, mypy for core and API, read-only existing venvs only with deliberate i188 import paths. No SQL, Docker, install, gate.
* Step 6 Changes, then author Review after checks, state, commit with gh-api-user identity and Copilot trailer, freeze ignored-clean.
* README contract wording updated only where it states seed difference.
