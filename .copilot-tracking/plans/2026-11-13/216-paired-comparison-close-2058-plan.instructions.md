---
applyTo: '.copilot-tracking/changes/2026-11-13/216-paired-comparison-close-2058-changes.md'
---

<!-- markdownlint-disable-file -->
# Plan: close #216 criteria 4 and 7 in the paired comparison

Research: [research](../../research/2026-11-13/216-paired-comparison-close-2058-research.md)
Details: [details](../../details/2026-11-13/216-paired-comparison-close-2058-details.md)
Tier: focused (non-gate scoring code and tests; no workflow, dependency, infra or security-control change).

## Phases

* [x] Phase 1: failing-first tests (test_paired_trial.py, test_regulatory_gates.py)
* [x] Phase 2: `beside_cost` shared builder and verdict rules in `regulatory_gates.py` and `paired_trial.py`
* [x] Phase 3: dated-price validation in `cost_per_accepted_check`
* [x] Phase 4: regenerate committed report; README update
* [x] Phase 5: focused validation, commit (Refs #216)
