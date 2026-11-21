---
description: Investigate the missing visible effect in empty regulatory alert states
ms.date: 2026-11-21
---

# Task Research: Regulatory plain-language checkbox

| Field | Value |
| --- | --- |
| Date | 2026-11-21 |
| Researcher | RPI Agent |
| Output mode | convergence |

## Executive Summary

The checkbox toggles extra explanation paragraphs, not the main guidance.
The unavailable-law-store state in the screenshot has no such paragraphs.
Research is complete; the source explains the reported lack of visible change.
The deployed version is not inspected.

## What You May Not Know

Plain-language summaries deliberately remain visible in both modes, so hiding
those summaries would break an existing safety-context contract.

## Findings

### F1: Empty states have nothing to toggle

Q1 is answered by C1 and C2. This is an evidence-backed finding: the law-store
early return sets status text and clears the list. Explanations only appear
inside alert articles. The checkbox changes its own announcement but no content
in the screenshot. Confidence is high for the inspected source.

### F2: Mandatory information must stay visible

Q2 is answered by C3. This is an evidence-backed finding: the existing regression
requires summaries, actions, owners and clocks in both modes. The repair should
add explanatory notes, not remove warnings or rewrite recorded information.

## Recommendation and Alternatives

Add a panel-level explanation for loading, unavailable, failed and loaded states.
Describe the checkbox as showing extra notes, with mandatory information retained.

| Option | Benefit | Risk | Evidence | Disposition |
| --- | --- | --- | --- | --- |
| State-specific extra explanation | Visible effect even without alert articles | Must retain uncertainty | C1-C3 | selected |
| Hide guidance or summaries | Larger visual change | Removes required context | C3 | rejected |
| Disable checkbox when empty | Avoids misleading interaction | No useful explanation for unavailable service | C1 | rejected |

## Scope and Questions

* Goal: make the reported checkbox produce a useful visible change.
* Audience: staff using the regulatory alert panel.
* Scope: alert rendering, control description and focused browser regressions.
* Exclusions: rule evaluation, law-store availability, deployment and legal claims.
* Acceptance: keyboard toggling changes explanatory content in the screenshot's
  state and other empty states, while safety, status and recorded facts remain.

| ID | Question | Source | Status |
| --- | --- | --- | --- |
| Q1 | Why is there no visible difference? | User screenshot | answered |
| Q2 | Which information must remain visible? | Existing tests | answered |

## Decisions and Feedback

| Group | Decision or feedback item | Status | Owner | Evidence |
| --- | --- | --- | --- | --- |
| D1 | Keep mandatory information; add state explanations | confirmed | agent | C1-C3 |
| D2 | Focused local validation, no shared deployment | confirmed | repository safeguards | Source-only UX change |

## Risks and Open Questions

The unavailable law store is a separate condition. This fix must not imply
that enabling explanations runs checks or resolves missing coverage.

## Planning Readiness and Next Step

| Field | Record |
| --- | --- |
| Research disposition | executed |
| Decision participation | agent-owned, automatic, user-selected end-to-end |
| Planning Readiness | Ready, C1-C3 |
| Research depth and helpers | Wider, Deeper, Contrarian completed directly |
| Blockers | None for implementation; deployment not authorized |
| Output mode | convergence, supports planning |
| Next action | Automatic Plan |
| Primary evidence file | .copilot-tracking/research/2026-11-21/regulatory-plain-language-research.md |

## Research Record

### Method and Boundaries

Focused posture for a bounded source defect with screenshot evidence. Date comes
from the user-provided current datetime; evidence root is `.copilot-tracking`.
Initial candidates were the checkbox handler, CSS visibility rules and browser
fixtures. No helpers were needed.

### Extension Registry

Repository instructions selected for branch safety and validation. Fresh
web-design-guidelines retrieved on 2026-11-21. Redesign skills skipped because
this is a functional repair, not a visual redesign.

### Cycle Log

* Wider: compared alert, lookup and CSS behavior.
* Deeper: traced unavailable-law-store early return and browser coverage.
* Contrarian: checked the always-visible summary regression; rejected hiding
  mandatory content. Existing keyboard behavior works for populated articles.
* Synthesis: no further cycle needed; the missing empty-state notes explain the
  symptom without a handler failure.

### Evidence Log

| ID | Source | Claim or finding |
| --- | --- | --- |
| C1 | src/api/src/zava_forward/api/web/chat.js, regulatoryPlainMode and regulatoryAlertsPanel | Class toggle; early-return states lack explanation content |
| C2 | src/api/src/zava_forward/api/web/style.css, plain-explanation selectors | Extra notes hidden unless plain-language class is set |
| C3 | src/api/tests/test_regulatory_a11y_cues.py, summary contract | Mandatory summaries stay visible |
| C4 | src/api/checks/regulatory_ux_check.py, run and check_refresh_focus | Existing keyboard browser harness and unavailable-store fixture |
| W1 | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md, retrieved 2026-11-21 | Labels, empty states, live announcements, focus |

### Self-check

Questions answered; scope and counter-evidence retained. No deployed behavior,
legal approval, hosted CI success or human acceptance is claimed.
