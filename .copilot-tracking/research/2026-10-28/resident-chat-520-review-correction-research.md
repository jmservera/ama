---
title: Resident chat review correction research
ms.date: 2026-10-28
---
<!-- markdownlint-disable-file -->

# Task Research: resident-chat-520-review-correction

## Research Brief

Date: 2026-10-28. Researcher: RPI parent, inline. Status: Complete.
Research disposition: executed. Output mode: convergence, preparing planning.
Evidence root: `.copilot-tracking/`.

Research the five supplied PR #525 review findings, their shared session and
async UI boundaries, and existing HTTP/browser/axe verification. Audience:
implementer and independent reviewer. Success means server-bound permission,
cross-tab clearing, punctuation-safe periods and correct asynchronous focus/input.
Non-goals: Azure, secrets, .env, private datasets, real AI, visual redesign,
earlier evidence rewrites, PR body changes or merging.

## Research Parameters and Direction Controls

Focused posture, selected by bounded caller scope and named source targets.
Internal candidates: resident_demo app/chat/web, owning tests and browser check.
External candidates: five GraphQL review threads and current web guidelines.
No-interaction rationale: caller explicitly requests all four phases and publication.
Heavy admission: nonblocking lock, retry every 60 seconds for at most 40 minutes,
explicitly superseding prior nonqueued-only advice for this cycle.
Ruff limit: 100. Normal topic push only, after exact-head full local gate.

## Extension Registry and Provenance

* Repository instructions: selected; synthetic-only evidence, Fluent/plain language,
  source commands, retained original artifacts and full publication gate.
* RPI research: selected; Wider, Deeper, Contrarian evidence then readiness.
* web-design-guidelines: selected and current source retrieved 2026-10-28.
* Design/redesign skills: skipped; behavioral corrections, no aesthetic redesign.
* Research specialist: skipped; one tightly coupled code trace is handled inline.

## Research Questions and Prior Knowledge Gate

Q1: Where can shared cookie identity diverge from tab permission and display?
Q2: How do tokenization, loading/error focus and async drafts/handoffs interact?
Q3: Which existing browser/axe and publication commands verify the exact behavior?

Read original/addendum, reference index/memory, sector primer, source gate and
earlier documents RV-001 evidence. Earlier failed/blocked gates remain adverse
historical evidence, not current success. Fetch/rebase completed at 685547ed,
clean matching open PR branch. All five supplied thread bodies read via GraphQL;
all unresolved. No secrets or private datasets read.

## Research Cycle Log

### Cycle 1: Wider

Read app.py, demo.js, assistant.js, chat.py, HTTP fixtures and source gate.
Reflection: shared valid CSRF is not identity binding; browser state and both
callback/chat permission need a per-login identity independent of resident ID.
SessionCodec already returns a random opaque per-login session id.

### Cycle 1: Deeper

Existing resident_assistant_browser_check uses actual loopback HTTP, shared
constructed fixtures, route.fetch/fulfill to hold replies and pinned axe scan.
Client fixture can retain tab-local sid independent of its cookie dictionary.
The existing codec verifies and returns sid, so no codec change is necessary.
Reflection: bind protected requests using a header (not body field/case selector),
include view loads to avoid rendering a switched identity during login, and
clear entire page plus controllers on cross-tab changes.

### Cycle 1: Contrarian

Broadcast alone cannot close the cookie-change/message-delivery race and cannot
protect a suspended tab. Require server sid/header match and response-generation
fences as well as BroadcastChannel clearing. Shared CSRF must remain valid for
pre-opened sign-in tabs. Do not rotate CSRF as a substitute for identity binding.
Old same-resident login permission is stale too: sid is per login, not resident.
Closing chat should not cancel accepted work or suppress a useful answer, only
its automatic focus/search handoff. Typed-ahead drafts must survive both success
and failures; compare original untrimmed value if clearing after success.
Manual route must choose visible heading, email or retry, otherwise launcher.
Reflection: alternatives rejected on concrete races, not aesthetic preference.

### Parent Synthesis and Disposition

Accepted C1-C5: reuse opaque verified sid in session/login responses, protected
headers and tab-local permission; cross-tab change clears stale personal state.
Accepted C7: extend existing browser harness rather than introduce new tooling.
Rejected notification-only and CSRF-rotation-only solutions. Deferred human/AT
acceptance: existing engineering harness does not establish conformance.
No further cycle required: all five questions traced to existing contracts and
tests; no unresolved design uncertainty changes the bounded implementation.

## Evidence Log

| ID | Claim | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Cookie validation lacks tab session binding | src/api/src/zava_forward/api/resident_demo/app.py:330 | High |
| C2 | Existing codec exposes opaque random login sid after verification | src/core/src/zava_forward/core/resident_showcase.py:417 | High |
| C3 | Permission/generation persist on cookie replacement | src/api/src/zava_forward/api/resident_demo/web/assistant.js:310 | High |
| C4 | View load and login share no tab identity fence | src/api/src/zava_forward/api/resident_demo/web/demo.js:288 | High |
| C5 | Routing uses word tokens, period uses whitespace | src/api/src/zava_forward/api/resident_demo/chat.py:40; src/api/src/zava_forward/api/resident_demo/app.py:407 | High |
| C6 | Original complete gate had a corrected fixture failure, then lock blocker | .copilot-tracking/changes/2026-10-28/resident-chat-documents-520-rv001-changes.md:84 | High |
| C7 | Actual browser harness already holds delayed replies and scans pinned axe | src/api/checks/resident_assistant_browser_check.py:132 | High |
| W1 | Five requested defects, exact thread IDs retained in task state | https://github.com/jmservera/ama/pull/525 | High |
| W2 | Current web interface rules, fetched 2026-10-28 | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md | High |

## Alternatives and Decision State

Prefer reuse of verified random sid to adding another credential or exposing cookie.
Notifications alone are insufficient: requests must reject stale sid server-side.
Preserve manual and assisted routes, native controls and bounded workflow authority.

## Planning Readiness

Ready. Q1 answered by C1-C4; Q2 by C3/C5/C7; Q3 by C6/C7 and
src/README.md local gate. Findings high confidence from source, not a preclaimed
test pass. Self-check: boundaries, alternatives, all three waves and source
identities recorded. Required heavy gates remain unrun this cycle.
