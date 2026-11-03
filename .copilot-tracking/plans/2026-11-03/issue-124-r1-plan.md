# Plan: issue 124 slice 1 discovery register rules (r1)

Stack: slice 1 (this PR) pure rule layer in `src/core`. Slice 2 (later): persistence and a read-only employee screen following Fluent 2, WCAG and plain-language standards, once the sponsor nominates an owner. Slice 3 (later): import of approved extracts and time attribution, needing the data owner and DPO decisions.

## Phases

* [x] Phase 1: add `discovery_register.py` (owner status, ten-event dictionary gaps, constraint register with decision rights)
* [x] Phase 2: unit tests, ruff, mypy
* [x] Phase 3: README section, log entry, RPI evidence

Details: `.copilot-tracking/details/2026-11-03/issue-124-r1-details.md`

## Critique (executed once, inline)

Verdict: proceed. Applied directly: events stay separate (invoice not merged into completion); the proposer cannot decide their own constraint; acceptance blocked without both evidence sides; decided constraints are closed to new evidence. Rejected: ranking constraints by score, because the brief forbids inferred causes; order is the proposed test order only. No user decision needed.
