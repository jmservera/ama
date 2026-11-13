# Critique (rubber-duck, executed once): verdict Revise, all applied

* PC-001 register `grant_eligibility` in `GRANT_ACTIONS`: applied.
* PC-002 ignore any legacy `pending.eligibility`; only `g["eligibility"]` counts on every transition; test it: applied.
* PC-003 fail closed on incomplete recorder, proposer or approver identity (email, code, oid): applied.
* PC-004 run SQL variants of the new tests via existing SQL grant test class: applied.
