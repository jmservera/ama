<!-- markdownlint-disable-file -->
# Plan: Issue #165 coverage status and synthetic/PII guard closure

Research: [.copilot-tracking/research/2026-11-13/165-synth-coverage-pii-2244-research.md](../../research/2026-11-13/165-synth-coverage-pii-2244-research.md)
Details: [.copilot-tracking/details/2026-11-13/165-synth-coverage-pii-2244-details.md](../../details/2026-11-13/165-synth-coverage-pii-2244-details.md)

## Phases

* [x] Phase 1: Validate coverage status with rationale and evidence (G1)
* [x] Phase 2: Emission guards for stream frames and provisioning report (G2, G3)
* [x] Phase 3: Generator-output audit test and focused validation

## Success criteria

* Every inventoried need is checked for status in covered, partial or missing, non-empty note, dataset ids and closure note.
* Stream frames and the provisioning report are labelled synthetic and refuse personal-data patterns.
* `test_scenario_manifest.py` and `test_needs_inventory.py` stay green; ruff and mypy clean.
* Single critique: self-critique recorded in the changes file (no conflicting decisions).
