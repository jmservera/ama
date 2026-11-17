# Plan: rubric prepare PR diff scope (Refs #198)

Date: 2026-11-14. Critique: one pass, no conflicting findings.

* [x] Phase 1: in `compute_state`, after `entries` is known, on `pull_request` with entries and not (bootstrap, force, instrument_changed), keep an artifact only when it left the registry or `classify_changes` returns non-empty present or removed.
* [x] Phase 2: append the `changed artifacts:` reason after filtering so it matches.
* [x] Phase 3: keep non-PR events on full fingerprint comparison.
* [x] Phase 4: add tests for lagging baseline: PR on other files not scored, PR on in-scope file opens `solution-code`, push still scores.
* [x] Phase 5: run focused validation.
