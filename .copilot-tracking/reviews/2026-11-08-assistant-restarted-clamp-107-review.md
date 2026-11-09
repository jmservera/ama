# Review: issue 107 restarted-process allowance clamp test (author review)

Date: 2026-11-08. Single author pass; not the independent exact-head review. No re-review in this task.

Review execution: executed. Outcome: Conformant for the LIGHT local scope; actual SQL unverified.

* Matches the plan: one method, no helper or production change. The diff touches only the test file and records.
* Reaches the clamp on a successful restarted claim: second wave succeeds, third is denied at the stored two calls, limits and expiry stay the originally stored values. The mutation check shows the test fails when the clamp uses configured limits, while the merged tests do not.
* Deterministic: sequential single-task workers, existing bounded barriers, no sleeps added.
* The critique returned no blocking findings; no plan revision was needed.

## Not established

* The method has not run on real MSSQL; it is planned for the maintained SQL group only.
* No FULL receipt, independent exact-head review, hosted checks or named human approvals. Fixture authority is not approval.
* Whole #107 and #104, real-model, attestation and Azure evidence remain open.
* Main may move; a later normal merge and exact-base FULL are needed.
