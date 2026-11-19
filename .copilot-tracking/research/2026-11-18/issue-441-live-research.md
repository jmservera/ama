# Research: issue 441 live assessment (2026-11-18)

* Base: `76d89fee2` on `origin/main`. Branch `test/resident-portal-docs-live-20261118T1137Z`.
* Research disposition: executed. Planning Readiness: Ready.
* Issue state: OPEN. Eight criteria ticked; criterion 5 unticked.

## Findings

* Criterion 5 asks the requirements owner to disposition FR-044/AC-084 wording, keep per-message human review default, keep any exception inactive, and keep unsigned status, quality findings, OD-52-55 and Not run criteria visible.
* BRD FR-044/AC-084 (docs/brds, line 1602) make named per-output review normative, with a routine exception only under RULE-028/FR-061. OD-53 stays OPEN.
* Owner direction 2026-11-02 is already recorded in BRD OD-53 and PRD OQ-029: exception approved in principle subject to named Legal/Compliance approval; demo display is not OD-53 or RULE-020 approval and does not satisfy FR-044/AC-084.
* Owner decisions 2026-11-18 (demo scope; DPO/Legal approval not needed for the demo) do not name FR-044/AC-084 and do not supply the named approval. They do not convert the criterion into evidence of a disposition.
* `tools/test_resident_portal_docs.py` passes (2 tests). Observed; raw output not retained.
* Live Azure and Playwright are not relevant: the criterion is a human decision, not a runtime behaviour. No resource was touched, no credential was read.

## Conclusion

Criterion 5 cannot be proven by evidence for the demo. Smallest outstanding step: the requirements owner confirms in the issue that integrated wording makes per-message review normative now, with the exception inactive pending OD-53/RULE-020.
