---
description: Focused alert explanation repair and browser regression plan
ms.date: 2026-11-21
---

# RPI Plan: Regulatory plain-language checkbox

## Task Metadata

* Task ID: regulatory-plain-language
* Task slug: regulatory-plain-language
* Plan date: 2026-11-21

## Executive Summary

Add short explanatory notes to alert loading, missing-store, failure and loaded
states so the checkbox changes useful content even without alert articles.
The control will explain that it shows extra notes, not different checks.
Planning and standard critique are complete; live deployment is outside scope.

### What You May Not Know

Main summaries, safety notices and recorded source facts remain visible in both
modes. The law-store problem is not repaired by this presentation change.

## Phase Checklist

P01 changes `regulatoryAlertsPanel` and the control description in
`regulatoryPlainMode`; existing CSS connections remain unchanged.

<!-- rpi:phase id=P01 -->
### [x] P01: Make explanatory mode useful in every alert state

Goals:

Make the reported interaction visibly useful without weakening required context.

Dependencies:

* Completed research and resolved critique.

Changes in the map: alert panel and checkbox description.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add state explanations and describe the control

Goals:

Show an extra explanatory paragraph even when no alerts are available.

Requirements:

* FR-001, FR-002, NFR-001.

Details:

* Use the existing `plain-explanation` mechanism. Include loading, missing store,
  request failure and loaded coverage states. Keep summaries and safety text.
* Explain that notes are optional and changing the checkbox does not run checks.
* Related business sources are unsigned proposal context, not new approval:
  BRD FR-034/AC-080 and PRD FR-034/AC-040 preserve explanation and uncertainty.

References:

* [src/api/src/zava_forward/api/web/chat.js](../../../src/api/src/zava_forward/api/web/chat.js)
* [docs/brds/agentic-retrofit-programme-brd.md](../../../docs/brds/agentic-retrofit-programme-brd.md)
* [docs/prds/zava-forward-retrofit-programme-demonstrator.md](../../../docs/prds/zava-forward-retrofit-programme-demonstrator.md)

Dependencies:

* None beyond phase prerequisites.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Verify keyboard behavior and retained safety context

Goals:

Demonstrate a visible difference in the reported state and preserve populated
alert behavior.

Requirements:

* FR-001, FR-002, NFR-001, NFR-002.

Details:

* Extend the existing synthetic browser harness with one focused state-matrix
  helper. Maximum one helper; remove no tests.
* Cover unavailable service, pending request, empty loaded list, failed request
  and populated alerts. Toggle with Space and verify actual visibility, status,
  safety notice and guidance. Verify mode persists over refresh.
* Existing source tests own unchanged summary and accessibility contracts.
* Run targeted regulatory/accessibility unittests, Node syntax check and
  `python3 src/api/checks/regulatory_ux_check.py` with a pinned local axe script
  if available. Report missing axe honestly.
* No generated UI assets. Test ownership stays in the existing harness.
* Update the API README with the control's scope.

References:

* [src/api/checks/regulatory_ux_check.py](../../../src/api/checks/regulatory_ux_check.py)
* [src/api/tests/test_regulatory_a11y_cues.py](../../../src/api/tests/test_regulatory_a11y_cues.py)
* [src/api/README.md](../../../src/api/README.md)

Dependencies:

* P01-T01.

## User Decisions and Requirements

* User reports no visible checkbox effect and selected end-to-end mode.
* User requested the RPI canvas; it is open.
* Agent-owned planning decisions preserve mandatory information.
* Remote push and deployment require separate consent.

## Planning Readiness and Next Step

Ready. Standard critique passed without findings; no implementation blocker is
known from research.

## Functional Requirements

* FR-001: Space toggling visibly shows/hides useful extra notes in all alert
  states, including unavailable store, without reloading or requesting checks.
* FR-002: Mandatory status, emergency route, guidance, summaries, recorded facts
  and citations remain visible and unchanged in both modes.

## Non-Functional Requirements

* NFR-001: Native labelled checkbox, polite state announcement and visible focus
  remain; no permissions, rule evaluations or safety-control changes.
* NFR-002: Focused local validation tier. Do not claim hosted CI, live-site,
  human comprehension or accessibility conformance acceptance.

## Risks and Open Questions

The serving site may be older than source. Deployment is not authorized.
No material implementation choice remains unresolved.

## Sources

* [.copilot-tracking/research/2026-11-21/regulatory-plain-language-research.md](../../research/2026-11-21/regulatory-plain-language-research.md)
* Fresh Web Interface Guidelines retrieved 2026-11-21.
* ADR not applicable: no architectural decision or connection change.

## Critique Disposition

* Setting: standard, first-task default.
* Execution: Complete; verdict: Pass.
* Findings: none. Direct assessment, not independent external review.

## Artifact Self-Check

Scope is bounded; test additions are locked above. Required context remains.

## Follow-Up Items

* Optional, unselected: investigate missing law-store deployment separately.

## Handoff

Automatic implementation is eligible after the completed critique.
