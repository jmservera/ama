<!-- markdownlint-disable-file -->
# Review: issue 1238 F3 manual_verified supersession (1109)

Review executed once, after implementation and validation, by an independent
read-only code-review agent. Original outcome, immutable. Boundary: uncommitted
diff of `resident_decisions.py` (the agent reported it did not read the test
diff or the README; those are covered by the passed runs in the changes record).

Outcome: Conformant, no material finding.

Checked: two-owner authorization and same-person refusal, identity continuity,
Independent review decision-maker refusal, no manager bypass, late outcome
cannot flip a `Superseded` attempt, `Superseded` keeps the resend gate closed,
receipt, reservation and key preserved, rollback on failure (JSON restore and
SQL discard), withdrawal logic.

## Findings

| ID | Severity | Finding | Routing |
| --- | --- | --- | --- |
| RV-1 | Low, non-blocking | Retention deletion removes `requested_by` and `resident_request_ref` from attempts but not the staff identities in `supersession.authorizations[].identity` (email, name, code, oid). | Later user-selected work. Whether staff identities are in purge scope is a retention-policy decision; the authorizer identities are the audit evidence this policy requires preserved. No correction cycle used; counter stays 1 of 5. |

No second Review runs in this task.
