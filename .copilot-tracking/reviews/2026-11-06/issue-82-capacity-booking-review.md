# Issue 82 capacity-at-booking review

Date: 2026-11-06 (UTC). Scope: the bounded plan and details supplements, the working-tree diff against `d688866b2`, and the supplement criteria. Reviewed once.

## Execution and outcome

Review executed against the diff and the plan criteria (not a self-check in Changes). Outcome: Conformant with qualifications. Light evidence only.

## Criteria

| Criterion | Result |
| --- | --- |
| Pass, Fail and Unknown are explicit and observable through `require_booked_capacity` and the `advance` path | Met (shared tests) |
| Known violation (period, deficit) is Fail; missing, legacy, hash or unreadable evidence is Unknown; both refuse | Met |
| Exception type and text, check order, authority and resident checks preserved; no state change on refusal | Met (tests plus existing authority and consultation tests) |
| No message matching, no blanket catch | Met (typed `.state`, single narrow try) |
| No schema, API or persistence change | Met |
| Provenance source, date, version and reviewer carried; reviewer stays "Unreviewed exercise rule" | Met |
| RED before implementation | Met (6 errors, exit 1) |

## Findings

* RV-001 (Low, open): the "single evidenced work order" ValueError is not converted, so that Unknown case is not expressed as a gate outcome. This differs from the plan supplement; disclosed in Changes.
* RV-002 (Low, open): the Pass result is not persisted or surfaced through the API, so only server-internal callers observe it.
* RV-003 (Medium, open): actual MssqlProcurement execution of the new tests is untested. FULL is held by #185.
* RV-004 (Info): no direct revoked-authority regression was added; existing tests are the control.
* The adversarial check found a conflict with `appointment_status`, which swallows the capacity error as text. It was fixed via `_appointment_assessment`, and the mixed-failure case stays a plain ValueError.

## Remaining and unmet

* FULL gate, independent exact-head assessment and publication are pending.
* Whole #82: eligibility, finance and other authority families are not established either way, and named professional rule review is unmet. The capacity provenance is an unreviewed exercise rule, not activation.
* This is not a whole-issue or full-gate Pass.

## Routing

RV-001 and RV-002 become later follow-ups. RV-003 is handled by the separately admitted full run.
