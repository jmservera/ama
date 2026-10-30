---
title: Case journey UX 526 research
description: Focused evidence and readiness for the employee case workspace
ms.date: 2026-10-28
---

## Brief and controls

Implement issue #526 using the supplied employee-case-workspace-redesign.md
specification. Audience: employees using the synthetic case demonstrator.
Output mode: convergence. Posture: focused, selected for a bounded code change.
No Azure, secrets, private data, framework swap or new AI authority.
The user explicitly requests the full ordered RPI loop and topic PR.
The existing branch is feat/case-journey-ux-526 with no open PR; the only dirty
input is the owner-supplied specification, explicitly authorized for inclusion.

## Extension registry and participation

* Repository instructions: selected, including src paths, local publication gate,
  privacy-safe Git identity and immutable original evidence.
* rpi-research: selected; all three waves inline because this is one coupled trace.
* redesign-existing-projects: selected; existing Fluent tokens/stack take precedence
  over its generic font, colour and animation recommendations.
* web-design-guidelines: selected; source retrieved 2026-10-28. Project sentence
  case and ASCII standard take precedence over generic title-case/Unicode advice.
* Design system, WCAG baseline and content standard: selected scoped constraints.
* Specialists: skipped for research; no independent uncertainty warrants dispatch.

## Questions

1. Which existing panels and handlers must remain reachable exactly once?
2. Which payload fields support journey, summary and AI state without API expansion?
3. How can tabs preserve drafts, route history and role/refusal behaviour?
4. Which synthetic browser/axe and publication gates cover the exact requirement?

## Cycle 1

### Wider

Intake verified with gh issue view 526. Read the original case study, addendum,
knowledge-base index and owner memory. The supplied specification fixes six
slide-order journey steps and nine tab destinations; human/resident decisions
remain authoritative. Existing stack is native JavaScript/CSS, not a framework.
Inspecting the case render, assistant cards, drafts and existing local checks.

### Deeper

The case is built by one caseView call. Panels can be constructed once into
nine named containers without replacing their handlers. Same-case tab changes
must bypass route() (which otherwise aborts requests, rebuilds panels and asks
to discard dirty forms). Other route/query changes retain the existing guard.
The challenge draft preservation deliberately retains live form nodes and
closures. Extend it for dirty field values on same-case refresh, without
reintroducing values from completed actions.

The case payload already contains funding.status, decision.status, returns,
work.blockers, work.overdue, work.evidence_freshness and work.handoff. No
server journey/confidence field is needed. Assistant status arrives separately
and must update summary/counts without delaying case controls. Its existing
hash equality check must compare case identity rather than tab query.

### Contrarian

Positional completion alone is incorrect for Funding and Resident agreement:
keep explicit confirmation checks. A closed case overrides blocker styling.
An unknown stage must not fabricate a current step. Safety cannot be hidden
inside a tab: move the single live safety panel above the stepper while open,
and keep a link in Blockers rather than duplicate its controls.

Chat answers have no existing recorded-review identifier or review endpoint.
Their existing boundary is informational answer plus a separately requested
assistant proposal. Do not invent a confidence score, fake local audit or
approve a chat turn. Use the same warning/source/confidence presentation and
make the existing proposal-review path explicit. This payload gap is flagged
for Review; recorded draft/proposal reviews continue through existing endpoints.

Existing browser checks assume all panels are visible. Update only their
navigation selectors where tabs intentionally change visibility; preserve all
behavioural assertions. Baseline unit command failed because distributions
were not installed (53 import errors); install existing declared extras in a
local venv, not PYTHONPATH source workarounds. The full gate is mandatory for
publication and owns its internal lock; acquire the same lock nonblocking in
60-second retries up to 40 minutes before invocation, without double locking.

## Evidence

* C1: docs/reference/research/ux/employee-case-workspace-redesign.md:1 - supplied design.
* C2: docs/reference/research/ux/design-system.md:17 - Fluent 2 selected; no swap.
* C3: docs/reference/research/ux/content-standard.md:25 - people decide, AI is not approval.
* W1: https://github.com/jmservera/ama/issues/526 - retrieved 2026-10-28;
  owner requires slide order and evidence-based completion.
* W2: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
  - retrieved 2026-10-28; semantics, focus, URL state, reduced motion and error rules.
* C4: src/api/src/zava_forward/api/web/app.js:467 - existing case panels/refresh.
* C5: src/api/src/zava_forward/api/web/app.js:171 - route abort and unsaved guard.
* C6: src/core/src/zava_forward/core/store.py:361 - payload preserves returns/funding.
* C7: src/core/src/zava_forward/core/taskqueues.py:229 - funding/resident blockers.
* C8: src/api/src/zava_forward/api/web/panels.js:239 - retained challenge form nodes.
* C9: src/api/src/zava_forward/api/web/assistants.js:64 - asynchronous registry/queue.
* C10: src/api/src/zava_forward/api/web/chat.js:48 - answers and separate proposals.
* C11: src/README.md:55 - complete local RPI gate and external exact-head receipt.

## Decisions and alternatives

Keep nine specified tabs initially. Do not add journey/confidence API fields
unless existing payload evidence proves them necessary; missing confidence
must say "not provided", never inferred from sources.

## Readiness and disposition

Research disposition: executed. Planning Readiness: Ready.
Selected approach: client derivation and retained native DOM panels, using
existing review APIs. Rejected: framework replacement, optional server journey
or confidence fields, position-only evidence and rebuilding on tab switches.
One completed wider/deeper/contrarian cycle covers the bounded change.
No further research cycle is warranted. Chat recorded-review gap is explicit,
not silently represented as delivered. Real staff, screen-reader and live
deployment acceptance remain owner work.
