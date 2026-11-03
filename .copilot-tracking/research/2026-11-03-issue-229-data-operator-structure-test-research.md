# Research: issue #229 slice 6, data operator structure test

Disposition: reused (existing evidence adequate). Planning Readiness: Ready.

## Delivered so far (merged)

* #654 view; #779, #819 browser check; #853 page-level queue; #932 browser evidence for the page queue; #793 artifacts. Criteria 1 to 3 have implementation, unit and browser evidence. Criterion 4 has automated Tab, reflow and axe only.
* Gap: criterion 5 (shared components, no role simulator) has no unit pin for the data operator screen, unlike the asset and board screen (#960, #226).

## Smallest slice

Add unit tests: sections use the shared `card screen-record` component with an h2 first, tables have captions and column-scoped headers, no inline handlers or role-switch attributes, Unresolved shown as text, and the screen source has no role simulator.

## Limits

Desk-based hypothesis. Not assistive-technology testing or WCAG conformance (#151, #155); Fluent adoption (#150) unproven. Not security, infrastructure, SQL or deployment: focused tier, no gate.
