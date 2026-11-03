# Research: issue #229 slice 3, tighten the data operator browser check

Disposition: reused (existing evidence adequate). Planning Readiness: Ready.

## Delivered so far (merged)

* #654: read-only Data steward and operator view (both source values with provenance, preserved Unknown eligibility, return and exception queue, event metadata with a not-an-audit-trail note). Criteria 1 to 3 and the "no role simulator" half of 5 have implementation and test evidence.
* #779: standalone browser check (keyboard Tab reach of all table regions, axe 4.10.3, 320px reflow, no writes). Its review follow-ups were non-blocking: PARTIAL exits 0 without ZF_AXE_JS, the reopened return reason is not asserted, and generic phrases ("Returned", "Eligibility") match anywhere in the evidence region.
* #793: preserved earlier RPI artifacts.

## Smallest slice

Close the #779 review follow-ups in `src/api/checks/data_operator_browser_check.py`: assert the reopened reason, scope return and conflict phrases to their own table regions, and add the `ZF_AXE_REQUIRED=1` fail-on-skip behaviour already used by the procurement check; document that the RESULT line is authoritative.

## Limits

Desk-based hypothesis. Engineering checks are not assistive-technology testing or WCAG conformance (#151, #155). Fluent adoption (#150) is unchanged. Not security, infrastructure, SQL or deployment: focused tier, no gate run.
