---
title: Issue 122 service continuity review
---

Review executed once. Outcome: acceptance criteria met in the synthetic prototype; no open material findings.

## Open items (owner decisions or external evidence)

* Witnessed authorised drill (owner activity).
* Recovery and response limits (NFR-004 / AC-058) approval.
* Supplier contract terms (NFR-006).
* Azure SQL / dev deployment evidence of suspension and export.
* Interface identifier mapping (NFR-005).
* Named restart authority; the reference is recorded, not verified.

## Follow-ups

1. Add a UI control for suspension and restart.
2. Run the suspension tests against Azure SQL.

## Second pass review (PR 269 findings)

* Review executed once for this pass. Outcome: truncation and tail-cut findings addressed by `complete`, recorded ledger head and `verify_export(expected_head=)`; tests `test_truncated_export_is_flagged_incomplete_never_valid` and `test_ledger_tail_truncation_and_external_head` cover them.
* Residual: a recorded head inside the bundle can be rewritten with the entries; only an externally held head detects that (documented). `ZF_TEST_MSSQL=1` not run locally (Docker permission denied); CI `mssql` job pending.
