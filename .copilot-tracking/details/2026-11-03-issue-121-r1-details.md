# Phase details: issue 121 r1

## Phase 1

* Eight `DataClass` entries; approval gates read from `DP_<CLASS>_<GATE>_REF`; `SYNTH-` never counts; values never echoed.
* `model_dispatch`: constructed allowed; actual denied without every required gate including TRANSFER; raw documents also need a `reviewed_redacted` derivative; every denial carries a manual path.
* `validate_task_payload`: field name, type, length for rule_lookup, check_explain, alert_triage; unknown task denied.
* `due_date` and `rights_status`: one calendar month, month-end clamp, timezone required; extensions not computed.

## Phase 2

* 12 unit tests covering defaults, synthetic refs, TRANSFER gap, derivative, payload limits, clamping and states.

## Phase 3

* README section "Data protection register and dispatch gate (#121)"; log entry.

## Phase 4

* `PYTHONPATH=src python3 -m unittest tests.test_data_protection tests.test_regulatory_privacy`, `ruff check`, `ruff format --check`, `mypy --cache-dir=/tmp/mypy-121`.
