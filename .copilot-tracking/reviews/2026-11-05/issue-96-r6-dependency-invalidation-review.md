<!-- markdownlint-disable-file -->
# Review: issue 96 r6 dependency invalidation

Executed once (self-review of the final diff; independent exact-head review remains required). Outcome: conformant for the bounded slice; no material finding open.

* Narrowing is fail-closed: verified lineage, equal form-wide references and equal field digests only; undeclared links and malformed lineage stay stale or Unknown (tests cover both).
* Read-only: no history, staging or approval write; approvals are evaluated, never created; `reviewed_ready` and Held status unchanged.
* Existing contracts: read budgets and draft availability isolation preserved by keeping proposal evaluation separate; three tests amended only for the identical-successor premise.
* Residual risks (routed, not fixed here): approval `bound` is a convention for future Finance records, to be fixed by the approval design under #93/#98; `proposal_freshness` has no API/UI exposure (API/web lanes own those); calculation inputs are conservatively treated as dependent on any change until declared.

## Unmet #96 criteria

C1 approved versioned schema (Finance/template authority). C5 reviewed export. C6 remains partial: approved-rule evaluation, reviewed pack review history and real approval records are not built; Refs #96, not closing.
