<!-- markdownlint-disable-file -->
# Task Research: case-view-ux-552

## Research Brief

Date: 2026-10-29. Status: Complete. Researcher: RPI Agent.
Resolve issue #552's compact case workflow, existing icon reuse, accessible
blocker disclosure and attached tab/panel layout for staff. Output mode:
convergence. Audience: implementer and independent reviewer.

## Research Parameters

Focused posture, selected for the bounded owner request. Source scope:
`src/api/src/zava_forward/api/web`; tests outside the package. Evidence root:
`.copilot-tracking/`. External scope: the current Web Interface Guidelines.
No Azure, deployment, push, framework swap or rubric-score editing.
Research writes evidence and required workflow state only.

## Extension Registry and Provenance

* Repository instructions: selected; preserve Fluent tokens, WCAG engineering
  baseline, plain wording and governance/manual paths.
* rpi-research: selected; wider, deeper, contrarian inline investigation.
* web-design-guidelines: selected and source fetched 2026-10-29.
* redesign-existing-projects: selected; targeted density/layout improvements
  only. Fluent typography/palette supersede generic font or palette changes.
* Research specialists: skipped; this is one coupled source trace.

## User Participation and Research Decisions

Owner explicitly requested the complete ordered RPI loop and a local commit,
without push. No additional interaction is needed or available. Track this
as a user-directed full loop, not an inferred automatic-session opt-in.

## Scope and Success Criteria

All six issue criteria require concrete source and desktop/narrow browser
evidence. Local engineering checks do not establish full WCAG conformance,
completed Fluent library adoption, user acceptance or operational approval.

## Direction Controls

Reuse `feat/case-view-ux-552`, initially clean with no open PR. Tests use
`/tmp/mv`; local app uses constructed synthetic data only. Preserve text
labels, status words, keyboard/touch interaction and reduced motion.

## Research Questions

* Q1: Which existing icons can cover all six workflow steps?
* Q2: How can full blocker reasons stay reachable without tall steps?
* Q3: Which container owns tab and panel scrolling today?
* Q4: Which existing tests and local browser harness cover this slice?

## Prior Knowledge Gate

Read both case studies, knowledge index, owner memory, sector primer and
UX design-system/WCAG/content standards. No earlier #552 artifact was found.
Owner memory is context, not evidence.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Initial evidence: native JS/HTML/CSS workspace, six-step journey and existing
manual-activation tabs. `docs/presentations` is absent in this worktree;
inspect existing web assets and presentation source asset references next.
Reflection: avoid new icon dependencies or assumed presentation assets.

#### Wave 2: Deeper

Slide 4 of the tracked capstone deck contains precisely the six requested
workflow icons (C4). Their embedded PNGs can be extracted without redrawing.
Current panels are already mounted once and selected without reconstruction
(C5); move the tablist into that shared workspace, above individually scrolling
panels, rather than introduce new routing or state. Native auto popovers provide
touch/click, keyboard activation, Escape and light dismissal without hover.
Reflection: keep full reason, owner and next action together in the disclosure.

#### Wave 3: Contrarian

Challenged hover-only tooltips (unusable by touch), horizontal tab scroll boxes
(retain reported separation), clipped labels (lose task identity), and hiding
safety warnings (unacceptable). Reject these alternatives. Wrap all tab buttons
with complete labels outside the panel's vertical scrolling area. Keep persistent
safety above the journey. Unknown stages and closed cases must retain existing
status logic, and missing blocker owners/actions must remain explicit.
Reflection: test long/multiple reasons, narrow viewport, native dismissal and
manual tab activation rather than assume the visual change is sufficient.

#### Parent Synthesis and Disposition

Accept exact slide-four icon reuse (C4), native auto popovers (W1), compact
token-based steps and one attached wrapping tab/panel surface (C1/C2/C5).
Reject replacement icon packages and a framework swap: unnecessary dependencies
and owner-selected design conflict. Another cycle is not needed: the bounded
questions have source evidence; rendered behaviour belongs to implementation.

## Evidence Log

* C1: `src/api/src/zava_forward/api/web/case-workspace.js:4` defines six steps;
  line 35 embeds full reasons in status text; line 109 nests tabs in a scroll
  region. Read directly, high confidence.
* C2: `src/api/src/zava_forward/api/web/style.css:145` defines six-column
  stepper; line 156 separates scrolling tabs with bottom margin. High confidence.
* C3: `docs/reference/research/ux/design-system.md:24` explicitly distinguishes
  native Fluent foundations from completed library adoption. High confidence.
* W1: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
  retrieved 2026-10-29: native controls, focus, reduced motion, overflow handling,
  labelled decorative imagery and URL-backed navigation.
* C4: `docs/capstone/deck/zava-forward-cowork-v2-draft.pptx`, slide 4 XML:
  Survey/Evidence/Cost/People/Contractor/Approval icons correspond to media
  image11/image6/image12/image13/image14/image15.png. Inspected ZIP relationships
  and picture descriptions; high confidence. `docs/presentations/` is absent;
  this tracked presentation is the available authoritative asset source.
* C5: `src/api/src/zava_forward/api/web/app.js:945` constructs mounted panels;
  `src/api/checks/design_system_browser_check.py:227` starts an isolated
  synthetic loopback server and cleans up its owned process.
* C6: `src/api/tests/test_case_journey.py:1235` exercises blocker mapping in the
  shipped JS; existing `/tmp/mv` distributions point at a different worktree,
  so validation must explicitly select this worktree's src roots.

## Alternatives and Decision State

Selected approach: exact extracted presentation PNGs plus visible text/status,
native auto popovers for blocker details, token-based compact step spacing,
wrapping tablist attached to a bounded independently scrolling active panel.
No new runtime dependencies. Residual risk: native popover compatibility is
checked in local Chromium only, not a full cross-browser/AT acceptance.

## Planning Readiness

Ready. Research disposition: executed. Q1-Q4 answered by C1-C6/W1.
Self-check: scope/criteria, three ordered waves, evidence, alternatives,
provenance and residual risk recorded. Parent continuation: owner explicitly
requested Plan next; no research-only restriction on the parent workflow.
