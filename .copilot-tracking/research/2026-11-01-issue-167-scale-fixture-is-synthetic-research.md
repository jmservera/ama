# Research: issue 167, per-record is_synthetic on the scale fixture

* Task: issue-167-scale-fixture-is-synthetic; mode: automatic; disposition: executed
* Date: 2026-11-01

## Findings

* Criterion 1 (routed child stories) is already ticked: needs-inventory v1.2.0, PRs 243/312.
* Criterion 2 is the open one. The issue comment and `docs/reference/research/retrofit-synthetic-data/README.md` (coverage baseline section) state the scale fixture's homes and events carry only a manifest-level label, not per-record `is_synthetic=true`.
* Code check, `src/core/src/zava_forward/core/synthetic/scale_fixture.py`: `households()` already sets `is_synthetic=True`; `homes()` and `events()` do not. Manifest carries `source_type="SYNTHETIC"`.
* Consumers of `homes()`: `sensor_backfill.sensor_for`, agents/api tests. They read named keys, so an additive key is compatible (to be proven by tests).
* Pinned goldens in `src/core/tests/test_synthetic_determinism.py::test_versioned_payload_goldens` hash homes.jsonl and events.jsonl; they must be re-pinned with a `VERSION` bump (1.2.0 to 1.3.0) since output bytes change.
* Private stock register (SN-01) is out of scope and untouched; no second generator.

## Planning readiness

Ready. Smallest slice: add `is_synthetic=True` to homes and events, bump version, re-pin goldens, add a test asserting every record in all three files carries it, update README statements.

## Remaining human decision

Owner confirmation of the mapping and any deferral stays with the owner; the issue cannot claim full closure.
