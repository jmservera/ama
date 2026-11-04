---
title: Issue 76 research, safeguarding clock and named owner
ms.date: 2026-11-04
---

## Scope

Issue 76, unmet criterion 5: hazard and safeguarding items show a clock and a named owner.

## Delivered already (merged on main)

* PR 325: role task queues and shared case context.
* PR 376, PR 407: queue signals, reset scope, current-stage blockers.
* PR 897 (commit f9a1faad3): hazard clocks state named owner, owner status, response state and resident update state. Unknown owners are stated plainly, never invented.
* Criteria 1 to 4, 6 and 7 are ticked on the issue.

## Findings

* The case model holds no safeguarding record. A search of `src/core` finds safeguarding only in data-protection prohibited-field lists, rule cards, regulatory chat gates and synthetic fixtures, never as case data with an owner or deadline.
* `data_protection.py` lists safeguarding among fields that must not enter free text, memory or AI paths. A new safeguarding data field is therefore a data-protection decision, not a plain engineering change.
* No approved safeguarding response time or named safeguarding role exists in the repository. Any clock length would be invented, which repository conventions forbid.
* Hazard clocks remain a recorded snapshot, not a live statutory clock (PR 325, PR 897).

## Planning readiness

Blocked for implementation. Needed from humans before a slice is honest:

1. Owner and legal decision on whether and how the demonstrator holds a safeguarding marker (DPIA, minimisation, role visibility).
2. A named safeguarding lead role and the approved response clock, with source.
3. Resident-consent and human-approval boundary for who may see the marker.

## Follow-ups

1. Record the safeguarding policy decisions above, then plan a stacked slice: marker field, server-enforced role projection, clock sentence reusing the PR 897 owner wording.
2. Live Entra and human acceptance stay open.
