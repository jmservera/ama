---
title: Review, served import refusal correction (#135 C4/5)
ms.date: 2026-11-10
---

Single Review, executed once after implementation and validation. Execution: self-review by the implementing session against the confirmed independent findings; it is not independent. The coordinator exact-head review follows and is not replaced by this one. Assessed boundary: the C4 working tree on frozen 67ad4680 before the local commit.

## Outcome

Conformant for the four scoped items on the evidence below, with the open items and adverse records listed after it. No claim of full #135 criteria, #73 closure, publication readiness or human approval.

## Findings and evidence

* Finding 1 (High, failed transfer persistence): fixed in Core. `test_import_refusals.py` fails on 67ad4680 (8 failures, 1 error in the non-MSSQL set) and passes after: 21 tests, 7 MSSQL opt-in skips locally. Actual disposable SQL Server 2022 run (image sha256:cf8f0ab2ebe6, container removed): 21 tests OK, 0 skips, including committed-reload, preserved prior pending audit, competing writer and a T-SQL trigger rollback. The external probe (4 tests, 10 failing subtests at 67ad4680) now exits 0.
* Finding 2 (Medium, CLI error contract): fixed. `TransferFailureTests` covers a real competing SQLite writer, committed-unconfirmed, partial, driver error and pre-commit refusal; each exits 2 with empty stdout and no traceback; "nothing was recorded" appears only where known. The importer CLI was not run against SQL Server.
* Finding 3 (Medium, source text): fixed. Stored and shown counts come from one locked snapshot; steward, operator, operator-only and unnamed manager covered, SQLite and JSON. The served browser render showed 1 stored and 1 shown for the steward, 1 stored and 0 shown for the operator, and 1 stored and 0 shown in roles_not_named.
* Finding 4 (coupled screen copy): fixed with one sentence at `role-screens.js:919`. Screen test fails on 67ad4680 and passes. Reviewed against the freshly fetched web-design-guidelines (vercel-labs command.md): plain text, no new element, no markup, colour, motion or semantics change; no violations found. Browser checks here are not assistive-technology acceptance.

## Open items and adverse records

* C3 order adverse (implementation before research and plan) is unchanged and remains a publication blocker; C4 order was research, plan, details, critique, changes record, then source edits, then tests, then this Review.
* Plan critique was a self-critique, not independent.
* Original 16 SQL skips from the coordinator runs are retained as their own evidence; the actual MSSQL run here covers only the new projection tests, not the wider API and Core SQL suites.
* JSON store keeps document and audit in two files: a crash between them is still possible and was not made atomic. A JSON-store server must be stopped before `transfer`.
* Rejected batches are not projected; no replay or recovery exists; roles and appointments remain unproven; eligibility is Unknown.
* API suites were not run against MSSQL; the importer CLI was not run against SQL Server.
* No assistive-technology or human accessibility acceptance.

## Routed follow-ups for later user-selected work

* Run the wider SQL-gated Core and API suites against disposable MSSQL if the owner wants broader SQL evidence.
* Decide whether the JSON store needs cross-file atomicity for any other domain (not this task).
