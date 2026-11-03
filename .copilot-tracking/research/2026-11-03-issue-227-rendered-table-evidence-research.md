# Research: issue #227 rendered table accessibility and SA-007 evidence

Disposition: executed (repository inspection). Planning Readiness: Ready.

Prior merged delivery: #653 per-home screens, #776 per-home browser and axe check, #806 cross-home referral table, #831 cross-home browser check; #854 documents and guards role-screen design-system classes (Refs #230). No open PR for #227.

Findings:
* Static guards exist (test_role_screens_conformance, test_design_system) but the rendered safety trees were not asserted for labelled focusable table regions, caption, column scope and cell/column alignment.
* The cross-home summary uses an unlimited table; only the per-home view had a beyond-fifty test (SA-007).

Criteria: 1-4 met in code (see earlier reviews). 5 (WCAG 2.2 baseline) and 6 (Fluent component adoption, #150) unproven.
Slice: test-only rendered-tree evidence for criteria 4 and 5. Tier: focused (no security, infrastructure, SQL or deployment).
