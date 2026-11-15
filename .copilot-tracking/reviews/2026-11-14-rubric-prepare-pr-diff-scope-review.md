# Review: rubric prepare PR diff scope (Refs #198)

Date: 2026-11-14. Execution: one self-review of the diff. Outcome: conformant for the scoped change.

* PR events with a diff no longer open artifacts the diff did not touch; removed artifacts and removed files still count.
* Bootstrap, force and instrument changes keep full behaviour; push and dispatch keep full fingerprint comparison.
* Reasons are consistent with the filtered list.
* The pre-change `entries is None` guard still runs on the unfiltered list.

Routed later work (not in this task): fix the 17 pre-existing failing tests and the two RUF100 noqa findings.
