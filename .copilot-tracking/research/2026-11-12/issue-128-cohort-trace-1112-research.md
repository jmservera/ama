# Research: issue 128 constructed source/sensor completeness trace (Refs #128)

Date: 2026-11-12. Base: fetched `origin/main` cd81888e4a81cf4c712d50b357ca900fd5c8c06b (worktree HEAD equals it, clean). Branch `research/constructed-cohort-trace-128-1112`. Research disposition: executed. Planning Readiness: Ready.

## Scope question

Is the trace "paired constructed source/sensor completeness inputs -> deterministic prioritisation or abstention -> existing diagnostic detection of unjustified exclusion" already implemented? Issue #128 RAI criteria 1, 3 and 5 name source/sensor completeness pairs, no rank lowering, and detection of every seeded defect.

## Evidence

* Issue #128 body and comments (to 2026-11-09): #1174 (paired_equity), #1211 (comparability), #1222 (diagnostic and regression correction) delivered bounded slices; no criterion ticked; `fairness_evidence=False`, `activation_allowed=False` stay.
* Deterministic ranking: `ranking.rank` rules (`safety_open`, `support`, `waiting_days`, `stage_order`, `case_id`) never read `source_record` or `sensor_data`; there is no abstention path, missing support only adds the `support_unknown` reason.
* `journey_register.human_review_route` treats `source_record` in (None, missing, stale, partial) as `source_missing` with `rank_effect=none`.
* `cohort_ranking_eval` / `cohort_eval` (#222) already pass source and sensor cohorts through the real ranker; its seeded defects are sensor drops and history demotions only. Not duplicated here.
* `paired_equity.DIMENSIONS` (#1174, #1211, id-collision fix) covers `sensor_completeness`, `support_or_contact_need`, `appointment_history`. There is no source-completeness dimension, in code, tests, README or the equity test plan, and none of the earlier RPI artifacts records a decision to exclude it.

## Finding (distinct, concrete)

A source-completeness pair given to `paired_equity.evaluate` is rejected as `<id>:invalid_pair`, so the existing paired diagnostic cannot test that a missing/stale source record leaves rank unchanged, nor detect a seeded source demotion. The defect is local to this diagnostic and does not repeat the #1211 comparability or id-collision cases.

## Authority

Issue criterion 1 and the PRD FR-054/AC-073 pairing language name source completeness. The existing pattern already uses fixture-local predeclared contrasts that are explicitly not a production field mapping or approved policy; this change adds one more of the same kind. No ranking policy, threshold, hash or order change; no human, actual-model, provider, private data, Azure or approval dependency.

## Not in scope

Ranking policy/threshold changes, AI task cohorts, geography/archetype, human review, screen-reader or research protocol, population-fairness or activation claims.
