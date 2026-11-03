# Research: issue 233 resident-choice summary withheld panel

Date: 2026-11-03. Disposition: executed (reuses the 2026-11-01 trace and 2026-11-03 withheld-panel research). Planning Readiness: Ready.

## Already delivered (merged PRs Refs #233)

* #671 trace and checker; #713 status refresh; #767 static guardrails; #815 withheld panel on `programme-queue` (overview, per-home) and `resident-choice` (per-home).

## Remaining gap found

* `docs/reference/research/ux/atlas-screen-trace.md` stated the `resident-choice` summary view does not show the "Not shown for this role" panel. The summary lists update commitments with a safe route reference, so withheld contact and access history should be disclosed there too.

## Acceptance criteria status (issue #233)

* Met: atlas findings labelled hypotheses.
* Partly: perspectives and themes traced (one theme deferred by record); tensions shown (proposed rule, rendered behaviour unassessed).
* Unmet: same-home walkthrough on screens (design-level only, stage 1 deferred, no EX-HOME-901 fixture); WCAG 2.2 accessibility (static only; no rendered or AT evidence); design-system components (static class check only); #155 validation.
* Tier: focused (web view and docs only; no security, infrastructure, SQL or deployment).
