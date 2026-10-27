<!-- markdownlint-disable-file -->
---
title: Resident account control research
ms.date: 2026-10-27
---

## Research Brief

Issue #467, parent #466: place signed-in identity and sign out at the resident
site's top right, matching the employee pattern. Audience: implementer/reviewer.
Output mode: convergence. Posture: focused, selected from the small named scope.
Evidence root: `.copilot-tracking/research/2026-10-27/`.

## Research Parameters and Direction Controls

Preserve sign-in/out and own-case isolation, native keyboard semantics, sensible
focus after logout, narrow widths and existing email disclosure boundaries.
No Azure, private data, secrets, environment files, verifier, MAX_MAPPINGS edits,
force push or merge. Stack on `feat/resident-interactive`, initially identical
to HEAD `55c239d90dabec1e974eb60330e224c3a0fc6190`.
Owner explicitly requests focused validation rather than the complete local gate.

## Extension Registry and Participation

Selected: repository instructions, RPI research, web-design-guidelines (full local
body read; current source fetched), Fluent 2/WCAG/content reference documents.
Public-page redesign skills skipped: bounded authenticated app control, not a
redesign. Research conducted inline; no independent lane warrants delegation.
No intake questions: explicit owner scope and acceptance criteria are sufficient.

## Questions and Candidate Areas

1. What employee header pattern can be reused? Employee web UI.
2. Where does resident identity/logout render and where should focus land?
   Resident demo assets and existing tests.
3. What small regression/browser checks cover isolation and narrow layout?
   Existing API/core tests and component READMEs.

## Research Cycle Log

Cycle 1, all inline, completed in order:

1. Wider: located the employee native details/summary account panel, resident
   bottom-of-page logout, component tokens, existing HTTP and browser harnesses.
   Reflection: reuse the employee disclosure rather than invent a menu widget.
2. Deeper: traced login, session restore, authorised view, logout and focus.
   The view deliberately excluded email; session provides only a boolean.
   Reflection: identity must survive reload without browser persistence and
   must be returned only after the existing own-case authorisation.
3. Contrarian: evaluated client-only email and session-endpoint identity.
   Client-only fails reload/new tabs; session endpoint does not recheck current
   row authority. Existing authorised view is the narrower safe disclosure.
   Existing SQL browser script requires database changes excluded by the owner;
   use the real HTTP app with the existing explicitly synthetic in-memory reader.
   Reflection: no SQL/Azure or core authorisation change is needed.

## Evidence Log

W1: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md,
retrieved 2026-10-27. Native actions, visible focus, long-content containment,
keyboard/touch operation and reduced-motion constraints apply.

C1: `src/api/src/zava_forward/api/web/index.html:15`, `web/style.css:1`
(employee account selectors), `web/app.js:948`: native disclosure, right-aligned
panel, Escape restores summary focus, outside click dismisses.

C2: `src/api/src/zava_forward/api/resident_demo/web/index.html:44`,
`web/demo.js:85`: logout currently rendered below content, hidden on denied/
signed-out states. Existing successful logout announces and focuses sign-in.

C3: `src/api/src/zava_forward/api/resident_demo/app.py:128`: view_for verifies
token and authorises the current own-case row before projection. Add only its
canonical account email here; never accept an identity from URL or client state.

C4: `src/api/tests/test_resident_demo_api.py:164`, `:262`, `:488`:
existing tests cover exact view shape, identity exclusion, case isolation,
revocation, expiry and focus source. Update only intentional own-email disclosure.

C5: `src/api/checks/resident_demo_browser_check.py:77`: existing SQL harness
creates/drops a database; not suitable for this owner's no-SQL scope.
`src/api/tests/test_resident_demo_api.py:47` supplies a synthetic reader suitable
for real loopback app/browser checks without SQL.

## Findings, Alternatives and Decision State

Select native top-right details/summary account with a text "Account" trigger,
synthetic account email and existing Sign out button (C1-C3).
Keep email out of anonymous/session responses; expose only own canonical email
in the authorised view. Render with textContent, clear on hidden/error states.
Rejected: client-only identity (lost reload), unrelated full Fluent framework
adoption, custom ARIA menu/keyboard implementation, SQL/browser infrastructure.
No new animation, photo lookup, storage or account-switch capability.

## Risks and Further Research

Long email and 320px reflow need real browser verification. Automated accessible
name/keyboard checks do not establish assistive-technology or human acceptance.
No further research is required before planning; re-enter only for new evidence
that changes this bounded implementation.

## Planning Readiness

Ready. Research disposition: executed and complete. All three questions answered
by C1-C5/W1; no open design decision. Self-check: genuine inline three-wave
investigation, sources and alternatives recorded; no source edited in research.
