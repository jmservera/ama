---
title: Plan, issue 176 five-home demo cohort replay regression
ms.date: 2026-11-12
---

## Plan

* [ ] Phase 1: add one focused test to `src/core/tests/test_generated_dataset.py` that parses the runbook five-home table and asserts the seed 20260901 / as-of 2026-10-13 synthetic build contains each id, open, with no hazard record, the runbook stage and property type, and exactly five rows.
* [ ] Phase 2: failing-first negative controls (wrong id, wrong stage, changed as-of) and the focused run, plus `test_scenario_manifest.py` for recipe-hash integrity.
* [ ] Phase 3: runbook provenance note, synthetic-data README paragraph and log entry. Refs #176, never Closes.

Details: [details](../details/2026-11-12-issue-176-demo-cohort-replay-2236-details.md).
Research: [research](../research/2026-11-12-issue-176-demo-cohort-replay-2236-research.md).

## Decisions

* Test-only source change; no generator, seed, builder, manifest or pinned recipe source edits, so recipe hashes and manifest integrity are untouched.
* Parse the runbook table rather than duplicating ids, so doc and generator cannot drift independently.
* Do not assert ARC codes or damp-report history (not in the seed output); say so in the test docstring and the doc note.
* Validation tier: focused (non-gate test addition, documentation). No blanket gate, no receipt.

## Critique (one pass, independent rubber-duck, executed 2026-11-12)

Verdict: revise, applied directly, no user decision needed. Findings applied: require five unique table ids with a duplicate-id negative control; parse only the named section and validate header, row count and required cells; correct the register size to 6,000 rows and claim reproduction with that fictional register only; state in the provenance note that rule selection, ARC codes, direct links, sensors, simulator cohort, AI scope and the private deployed store are not verified. No repeat critique.
