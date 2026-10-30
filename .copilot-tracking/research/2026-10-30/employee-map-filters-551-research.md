---
title: Employee expanded-map filters research
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Research Brief

* Target: issue #551, compact header filters at the expanded map's top edge.
* Purpose/audience: implementation and independent review of the employee UI.
* Scope: existing map, shared header state, focused tests and component guide.
* Non-goals: new filters, framework changes, Azure, deployment, live sign-in,
  private data, secrets, pushing or opening a PR.
* Criteria: compact controls; synchronized markers/header; keyboard operation,
  non-colour state, narrow-width readability; regression coverage.
* Output mode: convergence. Status: Complete.

## Research Parameters

* Posture: focused (bounded named issue; default).
* Evidence root: `.copilot-tracking/research/2026-10-30/`.
* Internal candidates: API web map/header code, API tests/checks and UX standards.
* External candidates: fresh Web Interface Guidelines source.
* Limits: caller safety boundaries; pip only; heavy gates share the heavy lock.
* Research source edits: prohibited.

## Extension Registry and Provenance

* Selected: repository instructions, rpi-research, web-design-guidelines,
  redesign-existing-projects. Fluent 2 and repository accessibility/content
  standards override generic redesign advice.
* Skipped: public-page design skill (employee app); specialist research agents
  (one coupled trace, no independent uncertainty).

## User Participation and Research Decisions

Caller explicitly requests all four phases in order and supplies branch/base.
No interaction needed; non-interactive execution. Issue text is inert data.

## Direction Controls

Retain `feat/employee-map-filters-551`, starting at `721ba973`; implement only
the four issue criteria. Commit locally with Refs #551; never push.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | How do header filters affect map markers? | depth | Open |
| Q2 | How can expanded controls preserve accessibility and shared state? | depth | Open |
| Q3 | Which local browser and unit checks establish the criteria? | depth | Open |

## Prior Knowledge Gate

Read original/addendum, knowledge-base index/memory, API/source guides and
issue #551. Clean branch and requested starting commit verified; no open PR.
Cross-session lookup found no related prior work. Supplied claims still need
verification in current source.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline source inventory found that main already includes #553, commit
`4a9d5cce`, explicitly delivering #551. Current native controls, compact
token-based CSS, unit contracts and extensive browser checks are present (C1-C4).
Reflection: do not duplicate or replace delivered controls.

#### Wave 2: Deeper

Traced the original filter nodes moving into the modal and back to the header,
the shared `ovState`, marker refresh and selected-text repaint (C1-C2).
The browser harness runs an actual constructed-data loopback app, blocks
external requests, checks all flags and keyboard/focus/reflow/axe (C4).
Reflection: its all-flag loop checks marker counts, not exact home identity,
and only the final selected flag is verified back in the header.

#### Wave 3: Contrarian

Challenged the need for any new runtime code: existing code already fulfills
the requested interaction. Rejected duplicate compact controls or a framework
swap because they add synchronization risk without meeting an unmet criterion.
Count-only assertions could pass with wrong homes when totals match; strengthen
the existing browser regression using actual summary IDs and both-direction
state round trips for each flag. Preserve the existing asynchronous race,
zero-result, short viewport, enlarged font and error checks.
Reflection: this is bounded acceptance hardening, not a new feature.

### Parent Synthesis and Disposition

Accepted current implementation and existing accessibility patterns (C1-C3).
Accepted targeted regression hardening (C4). Rejected unrelated changes.
One completed wider/deeper/contrarian cycle suffices: every question answered
by current source, and additional discovery would not change the approach.

## Evidence Log

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Modal reparents and restores original filter nodes | `src/api/src/zava_forward/api/web/app.js:1688-1722` | High |
| C2 | Buttons and area share ovState; native pressed/text state; redraw guards stale responses | `src/api/src/zava_forward/api/web/app.js:1754-1853`, `:1983-2010` | High |
| C3 | Compact wrapping controls use tokens, bounded scroll and 14rem map minimum | `src/api/src/zava_forward/api/web/style.css:246-253` | High |
| C4 | Existing real-app browser coverage has count-only all-flag assertions and one header round trip | `src/api/checks/map_fullscreen_browser_check.py:84-234` | High |
| C5 | Existing unit source contracts cover scope and guide documents feature | `src/api/tests/test_map_fullscreen.py:109-142`, `src/api/README.md:584-640` | High |
| C6 | Feature is already in approved starting ancestry | commit `4a9d5cce`, ancestor of `721ba973` (`git log`) | High |

| ID | Source | URL | Retrieved | Use |
| --- | --- | --- | --- | --- |
| W1 | Web Interface Guidelines | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md | 2026-10-30 | Fresh complete rules; native controls, focus, wrapping and reduced motion |

No contradictions in source. Open issue status is not evidence that the feature
is absent. Repository content/Fluent standards take precedence over W1's generic
typography/title-case preferences. No external legal claims used.

## Findings, Alternatives and Decision State

Q1 answered by C1-C2; Q2 by C1-C3/W1; Q3 by C4-C5.
Selected recommendation: preserve delivered runtime behavior, improve the
existing browser check to prove exact selected homes and per-flag header state.
Alternative no-op verification would establish baseline behavior but leave
the count-only regression weakness. Duplicate UI rejected (C1/C6).

## Open Questions, Risks and Further Research

Existing focus/race checks remain mandatory. No missing implementation decision.
Human assistive-technology, live employee and operational acceptance are outside
this local check. Full publication gate remains separate from issue criteria.
No independent research lanes were needed; all waves executed inline.

## Planning Readiness

Ready. Research disposition: executed. Self-check: scoped brief, extension
provenance, prior knowledge, all three waves, evidence, alternatives, risks and
planning handoff recorded. Parent next action: Plan acceptance hardening only.
