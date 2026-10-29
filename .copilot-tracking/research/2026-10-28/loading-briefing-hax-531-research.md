<!-- markdownlint-disable-file -->
---
title: Loading and briefing research for issue 531
description: Focused evidence for employee loading feedback and HAX briefing
ms.date: 2026-10-28
---

## Research brief

Deliver issue #531 and its latest owner comment on the existing native employee
workspace. Audience: implementer and independent reviewer. Output: convergence
for planning. Focused posture follows the explicit bounded request. No framework
swap, Azure, secrets, private data, live deployment or approval-boundary change.
Canonical evidence root: `.copilot-tracking/research/2026-10-28/`.

## Direction controls and participation

The user explicitly requests the full research, plan, implement, review loop,
dated committed evidence and a stacked PR targeting `feat/case-journey-ux-526`.
Use `Refs #531`, never closure wording. Noninteractive execution needs no
ordinary phase confirmation. Publication must not bypass the complete gate.
The branch is clean and its HEAD matches the unmerged parent branch.

## Extension registry

Selected: repository instructions; rpi-research, web-design-guidelines,
redesign-existing-projects. Preserve Fluent 2 tokens and existing typography
over generic redesign advice. Native semantic controls, plain ASCII content,
human approval and manual paths override conflicting generic styling advice.
The issue requests the UX agent for the design note; delegate that bounded
independent synthesis, not the implementation trace.

## Questions and candidate areas

1. Where can feedback render before scripts and during all employee actions?
2. How do briefing output, sources and draft feedback preserve server authority?
3. Which existing synthetic browser and axe checks cover the change?

Internal candidates: `src/api` web assets, tests/checks and component guides;
the four requested UX references. External candidates: HAX Library, Fluent
React Storybook and current Web Interface Guidelines.

## Research cycle log

Cycle 1, Wider: issue and latest comment inspected; requested UX baseline and
external pattern entrypoints retrieved. HAX and Storybook are client-rendered
shells, so deeper evidence must inspect their backing documents or browser.
Reflection: no React migration is needed or authorized; clarify draft review,
not "approval" of works.

Cycle 1, Deeper: traced the shared `h` event factory, independent briefing
loader, existing script retry budget, aiNotes and server review contracts.
Reflection: the shared factory can wire native async controls without dozens
of inconsistent wrappers. Existing manually managed disabled states must win
over helper cleanup. Direct listeners and fire-and-forget redraws need explicit
integration. Briefing citations are flattened after server validation; the raw
text is not available in the browser, so statement attribution must be retained
at the server boundary, not inferred from proximity.

Cycle 1, Contrarian: inspected server review and source verification. Review
is irreversible audit evidence, so undo must apply only to local dismissal or
unsaved edits, never erase a recorded review. Rules output must not inherit
the AI label. HAX G11 warns that explanations can increase misplaced trust;
show limitations and unresolved sources rather than claiming accuracy.
Reject alternatives: React migration (unauthorized), guessing statement
sources (misleading), auto-retry writes (duplicate mutations), making reason
optional (changes server boundary). One focused cycle covers the questions.

## Evidence log

* W1: https://github.com/jmservera/ama/issues/531 and latest comment, retrieved
  2026-10-28. Immediate action feedback, spinner at 200ms, scoped text entry.
* W2: https://www.microsoft.com/en-us/haxtoolkit/library/, retrieved 2026-10-28.
  Library advertises 18 human-AI guidelines; shell alone does not expose details.
* W3: https://storybooks.fluentui.dev/react/, retrieved 2026-10-28. Fluent v9
  Storybook entrypoint, pattern reference only.
* W4: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md,
  retrieved 2026-10-28. Semantic controls, polite announcements, inline errors,
  reduced motion and responsive content; repository content rules take precedence.
* W5: https://www.microsoft.com/en-us/haxtoolkit/guideline/make-clear-why-the-system-did-what-it-did/,
  retrieved 2026-10-28. G11 local/global explanations, output properties and
  input mapping; explanations are not evidence of correctness.
* W6: https://www.microsoft.com/en-us/haxtoolkit/guideline/support-efficient-correction/
  and https://www.microsoft.com/en-us/haxtoolkit/guideline/support-efficient-dismissal/,
  retrieved 2026-10-28. G9 editable output and G8 easy dismissal.
* W7: Fluent Storybook `index.json` and upstream
  https://raw.githubusercontent.com/microsoft/fluentui/master/packages/react-components/react-spinner/stories/src/Spinner/SpinnerBestPractices.md,
  retrieved 2026-10-28. Descriptive progress text, spinner only for non-immediate
  tasks, reduced-motion description. Storybook shell is not a rendered review.
* C1: `src/api/src/zava_forward/api/web/index.html:32` empty shell/main before
  blocking scripts. Static text plus an early independent watchdog is needed.
* C2: `src/api/src/zava_forward/api/web/app.js:15` central native event factory;
  `app.js:144` bounded retry; `app.js:314` shared aiNotes; `app.js:391`
  briefing; `app.js:1252` direct import listener; `app.js:1270` sign-out.
* C3: `src/core/src/zava_forward/core/ai_tasks.py:111` strips citation marks;
  `ai_tasks.py:198` output and comparison recording; `ai_tasks.py:271` enforces
  reason and immutable one-time review/source recheck.
* C4: `src/api/checks/employee_briefing_browser_check.py:24` role/scope loop;
  `checks/workspace_scripts_browser_check.py:61` real script failure checks;
  `checks/case_journey_browser_check.py:1` pinned axe/retained drafts.

## Design note and participation result

The requested UX agent was invoked once with the exact bounded note assignment.
It returned intake questions instead of a note. No user research is available;
this is stakeholder feedback, not validated usability. Parent continues the
bounded design note from verified HAX evidence, without inventing interviews
or re-dispatching the same objective.

G1/G2: label source type and limitations. G7: explicit rules/AI mode selection.
G8: local Hide briefing with Show briefing undo; case work stays available.
G9: choose edit or reject, reveal only relevant large text areas, require reason,
allow cancel before submission. G11: explain fixed ranking/input scope, show
per-statement declared references with actual case links and refresh timestamp.
G15: record draft feedback visibly with immutable audit semantics.
Native button + labelled text spinner follows Fluent's reference, with a static
icon and text under reduced motion. Do not equate references with truth.

## Current decisions

Retain native stack, Fluent tokens, optional AI and human authority.

## Planning readiness

Ready. Research disposition: executed, complete. Evidence C1-C4 and W1-W7
answers all three questions. No required design decision remains unknown;
human usability, screen reader/voice and live-site checks remain separate.
