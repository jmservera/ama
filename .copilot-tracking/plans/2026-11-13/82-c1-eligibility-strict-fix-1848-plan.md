# Plan: #82 eligibility strict fix

* [ ] P1 Add `grant_eligibility` action (id, eligibility, eligibility_source): Grants and Evidence Officer only, grant must be Claimable, records outcome, source, recorder identity, role, time on `g["eligibility"]`. Remove eligibility from propose/pending.
* [ ] P2 Approval to Submitted always evaluates `grant_eligibility_verdict`: missing, malformed or unverified record is unknown (blocks). Recorder role must be Grants and Evidence Officer and recorder must differ from proposer and approver (email, code, oid).
* [ ] P3 Approval of Rejected resets eligibility to Not assessed, so resubmission needs a fresh record.
* [ ] P4 Update UI panel and tests: fixtures record eligibility via GEO before Submitted; legacy-bypass test becomes a blocking test; add self-assert, role and rejection tests.
* [ ] P5 Run listed tests, ruff, mypy in /tmp/venv-82c1-1848.

Critique amendments: register action; ignore legacy pending eligibility; fail closed on incomplete identity; cover SQL store.
