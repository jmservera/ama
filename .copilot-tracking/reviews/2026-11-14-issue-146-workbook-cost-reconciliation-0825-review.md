# Review: issue 146 workbook cost reconciliation

Execution: once. Outcome: conformant with open items routed as follow-ups.

* Fallback yields Unknown/Unreconciled, never zero, when rows are absent, the currency differs or the window spans months.
* Follow-up 1: confirm the budget currency (`ExpectedCurrency='USD'` is assumed) and the export table schemas; KQL is untested against live data.
* Follow-up 2: install `zava_forward.orchestrator` to clear the unrelated test error.
* Human review remains unchecked.
