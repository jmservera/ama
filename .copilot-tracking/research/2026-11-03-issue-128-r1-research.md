# Research: issue 128 equity and journey ownership (R1)

Disposition: executed. Planning Readiness: Ready.

* Prior delivery: no merged PR references #128. Ranking cohort and missing-data evaluation shipped under #222 (`cohort_eval`, `cohort_ranking_eval`, PRs 636, 697, 821), covering the RAI paired-cohort, seeded-defect and threshold-block criteria for ranking only.
* Existing UX evidence: production acceptance protocol and WCAG baseline hold keyboard and screen reader scripts, all Not run. Resident journeys J1 to J6 and R1 each have a documented non-digital equivalent.
* Gaps: no journey owner, service-time threshold or escalation register (NFR-009, AC-071); no human-review routing helper for missing data and incomplete appointments; no user research protocol draft (SA-009, SA-010); AI task, geography and archetype cohorts not covered.
* Slice choice: smallest coherent first slice is a blocked-by-default journey register check, a no-rank-effect review route and a test plan with blank records. Later slices: staffed review workflow, AI task cohorts, human runs.
