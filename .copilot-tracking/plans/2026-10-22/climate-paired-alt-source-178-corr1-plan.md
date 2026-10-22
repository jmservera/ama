<!-- markdownlint-disable-file -->

# Plan: climate-paired-alt-source-178-corr1

Correction of FR3 monthly provenance, Refs #178, PR #425. Research: .copilot-tracking/research/2026-10-22/climate-paired-alt-source-178-corr1-research.md

* [x] P01 Monthly extremes carry every tied UTC timestamp in chronological order and the paired value; regenerate the report from the retained records; tests for ties, split months, provenance and annual reconciliation.
* [x] P02 Update affected synthesis wording; log entry; no index change (no file added).
* [ ] P03 Commit, full local gate with long lock timeout and new external path, official verifier, push to existing branch, update PR #425 (no closing keywords).

Critique Disposition: one critique executed on the final candidate (rubber-duck), verdict no material findings, nothing to apply. Artifact: .copilot-tracking/reviews/plans/2026-10-22/climate-paired-alt-source-178-corr1-plan-critique.md

## Correction 2 scope (independent functional review RV-001)

Input: independent functional-review finding RV-001: malformed nested JSON containers (hourly_units, header, parameters, properties, parameter, geometry, per-parameter entries) set to arrays or scalars raise uncaught AttributeError instead of ValueError. Prior completed work above is unchanged.

* [x] P04 Add container-type validation in tools/climate_paired_bounds.py so every nested container is a JSON object or the parser raises ValueError; add focused regressions in tools/test_climate_paired_bounds.py for both parsers. No fixture, report, review-record, issue or PR edits.
* [ ] P05 Coordinator-owned: full current-base gate, receipt verification, independent review and publication (not run here; no push, no competing gate).
