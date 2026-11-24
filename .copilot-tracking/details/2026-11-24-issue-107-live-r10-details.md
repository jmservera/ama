# Issue 107 live r10 details (2026-11-24)

* Worker: add `kind == "data"` appending "x" to `REGISTRY[cap]["categories"]`; `provenance` sets `assistants.PROVENANCE`; `model` sets module `MODEL` used for `provider.model_version`.
* Tests: `test_changed_data_process_revokes_and_fresh_process_stays_denied`, `test_changed_provenance_process_revokes_and_fresh_process_stays_denied`, `test_changed_model_process_revokes_and_fresh_process_stays_denied`.
