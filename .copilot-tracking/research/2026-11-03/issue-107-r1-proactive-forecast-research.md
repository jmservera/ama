<!-- markdownlint-disable-file -->
# Issue 107 R1 proactive forecast: research

Research disposition: reused (the 2026-11-03 model-bounds research and review ranked this first). Planning Readiness: Ready.

## Delivered already (merged PRs, not redone)

* PR 287, 293, 301 and the R1 dispatch rebuild: base criteria 1 to 5, RAI criteria 2, 4, 6, 7, 9.
* PR 863: Tokenomics criterion 1 (stated and tested model-call and depth bounds).

## Unmet

* RAI 1 (approvers unset, OQ-017), 3 (serving attestation), 5 (independent Azure SQL race evidence), 8 (delivered-build evidence).
* Tokenomics 2 (usage attribution) and 3 (proactive forecast per period).

## Findings

* `Assistants.scan` and `eligible` define each predicate; `_enqueue` derives a deterministic task ID, so an existing ID means no new provider call.
* `model_bounds` gives the per-request call bound. No read-only count of triggers existed.
* Slice: a read-only forecast reusing the same predicate, task ID and scope checks. Not security, infrastructure, SQL-schema or deployment tier (no DDL, no new write).
