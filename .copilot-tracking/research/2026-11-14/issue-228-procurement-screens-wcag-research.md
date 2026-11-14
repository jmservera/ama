# Research: #228 procurement screens WCAG 2.2 criterion

* Remaining criterion: accessible per the WCAG 2.2 baseline (#151) with textual state meaning and keyboard navigation.
* Disposition: executed (code read of `role-screens.js` and existing tests).
* Findings: package queue already had text prefixes for capacity and expiry (`screenCapacityState`, `screenExpiryState`). Work-order state, job-pack evidence states and finance invoice status were bare values. No procurement, job-pack or finance screen had section jump links. `a[data-jump]` links with the shared click handler (asset board) are the accepted keyboard pattern; buttons with `onclick` are rejected by existing tests.
* Constraint: `test_connected_home_check.py` matches literal `screenPanel("...",` calls, so panel titles stay literal and the anchor object is the second argument.
* Planning readiness: Ready.
