# Details: issue 124 slice 1

## Phase 1

* File: `src/core/src/zava_forward/core/discovery_register.py`. Frozen dataclasses, no I/O, no model, no store.
* `DiscoveryOwner.status()`: NOT_NOMINATED, ENDPOINT_NOT_AGREED, ENDPOINT_AGREED.
* `dictionary_gaps()` over ten required events; `validate_event()` only by the owning role.
* `Constraint`, `add_evidence`, `evidence_gaps`, `decide`, `register_rows`, `CANDIDATE_CONSTRAINTS` from the brief.

## Phase 2

* File: `src/core/tests/test_discovery_register.py` (12 tests).
* Commands from `src/core`: `PYTHONPATH=src:tests python3 -m unittest tests.test_discovery_register -q`; `ruff check --no-cache`; `mypy --cache-dir=/tmp/mypy-124`.

## Phase 3

* `src/core/README.md` section; `docs/reference/log.md` entry.
