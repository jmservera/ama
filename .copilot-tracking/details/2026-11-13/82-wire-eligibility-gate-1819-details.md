# Details: wire eligibility_gate (#82 F1)

* Body fields on `grant_open` and `grant_propose`: `eligibility` in (Eligible, Not eligible, Not assessed), `eligibility_source` (1-200 chars, required unless Not assessed). Stored in `pending["eligibility"]`; copied to `grant["eligibility"]` on approval.
* Critique dispositions (rubber-duck, Revise, applied): PC-001 `grant_open` stamps `eligibility = Not assessed` on every new grant, so only pre-field records lack the key and are exempt; PC-002 add optional eligibility inputs to the proposal form and show pending evidence to approvers; PC-003 select evidence by key presence (`"eligibility" in pending`), validate the whole record, treat malformed as unknown; test null, empty and missing source plus correction after unknown or fail.
* `_grant_approve` for `to == "Submitted"`: evidence is `pending.eligibility` else `grant.eligibility`. Absent (legacy) means no gate. Eligible passes, Not eligible fails, Not assessed or malformed is unknown. Anything but pass raises ValueError with reason, owner and next action before any mutation.
* History entry gains `eligibility` (recorded dict or "Not assessed (legacy record)").
* No new action name, so API role matrix and automation boundary tests are unchanged.
