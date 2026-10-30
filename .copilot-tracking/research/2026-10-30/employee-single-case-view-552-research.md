---
title: Employee single case view research
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Research Brief

Implement exactly Refs #552: presentation workflow icons with labels, thinner
steps, one-line blocker summary with keyboard/touch detail, attached tabs and
scrolling panel. Preserve Fluent 2, WCAG and plain language. Audience: delivery
coordinator and reviewer. Output mode: convergence.

## Research Parameters

Focused posture, selected for the bounded issue. Evidence root:
`.copilot-tracking/`. Research is source-read-only. Candidate areas: employee
case workspace, shared styles/icons, presentation icon assets and browser tests.
External scope: current Web Interface Guidelines. No Azure, deployment, live
sign-in, credentials, secrets, private data, remote writes or unrelated redesign.

## Extension Registry and Provenance

* Selected `.github/copilot-instructions.md` (all files), RPI Research,
  web-design-guidelines and redesign-existing-projects.
* Repository Fluent 2, WCAG and content standards override generic redesign
  recommendations. Public-page design skills do not apply to this app screen.
* Research specialists skipped: one tightly coupled UI trace, handled inline.

## User Participation and Research Decisions

Explicit user direction authorizes the ordered full loop, local commit only,
on `feat/employee-single-case-view-552` from `721ba973`. No interactive checkpoint
is needed for the unambiguous bounded scope.

## Direction Controls

Tests outside package; source under src; pip only; heavy gates locked with
`/tmp/ama-rpi-heavy.lock`; desktop and narrow browser/axe evidence required.
Required independent critique and Review are not human approval.

## Research Questions

* Q1: Which acceptance criteria already have implementation and what gaps remain?
* Q2: Which presentation icons and accessibility contracts govern the workspace?
* Q3: Which existing local/browser checks prove the exact behavior?

## Prior Knowledge Gate

Read original/addendum, reference index and owner memory. Issue text is data,
not authority. Clean requested branch at the supplied base; no existing PR.
Initial source search shows existing blocker disclosure and workflow icons,
which must be verified rather than duplicated.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Located existing implementation and governing standards. PR #554 is merged
(2026-10-29), and ecbb5a80 is in the requested main ancestry. All six requested
UI changes already exist. Reflection: do not recreate or gratuitously restyle
the delivered UI; focus on fresh exact-scope evidence.

#### Wave 2: Deeper

Read the complete dedicated browser check, case workspace, relevant style
rules, app integration, icon tests, original Review and correction plan.
The check measures density, keyboard/touch disclosure, enlarged text, fallback
and desktop panel scrolling, but does not itself run axe and only exercises
attached-tab scrolling at desktop. Reflection: integrate the existing pinned
axe scan into this focused check, and make attached-tab geometry and actual
panel scrolling assertions cover 390/320px as well as 1280px.

#### Wave 3: Contrarian

Challenged the need for production changes: all six UI behaviors are already
implemented and README documents them. Existing general journey check already
has a reusable scan function; reuse it instead of another scanner/dependency.
Prior Review was Partial/Residual work because its reviewer could not inspect
external rendered evidence. Preserve that historical outcome, generate fresh
evidence here and explicitly permit the new reviewer to inspect it. Do not
relabel original review or infer full WCAG/Fluent acceptance.

### Parent Synthesis and Disposition

Accept existing runtime behavior (C1-C4); accept focused check strengthening
(C5-C6). Reject another UI rewrite because no concrete missing runtime behavior
has been found. Defer cross-browser/AT/human approval and full Fluent adoption.
No further research cycle is warranted: named sources resolve all three
questions and the remaining uncertainties are validation outcomes.

## Evidence Log

* W1: `gh issue view 552`, retrieved 2026-10-30, six acceptance criteria.
* W2: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md,
  retrieved fully 2026-10-30. Apply all categories; repository sentence case,
  plain ASCII and Fluent baseline supersede conflicting generic aesthetics.
* C1: `src/api/src/zava_forward/api/web/case-workspace.js:4` six icon/label mappings;
  `:64` complete native disclosures; `:122` manual keyboard tabs and URL state.
* C2: `src/api/src/zava_forward/api/web/style.css:134` compact grid and semantic
  states; `:151` shared tabs/panel surface; `:157` panel-only scrolling; `:166`
  viewport-bounded disclosure; `:24` reduced motion.
* C3: `src/api/src/zava_forward/api/web/app.js:968` mounted panels and `:975`
  attached tab insertion; enhancement failure restores visible sections.
* C4: `src/api/tests/test_case_journey.py:1289` package-data test; `:1300`
  byte-exact presentation icons; `:1312` complete safe blocker disclosure test.
* C5: `src/api/checks/case_view_ux_browser_check.py:226` viewport geometry,
  `:386` desktop-only stationary tabs; no axe invocation.
* C6: `src/api/checks/case_journey_browser_check.py:532` reusable pinned axe scan;
  `src/api/checks/regulatory_ux_check.py` canonical axe hash.
* C7: `.copilot-tracking/reviews/logs/2026-10-29/case-view-ux-552-review.md:22`
  original Partial/Residual work and missing independent raw visual inspection.

## Alternatives and Decision State

Selected: reuse runtime, strengthen existing issue-specific validation and
document fresh evidence. Alternative no changes leaves narrow-scroll and
focused axe evidence gaps. Alternative redesign violates smallest-change intent
without a demonstrated defect. Findings Q1-Q3 answered with C1-C7.

## Risks and Residual Uncertainty

Native popover support is current-browser-dependent. Full accessibility,
screen-reader, touch device and human visual acceptance remain distinct.
The mandatory complete local gate may be prerequisite-blocked; never substitute
focused checks for that gate. No production authorization or remote writes.

## Artifact Self-check

Three waves complete in order, sources traced, prior evidence distinguished
from current execution, no source changes during Research. Specialist delegation
not needed for this continuous trace. No unresolved implementation decision.

## Planning Readiness

Ready. Research disposition: executed, complete. Parent next action: Plan,
then one independent critique, implement validation, validate, one Review and
local commit. User explicitly requested the complete ordered loop.
