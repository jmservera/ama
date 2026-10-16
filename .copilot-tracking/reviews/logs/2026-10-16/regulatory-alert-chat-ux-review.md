---
title: Issue 215 post-implementation review
description: One-pass synthetic UX review and honest residual acceptance
ms.date: 2026-10-16
---

Task: 215 / regulatory-alert-chat-ux.
Execution: Complete. Outcome: Residual work.

## Opening Review State

Review the full synthetic UX slice against the actual five issue criteria.
The implementation and evidence set are available; P01 and P02-T01/T02 are
complete, while P02-T03 publication remains a delivery action. Read-only final
comparison starts with authority/role preservation, then presentation,
accessibility, protocol and honest acceptance. No blocker to synthetic code
review; actual staff/operational acceptance is expressly unavailable.

## Boundary

Compare the full #215 implementation to the current research, plan, details,
one critique and changes record. Existing backend source/owner/role controls
are reused, not operationally accepted. Review only; no source correction loop.

## Inputs

* .copilot-tracking/research/2026-10-16/regulatory-alert-chat-ux-research.md
* .copilot-tracking/plans/2026-10-16/regulatory-alert-chat-ux-plan.md
* .copilot-tracking/details/2026-10-16/regulatory-alert-chat-ux-phase-details.md
* .copilot-tracking/plans/2026-10-16/regulatory-alert-chat-ux-critique.md
* .copilot-tracking/changes/2026-10-16/regulatory-alert-chat-ux-changes.md
* src/api web assets, browser check, pyproject and README; KB index/log diff.
* Synthetic browser JSON evidence: seventeen states and keyboard/reflow checks.
* .copilot-tracking/reviews/logs/2026-10-16/regulatory-alert-chat-ux-accessibility.json

## Comparison and dispositions

* Role guide and matrix cover the actual seven issue audiences, separately from
  seven existing account roles. Supplier guidance uses the existing Contractor
  view with no law/chat rights. Residents/leasehold remain design-only. PC-002
  is resolved without substituting research audiences for issue acceptance.
* Scoped alerts remain server-filtered. No client controls set clocks, approve
  cards, acknowledge as another owner, release holds or send messages. All six
  required alert fields are rendered. Empty/error coverage is not a clear result.
* Source changes do not clear a retained breach risk. UI distinguishes active
  control from the latest check and retained alert. Sources carry status/dates
  and relative provision links. Text is built with text nodes, not HTML injection.
* Structured chat renders the existing sections, unchanged quotations and fact
  IDs, source metadata and explicit missing-source states. Plain-language mode
  changes presentation only. Doubt uses the real bounded endpoint and receipt,
  with retained focus and retry on failure. Disabled lookup stays visible.
* Review preparation identified the in-flight input/draft race: the displayed
  question could change while awaiting an answer. A bounded correction captures
  the sent question and preserves a newly typed draft; a delayed-render local
  regression passed before this final evidence comparison. This source correction
  during preparation diverged from the nominal review-only write boundary; it
  was necessary to deliver correct behavior and did not initiate a second Review.
* Axe exposed list semantics overwritten by role=log; implementation corrected
  both chat logs with a live wrapper and an actual ordered list before final
  comparison. The final changed surfaces have zero detected axe violations.
* The test search-path addition resolves the shared typed API fixture without
  ignoring errors. No production core/agents/API authority contract changed.
* PC-001 blocker-reporting gate is present. There are no known blocking code
  defects in this assessed boundary; explicit acceptance gaps below remain open.
  The engineering slice can be reviewed as a PR, not accepted as full #215.
* README, KB index and appended log preserve synthetic-only status and do not
  convert the exercise owner into operational approval. No issue box was edited.

## Validation

| Check | Result | Boundary |
| --- | --- | --- |
| Local app/SQL HTTP/browser exercise | Passed | Constructed sources, homes and identities; health readiness and role requests; no private data or inference |
| axe 4.10.3 WCAG A/AA tags | Zero detected violations in 17 states | Eight states retain color-contrast incompletes on textareas; not conformance |
| Keyboard and focus | Passed | Enter/Space, Tab/Shift-Tab, traversal, visible focus, post-answer/doubt focus |
| Reflow/text size | Passed | 320/390/1280px; 200% text at 320px; changed surfaces |
| Pending-answer draft | Passed | Original sent question remains visible; edited next draft is preserved |
| API regressions | Passed | 86 tests, scoped chat/alerts, role matrix, isolation, design/accessibility baseline |
| Core regressions | Passed | 33 regulatory-chat/rule-engine tests |
| API ruff/format/mypy | Passed | 16 format-checked files; 46 type-checked files; no new suppression |
| JS syntax and Git whitespace | Passed | Changed JS and diff |
| Real staff comprehension | Not run / unmet | Real participants unavailable; protocol only |
| Full WCAG/assistive technology | Unassessed / unmet | Scanner/keyboard evidence cannot establish complete conformance |
| ADR chat-value/operational approval | Unmet | No paired human result, real delegate/source approval or release claimed |

## Findings and routing

### RV-001 - Medium: accessibility acceptance remains partial

Evidence: eight axe states retain color-contrast incomplete results for
`#chat-question` / `#regulatory-question`; full manual assistive-technology
assessment is unavailable. Impact: full WCAG 2.2 AA criterion cannot be ticked.
Owner: accessibility engineering/reviewer. Destination: distinct follow-up
to assess the textarea background/obscuration reports and manual criteria,
then implement any confirmed defects. Not a known violation or a synthetic
development blocker. Keep PR/README criterion partial.

### RV-002 - Medium: real staff comprehension remains untested

Evidence: no repairs, housing or grants participants; README provides a
predeclared, authorised-study protocol and critical-error gates. Impact:
comprehension/benefit claims and actual staff use cannot be accepted.
Owner: human research owner with privacy/participant authorization.
Destination: distinct later research task after authorization. Do not
replace participants with role agents or turn a protocol into a result.

### RV-003 - Medium: operational authority and chat ship test remain open

Evidence: ADR 0005 is accepted only for synthetic development; this slice
uses no live legal verification, actual company delegate approval or measured
paired chat-value result. Impact: no operational reliance or chat-value claim.
Owner: Juan Manuel Servera for exercise routing; actual accountable delegates
and product/research owners must be evidenced before operational use.
Destination: distinct source/owner verification and ADR evaluation follow-up,
not a defect in the authorized synthetic UX slice.

## Outcome and delivery routing

Execution Complete; outcome Residual work, not Conformant. Three medium
acceptance/evidence residuals; no known blocking implementation defect in the
assessed slice. The three original plan follow-ups remain distinct and open,
with owners/destinations above. No further Review or implementation loop is
scheduled here. Parent proceeds with the requested commit/push/PR, stating
Refs #215 and the criterion-by-criterion limits. Human merge decision remains.

## Owner-requested implementation follow-up verification

This section records bounded P03 evidence after the independent CHANGES verdict
on d79a737. It does not repeat the original full UX Review or replace its
Residual work outcome.

| Independent finding | Implementation evidence | Disposition |
| --- | --- | --- |
| High: regulatory UX harness absent from CI | src-api browser step invokes checks.regulatory_ux_check after design-system checks. Pinned download and SHA guard, explicit fallback warning, retained JSON. Exact new shell commands passed locally with successful and deliberately failed download. | Addressed in code; hosted CI pending per owner instruction not to wait |
| Medium: target size regression undetected | Per-state real bounding boxes enforce 24px controls, links and summaries, plus shipped 44px cited-lookup summary height. 142 target measurements over 17 states. Deletion of exact CSS rule fails at 1198 x 24px; restoration passes. | Addressed with mutation evidence; 44px assertion protects stronger design, not a claim that 24px violates AA |

The new measurements exposed 18px inline citation links; their directly coupled
24px inline-block sizing passes narrow/expanded text reflow. Static supplier
content remains control-free. Three harness unit tests, 86 existing API tests,
33 core tests, API ruff/format/mypy and existing design-system browser pass.
Wrong hash fails rather than silently skipping axe. Genuine download failure
only skips axe, explicitly recorded in JSON, not keyboard/target/API assertions.

No new legal source, approval, rule activation or access right. All five issue
criteria retain their audited dispositions: role patterns met only as synthetic
design/existing-role guidance; alert shape met only for scoped contracts; WCAG
partial/unmet (eight contrast incompletes and unassessed manual criteria);
doubt/no-source met only in the bounded synthetic slice; staff comprehension
Not run/unmet. Operational delegates/sources and ADR chat value stay open.
Issue body untouched. No conformant or hosted-CI-pass verdict is claimed.
