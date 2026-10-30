<!-- markdownlint-disable-file -->
---
title: Employee progress dashboard 533 research
description: Current-main acceptance investigation
ms.date: 2026-10-30
---

## Research Brief

* Topic: Refs #533, employee progress dashboard and closed-case archive.
* Purpose and audience: implement only missing in-scope behaviour and give the coordinator current local acceptance evidence.
* Scope: existing src/api implementation, external tests, local browser checks and dated RPI artifacts.
* Non-goals: Azure, deployment, live sign-in, credentials, private datasets, push, PR creation or issue closure.
* Criteria: daily/weekly opened and closed plus four statistics; table alternatives; filterable paged archive with boundary tests; demonstration labels; passing browser and unit checks.
* Output mode: convergence. Posture: focused, selected for bounded issue scope.
* Evidence root: .copilot-tracking/research/2026-10-30/.

## Research Parameters and Direction Controls

Initial internal areas: src/api progress API, web assets, tests/checks, README and prior #533 evidence. External areas: current Web Interface Guidelines and existing Fluent 2/WCAG/content standards. Research is read-only except evidence and workflow state. User explicitly requests the full ordered loop and local-only commit on feat/employee-progress-dashboard-533 at base 5634f9a077d175a931c15e3400114665d8c071ee.

## Extension Registry and Participation

Repository instructions and RPI research selected. Web Interface Guidelines selected for web scope. Public landing-page taste skills skipped: application dashboard, no public page or redesign requested. Specialist research delegation skipped: one tightly coupled current-main trace. Intake requires no questions: scope, branch, constraints and acceptance criteria supplied.

## Research Questions

* Q1: Which acceptance criteria are already implemented on this base?
* Q2: What exact gaps remain and what local checks prove them?
* Q3: Which claimed acceptance remains outside permitted local evidence?

## Prior Knowledge Gate

Issue read through gh issue view 533 and comments. First four criteria are checked upstream, but those marks are claims to verify. Owner comment says merged PR #540 leaves live deployed employee-site checks outstanding. Existing historical artifacts must remain intact.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Opening inspection confirms clean assigned branch at exact supplied base, no open PR for this branch, existing progress API/web/tests/browser checker and multiple original correction artifacts. Next: verify current implementation and check contracts rather than duplicate delivered features.

#### Wave 2: Deeper

Read progress.py, progress.js, progress.css, the synthetic fixture and all boundary tests, browser checker, API command guidance and UX standards. C2-C6 confirm the requested surfaces already exist. Focused baseline: 41 dashboard tests pass using the documented /tmp/mv environment and caller's source/fixture paths under the heavy lock. System Python lacks Ruff, mypy and Playwright; the documented existing environment has them, so no dependency installation or shared-environment mutation is needed.

Reflection: do not recreate features already merged. Remaining useful in-scope implementation is regression coverage of filtered, non-default page-size traversal and explicit browser first/last/empty boundary controls, followed by fresh local acceptance evidence.

#### Wave 3: Contrarian

Challenge: checked issue boxes and old evidence do not prove this candidate. Inspecting paging shows tests for 0/1/20/21/40/41 totals and beyond-end clamping, but no assertion that combined filters partition a multi-page cohort without duplicates at a custom limit. Browser tests check navigation and counts but not unavailable controls at each boundary or empty-page URL canonicalization. Preserve service semantics and add those exact checks.

Challenge: local shared-password synthetic sign-in is not live employee identity verification. Owner's outstanding deployed-site check cannot be satisfied under this task's exclusions. Full Fluent runtime adoption and direct assistive-technology acceptance also remain separate.

### Parent Synthesis and Disposition

* Accepted C2-C6: existing feature satisfies source-level scope; extend boundary evidence instead of replacing it.
* Rejected: rebuild, framework swap, deployment or modifying issue checkboxes.
* Deferred W1: actual deployed employee-site verification to coordinator/owner.
* Re-entry: not needed; bounded source and test questions answered, fresh execution belongs to implementation.

## Evidence Log

* W1: https://github.com/jmservera/ama/issues/533 retrieved 2026-10-30 using gh; five criteria and live-only outstanding owner comment.
* C1: src/api/src/zava_forward/api/progress.py:1 and associated progress assets/checks exist; semantics not yet verified.
* C2: src/api/src/zava_forward/api/progress.py:243-326 computes daily/weekly flow, backlog, median/p90, current journey/team/stalled/overdue and synthetic AI draft outcomes; :329-410 applies manager-only synthetic archive filters and deterministic paging.
* C3: src/api/src/zava_forward/api/web/progress.js:45-65 supplies semantic same-value tables for all charts; :100-154 supplies date range, five summary statistics and six charts with demonstration labels.
* C4: src/api/src/zava_forward/api/web/progress.js:156-212 supplies URL filters, page canonicalization, links and unavailable controls; progress.css:1-103 uses shared Fluent-derived tokens and native controls, no new motion.
* C5: src/api/tests/test_progress_dashboard.py:947-966 tests default page boundaries; 41 tests passed on 2026-10-30 (JSON and SQLite), heavy-lock command recorded in changes evidence next phase.
* C6: src/api/checks/progress_browser_check.py:28-304 already starts a constructed-data app and checks six charts against API/table values, history, filters, reflow, reduced motion, field errors and pinned axe.
* C7: src/api/README.md:299-387 documents semantics and local-only evidence boundaries; src/README.md:62-145 defines complete final candidate gate and external receipts.
* W2: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md retrieved in full 2026-10-30; native semantics, form labels, focus, URL state, tables, layout and reduced motion applicable. Repository plain-ASCII/sentence-case standards take precedence over generic punctuation/title-case advice.

## Findings Mapped to Questions

Q1 answered by C2-C4: requested implementation exists. Q2 answered by C5-C6: strengthen exact filtered/custom-limit and rendered boundary evidence, execute caller's full API checks and browser/axe. Q3 answered by W1/C7: deployed-site and direct human acceptance are not locally provable.

## Alternatives and Decision State

Prefer preserving existing behaviour and repairing only verified scope gaps. Rebuilding the dashboard would risk unrelated changes.

## Open Questions, Risks and Residual Uncertainty

Live deployed employee-site verification is excluded by the caller and cannot be inferred from local results.

## Planning Readiness

Ready. Research disposition: executed, complete. Evidence-backed recommendation: preserve production implementation, add tightly scoped paging regressions, document coverage and execute fresh local checks. Self-check: three ordered inline waves complete; citations, alternatives, constraints, uncertainty and handoff recorded.
