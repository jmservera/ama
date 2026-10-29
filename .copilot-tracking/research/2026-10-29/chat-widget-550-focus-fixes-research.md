<!-- markdownlint-disable-file -->
# Task Research: chat-widget-550-focus-fixes

## Research Brief

Selected follow-up to task 550, 2026-10-29. Fix RV-001 external focus
obscuration and RV-002 asynchronous employee focus theft. Focused, convergence,
inline research for implementer/reviewer. Scope: shared widget, employee adapter,
related unittest/browser checks and documentation. No Azure, push, rubric edits,
modal trap, backend authority change or unrelated redesign.

## Parameters, Extensions and Participation

Owner explicitly requests Research/Plan/Implement/Review and a local commit;
no routine phase prompts required, manual mode retained. Existing original RPI
evidence is prior knowledge, not a closure claim. Repository/Fluent/WCAG/plain
content requirements and freshly retrieved web guidelines apply. Public-page
and redesign skills skipped: bounded interaction defect, no visual redesign.
Research specialists skipped: one tightly coupled source trace, handled inline.

## Questions and Initial State

Q1: How can external focus remain unobscured without cancelling retained work?
Q2: Which async paths move focus and how can incoming replies stay polite only?
Q3: Which regression/browser oracles prove focus ownership and retention?

Original Review supplies concrete reproductions. Clean existing branch verified;
no PR found. Start with shared widget, employee/resident adapters and existing
shared real-app browser harness. Research disposition and readiness pending.

## Completed Focused Cycle

Wider: C1, `src/api/src/zava_forward/api/web/chat-widget.js:100` installs only
root key handling, with no external-focus dismissal. C2,
`src/api/src/zava_forward/api/web/chat.js:116,138` calls focusInput after
asynchronous send cleanup and initialization. Resident replies already append
to the shared polite log without focusing. Existing hide retains pending work.
Reflection: shared focus dismissal plus removal of async focus is sufficient;
no CSS measurement, modal conversion or backend change is needed.

Deeper: C3, `src/api/checks/chat_widget_browser_check.py:121` checks only whether
Tab exits, not visibility. `:190` exercises obsolete operations but not current
visible-background work. C4, `src/api/tests/test_workspace_scripts.py:11` provides
Node VM unit-test prior art; use a minimal DOM harness to execute actual shared
factory and employee adapter, including disposal listener cleanup.
Reflection: test pending setup, success/error, deliberately chosen internal
controls, external textarea, and visible launcher focus separately.

Contrarian: hiding every outside focus event except the launcher preserves
nonmodal navigation, retains draft/thread/pending work and avoids measuring
overlap. Launcher is outside the popup but cannot be obscured by it; keeping
the popup visible there provides an independent no-theft completion oracle
which hiding alone cannot accidentally satisfy. Reject guarded async refocus:
even internal focus may have moved deliberately (for example to Sources).
Keep focus changes only in explicit open/close/submit actions. Access-loss
focus routing remains the existing independent lifecycle boundary, not a reply
refocus; ensure outside focus is not stolen there either.

## External Evidence

W1: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md,
retrieved in full 2026-10-29: overlays must not cover focus; async updates polite.
W2: https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html,
retrieved 2026-10-29, relevant criterion/intent read (later examples truncated).
SC 2.4.11 requires the focused component not be entirely hidden; it explicitly
discusses nonmodal dialogs and closing on focus loss. No conformance claim.

## Synthesis and Planning Readiness

Q1-Q3 answered by C1-C4/W1-W2 and original RV reproductions. Selected:
document focusin listener hides without refocusing/cancelling for outside
targets except launcher; remove listener on dispose. Remove employee async
focusInput calls, retain explicit submit validation and open/close focus.
Keep existing polite log/status; protect external focus on access loss.
Add behavioral Node unittest and real-app keyboard/controlled promise coverage.
One completed three-wave inline cycle; no unresolved material uncertainty and
no broader discovery needed. Research disposition: executed. Readiness: Ready.
Human assistive-technology and publication gates remain out of scope.
