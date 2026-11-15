<!-- markdownlint-disable-file -->
# Plan critique: every list offers a read-only export (issue #80 criterion 2)

* Executions: one (independent rubber-duck critique). Not repeated.
* Verdict: proceed with changes.
* Process deviation: implementation began before the critique ran, so the strict research, plan, critique, implement order was not kept. Recorded honestly; the critique findings were still applied before Review.

## Findings and dispositions

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | Inventory scanner missed aftercare evaluator and law provisions and dynamic endpoint forms | Applied. Scanner now reads `AFTERCARE_API` and `read("...")` forms; remaining endpoints are listed as exempt with plain reasons. |
| 2 | Proposals CSV truncated at one 50-row page | Applied. `all_proposals` follows `next_after` up to 200 pages; paging test added. |
| 3 | `safe_cell` ignored whitespace-prefixed formulas | Applied. Leading space, tab, CR and LF are skipped before the trigger check; tests added. |
| 4 | Tests lacked privacy and role canaries and suppression data | Applied. Concern-row canary test, time-report minimum-group test, contractor 403 and anonymous 401 checks. |
| 5 | State comparison covered only the main database; link check proved little | Applied. Law store rows are compared too; every `/api/...csv` link on a screen must be a listed route. |
| - | New routes absent from the role endpoint inventory | Routed to follow-up. Role gating is inherited from the JSON prefix and is covered by the new end-to-end test. |
