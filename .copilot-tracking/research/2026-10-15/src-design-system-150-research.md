---
title: Issue 150 design system research
ms.date: 2026-10-15
---
<!-- markdownlint-disable-file -->

## Research Brief

Deliver issue #150 design system and accessible workbench component foundations
in `src/api`, reusing migrated code. Audience: implementation and PR reviewers.
Output mode: convergence, preparing planning. Research posture: focused, selected
from the explicit issue, ADR and path constraints.

## Research Parameters and Direction Controls

* Work only on `feat/src-design-system-150` in the issue-150 worktree.
* Owner selected adoption of Fluent UI (Fluent 2), not extension of the MVP.
* No new code in `mvp/`; preserve project dependencies and approval/consent gates.
* No private data, deployment, billable inference or changes to excluded paths.
* Record unsupported acceptance criteria honestly, not as completed evidence.
* Internal candidates: issue, ADR 0006, parity matrix, API web, tests and UX research.
* External candidates: official Fluent 2 guidance and accessibility standards.

## Extension Registry and Provenance

Repository instructions and caller constraints selected as binding boundaries.
RPI phase skills selected for lifecycle evidence; accessibility selected for UI
engineering guidance. Research specialist skipped: the UI trace is tightly coupled
and can be investigated directly. No delegation implied.

## User Participation and Research Decisions

Caller explicitly requested the full Research, Plan, Implement, Review loop and
PR delivery. Continue automatically for this bounded task without routine prompts.
Owner decisions will be verified against the issue, not inferred from memory.

## Research Cycle Log

### Cycle 1: Wider

Verified issue body and all four comments, accepted ADR, parity matrix and merged
moves #296 through #302. All five criteria remain unchecked in GitHub. Existing
PR #241 delivered tokens, state inventory and AI label, but its extend-current-UI
proposal is explicitly superseded. Reflection: preserve the working web and AI
contracts, adopt Fluent 2 foundations rather than revive the rejected decision.

### Cycle 1: Deeper

Traced Overview rendering, Leaflet, tiles, chart alternatives and existing static
tests. Markers are colour-only circles, clusters show only total counts, selected
tiles use border/shadow only. The current token test reads literal colours.
Reflection: use DOM-built Leaflet icons (no interpolated record HTML), shape and
visible text, shared status meanings, selected-filter words, and resolved-token
contrast checks. Preserve text list alternatives and native keyboard semantics.

### Cycle 1: Contrarian

Challenged whether simply renaming the old token palette constitutes adoption:
it does not demonstrate a Fluent component-library rollout. Adopt the official
Fluent 2 global/alias model and dimensions for native component foundations,
explicitly distinguish this from importing React/Web Components, and leave a
packaged Fluent UI runtime migration open rather than mislabel custom CSS as
library delivery. A framework rewrite would enlarge this foundation task and
replace proven auth/AI flows. Forced colours can remove backgrounds, so shapes
need borders and text, not just filled polygons or CSS-generated glyphs.
Reflection: no new owner decision is needed to record the existing adoption
decision; no human or real-service acceptance can be inferred.

### Parent synthesis and cycle re-entry

Accepted: Fluent 2 token foundation, semantic native components, visible map
status and selected-state words. Rejected: retain the superseded extend decision,
add a React build solely to solve shape signals, or claim library conformance.
Deferred: packaged Fluent UI runtime and human accessibility validation.
Another cycle is unnecessary: scoped implementation contracts and limits are
evidenced; deeper unrelated product discovery would not change this slice.

## Evidence Log

| ID | Evidence |
| --- | --- |
| C1 | `src/api/src/zava_forward/api/web/app.js:761` map panel; `:805` count-only clusters; `:811` colour-only circles; `:835` tiles |
| C2 | `src/api/src/zava_forward/api/web/style.css:1` existing tokens and `:153` state components |
| C3 | `src/api/tests/test_design_system.py:15` token/inventory tests and `src/api/tests/test_accessibility_baseline.py:48` contrast checks |
| C4 | `docs/reference/research/ux/design-system.md:19` superseded extend proposal |
| C5 | `docs/adrs/0006-src-layout-and-cutover.md:74` API web placement and `src/README.md:30` dependency rule |
| C6 | `docs/architecture/mvp-to-src-parity-matrix.md:215` migrated web and `:370` remaining #150 gaps |
| C7 | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:469` SA-001 through SA-004 and `src/api/src/zava_forward/api/web/app.js:164` AI review boundary |
| W1 | [Issue #150](https://github.com/jmservera/ama/issues/150), retrieved 2026-10-15; owner adoption comments 6194437555 and 6194477486, migration comment 6196723580 |
| W2 | [Official Fluent 2 tokens](https://fluent2.microsoft.design/design-tokens), retrieved 2026-10-15: global values plus semantic aliases, theming and accessibility |
| W3 | Merged PRs #296-302 metadata, retrieved with `gh pr view` on 2026-10-15: all merged, last at 19:27 UTC |
| W4 | Official microsoft/fluentui token sources at revision 84abdb5fd25a10c627a08465ae82a96e17927270, retrieved 2026-10-15: packages/tokens/src/global/spacings.ts, borderRadius.ts, durations.ts and alias/lightColor.ts; concrete values and official URLs recorded in details/design synthesis |

Official guessed button/spacing URLs returned branded not-found pages; not used
as evidence. WCAG 2.2 skill reference identifies colour, contrast, focus, keyboard
and reflow criteria as engineering checks, not an automated conformance verdict.

## Findings Mapped to Questions and Evidence

Q1 (answered): current owner direction is Fluent 2 adoption (W1), not C4.
Q2 (answered): API package owns web, API tests own UI regressions (C5/C6).
Q3 (answered): map markers, clusters and selected tiles need non-colour cues (C1).
Q4 (answered with limits): native foundations can preserve AI/consent controls
(C7); real AI/SQL/Azure and human accessibility acceptance remain unexecuted.

## Alternatives and Decision State

Fluent 2 is owner-selected. Implement its token model and native foundation
styles now, retaining the existing teal as a documented brand alias, without
claiming to ship the Fluent UI runtime package. This is a partial foundation
slice, not owner approval of a native-only final substitute. Critique PC-001
requires an explicit open adoption-delivery gate; plan/details implement it.

## Open Questions, Risks, and Residual Uncertainty

Full human accessibility acceptance cannot be invented from automated checks.

## Planning Readiness

Ready for the bounded foundation slice. Research disposition: executed, complete.
Self-check: evidence mapped, three ordered waves completed, alternatives and
limitations explicit, excluded paths untouched. Parent action: transition to Plan.
