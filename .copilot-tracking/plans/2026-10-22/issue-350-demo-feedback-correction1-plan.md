<!-- markdownlint-disable-file -->
# RPI Plan: Correction 1 (Refs #350)

* Task ID: issue-350-demo-feedback-correction1
* Planning status: ready
* Research: .copilot-tracking/research/2026-10-22/issue-350-demo-feedback-correction1-research.md
* Phase details: .copilot-tracking/details/2026-10-22/issue-350-demo-feedback-correction1-phase-details.md
* Plan critique: not executed before implementation (see review RV-C01)

## Requirements

* `case_write_reload` never returns `pass`; a response-shape-consistent bundle returns `blocked` stating SQL backing, restart and persistence are unverifiable offline.
* Compare the write response last contact with the submitted outcome (stored form) and channel, and with the reloaded last contact on every field; mismatch is `fail`; a held write outcome is `blocked`.
* Focused tests, including a mismatched write response with a matching reload, a held write response, and any-field divergence.
* New unique external full gate and official receipt verification before push.

## Acceptance criteria

* Tests assert no durability pass and the new fail cases; Ruff clean; only the two tools files and own tracking changed.
* No new provenance mechanism, live write authority or runtime change.

## Phase Checklist

### [x] P01: Correct checker
#### [x] P01-T01: Durability blocked and write-response comparison

### [x] P02: Tests
#### [x] P02-T01: Add and adjust focused tests; break fixture aliasing

### [ ] P03: Validate and publish
#### [ ] P03-T01: Full gate, receipt verification, push, draft PR

## Critique Disposition

* No critique was run before implementation; recorded as a process gap in the review.

## Follow-Up Items

* Carry forward parent RV-001..RV-004.
