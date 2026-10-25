# Review: seed demo baseline merge (issue 360)

Date: 2026-10-25. One independent review (code-review agent, read-only) run after implementation and the changes record, on the uncommitted candidate. The reviewer could not run the tests; test results are mine.

* Verdict: PASS-WITH-FINDINGS. No data-loss or atomicity defect. Transaction, rollback (including the MSSQL `@@TRANCOUNT` guard), `seq` and replica sync, MSSQL `_meta_set` and failure-injection tests were judged sound. Artifact phase order matched file times (research, details, plan and critique, then source and tests).
* Findings: (1) Medium, CLI could first-start seed an empty target with staff and `as_of`; (2) Low, derived queue columns and meta recomputed and undocumented; (3) Low, missing tests for omitted defaults and error-path privacy.
* Dispositions: all three were fixed in the same candidate before commit; see the Independent review section of `changes/2026-10-25/seed-demo-baseline-360-changes.md`. The fixes were not re-reviewed by a second reviewer (one review per task); they are covered by tests (36 OK) and the full gate.
* Residual limits: live execution, the image and job route, and the live counts are not yet performed and are outside this review. Staff are intentionally absent after the merge, so features needing staff rows stay unavailable until staff are provisioned through the supported route. The seed `as_of` (2026-10-13) differs from the live `as_of`.
