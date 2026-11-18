# Issue 125 discovery assistant research (2026-11-14)

* Task: issue-125-acceptance-status. Disposition: executed. Planning Readiness: Ready.
* Inspected `src/core/src/zava_forward/core/discovery_assistant_{boundary,evaluation,drafting,demo}.py` and tests; `src/agents` has no discovery assistant code.
* Existing: readiness gate (`assess_readiness`, ten items), default-deny tool boundary (`authorise_tool`, `ReadOnlyToolbox`), comparison record (`compare_methods`, three comparators), bounded synthetic demo (#1355, not to be duplicated).
* Gap: no record of observed no-write access (criterion 2) and no single status joining the three criteria.
* Constraint (issue #125): evidence pointers are human-supplied; company-data connection needs discovery, privacy and access approvals; all criteria remain unticked.
