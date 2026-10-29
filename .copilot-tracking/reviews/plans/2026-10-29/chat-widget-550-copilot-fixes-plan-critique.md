---
title: Chat widget 550 Copilot fixes independent plan critique
description: Final-candidate assessment of the four bounded corrections
ms.date: 2026-10-29
---

## Metadata

* Task ID: 550-copilot-fixes; parent: 550-rebase.
* Branch: feat/chat-widget-550; PR: 556, as supplied.
* Critique execution status: Complete.
* Verdict: Pass.
* Assessment count: exactly one final-candidate independent plan critique.

## Inputs and Criterion Boundary

* Plan: .copilot-tracking/plans/2026-10-29/chat-widget-550-copilot-fixes-plan.md.
* Phase details: .copilot-tracking/details/2026-10-29/chat-widget-550-copilot-fixes-phase-details.md.
* Research: .copilot-tracking/research/2026-10-29/chat-widget-550-copilot-fixes-research.md.
* Caller requirements: shared popup and launcher above employee map tier 1000
  and below account tier 1200; readable Close hover on both sites; follow only
  from the pre-append bottom with no history focus; assign/decorate the employee
  opener only without an existing widget. Preserve focus-not-obscured, no
  asynchronous focus theft and reduced motion.
* Narrow source assessment: shared chat-widget.css and chat-widget.js;
  employee chat.js; same-context route handling in app.js; employee/resident
  CSS tokens; test_chat_widget_focus.py; chat_widget_browser_check.py;
  test_chat_panel.py browser opt-in; src/api/pyproject.toml and related README
  validation references. All source paths are under src/api.
* Project context: original case study, addendum, reference index and memory.
* Boundary: assess implementation credibility, test ownership, change budget,
  dependencies, acceptance and evidence design. This is not implementation,
  executed test evidence, a fresh web-interface review, publication approval
  or human/assistive-technology acceptance.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Stacking; C1/C6; P01-T01 | Covered | Both shared selectors currently use 4. Proposed 1100 falls strictly between the observed map summary 1000 and account panel 1200. Real map-pane/control/summary overlap and account priority hit tests go beyond checking CSS text. |
| Close hover; C1/C7; P01-T01 | Covered | Shared Close lacks an explicit hover rule while each site supplies a dark generic button hover. Explicit soft background/brand foreground and computed >=4.5:1 checks on both actual applications target the cascade failure. |
| Conditional following; C2; P01-T01 | Covered | message currently appends and unconditionally calls bottom. The proposed pre-append distance <=1 and activeElement containment guard addresses both older-history reading and focused Sources at bottom; an eligible-bottom positive case prevents disabling following altogether. |
| Refresh ownership; C3/C4; P01-T01 | Covered | install currently overwrites onclick before its !widget decoration guard; create owns the actual toggle. Moving assignment/decorating into the same no-widget branch preserves ownership. Both open/closed refresh cases require identity, draft, ARIA and close/reopen assertions. |
| Focus, reduced motion; P01-T01/P02-T01 | Covered | No new focus calls or smooth scrolling are planned. Existing executable asynchronous focus matrices, outside-focus dismissal, focused-control hit testing and reduced-motion assertions are retained. |
| Documentation; P01-T02 | Covered | Existing API README is the designated behavior reference; no runtime tracking links or unrelated knowledge-base changes are planned. |
| Validation; P02-T01 | Covered | API source/test PYTHONPATH, /tmp/mv Python/Ruff/mypy, named chat-related unit groups, opt-in panel browser test, adapter/widget Node syntax and extended local browser check are specified. The explicit isolated helper formatting step addresses the configured checks/*.py formatter exclusion. |
| Evidence; P02-T02 | Covered | Per-finding semantic results, command status, counts, output paths, adverse attempts and limitations must be recorded; blocked checks cannot support acceptance. Existing harness verifies pinned axe bytes and uses synthetic loopback applications. |
| Review and persistence; P03 | Covered | One independent implementation Review follows validation and reconciliation. Scoped local commit follows identity resolution; no push, Azure action, rubric write or publication claim is authorized. |

## Findings

Actionable finding set: empty. No PC-xxx defect is supported by the supplied
final candidate and narrowly inspected source. Severity counts: Critical 0,
High 0, Medium 0, Low 0. No correction or significant/divergent user decision
is required. Implementation verification obligations below are not additional
critique findings.

## Test Ownership and Change Budget

* Existing src/api/tests/test_chat_widget_focus.py owns executable Node units.
  Its lightweight DOM currently lacks realistic scroll geometry; P01-T01
  explicitly assigns that extension rather than treating source matching as
  behavioral proof.
* Existing src/api/checks/chat_widget_browser_check.py owns real-layout,
  two-application regression assertions. Its current conversation checks do
  not hold a reply while history is deliberately being read; the planned
  held-response assertions add that missing scenario.
* Removals: none. Existing assertions remain required.
* Maximum additions: two unit test methods, four bounded browser helper
  functions, zero new test files. Four corrections fit these ownership
  boundaries without adding a parallel harness.
* Required semantic evidence includes scroll position and eligible following,
  active-element identity/visibility, actual overlap hit targets, computed
  hover contrast and widget/draft/ARIA/toggle continuity. Syntax, source
  strings and axe alone cannot substitute for these assertions.

## Strengths and Residual Risk

* The changes target the four observed causes without changing adapters'
  authorization, models, backend behavior or the native expanded-map top layer.
* P01 precedes P02, and evidence reconciliation precedes P03 Review and local
  persistence. No missing decision-critical research dependency was found.
* Browser geometry, rounding, cascade behavior and route lifecycle require
  execution. The research and plan explicitly preserve that limitation rather
  than claiming observed success.
* Validation blockers must remain explicit and prevent acceptance claims.
  Complete local publication gates, hosted checks and human/live acceptance
  remain future coordinator-owned obligations, not waived gates.

## Questions or Blocking Evidence Gaps

None for planning. No user response is required.

## Limitations

* No implementation or validation commands were executed during this critique.
  Planned checks are credible, not proven passing.
* The supplied clean, up-to-date pull result and PR lifecycle were not repeated.
  Read-only local inspection confirmed feat/chat-widget-550 and the supplied
  untracked planning/session artifacts; these were not moved or modified.
* No new guideline-source retrieval or full-site review was performed because
  this assessment is limited to the supplied plan and its source evidence.
* Only this critique artifact was written. Plan, details, research, source and
  prior review outcomes remain unchanged; no workers were launched.

## Recommended Next Action

* Highest-impact finding: none.
* Action owner: planning parent for handoff; implementer for P01/P02 evidence.
* Smallest next action: record this Pass and proceed with the bounded P01 work.
* Exact implementation resolving evidence: P02 command results and actual
  four-fix semantic assertions in the dated changes record, followed by the
  single independent P03 Review. This is future verification, not resolution
  of an open critique defect.
* Decision route: direct parent continuation; no significant/divergent choice.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-29/chat-widget-550-copilot-fixes-research.md](.copilot-tracking/research/2026-10-29/chat-widget-550-copilot-fixes-research.md) | Supplied cause and regression evidence |
| [.copilot-tracking/plans/2026-10-29/chat-widget-550-copilot-fixes-plan.md](.copilot-tracking/plans/2026-10-29/chat-widget-550-copilot-fixes-plan.md) | Assessed final candidate |
| [.copilot-tracking/details/2026-10-29/chat-widget-550-copilot-fixes-phase-details.md](.copilot-tracking/details/2026-10-29/chat-widget-550-copilot-fixes-phase-details.md) | Assessed implementation and validation tasks |
| [.copilot-tracking/reviews/plans/2026-10-29/chat-widget-550-copilot-fixes-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/chat-widget-550-copilot-fixes-plan-critique.md) | This single independent assessment |

## Next Steps

No user action is required. Return Complete / Pass to the active planning
parent for disposition and implementation handoff. This worker stops after
the critique; do not repeat it or execute implementation, tests or Review here.
