# Review: retry-check drift for #531 (2026-11-03)

* Review execution: executed once, self-review of the diff against plan and criteria; no independent reviewer.
* Outcome: Conformant for the scoped slice; not a closure of the issue.
* Checked: the new counts equal one load plus `SCRIPT_RETRY_DELAYS.length` (3) in `app.js`; paths that do not retry keep their counts; README matches the code; no product code, approval boundary or consent behaviour changed.
* Criteria: 1 to 6 evidenced by merged work plus fresh local checks on current main; criterion 7 (live verification on the employee site) remains unmet and owner-run.
* Routed follow-ups: owner live run via `checks/employee_live_acceptance.py` after redeploy; human screen-reader and voice-control acceptance; independent review of this PR; consider deriving the check's counts from `SCRIPT_RETRY_DELAYS` so the next change cannot drift silently.
