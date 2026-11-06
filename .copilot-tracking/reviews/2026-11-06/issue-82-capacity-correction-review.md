# Issue 82 capacity-at-booking correction review

Date: 2026-11-06 (UTC). Scope: the correction plan supplement, the diff against `8cae59ec8` and its criteria. Executed once as a dedicated review, not a Changes self-check.

## Outcome

Conformant with qualifications on light evidence only.

| Criterion | Result |
| --- | --- |
| RV-001: no single evidenced order is an explicit Unknown `GateResult`, still a `ValueError` with identical text, no mutation | Met; shared tests, Json and Sql |
| No exception-text comparison in `require_appointment_commitment`; typed, structural sole-failure decision | Met (`len(missing) == 1` plus typed error) |
| Mixed, authority and resident failures, order, classes, `appointment_status` shape unchanged | Met; 197 control tests pass |
| Tests fail before and pass after | Met; RED exit 1, GREEN exit 0 |
| No other family, API, schema or persistence change | Met |

## Findings

* RV-C1 (Low): `len(missing) == 1` couples the discriminator to the assessment's list structure. It is correct because the capacity handler appends last, but a future reordering needs care. Accepted; the tests cover mixed output.
* RV-C2 (Info): the two new cases cover Json and Sql; MssqlProcurement inheritance is not actually executed (RV-003 remains open).
* RV-C3 (Info): a snapshot bug in the first test draft was fixed; it affected only the test.
* r1 RV-001 is technically resolved; RV-002 (out of scope) and RV-003 (pending full validation) stay open. Original records are preserved.

## Remaining

FULL gate with real SQL Server, independent exact-head assessment, publication, named rule review and the eligibility, finance and other authority families. Not a whole-issue Pass.
