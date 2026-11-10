<!-- markdownlint-disable-file -->

# RPI Plan Critique: issue-152-mobile-empty-c5-1110

* Executed once, before implementation. Verdict: Revise. Boundary: plan, details and research only.

### PC-001 [Medium]: ancestor clipping loop must not misfire on the normally scrolling page
Fix applied: stop at body and html and skip ancestors whose overflow-y is `visible`; do not require the page to fit one viewport.

### PC-002 [Medium]: restoring only a property can leave a stale or removed style attribute
Fix applied: save and restore the exact `style` attribute in `finally`, removing it when originally absent.

### PC-003 [Low]: subpixel rounding could false-fail
Fix applied: one pixel tolerance in both own and ancestor comparisons.
