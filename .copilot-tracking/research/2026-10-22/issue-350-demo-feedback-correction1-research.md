<!-- markdownlint-disable-file -->
# Research: Correction 1 for the demo feedback checker (Refs #350)

* Task ID: issue-350-demo-feedback-correction1
* Parent task: issue-350-demo-feedback-harness
* Research disposition: reused (independent review of head 62c0f38a, supplied externally, plus parent research and review artifacts)
* Planning Readiness: Ready

## Evidence

* Finding 1 (medium): tools/check-demo-feedback.py `check_case_write` returned `pass` for SQL write, restart and reload using self-supplied response snapshots and a self-declared restart marker; fixtures and ledger reports built by the harness cannot establish SQL backing or a real restart.
* Finding 2 (medium): the same function compared only the written-contact count, not the last written contact with the submitted request or the reloaded contact, so contradictory snapshots could pass.
* Runtime evidence (parent research C-series): `Store.log_call` stores the outcome stripped and truncated to 80 characters, appends a contact (channel, outcome, note, by, at) and the POST response returns the case detail; contact outcomes are projected as the held note for roles without a recorded need.
* Reviewer instruction: keep durability blocked or not-run absent independently verifiable evidence, label fixture checks response-shape consistency only, and add no provenance mechanism or live write authority.

## Decision

Durability can never be `pass` offline: a fully consistent bundle reports `blocked`; contradictions report `fail`. Scope stays the two tools files. Original #350 criteria stay unmet.
