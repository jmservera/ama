# Plan 2026-11-23, issue 116 live r11

Tier: FULL (src change in a provider-boundary security control).

* [ ] Phase 1: add a failing test for surrogate text (system, string user, list part) in `src/core/tests/test_ai_input_bounds.py`.
* [ ] Phase 2: make `approved_payload` refuse unencodable text as `input-type-not-approved`.
* [ ] Phase 3: run core and api targeted tests, ruff, mypy; write the evidence note, index and log entries.
