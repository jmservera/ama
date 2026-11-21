# Review: issue 350 live (2026-11-20), one pass

Execution: executed once after implementation. Outcome: conformant for the assessed boundary (src/core drift repair, its test, the evidence note); open items routed as follow-ups, none re-reviewed in this task.

Assessed
* Fix is limited to six identity columns and repairs only disagreeing rows; body is canonical. A review-time defect (bool vs int comparison on Azure SQL bits would rewrite every row on each start) was corrected with a normaliser before commit; `test_sqlreads` and `test_sqlstore` (37 tests) pass.
* Claims in the evidence note match raw outputs; no criterion is stated proven beyond its evidence; the fix is labelled not deployed; no secret or personal data in retained files (scripts read credential files at runtime only).
* Unrun: live Azure SQL path, `src/api` suite, full gate (coordinator-owned).

Follow-ups routed
1. Deploy the repair to the demo (production change, owner decision) and re-measure own queue 16 vs CSV 133.
2. Edge design for criterion 1 (with #349).
3. Human-owned: release authority and SUS-1, map provider, photo consent, law seeding, further role accounts, audit job first run.
