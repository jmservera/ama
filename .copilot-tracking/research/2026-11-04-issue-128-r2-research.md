# Research: issue 128 R2 paired-cohort priority check

* Disposition: executed. Planning readiness: Ready.
* Prior delivery: merged PR 901 (journey register, human-review routing, test plan). `cohort_eval` (#222) covers ranking cohorts against an approved manifest. PR 421 draft pair manifest is not merged.
* Gap: nothing runs paired pairs that differ in one attribute against the deterministic policy, or proves a seeded deprioritisation defect is caught per dimension.
* Ranking uses hazards, support, waiting days and stage only, so sensor and appointment attributes must not move rank; support need may only raise it.
* Slice: pure `paired_equity` module in src/core. Out of scope: AI task cohorts, geography/archetype, staffed review, human AT runs, protocol agreement.
