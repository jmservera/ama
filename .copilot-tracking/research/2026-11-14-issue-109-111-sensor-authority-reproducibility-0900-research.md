---
title: Sensor non-authority and reproducibility research (Refs #109, #111)
date: 2026-11-14
---

Research disposition: executed. Planning Readiness: Ready.

## Findings

* `sensor_analysis.derive_signal` is a pure function: no store, clock, task, ranking, hazard, clock-start or hold access. `Signal` carries `priority_effect="NONE"` and `diagnoses_hazard=False`; `ReviewTaskCandidate` carries `changes_ranking`, `starts_clock`, `releases_hold` and `diagnoses_hazard` as `False`. A candidate exists only under an approved rule.
* `sensor_analysis_store.analyse_retained` reads through the consumer's read-only methods and fails closed to INSUFFICIENT. `sensor_review_draft` writes only an unapproved draft under `sensor_review_drafts` plus one audit row.
* Hazard state, service clocks (`aware_at`, `response_due_at`, `resident_update_due_at`), hazard holds, legal holds and `ranking.rank` have no sensor input path. No existing test proves this end to end with extreme readings.
* Gap found: `derive_signal` hashed rows order-independently (`input_digest`) but `comparator.analyse` flags `OUT_OF_ORDER` from row sequence, so the same digest could give different outputs for permuted rows. Retained reads happen to be sorted, so served output was stable, but the pure function was not a function of the reading set.
* The consumer rejects out-of-order arrival per sensor (`OUT_OF_ORDER`), so shuffled arrival yields a smaller retained set, which the analysis reports as INSUFFICIENT with no priority effect (deterministic, fail closed).

## Scope

* Tighten `derive_signal` to analyse rows in a canonical observation order.
* Add `src/api/tests/test_sensor_non_authority_boundary.py` (#109 criterion 3) and `src/core/tests/test_sensor_analysis_reproducibility.py` (#111 criterion 1).
* Focused tier: sensor, hazard and ranking tests, `ruff`, `mypy`.
