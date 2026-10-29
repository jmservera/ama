<!-- markdownlint-disable-file -->

# Task Research: chat-widget-550

| Field | Value |
| --- | --- |
| Date | 2026-10-29 |
| Researcher | RPI Agent, inline |
| Status | In progress |
| Artifact path | .copilot-tracking/research/2026-10-29/chat-widget-550-research.md |

## Research Brief

Converge on one native, Fluent-derived chat widget shared by the resident and
employee sites. Investigate existing API, consent, safety and rendering boundaries
and the unrelated resident-question fallback. Audience: implementer and reviewer.
Scope: src packages, external tests/checks and directly related documentation.
Non-goals: Azure, deployment, paid inference, new chat authority, framework swaps.
Acceptance: issue #550 and the owner's explicit local-validation instructions.

## Research Parameters

Focused posture (bounded caller scope), convergence output, evidence root
`.copilot-tracking/`. Research is read-only except evidence and workflow state.
Questions: shared mounting/rendering; resident question routing; established label
and source patterns; existing regression/browser tools. No invented deadline.

## Extension Registry and Provenance

Repository instructions and RPI research selected. Web guidelines fetched from
their canonical source on 2026-10-29; redesign skill selected only for targeted
existing-app improvements. Fluent 2, WCAG baseline and plain-content standard
override generic visual advice. Public-page design skill skipped (app screens).
Research specialists skipped: one tightly coupled code trace is best inline.

## User Participation and Research Decisions

The user explicitly requests the full ordered loop and commit without push.
Proceed through all four requested phases without routine prompts; do not infer
permission for publication, Azure changes or human approval.

## Direction Controls

Use the clean existing `feat/chat-widget-550` topic, based on merged #503.
Preserve #503/#525/#541 boundaries. Only use synthetic local fixtures.
Do not edit rubric scores; do not push. Required full publication gate applies
before publication, which is not requested.

## Research Questions and Prior Knowledge Gate

Q1: Where can the shared widget mount without changing routing or session scope?
Q2: Why does unrelated resident free text return a home summary?
Q3: What label/source and interaction patterns fit existing contracts?
Q4: Which local checks prove the stated acceptance criteria?

Issue #550 body and comments retrieved: no additional issue comments.
Case study, addendum, reference index, owner memory and UX standards read.
Supplied failure remains a hypothesis until the code trace confirms it.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Completed inline: employee chat.js, resident_demo/web/assistant.js, both entry
pages, static serving, API routing, UX standards and existing browser harnesses.
Reflection: both sites use native DOM and matching Fluent-derived tokens, so a
shared dependency-free factory is sufficient; a framework migration adds risk.

#### Wave 2: Deeper

Confirmed C1: `src/api/src/zava_forward/api/web/chat.js:18` resets the employee
dialog on every opening; line 79 replaces the visible exchange. Resident
`resident_demo/web/assistant.js:326` appends answers below the form inside a
whole-panel scroller. Shared layout and lifecycle can fix both without API changes.
Confirmed C2: `src/api/src/zava_forward/api/resident_demo/chat.py:183` routes any
question containing "home" to the home summary. Thus the rat report matches home.
Safety is already evaluated first and must remain so.
Confirmed C3: `resident_demo/app.py:390` dispatches bounded topics, never raw text
to AI, after explicit record consent. Existing session binding, row recheck and
advisor limits must remain unchanged.
Reflection: restrict free-text home lookup to explicit record/address/improvement
intents; unknown text must receive honest human handoff, not invented diagnosis.

#### Wave 3: Contrarian

Challenged persistence across identity/context changes: retaining employee content
across case navigation risks wrong-context disclosure; retain on close/reopen,
but dispose on route/session/access change. Resident consent withdrawal must
invalidate pending turns and clear text. Do not store resident text in browser
storage or send it to the model. Callback proposals must remain explicit manual
actions, not auto-close chat or silently book.
Rejected a generic LLM free-text proxy: violates the bounded #541 contract.
Rejected duplicated widget implementations: fails shared-component acceptance.
Selected shared UI factory with thin audience adapters and unchanged endpoints.
Cycle re-entry: no; all material questions covered within focused scope.

## Evidence Log

W1: https://github.com/jmservera/ama/issues/550, retrieved 2026-10-29.
W2: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md,
retrieved 2026-10-29, complete.
W3: https://learn.microsoft.com/en-us/microsoftteams/platform/agents-in-teams/integrate-ai/ai-content-labels,
retrieved 2026-10-29, relevant AI label and citations sections read (page tail
truncated, sensitivity-label implementation is not used).
W4: https://www.microsoft.com/en-us/haxtoolkit/guideline/make-clear-why-the-system-did-what-it-did/,
retrieved 2026-10-29, complete. Explanations can increase over-reliance: keep
advisory/verification caveats even with collapsed sources.
C4: `src/api/checks/employee_chat_browser_check.py:28` verifies late-success
fencing, route/session disposal and API denial. Preserve these guarantees.
C5: `.github/workflows/src-ci.yml:82` requires ruff check, format and mypy.
Existing `/tmp/mv` has Python 3.12, pinned ruff and Playwright.

## Findings, Alternatives and Decision State

Q1-Q4 answered by C1-C5 and W1-W4. Implement one shared native factory,
session-local scrolling history, pinned composer, native selector, textarea,
accessible launcher/nonmodal popup, delayed loading, visible errors, disabled
attach/voice reasons, compact truthful labels and native details sources.
Keep existing Fluent tokens/Segoe font and sentence-case ASCII content over
conflicting generic typography/content rules. No unsupported Fluent/WCAG claim.

## Open Questions, Risks and Residual Uncertainty

Human screen-reader/usability acceptance cannot be inferred from local automation.
No live model or live-site acceptance is authorized.

## Planning Readiness

Ready. Research disposition: executed, complete. Evidence IDs and alternatives
checked; parent continues to Plan as explicitly requested.
