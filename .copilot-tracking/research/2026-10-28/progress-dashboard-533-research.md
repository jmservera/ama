---
title: Task Research progress-dashboard-533
ms.date: 2026-10-28
---

<!-- markdownlint-disable-file -->

| Field | Value |
| --- | --- |
| Date | 2026-10-28 |
| Researcher | RPI Agent, rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-28/progress-dashboard-533-research.md |

## Research Brief

Research synthetic case lifecycle fields, staff navigation and API/test seams
for #533. Audience: implementer and independent reviewer. Output mode:
convergence. Deliver accurate date-bounded progress and URL-persisted closed
case filtering/paging without editing briefing or map modules.

## Research Parameters

Focused posture, selected for bounded issue scope. Internal candidates:
src/api, src/core, existing synthetic browser fixtures. External candidates:
Fluent UI React Storybook and Web Interface Guidelines. No framework swap,
private datasets, secrets, .env, Azure or az. Research writes restricted to
this research root and required session state. Heavy checks require
nonblocking /tmp/ama-rpi-heavy.lock with up to 40 minutes retry.

## Extension Registry and Provenance

Repository instructions and user scope selected. rpi-research and
web-design-guidelines selected. Public-page design skills skipped: this is
an employee app, not a landing page. Specialists skipped during research:
the data-to-screen trace is tightly coupled and handled inline.

## User Participation and Research Decisions

User explicitly requests the full loop, exact branch and stacked base.
No interaction needed; this is a confirmed automatic full-loop request.
PR #529 is OPEN with head feat/case-journey-ux-526. Worktree initially clean
on feat/progress-dashboard-533. Do not push without the complete local gate.

## Scope and Success Criteria

All #533 measures, date selector, accessible chart tables, server endpoint,
closed filters (status/date/team/text), URL state and boundary tests.
No authority changes or real operational metrics.

## Direction Controls

* Preserve native Fluent-token UI and existing dataset contracts.
* Keep new logic separate from briefing/map code.
* PR base feat/case-journey-ux-526; text "Refs #533", no closing keyword.
* Commit local delivery if full gate needs prohibited Azure prerequisites.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What lifecycle/team/AI data actually exists? | depth | Answered, C4-C8 |
| Q2 | How should date metrics and closure cohorts be defined? | depth | Answered, C4-C7 and synthesis |
| Q3 | Where can separate API/UI modules integrate safely? | straightforward | Answered, C1-C3 |
| Q4 | What focused automated/browser evidence is available? | straightforward | Answered, C9 and implementation evidence |

## Prior Knowledge Gate

Read original/addendum, reference index and owner memory. Read UX design
system, WCAG baseline and content standard. These establish native-token
foundations, plain language and known human accessibility acceptance gaps,
not full Fluent runtime adoption or WCAG conformance.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Issue #533 read with comments (none). Required dashboard measures and list
acceptance confirmed. Storybook shell and latest interface guidelines fetched
2026-10-28. Next inspect native app, data schema and synthetic fixtures.

Reflection: no new framework is justified. Dataset semantics need verification
before selecting calculations.

#### Wave 2: Deeper

Native hash router and script recovery provide separate-module integration.
Store lock refreshes SQL readers. Closed-case legacy branch returns before
free-text filtering, so a separate closed endpoint avoids changing shared queue
semantics. Generated history uses explicitly synthetic dated actions:
Identified, Accepted handover, Withdrawn, Excluded, and reopened aftercare.
Current team means owner_role, never actual staff identity.

Reflection: lifecycle dates can come from labelled simulation history, not
stage_since (which is only current-stage age). Actual human closure events
and controlled reopen events must also be included.

#### Wave 3: Contrarian

Challenged treating all serving data as synthetic: the dictionary explicitly
says tenant bindings and actual chat are not certified synthetic. Admit only
explicitly marked cases or cases with a wholly marked simulation history.
Do not open any dataset path. Unknown lifecycle stays excluded with coverage
counts. Do not treat template output as AI or draft review as approval.
Team/journey/stalled data describes the current recorded view, not a fabricated
historical owner or workflow reconstruction. Historical backlog counts only
cases with usable lifecycle evidence and accounts for reopen events.

Reflection: no new data generation or private source read is required.
Focused scope covered; no second cycle is needed.

#### Parent Synthesis and Disposition

Accept native modules, explicit synthetic admission, observed lifecycle cohort
and visible limitations. Reject inferred opening from earliest contact/current
stage and unlabelled current staff/AI data as demonstration evidence.

## Evidence Log

| ID | Source | Finding |
| --- | --- | --- |
| W1 | https://github.com/jmservera/ama/issues/533, retrieved 2026-10-28 | Dashboard and closed-case acceptance boundary |
| W2 | https://storybooks.fluentui.dev/react/, retrieved 2026-10-28 | React v9 reference only; shell retrieved, component patterns require further inspection |
| W3 | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md, retrieved 2026-10-28 | Labels, keyboard, URL state, tables, errors and focus rules |
| C1 | src/api/src/zava_forward/api/web/app.js:178 | Recoverable script registry and route cancellation |
| C2 | src/api/src/zava_forward/api/workbench.py:35 | Staff navigation and manager-only closed archive |
| C3 | src/core/src/zava_forward/core/store.py:246 | Legacy closed filter bypasses text search |
| C4 | support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/build_mvp_dataset.py:273 | Labelled simulation history schema; source code only inspected |
| C5 | src/core/src/zava_forward/core/appointments.py:58 | Explicit home-case closure history, independent of stage |
| C6 | src/core/src/zava_forward/core/workflows.py:133 | Controlled reopen event stored in returns |
| C7 | src/core/src/zava_forward/core/ai_tasks.py:174 | Task/source/case IDs, created and resolved_at, review status |
| C8 | docs/reference/research/retrofit-synthetic-data/data-dictionary.md:9 | Real chat and tenant bindings are not synthetic |
| C9 | src/api/checks/design_system_browser_check.py:231 | Owned constructed-data loopback harness |
| W4 | https://storybooks.fluentui.dev/react/index.json, retrieved 2026-10-28 | Table native/default/primary-cell, Field validation and Select initial-value patterns |
| W5 | https://raw.githubusercontent.com/microsoft/fluentui/master/packages/react-components/react-table/stories/src/Table/Default.stories.tsx, retrieved 2026-10-28 | Storybook default structured row/header/cell pattern; reference only, no React code imported |
| W6 | https://raw.githubusercontent.com/microsoft/fluentui/master/packages/react-components/react-field/stories/src/Field/FieldDefault.stories.tsx, retrieved 2026-10-28 | Labelled field and explicit validation-message pattern |

The first guessed table source filename returned 404; the Storybook index and
public repository directory resolved Default.stories.tsx successfully. The
guidelines source was refreshed before final web assessment.

## Alternatives and Decision State

Select standalone progress.py and progress.js, dedicated GET /api/progress and
GET /api/closed-cases with existing stats/cases authorization kinds. Native
tables/forms, CSS bars plus numeric text, and URL-based hash queries; no chart
dependency. React/framework migration excluded by user. Existing queues remain
unchanged. Current-role groupings are labelled as teams, with unknown explicit.

## Open Questions, Risks, and Residual Uncertainty

Missing dates/outcomes must remain unknown, not invented. Historical backlog
requires explicit temporal definitions. Full local gate may require prohibited
az; publication remains blocked rather than bypassed.

## Planning Readiness

Ready. Research disposition: executed. Q1-Q4 answered by C1-C9/W1-W4.
Self-check: three ordered inline waves, scope/alternatives/risks and dated
provenance recorded. No research worker or private dataset read claimed.
